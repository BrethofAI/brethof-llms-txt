"""Check an llms.txt against the format at llmstxt.org, and optionally check that every link answers."""
from __future__ import annotations

import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

LINK = re.compile(r"^- \[([^\]]+)\]\((\S+?)\)(?::\s*(.*))?$")


def check(text: str) -> tuple[list[str], list[str]]:
    """(errors, warnings). An error breaks the format; a warning is worth a look."""
    errors, warnings = [], []
    lines = text.splitlines()
    body = [(i, l) for i, l in enumerate(lines, 1) if l.strip()]
    if not body or not body[0][1].startswith("# "):
        errors.append("line 1: the file must start with a single H1 title ('# Name')")
    if sum(1 for _, l in body if re.match(r"^# ", l)) > 1:
        errors.append("more than one H1 title")
    section, links, urls = None, 0, {}
    empty = []
    for i, l in body[1:]:
        if l.startswith("## "):
            if section and links == 0:
                empty.append(section)
            section, links = l[3:].strip(), 0
            continue
        if re.match(r"^#{3,} ", l):
            warnings.append(f"line {i}: headings below H2 are not part of the format")
            continue
        if section is None:
            continue                       # summary and details: free text
        m = LINK.match(l)
        if not m:
            errors.append(f"line {i}: inside a section every line must be '- [title](url): notes'")
            continue
        links += 1
        url = m.group(2)
        if not re.match(r"https?://", url):
            warnings.append(f"line {i}: link is not an absolute URL: {url}")
        if url in urls:
            warnings.append(f"line {i}: duplicate link (first on line {urls[url]})")
        urls.setdefault(url, i)
    if section and links == 0:
        empty.append(section)
    for s in empty:
        warnings.append(f"section '{s}' has no links")
    if not urls:
        warnings.append("no links at all")
    return errors, warnings


def links(text: str, workers: int = 8, timeout: int = 20) -> list[tuple[str, str]]:
    """[(url, problem)] for every link that does not answer 200."""
    urls = []
    for l in text.splitlines():
        m = LINK.match(l)
        if m and m.group(2).startswith("http"):
            urls.append(m.group(2))

    def probe(url: str) -> tuple[str, str] | None:
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(url, method=method,
                                             headers={"User-Agent": "brethof-llms-txt (+https://github.com/BrethofAI/brethof-llms-txt)"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    if r.status == 200:
                        return None
                    problem = str(r.status)
            except urllib.error.HTTPError as e:
                problem = str(e.code)
                if e.code in (403, 405) and method == "HEAD":
                    continue
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                problem = type(e).__name__
            return url, problem
        return url, problem

    with ThreadPoolExecutor(workers) as ex:
        return [r for r in ex.map(probe, dict.fromkeys(urls)) if r]
