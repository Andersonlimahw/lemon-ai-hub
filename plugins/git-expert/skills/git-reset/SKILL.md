---
name: git-reset
description: Reset HEAD to a specified state, unstage files, or undo commits.
---

# Git Reset Skill

Reset the current HEAD to a specified state with three modes of operation.

## Capabilities
- Soft reset (keep changes staged): `git reset --soft <commit>`
- Mixed reset (unstage changes): `git reset --mixed <commit>` (default)
- Hard reset (discard changes): `git reset --hard <commit>` ⚠️ destructive
- Unstage file: `git reset HEAD <file>`
- Reset to HEAD: `git reset HEAD~1` (undo last commit)
- Keep working tree: `git reset --keep <commit>`
- Reset to remote: `git reset --hard origin/<branch>`
- Merge reset: `git reset --merge <commit>`

## Usage
Triggered when user says "reset", "unstage", "undo commit", "discard changes".
Warn before `--hard` — changes are unrecoverable (use reflog as safety net).
Prefer `--soft` or `--mixed` on shared branches. For shared branches, `git revert` is safer.
