---
name: sec-red-flag-ratio-checks
description: Run forensic ratio and trend checks from SEC filing data to validate or challenge Shenanigans hypotheses. Use when users ask for quantitative red-flag checks, earnings quality diagnostics, or quarter-over-quarter anomaly detection.
---
# SEC Red-Flag Ratio Checks

Produce quantitative corroboration for risk hypotheses.

## Inputs

- Required: `evidence-table.md`, `risk-register.md`
- Optional helper: statements fetched via `fetch_financial_sheets.py`

## Workflow

1. Validate input artifact schemas.
1. Build period-aligned metric dataset.
1. Compute core forensic ratios and deltas.
1. Link each anomaly to `risk_id` and category.
1. Write artifact `ratio-diagnostics.md`.

## Required Output Artifact

Write `ratio-diagnostics.md` with required columns defined in `../sec-shenanigans-orchestrator/references/bundle-contract.md`.

## Rules

- Favor trend breaks over one-period thresholds.
- Require at least 4 quarters for directional claims when data exists.
- Emit data-quality limitations explicitly.

Read metric definitions in `references/forensic-metric-library.md`.
