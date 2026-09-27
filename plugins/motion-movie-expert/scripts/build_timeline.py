#!/usr/bin/env python3
"""Build a video timeline from voiceover timestamps.

Input: word/segment timestamps (JSON) produced by a TTS API or a forced aligner,
plus an optional locked script. Output: timeline.json (chapters, shots, caption
blocks, frame numbers), captions.srt, captions.vtt, and warnings about caption
readability, dwell before cuts, pauses, and long silences.

The audio is the clock: this tool measures it and never shifts timings.

Timestamp JSON shapes accepted:
    {"segments": [{"text": str, "start": s, "end": s, "words": [{"word", "start", "end"}]}]}
    {"words": [{"word"|"text", "start", "end"}]}
    [{"word"|"text", "start", "end"}]

Script format (optional, --script):
    # CHAPTER 1 Title        -> starts a chapter
    blank line               -> starts a new shot (paragraph)
    |                        -> splits caption blocks inside a paragraph
    ## gap 0.6               -> the audio must pause >= 0.6 s after the paragraph;
                                produce that pause in TTS/edit (SSML <break>), this
                                tool only verifies it

Stdlib only. Usage:
    python3 build_timeline.py words.json --script script.txt --fps 30 --out-dir timeline/
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Readability rules (see skills/voice-video-sync/SKILL.md §6). Fixed on purpose:
# they are editorial standards, not per-project knobs.
MAX_SILENCE = 3.0     # s of no speech before the video reads as frozen
MAX_CPS = 17.0        # max caption reading speed, chars per second on screen
MIN_CAPTION = 1.0     # min seconds a caption stays on screen
CAPTION_HOLD = 1.0    # s a caption lingers after its last word
GAP_TOLERANCE = 0.05  # s of slack when verifying a requested pause

_norm_re = re.compile(r"[^\w]+", re.UNICODE)
_sentence_end = (".", "!", "?", "。", "！", "？")


def norm(token: str) -> str:
    return _norm_re.sub("", token.lower())


@dataclass
class Word:
    text: str
    start: float
    end: float


@dataclass
class Block:
    text: str
    start: float = 0.0
    end: float = 0.0
    shown_until: float = 0.0


@dataclass
class Shot:
    chapter: int
    blocks: list[Block]  # never empty: parse_script/shots_from_words drop empty paragraphs
    gap: float = 0.0

    @property
    def start(self) -> float:
        return self.blocks[0].start

    @property
    def end(self) -> float:
        return self.blocks[-1].end


@dataclass
class Script:
    chapters: list[str] = field(default_factory=list)
    shots: list[Shot] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _time(obj: dict, key: str, where: str) -> float:
    try:
        return float(obj[key])
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"{where}: missing or invalid '{key}'") from None


def load_words(data) -> list[Word]:
    if isinstance(data, dict) and "segments" in data:
        raw = []
        for i, seg in enumerate(data["segments"]):
            if seg.get("words"):
                raw.extend(seg["words"])
            else:  # segment-level only: spread the segment over its tokens
                toks = str(seg.get("text", "")).split()
                s, e = _time(seg, "start", f"segment {i}"), _time(seg, "end", f"segment {i}")
                span = (e - s) / max(len(toks), 1)
                raw.extend({"word": t, "start": s + k * span, "end": s + (k + 1) * span} for k, t in enumerate(toks))
    elif isinstance(data, dict) and "words" in data:
        raw = data["words"]
    elif isinstance(data, list):
        raw = data
    else:
        raise ValueError("unrecognized timestamp JSON shape")
    words: list[Word] = []
    untimed: list[int] = []
    for i, w in enumerate(raw):
        if not isinstance(w, dict):
            raise ValueError(f"word {i}: expected an object")
        text = str(w.get("word", w.get("text", ""))).strip()
        if not norm(text):
            continue
        if w.get("start") is None or w.get("end") is None:  # aligners (WhisperX) omit times for some tokens
            untimed.append(len(words))
            words.append(Word(text, -1.0, -1.0))
        else:
            words.append(Word(text, _time(w, "start", f"word {i}"), _time(w, "end", f"word {i}")))
    if len(untimed) == len(words):
        raise ValueError("no timed words found")
    has_time = [w.start >= 0 for w in words]
    for k in untimed:  # squeeze between the original timed neighbours
        prev = next((words[j].end for j in range(k - 1, -1, -1) if has_time[j]), None)
        nxt = next((words[j].start for j in range(k + 1, len(words)) if has_time[j]), None)
        words[k].start = prev if prev is not None else nxt
        words[k].end = nxt if nxt is not None else prev
    return words


def parse_script(text: str) -> Script:
    out = Script()
    para: list[str] = []

    def flush():
        joined = " ".join(para).strip()
        para.clear()
        blocks = [Block(b.strip()) for b in joined.split("|") if b.strip()]
        if blocks:
            if not out.chapters:
                out.chapters.append("")
            out.shots.append(Shot(len(out.chapters) - 1, blocks))

    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if re.match(r"##\s*gap", s):
            flush()
            m = re.fullmatch(r"##\s*gap\s+(\d+(?:\.\d+)?)", s)
            if not m:
                out.warnings.append(f"line {n}: malformed '{s}' ignored (use '## gap 0.6')")
            elif not out.shots:
                out.warnings.append(f"line {n}: '## gap' before any narration ignored")
            else:
                out.shots[-1].gap = float(m.group(1))
        elif re.match(r"#+\s", s):  # "#hashtag" lines stay narration
            flush()
            out.chapters.append(re.sub(r"^#+\s*(CHAPTER\s+\d+\s*)?", "", s, flags=re.I).strip())
        elif not s:
            flush()
        else:
            para.append(s)
    flush()
    return out


def shots_from_words(words: list[Word], max_block: int) -> Script:
    """No script: one shot per sentence, caption blocks of <= max_block chars, timed directly."""
    shots: list[Shot] = []
    blocks: list[Block] = []
    cur: list[Word] = []

    def close_block():
        if cur:
            blocks.append(Block(" ".join(w.text for w in cur), cur[0].start, cur[-1].end))
            cur.clear()

    for w in words:
        if cur and len(" ".join(x.text for x in cur)) + 1 + len(w.text) > max_block:
            close_block()
        cur.append(w)
        if w.text.endswith(_sentence_end):
            close_block()
            shots.append(Shot(0, blocks))
            blocks = []
    close_block()
    if blocks:
        shots.append(Shot(0, blocks))
    return Script(chapters=[""], shots=shots)


def _blocks_in_order(shots: list[Shot]) -> list[Block]:
    return [b for s in shots for b in s.blocks]


def align(shots: list[Shot], words: list[Word]) -> list[str]:
    """Time each script block from the audio via a diff of normalized tokens.

    Audio words missing from the script (fillers, TTS additions) are skipped,
    script words missing from the audio stay untimed, substitutions (e.g. "3"
    read as "three") are paired in order. One warning per mismatching run.
    """
    toks = [(si, b, t) for si, shot in enumerate(shots) for b in shot.blocks for t in b.text.split() if norm(t)]
    matcher = difflib.SequenceMatcher(a=[norm(t) for _, _, t in toks], b=[norm(w.text) for w in words], autojunk=False)
    timed: dict[int, tuple[float, float]] = {}
    warnings: list[str] = []
    for op, a1, a2, b1, b2 in matcher.get_opcodes():
        if op in ("equal", "replace"):
            for k in range(a1, a2):
                w = words[min(b1 + (k - a1), b2 - 1)]
                timed[k] = (w.start, w.end)
        if op == "equal":
            continue
        where = f"shot {toks[a1][0] + 1}" if a1 < len(toks) else "after the script"
        said = " ".join(t for _, _, t in toks[a1:a2])
        heard = " ".join(w.text for w in words[b1:b2])
        warnings.append({
            "replace": f"{where}: script '{said}' aligned to audio '{heard}'",
            "delete": f"{where}: script '{said}' not found in the audio",
            "insert": f"{where}: audio '{heard}' not in the script (skipped)",
        }[op])

    spans: dict[int, list[tuple[float, float]]] = {}
    for k, (_, block, _) in enumerate(toks):
        if k in timed:
            spans.setdefault(id(block), []).append(timed[k])
    prev_end = words[0].start
    for block in _blocks_in_order(shots):
        got = spans.get(id(block))
        block.start, block.end = (got[0][0], got[-1][1]) if got else (prev_end, prev_end)
        prev_end = block.end
    return warnings


def set_caption_ends(shots: list[Shot]) -> None:
    """On-screen end per caption: linger CAPTION_HOLD after speech, never overlap the next one."""
    flat = _blocks_in_order(shots)
    for k, b in enumerate(flat):
        want = max(b.end + CAPTION_HOLD, b.start + MIN_CAPTION)
        nxt = flat[k + 1].start if k + 1 < len(flat) else want
        b.shown_until = max(min(want, nxt), b.end)


def check(shots: list[Shot], words: list[Word], max_block: int, min_dwell: float) -> list[str]:
    warnings: list[str] = []
    for a, b in zip(words, words[1:]):
        if b.start - a.end > MAX_SILENCE:
            warnings.append(f"silence of {b.start - a.end:.1f}s at {a.end:.2f}s (>{MAX_SILENCE:.0f}s reads as frozen)")
    for si, shot in enumerate(shots):
        for b in shot.blocks:
            if len(b.text) > max_block:
                warnings.append(f"shot {si + 1}: caption too long ({len(b.text)} > {max_block} chars): '{b.text[:40]}…'")
            on_screen = b.shown_until - b.start
            if on_screen > 0 and len(b.text) / on_screen > MAX_CPS:
                warnings.append(f"shot {si + 1}: caption reads at {len(b.text) / on_screen:.0f} chars/s (>{MAX_CPS:.0f}): '{b.text[:40]}'")
        if si + 1 < len(shots):
            nxt = shots[si + 1].start
            dwell = nxt - shot.blocks[-1].start
            if dwell < min_dwell:
                warnings.append(
                    f"shot {si + 1}: last caption holds {dwell:.2f}s before the cut (<{min_dwell}s) — "
                    "add a pause in the audio (## gap + SSML <break>) or merge shots"
                )
            if shot.gap and nxt - shot.end < shot.gap - GAP_TOLERANCE:
                warnings.append(f"shot {si + 1}: '## gap {shot.gap}' requested, audio pauses {nxt - shot.end:.2f}s")
    return warnings


def ts(t: float, sep: str) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def wrap(text: str, max_chars: int) -> str:
    words = text.split()
    if len(text) <= max_chars or len(words) < 2:
        return text
    best = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(" ".join(words[k:]))))
    return " ".join(words[:best]) + "\n" + " ".join(words[best:])


def to_timeline(script: Script, fps: int, total_end: float, warnings: list[str]) -> dict:
    def fr(t: float) -> int:
        return int(round(t * fps))

    shots = script.shots
    out_shots = []
    for si, shot in enumerate(shots):
        end = shots[si + 1].start if si + 1 < len(shots) else total_end
        out_shots.append({
            "index": si + 1,
            "chapter": shot.chapter + 1,
            "start": round(shot.start, 3),
            "end": round(end, 3),
            "startFrame": fr(shot.start),
            "endFrame": fr(end),
            "blocks": [
                {"text": b.text, "start": round(b.start, 3), "end": round(b.end, 3),
                 "startFrame": fr(b.start), "endFrame": fr(b.end)}
                for b in shot.blocks
            ],
        })
    chapters = []
    for ci, title in enumerate(script.chapters):
        first = next((s for s in shots if s.chapter == ci), None)
        if first is not None:
            chapters.append({"index": ci + 1, "title": title, "start": round(first.start, 3), "startFrame": fr(first.start)})
    return {
        "fps": fps,
        "duration": round(total_end, 3),
        "durationFrames": fr(total_end),
        "chapters": chapters,
        "shots": out_shots,
        "warnings": warnings,
    }


def to_captions(shots: list[Shot], max_chars: int) -> tuple[str, str]:
    srt, vtt = [], ["WEBVTT", ""]
    for n, b in enumerate(_blocks_in_order(shots), 1):
        body = wrap(b.text, max_chars)
        srt += [str(n), f"{ts(b.start, ',')} --> {ts(b.shown_until, ',')}", body, ""]
        vtt_body = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        vtt += [f"{ts(b.start, '.')} --> {ts(b.shown_until, '.')}", vtt_body, ""]
    return "\n".join(srt), "\n".join(vtt)


def build(words: list[Word], script_text: str | None, fps: int, max_chars: int, min_dwell: float) -> tuple[dict, str, str]:
    max_block = 2 * max_chars  # a caption block is at most two lines
    if script_text is not None:
        script = parse_script(script_text)
        if not script.shots:
            raise ValueError("script has no narration lines")
        warnings = script.warnings + align(script.shots, words)
    else:
        script = shots_from_words(words, max_block)
        warnings = []
    set_caption_ends(script.shots)
    warnings += check(script.shots, words, max_block, min_dwell)
    # the video ends after the requested final pause and never cuts the last caption short
    total_end = max(words[-1].end + script.shots[-1].gap, script.shots[-1].blocks[-1].shown_until)
    srt, vtt = to_captions(script.shots, max_chars)
    return to_timeline(script, fps, total_end, warnings), srt, vtt


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("timestamps", type=Path, help="word/segment timestamps JSON")
    ap.add_argument("--script", type=Path, help="locked narration script")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--out-dir", type=Path, default=Path("timeline"))
    ap.add_argument("--max-chars", type=int, default=42, help="max characters per caption line")
    ap.add_argument("--min-dwell", type=float, default=1.0, help="min seconds the last caption holds before a cut")
    ap.add_argument("--strict", action="store_true", help="exit 1 when there are warnings")
    args = ap.parse_args(argv)
    if args.fps <= 0 or args.max_chars <= 0:
        ap.error("--fps and --max-chars must be positive")

    try:
        words = load_words(json.loads(args.timestamps.read_text(encoding="utf-8")))
        script = args.script.read_text(encoding="utf-8") if args.script else None
        timeline, srt, vtt = build(words, script, args.fps, args.max_chars, args.min_dwell)
    except (OSError, ValueError) as exc:  # JSONDecodeError is a ValueError
        print(f"error: {exc}", file=sys.stderr)
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "timeline.json").write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out_dir / "captions.srt").write_text(srt, encoding="utf-8")
    (args.out_dir / "captions.vtt").write_text(vtt, encoding="utf-8")
    print(f"{len(timeline['shots'])} shots, {timeline['duration']}s @ {args.fps} fps -> {args.out_dir}/")
    for w in timeline["warnings"]:
        print(f"warning: {w}")
    return 1 if args.strict and timeline["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())
