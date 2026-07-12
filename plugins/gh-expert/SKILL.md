---
name: gh-expert
description: Expert GitHub CLI plugin containing multiple skills for PR management, issue tracking, and GitHub workflows automation.
---

# GitHub Expert Plugin

This plugin provides a suite of advanced GitHub CLI skills for autonomous agents to use when managing pull requests, issues, workflows, and GitHub resources.

## Available Skills

- **gh-pr**: Create, review, manage, and merge pull requests via `gh`.
- **gh-issue**: Create, list, view, close, reopen, edit, and comment on issues.
- **gh-release**: Create, list, view, edit, delete releases and manage assets.
- **gh-repo**: Create, clone, fork, list, view, edit, and manage repositories.
- **gh-codespace**: Create, list, connect to, stop, and manage codespaces.
- **gh-gist**: Create, list, view, edit, delete, and clone code snippets.
- **gh-project**: Manage GitHub Projects (beta) with items, fields, and views.
- **gh-workflow**: List, run, view, cancel, and manage GitHub Actions workflows.
- **gh-search**: Search code, issues, PRs, repos, and commits across GitHub.
- **gh-label**: Create, list, edit, delete, and clone issue/PR labels.
- **gh-secret**: Set, list, and remove secrets for repos, orgs, and environments.
- **gh-discussion**: Create, list, view, edit, and comment on discussions.
- **gh-org**: List organizations, members, and manage org-level operations.
- **gh-ruleset**: List, view, and check repository rulesets for branch protection.
- **gh-copilot**: Use GitHub Copilot CLI for command explanation and suggestion.
- **gh-config**: View and modify GitHub CLI configuration settings.
- **gh-browse**: Open repositories, files, settings, and more in the browser.
- **gh-auth**: Login, logout, refresh, and check authentication status.

## Usage

Use the specific skills when you need advanced GitHub operations via the GitHub CLI.
Example: `/gh-pr create` to trigger a PR creation workflow.
Example: `/gh-issue list --label bug` to list bug issues.
Example: `/gh-workflow run ci.yml --ref main` to run a workflow.
Read https://cli.github.com/manual/ for documentation on `gh`.
