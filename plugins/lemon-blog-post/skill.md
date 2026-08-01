---
name: "lemon-blog-post"
description: "Skill para criar e publicar blog posts no Lemon Blog via MCP"
---
# lemon-blog-post

**Skill para criar e publicar blog posts no Lemon Blog via MCP**

## Quando usar

User pedir:
- "cria blog post sobre X"
- "lemon-blog-post new"
- "post no blog sobre"

## Fluxo

1. **Pesquisa profunda** (se necessário)
   - Spawn subagents para research paralela
   - Calibrar effort/modelo por subtarefa

2. **Geração de conteúdo**
   - seguir estilo Karpathy (minimal → incremental)
   - código executável
   - intuição antes de formalismo

3. **Review pedagógico**
   - karpathy-pedagogy-reviewer agent
   - verificar clareza, build-up, exemplos

4. **SEO e otimização**
   - article-seo-optimizer
   - gerar thumbnail prompt
   - cross-links internos

5. **Publicação**
   - lemon-admin-mcp: post_create()
   - status: draft
   - tags, categoria, metadata

## Subagents calibration

| Tarefa | Effort | Modelo |
|--------|--------|--------|
| Research benchmarks | medium | glm-5.2 |
| Análise custos | low | glm-4.5-air |
| Comparação modelos | high | glm-5.2[1m] |
| Geração exemplos | medium | glm-5.2 |
| Review pedagógico | high | glm-5.2[1m] |
| SEO | low | glm-4.5-air |

## MCP tools

- `mcp__lemon-admin__post_create` — criar draft
- `mcp__lemon-admin__post_update` — atualizar
- `mcp__lemon-admin__post_publish` — publicar

## Output

Arquivo markdown em `articles/` + draft no Lemon.
