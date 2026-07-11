---
name: gh-org
description: Manage GitHub organizations via gh CLI.
---

# GitHub Organization Skill

List organizations, members, and manage organization-level operations.

## Capabilities
- List org members: `gh org list --limit <n>`
- List members: `gh api orgs/<org>/members --jq '.[].login'`
- List outside collaborators: `gh api orgs/<org>/outside_collaborators`
- View org details: `gh api orgs/<org>`
- List org repos: `gh repo list <org> --limit <n>`
- List teams: Use `gh api orgs/<org>/teams`
- Check membership: `gh api orgs/<org>/members/<username>`
- List org secrets: `gh secret list --org <org>`
- Set org secret: `gh secret set <name> --org <org> --visibility <all|private|selected> --body "<value>"`

## Usage
Triggered when user says "org", "organization", "list org members", "org repos".
Use `gh api` for org operations not available as native gh commands.
