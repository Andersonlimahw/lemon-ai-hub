---
name: gh-project
description: Manage GitHub Projects (beta) via gh CLI.
---

# GitHub Project Skill

Create, list, view, edit, and manage GitHub Projects items.

## Capabilities
- List projects: `gh project list --owner <org|user> --limit <n>`
- View project: `gh project view <number> --owner <org|user>` or `--web`
- Create project: `gh project create --owner <org|user> --title "<title>"`
- Close project: `gh project close <number> --owner <org|user>`
- Delete project: `gh project delete <number> --owner <org|user>`
- Edit project: `gh project edit <number> --title "<title>" --description "<desc>"` --readme "<readme>"
- Copy project: `gh project copy <number> --target-owner <org|user>` --title "<title>"
- Mark template: `gh project mark-template <number>`
- Link project: `gh project link <number> --repo <owner/repo>`
- Unlink project: `gh project unlink <number> --repo <owner/repo>`
- List items: `gh project item-list <number> --owner <org|user> --limit <n>`
- Add item: `gh project item-add <number> --owner <org|user> --url <issue|pr-url>`
- Create item: `gh project item-create <number> --owner <org|user> --title "<title>" --body "<body>"`
- Edit item: `gh project item-edit <number> --item-id <id>` --field <field> --value <value>
- Delete item: `gh project item-delete <number> --item-id <id>`
- Archive item: `gh project item-archive <number> --item-id <id>`
- List fields: `gh project field-list <number> --owner <org|user>`
- Create field: `gh project field-create <number> --name <name> --data-type <TEXT|SINGLE_SELECT|DATE|NUMBER|ITERATION>`
- Delete field: `gh project field-delete <number> --field-id <id>`

## Usage
Triggered when user says "project", "github projects", "add to project", "project board".
Use `item-list` with `--format json` for programmatic access to project data.
