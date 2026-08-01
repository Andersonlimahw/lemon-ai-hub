---
name: prompts-catalog-index
description: Complete A-to-Z index of every plugin in the hub with a one-line when-to-use hint, grouped by area. Use to locate the right skill fast when no cookbook track matches, or to browse the full catalog without reading raw descriptions.
---

# Índice completo do catálogo (159 plugins)

Uma linha por plugin: **quando usar**. Agrupado por área; trilhas com receita completa estão linkadas no [SKILL.md raiz](../../SKILL.md). Regra transversal do hub: pares `X` × `X-advisor/-watch/-runner/-guardian/-detector` = pontual × contínuo/CI — escolha por objetivo.

## Entender & aprender

| Plugin | Quando usar |
|---|---|
| `architecture-deepener` | codebase raso/confuso: mapa de módulos + oportunidades de aprofundar design |
| `llm-wiki-curator` | gerar wiki navegável do código para onboarding |
| `teaching` | plano de aprendizado com milestones e checkpoints |
| `teaching-workspace` | ambiente de estudo estruturado para praticar |
| `learning-output-style` | respostas em formato didático |
| `doc-driven-grilling` | grilar plano/spec e gerar ADRs/glossário antes de codar |
| `task-interrogator` | grilar plano e transformar em tarefas com aceite |
| `session-handoff` | fim de sessão longa: handoff para a próxima começar sem re-explorar |
| `continual-learning` | persistir lições entre sessões |
| `bug-diagnostics` | entender comportamento quebrado: repro → hipóteses → fix |
| `code-smell` | análise pontual de cheiros de código |
| `code-smell-detector` | enforcement contínuo de cheiros em CI |

## Loops & QA

| Plugin | Quando usar |
|---|---|
| `api-test-loop` | loop de validação de API via CURL com findings.md |
| `chrome-qa-loop` | QA exploratório de app web vivo, um report por finding |
| `computer-use-swiftui-loop` | loop visual para apps macOS/SwiftUI (Computer Use, app Codex) |
| `error-fixer-loop` | falha de build/teste: investigar → fixar → regra anti-regressão |
| `karpathy-loop` | ciclos autônomos de otimização de métrica |
| `webapp-testing` | toolkit Playwright pontual: screenshots, logs, interação |
| `playwright` | E2E scriptado |
| `playwright-interactive` | sessão de browser interativa/assistida |
| `verification-before-completion` | gate "está pronto mesmo?" antes de declarar concluído |
| `agentic-value-loops` | loops de valor contínuos: feature, docs, manutenção/segurança, AI tuning |

## Método Karpathy

| Plugin | Quando usar |
|---|---|
| `karpathy-guidelines` | princípios comportamentais em qualquer código não-trivial |
| `karpathy-recipe` | receita por estágios para trabalho médio/grande |

## Engenharia & segurança

| Plugin | Quando usar |
|---|---|
| `code-review-expert` | review estruturado de diff/PR |
| `pr-review-canvas` | renderizar findings de review como comentários inline |
| `commit-quality` | higiene de commits semânticos |
| `async-patterns` | auditar races, N+1 async, paralelismo sem limite |
| `async-advisor` | gate de padrões async em CI/PR |
| `bundle-analyzer` | investigar bundle pesado agora |
| `bundle-watch` | gate de tamanho de bundle em CI |
| `db-advisor` | monitoramento contínuo do banco com relatórios de saúde |
| `db-index-advisor` | índice para query lenta específica |
| `load-test` | desenhar teste de carga/SLO |
| `load-test-runner` | rodar/agendar cargas recorrentes |
| `chaos-test` | desenhar experimentos de falha |
| `chaos-runner` | orquestrar/agendar chaos com score de resiliência |
| `security-best-practices` | checklist de práticas seguras no código |
| `security-guidance` | orientação de segurança contextual |
| `security-ownership-map` | mapear donos por área de segurança |
| `security-threat-model` | STRIDE de feature nova |
| `i18n-audit` | achar chaves faltando/órfãs/hardcoded |
| `i18n-sync` | sincronizar estrutura entre locales |
| `feature-flag` | implementar/usar flag pontual |
| `feature-flags` | gestão contínua de flags |
| `feature-purge` | remover feature inteira sem deixar código morto |
| `finishing-a-development-branch` | fechar branch com qualidade antes do merge |
| `git-expert` | commits semânticos, bisect, fluxo git |
| `gh-expert` | PRs, issues e automação via gh CLI |
| `incident-center` | registro e postmortem de incidentes |
| `incident-runbook` | resposta guiada durante o incidente |

