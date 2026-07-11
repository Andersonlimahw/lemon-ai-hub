---
name: git-tag
description: Manage lightweight and annotated git tags.
---

# Git Tag Skill

Create, list, delete, and manage git tags for releases and milestones.

## Capabilities
- List tags: `git tag` or `git tag -l "pattern*"`
- Create lightweight tag: `git tag <name>`
- Create annotated tag: `git tag -a <name> -m "message"`
- Create signed tag: `git tag -s <name> -m "message"`
- Tag specific commit: `git tag <name> <commit>`
- Delete local tag: `git tag -d <name>`
- Push tag: `git push origin <name>`
- Push all tags: `git push --tags`
- Delete remote tag: `git push --delete origin <name>`
- View tag details: `git show <name>`
- Checkout tag: `git checkout <name>` (detached HEAD warning)

## Usage
Triggered when user says "tag", "create release tag", "list tags", "delete tag".
Use annotated tags (`-a`) for releases and milestones. Warn about force-pushing tags.
