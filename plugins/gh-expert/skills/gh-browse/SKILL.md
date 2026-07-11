---
name: gh-browse
description: Open GitHub resources in the browser via gh CLI.
---

# GitHub Browse Skill

Open repositories, issues, PRs, releases, settings, and more in the default browser.

## Capabilities
- Open repo: `gh browse --repo <owner/repo>`
- Open specific path: `gh browse src/index.ts --branch main` (opens file at branch)
- Open line range: `gh browse src/index.ts:10-20` (opens file scrolled to lines 10-20)
- Open issue: `gh issue view <number> --web`
- Open PR: `gh pr view <number> --web`
- Open release: `gh release view <tag> --web`
- Open repo settings: `gh browse --settings`
- Open wiki: `gh browse --wiki`
- Open projects: `gh browse --projects`
- Open actions: `gh browse --actions`
- Open security: `gh browse --security`
- Open pulse: `gh browse --pulse`
- Open releases: `gh browse --releases`
- Open branches: `gh browse --branches`
- Open contributors: `gh browse --contributors`
- Open specific branch: `gh browse --branch <branch>`

## Usage
Triggered when user says "open in browser", "browse repo", "show in GitHub", "open settings".
Use `--repo` flag to specify target repo when not in its local directory.
