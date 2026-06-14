---
title: Documentation Index
status: active
updated: 2026-06-14
related: [docs/architecture.md, docs/skills.md, docs/token-saving.md, docs/cli-marketplace.md]
---

# AI Marketplace Documentation

Welcome to the documentation for the **AI Marketplace** project. This repository acts as a centralized workspace to manage, deploy, and share **AI Skills and Plugins** across multiple local AI coding agents such as Claude Code, Codex, OpenCode, and Antigravity (Agy).

## 🗂️ Documentation Guide

- [Architecture & Symlinking](architecture.md): Learn how the cross-agent sharing system is designed and structured using symlinks.
- [Available Skills](skills.md): Detailed information on the prompt pipelines, gatekeepers, and specialized routing skills.
- [Token Saving Ecosystem](token-saving.md): Deep dive into token optimization tools like RTK, Caveman Mode, Graphify, and Context-Mode.
- [Marketplace CLI Utility](cli-marketplace.md): Quick start guide on managing skills and plugins using the `./scripts/marketplace` CLI.

## 🚀 Getting Started

To initialize the repository and synchronize all your local AI CLIs:

1. Clone this repository locally.
2. Run the symlink setup script:
   ```bash
   chmod +x scripts/setup-symlinks.sh
   ./scripts/setup-symlinks.sh
   ```
3. (Optional) Setup token saving tools to optimize token budgets:
   ```bash
   ./skills/token-saver/scripts/setup-token-saving.sh
   ```

## ⚖️ General Guidelines
- For behavioral conventions, please read [AGENTS.md](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/AGENTS.md) at the root directory.
- For session setup rules, check [CLAUDE.md](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/CLAUDE.md) at the root directory.
