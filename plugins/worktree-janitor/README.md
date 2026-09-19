# Worktree Janitor

Faxina auditável das worktrees git que agentes de IA deixam para trás — com
autorização explícita do usuário e relatório HTML autocontido.

Agentes (Claude Code, Codex, Gemini CLI, Agy/Antigravity, OpenCode, Cursor)
criam worktrees para trabalho paralelo e nem sempre as removem. Cada uma é uma
cópia completa do repositório. Em poucas semanas viram gigabytes de branches
mergeadas, órfãs e esquecidas espalhadas por vários projetos.

## Instalação

Plugin do marketplace `lemon-ai-hub`:

```
/plugin install worktree-janitor@lemon-ai-hub
```

Depois, peça em linguagem natural: *"limpa as worktrees"*, *"faxina de
worktrees"*, *"remove as worktrees mergeadas"*.

Só precisa de `git` e `python3` (stdlib). Não depende de nenhum outro plugin.

## Fluxo

```
scan (read-only) → lista projetos/branches/diretórios → você aprova →
clean (só a seleção) → report.html + undo.sh
```

Nada é removido antes da sua confirmação.

## CLI

```bash
S=plugins/worktree-janitor/scripts/wtj.py

# 1. descobrir e classificar (nunca muta nada)
python3 $S scan --root ~/Projects --depth 5 --report --open

# 2. remover só o que foi aprovado
python3 $S clean --scan ~/.worktree-janitor/reports/<ts>/scan.json \
  --select safe --yes --open

# 3. re-renderizar o relatório
python3 $S report --result ~/.worktree-janitor/reports/<ts>/result.json --open
```

`--select` aceita `safe`, `review`, `risky`, `all`, `none`, ids (`1,3,5`) e
intervalos (`1-4`).

## Classificação

| Risco | Motivos | Pré-selecionado |
|---|---|---|
| `safe` | `prunable`, `merged`, `upstream-gone`, `orphan-detached`, `no-unique-commits` | ✅ |
| `review` | `stale` (≥ 14 dias sem commit) | ❌ |
| `risky` | `dirty` (alterações não commitadas) | ❌ |
| `keep` | `active` (commits próprios e recentes) | ❌ |
| `protected` | worktree principal, sessão atual, `locked`, glob `--protect` | 🔒 nunca |

Regras completas e limitações conhecidas: [`references/criteria.md`](references/criteria.md).

## Saída

Cada execução escreve em `~/.worktree-janitor/reports/<timestamp>/`:

| Arquivo | Conteúdo |
|---|---|
| `scan.json` | inventário classificado (entrada do `clean`) |
| `result.json` | o que foi removido, falhou ou pulado |
| `report.html` | relatório offline: cards, tabela filtrável, distribuição, undo, legenda |
| `undo.sh` | comandos de restauração de branches e worktrees |

O HTML é autocontido: sem CDN, sem fontes externas, sem rede. Abre em
`file://`, respeita `prefers-color-scheme`.

## Configuração opcional

`~/.worktree-janitor.json`:

```json
{
  "roots": ["~/Projects", "~/work"],
  "protect": ["*/hotfix-*"],
  "staleDays": 21
}
```

## Garantias

- `scan` nunca muta o repositório.
- `clean` exige `--yes` e só toca ids explicitamente selecionados.
- Worktree principal, sessão atual e worktrees `locked` nunca são removidas —
  nem com `--select all`.
- Worktree suja exige seleção manual do id **e** `--force`.
- Toda remoção gera `undo.sh`. Alterações não commitadas **não** são
  recuperáveis — por isso elas nunca entram na seleção padrão.

## Testes

```bash
cd plugins/worktree-janitor && python3 -m unittest discover -s tests -v
```

24 testes cobrindo classificação, seleção, remoção, política de branch,
proteção, undo e renderização (fixtures git reais em tmpdir).
