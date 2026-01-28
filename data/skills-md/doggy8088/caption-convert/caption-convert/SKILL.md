---
name: caption-convert
description: Convert subtitle/caption files between .srt, .vtt, and .ass using the caption-convert CLI. Use when asked to convert subtitles, run/verify the caption-convert command, or explain its format handling and limitations. Includes a bundled CLI in scripts/cli.mjs for use outside this repo.
---

# Caption Convert

## Overview

Convert subtitle files between SRT, WebVTT, and ASS using the local `caption-convert` CLI. Rely on file extensions to pick input/output formats and keep conversion notes in mind.

## Quick Start

- Run after global install: `caption-convert input.srt output.vtt`
- Run from repo without install: `node .\\src\\cli.mjs input.vtt output.ass`
- Use extensions `.srt`, `.vtt`, or `.ass` for both source and target
- Requires Node.js 18+

## Bundled Tool (scripts/cli.mjs)

If the repo is not available, use the bundled CLI in `scripts/cli.mjs`:

1. Copy `scripts/cli.mjs` into a working folder.
2. Run directly: `node .\\cli.mjs input.srt output.vtt`

## Workflow

1. Confirm the source/target paths end with supported extensions.
2. Run the CLI from the repo or after a global install.
3. Spot-check the output for timing and header correctness.
4. Call out format limitations that may drop styling/metadata.

## Format Notes and Limitations

- Infer formats strictly from filename extensions; unsupported or missing extensions exit with usage.
- Skip cues with invalid or unparseable time lines.
- Output `.vtt` always includes a `WEBVTT` header.
- Convert `.ass` output with a fixed header and default styles; styling from source is not preserved.
- Strip ASS override tags (`{...}`) and convert `\\N`/`\\n` to line breaks on input.

## Examples

```powershell
caption-convert demo.srt demo.vtt
caption-convert demo.vtt demo.ass
node .\src\cli.mjs demo.ass demo.srt
```

## Troubleshooting

- If the CLI prints usage, check that both paths are provided and use supported extensions.
- Ensure Node.js 18+ is available when running via `node`.
