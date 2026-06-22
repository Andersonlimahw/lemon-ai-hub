# chrome-qa-loop

> Reusable closed loop for **exploratory QA over any live web app**, driven by Claude through the **Chrome DevTools MCP**, with four expert lenses: **QA · Product · Engineering · Security**. Read-only on production. One markdown report per finding, auto-saved to disk.

```
you trigger ─▶ EXPLORE (Chrome DevTools MCP) ─▶ REPORT (md per finding) ─▶ you REVIEW ─▶ TRIAGE ─▶ IMPLEMENT (feature-dev loop) ─▶ REFLECT
```

## When to use

- You want a real human-in-the-loop QA pass over a **live** app, not mocked e2e.
- You need findings that the automated suite misses: AI/chat flows, real network errors, security smells, copy/UX friction.
- You want every finding captured the instant it's found — a mid-session crash loses nothing.

## Install

```
/plugin install chrome-qa-loop@lemon-ai-hub
```

The plugin registers the `chrome-devtools` MCP server (`chrome-devtools-mcp`, official Google Chrome DevTools MCP) via `.mcp.json`. Verify it with `list_pages`. Fallback automation: `claude-in-chrome`.

## Configure (per target repo)

Create `chrome-qa-loop.config.json` at the target repo root (or let the skill prompt you once and persist it):

```json
{
  "TARGET_BASE_URL": "https://example.com",
  "SCREEN_MANIFEST": "docs/qa/PLAN.md",
  "OWNER_DOCS_ROOT": "docs/features/",
  "REPORTS_ROOT": "docs/qa/reports/",
  "RUN_MODE": "core"
}
```

Scaffold the PLAN, screen manifest, and report contract from `templates/`:
`PLAN.template.md`, `screen-manifest.template.md`, `report.template.md`.

## Run

```
# 1. Log into your app in the Chrome profile connected to the DevTools MCP (skip for guest* modes).
# 2. Trigger the loop (default mode = core):
/chrome-qa-loop mode=core
#    → walks the manifest, auto-saves one report per finding to ${REPORTS_ROOT}/<run-id>/
#    → auto-creates _INDEX.md, prints the local path
# 3. Review the reports folder; mark status: triaged on accepted findings.
# 4. Hand back for triage:
/chrome-qa-loop triage run=<run-id>
#    → dedupes, prioritizes (P0–P3), emits triage/TASKS.md + per-fix PLAN.md stubs
# 5. Each accepted fix enters a Feature-Development loop (e.g. agentic-value-loops plugin).
# 6. Re-run smoke on fixed screens to verify (/verify) — closes the loop.
```

### Run modes

`guest` (public routes, no auth) · `guest-smoke` · `guest-full` · `smoke` (1–3 core routes, auth) · `core` (~6 routes, auth — default) · `full` (all routes, auth).

## Guardrails (non-negotiable)

- **Read-only on production** — no writes, payments, emails, or persisted content. Needs a write to prove a flow? → file "needs staging".
- **No blocking dialogs** — never trigger native `alert/confirm/prompt`; dismiss with `handle_dialog`.
- **Ground before judging** — read the owner-doc under `${OWNER_DOCS_ROOT}` before evaluating a screen.
- **Write immediately** — one report per finding, auto-saved before continuing.
- **Secrets/PII visible = P0** — capture location and shape only, never the value.

## Reference implementation — VibingCash

This plugin was born **QA'ing [VibingCash](https://vibingcash.com)**, an AI-native personal-finance SaaS — the Auri/Holo financial copilot, finance dashboards, the Vibing Guardian protection layer, and its differentiator: **chat with AI** over your own financial data. The loop exercised the live app with the four lenses (notably prompt-injection probes on `/chat` and authz/secrets checks across the dashboards), produced per-finding markdown reports, and fed a triage→implement handoff.

It was then **generalized**: the target product, base URL, screen manifest, and report paths are all configurable — *"this plugin was born QA'ing VibingCash, an AI-native finance SaaS, and was generalized for any web app."*

- Case / live app: <https://vibingcash.com>
- Blog post: **Veja o post no blog** — `blog/writer` slug `2026/.../chrome-qa-loop-claude-devtools` *(em breve)*

## Contents

```
chrome-qa-loop/
├── .claude-plugin/plugin.json   # manifest
├── agents/
│   ├── chrome-qa-explorer.md    # browser-driving QA brain (4 lenses)
│   └── qa-report-triage.md      # review→implement bridge
├── skills/chrome-qa-loop/SKILL.md
├── templates/
│   ├── PLAN.template.md
│   ├── screen-manifest.template.md
│   └── report.template.md
├── .mcp.json                    # registers chrome-devtools MCP
└── README.md
```

## License

MIT
