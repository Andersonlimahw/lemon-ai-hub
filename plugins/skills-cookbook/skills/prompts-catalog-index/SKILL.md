---
name: prompts-catalog-index
description: Complete A-to-Z index of every plugin in the hub with a one-line when-to-use hint, grouped by area. Use to locate the right skill fast when no cookbook track matches, or to browse the full catalog without reading raw descriptions.
---

# Complete catalog index (159 plugins)

One line per plugin: **when to use it**. Grouped by area; tracks with a full recipe are linked from the [root SKILL.md](../../SKILL.md). Hub-wide rule: `X` × `X-advisor/-watch/-runner/-guardian/-detector` pairs = one-shot × continuous/CI — pick by objective.

## Understand & learn

| Plugin | When to use |
|---|---|
| `architecture-deepener` | shallow/confusing codebase: module map + opportunities to deepen design |
| `llm-wiki-curator` | generate a navigable code wiki for onboarding |
| `teaching` | learning plan with milestones and checkpoints |
| `teaching-workspace` | structured study environment to practice |
| `learning-output-style` | responses in a didactic format |
| `doc-driven-grilling` | grill a plan/spec and generate ADRs/glossary before coding |
| `task-interrogator` | grill a plan and turn it into tasks with acceptance criteria |
| `session-handoff` | end of a long session: handoff so the next one starts without re-exploring |
| `continual-learning` | persist lessons across sessions |
| `bug-diagnostics` | understand broken behavior: repro → hypotheses → fix |
| `code-smell` | one-shot code-smell analysis |
| `code-smell-detector` | continuous code-smell enforcement in CI |

## Loops & QA

| Plugin | When to use |
|---|---|
| `api-test-loop` | API validation loop via CURL with findings.md |
| `chrome-qa-loop` | exploratory QA of a live web app, one report per finding |
| `computer-use-swiftui-loop` | visual loop for macOS/SwiftUI apps (Computer Use, Codex app) |
| `error-fixer-loop` | build/test failure: investigate → fix → anti-regression rule |
| `karpathy-loop` | autonomous cycles to optimize a metric |
| `webapp-testing` | one-shot Playwright toolkit: screenshots, logs, interaction |
| `playwright` | scripted E2E |
| `playwright-interactive` | interactive/assisted browser session |
| `verification-before-completion` | "is this actually done?" gate before declaring complete |
| `agentic-value-loops` | recurring value loops: feature, docs, maintenance/security, AI tuning |

## Karpathy method

| Plugin | When to use |
|---|---|
| `karpathy-guidelines` | behavioral principles on any non-trivial code |
| `karpathy-recipe` | staged recipe for medium/large work |

## Engineering & security

| Plugin | When to use |
|---|---|
| `code-review-expert` | structured review of a diff/PR |
| `pr-review-canvas` | render review findings as inline comments |
| `commit-quality` | semantic commit hygiene |
| `async-patterns` | audit races, N+1 async, unbounded parallelism |
| `async-advisor` | CI/PR gate for async patterns |
| `bundle-analyzer` | investigate a heavy bundle now |
| `bundle-watch` | CI gate for bundle size |
| `db-advisor` | continuous query monitoring: N+1 detection, repeated-query tracking |
| `db-index-advisor` | index for a specific slow query |
| `load-test` | design a load test/SLO |
| `load-test-runner` | run/schedule recurring load tests |
| `chaos-test` | design failure experiments |
| `chaos-runner` | orchestrate/schedule chaos with a resilience score |
| `security-best-practices` | secure-coding practice checklist |
| `security-guidance` | contextual security guidance |
| `security-ownership-map` | map owners per security area |
| `security-threat-model` | STRIDE for a new feature |
| `i18n-audit` | find missing/orphaned/hardcoded keys |
| `i18n-sync` | sync structure across locales |
| `feature-flag` | implement/use a one-shot flag |
| `feature-flags` | ongoing flag management |
| `feature-purge` | remove an entire feature with no dead code left |
| `finishing-a-development-branch` | close a branch with quality before merge |
| `git-expert` | semantic commits, bisect, git workflow |
| `gh-expert` | PRs, issues, and automation via the gh CLI |
| `incident-center` | incident logging and postmortem |
| `incident-runbook` | guided response during an incident |

## APIs & CLIs

| Plugin | When to use |
|---|---|
| `openapi-generate` | generate an OpenAPI spec from code (one-shot) |
| `openapi-hub` | ongoing management of multiple specs |
| `postman-generator` | Postman collection from a spec/routes |
| `cli-creator` | composable CLI from an API (Codex-focused) |
| `cli-generator` | full Bun CLI generated from a SPEC |
| `cli-for-agent` | rubric for a CLI operable by agents |
| `cli-wrapper` | wrap an external CLI with a digest and token savings |
| `agent-sdk-dev` | build agents on the Claude Agent SDK |

## Frontend & design

| Plugin | When to use |
|---|---|
| `frontend-design` | intentional visual direction for new UI |
| `design` | brand asset production: logos, CIP, banners, icons |
| `design-taste-frontend` | good-taste baseline when no aesthetic is chosen yet |
| `ui-ux-pro-max` | data base: styles, palettes, fonts, per-stack guidelines |
| `web-design-guidelines` | web guidelines checklist |
| `a11y-audit` | one-shot WCAG audit |
| `a11y-guardian` | continuous a11y gate in PR/CI |
| `minimalist-ui` | minimalist aesthetic (exclusive) |
| `industrial-brutalist-ui` | brutalist aesthetic (exclusive) |
| `high-end-visual-design` | premium aesthetic (exclusive) |
| `emil-design-eng` | design-engineer aesthetic (exclusive) |
| `image-to-code` | screenshot/mockup → component |
| `redesign-existing-projects` | new look preserving content/flow |
| `imagegen-frontend-web` | generate web visual reference |
| `imagegen-frontend-mobile` | generate mobile visual reference |
| `scroll-world` | scrollytelling experience |

