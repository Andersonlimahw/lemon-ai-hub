---
name: senior-prompt-engineer
description: Pipeline stage-0 prompt refiner. Runs FIRST — before skills-selector and smart-dispatch — turning a raw idea, pasted draft, or the current chat into a definitive, production-grade prompt (Anthropic prompt-engineering best practices), then hands the refined prompt + an Execution Map (agents, skills, models, effort, time & token estimate) to the routers so they pick the best skills/models with sharpened context. When no file path is given, the input IS the chat/pasted text and the output is returned inline (processed naturally), not forced to a file. Use when the user invokes /senior-prompt-engineer, says "refine my prompt", "improve this prompt", "turn this idea into a prompt", "rewrite idea.md to prompt.md", "definitive prompt", "professional prompt", or pastes a draft prompt/idea to be hardened. Cross-CLI: Claude, Codex, Gemini, OpenCode, Antigravity (agy), lemon-code (lemon).
---

# Senior Prompt Engineer

Turn a rough idea or weak prompt into a **definitive prompt** a coding agent can execute without re-clarifying. Channel Karpathy (state assumptions, simplest thing that works, verifiable goals) + Anthropic's prompt-library structure.

**Prime directive:** the output is a *better prompt* + an Execution Map — NOT the execution of the task. Produce the artifact; the downstream routers (skills-selector → smart-dispatch) run the task.

## Pipeline position — runs FIRST

This skill is **stage 0**, ahead of the routers. Order:

```
senior-prompt-engineer (refine prompt + build Execution Map)
        ↓ feeds sharpened prompt + context
skills-selector  (pick which skills activate, now with a clear prompt)
        ↓
smart-dispatch   (pick agent/model/provider, now with effort+estimates)
        ↓
execution
```

Refining first means the routers decide on a *clarified* request instead of a vague one — better skill/model picks, fewer wasted turns.

### Triviality gate (protect the harness)
Do **not** refine trivial, already-clear, one-line requests (e.g. "run the tests", "fix this typo", "what does X do?"). Auto-refinement on every turn adds latency and tokens for no gain. Engage only when:
- the user explicitly invokes the skill, OR
- the request is ambiguous, multi-step, underspecified, or high-stakes.
Otherwise emit one line — `Prompt already clear; skipping refinement → skills-selector` — and pass through. This gate is mandatory.

## Inputs you accept

- **No path given → the input IS the current chat / pasted text.** Refine that. Default output is **inline, processed naturally** (do not force a file).
- A pasted draft prompt or idea (inline text) — refine it.
- A file path to read (e.g. `idea.md`, `spec.txt`) — read it.
- An optional output path (e.g. `prompt.md`) — only then Write the refined prompt there.

Example invocations:
```
/senior-prompt-engineer Leia ./idea.md e reescreva em ./prompt.md de forma profissional
/senior-prompt-engineer            # no args → refine the current conversation/last request, reply inline
```

## Protocol — 6 steps

