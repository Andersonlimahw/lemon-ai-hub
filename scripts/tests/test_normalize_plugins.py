"""Tests for scripts/normalize_plugins.py.

Pure-function coverage (slugify, frontmatter split/parse/render, derive) plus
filesystem repairs against a temporary plugins tree with the module's
REPO_ROOT/PLUGINS_DIR globals patched. Runs with stdlib unittest (also
collected by pytest).

    python3 -m unittest discover -s scripts/tests
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import normalize_plugins as np


def make_changes(dry_run: bool = False) -> np.Changes:
    changes = np.Changes(dry_run)
    # Silence per-change printing during tests.
    changes.record = lambda message: changes.entries.append(message)  # type: ignore[method-assign]
    return changes


class TestSlugify(unittest.TestCase):
    def test_lowercases_and_dashes(self):
        self.assertEqual(np.slugify("My Cool Skill"), "my-cool-skill")

    def test_strips_quotes_and_specials(self):
        self.assertEqual(np.slugify('"Foo_Bar! (v2)"'), "foo-bar-v2")

    def test_collapses_dashes(self):
        self.assertEqual(np.slugify("a --- b"), "a-b")

    def test_already_slug(self):
        self.assertEqual(np.slugify("error-fixer-loop"), "error-fixer-loop")


class TestFrontmatterHelpers(unittest.TestCase):
    def test_split_no_frontmatter(self):
        block, body = np.split_frontmatter("# Title\nbody")
        self.assertIsNone(block)
        self.assertEqual(body, "# Title\nbody")

    def test_split_unterminated(self):
        block, body = np.split_frontmatter("---\nname: x\nno closing fence")
        self.assertIsNone(block)

    def test_split_valid(self):
        block, body = np.split_frontmatter("---\nname: x\ndescription: y\n---\n# Body\n")
        self.assertEqual(block, "name: x\ndescription: y")
        self.assertEqual(body, "# Body\n")

    def test_parse_key_values(self):
        data = np.parse_frontmatter("name: foo\ndescription: bar baz")
        self.assertEqual(data, {"name": "foo", "description": "bar baz"})

    def test_parse_continuation_lines(self):
        data = np.parse_frontmatter("description: first\n  second line\nname: x")
        self.assertEqual(data["description"], "first second line")
        self.assertEqual(data["name"], "x")

    def test_yaml_quote_escapes(self):
        self.assertEqual(np.yaml_quote('say "hi" \\ ok'), '"say \\"hi\\" \\\\ ok"')

    def test_render_preserves_unmanaged_keys(self):
        block = 'name: old\ndescription: old desc\nlicense: MIT\nallowed-tools: Read'
        out = np.render_frontmatter({"name": "new", "description": "d"}, block)
        self.assertIn('name: "new"', out)
        self.assertIn('description: "d"', out)
        self.assertIn("license: MIT", out)
        self.assertIn("allowed-tools: Read", out)
        self.assertNotIn("old desc", out)
        self.assertTrue(out.startswith("---\n"))
        self.assertTrue(out.endswith("---\n"))


class TestDeriveFromBody(unittest.TestCase):
    def test_heading_and_paragraph(self):
        name, desc = np.derive_from_body(
            "# My Skill\n\nDoes *great* `things`.\nMore detail.\n\n## Next\n", "fb"
        )
        self.assertEqual(name, "my-skill")
        self.assertEqual(desc, "Does great things. More detail.")

    def test_no_heading_falls_back(self):
        name, desc = np.derive_from_body("plain text only\n", "fallback-name")
        self.assertEqual(name, "fallback-name")
        self.assertEqual(desc, "fallback-name skill.")

    def test_heading_without_paragraph(self):
        name, desc = np.derive_from_body("# Solo\n", "fb")
        self.assertEqual(name, "solo")
        self.assertEqual(desc, "Solo skill.")


class RepairTestCase(unittest.TestCase):
    """Base: temp repo tree + patched module globals."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        self.plugins = self.root / "plugins"
        self.plugins.mkdir()
        self._orig = (np.REPO_ROOT, np.PLUGINS_DIR)
        np.REPO_ROOT = self.root
        np.PLUGINS_DIR = self.plugins

    def tearDown(self):
        np.REPO_ROOT, np.PLUGINS_DIR = self._orig
        self._tmp.cleanup()

    def make_plugin(self, name: str) -> Path:
        d = self.plugins / name
        d.mkdir(parents=True, exist_ok=True)
        return d

    @staticmethod
    def skill_md(name: str, description: str = "A test skill.") -> str:
        return f'---\nname: "{name}"\ndescription: "{description}"\n---\n# {name}\n\nBody.\n'


class TestFixFlatSkills(RepairTestCase):
    def test_moves_flat_file_into_directory(self):
        plugin = self.make_plugin("demo")
        (plugin / "skills").mkdir()
        (plugin / "skills" / "sub.md").write_text(self.skill_md("sub"), encoding="utf-8")
        changes = make_changes()
        materialized = np.fix_flat_skills(plugin, changes)
        self.assertEqual(list(materialized), ["sub"])
        self.assertTrue((plugin / "skills" / "sub" / "SKILL.md").exists())
        self.assertFalse((plugin / "skills" / "sub.md").exists())

    def test_ignores_canonical_and_non_md(self):
        plugin = self.make_plugin("demo")
        (plugin / "skills" / "ok").mkdir(parents=True)
        (plugin / "skills" / "ok" / "SKILL.md").write_text(self.skill_md("ok"), encoding="utf-8")
        (plugin / "skills" / "notes.txt").write_text("x", encoding="utf-8")
        changes = make_changes()
        self.assertEqual(np.fix_flat_skills(plugin, changes), {})
        self.assertEqual(changes.entries, [])

    def test_dry_run_moves_nothing(self):
        plugin = self.make_plugin("demo")
        (plugin / "skills").mkdir()
        (plugin / "skills" / "sub.md").write_text(self.skill_md("sub"), encoding="utf-8")
        changes = make_changes(dry_run=True)
        materialized = np.fix_flat_skills(plugin, changes)
        self.assertTrue((plugin / "skills" / "sub.md").exists())
        # Dry-run reports the source path so later steps still see the skill.
        self.assertEqual(materialized["sub"], plugin / "skills" / "sub.md")


