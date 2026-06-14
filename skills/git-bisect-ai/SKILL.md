---
name: git-bisect-ai
description: AI-guided git bisect for finding the exact commit that introduced a bug or regression. Automates the binary search, interprets test results, and identifies the responsible code change with full context. Use when you know a bug exists now but didn't exist before, or when a performance regression appeared somewhere in git history.
---

# Git Bisect AI

Find the commit that broke it — without reading 500 commits manually.

## Quick Start

```
/git-bisect-ai                          — interactive bisect session
/git-bisect-ai --auto "npm test"        — fully automated with test command
/git-bisect-ai --good v2.1.0 --bad HEAD — specify known good/bad points
/git-bisect-ai --perf "p99 latency"    — performance regression bisect
```

## How It Works

Binary search through commits: `O(log n)` — 1000 commits = ~10 steps.

Claude will:
1. Ask for symptom + known good commit (or tag)
2. Run `git bisect start`
3. At each step: checkout commit → run test/check → mark good/bad
4. Identify the culprit commit
5. Explain what changed and why it likely caused the regression
6. Suggest targeted fix or revert strategy

## Workflow

### Interactive Mode
```
/git-bisect-ai

Claude: What's the regression?
You: The /checkout page returns 500 after a database query

Claude: When did it last work?
You: It was fine in the v3.2.0 release

Claude will:
  git bisect start
  git bisect bad HEAD
  git bisect good v3.2.0
  → [steps through 8 commits]
  → Found: commit abc1234
     "feat: add discount coupon support"
  → Changed: src/checkout/service.ts line 142
     Added raw SQL interpolation (SQL injection + syntax error in some locales)
```

### Automated Mode (with test script)
```bash
git bisect start
git bisect bad HEAD
git bisect good v3.2.0

# Claude generates and runs:
git bisect run bash -c '
  npm run build:quiet &&
  curl -s -o /dev/null -w "%{http_code}" \
    http://localhost:3000/api/checkout | grep -q 200
'
# Exits 0 = good, non-0 = bad
```

### Performance Regression Mode
```bash
/git-bisect-ai --perf

Claude measures p95 latency at each bisect step:
  Commit abc → p95: 95ms  (good)
  Commit def → p95: 850ms (bad)
  Commit ghi → p95: 102ms (good)
  → Culprit: commit def
     "refactor: extract UserService"
     Introduced N+1 query in user.findByEmail()
```

## Bisect Script Templates

### HTTP status check
```bash
git bisect run bash -c 'npm start &>/dev/null & sleep 3 && \
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health) && \
  kill %1 && [ "$STATUS" = "200" ]'
```

### Unit test
```bash
git bisect run npm test -- --testPathPattern="checkout.test.ts" --silent
```

### Build check
```bash
git bisect run npm run build 2>/dev/null
```

### Performance threshold
```bash
git bisect run bash -c '
  npm start &>/dev/null & sleep 3 &&
  LATENCY=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:3000/api/products) &&
  kill %1 &&
  echo "$LATENCY < 0.5" | bc -l | grep -q 1
'
```

## After Finding Culprit

Claude will show:
```
BISECT RESULT
==============
Culprit commit: abc1234f
Author: Jane Doe <jane@example.com>
Date: 2026-06-10 14:32 UTC
Message: "feat: add discount coupon support"

CHANGED FILES
  src/checkout/service.ts    (+47, -12)
  src/models/coupon.ts       (+120, -0)  ← NEW FILE

ROOT CAUSE (line 142 in service.ts)
  const query = `SELECT * FROM orders WHERE code = '${couponCode}'`
  ← SQL injection + breaks on quotes in coupon codes (e.g., "MOTHER'S-DAY")

OPTIONS
  1. Fix: Parameterize query → db.query('...WHERE code = $1', [couponCode])
  2. Revert: git revert abc1234f (creates new commit, safe for main)
  3. Cherry-pick fix onto v3.2.0 patch branch
```
