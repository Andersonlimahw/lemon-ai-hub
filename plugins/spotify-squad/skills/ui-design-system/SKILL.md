---
name: ui-design-system
description: >
  UI design system creation and management. Use for design tokens, component
  specs, color palettes, typography scales, spacing systems, and visual
  consistency audits.
---

# UI Design System Skill

You are a design systems architect. You create, maintain, and evolve design systems that ensure visual consistency, developer efficiency, and accessible user experiences across all product surfaces.

---

## 1. Design Tokens

Design tokens are the atomic values of a design system — the single source of truth for colors, typography, spacing, elevation, and motion.

### 1.1 Token Naming Convention

Use a three-tier naming hierarchy:

```
[category]-[property]-[variant]-[state]
```

**Examples:**
```
color-background-primary
color-text-secondary
spacing-padding-md
elevation-shadow-lg
motion-duration-fast
```

### 1.2 Token Categories

| Category | Properties | Examples |
|----------|-----------|----------|
| Color | background, text, border, icon | `color-bg-primary`, `color-text-error` |
| Typography | family, size, weight, line-height, letter-spacing | `type-size-lg`, `type-weight-bold` |
| Spacing | padding, margin, gap | `spacing-md`, `spacing-section` |
| Elevation | shadow, z-index | `elevation-card`, `elevation-modal` |
| Motion | duration, easing, delay | `motion-duration-normal`, `motion-ease-out` |
| Border | width, radius, style | `border-radius-md`, `border-width-thin` |
| Opacity | transparency levels | `opacity-disabled`, `opacity-overlay` |

### 1.3 Token Format (JSON)
```json
{
  "color": {
    "primary": {
      "50": { "value": "#EEF2FF", "type": "color" },
      "100": { "value": "#E0E7FF", "type": "color" },
      "500": { "value": "#6366F1", "type": "color" },
      "600": { "value": "#4F46E5", "type": "color" },
      "900": { "value": "#312E81", "type": "color" }
    },
    "semantic": {
      "success": { "value": "{color.green.500}", "type": "color" },
      "warning": { "value": "{color.amber.500}", "type": "color" },
      "error": { "value": "{color.red.500}", "type": "color" },
      "info": { "value": "{color.blue.500}", "type": "color" }
    }
  },
  "spacing": {
    "xs": { "value": "4px", "type": "spacing" },
    "sm": { "value": "8px", "type": "spacing" },
    "md": { "value": "16px", "type": "spacing" },
    "lg": { "value": "24px", "type": "spacing" },
    "xl": { "value": "32px", "type": "spacing" },
    "2xl": { "value": "48px", "type": "spacing" },
    "3xl": { "value": "64px", "type": "spacing" }
  }
}
```

### 1.4 Token Transformation Pipeline
```
Design Tool (Figma) → Token JSON → Style Dictionary → Platform Output
                                                       ├── CSS Variables
                                                       ├── Tailwind Config
                                                       ├── iOS (Swift)
                                                       ├── Android (XML/Compose)
                                                       └── React Native
```

---

## 2. Color System

### 2.1 Color Categories

**Primary Palette:** Brand colors used for primary actions, active states, and focus indicators.

**Neutral Palette:** Grays used for text, backgrounds, borders, and dividers.

**Semantic Palette:** Functional colors that convey meaning.

| Semantic | Use Case | Light Mode | Dark Mode |
|----------|----------|------------|-----------|
| Success | Confirmations, positive states | `#16A34A` | `#4ADE80` |
| Warning | Caution, attention needed | `#D97706` | `#FBBF24` |
| Error | Errors, destructive actions | `#DC2626` | `#F87171` |
| Info | Informational, neutral alerts | `#2563EB` | `#60A5FA` |

**Surface Palette:** Background layers that create visual depth.

| Surface | Use Case | Light Mode | Dark Mode |
|---------|----------|------------|-----------|
| Background | Page background | `#FFFFFF` | `#0F172A` |
| Surface | Cards, containers | `#F8FAFC` | `#1E293B` |
| Elevated | Modals, popovers | `#FFFFFF` | `#334155` |
| Overlay | Backdrops | `rgba(0,0,0,0.5)` | `rgba(0,0,0,0.7)` |

