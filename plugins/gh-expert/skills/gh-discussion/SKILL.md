---
name: gh-discussion
description: Manage GitHub Discussions via gh CLI.
---

# GitHub Discussion Skill

Create, list, view, edit, and comment on discussions.

## Capabilities
- List discussions: `gh discussion list --repo <owner/repo> --limit <n> --author <user>`
- View discussion: `gh discussion view <id> --repo <owner/repo>` or `gh discussion view --web`
- Create discussion: `gh discussion create --repo <owner/repo> --title "<title>" --body "<body>" --category "<category>"`
- Edit discussion: `gh discussion edit <id> --repo <owner/repo> --title "<title>" --body "<body>"`
- Comment: `gh discussion comment <id> --repo <owner/repo> --body "<body>"`
- List categories: Use `gh api repos/<owner>/<repo>/discussions/categories` to get available categories

## Usage
Triggered when user says "discussion", "create discussion", "list discussions", Q&A", "forum".
Requires discussions to be enabled in the repository. Use appropriate categories (Q&A, Ideas, General, etc.).
