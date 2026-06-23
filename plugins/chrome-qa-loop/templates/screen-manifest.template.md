# Screen manifest — `<your app>`

> Production base: `${TARGET_BASE_URL}`. Each screen names its **owner-doc** under `${OWNER_DOCS_ROOT}` — the explorer **must** read it before navigating, to ground expectations (no guessing).

| Order | Route | Purpose | Owner-doc (`${OWNER_DOCS_ROOT}...`) | Key scenarios | Risk lens |
|---|---|---|---|---|---|
| 1 | `/` | Landing / marketing, entry, CTA, auth start | `landing/index.md`, `auth/index.md` | Hero loads; CTAs route; OAuth start; no console errors | Product, QA |
| 2 | `/<core-feature>` | Differentiator / core flow | `<feature>/index.md` | Primary happy path; streaming/async renders; error & empty states; mobile layout | QA, Product |
| 3 | `/<dashboard>` | Main authenticated surface | `dashboard/index.md` | Data renders & reconciles; filters; date ranges; locale formatting; empty/loading | QA, Product |
| 4 | `/<secondary>` | Secondary surface | `<x>/index.md` | Smoke: load, render, no errors; paywall/authz correctness | QA, Security |
| 5 | `/<ai-or-settings>` | AI personalization / settings | `<x>/index.md` | Settings persist; no secrets leaked client-side; prompt-injection probe (benign) | Security, Product |

> **Run modes.** `guest` = public routes only (no auth). `guest-smoke` = first few public pages. `guest-full` = all public pages. `smoke` = first 1–3 routes (needs auth). `core` = first ~6 routes (needs auth, default). `full` = all routes (needs auth).
