#!/usr/bin/env python3
"""Resolve a smart-sub-agents route and render harness-specific artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from validate_catalog import DEFAULT_CATALOG, validate


PROFILE_TIERS = {"budget": "budget", "balanced": "balanced", "quality": "quality", "research": "quality"}
HARNESS_NAMES = ("claude-code", "codex", "opencode", "antigravity", "gemini-cli", "lemon-code")
HARNESS_PROVIDER_TOKENS = {"claude", "claude-code", "codex", "opencode", "antigravity", "gemini", "gemini-cli", "lemon-code"}


def load_catalog(path: Path) -> dict:
    catalog = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(catalog)
    if errors:
        raise ValueError("; ".join(errors))
    return catalog


def model_index(catalog: dict) -> dict[tuple[str, str], dict]:
    return {
        (provider["id"], model["id"]): {
            **model,
            "provider": provider["id"],
            "providerName": provider["displayName"],
            "effortParameter": provider["effortParameter"],
        }
        for provider in catalog["providers"]
        for model in provider["models"]
    }


def choose_for_profile(catalog: dict, provider_id: str, profile: str) -> str:
    target_tier = PROFILE_TIERS[profile]
    provider = next(p for p in catalog["providers"] if p["id"] == provider_id)
    candidates = [m for m in provider["models"] if m["tier"] == target_tier]
    if not candidates:
        candidates = provider["models"]
    return candidates[0]["id"]


def default_route(catalog: dict, harness: str, profile: str) -> dict:
    route = catalog["profiles"][profile]["routes"][harness].copy()
    return resolve_route(catalog, harness, profile, route["provider"], route["model"], None)


def resolve_route(catalog: dict, harness: str, profile: str, provider: str | None, model: str | None, effort: str | None) -> dict:
    if harness not in catalog["harnesses"]:
        raise ValueError(f"unknown harness: {harness}")
    aliases = {key.lower(): value for key, value in catalog.get("aliases", {}).items()}
    known_providers = {p["id"] for p in catalog["providers"]}
    provider = provider.strip().lower() if provider else None
    raw_model = model.strip() if model else None
    alias = aliases.get(raw_model.lower()) if raw_model else None
    if alias:
        if not provider or provider not in known_providers or provider in HARNESS_PROVIDER_TOKENS:
            provider = alias["provider"]
        elif provider != alias["provider"]:
            raise ValueError(f"provider {provider!r} conflicts with alias for {alias['provider']}/{alias['model']}")
        model = alias["model"]
    elif raw_model and "/" in raw_model and not provider:
        provider, model = raw_model.split("/", 1)

    if not provider:
        return default_route(catalog, harness, profile)
    if provider not in {p["id"] for p in catalog["providers"]}:
        raise ValueError(f"unknown provider: {provider}")
    model = model or choose_for_profile(catalog, provider, profile)
    if model.startswith(f"{provider}/"):
        model = model.split("/", 1)[1]
    entry = model_index(catalog).get((provider, model))
    if not entry:
        raise ValueError(f"unknown model: {provider}/{model}")
    selected_effort = effort or catalog["profiles"][profile]["effort"]
    if selected_effort not in entry["efforts"]:
        raise ValueError(f"effort {selected_effort!r} is not supported by {provider}/{model}; use one of {entry['efforts']}")
    native = native_effort(entry, selected_effort)
    return {
        "schema": "smart-sub-agents/ROUTE-MAP/v1",
        "profile": profile,
        "harness": harness,
        "provider": provider,
        "model": model,
        "modelRef": f"{provider}/{model}",
        "effort": selected_effort,
        "nativeEffort": native,
        "tier": entry["tier"],
        "status": entry["status"],
        "capabilities": entry["capabilities"],
        "effortParameter": entry["effortParameter"],
        "source": next(p["docs"] for p in catalog["providers"] if p["id"] == provider),
        "fallback": "openrouter/auto" if provider != "openrouter" else None,
    }


def native_effort(entry: dict, effort: str) -> str:
    parameter = entry["effortParameter"]
    if parameter.startswith("reasoning"):
        return f"reasoning_effort={effort}"
    if parameter.startswith("effort"):
        return f"effort={effort}"
    if parameter == "thinking-mode":
        return "thinking=true" if effort in {"high", "xhigh", "max", "ultra"} else "thinking=false"
    if parameter == "thinkingConfig/model-specific":
        return f"thinkingConfig={effort} (model-specific)"
    if parameter in {"selected-model-specific", "model-specific", "provider-specific"}:
        return f"{parameter}={effort}"
    if parameter == "managed":
        return f"managed-effort={effort}"
    return f"requested={effort}"


def agent_name(route: dict) -> str:
    return f"smart-{route['provider']}-{re.sub(r'[^a-z0-9]+', '-', route['model'].lower()).strip('-')}"


def render_claude(route: dict) -> str:
    native = route["provider"] == "anthropic"
    model = route["model"] if native else "inherit"
    note = "Native Anthropic route." if native else f"Provider {route['provider']} is not native to Claude Code; use the OpenCode handoff."
    return f"""---
