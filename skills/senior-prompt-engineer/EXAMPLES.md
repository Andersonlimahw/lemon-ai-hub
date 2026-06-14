# Senior Prompt Engineer — Examples

Full before/after transformations. Study the *shape*, not the specific domain.

---

## Example 1 — idea.md → prompt.md (repo context FOUND)

**Invocation**
```
/senior-prompt-engineer Leia ./idea.md e reescreva em ./prompt.md de forma profissional
```

**Input `idea.md` (weak)**
```
preciso adicionar dark mode no app. usar o tema do tailwind. salvar a preferencia
```

**Step-2 probe found**: Next.js + Tailwind, `package.json` has `test`, `lint`; `AGENTS.md` defines conventions.

**Output `prompt.md` (definitive)**
```md
# Role / Context
You are a senior frontend engineer working in a Next.js 14 + Tailwind app
(App Router). Follow conventions in AGENTS.md. Theme tokens live in
tailwind.config.ts.

# Task
Add a user-toggleable dark mode that persists across reloads.

# Inputs
- tailwind.config.ts — theme tokens
- app/layout.tsx — root layout (theme provider mounts here)
- components/ — existing UI primitives

# Constraints
- Scope: theme system + a toggle component only. Do NOT restyle existing
  pages beyond wiring `dark:` variants where already implied.
- Use Tailwind `darkMode: 'class'`. No new CSS-in-JS, no extra theming lib.
- Match existing component patterns and naming.

# Plan
1. Enable `darkMode: 'class'` in tailwind.config.ts → verify: `lint` passes.
2. Add ThemeProvider reading/writing `localStorage('theme')`, default = system
   (prefers-color-scheme) → verify: reload keeps choice.
3. Build <ThemeToggle/> using existing button primitive → verify: toggles
   `class="dark"` on <html>.
4. Wire provider + toggle into app/layout.tsx → verify: no hydration warning.

# Output contract
- Deliverable: working dark mode + toggle, persisted.
- Definition of done: `test` + `lint` green; manual reload keeps theme; no
  hydration mismatch in console.

# Feedback — DO
- Read AGENTS.md first and mirror its conventions.
- Default to the system preference on first visit.
- Guard localStorage access for SSR (no `window` on server).

# Feedback — DO NOT
- Do NOT add a state-management library for one boolean.
- Do NOT touch unrelated components or "improve" their styling.
- Do NOT flash light-then-dark on load (set class before paint).
- Do NOT introduce a second source of truth for the theme.

# Execution Map
Agents: inline (single linear task).
Skills: skills-selector → smart-dispatch → git-commit.
Models: Sonnet (claude-sonnet-4-6) — standard frontend implementation, no
deep architectural ambiguity.
Effort: low | Time: ~15–25 min | Tokens: ~10k–20k | MCP/Tools: none.
```

**Changelog appended**
```
- Vague "salvar preferencia" → concrete localStorage + SSR guard + system default.
- Added verifiable DoD (test/lint/no-hydration) replacing "usar o tema".
- Added DO-NOT block killing the 3 classic dark-mode bugs (flash, extra lib, scope creep).
- Mapped model = Sonnet with rationale.
```

---

## Example 2 — inline idea (repo context ABSENT)

**Invocation**
```
/senior-prompt-engineer quero um prompt pra criar um script que organiza minhas fotos
```

**Step-2 probe**: not in a repo / no manifests. **Autocomplete withheld.**

**Correct response (ask, don't fabricate)**
```
Sem contexto de repo pra autocompletar boilerplate. Pra montar o prompt definitivo preciso de:
1. Linguagem/runtime (Python? Node? shell?)
2. Critério de organização (por data EXIF? por pasta? por evento?)
3. Origem e destino (pastas), e se pode mover ou só copiar
4. Critério de pronto (ex.: "roda em 1k fotos sem erro, idempotente")

Me passa esses 4 e eu devolvo o prompt completo.
```
Then, once answered, generate the full skeleton. Never guess the stack.

---

## Example 3 — hardening an existing prompt (fan-out task)

**Input (mediocre prompt)**
```
Refatora todo o módulo de pagamentos pra ficar mais limpo e adiciona testes
```

**Key fixes the skill applies**
- Splits the mega-verb into scoped steps with verify checks.
- Adds DO-NOT: "no behavior changes", "no public API rename without note".
- Flags it as genuinely fan-out → recommends an agent + Opus for the plan phase.

**Execution Map produced**
```
Agents: Plan agent (or gsd:plan-phase) to map the refactor BEFORE editing;
then general-purpose agent per submodule if it parallelizes.
Skills: skills-selector → smart-dispatch → (testing) → git-commit.
Models: Opus (claude-opus-4-8) for the refactor plan & risk analysis;
Sonnet (claude-sonnet-4-6) for the mechanical edits + test writing.
Effort: high | Time: ~60–120 min | Tokens: ~50k–90k (fan-out adds ~30%).
MCP/Tools: none. TBD — confirm there's a payments test suite to extend.
```

---

## Example 4 — no path → input IS the chat (inline output)

**Invocation** (no file, no output path)
```
/senior-prompt-engineer
```
**Input**: the skill reads the current conversation / last user request as the prompt to harden.
**Behavior**:
- If the last request is trivial/clear → triviality gate fires: `Prompt já claro; pulando refino → skills-selector`. No refino.
- Else → refine in place, return the definitive prompt + Execution Map **inline** (single fenced block), no file written. Then the routers (skills-selector → smart-dispatch) pick skills/models using the sharpened prompt.

**Execution Map (inline)**
```
Agents: inline. Skills: skills-selector → smart-dispatch.
Models: Opus for ambiguity resolution, Sonnet for impl.
Effort: medium | Time: ~20–40 min | Tokens: ~15k–35k | MCP/Tools: TBD.
```

---

## What a good output always has
1. All applicable skeleton blocks, in order.
2. A **task-specific** DO-NOT block (the differentiator).
3. Verify checks on every step.
4. An honest Execution Map (agents / skills / models, with `TBD` where unknown).
5. A short changelog teaching the user what improved.