### 2.2 Color Scale Generation

Generate a 10-step scale (50–900) for each base color:

```
50  — Lightest tint (backgrounds, subtle fills)
100 — Light tint (hover states, badges)
200 — Light (borders, dividers)
300 — Medium light (inactive icons)
400 — Medium (placeholder text)
500 — Base (primary usage)
600 — Medium dark (hover on primary)
700 — Dark (active/pressed states)
800 — Darker (high-contrast text)
900 — Darkest (headings on light backgrounds)
```

### 2.3 Accessibility — Contrast Requirements

| Context | WCAG Level | Minimum Ratio |
|---------|-----------|---------------|
| Body text (normal) | AA | 4.5:1 |
| Large text (18px+ or 14px bold) | AA | 3:1 |
| Body text (normal) | AAA | 7:1 |
| UI components & graphics | AA | 3:1 |
| Focus indicators | AA | 3:1 |
| Decorative elements | — | No requirement |

**Always verify:** Use tools like Stark, WebAIM Contrast Checker, or `chrome-devtools` accessibility audit.

---

## 3. Typography Scale

### 3.1 Modular Scale

Use a modular scale with a ratio (recommended: 1.250 Major Third or 1.200 Minor Third).

**Base size:** 16px (1rem)

| Token | Size | Weight | Line Height | Letter Spacing | Use Case |
|-------|------|--------|-------------|----------------|----------|
| `display-2xl` | 72px / 4.5rem | 800 | 1.0 | -0.02em | Hero headlines |
| `display-xl` | 60px / 3.75rem | 800 | 1.1 | -0.02em | Page titles |
| `display-lg` | 48px / 3rem | 700 | 1.1 | -0.01em | Section headers |
| `heading-xl` | 36px / 2.25rem | 700 | 1.2 | -0.01em | H1 |
| `heading-lg` | 30px / 1.875rem | 600 | 1.3 | 0 | H2 |
| `heading-md` | 24px / 1.5rem | 600 | 1.3 | 0 | H3 |
| `heading-sm` | 20px / 1.25rem | 600 | 1.4 | 0 | H4 |
| `body-lg` | 18px / 1.125rem | 400 | 1.6 | 0 | Lead paragraphs |
| `body-md` | 16px / 1rem | 400 | 1.5 | 0 | Body text |
| `body-sm` | 14px / 0.875rem | 400 | 1.5 | 0.01em | Secondary text |
| `caption` | 12px / 0.75rem | 500 | 1.4 | 0.02em | Captions, labels |
| `overline` | 11px / 0.6875rem | 700 | 1.4 | 0.08em | Overlines, tags |

### 3.2 Font Stack
```css
/* Primary — UI and body text */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
  'Helvetica Neue', Arial, sans-serif;

/* Mono — Code and technical content */
--font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;

/* Display — Headlines (optional, for personality) */
--font-display: 'Cal Sans', 'Inter', sans-serif;
```

### 3.3 Responsive Typography

Use `clamp()` for fluid scaling:
```css
--type-display-2xl: clamp(2.5rem, 5vw + 1rem, 4.5rem);
--type-heading-xl: clamp(1.75rem, 3vw + 0.5rem, 2.25rem);
--type-body-md: clamp(0.9375rem, 1vw + 0.5rem, 1rem);
```

---

## 4. Spacing System

### 4.1 Base Unit: 4px Grid

All spacing values are multiples of 4px for visual consistency.

| Token | Value | CSS Variable | Common Use |
|-------|-------|-------------|------------|
| `0` | 0px | `--space-0` | Reset |
| `px` | 1px | `--space-px` | Borders, hairlines |
| `0.5` | 2px | `--space-0-5` | Minimal gaps |
| `1` | 4px | `--space-1` | Tight padding |
| `2` | 8px | `--space-2` | Icon gaps, inline spacing |
| `3` | 12px | `--space-3` | Compact padding |
| `4` | 16px | `--space-4` | Standard padding |
| `5` | 20px | `--space-5` | Card padding |
| `6` | 24px | `--space-6` | Section gap |
| `8` | 32px | `--space-8` | Component gap |
| `10` | 40px | `--space-10` | Large gap |
| `12` | 48px | `--space-12` | Section spacing |
| `16` | 64px | `--space-16` | Page section |
| `20` | 80px | `--space-20` | Major section |
| `24` | 96px | `--space-24` | Page margin |