name: {agent_name(route)}
description: Dynamic subagent route for {route['provider']}/{route['model']} at {route['effort']} effort.
model: {model}
effort: {route['effort']}
---

Route every delegated task through the selected model and return concise evidence.
{note}
Requested native mapping: {route['nativeEffort']}.
Do not invent provider availability or expose credentials.
"""


def render_codex(route: dict) -> str:
    native = route["provider"] == "openai"
    model = route["model"] if native else "gpt-5.6-terra"
    note = "Native OpenAI route." if native else f"Provider {route['provider']} is not native to Codex; use the OpenCode handoff."
    return f'''name = "{agent_name(route)}"
description = "Dynamic subagent route for {route['provider']}/{route['model']} at {route['effort']} effort."
model = "{model}"
model_reasoning_effort = "{route['effort']}"
developer_instructions = """
Use the selected route for bounded delegated work. Return evidence, changed files, and validation results.
{note}
Requested native mapping: {route['nativeEffort']}.
Do not invent provider availability or expose credentials.
"""
'''


def render_opencode(route: dict) -> str:
    agent = {
        "description": f"Dynamic subagent route for {route['modelRef']} at {route['effort']} effort. Native mapping: {route['nativeEffort']}.",
        "mode": "subagent",
        "model": route["modelRef"],
        "steps": 12 if route["effort"] in {"high", "xhigh", "max", "ultra"} else 6,
    }
    if route["provider"] == "openai":
        agent["reasoningEffort"] = route["effort"]
    return json.dumps({"$schema": "https://opencode.ai/config.json", "agent": {agent_name(route): agent}}, indent=2) + "\n"


def render_manifest(route: dict) -> str:
    return json.dumps({"route": route, "handoff": f"Delegate to {route['modelRef']} with {route['effort']} effort and preserve the native mapping."}, indent=2) + "\n"


def render(harness: str, route: dict) -> tuple[str, str]:
    if harness == "claude-code":
        return f"{agent_name(route)}.md", render_claude(route)
    if harness == "codex":
        return f"{agent_name(route)}.toml", render_codex(route)
    if harness == "opencode":
        return "opencode.json", render_opencode(route)
    return "route.json", render_manifest(route)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--harness", choices=[*HARNESS_NAMES, "all"], required=True)
    parser.add_argument("--profile", choices=["budget", "balanced", "quality", "research"], default="balanced")
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--effort", choices=["none", "low", "medium", "high", "xhigh", "max", "ultra"])
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--all-providers", action="store_true", help="render one route per provider for the selected harness")
    args = parser.parse_args()

    try:
        catalog = load_catalog(args.catalog)
        harnesses = HARNESS_NAMES if args.harness == "all" else (args.harness,)
        outputs: list[tuple[Path, str]] = []
        for harness in harnesses:
            if args.all_providers:
                routes = []
                for provider in catalog["providers"]:
                    model = choose_for_profile(catalog, provider["id"], args.profile)
                    routes.append(resolve_route(catalog, harness, args.profile, provider["id"], model, args.effort))
            elif args.provider or args.model or args.effort:
                routes = [resolve_route(catalog, harness, args.profile, args.provider, args.model, args.effort)]
            else:
                routes = [default_route(catalog, harness, args.profile)]
            for route in routes:
                filename, content = render(harness, route)
                path = Path(harness) / filename
                if len(routes) > 1:
                    path = Path(harness) / f"{agent_name(route)}.{filename.split('.', 1)[1]}"
                outputs.append((path, content))

        if args.output_dir:
            for relative, content in outputs:
                target = args.output_dir / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            print(f"OK: rendered {len(outputs)} artifact(s) under {args.output_dir}")
        else:
            for index, (relative, content) in enumerate(outputs):
                if index:
                    print("\n---")
                print(f"# {relative}")
                print(content, end="")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
