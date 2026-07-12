---
name: gh-ruleset
description: Manage GitHub repository rulesets via gh CLI.
---

# GitHub Ruleset Skill

Check, list, and view repository rulesets for branch protection and policies.

## Capabilities
- List rulesets: `gh ruleset list --repo <owner/repo>`
- View ruleset: `gh ruleset view <ruleset-id> --repo <owner/repo>`
- Check ruleset: `gh ruleset check <branch> [--repo <owner/repo>]` (check if branch is affected by any ruleset)

## Usage
Triggered when user says "ruleset", "branch protection", "rules", "check ruleset".
Rulesets are GitHub's modern replacement for branch protection rules.
