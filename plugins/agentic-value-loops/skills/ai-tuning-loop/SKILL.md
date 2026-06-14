---
name: ai-tuning-loop
description: >
  AI Tuning Loop. Goal: raise chat answer quality for one agent + category per iteration.
---

# AI Tuning Loop

**Goal:** raise chat answer quality for one agent + category per iteration.
**Cadence:** per agent / category.

## Phase 0 · IDEA
- Find the gap using `vc-evals-auditor` for a target agent and category.
- **verify:** a named gap with concrete examples (not just "make it better").

## Phase 1 · PLAN
- Write `docs/features/chat/training/<run-name>.md`.
- Detail the gap, current score, target score, batch size.
- Hard guardrails: NO hard-coded scores, NO fabricated `source_model`, NO duplicate Q&A, mandatory PII scrubbing.
- **verify:** plan cites gap, target metric, and guardrails.

## Phase 2 · IMPLEMENT
- Run real generator and evaluator scripts (e.g. `financial-qa:generate`, `financial-qa:evaluate`).
- Avoid running massive parallel batches locally to prevent OOM.
- **verify:** batch generated, every item has a computed score.

## Phase 3 · TEST
- Validate schema (`financial-qa:validate`).
- Import and register staging data into DB (`financial-qa:import`, `financial-qa:register`).
- **verify:** 0 validation errors; rows registered; deduplication respected.

## Phase 4 · QUALITY GATE
- Run the evals (`eval:financial-qa`).
- Re-run `vc-evals-auditor` from Phase 0.
- Check security / prompt injections.
- **verify:** target category score improved; guardrails intact.

## Phase 5 · SHIP
- Promote production sessions to corpus (`holo:promote`).
- Create PR: "feat(ai): tune <agent>/<category> +<delta> eval".
- **verify:** CI green; corpus delta reviewed.

## Phase 6 · REFLECT
- Append `ITERATION_LOG.md`: eval delta, cost, near-misses.
- Queue next weakest category for Phase 0.
- Reconcile local state with DB.
- **verify:** gap closed, next category queued, state reconciled.
