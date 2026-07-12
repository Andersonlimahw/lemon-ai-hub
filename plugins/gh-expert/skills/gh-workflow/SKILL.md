---
name: gh-workflow
description: Manage GitHub Actions workflows and runs via gh CLI.
---

# GitHub Workflow Skill

List, view, run, and manage GitHub Actions workflows.

## Capabilities
- List workflows: `gh workflow list --limit <n> --all|--enabled|--disabled`
- View workflow: `gh workflow view <id|name>` or `gh workflow view <id|name> --yaml` (show source YAML)
- Run workflow: `gh workflow run <id|name> --ref <branch> -f <key>=<value>`
- List runs: `gh run list --limit <n> --workflow <id|name> --branch <branch> --status <status>`
- View run: `gh run view <run-id> --log` or `gh run view --job <job-id>` or `gh run view --web`
- Cancel run: `gh run cancel <run-id>`
- Rerun run: `gh run rerun <run-id> --failed` (only failed jobs) or `gh run rerun <run-id>` (all)
- Download logs: `gh run download <run-id> [--dir <dir>]`
- Watch run: `gh run watch <run-id>` (live output)
- View workflow list: `gh workflow list`
- List artifacts: `gh run view <run-id> --log-failed`
- Download artifact: `gh run download <run-id>`

## Usage
Triggered when user says "workflow", "actions", "run workflow", "check CI", "view action run".
Use `--json` flag with `gh run list` to get structured data. Use `--branch` to filter runs.
