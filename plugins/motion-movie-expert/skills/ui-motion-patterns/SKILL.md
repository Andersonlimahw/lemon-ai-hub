---
name: ui-motion-patterns
description: Motion tokens, spring presets, and React/Next.js (motion/react) interaction patterns for product UI that appears in a video — rebuilding real product screens faithfully, animating them as seekable scenes, and keeping the live product's motion consistent with the film. Use when a motion video shows or recreates product UI; for web UI work with no video deliverable use design-expert instead.
---

# UI Motion Patterns

Two jobs: animate real product UI on the web, and rebuild product UI for video without redesigning
it. Both use the same tokens.

## 1. Tokens first

Define motion once and import it everywhere. No inline numbers in components.

```ts
// lib/motion-tokens.ts
export const motionTokens = {
  duration: { instant: 0.1, fast: 0.18, normal: 0.3, slow: 0.5, scene: 0.7 },
  easing: {
    standard: [0.2, 0, 0, 1],   // enter + move
    exit: [0.4, 0, 1, 1],       // leave
    emphasized: [0.3, 0, 0, 1],
  },
  distance: { nudge: 4, small: 8, medium: 16, large: 32 },
  stagger: 0.06,                // keep between 0.05 and 0.10
} as const;

export const springs = {
  press:   { type: "spring", stiffness: 600, damping: 38 },  // buttons, toggles
  snappy:  { type: "spring", stiffness: 420, damping: 34 },  // chips, menus
  gentle:  { type: "spring", stiffness: 260, damping: 27 },  // cards, panels
  layout:  { type: "spring", stiffness: 320, damping: 30 },  // reorder, resize
  camera:  { type: "spring", stiffness: 140, damping: 20 },  // big moves, video only
} as const;
```

With mass 1, damping ratio ζ = damping / (2·√stiffness): press 0.78, snappy 0.83, gentle 0.84,
layout 0.84, camera 0.85 — all inside the 0.75–0.90 band (overshoot ≤ ~6 %). Adjust per brand with
that formula, and keep this table the single source.

## 2. Accessibility and SSR

```tsx
"use client";
import { useReducedMotion } from "motion/react";

export function useSafeMotion() {
  const reduce = useReducedMotion();
  return {
    reduce,
    // reduced motion: drop transforms, keep short opacity changes (≤0.2 s)
    enter: reduce ? { opacity: 1 } : { opacity: 1, y: 0 },
    initial: reduce ? { opacity: 0 } : { opacity: 0, y: 8 },
    transition: reduce ? { duration: 0.2 } : undefined,
  };
}
```

- Use `initial={false}` for elements already visible on first paint to avoid hydration flashes.
- Animate `transform` and `opacity` only. Never animate `width`, `height`, `top`, `left`, or
  `box-shadow` in loops; use `layout` or scale instead.
- Low-end devices: shorten durations and skip decorative motion.

## 3. Patterns and their rules

| Pattern | Rule |
|---|---|
| Button press | `whileTap={{ scale: 0.96 }}` with `springs.press`; feedback within 100 ms |
| Conditional render | wrap in `AnimatePresence` with a stable `key`; every `initial` + `animate` gets an `exit` |
| Page / route transition | `AnimatePresence mode="wait"`: exit completes before enter |
| List stagger | `staggerChildren` 0.05–0.10 s; cap staggered items at ~8, the rest appear together |
| Reorder / resize | `layout` on small subtrees only (≲5 children); otherwise explicit `x`/`y` |
| Modal / sheet | focus trap, Escape closes, scroll lock, `role="dialog"`, `aria-modal="true"`, return focus |
| Toast | enters from the edge it lives on; auto-dismiss pauses on hover/focus |
| Number change | vertical roll: old value exits up with blur, new enters from below; `font-variant-numeric: tabular-nums` |
| Scroll reveal | `whileInView` with `viewport={{ once: true }}`; never re-animate on scroll-out |
| Loading → success | button compresses → spinner → check; keep the button's width stable |

## 4. Rebuilding product UI for video

- **Measure, do not guess.** Take tokens from the product source or computed styles: colors, radii,
  font family/weights/tracking, spacing, icon set and stroke. Sample colors from real screenshots
  and compare.
- **Hybrid default.** Real screenshot as context; rebuild only the elements that animate, pixel-aligned
  over it.
- **Never redesign** without explicit approval. No new colors, fonts, icons, or copy.
- **Capture clean.** Logged out or demo account, fictional data, no PII, no third-party brands
  unless the user owns them.
- **Seekable.** In video, drive every animated value from absolute time (`value = f(t)`), not from
  `motion/react` runtime state. Use `motion/react` for the live web, closed-form springs or GSAP
  timelines for rendered video.

When these patterns are used on a website rather than a video, run the `design-expert` verification
gate (keyboard, focus, reduced motion, performance) before shipping.
