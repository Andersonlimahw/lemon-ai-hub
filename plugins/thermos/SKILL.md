---
name: thermos
description: Run both thermo-nuclear review (security/correctness) and thermo-nuclear-code-quality-review (maintainability/structure) subagents in parallel, then synthesize findings. Use for full-spectrum branch audits combining bug/security and code-quality passes.
---

# Thermos

Launch the two thermo review passes as async background subagents in parallel, then synthesize results.

## Workflow

1. Determine review scope from user request, PR, current branch, or changed files.
2. Gather diff + file context needed for reviewers.
3. Launch both subagents in parallel:
   - `thermo-nuclear-review-subagent` — bugs, breakages, security, devex regressions, feature-flag leaks
   - `thermo-nuclear-code-quality-review-subagent` — maintainability, structure, file-size, spaghetti, abstractions
4. Pass each the same scoped diff/context.
5. After both finish, synthesize: findings first, deduplicated, overlapping findings weighted more heavily.

## Skills Included

| Skill | Description |
|-------|-------------|
| `thermo-nuclear-review` | Deep branch audit (bugs, breakages, security, devex, feature-flag leaks) |
| `thermo-nuclear-code-quality-review` | Strict maintainability audit (code-judo, 1k-line rule, spaghetti, boundaries) |
| `thermos` | Run both review subagents in parallel and synthesize |

## Usage

Invoke via task agent with both subagents:

```
Gather git diff main...HEAD and full contents of changed files.
Invoke both subagents in one message with run_in_background: true.
Synthesize prioritized, deduped findings.
```
