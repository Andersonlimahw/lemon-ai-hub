---
name: code-smell
description: Code smell detection and remediation. Identifies long methods, god classes, feature envy, primitive obsession, shotgun surgery, dead code, magic numbers, and other structural anti-patterns. Goes beyond linters — understands semantic coupling and design intent. Use when code is hard to change, PRs are consistently risky, or technical debt is growing faster than features.
---

# Code Smell

Find structural problems before they calcify into permanent pain.

## Quick Start

```
/code-smell                     — full codebase smell analysis
/code-smell --file src/user.ts  — analyze single file
/code-smell --category god-class — hunt specific smell type
/code-smell --fix               — apply safe refactors (extract method, rename)
/code-smell --rank              — sort files by smell density
```

## Smell Catalog

### Bloaters (things that grew too big)
| Smell | Signal | Fix |
|-------|--------|-----|
| **Long Method** | >20 lines, multiple levels of abstraction | Extract Method |
| **Large Class** | >300 lines, too many responsibilities | Extract Class / SRP |
| **Long Parameter List** | >4 params | Introduce Parameter Object |
| **Data Clumps** | Same 3+ vars always appear together | Extract Class |
| **Primitive Obsession** | `string` for email/money/status | Value Object |

### OO Abusers
| Smell | Signal | Fix |
|-------|--------|-----|
| **Switch Statements** | Switch/if-chain on type | Polymorphism |
| **Temporary Field** | Field only set in one method | Extract Class |
| **Refused Bequest** | Child ignores most of parent | Replace Inheritance with Delegation |
| **Alternative Classes** | Two classes do the same thing | Merge |

### Change Preventers
| Smell | Signal | Fix |
|-------|--------|-----|
| **Divergent Change** | Changing feature X always touches Class Y | Split class |
| **Shotgun Surgery** | One change → 8 files | Move Method / Inline Class |
| **Parallel Inheritance** | Adding subclass A requires subclass B | Merge hierarchies |

### Dispensables (things to delete)
| Smell | Signal | Fix |
|-------|--------|-----|
| **Dead Code** | Unreachable / never called | Delete |
| **Speculative Generality** | `AbstractFactory` for one use case | Simplify |
| **Lazy Class** | Class does almost nothing | Inline Class |
| **Duplicate Code** | Copy-paste across files | Extract + reuse |

### Couplers
| Smell | Signal | Fix |
|-------|--------|-----|
| **Feature Envy** | Method uses other class's data more than own | Move Method |
| **Inappropriate Intimacy** | Two classes read each other's privates | Move / Extract |
| **Message Chains** | `a.b().c().d().e()` | Introduce delegate method |
| **Middle Man** | Class delegates everything to another | Inline Class |

## Output Format

```
CODE SMELL ANALYSIS — 2026-06-14
===================================
Files analyzed: 147  |  Smell density: 2.3 smells/100 lines (HIGH)

CRITICAL
  [C1] src/services/UserService.ts — GOD CLASS (847 lines, 23 methods)
       Handles: auth, profile, billing, notifications, admin, analytics
       → Extract: AuthService, BillingService, NotificationService
       Estimated effort: 2 days | Risk: HIGH (many callers)

  [C2] src/api/checkout.ts:145 — LONG METHOD (94 lines, 7 abstraction levels)
       → Extract: validateCart(), applyDiscounts(), chargePayment(), sendConfirmation()

HIGH
  [H1] src/models/Product.ts:12 — PRIMITIVE OBSESSION
       price: number (no currency, no precision)
       → type Money = { amount: number; currency: Currency }

  [H2] src/components/AdminPanel.tsx — FEATURE ENVY
       References user.subscription.plan.features 14 times
       → Move canAccessFeature(featureId) to User or Subscription model

MEDIUM
  [M1] src/utils/helpers.ts — DEAD CODE (3 exported functions, 0 callers)
       formatLegacyDate(), parseOldSKU(), migrateV1User()
       → Safe to delete (confirmed by grep + git log)

  [M2] src/api/ — DUPLICATE CODE
       validateEmail() defined in auth.ts, users.ts, and checkout.ts
       → Extract to src/utils/validation.ts

LOW
  [L1] 12 occurrences of magic numbers (HTTP status codes, timeout values)
       → Extract to src/constants/http.ts and src/config/timeouts.ts
```

## Safe Refactor Patterns

### Extract Method
```typescript
// ❌ 60-line method
async processOrder(cart: Cart, user: User) {
  // validate cart
  if (!cart.items.length) throw new Error('Empty cart')
  const inventory = await this.checkInventory(cart.items)
  // ... 50 more lines
}

// ✅ decomposed
async processOrder(cart: Cart, user: User) {
  await this.validateCart(cart)
  const payment = await this.chargePayment(cart, user)
  await this.fulfillOrder(cart, payment)
  await this.sendConfirmation(user, payment)
}
```

### Introduce Value Object
```typescript
// ❌ primitive obsession
function charge(amount: number, currency: string) { ... }

// ✅ value object
class Money {
  constructor(readonly amount: number, readonly currency: 'USD' | 'BRL' | 'EUR') {}
  plus(other: Money): Money {
    if (this.currency !== other.currency) throw new Error('Currency mismatch')
    return new Money(this.amount + other.amount, this.currency)
  }
}
```

### Replace Switch with Map
```typescript
// ❌ switch smells
function getDiscount(tier: string): number {
  switch (tier) {
    case 'bronze': return 0.05
    case 'silver': return 0.10
    case 'gold': return 0.20
    default: return 0
  }
}

// ✅ data-driven
const DISCOUNTS: Record<string, number> = { bronze: 0.05, silver: 0.10, gold: 0.20 }
const getDiscount = (tier: string) => DISCOUNTS[tier] ?? 0
```
