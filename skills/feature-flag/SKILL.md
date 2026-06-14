---
name: feature-flag
description: Feature flag implementation, management, and cleanup. Handles flag creation, gradual rollout strategies, A/B testing wiring, stale flag detection, and safe flag removal. Supports LaunchDarkly, Unleash, GrowthBook, Statsig, custom env-var flags, and database-backed toggles. Use when adding gated features, rolling out gradually, or cleaning up old flags.
---

# Feature Flag

Implement, manage, and retire feature flags safely across any stack.

## Quick Start

```
/feature-flag add <name>           — scaffold a new flag
/feature-flag rollout <name> 10%   — set gradual rollout percentage
/feature-flag audit                — find all flags + flag staleness
/feature-flag remove <name>        — safe removal with dead-code cleanup
/feature-flag list                 — show all flags and current state
```

## Flag Types

| Type | When to Use |
|------|-------------|
| **Kill switch** | Turn off broken feature instantly in prod |
| **Release gate** | Ship code dark, enable when ready |
| **Gradual rollout** | 1% → 10% → 50% → 100% |
| **A/B experiment** | Split traffic, measure variant metrics |
| **User segment** | Beta users, internal users, region-specific |

## Workflow

### Add New Flag
Claude will:
1. Name-check (format: `snake_case`, category prefix: `feat_`, `exp_`, `ops_`)
2. Create flag definition in chosen provider or local config
3. Scaffold flag-gated code with proper `if/else` fallback
4. Add cleanup TODO with target removal date
5. Add to flag registry / CLAUDE.md

### Gradual Rollout
```
/feature-flag rollout feat_new_checkout 10%
/feature-flag rollout feat_new_checkout 50%
/feature-flag rollout feat_new_checkout 100%
/feature-flag promote feat_new_checkout    — remove flag, keep code
```

### Audit Stale Flags
Finds flags that:
- Are 100% enabled and have no A/B experiment
- Were last modified > 90 days ago
- Control code paths never hit in production

## Code Patterns

### Environment variable (simplest)
```typescript
// flag-registry.ts
export const FLAGS = {
  NEW_CHECKOUT: process.env.FLAG_NEW_CHECKOUT === 'true',
  DARK_MODE_V2: process.env.FLAG_DARK_MODE_V2 === 'true',
} as const

// usage
if (FLAGS.NEW_CHECKOUT) {
  return <NewCheckout />
}
return <OldCheckout />
```

### LaunchDarkly
```typescript
import { LDClient } from '@launchdarkly/node-server-sdk'

const flag = await client.variation('feat-new-checkout', user, false)
if (flag) { ... }
```

### GrowthBook
```typescript
const gb = new GrowthBook({ features })
if (gb.isOn('feat-new-checkout')) { ... }
```

### Database-backed (custom)
```sql
-- flags table
CREATE TABLE feature_flags (
  key        TEXT PRIMARY KEY,
  enabled    BOOLEAN DEFAULT false,
  rollout_pct INT DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

## Safe Flag Removal Checklist

```
[ ] Flag is 100% enabled in all environments
[ ] No A/B experiment data still being collected
[ ] Metrics confirmed (conversion, error rate, latency)
[ ] Remove flag check from code (keep the new path)
[ ] Delete flag from provider / config
[ ] Delete tests that mock the disabled path
[ ] Update changelog
```

## Naming Conventions

```
feat_<feature>          — user-facing feature gate
exp_<hypothesis>        — A/B experiment
ops_<operation>         — operational kill switch
tmp_<migration>         — temporary migration flag (max 30 days)
```

## Anti-Patterns

- Nesting flags inside flags (creates truth table hell)
- Flags with no owner or target removal date
- Testing only the enabled path (always test both)
- Keeping flags after 100% rollout > 2 weeks
