---
name: feature-development-loop
description: >
  Feature Development Loop. Goal: ship one new user-facing feature per iteration, fully behind the quality gate.
---

# Feature Development Loop

**Goal:** ship one new user-facing feature per iteration, fully behind the quality gate.
**Cadence:** per feature.

## Phase 0 · IDEA
- Ground in reality with `/graphify "..."` to check coupling.
- Score the bet with `/quantic "..."`.
- **verify:** hypothesis defined and quantic recommended proceed.

## Phase 1 · PLAN (SDD)
- Refine prompt and generate EXEC-MAP.
- Grill with docs.
- Draft design across specialists.
- Write the spec → `docs/features/<feature>/PLAN.md`.
- **verify:** every task has verify steps; success criteria are testable.

## Phase 2 · IMPLEMENT
- Generate types, validation, migrations, repository, actions, and components.
- Make surgical, atomic commits with `/git-save`.
- **verify:** code runs; diff is surgical.

## Phase 3 · TEST
- Build eval harness.
- Apply TDD for generation logic.
- Run `rtk vitest`.
- **verify:** tests green; eval cases pass.

## Phase 4 · QUALITY GATE
- `rtk npm run version:validate` — MUST exit 0.
- Perform code review / security review.
- Check guardrails.
- **verify:** `version:validate` exit 0, review passed.

## Phase 5 · SHIP
- `/git-save` and `/git-pr-create`.
- Verify PR checks in CI.
- **verify:** all CI checks green.

## Phase 6 · REFLECT
- Append to `ITERATION_LOG.md`.
- Update knowledge graph with `/graphify . --update`.
- Queue next idea.
- **verify:** log updated, next idea queued.
