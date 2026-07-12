---
name: git-revert
description: Safely revert commits by creating new inverse commits.
---

# Git Revert Skill

Undo commits safely by creating new commits that reverse the changes.

## Capabilities
- Revert single commit: `git revert <commit>`
- Revert multiple commits: `git revert <oldest..newest>`
- No-edit revert: `git revert --no-edit <commit>`
- Abort revert on conflict: `git revert --abort`
- Continue revert: `git revert --continue`
- Revert with custom message: `git revert -m <message> <commit>`
- Revert merge commit: `git revert -m <parent-number> <merge-commit>`

## Usage
Triggered when user says "revert commit", "undo commit safely", "rollback changes".
Prefer `git revert` over `git reset` for shared branches. Always explain what the revert will do.
