---
title: Worktree Hygiene (MANDATORY)
status: active
updated: 2026-07-16
related: [AGENTS.md, docs/rules/marketplace-sync.md]
---

# Rule: Clean up local worktrees and never commit `.claude/`

**Why:** Claude Code and other agents spawn short-lived git worktrees under
`.claude/worktrees/` for parallel or isolated work. Each worktree is a full
working copy (≈9 MB) plus its own `.git` link, and they accumulate fast — a
single multi-agent session can leave 5–6 of them behind. They are also
machine-local state: they embed absolute paths and per-machine refs, so
committing them to the repo (or even staging them by accident) is a leak
risk and pollutes `git status` forever after.

This rule exists so the repo stays clean and so a stale worktree never
lands in a commit by mistake.

## The invariants

1. **`.claude/` MUST be in `.gitignore`.** Any file or directory under
   `.claude/` is local machine state, never to be tracked.
2. **Before any `git commit`, `git push`, or PR creation, the local
   worktree list MUST contain only the main checkout plus the branch you
   are actively working on.** Stale agent worktrees MUST be removed.
3. **When an agent session (Claude, Codex, Agy, Gemini, OpenCode) ends,
   its worktree MUST be removed in the same turn** — not deferred to a
   later cleanup.

## How to clean up

List first (mandatory preflight per `AGENTS.md`):

```bash
rtk git worktree list
```

Remove a specific worktree:

```bash
rtk git worktree remove .claude/worktrees/<name> --force
```

Prune dead administrative refs after bulk removal:

```bash
rtk git worktree prune
```

One-shot bulk cleanup (paste-friendly):

```bash
git worktree list --porcelain | awk '/^worktree/ {print $2}' | grep '\.claude/worktrees/' | while read wt; do
  git worktree remove "$wt" --force
done
git worktree prune
```

## How to verify before committing

```bash
# Should print only the main checkout (and any branch you are on):
rtk git worktree list

# Should be empty under .claude/:
ls -la .claude/

# Should NOT show .claude/ in untracked:
rtk git status -s | grep -E '^\?\? \.claude' || echo "clean"
```

If `git status` shows `.claude/` as untracked, that means the `.gitignore`
entry is missing — restore it (see `## How to fix a leak` below).

## When you spawn or hand off to a sub-agent

- **Creating:** every agent that does its own branch work should work in a
  worktree at `.claude/worktrees/<id>`. Always record the path so it can
  be cleaned up.
- **Ending:** as the **last** step of any agent task that used a worktree,
  remove it. Don't leave it for "later" — later never comes, and the next
  session inherits a noisy `git worktree list`.
- **Handing off:** if you must leave a worktree for another agent to pick
  up, leave a note in `.claude/worktrees/<id>/.HANDOFF` with the next
  action; the receiving agent is responsible for cleanup.

## How to fix a leak

If `.claude/` was ever committed (visible in `git log -- .claude/`):

```bash
# 1. Remove from tracking but keep on disk (if you still need it):
git rm -r --cached .claude/

# 2. Add the gitignore entry (idempotent — see existing .gitignore):
grep -q '^\.claude/' .gitignore || printf '\n.claude/\n' >> .gitignore

# 3. Commit the cleanup:
git add .gitignore
git commit -m "chore(gitignore): stop tracking .claude/ (worktree-hygiene rule)"

# 4. (optional, if the worktrees are still useful) move them somewhere safe
#    outside the repo before deletion, or just `git worktree remove` them.
```

## Scope of the rule

Applies to **every** harness, every developer, every CI runner. The
`.claude/` directory is not project content — it is local state and
must never enter the index.
