---
name: cli-wrapper-setup
description: >
  One-shot setup that configures the CLI wrapper ecosystem across ALL AI harnesses
  (Claude Code, Gemini, Codex, Agy, OpenCode). Creates symlinks from Claude (single
  source of truth) to every other CLI, registers wrapper skills/agents in each harness,
  and injects the "prefer wrapped CLI" policy into each CLI's config file.
  Run once per machine or after adding a new CLI to the ecosystem.
---

# CLI Wrapper Setup

Configura o ecossistema de CLI wrappers em TODOS os harnesses AI.
Claude = single source of truth. Demais CLIs = symlinks.

## Quick Start

```
/cli-wrapper:cli-wrapper-setup          — full auto-detect + setup
/cli-wrapper:cli-wrapper-setup --dry-run — preview, no changes
/cli-wrapper:cli-wrapper-setup --verify  — audit existing setup
/cli-wrapper:cli-wrapper-setup --add <cli> — add single CLI to ecosystem
```

## What It Does

### Phase 1: Discovery
1. Detect installed CLIs: `which gemini codex agy opencode claude`
2. Map each CLI to its config directory (`~/.<cli>/`)
3. Check existing symlinks, skills, agents, config files
4. Report what exists vs what needs creation

### Phase 2: Claude Canonical Setup
1. Ensure `~/.claude/skills/cli-wrapper/` exists → symlink to this plugin's source
2. Ensure `~/.claude/agents/cli-wrapper/` exists → symlink to `agents/`
3. Register in Claude's skill/agent registry

### Phase 3: Cross-CLI Symlinks
For each detected non-Claude CLI:

| CLI | Skills | Agents | Config |
|-----|--------|--------|--------|
| **Codex** | Already symlinked (`skills → ~/.claude/skills`) | Create `~/.codex/agents/cli-wrapper/` → Claude agents | Update `~/.codex/AGENTS.md` |
| **Agy** | Already symlinked (`skills → ~/.claude/skills`) | Create `~/.agy/agents/` + symlinks | Create `~/.agy/AGENTS.md` |
| **OpenCode** | Already symlinked (`skills → ~/.claude/skills`) | Create `~/.opencode/agents/` + symlinks | Create `~/.opencode/AGENTS.md` |
| **Gemini** | Individual skill symlinks in `~/.gemini/skills/` | Individual agent symlinks in `~/.gemini/agents/` | Update `~/.gemini/GEMINI.md` |

### Phase 3.5: Agent Frontmatter Sync (MANDATORY)

**Retrocompatibility contract:** raw symlinks from `~/.{harness}/agents/` to
Claude-format files BREAK OpenCode and may break Agy/Gemini because the
frontmatter schema is harness-specific. This phase materializes per-harness
copies via `scripts/sync-agents.py` with strict schema enforcement.

**Why this exists:** a previous setup created raw symlinks to Claude-format
agents. OpenCode then silently dropped `name:` (file name = agent identity)
and the missing `description:` caused a hard parse error. A migration attempt
that uppercased `tools:` to `Tools:` and pluralized `color:` to `colors:`
would also be invalid — both keys are rejected.

**Per-harness schema (strict):**

| Harness | Top-level keys kept | Drops | Sidecar |
|---------|--------------------|----|---------|
| Claude | `name`, `description`, `color`, `mode`, `permission`, `tools` | — | — |
| Codex | `name`, `description`, `color`, `mode`, `permission` | — | `.toml` |
| Gemini | `name`, `description`, `color`, `mode`, `permission` | — | — |
| Agy | `name`, `description`, `color`, `mode`, `permission` | — | — |
| OpenCode | `description`, `color`, `mode`, `permission` | `name` | — |

**Behavior:**
- Reads canonical agents from `plugins/cli-wrapper/agents/*.md`
- Emits materialized files (not symlinks) at `~/.{harness}/agents/{name}.md`
- Codex additionally gets `~/.codex/agents/{name}.toml` with the same body
- Drops any key not in the harness whitelist; logs a `[warn]` line
- Idempotent: re-running with no source change = no writes
- `--dry-run` previews writes; `--verify` audits existing files (exit 1 on drift)

**Commands:**
```bash
python3 scripts/sync-agents.py            # apply
python3 scripts/sync-agents.py --dry-run  # preview
python3 scripts/sync-agents.py --verify   # audit, exit 1 on drift
python3 scripts/sync-agents.py --harness opencode  # single harness
```

This phase is wired into `scripts/setup-symlinks.sh` and `scripts/menu.sh`
so any symlink run automatically syncs agent frontmatter.

### Phase 4: Config Injection
Add to each CLI's main config file:

```markdown
## 🔌 CLI Wrapper Policy (managed by cli-wrapper-setup)

⚠️ **PREFER** `/cli-wrapper:<cli>-cli invoke ...` over raw `<cli> ...` commands.
Wrapped CLIs save 60-95% tokens per invocation. List: `/cli-wrapper list`
Setup: `/cli-wrapper:cli-wrapper-setup --verify`
```

Files updated:
- `~/.claude/CLAUDE.md` — append policy block
- `~/.gemini/GEMINI.md` — append policy block
- `~/.codex/AGENTS.md` — append policy block
- `~/.agy/AGENTS.md` — create + append
- `~/.opencode/AGENTS.md` — create + append

### Phase 5: Verification
1. Every symlink resolves correctly
2. `cli-wrapper list` works in each CLI
3. Token audit runs without errors
4. Config files contain the policy block
5. Report: green checkmarks or red X's

## Architecture — Single Source of Truth

