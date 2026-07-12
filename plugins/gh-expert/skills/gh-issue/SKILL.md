---
name: gh-issue
description: Manage GitHub issues via gh CLI.
---

# GitHub Issue Skill

Create, list, view, close, reopen, edit, comment, and manage issues.

## Capabilities
- Create issue: `gh issue create --title "<title>" --body "<body>" --label "<labels>" --assignee "<user>"`
- List issues: `gh issue list --limit <n> --state <open|closed> --label "<label>" --assignee "<user>"`
- View issue: `gh issue view <number> --json <fields>` or `gh issue view --web`
- Close issue: `gh issue close <number> --reason <completed|not_planned>`
- Reopen issue: `gh issue reopen <number>`
- Edit issue: `gh issue edit <number> --title "<title>" --body "<body>" --add-label "<label>" --remove-label "<label>"`
- Comment: `gh issue comment <number> --body "<body>"`
- Lock/unlock: `gh issue lock <number>` / `gh issue unlock <number>`
- Pin/unpin: `gh issue pin <number>` / `gh issue unpin <number>`
- Transfer: `gh issue transfer <number> <repo>`
- List milestones: `gh issue list --milestone "<name>"`
- Search issues: `gh issue list --search "<query>"`
- View status: `gh issue status`

## Usage
Triggered when user says "issue", "create issue", "file a bug", "feature request", "list issues".
Use `gh issue view --json` with specific fields for machine-readable output.
