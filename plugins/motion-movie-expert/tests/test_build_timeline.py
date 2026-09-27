#!/usr/bin/env python3
"""Tests for scripts/build_timeline.py. Run: python3 -m unittest discover -s tests"""

from __future__ import annotations

import contextlib
import io
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


def blocks(tl):
    return [b for s in tl["shots"] for b in s["blocks"]]


class ParseScript(unittest.TestCase):
    def test_chapters_shots_blocks_and_gap(self):
        sc = bt.parse_script(SCRIPT)
        self.assertEqual(sc.chapters, ["Why maps lie", "Scale"])
        self.assertEqual(len(sc.shots), 3)
        self.assertEqual([b.text for b in sc.shots[0].blocks], ["Every map you have seen", "was drawn by someone."])
        self.assertEqual(sc.shots[1].gap, 0.5)
        self.assertEqual(sc.shots[2].chapter, 1)
        self.assertEqual(sc.warnings, [])

    def test_gap_variants_and_hashtags(self):
        sc = bt.parse_script("## gap 1\n#motion rocks\n##gap 0.3\n## gapx\n")
        self.assertEqual(len(sc.shots), 1)
        self.assertEqual(sc.shots[0].blocks[0].text, "#motion rocks")  # hashtag is narration, not a chapter
        self.assertEqual(sc.shots[0].gap, 0.3)  # no space after ## still a gap
        self.assertEqual(len(sc.warnings), 2)  # gap before narration + malformed gap
        self.assertIn("before any narration", sc.warnings[0])
        self.assertIn("malformed", sc.warnings[1])


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

    def test_untimed_words_are_interpolated(self):
        # WhisperX omits times for tokens it cannot align, often numbers.
        ws = bt.load_words([
            {"word": "we", "start": 0.0, "end": 0.2},
            {"word": "have"},
            {"word": "3", "start": None, "end": None},
            {"word": "maps", "start": 1.0, "end": 1.3},
        ])
        self.assertEqual([(w.start, w.end) for w in ws[1:3]], [(0.2, 1.0), (0.2, 1.0)])

    def test_invalid_times_raise_value_error(self):
        with self.assertRaisesRegex(ValueError, "word 0: missing or invalid 'start'"):
            bt.load_words([{"word": "a", "start": "soon", "end": 1}])
        with self.assertRaisesRegex(ValueError, "expected an object"):
            bt.load_words(["a"])


class Align(unittest.TestCase):
    def test_extra_script_word_does_not_shift_later_words(self):
        words = bt.load_words(timed("alpha beta gamma delta", step=0.5))
        tl, _, _ = bt.build(words, "alpha EXTRA beta | gamma delta", fps=30, max_chars=42, min_dwell=0.1)
        b1, b2 = blocks(tl)
        self.assertEqual((b1["start"], b1["end"]), (0.0, 0.95))  # alpha..beta
        self.assertEqual((b2["start"], b2["end"]), (1.0, 1.95))  # gamma..delta
        self.assertTrue(any("'EXTRA' not found in the audio" in w for w in tl["warnings"]))

    def test_extra_audio_word_is_skipped(self):
        words = bt.load_words(timed("alpha um beta gamma", step=0.5))
        tl, _, _ = bt.build(words, "alpha beta | gamma", fps=30, max_chars=42, min_dwell=0.1)
        b1, b2 = blocks(tl)
        self.assertEqual((b1["start"], b1["end"]), (0.0, 1.45))
        self.assertEqual(b2["start"], 1.5)
        self.assertTrue(any("audio 'um' not in the script" in w for w in tl["warnings"]))

    def test_substitution_is_paired(self):
        words = bt.load_words(timed("We have three maps."))
        tl, _, _ = bt.build(words, "We have 3 maps.", fps=25, max_chars=42, min_dwell=0.1)
        self.assertEqual(blocks(tl)[0]["end"], words[-1].end)
        self.assertTrue(any("script '3' aligned to audio 'three'" in w for w in tl["warnings"]))

    def test_script_longer_than_audio_warns(self):
        words = bt.load_words(timed("Every map"))
        tl, _, _ = bt.build(words, "Every map you have seen.", fps=30, max_chars=42, min_dwell=0.1)
        self.assertTrue(any("not found in the audio" in w for w in tl["warnings"]))


