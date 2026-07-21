---
name: error-fixer-loop
description: Recursive error-fix loop. Use when a bash command fails with a build/test/typecheck error, when the same class of error appears more than once, or when the harness itself needs a persistent rule so the error does not come back. Detect → root-cause → minimal fix → test → lint/typecheck → persist rule (SKILL.md / AGENTS.md / docs/rules) → audit with evidence. Cross-harness (Claude Code, OpenCode, Codex, Gemini, Agy).
---

# Error Fixer Loop

> Every fixed error must reduce the chance of the same error returning.
> If the loop ends at the patch, it failed — even if the patch worked.

Recursive skill: it closes the cycle between **execution**, **verification**, and **harness improvement**. Each run produces evidence (error found, decision made, test run, rule created, harness adjusted) and leaves the system harder to break in the same way.

Reference pattern: [Como Criar uma Skill Recursiva](https://lemon.dev.br/pt/blog/skill-recursiva-feedback-loop-harness).

---

## Trigger

Load this skill when ANY of these is true:

- A `bash`/`shell` tool call returns output matching a known build/test/typecheck error pattern (see `hooks/` — they auto-inject a reminder).
- The user says: "investigate this error", "fix this build", "test failed", "typecheck broken", "error keeps coming back".
- You are about to conclude a fix and have not yet written a persistent rule.

Do **not** load for:

- Transient network/permission errors (one-off, not repeatable).
- Errors in code owned by external vendors (no write access).
- Pure refactors with no failing signal (use `code-smell` or `architecture-deepener` instead).

---

## Protocol (non-negotiable)

Follow the steps in order. Skipping steps is the exact failure this skill prevents.

### 1. Capture the event
- Paste the **exact command** that failed.
- Paste the **exact error output** (trimmed to the relevant 50 lines).
- Note the **working directory** and **exit code**.

### 2. Declare the root cause in one sentence
Format: `<Component> fails because <specific reason>, triggered by <minimal repro>.`

If you cannot write this sentence yet, you are not at root cause — go back to step 1 with a tighter repro (see `bug-diagnostics` for repro-building techniques).

### 3. Classify the failure
Pick exactly one primary class. This decides where the fix lives.

| Class | Symptom | Where the fix belongs |
|---|---|---|
| `procedure` | Skill/agent didn't say to run the check | this `SKILL.md` or the calling skill |
| `missing-rule` | Project convention violated repeatedly | `docs/rules/<topic>.md` or `AGENTS.md` |
| `missing-test` | Bug escaped because no seam | test suite (add regression test) |
| `permission` | Tool denied, sandbox blocked, path forbidden | harness policy (`~/.config/opencode/permission.json`, Claude settings) |
| `observability` | No log, no checkpoint, no evidence | logging/checkpoint layer |
| `documentation` | Agent followed stale doc | doc file referenced by agent |

### 4. Apply the minimal fix
- Touch only what is load-bearing for the error.
- No drive-by improvements. No "while I'm here" refactors.
- Match existing style.

### 5. Run the relevant verification
- If a test exists: run it.
- If no test exists and the bug is repeatable: **write a failing test first**, then fix, then watch it pass.
- Always run `lint` and `typecheck` for TS/JS projects (`tsc --noEmit`, `biome check`, `eslint`).
- Paste the verification output in the final report.

### 6. Persist the rule
If the failure is **repeatable** (same class can appear again), write a rule. Use this decision tree:

```
Is it specific to THIS project?
  ├─ yes → docs/rules/<topic>.md in the project, link from AGENTS.md
  └─ no  → could other projects hit it?
        ├─ yes → this SKILL.md (anti-patterns section) or a new global rule
        └─ no  → record in the final report only; do NOT write a rule
```

Rule format (one line, operational, verifiable):

```markdown
- **<Rule name>**: <imperative sentence>. Verify with: <command or check>.
```

Good: `Never use `as any` to silence a TS error without a `// justified: <reason>` comment. Verify with: grep -rn "as any" src/ | grep -v justified.`
Bad: `Be careful with types.` (not operational, not verifiable)

### 7. Update the harness index
- If you wrote a rule in `docs/rules/`, link it from `AGENTS.md` under the relevant section.
- If you updated this `SKILL.md`, bump the version in `plugin.json` and note the change in the audit.

### 8. Generate the fix-prompt artifact
Write a dynamic fix-prompt file so the fix can be replayed, delegated, or audited later — even in another session or harness.

- **Location:** `.error-fixer-loop/<YYYYMMDD-HHMMSS>-<short-slug>.md` (create the folder if missing; add it to `.gitignore` if the project doesn't want it versioned).
- **Template:** use `templates/fix-prompt.md` from this plugin.
- **Format:** the file MUST follow the `senior-prompt-engineer` output shape — Role/Context, Task, Inputs/files, Constraints, Plan with `→ verify:` per step, Output contract, Feedback DO, Feedback DO NOT, and a closing `EXEC-MAP v1` fenced block.
- **Slug:** 3–6 lowercase words describing the error class (e.g. `ts2322-string-to-number`, `jest-module-not-found`).
- **Fill placeholders** with real values from steps 1–7. Never ship a template with `<...>` still in it.

This artifact is what makes the loop **recursive across sessions**: the next agent (or the same agent next week) can pick up the file and execute the fix without re-doing the investigation.

### 9. Final audit (mandatory)
Produce a short report answering ALL of:

- What was the failure (one sentence)?
- What was the root cause (one sentence)?
- What class (from step 3)?
- What changed (file:line list)?
- What verification ran (command + result)?
- What rule was persisted (file + one-line rule)?
- What fix-prompt was generated (path)?
- What risk remains?

Without the audit AND the fix-prompt, the loop is not closed.

---

## Escopo de escrita (write scope)

This skill MAY propose or edit:

- This `SKILL.md` (anti-patterns, protocol refinements).
- Project rule files: `docs/rules/*.md`, `docs/ai/rules/*.md`, `AGENTS.md`, `CLAUDE.md`.
- Test files that reproduce the original error.
- Evals in this plugin (`evals.json`).
- Fix-prompt artifacts under `.error-fixer-loop/` (always allowed; never requires confirmation).

This skill MUST NOT:

- Rewrite unrelated rules or remove guardrails.
- Change security/permission policy without explicit user confirmation.
- Mask a failing test to make verification pass.
- Delete a pre-existing failing test without documenting why.
- Use `as any`, `@ts-ignore`, `eslint-disable` or equivalent **to silence** an error without an inline `// justified: <reason>` comment and a rule entry.

---

## Anti-patterns (hard no)

- ❌ Concluding with "fixed" but no test run.
- ❌ Concluding without generating the fix-prompt artifact in `.error-fixer-loop/`.
- ❌ Shipping a fix-prompt with unfilled `<placeholders>`.
- ❌ Adding a rule based on personal preference (no evidence).
- ❌ Widening scope because "we might need it later".
- ❌ Removing a guardrail to reach "done" faster.
- ❌ Accepting a green test that does not cover the original failure.
- ❌ Writing a rule longer than one operational sentence.
- ❌ Updating the skill when the learning belongs to the project (and vice-versa).

---

## Recursive improvement criteria

Update **this** `SKILL.md` only when ALL are true:

1. The current protocol allowed a repeatable failure.
2. The new rule is short and generalizable across projects.
3. The change reduces future ambiguity.
4. There is verification or evidence supporting it.

Update a **project** rule file when the learning is project-specific (e.g., "in this repo, blog posts need both `index.md` and `index-pt-br.md`").

Create an **eval** (`evals.json`) when the failure can be simulated (e.g., "agent concludes without running tests", "agent uses `as any`").

---

## Hook integration

Two hooks auto-detect build/test errors in bash output and inject a reminder to run this loop:

- **Claude Code**: `hooks/error-fixer-loop-hook.sh` — register as `PostToolUse` on `Bash`.
- **OpenCode**: `hooks/error-fixer-loop.ts` — plugin listening on `tool.execute.after`.

Both are passive: they only print a one-line reminder. They never block, never mutate the tool result, never auto-run the fix.

Detected patterns (extend via `ERROR_PATTERNS` in the TS hook or the regex in the shell hook):

- TypeScript: `error TS\d+`
- Module resolution: `Cannot find module`, `Module not found:`, `Unable to find a specification for`
- Build: `BUILD FAILED`, `GRADLE.*FAILED`, `npm ERR!`, `pod install.*fail`
- Tests: `Test Suites:.*[1-9]\d* failed`, `Tests:.*[1-9]\d* failed`, `jest.*FAIL`
- iOS/RN: `NitroModules.*not found`
- Python: `ModuleNotFoundError`, `ImportError`, `AssertionError`, `FAILED tests/`
- Go: `FAIL\s+\S+`, `undefined:`, `cannot find package`
- Rust: `error\[E\d+\]`, `panicked at`
- Java/Kotlin: `BUILD FAILURE`, `Compilation failure`, `> Task .* FAILED`

Add new patterns only when you have seen them fire in the wild — not speculatively.

---

## Layered feedback model

Do not pile every learning into this file. Four layers:

1. **Execution** — the current task (tools, commands, files).
2. **Verification** — tests, typecheck, lint, evals.
3. **Operational memory** — `docs/rules/`, `AGENTS.md`, this `SKILL.md`.
4. **Harness evolution** — new tools, permission changes, new evals, dispatch tweaks.

Layer 4 is the most sensitive. Changes there must be small, verified, and reversible.

---

## References

- Article: https://lemon.dev.br/pt/blog/skill-recursiva-feedback-loop-harness
- Legacy hook: `~/.claude/hooks/error-fix-loop-hook.sh` (replaced by `hooks/error-fixer-loop-hook.sh`)
- Companion skill: `bug-diagnostics` (deep repro/hypothesis work when step 2 stalls)
- Harness rules: `~/.config/opencode/AGENTS.md` (global), project `AGENTS.md` (local)
