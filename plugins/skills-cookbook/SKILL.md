---
name: skills-cookbook
description: Example-prompt cookbook for the hub's skills — recipes, combos, and anti-patterns. Use when the user wants example prompts, asks how to use or combine skills (project understanding, feedback loops, product, marketing, design/frontend), or wants to reduce cognitive load while navigating the skill catalog.
---

# Skills Cookbook

Ready-to-paste prompt recipes that teach efficient use of this hub's skills — less trial-and-error, less cognitive load. Every recipe names the skills by their exact identifier, uses `<placeholders>`, and ends with a verifiable success criterion.

## How to use

1. Pick the track (below) and the recipe that matches your situation.
2. Copy the prompt, fill in the `<placeholders>`.
3. Paste it in chat. On non-trivial requests, the hub's standard pipeline runs on top: `senior-prompt-engineer` → `skills-selector` → `smart-dispatch`.
4. Check the result against the recipe's **Success:** line before accepting it.

## Combination rules

1. **Combine different layers, never the same layer twice.** Example: visual direction (`frontend-design`) + design data (`ui-ux-pro-max`) + compliance (`a11y-audit`) works; two aesthetics together doesn't.
2. **Max ~3 skills per prompt.** More than that dilutes context and weakens all of them.
3. **One aesthetic at a time.** `minimalist-ui`, `industrial-brutalist-ui`, `high-end-visual-design`, and `emil-design-eng` are mutually exclusive art directions.
4. **One loop driver at a time.** `karpathy-loop`, `error-fixer-loop`, `api-test-loop`, and `chrome-qa-loop` own their cycle; chain them in sequence, never run two in parallel on the same target.
5. **Name the skill exactly** in the prompt — the selector activates with far more precision.
6. **Always close with a verifiable success criterion** (Karpathy: strong verifiable goals let the agent iterate independently).

## Anti-patterns (never combine)

| Skills | Type | Rule |
|---|---|---|
| `minimalist-ui` × `industrial-brutalist-ui` × `high-end-visual-design` × `emil-design-eng` | mutually exclusive | pick ONE art direction per screen/project |
| `design-taste-frontend` × any aesthetic above | overlap | use taste as a general baseline OR a specific aesthetic, not both |
| `feature-flag` × `feature-flags` | overlap | one-shot implementation/fix OR continuous CI tracking — pick by objective, not both as driver |
| `code-smell` × `code-smell-detector` | overlap | on-demand analysis OR continuous CI enforcement — pick by objective |
| `doc-driven-grilling` × `task-interrogator` | overlap | same base grilling; one produces docs (ADRs/glossary), the other produces tasks — fine in sequence, not as parallel drivers |
| `competitors` × `competitor-profiling` | overlap | broad market scan OR deep single-player profile |
| `webapp-testing` × `playwright` × `chrome-qa-loop` | overlap | point-in-time toolkit OR scripted E2E OR exploratory loop — pick by goal |
| `image` × `imagegen` × `brandkit` | overlap | one-off asset OR frontend imagery OR brand board |
| `caveman` × `teaching` / `learning-output-style` | conflicting goals | max compression vs. didactic — never in the same turn |
| `copywriting` × `copy-editing` | pass conflict | writing from scratch OR editing existing copy; sequential ok, simultaneous not |
| `karpathy-loop` × `error-fixer-loop` (same target) | driver conflict | one loop owns the cycle; the other enters as a step, not as driver |
| `X` × `X-advisor/-watch/-runner/-guardian/-detector` | hub-wide rule | one-shot (investigate/fix now) × continuous (CI gate) — pick by objective, never both as driver of the same pass (`async-patterns`×`async-advisor`, `bundle-analyzer`×`bundle-watch`, `load-test`×`load-test-runner`, `chaos-test`×`chaos-runner`, `a11y-audit`×`a11y-guardian`) |
| `create-plugin` × `plugin-creator` × `plugin-generator` × `skill-creator` | generator overlap | ONE generator per artifact; in this repo the canonical layout from `validate_plugins.py` wins |
| `security-best-practices` × `security-guidance` | overlap | code checklist OR contextual guidance — don't stack |
| `playwright` × `playwright-interactive` | overlap | scripted E2E OR interactive session |
| `openapi-generate` × `openapi-hub` | overlap | one-shot spec generation OR continuous multi-spec management |
| `cli-creator` × `cli-generator` | overlap | pick by target runtime (Codex-composable vs. Bun spec-first) |
| `imagegen` × `imagegen-frontend-web` / `imagegen-frontend-mobile` | overlap | general purpose OR frontend-specific — by asset purpose |

