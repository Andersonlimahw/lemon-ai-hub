# Lemon AI Hub

> **Build, Launch, and Scale with AI-Native Architecture.**

**Lemon AI Hub** is a centralized and optimized repository to manage **AI Skills and Plugins** across different local agents (Claude Code, Codex, OpenCode, Agy). It is the technical foundation of the [Lemon.dev](https://lemon.dev.br) ecosystem, designed by [Anderson Lima](https://github.com/Andersonlimahw) to help founders and developers bridge the gap between AI-generated code and production-ready products.

This project is based on and inspired by Peter Steinberger's pattern (`steipete/agent-scripts`), but structured with a focus on `.claude` and shared with other providers via transparent symbolic links.

---

## 🍋 The Lemon.dev Philosophy

The best code is invisible—it works, scales, and converts. Lemon AI Hub embodies this by providing:
- **AI-Native Squads:** Specialized agents that understand architecture and product strategy.
- **Value Loops:** Continuous improvement engines that keep quality high without manual overhead.
- **Token Efficiency:** Tools like RTK and Caveman Mode to maximize speed and minimize costs.

---

## 🧩 Install as a Claude Code Hub

This repository ships a marketplace manifest (`.claude-plugin/marketplace.json`) so you can install its plugins directly inside Claude Code.

### 1. Register the marketplace

Inside a Claude Code session, run the slash command:

```text
/plugin marketplace add Andersonlimahw/lemon-ai-hub
```

### 2. Browse & install plugins

Open the interactive installer, or install a plugin by name using the `plugin@marketplace` syntax:

```text
/plugin                                            # browse the catalog UI
/plugin install spotify-squad@lemon-ai-hub
/plugin install agentic-value-loops@lemon-ai-hub
```

| Plugin | Description |
| --- | --- |
| `spotify-squad` | AI-Native Squad — Spotify-model autonomous engineering team. 12 specialized agents (Tech Lead, Backend, Frontend, Mobile, UX, UI, Product, Scrum Master, DevOps, QA, Data, Security) with orchestrated collaboration and 17 domain-specific skills. |
| `agentic-value-loops` | Continuous improvement engine that ships verified increments with constant quality. Loops for Feature Development, Maintenance & Security, Documentation Sync, and AI Tuning. |
| `a11y-guardian` | Accessibility guardian plugin. Continuous WCAG 2.1 AA/AAA compliance monitoring for web projects. |
| `async-advisor` | Async and concurrency static analysis plugin. Scans TypeScript/JavaScript codebases for race conditions and async patterns. |
| `bundle-watch` | Bundle size monitoring and budget enforcement plugin. Tracks JS/CSS bundle size per commit. |
| `chaos-runner` | Chaos engineering orchestration plugin. Manages chaos experiments and reliability verification. |
| `code-smell-detector` | Automated code smell tracking and trend plugin. Runs smell detection on every PR. |
| `commit-quality` | Commit message quality enforcement plugin. Validates Conventional Commits format and atomic splits. |
| `db-advisor` | Database optimization advisor plugin. Monitors query performance and detects N+1 queries. |
| `feature-flags` | Feature flag lifecycle management plugin. Tracks flags across the codebase and detects stale flags. |
| `i18n-sync` | Internationalization key synchronization plugin. Keeps locale JSON files in sync across all languages. |
| `incident-center` | Incident management hub plugin. Manages active incidents, runbooks, and on-call rotations. |
| `load-test-runner` | Load testing orchestration plugin. Manages k6 and Artillery test suites. |
| `openapi-hub` | OpenAPI spec management hub. Maintains versioned API specs and validates breaking changes. |

### 3. Manage the marketplace

```text
/plugin marketplace list                           # show registered marketplaces
/plugin marketplace update lemon-ai-hub          # pull the latest manifest
/plugin marketplace remove lemon-ai-hub          # unregister
```

---

## 📂 Repository Structure

### 🧠 Core Agent Pipeline (`skills/`)
Reusable skills and prompt routers at the repository root.
- [`senior-prompt-engineer`](./skills/senior-prompt-engineer/SKILL.md): Stage-0 prompt refiner and EXEC-MAP builder.
- [`skills-selector`](./skills/skills-selector/SKILL.md): Meta-skill gatekeeper for on-demand skill loading.
- [`smart-dispatch`](./skills/smart-dispatch/SKILL.md): Intelligent routing of implementations with fallback.
- [`karpathy-recipe`](./skills/karpathy-recipe/SKILL.md): Incremental development methodology.
- [`llm-wiki-curator`](./skills/llm-wiki-curator/SKILL.md): Automated maintenance of structured documentation.
- [`token-saver`](./skills/token-saver/SKILL.md): Installation wizard for token-saving tools.
- [`code-review-adversary`](./skills/code-review-adversary/SKILL.md): Adversarial PR review flow.

### 🧩 Plugin Skills (`.claude/skills/`)
Skills bundled as part of specialized plugins.
- [`a11y-audit`](./.claude/skills/a11y-audit/SKILL.md), [`async-patterns`](./.claude/skills/async-patterns/SKILL.md), [`bundle-analyzer`](./.claude/skills/bundle-analyzer/SKILL.md), [`chaos-test`](./.claude/skills/chaos-test/SKILL.md), [`code-smell`](./.claude/skills/code-smell/SKILL.md), [`db-index-advisor`](./.claude/skills/db-index-advisor/SKILL.md), [`feature-flag`](./.claude/skills/feature-flag/SKILL.md), [`feature-purge`](./.claude/skills/feature-purge/SKILL.md), [`git-bisect-ai`](./.claude/skills/git-bisect-ai/SKILL.md), [`i18n-audit`](./.claude/skills/i18n-audit/SKILL.md), [`incident-runbook`](./.claude/skills/incident-runbook/SKILL.md), [`load-test`](./.claude/skills/load-test/SKILL.md), [`openapi-generate`](./.claude/skills/openapi-generate/SKILL.md).

---

## 🚀 Installation & Symlink Setup

To synchronize your global agent configurations and share the same skills folder across all of them:

```bash
chmod +x scripts/setup-symlinks.sh
./scripts/setup-symlinks.sh
```

---

## 🪙 Context Optimization and Token Saving

- **RTK (Rust Token Killer)**: Intercepts shell commands and removes verbose outputs.
- **Caveman Mode**: Reduces response sizes (output tokens) by ~75% through compact writing.
- **Graphify**: Structures your codebase into `graphify-out/` relationship graphs.
- **Context-Mode**: Compresses long logs and API dumps.

---

## 🤝 Connect & Support

**Lemon AI Hub** is maintained by **Anderson Lima**. 

[Website](https://lemon.dev.br) • [GitHub](https://github.com/Andersonlimahw) • [LinkedIn](https://www.linkedin.com/in/andersonlimadev/) • [X/Twitter](https://x.com/andersonlimadev)

---
*Built with 🍋 by Anderson Lima.*
