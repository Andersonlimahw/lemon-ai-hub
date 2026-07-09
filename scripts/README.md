# Lemon AI Hub Scripts

This directory contains utility scripts to help manage and configure your AI agents with the Lemon AI Hub ecosystem.

## Available Scripts

### `menu.sh`
An interactive menu that provides a guided way to:
- Add the marketplace to Claude Code
- Setup symlinks for all your local AI agents
- Setup symlinks for a specific agent (e.g., only Gemini or OpenCode)

**Usage:**
```bash
./scripts/menu.sh
```
*Or directly via curl without cloning:*
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Andersonlimahw/lemon-ai-hub/main/scripts/menu.sh)"
```

### `setup-symlinks.sh`
Automatically creates symlinks in the correct directories for all supported agents (`~/.claude/skills`, `~/.codex/skills`, `~/.gemini/skills`, etc.) pointing to this repository's `plugins/` directory.

**Usage:**
```bash
./scripts/setup-symlinks.sh
```

### Marketplace & Maintenance Scripts
- `update_marketplace.py`: Generates/updates the `marketplace.json` manifest dynamically based on the available plugins.
- `normalize_plugins.py`: Normalizes plugin configuration files and ensures manifest schema conformity.
