# Skills Cookbook

Ready-to-paste example prompts that teach efficient use of the lemon-ai-hub skills. Five tracks, each a sub-skill with 4–5 recipes (prompt template + placeholders + verifiable success criterion), plus combination rules and an anti-pattern matrix of mutually exclusive or redundant skills.

Prompt templates are written in pt-BR (the author's working language); skill names and identifiers are always exact English. Adapt the prose to any language — skills trigger on intent.

## Tracks

| Track | Sub-skill | Focus |
|---|---|---|
| Project understanding | `prompts-project-understanding` | cut cognitive load: architecture X-ray, project wiki, guided learning, spec grilling |
| Feedback loops | `prompts-feedback-loops` | API test loops, exploratory browser QA, error-fix loops, metric optimization |
| Product | `prompts-product` | positioning, monetization funnel, onboarding, launch, user-feedback instrumentation |
| Marketing | `prompts-marketing` | copy + psychology, SEO + AI search, email sequences, social distribution |
| Design & Frontend | `prompts-design-frontend` | visual direction, single-aesthetic rule, screenshot-to-code, redesign, a11y |

## Core rules (from the root skill)

1. Combine different layers, never the same layer twice.
2. Max ~3 skills per prompt.
3. One aesthetic at a time (`minimalist-ui` × `industrial-brutalist-ui` × `high-end-visual-design` × `emil-design-eng` are mutually exclusive).
4. One loop driver at a time — chain loops sequentially, never in parallel on the same target.
5. Name skills exactly; end every prompt with a verifiable success criterion.

## Usage

Open the root [SKILL.md](SKILL.md) for the full combination rules and anti-pattern matrix, pick a track, copy a recipe, fill the `<placeholders>`, paste. On non-trivial requests the hub pipeline (`senior-prompt-engineer` → `skills-selector` → `smart-dispatch`) runs on top.
