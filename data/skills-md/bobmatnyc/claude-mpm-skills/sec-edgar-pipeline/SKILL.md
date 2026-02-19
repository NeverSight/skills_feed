---
name: sec-edgar-pipeline
description: "SEC EDGAR extraction pipeline: setup, filing discovery by CIK, recipe-driven extraction, and report generation."
version: 1.0.0
category: universal
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "EDGAR pipeline: configure keys + user-agent, find filings by CIK, extract data via recipes/scripts, and export CSV/JSON reports."
    when_to_use: "Building SEC EDGAR extraction flows, running edgar-analyzer CLI, or generating compensation/filing reports from DEF 14A and related filings."
    quick_start: "1. edgar-analyzer setup 2. edgar-analyzer analyze-project projects/<name> 3. edgar-analyzer generate-code 4. edgar-analyzer run-extraction"
tags:
  - sec
  - edgar
  - filings
  - cik
  - def14a
  - extraction
---

# SEC EDGAR Pipeline

## Overview

This pipeline is centered on `edgar-analyzer` and the EDGAR data sources. The core loop is: configure credentials, create a project with examples, analyze patterns, generate code, run extraction, and export reports.

## Setup (Keys + User Agent)

Use the setup wizard to configure required keys:

```bash
python -m edgar_analyzer setup
# or
edgar-analyzer setup
```

Required entries:

- `OPENROUTER_API_KEY`
- (Optional) `JINA_API_KEY`
- `EDGAR` user agent string ("Name email@example.com")

## End-to-End CLI Workflow

```bash
# 1. Create project
edgar-analyzer project create my_project --template minimal

# 2. Add examples + project.yaml
# projects/my_project/examples/*.json

# 3. Analyze examples
edgar-analyzer analyze-project projects/my_project

# 4. Generate extraction code
edgar-analyzer generate-code projects/my_project

# 5. Run extraction
edgar-analyzer run-extraction projects/my_project --output-format csv
```

Outputs land in `projects/<name>/output/`.

## EDGAR-Specific Conventions

- **CIK** values are 10-digit, zero-padded (e.g., `0000320193`).
- **Rate limit**: SEC API allows 10 requests/sec. Scripts use ~0.11s delays.
- **User agent** is mandatory; include name + email.

## Scripted Example (Apple DEF 14A)

`edgar/scripts/fetch_apple_def14a.py` shows the direct flow:

1. Fetch latest DEF 14A metadata
2. Download HTML
3. Parse Summary Compensation Table (SCT)
4. Save raw HTML + extracted JSON + ground truth

## Recipe-Driven Extraction

`edgar/recipes/sct_extraction/config.yaml` defines a multi-step pipeline:

- Fetch DEF 14A filings by company list
- Extract SCT tables with `SCTAdapter`
- Validate with `sct_validator`
- Write results to `output/sct`

## Report Generation

`edgar/scripts/create_csv_reports.py` converts JSON results into:

- `executive_compensation_<timestamp>.csv`
- `top_25_executives_<timestamp>.csv`
- `company_summary_<timestamp>.csv`

## Troubleshooting

- **No filings found**: confirm CIK formatting and filing type (DEF 14A vs DEF 14A/A).
- **API errors**: slow down requests and confirm user-agent is set.
- **Extraction errors**: regenerate code or use manual ground truth in POC scripts.

## Related Skills

- `universal/data/reporting-pipelines`
- `toolchains/python/testing/pytest`