## APIs & CLIs

| Plugin | Quando usar |
|---|---|
| `openapi-generate` | gerar spec OpenAPI do código (pontual) |
| `openapi-hub` | gestão contínua de múltiplas specs |
| `postman-generator` | collection Postman a partir de spec/rotas |
| `cli-creator` | CLI composável de uma API (foco Codex) |
| `cli-generator` | CLI Bun completa a partir de SPEC |
| `cli-for-agent` | rubrica de CLI operável por agentes |
| `cli-wrapper` | envelopar CLI externo com digest e economia de tokens |
| `agent-sdk-dev` | construir agentes no Claude Agent SDK |

## Frontend & design

| Plugin | Quando usar |
|---|---|
| `frontend-design` | direção visual intencional para UI nova |
| `design` | produção de assets de marca: logos, CIP, banners, ícones |
| `design-taste-frontend` | bom gosto de base quando ainda não há estética escolhida |
| `ui-ux-pro-max` | base de dados: estilos, paletas, fontes, guidelines por stack |
| `web-design-guidelines` | checklist de guidelines web |
| `a11y-audit` | auditoria WCAG pontual |
| `a11y-guardian` | gate contínuo de a11y em PR/CI |
| `minimalist-ui` | estética minimalista (exclusiva) |
| `industrial-brutalist-ui` | estética brutalista (exclusiva) |
| `high-end-visual-design` | estética premium (exclusiva) |
| `emil-design-eng` | estética design-engineer (exclusiva) |
| `image-to-code` | screenshot/mockup → componente |
| `redesign-existing-projects` | cara nova preservando conteúdo/fluxo |
| `imagegen-frontend-web` | gerar referência visual web |
| `imagegen-frontend-mobile` | gerar referência visual mobile |
| `scroll-world` | experiência scrollytelling |

## Vercel & React

| Plugin | Quando usar |
|---|---|
| `vercel-react-best-practices` | padrões React/Next: componentes, fetching, rendering |
| `vercel-optimize` | Core Web Vitals, caching, imagens/fontes |
| `vercel-composition-patterns` | matar prop-drilling/god components por composição |
| `vercel-react-view-transitions` | transições de página/elemento |
| `vercel-react-native-skills` | performance RN/Expo: listas, animações, nativo |
| `vercel-cli-with-tokens` | Vercel CLI autenticada por token (não-interativa) |
| `deploy-to-vercel` | publicar preview/produção |

## Mobile & release

| Plugin | Quando usar |
|---|---|
| `apple-store-release-agent` | go/no-go auditável de release iOS |
| `google-play-release-agent` | go/no-go auditável de release Android |
| `app-store-connect-api` | automação App Store Connect: TestFlight, IAP, relatórios |
| `google-play-developer-api` | automação Play Console: tracks, rollout |
| `aso` | otimizar listing das lojas |

## Dados & backend

| Plugin | Quando usar |
|---|---|
| `supabase` | operar Supabase: schema, RLS, functions |
| `supabase-postgres-best-practices` | modelagem e índices Postgres corretos |
| `firebase-expert` | Firestore/Auth/Functions/Hosting |

## Conhecimento & Notion

| Plugin | Quando usar |
|---|---|
| `notion-knowledge-capture` | decisões do chat → páginas Notion rastreáveis |
| `notion-meeting-intelligence` | notas de reunião → ações com dono |
| `notion-research-documentation` | pesquisa com trilha auditável de fontes |
| `notion-spec-to-implementation` | spec no Notion → plano de implementação |

## Produto & growth

