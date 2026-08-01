---
name: prompts-meta-harness
description: Ready-to-paste prompts for extending and operating the AI harness itself — authoring skills and plugins, hooks, multi-agent orchestration, cross-harness migration, and token economy.
---

# Prompts — Meta-harness (estender o próprio hub)

Receitas para criar skills/plugins, automatizar o harness com hooks, orquestrar subagentes e economizar tokens. Escolha de gerador: `skill-creator` (skill nova guiada) × `create-plugin` / `plugin-creator` / `plugin-generator` (geradores de plugin sobrepostos) — escolha UM gerador por artefato; neste repo, siga o layout canônico validado por `scripts/validate_plugins.py`.

## R1 — Criar uma skill nova

**Skills:** `skill-creator` + `skill-authoring`
**Quando:** um fluxo seu se repete e merece virar skill reutilizável.

```text
Crie com skill-creator a skill <nome> que <capacidade>. Aplique
skill-authoring: description com gatilhos explícitos ("Use
when..."), corpo enxuto, exemplos multishot só onde desambiguam.
Trigger esperado: <frases que devem ativar>.
Sucesso: SKILL.md com frontmatter válido; as frases de trigger
ativam a skill em teste; nenhuma instrução redundante com o
harness.
```

## R2 — Automatizar com hooks

**Skills:** `hookify`
**Quando:** "sempre que X acontecer, faça Y" — comportamento que precisa ser do harness, não de memória.

```text
Crie com hookify um hook que <comportamento — ex.: rode o linter
após cada Edit em *.ts; bloqueie commit se validate_plugins.py
falhar>. Evento: <PreToolUse/PostToolUse/SessionStart/...>.
Sucesso: hook registrado em settings.json; disparo demonstrado com
um caso positivo e um negativo; fácil de desativar.
```

## R3 — Orquestração multi-agente

**Skills:** `orchestrate` + `subagent-driven-development`
**Quando:** trabalho fan-out (muitos arquivos/frentes) que uma sessão só não segura.

```text
Orquestre <trabalho> com orchestrate: quebre em subtarefas
independentes, um subagente por frente com modelo/esforço adequado
à complexidade de cada uma (subagent-driven-development), e um
passe final de integração + review.
Sucesso: cada subagente com entrega verificável; integração sem
conflito; custo/modelo por subagente justificado em uma linha.
```

## R4 — Migrar/espelhar para outro harness

**Skills:** `migrate-to-codex` + `opencode-subagent`
**Quando:** levar skills/fluxos do Claude Code para Codex/OpenCode ou delegar entre CLIs.

```text
Migre <skill/fluxo> para <Codex/OpenCode> com migrate-to-codex:
mapeie o que é portável, ajuste frontmatter/paths por harness e
mantenha o Claude Code como fonte canônica (symlinks). Para
delegação pontual, use opencode-subagent.
Sucesso: skill visível e funcional no harness alvo; fonte única
preservada (nenhum fork divergente).
```

## R5 — Economia de tokens

**Skills:** `token-saver` + `caveman`
**Quando:** sessões estourando contexto ou custo; respostas verbosas demais.

```text
Aplique token-saver na sessão/projeto <alvo>: identifique os
maiores consumidores (outputs de CLI, arquivos relidos, verbosidade)
e proponha cortes. Ative caveman <lite|full|ultra> para compressão
de resposta.
Sucesso: economia estimada por fonte com número; conteúdo técnico
preservado (nenhuma informação de código perdida).
```

## Veja também

- `senior-prompt-engineer` → `skills-selector` → `smart-dispatch` — o pipeline padrão do hub; refine antes de rotear.
- `ai-workspace-orchestrator` — montar um workspace de agentes do zero (contrato + review adversarial do setup).
- `agentic-value-loops` — loops de valor contínuos (docs, manutenção, segurança) rodando como rotina.
- `cli-wrapper` — envelopar CLIs externos (trilha [prompts-apis-clis](../prompts-apis-clis/SKILL.md) R3).
- `agent-sdk-dev` — construir agentes programáticos no Claude Agent SDK.
- `skill-installer` — instalar skills de fora no harness local.
