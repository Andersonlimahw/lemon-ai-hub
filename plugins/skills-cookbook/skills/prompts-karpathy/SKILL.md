---
name: prompts-karpathy
description: Ready-to-paste prompts for the Karpathy method — behavioral guidelines while coding, the full recipe for medium/large work, review against the four principles, and the autonomous optimization loop.
---

# Prompts — Método Karpathy

O trio `karpathy-guidelines` (princípios comportamentais), `karpathy-recipe` (receita para trabalho médio/grande) e `karpathy-loop` (ciclos autônomos de otimização). São complementares, não redundantes: guidelines valem sempre; recipe estrutura trabalho grande; loop persegue métrica.

## R1 — Guidelines em qualquer implementação

**Skills:** `karpathy-guidelines`
**Quando:** qualquer código não-trivial — o default para reduzir os erros clássicos de LLM.

```text
Implemente <feature/fix> em <path> aplicando karpathy-guidelines:
declare assunções antes de codar (pergunte se alguma for
estrutural), mínimo código que resolve, mudanças cirúrgicas
(nada de "melhorar" código vizinho), e plano numerado com
"→ verify:" por passo.
Sucesso: cada linha do diff rastreia ao pedido; todos os verify
executados com evidência.
```

## R2 — Receita completa para trabalho médio/grande

**Skills:** `karpathy-recipe` + `verification-before-completion`
**Quando:** feature/refactor que atravessa vários arquivos ou sessões.

```text
Estruture <trabalho> com karpathy-recipe: quebre em estágios com
critério verificável cada, execute estágio a estágio, e feche cada
um com verification-before-completion antes de avançar.
Sucesso: plano com estágios + verificação; nenhum estágio marcado
completo sem o check rodado; diff final sem escopo extra.
```

## R3 — Review contra os quatro princípios

**Skills:** `karpathy-guidelines` + `code-review-expert`
**Quando:** revisar um diff/PR procurando os vícios que as guidelines previnem.

```text
Revise o diff de <branch/PR> com code-review-expert usando
karpathy-guidelines como rubrica: (1) assunções escondidas,
(2) complexidade especulativa/abstração prematura, (3) mudanças
não-cirúrgicas fora do escopo, (4) critérios de sucesso fracos ou
não verificados.
Sucesso: cada finding mapeado a um princípio, com arquivo:linha
e fix de 1 frase.
```

## R4 — Loop autônomo de métrica

**Skills:** `karpathy-loop`
**Quando:** métrica objetiva para otimizar em ciclos. Receita completa na trilha [prompts-feedback-loops](../prompts-feedback-loops/SKILL.md) (R4) — um loop driver por vez.

## Veja também

- `verification-before-completion` — gate universal de "está pronto mesmo?".
- `continual-learning` — persistir lições dos ciclos entre sessões.
