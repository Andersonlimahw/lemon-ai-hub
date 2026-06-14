---
name: token-saver
description: "Configures token-saving tools (rtk, caveman, graphify, context-mode) globally or per project. Allows auditing and calculating the token savings obtained."
---

# token-saver

This skill guides and performs the installation and configuration of tools optimized to reduce token consumption (input/output) and context compression in coding LLMs (Claude Code, Codex, OpenCode, Agy).

The configurable tools are:
1. **rtk (Rust Token Killer)**: CLI command proxy that filters redundant outputs from builds, lints, tests, and git, generating 60-90% savings in local operations.
2. **caveman**: Ultra-compressed communication mode that reduces ~75% of output token consumption by speaking in a telegraphic style (without linking verbs or formalities) without losing technical precision.
3. **graphify**: Codebase mapping into a structured knowledge graph. Allows the LLM to query relationships between files and god nodes without linearly scanning or cross-reading files.
4. **context-mode**: MCP/Plugin that intercepts giant outputs from tools (APIs, long logs, dumps) and stores them in a local FTS5 database, returning only compressed summaries to the active context window.

---

## How to Calculate Token Savings for Each Tool

1. **rtk**:
   - Command: `rtk gain`
   - What it shows: Report of tokens saved in intercepted commands.
   - Command with history: `rtk gain --history`

2. **caveman**:
   - Calculation: Compare character/token counts generated in normal mode vs caveman mode.
   - Example: A 400-token response drops to ~100 tokens. Typical saving is **~75%** on output tokens.

3. **graphify**:
   - Saving: Reduces input token consumption when searching the codebase.
   - Instead of reading 10 related files via grep/search (e.g., 20k-50k tokens), the LLM queries the graph in `graphify-out/` directly, consuming less than 1k tokens.

4. **context-mode**:
   - Saving: Prevents context overflow from console dumps/logs.
   - A 50k-token build log is summarized to 1k tokens in the active window, while keeping the full log searchable via the local SQLite database. Typical saving of **90-98%** on long logs and extensive outputs.

---

## Skill Execution Flow

When this skill is activated:

1. **Ask User (Iterative)**:
   Ask the user for each tool if they want to install/configure it, and the scope of the installation:
   - **rtk**: Install? [y/n] -> Scope: [g]lobal or [p]roject?
   - **caveman**: Install/Activate? [y/n] -> Scope: [g]lobal or [p]roject?
   - **graphify**: Install/Configure? [y/n] -> Scope: [g]lobal or [p]roject?
   - **context-mode**: Install/Configure? [y/n] -> Scope: [g]lobal or [p]roject?

2. **Run Setup Script**:
   Run the helper script `skills/token-saver/scripts/setup-token-saving.sh` (with BypassSandbox when necessary) to perform actions based on the user's selection.

3. **Confirm and Teach**:
   Display a summary of what was configured and quick usage instructions (command cheat-sheet) for each activated tool.
