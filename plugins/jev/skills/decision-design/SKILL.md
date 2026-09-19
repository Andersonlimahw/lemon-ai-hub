---
name: decision-design
description: Decompose broad AI tasks into atomic Choice, Score, and Noul judgments; batch independent questions and compose results deterministically with confidence-aware routing.
---

# Decision Design

## Workflow

1. Write deterministic workflow first. Mark only steps needing judgment over unstructured data.
2. Define minimal shared `state`; exclude instructions unrelated to judgment.
3. Decompose each judgment into one atomic question:
   - `choice`: select exactly one declared option; return full distribution.
   - `score`: rate against ordered, described levels; return score and distribution.
   - `noul`: return probability statement is true. `0.5` means uncertainty, not medium intensity.
4. Batch independent questions against same state. Keep dependent questions in later calls.
5. Compose with code: thresholds, vetoes, weighted sums, ranking, or routing.
6. Define uncertainty bands by impact: auto-act, fallback model/tool, human review, or safe stop.
7. Test representative labeled cases; calibrate thresholds per pinned model/schema version.

## Question quality gate

- One semantic decision per question.
- Criteria/options exhaustive enough for intended route; include `unknown`/`other` when valid.
- No hidden calculation a deterministic function should perform.
- IDs correlate results only; meaning lives in instructions and criteria.
- State contains evidence, not desired answer.
- Security vetoes execute before convenience rules.

## Model-agnostic contract

Use canonical schema in `../../references/decision-spec.schema.json`. Provider-specific prompt/tool syntax belongs behind adapter boundary. Never invent calibrated confidence when provider supplies only a label; mark it unavailable and take configured fallback.
