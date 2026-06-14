---
name: async-advisor
description: Async pattern CI gate and PR review. Detects promise pitfalls, race conditions, and unbounded parallelism in changed files. Posts inline PR comments with corrected code. Use when setting up async quality gates or reviewing a PR with complex async logic.
---

# Async Advisor Plugin

Catch async bugs in CI before they hit production.

## Commands

```
/async-advisor setup       — install ESLint async rules + pre-commit hook
/async-advisor pr          — check async patterns in current git diff
/async-advisor scan        — full codebase async audit
/async-advisor rules       — show all enforced rules with rationale
```

## ESLint Rules Configured

```json
{
  "no-floating-promises": "error",
  "no-misused-promises": "error",
  "await-thenable": "error",
  "require-await": "warn",
  "@typescript-eslint/no-explicit-any": "warn",
  "promise/always-return": "error",
  "promise/catch-or-return": "error"
}
```

## PR Inline Comments

On a PR touching `src/api/reports.ts`:

```
⚠️ Line 45: Unbounded Promise.all over large array
   Promise.all(reportIds.map(...)) — reportIds can be up to 5,000 items
   → Wrap with pLimit(20) to avoid connection pool exhaustion
   
   import pLimit from 'p-limit'
   const limit = pLimit(20)
   const results = await Promise.all(reportIds.map(id => limit(() => ...)))
```

```
❌ Line 89: Floating promise (swallowed rejection)
   sendEmail(user) — no await, no .catch()
   → Add: await sendEmail(user) OR sendEmail(user).catch(logger.error)
```

## CI Configuration

```yaml
- name: Async pattern check
  run: npx eslint src/ --rule 'no-floating-promises: error' --ext .ts,.tsx
```

Pairs with `/async-patterns` skill for deep interactive analysis.
