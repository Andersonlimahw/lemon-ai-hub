#!/usr/bin/env python3
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
HUB_ROOT = PLUGIN_ROOT.parents[1]
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"
VALIDATOR = SCRIPTS_DIR / "validate_catalog.py"
RENDERER = SCRIPTS_DIR / "render_agents.py"
INSTALLER = SCRIPTS_DIR / "install_worker_matrix.py"
SYNCER = SCRIPTS_DIR / "sync_provider_matrix.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SmartSubAgentsCatalogTests(unittest.TestCase):
    def run_cli(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, check=False)

    def validate_catalog(self, catalog: object) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(catalog, f)
            catalog_path = Path(f.name)
        try:
            return self.run_cli(VALIDATOR, "--catalog", str(catalog_path))
        finally:
            catalog_path.unlink(missing_ok=True)

    def test_catalog_is_valid(self) -> None:
        result = self.run_cli(VALIDATOR)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"\d+ providers")
        self.assertIn("harnesses", result.stdout)

    def test_decision_router_contract_is_model_agnostic_fail_open_and_calibrated(self) -> None:
        catalog = json.loads((PLUGIN_ROOT / "references" / "provider-matrix.json").read_text(encoding="utf-8"))
        routing = catalog["decisionRouting"]
        contract = routing["scoreContract"]
        self.assertEqual(routing["defaultMode"], "heuristic")
        self.assertNotIn("engines", routing)
        self.assertEqual(contract["output"], "typed-option-probabilities")
        self.assertTrue(contract["requiresCalibration"])
        self.assertEqual(contract["failureTier"], "balanced")
        self.assertTrue(routing["sharedState"]["reusePrefix"])
        self.assertTrue(routing["sharedState"]["batchIndependentCriteria"])

    def test_invalid_decision_confidence_gate_fails_closed(self) -> None:
        catalog = json.loads((PLUGIN_ROOT / "references" / "provider-matrix.json").read_text(encoding="utf-8"))
        catalog["decisionRouting"]["scoreContract"]["confidenceGate"] = 1.2
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(catalog, f)
            catalog_path = Path(f.name)
        try:
            result = self.run_cli(VALIDATOR, "--catalog", str(catalog_path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("confidenceGate", result.stderr)
        finally:
            catalog_path.unlink(missing_ok=True)

    def test_malformed_decision_objects_fail_without_traceback(self) -> None:
        source = json.loads((PLUGIN_ROOT / "references" / "provider-matrix.json").read_text(encoding="utf-8"))
        mutations = (
            ("decisionRouting", lambda catalog: catalog.__setitem__("decisionRouting", None)),
            ("scoreContract", lambda catalog: catalog["decisionRouting"].__setitem__("scoreContract", None)),
            ("sharedState", lambda catalog: catalog["decisionRouting"].__setitem__("sharedState", None)),
            ("safetyFloor", lambda catalog: catalog["decisionRouting"].__setitem__("safetyFloor", None)),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected):
                catalog = json.loads(json.dumps(source))
                mutate(catalog)
                result = self.validate_catalog(catalog)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_invalid_decision_safety_fields_fail_closed(self) -> None:
        source = json.loads((PLUGIN_ROOT / "references" / "provider-matrix.json").read_text(encoding="utf-8"))
        mutations = (
            ("confidenceGate", lambda routing: routing["scoreContract"].__setitem__("confidenceGate", True)),
            ("requiresCalibration", lambda routing: routing["scoreContract"].__setitem__("requiresCalibration", False)),
            ("tasks", lambda routing: routing["safetyFloor"].__setitem__("tasks", [])),
            ("tasks", lambda routing: routing["safetyFloor"].__setitem__("tasks", ["legal", "legal"])),
            ("tasks", lambda routing: routing["safetyFloor"].__setitem__("tasks", ["legal", 7])),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected):
                catalog = json.loads(json.dumps(source))
                mutate(catalog["decisionRouting"])
                result = self.validate_catalog(catalog)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)

    def test_router_contract_is_lossless_across_pipeline(self) -> None:
        senior = (HUB_ROOT / "plugins" / "senior-prompt-engineer" / "SKILL.md").read_text(encoding="utf-8")
        selector = (HUB_ROOT / "plugins" / "skills-selector" / "SKILL.md").read_text(encoding="utf-8")
        dispatch = (HUB_ROOT / "plugins" / "smart-dispatch" / "SKILL.md").read_text(encoding="utf-8")
        subagents = (PLUGIN_ROOT / "SKILL.md").read_text(encoding="utf-8")

        match = re.search(r"^intent:\s+<([^>]+)>", senior, re.MULTILINE)
        self.assertIsNotNone(match)
        senior_intents = {intent.strip() for intent in match.group(1).split("|")}
        intent_table = selector.split("### 1a. Classify", 1)[1].split("Ambiguous?", 1)[0]
        selector_intents = set(re.findall(r"^\| `([^`]+)`\s+\|", intent_table, re.MULTILINE))
        expected_intents = {
            "plan", "design-ui", "build-code", "fix-bug", "refactor", "review", "test", "git-op",
            "debug", "docs", "research", "data", "content", "media", "mcp-or-skill", "config-harness",
            "ops", "trivial-or-chat",
        }
        self.assertEqual(senior_intents, expected_intents)
        self.assertEqual(selector_intents, expected_intents)

        for document in (senior, selector, dispatch, subagents):
            for field in ("router:", "router_mode:", "router_confidence:", "router_fallback:"):
                self.assertIn(field, document)
        route_match = re.search(r"```text\n(ROUTE-MAP v1.*?)\n```", subagents, re.DOTALL)
        self.assertIsNotNone(route_match)
        route_contract = route_match.group(1)
        self.assertIn("provider_fallback:", route_contract)
        self.assertIn("router_fallback:", route_contract)
        self.assertNotRegex(route_contract, r"(?m)^fallback:")

        route_agent = (PLUGIN_ROOT / "agents" / "smart-route.md").read_text(encoding="utf-8")
        decision_reference = (PLUGIN_ROOT / "references" / "decision-routing.md").read_text(encoding="utf-8")
        order_contracts = (
            (subagents, "Apply an explicit user route override", "Otherwise, if confidence", "Apply `decisionRouting.safetyFloor`"),
            (route_agent, "Apply an explicit user route override", "Without an explicit override, fail open", "Apply the safety floor"),
            (decision_reference, "Apply an explicit user route", "Without an explicit route, fail open", "Apply safety floors"),
        )
        for policy, explicit, fallback, floor in order_contracts:
            self.assertLess(policy.index(explicit), policy.index(fallback))
            self.assertLess(policy.index(fallback), policy.index(floor))

    def test_sol_route_renders(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "codex", "--provider", "openai", "--model", "gpt-5.6-sol", "--effort", "xhigh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('model = "gpt-5.6-sol"', result.stdout)
        self.assertIn('model_reasoning_effort = "xhigh"', result.stdout)

    def test_alias_normalizes_lunce_to_luna(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "codex", "--model", "gpt-5.6 lunce", "--effort", "low")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('model = "gpt-5.6-luna"', result.stdout)

    def test_deepseek_route_keeps_thinking_mapping(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "opencode", "--provider", "deepseek", "--model", "deepseek-v4-flash", "--effort", "max")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("deepseek/deepseek-v4-flash", result.stdout)
        self.assertIn("thinking=true", result.stdout)

    def test_user_examples_normalize_harness_and_provider_aliases(self) -> None:
        examples = (
            (("--harness", "codex", "--provider", "openai", "--model", "l 5.6 lunce", "--effort", "max"), "gpt-5.6-luna"),
            (("--harness", "opencode", "--provider", "opencode", "--model", "kimi k3", "--effort", "low"), "moonshotai/kimi-k2"),
            (("--harness", "claude-code", "--provider", "anthropic", "--model", "Opus %", "--effort", "medium"), "claude-opus-5"),
            (("--harness", "opencode", "--provider", "deepseek api", "--model", "deepseek v4 flash", "--effort", "max"), "deepseek/deepseek-v4-flash"),
            (("--harness", "opencode", "--provider", "google", "--model", "Gemini 3.5 Pro", "--effort", "high"), "google/gemini-2.5-pro"),
        )
        for arguments, expected in examples:
            with self.subTest(expected=expected):
                result = self.run_cli(RENDERER, *arguments)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)

    def test_all_harnesses_render_to_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_cli(RENDERER, "--harness", "all", "--profile", "balanced", "--output-dir", temp_dir)
            self.assertEqual(result.returncode, 0, result.stderr)
            for harness in ("claude-code", "codex", "opencode", "antigravity", "gemini-cli", "lemon-code"):
                self.assertTrue((Path(temp_dir) / harness).exists(), harness)

    def test_unknown_model_fails_closed(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "opencode", "--provider", "openai", "--model", "gpt-5.6-lunce")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown model", result.stderr)

    def test_worker_matrix_tier_mismatch_fails_closed(self) -> None:
        """Regression: a workerMatrix family tier that disagrees with the model's
        own canonical tier must fail validation. Otherwise a family can silently
        route budget-tier volume to a quality-priced model (or vice versa) — the
        exact cost-leak vector reported against opencode-go/zen worker families
        pointing at Anthropic/OpenAI-owned model ids."""
        catalog = json.loads((PLUGIN_ROOT / "references" / "provider-matrix.json").read_text(encoding="utf-8"))
        for lane in catalog["workerMatrix"]["opencode"]["lanes"].values():
            for family in lane["families"]:
                if family["id"] == "zen_opus":
                    family["tier"] = "budget"  # tamper: claude-opus-5 is quality
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(catalog, f)
            catalog_path = Path(f.name)
        try:
            result = self.run_cli(VALIDATOR, "--catalog", str(catalog_path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("tier", result.stderr)
            self.assertIn("does not match", result.stderr)
        finally:
            catalog_path.unlink(missing_ok=True)


class InstallHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SCRIPTS_DIR))
        cls.installer = _load_module("install_worker_matrix", INSTALLER)

    def test_slug_normalizes_punctuation(self) -> None:
        self.assertEqual(self.installer.slug("Go Luna #1!"), "go_luna_1")

    def test_worker_name_format(self) -> None:
        self.assertEqual(self.installer.worker_name("go_luna", "high"), "go_luna_worker_high")

    def test_load_catalog_fails_closed_on_invalid_matrix(self) -> None:
        bad = {
            "schemaVersion": 99,
            "updated": "not-a-date",
            "efforts": [],
            "harnesses": {},
            "providers": [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(bad, f)
            catalog_path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                self.installer.load_catalog(catalog_path)
        finally:
            catalog_path.unlink(missing_ok=True)


class SyncHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SCRIPTS_DIR))
        cls.syncer = _load_module("sync_provider_matrix", SYNCER)

    def test_tier_guess_minimax_is_balanced(self) -> None:
        self.assertEqual(self.syncer.tier_guess("minimax-m3"), "balanced")

    def test_tier_guess_flash_is_budget(self) -> None:
        self.assertEqual(self.syncer.tier_guess("gemini-3.6-flash"), "budget")

    def test_tier_guess_sol_is_quality(self) -> None:
        self.assertEqual(self.syncer.tier_guess("gpt-5.6-sol"), "quality")


if __name__ == "__main__":
    unittest.main()