### 4.2 Spacing Principles

1. **Consistency:** Use tokens — never arbitrary pixel values.
2. **Proximity:** Related elements are closer together; unrelated elements are farther apart.
3. **Hierarchy:** More spacing = more visual importance/separation.
4. **Density Modes:**
   - **Compact:** Reduce by one step (e.g., `md` → `sm`)
   - **Default:** Standard spacing
   - **Comfortable:** Increase by one step (e.g., `md` → `lg`)

---

## 5. Elevation System

### 5.1 Shadow Scale

| Token | Box-Shadow | Use Case |
|-------|-----------|----------|
| `elevation-none` | `none` | Flat elements |
| `elevation-xs` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle cards |
| `elevation-sm` | `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)` | Cards, buttons |
| `elevation-md` | `0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)` | Dropdowns |
| `elevation-lg` | `0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)` | Modals |
| `elevation-xl` | `0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)` | Popovers |
| `elevation-2xl` | `0 25px 50px rgba(0,0,0,0.25)` | Full-screen overlays |

### 5.2 Z-Index Scale

| Token | Value | Use Case |
|-------|-------|----------|
| `z-base` | 0 | Default stacking |
| `z-raised` | 10 | Sticky elements |
| `z-dropdown` | 100 | Dropdowns, popovers |
| `z-sticky` | 200 | Sticky headers |
| `z-overlay` | 300 | Backdrop overlays |
| `z-modal` | 400 | Modals, dialogs |
| `z-toast` | 500 | Toast notifications |
| `z-tooltip` | 600 | Tooltips |
| `z-max` | 9999 | System-level (debug) |

---

## 6. Motion & Animation Guidelines

### 6.1 Duration Scale

| Token | Value | Use Case |
|-------|-------|----------|
| `instant` | 0ms | Immediate state change |
| `fastest` | 50ms | Micro-interactions (checkboxes) |
| `fast` | 100ms | Button press, icon change |
| `normal` | 200ms | Standard transitions |
| `slow` | 300ms | Panel slides, modals |
| `slower` | 400ms | Complex animations |
| `slowest` | 500ms | Page transitions |

### 6.2 Easing Curves

| Token | Value | Use Case |
|-------|-------|----------|
| `ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Elements exiting |
| `ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Elements entering |
| `ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Elements moving |
| `spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful bounces |

### 6.3 Motion Principles

1. **Purposeful:** Animation must communicate meaning (feedback, spatial relationships, state change).
2. **Fast:** Keep durations under 400ms — users shouldn't wait for animations.
3. **Natural:** Follow physical metaphors — objects accelerate and decelerate.
4. **Accessible:** Respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 7. Dark Mode Implementation

### 7.1 Strategy

Use **semantic tokens** that map to different values per theme — never hardcode colors.

```css
/* Light theme (default) */
:root {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8FAFC;
  --color-text-primary: #0F172A;
  --color-text-secondary: #475569;
  --color-border-default: #E2E8F0;
}

/* Dark theme */
[data-theme="dark"] {
  --color-bg-primary: #0F172A;
  --color-bg-secondary: #1E293B;
  --color-text-primary: #F1F5F9;
  --color-text-secondary: #94A3B8;
  --color-border-default: #334155;
}
```

### 7.2 Dark Mode Rules

1. **Don't invert.** Dark mode is not `filter: invert()`. Design intentionally.
2. **Reduce contrast.** Use off-white text (`#F1F5F9`) not pure white (`#FFFFFF`).
3. **Reduce saturation.** Saturated colors on dark backgrounds cause eye strain.
4. **Elevate with lightness.** Higher surfaces = lighter backgrounds (not shadows).
5. **Test independently.** Dark mode is a first-class citizen — not an afterthought.
6. **Handle images.** Add subtle borders or backgrounds behind transparent images.

---

## 8. Component States

Every interactive component must define these states:

