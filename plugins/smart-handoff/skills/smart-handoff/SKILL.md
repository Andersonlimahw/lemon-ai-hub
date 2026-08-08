---
name: smart-handoff
description: Save a resumable handoff when a session's context/usage budget is nearly exhausted, so any AI runtime (Claude Code, Codex, Antigravity/Agy, OpenCode, Gemini CLI, or any future agent) can pick the work up with zero lost context. Use proactively when you estimate you're at or above ~90-95% of your context window, token budget, or usage limit for this session, OR when the user explicitly asks to "save a handoff", "prepare handoff", "continue later", or invokes this skill by name.
---

# Session Handoff Protocol

Runtime-agnostic protocol for pausing long-running work in this repository without losing state. Any agent — this one or a different runtime entirely — must be able to read the latest handoff file and continue exactly where the previous agent stopped.

## When to trigger

Trigger this protocol proactively, without waiting to be asked, when **any** of these hold:

- You estimate your context window is at or above **~90-95% full** (approaching compaction/truncation).
- You are told or infer that the session's token/usage budget (session, daily, or weekly) is nearly exhausted.
- The user explicitly asks you to save a handoff, pause, or "continue later".
- You are about to be interrupted by a hard limit you can see coming (e.g. a plan/quota ceiling).

Do **not** trigger it for ordinary task completion — this is for *involuntary or anticipated* interruption of unfinished work, not for wrapping up a finished task.

## The protocol (steps 0-6, execute in order)

### 0 — Write the handoff file

Path: `docs/ai/handoff/<runtime_name>/<ddmmaaaa>/handoff_<step_name>.md`

- `<runtime_name>`: lowercase slug of the agent/CLI you are running as — `claude-code`, `codex`, `antigravity`, `opencode`, `gemini-cli`, etc. If genuinely unknown, use `unknown-runtime`.
- `<ddmmaaaa>`: today's date, day-month-year, no separators (e.g. `08082026`).
- `<step_name>`: short kebab-case slug naming *what phase was in flight* (e.g. `migrate-repositories`, `fix-typecheck-errors`, `wire-bff-routes`). Use `handoff_<step_name>.md` as the filename, e.g. `handoff_fix-typecheck-errors.md`.

Use the template in `templates/handoff.md` (in this skill directory) verbatim as the structure. It requires, at minimum:

- **Session identity**: runtime name, model, session/conversation id if the runtime exposes one (if not exposable, write `unknown` — never fabricate one), timestamp, git branch, git HEAD sha.
- **Goal**: the original user request, verbatim or faithfully summarized, plus any constraints/decisions the user already made (quote them).
- **State**: what is DONE (with commit shas), what is IN PROGRESS (exact file, exact line/function, exact error if mid-fix), what is NOT STARTED.
- **Next action**: the *single next concrete step* — not a vague "continue migration" but "run `npx tsc --noEmit`, fix the N errors it reports starting with `src/app/lib/repositories/notification-repository.ts:20`, pattern: `X`".
- **Verification commands**: exact commands to re-establish ground truth (typecheck, lint, test, build) with the last known-good output counts, so the next agent can diff "did I regress".
- **Resume pointer**: path to this file, and the path to the *previous* handoff file if one exists (chain them).

### 1 — Commit

Stage and commit everything reversible (code + the handoff file itself) with a semantic commit message. Never commit secrets — check `git status` output for anything suspicious before staging broadly. If the tree has partially-broken code (e.g. mid-refactor, typecheck failing), that is fine and expected — commit it anyway with a message that says so (e.g. `wip(migration): repositories mid-migration, typecheck 72 errors remaining`). A handoff is only useful if the tree matches the file.

### 2 — Push

Push the current branch to `origin` (create upstream tracking with `-u` if not already set). If push is rejected or blocked, say so explicitly in the response — do not silently skip it. Never force-push as part of this protocol.

### 3 — Handoff file must contain session data for continuation

Confirm before finishing that the committed handoff file includes:
- The commit sha you just created (append it after committing — a two-step write: draft, commit, then edit in the final sha, then amend or note it in a trailing line — whichever is simpler is fine, but the sha must end up in the file).
- The exact resume command for a fresh agent (see `templates/handoff.md`).

### 4 — Runtime-agnostic requirement

The handoff file must be **fully self-contained markdown** — no runtime-specific syntax, no references to "this conversation", no assumption the reader has any prior context. Write it so that a cold agent with only repo access and this file can resume. This is the test: *would a different AI product, with no memory of this session, know exactly what to do next by reading only this file plus the repo?*

### 5 — Stop and clean up

After steps 0-4 complete:
- Stop implementation work — do not start a new task.
- Terminate any background processes/tasks you started (dev servers, watch commands, background agents) rather than leaving them running unsupervised.
- Tell the user in plain language: what was saved, where, the commit sha, and that the session is paused pending a resume request.

### 6 — Resuming (for whichever agent picks this up next)

When a user says "implement the handoff" (in Claude, Codex, Antigravity, OpenCode, or elsewhere):

1. Find the latest handoff: `docs/ai/handoff/*/*/handoff_*.md`, sorted by date directory then file mtime — the most recent one across *all* runtime subfolders, not just your own runtime's folder (a Codex session may need to resume a Claude handoff).
2. Read it fully before doing anything else.
3. Run the verification commands it lists and diff against its recorded last-known-good output — confirm the tree state matches what the file claims (git HEAD sha, error counts). If it doesn't match, say so and ask before proceeding rather than guessing.
4. Resume from the exact "Next action" — do not re-derive the plan from scratch, do not re-litigate decisions already recorded under "Goal" and "Key decisions".
5. Continue applying this same protocol (steps 0-5) again when *you* approach your own limit — chain the handoff by linking back to the file you resumed from.

## Anti-patterns

- Writing a vague handoff ("continuing the migration") instead of a precise one (file, line, error, next command). A vague handoff wastes the next agent's first several tool calls rediscovering state that was already known.
- Skipping the commit/push because "the code doesn't fully work yet". Broken-but-committed beats uncommitted-and-lost.
- Fabricating a session/conversation ID when the runtime doesn't expose one. Write `unknown` — a next agent must not trust a made-up identifier.
- Forgetting to stop background processes, leaving orphaned dev servers or watchers running after the handoff.
- Writing the handoff *after* being cut off. This must be proactive — triggered by your own estimate of remaining budget, before you're forcibly interrupted.
