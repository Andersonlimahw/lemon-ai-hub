---
name: git-merge
description: Merge branches and resolve merge conflicts.
---

# Git Merge Skill

Merge one branch into another with conflict resolution and strategy selection.

## Capabilities
- Merge branches (`git merge <branch>`)
- Choose strategy: `--ff` (fast-forward), `--no-ff` (no fast-forward), `--squash`, `--ff-only`
- Abort merge on conflict: `git merge --abort`
- Resolve conflicts with `git mergetool` or manual editing
- Continue merge after resolving: `git merge --continue`
- View merge log: `git log --merge`
- Create merge commits with custom messages (`-m`)

## Usage
Triggered when user says "merge branch", "merge X into Y", "resolve conflicts", "squash merge".
Use `run_command` with `git merge` and appropriate flags.
