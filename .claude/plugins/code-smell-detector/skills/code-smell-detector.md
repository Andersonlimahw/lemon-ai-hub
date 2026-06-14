---
name: code-smell-detector
description: PR-level code smell gating and trend tracking. Detects new smells introduced in a PR, blocks merge if smell density exceeds threshold, tracks file-level smell trends over time, and generates weekly maintainability reports. Use when enforcing code quality standards in CI or monitoring technical debt accumulation.
---

# Code Smell Detector Plugin

Quality gates on every PR. Trend tracking over time.

## Commands

```
/code-smell-detector setup       — configure CI quality gate
/code-smell-detector pr          — analyze smells introduced in current PR
/code-smell-detector trend       — show smell density trend (last 30 days)
/code-smell-detector hotspots    — files with worst smell density
/code-smell-detector report      — weekly maintainability report
```

## PR Gate

Blocks merge if PR introduces:
- New god class (>300 lines, >10 methods)
- Method longer than 50 lines
- Duplication of >15 lines found elsewhere in codebase
- >3 new magic numbers

```
CODE SMELL PR CHECK — PR #247
================================
⚠️ 2 new smells introduced (non-blocking, warning)
❌ 1 critical smell introduced (BLOCKING)

  [BLOCK] src/services/PaymentService.ts — GOD CLASS
          File grew from 180 → 520 lines in this PR
          Added 8 new methods across 4 different concerns
          → Break into: PaymentGatewayService, RefundService, InvoiceService

  [WARN] src/utils/checkout.ts:45 — method too long (78 lines)
  [WARN] src/utils/checkout.ts:12 — magic number 86400 (seconds/day?)
         → const SECONDS_PER_DAY = 86_400
```

## Trend Report

```
SMELL TREND — last 30 days
============================
Smell density: 2.4 → 2.1 smells/100 lines ✅ (improving)

HOTSPOT FILES (by smell density)
  src/services/UserService.ts    4.8/100  ↑ worsening
  src/api/checkout.ts            3.2/100  → stable
  src/components/AdminPanel.tsx  2.9/100  ↓ improving
```

## Weekly Report

Generated every Monday:
- Overall smell density vs last week
- Top 5 files added/removed from hotspot list
- Recommended refactors ranked by impact
- Team velocity correlation (high smell density = slower feature delivery)

Pairs with `/code-smell` skill for deep interactive analysis.
