#!/usr/bin/env python3
"""Validate the smart-sub-agents provider/model matrix."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "references" / "provider-matrix.json"
SLUG = re.compile(r"^[a-z0-9]+(?:[._/-][a-z0-9]+)*$")
TIERS = {"budget", "balanced", "quality"}
DECISION_MODES = {"heuristic", "shadow", "advisory", "enforce"}
REQUIRED_HARNESSES = {"claude-code", "codex", "opencode", "antigravity", "gemini-cli", "lemon-code"}


def _object(value: object, path: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return {}
    return value


def validate(catalog: object) -> list[str]:
    errors: list[str] = []
    catalog = _object(catalog, "catalog", errors)
    if errors:
        return errors
    if catalog.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(catalog.get("updated", ""))):
        errors.append("updated must be an ISO date")

    efforts = set(catalog.get("efforts", []))
    required_efforts = {"low", "medium", "high", "max"}
    if not required_efforts <= efforts:
        errors.append(f"efforts must include {sorted(required_efforts)}")

    decision_routing = _object(catalog.get("decisionRouting", {}), "decisionRouting", errors)
    raw_modes = decision_routing.get("modes", [])
    modes = set(raw_modes) if isinstance(raw_modes, list) and all(isinstance(mode, str) for mode in raw_modes) else set()
    if modes != DECISION_MODES:
        errors.append(f"decisionRouting modes must equal {sorted(DECISION_MODES)}")
    if decision_routing.get("defaultMode") not in modes:
        errors.append("decisionRouting defaultMode must be a declared mode")
    score_contract = _object(decision_routing.get("scoreContract", {}), "decisionRouting scoreContract", errors)
    gate = score_contract.get("confidenceGate")
    if isinstance(gate, bool) or not isinstance(gate, (int, float)) or not 0 <= gate <= 1:
        errors.append("decisionRouting scoreContract: confidenceGate must be between 0 and 1")
    if score_contract.get("output") != "typed-option-probabilities":
        errors.append("decisionRouting scoreContract: output must be typed-option-probabilities")
    for field in ("lowConfidenceTier", "failureTier"):
        if score_contract.get(field) not in TIERS:
            errors.append(f"decisionRouting scoreContract: invalid {field}")
    latency = score_contract.get("maxAddedLatencyMs")
    if isinstance(latency, bool) or not isinstance(latency, int) or latency <= 0:
        errors.append("decisionRouting scoreContract: maxAddedLatencyMs must be a positive integer")
    if score_contract.get("requiresCalibration") is not True:
        errors.append("decisionRouting scoreContract: requiresCalibration must be true")
    shared_state = _object(decision_routing.get("sharedState", {}), "decisionRouting sharedState", errors)
    if shared_state.get("reusePrefix") is not True or shared_state.get("batchIndependentCriteria") is not True:
        errors.append("decisionRouting sharedState must enable prefix reuse and independent-criteria batching")
    safety_floor = _object(decision_routing.get("safetyFloor", {}), "decisionRouting safetyFloor", errors)
    tasks = safety_floor.get("tasks")
    if (
        not isinstance(tasks, list)
        or not tasks
        or any(not isinstance(task, str) or not task.strip() for task in tasks)
        or len(tasks) != len(set(tasks))
    ):
        errors.append("decisionRouting safetyFloor: tasks must be unique non-empty strings")
    if safety_floor.get("tier") not in TIERS:
        errors.append("decisionRouting safetyFloor: invalid tier")
    if safety_floor.get("effort") not in efforts:
        errors.append("decisionRouting safetyFloor: invalid effort")

    harnesses = catalog.get("harnesses", {})
    missing_harnesses = REQUIRED_HARNESSES - set(harnesses)
    if missing_harnesses:
        errors.append(f"missing harnesses: {sorted(missing_harnesses)}")

    providers = catalog.get("providers", [])
    provider_ids: set[str] = set()
    model_keys: set[tuple[str, str]] = set()
    models_by_key: dict[tuple[str, str], dict] = {}
    for provider in providers:
        provider_id = provider.get("id", "")
        if provider_id in provider_ids:
            errors.append(f"duplicate provider: {provider_id}")
        provider_ids.add(provider_id)
        if not SLUG.fullmatch(provider_id):
            errors.append(f"invalid provider id: {provider_id}")
        if not provider.get("docs", "").startswith("https://"):
            errors.append(f"{provider_id}: docs must be an https URL")
        for model in provider.get("models", []):
            model_id = model.get("id", "")
            key = (provider_id, model_id)
            if key in model_keys:
                errors.append(f"duplicate model: {provider_id}/{model_id}")
            model_keys.add(key)
            models_by_key[key] = model
            if not SLUG.fullmatch(model_id):
                errors.append(f"invalid model id: {provider_id}/{model_id}")
            if model.get("tier") not in TIERS:
                errors.append(f"{provider_id}/{model_id}: invalid tier")
            model_efforts = set(model.get("efforts", []))
            if not model_efforts or not model_efforts <= efforts:
                errors.append(f"{provider_id}/{model_id}: invalid effort list")
            if not model.get("capabilities"):
                errors.append(f"{provider_id}/{model_id}: capabilities are required")

    aliases = catalog.get("aliases", {})
    for alias, route in aliases.items():
        key = (route.get("provider", ""), route.get("model", ""))
        if key not in models_by_key:
            errors.append(f"alias {alias!r} points to unknown model {key[0]}/{key[1]}")

    for profile_name, profile in catalog.get("profiles", {}).items():
        if profile.get("effort") not in efforts:
            errors.append(f"profile {profile_name}: invalid effort")
        for harness, route in profile.get("routes", {}).items():
            if harness not in harnesses:
                errors.append(f"profile {profile_name}: unknown harness {harness}")
            key = (route.get("provider", ""), route.get("model", ""))
            if key not in models_by_key:
                errors.append(f"profile {profile_name}/{harness}: unknown model {key[0]}/{key[1]}")
            elif profile.get("effort") not in models_by_key[key].get("efforts", []):
                errors.append(f"profile {profile_name}/{harness}: effort unsupported by {key[0]}/{key[1]}")

    # Optional worker matrix (Claude canonical + per-harness families/lanes)
    worker_matrix = catalog.get("workerMatrix", {})
    for harness_id, matrix in worker_matrix.items():
        if harness_id not in harnesses:
            errors.append(f"workerMatrix: unknown harness {harness_id}")
            continue
        families = matrix.get("families", [])
        if "lanes" in matrix:
            for lane_id, lane in matrix["lanes"].items():
                families = families + lane.get("families", [])
        for family in families:
            key = (family.get("provider", ""), family.get("model", ""))
            if key not in models_by_key:
                errors.append(f"workerMatrix {harness_id}/{family.get('id')}: unknown model {key[0]}/{key[1]}")
                continue
            family_efforts = set(family.get("efforts", []))
            if not family_efforts or not family_efforts <= efforts:
                errors.append(f"workerMatrix {harness_id}/{family.get('id')}: invalid efforts")
            elif not family_efforts <= set(models_by_key[key].get("efforts", [])):
                errors.append(
                    f"workerMatrix {harness_id}/{family.get('id')}: effort not supported by {key[0]}/{key[1]}"
                )
            if family.get("tier") not in TIERS:
                errors.append(f"workerMatrix {harness_id}/{family.get('id')}: invalid tier")
            elif family.get("tier") != models_by_key[key].get("tier"):
                errors.append(
                    f"workerMatrix {harness_id}/{family.get('id')}: tier {family.get('tier')!r} does not match "
                    f"canonical tier {models_by_key[key].get('tier')!r} of {key[0]}/{key[1]} "
                    "(cost-tier mismatch — a mislabeled family can route budget-tier volume to a "
                    "quality-priced model or vice versa)"
                )

    task_routing = catalog.get("taskRouting", {})
    for task_name, route in task_routing.items():
        if route.get("tier") not in TIERS:
            errors.append(f"taskRouting {task_name}: invalid tier")
        if route.get("effort") not in efforts:
            errors.append(f"taskRouting {task_name}: invalid effort")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read catalog: {exc}", file=sys.stderr)
        return 1

    errors = validate(catalog)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {len(catalog['providers'])} providers, {sum(len(p['models']) for p in catalog['providers'])} models, {len(catalog['harnesses'])} harnesses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
