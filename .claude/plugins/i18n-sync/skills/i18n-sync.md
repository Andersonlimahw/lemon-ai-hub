---
name: i18n-sync
description: Locale file synchronization and CI enforcement. Detects missing keys added to base locale, auto-stubs them in all other locales, blocks PRs with hardcoded strings, and generates a translation completeness badge. Use when onboarding a new locale or enforcing translation discipline in CI.
---

# i18n Sync Plugin

Keep all locales in sync. Zero missing keys in CI.

## Commands

```
/i18n-sync check           — compare all locales vs base locale
/i18n-sync stub            — add missing keys to all locales with [UNTRANSLATED] prefix
/i18n-sync clean           — remove orphaned keys from all locales
/i18n-sync ci-setup        — configure pre-commit + GitHub Actions check
/i18n-sync badge           — generate translation completeness badge
```

## CI Gate

Blocks merge if:
- New keys added to `en.json` without stubs in other locales
- Hardcoded string detected in `.tsx`/`.vue` files added in PR
- Any locale file is invalid JSON

```yaml
# .github/workflows/i18n.yml
- name: Check i18n completeness
  run: npx i18n-sync check --fail-on-missing
```

## Auto-Stub Example

New key added to `en.json`:
```json
{ "checkout.coupon.invalid": "Coupon code is not valid" }
```

Auto-stubbed in `pt-BR.json`:
```json
{ "checkout.coupon.invalid": "[UNTRANSLATED] Coupon code is not valid" }
```

Auto-stubbed in `es.json`:
```json
{ "checkout.coupon.invalid": "[UNTRANSLATED] Coupon code is not valid" }
```

## Pre-commit Hook

```bash
# Runs on every commit touching locale files
npx i18n-sync check --base en --locales pt-BR,es,fr,de
```

Pairs with `/i18n-audit` skill for comprehensive manual audits.
