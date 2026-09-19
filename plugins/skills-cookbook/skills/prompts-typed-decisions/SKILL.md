---
name: prompts-typed-decisions
description: Ready-to-paste prompts for model-agnostic typed decisions — atomic choice/score/binary-probability design, provider adapters, runtime validation, uncertainty routing, and comparable token/cost benchmarks.
---

# Prompts — Typed decisions

Recipes for typed decision engineering with any LM. Code owns control flow and side effects; models answer narrow typed questions. Use `typed-decision-engineering` as router, then name only needed sub-skills.

## R1 — Decompose a broad judgment

**Skills:** `typed-decision-engineering` + `decision-design`
**When:** a prompt asks one model to classify, score, explain, and decide an action in one response.

```text
Use typed-decision-engineering and decision-design to redesign
<current workflow> as atomic
typed judgments over <shared state>. Separate each judgment into
Choice, Score, or Noul; batch only independent questions; keep
calculations, permissions, side effects, and final routing in code.
Define explicit uncertainty routes for auto-act, fallback, human
review, and safe stop.
Success: every question tests one semantic decision; every output
has a deterministic consumer; dependent questions are in a later
round; no side effect is model-controlled.
```

## R2 — Add a provider-neutral typed boundary

**Skills:** `typed-decision-engineering` + `type-safe-contracts`
**When:** the same decision flow must work with native classifiers, JSON-schema/tool-calling LMs, or guarded JSON parsing.

```text
Use typed-decision-engineering and type-safe-contracts to implement
a provider-neutral
DecisionSpec and DecisionResult for <workflow>. Add adapters for
<providers/models>, runtime schema validation, semantic validation
(IDs/types, option membership, probability bounds/sum), one bounded
repair attempt, and an explicit low-confidence/invalid-output fallback.
Pin model and schema versions; redact secrets from raw audit data.
Success: identical contract tests pass for every adapter; malformed,
unknown-option, non-finite, and low-confidence fixtures take the
declared fallback without executing a side effect.
```

## R3 — Compare token/cost efficiency with slides

**Skills:** `typed-decision-engineering` + `token-benchmark`
**When:** deciding whether a typed-decision pipeline is cheaper/faster than a generative baseline.

```text
Use typed-decision-engineering and token-benchmark to compare
<baseline> against <candidate>
on paired cases from <dataset>. Capture provider/model/version,
tokenizer, evaluator/version, input/output/cached/reasoning tokens,
calls, latency, cost, retries, parse failures, and quality. Label each
value measured, estimated, or vendor_claimed. Generate report.md and
slides.md with Mermaid architecture, p50/p95, limitations, and an
adopt/revise/reject decision. Check provider benchmark-publication
terms before producing anything public.
Success: both variants cover identical unique case_ids; incompatible
tokenizers/evaluators/evidence are rejected; savings are claimed only
when quality passes and comparable measured data supports them.
```

## R4 — End-to-end typed decision migration

**Skills:** `decision-design` → `type-safe-contracts` → `token-benchmark`
**When:** replacing fragile free-text parsing or repeated agent calls with a controlled decision pipeline.

```text
Migrate <workflow> to typed decisions. First use decision-design to
extract atomic judgments and deterministic policy. Then use
type-safe-contracts to implement and validate provider adapters with
safe uncertainty routing. Finally use token-benchmark on <paired
evaluation set> and produce a private report + slide comparison.
Do not optimize tokens at the expense of semantic quality.
Success: representative evals pass; invalid outputs cannot reach side
effects; benchmark inputs are comparable; final decision cites quality,
tokens, calls, latency, cost, and limitations.
```

## See also

- `verification-before-completion` — final evidence gate after implementation.
- `prompts-feedback-loops` — continuous metric optimization after baseline calibration.
