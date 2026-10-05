"""brethof-llms-txt — write and keep an llms.txt for a repository.

  brethof-llms-txt generate [PATH] [--out llms.txt] [--state FILE] [model options]
  brethof-llms-txt check FILE [--links]

Model options (all optional; without them descriptions come from the pages themselves):
  --api-base URL     OpenAI-compatible endpoint (…/v1), or an Ollama host with --backend ollama
  --model NAME       model name at that endpoint
  --api-key KEY      or env LLMS_TXT_API_KEY
  --backend B        openai (default) or ollama
  --think T          openai: "off" disables thinking on Qwen-style models; ollama: low/high/false
  --workers N        parallel model requests (default 4)
Environment: LLMS_TXT_API_BASE, LLMS_TXT_MODEL, LLMS_TXT_API_KEY, LLMS_TXT_BACKEND, LLMS_TXT_THINK.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import __version__
from .build import generate
from .collect import collect
from .describe import Model, ModelUnavailable
from .validate import check, links


def _model(a) -> Model | None:
    base = a.api_base or os.environ.get("LLMS_TXT_API_BASE", "")
    name = a.model or os.environ.get("LLMS_TXT_MODEL", "")
    if a.no_ai or not (base and name):
        return None
    return Model(base=base, model=name, key=a.api_key or os.environ.get("LLMS_TXT_API_KEY", ""),
                 backend=a.backend or os.environ.get("LLMS_TXT_BACKEND", "openai"),
                 think=a.think or os.environ.get("LLMS_TXT_THINK", ""), workers=a.workers)


_last_model: Model | None = None


def cmd_generate(a) -> int:
    root = Path(a.path)
    repo = collect(root, owner=a.owner or "", name=a.name or "", branch=a.branch or "")
    state = Path(a.state) if a.state else None
    cache = json.loads(state.read_text()) if state and state.is_file() else {}
    global _last_model
    _last_model = _model(a)
    try:
        text, new_cache = generate(repo, _last_model, cache)
    except ModelUnavailable as e:
        print(f"the model did not answer, nothing written: {e}", file=sys.stderr)
        return 2
    errors, warnings = check(text)
    out = Path(a.out) if Path(a.out).is_absolute() else root / a.out
    old = out.read_text(encoding="utf-8") if out.is_file() else None
    if a.stdout:
        sys.stdout.write(text)
    elif old != text:
        out.write_text(text, encoding="utf-8")
    if state:
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text(json.dumps(new_cache, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
    links_n = text.count("\n- [")
    m = _last_model
    if m and m.usage["calls"]:
        u = m.usage
        print(f"model {m.model}: {u['calls']} calls, {u['in']} tokens in, {u['out']} tokens out, "
              f"{u['seconds']:.1f} s", file=sys.stderr)
    print(f"{'unchanged' if old == text else 'wrote'} {out.name}: {links_n} links, "
          f"{len(errors)} errors, {len(warnings)} warnings", file=sys.stderr)
    for e in errors:
        print("  error:", e, file=sys.stderr)
    return 1 if errors else 0


def cmd_check(a) -> int:
    text = Path(a.file).read_text(encoding="utf-8")
    errors, warnings = check(text)
    for e in errors:
        print("error:", e)
    for w in warnings:
        print("warning:", w)
    dead = links(text) if a.links else []
    for url, problem in dead:
        print(f"dead link ({problem}): {url}")
    print(f"{a.file}: {len(errors)} errors, {len(warnings)} warnings"
          + (f", {len(dead)} dead links" if a.links else ""))
    return 1 if errors or dead else 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="brethof-llms-txt", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate", help="write llms.txt for a repository checkout")
    g.add_argument("path", nargs="?", default=".")
    g.add_argument("--out", default="llms.txt")
    g.add_argument("--state", help="JSON file that keeps descriptions between runs")
    g.add_argument("--stdout", action="store_true", help="print instead of writing the file")
    g.add_argument("--owner"); g.add_argument("--name"); g.add_argument("--branch")
    g.add_argument("--api-base"); g.add_argument("--model"); g.add_argument("--api-key")
    g.add_argument("--backend"); g.add_argument("--think")
    g.add_argument("--workers", type=int, default=4)
    g.add_argument("--no-ai", action="store_true", help="never call a model")
    g.set_defaults(func=cmd_generate)
    c = sub.add_parser("check", help="check an llms.txt against the format")
    c.add_argument("file")
    c.add_argument("--links", action="store_true", help="also check that every link answers 200")
    c.set_defaults(func=cmd_check)
    a = p.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main())
