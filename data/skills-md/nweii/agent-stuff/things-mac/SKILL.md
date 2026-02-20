---
name: things-mac
description: "Manage Things 3 on macOS via CLI. Read, search, add, or update tasks, projects, and areas. Use for task management, listing inbox/today, and inspecting tags or repeating templates."
metadata:
  author: nweii
  source: https://github.com/steipete/clawdis-skills/things-mac
---

# Things 3 CLI

Use `things` to read your local Things database (inbox/today/search/projects/areas/tags) and to add/update todos via the Things URL scheme.

## Setup

- Check if already installed: `which things` (if it returns a path, skip installation)
- Install (Homebrew): `brew install ossianhempel/tap/things3-cli`
- Install (Go, recommended for Apple Silicon): `GOBIN=/opt/homebrew/bin go install github.com/ossianhempel/things3-cli/cmd/things@latest`
- Optional: set `THINGSDB` (or pass `--db`) to point at your `ThingsData-*` folder.

### Things auth token

Update operations require an auth token. You should set `THINGS_AUTH_TOKEN` in your shell profile (e.g., `~/.zshrc`) to persist it.

## Read-only (DB)

- `things inbox --limit 50`
- `things today` / `things logtoday` / `things createdtoday`
- `things upcoming` / `things deadlines`
- `things search "query"`
- `things projects` / `things areas` / `things tags`
- **Inspect contents**:
  - `things show "Area Name"` / `things show "Project Name"`
  - `things tasks --area "Area Name"`
  - `things tasks --project "Project Name"`

## Write (URL scheme)

- Prefer safe preview: `things --dry-run add "Title"`
- Add: `things add "Title" --notes "..." --when today --deadline 2026-01-02`
- Scheduling: `--when=someday`, `--later` (This Evening), `--when=evening`
- Bring Things to front: `things --foreground add "Title"`

## Examples

### Add a todo

- Basic: `things add "Buy milk"`
- With notes: `things add "Buy milk" --notes "2% + bananas"`
- Into a project/area: `things add "Book flights" --list "Travel"`
- Into a project heading: `things add "Pack charger" --list "Travel" --heading "Before"`
- With tags: `things add "Call dentist" --tags "health,phone"`
- Checklist: `things add "Trip prep" --checklist-item "Passport" --checklist-item "Tickets"`
- Repeating: `things add "Daily standup" --repeat day --repeat-mode schedule`
- From STDIN (multi-line => title + notes):
  - `cat <<'EOF' | things add -`
  - `Title line`
  - `Notes line 1`
  - `Notes line 2`
  - `EOF`

### Projects and areas

- Add area: `things add-area "Health"`
- Add project: `things add-project "New Site" --area "Work" --notes "Plan out the redesign"`
- Update project: `things update-project --id <UUID> --auth-token <TOKEN> "New Title" --notes "Updated notes"`

### Modify a todo (needs auth token)

- First: get the ID (UUID column): `things search "milk" --limit 5`
- Auth: set `THINGS_AUTH_TOKEN` or pass `--auth-token <TOKEN>`
- Title: `things update --id <UUID> --auth-token <TOKEN> "New title"`
- Notes replace: `things update --id <UUID> --auth-token <TOKEN> --notes "New notes"`
- Notes append/prepend: `things update --id <UUID> --auth-token <TOKEN> --append-notes "..."` / `--prepend-notes "..."`
- Move lists: `things update --id <UUID> --auth-token <TOKEN> --list "Travel" --heading "Before"`
- Tags replace/add: `things update --id <UUID> --auth-token <TOKEN> --tags "a,b"` / `things update --id <UUID> --auth-token <TOKEN> --add-tags "a,b"`
- Complete/cancel (soft-delete-ish): `things update --id <UUID> --auth-token <TOKEN> --completed` / `--canceled`
- Safe preview: `things --dry-run update --id <UUID> --auth-token <TOKEN> --completed`

### Delete a todo

- Supported via AppleScript: `things delete --id <UUID>`
- Also supports: `delete-project --id <UUID>` and `delete-area --id <UUID>`
- Note: This prompts for confirmation interactively. Use `--confirm` for non-interactive scripts.
- Alternatively: mark as completed/canceled via `things update --id <UUID> --completed` / `--canceled` (needs auth token).

## Notes

- macOS-only.
- `--dry-run` prints the URL and does not open Things.
