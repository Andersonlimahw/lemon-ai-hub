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
| `a11y-audit` | WCAG 2.1 AA/AAA accessibility audit for web components, pages, and apps. Detects contrast failures, missing ARIA labels, keyboard trap issues, focus order problems, and screen-reader gotchas. Use when user wants to audit accessibility, fix a11y warnings, prepare for compliance review, or validate UI against WCAG standards. |
| `a11y-guardian` | Accessibility guardian plugin. Continuous WCAG 2.1 AA/AAA compliance monitoring for web projects. Integrates static analysis of React/Vue/HTML components, contrast ratio checks, ARIA validation, keyboard navigation audit, and generates actionable HTML reports. Pairs with a11y-audit skill. |
| `agentic-value-loops` | Agentic Value Loops plugin — Continuous improvement engine that ships verified increments with constant quality. Includes loops for Feature Development, Maintenance & Security, Documentation Sync, and AI Tuning. |
| `async-advisor` | Async and concurrency static analysis plugin. Scans TypeScript/JavaScript codebases for race conditions, unbounded Promise.all, missing AbortController, swallowed rejections, and N+1 async patterns. Runs as a pre-commit hook or CI check and provides inline fix suggestions. |
| `async-patterns` | Async and concurrency pattern advisor for JavaScript/TypeScript, Python, Go, and Rust. Identifies race conditions, missing error handling in promise chains, N+1 async anti-patterns, unbounded parallelism, and missing cancellation. Recommends correct patterns: Promise.all, p-limit, AbortController, AsyncLocalStorage, worker threads. Use when async code has bugs, timeouts, or memory leaks. |
| `bundle-analyzer` | JavaScript/TypeScript bundle size analysis, tree-shaking audit, and code splitting recommendations. Identifies heavy dependencies, duplicate packages, unused imports, and suggests dynamic imports and lazy loading. Use when bundle is too large, Lighthouse score is low, or user wants to optimize web app loading performance. |
| `bundle-watch` | Bundle size monitoring and budget enforcement plugin. Tracks JS/CSS bundle size per commit, blocks PRs that exceed size budgets, posts bundle size diff comments on PRs, and generates size trend charts. Supports Vite, Webpack, Next.js, Remix, and Rollup build outputs. |
| `chaos-runner` | Chaos engineering orchestration plugin. Manages chaos experiments via Toxiproxy, chaos-monkey scripts, and kubectl. Schedules regular chaos game days, tracks experiment results over time, and verifies steady-state hypotheses automatically. Integrates with Grafana for before/after metric comparison. |
| `chaos-test` | Chaos engineering scenarios for resilience testing. Designs fault injection experiments (network partitions, latency injection, dependency failures, disk pressure, memory leaks) and verifies circuit breakers, retries, and fallbacks work correctly. Use when building resilience features, verifying SLO under failure conditions, or preparing for production chaos days. |
| `code-review-adversary` | > |
| `code-smell` | Code smell detection and remediation. Identifies long methods, god classes, feature envy, primitive obsession, shotgun surgery, dead code, magic numbers, and other structural anti-patterns. Goes beyond linters — understands semantic coupling and design intent. Use when code is hard to change, PRs are consistently risky, or technical debt is growing faster than features. |
| `code-smell-detector` | Automated code smell tracking and trend plugin. Runs smell detection on every PR, tracks smell density per file over time, identifies files with worsening trends, and generates weekly code quality reports. Detects god classes, long methods, feature envy, duplicate code, and dead code without requiring linter configuration. |
| `commit-quality` | Commit message quality enforcement plugin. Validates Conventional Commits format, enforces max diff size per commit, detects commits that mix unrelated changes, suggests atomic commit splits, and generates CHANGELOG entries from commit history. Integrates with commitlint, husky, and CI pipelines. |
| `db-advisor` | Database optimization advisor plugin. Continuously monitors query performance, detects N+1 queries from ORM logs, suggests missing indexes, identifies table bloat, tracks connection pool health, and generates weekly database health reports. Supports PostgreSQL, MySQL, SQLite, and PlanetScale. |
| `db-index-advisor` | Database index optimization advisor for PostgreSQL, MySQL, and SQLite. Analyzes slow queries, missing indexes, unused indexes, and over-indexed tables. Generates CREATE INDEX statements with EXPLAIN ANALYZE estimates. Use when queries are slow, p99 DB latency spikes, or when reviewing a new schema. |
| `feature-flag` | Feature flag implementation, management, and cleanup. Handles flag creation, gradual rollout strategies, A/B testing wiring, stale flag detection, and safe flag removal. Supports LaunchDarkly, Unleash, GrowthBook, Statsig, custom env-var flags, and database-backed toggles. Use when adding gated features, rolling out gradually, or cleaning up old flags. |
| `feature-flags` | Feature flag lifecycle management plugin. Tracks all flags across the codebase, detects stale flags (>90 days enabled at 100%), enforces naming conventions, auto-generates flag registry, and produces cleanup PRs for dead flags. Integrates with LaunchDarkly, GrowthBook, Unleash, Statsig, and env-var flag patterns. |
| `feature-purge` | Safely remove an entire feature and every dead reference it leaves behind — not just the folder you point at, but the sibling folders in other architecture layers, the imports/registries/routes/i18n keys that point to it, and any newly-orphaned code. Verifies the quality gate stays 100% green and writes a Markdown removal report. Use when deleting a feature, screen, module, or directory and you need it gone WITHOUT leaving dead files or dead code. Triggers on /feature-purge <path>, "remove this feature", "delete this folder safely", "apaga essa feature sem deixar código morto", "limpa essa screen e as camadas". |
| `git-bisect-ai` | AI-guided git bisect for finding the exact commit that introduced a bug or regression. Automates the binary search, interprets test results, and identifies the responsible code change with full context. Use when you know a bug exists now but didn't exist before, or when a performance regression appeared somewhere in git history. |
| `app-store-connect-api` | Apple Store Connect API Expert Agent and Skills. Provides comprehensive tools and knowledge for interacting with the App Store Connect API, covering domains like TestFlight, In-app purchases, Subscriptions, App management, and Provisioning. |
| `apple-store-release-agent` | AI release agent for the Apple App Store. Audits Expo/React Native iOS builds, App Store metadata, App Privacy readiness, TestFlight, RevenueCat/IAP, Firebase, i18n parity (PT/EN/ES), screenshots, and review notes — build readiness (app.json, eas.json, bundleId, version), metadata wording risk, privacy labels suggestions, SDK data-collection map, restore-purchases, paywall fallback, native-alert UX, and account deletion. Generates reports + GO/GO_WITH_WARNINGS/NO_GO checklist. Never submits to App Review or alters the store without explicit human approval. Use when preparing an iOS app for the App Store, auditing a submission, generating review notes, validating RevenueCat/App Privacy, or running a release go/no-go. |
| `google-play-release-agent` | AI release agent for Google Play Store. Audits Android/Expo/React Native/Firebase/RevenueCat before submission — build readiness (app.json, eas.json, AAB, versionCode), Play Console metadata, Data Safety Form, Android permissions, RevenueCat/IAP, i18n parity (PT/EN/ES), policy-risk copy, internal/closed testing and staged rollout. Generates reports + GO/NO-GO checklist. Never publishes or rolls out without explicit human approval. Use when preparing an Android app for Google Play, auditing a submission, generating release notes, validating Data Safety or permissions, or running a release go/no-go. |
| `i18n-audit` | Internationalization completeness audit and key synchronization. Finds missing translation keys, hardcoded strings, pluralization bugs, RTL layout issues, date/number formatting gaps, and untranslated copy. Supports i18next, react-intl, vue-i18n, next-intl, and custom JSON locale files. Use when adding a new language, auditing translation completeness, or debugging locale mismatch errors. |
| `i18n-sync` | Internationalization key synchronization plugin. Keeps locale JSON files in sync across all supported languages, detects missing and orphaned keys, enforces key naming conventions, blocks PRs that introduce hardcoded strings, and generates translation stubs for new keys. Supports i18next, react-intl, vue-i18n, next-intl, and custom JSON locale files. |
| `incident-center` | Incident management hub plugin. Manages active incidents, runbooks, on-call rotations, and postmortem backlog. Integrates with PagerDuty, OpsGenie, and Slack. Auto-generates incident channels, tracks MTTR/MTTD metrics over time, and maintains a searchable postmortem library for recurring issue detection. |
| `incident-runbook` | Incident response runbooks, on-call workflows, and postmortem templates. Generates severity-tiered runbooks, communication templates, timeline reconstruction, and blameless postmortem docs. Use when user is in an incident, doing on-call prep, writing a postmortem, or building incident response playbooks. |
| `karpathy-guidelines` | > |
| `karpathy-recipe` | Applies Karpathy's "A Recipe for Training Neural Networks" adapted to software engineering. Forces a minimum runnable baseline before optimizing, one knob at a time, with verifiable eval at the beginning. Use when implementing a new feature, doing a non-trivial refactor, integrating an external service, or when the user says "implement X from scratch", "how to start feature Y", "recipe", "incremental approach", "baseline first". |
| `llm-wiki-curator` | Maintains docs/ in the Karpathy-style LLM-wiki standard. Generates docs/llms.txt (flat machine-readable index conforming to llmstxt.org), validates broken links, enforces a minimum front-matter in new .md files (title, status, updated, related), groups orphan docs. Use when the user says "update docs index", "generate llms.txt", "audit docs", "organize wiki", "cure documentation", or after adding/renaming a file in docs/. |
| `load-test` | Load testing setup, execution, and analysis with k6, Artillery, or Locust. Generates test scripts, defines VU ramp-up scenarios, interprets p99 latency and error rate results, and suggests infrastructure fixes. Use when user wants to load test an API, check throughput limits, validate SLO headroom, or diagnose performance under traffic. |
| `load-test-runner` | Load testing orchestration plugin. Manages k6 and Artillery test suites, schedules nightly soak tests, stores historical performance baselines, detects performance regressions between releases, and generates Grafana-compatible performance reports. Tracks p50/p95/p99 trends over time. |
| `openapi-generate` | Generate OpenAPI 3.1 specs from existing code (routes, controllers, types, Zod/Joi schemas), or generate code from an existing spec. Produces valid openapi.yaml, typed client SDKs, mock servers, and Postman collections. Use when documenting an API, onboarding clients, generating typed SDKs, or migrating to spec-first development. |
| `openapi-hub` | OpenAPI spec management hub. Maintains versioned API specs, validates specs on every commit, detects breaking changes between versions, generates typed clients (TypeScript, Python, Go), publishes developer documentation (Redoc/Swagger UI), and exports Postman collections. Enforces spec-first development workflow. |
| `plugin-generator` | Generator for Lemon AI Hub plugins. Creates a new plugin directory following current standards, including plugin.json, SKILL.md, and automatically updates marketplace.json to ensure the plugin is discoverable. Use when the user asks to "create a plugin", "add a plugin", or "generate a new plugin". |
| `senior-prompt-engineer` | Pipeline stage-0 prompt refiner. Runs FIRST — before skills-selector and smart-dispatch — turning a raw idea, pasted draft, or the current chat into a definitive, production-grade prompt (Anthropic prompt-engineering best practices), then hands the refined prompt + an Execution Map (agents, skills, models, effort, time & token estimate) to the routers so they pick the best skills/models with sharpened context. When no file path is given, the input IS the chat/pasted text and the output is returned inline (processed naturally), not forced to a file. Use when the user invokes /senior-prompt-engineer, says "refine my prompt", "improve this prompt", "turn this idea into a prompt", "rewrite idea.md to prompt.md", "definitive prompt", "professional prompt", or pastes a draft prompt/idea to be hardened. Cross-CLI: Claude, Codex, Gemini, OpenCode, Antigravity (agy), lemon-code (lemon). |
| `skills-selector` | Meta-skill gatekeeper that runs FIRST on every task to decide which other skill(s) — if any — should activate. Analyzes the user request, matches it against a ranked catalog (frontend-design, ui-ux-pro-max, superpowers/planning, git-*, mcp-builder, smart-dispatch, claude-api, etc.), and emits a tight SELECTION plan so other skills are loaded on-demand only. Minimizes token/context consumption by refusing to activate heavy skills unless clearly justified. Triggers on ANY user instruction that could plausibly benefit from a specialized skill — i.e. essentially every turn that starts new work. Keywords: "plan", "design", "ui", "ux", "implement", "build", "create", "fix", "refactor", "commit", "pr", "review", "test", "debug", "deploy", "mobile", "video", "mcp", "skill", "architecture", "api", "ci", "docs", "copy", "social", "setup", "doctor". |
| `smart-dispatch` | Automatically routes tasks to the optimal AI agent, model, or provider based on complexity, cost, and capability. Use when implementing features, fixing bugs, or any multi-step development work. Triggers on "implement", "build", "create", "fix", "add feature", "develop", or when the user asks to do any coding task. |
| `spotify-squad` | AI-Native Squad — Spotify-model autonomous engineering team. 12 specialized agents (Tech Lead, Backend, Frontend, Mobile, UX, UI, Product, Scrum Master, DevOps, QA, Data, Security) with orchestrated collaboration, domain-specific skills, and cross-functional workflows. Based on the AI Native Developer methodology. |
| `token-saver` | Configures token-saving tools (rtk, caveman, graphify, context-mode) globally or per project. Allows auditing and calculating the token savings obtained. |

### 3. Manage the marketplace

```text
/plugin marketplace list                           # show registered marketplaces
/plugin marketplace update lemon-ai-hub          # pull the latest manifest
/plugin marketplace remove lemon-ai-hub          # unregister
```

---

## 📂 Repository Structure

All tools in this hub are organized as **Plugins**. You can explore them in the `plugins/` directory. Each plugin includes its own `SKILL.md` (logic) and `plugin.json` (manifest).

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
