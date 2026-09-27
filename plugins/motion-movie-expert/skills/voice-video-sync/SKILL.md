---
name: voice-video-sync
description: Synchronize narration, captions, music, and SFX with picture — narration writing, script lock, TTS or recorded voiceover, word-level timestamps, caption blocks, shot windows derived from the voice track, dwell budgets, ducking, and loudness targets. Use for narrated explainers, voiceover changes, subtitles, or any video where timing must follow audio.
---

# Voice ↔ Video Sync

Rule zero: **the voice track drives the clock.** Picture is timed to measured audio, never to
guessed durations.

## 1. Write the narration

- Open on the viewer's situation, not a definition. One storyline; cause before effect.
- Convert numbers to felt scale ("the size of a phone book", not "3.2 MB").
- Metaphors must carry weight; the narrator has a point of view.
- Do not describe what the picture already shows; say what the picture cannot.
- End by calling back to the opening. Chapter boundaries hand off: last line of chapter N sets up
  the first line of N+1.
- Budget by speaking rate: English ≈ 125–150 words/min (TTS voices vary — measure one sample);
  Portuguese ≈ 140–160 words/min; Chinese ≈ 4–5.5 characters/s.

Format for the script file (one paragraph = one shot, `|` splits caption blocks):

```text
# CHAPTER 1 Why maps lie
Every map you have seen | was drawn by someone | with a reason.

Mercator wanted sailors | to hold a straight course.
## gap 0.6
```

`## gap <seconds>` asks for a pause of at least that long after the paragraph (dwell for the last
visual). Produce it in the audio — SSML `<break time="600ms"/>` for TTS, or inserted silence when
assembling per-paragraph files. The timeline tool never shifts timings; it verifies the pause.

## 2. Lock the script

Show the full script with word count and estimated duration and get an explicit "approved". After
lock, every timing is derived from audio; changing a word re-times all shots after it.

## 3. Produce the voice

- **TTS** (default when no recording): ask the user for a preferred engine/voice. Sending text to a
  cloud TTS (ElevenLabs, Azure, OpenAI, Google, edge-tts) shares the script with that provider —
  confirm first. Local options (Kokoro, Piper) keep it on the machine.
- **Recorded VO**: accept WAV 48 kHz. Trim silence, keep breaths natural, normalize later in the mix.
- Keep one file per paragraph or one master file plus timestamps; both work with the timeline tool.

## 4. Get timestamps

Use word- or segment-level timestamps from the TTS API response, or force-align the audio with the
script (WhisperX, `whisper-timestamped`, `stable-ts`, or Whisper with `word_timestamps=True`).
Normalize them to this JSON:

```json
{"segments": [{"text": "Every map you have seen", "start": 0.00, "end": 1.42,
  "words": [{"word": "Every", "start": 0.00, "end": 0.21}]}]}
```

## 5. Build the timeline

```bash
python3 <plugin-root>/scripts/build_timeline.py words.json --script script.txt --fps 30 \
  --out-dir timeline/ --max-chars 42 --min-dwell 1.0
```

Produces `timeline.json` (shots with start/end frames, caption blocks, chapter starts),
`captions.srt`, `captions.vtt`, and warnings for: script words missing from the audio (or audio
words missing from the script), captions too long or too fast to read, shots whose last caption
leaves less than `--min-dwell` seconds before the next shot (add a pause in the audio or merge),
requested `## gap` pauses the audio does not have, and silences longer than 3 s. Words a forced
aligner left untimed (common for numbers in WhisperX) are interpolated between their neighbours. Feed `timeline.json` to the composition; never
retype frame numbers by hand.

## 6. Caption rules

- ≤42 characters per line, ≤2 lines, ≥1.0 s on screen, ≈17 characters/s reading speed maximum.
- Break at phrase boundaries, never between article and noun.
- Keep captions out of the lower platform UI zone in 9:16 and away from on-screen UI text.
- Burned-in captions for social; sidecar SRT/VTT for YouTube and web players.

## 7. Mix

| Layer | Target |
|---|---|
| Integrated loudness (final) | −14 LUFS for social/web (−16 acceptable); −23 LUFS for broadcast |
| True peak | ≤ −1 dBTP |
| Music under VO | duck 8–12 dB while speech is present, 150–300 ms attack/release |
| SFX | ≈10 dB under music; on the causing frame, not after |

Measure with `<plugin-root>/scripts/qc.sh loudness final.mp4` (add `-23` for broadcast). When HyperFrames audio skills are installed,
`hyperframes-audio` provides ducking ("voiceover carve"), EQ, and automation inside the composition;
otherwise use FFmpeg `sidechaincompress` and `loudnorm` (two-pass).

## 8. Preview checkpoint

Render the first ≤30 s with voice, captions, and music and ask: "Voice, pace, caption size, and
rhythm — OK?" Changing pace after this point means re-running TTS and re-timing everything.
