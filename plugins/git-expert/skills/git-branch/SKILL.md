---
name: git-branch
description: Manage git branches with listing, creation, deletion, and rename operations.
---

# Git Branch Skill

Create, list, rename, and delete branches across local and remote.

## Capabilities
- List branches: `git branch`
- List all (including remotes): `git branch -a`
- List with last commit: `git branch -v`
- List merged branches: `git branch --merged`
- List unmerged branches: `git branch --no-merged`
- Create branch: `git branch <name>` or `git branch <name> <start-point>`
- Create and switch: `git checkout -b <name>` or `git switch -c <name>`
- Delete branch: `git branch -d <name>` (safe)
- Force delete: `git branch -D <name>` (unmerged)
- Rename branch: `git branch -m <old> <new>`
- Move branch: `git branch -M <old> <new>` (force rename)
- Set upstream: `git branch -u <remote>/<branch>`
- Show current branch: `git branch --show-current`
- Delete remote branch: `git push origin --delete <branch>`

## Usage
Triggered when user says "branch", "create branch", "list branches", "delete branch", "rename branch".
Always check current branch before deleting. Warn about deleting unmerged branches.
