# Error Fixer Loop — Audit

<!-- Duplicate this template for each loop execution. Keep it short. -->

- **Date**: <YYYY-MM-DD HH:mm>
- **Status**: fixed | not-reproducible | blocked-needs-human | wontfix-not-repeatable
- **Failure**: <one sentence>
- **Root cause**: <one sentence>
- **Class**: procedure | missing-rule | missing-test | permission | observability | documentation

## Changes

| File | Lines | Why |
|---|---|---|
| path/to/file.ts | 42-58 | <one sentence> |

## Verification

| Command | Result | Excerpt |
|---|---|---|
| `pnpm test path/to/test` | pass | `1 passed` |
| `pnpm tsc --noEmit` | pass | `(no output)` |

## Rule persisted

- **Location**: `docs/rules/<topic>.md` | `AGENTS.md` | `SKILL.md` | `none`
- **Text**: `<one-line operational rule>`

## Residual risk

<one sentence, or "none">
