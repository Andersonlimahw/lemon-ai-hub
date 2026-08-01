---
name: prompts-feedback-loops
description: Ready-to-paste prompts to run continuous validation and feedback loops — API test loops, exploratory browser QA, error-fix loops, metric optimization, and completion verification gates.
---

# Prompts — Feedback and quality loops

Recipes to turn "I think it works" into evidence. Golden rule of this track: **one loop driver at a time** — chain loops in sequence, never two owning the same cycle.

## R1 — API validation loop

**Skills:** `api-test-loop` + `verification-before-completion`
**When:** new or changed endpoints; you want proof via CURL, not opinion.

```text
Run api-test-loop on endpoints <list or route prefix>. Validate
REST practices, edge-case inputs (nulls, negatives, overflow,
injection), security, and output format via CURL. Log every
finding in findings.md with severity and a reproduction curl.
Apply surgical fixes and re-validate until all CRITICALs are
closed. Close out with verification-before-completion.
Success: findings.md with every CRITICAL closed, each with the
before/after proof curl.
```

## R2 — Exploratory browser QA

**Skills:** `chrome-qa-loop`
**When:** a live web app needs exploratory eyes, not an E2E suite.

```text
Run chrome-qa-loop on app <url>, using screen manifest
<path/config>. Explore each screen with the doc's context, produce
one markdown report per finding (severity, repro steps, evidence).
Don't fix anything yet — triage only.
Success: one report per finding, triageable without opening the
app; zero duplicate findings.
```

## R3 — Error-fix loop

**Skills:** `error-fixer-loop`
**When:** a build/test/typecheck broke and you want a fix + anti-regression rule, not a band-aid.

```text
Captured this failure: <paste exact stack/error>.
Run error-fixer-loop: investigate root cause → minimal fix →
verify with the same command that failed → persist the
anti-regression rule for this error pattern.
Success: verification command green + rule persisted; the diff
touches only what's necessary.
```

## R4 — Metric optimization loop

**Skills:** `karpathy-loop`
**When:** an objective metric exists (latency, bundle size, tokens, coverage) and you want autonomous improvement cycles.

```text
Run karpathy-loop with target: improve <metric> from <baseline> to
<goal> in <file/area>. Each cycle: hypothesis → minimal change →
measure with <measurement command> → keep or revert. Stop at <N>
cycles or at the goal.
Success: metric at goal (or best result after N cycles) with a log
of every cycle and a reproducible measurement.
```

## Recommended chaining

`chrome-qa-loop` (find) → `bug-diagnostics` (diagnose the tricky finding) → `error-fixer-loop` (fix with a rule). Sequence, never simultaneous — each stage hands off an artifact to the next.
