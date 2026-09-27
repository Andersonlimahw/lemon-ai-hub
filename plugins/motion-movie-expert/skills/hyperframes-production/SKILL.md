---
name: hyperframes-production
description: Build and render a deterministic video composition — HyperFrames (HTML + GSAP) by default, or a custom seek(t) + Playwright + FFmpeg pipeline. Covers project setup, composition contract, timeline rules, creative direction for frames, lint/check/snapshot, preview, and local render. Use when implementing an approved storyboard as code.
---

# HyperFrames Production

Implements an approved storyboard. If there is no storyboard, stop and run `motion-storyboard`.

## Choose the renderer

| Situation | Renderer |
|---|---|
| Default for new work; HTML/CSS/GSAP skills; registry blocks wanted | **HyperFrames** (`npx hyperframes …`) |
| The project already uses Remotion | stay on **Remotion**; the same determinism rules apply |
| A product repo already has its own studio (`seek(t)` + Playwright + FFmpeg) | **use that studio**; do not introduce a second one |
| Pure edit of existing footage | skip this skill → `video-edit-qc` |

Installing the HyperFrames CLI or adding registry blocks (`npx hyperframes add …`) installs third-party
code: confirm with the user first and pin the version in `package.json`. Do not run self-update
commands for skills (`npx hyperframes skills update`, `npx skills add …`) on your own.

## Composition contract (HyperFrames)

- **Standalone root**: `<div data-composition-id="main" data-width="1920" data-height="1080"
  data-duration="24">` directly in `<body>`, sized `width/height: 100%` — never hardcode pixel size
  on the root. **Sub-compositions** (loaded via `data-composition-src`) wrap their root in
  `<template>` and keep their `<style>`/`<script>` inside it.
- **One paused timeline per composition**: `window.__timelines["<composition-id>"] =
  gsap.timeline({ paused: true })`, registered after the build finishes (it may be built inside
  `document.fonts.ready`). Render length comes from the root `data-duration`.
- **Timed clips**: elements with `class="clip"` and `data-start`/`data-duration` are shown and
  hidden by the runtime. Never tween `display`, `visibility`, or `autoAlpha` on a `.clip`; animate a
  child.
- **Transforms**: never pair a CSS initial `transform` with a GSAP tween on the same property; use
  `gsap.fromTo`. Center with flex/inset, not `translate(-50%,-50%)` on a node you also move.
- **Media**: every `<audio>` has an `id` (otherwise the render is silent); no `crossorigin` on
  media; do not put `data-start` on both a `<video>` and an ancestor.
- **Fonts**: every named `font-family` has an in-file `@font-face` pointing to a shipped local file.
- **Determinism**: no wall-clock reads, unseeded `Math.random`, network fetches at render time,
  input state, or infinite repeats (`repeat: -1`). Use a seeded PRNG when randomness is needed.
- **Ids**: unique across the assembled page; prefix sub-composition ids with the composition id.

## Build order

1. `npx hyperframes init` (after confirmation) or open the existing project.
2. Write a design spec (`frame.md` / `design.md`): tokens, type scale, grid, safe areas, per aspect
   ratio. Resting frames first — each beat must work as a still.
3. Build scene by scene in storyboard order; implement seams from the transition map
   (`motion-choreography`), carriers first.
4. Place audio from `voice-video-sync`: music bed, VO, SFX with ids and start times from the
   timeline file — never hand-typed guesses.
5. Keep text crisp: move containers, not glyphs; no `will-change` on text.

## Validate

Run in this order and fix before moving on:

```bash
npx hyperframes lint          # contract errors; a lint error disables the layout/contrast audits
npx hyperframes check         # layout, overflow, contrast
npx hyperframes snapshot      # stills for review; compare against storyboard beats
npx hyperframes preview       # local preview for the user
```

Then render locally: `npx hyperframes render --quality <draft|high>`. Draft first (≤30 s window or
low quality) for the user's approval, then the final.

Outward-facing commands — `publish`, `cloud`, `lambda`, `cloudrun`, `feedback`, `auth`, and
telemetry settings — upload data or change accounts. Run them only when the user asks.

## Custom seek(t) pipeline (when not using HyperFrames)

```text
composition(t) → Playwright page.evaluate(seek, t) → wait fonts/images → screenshot
→ N subframes per output frame → ffmpeg tmix (motion blur) → x264/x265 → mux audio
```

- 60 fps × 4 subframes, shutter 0.5, is a good default; drop blur on frames where numbers change if
  it hurts legibility.
- Encode: `-c:v libx264 -pix_fmt yuv420p -crf 16 -preset slow -movflags +faststart`, AAC 320 kbps.
- The same timestamp rendered twice must produce identical pixels; test it on 3 random frames.

## Hand-off

Deliver the render plus the stills/contact sheet to `video-edit-qc`. When HyperFrames skills are
installed (`hyperframes-core`, `hyperframes-animation`, `hyperframes-creative`, `hyperframes-cli`),
use them for exact flags, adapters (Lottie, Three.js, …), and registry block names.
