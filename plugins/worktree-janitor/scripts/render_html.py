#!/usr/bin/env python3
"""render_html.py — self-contained HTML report for Worktree Janitor.

No external assets, no CDN, no network: the produced file opens offline from
`file://`. Renders two modes:

- `preview`  — what a `scan` found and what it would remove.
- `executed` — what a `clean` actually removed, failed on, or skipped.
"""

from __future__ import annotations

import html
import json
from typing import Callable

RISK_META = {
    "safe": ("Seguro", "safe"),
    "review": ("Revisar", "review"),
    "risky": ("Arriscado", "risky"),
    "keep": ("Manter", "keep"),
    "protected": ("Protegido", "protected"),
}

STATUS_META = {
    "removed": ("Removida", "safe"),
    "failed": ("Falhou", "risky"),
    "skipped": ("Pulada", "keep"),
}

TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  color-scheme: light dark;
  --bg: #f6f6f7;
  --panel: #ffffff;
  --border: rgba(0,0,0,.09);
  --text: #16181d;
  --muted: #6b7280;
  --safe: #16a34a;
  --review: #d97706;
  --risky: #dc2626;
  --keep: #64748b;
  --protected: #2563eb;
  --shadow: 0 1px 2px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.05);
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d0e11;
    --panel: #16181d;
    --border: rgba(255,255,255,.1);
    --text: #e9eaee;
    --muted: #9aa1ad;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.35);
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 40px 24px 72px;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.55 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 1160px; margin: 0 auto; }
header { margin-bottom: 28px; }
h1 { margin: 0 0 6px; font-size: 27px; letter-spacing: -.02em; font-weight: 650; }
.sub { color: var(--muted); font-size: 13px; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin: 26px 0; }
.card { background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 16px 18px; box-shadow: var(--shadow); }
.card .label { font-size: 11px; text-transform: uppercase; letter-spacing: .07em; color: var(--muted); }
.card .value { font-size: 27px; font-weight: 640; margin-top: 6px; letter-spacing: -.02em; }
.card .value small { font-size: 13px; font-weight: 500; color: var(--muted); }
section { background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 20px 22px; margin-bottom: 20px; box-shadow: var(--shadow); }
section h2 { margin: 0 0 14px; font-size: 15px; font-weight: 640; letter-spacing: -.01em; }
.bars { display: grid; gap: 10px; }
.bar-row { display: grid; grid-template-columns: 220px 1fr 64px; align-items: center; gap: 12px; font-size: 13px; }
.bar-track { background: color-mix(in srgb, var(--text) 8%, transparent); border-radius: 999px; height: 8px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; background: var(--protected); }
.bar-row .num { text-align: right; color: var(--muted); font-variant-numeric: tabular-nums; }
.toolbar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 14px; }
.toolbar input {
  flex: 1 1 240px; min-width: 200px; padding: 8px 12px; font: inherit; font-size: 13px;
  border: 1px solid var(--border); border-radius: 9px; background: var(--bg); color: var(--text);
}
.chip {
  border: 1px solid var(--border); background: var(--bg); color: var(--muted); cursor: pointer;
  border-radius: 999px; padding: 6px 13px; font: inherit; font-size: 12px;
}
.chip[aria-pressed="true"] { background: var(--text); color: var(--panel); border-color: transparent; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { text-align: left; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); padding: 0 10px 10px; }
td { padding: 11px 10px; border-top: 1px solid var(--border); vertical-align: top; }
td.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
th:nth-child(2), td:nth-child(2) { width: 36%; }
th:nth-child(6), td:nth-child(6) { width: 22%; }
.path { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace; font-size: 11.5px; color: var(--muted); word-break: break-all; }
.branch { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace; font-size: 12.5px; }
.tag { display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 11px; font-weight: 600; white-space: nowrap; }
.tag.safe { background: color-mix(in srgb, var(--safe) 16%, transparent); color: var(--safe); }
.tag.review { background: color-mix(in srgb, var(--review) 18%, transparent); color: var(--review); }
.tag.risky { background: color-mix(in srgb, var(--risky) 16%, transparent); color: var(--risky); }
.tag.keep { background: color-mix(in srgb, var(--keep) 18%, transparent); color: var(--keep); }
.tag.protected { background: color-mix(in srgb, var(--protected) 16%, transparent); color: var(--protected); }
pre {
  margin: 0; padding: 14px 16px; background: var(--bg); border: 1px solid var(--border);
  border-radius: 10px; overflow-x: auto; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px;
}
.note { font-size: 12.5px; color: var(--muted); margin-top: 10px; }
.warn { border-left: 3px solid var(--review); padding-left: 12px; }
dl.legend { display: grid; grid-template-columns: max-content 1fr; gap: 8px 16px; margin: 0; font-size: 13px; }
dl.legend dt { font-weight: 600; }
dl.legend dd { margin: 0; color: var(--muted); }
footer { color: var(--muted); font-size: 12px; text-align: center; margin-top: 30px; }
.empty { color: var(--muted); font-size: 13px; padding: 14px 0; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>__HEADING__</h1>
    <div class="sub">__SUBTITLE__</div>
  </header>

  <div class="cards">__CARDS__</div>

  __EXEC_SECTION__

  <section>
    <h2>Worktrees</h2>
    <div class="toolbar">
      <input id="q" type="search" placeholder="Filtrar por projeto, branch, caminho ou motivo…" aria-label="Filtrar worktrees">
      __CHIPS__
    </div>
    <div class="note">__SELECTION_NOTE__</div>
    <table>
      <thead>
        <tr>
          <th>#</th><th>Projeto</th><th>Branch</th><th>Harness</th>
          <th>Classificação</th><th>Motivo</th><th class="num">Tamanho</th><th class="num">Idade</th>
        </tr>
      </thead>
      <tbody id="rows">__ROWS__</tbody>
    </table>
    <div class="empty" id="noresults" hidden>Nenhuma linha corresponde ao filtro.</div>
  </section>

  <section>
    <h2>Distribuição</h2>
    <div class="bars">__BARS__</div>
  </section>

  __UNDO_SECTION__

  <section>
    <h2>Critérios de classificação</h2>
    <dl class="legend">__LEGEND__</dl>
  </section>

  <footer>Worktree Janitor v__VERSION__ · gerado em __GENERATED__</footer>
</div>
<script>
(function () {
  var q = document.getElementById('q');
  var rows = Array.prototype.slice.call(document.querySelectorAll('#rows tr'));
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var none = document.getElementById('noresults');
  var active = 'all';

  function apply() {
    var term = q.value.trim().toLowerCase();
    var shown = 0;
    rows.forEach(function (row) {
      var matchesRisk = active === 'all' || row.dataset.risk === active;
      var matchesTerm = !term || row.dataset.search.indexOf(term) !== -1;
      var visible = matchesRisk && matchesTerm;
      row.hidden = !visible;
      if (visible) shown++;
    });
    none.hidden = shown !== 0;
  }

  q.addEventListener('input', apply);
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      active = chip.dataset.risk;
      chips.forEach(function (other) { other.setAttribute('aria-pressed', String(other === chip)); });
      apply();
    });
  });
  apply();
})();
</script>
</body>
</html>
"""


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _card(label: str, value: str, suffix: str = "") -> str:
    tail = f" <small>{esc(suffix)}</small>" if suffix else ""
    return f'<div class="card"><div class="label">{esc(label)}</div><div class="value">{esc(value)}{tail}</div></div>'


def _bars(counts: dict[str, int], total: int) -> str:
    if not counts:
        return '<div class="empty">Sem dados.</div>'
    rows = []
    biggest = max(counts.values()) or 1
    for key, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        pct = round(100 * count / biggest)
        share = round(100 * count / total) if total else 0
        rows.append(
            f'<div class="bar-row"><div>{esc(key)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>'
            f'<div class="num">{count} · {share}%</div></div>'
        )
    return "".join(rows)


def render_report(
    data: dict,
    reason_labels: dict[str, str],
    human_bytes: Callable[[int], str],
) -> str:
    executed = data.get("mode") == "executed"
    items = data.get("items", [])
    summary = data.get("summary") or {}
    by_risk = summary.get("byRisk", {})
    status_by_id = {r["id"]: r for r in data.get("results", []) if "id" in r}

    # ---- cards ----------------------------------------------------------- #
    if executed:
        cards = "".join([
            _card("Removidas", str(data.get("removedCount", 0))),
            _card("Falhas", str(data.get("failedCount", 0))),
            _card("Puladas", str(data.get("skippedCount", 0))),
            _card("Espaço liberado", human_bytes(data.get("reclaimedBytes", 0))),
            _card("Repositórios", str(data.get("reposScanned", 0))),
        ])
        heading = "Limpeza de worktrees concluída"
        subtitle = (
            f"{data.get('removedCount', 0)} worktree(s) removida(s) em "
            f"{data.get('reposScanned', 0)} repositório(s) · política de branch: "
            f"{data.get('branchPolicy', 'auto')}"
        )
    else:
        cards = "".join([
            _card("Worktrees", str(summary.get("total", len(items)))),
            _card("Candidatas", str(summary.get("candidates", 0))),
            _card("Seguras", str(by_risk.get("safe", 0))),
            _card("Arriscadas", str(by_risk.get("risky", 0))),
            _card("Recuperável", human_bytes(summary.get("reclaimableBytes", 0))),
        ])
        heading = "Prévia de limpeza de worktrees"
        subtitle = (
            f"Varredura read-only em {data.get('reposScanned', 0)} repositório(s) · "
            f"raízes: {', '.join(data.get('roots', [])) or '—'} · stale ≥ {data.get('staleDays', '—')} dias"
        )

    # ---- rows ------------------------------------------------------------ #
    row_html = []
    for item in items:
        risk = item.get("risk", "keep")
        label, css = RISK_META.get(risk, (risk, "keep"))
        if executed:
            outcome = status_by_id.get(item["id"])
            if outcome:
                label, css = STATUS_META.get(outcome.get("status", ""), (label, css))
        reason = reason_labels.get(item.get("reason"), item.get("reason", ""))
        harness = item.get("harness") or ("agente" if item.get("agentManaged") else "humano")
        age = f"{item['ageDays']}d" if item.get("ageDays") is not None else "—"
        size = human_bytes(item.get("sizeBytes", 0)) if item.get("sizeBytes") else "—"
        search = " ".join(str(part).lower() for part in [
            item.get("repoName"), item.get("branch"), item.get("path"), reason, harness, label,
        ] if part)
        outcome = status_by_id.get(item["id"], {}) if executed else {}
        reason_cell = esc(reason)
        if outcome.get("error"):
            reason_cell += f'<div class="path">⚠ {esc(outcome["error"])}</div>'
        if outcome.get("branchDeleted"):
            reason_cell += f'<div class="path">branch local removida: {esc(item.get("branch"))}</div>'
        elif outcome.get("branchError"):
            reason_cell += f'<div class="path">⚠ branch não removida: {esc(outcome["branchError"])}</div>'
        row_html.append(
            f'<tr data-risk="{esc(risk)}" data-search="{esc(search)}">'
            f'<td class="num">{esc(item.get("id"))}</td>'
            f'<td>{esc(item.get("repoName"))}<div class="path">{esc(item.get("path"))}</div></td>'
            f'<td class="branch">{esc(item.get("branch") or "(detached)")}</td>'
            f'<td>{esc(harness)}</td>'
            f'<td><span class="tag {css}">{esc(label)}</span></td>'
            f'<td>{reason_cell}</td>'
            f'<td class="num">{esc(size)}</td>'
            f'<td class="num">{esc(age)}</td>'
            f"</tr>"
        )
    rows = "".join(row_html) or '<tr><td colspan="8" class="empty">Nenhuma worktree encontrada.</td></tr>'

    chips = ['<button class="chip" data-risk="all" aria-pressed="true" type="button">Todas</button>']
    for key, (label, _css) in RISK_META.items():
        if by_risk.get(key):
            chips.append(
                f'<button class="chip" data-risk="{esc(key)}" aria-pressed="false" type="button">'
                f'{esc(label)} ({by_risk[key]})</button>'
            )

    # ---- bars ------------------------------------------------------------ #
    total = summary.get("total", len(items)) or 1
    by_reason = {reason_labels.get(k, k): v for k, v in (summary.get("byReason") or {}).items()}
    bars = (
        '<div style="margin-bottom:6px;font-size:12px;color:var(--muted)">Por motivo</div>'
        + _bars(by_reason, total)
        + '<div style="margin:16px 0 6px;font-size:12px;color:var(--muted)">Por harness</div>'
        + _bars(summary.get("byHarness") or {}, total)
    )

    # ---- executed detail -------------------------------------------------- #
    exec_section = ""
    if executed:
        failures = [r for r in data.get("results", []) if r.get("status") in ("failed", "skipped")]
        if failures:
            lines = "".join(
                f'<li><strong>[{esc(r.get("id"))}]</strong> {esc(r.get("path"))} — '
                f'{esc(r.get("status"))}: {esc(r.get("error") or "sem detalhe")}</li>'
                for r in failures
            )
            exec_section = f'<section class="warn"><h2>Não removidas</h2><ul>{lines}</ul></section>'

    # ---- undo ------------------------------------------------------------- #
    undo_section = ""
    if executed:
        commands = [c for r in data.get("results", []) for c in (r.get("undo") or [])]
        if commands:
            undo_section = (
                "<section><h2>Desfazer</h2>"
                f"<pre>{esc(chr(10).join(commands))}</pre>"
                '<div class="note warn">Restaura branches e worktrees removidas. '
                "Alterações não commitadas que existiam dentro das worktrees "
                "<strong>não</strong> são recuperáveis.</div></section>"
            )

    if executed:
        selection_note = (
            f"Seleção aplicada: ids {', '.join(str(i) for i in data.get('selectedIds', [])) or '—'}. "
            "Nada fora dessa lista foi tocado."
        )
    else:
        selection_note = (
            f"Pré-selecionadas por default: {by_risk.get('safe', 0)} worktree(s) <strong>segura(s)</strong>. "
            f"{by_risk.get('review', 0)} para revisar e {by_risk.get('risky', 0)} arriscada(s) exigem escolha "
            "explícita do id. Protegidas nunca são removidas."
        )

    legend = "".join(
        f"<dt>{esc(key)}</dt><dd>{esc(value)}</dd>" for key, value in reason_labels.items()
    )

    return (
        TEMPLATE
        .replace("__TITLE__", esc(heading))
        .replace("__HEADING__", esc(heading))
        .replace("__SUBTITLE__", esc(subtitle))
        .replace("__CARDS__", cards)
        .replace("__EXEC_SECTION__", exec_section)
        .replace("__CHIPS__", "".join(chips))
        .replace("__SELECTION_NOTE__", selection_note)
        .replace("__ROWS__", rows)
        .replace("__BARS__", bars)
        .replace("__UNDO_SECTION__", undo_section)
        .replace("__LEGEND__", legend)
        .replace("__VERSION__", esc(data.get("version", "1.0.0")))
        .replace("__GENERATED__", esc(data.get("generatedAt", "")))
    )


if __name__ == "__main__":  # pragma: no cover - manual rendering helper
    import sys

    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(render_report(payload, {}, lambda b: f"{b} B"))
