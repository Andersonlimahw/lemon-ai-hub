---
name: git-cherry-pick
description: Cherry-pick commits from one branch to another.
---

# Git Cherry-Pick Skill

Apply specific commits from one branch onto the current branch.

## Capabilities
- Cherry-pick single commit: `git cherry-pick <commit>`
- Cherry-pick range: `git cherry-pick <start>..<end>`
- Cherry-pick with no commit: `git cherry-pick --no-commit <commit>`
- Add sign-off: `git cherry-pick -s <commit>`
- Edit commit message: `git cherry-pick -e <commit>`
- Abort on conflict: `git cherry-pick --abort`
- Continue after resolve: `git cherry-pick --continue`
- Skip commit: `git cherry-pick --skip`

## Usage
Triggered when user says "cherry-pick", "pick commit X to this branch", "backport".
Mention the source commit hash and explain what changes are being moved.
