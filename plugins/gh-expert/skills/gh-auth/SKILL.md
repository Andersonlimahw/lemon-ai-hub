---
name: gh-auth
description: Manage GitHub CLI authentication via gh CLI.
---

# GitHub Auth Skill

Login, logout, refresh, and check authentication status for GitHub CLI.

## Capabilities
- Login: `gh auth login` (interactive) or `gh auth login --hostname <hostname> --with-token < <token-file>`
- Login with SSH: `gh auth login -p ssh`
- Login with browser: `gh auth login -w` (web-first flow)
- Logout: `gh auth logout [--hostname <hostname>]`
- Refresh token: `gh auth refresh --scopes "<scope1,scope2>"`
- Status: `gh auth status [--hostname <hostname>]`
- Token: `gh auth token [--hostname <hostname>]` (print the current auth token)
- Setup git: `gh auth setup-git` (configure git to use gh as credential helper)
- Switch account: `gh auth switch [--hostname <hostname>]`
- List hosts: `gh auth status` shows all authenticated hosts

## Scopes
Common scopes for `gh auth refresh`: `repo`, `read:org`, `admin:org`, `gist`, `project`, `workflow`, `write:packages`, `admin:repo_hook`, `admin:org_hook`

## Usage
Triggered when user says "auth", "login", "logout", "authentication", "gh token", "check auth".
Use `gh auth status` to verify authentication before running other commands.
Use `gh auth refresh --scopes` to add new permissions without re-logging in.