class TestEnsureRootSkill(RepairTestCase):
    def test_promotes_single_sub_skill(self):
        plugin = self.make_plugin("demo")
        (plugin / "skills" / "only").mkdir(parents=True)
        (plugin / "skills" / "only" / "SKILL.md").write_text(
            self.skill_md("only", "Only sub."), encoding="utf-8"
        )
        np.ensure_root_skill(plugin, make_changes())
        root = (plugin / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('name: "demo"', root)
        self.assertIn('description: "Only sub."', root)

    def test_generates_index_for_multiple(self):
        plugin = self.make_plugin("demo")
        for sub in ("alpha", "beta"):
            (plugin / "skills" / sub).mkdir(parents=True)
            (plugin / "skills" / sub / "SKILL.md").write_text(
                self.skill_md(sub, f"{sub} desc."), encoding="utf-8"
            )
        np.ensure_root_skill(plugin, make_changes())
        root = (plugin / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Routes to its sub-skills: alpha, beta", root)
        self.assertIn("skills/alpha/SKILL.md", root)
        self.assertIn("skills/beta/SKILL.md", root)

    def test_existing_root_untouched(self):
        plugin = self.make_plugin("demo")
        (plugin / "SKILL.md").write_text("original", encoding="utf-8")
        np.ensure_root_skill(plugin, make_changes())
        self.assertEqual((plugin / "SKILL.md").read_text(encoding="utf-8"), "original")

    def test_no_sources_skips(self):
        plugin = self.make_plugin("demo")
        changes = make_changes()
        np.ensure_root_skill(plugin, changes)
        self.assertFalse((plugin / "SKILL.md").exists())
        self.assertTrue(any("SKIPPED" in e for e in changes.entries))


class TestEnsurePluginJson(RepairTestCase):
    def test_creates_from_root_skill(self):
        plugin = self.make_plugin("demo")
        (plugin / "SKILL.md").write_text(self.skill_md("demo", "From skill."), encoding="utf-8")
        np.ensure_plugin_json(plugin, make_changes())
        data = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "demo")
        self.assertEqual(data["description"], "From skill.")
        self.assertEqual(data["version"], np.DEFAULT_VERSION)
        self.assertEqual(data["license"], np.DEFAULT_LICENSE)
        self.assertEqual(data["author"], np.AUTHOR)
        for kw in np.BASE_KEYWORDS + ["demo"]:
            self.assertIn(kw, data["keywords"])

    def test_regenerates_invalid_json(self):
        plugin = self.make_plugin("demo")
        (plugin / "SKILL.md").write_text(self.skill_md("demo"), encoding="utf-8")
        (plugin / "plugin.json").write_text("{not json", encoding="utf-8")
        np.ensure_plugin_json(plugin, make_changes())
        data = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "demo")

    def test_preserves_existing_fields(self):
        plugin = self.make_plugin("demo")
        (plugin / "SKILL.md").write_text(self.skill_md("demo"), encoding="utf-8")
        (plugin / "plugin.json").write_text(
            json.dumps({"name": "demo", "version": "3.1.4", "description": "Keep me",
                        "keywords": ["custom"], "homepage": "https://example.com"}),
            encoding="utf-8",
        )
        np.ensure_plugin_json(plugin, make_changes())
        data = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(data["version"], "3.1.4")
        self.assertEqual(data["description"], "Keep me")
        self.assertEqual(data["homepage"], "https://example.com")
        self.assertIn("custom", data["keywords"])


class TestNormalizePlugin(RepairTestCase):
    def messy_plugin(self) -> Path:
        """Flat sub-skill, no root SKILL.md, no plugin.json."""
        plugin = self.make_plugin("messy")
        (plugin / "skills").mkdir()
        (plugin / "skills" / "core.md").write_text(
            "# Core Thing\n\nDoes the core thing.\n", encoding="utf-8"
        )
        return plugin

    def test_full_repair(self):
        plugin = self.messy_plugin()
        np.normalize_plugin(plugin, make_changes())
        self.assertTrue((plugin / "skills" / "core" / "SKILL.md").exists())
        self.assertTrue((plugin / "SKILL.md").exists())
        self.assertTrue((plugin / "plugin.json").exists())
        root = (plugin / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('name: "messy"', root)

    def test_idempotent(self):
        plugin = self.messy_plugin()
        np.normalize_plugin(plugin, make_changes())
        second = make_changes()
        np.normalize_plugin(plugin, second)
        self.assertEqual(second.entries, [], f"second run not idempotent: {second.entries}")

    def test_dry_run_writes_nothing(self):
        plugin = self.messy_plugin()
        np.normalize_plugin(plugin, make_changes(dry_run=True))
        self.assertFalse((plugin / "SKILL.md").exists())
        self.assertFalse((plugin / "plugin.json").exists())
        self.assertTrue((plugin / "skills" / "core.md").exists())


if __name__ == "__main__":
    unittest.main()
