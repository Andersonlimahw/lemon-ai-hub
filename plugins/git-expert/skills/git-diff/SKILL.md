---
name: git-diff
description: Show changes between commits, branches, and working tree.
---

# Git Diff Skill

Inspect differences in working tree, staging area, and between commits.

## Capabilities
- Working tree vs index: `git diff`
- Staged vs last commit: `git diff --staged` or `--cached`
- Between commits: `git diff <commit1> <commit2>`
- Between branches: `git diff <branch1> <branch2>`
- Specific file: `git diff -- <file>`
- Word diff: `git diff --word-diff`
- Stat summary: `git diff --stat`
- Name only: `git diff --name-only`
- Ignore whitespace: `git diff -w` or `--ignore-all-space`
- Show diff with context: `git diff -U<n>`
- Check for changes: `git diff --exit-code` (exit 0 if no changes)
- Diff cached: `git diff --cached`

## Usage
Triggered when user says "diff", "show changes", "what changed", "compare branches".
Use `--stat` for quick overview, `--name-only` for file list, full diff for detailed review.
