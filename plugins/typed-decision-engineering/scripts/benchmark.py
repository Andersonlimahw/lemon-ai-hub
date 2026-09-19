#!/usr/bin/env python3
"""Summarize provider-neutral JSONL usage into Markdown report and slides."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

NUMERIC = ("calls", "input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens", "latency_ms", "cost_usd", "schema_retries", "parse_failures", "quality_score")
EVIDENCE = {"measured", "estimated", "vendor_claimed"}
REQUIRED = {"experiment", "variant", "case_id", "run_id", "provider", "model", "model_version", "tokenizer", "evaluator", "evaluator_version", "calls", "latency_ms", "evidence"}
ALLOWED = REQUIRED | {"input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens", "cost_usd", "schema_retries", "parse_failures", "quality_score", "price_snapshot_date", "notes"}
INTEGER_FIELDS = {"calls", "input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens", "schema_retries", "parse_failures"}


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = (len(ordered) - 1) * fraction
    low, high = math.floor(index), math.ceil(index)
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (index - low)


def load_rows(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid JSON constant {value}")))
        missing = REQUIRED - row.keys()
        extra = row.keys() - ALLOWED
        if missing or extra:
            detail = f"missing {sorted(missing)}" if missing else f"unknown {sorted(extra)}"
            raise ValueError(f"line {line_number}: {detail}")
        if row["evidence"] not in EVIDENCE:
            raise ValueError(f"line {line_number}: invalid evidence")
        for key in REQUIRED - {"calls", "latency_ms"}:
            if key != "evidence" and (not isinstance(row[key], str) or not row[key]):
                raise ValueError(f"line {line_number}: {key} must be non-empty string")
        for key in NUMERIC:
            if key in row and (isinstance(row[key], bool) or not isinstance(row[key], (int, float)) or not math.isfinite(row[key]) or row[key] < 0):
                raise ValueError(f"line {line_number}: {key} must be finite non-negative number")
            if key in row and key in INTEGER_FIELDS and not isinstance(row[key], int):
                raise ValueError(f"line {line_number}: {key} must be integer")
        rows.append(row)
    if not rows:
        raise ValueError("no benchmark rows")
    return rows


def summarize(rows: list[dict]) -> dict:
    result = {"runs": len(rows), "evidence": sorted({r["evidence"] for r in rows})}
    for key in NUMERIC:
        values = [float(r[key]) for r in rows if key in r]
        if values:
            result[key] = statistics.mean(values)
    latencies = [float(r["latency_ms"]) for r in rows]
    result["latency_p50_ms"] = percentile(latencies, 0.50)
    result["latency_p95_ms"] = percentile(latencies, 0.95)
    return result


def delta(base: float, candidate: float) -> str:
    if base == 0:
        return "n/a"
    return f"{((candidate - base) / base) * 100:+.1f}%"


def render(name: str, baseline: dict, candidate: dict, baseline_name: str, candidate_name: str) -> str:
    metrics = [
        ("Calls / run", "calls"), ("Input tokens / run", "input_tokens"), ("Output tokens / run", "output_tokens"),
        ("Cached tokens / run", "cached_tokens"), ("Reasoning tokens / run", "reasoning_tokens"),
        ("Latency p50 ms", "latency_p50_ms"), ("Latency p95 ms", "latency_p95_ms"),
        ("Cost USD", "cost_usd"), ("Schema retries", "schema_retries"),
        ("Parse failures", "parse_failures"), ("Mean quality", "quality_score"),
    ]
    lines = [f"# {name}", "", f"Runs: `{baseline_name}` {baseline['runs']}; `{candidate_name}` {candidate['runs']}.", "", "| Metric | Baseline | Candidate | Delta |", "|---|---:|---:|---:|"]
    for label, key in metrics:
        b, c = baseline.get(key), candidate.get(key)
        if b is None or c is None:
            lines.append(f"| {label} | {'n/a' if b is None else f'{b:.3f}'} | {'n/a' if c is None else f'{c:.3f}'} | n/a |")
        else:
            lines.append(f"| {label} | {b:.3f} | {c:.3f} | {delta(b, c)} |")
    lines += ["", f"Evidence labels: baseline `{', '.join(baseline['evidence'])}`; candidate `{', '.join(candidate['evidence'])}`.", "", "> Token units may differ across providers/tokenizers. Validate quality and provider publication terms before claiming savings.", ""]
    return "\n".join(lines)


def render_slides(name: str, report: str, baseline: dict, candidate: dict) -> str:
    table = "\n".join(line for line in report.splitlines() if line.startswith("|"))
    return f"""# {name}

