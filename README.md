# AI Marketplace

Centralized and optimized repository to manage **AI Skills and Plugins** across different local agents (Claude Code, Codex, OpenCode, Agy).

This project is based on and inspired by Peter Steinberger's pattern (`steipete/agent-scripts`), but structured with a focus on `.claude` and shared with other providers via transparent symbolic links.

---

## 🧩 Install as a Claude Code Marketplace

This repository ships a marketplace manifest (`.claude-plugin/marketplace.json`) so you can install its plugins directly inside Claude Code.

### 1. Register the marketplace

Inside a Claude Code session, run the slash command:

```text
/plugin marketplace add Andersonlimahw/ai-marketplace
```

You can also point at any Git URL or a local path:

```text
/plugin marketplace add https://github.com/Andersonlimahw/ai-marketplace.git
/plugin marketplace add ./ai-marketplace          # local checkout
```

### 2. Browse & install plugins

Open the interactive installer, or install a plugin by name using the `plugin@marketplace` syntax:

```text
/plugin                                            # browse the catalog UI
/plugin install spotify-squad@ai-marketplace
/plugin install agentic-value-loops@ai-marketplace
```

| Plugin | What you get |
| --- | --- |
| `spotify-squad` | 12 specialized agents (Tech Lead, Backend, Frontend, Mobile, UX, UI, Product, Scrum Master, DevOps, QA, Data, Security) + 17 domain skills. |
| `agentic-value-loops` | Continuous-improvement loops: Feature Development, Maintenance & Security, Documentation Sync, AI Tuning. |

### 3. Manage the marketplace

```text
/plugin marketplace list                           # show registered marketplaces
/plugin marketplace update ai-marketplace          # pull the latest manifest
/plugin marketplace remove ai-marketplace          # unregister
```

> Plugins bundle their own agents, skills, and commands — once installed they are auto-discovered by Claude Code. The standalone `skills/` in this repo are shared globally via symlinks instead (see **Installation & Symlink Setup** below).

---

## 📂 Repository Structure

- **`skills/`**: Reusable skills and prompt routers.
  - [`senior-prompt-engineer`](./skills/senior-prompt-engineer/SKILL.md): Stage-0 prompt refiner and Execution Map (`EXEC-MAP v1`) builder.
  - [`skills-selector`](./skills/skills-selector/SKILL.md): Meta-skill gatekeeper that dynamically decides which skills to load on-demand.
  - [`smart-dispatch`](./skills/smart-dispatch/SKILL.md): Intelligent routing of implementations with fallback and YOLO-mode.
  - [`karpathy-recipe`](./skills/karpathy-recipe/SKILL.md): Incremental development methodology (based on Karpathy's recipe).
  - [`llm-wiki-curator`](./skills/llm-wiki-curator/SKILL.md): Automated maintenance of structured `llms.txt` documentation.
  - [`token-saver`](./skills/token-saver/SKILL.md): Generic skill for installing and configuring token-saving tools.
  - [`code-review-adversary`](./skills/code-review-adversary/SKILL.md): Senior-vs-junior adversarial PR review with configurable model, criticality, and inline-comment/resolve flow.
- **`plugins/`**: Installable Claude Code plugins (`spotify-squad`, `agentic-value-loops`) — see [Install as a Claude Code Marketplace](#-install-as-a-claude-code-marketplace).
- **`scripts/`**: Utility helpers.
  - `setup-symlinks.sh`: Script to automate the creation of global symbolic links.
  - `marketplace`: CLI interface for listing and managing IA tools in the repository.

---

## 🚀 Installation & Symlink Setup

To synchronize your global agent configurations and share the same skills folder across all of them, run the setup script from the root of the repository:

```bash
chmod +x scripts/setup-symlinks.sh
./scripts/setup-symlinks.sh
```

This script performs the following steps:
1. Backs up existing folders (like `~/.claude/skills` if they already exist).
2. Creates the symbolic link `~/.claude/skills` pointing to the `skills/` folder of this repository.
3. Creates symbolic links for `~/.codex/skills`, `~/.opencode/skills`, and `~/.agy/skills` pointing directly to `~/.claude/skills`.

With this, any skill added or updated in this repository will be immediately available in all your AI CLIs!

---

## 🛒 The `marketplace` CLI

You can list active skills and plugins at any time using the `marketplace` utility:

```bash
./scripts/marketplace list-skills
./scripts/marketplace list-plugins
```

---

## 🪙 Context Optimization and Token Saving (`token-saver`)

To install and configure the main token-saving tools in the ecosystem with assistance, use the `token-saver` skill (or run the script directly):

```bash
chmod +x skills/token-saver/scripts/setup-token-saving.sh
./skills/token-saver/scripts/setup-token-saving.sh
```

### What the Setup Optimizes:
- **RTK (Rust Token Killer)**: Intercepts shell commands (git, tests, build) and removes verbose outputs. (Use `rtk gain` to view the audit).
- **Caveman Mode**: Reduces response sizes (output tokens) by ~75% through compact telegraphic writing.
- **Graphify**: Structures your codebase into `graphify-out/` relationship graphs so that the LLM finds files without reading the entire folder.
- **Context-Mode**: Compresses long logs, APIs, and large dumps, sending only structured summaries to the active chat context.
