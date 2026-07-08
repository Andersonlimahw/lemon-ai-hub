---
name: skills-selector
description: Meta-skill gatekeeper that runs FIRST on every task to decide which other skill(s) — if any — should activate. Analyzes the user request, matches it against a ranked catalog (frontend-design, ui-ux-pro-max, superpowers/planning, git-*, mcp-builder, smart-dispatch, claude-api, etc.), and emits a tight SELECTION plan so other skills are loaded on-demand only. Minimizes token/context consumption by refusing to activate heavy skills unless clearly justified. Triggers on ANY user instruction that could plausibly benefit from a specialized skill — i.e. essentially every turn that starts new work. Keywords: "plan", "design", "ui", "ux", "implement", "build", "create", "fix", "refactor", "commit", "pr", "review", "test", "debug", "deploy", "mobile", "video", "mcp", "skill", "architecture", "api", "ci", "docs", "copy", "social", "setup", "doctor".
allowed-tools: Read, Grep, Glob
---

# Skills Selector — The Skill That Picks Skills

> Prime directive: you are the **first gate** for every task. Decide which skill(s) deserve to load, or declare that none are needed. Every token spent on an unused skill is a token stolen from the user's real work.

## Why this skill exists

Loading a skill injects hundreds to thousands of tokens into the context. Many CLIs now ship 20–80+ skills. Without a gatekeeper, every plausible match fires, the context fills with orchestration noise, and the model gets slower, more expensive, and more confused. `skills-selector` fixes that by running once at the top of a task and committing to a **minimal, justified selection**.

This skill is intentionally short. If you want depth, call the chosen skill — don't add it here.

---

## Protocol — run exactly these steps, in order

### 0. Consume the EXEC-MAP contract if present (skip re-classification)

