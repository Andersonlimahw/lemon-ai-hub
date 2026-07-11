---
name: gh-config
description: Manage GitHub CLI configuration via gh CLI.
---

# GitHub Config Skill

View and modify gh CLI configuration settings.

## Capabilities
- List config: `gh config list`
- Get value: `gh config get <key>`
- Set value: `gh config set <key> <value>`
- Clear cache: `gh config clear-cache`
- Common keys: `git_protocol` (ssh/https), `editor`, `browser`, `prompt` (enabled/disabled), `pager`
- Set git protocol: `gh config set git_protocol ssh`
- Set editor: `gh config set editor code --wait`
- Disable prompts: `gh config set prompt disabled` (for scripting)
- Pager: `gh config set pager "less -R"`

## Usage
Triggered when user says "config", "gh config", "configure gh", "set gh editor".
Use `gh config get git_protocol` to check if gh uses SSH or HTTPS.
