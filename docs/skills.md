---
title: Available AI Skills
status: active
updated: 2026-06-14
related: [docs/index.md, docs/token-saving.md]
---

# Available AI Skills

Custom skills modify agent reasoning patterns and extend their toolboxes. Below is a detailed review of all skills included in the Lemon AI Hub.

## 🧠 Core Agent Pipeline (Stage 0 → 1 → 2)

These three skills are designed to work together sequentially to classify, select, and route incoming requests with optimal token efficiency.

```
User Input 
   ↓
[Stage-0: senior-prompt-engineer] 
   • Classifies intent, detects context, refines prompt.
   • Emits Execution Map (EXEC-MAP v1).
   ↓
[Stage-1: skills-selector]
   • Dynamic gatekeeper. Loads required skills on-demand.
   ↓
[Stage-2: smart-dispatch]
   • Model/Agent router. Selects the cheapest capable tier.
   ↓
Execution
```

## 📂 Complete Skills Registry

The following skills are available in the Lemon AI Hub and can be used across multiple AI agents (Claude Code, Codex, Gemini, Agy, OpenCode).

### `a11y-audit`
- **Location**: [skills/a11y-audit/SKILL.md](./skills/a11y-audit/SKILL.md)

### `async-patterns`
- **Location**: [skills/async-patterns/SKILL.md](./skills/async-patterns/SKILL.md)

### `bundle-analyzer`
- **Location**: [skills/bundle-analyzer/SKILL.md](./skills/bundle-analyzer/SKILL.md)

### `chaos-test`
- **Location**: [skills/chaos-test/SKILL.md](./skills/chaos-test/SKILL.md)

### `code-review-adversary`
- **Location**: [skills/code-review-adversary/SKILL.md](./skills/code-review-adversary/SKILL.md)

### `code-smell`
- **Location**: [skills/code-smell/SKILL.md](./skills/code-smell/SKILL.md)

### `db-index-advisor`
- **Location**: [skills/db-index-advisor/SKILL.md](./skills/db-index-advisor/SKILL.md)

### `feature-flag`
- **Location**: [skills/feature-flag/SKILL.md](./skills/feature-flag/SKILL.md)

### `feature-purge`
- **Location**: [skills/feature-purge/SKILL.md](./skills/feature-purge/SKILL.md)

### `git-bisect-ai`
- **Location**: [skills/git-bisect-ai/SKILL.md](./skills/git-bisect-ai/SKILL.md)

### `i18n-audit`
- **Location**: [skills/i18n-audit/SKILL.md](./skills/i18n-audit/SKILL.md)

### `incident-runbook`
- **Location**: [skills/incident-runbook/SKILL.md](./skills/incident-runbook/SKILL.md)

### `karpathy-recipe`
- **Location**: [skills/karpathy-recipe/SKILL.md](./skills/karpathy-recipe/SKILL.md)

### `llm-wiki-curator`
- **Location**: [skills/llm-wiki-curator/SKILL.md](./skills/llm-wiki-curator/SKILL.md)

### `load-test`
- **Location**: [skills/load-test/SKILL.md](./skills/load-test/SKILL.md)

### `openapi-generate`
- **Location**: [skills/openapi-generate/SKILL.md](./skills/openapi-generate/SKILL.md)

### `senior-prompt-engineer`
- **Location**: [skills/senior-prompt-engineer/SKILL.md](./skills/senior-prompt-engineer/SKILL.md)

### `skills-selector`
- **Location**: [skills/skills-selector/SKILL.md](./skills/skills-selector/SKILL.md)

### `smart-dispatch`
- **Location**: [skills/smart-dispatch/SKILL.md](./skills/smart-dispatch/SKILL.md)

### `token-saver`
- **Location**: [skills/token-saver/SKILL.md](./skills/token-saver/SKILL.md)