### 1. Ingest & classify
Read the input (file, inline, or current chat). In one line, classify the **task intent** (build-code, refactor, design-ui, fix-bug, research, content, data, ops…) and the **target executor** (this CLI's agent, an API call, another LLM CLI). This drives every later choice.

### 2. Detect repo context (gates autocomplete) — cheap + rtk
Probe lightly; never flood context. Prefer `rtk` (token-killer) over raw shell:
```bash
rtk git status && rtk ls . && rtk read AGENTS.md   # or CLAUDE.md / README.md / package.json — one at a time, only if present
```
- **`graphify-out/` present**: prefer the `graphify` knowledge graph over raw probing — query it for architecture/file relationships (god nodes, communities) and cite findings in the prompt context. Far cheaper than exploring files.
- **Context found** (framework, scripts, conventions): you MAY suggest a boilerplate scaffold pre-filled with real paths/scripts/stack. See [REFERENCE.md](REFERENCE.md#boilerplate-autocomplete).
- **No usable context**: DO NOT invent a scaffold. Ask the user for the missing facts (stack, target files, success criteria). Fabricating context is the cardinal sin of this skill.
Keep the probe minimal — do not `cat` large files into context.

### 3. Extract requirements & surface gaps (Karpathy gate)
List explicitly: **Assumptions** (ask if a load-bearing one is uncertain), **Ambiguities** (name them, don't silently pick), **Success criteria** (vague verbs → verifiable checks). If a critical gap blocks a good prompt, ask 1–3 sharp questions before generating (Claude: AskUserQuestion; other CLIs: plain questions).

### 4. Generate the definitive prompt
Assemble using the canonical block order in [REFERENCE.md](REFERENCE.md#prompt-skeleton): 1. Role/Context 2. Task 3. Inputs/files 4. Constraints (surgical-edit rule) 5. Plan (numbered, each with `→ verify:`) 6. Output contract 7. Examples (multishot, only when it disambiguates) 8. Feedback — DO 9. Feedback — DO NOT (highest-leverage; most failures come from unspoken don'ts).

### 5. Emit the EXEC-MAP contract (the routers CONSUME this — don't make them re-classify)
Append a machine-readable **`EXEC-MAP v1`** fenced block. This is a **contract**: `skills-selector` reads `intent` + `skills` and only validates/prunes; `smart-dispatch` reads `effort` + `models` and only routes/escalates. Classifying intent here once is what kills the 3× re-classification overlap.

```
EXEC-MAP v1
intent:   <build-code | refactor | design-ui | fix-bug | research | content | data | ops | docs | git-op | debug | test | trivial-or-chat>
executor: <claude | codex | gemini | opencode | lemon | api>
effort:   <trivial | low | medium | high>
time:     <rough range, e.g. ~5–10 min>
tokens:   <rough range, e.g. ~8k–15k>
skills:   [<candidate skills in order, executor-aware; [] if inline>]
models:   {plan: <opus|tier>, impl: <sonnet|tier>, mechanical: <haiku|tier>}
agents:   <inline | [named subagents only if the task truly fans out]>
mcp:      [<tools needed, or empty>]
notes:    <one line; mark unknowns "TBD — needs user input">
```

Rules for the block:
- **Executor-aware**: only name skills/agents/models that exist on the target CLI; map to the closest tier and note substitutions in `notes`. Non-Claude → map opus/sonnet/haiku to that CLI's quality/balanced/budget tier.
- **Honest over confident**: `TBD` beats a wrong guess. Never fabricate a model/agent/skill.
- `effort`, `time`, `tokens` are **mandatory**. Estimation method + catalogs in [REFERENCE.md](REFERENCE.md#execution-map).
- Keep a 1–2 line human-readable gloss above the block for the user; the block itself is the contract the routers parse.

### 6. Deliver
- **No output path** (default): return the refined prompt inline in one fenced block + the Execution Map, ready to copy or to feed the routers.
- **Output path given**: Write the refined prompt there (native Write, full file). Confirm path + one-line summary.
- Always end with a 2–4 line **changelog** of the biggest improvements (weak → fixed), so the user learns.

## Hard rules

- Output a prompt + Execution Map, never execute the underlying task.
- Triviality gate first: skip refino on trivial/clear requests.
- No invented repo context. No-context → ask, don't hallucinate. Non-negotiable.
- The **DO NOT** section is mandatory and task-specific, not generic filler.
- EXEC-MAP must be honest: `TBD` beats a confident wrong guess. Executor-aware (don't name skills the target CLI lacks).
- Effort + time + token estimate are mandatory in the EXEC-MAP block.
- The EXEC-MAP is a **contract**: emit it once, in the canonical `EXEC-MAP v1` shape, so skills-selector and smart-dispatch consume it instead of re-classifying intent.
- Preserve the user's intent and domain language; sharpen, don't hijack.
- Match the user's language (pt-BR stays pt-BR); keep identifiers/skill names in English.
- Use `rtk` for any CLI command rtk supports (git/ls/read/grep/build/test…). User-facing summary in caveman; the prompt artifact stays normal prose.

## Files
- [REFERENCE.md](REFERENCE.md) — prompt skeleton, Anthropic techniques, model routing, agent/skill catalog, estimation, boilerplate autocomplete, per-CLI notes.
- [EXAMPLES.md](EXAMPLES.md) — full before/after transformations (idea.md → prompt.md, chat-as-input).
