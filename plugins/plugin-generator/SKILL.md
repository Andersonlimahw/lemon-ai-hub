---
name: plugin-generator
description: Generator for Lemon AI Hub plugins. Creates a new plugin directory following current standards, including plugin.json, SKILL.md, and automatically updates marketplace.json to ensure the plugin is discoverable. Use when the user asks to "create a plugin", "add a plugin", or "generate a new plugin".
---

# Plugin Generator

This skill scaffolds a new plugin in the Lemon AI Hub project following the current standards.

## Responsibilities
1. **Scaffold Directory**: Create `plugins/<plugin-name>/`.
2. **Create `plugin.json`**: Add the standard metadata.
3. **Create `SKILL.md`**: Add the skill definition.
4. **Update Marketplace**: Register the new plugin in `.claude-plugin/marketplace.json` alphabetically.

## Usage
When the user requests to create a new plugin, run this skill to prompt for the name and description if not provided, and then execute the steps. Make sure to adhere to the rule in `docs/rules/marketplace-sync.md`.
