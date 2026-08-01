---
name: skills-cookbook
description: Example-prompt cookbook for the hub's skills — recipes, combos, and anti-patterns. Use when the user wants example prompts, asks how to use or combine skills (project understanding, feedback loops, product, marketing, design/frontend), or wants to reduce cognitive load while navigating the skill catalog.
---

# Skills Cookbook

Receitas de prompts prontos-para-colar que ensinam a usar as skills deste hub com eficiência — menos tentativa-e-erro, menos carga cognitiva. Cada receita cita as skills pelo nome exato, traz placeholders `<...>` e termina com um critério de sucesso verificável.

## Como usar

1. Escolha a trilha (abaixo) e a receita que casa com sua situação.
2. Copie o prompt, preencha os `<placeholders>`.
3. Cole no chat. Em pedidos não-triviais o pipeline padrão do hub roda por cima: `senior-prompt-engineer` → `skills-selector` → `smart-dispatch`.
4. Cheque o resultado contra o **Sucesso:** da receita antes de aceitar.

## Regras de combinação

1. **Combine camadas diferentes, nunca a mesma camada duas vezes.** Ex.: direção visual (`frontend-design`) + dados de design (`ui-ux-pro-max`) + compliance (`a11y-audit`) funciona; duas estéticas juntas não.
2. **Máximo ~3 skills por prompt.** Mais que isso dilui o contexto e piora todas.
3. **Uma estética por vez.** `minimalist-ui`, `industrial-brutalist-ui`, `high-end-visual-design` e `emil-design-eng` são direções de arte autoexcludentes.
4. **Um loop driver por vez.** `karpathy-loop`, `error-fixer-loop`, `api-test-loop` e `chrome-qa-loop` são donos de ciclo; encadeie em sequência, nunca em paralelo sobre o mesmo alvo.
5. **Cite a skill pelo nome exato** no prompt — o seletor ativa com muito mais precisão.
6. **Sempre feche com critério de sucesso verificável** (Karpathy: metas verificáveis deixam o agente iterar sozinho).

## Anti-padrões (nunca combinar)

| Skills | Tipo | Regra |
|---|---|---|
| `minimalist-ui` × `industrial-brutalist-ui` × `high-end-visual-design` × `emil-design-eng` | autoexcludentes | escolha UMA direção estética por tela/projeto |
| `design-taste-frontend` × qualquer estética acima | sobreposição | use taste como base geral OU uma estética específica, não ambos |
| `feature-flag` × `feature-flags` | sobreposição | implementação/fix pontual OU tracking contínuo em CI — escolha por objetivo, não os dois como driver |
| `code-smell` × `code-smell-detector` | sobreposição | análise pontual sob demanda OU enforcement contínuo em CI — escolha por objetivo |
| `doc-driven-grilling` × `task-interrogator` | sobreposição | mesmo grilling de base; um gera docs (ADRs/glossário), o outro gera tarefas — em sequência ok, como drivers paralelos não |
| `competitors` × `competitor-profiling` | sobreposição | análise ampla de mercado OU perfil profundo de um player |
| `webapp-testing` × `playwright` × `chrome-qa-loop` | sobreposição | toolkit pontual OU E2E scriptado OU loop exploratório — por objetivo |
| `image` × `imagegen` × `brandkit` | sobreposição | asset avulso OU imagem de frontend OU brand board |
| `caveman` × `teaching` / `learning-output-style` | objetivos conflitantes | compressão máxima vs. didática — nunca no mesmo turno |
| `copywriting` × `copy-editing` | conflito de passe | escrever do zero OU editar existente; sequencial ok, simultâneo não |
| `karpathy-loop` × `error-fixer-loop` (mesmo alvo) | conflito de driver | um loop dono do ciclo; o outro entra como etapa, não como driver |

## Combos que funcionam

- `frontend-design` + `ui-ux-pro-max` + `a11y-audit` — direção + dados + compliance
- `image-to-code` + `ui-ux-pro-max` — screenshot → código com tokens de design
- `copywriting` + `marketing-psychology` + `emails` — mensagem + persuasão + canal
- `seo-audit` + `ai-seo` + `schema` — SEO clássico + AI search + dados estruturados (complementares, não redundantes)
- `pricing` + `paywalls` + `churn-prevention` — funil de monetização ponta a ponta
- `product-marketing` + `launch` + `social` — posicionamento + lançamento + distribuição
- `architecture-deepener` + `llm-wiki-curator` + `teaching` — entender + documentar + aprender
- `api-test-loop` + `verification-before-completion` — loop de validação + gate de conclusão
- `chrome-qa-loop` → `bug-diagnostics` → `error-fixer-loop` — sequência finding → diagnóstico → fix (nunca simultâneos)

## Trilhas

| Trilha | Sub-skill | Foco |
|---|---|---|
| Entender projetos | [prompts-project-understanding](skills/prompts-project-understanding/SKILL.md) | reduzir carga cognitiva: arquitetura, wiki, aprendizado guiado, grilling de specs |
| Loops de feedback | [prompts-feedback-loops](skills/prompts-feedback-loops/SKILL.md) | validação contínua: API, QA exploratório, fix de erros, otimização |
| Produto | [prompts-product](skills/prompts-product/SKILL.md) | posicionamento, monetização, onboarding, lançamento, feedback de usuários |
| Marketing | [prompts-marketing](skills/prompts-marketing/SKILL.md) | copy, SEO + AI search, email, social, marca |
| Design & Frontend | [prompts-design-frontend](skills/prompts-design-frontend/SKILL.md) | direção visual, estéticas, screenshot→código, redesign, acessibilidade |

## Guardrails

- Prompts de exemplo em pt-BR; identificadores e nomes de skills sempre em inglês, exatos.
- O cookbook aponta e ensina — não replica o conteúdo das skills alvo.
- Toda skill citada existe em `plugins/` deste repo; se uma receita citar algo que não existe mais, a receita está quebrada e deve ser corrigida.
