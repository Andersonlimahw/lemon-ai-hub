# error-fixer-loop

Recursive error-fix loop. Every fixed error must reduce the chance of the same error returning.

## What it does

1. **Detects** build/test/typecheck errors in bash output (via cross-harness hooks).
2. **Captures** the failing command + output + cwd.
3. **Root-causes** in one sentence.
4. **Classifies** the failure (procedure / missing-rule / missing-test / permission / observability / documentation).
5. **Applies** the minimal fix.
6. **Verifies** with test + lint + typecheck.
7. **Persists** a one-line rule in `docs/rules/`, `AGENTS.md`, or this `SKILL.md` — depending on scope.
8. **Generates a fix-prompt artifact** in `.error-fixer-loop/<timestamp>-<slug>.md` following the `senior-prompt-engineer` format (Role/Context, Task, Inputs, Constraints, Plan with `→ verify:`, Output contract, Feedback DO/DON'T, `EXEC-MAP v1`). This makes the fix replayable and delegable across sessions and harnesses.
9. **Audits** with evidence. No audit + fix-prompt → loop not closed.

## Components

| Path | Purpose |
|---|---|
| `SKILL.md` | The recursive loop protocol (load on demand). |
| `agents/error-fixer-loop-runner.md` | Focused subagent that executes the protocol for one captured failure. |
| `hooks/error-fixer-loop-hook.sh` | Claude Code `PostToolUse` hook for `Bash`. |
| `hooks/error-fixer-loop.ts` | OpenCode plugin on `tool.execute.after`. |
| `scripts/install.sh` | Idempotent installer for both harnesses. |
| `scripts/detect-error.sh` | Standalone detector for CI / pre-push. |
| `templates/rule-entry.md` | Boilerplate for new `docs/rules/<topic>.md`. |
| `templates/audit.md` | Final audit report template. |
| `templates/fix-prompt.md` | Fix-prompt template (senior-prompt-engineer format). |
| `evals.json` | Eval cases defending the loop's invariants. |

## Output artifacts

Each loop execution produces:

| Artifact | Location | Purpose |
|---|---|---|
| Rule | `docs/rules/<topic>.md` or `AGENTS.md` | Persistent memory for the project |
| Fix-prompt | `.error-fixer-loop/<YYYYMMDD-HHMMSS>-<slug>.md` | Replayable/delegable prompt (senior-prompt-engineer format) |
| Audit | inline report + optional `docs/audits/` | Evidence trail |

Add `.error-fixer-loop/` to `.gitignore` if you don't want the artifacts versioned (recommended for local-only memory), or commit them to share learnings across the team.

## Install

```bash
# Both Claude Code and OpenCode
./scripts/install.sh

# Or pick one
./scripts/install.sh claude
./scripts/install.sh opencode
```

## Quick use

```
User: tests are failing with `Cannot find module '@/lib/auth'`
Agent (via hook reminder): runs error-fixer-loop →
  captures → root-cause → fixes → tests → writes rule in docs/rules/typescript.md
  → writes .error-fixer-loop/20260720-143022-module-not-found.md
  → audits
```

## Reference

- Article: https://lemon.dev.br/pt/blog/skill-recursiva-feedback-loop-harness
- Prompt format: `senior-prompt-engineer` skill (stage-0 refiner)
- Legacy: `error-fix-loop` (superseded — this plugin replaces it)
