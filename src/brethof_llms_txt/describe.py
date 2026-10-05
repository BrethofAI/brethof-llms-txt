"""The writing: a one-line summary of the project and one line per linked page.

A model writes them when one is configured; otherwise they are taken from the page itself
(its front-matter description or its first sentence). Either way a page whose content has
not changed keeps the description it already had, so a rerun on an unchanged repo makes no
model calls and produces the same file byte for byte.
"""
from __future__ import annotations

import json
import http.client
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from .collect import Page, Repo

SUMMARY_PROMPT = """You write the opening of an llms.txt file: the short guide that tells an AI \
assistant what a software project is and where its documentation lives.

Project: {name}
{package}
README (start):
<<<
{readme}
>>>

Reply with JSON only: {{"summary": "...", "details": "..."}}
- summary: ONE sentence, at most 30 words, saying what the project is and what it does. Start with \
the thing itself ("A ...", "Python library ...", "Desktop app ..."), not with the project name.
- details: two or three short sentences of the facts an assistant most needs to use it well: \
language or platform, how it is installed or run, the main parts. Empty string if the README does \
not say.
If the repository holds documentation (a wiki or a docs site), say what that documentation covers.
Use only facts the README states; do not guess what a tool it mentions is for. Describe the project, never the README itself (no "the README does not mention ..."). No praise, no adjectives like powerful, seamless, cutting-edge, \
blazing. No markdown, no links."""

PAGES_PROMPT = """You write the link descriptions of an llms.txt file for the project {name}. \
For each page below, write what a reader finds on it, in at most 18 words: a plain noun phrase \
or a sentence fragment, like "How to install from source and with pip, and the GPU build flags." \
Never start with "This page", "This document" or the page title. Use only what the excerpt says. \
No praise, no markdown.

{pages}

Reply with JSON only, one key per page id: {{"1": "...", "2": "..."}}"""


class ModelUnavailable(RuntimeError):
    """The model server did not answer. Never paper over this with weaker text: the caller
    decides (the App puts the job back in the queue; the CLI stops and says so)."""


@dataclass
class Model:
    base: str                 # OpenAI-compatible base (…/v1) or an Ollama host (…:11434)
    model: str
    key: str = ""
    backend: str = "openai"   # "openai" or "ollama" (native /api/chat, which honours `think`)
    think: str = ""           # openai backend: "off" sends enable_thinking=false (Qwen on vLLM);
                              # ollama backend: passed as `think` ("low", "high", or "false")
    workers: int = 4
    timeout: int = 180

    def chat(self, prompt: str, max_tokens: int = 1200) -> str:
        msgs = [{"role": "user", "content": prompt}]
        if self.backend == "ollama":
            body = {"model": self.model, "messages": msgs, "stream": False,
                    "options": {"temperature": 0.2, "num_predict": max_tokens * 4}}
            if self.think:
                body["think"] = False if self.think == "false" else self.think
            url = self.base.rstrip("/") + "/api/chat"
        else:
            body = {"model": self.model, "messages": msgs, "temperature": 0.2, "max_tokens": max_tokens}
            if self.think == "off":
                body["chat_template_kwargs"] = {"enable_thinking": False}
            url = self.base.rstrip("/") + "/chat/completions"
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json",
                                              **({"Authorization": f"Bearer {self.key}"} if self.key else {})})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code >= 500 or e.code in (404, 408, 429):
                raise ModelUnavailable(f"{self.base}: HTTP {e.code}") from e
            raise
        except (urllib.error.URLError, OSError, TimeoutError, http.client.HTTPException) as e:
            raise ModelUnavailable(f"{self.base}: {type(e).__name__}: {e}") from e
        if self.backend == "ollama":
            return d.get("message", {}).get("content", "") or ""
        return d["choices"][0]["message"].get("content") or ""


def _chat_retry(model: "Model", prompt: str, max_tokens: int) -> str:
    """One more try after a pause for a blip; a server that is really gone raises ModelUnavailable."""
    try:
        return model.chat(prompt, max_tokens)
    except ModelUnavailable:
        time.sleep(10)
        return model.chat(prompt, max_tokens)


