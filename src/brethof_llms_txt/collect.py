"""Find what a repository says about itself: its README, its docs, its examples.

Everything here is plain file reading. No network, no model.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import subprocess
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DOC_EXT = {".md", ".mdx", ".rst", ".adoc", ".ipynb"}
DOC_ROOTS = ["docs", "doc", "Documentation", "documentation", "website/docs", "src/content/docs",
             "content/docs", "content", "pages", "guide", "guides", "manual", "wiki"]
EXAMPLE_ROOTS = ["examples", "example", "cookbook", "recipes", "samples"]
SKIP_DIRS = {".git", ".github", "node_modules", "vendor", "third_party", "third-party", "thirdparty",
             "external", "deps", "build", "dist", "site", "_build", "venv", ".venv", "__pycache__",
             "test", "tests", "testdata", "fixtures", "i18n", "translations", "translation", "locales",
             "locale", ".changeset", "_static", "_templates", "assets", "images", "img", "static",
             "blog", "news", "_posts", "_includes", "_layouts", "_data", "changelog", "changelogs", "releases", "archive", "old", "legacy"}
LANG_DIRS = {"zh", "zh-cn", "zh_cn", "zh-tw", "zh_tw", "zh-hans", "zh-hant", "cn", "ja", "jp", "ko", "kr",
             "fr", "de", "es", "ru", "pt", "pt-br", "pt_br", "it", "tr", "vi", "id", "pl", "uk", "ar",
             "fa", "he", "hi", "th", "nl", "sv", "cs", "hu", "ro", "el", "bn"}
LANG_SUFFIX = re.compile(r"[._-](zh|cn|ja|jp|ko|kr|fr|de|es|ru|pt|it|tr|vi|ar|fa|hi|th|pl|uk)"
                         r"([-_][A-Za-z]{2,4})?$", re.I)
SECONDARY = {"changelog": "Changelog", "changes": "Changelog", "history": "Changelog",
             "releases": "Release notes", "release_notes": "Release notes", "release": "Releasing",
             "releasing": "Releasing", "publishing": "Releasing",
             "contributing": "Contributing", "development": "Development"}
SKIP_ROOT = {"code_of_conduct", "security", "license", "licence", "copying", "authors", "contributors",
             "maintainers", "codeowners", "notice", "support", "funding", "pull_request_template",
             "issue_template", "citation", "third_party_notices", "thirdpartynotices", "agents", "claude",
             "gemini", "copilot-instructions", "llms", "llms-full"}
PRIORITY = ["index", "readme", "intro", "introduction", "overview", "about", "getting-started",
            "getting_started", "quickstart", "quick-start", "quick_start", "start", "install",
            "installation", "setup", "usage", "tutorial", "guide", "configuration", "config",
            "features", "api", "reference", "cli", "faq", "troubleshooting"]


@dataclass
class Page:
    path: str                 # repo-relative, forward slashes
    title: str
    text: str                 # readable text, markup mostly stripped
    sha: str                  # content hash: a page whose sha is unchanged keeps its description
    meta_description: str = ""
    headed: bool = True             # the title came from the page, not from its file name
    position: float | None = None   # the page's own nav_order / sidebar_position / weight
    group: str = ""           # section key
    order: int = 10**6        # position in the project's own navigation, if it has one


@dataclass
class Repo:
    root: Path
    owner: str
    name: str
    branch: str
    title: str = ""
    readme: Page | None = None
    pages: list[Page] = field(default_factory=list)
    examples: list[Page] = field(default_factory=list)
    secondary: list[Page] = field(default_factory=list)
    homepage: str = ""
    package_description: str = ""
    docs_root: str = ""
    config: dict = field(default_factory=dict)


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def repo_identity(root: Path) -> tuple[str, str, str]:
    """owner, name, default branch — from the git remote, falling back to the folder name."""
    url = _git(root, "remote", "get-url", "origin")
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    owner, name = (m.group(1), m.group(2)) if m else ("", root.resolve().name)
    head = _git(root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    branch = head.split("/", 1)[1] if "/" in head else (_git(root, "rev-parse", "--abbrev-ref", "HEAD") or "main")
    if branch == "HEAD":
        branch = "main"
    return owner, name, branch


# ── reading one file ─────────────────────────────────────────────────────────

FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def _frontmatter(raw: str) -> tuple[dict, str]:
    m = FRONTMATTER.match(raw)
    if not m:
        return {}, raw
    meta = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and k.strip() in ("title", "description", "sidebar_label", "sidebar_position", "nav_order",
                                 "weight", "draft", "slug"):
            meta[k.strip()] = v.strip().strip("'\"")
    return meta, raw[m.end():]


def _plain(body: str) -> str:
    """Markdown/RST/MDX to readable text — enough for a model or a first sentence, not a renderer."""
    t = re.sub(r"```.*?```|~~~.*?~~~", " ", body, flags=re.S)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"^\s*(import|export) .*$", " ", t, flags=re.M)              # MDX
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)                                # images
    t = re.sub(r"\[!\[.*?\]\(.*?\)\]\(.*?\)", " ", t)                           # badge links
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)                              # links → text
    t = re.sub(r"<[^>]+>", " ", t)                                             # html
    t = re.sub(r"^\.\. [a-z-]+::.*$", " ", t, flags=re.M)                      # rst directives
    t = re.sub(r":[a-z]+:`([^`<]+?)(\s*<[^>]+>)?`", r"\1", t)                   # rst roles
    t = re.sub(r"^[=\-~^*#+\"']{3,}\s*$", " ", t, flags=re.M)                  # rst underlines
    t = re.sub(r"^\s*\|.*\|\s*$", " ", t, flags=re.M)                          # tables
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()


def _title(path: Path, meta: dict, body: str) -> str:
    t = _raw_title(path, meta, body)
    return re.sub(r"^[^\w(\[]+", "", t).strip() or t


def _raw_title(path: Path, meta: dict, body: str) -> str:
    if meta.get("title"):
        return meta["title"]
    for line in body.splitlines()[:60]:
        m = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if m:
            t = _plain(m.group(1)).strip(" *_`")
            if t:
                return t
    lines = body.splitlines()
    for i, line in enumerate(lines[:60]):                                     # RST: title over ===
        if i + 1 < len(lines) and line.strip() and re.match(r"^[=\-~^*#]{3,}\s*$", lines[i + 1]) \
                and not re.match(r"^[=\-~^*#]{3,}\s*$", line):
            return line.strip()
    return ""


def _file_title(path: Path) -> str:
    stem = path.stem
    if stem.lower() in ("index", "readme") and path.parent.name:
        stem = path.parent.name
    return re.sub(r"[-_]+", " ", stem).strip().capitalize()


def read_page(root: Path, path: Path) -> Page | None:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if path.suffix.lower() == ".ipynb":
        try:
            cells = json.loads(raw).get("cells", [])
        except ValueError:
            return None
        raw = "\n\n".join("".join(c.get("source", [])) for c in cells if c.get("cell_type") == "markdown")
    meta, body = _frontmatter(raw)
    if meta.get("draft", "").lower() == "true":
        return None
    text = _plain(body)
    rel = path.relative_to(root).as_posix()
    return Page(path=rel, title=(_title(path, meta, body) or _file_title(path))[:120], text=text,
                headed=bool(_title(path, meta, body)),
                sha=hashlib.sha1(raw.encode("utf-8", "replace")).hexdigest()[:12],
                meta_description=meta.get("description", ""), position=_num(
                    meta.get("nav_order") or meta.get("sidebar_position") or meta.get("weight")))


def _num(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ── walking the tree ─────────────────────────────────────────────────────────

_MIRRORS: set[Path] = set()


def _skip_dir(name: str) -> bool:
    low = name.lower()
    return name.startswith(".") or low in SKIP_DIRS or low in LANG_DIRS


README_PART = re.compile(r"^readme[._-].+", re.I)   # README.head.md, README.foot.md: pieces of the README


def _doc_files(base: Path, skip: set[Path] | None = None) -> list[Path]:
    skip = _MIRRORS if skip is None else skip
    out = []
    if not base.is_dir():
        return out
    stack = [base]
    while stack:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir())
        except OSError:
            continue
        for p in entries:
            if p.is_dir():
                if not _skip_dir(p.name) and not p.is_symlink() and p.resolve() not in skip:
                    stack.append(p)
            elif p.suffix.lower() in DOC_EXT and not LANG_SUFFIX.search(p.stem) \
                    and p.stem.lower() not in SKIP_ROOT and not README_PART.match(p.stem):
                out.append(p)
    return out


def _mirrors(docs: Path) -> set[Path]:
    """Folders that are translations of the docs: named like a language code (de, pt-br, zh_CN)
    and holding mostly files whose names also exist outside them. Detected from the tree, so a
    folder called 'ml' or 'os' holding its own pages is kept."""
    out = set()
    try:
        subs = [p for p in docs.iterdir() if p.is_dir() and re.fullmatch(r"[a-z]{2}([-_][A-Za-z]{2,4})?", p.name)]
    except OSError:
        return out
    if not subs:
        return out
    every = {}
    for f in _doc_files(docs, skip=set()):
        every.setdefault(f.name, set()).add(f)
    for sub in subs:
        files = _doc_files(sub, skip=set())
        if not files:
            continue
        shared = sum(1 for f in files if any(not g.is_relative_to(sub) for g in every.get(f.name, ())))
        if shared / len(files) >= 0.5:
            out.add(sub.resolve())
    return out


def _find_docs_root(root: Path, cfg: dict) -> Path | None:
    if cfg.get("docs"):
        p = root / cfg["docs"]
        return p if p.is_dir() else None
    best, best_n = None, 0
    cands = [root / c for c in DOC_ROOTS]
    if (root / "book.toml").is_file():        # mdBook: the book lives in its src folder
        try:
            with (root / "book.toml").open("rb") as f:
                cands.insert(0, root / tomllib.load(f).get("book", {}).get("src", "src"))
        except (OSError, tomllib.TOMLDecodeError):
            cands.insert(0, root / "src")
    for depth in ("*/", "*/*/"):              # aider keeps its docs in aider/website/docs
        for name in ("docs", "doc", "documentation", "Documentation"):
            cands += [p for p in root.glob(depth + name)
                      if not any(_skip_dir(part) for part in p.relative_to(root).parts[:-1])]
    for p in cands:
        if p.is_dir():
            n = len(_doc_files(p))
            # a folder NAMED docs is docs from its first page; a generic name (content, pages,
            # guide) has to hold a few pages before it is taken for the documentation
            need = 1 if p.name.lower() in ("docs", "doc", "documentation") else 3
            if n >= need and n > (best_n if best else 0):
                best, best_n = p, n
    return best


def _nav_order(root: Path, docs: Path | None) -> dict[str, int]:
    """Order of first mention in the project's own navigation files: mkdocs.yml, SUMMARY.md,
    sidebars.*, _toc.yml, mint.json/docs.json, and the index pages' toctrees. A key is a path
    without its extension, relative to the repo root and to the docs root."""
    sources: list[Path] = []
    for name in ("mkdocs.yml", "mkdocs.yaml", "_toc.yml", "SUMMARY.md", "sidebars.js", "sidebars.ts",
                 "sidebars.json", "mint.json", "docs.json", "_sidebar.md", "astro.config.mjs",
                 "astro.config.ts", "docusaurus.config.js", "docusaurus.config.ts", "book.toml"):
        for base in filter(None, [root, docs, root / "website" if (root / "website").is_dir() else None]):
            if (base / name).is_file():
                sources.append(base / name)
            if (base / "src" / name).is_file():
                sources.append(base / "src" / name)
    if docs:
        for idx in ("index.rst", "index.md", "README.md", "index.mdx", "SUMMARY.md"):
            if (docs / idx).is_file():
                sources.append(docs / idx)
    order: dict[str, int] = {}
    n = 0
    for src in sources:
        try:
            txt = src.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in re.finditer(r"[\w./-]+", txt):
            tok = m.group(0).strip("./")
            tok = re.sub(r"\.(md|mdx|rst|adoc|html)$", "", tok)
            tok = re.sub(r"/index$", "", tok)
            if tok and tok not in order:
                order[tok] = n
                n += 1
    return order


def _position(page: Page, docs_rel: str, nav: dict[str, int]) -> int:
    key = re.sub(r"\.(md|mdx|rst|adoc)$", "", page.path)
    keys = [key, re.sub(r"/(index|README)$", "", key)]
    if docs_rel and key.startswith(docs_rel + "/"):
        sub = key[len(docs_rel) + 1:]
        keys += [sub, re.sub(r"/(index|README)$", "", sub)]
    pos = [nav[k] for k in keys if k in nav]
    return min(pos) if pos else 10**6


def _priority(path: str) -> tuple:
    stem = Path(path).stem.lower()
    return (PRIORITY.index(stem) if stem in PRIORITY else len(PRIORITY), path.count("/"), path.lower())


def load_config(root: Path) -> dict:
    for p in (root / ".github" / "llms-txt.toml", root / "llms-txt.toml"):
        if p.is_file():
            with p.open("rb") as f:
                return tomllib.load(f).get("llms-txt", {})
    return {}


def _package_meta(root: Path) -> tuple[str, str]:
    """(description, homepage) from the package manifest, when there is one."""
    try:
        if (root / "pyproject.toml").is_file():
            with (root / "pyproject.toml").open("rb") as f:
                d = tomllib.load(f)
            proj = d.get("project") or d.get("tool", {}).get("poetry", {})
            urls = proj.get("urls", {}) or {}
            home = proj.get("homepage") or urls.get("Homepage") or urls.get("homepage") or \
                urls.get("Documentation") or ""
            return proj.get("description", "") or "", home
        if (root / "package.json").is_file():
            d = json.loads((root / "package.json").read_text(encoding="utf-8"))
            return d.get("description", "") or "", d.get("homepage", "") or ""
        if (root / "Cargo.toml").is_file():
            with (root / "Cargo.toml").open("rb") as f:
                d = tomllib.load(f).get("package", {})
            return d.get("description", "") or "", d.get("homepage") or d.get("documentation") or ""
    except (OSError, ValueError, tomllib.TOMLDecodeError):
        pass
    return "", ""


def _readme(root: Path) -> Path | None:
    for name in ("README.md", "readme.md", "Readme.md", "README.rst", "README.mdx", "README", "README.txt",
                 "README.adoc"):
        if (root / name).is_file():
            return root / name
    return None


def _clean_title(readme: Page | None, name: str) -> str:
    """The project's name as the project writes it: 'FastEmbed', not 'fastembed', and never a
    README heading like 'What is FastEmbed?'."""
    norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
    if readme and readme.headed:
        cand = re.sub(r"^(welcome to|introducing|about)\s+(the\s+)?", "", readme.title, flags=re.I)
        cand = cand.strip(" !.")
        short = len(cand.split()) <= 5 and not re.search(r"[?:]", cand)
        generic = name.lower() in ("docs", "doc", "wiki", "website", "site", "documentation", "book",
                                   "handbook", "manual", "guide", "www", "web")
        if short and (norm(name) in norm(cand) or generic):
            return cand
        for tok in re.findall(r"[\w.+-]+", readme.title):
            if norm(tok) == norm(name):
                return tok
    return name


def collect(root: Path, owner: str = "", name: str = "", branch: str = "") -> Repo:
    root = root.resolve()
    o, n, b = repo_identity(root)
    repo = Repo(root=root, owner=owner or o, name=name or n, branch=branch or b)
    repo.config = load_config(root)
    repo.package_description, repo.homepage = _package_meta(root)

    rp = _readme(root)
    repo.readme = read_page(root, rp) if rp else None
    repo.title = repo.config.get("title") or _clean_title(repo.readme, repo.name)

    excluded = [re.compile(x) for x in repo.config.get("exclude", [])]
    _MIRRORS.clear()
    docs = _find_docs_root(root, repo.config)
    if docs:
        _MIRRORS.update(_mirrors(docs))
    repo.docs_root = docs.relative_to(root).as_posix() if docs else ""
    nav = _nav_order(root, docs)

    seen = {rp.resolve()} if rp else set()
    readme_head = " ".join(repo.readme.text.split())[:800] if repo.readme else ""

    def take(paths: list[Path]) -> list[Page]:
        out = []
        for p in paths:
            rel = p.relative_to(root).as_posix()
            if p.resolve() in seen or any(x.search(rel) for x in excluded):
                continue
            seen.add(p.resolve())
            pg = read_page(root, p)
            if pg and repo.readme and pg.title.lower() == repo.readme.title.lower() and difflib.SequenceMatcher(
                    None, readme_head, " ".join(pg.text.split())[:800]).quick_ratio() > 0.6:
                continue                             # docs/index.md: the README again, lightly edited
            if pg and readme_head and difflib.SequenceMatcher(
                    None, readme_head, " ".join(pg.text.split())[:800]).quick_ratio() > 0.92 \
                    and difflib.SequenceMatcher(None, readme_head, " ".join(pg.text.split())[:800]).ratio() > 0.9:
                continue                             # docs/index.md that repeats the README
            if pg and len(pg.text) >= 80:            # a page with nothing to read is not worth a link
                pg.order = _position(pg, repo.docs_root, nav)
                if pg.order >= 10**6 and pg.position is not None:   # Jekyll/Docusaurus front matter
                    pg.order = int(500_000 + pg.position * 10)
                out.append(pg)
        return out

    # secondary root files (changelog, contributing) — "Optional"
    for p in sorted(root.iterdir()):
        if p.is_file() and p.suffix.lower() in DOC_EXT | {""} and p.stem.lower() in SECONDARY:
            repo.secondary += take([p])

    if docs:
        repo.pages = take(_doc_files(docs))
        for pg in repo.pages:
            sub = pg.path[len(repo.docs_root) + 1:] if repo.docs_root else pg.path
            pg.group = sub.split("/", 1)[0] if "/" in sub else ""
    # other root-level documents (llama.cpp keeps docs at the root too)
    roots = [p for p in sorted(root.iterdir()) if p.is_file() and p.suffix.lower() in DOC_EXT
             and p.stem.lower() not in SKIP_ROOT and p.stem.lower() not in SECONDARY
             and not LANG_SUFFIX.search(p.stem) and not README_PART.match(p.stem)]
    repo.pages = take(roots) + repo.pages

    for cand in EXAMPLE_ROOTS:
        if (root / cand).is_dir():
            repo.examples += take(_doc_files(root / cand))
    for pg in repo.examples:
        pg.group = "examples"
    return repo


def ordered(pages: list[Page]) -> list[Page]:
    return sorted(pages, key=lambda p: (p.order, _priority(p.path)))
