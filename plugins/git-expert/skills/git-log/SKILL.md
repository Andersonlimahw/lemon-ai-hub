---
name: git-log
description: Inspect commit history with advanced filtering and formatting.
---

# Git Log Skill

Browse, filter, and format commit history with powerful options.

## Capabilities
- Basic log: `git log`
- One-line per commit: `git log --oneline`
- Graph view: `git log --graph --oneline --decorate --all`
- Filter by author: `git log --author="<name>"`
- Filter by date: `git log --after="2024-01-01" --before="2024-12-31"`
- Filter by file: `git log -- <file>`
- Search commit messages: `git log --grep="<pattern>"`
- Show diff stats: `git log --stat`
- Show patches: `git log -p`
- Show last N commits: `git log -n 5`
- Custom format: `git log --pretty=format:"%h %s %an %ar"`
- Range: `git log <branch1>..<branch2>`
- First parent: `git log --first-parent`
- Since ref: `git log --since="2 weeks ago"`

## Usage
Triggered when user says "show history", "git log", "see commits", "what changed".
Use `--oneline --graph --decorate` for concise tree view.
