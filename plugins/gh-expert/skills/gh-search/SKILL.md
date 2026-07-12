---
name: gh-search
description: Search GitHub for code, issues, PRs, repos, and more via gh CLI.
---

# GitHub Search Skill

Search across GitHub using powerful query syntax.

## Capabilities
- Search issues/PRs: `gh search issues "<query>" --owner <org> --repo <repo> --state <open|closed> --author <user>`
- Search code: `gh search code "<query>" --owner <org> --repo <repo> --language <lang> --extension <ext>`
- Search repos: `gh search repos "<query>" --owner <org> --topic <topic> --language <lang> --stars ">100"`
- Search PRs: `gh search prs "<query>" --state <open|closed> --author <user> --reviewer <user>`
- Search commits: `gh search commits "<query>" --author <user> --repo <repo>`
- Filter by labels: `gh search issues "<query>" --label "<label>"`
- Filter by date: Add to query: `created:>2024-01-01` or `updated:<2024-12-31`
- Filter by status: `is:open`, `is:closed`, `is:merged`, `is:unmerged`
- Limit results: `--limit <n>`
- JSON output: `--json <fields> --jq "<expression>"`

## Usage
Triggered when user says "search", "find code", "search issues", "search repositories".
Use specific scopes (`issues`, `code`, `repos`, `prs`) for targeted results.
GitHub search syntax supports `AND`, `OR`, `NOT` and parentheses for complex queries.