```
lemon-ai-hub/plugins/cli-wrapper/     ← CANONICAL SOURCE (git)
  ├── SKILL.md
  ├── plugin.json
  ├── skills/                          ← wrapper skills
  │   ├── cli-wrapper-setup/
  │   ├── claude-cli/
  │   ├── gemini-cli/
  │   ├── codex-cli/
  │   ├── opencode-cli/
  │   └── agy-cli/
  ├── agents/                          ← wrapper agents
  │   ├── claude-cli.md
  │   ├── gemini-cli.md
  │   ├── codex-cli.md
  │   ├── opencode-cli.md
  │   └── agy-cli.md
  └── templates/                       ← config templates
      └── symlink-map.json

              ↓ symlink

~/.claude/skills/cli-wrapper/ → project/plugins/cli-wrapper/
~/.claude/agents/cli-wrapper/  → project/plugins/cli-wrapper/agents/

              ↓ symlink (existing: skills → ~/.claude/skills)

~/.codex/skills/cli-wrapper/   → resolved via skills symlink
~/.agy/skills/cli-wrapper/     → resolved via skills symlink
~/.opencode/skills/cli-wrapper/ → resolved via skills symlink

              ↓ individual symlinks (Gemini only — no top-level skills symlink)

~/.gemini/skills/cli-wrapper/  → ~/.claude/skills/cli-wrapper/
~/.gemini/skills/claude-cli/   → ~/.claude/skills/cli-wrapper/skills/claude-cli/
~/.gemini/skills/gemini-cli/   → ~/.claude/skills/cli-wrapper/skills/gemini-cli/
... (one per sub-skill)

              ↓ agent symlinks

~/.codex/agents/claude-cli.md  → ~/.claude/agents/cli-wrapper/claude-cli.md
~/.gemini/agents/claude-cli.md → ~/.claude/agents/cli-wrapper/claude-cli.md
... (one per agent per CLI)
```

## Supported CLIs

| CLI | Binary | Config Dir | Wrapper Skill | Wrapper Agent |
|-----|--------|-----------|---------------|---------------|
| Claude Code | `claude` | `~/.claude/` | `claude-cli` | `claude-cli` |
| Gemini CLI | `gemini` | `~/.gemini/` | `gemini-cli` | `gemini-cli` |
| Codex CLI | `codex` | `~/.codex/` | `codex-cli` | `codex-cli` |
| OpenCode | `opencode` | `~/.opencode/` | `opencode-cli` | `opencode-cli` |
| Agy (Antigravity) | `agy` | `~/.agy/` | `agy-cli` | `agy-cli` |

Extensible: edit `templates/symlink-map.json` to add new CLIs.

## Token Savings

Setup-enabled ecosystem saves tokens on EVERY cross-CLI invocation:

| Without Wrapper | With Wrapper |
|----------------|-------------|
| Raw `gemini --help` → 3-5KB each session | Pre-cached digest → 0.3KB |
| Raw CLI output → unbounded | Post-processed → 500 line cap |
| Harness guesses flags → retries | Digest validates → first try |
| No cross-CLI metrics | Unified audit trail |

## Post-Setup

After setup completes:
1. Test: `/cli-wrapper:gemini-cli audit`
2. Test: `/cli-wrapper:codex-cli explain`
3. Delegate: spawn `codex-cli` agent for Codex tasks
4. Monitor: `/cli-wrapper audit all` for ecosystem-wide savings

## Dry Run Example

```
User: /cli-wrapper:cli-wrapper-setup --dry-run
Claude:
  🔍 CLI WRAPPER ECOSYSTEM — Dry Run
  ====================================
  ✓ claude — installed (/usr/local/bin/claude)
  ✓ gemini — installed (/opt/homebrew/bin/gemini)
  ✓ codex  — installed (/opt/homebrew/bin/codex)
  ✓ opencode — installed (~/.opencode/bin/opencode)
  ✓ agy    — installed (~/.local/bin/agy)

  Skills:
  ✓ ~/.claude/skills/cli-wrapper/ → project (CREATE)
  ✓ ~/.codex/skills/cli-wrapper/ → resolved via existing symlink
  ⚠ ~/.gemini/skills/cli-wrapper/ → INDIVIDUAL SYMLINKS (6 skills)
  ✓ ~/.agy/skills/cli-wrapper/ → resolved via existing symlink
  ✓ ~/.opencode/skills/cli-wrapper/ → resolved via existing symlink

  Agents:
  ✓ ~/.claude/agents/cli-wrapper/ → project/agents/ (CREATE)
  ⚠ ~/.codex/agents/claude-cli.md → symlink (5 agents)
  ⚠ ~/.gemini/agents/claude-cli.md → symlink (5 agents)
  ⚠ ~/.agy/agents/ → CREATE DIR + symlinks
  ⚠ ~/.opencode/agents/ → CREATE DIR + symlinks

  Config:
  ⚠ ~/.claude/CLAUDE.md → APPEND policy block
  ⚠ ~/.gemini/GEMINI.md → APPEND policy block
  ⚠ ~/.codex/AGENTS.md → APPEND policy block
  ⚠ ~/.agy/AGENTS.md → CREATE + policy block
  ⚠ ~/.opencode/AGENTS.md → CREATE + policy block

  12 actions pending. Run without --dry-run to apply.

User: /cli-wrapper:cli-wrapper-setup
Claude:
  ✓ Done. 12/12 actions completed.
  Ecosystem: 5 CLIs, 30 skills, 25 agents, 5 configs.
  Estimated savings: ~45,000 tokens/month across all harnesses.
```
