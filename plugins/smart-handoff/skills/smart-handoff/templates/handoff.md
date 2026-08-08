<!--
Template for docs/ai/handoff/<runtime_name>/<ddmmaaaa>/handoff_<step_name>.md
Fill every section. Do not leave placeholders like "TBD" — if something is
genuine unknown, write "unknown" explicitly rather than omitting the field.
This file must be readable and actionable by an agent with NO memory of the
session that created it, running in a DIFFERENT AI product.
-->

# Handoff: <short title of the phase in flight>

## Session identity

- **Runtime**: <claude-code | codex | antigravity | opencode | gemini-cli | unknown-runtime>
- **Model**: <model id/name if known, else "unknown">
- **Session/conversation id**: <id if the runtime exposes one, else "unknown">
- **Timestamp**: <ISO 8601, e.g. 2026-08-08T23:45:00Z>
- **Git branch**: <branch name>
- **Git HEAD sha (before this handoff's commit)**: <sha>
- **Handoff commit sha (this file + code, added after committing)**: <sha — fill in after step 1>
- **Previous handoff (if any)**: <relative path to prior handoff_*.md, or "none — first handoff in this chain">

## Goal (verbatim/faithful summary of the user's request)

<Paste or closely summarize the original ask. Quote any explicit constraints
or decisions the user made along the way — these are not up for
re-litigation by whoever resumes.>

## Key decisions already made (do not re-ask)

- <Decision 1 — what was chosen, and why, in one line>
- <Decision 2>
- <...>

## State

## DONE (committed, verified)

- <Item> — commit `<sha>` — verified by: <command + result, e.g. "npx tsc --noEmit: 0 errors">
- <Item> — commit `<sha>`

### IN PROGRESS (uncommitted or partially done — be exact)

- **File**: `<exact path>`
- **Function/section**: `<exact name or line range>`
- **What's broken/incomplete**: <precise description — an error message, a
  missing case, a half-written function>
- **Why it's this way**: <one line of reasoning, if non-obvious>

### NOT STARTED

- <Task 1 — one line>
- <Task 2>

## Next action (the single next concrete step)

<Not "continue the migration". Instead: "Run `npx tsc --noEmit`. It will
report ~72 errors. Fix them in this order: (1) src/app/lib/repositories/
notification-repository.ts:20 — `select` doesn't exist on type `never`,
caused by X, fix by Y. (2) ...". If you don't know the exact next step,
say what you were about to try and why.>

## Verification commands (re-establish ground truth)

Run these, in order, and compare against the last-known counts below. If
they don't match, STOP and tell the user before proceeding — the tree may
not match what this file claims.

```bash
git log --oneline -1        # expect: <sha> <subject>
git status --short           # expect: <clean, or list of expected dirty files>
npx tsc --noEmit              # last known: <N errors, or "clean">
npx eslint .                  # last known: <clean | N issues>
npx vitest run --reporter=basic  # last known: <PASS (N) FAIL (0)>
```

## Resume pointer

- This file: `docs/ai/handoff/<runtime_name>/<ddmmaaaa>/handoff_<step_name>.md`
- To resume: read this file fully, run the verification commands above,
  then proceed from "Next action". Do not re-derive the plan.
- When you (the resuming agent) approach your own budget limit, repeat this
  same protocol and set "Previous handoff" above to point back to this file.
