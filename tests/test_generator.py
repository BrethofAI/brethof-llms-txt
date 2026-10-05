"""Run with:  PYTHONPATH=src python3 -m unittest discover -s tests"""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from brethof_llms_txt.build import generate
from brethof_llms_txt.collect import collect
from brethof_llms_txt.validate import check


def make_repo(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp()) / "demo"
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", "https://github.com/acme/demo.git"],
                   check=True)
    return root


PAGE = "This page explains a part of the project in enough words to be worth a link, really.\n"

REPO = {
    "README.md": "# Demo\n\nDemo is a small library that turns widgets into gadgets for testing.\n",
    "CHANGELOG.md": "# Changelog\n\n## 1.0\n\nFirst release of the library with all of its features, and the docs to go with them.\n",
    "docs/index.md": "# Docs home\n\n" + PAGE,
    "docs/install.md": "---\ntitle: Installing\ndescription: Install with pip or from source.\n---\n" + PAGE,
    "docs/guides/first.md": "# First steps\n\n" + PAGE,
    "docs/de/install.md": "# Installation\n\n" + PAGE,            # a translation: skipped
    "docs/decisions/0001.md": "# Use widgets\n\n" + PAGE,         # internal: Optional
    "docs/tiny.md": "# Tiny\n\nToo short.\n",                     # nothing to read: skipped
}


class Generator(unittest.TestCase):
    def test_structure_and_format(self):
        repo = collect(make_repo(REPO))
        text, cache = generate(repo, None)
        self.assertEqual(check(text)[0], [])
        self.assertTrue(text.startswith("# Demo\n\n> Demo is a small library"))
        self.assertIn("## Docs", text)
        self.assertIn("## Guides", text)
        self.assertIn("[Installing](https://raw.githubusercontent.com/acme/demo/", text)
        self.assertIn(": Install with pip or from source.", text)
        self.assertNotIn("/de/", text)
        self.assertNotIn("tiny.md", text)
        self.assertLess(text.index("## Guides"), text.index("## Optional"))
        self.assertGreater(text.index("decisions/0001.md"), text.index("## Optional"))
        self.assertGreater(text.index("CHANGELOG.md"), text.index("## Optional"))

    def test_rerun_is_identical(self):
        root = make_repo(REPO)
        a, cache = generate(collect(root), None)
        b, _ = generate(collect(root), None, json.loads(json.dumps(cache)))
        self.assertEqual(a, b)


class Repair(unittest.TestCase):
    """known_only: the no-model fix between weekly passes."""

    def setUp(self):
        self.root = make_repo(REPO)
        self.text, cache = generate(collect(self.root), None)
        # pretend a model wrote these, so a reused one is recognisable
        self.cache = {k: ({**v, "desc": "MODEL " + k} if not k.startswith("_") else v) for k, v in cache.items()}

    def run_repair(self):
        return generate(collect(self.root), None, json.loads(json.dumps(self.cache)), known_only=True)

    def test_moved_page_keeps_its_description(self):
        (self.root / "docs/guides").mkdir(exist_ok=True)
        (self.root / "docs/install.md").rename(self.root / "docs/guides/install.md")
        text, _ = self.run_repair()
        self.assertIn("docs/guides/install.md", text)
        self.assertIn("MODEL docs/install.md", text)

    def test_deleted_page_drops_out_and_new_page_waits(self):
        (self.root / "docs/guides/first.md").unlink()
        (self.root / "docs/new.md").write_text("# New\n\n" + PAGE)
        text, _ = self.run_repair()
        self.assertNotIn("first.md", text)
        self.assertNotIn("docs/new.md", text)

    def test_changed_page_keeps_old_words_until_the_next_pass(self):
        (self.root / "docs/install.md").write_text("# Installing\n\nCompletely new install text, long enough to read and to be worth a link in the file.\n")
        text, cache = self.run_repair()
        self.assertIn("MODEL docs/install.md", text)
        self.assertEqual(cache["docs/install.md"]["sha"], self.cache["docs/install.md"]["sha"])


class Validator(unittest.TestCase):
    def test_good(self):
        self.assertEqual(check("# X\n\n> s\n\n## Docs\n\n- [a](https://a.b/c): d\n")[0], [])

    def test_bad(self):
        errs, _ = check("no title\n## Docs\nnot a link\n")
        self.assertEqual(len(errs), 2)


if __name__ == "__main__":
    unittest.main()
