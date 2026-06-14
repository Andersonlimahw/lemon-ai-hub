---
name: maintenance-security-loop
description: >
  Maintenance & Security Loop. Goal: keep dependencies current and the app free of known vulnerabilities — one safe batch per iteration.
---

# Maintenance & Security Loop

**Goal:** keep dependencies current and the app free of known vulnerabilities — one safe batch per iteration.
**Cadence:** weekly.

## Phase 0 · IDEA
- Triage the risk surface: `npm audit`, `npm outdated`, check CI secrets jobs.
- Group findings into a coherent batch.
- **verify:** batch is scoped.

## Phase 1 · PLAN
- Write `docs/features/platform/maintenance/PLAN.md`.
- List each package target, severity, breaking changes.
- **verify:** explicit "no behaviour change" criterion.

## Phase 2 · IMPLEMENT
- Run safe semver-compatible fixes (`npm audit fix`).
- Explicitly bump major/pinned dependencies.
- Commit atomically per group.
- **verify:** `package-lock.json` updated; revert path clean.

## Phase 3 · TEST
- Run full unit suite (failures-only).
- Run E2E smoke tests for critical flows.
- **verify:** suites green WITHOUT editing tests (otherwise it's a behaviour change).

## Phase 4 · QUALITY GATE
- `rtk npm run version:validate` — MUST exit 0.
- Re-check `npm audit` for 0 high/critical.
- Security review for auth/payments adjacencies.
- **verify:** `version:validate` exit 0. Audit clean.

## Phase 5 · SHIP
- Create PR: "chore(deps): weekly security batch".
- Check CI jobs, specially Gitleaks/secret scan.
- **verify:** CI green, Gitleaks clean.

## Phase 6 · REFLECT
- Append to `ITERATION_LOG.md`: CVEs closed, deferred bumps, breakages (Never-Repeat).
- Set `overrides` if a transitive dep is stubborn.
- **verify:** log updated.
