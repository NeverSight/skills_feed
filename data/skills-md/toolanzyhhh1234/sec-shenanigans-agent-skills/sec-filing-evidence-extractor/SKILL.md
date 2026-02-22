---
name: sec-filing-evidence-extractor
description: Extract structured forensic evidence from SEC filings (10-K, 10-Q, 8-K, S-1 proxy appendices) for accounting-quality analysis. Use when a user asks to review filings, gather red flags, or prepare inputs for Shenanigans classification.
---
# SEC Filing Evidence Extractor

Extract section-anchored facts before interpretation.

## Workflow

1. Identify filing set and periods.
1. Prefer latest annual plus at least 8 quarters.
1. Extract evidence rows with exact filing anchors and numbers.
1. Validate schema against bundle contract.
1. Write artifact `evidence-table.md`.

## Required Output Artifact

Write `evidence-table.md` with required columns defined in `../sec-shenanigans-orchestrator/references/bundle-contract.md`.

## Quality Rules

- Keep one factual disclosure per row.
- Separate extraction confidence from manipulation confidence.
- Preserve sign and units in `numbers`.
- Mark ambiguous extraction with `confidence=low`.

## Pre-Stage Input Helper

1. **Local Priority:** Always begin by scanning the workspace for a directory matching the `/<ticker>` (e.g., `/PTC`, `/TSLA`). The user will often supply local `10-K`, `10-Q`, or `.xlsx` files in these nested directories. Treat these local files as your primary source of truth.
2. **External Fallback:** If local information is insufficient or missing, you are expected to proactively crawl the SEC website (EDGAR) or use provided fetching scripts to locate the necessary filings.

If raw statement tables are missing locally, orchestrator may run:

```bash
python skills/sec-shenanigans-orchestrator/scripts/fetch_financial_sheets.py <TICKER>
```

Use generated markdown only as a data helper; keep evidence anchored to SEC filing sections.

Use `references/sec-filing-hotspots.md` for section priorities.
