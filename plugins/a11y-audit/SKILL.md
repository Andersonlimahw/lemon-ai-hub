---
name: a11y-audit
description: WCAG 2.1 AA/AAA accessibility audit for web components, pages, and apps. Detects contrast failures, missing ARIA labels, keyboard trap issues, focus order problems, and screen-reader gotchas. Use when user wants to audit accessibility, fix a11y warnings, prepare for compliance review, or validate UI against WCAG standards.
---

# Accessibility Audit (a11y)

WCAG 2.1 AA/AAA audit — find and fix accessibility issues before they block users or compliance.

## Quick Start

```
/a11y-audit                    — full page audit (reads current UI files)
/a11y-audit --component Button — audit single component
/a11y-audit --wcag AAA         — strict AAA audit
/a11y-audit --fix              — audit + auto-apply safe fixes
/a11y-audit --report           — generate HTML accessibility report
```

## What Gets Audited

### 1. Perceivable
- **1.1.1** Non-text content: all `<img>`, `<svg>`, `<canvas>` have meaningful `alt` / `aria-label`
- **1.3.1** Info and relationships: semantic HTML structure (headings, lists, tables)
- **1.4.3** Contrast ratio: text ≥ 4.5:1 (normal) or ≥ 3:1 (large text / UI components)
- **1.4.4** Resize text: layout survives 200% browser zoom

### 2. Operable
- **2.1.1** Keyboard accessible: all interactive elements reachable via Tab / Enter / Space
- **2.1.2** No keyboard trap: Esc always escapes modals, dialogs, and popovers
- **2.4.3** Focus order: Tab sequence follows visual reading order
- **2.4.7** Focus visible: focus ring visible on all interactive elements

### 3. Understandable
- **3.1.1** Language of page: `<html lang="...">` present and correct
- **3.3.1** Error identification: form errors describe what went wrong + how to fix
- **3.3.2** Labels or instructions: all inputs have `<label>` or `aria-labelledby`

### 4. Robust
- **4.1.2** Name, role, value: custom components expose correct ARIA roles and states
- **4.1.3** Status messages: toasts and alerts use `role="alert"` or `aria-live`

## Workflow

Claude will:
1. Scan component files for a11y violations (static analysis)
2. Check color variables against contrast ratio thresholds
3. Validate ARIA role/state usage
4. Check keyboard interaction patterns
5. Produce severity-ranked findings (CRITICAL / HIGH / MEDIUM / LOW)
6. With `--fix`: apply non-breaking fixes (add `alt=""`, `aria-label`, `lang`, focus styles)

## Output Format

```
A11Y AUDIT REPORT — 2026-06-14
================================
SCORE: 68/100   WCAG 2.1 AA

CRITICAL (blocks WCAG compliance)
  [C1] src/Button.tsx:12 — Interactive element has no accessible name
       → Add aria-label="Close dialog" or visible text content
  [C2] src/Card.tsx:8  — Contrast ratio 2.1:1 (required: 4.5:1)
       → Change text from #9ca3af → #6b7280 (ratio 4.6:1)

HIGH (fails WCAG AA)
  [H1] src/Modal.tsx:45 — No focus trap in modal
       → Use focus-trap-react or implement manual Tab/Shift+Tab containment
  [H2] src/Form.tsx:23  — Input has no associated label
       → Add <label htmlFor="email"> or aria-labelledby

MEDIUM
  [M1] src/Nav.tsx:5  — Missing skip-to-content link
       → Add <a href="#main" className="skip-link">Skip to content</a>
```

## Common Fixes

### Missing alt text
```tsx
// ❌
<img src="/hero.png" />
// ✅ decorative
<img src="/hero.png" alt="" />
// ✅ meaningful
<img src="/avatar.png" alt="Profile photo of Jane Doe" />
```

### Focus visible
```css
/* ❌ never do this */
:focus { outline: none; }
/* ✅ */
:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
```

### ARIA live regions
```tsx
// ❌ toast appears but screen readers don't announce
<Toast>{message}</Toast>
// ✅
<div role="alert" aria-live="polite">{message}</div>
```

## Tools Referenced

- axe-core (static analysis basis)
- WCAG 2.1 guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Color contrast: APCA algorithm for large text
