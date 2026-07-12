---
name: gh-label
description: Manage GitHub issue/PR labels via gh CLI.
---

# GitHub Label Skill

Create, list, edit, delete, and clone labels across repositories.

## Capabilities
- List labels: `gh label list --repo <owner/repo> --limit <n>`
- Create label: `gh label create <name> --description "<desc>" --color "<hex-color>" --repo <owner/repo>`
- Edit label: `gh label edit <name> --name <new-name> --description "<desc>" --color "<hex-color>" --repo <owner/repo>`
- Delete label: `gh label delete <name> --repo <owner/repo> --yes`
- Clone labels: `gh label clone <source-repo> --target-repo <target-repo>`
- List with counts: `gh label list --limit <n> --repo <owner/repo> --json name,description,color,issuesCount,prsCount`
- Force color: Colors must be 6-digit hex (e.g., `"ff0000"`)

## Usage
Triggered when user says "label", "create label", "list labels", "manage labels", "clone labels".
Use consistent color schemes across repos. Good defaults: `"d73a4a"` (bug-red), `"a2eeef"` (enhancement-blue), `"7057ff"` (feature-purple).
