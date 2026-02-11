---
name: headline-crafter
description: Generate authentic, compelling article headlines using composable keyword extraction and pattern-based title generation.
version: 0.1.0
license: Apache-2.0
---

# Headline Crafter

Composable scripts for generating article headlines from ideas or drafts. Extract keywords, apply proven title patterns, and format the output.

## Purpose

Headlines make or break content. This skill extracts key topics from your input, applies curated title formulas across styles (professional, casual, provocative, how-to), and outputs formatted results. Each script is independently usable in a pipeline.

## Scripts Overview

| Script | Description |
|--------|-------------|
| `scripts/run.sh` | Main pipeline — extract | generate | format |
| `scripts/extract.sh` | Extract keywords from text input |
| `scripts/generate.sh` | Generate titles from comma-separated keywords |
| `scripts/format.sh` | Format title output as numbered list, JSON, or plain |
| `scripts/test.sh` | Run the full test suite |

## Pipeline Examples

```bash
# Generate 5 headlines from an article idea
echo "How to deploy machine learning models in production" | ./scripts/run.sh

# Extract keywords, then generate with a specific style
echo "The future of remote work" | ./scripts/extract.sh | ./scripts/generate.sh --style professional --count 8

# Generate and format as JSON
echo "react,hooks,state,management" | ./scripts/generate.sh --count 5 | ./scripts/format.sh --format json

# Full pipeline with custom count
cat article-draft.md | ./scripts/run.sh --count 10 --style casual
```

## Inputs and Outputs

- `extract.sh`: text via stdin → comma-separated keywords to stdout
- `generate.sh`: comma-separated keywords via stdin → one title per line to stdout
- `format.sh`: one title per line via stdin → formatted output to stdout
- `run.sh`: text via stdin → formatted titles to stdout (orchestrates the pipeline)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HEADLINE_STYLE` | `mixed` | Default title style |
| `HEADLINE_COUNT` | `5` | Default number of titles |
