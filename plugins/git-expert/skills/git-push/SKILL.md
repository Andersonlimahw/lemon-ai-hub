---
name: git-push
description: Push commits to remote repositories.
---

# Git Push Skill

Push local branch commits to remote repositories with safety options.

## Capabilities
- Push to remote: `git push origin <branch>`
- Push current branch: `git push`
- Set upstream: `git push -u origin <branch>`
- Push all branches: `git push --all origin`
- Push tags: `git push --tags`
- Force push: `git push --force` ⚠️ destructive
- Force with lease: `git push --force-with-lease` (safer force)
- Delete remote branch: `git push origin --delete <branch>`
- Push to specific remote: `git push <remote> <branch>`
- Dry run: `git push --dry-run`
- Push and set upstream: `git push --set-upstream origin <branch>`

## Usage
Triggered when user says "push", "push to remote", "upload commits".
Prefer `--force-with-lease` over `--force`. Warn before force-pushing shared branches.
Use `-u` for first push of a new branch.
