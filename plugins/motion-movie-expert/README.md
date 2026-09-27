# motion-movie-expert

Create and edit motion videos with any AI coding agent — Claude Code, Codex, Antigravity (Agy),
OpenCode, Gemini CLI. One orchestrator (`SKILL.md`) routes to focused sub-skills:

| Skill | Purpose |
|---|---|
| `motion-storyboard` | Intake, master prompt template (PT-BR), storyboard contract and approval gate |
| `motion-choreography` | Seam Law, carriers, causal motion, springs/timing, camera, loops |
| `motion-graphics-shots` | Short design-led pieces: kinetic type, stats, charts, logo stings, maps, UI |
| `hyperframes-production` | Deterministic build and render (HyperFrames default, custom `seek(t)` pipeline) |
| `voice-video-sync` | Narration, script lock, TTS/VO, timestamps → timeline, captions, mix and loudness |
| `ui-motion-patterns` | Motion tokens, springs, React `motion/react` patterns, faithful UI rebuilds |
| `video-edit-qc` | FFmpeg edit recipes and the QC gates for every render |

Agents: `motion-director` (plans, never builds) and `motion-qc` (read-only review with evidence).

## Scripts

```bash
# voiceover timestamps + locked script -> timeline.json, captions.srt/.vtt, warnings
python3 scripts/build_timeline.py words.json --script script.txt --fps 30 --out-dir timeline/

# render QC (ffmpeg/ffprobe)
scripts/qc.sh probe|loudness|sheet|stills|loop <video> …
```

Tests: `python3 -m unittest discover -s tests` (stdlib only).

## Sources and curation

Built from, not copied from: a production master prompt for product motion films (YourMapSeat),
HeyGen's HyperFrames skills (`motion-graphics`, `hyperframes-animation`, `hyperframes-creative`,
`hyperframes-core`, `motion-doctrine`), `affaan-m/ecc` (`motion-foundations`, `motion-patterns`),
`Vincentwei1021/anything2explainer` (narration-first timing and QC ideas; no code reused), and this
hub's `design-expert` principles. Upstream instructions were reviewed for prompt-injection and
supply-chain risk: runtime self-update of skills, unconfirmed package installs, hosted publishing,
and uploads to third-party APIs are gated behind explicit user confirmation here.

Upstream HyperFrames skills remain optional runtime helpers: install them separately
(`npx skills add heygen-com/hyperframes`) if you want exact CLI flags and registry blocks.