If stage-0 (`senior-prompt-engineer`) already ran, an `EXEC-MAP v1` block is in context. **Consume it — do not re-classify from scratch:**
- Take `intent` directly as the primary intent (skip step 1).
- Seed candidates from `EXEC-MAP.skills` (skip step 2's catalog lookup; still run step 3 rank/prune to validate, cap at 2, and drop heavy skills lacking signal).
- Carry `effort`/`tokens` into `BUDGET`.
- Add `MAP: consumed` to the emitted block so the audit trail shows stage-0's work wasn't redone.

Only fall through to steps 1–2 when **no** EXEC-MAP block exists.

### 1. Classify the request (inline, silent) — only if no EXEC-MAP

Assign the user's turn to **one primary intent** from:

| Intent                      | Typical verbs / nouns                                        |
| --------------------------- | ------------------------------------------------------------ |
| `plan`                      | "plan", "design the approach", "how should we", "architect"  |
| `design-ui`                 | "design", "redesign", "landing page", "polish UI", "figma"   |
| `build-code`                | "implement", "build", "create <component/feature>", "add"    |
| `fix-bug`                   | "fix", "not working", "error", "broken", "regression"        |
| `refactor`                  | "refactor", "simplify", "clean up", "extract"                |
| `review`                    | "review", "audit", "check diff", "is this safe"              |
| `test`                      | "write tests", "coverage", "e2e", "unit test"                |
| `git-op`                    | "commit", "pr", "branch", "changelog", "release notes"       |
| `debug`                     | "debug", "trace", "repro", "investigate"                     |
| `docs`                      | "readme", "document", "write docs", "api doc"                |
| `content`                   | "copy", "tweet", "post", "landing copy", "pitch"             |
| `media`                     | "video", "remotion", "heygen", "thumbnail", "render"         |
| `mcp-or-skill`              | "mcp server", "new skill", "create a skill", "extend"        |
| `config-harness`            | "hook", "settings.json", "permission", "keybinding"          |
| `ops`                       | "deploy", "ci", "docker", "k8s", "pipeline"                  |
| `trivial-or-chat`           | Q&A, clarification, status checks, tiny edits                |

Ambiguous? Ask yourself: *what artifact does the user expect at the end?* That answer usually disambiguates.

### 2. Match candidates from the catalog

Look up the intent in the **Catalog** below. A request can match multiple rows — that's fine, rank them next.

3. **Rank and prune (token-aware)**

Apply these rules, in order — each one can drop a candidate:

1. **RTK Bypass Dispatch for Boilerplate.** If the task is a repetitive, mechanical fix (lint, typecheck, test fixes in test files, or i18n), ALWAYS select `smart-dispatch` and prioritize the correct bypass command (e.g., `rtk gemini --yolo` as primary). Emit `BUDGET: low`.
2. **Trivial requests stay inline.** If the task is a single-line edit, a status check, a factual question, or something the model can handle in under ~3 tool calls: **select nothing**. Emit `SKILLS: []`.
3. **Cap at 2 skills per turn.** Orchestration cost grows super-linearly. If you picked 3+, drop the lowest-weight one or split the work.
4. **Prefer narrow over broad.** `git-commit` beats `git-master` for a commit. `ui-polisher` beats `ui-ux-pro-max` for a minor CSS tweak.
5. **Heavy skills need explicit signal.** `ui-ux-pro-max`, `frontend-design`, `gsd:new-project`, `superpowers` (if present), `remotion-best-practices`, `heygen-best-practices`, `mcp-builder`, `Agent Development` — only if the user names their domain or explicitly asks for depth.
6. **Never chain design + plan + build in one turn.** Pick the nearest waypoint and let the user confirm before escalating.
7. **If a domain skill and a meta-skill both match, pick the domain one.** E.g. for "write a PR", `git-pr-create` beats `smart-dispatch`.

### 4. Emit the selection block, then hand off

Print **exactly one** block at the top of your response, then stop this skill and let the chosen skill(s) take over. Do not repeat the block. Do not wrap it in prose.

```
SKILLS: [skill-a, skill-b]   # [] means "none — handle inline"
INTENT: <one-word>
REASON: <≤15 words, concrete>
BUDGET: <low | medium | high>   # token/context intent
MAP:    <consumed | none>       # consumed = seeded from senior-prompt-engineer EXEC-MAP
NEXT:   <first concrete action>
```

If `SKILLS: []`, proceed inline without invoking any skill. If one or more skills are selected, **invoke them via the platform's Skill mechanism** (Claude Code: `Skill` tool; Codex: `/<skill>` or skill invocation; Gemini: slash command / skill call). Never paraphrase a skill — always invoke it so its authoritative content drives behavior.

---

## Catalog — keyword → skill (keep compact; depth lives inside each skill)

Legend: **P** = platform scope (C=Claude, X=Codex, G=Gemini, L=lemon-code built-in, any=portable).
Weight is a rough token cost: `·` tiny, `··` small, `···` medium, `····` heavy. Prefer lower-weight skills when the task is small.

### Planning & orchestration
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `smart-dispatch`               | any   | ··   | Multi-step feature spanning ≥2 models/agents               |
| `superpowers` (if installed)   | C     | ···· | User explicitly asks for "superpowers" or deep plan kit    |
| `gsd:plan-phase`               | C/X   | ···  | Phase-level plan inside an existing GSD project            |
| `gsd:discuss-phase`            | C/X   | ··   | Gathering phase context through Q&A                        |
| `gsd:new-project`              | C/X   | ···· | Bootstrapping a brand-new GSD project                      |
| `gsd:do` / `gsd:next`          | C/X   | ·    | "what's next" routing inside GSD workflow                  |
| `gsd:fast` / `gsd:quick`       | C/X   | ·    | Trivial or quick guaranteed-atomic task                    |

### Design & UI
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `frontend-design`              | C/X   | ···· | From-scratch page/component with strong visual identity    |
| `ui-ux-pro-max`                | C/X   | ···· | Redesign, design system, accessibility sweep, figma import |
| `ui-polisher` (lemon)          | L     | ··   | Small polish: spacing, hierarchy, micro-interactions       |
| `web-design-guidelines`        | L     | ··   | Principles Q&A: typography, spacing, color                 |
| `vercel-react-native-skills`   | C     | ···  | React Native / Expo perf, nav, lists                       |

### Frontend & mobile code
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `frontend` (lemon)             | L     | ··   | React/Next/Tailwind component work                         |
| `react-native` (lemon)         | L     | ··   | RN/Expo screens, animations                                |
| `vercel-react-best-practices`  | L     | ··   | Vercel/ISR/edge/bundle tuning                              |
| `mobile-fix-release-certificates` | C  | ··   | Android Google Sign-In DEVELOPER_ERROR                     |

### Backend / language
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `nodejs-backend`               | L     | ··   | REST, middleware, auth in Node/Bun                         |
| `java-backend`                 | L     | ··   | Spring/JPA/Maven                                           |
| `csharp-backend`               | L     | ··   | .NET / ASP.NET / EF                                        |
| `golang`                       | L     | ·    | Go idiomatic code, goroutines                              |
| `typescript-expert`            | L     | ·    | Advanced TS types/generics                                 |
| `javascript-expert`            | L     | ·    | Modern JS, Bun, ESM                                        |
| `python-ml`                    | L     | ··   | Python, pandas, ML                                         |

### Git workflow
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `git-commit`                   | any   | ·    | Creating a commit from staged/unstaged changes             |
| `git-branch`                   | any   | ·    | Creating/switching/cleaning branches                       |
| `git-pr-create`                | any   | ··   | Opening a PR with semantic title + body                    |
| `git-review` / `review`        | any   | ··   | Code review of diff/PR                                     |
| `git-changelog`                | any   | ·    | Generating changelogs / release notes                      |
| `git-master`                   | any   | ··   | Broad flow automation across commit+branch+PR              |

### Quality, testing, debugging
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `testing`                      | L     | ··   | TDD, unit/integration strategy                             |
| `webapp-testing`               | L     | ··   | Playwright / Cypress / Testing Library                     |
| `backend-testing`              | L     | ··   | API tests, DB mocks, integration                           |
| `api-test-loop`                | any   | ···  | REST API validation loop via CURL (REST, security, perf, inputs, outputs) |
| `postman-generator`            | any   | ··   | Create Postman collections, environments, JS tests and run Newman        |
| `systematic-debugging`         | L     | ··   | Non-trivial bug, needs repro/isolate/hypothesize           |
| `auto-fix`                     | L     | ·    | Build/TS/test error with known pattern                     |
| `error-fix-loop`               | any   | ···  | Any error requiring full quality cycle + docs/rules update |
| `security-review`              | any   | ··   | Security sweep of PR / diff                                |
| `refactoring-pro` / `simplify` | any   | ·    | Reduce complexity, extract, DRY                            |

### AI / agents / MCP / skills
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `claude-api`                   | C     | ··   | Building on Anthropic SDK, prompt caching, tool-use        |
| `graphify`                     | any   | ···  | Codebase/architecture question AND `graphify-out/` exists — query graph before raw exploration |
| `mcp-builder` / `create-mcp`   | any   | ···  | New MCP server with FastMCP or official SDK                |
| `skill-creator`                | any   | ··   | Creating a new skill (use AFTER this selector decides)     |
| `Agent Development`            | C     | ···  | Designing a new sub-agent / agent definition               |
| `ai-setup`                     | L     | ··   | Configure providers, models, keys                          |
| `azure-ai`                     | L     | ··   | Azure OpenAI / Cognitive Services                          |

### Media, content, marketing
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `remotion-best-practices`      | any   | ··   | React video with Remotion                                  |
| `heygen-best-practices`        | any   | ··   | HeyGen AI avatar video                                     |
| `copywriting`                  | any   | ·    | Landing copy, CTA, headline                                |
| `social-content`               | any   | ·    | LinkedIn / X / IG / social strategy                        |
| `lemon-blog-post`              | C/G   | ··   | Lemon blog article generation                              |
| `seo-audit`                    | L     | ··   | SEO audit, meta, Core Web Vitals                           |

### Documents & files
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `xlsx`                         | any   | ··   | Excel / CSV / spreadsheets                                 |
| `pptx`                         | L     | ·    | PowerPoint slide generation                                |
| `docx`                         | L     | ·    | Word doc generation                                        |
| `pdf`                          | L     | ·    | PDF manipulation                                           |

### Harness, config, workflow
| Skill                          | P     | W    | Activate when                                              |
| ------------------------------ | ----- | ---- | ---------------------------------------------------------- |
| `update-config`                | C     | ·    | Edit settings.json, hooks, permissions                     |
| `fewer-permission-prompts`     | C     | ·    | Prune permission prompts from transcripts                  |
| `keybindings-help`             | C     | ·    | Rebind Claude Code keys / chords                           |
| `loop` / `schedule`            | C     | ·    | Recurring tasks, cron, polling                             |
| `find-skills`                  | any   | ·    | User asks "is there a skill for X"                         |
| `init`                         | C     | ·    | Initialize a new CLAUDE.md                                 |

### GSD (Get-Shit-Done) family — decimal phases, UAT, milestones
Activate only when the user is clearly inside a GSD workflow (you'll see a `.planning/` directory, a phase number, or explicit GSD vocabulary). Map 1:1 to the slash command:
`gsd:do`, `gsd:next`, `gsd:progress`, `gsd:plan-phase`, `gsd:execute-phase`, `gsd:verify-work`, `gsd:add-tests`, `gsd:debug`, `gsd:ship`, `gsd:review`, `gsd:audit-uat`, `gsd:add-backlog`, `gsd:new-milestone`, `gsd:complete-milestone`, `gsd:cleanup`, `gsd:health`, etc.

> Rule: never pre-emptively open a GSD command outside a GSD project.

---

## Matching heuristics — fast patterns

The table above is authoritative. This list is a quick regex-ish cheatsheet for the first pass:

- `\bcommit\b|\bcommita\b|git add` → `git-commit`
- `\bpr\b|pull request|merge request` → `git-pr-create`
- `\breview(ing)?\b|audit diff` → `git-review` or `security-review`
- `\bbranch\b|checkout|switch` → `git-branch`
- `changelog|release notes` → `git-changelog`
- `design|redesign|landing|hero|figma` → `frontend-design` or `ui-ux-pro-max`
- `accessibility|a11y|wcag|contrast|keyboard nav` → `ui-ux-pro-max`
- `polish|micro(-| )interaction|spacing` → `ui-polisher`
- `react native|expo|android|ios\b` → `react-native` + possibly `vercel-react-native-skills`
- `mcp server|fastmcp|mcp tool` → `mcp-builder` / `create-mcp`
- `new skill|create a skill|skill md` → `skill-creator`
- `prompt cach(e|ing)|anthropic sdk|claude api` → `claude-api`
- `e2e|playwright|cypress` → `webapp-testing`
- `unit test|tdd|vitest|jest|bun test` → `testing` / `backend-testing`
- `\bapi-test-loop\b|validate api|test backend api|curl api` → `api-test-loop`
- `\bpostman-generator\b|postman|newman|collection|env|validate postman|valide` → `postman-generator`
- `bug|error|stack trace|regression` → `auto-fix` first, escalate to `systematic-debugging`
- `pod install.*error|NitroModules|Unable to find a specification|BUILD FAILED|update rules|update docs` → `error-fix-loop`
- `deploy|docker|k8s|pipeline|ci/cd` → `devops`
- `landing copy|headline|cta|pitch` → `copywriting`
- `linkedin|tweet|instagram|post` → `social-content`
- `xlsx|excel|spreadsheet` → `xlsx`
- `settings\.json|hook|permission|keybind` → `update-config` / `keybindings-help`
- `loop|every \d+ (min|hour)|cron` → `loop` / `schedule`
- `\bgsd\b|\.planning|phase \d+\.\d+` → GSD family
- `architecture|how does .* relate|understand the codebase` + `graphify-out/` exists → `graphify` (query mode)

Multiple matches? Apply step 3 (rank & prune) before emitting.

---

## Examples

**Trivial Q&A**
User: "what's the file that sets our default theme?"
→ `SKILLS: []` — answer inline with a grep. No skill earns its keep here.

**Clear single-skill match**
User: "open a PR with the staged changes"
→ `SKILLS: [git-pr-create]` | INTENT: git-op | REASON: direct PR request | BUDGET: low | NEXT: run git status + git diff.

**Conflict, pick narrower**
User: "create the commit"
→ `SKILLS: [git-commit]` (not `git-master`) | INTENT: git-op | REASON: narrow beats broad | BUDGET: low.

**Design: light vs heavy**
User: "adjust header spacing" → `SKILLS: [ui-polisher]`.
User: "redesign the landing with a bolder identity" → `SKILLS: [frontend-design]` (or `ui-ux-pro-max` if a system-level sweep is asked).

**Planning + build — do NOT chain**
User: "plan and implement watchlist feature X"
→ First turn: `SKILLS: [smart-dispatch]` | REASON: multi-model plan. Let it emit the dispatch table, then the user confirms before building.

**Bug report**
User: "breaking with TS2322 in agent.ts:210"
→ `SKILLS: [auto-fix]` — pattern-matched, cheap. If 2 fix attempts fail, escalate to `systematic-debugging`.

**New skill**
User: "create a skill to review SQL"
→ `SKILLS: [skills-selector, skill-creator]`? **No** — skills-selector is already running. Emit `SKILLS: [skill-creator]`.

---

## Rules & guardrails

1. **Self-recursion is forbidden.** Never put `skills-selector` in the `SKILLS:` list. You are the chooser, not the choice.
2. **No silent escalation.** If you picked a heavy skill, your `REASON` must name the signal that justified it.
3. **Announce before you invoke.** Always emit the block. Never call a skill without emitting the plan first — the block is the audit trail.
4. **Respect user overrides.** If the user explicitly names a skill ("use ui-ux-pro-max for this"), pass it through — your job is scoping, not vetoing.
5. **Language stays with the user.** Keep the selection block in the user's language if non-English (US English/pt-BR OK). Identifiers (skill names, `SKILLS:` key) stay in English.
6. **Portability.** If the selected skill doesn't exist on the current platform, downgrade to the closest match on the same row of the catalog; note the substitution in `REASON`.
7. **Stop at selection.** After the block, hand off. Do not continue executing the selected skill's body — invoke it via the platform's Skill mechanism.
8. **If nothing fits, emit `[]`.** No-skill is a valid, often correct, answer. The default is to do the work inline with the base tools.

---

## Output template (copy exactly)

```
SKILLS: [<csv or empty>]
INTENT: <intent-label>
REASON: <≤15 words>
BUDGET: <low|medium|high>
MAP:    <consumed | none>
NEXT:   <first concrete action>
```

That block — or silence plus inline work — is the entire surface of this skill. Depth belongs to the skills you dispatch, not here.
