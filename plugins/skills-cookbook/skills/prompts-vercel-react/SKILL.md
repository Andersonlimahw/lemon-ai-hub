---
name: prompts-vercel-react
description: Ready-to-paste prompts for the Vercel/React family — React and Next.js best-practice audits, performance optimization, composition refactors, view transitions, React Native/Expo, and deploys.
---

# Prompts — Vercel & React

Recipes for the `vercel-*` family: audit, optimize, compose, animate, and deploy React/Next.js and React Native apps.

## R1 — Best-practice + performance audit

**Skills:** `vercel-react-best-practices` + `vercel-optimize` + `bundle-analyzer`
**When:** a slow React/Next app, a low Lighthouse score, or inherited code with no standard.

```text
Audit <app/directory> with vercel-react-best-practices (component
patterns, data fetching, rendering strategy) and vercel-optimize
(Core Web Vitals, caching, images/fonts). Run bundle-analyzer for
heavy dependencies and code splitting.
Success: a single list prioritized by measured impact
(LCP/CLS/bundle kB), each item with a proposed diff; top 3 applied
and re-measured.
```

## R2 — Composition refactor

**Skills:** `vercel-composition-patterns`
**When:** prop-drilling, god components, or duplicated logic across trees.

```text
Refactor <component/tree> with vercel-composition-patterns:
eliminate prop-drilling and god components using composition
(children, slots, compound components) instead of new props.
Identical behavior — no new feature.
Success: before/after tree documented; existing tests green with
no changes; no new prop crossing >2 levels.
```

## R3 — View transitions

**Skills:** `vercel-react-view-transitions`
**When:** navigation/state needs a fluid transition without layout cost.

```text
Add view transitions on <pages/elements> with
vercel-react-view-transitions: page transition on routes <routes>
and element morph for <element> between screens.
Success: transitions running in supported browsers with a clean
fallback; zero measured CLS/INP regression.
```

## R4 — Performant React Native / Expo

**Skills:** `vercel-react-native-skills`
**When:** lists jank, animations at 30fps, or native API access in Expo/RN.

```text
Optimize <screen/list> of the RN/Expo app with
vercel-react-native-skills: correct virtualization for list
<list>, animations on the UI thread, and native access via
<module>.
Success: FPS measured before/after on the target screen; smooth
scroll with <N> items, no frame drops; no JS bridge in the hot
path.
```

## R5 — Deploy with correct envs and tokens

**Skills:** `deploy-to-vercel` + `vercel-cli-with-tokens`
**When:** publishing preview/production without leaking a secret or breaking env.

```text
Deploy <app> to Vercel with deploy-to-vercel using
vercel-cli-with-tokens for token-based auth (no interactive
login). Check env vars for <environments> before deploying.
Success: preview URL live + env checklist confirmed; no secret in
a log or commit.
```

## See also

- `frontend-design` + `ui-ux-pro-max` — the visual layer (track [prompts-design-frontend](../prompts-design-frontend/SKILL.md)).
- `webapp-testing` / `chrome-qa-loop` — validate the result in-browser.
- `bundle-watch` — after the one-shot fix: continuous size gate in CI.
