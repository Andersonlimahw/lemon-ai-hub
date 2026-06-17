---
name: write-project-skill
description: Create global or project-local agent skills with concise SKILL.md files, progressive disclosure, and optional deterministic scripts. Use when the user wants new skills for a project, workspace, domain, or global AI setup.
---

# Write Project Skill

Goal: create only the skills that improve future agent performance for repeated work.

## Process

1. Identify scope:
   - Global: reusable across unrelated projects, placed under the user's global skills directory.
   - Project-local: tied to this repo/domain, placed under the project's skill/plugin structure and referenced from `AGENTS.md`.
2. Ask for missing requirements one at a time:
   - Task/domain covered.
   - Trigger phrases.
   - Concrete use cases.
   - Whether scripts or references are needed.
3. Draft the skill:
   - `SKILL.md` with only `name` and `description` in frontmatter.
   - Body under 100 lines when possible.
   - References one level deep when details would bloat the main file.
   - Scripts only for deterministic repeated operations.
4. Validate:
   - Description says what the skill does and when to use it.
   - Name is lowercase hyphen-case.
   - No stale placeholders.
   - Script examples run when scripts were added.

## Placement Policy

- Put repo-specific conventions in project-local skills.
- Put universal workflows in global skills.
- Do not duplicate the same skill globally and locally; create a global skill plus project references when needed.
- For plugin work in this repo, update `.claude-plugin/marketplace.json` whenever a plugin directory is added, renamed, removed, or plugin metadata changes.

## Skill Template

```md
---
name: skill-name
description: One sentence describing capability. Use when specific trigger or context applies.
---

# Skill Name

Goal: short outcome.

## Process

1. Step.
2. Step.
3. Verify.

## Rules

- Constraint.
- Constraint.
```

## Review Checklist

- Description includes concrete triggers.
- Body contains workflow, rules, and verification.
- References are only loaded when needed.
- Scripts are justified by determinism or repetition.
- Every created skill maps to a real future task.
