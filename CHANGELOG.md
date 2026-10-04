# Changelog

## [Unreleased]

### Added
- **ai-benchmark-expert plugin**: Multi-provider LLM benchmark. Gives the same task to many models as headless CLI subagents (Claude Code, Codex, Gemini CLI, OpenCode/MiniMax, mm-run or any command) in isolated git workdirs, runs hidden deterministic checks, scores anonymised output with a blind LLM judge on an 8-dimension weighted rubric (tiers A/B/C/D), and renders one self-contained interactive HTML report (leaderboard, quality-vs-cost Pareto, efficiency, rubric heatmap, sortable table, per-run evidence, methodology). Includes `ai-benchmark-runner` agent, example suite and offline tests.
- **motion-movie-expert plugin**: Cross-harness orchestrator for creating and editing motion videos — master-prompt template (PT-BR) and storyboard contract, seam-law choreography, motion-graphics shots, HyperFrames/`seek(t)` production, voice↔video sync (`scripts/build_timeline.py`: timestamps → timeline, SRT/VTT, dwell/readability warnings), UI motion patterns, FFmpeg edit recipes and render QC (`scripts/qc.sh`). Includes `motion-director` and `motion-qc` agents. Upstream skills curated with prompt-injection/supply-chain gating (no runtime self-updates, confirmed installs/uploads/publishing).
- **smart-handoff plugin**: Runtime-agnostic session handoff protocol. Pauses long-running AI coding sessions when context/token budget is nearly exhausted (~90-95%), writes a self-contained handoff file, commits, pushes, and stops — enabling any runtime (Claude Code, Codex, Antigravity/Agy, OpenCode, Gemini CLI) to cleanly resume. Includes `handoff-writer` and `handoff-resumer` agents plus a handoff template.

## [1.2.0] - 2026-07-11

### Added
- **git-expert**: 23 new skills (merge, worktree, rebase, stash, revert, cherry-pick, tag, remote, log, blame, reflog, clean, reset, config, hooks, push, pull, fetch, diff, branch, switch, clone, submodule) — total 25 skills.
- **gh-expert**: 17 new skills (issue, release, repo, codespace, gist, project, workflow, search, label, secret, discussion, org, ruleset, copilot, config, browse, auth) — total 18 skills.
- All skills documented with full CLI capabilities, usage triggers, and safety warnings.

## [1.1.0] - 2026-07-11

### Added
- **git-expert plugin**: Advanced version control with semantic commits (`git-commit`) and AI-guided bisect (`git-bisect-ai`) skills.
- **gh-expert plugin**: GitHub CLI automation with PR management, issue tracking, and workflow skills (`gh-pr`).
- `git-bisect-ai` migrated from standalone plugin to skill inside `git-expert`.

### Changed
- README: added `git-expert` and `gh-expert` to plugin table.
- Marketplace: registered `git-expert` and `gh-expert` plugins.
