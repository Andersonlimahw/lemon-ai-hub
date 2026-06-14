---
name: bundle-analyzer
description: JavaScript/TypeScript bundle size analysis, tree-shaking audit, and code splitting recommendations. Identifies heavy dependencies, duplicate packages, unused imports, and suggests dynamic imports and lazy loading. Use when bundle is too large, Lighthouse score is low, or user wants to optimize web app loading performance.
---

# Bundle Analyzer

Cut your JS bundle. Faster page loads, better Core Web Vitals.

## Quick Start

```
/bundle-analyzer                  — analyze current project bundle
/bundle-analyzer --why lodash     — trace why a dep is included
/bundle-analyzer --alternatives   — find lighter alternatives to heavy deps
/bundle-analyzer --budget 200kb   — check against size budget
/bundle-analyzer --diff           — compare bundle size before/after change
```

## What Gets Analyzed

- **Total bundle size** (gzipped vs raw)
- **Chunk composition** (which routes include what)
- **Duplicate packages** (same lib at different versions)
- **Side-effect imports** (prevents tree-shaking)
- **Dynamic import opportunities** (code-split candidates)
- **Unused exports** (dead exports still in bundle)
- **Heavy dependencies** (sorted by size contribution)

## Workflow

Claude will:
1. Run `npx vite-bundle-visualizer` / `npx @next/bundle-analyzer` / `npx webpack-bundle-analyzer`
2. Parse stats JSON
3. List top 20 largest modules
4. Identify duplicate packages (e.g., lodash + lodash-es)
5. Flag non-tree-shakeable side-effect imports
6. Detect unneeded full library imports (`import _ from 'lodash'`)
7. Recommend: dynamic imports, lighter alternatives, CDN externals

## Output Format

```
BUNDLE ANALYSIS — 2026-06-14
==============================
Total:  1.24 MB raw  |  342 KB gzip
Budget: 200 KB gzip  ❌ (over by 142 KB)

TOP MODULES BY SIZE
  moment.js          94 KB  ← replace with date-fns (tree-shakeable)
  lodash             72 KB  ← import specific functions, not full bundle
  @mui/icons-material 68 KB ← only 3 icons used; import individually
  react-pdf          55 KB  ← load dynamically (only used in /reports)

DUPLICATE PACKAGES
  ⚠ react@18.2.0 + react@17.0.2 (from old-dep peer requirement)
  ⚠ axios@0.27 + axios@1.4 (from two different SDKs)

CODE SPLITTING OPPORTUNITIES
  /admin dashboard — 180 KB (never shown to non-admins)
  PDF generator    — 55 KB (used only on /reports route)
  Charts           — 44 KB (used only on /analytics route)

QUICK WINS (estimated savings: 210 KB gzip)
  1. Replace moment.js → date-fns               → -61 KB
  2. Use individual MUI icon imports             → -62 KB
  3. Dynamic import for react-pdf               → -38 KB (deferred)
  4. Deduplicate lodash versions                → -49 KB
```

## Common Fixes

### Heavy library → lighter alternative

| Replace | With | Savings |
|---------|------|---------|
| `moment` | `date-fns` or `dayjs` | ~90 KB |
| `lodash` | Native ES6 methods | ~70 KB |
| `axios` | `ky` or native `fetch` | ~40 KB |
| `@mui/icons` (full) | Individual icon imports | ~60 KB |
| `chart.js` | `uplot` or `lightweight-charts` | ~100 KB |

### Dynamic import (code splitting)
```typescript
// ❌ always in bundle
import { PDFViewer } from 'react-pdf'

// ✅ only loaded when needed
const PDFViewer = dynamic(() => import('react-pdf').then(m => m.PDFViewer), {
  loading: () => <Spinner />,
  ssr: false,
})
```

### Tree-shakeable import
```typescript
// ❌ full lodash bundle
import _ from 'lodash'
const sorted = _.sortBy(arr, 'name')

// ✅ only imports sortBy
import sortBy from 'lodash/sortBy'
const sorted = sortBy(arr, 'name')

// ✅✅ native (zero bundle cost)
const sorted = [...arr].sort((a, b) => a.name.localeCompare(b.name))
```

## Size Budgets (reference)

| Page Type | Target (gzip) | Max (gzip) |
|-----------|---------------|------------|
| Landing page | <50 KB | 100 KB |
| App shell | <100 KB | 200 KB |
| Feature page | <50 KB incremental | 100 KB |
| Admin/internal | <300 KB | 500 KB |
