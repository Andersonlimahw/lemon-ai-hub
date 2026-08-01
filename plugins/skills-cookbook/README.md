# Skills Cookbook

Ready-to-paste example prompts that teach efficient use of the lemon-ai-hub skills. Thirteen recipe tracks, each a sub-skill with recipes (prompt template + placeholders + verifiable success criterion), plus combination rules, an anti-pattern matrix of mutually exclusive or redundant skills, and a complete A–Z index sub-skill covering all 159 plugins in the hub.

## Tracks

| Track | Sub-skill | Focus |
|---|---|---|
| Project understanding | `prompts-project-understanding` | cut cognitive load: architecture X-ray, project wiki, guided learning, spec grilling |
| Feedback loops | `prompts-feedback-loops` | API test loops, exploratory browser QA, error-fix loops, metric optimization |
| Product | `prompts-product` | positioning, monetization funnel, onboarding, launch, user-feedback instrumentation |
| Marketing | `prompts-marketing` | copy + psychology, SEO + AI search, email sequences, social distribution |
| Design & Frontend | `prompts-design-frontend` | visual direction, single-aesthetic rule, screenshot-to-code, redesign, a11y |
| Karpathy method | `prompts-karpathy` | guidelines, recipe for large work, principle-based review, metric loop |
| Vercel & React | `prompts-vercel-react` | best practices, optimization, composition, view transitions, RN/Expo, deploy |
| Engineering quality | `prompts-engineering-quality` | PR review, async, database, threat model, load/chaos, i18n |
| APIs & CLIs | `prompts-apis-clis` | OpenAPI, Postman, agent-friendly CLIs, CLI wrapping |
| Mobile & Release | `prompts-mobile-release` | iOS/Android go/no-go, App Store Connect, Play API, ASO |
| Data & Backend | `prompts-data-backend` | Supabase/Postgres, Firebase, database decisions, incidents |
| Knowledge & Notion | `prompts-knowledge-notion` | decision capture, meetings, research docs, spec-to-code, persistent learning |
| Meta-harness | `prompts-meta-harness` | authoring skills/plugins, hooks, multi-agent orchestration, migration, tokens |
| A–Z index | `prompts-catalog-index` | every plugin in the hub with a one-line when-to-use hint |

## Core rules (from the root skill)

1. Combine different layers, never the same layer twice.
2. Max ~3 skills per prompt.
3. One aesthetic at a time (`minimalist-ui` × `industrial-brutalist-ui` × `high-end-visual-design` × `emil-design-eng` are mutually exclusive).
4. One loop driver at a time — chain loops sequentially, never in parallel on the same target.
5. Name skills exactly; end every prompt with a verifiable success criterion.

## Usage

Open the root [SKILL.md](SKILL.md) for the full combination rules and anti-pattern matrix, pick a track, copy a recipe, fill the `<placeholders>`, paste. On non-trivial requests the hub pipeline (`senior-prompt-engineer` → `skills-selector` → `smart-dispatch`) runs on top.