| Plugin | Quando usar |
|---|---|
| `product-marketing` | posicionamento e mensagens-chave |
| `pricing` | tiers, âncoras e estratégia de preço |
| `paywalls` | paywall in-app nos momentos de valor |
| `offers` | bônus, garantia, framing de valor |
| `onboarding` | do cadastro ao aha-moment |
| `signup` | fluxo de cadastro que converte |
| `launch` | cronograma e execução de lançamento |
| `churn-prevention` | cancel flow, save offers, dunning, win-back |
| `analytics` | tracking plan, GA4, eventos, atribuição |
| `free-tools` | ferramenta gratuita como motor de aquisição |
| `lead-magnets` | iscas de captura de leads |
| `referrals` | programa de indicação |
| `popups` | popups de conversão sem irritar |
| `revops` | operação de receita: funil, CRM, handoffs |
| `prospecting` | prospecção outbound |
| `sales-enablement` | material e argumentos para vendas |

## Marketing & conteúdo

| Plugin | Quando usar |
|---|---|
| `copywriting` | escrever copy persuasiva do zero |
| `copy-editing` | editar/afiar copy existente |
| `writing-guidelines` | padrão de escrita clara |
| `marketing-psychology` | vieses e comportamento aplicados com ética |
| `marketing-plan` | plano de marketing completo |
| `marketing-ideas` | gerar ideias/ângulos novos |
| `marketing-council` | painel de perspectivas de marketing |
| `marketing-loops` | workflows de marketing recorrentes/agendados (cadência ou trigger) |
| `content-strategy` | estratégia e calendário de conteúdo |
| `emails` | sequências e campanhas de email |
| `sms` | campanhas SMS |
| `social` | distribuição e formatos por rede |
| `ads` | mídia paga: campanha, targeting, otimização |
| `brand` | voz, identidade e consistência de marca |
| `brandkit` | boards de brand guidelines premium |
| `seo-audit` | auditoria SEO técnica + on-page |
| `ai-seo` | ser citado por LLMs: AEO/GEO, llms.txt |
| `programmatic-seo` | páginas SEO em escala programática |
| `schema` | dados estruturados JSON-LD |
| `site-architecture` | arquitetura de site para SEO/navegação |
| `competitors` | análise ampla de concorrência |
| `competitor-profiling` | perfil profundo de um concorrente |
| `co-marketing` | parcerias de marketing |
| `community-marketing` | crescer via comunidade |
| `influencer-marketing` | campanhas com criadores |
| `public-relations` | assessoria e PR |
| `video` | roteiro e estratégia de vídeo |
| `image` | gerar/editar imagem avulsa |
| `imagegen` | geração de imagem (geral; ver variantes frontend) |

## Meta-harness & tokens

| Plugin | Quando usar |
|---|---|
| `senior-prompt-engineer` | refinar pedido em prompt definitivo + EXEC-MAP (stage-0) |
| `skills-selector` | decidir quais skills ativar (stage-1) |
| `smart-dispatch` | rotear agente/modelo/custo (stage-2) |
| `skill-creator` | criar skill nova guiada |
| `skill-authoring` | boas práticas de escrita de skill |
| `skill-installer` | instalar skills externas |
| `create-plugin` | gerador de plugin (escolha UM gerador) |
| `plugin-creator` | gerador de plugin (escolha UM gerador) |
| `plugin-generator` | gerador de plugin (escolha UM gerador) |
| `hookify` | automações "sempre que X, faça Y" via hooks |
| `orchestrate` | fan-out multi-agente com integração final |
| `subagent-driven-development` | desenvolvimento dirigido por subagentes |
| `ai-workspace-orchestrator` | montar workspace de agentes com contrato + review |
| `opencode-subagent` | delegar para OpenCode |
| `migrate-to-codex` | portar skills/fluxos para Codex |
| `caveman` | compressão de resposta (lite/full/ultra) |
| `token-saver` | cortar os maiores consumidores de contexto |
| `skills-cookbook` | este cookbook: receitas, combos e anti-padrões |

## Diversão & experimentos

| Plugin | Quando usar |
|---|---|
| `hatch-pet` | gerar/reparar spritesheet de pet (Codex) a partir de arte/imagem |
| `spotify-squad` | experiência squad + Spotify |
