# brand-naming — portable agent instructions

Same methodology as `SKILL.md`, written for agents that read `AGENTS.md`
instead of Claude skill frontmatter: **Codex, OpenCode, Agy, Cursor, Aider,
Gemini CLI** and others.

## When to activate

The user asks to name or rename a company, product or feature, asks for a
"naming sprint", or asks you to validate a shortlist of candidate names.

## Install

Point your agent at this directory, or copy it into the project:

```bash
# Codex / OpenCode / Agy — merge into the repo-level agent instructions
cat plugins/brand-naming/AGENTS.md >> AGENTS.md

# Cursor
cp plugins/brand-naming/AGENTS.md .cursor/rules/brand-naming.md

# Aider
aider --read plugins/brand-naming/AGENTS.md

# Any agent — pass the raw prompt
cat plugins/brand-naming/AGENTS.md plugins/brand-naming/references/*.md
```

The `references/` files are the substance. Read the one relevant to the
stage you are in rather than loading all of them at once.

## The loop

```
GENERATE -> RESEARCH -> TRY TO DESTROY -> DISCARD OR PROMOTE
```

Never `GENERATE -> FALL IN LOVE -> JUSTIFY`.

## Hard rules

1. Never present a candidate you have not researched.
2. Never invent availability, URLs or search results. Unverified is
   `NOT VERIFIED`.
3. Never say "available for registration" — say "no material collision
   found in preliminary research".
4. Score never overrides collision. A collision is a gate, not a deduction.
5. Never force a winner. Non-convergence is a valid result.
6. Log every rejected name with its reason so no agent recycles it.
7. **Domains gate before red team, not after.** Verify domains on funnel
   survivors first. `NOT VERIFIED` (WHOIS and RDAP both failed/timed out)
   always demotes a candidate — it never means "likely free" and never
   advances to red team.

## Stages

| Stage | Read | Output |
|---|---|---|
| 1. Brief | — | `naming/00-brief.md` |
| 2. Longlist 300+ | `references/generation.md` | `naming/01-longlist.md` |
| 3. Funnel 300→30 | `references/scorecard.md` | `naming/02-funnel.md`, `naming/03-scorecard.md` |
| 4. Domains (transactional gate) | `references/domain-verification.md` | `naming/04-domains.md` |
| 5. Red team (domain-gate survivors only) | `references/collision-research.md` | `naming/05-collisions.md` |
| 6. Trademark | `references/trademark.md` | `naming/06-trademark.md` |
| 7. Final gates | `references/final-tests.md` | — |
| 8. Report | `references/output-format.md` | `naming/07-decision.md` |

Append every elimination to `naming/REJECTED.md` as you go, not at the end.

## Funnel

```
300+ -> 150 -> 75 -> 30 -> 15 -> 10 -> 5 -> 3 -> 1
```

Four categories, tracked separately: real words, rare words, linguistic
roots, grounded neologisms.

## Tooling

```bash
python3 scripts/check_domains.py --names candidates.txt \
        --tlds com com.br --confirm --json domains.json
```

DNS absence of NS is a pre-filter only. Quote RDAP results, never DNS ones.
If RDAP is unreachable, retry once with a direct WHOIS query (see
`references/domain-verification.md`) before reporting `NOT VERIFIED`.
Never fall back to the DNS pre-filter guess as if it were a verified
result.

## Two failure modes to avoid

**The MAVEN error.** A name that is a legitimate word can still be a
well-known developer tool. Always run the developer-ecosystem test
(GitHub, npm, PyPI, Maven Central, Apache, CNCF, Docker Hub). If the name
already means a tool your audience uses, discard it — other meanings do not
rescue it.

**The pharmaceutical coinage.** Latin-flavoured neologisms ending in `-um`,
`-ium` or mechanical root+suffix constructions score well on structure and
availability while sounding like a drug. Run the wrong-category test before
you get attached.
