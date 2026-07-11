---
name: git-fetch
description: Fetch branches and history from remote repositories.
---

# Git Fetch Skill

Download objects and refs from remote repositories without merging.

## Capabilities
- Fetch from origin: `git fetch origin`
- Fetch all remotes: `git fetch --all`
- Fetch specific branch: `git fetch origin <branch>`
- Fetch with tags: `git fetch --tags`
- Fetch and prune: `git fetch --prune` (remove stale remote-tracking branches)
- Fetch with depth: `git fetch --depth <n>` (shallow fetch)
- Fetch specific refspec: `git fetch origin <src>:<dst>`
- Dry run: `git fetch --dry-run`
- Fetch all: `git fetch --all --prune`

## Usage
Triggered when user says "fetch", "git fetch", "check remote", "sync remote branches".
Safer than `git pull` — inspect fetched changes before merging.
Always used before `git log <remote>/<branch>` to check remote state.
