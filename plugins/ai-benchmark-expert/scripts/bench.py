#!/usr/bin/env python3
"""ai-benchmark-expert runner.

Gives the SAME task to many providers/models (headless CLI subagents), runs
deterministic checks on what each one produced, optionally scores it with a
blind LLM judge against a weighted rubric, and writes `results.json` plus a
self-contained interactive `report.html`.

    bench.py run  suite.json [-o out/] [--targets a,b] [--tasks x] [--repeat N]
                             [--parallel N] [--no-judge] [--resume] [--dry-run]
    bench.py summary out/results.json        # terminal leaderboard (markdown)

Python 3.9+, standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shlex
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "ai-benchmark-expert/results@1"

# 8 weighted dimensions (sum = 100), modelled on the akitaonrails coding rubric.
DEFAULT_RUBRIC = [
    {"id": "correctness", "label": "Correctness", "weight": 25,
     "desc": "Does the result actually work and do what was asked, without bugs?"},
    {"id": "completeness", "label": "Completeness", "weight": 15,
     "desc": "Are all requested parts delivered, nothing stubbed or skipped?"},
    {"id": "instructions", "label": "Instruction following", "weight": 15,
     "desc": "Respects every explicit constraint (stack, format, scope, no extras)."},
    {"id": "quality", "label": "Code quality", "weight": 10,
     "desc": "Readable, idiomatic, well structured, no dead code."},
    {"id": "testing", "label": "Tests & verification", "weight": 10,
     "desc": "Meaningful tests or evidence that the result was verified."},
    {"id": "robustness", "label": "Robustness", "weight": 10,
     "desc": "Edge cases, input validation, error handling."},
    {"id": "security", "label": "Security & hygiene", "weight": 10,
     "desc": "No leaked secrets, unsafe calls or risky defaults."},
    {"id": "clarity", "label": "Clarity", "weight": 5,
     "desc": "Clear final answer / docs; honest about limitations."},
]
TIERS = [(80, "A"), (60, "B"), (40, "C"), (0, "D")]
DEFAULT_WEIGHTS = {"checks": 0.6, "judge": 0.4}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
             ".next", "target", ".pytest_cache", ".mypy_cache"}
EXCERPT = 4000


# ---------------------------------------------------------------- parsing ---
def _json_lines(text: str):
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>\s*", "", text or "", flags=re.S).strip()


def parse_output(kind: str, stdout: str) -> dict:
    """Extract final text + usage from a CLI's stdout. Unknown fields stay None."""
    out = {"text": stdout.strip(), "input_tokens": None, "output_tokens": None, "cost_usd": None}
    try:
        if kind == "claude-json":
            d = list(_json_lines(stdout))[-1]
            u = d.get("usage") or {}
            out["text"] = d.get("result") or ""
            out["input_tokens"] = sum(u.get(k) or 0 for k in (
                "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
            out["output_tokens"] = u.get("output_tokens")
            out["cost_usd"] = d.get("total_cost_usd")
        elif kind == "codex-jsonl":
            texts, tin, tout = [], 0, 0
            for d in _json_lines(stdout):
                item = d.get("item") or {}
                if d.get("type") == "item.completed" and item.get("type") == "agent_message":
                    texts.append(item.get("text") or "")
                if d.get("type") == "turn.completed":
                    u = d.get("usage") or {}
                    tin += u.get("input_tokens") or 0
                    tout += u.get("output_tokens") or 0
            out.update(text=texts[-1] if texts else "", input_tokens=tin, output_tokens=tout)
        elif kind == "gemini-json":
            d = json.loads(stdout[stdout.index("{"):])
            out["text"] = d.get("response") or ("ERROR: " + (d.get("error") or {}).get("message", "") if d.get("error") else "")
            models = ((d.get("stats") or {}).get("models") or {}).values()
            toks = [m.get("tokens") or {} for m in models]
            out["input_tokens"] = sum(t.get("prompt") or 0 for t in toks)
            out["output_tokens"] = sum((t.get("candidates") or 0) + (t.get("thoughts") or 0) for t in toks)
        elif kind == "opencode-json":
            texts, tin, tout, cost = [], 0, 0, 0.0
            for d in _json_lines(stdout):
                part = d.get("part") or {}
                if d.get("type") == "text":
                    texts.append(part.get("text") or "")
                if d.get("type") == "step_finish":
                    t = part.get("tokens") or {}
                    c = t.get("cache") or {}
                    tin += (t.get("input") or 0) + (c.get("read") or 0) + (c.get("write") or 0)
                    tout += (t.get("output") or 0) + (t.get("reasoning") or 0)
                    cost += part.get("cost") or 0
            out.update(text="\n".join(texts), input_tokens=tin, output_tokens=tout, cost_usd=cost)
    except (ValueError, IndexError, AttributeError, TypeError):
        pass  # keep the raw stdout as text; usage stays unknown
    out["text"] = strip_think(out["text"])
    return out


# ---------------------------------------------------------------- running ---
def render_cmd(template: str, prompt: str, prompt_file: Path, workdir: Path, model: str):
    """Fill placeholders. Returns (command, stdin_text_or_None)."""
    uses_prompt = "{prompt}" in template or "{prompt_file}" in template
    cmd = (template.replace("{prompt_file}", shlex.quote(str(prompt_file)))
                   .replace("{prompt}", shlex.quote(prompt))
                   .replace("{workdir}", shlex.quote(str(workdir)))
                   .replace("{model}", model or ""))
    return cmd, (None if uses_prompt else prompt)


def sh(cmd: str, cwd: Path, timeout: float, stdin: str | None = None, env: dict | None = None):
    """Run a shell command in its own process group. Returns (rc, stdout, stderr, secs, timed_out)."""
    t0 = time.monotonic()
    p = subprocess.Popen(cmd, shell=True, cwd=str(cwd), env=env, text=True,
                         stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        so, se = p.communicate(stdin, timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        so, se = p.communicate()
        timed_out = True
    return p.returncode, so or "", se or "", time.monotonic() - t0, timed_out


def build_env(target: dict) -> dict:
    env = dict(os.environ)
    for k in target.get("unset_env", []):
        env.pop(k, None)
    env.update({k: str(v) for k, v in (target.get("env") or {}).items()})
    return env


def run_one(cfg: dict, base: Path, out: Path, target: dict, task: dict, rep: int, resume: bool) -> dict:
    rdir = out / "runs" / target["id"] / task["id"] / f"r{rep}"
    rjson = rdir / "run.json"
    if resume and rjson.exists():
        return json.loads(rjson.read_text())
    if rdir.exists():
        shutil.rmtree(rdir)
    work = rdir / "work"
    if task.get("fixture"):
        shutil.copytree(base / task["fixture"], work)
    else:
        work.mkdir(parents=True)
    if shutil.which("git"):  # own repo root: agents stay inside, judge sees a clean baseline
        subprocess.run("git init -q && git add -A && git -c user.name=bench -c user.email=bench@localhost "
                       "commit -qm baseline --allow-empty", shell=True, cwd=work, capture_output=True)
    prompt_file = rdir / "prompt.md"
    prompt_file.write_text(task["prompt"])
    cmd, stdin = render_cmd(target["cmd"], task["prompt"], prompt_file, work, target.get("model", ""))
    timeout = task.get("timeout") or target.get("timeout") or cfg.get("timeout", 900)
    rc, so, se, secs, timed_out = sh(cmd, work, timeout, stdin, build_env(target))
    (rdir / "stdout.txt").write_text(so)
    (rdir / "stderr.txt").write_text(se)
    parsed = parse_output(target.get("parse", "text"), so)
    answer = rdir / "answer.txt"
    answer.write_text(parsed["text"])

    price = target.get("price")
    if parsed["cost_usd"] is None and price and parsed["input_tokens"] is not None:
        parsed["cost_usd"] = (parsed["input_tokens"] * price.get("input", 0)
                              + (parsed["output_tokens"] or 0) * price.get("output", 0)) / 1e6

    checks = []
    check_env = dict(os.environ, BENCH_ANSWER=str(answer), BENCH_WORKDIR=str(work), BENCH_SUITE_DIR=str(base))
    for c in task.get("checks", []):
        crc, cso, cse, csecs, cto = sh(c["cmd"], work, c.get("timeout", 300), env=check_env)
        checks.append({"name": c.get("name", c["cmd"]), "passed": crc == 0 and not cto,
                       "seconds": round(csecs, 2), "output": (cso + cse)[-1500:]})

    status = "timeout" if timed_out else ("ok" if rc == 0 else "error")
    run = {
        "target": target["id"], "task": task["id"], "rep": rep, "status": status, "exit_code": rc,
        "seconds": round(secs, 2), "input_tokens": parsed["input_tokens"],
        "output_tokens": parsed["output_tokens"], "cost_usd": parsed["cost_usd"],
        "answer_excerpt": parsed["text"][:EXCERPT], "stderr_tail": se[-1500:],
        "checks": checks, "judge": None, "dir": str(rdir.relative_to(out)),
    }
    rjson.write_text(json.dumps(run, indent=2))
    mark = "✓" if status == "ok" else "✗"
    print(f"  {mark} {target['id']:<24} {task['id']:<20} r{rep}  {secs:6.1f}s  "
          f"checks {sum(c['passed'] for c in checks)}/{len(checks)}", file=sys.stderr)
    return run


# ----------------------------------------------------------------- judging ---
def snapshot(work: Path, budget: int = 40_000, per_file: int = 8_000) -> str:
    """Text dump of the files a target produced, for the judge."""
    parts, used = [], 0
    for path in sorted(work.rglob("*")):
        if any(p in SKIP_DIRS for p in path.relative_to(work).parts) or not path.is_file():
            continue
        try:
            body = path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        chunk = f"--- {path.relative_to(work)} ---\n{body[:per_file]}\n"
        if used + len(chunk) > budget:
            parts.append(f"--- (truncated: more files omitted) ---")
            break
        parts.append(chunk)
        used += len(chunk)
    return "".join(parts) or "(no files produced)"


def judge_prompt(task: dict, rubric: list, run: dict, out: Path) -> str:
    dims = "\n".join(f'- "{d["id"]}" ({d["label"]}, weight {d["weight"]}): {d["desc"]}' for d in rubric)
    checks = "\n".join(f'- {c["name"]}: {"PASS" if c["passed"] else "FAIL"}' for c in run["checks"]) or "- (none)"
    answer = (out / run["dir"] / "answer.txt").read_text()[:12_000]
    files = snapshot(out / run["dir"] / "work")
    keys = ", ".join(f'"{d["id"]}": <0-10>' for d in rubric)
    return f"""You are a strict, impartial benchmark judge. The submission is anonymous;
judge only what is in front of you. Do not reward length or confidence.

# Task given to the model
{task["prompt"]}

# Rubric (score each dimension 0-10, 10 = flawless)
{dims}

# Automated check results
{checks}

# Model's final answer
{answer or "(empty)"}

# Files the model produced
{files}

Reply with ONLY one JSON object, no prose before or after:
{{"scores": {{{keys}}}, "notes": "<=2 sentences: the most important strengths and defects"}}"""


def extract_json(text: str) -> dict | None:
    for m in re.finditer(r"\{.*\}", text, flags=re.S):
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
    return None


def judge_one(cfg: dict, out: Path, task: dict, rubric: list, run: dict) -> dict:
    jcfg = cfg["judge"]
    jdir = out / run["dir"] / "judge"
    jdir.mkdir(exist_ok=True)
    prompt = judge_prompt(task, rubric, run, out)
    pfile = jdir / "prompt.md"
    pfile.write_text(prompt)
    cmd, stdin = render_cmd(jcfg["cmd"], prompt, pfile, jdir, jcfg.get("model", ""))
    rc, so, se, secs, _ = sh(cmd, jdir, jcfg.get("timeout", 300), stdin, build_env(jcfg))
    (jdir / "stdout.txt").write_text(so)
    data = extract_json(parse_output(jcfg.get("parse", "text"), so)["text"]) or {}
    raw = data.get("scores") or {}
    scores = {}
    for d in rubric:
        try:
            scores[d["id"]] = max(0.0, min(10.0, float(raw[d["id"]])))
        except (KeyError, TypeError, ValueError):
            pass
    if len(scores) != len(rubric):
        run["judge"] = {"error": f"judge returned unparseable scores (rc={rc})", "notes": so[-500:]}
    else:
        total = sum(d["weight"] for d in rubric)
        score = sum(scores[d["id"]] * d["weight"] for d in rubric) / total * 10
        run["judge"] = {"scores": scores, "score": round(score, 1), "notes": str(data.get("notes", ""))[:600],
                        "seconds": round(secs, 1)}
    (out / run["dir"] / "run.json").write_text(json.dumps(run, indent=2))
    return run


# -------------------------------------------------------------- scoring ---
def tier(score: float | None) -> str | None:
    if score is None:
        return None
    return next(t for floor, t in TIERS if score >= floor)


def run_score(run: dict, weights: dict) -> float:
    """0-100. Checks pass-rate and judge score blended by `weights`; missing parts drop out."""
    parts = []
    if run["checks"]:
        parts.append((weights["checks"], 100 * sum(c["passed"] for c in run["checks"]) / len(run["checks"])))
    j = run.get("judge") or {}
    if j.get("score") is not None:
        parts.append((weights["judge"], j["score"]))
    if not parts:  # no checks, no judge: did it at least finish?
        return 100.0 if run["status"] == "ok" else 0.0
    if run["status"] == "timeout":
        return 0.0
    return sum(w * s for w, s in parts) / sum(w for w, _ in parts)


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def _sum(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) if xs else None


def aggregate(runs: list, rubric: list) -> dict:
    by_rep: dict = {}
    for r in runs:
        by_rep.setdefault(r["rep"], []).append(r["score"])
    rep_means = [sum(v) / len(v) for v in by_rep.values()]
    checks = [c["passed"] for r in runs for c in r["checks"]]
    judged = [r["judge"]["scores"] for r in runs if (r.get("judge") or {}).get("scores")]
    jscores = [r["judge"]["score"] for r in runs if (r.get("judge") or {}).get("score") is not None]
    score = _mean(r["score"] for r in runs)
    cost = _sum(r["cost_usd"] for r in runs)
    return {
        "score": round(score, 1) if score is not None else None,
        "score_std": round(statistics.stdev(rep_means), 1) if len(rep_means) > 1 else None,
        "tier": tier(score),
        "runs": len(runs),
        "failures": sum(r["status"] != "ok" for r in runs),
        "pass_rate": round(100 * sum(checks) / len(checks), 1) if checks else None,
        "judge": round(_mean(jscores), 1) if jscores else None,
        "dims": {d["id"]: round(_mean(j.get(d["id"]) for j in judged), 1) for d in rubric} if judged else {},
        "seconds": round(_sum(r["seconds"] for r in runs) or 0, 1),
        "seconds_mean": round(_mean(r["seconds"] for r in runs) or 0, 1),
        "input_tokens": _sum(r["input_tokens"] for r in runs),
        "output_tokens": _sum(r["output_tokens"] for r in runs),
        "cost_usd": round(cost, 4) if cost is not None else None,
        "cost_complete": all(r["cost_usd"] is not None for r in runs),
    }


def summarize(results: dict) -> dict:
    """{"*": {target: agg}, "<task>": {target: agg}} — the report reads only this."""
    weights = {**DEFAULT_WEIGHTS, **(results.get("weights") or {})}
    for r in results["runs"]:
        r["score"] = round(run_score(r, weights), 1)
    out = {}
    for scope in ["*"] + [t["id"] for t in results["tasks"]]:
        out[scope] = {}
        for tg in results["targets"]:
            rs = [r for r in results["runs"] if r["target"] == tg["id"] and scope in ("*", r["task"])]
            if rs:
                out[scope][tg["id"]] = aggregate(rs, results["rubric"])
    return out


def leaderboard_md(results: dict) -> str:
    summ = results["summary"]["*"]
    label = {t["id"]: t.get("label", t["id"]) for t in results["targets"]}
    rows = sorted(summ.items(), key=lambda kv: -(kv[1]["score"] or 0))
    lines = [f"## {results['name']}", "",
             "| # | Model | Score | Tier | Checks | Time | Tokens (in/out) | Cost |",
             "|---|---|---|---|---|---|---|---|"]
    for i, (tid, a) in enumerate(rows, 1):
        std = f" ±{a['score_std']}" if a["score_std"] is not None else ""
        toks = f"{a['input_tokens'] or '—'}/{a['output_tokens'] or '—'}"
        cost = f"${a['cost_usd']:.4f}" if a["cost_usd"] is not None else "—"
        pr = f"{a['pass_rate']}%" if a["pass_rate"] is not None else "—"
        lines.append(f"| {i} | {label[tid]} | {a['score']}{std} | {a['tier']} | {pr} | {a['seconds']}s | {toks} | {cost} |")
    return "\n".join(lines)


# ------------------------------------------------------------------ main ---
def cmd_run(args) -> int:
    cfg_path = Path(args.config).resolve()
    cfg = json.loads(cfg_path.read_text())
    base = cfg_path.parent
    # Default outside any repo, so agents under test cannot wander into a parent project.
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = Path(args.out or Path(tempfile.gettempdir()) / "ai-benchmark" / f"{cfg_path.stem}-{stamp}").resolve()
    rubric = cfg.get("rubric") or DEFAULT_RUBRIC
    pick = lambda items, sel: [i for i in items if not sel or i["id"] in sel.split(",")]
    targets, tasks = pick(cfg["targets"], args.targets), pick(cfg["tasks"], args.tasks)
    repeat = args.repeat or cfg.get("repeat", 1)
    jobs = [(tg, tk, r) for r in range(1, repeat + 1) for tk in tasks for tg in targets]
    if not jobs:
        print("nothing to run: check --targets/--tasks", file=sys.stderr)
        return 2

    if args.dry_run:
        for tg, tk, r in jobs:
            cmd, stdin = render_cmd(tg["cmd"], tk["prompt"], Path("<prompt.md>"), Path("<workdir>"), tg.get("model", ""))
            print(f"[{tg['id']} × {tk['id']} r{r}] {cmd[:200]}{'  <stdin: prompt>' if stdin else ''}")
        return 0

    out.mkdir(parents=True, exist_ok=True)
    print(f"▶ {len(targets)} targets × {len(tasks)} tasks × {repeat} reps = {len(jobs)} runs → {out}", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=args.parallel or cfg.get("parallel", 4)) as pool:
        runs = list(pool.map(lambda j: run_one(cfg, base, out, j[0], j[1], j[2], args.resume), jobs))

    if cfg.get("judge") and not args.no_judge:
        task_by_id = {t["id"]: t for t in tasks}
        todo = [r for r in runs if task_by_id[r["task"]].get("judge", True) and r["status"] != "timeout"
                and not (args.resume and (r.get("judge") or {}).get("score") is not None)]
        print(f"⚖ judging {len(todo)} runs (blind)…", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=args.parallel or cfg.get("parallel", 4)) as pool:
            list(pool.map(lambda r: judge_one(cfg, out, task_by_id[r["task"]], rubric, r), todo))

    versions = {}
    for tg in targets:
        if tg.get("version_cmd"):
            rc, so, se, _, _ = sh(tg["version_cmd"], base, 30, env=build_env(tg))
            versions[tg["id"]] = (so or se).strip().splitlines()[0][:120] if (so or se).strip() else None

    results = {
        "schema": SCHEMA, "name": cfg.get("name", cfg_path.stem), "description": cfg.get("description", ""),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "environment": {"os": f"{platform.system()} {platform.release()}",
                        "python": platform.python_version(), "versions": versions},
        "repeat": repeat, "weights": {**DEFAULT_WEIGHTS, **(cfg.get("weights") or {})},
        "judge": {k: cfg["judge"].get(k) for k in ("label", "model")} if cfg.get("judge") and not args.no_judge else None,
        "rubric": rubric, "tiers": [{"min": f, "tier": t} for f, t in TIERS],
        "tasks": [{k: t.get(k) for k in ("id", "title", "category", "prompt")} | {"checks": [c.get("name", c["cmd"]) for c in t.get("checks", [])]} for t in tasks],
        "targets": [{k: t.get(k) for k in ("id", "label", "provider", "model", "harness")} for t in targets],
        "runs": runs,
    }
    results["summary"] = summarize(results)
    (out / "results.json").write_text(json.dumps(results, indent=2))

    sys.path.insert(0, str(Path(__file__).parent))
    from report import render  # noqa: E402
    html = out / "report.html"
    html.write_text(render(results))
    print(leaderboard_md(results))
    print(f"\nresults: {out / 'results.json'}\nreport:  {html}", file=sys.stderr)
    return 0


def cmd_summary(args) -> int:
    results = json.loads(Path(args.results).read_text())
    results["summary"] = summarize(results)
    print(leaderboard_md(results))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="bench.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run a suite and write results.json + report.html")
    r.add_argument("config")
    r.add_argument("-o", "--out")
    r.add_argument("--targets", help="comma-separated target ids")
    r.add_argument("--tasks", help="comma-separated task ids")
    r.add_argument("--repeat", type=int)
    r.add_argument("--parallel", type=int)
    r.add_argument("--no-judge", action="store_true")
    r.add_argument("--resume", action="store_true", help="reuse finished runs in --out")
    r.add_argument("--dry-run", action="store_true", help="print the command matrix only")
    r.set_defaults(fn=cmd_run)
    s = sub.add_parser("summary", help="print the leaderboard of a results.json")
    s.add_argument("results")
    s.set_defaults(fn=cmd_summary)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
