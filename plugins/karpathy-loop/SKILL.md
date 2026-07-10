---
name: karpathy-loop
description: Executes autonomous Loop Engineering cycles (Autoresearch) for continuous code and metric optimization.
version: 2.0.0
---

# Karpathy Loop (Autoresearch)

Implements **Loop Engineering** — the practice of delegating experimentation loops to AI agents that iteratively modify code, run experiments, evaluate metrics, and decide to keep or revert changes. Based on Andrej Karpathy's Autoresearch method.

## Core Architecture

Three-file contract:

| File | Role | Agent Editable? |
|------|------|----------------|
| `prepare.py` | Static experiment setup: data, tokenizer, metric definition | No (immutable baseline) |
| `train.py` (or target) | Model/code under optimization | Yes (agent's playground) |
| `program.md` | Human-written instructions, constraints, and acceptance criteria | No (human edits only) |

Each iteration: agent reads `program.md` → forms hypothesis → edits target code → runs timed experiment (default 5 min) → evaluates metric → commits if improved, reverts if regressed.

## Memory Caching Strategy

Two-layer cache inspired by the AI Engineering Guidebook:

**Layer 1 — Cold Cache (CAG / KV Cache)**
Stable, rarely-changing context cached directly in KV memory:
- `program.md` instructions
- Baseline metrics and experiment contract
- Permission policies and constraints
- Shared system prompts

Avoids recomputing the same static information on every iteration. Uses Paged Attention to prevent GPU memory fragmentation.

**Layer 2 — Hot Cache (Prompt Cache)**
Dynamic per-iteration state via OpenAI/Anthropic prompt caching:
- Agent hypotheses generated this session
- Runtime logs and partial results
- Frequently changing context

Cold + hot separation keeps cache size bounded while maximizing reuse. See `/getCacheStatus` endpoint for current cache utilization.

## Endpoints

### `POST /runLoop`
Start an autonomous optimization loop.

```json
{
  "program_file": "./program.md",
  "target_file": "./train.py",
  "evaluation_script": "./prepare.py",
  "metric_name": "val_bpb",
  "max_iterations": 100,
  "timeout_seconds": 300,
  "cache_strategy": "prompt_cache"
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "loop_id": "loop_a1b2c3d4",
    "status": "running",
    "started_at": "2026-07-09T20:00:00Z"
  }
}
```

### `GET /getResults`
Retrieve loop progress and history.

```json
{
  "loop_id": "loop_a1b2c3d4"
}
```

Response:
```json
{
  "loop_id": "loop_a1b2c3d4",
  "status": "running",
  "current_iteration": 42,
  "best_metric": {
    "name": "val_bpb",
    "value": 1.1023,
    "improvement_pct": 12.4
  },
  "total_improvements": 5,
  "iterations": [
    {
      "number": 38,
      "hypothesis": "Increase depth from 8 to 12",
      "metric_value": 1.1023,
      "accepted": true,
      "duration_seconds": 298
    }
  ],
  "cache_hits": 38,
  "cache_savings_ms": 15200
}
```

### `POST /runExperiment`
Run a single isolated experiment without commit.

```json
{
  "target_file": "./train.py",
  "dry_run": false,
  "use_cache": true
}
```

Response:
```json
{
  "execution_time_seconds": 298,
  "metric": { "name": "val_bpb", "value": 1.2345 },
  "logs": "Epoch 1 loss: 2.1... val_bpb final: 1.2345",
  "cached": true
}
```

### `GET /getCacheStatus`
Inspect cache state across layers.

Response:
```json
{
  "prompt_cache": { "active_entries": 3, "hits": 38, "misses": 4, "savings_ms": 15200 },
  "kv_cache": { "active_entries": 2, "memory_usage_mb": 128, "fragmentation_pct": 3.2 },
  "cold_storage": { "cached_files": ["program.md", "baseline.json"], "size_bytes": 24576 }
}
```

### `POST /revertLast`
Revert the last accepted change.

```json
{ "loop_id": "loop_a1b2c3d4" }
```

Response:
```json
{
  "status": "success",
  "reverted_iteration": 38,
  "previous_metric": { "name": "val_bpb", "value": 1.1500 }
}
```

## Permissions

| Permission | Purpose |
|-----------|---------|
| `gpu_access` | Run ML experiments (PyTorch) within strict time windows |
| `llm_api_access` | Agent generates hypotheses and code edits via LLM APIs |
| `file_storage_read_write` | Read/write target files, logs, and progress artifacts |
| `network_access` | Download datasets, sync results, call LLM APIs |
| `git_operations` | Commit accepted changes, revert regressions, track history |

## Testing

1. `lemon-cli plugin audit karpathy-loop` — verify all 5 permissions requested
2. Create mock `train.py` that prints `val_bpb: 1.50` → `/runExperiment` → verify metric extraction
3. Write `program.md` targeting metric reduction → `/runLoop` with `max_iterations: 3` → verify autonomous cycle
4. `/getCacheStatus` pre/post loop — verify prompt cache hits increase with shared prefixes
5. `/getResults` during loop + `/revertLast` — verify iteration tracking and git revert
