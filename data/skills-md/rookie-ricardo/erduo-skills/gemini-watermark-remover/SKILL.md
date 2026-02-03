---
name: gemini-watermark-remover
description: Remove the visible Gemini AI watermark from images using reverse alpha blending. Use when asked to strip Gemini watermarks, batch-process Gemini images, or build/modify a CLI script that removes the bottom-right Gemini watermark without HTML or server-side components.
---

# Gemini Watermark Remover

## Dependencies

- Python 3.9+
- Pillow (install with `pip install -r requirements.txt`)

## Quick start

1) Install dependencies in the scripts folder:
   - `cd skills/gemini-watermark-remover/scripts && pip install -r requirements.txt`
2) Run the CLI:
   - `python remove_watermark.py <input-image> <output-image>`

## CLI usage

- Parameters:
  - `input-image`: path to the Gemini watermarked image
  - `output-image`: path for the cleaned image (format inferred from extension)

Example:

```
python remove_watermark.py ./in.png ./out.png
```

## What this skill provides

- `scripts/remove_watermark.py`: CLI entry point and core algorithm.
- `assets/bg_48.png`, `assets/bg_96.png`: Pre-captured watermark alpha maps.
- `references/algorithm.md`: Math, detection rules, and limits.

## Workflow

1) Use `remove_watermark.py` for one-off processing.
2) If you need to adjust detection rules or alpha logic, read `references/algorithm.md`.

## Notes

- The script uses Pillow for image IO and per-pixel edits.
- Output format is inferred from the output file extension by Pillow.
