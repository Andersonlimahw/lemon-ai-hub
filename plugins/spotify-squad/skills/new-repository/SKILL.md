---
name: new-repository
description: >
  New repository bootstrap workflow. Use when creating a new project
  repository from scratch, setting up all the foundational tooling,
  CI/CD, and team conventions.
---

# New Repository — Repository Bootstrap Workflow

You are the Repository Architect. You bootstrap new repositories with production-grade tooling, conventions, and automation from day one. Every new repo should be deployable, testable, and contributor-friendly within the first hour.

## Repository Bootstrap Pipeline

```
Structure → Git Config → Dev Environment → Code Quality → CI/CD
    │            │              │                │           │
    ▼            ▼              ▼                ▼           ▼
 Layout &    Branch rules   Docker +         Lint +       Build +
 Monorepo    PR templates   Devcontainer     Hooks        Deploy

    → Documentation → Security → Testing → Monitoring
           │              │          │          │
           ▼              ▼          ▼          ▼
        README +       Scanning   Framework   Error +
        CONTRIB        + CODEOWN  + Coverage   APM
```

## Phase 1: Repository Structure

### Monorepo vs Polyrepo Decision

```markdown
## Decision: Repository Strategy

| Factor | Monorepo | Polyrepo |
|--------|----------|----------|
| Team size < 10 | ✅ Preferred | ⚠️ Overhead |
| Team size > 30 | ⚠️ Complex tooling | ✅ Clear ownership |
| Shared code | ✅ Easy sharing | ❌ Package publishing |
| Independent deploys | ⚠️ Needs tooling | ✅ Natural |
| Code discoverability | ✅ Everything in one place | ❌ Scattered |
| CI/CD complexity | ⚠️ Affected-based builds | ✅ Simple pipelines |
| Onboarding | ✅ Single clone | ❌ Multiple repos |

**Recommendation**: [Monorepo / Polyrepo] because [rationale]
```

### Monorepo Directory Layout

```
project-root/
├── .github/                    # GitHub configuration
│   ├── workflows/              # CI/CD pipelines
│   │   ├── ci.yml
│   │   ├── deploy-staging.yml
│   │   └── deploy-production.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── CODEOWNERS
├── apps/                       # Deployable applications
│   ├── web/                    # Web application
│   ├── api/                    # Backend API
│   └── mobile/                 # Mobile application
├── packages/                   # Shared packages
│   ├── ui/                     # Shared UI components
│   ├── config/                 # Shared configurations
│   └── utils/                  # Shared utilities
├── infra/                      # Infrastructure as code
│   ├── terraform/
│   └── kubernetes/
├── docs/                       # Documentation
│   ├── architecture/
│   ├── adr/                    # Architecture Decision Records
│   └── runbooks/
├── scripts/                    # Development scripts
│   ├── setup.sh
│   └── seed-db.sh
├── .devcontainer/              # VS Code devcontainer
│   └── devcontainer.json
├── .env.example                # Environment variable template
├── .gitignore
├── .prettierrc
├── .eslintrc.js
├── biome.json                  # Alternative: Biome config
├── package.json                # Root package.json (workspace)
├── turbo.json                  # Turborepo config (if monorepo)
├── docker-compose.yml          # Local development services
├── Dockerfile                  # Production build
├── README.md
├── CONTRIBUTING.md
├── ARCHITECTURE.md
├── LICENSE
└── SECURITY.md
```

### Polyrepo Directory Layout

```
project-name/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── deploy.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
├── src/                        # Source code
│   ├── modules/                # Feature modules
│   │   ├── auth/
│   │   ├── users/
│   │   └── playlists/
│   ├── common/                 # Shared utilities
│   │   ├── middleware/
│   │   ├── guards/
│   │   └── utils/
│   ├── config/                 # Configuration
│   ├── database/               # DB migrations & seeds
│   │   ├── migrations/
│   │   └── seeds/
│   └── main.ts                 # Entry point
├── test/                       # Test files
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
├── docs/
├── scripts/
├── .devcontainer/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── docker-compose.yml
├── Dockerfile
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Phase 2: Git Configuration

### .gitignore Template

```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Build
dist/
build/
.next/
out/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.nyc_output/

