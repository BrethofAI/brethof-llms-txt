# brethof-llms-txt

Writes an [`llms.txt`](https://llmstxt.org) for a GitHub repository from its README and docs, and keeps it current as the docs change.

An `llms.txt` is a short markdown file at the root of a project. It tells AI assistants what the project is and where its documentation lives, so they read your docs instead of guessing.

- **Works from the repository itself.** You don't need a docs website or a docs plugin. It reads the README, the docs folder (Markdown, MDX, reStructuredText, AsciiDoc, notebooks), the examples, and the project's own navigation (`mkdocs.yml`, mdBook `SUMMARY.md`, Docusaurus sidebars, Sphinx toctrees, front-matter order).
- **Structure by rules, words by a model.** The file's sections and order follow your docs folders and navigation; scripts decide that, and the same input always gives the same structure. A model, if you configure one, writes only the one-line summary and the link descriptions. Without a model, the descriptions come from each page's own front matter or first sentence.
- **Cheap to keep current.** Descriptions are stored with a hash of each page. On the next run, only changed pages are described again; an unchanged repo makes no model calls and produces the same file byte for byte.
- **Checks the format.** `check` validates a file against the llms.txt format and, with `--links`, checks that every link answers.
- **No dependencies.** Python 3.11+ standard library only.

## Use the GitHub App

[Install Brethof llms.txt](https://github.com/apps/brethof-llms-txt) on the repositories you choose. It opens a pull request that adds `llms.txt`, written with our hosted model, and updates that pull request (or opens a new one) when your docs change. Nothing to configure and no API key. Its commits are made through GitHub's API, so GitHub signs them (Verified). Free for public repositories.

If you already have an `llms.txt`, it offers its own version as a pull request for you to compare; nothing changes unless you merge. Close its pull request without merging and it will not open another on that repository.

## Use it as a GitHub Action

Copy [`examples/llms-txt.yml`](examples/llms-txt.yml) to `.github/workflows/llms-txt.yml`. When the docs change, the Action rebuilds `llms.txt` and opens a pull request (or commits directly, with `mode: commit`).

```yaml
- uses: actions/checkout@v4
- uses: BrethofAI/brethof-llms-txt@v1
  with:                        # optional: a model for the descriptions
    api-base: https://api.example.com/v1
    model: your-model
    api-key: ${{ secrets.LLMS_TXT_API_KEY }}
```

## Use it from the command line

```bash
pip install git+https://github.com/BrethofAI/brethof-llms-txt
brethof-llms-txt generate path/to/repo                       # descriptions from the pages
brethof-llms-txt generate path/to/repo --api-base http://localhost:8000/v1 --model my-model
brethof-llms-txt check path/to/repo/llms.txt --links
```

Any OpenAI-compatible endpoint works (vLLM, llama.cpp server, LM Studio, hosted APIs), as does Ollama with `--backend ollama`.

## Settings

Optional, in `.github/llms-txt.toml`:

```toml
[llms-txt]
title = "Project Name"          # default: the README title or the repository name
summary = "One sentence."       # write it yourself instead of the model
docs = "website/docs"           # where the docs are, if not found automatically
exclude = ["^docs/internal/"]   # regular expressions on repository paths
max_links = 80
links = "raw"                   # raw (plain markdown, default), blob (GitHub pages) or relative (paths in the repo)
base_url = "https://example.com/docs-src"   # link to another host instead
mode = "commit"                 # for the app: commit instead of opening pull requests
skip = true                     # for the app: keep your own llms.txt, never offer one
```

## How it chooses what to link

- **Docs:** the README and the top-level docs pages.
- **One section per docs folder,** in the project's own navigation order.
- **Very large trees** (the Linux kernel has about a hundred documentation folders) are folded: each folder becomes one link to its index page, and the folders the navigation doesn't name go under **Optional**.
- **README-only projects:** when the docs are just the README, its sections (installation, usage, configuration…) are linked directly, by their GitHub anchors.
- **Optional also holds** the changelog, the contributing guide, and folders written for the project's own developers (design decisions, specs, RFCs).
- **Left out:** translations (folders that mirror the docs in another language), blog posts, tests, and pages too short to be worth a link.

## Privacy and support

The App's [terms of service](TERMS.md) and [privacy policy](PRIVACY.md). For help, open an [issue](https://github.com/BrethofAI/brethof-llms-txt/issues) or email hello@brethof.ai.

## Licence

MIT. Made by [BrethofAI](https://github.com/BrethofAI).
