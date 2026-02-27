---
name: mesh
description: Execute plan-driven orchestration with CSV waves, strict coder-to-fixer-to-integrator unit gates, and budget-aware parallelism. Use for `$mesh`, parallel step execution from `update_plan`, `spawn_agents_on_csv` wave runs, CAS budget clamping, and event-only orchestration ledgers.
---

# mesh

## Overview

`$mesh` is the execution engine for implementation orchestration:

- Uses `update_plan` as the canonical ready queue.
- Slices coarse steps into atomic units.
- Builds disjoint-scope CSV waves.
- Executes waves with `spawn_agents_on_csv`.
- Enforces `coder -> fixer -> integrator` on each unit.
- Emits an event-only orchestration ledger.

## Zig CLI Iteration Repos

When iterating on the Zig-backed `mesh` helper CLI path, use these two repos:

- `skills-zig` (`/Users/tk/workspace/tk/skills-zig`): source for the `mesh` Zig binary, build/test wiring, and release tags.
- `homebrew-tap` (`/Users/tk/workspace/tk/homebrew-tap`): Homebrew formula updates/checksum bumps for released `mesh` binaries.

## Quick Start (Zig Binary + Brew Bootstrap)

```bash
run_mesh() {
  if command -v mesh >/dev/null 2>&1 && mesh --help 2>&1 | grep -q "mesh.zig"; then
    mesh "$@"
    return
  fi
  if [ "$(uname -s)" = "Darwin" ] && command -v brew >/dev/null 2>&1; then
    if ! brew install tkersey/tap/mesh; then
      echo "brew install tkersey/tap/mesh failed; refusing fallback." >&2
      return 1
    fi
    if command -v mesh >/dev/null 2>&1 && mesh --help 2>&1 | grep -q "mesh.zig"; then
      mesh "$@"
      return
    fi
    echo "brew install tkersey/tap/mesh did not produce a compatible mesh binary." >&2
    return 1
  fi
  echo "mesh binary missing or incompatible (marker mesh.zig not found)." >&2
  return 1
}

run_mesh --help
```

## Commands

- `mesh budget`: compute active-unit clamp from 5-hour + weekly remaining budget.
- `mesh plan_sync`: summarize and normalize plan JSON payloads.
- `mesh slice`: produce atomic units from plan steps.
- `mesh wave`: emit a wave-template CSV from sliced units.
- `mesh run_csv`: validate input CSV, enforce template/output path separation, and prepare output CSV.
- `mesh ledger`: filter ledger payloads to occurred events only.
- `mesh replay`: preflight simulation of budget/wave behavior without execution.

## Orchestration Policy

- Source of truth: `update_plan` queue.
- `$st` sync: when `.step/st-plan.jsonl` is active, keep `$st` and `update_plan` aligned in the same turn.
- Unit pipeline (hard gate): `coder -> fixer -> integrator`.
- Delivery default: `commit_first`; use `patch_first` only when explicitly requested.
- Budget clamp uses strictest remaining window (`min(remaining_5h, remaining_weekly)`):
  - `> 33%`: no budget-based clamp.
  - `10%..33%`: linear clamp.
  - `<= 10%`: single active unit, sequential single-agent execution.
- Scale-out gate: only allow CAS multi-instance fanout when backlog/saturation warrants it and strict remaining budget is `> 25%`.

For orchestration integration patterns (fleet/worktree/test-first), see `codex/ORCHESTRATION.md`.

## CSV-Wave Contract (`spawn_agents_on_csv`)

Required input headers:

- `id`
- `objective`
- `unit_scope`
- `constraints`
- `invariants`
- `proof_command`
- `delivery_mode`
- `attempt`
- `variant`
- `budget_tier`

### `spawn_agents_on_csv` Tool Arguments (Upstream Codex)

`spawn_agents_on_csv` takes:

