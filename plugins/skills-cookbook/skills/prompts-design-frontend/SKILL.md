---
name: prompts-design-frontend
description: Ready-to-paste prompts for UI and frontend design — intentional visual direction, design-system data, accessibility gates, screenshot-to-code, and redesigns. One aesthetic at a time.
---

# Prompts — Design & Frontend

Recipes for UI with intent. Non-negotiable rule of this track: **one aesthetic at a time** — `minimalist-ui`, `industrial-brutalist-ui`, `high-end-visual-design`, and `emil-design-eng` are mutually exclusive art directions; mixing two produces generic or incoherent UI.

## R1 — New screen with direction + data + compliance

**Skills:** `frontend-design` + `ui-ux-pro-max` + `a11y-audit`
**When:** building new UI that shouldn't look like a template default.

```text
Build <screen/component> in <stack> for <product/persona>.
Intentional visual direction with frontend-design (no template
default); palette, typography, and stack guidelines via
ui-ux-pro-max; close with a11y-audit at WCAG 2.1 AA.
Success: rendering component + documented tokens (colors, fonts,
spacing) + a11y audit with no CRITICAL findings.
```

## R2 — Specific aesthetic (pick ONE)

**Skills:** `minimalist-ui` OR `industrial-brutalist-ui` OR `high-end-visual-design` OR `emil-design-eng`
**When:** the project calls for a strong, defined art direction.

```text
Apply aesthetic <ONE: minimalist-ui | industrial-brutalist-ui |
high-end-visual-design | emil-design-eng> to screen <screen> in
<stack>. Follow the direction strictly: typography, density,
color, and motion coherent with the chosen aesthetic — nothing
borrowed from another.
Success: the screen is identifiable as the chosen aesthetic in a
screenshot, and a 5-trait checklist for the aesthetic passes.
```

## R3 — Screenshot → code

**Skills:** `image-to-code` + `ui-ux-pro-max`
**When:** you have a visual reference (screenshot, mockup) and want a faithful component.

```text
Attached: <screenshot/mockup>. Generate with image-to-code the
component in <stack>, faithful to the layout. Map colors and
fonts to design-system tokens via ui-ux-pro-max — no loose
hardcoded values.
Success: minimal visual diff vs. the reference + zero colors/fonts
outside the tokens.
```

## R4 — Redesign without breaking content

**Skills:** `redesign-existing-projects` + `web-design-guidelines` + `a11y-audit`
**When:** an existing page/product needs a new look while preserving information and flow.

```text
Redesign <page/flow> with redesign-existing-projects, preserving
information architecture and content. Validate against
web-design-guidelines and close with a11y-audit (AA).
Success: side-by-side before/after + guidelines checklist passing
+ no content or navigation regression.
```

## See also

- `design-taste-frontend` — good-taste baseline when you have NOT yet chosen an aesthetic (don't combine with a specific aesthetic).
- `imagegen-frontend-web` / `imagegen-frontend-mobile` — generate visual reference before coding.
- `a11y-guardian` — after the one-shot audit: continuous a11y gate in CI.
