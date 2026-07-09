---
name: pr-review-canvas
description: Render a PR diff review as an interactive walkthrough that groups changes by reviewer importance, separates boilerplate from core logic, and highlights tricky or unexpected code. Use when reviewing a pull request, summarizing a diff, or asking for a diff walkthrough.
---

# PR Review Canvas

Build an interactive review walkthrough that presents a PR diff reorganized for reviewer comprehension — not in file-tree order.

## Gather the Diff

Expect a GitHub PR link (full URL or `gh`-resolvable reference). Use `gh pr diff <pr>` to collect every file's path, additions, deletions, and hunks.

If the user didn't provide a PR link, stop and ask. Do not guess at the current branch.

## Group Changes for Comprehension

Reorganize into sections ordered by reviewer value:

1. **Core logic** — New behavior, algorithm changes, state transitions, API surface. Full diffs with context.
2. **Wiring & integration** — Route registration, DI, config plumbing. Condensed.
3. **Boilerplate & mechanical** — Renames, generated code, formatting. Summarized as a list.

## Distill Complex Logic

When a change involves dense logic, add a short pseudocode summary next to the diff.

## Trace Tricky Behavior

Pick a concrete input and walk it through both old and new code paths side-by-side for genuinely surprising behavior changes.

## Call Attention

Tag surprising/risky hunks with labels like "Subtle", "Breaking", "Race condition", "Perf" and a one-sentence explanation.

## Output

Generate an HTML page with categorized sections, diff views, and annotated findings.
