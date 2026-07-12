---
name: gh-gist
description: Manage GitHub Gists via gh CLI.
---

# GitHub Gist Skill

Create, list, view, edit, delete, rename, and clone gists.

## Capabilities
- Create gist: `gh gist create <file> --desc "<description>" --public|--private`
- Create from stdin: `echo "<content>" | gh gist create --filename <name>`
- List gists: `gh gist list --limit <n> --public|--secret`
- View gist: `gh gist view <id> --raw` or `--files <filename>` or `--web`
- Edit gist: `gh gist edit <id> --add <file>` or `--remove <filename>`
- Delete gist: `gh gist delete <id>`
- Rename file: `gh gist edit <id> --rename <old>:<new>`
- Clone gist: `gh gist clone <id> <dir>`

## Usage
Triggered when user says "gist", "create gist", "share code snippet", "list gists".
Use `--public` for shareable snippets, `--secret` for private. Note: "secret" gists are still accessible via URL.
