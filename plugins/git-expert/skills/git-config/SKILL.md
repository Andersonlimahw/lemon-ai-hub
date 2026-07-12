---
name: git-config
description: Manage git configuration at system, global, and local levels.
---

# Git Config Skill

Read and write git configuration values across all config levels.

## Capabilities
- List all config: `git config --list`
- List global config: `git config --global --list`
- List local config: `git config --local --list`
- Get value: `git config <key>`
- Set value: `git config <key> <value>`
- Set global: `git config --global <key> <value>`
- Unset value: `git config --unset <key>`
- Edit config: `git config --edit` or `--global --edit`
- Set user: `git config user.name "Name"` / `user.email "email"`
- Set default branch: `git config init.defaultBranch main`
- Set aliases: `git config alias.<name> <command>`
- Set diff tool: `git config diff.tool <tool>`
- Set merge tool: `git config merge.tool <tool>`
- Safe directory: `git config --global --add safe.directory <path>`

## Usage
Triggered when user says "config", "git config", "set git user", "git alias".
Read current config before making changes. Prefer `--global` for identity settings.
