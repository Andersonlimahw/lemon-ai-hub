---
name: motion-choreography
description: Motion law for multi-scene videos — seam continuity (axis, direction, speed, phase), carriers, causal motion, springs and timing, camera, transitions, stillness, and loop design. Use when planning or fixing how scenes connect and move, before and during any animation build.
---

# Motion Choreography

The failure this prevents: scenes authored in isolation. The eye's momentum dies at every cut and
elements wobble in place between entry and exit. A good film reads as one continuous camera move.

## 1. The Seam Law

How scene A exits decides how scene B enters.

1. **Axis** — x stays x, y stays y, z stays z across a cut.
2. **Direction** — never mirror. On z, direction is the sign of scale change: growing = push in,
   shrinking = pull out. A receding exit answered by a grow-from-small entry is a mirrored vector.
3. **Speed** — entry start velocity ≈ exit end velocity: mirrored eases (exit `power3.in` → entry
   `power3.out`, same distance and duration).
4. **Phase** — cut mid-motion on both sides. Settling to rest before a cut, or starting from rest
   after it, is a dead beat.

**The current.** Pick one dominant direction for ordinary "next beat" seams (default: leftward).
Reserve the others for meaning: upward = conclusion/reveal, z-forward = deeper into the same
thought, z-backward = arrival of something bigger, burst outward = leaving a world. Never run two
consecutive seams in opposite directions; a direction change needs a visible cause (click, impact)
or a chapter boundary.

**Seam ledger.** Before building, add one row per cut to the storyboard transition map: cut time,
exit vector, entry vector, carrier, technique. If a row mismatches, fix the plan, not the easing.

## 2. Carriers and anchors

The eye follows objects. The strongest seam hands a concrete carrier across the cut at matched
position and velocity: a cursor mid-path, a container that shrinks and docks into the next layout,
a chip that flies into its exact slot, a number that becomes the next headline. With no natural
carrier, the scene's hero element carries it (partial travel + early fade, next entry mid-flight).
A plain crossfade has no carrier — use it only between chapters, and prefer a hard cut on a beat.

## 3. Causal motion

Chain moves so each is visibly launched by the last:
`press → squash → release spring → flight → impact → recoil → reveal`.

- Effects start on the causing frame, never "shortly after".
- Reactions scale with implied mass: large elements rebound slower, small ones snap.
- A force is a license to change direction; an uncaused flip reads as an error.

## 4. Timing and springs

| Use | Duration | Curve |
|---|---|---|
| Micro-interaction (press, toggle, chip) | 180–450 ms | spring, damping ratio 0.75–0.90 |
| Layout / state transition | 400–700 ms | spring or `power3.out` |
| Camera move / map fly-to | 600–1200 ms | short ease-out, no gratuitous rotation |
| Stagger interval | 50–100 ms | same curve per item |
| Dwell after a key element lands | ≥1.0 s (≥30 frames at 30 fps) | still, or a 1.00 → 1.05 slow push |

- Overshoot ≤6 %. Bouncy easing reads as cheap.
- Springs are **closed-form functions of absolute time** (no integrators carrying state between
  frames). Multiple targets = sum of independent responses, each starting at its own trigger time.
- Direct manipulation (drag, pinch, scroll): value follows the pointer; on release, the spring
  starts from the exact release position and velocity.
- Put key actions on the beat grid (at 120 BPM: every 0.5 s). Leave the viewer time to read
  on-screen text; caption reading-speed limits live in `voice-video-sync` §6.

## 5. Performance: the scene keeps performing

- **No idle wobble.** Between entry and exit, an element either holds still with intent or keeps a
  motivated motion (slow push, count-up, progress). Floating sine-bobs are filler.
- **Stillness before the climax.** A short hold (0.3–0.6 s) before the key reveal makes it land.
- **Maximum unmotivated stillness: 3 s.** Longer reads as a frozen video.
- **One hero per beat.** Everything else dims (≈12–40 % opacity) or holds.

## 6. Camera

The UI is a physical stage. The camera zooms, pans, follows, and focuses to reinforce the
interaction, and nothing else. Key information fills 55–80 % of the frame at its moment. Animate
transforms on a container, never on text itself, so type stays crisp. Avoid random handheld shake,
dutch angles, and 3D orbits without narrative purpose.

## 7. Text in motion

- Old text leaves (opacity↓, blur↑, translate) before new text enters. Never two texts in one slot.
- Changing numbers: vertical roll, tabular numerals, the old value exits with blur.
- Kinetic type: reveal by word or line on the beat; keep the resting layout readable as a still.

## 8. Loops

Design the loop from beat 1: the frame that would follow the last frame is the first frame — same
camera, geometry, cursor, opacity, velocity, text, and state — so the seam looks like any other
frame step (a duplicated frame at the seam is a visible hitch). Verify with
`<plugin-root>/scripts/qc.sh loop` (see `video-edit-qc`).

## 9. Reduced motion and accessibility

For web/UI deliverables, respect `prefers-reduced-motion` (swap transforms for opacity ≤200 ms).
For video: no more than 3 flashes per second, no full-frame high-contrast strobing, and captions
for all speech.

## Gate before build

- [ ] every cut in the transition map has a carrier and matching vectors;
- [ ] consecutive seams do not ping-pong;
- [ ] each beat has one hero and a dwell long enough to read;
- [ ] no stretch of unmotivated stillness > 3 s;
- [ ] durations and springs come from the table above or a stated reason.

When HyperFrames skills are installed, `motion-doctrine`, `cut-the-curve`, and
`hyperframes-animation` provide GSAP recipes and a seam verifier for these same laws.