# Logs
*.log
npm-debug.log*

# Caches
.turbo/
.cache/
.parcel-cache/

# Generated
*.generated.*
```

### Branch Protection Rules

```markdown
## Branch Protection: main

### Rules
- [x] Require pull request before merging
  - Required approvals: 1 (2 for critical paths)
  - Dismiss stale reviews on new pushes
  - Require review from CODEOWNERS
- [x] Require status checks to pass
  - Required: ci/build, ci/test, ci/lint, ci/typecheck
  - Require branches to be up to date
- [x] Require signed commits
- [x] Require linear history (squash or rebase)
- [x] Do not allow force pushes
- [x] Do not allow deletions

### Branch Naming Convention
| Type | Pattern | Example |
|------|---------|---------|
| Feature | feature/<ticket>-<description> | feature/SPOT-123-playlist-sharing |
| Bugfix | fix/<ticket>-<description> | fix/SPOT-456-playback-crash |
| Hotfix | hotfix/<ticket>-<description> | hotfix/SPOT-789-auth-bypass |
| Release | release/v<semver> | release/v2.1.0 |
| Chore | chore/<description> | chore/update-dependencies |
```

### PR Template

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->

## Description
<!-- What does this PR do? Why? -->

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] CI/CD
- [ ] Dependencies

## Changes
<!-- List key changes -->
-

## Testing
<!-- How was this tested? -->
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project conventions
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] No console.log or debug code
- [ ] No secrets or credentials committed
- [ ] Migration is reversible (if applicable)
- [ ] Feature flag added (if applicable)

## Screenshots/Recordings
<!-- If UI change, add before/after -->

## Related Issues
<!-- Closes #123 -->
```

### Commit Convention

```markdown
## Commit Format (Conventional Commits)

\`\`\`
<type>(<scope>): <description>

[optional body]

[optional footer]
\`\`\`

### Types
| Type | Usage | Triggers |
|------|-------|----------|
| feat | New feature | Minor version bump |
| fix | Bug fix | Patch version bump |
| docs | Documentation only | No release |
| style | Formatting (no code change) | No release |
| refactor | Code restructuring | No release |
| perf | Performance improvement | Patch version bump |
| test | Adding/fixing tests | No release |
| ci | CI/CD changes | No release |
| chore | Maintenance | No release |
| revert | Revert previous commit | Depends on reverted type |

### Breaking Changes
\`\`\`
feat(api)!: change authentication endpoint

BREAKING CHANGE: /auth/login now requires email instead of username
\`\`\`
```

---

## Phase 3: Development Environment

### Docker Compose Template

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: npm run dev

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  postgres_data:
```

### Devcontainer Template

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "Project Dev",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/app",
  "features": {
    "ghcr.io/devcontainers/features/node:1": { "version": "20" },
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "prisma.prisma",
        "bradlc.vscode-tailwindcss",
        "biomejs.biome"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
      }
    }
  },
  "postCreateCommand": "npm install && npm run db:migrate",
  "forwardPorts": [3000, 5432, 6379]
}
```

### Environment Variables Template

```bash
# .env.example — Copy to .env and fill in values

# ─── Application ───────────────────────────────
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000
API_URL=http://localhost:3000/api

# ─── Database ──────────────────────────────────
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app_dev

# ─── Redis ─────────────────────────────────────
REDIS_URL=redis://localhost:6379

# ─── Authentication ────────────────────────────
JWT_SECRET=CHANGE_ME_IN_PRODUCTION
JWT_EXPIRATION=15m
REFRESH_TOKEN_EXPIRATION=7d

# ─── External Services ────────────────────────
# STRIPE_SECRET_KEY=sk_test_...
# SENDGRID_API_KEY=SG...
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_REGION=us-east-1
# S3_BUCKET=

# ─── Monitoring ────────────────────────────────
# SENTRY_DSN=
# DATADOG_API_KEY=
# LOG_LEVEL=debug
```