## Vercel & React

| Plugin | When to use |
|---|---|
| `vercel-react-best-practices` | React/Next patterns: components, fetching, rendering |
| `vercel-optimize` | Core Web Vitals, caching, images/fonts |
| `vercel-composition-patterns` | kill prop-drilling/god components via composition |
| `vercel-react-view-transitions` | page/element transitions |
| `vercel-react-native-skills` | RN/Expo performance: lists, animations, native |
| `vercel-cli-with-tokens` | token-authenticated Vercel CLI (non-interactive) |
| `deploy-to-vercel` | publish preview/production |

## Mobile & release

| Plugin | When to use |
|---|---|
| `apple-store-release-agent` | auditable go/no-go for an iOS release |
| `google-play-release-agent` | auditable go/no-go for an Android release |
| `app-store-connect-api` | App Store Connect automation: TestFlight, IAP, reports |
| `google-play-developer-api` | Play Console automation: tracks, rollout |
| `aso` | optimize store listings |

## Data & backend

| Plugin | When to use |
|---|---|
| `supabase` | operate Supabase: schema, RLS, functions |
| `supabase-postgres-best-practices` | correct Postgres modeling and indexes |
| `firebase-expert` | Firestore/Auth/Functions/Hosting |

## Knowledge & Notion

| Plugin | When to use |
|---|---|
| `notion-knowledge-capture` | chat decisions → traceable Notion pages |
| `notion-meeting-intelligence` | meeting notes → owned actions |
| `notion-research-documentation` | research with an auditable source trail |
| `notion-spec-to-implementation` | Notion spec → implementation plan |

## Product & growth

| Plugin | When to use |
|---|---|
| `product-marketing` | positioning and key messages |
| `pricing` | tiers, anchors, and pricing strategy |
| `paywalls` | in-app paywall at value moments |
| `offers` | bonuses, guarantee, value framing |
| `onboarding` | from signup to aha-moment |
| `signup` | a signup flow that converts |
| `launch` | launch timeline and execution |
| `churn-prevention` | cancel flow, save offers, dunning, win-back |
| `analytics` | tracking plan, GA4, events, attribution |
| `free-tools` | a free tool as an acquisition engine |
| `lead-magnets` | lead-capture magnets |
| `referrals` | referral program |
| `popups` | conversion popups without annoying users |
| `revops` | revenue operations: funnel, CRM, handoffs |
| `prospecting` | outbound prospecting |
| `sales-enablement` | material and talking points for sales |

## Marketing & content

| Plugin | When to use |
|---|---|
| `copywriting` | write persuasive copy from scratch |
| `copy-editing` | edit/sharpen existing copy |
| `writing-guidelines` | clear-writing standard |
| `marketing-psychology` | biases and behavior applied ethically |
| `marketing-plan` | full marketing plan |
| `marketing-ideas` | generate new ideas/angles |
| `marketing-council` | panel of marketing perspectives |
| `marketing-loops` | recurring/scheduled marketing workflows (cadence or trigger) |
| `content-strategy` | content strategy and calendar |
| `emails` | email sequences and campaigns |
| `sms` | SMS campaigns |
| `social` | per-network distribution and formats |
| `ads` | paid media: campaign, targeting, optimization |
| `brand` | voice, identity, and brand consistency |
| `brandkit` | premium brand-guidelines boards |
| `seo-audit` | technical + on-page SEO audit |
| `ai-seo` | get cited by LLMs: AEO/GEO, llms.txt |
| `programmatic-seo` | SEO pages at programmatic scale |
| `schema` | structured data (JSON-LD) |
| `site-architecture` | site architecture for SEO/navigation |
| `competitors` | broad competitive analysis |
| `competitor-profiling` | deep profile of one competitor |
| `co-marketing` | marketing partnerships |
| `community-marketing` | grow via community |
| `influencer-marketing` | creator campaigns |
| `public-relations` | PR and press |
| `video` | video script and strategy |
| `image` | one-off image generation/editing |
| `imagegen` | general-purpose image generation (see the frontend variants) |

## Meta-harness & tokens

| Plugin | When to use |
|---|---|
| `senior-prompt-engineer` | refine a request into a definitive prompt + EXEC-MAP (stage-0) |
| `skills-selector` | decide which skills to activate (stage-1) |
| `smart-dispatch` | route agent/model/cost (stage-2) |
| `skill-creator` | guided creation of a new skill |
| `skill-authoring` | best practices for writing a skill |
| `skill-installer` | install external skills |
| `create-plugin` | plugin generator (pick ONE generator) |
| `plugin-creator` | plugin generator (pick ONE generator) |
| `plugin-generator` | plugin generator (pick ONE generator) |
| `hookify` | "whenever X, do Y" automations via hooks |
| `orchestrate` | multi-agent fan-out with a final integration pass |
| `subagent-driven-development` | subagent-driven development |
| `ai-workspace-orchestrator` | build an agent workspace with contract + review |
| `opencode-subagent` | delegate to OpenCode |
| `migrate-to-codex` | port skills/flows to Codex |
| `caveman` | response compression (lite/full/ultra) |
| `token-saver` | cut the biggest context consumers |
| `skills-cookbook` | this cookbook: recipes, combos, and anti-patterns |

## Fun & experiments

| Plugin | When to use |
|---|---|
| `hatch-pet` | generate/repair a pet spritesheet (Codex) from art/image |
| `spotify-squad` | squad + Spotify experience |
