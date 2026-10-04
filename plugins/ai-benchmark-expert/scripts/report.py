#!/usr/bin/env python3
"""Render a results.json into ONE self-contained, shareable report.html.

No network, no CDN, no build step: the data is embedded as JSON and the charts
are drawn with inline SVG/HTML, so the file can be emailed, attached to a PR,
dropped in a gist or hosted as-is.

    report.py out/results.json [-o out/report.html]
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "report-template.html"


def render(results: dict) -> str:
    sys.path.insert(0, str(HERE))
    from bench import summarize  # noqa: E402

    results["summary"] = summarize(results)
    # `<` escaped as <: the JSON can never close or comment out its <script>.
    data = json.dumps(results, ensure_ascii=False).replace("<", "\\u003c")
    title = html.escape(results.get("name") or "AI benchmark")
    desc = html.escape(results.get("description") or "Same task, many models: score, cost and speed side by side.")
    return (TEMPLATE.read_text()
            .replace("__BENCH_TITLE__", title)
            .replace("__BENCH_DESC__", desc)
            .replace("/*__BENCH_DATA__*/", data))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("results")
    ap.add_argument("-o", "--out")
    args = ap.parse_args(argv)
    src = Path(args.results)
    dst = Path(args.out) if args.out else src.with_name("report.html")
    dst.write_text(render(json.loads(src.read_text())))
    print(dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
