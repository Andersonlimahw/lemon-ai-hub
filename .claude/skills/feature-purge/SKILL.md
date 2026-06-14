---
name: feature-purge
description: Safely remove an entire feature and every dead reference it leaves behind — not just the folder you point at, but the sibling folders in other architecture layers, the imports/registries/routes/i18n keys that point to it, and any newly-orphaned code. Verifies the quality gate stays 100% green and writes a Markdown removal report. Use when deleting a feature, screen, module, or directory and you need it gone WITHOUT leaving dead files or dead code. Triggers on /feature-purge <path>, "remove this feature", "delete this folder safely", "apaga essa feature sem deixar código morto", "limpa essa screen e as camadas".
---

# Feature Purge

Delete a feature for real. You give it one path; it finds the rest of the feature across the codebase, removes it, cleans every reference, and proves the quality gate is still green.

The danger this skill exists to kill: you delete `screens/Bets/` but leave `usecases/bets/`, the repository impl, the navigation route, the barrel `export *`, and 12 `import { Bets } from ...` lines — half-dead feature, red build, ghost code.

## Invocation

```
/feature-purge <path> [<path2> ...]
```

`<path>` is the primary folder/file to remove (usually the most visible one — a screen, a module). The skill derives the **feature slug** from it (folder name, normalized: `Bets` → `bets`/`Bets`) and uses that slug to discover the rest.

## Workflow (do in order, do not skip)

### 1. Scope — derive slug + map the primary target
- Resolve the path. Confirm it exists and is inside the repo.
- Derive `slug` from the leaf name. Keep both casings (`Bets`, `bets`) and obvious variants (`bet`, `betting`) — list them, you'll grep for all.
- List the primary target's files (these are the **main removals**).

### 2. Discover sibling targets across layers (the whole point)
Most codebases split one feature across parallel directories (layers, packages, test mirrors). Find the siblings by slug:
- Detect the project's layering from the path. Generic heuristic: take the repo's top source roots (e.g. `src/`, `app/`, `lib/`, `packages/*`, `test/`, `__tests__/`) and look for any directory or file whose name matches the slug under each root.
- Typical siblings: business logic, data/repository, domain/model, infrastructure, state/store, hooks, types, tests, fixtures, styles.
- Build a **candidate list**. Mark each `confident` (name is an exact slug match in a recognized layer) or `maybe` (fuzzy / shared dir).

### 3. Ask before the deep sweep
The slug match finds folders. It does NOT find scattered references (a single `import`, a route string, an i18n key, a feature-flag entry). Those need a repo-wide grep that is slower and noisier.

Use **AskUserQuestion** to confirm scope before the expensive search:
- Question: run the deep reference sweep (grep the whole repo for the slug + import paths)?
- Options: **Yes — full sweep (recommended)** / Targeted only (just the listed folders) / Let me edit the target list first.

If the user already said "be thorough" / "remove everything", skip the question and do the full sweep.

### 4. Find references (orphan hunt)
For every file about to be removed, grep the repo for things that point at it:
- `import` / `require` / re-export (`export * from`, barrel `index` files).
- Registry/DI wiring (a container that binds the repository, a `useCases` map).
- Navigation routes / deep links / route-name constants.
- i18n keys namespaced under the slug.
- Feature flags, config entries, menu/tab definitions referencing it.
Record each as a **reference to clean** with file + line.

### 5. Confirm the plan, then execute
Print the plan: main removals · sibling removals · references to clean. Then:
- Delete folders/files (`rm`/`git rm`).
- In each referencing file, surgically remove ONLY the orphaned lines (the import, the route entry, the barrel re-export, the i18n key). Do not refactor adjacent code (Karpathy surgical rule).
- After removing imports, remove anything those removals just orphaned (now-unused local imports/vars) — but only what YOUR change orphaned.

### 6. Quality gate — must end 100% green
Run the project's gate (typecheck / lint / i18n check / tests / build — whatever the repo has). If anything fails because a reference was missed, fix it and re-run. Loop until green. Never finish red.

### 7. Write the report
Write `feature-purge-<slug>-<YYYY-MM-DD>.md` (in the repo's docs/reports dir if one exists, else repo root). Use the template below.

## Report template

```markdown
# Feature Purge — <slug>

Date: <YYYY-MM-DD> · Invoked with: `<paths>`

## Removed — primary
- <path/file>  (N files)

## Removed — related (other layers)
- <path/file>  — <layer> — confident|maybe

## Modified — references cleaned
- <file>:<line> — removed <import|route|barrel export|i18n key|DI binding>

## Quality gate
- typecheck: ✅ | lint: ✅ | i18n: ✅ | tests: ✅ (<n> passed) | build: ✅

## Notes
- <anything skipped, any `maybe` left in place and why>
```

## Rules
- One path in, whole feature out. Always look for siblings in other layers — that is the core value.
- Ask before the repo-wide sweep unless the user opted into thoroughness.
- Surgical: every line you touch traces to removing this feature. No drive-by refactors.
- Never leave the gate red. If you cannot make it green, stop and report what blocks it instead of deleting more.
- Optimized: derive the slug once, grep once per scope, fix-and-recheck only the failing gate step.
