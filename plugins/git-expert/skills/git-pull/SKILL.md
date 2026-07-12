---
name: git-pull
description: Fetch from and integrate with remote repository.
---

# Git Pull Skill

Fetch changes from remote and integrate them into the current branch.

## Capabilities
- Pull from remote: `git pull origin <branch>`
- Pull current branch: `git pull`
- Pull with rebase: `git pull --rebase`
- Auto-stash: `git pull --autostash`
- Pull with no commit: `git pull --no-commit`
- Fast-forward only: `git pull --ff-only`
- Squash merge pull: `git pull --squash`
- Pull all remotes: `git pull --all`
- Verbose: `git pull --verbose`

## Usage
Triggered when user says "pull", "git pull", "update branch", "sync with remote".
Prefer `git pull --rebase` over default merge for clean linear history.
Check for local changes before pull — stash if necessary.
