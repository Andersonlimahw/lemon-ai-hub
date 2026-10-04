#!/usr/bin/env python3
"""bench.py + report.py, fully offline: fake CLI targets and a fake judge."""

import contextlib
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN / "scripts"))
import bench  # noqa: E402
from report import render  # noqa: E402

REF = PLUGIN / "tests" / "ref"
ALL_EIGHT = json.dumps({"scores": {d["id"]: 8 for d in bench.DEFAULT_RUBRIC}, "notes": "solid"})


class ParseOutputTests(unittest.TestCase):
    def test_claude_json(self):
        out = bench.parse_output("claude-json", json.dumps({
            "result": "ok", "total_cost_usd": 0.0868,
            "usage": {"input_tokens": 9, "cache_creation_input_tokens": 43305, "cache_read_input_tokens": 0, "output_tokens": 38}}))
        self.assertEqual((out["text"], out["input_tokens"], out["output_tokens"], out["cost_usd"]), ("ok", 43314, 38, 0.0868))

    def test_codex_jsonl_ignores_log_noise(self):
        stdout = "\n".join([
            '{"type":"thread.started","thread_id":"x"}',
            "2026-10-04T05:09:16Z ERROR rmcp::transport::worker: worker quit",
            '{"type":"item.completed","item":{"id":"i0","type":"agent_message","text":"ok"}}',
            '{"type":"turn.completed","usage":{"input_tokens":30903,"cached_input_tokens":6912,"output_tokens":5}}'])
        out = bench.parse_output("codex-jsonl", stdout)
        self.assertEqual((out["text"], out["input_tokens"], out["output_tokens"], out["cost_usd"]), ("ok", 30903, 5, None))

    def test_gemini_json_sums_every_model(self):
        stdout = "warning line\n" + json.dumps({"response": "ok", "stats": {"models": {
            "a": {"tokens": {"prompt": 100, "candidates": 3, "thoughts": 7}},
            "b": {"tokens": {"prompt": 50, "candidates": 1, "thoughts": 0}}}}}, indent=2)
        out = bench.parse_output("gemini-json", stdout)
        self.assertEqual((out["text"], out["input_tokens"], out["output_tokens"]), ("ok", 150, 11))

    def test_gemini_error_is_surfaced(self):
        out = bench.parse_output("gemini-json", json.dumps({"error": {"message": "quota exhausted"}}))
        self.assertEqual(out["text"], "ERROR: quota exhausted")

    def test_opencode_json_strips_think_and_counts_cache(self):
        stdout = "\n".join([
            '{"type":"text","part":{"type":"text","text":"<think>\\nhmm\\n</think>\\n\\nok"}}',
            '{"type":"step_finish","part":{"tokens":{"input":100,"output":2,"reasoning":20,"cache":{"write":0,"read":1339}},"cost":0.07}}'])
        out = bench.parse_output("opencode-json", stdout)
        self.assertEqual((out["text"], out["input_tokens"], out["output_tokens"], out["cost_usd"]), ("ok", 1439, 22, 0.07))

    def test_garbage_falls_back_to_raw_text(self):
        out = bench.parse_output("claude-json", "not json at all")
        self.assertEqual((out["text"], out["input_tokens"]), ("not json at all", None))


class RenderCmdTests(unittest.TestCase):
    def test_stdin_when_no_placeholder(self):
        cmd, stdin = bench.render_cmd("claude -p --model {model}", "hi 'there'", Path("/p"), Path("/w"), "m1")
        self.assertEqual((cmd, stdin), ("claude -p --model m1", "hi 'there'"))

    def test_prompt_is_shell_quoted(self):
        cmd, stdin = bench.render_cmd("tool run {prompt}", "a'; rm -rf / #", Path("/p"), Path("/w"), "")
        self.assertIsNone(stdin)
        self.assertEqual(cmd, "tool run 'a'\"'\"'; rm -rf / #'")


class ScoringTests(unittest.TestCase):
    def run_(self, passed, judge=None, status="ok"):
        return {"status": status, "checks": [{"passed": p} for p in passed],
                "judge": {"score": judge} if judge is not None else None}

    def test_blend_and_drop_missing_parts(self):
        w = bench.DEFAULT_WEIGHTS
        self.assertAlmostEqual(bench.run_score(self.run_([True, False], 80), w), 0.6 * 50 + 0.4 * 80)
        self.assertEqual(bench.run_score(self.run_([True, True]), w), 100)
        self.assertEqual(bench.run_score(self.run_([], 70), w), 70)
        self.assertEqual(bench.run_score(self.run_([True], 90, status="timeout"), w), 0)

    def test_tiers(self):
        self.assertEqual([bench.tier(s) for s in (95, 80, 79.9, 60, 45, 10, None)], ["A", "A", "B", "B", "C", "D", None])


class EndToEndTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(PLUGIN / "examples", self.tmp / "suite")
        cfg = json.loads((self.tmp / "suite" / "quick-suite.json").read_text())
        perfect = (f"cp {REF}/duration.py {REF}/test_duration.py . 2>/dev/null; "
                   f"[ -f slugify.py ] && cp {REF}/slugify.py {REF}/test_slugify.py .; "
                   "printf 'working...\\nANSWER: 443\\n'")
        cfg["targets"] = [
            {"id": "perfect", "label": "Perfect </script><script>alert(1)</script>", "provider": "ref", "cmd": perfect,
             "price": {"input": 1, "output": 1}},
            {"id": "lazy", "label": "Lazy", "provider": "ref", "cmd": "cat >/dev/null; echo 'ANSWER: 7'"},
            {"id": "slow", "label": "Slow", "provider": "other", "cmd": "sleep 5", "timeout": 1},
        ]
        cfg["judge"] = {"label": "fake judge", "cmd": f"cat >/dev/null; echo '{ALL_EIGHT}'"}
        self.cfg = self.tmp / "suite" / "quick-suite.json"
        self.cfg.write_text(json.dumps(cfg))
        self.out = self.tmp / "out"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_bench(self, *extra):
        with contextlib.redirect_stdout(io.StringIO()) as so, contextlib.redirect_stderr(io.StringIO()):
            rc = bench.main(["run", str(self.cfg), "-o", str(self.out), *extra])
        return rc, so.getvalue()

    def test_full_pipeline(self):
        rc, md = self.run_bench()
        self.assertEqual(rc, 0)
        res = json.loads((self.out / "results.json").read_text())
        summ = res["summary"]["*"]
        self.assertEqual(summ["perfect"]["pass_rate"], 100.0)
        self.assertEqual(summ["perfect"]["tier"], "A")
        self.assertEqual(summ["perfect"]["dims"]["correctness"], 8.0)
        self.assertLess(summ["lazy"]["score"], 60)
        self.assertEqual(summ["slow"]["score"], 0)
        self.assertEqual(summ["slow"]["failures"], 3)
        self.assertIn("| 1 | Perfect", md)
        # the reasoning task opted out of the judge
        math = [r for r in res["runs"] if r["task"] == "shipping-math"]
        self.assertTrue(all(r["judge"] is None for r in math))
        # judge is blind: the target label never reaches its prompt
        jp = (self.out / "runs" / "perfect" / "parse-duration" / "r1" / "judge" / "prompt.md").read_text()
        self.assertNotIn("Perfect", jp)
        self.assertIn("duration.py", jp)

        html = (self.out / "report.html").read_text()
        self.assertNotIn("</script><script>alert", html)
        data = re.search(r'<script type="application/json" id="bench-data">(.*?)</script>', html, re.S).group(1)
        self.assertEqual(json.loads(data)["name"], "Quick coding suite")
        self.assertNotIn("__BENCH_", html)

    def test_resume_reuses_finished_runs(self):
        self.run_bench("--targets", "lazy", "--no-judge")
        marker = self.out / "runs" / "lazy" / "parse-duration" / "r1" / "run.json"
        run = json.loads(marker.read_text())
        run["seconds"] = 123.0
        marker.write_text(json.dumps(run))
        self.run_bench("--targets", "lazy", "--no-judge", "--resume")
        res = json.loads((self.out / "results.json").read_text())
        self.assertIn(123.0, [r["seconds"] for r in res["runs"]])

    def test_dry_run_executes_nothing(self):
        rc, md = self.run_bench("--dry-run")
        self.assertEqual(rc, 0)
        self.assertIn("[perfect × parse-duration r1]", md)
        self.assertFalse(self.out.exists())

    def test_render_is_standalone(self):
        self.run_bench("--targets", "lazy", "--tasks", "shipping-math", "--no-judge")
        html = render(json.loads((self.out / "results.json").read_text()))
        self.assertNotRegex(html, r'<(script|link)[^>]+(src|href)="https?://')


if __name__ == "__main__":
    unittest.main()
