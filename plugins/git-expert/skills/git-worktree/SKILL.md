---
name: git-worktree
description: Manage multiple working trees for parallel branch development.
---

# Git Worktree Skill

Work on multiple branches simultaneously without stashing or cloning.

## Capabilities
- Add worktree: `git worktree add <path> <branch>`
- List worktrees: `git worktree list`
- Remove worktree: `git worktree remove <path>`
- Prune stale worktree references: `git worktree prune`
- Lock/unlock worktree: `git worktree lock|unlock <path>`
- Create worktree with new branch: `git worktree add -b <new-branch> <path> <base-branch>`

## Usage
Triggered when user says "worktree", "parallel branches", "work on X without switching", "add worktree".
Use `run_command` with `git worktree` subcommands.
See docs/rules/marketplace-sync.md for project-specific worktree conventions.
