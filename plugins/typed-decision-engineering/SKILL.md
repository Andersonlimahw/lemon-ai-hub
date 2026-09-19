---
name: typed-decision-engineering
description: Design model-agnostic workflows using narrow typed decisions, deterministic composition, uncertainty routing, and measured token/cost comparisons. Use for typed AI decisions, bounded choice/score/binary-probability questions, structured-output routing, token-efficiency benchmarks, or replacing fragile LM parsing.
---

# Typed Decision Engineering

Build provider-neutral decision pipelines: code owns control flow and side effects; models answer narrow typed questions about shared state.

## Route

1. Need question decomposition or confidence policy → read `skills/decision-design/SKILL.md`.
2. Need schemas, adapters, validation, retries, or fallbacks → read `skills/type-safe-contracts/SKILL.md`.
3. Need token/cost comparison, report, or slides → read `skills/token-benchmark/SKILL.md`.
4. For architecture background and terminology → read `references/decision-model-background.md`.

Load only relevant file. For end-to-end implementation, use all three skills in listed order.

## Invariants

- Keep deterministic rules, arithmetic, control flow, permissions, and side effects in code.
- Ask atomic independent questions together over one minimal shared state.
- Use a discriminated union: `choice`, `score`, or `noul`.
- Validate every model response at runtime. Static types alone do not validate network output.
- Treat probabilities/confidence as routing signals, never truth or authorization.
- Compose answers in pure code; use another call only for dependent questions or new evidence.
- Record provider/model/version/schema, calls, latency, tokens, retries, failures, and price snapshot.
- Never claim savings without comparable measured data. Label values `measured`, `estimated`, or `vendor_claimed`.

## Completion

Deliver validated decision spec, provider adapter boundary, deterministic policy, uncertainty fallback, eval cases, and usage report. If benchmarking, generate summary and slides with `scripts/benchmark.py`.
