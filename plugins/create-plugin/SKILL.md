---
name: create-plugin-scaffold
description: Scaffold a new AI agent plugin directory with valid manifest, component directories, and marketplace wiring. Use when starting a new plugin, adding a plugin to a multi-plugin repository, or reviewing a plugin before submission.
---

# Create Plugin

Meta workflows for creating and reviewing AI agent plugins that are marketplace-ready.

## Components

### Skills

| Skill | Description |
|-------|-------------|
| `create-plugin-scaffold` | Scaffold a new plugin directory with manifest, components, and repository wiring |
| `review-plugin-submission` | Run a pre-submission quality check against marketplace expectations |

## Workflow: Scaffold

1. Validate plugin name (lowercase kebab-case, starts/ends with alphanumeric).
2. Create base files: `plugin.json`, `SKILL.md`, optional `README.md`.
3. Populate `plugin.json` with name, version, description, author, license, keywords.
4. Create component files with valid frontmatter.
5. If marketplace exists, add plugin entry.
6. Ensure all paths are relative and valid.

## Workflow: Review Submission

1. Verify manifest validity.
2. Verify component discoverability.
3. Verify component metadata (frontmatter).
4. Verify marketplace integration.
5. Verify documentation quality.

## Guardrails

- Keep plugin focused on one use case.
- Prefer concise, actionable skill text.
- Do not reference files that don't exist.
- Use folder discovery defaults unless custom paths required.
