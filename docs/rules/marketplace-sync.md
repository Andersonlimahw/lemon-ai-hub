---
title: Plugin ↔ Marketplace Sync (MANDATORY)
status: active
updated: 2026-06-15
related: [docs/cli-marketplace.md, docs/architecture.md, AGENTS.md]
---

# Rule: Every plugin MUST be registered in `marketplace.json`

**Why:** PR #8 added the `cli-generator` and `cli-wrapper` plugins under `plugins/`
but did **not** update `.claude-plugin/marketplace.json`. The plugins existed on
disk yet were invisible to the marketplace — they could not be discovered or
installed. This rule exists so that mismatch never happens again.

## The invariant

The set of directories in `plugins/` MUST equal the set of entries in
`.claude-plugin/marketplace.json` → `plugins[]`. No orphans on either side.

```
count(plugins/*/)  ==  count(marketplace.json .plugins[])
```

## When you add, rename, or remove a plugin

Whenever you touch `plugins/` you MUST, in the **same** change/PR:

1. **Add** — create the plugin dir AND append a matching `plugins[]` entry in
   `.claude-plugin/marketplace.json` (alphabetical order by `name`). Copy
   `name`, `description`, `version`, `license`, and `keywords` from the
   plugin's own `plugin.json` so they stay consistent.
2. **Rename** — update both the directory name and the `name` + `source` fields.
3. **Remove** — delete the dir AND its `plugins[]` entry.

## How to verify before committing

```bash
# Plugin dirs missing from the marketplace (must print nothing):
comm -23 \
  <(ls -1 plugins/ | sort) \
  <(grep -oE '"\./plugins/[^"]+"' .claude-plugin/marketplace.json \
      | sed -E 's#.*/plugins/([^"]+)"#\1#' | sort)

# Counts must match:
echo "dirs:     $(ls -1d plugins/*/ | wc -l)"
echo "registry: $(grep -c '"source": "./plugins/' .claude-plugin/marketplace.json)"
```

If `comm` prints any name, that plugin is unregistered — fix `marketplace.json`
before merging.
