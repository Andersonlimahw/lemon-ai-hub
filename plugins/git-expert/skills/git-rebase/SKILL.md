---
name: git-rebase
description: Rebase branches and manage interactive rebase sessions.
---

# Git Rebase Skill

Reapply commits on top of another base tip, with interactive editing.

## Capabilities
- Standard rebase: `git rebase <base-branch>`
- Interactive rebase: `git rebase -i <base>` (pick, reword, edit, squash, fixup, drop)
- Abort rebase on conflict: `git rebase --abort`
- Continue rebase after resolve: `git rebase --continue`
- Skip problematic commit: `git rebase --skip`
- Rebase onto different branch: `git rebase --onto <new-base> <old-base>`
- Auto-squash: `git rebase -i --autosquash <base>`
- Update branch with remote: `git rebase <remote>/<branch>`

## Usage
Triggered when user says "rebase", "interactive rebase", "squash commits", "edit commit history".
Always prefer rebase over merge for clean linear history. Warn about force-pushing rebased branches.
