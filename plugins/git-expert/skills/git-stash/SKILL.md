---
name: git-stash
description: Temporarily stash changes and manage the stash list.
---

# Git Stash Skill

Save uncommitted work temporarily and reapply it later.

## Capabilities
- Stash changes: `git stash push -m "message"` or `git stash save`
- Stash including untracked: `git stash -u` or `--include-untracked`
- Stash including all files: `git stash --all`
- List stashes: `git stash list`
- Pop stash: `git stash pop` (apply + drop)
- Apply stash: `git stash apply stash@{n}`
- Drop stash: `git stash drop stash@{n}`
- Show stash diff: `git stash show -p stash@{n}`
- Create branch from stash: `git stash branch <branch> stash@{n}`
- Clear all stashes: `git stash clear`

## Usage
Triggered when user says "stash", "save my changes", "temporarily put aside", "pop stash".
Use `run_command` with `git stash` subcommands.
