---
name: git-expert
description: Expert git plugin containing multiple skills for advanced version control, semantic commits, and bisect automation.
---

# Git Expert Plugin

This plugin provides a suite of advanced Git skills for autonomous agents to use when managing version control.
It follows the multi-skill architecture.

## Available Skills

- **git-bisect-ai**: AI-guided git bisect for finding the exact commit that introduced a bug or regression.
- **git-commit**: High-quality semantic commits based on the diff. Conventional commit standards.
- **git-merge**: Merge branches with strategy selection and conflict resolution.
- **git-worktree**: Manage multiple working trees for parallel branch development.
- **git-rebase**: Rebase branches with interactive editing and conflict resolution.
- **git-stash**: Temporarily stash changes and manage the stash list.
- **git-revert**: Safely revert commits by creating inverse commits.
- **git-cherry-pick**: Apply specific commits from one branch to another.
- **git-tag**: Create, list, delete, and manage lightweight and annotated tags.
- **git-remote**: Add, remove, rename, and inspect remote repository connections.
- **git-log**: Browse, filter, and format commit history with advanced options.
- **git-blame**: Find who changed what lines and when.
- **git-reflog**: Track and recover commits not reachable from any branch.
- **git-clean**: Remove untracked files and directories from working tree.
- **git-reset**: Reset HEAD, unstage files, or undo commits (soft/mixed/hard).
- **git-config**: Read and write git configuration at system/global/local levels.
- **git-hooks**: Install and manage client-side Git hooks for automation.
- **git-push**: Push commits to remote repositories with safety options.
- **git-pull**: Fetch and integrate remote changes into current branch.
- **git-fetch**: Download objects and refs from remotes without merging.
- **git-diff**: Show changes between commits, branches, and working tree.
- **git-branch**: Create, list, rename, delete, and manage branches.
- **git-switch**: Switch between branches with safety checks.
- **git-clone**: Clone repositories with depth, branch, and submodule options.
- **git-submodule**: Add, update, remove, and manage nested repositories.

## Usage

Use the specific skills when you need advanced git operations.
Example: `/git-commit` to trigger semantic commit generation.
Example: `/git-merge feature/main` to merge branches.
Example: `/git-worktree add ../hotfix hotfix/urgent` to create a worktree.