def _json(reply: str) -> dict:
    reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.S)
    m = re.search(r"\{.*\}", reply, re.S)
    if not m:
        raise ValueError("no JSON in reply")
    return json.loads(m.group(0))


def _tidy(s: str, words: int) -> str:
    s = " ".join(str(s).replace("\n", " ").split()).strip(" \"'")
    w = s.split()
    if len(w) > words:
        s = " ".join(w[:words]).rstrip(",;:") + "…"
    if s and s[-1] not in ".…!?":
        s += "."
    return s[:1].upper() + s[1:]


def first_sentence(page: Page, words: int = 25) -> str:
    """No model: the page's own description, else its first real sentence."""
    if page.meta_description:
        return _tidy(page.meta_description, words)
    for para in page.text.split("\n\n"):
        para = " ".join(para.split())
        if len(para) < 40 or para.startswith(("#", "-", "*", ">", "|")) or para.lower() == page.title.lower():
            continue
        para = re.sub(r"^#+\s*", "", para)
        m = re.match(r"(.+?[.!?])(\s|$)", para)
        return _tidy(m.group(1) if m else para, words)
    return ""


def summarize(repo: Repo, model: Model | None) -> tuple[str, str]:
    readme = repo.readme.text if repo.readme else ""
    if model and readme:
        prompt = SUMMARY_PROMPT.format(
            name=repo.title,
            package=f"Package description: {repo.package_description}" if repo.package_description else "",
            readme=readme[:6000])
        for attempt in range(3):
            try:
                d = _json(_chat_retry(model, prompt, 600))
                s = _tidy(d.get("summary", ""), 34)
                if s:
                    det = d.get("details", "")
                    return s, (" ".join(str(det).split()) if det else "")
            except (ValueError, KeyError, json.JSONDecodeError):
                continue                       # a reply we could not read: ask again
    if repo.package_description:
        return _tidy(repo.package_description, 34), ""
    return (first_sentence(repo.readme, 34) if repo.readme else ""), ""


def describe(repo: Repo, pages: list[Page], model: Model | None, cache: dict) -> dict[str, str]:
    """path → description. A cached description is reused when the page's content is unchanged —
    at the same path, or at a new one (a moved or renamed page needs no model)."""
    out: dict[str, str] = {}
    todo: list[Page] = []
    by_sha = {v["sha"]: v["desc"] for k, v in cache.items()
              if not k.startswith("_") and isinstance(v, dict) and v.get("sha") and v.get("desc")}
    for p in pages:
        hit = cache.get(p.path)
        if hit and hit.get("sha") == p.sha and hit.get("desc"):
            out[p.path] = hit["desc"]
        elif p.sha in by_sha:
            out[p.path] = by_sha[p.sha]
        elif model:
            todo.append(p)
        else:
            out[p.path] = first_sentence(p)

    def batch(group: list[Page]) -> dict[str, str]:
        listing = "\n\n".join(f"[{i}] {p.title} ({p.path})\n{p.meta_description + ' ' if p.meta_description else ''}"
                              f"{p.text[:1400]}" for i, p in enumerate(group, 1))
        for _ in range(3):
            try:
                d = _json(_chat_retry(model, PAGES_PROMPT.format(name=repo.title, pages=listing), 150 * len(group)))
                res = {}
                for i, p in enumerate(group, 1):
                    v = d.get(str(i)) or d.get(i)
                    res[p.path] = _tidy(v, 22) if v else first_sentence(p)
                return res
            except (ValueError, KeyError, json.JSONDecodeError):
                continue
        return {p.path: first_sentence(p) for p in group}

    if todo:
        groups = [todo[i:i + 6] for i in range(0, len(todo), 6)]
        with ThreadPoolExecutor(max(1, model.workers)) as ex:
            for res in ex.map(batch, groups):
                out.update(res)
    return out