Typed-decision efficiency comparison

---

# Architecture

```mermaid
flowchart LR
  A[App] --> S[Typed spec] --> P[Provider adapter] --> V[Runtime validation]
  V --> C[Deterministic policy] --> X[Action]
  C --> F[Fallback / human]
  P -. usage .-> U[Ledger]
```

---

# Comparison ({', '.join(baseline['evidence'])} vs {', '.join(candidate['evidence'])})

{table}

---

# Method and guardrails

- Same paired `case_id` set; per-run means plus latency p50/p95.
- Preserve `measured`, `estimated`, and `vendor_claimed` labels.
- Token units may differ across providers/tokenizers.
- Quality gate before savings claim.
- Check provider terms before publication.

---

# Decision

Document adopt / revise / reject after quality and calibration review.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--slides", type=Path)
    args = parser.parse_args()
    rows = load_rows(args.input)
    groups = {name: [r for r in rows if r["variant"] == name] for name in (args.baseline, args.candidate)}
    if any(not group for group in groups.values()):
        raise ValueError("baseline and candidate variants must both exist")
    experiments = {r["experiment"] for r in rows}
    if len(experiments) != 1:
        raise ValueError("all rows must share one experiment")
    baseline_cases = {r["case_id"] for r in groups[args.baseline]}
    candidate_cases = {r["case_id"] for r in groups[args.candidate]}
    if baseline_cases != candidate_cases:
        raise ValueError("baseline and candidate must contain identical case_id sets")
    for variant, group in groups.items():
        case_ids = [row["case_id"] for row in group]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError(f"{variant} case_id values must be unique")
    run_ids = [r["run_id"] for r in rows]
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("run_id values must be unique")
    for variant, group in groups.items():
        for key in ("provider", "model", "model_version", "tokenizer", "evaluator", "evaluator_version", "evidence"):
            if len({row[key] for row in group}) != 1:
                raise ValueError(f"{variant} rows must use one {key}")
        if any("cost_usd" in row and "price_snapshot_date" not in row for row in group):
            raise ValueError(f"{variant} cost rows require price_snapshot_date")
    for key in ("tokenizer", "evaluator", "evaluator_version", "evidence"):
        if groups[args.baseline][0][key] != groups[args.candidate][0][key]:
            raise ValueError(f"baseline and candidate must use same {key}")
    for key in NUMERIC:
        baseline_coverage = {row["case_id"] for row in groups[args.baseline] if key in row}
        candidate_coverage = {row["case_id"] for row in groups[args.candidate] if key in row}
        if baseline_coverage != candidate_coverage or (baseline_coverage and baseline_coverage != baseline_cases):
            raise ValueError(f"metric {key} must cover every paired case or be absent")
    if any("cost_usd" in row for row in rows):
        dates = {row.get("price_snapshot_date") for row in rows}
        if len(dates) != 1:
            raise ValueError("cost comparison requires one shared price_snapshot_date")
    baseline_summary = summarize(groups[args.baseline])
    candidate_summary = summarize(groups[args.candidate])
    report = render(experiments.pop(), baseline_summary, candidate_summary, args.baseline, args.candidate)
    args.output.write_text(report, encoding="utf-8")
    if args.slides:
        args.slides.write_text(render_slides(args.input.stem, report, baseline_summary, candidate_summary), encoding="utf-8")


if __name__ == "__main__":
    main()
