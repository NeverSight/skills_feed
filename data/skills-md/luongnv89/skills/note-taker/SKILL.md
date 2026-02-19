---
name: note-taker
version: 1.4.0
description: Capture chat notes (text, voice, image, video, file) into the git-backed notes repo, summarize and organize them, extract tasks into KANBAN.md, commit/push changes, and always report GitHub web links to new/updated notes. Use when user says they want to take a note, save a note, capture this, or manage their notes/backlog.
argument-hint: "[optional title or tags]"
disable-model-invocation: true
---

# Note Taker (Git-managed)

This skill maintains a private notes system in a dedicated git-backed notes repository.

**Setup:** The notes repo path must be configured. Look for a `NOTES_REPO` variable in the project's CLAUDE.md or AGENTS.md, or ask the user for the path on first use.

**Rule:** This skill has side effects (writes + commits + pushes) so it must be user-invoked.

## Workflow

### 1) Intake
Accept input as:
- **Text**: the message content
- **Voice**: summarize (do not store full transcript unless user asks)
- **Image / video / file**: copy attachment file and reference it from the note

If the user provides multiple items, treat each as a separate note unless they explicitly want a single combined note.

### 2) Decide filename + folder
Create processed notes at:
- `notes/YYYY/MM/YYYY-MM-DD--<slug>.md`

Use a short, stable slug (kebab-case). If unsure, ask for a title.

### 3) Write the note
Use the template in `assets/note-template.md`.
Minimum sections:
- Summary (short)
- Details (only what matters)
- Tasks (checkboxes)
- Attachments (paths + links)

### 4) Store attachments (mandatory)
Always store attachment files in the **same folder as the note file**.

Example:
- Note: `notes/2026/02/2026-02-11--example.md`
- Attachments:
  - `notes/2026/02/2026-02-11--example--1.jpg`
  - `notes/2026/02/2026-02-11--example--2.mp4`

Rules:
- Never store note attachments for this workflow under `assets/images` or `assets/audio`.
- Keep deterministic suffixes: `--1`, `--2`, ...
- Use relative paths in note markdown.

### 5) Embed images in note markdown (mandatory)
For every image attachment, include an inline markdown image so it renders in the note:

- `![<short-alt-text>](./<attachment-filename>)`

For non-image files (video/audio/docs), keep normal markdown links under Attachments.

### 6) Redact secrets (mandatory)
Before committing, scan the note (and any pasted snippets) for:
- API keys / tokens / passwords / private keys

If found:
- replace with `[REDACTED_SECRET]`
- if ambiguity remains, **ask before commit**

### 7) Extract tasks → Kanban
Update `KANBAN.md`:
- Add new tasks to **Backlog**
- Each task should include a link to the note path

### 8) Maintain README index (mandatory)
After updating notes and `KANBAN.md`, update the notes repo README so it stays clickable and current:
- Preferred: run `python3 scripts/update_readme_overview.py` from repo root (if the script exists)
- Fallback: update `README.md` manually (overview counts + notes index)

### 9) Commit and push (mandatory for reporting links)
Commit message conventions:
- `note: add <short-title>`
- `kanban: add tasks from <slug>`
- `note: update <slug>`
- `docs: update notes README` (if README changed)

Always push when remote exists, so reported GitHub links are valid for user.

### 10) Report back with GitHub links (mandatory)
When reporting completion of any note action, include:
- GitHub link to each new/updated note markdown file
- GitHub link to each attached media file (if added)
- Commit hash

Link format:
- `https://github.com/<owner>/<repo>/blob/main/<relative-path>`

Detect the remote URL from the notes repo's `git remote get-url origin` to build correct links.

## Daily routines
- End-of-day: list today’s notes + propose re-organization (tags / merges / splits)
- Daily 10–15min: review Backlog → pick → move to In Progress → Done

## References
- Repo process rules: `AGENTS.md` in the notes repo root
- Redaction + workflow policy: `POLICY.md` in the notes repo root
