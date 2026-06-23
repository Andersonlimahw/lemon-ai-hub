---
name: chrome-qa-loop
description: Reusable closed loop for exploratory QA over ANY live web app via the Chrome DevTools MCP. You trigger it → Claude navigates the app with full per-screen doc context → writes one markdown report per finding → you review → hand back for triage → fixes enter a Feature-Development loop. Product-agnostic: target URL, screen manifest and report paths come from chrome-qa-loop.config.json. Trigger with "/chrome-qa-loop", "qa loop", "explore the app", "test the live app", "chrome qa".
---

# Chrome QA Loop

A reusable human-in-the-loop QA cycle, driven by Claude via the **Chrome DevTools MCP** (`chrome-devtools-mcp`). Generalized from a real implementation that QA'd VibingCash (see README) — nothing here is bound to a single product.

```
you trigger ─▶ EXPLORE (Chrome DevTools MCP) ─▶ REPORT (md per finding) ─▶ you REVIEW ─▶ TRIAGE ─▶ IMPLEMENT (feature-dev loop) ─▶ REFLECT ─▶ (back to you)
```

## Configuration (per repo)

The loop reads `chrome-qa-loop.config.json` from the target repo root. If absent, ask the operator once and persist it:

```json
{
  "TARGET_BASE_URL": "https://example.com",
  "SCREEN_MANIFEST": "docs/qa/PLAN.md",
  "OWNER_DOCS_ROOT": "docs/features/",
  "REPORTS_ROOT": "docs/qa/reports/",
  "RUN_MODE": "core"
}
```

Scaffold the manifest + report contract from `templates/` in this plugin:
`PLAN.template.md`, `screen-manifest.template.md`, `report.template.md`.

## Invocation

```
/chrome-qa-loop [mode=guest|guest-smoke|guest-full|smoke|core|full]   # run an exploration pass (default: core)
/chrome-qa-loop triage run=<run-id>                                   # turn reviewed reports into tasks + PLAN stubs
```

- **mode=guest** → public routes only (no auth needed).
- **mode=guest-smoke** → first few public pages (landing + auth). Fast public-surface check.
- **mode=guest-full** → all public pages.
- **mode=smoke** → first 1–3 core routes. Needs auth.
- **mode=core** → first ~6 routes. Needs auth. Default.
- **mode=full** → all routes in the manifest. Needs auth.

## Step 0 — preconditions (check, don't assume)

1. `chrome-qa-loop.config.json` exists (or create it from `templates/`).
2. For `smoke`/`core`/`full`: operator is logged into `${TARGET_BASE_URL}` in the Chrome profile connected to the DevTools MCP. For `guest*` modes: no login required — only public routes explored.
3. `chrome-devtools` MCP tools are available (`chrome-devtools-mcp` server, registered in this plugin's `.mcp.json`). Verify with `list_pages`. Fallback: `claude-in-chrome`.
4. The reports root `${REPORTS_ROOT}` exists (create if missing).

## Step 1 — EXPLORE + REPORT (delegated)

1. Mint a `run-id`: `qa-<YYYYMMDD>-<mode>` (read today's date via Bash `date`; the runtime forbids `Date.now()` in scripts).
2. Create `${REPORTS_ROOT}/<run-id>/`.
3. Dispatch the **`chrome-qa-explorer`** agent with: the `run-id`, the `mode`, the config, and a pointer to the PLAN (manifest + guardrails + report contract). It navigates, exercises scenarios, and writes one report file per finding immediately, plus `_INDEX.md`.
4. When it returns, surface to the operator: findings count by severity + the reports folder path.

> The explorer is read-only on prod. It never writes real data, completes payments, or triggers blocking dialogs.

## Step 2 — REVIEW (human gate)

Tell the operator: open the reports folder, review each finding, and set `status: triaged` on the ones to act on (or `rejected` to drop). This is the human-in-the-loop checkpoint — do not auto-proceed.

## Step 3 — TRIAGE (delegated)

On `/chrome-qa-loop triage run=<run-id>`: dispatch the **`qa-report-triage`** agent. It dedupes, prioritizes (P0–P3), locates likely code via `/graphify`, and emits `triage/TASKS.md` + per-fix `PLAN.md` stubs.

## Step 4 — IMPLEMENT (handoff, not in this loop)

Each accepted PLAN stub enters a **Feature-Development loop** (e.g. the `agentic-value-loops` plugin): plan → implement → test → quality gate → ship. This loop does **not** re-implement that machinery.

## Step 5 — REFLECT

Log the run: findings shipped, what the explorer missed, manifest gaps (new routes/screens to add). Update the manifest when the product changes. Re-run `mode=smoke` on fixed screens to verify (use `/verify`), closing the loop.

## Assets this loop uses

- **Agent** `chrome-qa-explorer` — browser-driving QA brain (per screen, per run).
- **Agent** `qa-report-triage` — review→implement bridge.
- **MCP** `chrome-devtools` (`chrome-devtools-mcp`, official Google Chrome DevTools MCP) — registered in `.mcp.json`. Verify with `list_pages`. Fallback: `claude-in-chrome`.
- **Token stack:** `rtk`, `context-mode`, `/caveman`, `/graphify` — when available.

## Guardrails (summary — full set in the PLAN)

Read-only on production · no blocking dialogs (use `handle_dialog`) · ground expectations in owner-docs before judging · secrets/PII = P0 (location only) · benign prompt-injection probe only · write a report per finding immediately (auto-saved to disk, no manual download).
