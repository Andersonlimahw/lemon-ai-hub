---
name: feature-flags
description: Feature flag registry management. Scans codebase for all flags, tracks age and rollout state, generates cleanup reports, and creates removal PRs for stale flags. Use when managing technical debt from old flags or auditing flag hygiene across the repo.
---

# Feature Flags Plugin

Registry + hygiene for all your feature toggles.

## Commands

```
/feature-flags registry       — list all flags found in codebase
/feature-flags stale          — flags that are 100% enabled >90 days (cleanup candidates)
/feature-flags cleanup <name> — generate PR removing a flag (keep enabled code path)
/feature-flags report         — markdown report of all flags with owner and age
```

## Flag Registry (auto-generated)

Scans for patterns: `FLAGS.X`, `isOn('...')`, `process.env.FLAG_*`, `variation('...')`

```
FLAG REGISTRY — 2026-06-14
============================
feat_new_checkout      100%   Active   Added: 2026-01-10  Owner: @checkout-team  ← STALE
exp_pricing_v2          50%   Active   Added: 2026-05-20  Owner: @growth
ops_disable_ai_recs      0%   Disabled Added: 2026-03-01  Owner: @ml-team
tmp_v3_migration       100%   Active   Added: 2026-02-15  Owner: @backend  ← STALE
```

## Stale Flag Report

Flag is "stale" when:
- Rollout is 100% AND age > 90 days, OR
- Rollout is 0% AND age > 30 days (was never turned on)

## Cleanup PR Generation

`/feature-flags cleanup feat_new_checkout` will:
1. Remove all `if (FLAGS.feat_new_checkout)` conditionals
2. Keep the enabled code path
3. Delete tests that test the disabled path
4. Open a PR with the changes

Pairs with `/feature-flag` skill for implementation guidance.
