---
name: gh-codespace
description: Manage GitHub Codespaces via gh CLI.
---

# GitHub Codespace Skill

Create, list, view, connect to, and manage codespaces.

## Capabilities
- Create codespace: `gh codespace create --repo <owner/repo> --branch <branch> --machine <type>`
- List codespaces: `gh codespace list`
- View codespace: `gh codespace view [--codespace <name>]`
- Stop codespace: `gh codespace stop [--codespace <name>]`
- Delete codespace: `gh codespace delete [--codespace <name>]`
- SSH into codespace: `gh codespace ssh [--codespace <name>]`
- Copy file: `gh codespace cp <source> <dest>`
- Ports forward: `gh codespace ports forward <port>[:<local-port>]`
- Ports visibility: `gh codespace ports visibility <port>:<org|public|private>`
- List ports: `gh codespace ports list`
- Open in editor: `gh codespace code [--codespace <name>]`
- Rebuild: `gh codespace rebuild [--codespace <name>]`
- View logs: `gh codespace logs [--codespace <name>]`
- Jupyter: `gh codespace jupyter [--codespace <name>]`

## Usage
Triggered when user says "codespace", "create codespace", "list codespaces", "ssh codespace".
Check existing codespaces before creating new ones. Use `--machine` to specify resource size.
