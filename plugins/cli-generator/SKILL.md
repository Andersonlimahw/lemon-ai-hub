---
name: cli-generator
description: >
  Generate a complete, production-ready CLI in Bun from a SPEC (OpenAPI,
  JSON Schema, markdown contract, or natural-language description). Outputs
  a runnable binary with commander-style arg parsing, shell autocomplete,
  --help generation, man page, and token-aware output formatting. Use when
  you need to turn an API spec or feature description into a working CLI
  in minutes.
---

# CLI Generator

SPEC → Bun CLI. Production-ready. Autocomplete, --help, token-aware output.

## Quick Start

```
/cli-generator from-spec <spec-file>          — OpenAPI / JSON Schema → CLI
/cli-generator from-api <url>                 — live API → CLI (probe endpoints)
/cli-generator from-description "<text>"      — natural language → CLI
/cli-generator validate <cli-dir>             — check generated CLI against spec
```

## Input Sources

| Source | Example | Best for |
|--------|---------|----------|
| OpenAPI 3.x | `openapi.yaml`, `swagger.json` | REST APIs |
| JSON Schema | `schema.json` | Data tools, validators |
| GraphQL SDL | `schema.graphql` | GraphQL APIs |
| Markdown spec | `SPEC.md` | Feature-driven design |
| NL description | `"CLI to manage user accounts with CRUD"` | Rapid prototyping |
| Live API URL | `https://api.example.com` | Reverse-engineering |

## Output — What You Get

```
my-cli/
├── package.json          # bin entry, dependencies
├── tsconfig.json         # Bun-optimized TS config
├── src/
│   ├── index.ts          # entry point, commander setup
│   ├── commands/         # one file per subcommand
│   │   ├── list.ts
│   │   ├── get.ts
│   │   ├── create.ts
│   │   ├── update.ts
│   │   └── delete.ts
│   ├── lib/
│   │   ├── client.ts     # typed API client (generated)
│   │   ├── format.ts     # output formatters (json, table, yaml)
│   │   └── config.ts     # env vars, config file handling
│   └── types.ts          # generated from spec
├── completions/
│   ├── bash.sh
│   ├── zsh.sh
│   └── fish.sh
├── man/
│   └── my-cli.1          # man page
├── test/
│   └── commands.test.ts  # bun test suite
├── README.md             # usage docs
└── Makefile              # build, install, test
```

## Workflow — Spec to CLI

Claude will:

### Phase 1: Parse
1. Read the input (OpenAPI, JSON Schema, markdown, or NL)
2. Extract: commands, subcommands, flags, args, types
3. Infer missing details (descriptions, defaults, validation rules)
4. Confirm the command tree with user before generating

### Phase 2: Generate
1. Scaffold project structure with `package.json` + `tsconfig.json`
2. Generate typed API client from spec (if OpenAPI/GraphQL)
3. Generate one file per subcommand with commander/args
4. Wire up autocomplete (bash/zsh/fish)
5. Generate man page
6. Generate test suite with `bun test`

### Phase 3: Verify
1. `bun run src/index.ts --help` — validates CLI boots
2. `bun test` — all generated tests pass
3. `bun run build` — compiles without errors
4. Output: ready to `npm install -g` or `bun link`

## Generated Code Example

Input — OpenAPI snippet:
```yaml
paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      parameters:
        - name: role
          in: query
          schema:
            type: string
            enum: [admin, user, guest]
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
    post:
      operationId: createUser
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [name, email]
              properties:
                name:
                  type: string
                email:
                  type: string
                  format: email
                role:
                  type: string
                  enum: [admin, user, guest]
                  default: user
  /users/{id}:
    get:
      operationId: getUser
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
```

Output — `src/commands/list.ts`:
```typescript
import { Command } from 'commander'
import { client } from '../lib/client'
import { formatOutput } from '../lib/format'
import type { User } from '../types'

export const listUsersCommand = new Command('list')
  .description('List all users')
  .option('--role <role>', 'Filter by role (admin, user, guest)')
  .option('--limit <number>', 'Max results', '20')
  .option('--offset <number>', 'Pagination offset', '0')
  .action(async (opts) => {
    const { data, error } = await client.GET('/users', {
      params: {
        query: {
          role: opts.role,
          limit: Number(opts.limit),
          offset: Number(opts.offset),
        },
      },
    })

    if (error) {
      console.error(`Error: ${error.message}`)
      process.exit(1)
    }

    formatOutput<User[]>(data, {
      columns: ['id', 'name', 'email', 'role'],
      format: opts.format ?? 'table',
    })
  })
```

## Bundled Runtime — Token-Aware Output

Every generated CLI includes `src/lib/format.ts` with three modes:

| Flag | Mode | Use case |
|------|------|----------|
| `--format json` | Structured | Piped to jq, scripts |
| `--format table` | Human-readable | Terminal viewing |
| `--format tokens` | Token-optimized | AI harness consumption |

`--format tokens` strips whitespace, deduplicates, and outputs only essential fields — minimizing context window consumption when a CLI is invoked by an AI agent.

## Validation

```
/cli-generator validate ./my-cli
```

Checks:
- ✓ All spec endpoints have corresponding commands
- ✓ All required params are enforced
- ✓ Types match between spec and generated code
- ✓ Autocomplete covers all flags
- ✓ Tests exist for every command
- ✓ Build succeeds
- ✓ --help output is complete

## Frameworks Used

- **Runtime**: [Bun](https://bun.sh) — fast startup, native TS, built-in test runner
- **Arg parsing**: `commander` (most mature) or `citty` (lighter, Bun-native)
- **API client**: generated `openapi-fetch` wrapper (typed) or `fetch` with Zod validation
- **Output**: custom `--format tokens` mode for AI harness consumption

## Design Decisions

1. **One file per command** — keeps files small, AI-navigable
2. **Typed client from spec** — no manual fetch calls, full autocomplete
3. **Token-aware by default** — every CLI ships with `--format tokens`
4. **Tests generated alongside code** — not an afterthought
5. **Shell completions built-in** — no extra install step

## Example Session

```
User: /cli-generator from-spec ./openapi.yaml
Claude:
  ✓ Parsed OpenAPI 3.1 — 12 endpoints, 5 schemas
  Command tree:
    users list [--role] [--limit] [--offset]
    users get <id>
    users create --name --email [--role]
    users update <id> [--name] [--email] [--role]
    users delete <id>
  Confirm? (y/n)

User: y
Claude:
  ✓ Scaffolded project (8 files)
  ✓ Generated typed client
  ✓ Generated 5 command files
  ✓ Generated autocomplete (bash/zsh/fish)
  ✓ Generated man page
  ✓ Generated 12 tests
  ✓ Build passing
  ✓ CLI boots: my-cli --help

  Done. Try:
    cd my-cli && bun link && my-cli users list --format tokens
```
