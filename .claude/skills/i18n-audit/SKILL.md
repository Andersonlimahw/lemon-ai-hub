---
name: i18n-audit
description: Internationalization completeness audit and key synchronization. Finds missing translation keys, hardcoded strings, pluralization bugs, RTL layout issues, date/number formatting gaps, and untranslated copy. Supports i18next, react-intl, vue-i18n, next-intl, and custom JSON locale files. Use when adding a new language, auditing translation completeness, or debugging locale mismatch errors.
---

# i18n Audit

Find every missing translation, hardcoded string, and locale gap before your users do.

## Quick Start

```
/i18n-audit                    — full audit across all locales
/i18n-audit --lang pt-BR       — audit single locale
/i18n-audit --missing          — show only missing keys
/i18n-audit --hardcoded        — scan codebase for hardcoded strings
/i18n-audit --fix              — add placeholder keys for missing translations
/i18n-audit --new-lang es      — scaffold a new language from base locale
```

## What Gets Audited

### Key Completeness
- Keys present in base locale (`en`) but missing in target locales
- Keys present in target locales but removed from base (orphaned keys)
- Nested key depth mismatches
- Empty string values (untranslated placeholder)

### Code Quality
- Hardcoded strings in JSX/TSX/Vue templates
- Missing plural forms (`one` / `other` / `few` / `many` / `zero`)
- Missing interpolation variables (`{name}` in key but `{user}` in code)
- Date formatting using `new Date().toLocaleDateString()` without locale param

### Layout Issues
- Fixed-width containers that break with German/Japanese text expansion
- Missing `dir="rtl"` for Arabic / Hebrew locales
- Icons or arrows that assume LTR direction

### Number / Currency / Date
- Hardcoded `$` currency symbols
- Hardcoded date formats (`MM/DD/YYYY`)
- Missing `Intl.NumberFormat` / `Intl.DateTimeFormat` locale params

## Output Format

```
i18n AUDIT REPORT — 2026-06-14
================================
Base locale: en  |  Target locales: pt-BR, es, fr, de, ja

COMPLETENESS
  pt-BR  96/100  ✅  8 missing keys
  es     88/100  ⚠️  24 missing keys
  fr     71/100  ❌  58 missing keys (stale, needs attention)
  de     100/100 ✅  complete
  ja     45/100  ❌  110 missing keys

MISSING KEYS (es)
  checkout.summary.discount_label
  checkout.summary.free_shipping
  profile.settings.notification_email
  ... (21 more)

HARDCODED STRINGS DETECTED
  src/components/Header.tsx:14  → "Welcome back, "
  src/pages/checkout.tsx:87    → "Free shipping on orders over $50"
  src/utils/date.ts:23         → new Date().toLocaleDateString() ← no locale

PLURAL ISSUES
  pt-BR → cart.items_count: missing 'other' form
  es    → notification.unread: uses 'plural' (nonstandard), should be 'other'

ORPHANED KEYS (in pt-BR but not in en — likely stale)
  auth.login_with_facebook  ← Facebook login removed 3 months ago
  checkout.cod_payment      ← COD feature removed
```

## Common Fixes

### Add missing plural forms (i18next)
```json
{
  "cart": {
    "items_count_one": "{{count}} item",
    "items_count_other": "{{count}} items"
  }
}
```

### Currency with Intl
```typescript
// ❌
`$${price.toFixed(2)}`

// ✅
new Intl.NumberFormat(locale, {
  style: 'currency',
  currency: currencyCode,
}).format(price)
```

### Date with locale
```typescript
// ❌
new Date(ts).toLocaleDateString()

// ✅
new Intl.DateTimeFormat(locale, { dateStyle: 'medium' }).format(new Date(ts))
```

### RTL support
```tsx
// globals.css
[dir="rtl"] .card-icon { transform: scaleX(-1); }

// layout
<html lang={locale} dir={rtlLocales.includes(locale) ? 'rtl' : 'ltr'}>
```

## New Language Scaffold

Running `/i18n-audit --new-lang es` will:
1. Copy base locale JSON structure
2. Mark all values as `[NEEDS TRANSLATION] Original: ...`
3. Add new lang to i18n config
4. Add new lang to CI translation coverage check
