---
name: adversarial-setup-review
description: Principal-engineer adversarial review for AI workspace setup changes, agent/skill topology, AGENTS.md/CLAUDE.md contracts, and plugin marketplace registration. Use when reviewing a PR, diff, or setup plan for overengineering, missing verification, broken orchestration, stale instructions, or weak agent boundaries.
---

# Adversarial Setup Review

Goal: block fragile AI workspace setups before they become permanent project instructions.

## Review Process

1. Establish scope:
   - PR, branch diff, staged diff, or proposed setup plan.
   - Base branch and target project/domain.
   - Whether files are executable config, docs-only instructions, plugin manifests, skills, or agents.
2. Load evidence:
   - `AGENTS.md`, `CLAUDE.md`, plugin manifests, marketplace file, changed skill files, changed agent files, and validation output.
   - If a claim is not backed by a file or command, treat it as unproven.
3. Review as a principal engineer:
   - Assume the author is junior and the setup may be plausible but incomplete.
   - Challenge every new skill, agent, and rule for necessity, trigger clarity, and verification.
   - Prefer fewer stronger artifacts over broad vague orchestration.
4. Report findings first:
   - Critical issues.
   - Non-blocking suggestions.
   - Nitpicks only when they prevent future confusion.
5. End with a merge verdict.

## Failure Modes To Hunt

- Marketplace drift: plugin directory added, renamed, or removed without matching marketplace entry.
- Manifest drift: marketplace metadata no longer matches `plugin.json` after changing description, version, license, or keywords.
- Hollow orchestration: agent names exist, but delegation inputs, outputs, and verification gates are undefined.
- Overbroad agents: generic specialists created without a real project boundary.
- Duplicated contracts: long rules copied into both `AGENTS.md` and `CLAUDE.md` instead of one canonical source.
- Unsafe symlink plan: recommends `CLAUDE.md -> AGENTS.md` without preserving existing content or fallback pointer.
- Weak skill trigger: description does not say when the skill should load.
- Bloated skill: body teaches obvious model knowledge instead of local procedure.
- Missing validation: no `quick_validate.py`, plugin validation, JSON parse, marketplace invariant, or line-level evidence.
- Unowned cross-domain flow: backend/frontend/mobile/data integration lacks one responsible orchestrator.

## Output Format

```md
## Adversarial Review

### Critical Issues
**[Category]** `path:line`
> Problem.
> Why this can fail.
> Required fix.

### Suggestions
**[Category]** `path:line`
> Improvement.
> Why it matters.
> Suggested direction.

### Residual Risk
- Risk that remains after the current diff.

### Verdict
CHANGES REQUESTED | APPROVE WITH COMMENTS | LGTM
```

## Rules

- Cite exact file lines for every finding.
- Do not invent failures; if evidence is weak, state the missing evidence.
- Treat docs-only changes as production behavior when future agents will obey them.
- Separate must-fix correctness issues from taste.
- If no blocking issue exists, say so directly and list residual risk.
- Never praise vague scope. Require a clear owner, trigger, and verification path.
