---
name: git-hooks
description: Manage Git hooks for automating pre-commit, pre-push, and other lifecycle events.
---

# Git Hooks Skill

Install, manage, and troubleshoot client-side Git hooks.

## Capabilities
- List hooks: `ls .git/hooks/`
- View hook content: `cat .git/hooks/<hook-name>`
- Install hook: Create executable script in `.git/hooks/<hook-name>`
- Remove hook: `rm .git/hooks/<hook-name>`
- Bypass hook: `git commit --no-verify` / `git push --no-verify`
- Share hooks: Use `.githooks/` directory with `git config core.hooksPath .githooks`
- Available hooks: `pre-commit`, `prepare-commit-msg`, `commit-msg`, `post-commit`, `pre-push`, `post-checkout`, `post-merge`, `pre-rebase`, `post-rewrite`, `pre-auto-gc`

## Common Hooks

### pre-commit
```bash
#!/bin/sh
# Run linters, tests, or format checkers
npx lint-staged
```

### commit-msg
```bash
#!/bin/sh
# Validate conventional commit format
grep -Eq "^(feat|fix|chore|docs|refactor|test|style)\(.*\): .{1,72}" "$1"
```

### pre-push
```bash
#!/bin/sh
# Run full test suite before push
npm test
```

## Usage
Triggered when user says "hooks", "git hooks", "pre-commit hook", "pre-push hook".
For shared hooks, use `.githooks/` directory approach. Make hooks executable with `chmod +x`.