class Build(unittest.TestCase):
    def setUp(self):
        # 0.6 s silence after "course." (word index 15) satisfies '## gap 0.5'.
        self.words = bt.load_words(timed(TEXT, pause_after={15: 0.6}))

    def test_alignment_frames_and_captions(self):
        tl, srt, vtt = bt.build(self.words, SCRIPT, fps=30, max_chars=42, min_dwell=0.5)
        self.assertEqual([c["title"] for c in tl["chapters"]], ["Why maps lie", "Scale"])
        s1, s2, s3 = tl["shots"]
        self.assertEqual((s1["start"], s1["startFrame"]), (0.0, 0))
        self.assertEqual((s2["start"], s2["startFrame"]), (3.6, 108))  # word 9 at 9 * 0.4 s
        self.assertEqual(s1["end"], s2["start"])  # shots tile the timeline
        self.assertEqual(tl["chapters"][1]["startFrame"], s3["startFrame"])
        self.assertEqual(srt.count(" --> "), 5)
        self.assertIn("1\n00:00:00,000 --> 00:00:02,000\nEvery map you have seen\n", srt)
        self.assertTrue(vtt.startswith("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nEvery map you have seen\n"))
        self.assertEqual(tl["warnings"], [w for w in tl["warnings"] if "chars/s" in w])  # only reading-speed notes

    def test_captions_never_overlap_and_video_holds_last_caption(self):
        tl, _, vtt = bt.build(self.words, SCRIPT, fps=30, max_chars=42, min_dwell=0.5)
        cues = [line.split(" --> ") for line in vtt.splitlines() if " --> " in line]
        for (_, end), (start, _) in zip(cues, cues[1:]):
            self.assertLessEqual(end, start)
        last_end = cues[-1][1]
        self.assertLessEqual(last_end, bt.ts(tl["duration"], "."))

    def test_missing_gap_and_short_dwell_warn(self):
        words = bt.load_words(timed(TEXT))  # no silence inserted
        tl, _, _ = bt.build(words, SCRIPT, fps=30, max_chars=42, min_dwell=2.0)
        joined = "\n".join(tl["warnings"])
        self.assertIn("'## gap 0.5' requested, audio pauses 0.05s", joined)
        self.assertIn("before the cut", joined)

    def test_long_silence_warns(self):
        words = bt.load_words(timed("one two", pause_after={0: 4.0}))
        tl, _, _ = bt.build(words, None, fps=30, max_chars=42, min_dwell=0.1)
        self.assertTrue(any("silence of" in w for w in tl["warnings"]))

    def test_no_script_splits_sentences_and_long_blocks(self):
        tl, _, _ = bt.build(self.words, None, fps=30, max_chars=42, min_dwell=0.1)
        self.assertEqual(len(tl["shots"]), 3)
        tl, _, _ = bt.build(bt.load_words(timed("aaaa bbbb cccc dddd")), None, fps=30, max_chars=5, min_dwell=0.1)
        self.assertEqual([b["text"] for b in blocks(tl)], ["aaaa bbbb", "cccc dddd"])

    def test_vtt_escapes_markup(self):
        words = bt.load_words(timed("R&D under <5 ms"))
        _, srt, vtt = bt.build(words, None, fps=30, max_chars=42, min_dwell=0.1)
        self.assertIn("R&amp;D under &lt;5 ms", vtt)
        self.assertIn("R&D under <5 ms", srt)

    def test_reading_speed_uses_on_screen_time(self):
        # Fast speech, but the caption stays up until the next one: readable.
        words = bt.load_words(timed("Scale changes everything. Next.", step=0.2, pause_after={2: 3.0}))
        tl, _, _ = bt.build(words, None, fps=30, max_chars=42, min_dwell=0.1)
        self.assertFalse([w for w in tl["warnings"] if "chars/s" in w], tl["warnings"])


class Helpers(unittest.TestCase):
    def test_timestamp_format(self):
        self.assertEqual(bt.ts(3723.456, ","), "01:02:03,456")

    def test_wrap(self):
        self.assertEqual(bt.wrap("short", 42), "short")
        self.assertEqual(bt.wrap("aaaa bbbb cccc dddd", 10), "aaaa bbbb\ncccc dddd")
        self.assertEqual(bt.wrap("supercalifragilistic", 5), "supercalifragilistic")


class Cli(unittest.TestCase):
    def run_main(self, argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            rc = bt.main(argv)
        return rc, out.getvalue()

    def test_writes_outputs_and_strict_exit(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "w.json").write_text(json.dumps(timed(TEXT)))
            (d / "s.txt").write_text(SCRIPT)
            args = [str(d / "w.json"), "--script", str(d / "s.txt"), "--out-dir", str(d / "out")]
            rc, out = self.run_main(args)
            self.assertEqual(rc, 0)
            self.assertIn("3 shots", out)
            for f in ("timeline.json", "captions.srt", "captions.vtt"):
                self.assertTrue((d / "out" / f).stat().st_size > 0)
            rc, _ = self.run_main(args + ["--strict"])
            self.assertEqual(rc, 1)  # missing gap warning

    def test_bad_input_returns_2(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.json"
            for payload in ("{}", "not json", json.dumps([{"word": "a", "start": [], "end": 1}])):
                p.write_text(payload)
                rc, out = self.run_main([str(p), "--out-dir", str(Path(d) / "o")])
                self.assertEqual(rc, 2, payload)
                self.assertIn("error:", out)


if __name__ == "__main__":
    unittest.main()
