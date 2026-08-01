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
| `X` × `X-advisor/-watch/-runner/-guardian/-detector` | regra geral do hub | pontual (investigar/fixar agora) × contínuo (gate de CI) — escolha por objetivo, nunca os dois como driver do mesmo passe (`async-patterns`×`async-advisor`, `bundle-analyzer`×`bundle-watch`, `load-test`×`load-test-runner`, `chaos-test`×`chaos-runner`, `a11y-audit`×`a11y-guardian`) |
| `create-plugin` × `plugin-creator` × `plugin-generator` × `skill-creator` | sobreposição de geradores | UM gerador por artefato; neste repo o layout canônico de `validate_plugins.py` manda |
| `security-best-practices` × `security-guidance` | sobreposição | checklist de código OU orientação contextual — não empilhar |
| `playwright` × `playwright-interactive` | sobreposição | E2E scriptado OU sessão interativa |
| `openapi-generate` × `openapi-hub` | sobreposição | gerar spec pontual OU gestão contínua de specs |
| `cli-creator` × `cli-generator` | sobreposição | escolha pelo runtime alvo (Codex-composável vs Bun spec-first) |
| `imagegen` × `imagegen-frontend-web` / `imagegen-frontend-mobile` | sobreposição | geral OU específica de frontend — pela finalidade do asset |

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
- `karpathy-guidelines` + `karpathy-recipe` + `karpathy-loop` — princípios sempre, receita no trabalho grande, loop na métrica (complementares)
- `vercel-react-best-practices` + `vercel-optimize` + `bundle-analyzer` — padrões + vitals + peso do bundle
- `openapi-generate` + `postman-generator` + `api-test-loop` — spec → collection → validação viva
- `db-index-advisor` + `supabase-postgres-best-practices` — índice certo na modelagem certa
- `code-review-expert` + `commit-quality` + `pr-review-canvas` — review + higiene + apresentação
- `notion-spec-to-implementation` + `doc-driven-grilling` — spec grilada antes de virar código

## Trilhas

| Trilha | Sub-skill | Foco |
|---|---|---|
| Entender projetos | [prompts-project-understanding](skills/prompts-project-understanding/SKILL.md) | reduzir carga cognitiva: arquitetura, wiki, aprendizado guiado, grilling de specs |
| Loops de feedback | [prompts-feedback-loops](skills/prompts-feedback-loops/SKILL.md) | validação contínua: API, QA exploratório, fix de erros, otimização |
| Produto | [prompts-product](skills/prompts-product/SKILL.md) | posicionamento, monetização, onboarding, lançamento, feedback de usuários |
| Marketing | [prompts-marketing](skills/prompts-marketing/SKILL.md) | copy, SEO + AI search, email, social, marca |
| Design & Frontend | [prompts-design-frontend](skills/prompts-design-frontend/SKILL.md) | direção visual, estéticas, screenshot→código, redesign, acessibilidade |
| Método Karpathy | [prompts-karpathy](skills/prompts-karpathy/SKILL.md) | guidelines, receita para trabalho grande, review por princípios, loop de métrica |
| Vercel & React | [prompts-vercel-react](skills/prompts-vercel-react/SKILL.md) | best practices, otimização, composição, view transitions, RN/Expo, deploy |
| Qualidade de engenharia | [prompts-engineering-quality](skills/prompts-engineering-quality/SKILL.md) | review de PR, async, banco, threat model, carga/caos, i18n |
| APIs & CLIs | [prompts-apis-clis](skills/prompts-apis-clis/SKILL.md) | OpenAPI, Postman, CLIs para agentes, wrapping de CLIs |
| Mobile & Release | [prompts-mobile-release](skills/prompts-mobile-release/SKILL.md) | go/no-go iOS/Android, App Store Connect, Play API, ASO |
| Dados & Backend | [prompts-data-backend](skills/prompts-data-backend/SKILL.md) | Supabase/Postgres, Firebase, decisões de banco, incidentes |
| Conhecimento & Notion | [prompts-knowledge-notion](skills/prompts-knowledge-notion/SKILL.md) | capturar decisões, reuniões, pesquisa, spec→código, aprendizado persistente |
| Meta-harness | [prompts-meta-harness](skills/prompts-meta-harness/SKILL.md) | criar skills/plugins, hooks, orquestração multi-agente, migração, tokens |
| Índice A–Z | [prompts-catalog-index](skills/prompts-catalog-index/SKILL.md) | todos os 159 plugins do hub com quando-usar de uma linha |

## Guardrails

- Prompts de exemplo em pt-BR; identificadores e nomes de skills sempre em inglês, exatos.
- O cookbook aponta e ensina — não replica o conteúdo das skills alvo.
- Toda skill citada existe em `plugins/` deste repo; se uma receita citar algo que não existe mais, a receita está quebrada e deve ser corrigida.
