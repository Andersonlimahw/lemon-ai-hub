import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTest(unittest.TestCase):
    def test_generates_report_and_slides(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            slides = Path(directory) / "slides.md"
            subprocess.run(["python3", str(ROOT / "scripts/benchmark.py"), str(ROOT / "tests/fixtures/runs.jsonl"), "--baseline", "baseline", "--candidate", "typed", "--output", str(report), "--slides", str(slides)], check=True)
            text = report.read_text(encoding="utf-8")
            self.assertIn("Input tokens", text)
            self.assertIn("Evidence labels", text)
            slide_text = slides.read_text(encoding="utf-8")
            self.assertIn("```mermaid", slide_text)
            self.assertIn("# Method and guardrails", slide_text)

    def test_rejects_missing_required_field(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.jsonl"
            source.write_text(json.dumps({"variant": "baseline"}) + "\n", encoding="utf-8")
            result = subprocess.run(["python3", str(ROOT / "scripts/benchmark.py"), str(source), "--baseline", "baseline", "--candidate", "typed", "--output", str(Path(directory) / "out.md")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing", result.stderr)

    def test_rejects_non_finite_and_bool(self):
        for value in ("NaN", "true"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "bad.jsonl"
                source.write_text('{"experiment":"x","variant":"baseline","case_id":"c","run_id":"r","provider":"p","model":"m","calls":1,"latency_ms":' + value + ',"evidence":"measured"}\n', encoding="utf-8")
                result = subprocess.run(["python3", str(ROOT / "scripts/benchmark.py"), str(source), "--baseline", "baseline", "--candidate", "typed", "--output", str(Path(directory) / "out.md")], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)

    def test_rejects_unpaired_cases(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "unpaired.jsonl"
            rows = [
                {"experiment":"x","variant":"baseline","case_id":"a","run_id":"b","provider":"p","model":"m","model_version":"1","tokenizer":"t","evaluator":"e","evaluator_version":"1","calls":1,"latency_ms":1,"evidence":"measured"},
                {"experiment":"x","variant":"typed","case_id":"z","run_id":"t","provider":"p","model":"m","model_version":"1","tokenizer":"t","evaluator":"e","evaluator_version":"1","calls":1,"latency_ms":1,"evidence":"measured"},
            ]
            source.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            result = subprocess.run(["python3", str(ROOT / "scripts/benchmark.py"), str(source), "--baseline", "baseline", "--candidate", "typed", "--output", str(Path(directory) / "out.md")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("case_id", result.stderr)


if __name__ == "__main__":
    unittest.main()
