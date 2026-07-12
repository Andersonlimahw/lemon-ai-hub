---
name: gh-repo
description: Manage GitHub repositories via gh CLI.
---

# GitHub Repository Skill

Create, clone, fork, list, view, edit, and manage repositories.

## Capabilities
- Create repo: `gh repo create <name> --public|--private --add-readme --gitignore <type> --license <license>`
- Create from template: `gh repo create <name> --template <owner/repo>`
- Clone repo: `gh repo clone <owner/repo> [directory]`
- Fork repo: `gh repo fork <owner/repo> --clone --remote`
- List repos: `gh repo list <owner> --limit <n> --language <lang> --topic <topic>`
- View repo: `gh repo view <owner/repo> --json <fields>` or `--web`
- Edit repo: `gh repo edit <owner/repo> --description "<desc>" --homepage "<url>" --default-branch <branch>`
- Archive repo: `gh repo archive <owner/repo> --yes`
- Unarchive: `gh repo unarchive <owner/repo> --yes`
- Delete repo: `gh repo delete <owner/repo> --yes` ⚠️ irreversible
- Rename repo: `gh repo edit <owner/repo> --name <new-name>`
- Sync fork: `gh repo sync <owner/repo> --branch <branch> [--force]`
- Deploy key: `gh repo deploy-key add <key-file>` / `list` / `delete <id>`
- Read file: `gh repo read-dir <path>` / `gh repo read-file <path>`
- Set default repo: `gh repo set-default <owner/repo>`
- View license: `gh repo license view`
- View gitignore: `gh repo gitignore view <type>`

## Usage
Triggered when user says "repo", "repository", "create repo", "fork", "clone repo", "delete repo".
Always verify repo name before destructive operations like delete or archive.
