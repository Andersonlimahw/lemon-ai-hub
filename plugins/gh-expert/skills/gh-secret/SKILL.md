---
name: gh-secret
description: Manage GitHub Secrets for repos, orgs, and environments via gh CLI.
---

# GitHub Secret Skill

Set, list, and remove secrets for repositories, organizations, and environments.

## Capabilities
- List repo secrets: `gh secret list --repo <owner/repo>`
- Set repo secret: `gh secret set <name> --body "<value>" --repo <owner/repo>`
- Set from file: `gh secret set <name> < <file> --repo <owner/repo>`
- Delete repo secret: `gh secret remove <name> --repo <owner/repo>`
- Org secrets: `gh secret list --org <org>`
- Set org secret: `gh secret set <name> --body "<value>" --org <org>`
- Org visibility: `gh secret set <name> --org <org> --visibility <all|private|selected>`
- Environment secrets: `gh secret set <name> --env <env> --repo <owner/repo>`
- List environment secrets: `gh secret list --env <env> --repo <owner/repo>`
- Remove environment secret: `gh secret remove <name> --env <env> --repo <owner/repo>`

## Usage
Triggered when user says "secret", "set secret", "github secret", "add environment secret".
ALWAYS use `--body` with caution — secrets appear in shell history. Prefer file input for sensitive values.
Prefer reading from files rather than inline body to avoid shell history exposure.
