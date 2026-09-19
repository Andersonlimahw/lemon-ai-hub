---
name: "worktree-janitor"
description: "Limpa worktrees git abandonadas por agentes de IA (Claude Code, Codex, Gemini CLI, Agy/Antigravity, OpenCode, Cursor) em todos os projetos da máquina, com autorização explícita do usuário e relatório HTML autocontido. Classifica cada worktree por risco — órfã, mergeada, upstream removido, sem commits próprios, stale, suja, ativa, protegida — lista projetos/branches/diretórios antes de remover qualquer coisa, aplica só a seleção aprovada e gera undo.sh. Use quando o usuário pedir para limpar worktrees, remover worktrees órfãs ou mergeadas, fazer faxina de branches de agentes, liberar espaço de worktrees, auditar worktrees da máquina, ou disser \"limpar worktrees\", \"worktree cleanup\", \"faxina de worktrees\", \"clean worktrees\", \"remover worktrees antigas\", \"relatório de worktrees\"."
---

# Worktree Janitor

Faxina auditável das worktrees git que agentes de IA deixam para trás. **Nada é
removido sem aprovação explícita do usuário.**

O plugin é *apartado*: não depende de `git-expert`, `rtk` ou de qualquer outro
plugin do hub. Só precisa de `git` e `python3` (stdlib).

## Contrato de segurança (não negociável)

1. `scan` é **read-only**. Nunca mutila nada.
2. `clean` só toca ids passados em `--select` e exige `--yes`.
3. Worktree principal do repositório, worktree da sessão atual e worktrees
   travadas (`git worktree lock`) são **protegidas** — jamais removidas, nem com
   `--select all`.
4. Worktree com alterações não commitadas é classificada `risky` e **não entra**
   na seleção padrão. Só vai embora se o usuário escolher o id explicitamente.
5. Toda execução gera `undo.sh` com os comandos de restauração.
6. Se o usuário negar ou não responder, a resposta correta é **não remover nada**
   e entregar só o relatório de prévia.

## Fluxo (siga na ordem)

### 1. Preflight

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/wtj.py --version
```

Fora do Claude Code, use o caminho real do plugin (ex.:
`~/Projects/IA/lemon-ai-hub/plugins/worktree-janitor/scripts/wtj.py`).

Se o usuário informou raízes de busca, use-as. Caso contrário o default é
`~/Projects` (ou o que estiver em `~/.worktree-janitor.json`).

### 2. Varredura e listagem

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/wtj.py scan \
  --root ~/Projects --depth 5 --out /tmp/wtj-$(date +%s) --json
```

Apresente ao usuário, **agrupado por projeto**, e nesta ordem de colunas:

| id | projeto | branch | diretório | harness | classificação | motivo | tamanho | idade |

Regras de apresentação:

- Liste primeiro `safe`, depois `review`, depois `risky`. `keep` e `protected`
  entram em uma linha-resumo ("N worktrees ativas/protegidas foram ignoradas"),
  não na tabela principal — elas não são candidatas.
- Sempre mostre o caminho absoluto do diretório: é isso que o usuário reconhece.
- Sempre mostre o total de espaço recuperável.
- Se `summary.candidates == 0`, diga que não há nada a limpar, gere o relatório
  de prévia (`scan --report`) e **encerre** — não pergunte nada.

### 3. Autorização explícita

Use `AskUserQuestion` (ou pergunta direta, se o harness não tiver a ferramenta)
com as opções:

- **Confirmar todas as seguras** — `--select safe` (recomendado)
- **Seguras + revisar** — `--select all` exceto `risky`
- **Selecionar manualmente** — o usuário responde com os ids
- **Cancelar** — nada é removido

Nunca assuma consentimento. Nunca interprete silêncio como "sim". Se o usuário
escolher ids que incluem `risky`, repita em uma frase o que será perdido
(alterações não commitadas) e confirme antes de executar.

### 4. Limpeza

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/wtj.py clean \
  --scan <scan.json> --select <safe|all|1,3,5-7> --yes --open
```

- `--delete-branch auto` (default): remove a branch local só quando ela está
  mergeada, com upstream removido ou sem commits próprios.
- `--delete-branch never`: mantém todas as branches locais.
- `--force`: necessário para remover worktree suja selecionada manualmente.

### 5. Relatório

`clean` renderiza o HTML automaticamente. Entregue ao usuário o **caminho
absoluto**, pronto para abrir:

```
file:///Users/<user>/.worktree-janitor/reports/<timestamp>/report.html
```

Diga a frase completa, por exemplo:

> Relatório: `/Users/x/.worktree-janitor/reports/20260919-213000/report.html`
> — abra no browser (`open <caminho>`) ou clique no link `file://` acima.

Cada execução deixa 4 arquivos no mesmo diretório:
`scan.json`, `result.json`, `report.html`, `undo.sh`.

### 6. Fechamento

Reporte em uma linha: removidas, falhas, puladas, espaço liberado, caminho do
`undo.sh`. Se houve falha, mostre o erro do git literalmente.

## Critérios de classificação

Detalhes, casos de borda e limitações conhecidas: `references/criteria.md`.

| Classificação | Significado | Na seleção padrão? |
|---|---|---|
| `safe` | órfã (`prunable`), mergeada, upstream removido, sem commits próprios | sim |
| `review` | stale (sem commits há ≥ N dias) ou segura porém suja | não |
| `risky` | alterações não commitadas | não |
| `keep` | commits próprios e recentes — trabalho ativo | não |
| `protected` | worktree principal, sessão atual, travada, glob protegido | nunca |

## Configuração opcional

`~/.worktree-janitor.json`:

```json
{
  "roots": ["~/Projects", "~/work"],
  "protect": ["*/hotfix-*", "/Users/x/Projects/critico/*"],
  "staleDays": 21
}
```

## Uso não interativo (CI / cron)

```bash
python3 scripts/wtj.py scan --root ~/Projects --json --out /tmp/wtj > /tmp/wtj/scan.out
python3 scripts/wtj.py clean --scan /tmp/wtj/scan.json --select safe --yes --json
```

`clean` sai com código 1 se qualquer remoção falhar. Em automação, prefira
`--select safe` — nunca `all`.

## Anti-padrões

- ❌ Rodar `clean` sem mostrar a lista antes.
- ❌ Usar `--select all --force` por conveniência.
- ❌ Remover worktrees dentro do repositório em que o usuário está trabalhando
  agora (o script já protege a sessão atual; não tente contornar).
- ❌ Reescrever o relatório à mão em Markdown — o entregável é o HTML.