| State | Visual Cue | Behavior |
|-------|-----------|----------|
| **Default** | Base appearance | Resting state |
| **Hover** | Subtle background/color shift | Mouse enters target area |
| **Focus** | Visible focus ring (2px, offset) | Keyboard navigation |
| **Active/Pressed** | Darker shade, scale down | Mouse down / touch press |
| **Disabled** | Reduced opacity (0.5), no pointer | Non-interactive, `aria-disabled` |
| **Loading** | Spinner or skeleton, disabled interaction | Async operation in progress |
| **Error** | Red border, error icon, message | Validation failure |
| **Success** | Green accent, check icon | Validation pass / operation complete |
| **Selected** | Filled/highlighted state | Active selection in a group |
| **Read-only** | Subtle background, no border | Viewable but not editable |

### Focus Ring Standard
```css
:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
  border-radius: var(--border-radius-sm);
}
```

---

## 9. Component Specification Format

### Component Spec Template
```markdown
## Component: [Name]

**Status:** [Draft | In Review | Approved | Deprecated]
**Version:** [1.0.0]
**Last Updated:** [Date]
**Owner:** [Name]

### Description
[What this component does and when to use it]

### Anatomy
[Diagram or list of sub-elements]
1. Container
2. Label
3. Icon (optional)
4. Helper text (optional)

### Variants
| Variant | Description | Use Case |
|---------|-------------|----------|
| Primary | Filled, high emphasis | Main CTA |
| Secondary | Outlined, medium emphasis | Secondary actions |
| Ghost | Text-only, low emphasis | Tertiary actions |

### Props / API
| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'ghost'` | `'primary'` | No | Visual variant |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | No | Component size |
| `disabled` | `boolean` | `false` | No | Disables interaction |
| `loading` | `boolean` | `false` | No | Shows loading state |

### Tokens Used
- `color-bg-primary` — Container background
- `color-text-on-primary` — Label text
- `spacing-3` — Horizontal padding
- `border-radius-md` — Corner radius
- `elevation-sm` — Drop shadow

### States
[Reference the component states table above with component-specific details]

### Accessibility
- **Role:** `button`
- **Keyboard:** `Enter` / `Space` to activate, `Tab` to focus
- **ARIA:** `aria-disabled`, `aria-busy` (when loading)
- **Contrast:** Label text meets 4.5:1 against container

### Do / Don't
| ✅ Do | ❌ Don't |
|------|---------|
| Use for primary actions | Use multiple primary buttons in one view |
| Keep labels concise (2–4 words) | Use generic labels like "Click Here" |
| Pair with a secondary button | Stack more than 3 buttons together |

### Code Example
[Framework-specific implementation snippet]
```

---

## 10. Handoff Documentation Format

### Design-to-Dev Handoff Checklist
```markdown
## Handoff: [Feature / Component]

**Designer:** [Name]
**Date:** [Date]
**Figma Link:** [URL]

### Specs Provided
- [ ] All screen states (empty, loading, populated, error)
- [ ] Responsive breakpoints (mobile, tablet, desktop)
- [ ] Dark mode variants
- [ ] Component states (default, hover, active, disabled, focus, error)
- [ ] Spacing and layout specs (using design tokens)
- [ ] Typography specs (using type scale tokens)
- [ ] Color specs (using color tokens, not hex values)
- [ ] Animation/transition specs (duration, easing)
- [ ] Interaction notes (hover behaviors, click areas, gestures)
- [ ] Accessibility annotations (focus order, ARIA roles, alt text)
- [ ] Edge cases (long text, missing data, permissions)
- [ ] Copy/microcopy (finalized, approved)

### Assets
- [ ] Icons exported (SVG, optimized)
- [ ] Images/illustrations (with alt text)
- [ ] Fonts (licensed, hosted)

### Notes for Engineering
[Anything unusual, known trade-offs, or implementation preferences]
```

---

## Quality Standards

1. **Token-first.** Never use raw values — always reference design tokens.
2. **Accessible by default.** Every component must meet WCAG 2.1 AA.
3. **Responsive.** Every component must work across mobile, tablet, and desktop.
4. **Dark mode.** Every component must support light and dark themes.
5. **Documented.** Every component must have a spec before development begins.
6. **Versioned.** Use semver for breaking changes, additions, and patches.
7. **Auditable.** Run periodic visual consistency audits against the token system.
8. **Platform-agnostic tokens.** Tokens must transform to any target platform.
