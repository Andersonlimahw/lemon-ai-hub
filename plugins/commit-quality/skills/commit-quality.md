---
name: commit-quality
description: Commit message linting, atomic commit enforcement, and changelog generation. Validates Conventional Commits format, warns on oversized diffs, detects mixed-concern commits, and generates changelog from history. Use when setting up commit standards, reviewing commit hygiene, or generating a release changelog.
---

# Commit Quality Plugin

Atomic commits. Consistent messages. Auto-changelog.

## Commands

```
/commit-quality setup          — install commitlint + husky hooks
/commit-quality lint           — check recent commits against Conventional Commits
/commit-quality analyze        — detect mixed-concern commits in current branch
/commit-quality split          — suggest how to split a large commit
/commit-quality changelog      — generate CHANGELOG from commits since last tag
```

## Conventional Commits Enforcement

Valid formats:
```
feat(checkout): add coupon code support
fix(auth): prevent session expiry on tab switch
chore(deps): upgrade React to 18.3.0
docs(api): update authentication section
perf(db): add composite index on orders table
refactor(user): extract UserService from controller
test(checkout): add coupon validation edge cases
```

## Lint Results

```
COMMIT QUALITY — last 5 commits
==================================
✅ feat(checkout): add coupon code support
✅ fix(auth): prevent session expiry
⚠️ "updated stuff and fixed things" — no type, no scope, no description
❌ "WIP" — work-in-progress commit on main branch (squash before merge)
⚠️ feat(checkout): add payment + fix bug + refactor service ← mixed concerns
    → Split into: feat(checkout), fix(payment), refactor(checkout)
```

## Mixed Concern Detection

```
/commit-quality analyze

Commit abc1234 touches:
  src/auth/service.ts       — auth concern
  src/payment/gateway.ts    — payment concern
  src/ui/Button.tsx         — UI concern
  tests/payment.test.ts     — test concern

→ 4 concerns in 1 commit
→ Suggested split:
  1. refactor(auth): extract token refresh logic
  2. fix(payment): handle gateway timeout
  3. style(ui): update Button hover state
  4. test(payment): add timeout edge case
```

## Changelog Generation

```
/commit-quality changelog v3.3.0..HEAD

## [3.4.0] — 2026-06-14

### Features
- **checkout**: add coupon code support (#142)
- **products**: add featured products filter (#138)

### Bug Fixes
- **auth**: prevent session expiry on tab switch (#145)
- **payment**: handle gateway timeout gracefully (#143)

### Performance
- **db**: add composite index on orders table (#140)
```

Pairs with `/git-save` and `/git-commit` skills for commit workflows.
