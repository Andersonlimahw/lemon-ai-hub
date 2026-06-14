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
| `a11y-guardian` | Accessibility guardian plugin. Continuous WCAG 2.1 AA/AAA compliance monitoring for web projects. Integrates static analysis of React/Vue/HTML components, contrast ratio checks, ARIA validation, keyboard navigation audit, and generates actionable HTML reports. Pairs with a11y-audit skill. |
| `agentic-value-loops` | Agentic Value Loops plugin — Continuous improvement engine that ships verified increments with constant quality. Includes loops for Feature Development, Maintenance & Security, Documentation Sync, and AI Tuning. |
| `async-advisor` | Async and concurrency static analysis plugin. Scans TypeScript/JavaScript codebases for race conditions, unbounded Promise.all, missing AbortController, swallowed rejections, and N+1 async patterns. Runs as a pre-commit hook or CI check and provides inline fix suggestions. |
| `bundle-watch` | Bundle size monitoring and budget enforcement plugin. Tracks JS/CSS bundle size per commit, blocks PRs that exceed size budgets, posts bundle size diff comments on PRs, and generates size trend charts. Supports Vite, Webpack, Next.js, Remix, and Rollup build outputs. |
| `chaos-runner` | Chaos engineering orchestration plugin. Manages chaos experiments via Toxiproxy, chaos-monkey scripts, and kubectl. Schedules regular chaos game days, tracks experiment results over time, and verifies steady-state hypotheses automatically. Integrates with Grafana for before/after metric comparison. |
| `code-smell-detector` | Automated code smell tracking and trend plugin. Runs smell detection on every PR, tracks smell density per file over time, identifies files with worsening trends, and generates weekly code quality reports. Detects god classes, long methods, feature envy, duplicate code, and dead code without requiring linter configuration. |
| `commit-quality` | Commit message quality enforcement plugin. Validates Conventional Commits format, enforces max diff size per commit, detects commits that mix unrelated changes, suggests atomic commit splits, and generates CHANGELOG entries from commit history. Integrates with commitlint, husky, and CI pipelines. |
| `db-advisor` | Database optimization advisor plugin. Continuously monitors query performance, detects N+1 queries from ORM logs, suggests missing indexes, identifies table bloat, tracks connection pool health, and generates weekly database health reports. Supports PostgreSQL, MySQL, SQLite, and PlanetScale. |
| `feature-flags` | Feature flag lifecycle management plugin. Tracks all flags across the codebase, detects stale flags (>90 days enabled at 100%), enforces naming conventions, auto-generates flag registry, and produces cleanup PRs for dead flags. Integrates with LaunchDarkly, GrowthBook, Unleash, Statsig, and env-var flag patterns. |
| `i18n-sync` | Internationalization key synchronization plugin. Keeps locale JSON files in sync across all supported languages, detects missing and orphaned keys, enforces key naming conventions, blocks PRs that introduce hardcoded strings, and generates translation stubs for new keys. Supports i18next, react-intl, vue-i18n, next-intl, and custom JSON locale files. |
| `incident-center` | Incident management hub plugin. Manages active incidents, runbooks, on-call rotations, and postmortem backlog. Integrates with PagerDuty, OpsGenie, and Slack. Auto-generates incident channels, tracks MTTR/MTTD metrics over time, and maintains a searchable postmortem library for recurring issue detection. |
| `load-test-runner` | Load testing orchestration plugin. Manages k6 and Artillery test suites, schedules nightly soak tests, stores historical performance baselines, detects performance regressions between releases, and generates Grafana-compatible performance reports. Tracks p50/p95/p99 trends over time. |
| `openapi-hub` | OpenAPI spec management hub. Maintains versioned API specs, validates specs on every commit, detects breaking changes between versions, generates typed clients (TypeScript, Python, Go), publishes developer documentation (Redoc/Swagger UI), and exports Postman collections. Enforces spec-first development workflow. |
| `spotify-squad` | AI-Native Squad — Spotify-model autonomous engineering team. 12 specialized agents (Tech Lead, Backend, Frontend, Mobile, UX, UI, Product, Scrum Master, DevOps, QA, Data, Security) with orchestrated collaboration, domain-specific skills, and cross-functional workflows. Based on the AI Native Developer methodology. |

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
