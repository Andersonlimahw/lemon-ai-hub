---
name: llm-wiki-curator
description: Mantém docs/ no padrão LLM-wiki estilo Karpathy. Gera docs/llms.txt (índice flat machine-readable conforme llmstxt.org), valida links quebrados, força front-matter mínimo em novos .md (title, status, updated, related), agrupa docs órfãos. Use quando user disser "atualizar índice docs", "gerar llms.txt", "auditar docs", "organizar wiki", "curar documentação", ou após adicionar/renomear arquivo em docs/.
---

# llm-wiki-curator

Aplica filosofia Karpathy de docs-como-código LLM-first: flat, link-rich, sem prosa decorativa, com headers previsíveis para indexação por agentes.

## Padrão de front-matter obrigatório

Todo arquivo em `docs/**/*.md` (exceto `adr/` e `llms.txt`) deve começar com:

```yaml
---
title: <título humano curto>
status: draft | active | deprecated | superseded-by:<path>
updated: YYYY-MM-DD
related: [<path1>, <path2>]
---
```

## Comandos

### 1. Gerar `docs/llms.txt`

```bash
bash .Codex/skills/llm-wiki-curator/scripts/build-index.sh
```

Saída: `docs/llms.txt` no formato [llmstxt.org](https://llmstxt.org) — H1 do projeto, blockquote curta, seções por subpasta de `docs/`, cada item `- [Title](relative-path): one-liner`.

### 2. Auditar docs

```bash
bash .Codex/skills/llm-wiki-curator/scripts/audit.sh
```

Reporta:
- arquivos sem front-matter
- links markdown quebrados (alvo não existe)
- arquivos não referenciados por nenhum outro (órfãos)
- status `deprecated` ainda linkado a partir de docs `active`

### 3. Promover doc para `active`

Editar front-matter `status: active` e rodar `build-index.sh` para republicar.

## Princípios Karpathy aplicados

- **Flat > hierárquico**: 1-2 níveis de subpasta máximo. Achatar se possível.
- **Links bidirecionais**: cada doc lista `related:` para vizinhos.
- **Sem prosa decorativa**: docs são código. Bullets > parágrafos.
- **Verificável**: cada feature doc termina com seção `## Eval` — como confirmar que funciona.
- **Recipe-first**: tutoriais começam com baseline mínimo rodável antes de otimizar.

## Quando NÃO usar

- ADRs em `docs/adr/` — usam template próprio (data + decisão imutável).
- `CHANGELOG.md` raiz — segue Keep-a-Changelog, fora de escopo.
