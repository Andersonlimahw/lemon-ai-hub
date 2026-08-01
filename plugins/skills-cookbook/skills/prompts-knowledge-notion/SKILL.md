---
name: prompts-knowledge-notion
description: Ready-to-paste prompts for knowledge workflows — capturing decisions into Notion, meeting intelligence, research documentation, spec-to-implementation, and cross-session learning persistence.
---

# Prompts — Conhecimento & Notion

Receitas para transformar conversa volátil em conhecimento persistente — no Notion e entre sessões do harness. Complementa a trilha [prompts-project-understanding](../prompts-project-understanding/SKILL.md): lá você entende; aqui você registra e reaproveita.

## R1 — Capturar decisões e conhecimento

**Skills:** `notion-knowledge-capture`
**Quando:** a sessão/discussão gerou decisões que não podem morrer no chat.

```text
Capture com notion-knowledge-capture as decisões desta
sessão/thread sobre <tema> na página/database <destino>: decisão,
contexto, alternativas descartadas e follow-ups com dono.
Sucesso: página criada com as decisões rastreáveis; follow-ups
como itens acionáveis; nada de transcrição bruta.
```

## R2 — Inteligência de reunião

**Skills:** `notion-meeting-intelligence`
**Quando:** notas de reunião precisam virar ações, não arqueologia.

```text
Processe com notion-meeting-intelligence as notas da reunião
<reunião/página>: extraia decisões, ações com dono e prazo, e
pontos em aberto; cruze com as reuniões anteriores de <série>.
Sucesso: resumo com ações atribuídas; pendências recorrentes
sinalizadas; link para as fontes.
```

## R3 — Pesquisa documentada

**Skills:** `notion-research-documentation`
**Quando:** pesquisa (técnica ou de mercado) precisa de trilha auditável de fontes.

```text
Documente com notion-research-documentation a pesquisa sobre
<pergunta>: estrutura pergunta → fontes → achados → síntese →
recomendação, na database <destino>.
Sucesso: cada achado com fonte linkada; síntese separada de
opinião; recomendação com confiança declarada.
```

## R4 — Spec no Notion → implementação

**Skills:** `notion-spec-to-implementation` + `doc-driven-grilling`
**Quando:** a spec vive no Notion e vai virar código.

```text
Puxe a spec <página Notion> com notion-spec-to-implementation e
grile antes com doc-driven-grilling: ambiguidades e assunções
primeiro, depois o plano de implementação com verificação por
etapa.
Sucesso: gaps da spec respondidos ou registrados; plano com
"→ verify:" por etapa; rastreio spec→código por item.
```

## R5 — Aprendizado que sobrevive à sessão

**Skills:** `continual-learning` + `session-handoff`
**Quando:** lições e contexto precisam atravessar sessões/compactações.

```text
Persista com continual-learning as lições desta sessão sobre
<tema> (erros cometidos, padrões que funcionaram). Gere com
session-handoff o handoff para a próxima sessão continuar sem
re-explorar.
Sucesso: lições consultáveis na próxima sessão; handoff com estado,
decisões e próximos passos em ≤1 página.
```

## Veja também

- `teaching-workspace` — ambiente de estudo estruturado; `teaching` monta o plano (trilha [prompts-project-understanding](../prompts-project-understanding/SKILL.md) R3).
- `llm-wiki-curator` — wiki do código; Notion guarda o resto do conhecimento.
- `writing-guidelines` — padrão de escrita para tudo que essas receitas produzem.
