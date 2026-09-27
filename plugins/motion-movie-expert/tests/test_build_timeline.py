#!/usr/bin/env python3
"""Tests for scripts/build_timeline.py. Run: python3 -m unittest discover -s tests"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_timeline as bt  # noqa: E402


def timed(text: str, start: float = 0.0, step: float = 0.4, pause_after: dict[int, float] | None = None):
    """Evenly timed words; pause_after maps word index -> extra silence."""
    out, t = [], start
    for i, w in enumerate(text.split()):
        out.append({"word": w, "start": round(t, 3), "end": round(t + step - 0.05, 3)})
        t += step + (pause_after or {}).get(i, 0.0)
    return out


SCRIPT = """# CHAPTER 1 Why maps lie
Every map you have seen | was drawn by someone.

Mercator wanted sailors | to hold a course.
## gap 0.5

# CHAPTER 2 Scale
Scale changes everything.
"""
TEXT = "Every map you have seen was drawn by someone. Mercator wanted sailors to hold a course. Scale changes everything."


class ParseScript(unittest.TestCase):
    def test_chapters_shots_blocks_and_gap(self):
        chapters, shots = bt.parse_script(SCRIPT)
        self.assertEqual([c.title for c in chapters], ["Why maps lie", "Scale"])
        self.assertEqual(len(shots), 3)
        self.assertEqual([b.text for b in shots[0].blocks], ["Every map you have seen", "was drawn by someone."])
        self.assertEqual(shots[1].gap, 0.5)
        self.assertEqual(shots[2].chapter, 1)


class LoadWords(unittest.TestCase):
    def test_shapes(self):
        words = timed("a b")
        self.assertEqual(len(bt.load_words(words)), 2)
        self.assertEqual(len(bt.load_words({"words": words})), 2)
        self.assertEqual(len(bt.load_words({"segments": [{"text": "a b", "start": 0, "end": 1, "words": words}]})), 2)

    def test_segment_without_words_is_spread(self):
        ws = bt.load_words({"segments": [{"text": "one two", "start": 0.0, "end": 1.0}]})
        self.assertEqual([(w.start, w.end) for w in ws], [(0.0, 0.5), (0.5, 1.0)])

    def test_punctuation_only_tokens_dropped_and_empty_rejected(self):
        self.assertEqual(len(bt.load_words([{"word": "—", "start": 0, "end": 1}, {"word": "hi", "start": 1, "end": 2}])), 1)
        with self.assertRaises(ValueError):
            bt.load_words([])


class Build(unittest.TestCase):
    def setUp(self):
        # 0.6 s silence after "course." (word index 16) to satisfy the gap.
        self.words = bt.load_words(timed(TEXT, pause_after={16: 0.6}))

    def test_alignment_frames_and_captions(self):
        tl, srt, vtt = bt.build(self.words, SCRIPT, fps=30, max_chars=42, min_dwell=0.5)
        self.assertEqual(len(tl["shots"]), 3)
        self.assertEqual([c["title"] for c in tl["chapters"]], ["Why maps lie", "Scale"])
        s1, s2 = tl["shots"][0], tl["shots"][1]
        self.assertEqual(s1["start"], 0.0)
        self.assertEqual(s1["end"], s2["start"])  # shots tile the timeline
        self.assertEqual(s2["blocks"][0]["startFrame"], round(s2["blocks"][0]["start"] * 30))
        self.assertEqual(tl["chapters"][1]["start"], tl["shots"][2]["start"])
        self.assertIn("00:00:00,000 --> ", srt)
        self.assertTrue(vtt.startswith("WEBVTT"))
        self.assertEqual(srt.count(" --> "), 5)
        self.assertFalse([w for w in tl["warnings"] if "not matched" in w], tl["warnings"])

    def test_missing_gap_and_short_dwell_warn(self):
        words = bt.load_words(timed(TEXT))  # no silence inserted
        tl, _, _ = bt.build(words, SCRIPT, fps=30, max_chars=42, min_dwell=2.0)
        joined = "\n".join(tl["warnings"])
        self.assertIn("expected gap 0.5s", joined)
        self.assertIn("before the cut", joined)

    def test_tts_normalization_mismatch_is_tolerated(self):
        script = "We have 3 maps."
        words = bt.load_words(timed("We have three maps."))
        tl, _, _ = bt.build(words, script, fps=25, max_chars=42, min_dwell=0.1)
        self.assertEqual(tl["shots"][0]["blocks"][0]["end"], words[-1].end)
        self.assertTrue(any("'3' not matched" in w for w in tl["warnings"]))

    def test_long_silence_warns(self):
        words = bt.load_words(timed("one two", pause_after={0: 4.0}))
        tl, _, _ = bt.build(words, None, fps=30, max_chars=42, min_dwell=0.1)
        self.assertTrue(any("silence of" in w for w in tl["warnings"]))

    def test_no_script_splits_sentences(self):
        tl, _, _ = bt.build(self.words, None, fps=30, max_chars=42, min_dwell=0.1)
        self.assertEqual(len(tl["shots"]), 3)

    def test_script_longer_than_audio_warns(self):
        words = bt.load_words(timed("Every map"))
        tl, _, _ = bt.build(words, "Every map you have seen.", fps=30, max_chars=42, min_dwell=0.1)
        self.assertTrue(any("runs past the audio" in w for w in tl["warnings"]))


class Helpers(unittest.TestCase):
    def test_timestamp_format(self):
        self.assertEqual(bt.ts(3723.456, ","), "01:02:03,456")

    def test_wrap_balances_two_lines(self):
        self.assertEqual(bt.wrap("short", 42), "short")
        self.assertEqual(bt.wrap("aaaa bbbb cccc dddd", 10), "aaaa bbbb\ncccc dddd")

    def test_wrap_single_long_word(self):
        self.assertEqual(bt.wrap("supercalifragilistic", 5), "supercalifragilistic")

    def test_reading_speed_uses_on_screen_time(self):
        # Fast speech, but the caption stays up until the next one 3 s later: readable.
        words = bt.load_words(timed("Scale changes everything. Next.", step=0.2, pause_after={2: 3.0}))
        tl, _, _ = bt.build(words, None, fps=30, max_chars=42, min_dwell=0.1)
        self.assertFalse([w for w in tl["warnings"] if "chars/s" in w], tl["warnings"])


class Cli(unittest.TestCase):
    def test_writes_outputs_and_strict_exit(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "w.json").write_text(json.dumps(timed(TEXT)))
            (d / "s.txt").write_text(SCRIPT)
            rc = bt.main([str(d / "w.json"), "--script", str(d / "s.txt"), "--out-dir", str(d / "out")])
            self.assertEqual(rc, 0)
            for f in ("timeline.json", "captions.srt", "captions.vtt"):
                self.assertTrue((d / "out" / f).stat().st_size > 0)
            rc = bt.main([str(d / "w.json"), "--script", str(d / "s.txt"), "--out-dir", str(d / "out"), "--strict"])
            self.assertEqual(rc, 1)  # missing gap warning

    def test_bad_input_returns_2(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.json"
            p.write_text("{}")
            self.assertEqual(bt.main([str(p), "--out-dir", str(Path(d) / "o")]), 2)


if __name__ == "__main__":
    unittest.main()