---

## Phase 4: Code Quality

### ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  root: true,
  env: { node: true, es2022: true },
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: './tsconfig.json',
    ecmaVersion: 2022,
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint', 'import'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-type-checked',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'prettier', // Must be last
  ],
  rules: {
    // TypeScript
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/no-floating-promises': 'error',

    // Import
    'import/order': ['error', {
      groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
      'newlines-between': 'always',
      alphabetize: { order: 'asc' },
    }],
    'import/no-duplicates': 'error',

    // General
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'no-debugger': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
  },
  settings: {
    'import/resolver': { typescript: {} },
  },
};
```

### Biome Configuration (Alternative)

```jsonc
// biome.json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExcessiveCognitiveComplexity": { "level": "warn", "options": { "maxAllowedComplexity": 15 } }
      },
      "suspicious": {
        "noExplicitAny": "warn",
        "noConsoleLog": "warn"
      },
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "all",
      "semicolons": "always"
    }
  }
}
```

### Prettier Configuration

```jsonc
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "bracketSpacing": true,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### Pre-commit Hooks (Husky + lint-staged)

```jsonc
// package.json (partial)
{
  "scripts": {
    "prepare": "husky",
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit"
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged

# .husky/commit-msg
npx commitlint --edit $1
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'ci', 'chore', 'revert',
    ]],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100],
  },
};
```

---

## Phase 5: CI/CD Pipeline

### GitHub Actions CI Template

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npm run typecheck

  test:
    name: Test
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: app_test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run db:migrate
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/app_test
      - run: npm test -- --coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/app_test
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript-typescript
      - uses: github/codeql-action/analyze@v3
```

### Deploy Pipeline Template

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
      - name: Push to registry
        run: |
          echo "${{ secrets.REGISTRY_PASSWORD }}" | docker login -u "${{ secrets.REGISTRY_USER }}" --password-stdin
          docker tag app:${{ github.sha }} registry.example.com/app:staging
          docker push registry.example.com/app:staging
      - name: Deploy to staging
        run: |
          # kubectl, terraform, or platform-specific deploy

  deploy-production:
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: production
    needs: [deploy-staging]
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          # Production deployment steps
```

---

## Phase 6: Documentation

### README Template

```markdown
# Project Name

> One-line description of what this project does.

[![CI](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/org/repo/actions)
[![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)](./coverage)

## Quick Start

\`\`\`bash
# Clone
git clone https://github.com/org/repo.git
cd repo

# Setup
cp .env.example .env
docker compose up -d
npm install
npm run db:migrate
npm run db:seed

# Run
npm run dev        # http://localhost:3000
\`\`\`

## Scripts

| Command | Description |
|---------|------------|
| \`npm run dev\` | Start development server |
| \`npm run build\` | Build for production |
| \`npm run test\` | Run tests |
| \`npm run lint\` | Run linter |
| \`npm run typecheck\` | TypeScript type check |
| \`npm run db:migrate\` | Run database migrations |
| \`npm run db:seed\` | Seed database |

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for system design and decisions.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development workflow and conventions.

## License

[MIT](./LICENSE)
```

### CONTRIBUTING Template

```markdown
# Contributing

## Development Workflow

1. Create a branch from \`main\`: \`feature/SPOT-123-description\`
2. Make changes with conventional commits
3. Push and create a Pull Request
4. Address review feedback
5. Squash merge after approval

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

\`\`\`
feat(scope): add new feature
fix(scope): fix bug
docs: update README
\`\`\`

## Code Style

- TypeScript strict mode
- ESLint + Prettier (auto-formatted on save)
- Run \`npm run lint\` before committing

## Testing

- Write tests for all new features
- Maintain > 80% coverage
- Run \`npm test\` before pushing

## Pull Request

- Fill out the PR template completely
- Keep PRs small (< 400 lines ideally)
- One concern per PR
```

