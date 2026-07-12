---
name: git-switch
description: Switch between branches with safety checks.
---

# Git Switch Skill

Switch git branches using the modern `git switch` command.

## Capabilities
- Switch to branch: `git switch <branch>`
- Create and switch: `git switch -c <new-branch>`
- Create from commit: `git switch -c <new-branch> <commit>`
- Detach HEAD: `git switch --detach <commit>`
- Switch to previous: `git switch -` (dash for previous branch)
- Force switch: `git switch -f <branch>` (discard local changes)
- Switch with merge: `git switch -m <branch>` (merge local changes)
- Show progress: `git switch --progress <branch>`

## Usage
Triggered when user says "switch branch", "checkout branch", "change branch", "go to branch".
Warn about uncommitted changes before switching. Use `-` to toggle between two branches.
