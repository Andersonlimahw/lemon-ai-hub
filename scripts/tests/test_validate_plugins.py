"""Tests for scripts/validate_plugins.py.

Every finding code is exercised against a temporary plugins tree with the
module's REPO_ROOT/PLUGINS_DIR/MARKETPLACE globals patched, plus an
integration test: normalize a messy plugin, then assert the validator reports
zero errors on it. Runs with stdlib unittest (also collected by pytest).

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
import validate_plugins as vp


def codes(report: vp.Report) -> list[str]:
    return [f.code for f in report.findings]


class ValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        self.plugins = self.root / "plugins"
        self.plugins.mkdir()
        self.marketplace = self.root / ".claude-plugin" / "marketplace.json"
        self._orig = (vp.REPO_ROOT, vp.PLUGINS_DIR, vp.MARKETPLACE)
        vp.REPO_ROOT = self.root
        vp.PLUGINS_DIR = self.plugins
        vp.MARKETPLACE = self.marketplace

    def tearDown(self):
        vp.REPO_ROOT, vp.PLUGINS_DIR, vp.MARKETPLACE = self._orig
        self._tmp.cleanup()

    def make_plugin(self, name: str, *, skill: bool = True, plugin_json: bool = True) -> Path:
        d = self.plugins / name
        d.mkdir(parents=True, exist_ok=True)
        if skill:
            (d / "SKILL.md").write_text(
                f'---\nname: "{name}"\ndescription: "A valid skill."\n---\n# {name}\n',
                encoding="utf-8",
            )
        if plugin_json:
            (d / "plugin.json").write_text(
                json.dumps({"name": name, "version": "1.0.0", "description": "Valid."}),
                encoding="utf-8",
            )
        return d

    def write_skill(self, plugin: Path, content: str) -> Path:
        path = plugin / "SKILL.md"
        path.write_text(content, encoding="utf-8")
        return path


class TestParseFrontmatter(ValidatorTestCase):
    def test_missing_file(self):
        self.assertIsNone(vp.parse_frontmatter(self.root / "nope.md"))

    def test_no_frontmatter(self):
        p = self.root / "a.md"
        p.write_text("# just a body\n", encoding="utf-8")
        self.assertIsNone(vp.parse_frontmatter(p))

    def test_continuation_lines(self):
        p = self.root / "a.md"
        p.write_text("---\ndescription: first\n  second\n---\nbody\n", encoding="utf-8")
        self.assertEqual(vp.parse_frontmatter(p), {"description": "first second"})


class TestCheckSkillFile(ValidatorTestCase):
    def check(self, content: str, expected_name: str = "demo") -> vp.Report:
        plugin = self.make_plugin("demo", plugin_json=False)
        path = self.write_skill(plugin, content)
        report = vp.Report()
        vp.check_skill_file(report, "demo", path, expected_name)
        return report

    def test_valid_no_findings(self):
        report = self.check('---\nname: "demo"\ndescription: "ok"\n---\n')
        self.assertEqual(codes(report), [])

    def test_no_frontmatter(self):
        report = self.check("# no frontmatter\n")
        self.assertEqual(codes(report), ["SKILL_NO_FRONTMATTER"])

    def test_missing_name(self):
        report = self.check('---\ndescription: "ok"\n---\n')
        self.assertEqual(codes(report), ["SKILL_NO_NAME"])

    def test_doubled_quotes(self):
        report = self.check('---\nname: ""demo""\ndescription: "ok"\n---\n')
        self.assertIn("SKILL_NAME_QUOTED", codes(report))

    def test_name_mismatch(self):
        report = self.check('---\nname: "other"\ndescription: "ok"\n---\n')
        self.assertIn("SKILL_NAME_MISMATCH", codes(report))

    def test_name_not_slug(self):
        report = self.check('---\nname: "Demo Name"\ndescription: "ok"\n---\n', "Demo Name")
        self.assertIn("SKILL_NAME_NOT_SLUG", codes(report))

    def test_missing_description(self):
        report = self.check('---\nname: "demo"\n---\n')
        self.assertEqual(codes(report), ["SKILL_NO_DESCRIPTION"])

    def test_long_description_warns(self):
        long_desc = "x" * (vp.MAX_DESCRIPTION + 1)
        report = self.check(f'---\nname: "demo"\ndescription: "{long_desc}"\n---\n')
        self.assertEqual(codes(report), ["SKILL_DESCRIPTION_LONG"])
        self.assertEqual(report.findings[0].severity, "WARN")
        self.assertEqual(report.errors, [])


class TestCheckPlugin(ValidatorTestCase):
    def test_valid_plugin(self):
        plugin = self.make_plugin("demo")
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertEqual(codes(report), [])

    def test_missing_plugin_json(self):
        plugin = self.make_plugin("demo", plugin_json=False)
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertIn("NO_PLUGIN_JSON", codes(report))

    def test_invalid_plugin_json(self):
        plugin = self.make_plugin("demo")
        (plugin / "plugin.json").write_text("{oops", encoding="utf-8")
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertIn("PLUGIN_JSON_INVALID", codes(report))

    def test_plugin_json_name_mismatch(self):
        plugin = self.make_plugin("demo")
        (plugin / "plugin.json").write_text(
            json.dumps({"name": "wrong", "version": "1.0.0", "description": "d"}),
            encoding="utf-8",
        )
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertIn("PLUGIN_JSON_NAME_MISMATCH", codes(report))

    def test_plugin_json_no_description_and_no_version(self):
        plugin = self.make_plugin("demo")
        (plugin / "plugin.json").write_text(json.dumps({"name": "demo"}), encoding="utf-8")
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertIn("PLUGIN_JSON_NO_DESCRIPTION", codes(report))
        self.assertIn("PLUGIN_JSON_NO_VERSION", codes(report))
        self.assertEqual([f.code for f in report.warnings], ["PLUGIN_JSON_NO_VERSION"])

    def test_missing_root_skill(self):
        plugin = self.make_plugin("demo", skill=False)
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertIn("NO_ROOT_SKILL", codes(report))

    def test_subskill_without_skill_md(self):
        plugin = self.make_plugin("demo")
        (plugin / "skills" / "empty").mkdir(parents=True)
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertIn("SUBSKILL_NO_SKILL_MD", codes(report))

    def test_flat_skill_file(self):
        plugin = self.make_plugin("demo")
        (plugin / "skills").mkdir()
        (plugin / "skills" / "flat.md").write_text("x", encoding="utf-8")
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertIn("FLAT_SKILL_FILE", codes(report))

    def test_valid_subskill(self):
        plugin = self.make_plugin("demo")
        sub = plugin / "skills" / "helper"
        sub.mkdir(parents=True)
        (sub / "SKILL.md").write_text(
            '---\nname: "helper"\ndescription: "ok"\n---\n', encoding="utf-8"
        )
        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertEqual(codes(report), [])


class TestCheckMarketplace(ValidatorTestCase):
    def write_marketplace(self, entries: list[dict]) -> None:
        self.marketplace.parent.mkdir(parents=True, exist_ok=True)
        self.marketplace.write_text(json.dumps({"plugins": entries}), encoding="utf-8")

    def test_missing_marketplace(self):
        report = vp.Report()
        vp.check_marketplace(report, [])
        self.assertEqual(codes(report), ["NO_MARKETPLACE"])

    def test_invalid_json(self):
        self.marketplace.parent.mkdir(parents=True, exist_ok=True)
        self.marketplace.write_text("{bad", encoding="utf-8")
        report = vp.Report()
        vp.check_marketplace(report, [])
        self.assertEqual(codes(report), ["MARKETPLACE_INVALID"])

    def test_consistent(self):
        plugin = self.make_plugin("demo")
        self.write_marketplace([{"name": "demo", "source": "./plugins/demo"}])
        report = vp.Report()
        vp.check_marketplace(report, [plugin])
        self.assertEqual(codes(report), [])

    def test_on_disk_not_listed(self):
        plugin = self.make_plugin("demo")
        self.write_marketplace([])
        report = vp.Report()
        vp.check_marketplace(report, [plugin])
        self.assertEqual(codes(report), ["PLUGIN_NOT_LISTED"])

    def test_listed_missing_on_disk(self):
        self.write_marketplace([{"name": "ghost"}])
        report = vp.Report()
        vp.check_marketplace(report, [])
        self.assertEqual(codes(report), ["PLUGIN_MISSING_ON_DISK"])

    def test_source_not_found(self):
        plugin = self.make_plugin("demo")
        self.write_marketplace([{"name": "demo", "source": "./plugins/gone"}])
        report = vp.Report()
        vp.check_marketplace(report, [plugin])
        self.assertEqual(codes(report), ["SOURCE_NOT_FOUND"])


class TestNormalizeThenValidate(ValidatorTestCase):
    """Integration: the normalizer's output must satisfy the validator."""

    def setUp(self):
        super().setUp()
        self._np_orig = (np.REPO_ROOT, np.PLUGINS_DIR)
        np.REPO_ROOT = self.root
        np.PLUGINS_DIR = self.plugins

    def tearDown(self):
        np.REPO_ROOT, np.PLUGINS_DIR = self._np_orig
        super().tearDown()

    def test_messy_plugin_becomes_valid(self):
        plugin = self.plugins / "messy"
        (plugin / "skills").mkdir(parents=True)
        (plugin / "skills" / "core.md").write_text(
            "# Core Thing\n\nDoes the core thing.\n", encoding="utf-8"
        )
        changes = np.Changes(dry_run=False)
        changes.record = lambda m: changes.entries.append(m)  # type: ignore[method-assign]
        np.normalize_plugin(plugin, changes)

        report = vp.Report()
        vp.check_plugin(report, plugin)
        self.assertEqual(
            [str(f) for f in report.errors], [], "normalized plugin still has errors"
        )


if __name__ == "__main__":
    unittest.main()
