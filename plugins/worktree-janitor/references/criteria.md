# Critérios de classificação

Cada worktree recebe **um** motivo primário (`reason`) e **um** nível de risco
(`risk`). Os sinais acumulados ficam em `signals[]`.

## Ordem de avaliação

A classificação é sequencial e para no primeiro critério que casar. A ordem
existe para que segurança sempre vença conveniência.

```
1. worktree principal do repositório      -> protected / main-worktree
2. worktree da sessão atual               -> protected / current-session
3. casa com um glob de --protect          -> protected / protected
4. git worktree lock                      -> protected / locked
5. prunable ou diretório inexistente      -> safe      / prunable
6. alterações não commitadas              -> risky     / dirty        (sem --include-dirty)
7. HEAD é ancestral da base               -> safe      / merged
8. upstream marcado [gone]                -> safe      / upstream-gone
9. detached sem commits à frente          -> safe      / orphan-detached
10. zero commits à frente da base         -> safe      / no-unique-commits
11. último commit há >= staleDays         -> review    / stale
12. resto                                 -> keep      / active
```

Um item `safe` que também esteja sujo (só possível com `--include-dirty`) é
rebaixado para `review`. Item `safe` é o único pré-selecionado por default.

## Detalhes por critério

### `prunable`
`git worktree list --porcelain` marca `prunable` quando o diretório de trabalho
sumiu mas o ref administrativo em `.git/worktrees/<id>` continua lá. É o caso
mais comum quando um agente é interrompido: `rm -rf` na pasta sem
`git worktree remove`. Remoção equivale a `git worktree prune` — zero risco.

A **branch local é preservada** nesse caso: o diretório já não existe, então não
há espaço a recuperar removendo-a, e ela pode conter o único ponteiro para
commits não publicados.

### `merged`
`git merge-base --is-ancestor <HEAD da worktree> <base>`. A base é, em ordem de
preferência: `origin/HEAD`, depois `origin/{main,master,develop,trunk}`, depois
o equivalente local.

**Limitação conhecida:** squash-merge e rebase-merge reescrevem os commits, então
o HEAD antigo *não* é ancestral da base e o critério não dispara. Nesses casos o
sinal que salva é `upstream-gone` (a plataforma apaga a branch remota ao mergear
a PR). Se o remoto não apaga branches, a worktree cairá em `stale` depois de
`staleDays` — por design, exige revisão humana.

### `upstream-gone`
`git for-each-ref --format='%(upstream:short)|%(upstream:track)'` retorna
`[gone]` quando a branch tem upstream configurado mas ele não existe mais. É a
assinatura de "PR mergeada e branch deletada no remoto".

Depende de `git fetch --prune` ter rodado. Sem fetch recente, o critério não
dispara — falso negativo, nunca falso positivo.

### `orphan-detached` / `no-unique-commits`
Worktree em HEAD detached, ou em uma branch que não tem nenhum commit além da
base. Agentes criam isso ao abrir worktree para inspeção e nunca commitar.

### `stale`
Último commit com idade `>= staleDays` (default 14). Nunca é pré-selecionado:
"antigo" não é o mesmo que "descartável".

### `dirty`
Qualquer saída de `git status --porcelain --untracked-files=normal`. Arquivos
não commitados **não são recuperáveis** pelo `undo.sh`. Por isso a worktree só
sai se o usuário digitar o id dela.

### `protected`
- **Worktree principal**: o checkout onde fica `.git/`. Removê-la quebraria o
  repositório.
- **Sessão atual**: resolvida via `git rev-parse --show-toplevel` no cwd do
  processo. Impede que o janitor apague o chão sob os próprios pés.
- **Locked**: `git worktree lock` é uma declaração explícita de intenção humana.
- **Glob `--protect`**: casado contra o caminho absoluto com `fnmatch`.

## Detecção de harness

O harness dono da worktree é inferido de um segmento do caminho:

| Segmento | Harness |
|---|---|
| `.claude` | Claude Code |
| `.codex` | Codex |
| `.agy` | Agy |
| `.antigravity` | Antigravity |
| `.gemini` | Gemini CLI |
| `.opencode` | OpenCode |
| `.cursor` | Cursor |
| `.aider` | Aider |
| `.windsurf` | Windsurf |
| `.continue` | Continue |

Caminho com segmento `worktrees`/`.worktrees` sem harness conhecido conta como
"agente (genérico)". Os demais contam como "humano". A detecção é informativa:
**não** altera a classificação de risco.

## Descoberta de repositórios

`os.walk` a partir de cada raiz, até `--depth` níveis, pulando artefatos de build
(`node_modules`, `.venv`, `dist`, `build`, `target`, `Pods`, `.gradle`, `vendor`,
`.next`, `DerivedData`, ...). Só diretórios com `.git` **como diretório** contam
como repositório principal — worktrees linkadas têm `.git` como *arquivo* e são
enumeradas pelo repositório pai.

A descida para em cada raiz de repositório encontrada. **Limitação:** repositórios
aninhados dentro de outro repositório não são descobertos; passe-os como `--root`
explícito.
