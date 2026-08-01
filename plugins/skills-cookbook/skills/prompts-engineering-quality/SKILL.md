---
name: prompts-engineering-quality
description: Ready-to-paste prompts for engineering quality — PR review with semantic commits, async-pattern audits, database indexing, security threat modeling, resilience/load testing, and i18n sync.
---

# Prompts — Engineering quality

Cross-cutting quality recipes. Hub-wide pattern that applies across this whole track: many pairs come as **one-shot × continuous** duos (`async-patterns`×`async-advisor`, `bundle-analyzer`×`bundle-watch`, `load-test`×`load-test-runner`, `chaos-test`×`chaos-runner`, `a11y-audit`×`a11y-guardian`). Use the one-shot to investigate/fix now; the continuous one as a CI gate. Never both as driver of the same pass.

## R1 — Full PR review

**Skills:** `code-review-expert` + `pr-review-canvas` + `commit-quality`
**When:** a significant PR needs a structured review, not a "LGTM".

```text
Review PR <number/branch> with code-review-expert; render the
findings with pr-review-canvas (inline comments per file:line).
Check commit hygiene with commit-quality (semantic messages,
per-commit scope).
Success: findings with severity + suggested fix each; commits off
the standard listed with a corrected message proposed.
```

## R2 — Async audit

**Skills:** `async-patterns`
**When:** timeouts, race conditions, memory leaks, or unbounded parallelism in async code.

```text
Audit <path> with async-patterns: races, promises without error
handling, N+1 async, unbounded parallelism, missing cancellation.
For each finding, the correct pattern (Promise.all, p-limit,
AbortController...) with the diff.
Success: each finding with a plausible reproduction + applicable
fix; then stabilize with async-advisor as a CI gate (not together).
```

## R3 — Database indexes and queries

**Skills:** `db-index-advisor` + `supabase-postgres-best-practices`
**When:** slow queries, full scans, or modeling doubts in Postgres.

```text
Analyze the slow queries of <app/schema> with db-index-advisor:
propose indexes with a justification per query. If Postgres/
Supabase, apply supabase-postgres-best-practices for modeling and
RLS.
Success: EXPLAIN ANALYZE before/after per optimized query; no
proposed index without a query that uses it.
```

## R4 — Feature threat model

**Skills:** `security-threat-model` + `security-best-practices` + `security-ownership-map`
**When:** a new feature touches auth, sensitive data, or an external surface.

```text
Threat-model <feature> with security-threat-model (actors,
surfaces, STRIDE). Validate mitigations against
security-best-practices and map owners per area with
security-ownership-map.
Success: table of threat → mitigation → owner; every HIGH threat
with a concrete mitigation or an explicitly accepted risk.
```

## R5 — Resilience under load and failure

**Skills:** `load-test` + `chaos-test`
**When:** ahead of production or an expected spike; validating SLOs under failure.

```text
Design with load-test the load test for <service> (profile
<RPS/duration>) and with chaos-test the failure experiments
(injected latency, dependency down, disk full) on
<dependencies>. Verify circuit breakers, retries, and fallbacks.
Success: report with target SLO vs. measured per scenario; every
resilience mechanism triggered at least once with evidence.
```

## R6 — Synced i18n

**Skills:** `i18n-audit` + `i18n-sync`
**When:** divergent locales, orphaned keys, or a new language coming in.

```text
Audit the locales of <project> with i18n-audit (missing keys,
orphaned keys, hardcoded strings) and sync with i18n-sync keeping
locales/{lang}.json structurally identical.
Success: zero key diff between languages; test in target language
<target> passing; no hardcoded strings on screens <screens>.
```

## See also

- `git-expert` (`/git-commit`, bisect) and `gh-expert` — the git/GitHub flow behind every review.
- `feature-purge` — remove an entire feature with no dead code left; `finishing-a-development-branch` — close a branch with quality.
- `incident-runbook` + `incident-center` — when quality failed in production.
- `code-smell` (one-shot) / `code-smell-detector` (continuous) — code smell in both cadences.
