---
name: video-edit-qc
description: Edit existing video and verify any render before delivery — recut, trim, reframe to other aspect ratios, burn in or attach captions, swap or remix audio, loop, and export; plus the QC gates (probe, contact sheet, stills per beat, loudness, loop seam, legibility, facts, PII). Use for editing footage or for the final check of any motion video.
---

# Video Edit & QC

Never edit in place. Write outputs to a new file (`*_v2.mp4`, `renders/`), keep the source intact,
and confirm before overwriting or deleting anything.

## Edit recipes (FFmpeg)

```bash
# Trim without re-encode (cuts on keyframes) / frame-accurate with re-encode
ffmpeg -ss 00:00:05 -to 00:00:20 -i in.mp4 -c copy out.mp4
ffmpeg -i in.mp4 -ss 5 -to 20 -c:v libx264 -crf 16 -c:a aac out.mp4

# Concatenate clips with identical codecs
printf "file '%s'\n" a.mp4 b.mp4 > list.txt && ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4

# Reframe 16:9 -> 9:16 around a subject at x=CX (pixels); prefer re-composing the design instead
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih:CX-ih*9/32:0,scale=1080:1920" -c:a copy out_9x16.mp4

# Burn in captions (style for social) / attach as a soft track
ffmpeg -i in.mp4 -vf "subtitles=captions.srt:force_style='FontName=Inter,FontSize=14,Outline=1,MarginV=60'" out.mp4
ffmpeg -i in.mp4 -i captions.srt -c copy -c:s mov_text out.mp4

# Replace audio / duck music under voice / normalize to -14 LUFS
ffmpeg -i in.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -shortest out.mp4
ffmpeg -i music.wav -i vo.wav -filter_complex "[0][1]sidechaincompress=threshold=0.05:ratio=8:attack=150:release=300[m];[m][1]amix=inputs=2:normalize=0" mix.wav
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=11 -ar 48000 mix_norm.wav   # two-pass for final delivery

# Web/social delivery encode (from the master; the master itself is CRF 16 — see hyperframes-production)
ffmpeg -i in.mp4 -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -movflags +faststart -c:a aac -b:a 192k out.mp4
```

For talking-head recuts, cut on sentence boundaries from a transcript (`voice-video-sync`
timestamps), remove fillers only where the cut is invisible, and keep 80–150 ms of room tone at
each cut. For reframing designed motion, re-compose per aspect ratio in the source project instead
of cropping when possible.

## QC gates

Run from the project directory (`QC=<plugin-root>/scripts/qc.sh`):

```bash
$QC probe    final.mp4                  # codec, size, fps, duration, audio present
$QC sheet    final.mp4 qc/sheet.png 4 4 # contact sheet for a full read-through
$QC stills   final.mp4 qc/ 0.5 3 7.5    # one still per storyboard beat; fails past the end
$QC loudness final.mp4                  # -14 ±1 LUFS (pass -23 for broadcast), true peak <= -1 dBTP
$QC loop     final.mp4                  # loops only: seam must look like a normal frame step
```

Then review the stills and sheet against the storyboard:

| Gate | Pass when |
|---|---|
| Spec | resolution, fps, duration, and codec match the brief for every aspect ratio |
| Story | understandable with sound off; first 2 s carry the value or the hook |
| Continuity | every cut has its carrier; no crossfade between unrelated screens; no ping-pong seams |
| Rhythm | key actions on beats; no dead frames; no unmotivated stillness > 3 s |
| Legibility | no clipped or overlapping text; captions ≤2 lines inside safe areas; numbers readable through motion blur |
| Brand | sampled colors match tokens; correct fonts and icon set; no redesign |
| Facts | every on-screen number or claim is in the storyboard fact list |
| Safety | no PII, no real third-party brands without permission, licenses and attributions present |
| Audio | loudness and true peak in range; SFX under music; VO intelligible over music |
| Accessibility | ≤3 flashes per second; captions match the spoken words |
| Loop | when requested, the seam passes `qc.sh loop` |
| Determinism | the same timestamp rendered twice is identical (spot-check 3 frames) |

Report each gate as pass / fail / not checked, with the evidence path (still, sheet, command output).
Fix failures in the source and re-render; do not paper over them in the final encode. For long
videos, split QC by chapter and use the `motion-qc` agent per chapter in parallel.
