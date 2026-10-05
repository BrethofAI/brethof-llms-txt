"""Assemble llms.txt from a collected repo: the structure is decided here, by rules, never by the model."""
from __future__ import annotations

import hashlib
import re
from urllib.parse import quote

from .collect import Page, Repo, ordered
from .describe import Model, describe, summarize

MAX_LINKS = 80
MAX_SECTIONS = 12
# folders written for the project's own developers: kept, but under Optional
INTERNAL = {"decisions", "adr", "adrs", "design", "designs", "spec", "specs", "rfc", "rfcs", "proposals",
            "internal", "legal", "meetings", "meeting-notes", "roadmap", "archive", "maintainers"}


def link(repo: Repo, path: str) -> str:
    style = repo.config.get("links", "raw")
    if repo.config.get("base_url"):
        return repo.config["base_url"].rstrip("/") + "/" + quote(path)
    if not repo.owner:
        return path
    if style == "blob":
        return f"https://github.com/{repo.owner}/{repo.name}/blob/{repo.branch}/{quote(path)}"
    # raw markdown: what an assistant can read directly, no HTML around it
    return f"https://raw.githubusercontent.com/{repo.owner}/{repo.name}/{repo.branch}/{quote(path)}"


def _section_name(key: str) -> str:
    words = re.sub(r"[-_]+", " ", key).strip()
    if words.lower() in ("api", "cli", "faq", "sdk", "gpu", "ui"):
        return words.upper()
    return words[:1].upper() + words[1:]


def _folder_index(pages: list[Page]) -> Page:
    """The page that stands for a whole folder: its index/README, else its first page."""
    for p in pages:
        if re.search(r"(^|/)(index|README|readme|overview|introduction)\.\w+$", p.path) \
                and p.path.count("/") == min(x.path.count("/") for x in pages):
            return p
    return pages[0]


def plan(repo: Repo, max_links: int = MAX_LINKS) -> tuple[list[tuple[str, list[Page]]], list[Page]]:
    """Sections and their pages, plus the Optional pages.

    Small docs trees get one section per top-level docs folder. A tree too big for that
    (the Linux kernel has ~100 folders and thousands of pages) is folded: each folder becomes
    one link to its index page, in the project's own navigation order, and what does not fit
    goes to Optional.
    """
    pages = ordered(repo.pages)
    groups: dict[str, list[Page]] = {}
    for p in pages:
        groups.setdefault(p.group, []).append(p)
    group_order = sorted(groups, key=lambda g: (g != "", min(p.order for p in groups[g]),
                                                min(p.path for p in groups[g])))
    readme = [repo.readme] if repo.readme else []
    if repo.readme and repo.readme.title.lower() != repo.title.lower():
        repo.readme.title = f"{repo.title} README"      # not "What is FastEmbed?"
    optional = list(repo.secondary)
    sections: list[tuple[str, list[Page]]] = []

    internal = [g for g in group_order if g.lower() in INTERNAL]
    folders = [g for g in group_order if g and g not in internal]
    folded = len(folders) > MAX_SECTIONS
    if not folded:
        # one section per docs folder; a big tree keeps each folder's first pages in the
        # project's own order, so every part of the docs is reachable and the file stays short
        cap = max(4, max_links // max(1, len(folders) + 1)) if len(pages) > max_links else 10**6
        sections.append(("Docs", readme + groups.get("", [])[:cap]))
        for g in folders:
            sections.append((_section_name(g), groups[g][:cap]))
        for g in internal:
            optional += groups[g][:5]
    else:
        top = readme + groups.get("", [])[:max(8, max_links // 8)]
        stand_ins = [_folder_index(groups[g]) for g in folders]
        # folders the project's own navigation names come first; the rest are optional
        named = [p for p in stand_ins if p.order < 10**6]
        rest = [p for p in stand_ins if p.order >= 10**6]
        room = max(0, max_links - len(top))
        sections.append(("Docs", top))
        if named[:room]:
            sections.append(("Guides", named[:room]))
        optional += named[room:] + rest
        optional = optional[:max_links]
        for p in stand_ins:          # a folder link is titled by its folder when its index is generic
            if p.title.lower() in ("index", "readme", "introduction", "overview", "contents"):
                p.title = _section_name(p.path.rsplit("/", 2)[-2])

    if repo.examples:
        ex = ordered(repo.examples)
        if len(ex) > 20:
            ex = [p for p in ex if re.search(r"(^|/)(README|index)\.\w+$", p.path)][:20] or ex[:20]
        sections.append(("Examples", ex))
    sections = [(n, ps) for n, ps in sections if ps]
    return sections, optional


def generate(repo: Repo, model: Model | None, cache: dict | None = None,
             max_links: int = MAX_LINKS, known_only: bool = False) -> tuple[str, dict]:
    """Return the llms.txt text and the new cache (descriptions keyed by page sha).

    known_only: the no-model repair the App makes between weekly passes. Pages already in the
    file keep their description (a moved page follows its content), deleted pages drop out,
    and NEW pages wait for the next pass with a model. A page whose content changed keeps its
    old description and its old sha, so the next pass still sees the change."""
    cache = dict(cache or {})
    sections, optional = plan(repo, repo.config.get("max_links", max_links))
    if known_only:
        known_sha = {v.get("sha") for k, v in cache.items() if not k.startswith("_") and isinstance(v, dict)}
        keep = lambda p: p.path in cache or p.sha in known_sha
        sections = [(n, [p for p in ps if keep(p)]) for n, ps in sections]
        sections = [(n, ps) for n, ps in sections if ps]
        optional = [p for p in optional if keep(p)]
    every = [p for _, ps in sections for p in ps] + optional

    # summary: reused while the README and package description are unchanged
    skey = hashlib.sha1(((repo.readme.sha if repo.readme else "") + repo.package_description
                         + repo.title).encode()).hexdigest()[:12]
    hit = cache.get("_summary", {})
    if repo.config.get("summary"):
        summary, details = repo.config["summary"], repo.config.get("details", "")
    elif hit.get("sha") == skey or (known_only and hit):
        summary, details = hit.get("summary", ""), hit.get("details", "")
        skey = hit.get("sha", skey)
    else:
        summary, details = summarize(repo, model)
    if known_only:
        stale = {p.path: cache[p.path] for p in every if p.path in cache and cache[p.path].get("sha") != p.sha}
        descs = describe(repo, [p for p in every if p.path not in stale], None, cache)
        descs.update({path: v.get("desc", "") for path, v in stale.items()})
    else:
        descs = describe(repo, every, model, cache)

    new_cache = {"_summary": {"sha": skey, "summary": summary, "details": details}}
    for p in every:
        old = cache.get(p.path) if known_only else None
        new_cache[p.path] = {"sha": old["sha"] if old and old.get("sha") != p.sha else p.sha,
                             "desc": descs.get(p.path, "")}

    out = [f"# {repo.title}", ""]
    if summary:
        out += [f"> {summary}", ""]
    if details:
        out += [details, ""]
    seen = set()
    for name, ps in sections + ([("Optional", optional)] if optional else []):
        lines = []
        for p in ps:
            if p.path in seen:
                continue
            seen.add(p.path)
            title = p.title.replace("[", "(").replace("]", ")")
            d = descs.get(p.path, "")
            lines.append(f"- [{title}]({link(repo, p.path)})" + (f": {d}" if d else ""))
        if lines:
            out += [f"## {name}", ""] + lines + [""]
    return "\n".join(out).rstrip() + "\n", new_cache
