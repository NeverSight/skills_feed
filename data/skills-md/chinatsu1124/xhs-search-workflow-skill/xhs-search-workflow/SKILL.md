---
name: xhs-search-workflow
description: Run a fully self-contained Xiaohongshu workflow with cookie auth and bundled JS signing assets. Use for note search, note text/image extraction, image download, user/profile data, comments, message center data, homefeed data, creator posted-note data, no-watermark URL conversion, and Excel/media export without depending on the original Spider_XHS repository.
---

# XHS Search Workflow

## Setup
Run once on a new machine:

```bash
skills/xhs-search-workflow/scripts/setup_env.sh
```

This creates `skills/xhs-search-workflow/.venv` and installs Python deps.

## Cookie Input
Use either:
- `--cookie "..."`
- `--env-file /path/to/.env` with `COOKIES="..."`

Add `--no-env-proxy` when host proxy vars break network.

## Main Scripts
- `scripts/search_notes.py`: note search (supports advanced filters)
- `scripts/fetch_note_texts.py`: extract note text and image URLs, optional image download
- `scripts/xhs_full_cli.py`: unified entry for user/comment/message/homefeed/creator/no-water APIs
- `scripts/export_notes.py`: export note data to Excel and/or media files

## Typical Commands

### 1) Search notes
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/search_notes.py "汇丰银行" \
  --num 10 --sort 0 --note-type 0 --no-env-proxy --json
```

### 2) Extract note text + image URLs
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/fetch_note_texts.py \
  --url-file note_urls.txt --no-env-proxy \
  --timeout 30 --retries 2 --min-interval 4 --max-interval 7 \
  --out note_content.json
```

### 3) Download note images while extracting
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/fetch_note_texts.py \
  --url-file note_urls.txt --no-env-proxy \
  --download-images --image-dir xhs_images \
  --timeout 30 --retries 2 --min-interval 4 --max-interval 7 \
  --out note_content.json
```

### 4) Full API CLI examples
Search users:
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/xhs_full_cli.py \
  --env-file .env --no-env-proxy search-users --query "汇丰银行" --num 10
```

Get note comments:
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/xhs_full_cli.py \
  --env-file .env --no-env-proxy note-comments \
  --url "https://www.xiaohongshu.com/explore/<note_id>?xsec_token=<token>"
```

Get creator posted notes:
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/xhs_full_cli.py \
  --env-file .env --no-env-proxy creator-posted
```

No-watermark URL conversion:
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/xhs_full_cli.py \
  --no-env-proxy no-water-img --img-url "https://..."
```

### 5) Export Excel/media
From query:
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/export_notes.py \
  --query "汇丰银行" --num 10 --save all \
  --excel xhs_notes.xlsx --media-dir xhs_media --no-env-proxy
```

From URL file:
```bash
skills/xhs-search-workflow/.venv/bin/python \
  skills/xhs-search-workflow/scripts/export_notes.py \
  --url-file note_urls.txt --save excel --excel xhs_notes.xlsx --no-env-proxy
```

## `xhs_full_cli.py` Subcommands
- `user-info --user-id <id>`
- `user-self-info`
- `user-self-info2`
- `user-posts --user-url <url>`
- `user-likes --user-url <url>`
- `user-collects --user-url <url>`
- `note-info --url <url>`
- `note-comments --url <url>`
- `search-keyword --word <kw>`
- `search-users --query <kw> --num <n>`
- `messages-unread`
- `messages-mentions`
- `messages-likes`
- `messages-connections`
- `homefeed-channels`
- `homefeed-recommend --category <name> --num <n>`
- `creator-posted`
- `no-water-video --note-id <id>`
- `no-water-img --img-url <url>`

## Offline/Portable Design
- Skill bundles signing JS in `assets/js/`.
- Skill bundles offline `crypto-js` at `assets/js/vendor/crypto-js.js`.
- Skill does not import `apis/` or `xhs_utils/` from original repository.

## Validation
Run after edits:

```bash
skills/xhs-search-workflow/.venv/bin/python \
  "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/xhs-search-workflow
```

Basic smoke tests:

```bash
skills/xhs-search-workflow/.venv/bin/python skills/xhs-search-workflow/scripts/xhs_full_cli.py --help
skills/xhs-search-workflow/.venv/bin/python skills/xhs-search-workflow/scripts/export_notes.py --help
```

## Execution Notes
- Prefer `skills/xhs-search-workflow/.venv/bin/python` instead of system `python`.
- If environment changed, rerun `scripts/setup_env.sh` before debugging.
- Keep `assets/js/vendor/crypto-js.js` with the skill for cross-machine offline use.
- Scripts force UTF-8 stdout/stderr; on Windows, also set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`.
- `scripts/xhs_client.py` auto-checks JS assets and syncs `assets/js/static/xhs_xray_pack{1,2}.js` for runtime compatibility.
- For `xhs_full_cli.py`, place global flags before subcommand:
  - Correct: `xhs_full_cli.py --env-file .env --no-env-proxy <subcommand> ...`
  - Wrong: `xhs_full_cli.py <subcommand> ... --env-file .env`
- `messages-mentions/messages-likes/messages-connections` can return very large JSON; prefer `--out` to file.
- `fetch_note_texts.py` defaults to serial throttling and retries to reduce hang/risk-control issues.

## Troubleshooting
See `references/troubleshooting.md`.
