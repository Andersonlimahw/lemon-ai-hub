#!/usr/bin/env python3
"""Build a video timeline from voiceover timestamps.

Input: word/segment timestamps (JSON) produced by a TTS API or a forced aligner,
plus an optional locked script. Output: timeline.json (chapters, shots, caption
blocks, frame numbers), captions.srt, captions.vtt, and warnings about caption
readability, dwell before cuts, and long silences.

Timestamp JSON shapes accepted:
    {"segments": [{"text": str, "start": s, "end": s, "words": [{"word", "start", "end"}]}]}
    {"words": [{"word"|"text", "start", "end"}]}
    [{"word"|"text", "start", "end"}]

Script format (optional, --script):
    # CHAPTER 1 Title        -> starts a chapter
    blank line               -> starts a new shot (paragraph)
    |                        -> splits caption blocks inside a paragraph
    ## gap 0.6               -> expected silence after the paragraph (validated)

Stdlib only. Usage:
    python3 build_timeline.py words.json --script script.txt --fps 30 --out-dir timeline/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

LOOKAHEAD = 4
MAX_SILENCE = 3.0
MAX_CPS = 17.0
MIN_CAPTION = 1.0
CAPTION_HOLD = 1.0

_norm_re = re.compile(r"[^\w]+", re.UNICODE)


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


@dataclass
class Shot:
    chapter: int
    blocks: list[Block] = field(default_factory=list)
    gap: float = 0.0

    @property
    def start(self) -> float:
        return self.blocks[0].start if self.blocks else 0.0

    @property
    def end(self) -> float:
        return self.blocks[-1].end if self.blocks else 0.0


@dataclass
class Chapter:
    title: str


def load_words(data) -> list[Word]:
    if isinstance(data, dict) and "segments" in data:
        raw = []
        for seg in data["segments"]:
            if seg.get("words"):
                raw.extend(seg["words"])
            else:  # segment-level only: spread the segment over its tokens
                toks = seg["text"].split()
                span = (seg["end"] - seg["start"]) / max(len(toks), 1)
                raw.extend(
                    {"word": t, "start": seg["start"] + i * span, "end": seg["start"] + (i + 1) * span}
                    for i, t in enumerate(toks)
                )
    elif isinstance(data, dict) and "words" in data:
        raw = data["words"]
    elif isinstance(data, list):
        raw = data
    else:
        raise ValueError("unrecognized timestamp JSON shape")
    words = []
    for w in raw:
        text = str(w.get("word", w.get("text", ""))).strip()
        if not norm(text):
            continue
        words.append(Word(text, float(w["start"]), float(w["end"])))
    if not words:
        raise ValueError("no timed words found")
    return words


def parse_script(text: str) -> tuple[list[Chapter], list[Shot]]:
    chapters: list[Chapter] = []
    shots: list[Shot] = []
    para: list[str] = []

    def flush():
        joined = " ".join(para).strip()
        para.clear()
        if not joined:
            return
        if not chapters:
            chapters.append(Chapter(""))
        blocks = [Block(b.strip()) for b in joined.split("|") if b.strip()]
        shots.append(Shot(len(chapters) - 1, blocks))

    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## gap"):
            flush()
            m = re.match(r"##\s*gap\s+([\d.]+)", s)
            if m and shots:
                shots[-1].gap = float(m.group(1))
        elif s.startswith("#"):
            flush()
            title = re.sub(r"^#+\s*(CHAPTER\s+\d+\s*)?", "", s, flags=re.I).strip()
            chapters.append(Chapter(title))
        elif not s:
            flush()
        else:
            para.append(s)
    flush()
    return chapters, shots


def shots_from_words(words: list[Word], max_chars: int) -> tuple[list[Chapter], list[Shot]]:
    """No script: one shot per sentence, blocks split by max_chars."""
    shots: list[Shot] = []
    cur: list[str] = []
    for w in words:
        cur.append(w.text)
        if w.text.rstrip().endswith((".", "!", "?", "。", "！", "？")):
            shots.append(Shot(0, split_blocks(" ".join(cur), max_chars)))
            cur = []
    if cur:
        shots.append(Shot(0, split_blocks(" ".join(cur), max_chars)))
    return [Chapter("")], shots


def split_blocks(text: str, max_chars: int) -> list[Block]:
    blocks, line = [], ""
    for tok in text.split():
        cand = f"{line} {tok}".strip()
        if len(cand) > max_chars * 2 and line:
            blocks.append(Block(line))
            line = tok
        else:
            line = cand
    if line:
        blocks.append(Block(line))
    return blocks


def align(shots: list[Shot], words: list[Word]) -> list[str]:
    """Greedy sequential alignment of script tokens to timed words."""
    warnings: list[str] = []
    i = 0
    for si, shot in enumerate(shots):
        for block in shot.blocks:
            first = last = None
            for tok in block.text.split():
                n = norm(tok)
                if not n:
                    continue
                if i >= len(words):
                    warnings.append(f"shot {si + 1}: script runs past the audio at '{tok}'")
                    break
                j = next(
                    (k for k in range(i, min(i + LOOKAHEAD, len(words))) if norm(words[k].text) == n),
                    None,
                )
                if j is None:
                    j = i  # mismatch (TTS normalization, typo): consume one word
                    warnings.append(f"shot {si + 1}: '{tok}' not matched, aligned to '{words[j].text}'")
                first = first if first is not None else j
                last = j
                i = j + 1
            if first is None:
                prev = words[max(i - 1, 0)]
                block.start = block.end = prev.end
            else:
                block.start, block.end = words[first].start, words[last].end
    if i < len(words):
        warnings.append(f"{len(words) - i} timed words after the end of the script were ignored")
    return warnings


def caption_ends(shots: list[Shot]) -> list[tuple[Block, float]]:
    """On-screen end per caption: linger CAPTION_HOLD after speech, never overlap the next one."""
    flat = [b for s in shots for b in s.blocks]
    out = []
    for k, b in enumerate(flat):
        want = max(b.end + CAPTION_HOLD, b.start + MIN_CAPTION)
        nxt = flat[k + 1].start if k + 1 < len(flat) else want
        out.append((b, max(min(want, nxt), b.end)))
    return out


def check(shots: list[Shot], words: list[Word], max_chars: int, min_dwell: float) -> list[str]:
    warnings: list[str] = []
    for a, b in zip(words, words[1:]):
        if b.start - a.end > MAX_SILENCE:
            warnings.append(f"silence of {b.start - a.end:.1f}s at {a.end:.2f}s (>{MAX_SILENCE:.0f}s reads as frozen)")
    shown_until = {id(b): end for b, end in caption_ends(shots)}
    for si, shot in enumerate(shots):
        for b in shot.blocks:
            if len(b.text) > max_chars * 2:
                warnings.append(f"shot {si + 1}: caption too long ({len(b.text)} > {max_chars * 2} chars): '{b.text[:40]}…'")
            dur = shown_until[id(b)] - b.start  # reading time = how long the caption is on screen
            if dur > 0 and len(b.text) / dur > MAX_CPS:
                warnings.append(f"shot {si + 1}: caption reads at {len(b.text) / dur:.0f} chars/s (>{MAX_CPS:.0f}): '{b.text[:40]}'")
        if si + 1 < len(shots) and shot.blocks:
            nxt = shots[si + 1].start
            dwell = nxt - shot.blocks[-1].start
            if dwell < min_dwell:
                warnings.append(
                    f"shot {si + 1}: last caption holds {dwell:.2f}s before the cut (<{min_dwell}s) — add '## gap' or merge shots"
                )
            if shot.gap and nxt - shot.end < shot.gap - 0.05:
                warnings.append(f"shot {si + 1}: expected gap {shot.gap}s, audio has {nxt - shot.end:.2f}s")
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


def build(words: list[Word], script: str | None, fps: int, max_chars: int, min_dwell: float) -> tuple[dict, str, str]:
    if script is not None:
        chapters, shots = parse_script(script)
        if not shots:
            raise ValueError("script has no narration lines")
    else:
        chapters, shots = shots_from_words(words, max_chars)
    warnings = align(shots, words)
    total_end = words[-1].end + shots[-1].gap
    warnings += check(shots, words, max_chars, min_dwell)

    def fr(t: float) -> int:
        return int(round(t * fps))

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
    out_chapters = []
    for ci, ch in enumerate(chapters):
        first = next((s for s in shots if s.chapter == ci), None)
        if first is not None:
            out_chapters.append({"index": ci + 1, "title": ch.title,
                                 "start": round(first.start, 3), "startFrame": fr(first.start)})
    timeline = {
        "fps": fps,
        "duration": round(total_end, 3),
        "durationFrames": fr(total_end),
        "chapters": out_chapters,
        "shots": out_shots,
        "warnings": warnings,
    }
    srt, vtt = [], ["WEBVTT", ""]
    for n, (b, end) in enumerate(caption_ends(shots), 1):
        body = wrap(b.text, max_chars)
        srt += [str(n), f"{ts(b.start, ',')} --> {ts(end, ',')}", body, ""]
        vtt += [f"{ts(b.start, '.')} --> {ts(end, '.')}", body, ""]
    return timeline, "\n".join(srt), "\n".join(vtt)


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
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
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
