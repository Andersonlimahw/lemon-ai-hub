---
name: session-handoff
description: Compacta a conversa atual em um documento de handoff para outro agent continuar o trabalho. Preserva o contexto sem duplicar artefatos.
argument-hint: "Para que será usada a próxima sessão?"
disable-model-invocation: true
---

# session-handoff

Escreva um documento de handoff resumindo a conversa atual para que um agent novo possa continuar o trabalho. Salve no diretório temporário do sistema operacional do usuário — não no workspace atual.

## Diretrizes

### Evite duplicar artefatos

Não duplique conteúdo já capturado em outros artefatos (specs, planos, ADRs, issues, commits, diffs). Faça referência a eles por caminho ou URL.

Exemplo: em vez de colar o conteúdo de um plano, escreva:

```
- Plano de implementação: docs/plans/auth-refactor-plan.md
- ADR aprovado: docs/adr/0007-session-storage.md
- Issue de origem: #142 (https://github.com/org/repo/issues/142)
- Diff em andamento: ver `git diff` no branch `feat/auth`
```

### Remova dados sensíveis

Redija qualquer informação sensível antes de escrever o documento:

- **API keys e tokens** — substitua por `[REDACTED: tipo]`, ex.: `[REDACTED: stripe_key]`
- **Senhas e segredos** — nunca os inclua; referencie o cofre/variável de ambiente, ex.: `SECRET_DB_URL (via .env / vault)`
- **PII (dados pessoais)** — emails, CPFs, telefones, nomes de usuários reais, endereços. Use marcadores como `[REDACTED: email usuário]`
- **URLs internas/privadas** — mantenha apenas se estritamente necessário para continuidade

### Seção de skills sugeridas

Inclua uma seção "Skills sugeridas" no documento, recomendando skills que o agent deveria invocar na próxima sessão.

### Argumentos do usuário

Se o usuário passou argumentos, trate-os como a descrição do foco da próxima sessão e adapte o documento de handoff de acordo.

## Estrutura do documento de handoff

Use o modelo abaixo como ponto de partida, adaptando conforme o contexto:

```markdown
# Handoff — <título curto da tarefa>

**Data:** <YYYY-MM-DD>
**Foco da próxima sessão:** <argumento do usuário, se houver>

## Objetivo
<1-3 frases descrevendo o que estava sendo feito>

## Progresso atual
- <bullets do que já foi concluído>

## Pendências
- <bullets do que ainda falta fazer>

## Decisões importantes
- <decisões tomadas e por quê>

## Artefatos de referência
- Specs/planos/ADRs: <caminhos ou URLs>
- Issues/PRs: <links>
- Branch/diff: <branch e estado>

## Armadilhas e contexto não-óbvio
- <gotchas, dependências implícitas, comandos específicos>

## Skills sugeridas
- <skill-name> — <motivo>
- <skill-name> — <motivo>

## Próximos passos sugeridos
1. <passo imediato>
2. <passo seguinte>
```

## Onde salvar

Salve o documento no diretório temporário do SO:

- **macOS/Linux:** `$TMPDIR` (geralmente `/var/folders/.../T/`) ou `/tmp/`
- **Windows:** `%TEMP%`

Nome sugerido: `handoff-<timestamp>-<slug>.md`, ex.: `handoff-20260715-auth-refactor.md`.

Informe ao usuário o caminho completo do arquivo salvo.
