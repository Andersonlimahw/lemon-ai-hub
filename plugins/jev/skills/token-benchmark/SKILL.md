---
name: token-benchmark
description: Measure baseline versus typed-decision pipelines using comparable token, call, latency, cost, retry, and quality data; generate honest Markdown reports and slides.
---

# Token Benchmark

## Required experiment design

1. Define same task set, inputs, acceptance criteria, concurrency, warmup, and sample count.
2. Capture one JSONL row per run using `references/usage-ledger.schema.json`; pair variants by `case_id`, pin tokenizer and evaluator versions, and keep provider/model/evidence constant within each variant.
3. Record actual provider usage when available. Otherwise label estimate and document tokenizer/method.
4. Compare total input/output/cached/reasoning tokens, calls, latency median/p95, schema retries, parse failures, task accuracy/calibration, and USD using dated price snapshot.
5. Do not compare token counts across different tokenizers as if units were identical. Show calls, latency, cost, and quality beside tokens.
6. Run `python3 scripts/benchmark.py runs.jsonl --baseline baseline --candidate typed --output report.md --slides slides.md` (Python standard library only).
7. Review generated report/slides; add methodology, limitations, and decision.

## Claim policy

- `measured`: observed in this experiment.
- `estimated`: derived from disclosed tokenizer or price assumptions.
- `vendor_claimed`: quoted claim with source/date; never present as reproduced result.

TypeSafe MCA may restrict publication of service benchmarks. Treat Jev results as internal/private unless legal terms and written permission allow publication. Provider-neutral local comparisons remain subject to each provider's terms.

Do not optimize tokens alone. A cheaper invalid decision is regression.
