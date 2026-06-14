---
title: Token Saving Ecosystem
status: active
updated: 2026-06-14
related: [docs/index.md, docs/skills.md]
---

# Token Saving Ecosystem

Large Context Windows permit long chat history, but feeding verbose compiler logs, unused files, and repetitive greetings wasting thousands of tokens. This repository includes integrations for four primary optimization tools.

---

## 1. Rust Token Killer (RTK)
- **Concept**: A lightweight terminal proxy that filters terminal stderr/stdout before sending outputs back to the AI's chat context.
- **Savings**: **60% - 90%** on local development commands (e.g., git, package installations, typescript checks, test suites).
- **Audit Command**: Run `rtk gain` or `rtk gain --history` to inspect local token savings analytics.

---

## 2. Caveman Mode
- **Concept**: Instructs the LLM to skip conversational filler (e.g., "Certainly! I'd be happy to help you with that..."), pleasantries, and descriptive boilerplate.
- **Savings**: **~75%** on output tokens.
- **Resulting style**: Telegraphic, brief, dense sentences focusing strictly on technical implementations, paths, and commands.

---

## 3. Graphify (Knowledge Graph codebase search)
- **Concept**: Indexes the codebase structure (files, modules, directories) as an AST-parsed Knowledge Graph in `graphify-out/`.
- **Savings**: **90%+** on codebase search operations.
- **Advantage**: Instead of running expensive recursive `grep` commands that dump multiple long files into the context window, the agent queries the local graph database for specific relationships or definitions.

---

## 4. Context-Mode
- **Concept**: An MCP plugin that intercepts terminal buffer overflows, massive API dumps, and database logs. It offloads these outputs to a local SQLite FTS5 database and sends only structured, compact summaries back to the LLM.
- **Savings**: **90% - 98%** on long logs.
