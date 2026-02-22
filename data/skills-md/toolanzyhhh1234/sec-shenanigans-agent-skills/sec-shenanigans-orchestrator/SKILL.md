---
name: sec-shenanigans-orchestrator
description: Orchestrate end-to-end SEC forensic analysis by chaining evidence extraction, Shenanigans classification, ratio diagnostics, and memo generation. Use when users ask for a full pipeline run, complete diligence workflow, or one-command analysis.
---
# SEC Shenanigans Orchestrator

Coordinate a strict 5-artifact pipeline.

## Pre-Stage Data Fetch

Before running any fetch scripts, the Orchestrator must instruct agents to check the local filesystem for `/<ticker>` directories containing user-provided filings (`10-K`, `10-Q`, `.xlsx`). Only rely on external SEC crawls or fetch scripts if the local data is incomplete or missing.

If filing tables are not readily available locally, run:

```bash
python skills/sec-shenanigans-orchestrator/scripts/fetch_financial_sheets.py <TICKER>
```

Use output as numeric support material; keep forensic evidence anchored to filing sections.

## Pipeline Order

1. `sec-filing-evidence-extractor` -> `evidence-table.md`
1. `sec-shenanigans-classifier` -> `risk-register.md`
1. `sec-red-flag-ratio-checks` -> `ratio-diagnostics.md`
1. `sec-shenanigans-memo-writer` -> `shenanigans-memo.md`, `open-questions.md`

## Contract

Use exact filenames and required fields in `references/bundle-contract.md`.

## Stop Conditions

- Missing artifact file required by next stage.
- Artifact exists but required fields are missing.
- Cross-file link errors (`risk-register` references unknown `evidence_id`, etc.).

## Golden Path

Use this self-contained example set as formatting anchor:

- `references/golden-path/evidence-table.md`
- `references/golden-path/risk-register.md`
- `references/golden-path/ratio-diagnostics.md`
- `references/golden-path/shenanigans-memo.md`
- `references/golden-path/open-questions.md`

## Output Bundle

Return all artifacts in this order:

1. `evidence-table.md`
1. `risk-register.md`
1. `ratio-diagnostics.md`
1. `shenanigans-memo.md`
1. `open-questions.md`

For run profiles, read `references/pipeline-profiles.md`.
