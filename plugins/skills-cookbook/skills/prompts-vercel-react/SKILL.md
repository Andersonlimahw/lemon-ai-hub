---
name: prompts-vercel-react
description: Ready-to-paste prompts for the Vercel/React family — React and Next.js best-practice audits, performance optimization, composition refactors, view transitions, React Native/Expo, and deploys.
---

# Prompts — Vercel & React

Receitas para a família `vercel-*`: auditar, otimizar, compor, animar e deployar apps React/Next.js e React Native.

## R1 — Auditoria de best practices + performance

**Skills:** `vercel-react-best-practices` + `vercel-optimize` + `bundle-analyzer`
**Quando:** app React/Next lento, Lighthouse baixo, ou herança de código sem padrão.

```text
Audite <app/diretório> com vercel-react-best-practices (padrões de
componente, data fetching, rendering strategy) e vercel-optimize
(Core Web Vitals, caching, imagens/fontes). Rode bundle-analyzer
para dependências pesadas e code splitting.
Sucesso: lista única priorizada por impacto medido (LCP/CLS/bundle
kB), cada item com diff proposto; top-3 aplicados e re-medidos.
```

## R2 — Refactor de composição

**Skills:** `vercel-composition-patterns`
**Quando:** prop-drilling, god components, ou lógica duplicada entre árvores.

```text
Refatore <componente/árvore> com vercel-composition-patterns:
elimine prop-drilling e god components usando composição
(children, slots, compound components) em vez de novas props.
Comportamento idêntico — sem feature nova.
Sucesso: árvore antes/depois documentada; testes existentes verdes
sem alteração; nenhuma prop nova atravessando >2 níveis.
```

## R3 — View transitions

**Skills:** `vercel-react-view-transitions`
**Quando:** navegação/estado precisa de transição fluida sem custo de layout.

```text
Adicione view transitions em <páginas/elementos> com
vercel-react-view-transitions: transição de página em <rotas> e
morph do elemento <elemento> entre telas.
Sucesso: transições rodando nos navegadores suportados com
fallback limpo; zero regressão de CLS/INP medida.
```

## R4 — React Native / Expo performático

**Skills:** `vercel-react-native-skills`
**Quando:** listas travando, animações a 30fps, ou uso de APIs nativas no Expo/RN.

```text
Otimize <tela/lista> do app RN/Expo com vercel-react-native-skills:
virtualização correta da lista <lista>, animações no UI thread e
acesso nativo via <módulo>.
Sucesso: FPS medido antes/depois na tela alvo; scroll sem frame
drop com <N> itens; nenhuma ponte JS em hot path.
```

## R5 — Deploy com envs e tokens corretos

**Skills:** `deploy-to-vercel` + `vercel-cli-with-tokens`
**Quando:** publicar preview/produção sem vazar segredo nem quebrar env.

```text
Deploye <app> na Vercel com deploy-to-vercel usando
vercel-cli-with-tokens para autenticação por token (sem login
interativo). Confira env vars de <ambientes> antes do deploy.
Sucesso: preview URL no ar + checklist de envs conferido; nenhum
segredo em log ou commit.
```

## Veja também

- `frontend-design` + `ui-ux-pro-max` — a camada visual (trilha [prompts-design-frontend](../prompts-design-frontend/SKILL.md)).
- `webapp-testing` / `chrome-qa-loop` — validar o resultado no browser.
- `bundle-watch` — depois do fix pontual: gate contínuo de tamanho em CI.
