---
name: email-imap-full-fetch
description: Fetch full email MIME content and attachment files from IMAP by message reference. Use when downstream steps already have a stage-1 mail_ref and need full headers/body/attachments for a specific message, with message_id_norm as the primary lookup key and uid only as fallback.
---

# Email IMAP Full Fetch

## Core Goal
- Fetch one target email by stable message reference from IMAP.
- Enforce lookup order: `HEADER Message-Id` exact match first, then `uid` fallback.
- Download full raw MIME via `BODY.PEEK[]`.
- Parse and return headers, full text body, html body, and attachment metadata.
- Save `.eml` and attachment files to disk with filename safety and idempotent indexing.

## Standard Flow
1. Input must include `message_id_norm` from stage-1 routing output (`mail_ref.message_id_norm`).
2. Use `fetch --message-id "<message_id_norm or raw Message-Id>"` as the default path.
3. Use `fetch --uid "<uid>"` only when no usable message-id is available.
4. Keep mailbox selection consistent with stage-1 (`--mailbox` or `IMAP_MAILBOX`).
5. Read JSON output and continue downstream processing with returned `mail_ref`.

## Commands
Fetch by Message-Id (preferred):

```bash
python3 scripts/imap_full_fetch.py fetch --message-id "<caa123@example.com>"
```

Fetch by UID (fallback only):

```bash
python3 scripts/imap_full_fetch.py fetch --uid "123456"
```

Use both when needed (message-id lookup first, uid fallback second):

```bash
python3 scripts/imap_full_fetch.py fetch --message-id "<caa123@example.com>" --uid "123456"
```

## Output Contract
- Output is a single JSON object.
- Required top-level fields:
  - `mail_ref`
  - `headers`
  - `text_plain`
  - `text_html`
  - `attachments`
  - `saved_eml_path`
- `mail_ref` contains:
  - `account`, `mailbox`, `uid`, `message_id_raw`, `message_id_norm`, `date`
- `attachments[]` contains per-file metadata and persistence result:
  - `filename`, `content_type`, `bytes`, `disposition`, `saved_path`, `skipped_reason`

## Storage And Idempotency
- `saved_eml_path` points to local `.eml` file saved from `BODY.PEEK[]`.
- Attachments are saved without returning attachment binary content in JSON.
- Filenames are sanitized to remove path separators and unsafe characters.
- Duplicate attachment names are deduped with content-hash suffix.
- Repeated requests are idempotent by `message_id_norm` index and return existing persisted JSON record directly.

## Parameters
- `--message-id`: primary lookup key.
- `--uid`: fallback lookup key.
- `--mailbox`: mailbox to query (default `IMAP_MAILBOX` or `INBOX`).
- `--save-eml-dir`: target dir for `.eml` files (env `IMAP_FULL_SAVE_EML_DIR`).
- `--index-dir`: target dir for idempotency index JSON files (env `IMAP_FULL_INDEX_DIR`, default `<save-eml-dir>/.index`).
- `--save-attachments-dir`: target dir for attachments (env `IMAP_FULL_SAVE_ATTACHMENTS_DIR`).
- `--max-attachment-bytes`: max saved attachment size (env `IMAP_FULL_MAX_ATTACHMENT_BYTES`).
- `--allow-ext`: allowed attachment extensions, comma-separated (env `IMAP_FULL_ALLOW_EXT`).
- `--connect-timeout`: IMAP connect timeout seconds (default from `IMAP_CONNECT_TIMEOUT`).

## Required Environment
- `IMAP_HOST`
- `IMAP_USERNAME`
- `IMAP_PASSWORD`

Optional account defaults:
- `IMAP_NAME`
- `IMAP_PORT`
- `IMAP_SSL`
- `IMAP_MAILBOX`

## Scripts
- `scripts/imap_full_fetch.py`