### ARCHITECTURE Template

```markdown
# Architecture

## System Overview

[High-level architecture diagram]

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | React + Next.js | SSR, file routing |
| Backend | Node.js + Express | Team expertise |
| Database | PostgreSQL | Relational data |
| Cache | Redis | Session, rate limiting |
| Queue | BullMQ | Background jobs |
| Infra | AWS / GCP | [Choice rationale] |

## Architecture Decision Records

See [docs/adr/](./docs/adr/) for all architecture decisions.

### ADR Template
\`\`\`markdown
# ADR-001: [Title]

## Status: [Proposed | Accepted | Deprecated | Superseded]
## Date: YYYY-MM-DD

## Context
[What is the issue we're facing?]

## Decision
[What is the change we're proposing?]

## Consequences
[What are the trade-offs?]
\`\`\`
```

---

## Phase 7: Security

### Dependency Scanning

```yaml
# Automated via CI (see ci.yml security job)
# Manual check:
npm audit
npx better-npm-audit audit

# Automated dependency updates (Renovate or Dependabot)
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
    groups:
      production:
        patterns: ["*"]
        exclude-patterns: ["@types/*", "eslint*", "prettier*"]
      dev:
        patterns: ["@types/*", "eslint*", "prettier*"]
```

### Secret Detection

```yaml
# .github/workflows/secrets-scan.yml (or use pre-commit)
# Pre-commit hook with gitleaks:
# brew install gitleaks
# gitleaks detect --source . --verbose
```

```toml
# .gitleaks.toml
[allowlist]
  description = "Global allowlist"
  paths = [
    '''\.env\.example''',
    '''package-lock\.json''',
  ]
```

### CODEOWNERS

```
# .github/CODEOWNERS

# Default owners
* @team-lead

# Backend
/apps/api/ @backend-team
/packages/utils/ @backend-team

# Frontend
/apps/web/ @frontend-team
/packages/ui/ @frontend-team

# Infrastructure
/infra/ @devops-team
/.github/workflows/ @devops-team
/Dockerfile @devops-team
/docker-compose.yml @devops-team

# Security-sensitive
/apps/api/src/auth/ @security-team @team-lead
/.env.example @team-lead
```

### SECURITY.md Template

```markdown
# Security Policy

## Reporting Vulnerabilities

Please report security vulnerabilities to security@example.com.
Do NOT create public GitHub issues for security vulnerabilities.

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | ✅        |
| < 1.0   | ❌        |

## Security Practices

- Dependencies are scanned weekly (Dependabot)
- Code is scanned on every PR (CodeQL)
- Secrets are detected pre-commit (gitleaks)
- All commits to main require review
```

---

## Phase 8: Testing Setup

### Test Framework Configuration

```typescript
// jest.config.ts (or vitest.config.ts)
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
      exclude: [
        'node_modules/',
        'test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/types/',
      ],
    },
    include: ['src/**/*.test.ts', 'test/**/*.test.ts'],
    setupFiles: ['./test/setup.ts'],
  },
});
```

### Test Structure Convention

```
test/
├── setup.ts                    # Global test setup
├── fixtures/                   # Shared test data
│   ├── users.ts
│   └── playlists.ts
├── helpers/                    # Test utilities
│   ├── db.ts                   # Database test helpers
│   ├── auth.ts                 # Auth test helpers
│   └── factory.ts              # Test data factories
├── unit/                       # Unit tests (mirror src/)
│   └── modules/
│       └── playlists/
│           └── service.test.ts
├── integration/                # Integration tests
│   └── api/
│       └── playlists.test.ts
└── e2e/                        # End-to-end tests
    └── flows/
        └── create-playlist.test.ts
```

### Coverage Thresholds

```markdown
| Metric | Minimum | Target | Critical Path |
|--------|---------|--------|--------------|
| Lines | 80% | 90% | 95% |
| Branches | 80% | 85% | 90% |
| Functions | 80% | 90% | 95% |
| Statements | 80% | 90% | 95% |
```

