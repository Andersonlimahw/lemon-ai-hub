---
name: git-reflog
description: Recover lost commits and manage the reference log.
---

# Git Reflog Skill

Track and recover commits that are no longer reachable from any branch or tag.

## Capabilities
- View reflog: `git reflog` or `git log -g`
- Show reflog for specific ref: `git reflog show <ref>`
- View reflog with dates: `git reflog --date=iso`
- Recover lost commit: `git checkout <reflog-hash>` then create branch
- Reset to reflog entry: `git reset --hard HEAD@{n}`
- View specific entry: `git show HEAD@{n}`
- Expire reflog: `git reflog expire --expire=30.days --all`
- Delete reflog entries: `git reflog delete HEAD@{n}`
- Stash reflog: `git reflog show refs/stash`

## Usage
Triggered when user says "reflog", "lost commit", "recover deleted branch", "undo reset".
First check reflog, then use `git checkout -b <new-branch> <hash>` to restore lost work.
