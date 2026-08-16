#!/usr/bin/env python3
"""Sync provider-matrix.json against live harness model catalogs.

Sources:
- OpenCode: `opencode models`
- Optional overrides via --seed JSON

Never invents models. Marks missing live models as status=stale and adds
newly observed OpenCode Zen/Go models as status=discovered (manual promote).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = PLUGIN_ROOT / "references" / "provider-matrix.json"


def run_opencode_models() -> list[str]:
    try:
        result = subprocess.run(
            ["opencode", "models"],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"WARN: opencode models unavailable: {exc}", file=sys.stderr)
        return []
    if result.returncode != 0:
        print(f"WARN: opencode models exit {result.returncode}: {result.stderr}", file=sys.stderr)
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip() and "/" in line]


def parse_model_ref(ref: str) -> tuple[str, str]:
    provider, model = ref.split("/", 1)
    return provider, model


def ensure_provider(catalog: dict, provider_id: str) -> dict:
    for provider in catalog["providers"]:
        if provider["id"] == provider_id:
            return provider
    provider = {
        "id": provider_id,
        "displayName": provider_id,
        "apiKeyEnv": f"{provider_id.upper().replace('-', '_')}_API_KEY",
        "docs": "https://opencode.ai/docs/models",
        "effortParameter": "model-specific",
        "models": [],
    }
    catalog["providers"].append(provider)
    return provider


def tier_guess(model_id: str) -> str:
    low = model_id.lower()
    if any(x in low for x in ("flash", "lite", "nano", "mini", "free", "luna", "haiku", "air")):
        return "budget"
    if any(x in low for x in ("opus", "sol", "pro", "max", "fable", "ultra")):
        return "quality"
    return "balanced"


def sync_opencode(catalog: dict, live: list[str]) -> dict:
    report = {"live": len(live), "added": [], "stale": [], "kept": []}
    live_by_provider: dict[str, set[str]] = {}
    for ref in live:
        provider, model = parse_model_ref(ref)
        if provider not in {"opencode", "opencode-go"}:
            continue
        live_by_provider.setdefault(provider, set()).add(model)

    for provider_id, models in live_by_provider.items():
        provider = ensure_provider(catalog, provider_id)
        known = {m["id"]: m for m in provider["models"]}
        for model_id in sorted(models):
            if model_id in known:
                known[model_id]["status"] = "stable"
                report["kept"].append(f"{provider_id}/{model_id}")
            else:
                entry = {
                    "id": model_id,
                    "displayName": model_id,
                    "tier": tier_guess(model_id),
                    "status": "discovered",
                    "efforts": ["low", "medium", "high"],
                    "capabilities": ["discovered-via-opencode-models"],
                }
                provider["models"].append(entry)
                report["added"].append(f"{provider_id}/{model_id}")
        for model_id, entry in known.items():
            if model_id not in models and entry.get("status") != "discovered":
                entry["status"] = "stale"
                report["stale"].append(f"{provider_id}/{model_id}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--write", action="store_true", help="persist catalog updates")
    parser.add_argument("--json", action="store_true", help="print machine report")
    args = parser.parse_args()

    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    live = run_opencode_models()
    report = {"date": date.today().isoformat(), "opencode": sync_opencode(catalog, live)}
    catalog["updated"] = date.today().isoformat()

    if args.write:
        args.catalog.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
        # re-validate
        validator = PLUGIN_ROOT / "scripts" / "validate_catalog.py"
        result = subprocess.run([sys.executable, str(validator), "--catalog", str(args.catalog)], capture_output=True, text=True)
        report["validate"] = {"code": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        oc = report["opencode"]
        print(f"date={report['date']}")
        print(f"opencode live={oc['live']} kept={len(oc['kept'])} added={len(oc['added'])} stale={len(oc['stale'])}")
        if oc["added"]:
            print("added:")
            for item in oc["added"][:40]:
                print(f"  + {item}")
        if oc["stale"]:
            print("stale:")
            for item in oc["stale"][:40]:
                print(f"  ~ {item}")
        if args.write:
            print(f"wrote {args.catalog}")
            print(report.get("validate", {}).get("stdout", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