## Combos that work

- `frontend-design` + `ui-ux-pro-max` + `a11y-audit` — direction + data + compliance
- `image-to-code` + `ui-ux-pro-max` — screenshot → code with design tokens
- `copywriting` + `marketing-psychology` + `emails` — message + persuasion + channel
- `seo-audit` + `ai-seo` + `schema` — classic SEO + AI search + structured data (complementary, not redundant)
- `pricing` + `paywalls` + `churn-prevention` — end-to-end monetization funnel
- `product-marketing` + `launch` + `social` — positioning + launch + distribution
- `architecture-deepener` + `llm-wiki-curator` + `teaching` — understand + document + learn
- `api-test-loop` + `verification-before-completion` — validation loop + completion gate
- `chrome-qa-loop` → `bug-diagnostics` → `error-fixer-loop` — finding → diagnosis → fix sequence (never simultaneous)
- `karpathy-guidelines` + `karpathy-recipe` + `karpathy-loop` — principles always, recipe for large work, loop for metrics (complementary)
- `vercel-react-best-practices` + `vercel-optimize` + `bundle-analyzer` — patterns + vitals + bundle weight
- `openapi-generate` + `postman-generator` + `api-test-loop` — spec → collection → live validation
- `db-index-advisor` + `supabase-postgres-best-practices` — correct index on correct modeling
- `code-review-expert` + `commit-quality` + `pr-review-canvas` — review + hygiene + presentation
- `notion-spec-to-implementation` + `doc-driven-grilling` — spec grilled before it becomes code

## Tracks

| Track | Sub-skill | Focus |
|---|---|---|
| Project understanding | [prompts-project-understanding](skills/prompts-project-understanding/SKILL.md) | cut cognitive load: architecture, wiki, guided learning, spec grilling |
| Feedback loops | [prompts-feedback-loops](skills/prompts-feedback-loops/SKILL.md) | continuous validation: API, exploratory QA, error fixing, optimization |
| Product | [prompts-product](skills/prompts-product/SKILL.md) | positioning, monetization, onboarding, launch, user feedback |
| Marketing | [prompts-marketing](skills/prompts-marketing/SKILL.md) | copy, SEO + AI search, email, social, brand |
| Design & Frontend | [prompts-design-frontend](skills/prompts-design-frontend/SKILL.md) | visual direction, aesthetics, screenshot-to-code, accessibility |
| Karpathy method | [prompts-karpathy](skills/prompts-karpathy/SKILL.md) | guidelines, recipe for large work, principle-based review, metric loop |
| Vercel & React | [prompts-vercel-react](skills/prompts-vercel-react/SKILL.md) | best practices, optimization, composition, view transitions, RN/Expo, deploy |
| Engineering quality | [prompts-engineering-quality](skills/prompts-engineering-quality/SKILL.md) | PR review, async, database, threat model, load/chaos, i18n |
| APIs & CLIs | [prompts-apis-clis](skills/prompts-apis-clis/SKILL.md) | OpenAPI, Postman, agent-friendly CLIs, CLI wrapping |
| Mobile & Release | [prompts-mobile-release](skills/prompts-mobile-release/SKILL.md) | iOS/Android go/no-go, App Store Connect, Play API, ASO |
| Data & Backend | [prompts-data-backend](skills/prompts-data-backend/SKILL.md) | Supabase/Postgres, Firebase, database decisions, incidents |
| Knowledge & Notion | [prompts-knowledge-notion](skills/prompts-knowledge-notion/SKILL.md) | decision capture, meetings, research docs, spec-to-code, persistent learning |
| Meta-harness | [prompts-meta-harness](skills/prompts-meta-harness/SKILL.md) | authoring skills/plugins, hooks, multi-agent orchestration, migration, tokens |
| A–Z index | [prompts-catalog-index](skills/prompts-catalog-index/SKILL.md) | every plugin in the hub with a one-line when-to-use hint |

## Guardrails

- All prose — recipes, hints, headers — is written in English, matching this project's language policy. Skill identifiers are always exact.
- The cookbook points and teaches — it does not replicate the content of the target skills.
- Every skill cited exists in this repo's `plugins/`; if a recipe cites something that no longer exists, the recipe is broken and must be fixed.
