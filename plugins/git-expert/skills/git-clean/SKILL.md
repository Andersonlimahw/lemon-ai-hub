---
name: git-clean
description: Remove untracked files and directories from working tree.
---

# Git Clean Skill

Clean the working tree by removing untracked files and directories.

## Capabilities
- Dry run (show what would be removed): `git clean -n`
- Remove untracked files: `git clean -f`
- Remove untracked directories: `git clean -fd`
- Remove ignored files too: `git clean -fx`
- Remove both untracked and ignored: `git clean -fdx`
- Interactive mode: `git clean -i`
- Exclude specific files: `git clean -e <pattern>`

## Usage
Triggered when user says "clean untracked", "remove untracked files", "clean working directory".
ALWAYS do a dry run (`-n`) first before actual removal. Warn about irreversible deletion.
