---
name: bundle-watch
description: Bundle size CI gate and trend tracking. Compares bundle size of current branch vs main, posts PR comment with size diff, and blocks merge if budget is exceeded. Use when setting up bundle size enforcement or investigating a sudden size increase in CI.
---

# Bundle Watch Plugin

PR-level bundle size gating. No surprises in production.

## Commands

```
/bundle-watch setup              — configure CI gate + size budgets
/bundle-watch diff               — compare current branch bundle vs main
/bundle-watch budget <kb>        — set or update size budget
/bundle-watch history            — show bundle size trend over last 30 commits
/bundle-watch blame <chunk>      — find what commit caused a chunk to grow
```

## CI Setup (GitHub Actions)

```yaml
name: Bundle Size Check
on: [pull_request]
jobs:
  bundle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: andersonlimahw/bundle-watch-action@v1
        with:
          budget_kb: 200
          fail_on_exceed: true
```

## PR Comment Example

```
📦 Bundle Size Report

          main    PR      diff
─────────────────────────────
Total    284 KB  312 KB  +28 KB ❌ (budget: 300 KB)
/app     180 KB  195 KB  +15 KB
/checkout 48 KB   62 KB  +14 KB ⚠️

Top additions:
  + react-pdf  (+38 KB) — loaded eagerly, consider dynamic import
  - lodash-es  (-10 KB) — ✅ good removal
```

## Budget Configuration

```json
// bundle-watch.config.json
{
  "budgets": {
    "total": { "maxKB": 300, "warnKB": 250 },
    "/app": { "maxKB": 200 },
    "/checkout": { "maxKB": 60 }
  },
  "baseline": "main"
}
```

Pairs with `/bundle-analyzer` skill for deep analysis of violations.
