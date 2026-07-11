---
name: git-blame
description: Find who changed what lines and when.
---

# Git Blame Skill

Annotate files line-by-line to find the last commit that modified each line.

## Capabilities
- Blame file: `git blame <file>`
- Blame with date: `git blame --date=short <file>`
- Blame with email: `git blame -e <file>`
- Blame range: `git blame -L <start>,<end> <file>`
- Show raw contents: `git blame -s <file>` (supports author/timestamp)
- Blame since commit: `git blame <commit>.. <file>`
- Ignore whitespace: `git blame -w <file>`
- Show line count: `git blame --line-porcelain <file>`

## Usage
Triggered when user says "blame", "who changed this line", "find the commit that added this".
Use `-L` to target specific lines. Always show the commit hash, author, date, and line content.
