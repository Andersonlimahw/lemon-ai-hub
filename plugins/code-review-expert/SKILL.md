---
name: code-review-expert
description: Run both thermo-nuclear review (security/correctness) and thermo-nuclear-code-quality-review (maintainability/structure) subagents in parallel, then synthesize findings. Use for full-spectrum branch audits combining bug/security and code-quality passes. The plugin also includes `code-review-adversary` for interactive, mentor-style senior-vs-junior PR reviews.
---

# Code Review Expert Suite

The Code Review Expert suite provides deep, rigorous code review tools. It includes two primary modes of operation: the autonomous parallel `code-review-expert` review, and the interactive mentor-style `code-review-adversary` review.

## 1. Code Review Expert Parallel Audit (Autonomous)

Launch the two thermo review passes as async background subagents in parallel, then synthesize results.

### Workflow
1. Determine review scope from user request, PR, current branch, or changed files.
2. Gather diff + file context needed for reviewers.
3. Launch both subagents in parallel:
   - `thermo-nuclear-review-subagent` — bugs, breakages, security, devex regressions, feature-flag leaks
   - `thermo-nuclear-code-quality-review-subagent` — maintainability, structure, file-size, spaghetti, abstractions
4. Pass each the same scoped diff/context.
5. After both finish, synthesize: findings first, deduplicated, overlapping findings weighted more heavily.

## 2. Code Review Adversary (Interactive Mentoring)

Use `code-review-adversary` when the user wants a strict, expert-grade review framed as a Senior Engineer reviewing a Junior Developer. It offers interactive configuration (model, criticality, inline PR comments) and focuses on teaching the "why" behind every finding.

## Skills Included

| Skill | Description |
|-------|-------------|
| `thermo-nuclear-review` | Deep branch audit (bugs, breakages, security, devex, feature-flag leaks) |
| `thermo-nuclear-code-quality-review` | Strict maintainability audit (code-judo, 1k-line rule, spaghetti, boundaries) |
| `code-review-expert` | Run both review subagents in parallel and synthesize |
| `code-review-adversary` | Adversarial code review where the reviewer plays a senior software engineer teaching a junior developer |

## Usage

**For an autonomous double-pass audit (`code-review-expert`):**
Gather git diff main...HEAD and full contents of changed files. Invoke both `thermo-nuclear-*` subagents in one message with `run_in_background: true`. Synthesize prioritized, deduped findings.

**For a mentoring review (`code-review-adversary`):**
Gather the diff and prompt the user interactively (Scope, Model, Criticality, Inline comments) if not already specified, then generate a single comprehensive report or inline PR comments.
