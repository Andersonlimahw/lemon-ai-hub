---
name: git-remote
description: Manage remote repositories and their connections.
---

# Git Remote Skill

Add, remove, rename, and inspect remote repository connections.

## Capabilities
- List remotes: `git remote -v`
- Show remote details: `git remote show <name>`
- Add remote: `git remote add <name> <url>`
- Remove remote: `git remote remove <name>`
- Rename remote: `git remote rename <old> <new>`
- Change URL: `git remote set-url <name> <new-url>`
- Change fetch URL: `git remote set-url --push <name> <url>`
- Prune stale remote branches: `git remote prune <name>`
- Update remote: `git remote update <name>`
- Get remote URL: `git remote get-url <name>`

## Usage
Triggered when user says "remote", "add remote", "change remote URL", "list remotes".
Always verify remote URLs before changing. Support SSH and HTTPS URL formats.
