---
name: documentation-sync-loop
description: >
  Documentation Sync Loop. Goal: keep docs truthful — no drift between code and the docs/guardrails that agents rely on.
---

# Documentation Sync Loop

**Goal:** keep `docs/` truthful — no drift between code and the docs/guardrails that agents rely on.
**Cadence:** per merge / weekly.

## Phase 0 · IDEA
- Detect drift via git logs and `/graphify` comparing changed modules vs their docs.
- Candidate drifts: new repositories with no rules, renamed folders, outdated guardrails.
- **verify:** concrete list of drifted docs.

## Phase 1 · PLAN
- Inline plan: list `<doc path> → <action>`.
- **verify:** mapped to concrete actions.

## Phase 2 · IMPLEMENT
- Use `llm-wiki-curator` to enforce LLM-wiki standards (front-matter on all .md, regenerate llms.txt).
- Update specific rules/guardrails that drifted.
- **verify:** valid front-matter on touched docs; `llms.txt` generated.

## Phase 3 · TEST
- Validate link and structure integrity.
- Run `rtk npm run build:docs`.
- **verify:** zero broken links; docs build succeeds.

## Phase 4 · QUALITY GATE
- `rtk npm run build:docs` must pass (mirrors CI).
- **verify:** docs build green.

## Phase 5 · SHIP
- Create PR: "docs: weekly sync".
- Check CI jobs.
- **verify:** CI green (esp. Build Documentation).

## Phase 6 · REFLECT
- Append to `ITERATION_LOG.md`: which docs drifted and why.
- If same doc keeps drifting, create a hook or reminder (Never-Repeat).
- **verify:** recurring drift sources flagged for automation.
