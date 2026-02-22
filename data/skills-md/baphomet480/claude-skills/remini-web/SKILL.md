---
name: remini-web
description: Apply Remini AI enhancements through a logged-in Remini web account from local image files. Use when the user asks to enhance, upscale, restore, unblur, or retouch photos with Remini Web, or wants a repeatable browser automation workflow for Remini output downloads.
---

# Remini Web

Use Remini Web with a human-in-the-loop browser automation flow that keeps account login and verification manual.

## Quick Start

1. Run script help first:
   ```bash
   python3 scripts/remini_apply.py --help
   ```
2. Install prerequisites if needed:
   ```bash
   python3 -m pip install playwright
   python3 -m playwright install chromium
   ```
3. Run a standard enhancement:
   ```bash
   python3 scripts/remini_apply.py /path/to/photo.jpg
   ```

The script opens Chromium, reuses a local browser profile, attempts upload/start actions, and waits for the Remini download.

## Core Workflow

1. Confirm the input is a local image (`.jpg`, `.jpeg`, `.png`, `.webp`, `.heic`, `.heif`).
2. Launch `scripts/remini_apply.py` with a persistent profile.
3. Log in manually in the browser if needed.
4. Let the script try auto-upload and auto-start.
5. Complete actions manually in-browser if UI labels differ.
6. Click Download in Remini and let the script capture/save the output.

## Common Commands

```bash
# Standard run (visible browser)
python3 scripts/remini_apply.py ./input/portrait.jpg

# Save to explicit output path
python3 scripts/remini_apply.py ./input/portrait.jpg --output ./output/portrait-remini.png

# Disable action click automation if the UI text changed
python3 scripts/remini_apply.py ./input/portrait.jpg --no-auto-start

# Add a custom action label for one-off UI variants
python3 scripts/remini_apply.py ./input/portrait.jpg --action-label "Create"

# Batch from a shell loop (one process per image)
for img in ./batch/*.{jpg,jpeg,png}; do
  python3 scripts/remini_apply.py "$img" --downloads-dir ./output/downloads
done
```

## Operational Rules

- Keep login, MFA, and checkout actions manual.
- Do not store passwords or one-time codes in files.
- Prefer `--no-auto-start` when Remini changes button text or flow.
- Increase `--timeout` for long-running jobs.
- Load troubleshooting notes from `references/workflow.md` when upload/download capture fails.

## Resources

- `scripts/remini_apply.py`: Interactive Playwright helper for Remini Web.
- `references/workflow.md`: UI matching strategy and troubleshooting.