---

## Phase 9: Monitoring

### Error Tracking (Sentry)

```typescript
// src/config/sentry.ts
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
  integrations: [
    Sentry.httpIntegration(),
    Sentry.expressIntegration(),
    Sentry.postgresIntegration(),
  ],
  beforeSend(event) {
    // Scrub PII
    if (event.user) {
      delete event.user.email;
      delete event.user.ip_address;
    }
    return event;
  },
});
```

### Logging Configuration

```typescript
// src/config/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
  redact: ['req.headers.authorization', 'req.body.password', 'user.email'],
  serializers: {
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res,
    err: pino.stdSerializers.err,
  },
  // Standard fields
  base: {
    service: process.env.SERVICE_NAME || 'api',
    version: process.env.APP_VERSION,
  },
});
```

### Health Check Endpoint

```typescript
// src/health.ts
app.get('/health', async (req, res) => {
  const checks = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION,
    uptime: process.uptime(),
    checks: {
      database: await checkDatabase(),
      redis: await checkRedis(),
      memory: {
        rss: process.memoryUsage().rss,
        heapUsed: process.memoryUsage().heapUsed,
      },
    },
  };

  const allHealthy = Object.values(checks.checks)
    .every(c => typeof c === 'object' && 'status' in c ? c.status === 'ok' : true);

  res.status(allHealthy ? 200 : 503).json(checks);
});
```

### APM Dashboard Template

```markdown
## Monitoring Dashboard

### Service Health
- Uptime percentage (target: 99.9%)
- Health check status
- Active instances

### Performance
- Request latency (p50, p95, p99)
- Throughput (requests/second)
- Error rate (%)
- Apdex score

### Resources
- CPU usage
- Memory usage
- Database connections (active/idle/max)
- Redis memory usage

### Business Metrics
- Active users
- Key feature usage
- Conversion rates

### Alerts
| Alert | Condition | Severity | Notification |
|-------|-----------|----------|-------------|
| High error rate | > 1% for 5min | Critical | PagerDuty |
| High latency | p99 > 1s for 5min | Warning | Slack |
| Low throughput | < 50% baseline for 10min | Critical | PagerDuty |
| High memory | > 85% for 10min | Warning | Slack |
| DB connections | > 80% pool for 5min | Warning | Slack |
```

---

## Bootstrap Checklist

When creating a new repository, verify all items:

### Structure
- [ ] Directory layout created
- [ ] Monorepo/polyrepo decision documented

### Git
- [ ] .gitignore configured
- [ ] Branch protection rules set
- [ ] PR template created
- [ ] Issue templates created
- [ ] Commit convention configured (commitlint)

### Development
- [ ] Docker compose for local services
- [ ] .env.example with all variables documented
- [ ] Devcontainer configuration
- [ ] Setup script that works from clean clone

### Code Quality
- [ ] Linter configured (ESLint or Biome)
- [ ] Formatter configured (Prettier or Biome)
- [ ] Pre-commit hooks (Husky + lint-staged)
- [ ] TypeScript strict mode enabled

### CI/CD
- [ ] CI pipeline (lint, test, build, security)
- [ ] Deploy pipeline (staging, production)
- [ ] Status badges in README

### Documentation
- [ ] README with quick start
- [ ] CONTRIBUTING with workflow
- [ ] ARCHITECTURE with tech stack
- [ ] SECURITY with reporting process
- [ ] LICENSE file

### Security
- [ ] Dependency scanning in CI
- [ ] Secret detection (gitleaks)
- [ ] CODEOWNERS file
- [ ] Dependabot/Renovate configured

### Testing
- [ ] Test framework configured
- [ ] Coverage thresholds set
- [ ] Test directory structure created
- [ ] Test helpers and factories ready

### Monitoring
- [ ] Error tracking (Sentry) initialized
- [ ] Structured logging configured
- [ ] Health check endpoint
- [ ] APM dashboard template
