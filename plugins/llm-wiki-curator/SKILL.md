---
name: llm-wiki-curator
description: Maintains docs/ in the Karpathy-style LLM-wiki standard. Generates docs/llms.txt (flat machine-readable index conforming to llmstxt.org), validates broken links, enforces a minimum front-matter in new .md files (title, status, updated, related), groups orphan docs. Use when the user says "update docs index", "generate llms.txt", "audit docs", "organize wiki", "cure documentation", or after adding/renaming a file in docs/.
---

# llm-wiki-curator

Applies Karpathy's philosophy of LLM-first docs-as-code: flat, link-rich, no decorative prose, with predictable headers for indexing by agents.

## Mandatory Front-Matter Pattern

Every file in `docs/**/*.md` (except `adr/` and `llms.txt`) must start with:

```yaml
---
title: <short human title>
status: draft | active | deprecated | superseded-by:<path>
updated: YYYY-MM-DD
related: [<path1>, <path2>]
---
```

## Commands

### 1. Generate `docs/llms.txt`

```bash
bash .Codex/skills/llm-wiki-curator/scripts/build-index.sh
```

Output: `docs/llms.txt` in [llmstxt.org](https://llmstxt.org) format — project H1, short blockquote, sections by `docs/` subdirectory, each item `- [Title](relative-path): one-liner`.

### 2. Audit docs

```bash
bash .Codex/skills/llm-wiki-curator/scripts/audit.sh
```

Reports:
- files without front-matter
- broken markdown links (target does not exist)
- files not referenced by any other (orphans)
- `deprecated` status still linked from `active` docs

### 3. Promote doc to `active`

Edit front-matter `status: active` and run `build-index.sh` to republish.

## Karpathy Principles Applied

- **Flat > hierarchical**: maximum of 1-2 levels of subfolders. Flatten if possible.
- **Bi-directional links**: each doc lists `related:` to neighbors.
- **No decorative prose**: docs are code. Bullets > paragraphs.
- **Verifiable**: each feature doc ends with an `## Eval` section — how to confirm it works.
- **Recipe-first**: tutorials start with a minimum runnable baseline before optimizing.

## When NOT to use

- ADRs in `docs/adr/` — they use their own template (date + immutable decision).
- Root `CHANGELOG.md` — follows Keep-a-Changelog, out of scope.
