---
name: prompts-design-frontend
description: Ready-to-paste prompts for UI and frontend design — intentional visual direction, design-system data, accessibility gates, screenshot-to-code, and redesigns. One aesthetic at a time.
---

# Prompts — Design & Frontend

Receitas para UI com intenção. Regra inegociável da trilha: **uma estética por vez** — `minimalist-ui`, `industrial-brutalist-ui`, `high-end-visual-design` e `emil-design-eng` são direções autoexcludentes; misturar duas produz UI genérica ou incoerente.

## R1 — Tela nova com direção + dados + compliance

**Skills:** `frontend-design` + `ui-ux-pro-max` + `a11y-audit`
**Quando:** construir UI nova que não pareça template.

```text
Construa <tela/componente> em <stack> para <produto/persona>.
Direção visual intencional com frontend-design (nada de default
de template); palette, tipografia e guidelines do stack via
ui-ux-pro-max; feche com a11y-audit em WCAG 2.1 AA.
Sucesso: componente renderizando + tokens documentados (cores,
fontes, espaçamento) + auditoria a11y sem findings CRITICAL.
```

## R2 — Estética específica (escolha UMA)

**Skills:** `minimalist-ui` OU `industrial-brutalist-ui` OU `high-end-visual-design` OU `emil-design-eng`
**Quando:** o projeto pede uma direção de arte forte e definida.

```text
Aplique a estética <UMA: minimalist-ui | industrial-brutalist-ui |
high-end-visual-design | emil-design-eng> na tela <tela> em
<stack>. Siga a direção à risca: tipografia, densidade, cor e
motion coerentes com a estética escolhida — sem emprestar
elementos de outra.
Sucesso: a tela é identificável como a estética escolhida em um
screenshot, e um checklist de 5 traços da estética passa.
```

## R3 — Screenshot → código

**Skills:** `image-to-code` + `ui-ux-pro-max`
**Quando:** você tem referência visual (screenshot, mockup) e quer componente fiel.

```text
Anexo: <screenshot/mockup>. Gere com image-to-code o componente
em <stack>, fiel ao layout. Mapeie cores e fontes para os tokens
do design system via ui-ux-pro-max — nada de valores hardcoded
soltos.
Sucesso: diff visual mínimo vs a referência + zero cores/fontes
fora dos tokens.
```

## R4 — Redesign sem quebrar o conteúdo

**Skills:** `redesign-existing-projects` + `web-design-guidelines` + `a11y-audit`
**Quando:** página/produto existente precisa de cara nova preservando informação e fluxo.

```text
Redesenhe <página/fluxo> com redesign-existing-projects,
preservando arquitetura de informação e conteúdo. Valide contra
web-design-guidelines e feche com a11y-audit (AA).
Sucesso: before/after lado a lado + checklist de guidelines
passando + nenhuma regressão de conteúdo ou navegação.
```

## Veja também

- `design-taste-frontend` — base de bom gosto quando você ainda NÃO escolheu estética (não combinar com uma estética específica).
- `imagegen-frontend-web` / `imagegen-frontend-mobile` — gerar referência visual antes de codar.
- `a11y-guardian` — depois do audit pontual: gate contínuo de a11y em CI.
