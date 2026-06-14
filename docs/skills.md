---
title: Available AI Skills
status: active
updated: 2026-06-14
related: [docs/index.md, docs/token-saving.md]
---

# Available AI Skills

Custom skills modify agent reasoning patterns and extend their toolboxes. Below is a detailed review of all skills included in the AI Marketplace.

## 🧠 Core Agent Pipeline (Stage 0 → 1 → 2)

These three skills are designed to work together sequentially to classify, select, and route incoming requests with optimal token efficiency.

```
User Input 
   ↓
[Stage-0: senior-prompt-engineer] 
   • Classifies intent, detects context, refines prompt.
   • Emits Execution Map (EXEC-MAP v1).
   ↓
[Stage-1: skills-selector]
   • Dynamic gatekeeper. Loads required skills on-demand.
   ↓
[Stage-2: smart-dispatch]
   • Model/Agent router. Selects the cheapest capable tier.
   ↓
Execution
```

### 1. `senior-prompt-engineer`
- **Location**: [skills/senior-prompt-engineer/SKILL.md](./skills/senior-prompt-engineer/SKILL.md)
- **Role**: Prompts refiner & architect.
- **Function**: Takes a raw, ambiguous task and hardens it into a definitive prompt using Anthropic's prompt engineering rules.
- **Contract**: Generates an `EXEC-MAP v1` block mapping execution details (expected intent, effort, target executor, candidate models/skills).
- **Triviality Gate**: Automatically skips refinement on simple queries (like "run tests") to save time and tokens.

### 2. `skills-selector`
- **Location**: [skills/skills-selector/SKILL.md](./skills/skills-selector/SKILL.md)
- **Role**: Dynamic gatekeeper.
- **Function**: Rather than loading all available skills (which overwhelms the LLM context window), it intercepts requests and loads the minimal set of skills on-demand.
- **Rule**: Limits loaded skills to a maximum of 2 per conversation turn to optimize input tokens.

### 3. `smart-dispatch`
- **Location**: [skills/smart-dispatch/SKILL.md](./skills/smart-dispatch/SKILL.md)
- **Role**: Intelligent router.
- **Function**: Maps tasks to the appropriate model class based on complexity:
  - **Budget (e.g., Gemini Flash, Claude Haiku)**: Mechanical edits, documentation, linting, formatting.
  - **Balanced (e.g., Claude Sonnet, Gemini Pro)**: Bulk coding, feature implementation.
  - **Quality (e.g., Claude Opus, Gemini Pro max thinking)**: Long-horizon planning, complex architecture designs, security reviews.
- **Auto-Escalation**: If a cheaper model fails to resolve validation issues twice, it automatically escalates the request to a higher-tier model.

---

## 🛠️ Specialty Skills

### 4. `karpathy-recipe`
- **Location**: [skills/karpathy-recipe/SKILL.md](./skills/karpathy-recipe/SKILL.md)
- **Concept**: Adapted from Andrej Karpathy's *"A Recipe for Training Neural Networks"*.
- **Function**: Enforces a paranoid, step-by-step product building flow:
  1. Learn from real domain data.
  2. Setup an end-to-end skeleton with fixed mock responses first.
  3. Overfit a single real case.
  4. Add one feature "knob" at a time, running validation tests after each commit.

### 5. `llm-wiki-curator`
- **Location**: [skills/llm-wiki-curator/SKILL.md](./skills/llm-wiki-curator/SKILL.md)
- **Concept**: Keeps project documentation LLM-friendly.
- **Function**: Automatically compiles the `docs/llms.txt` index block conforming to llmstxt.org guidelines. Audits for broken markdown links, orphan documents, and missing metadata front-matter.

### 6. `token-saver`
- **Location**: [skills/token-saver/SKILL.md](./skills/token-saver/SKILL.md)
- **Concept**: Facilitates setup of token saving tools.
- **Function**: Launches an interactive CLI wizard to configure RTK, Caveman Mode, Graphify, and Context-Mode across projects.