- `csv_path` (required): path to the input CSV
- `instruction` (required): template string; `{column_name}` placeholders expand per row
- `id_column` (optional): which column to use as stable `item_id` (duplicates are suffixed)
- `output_csv_path` (optional): exported CSV path (default is derived from input filename)
- `max_concurrency` (optional): max parallel workers (default 16; capped by config; max 64)
- `max_workers` (optional): alias for `max_concurrency`
- `max_runtime_seconds` (optional): per-worker runtime timeout (default 1800)
- `output_schema` (optional): JSON shown to workers as the expected schema (not runtime-validated)

Placeholder escaping:

- Use `{{` and `}}` to emit literal braces in the rendered instruction.
- To show a placeholder literally (without expansion), write `{{column_name}}`.

### Canonical CSV Example (Fully Filled)

This is a minimal, parseable example row that maps a plan task into one atomic unit.

```csv
id,objective,unit_scope,constraints,invariants,proof_command,delivery_mode,attempt,variant,budget_tier
u-001,"Fix flaky parser: treat trailing commas as invalid","src/parser.py; tests/test_parser.py","Do not change public API; keep diff minimal; no git push","No new allocations in hot path; reject invalid input at boundary","uv run pytest tests/test_parser.py::test_reject_trailing_comma","commit_first",1,"wave","aware"
```

Field mapping from a typical subagent task template:

- Plan/Goals/Task/Acceptance -> `objective`
- Location/File paths -> `unit_scope`
- Constraints/Risks/"do not touch" -> `constraints`
- Invariants/"must never" rules -> `invariants`
- Validation command -> `proof_command`
- Commit vs patch delivery choice -> `delivery_mode`

Required worker output fields:

- `id`
- `decision`
- `proof_status`

These fields are expected inside the worker's `report_agent_job_result.result` object (exported in
the `result_json` column). See `references/output-contract.md`.

### Machine Output Precedence (Strict Mode)

When using Codex agent jobs, the machine output is the `report_agent_job_result` tool call.
Prefer the recorded `result_json` over any narrative text.
If `result_json` is missing or cannot be parsed, classify the unit as `invalid_output_schema`.

Recommended strict-mode contract: `references/output-contract.md`.

Optional output fields:

- `failure_code`
- `patch`
- `notes`

Export note:

- `spawn_agents_on_csv` exports an output CSV that includes the original input columns plus job
  metadata columns like `job_id`, `item_id`, `status`, `attempt_count`, `last_error`, and
  `result_json`.

Important:

- Keep `csv_path` and `output_csv_path` distinct per run.
- `output_schema` metadata is not runtime-enforced by `spawn_agents_on_csv`; mesh must enforce strict output parsing before integration.

## Recommended Flow

1. `mesh budget --remaining-five-hour <pct> --remaining-weekly <pct> --max-threads 12`
2. `mesh plan_sync --input-json <plan.json>`
3. `mesh slice --input-json <plan.json> --output-json <units.json>`
4. `mesh wave --units-json <units.json> --csv-path <run-wave.csv> --max-active <n>`
5. Run `spawn_agents_on_csv` against `<run-wave.csv>` with a distinct output CSV path.
6. `mesh run_csv --csv-path <run-wave.csv> --output-csv-path <run-output.csv>` for preflight/contract checks.
7. `mesh ledger --input-json <ledger.json>` to emit event-only final ledger payload.

## Replay Mode

Use `mesh replay` to simulate orchestration before spending budget:

```bash
mesh replay --remaining-five-hour 62 --remaining-weekly 41 --max-threads 12 --ready-units 19
```

Replay returns predicted active-unit clamp, wave count, and per-wave unit counts.

## Validation

```bash
mesh --help
mesh budget --remaining-five-hour 40 --remaining-weekly 28 --max-threads 12
mesh replay --remaining-five-hour 72 --remaining-weekly 55 --max-threads 12 --ready-units 24
mesh run_csv --csv-path /tmp/mesh_wave.csv --output-csv-path /tmp/mesh_wave.out.csv
```

## References

- `references/failure-taxonomy.md`
- `references/coder-rubric.md`
- `references/output-contract.md`
