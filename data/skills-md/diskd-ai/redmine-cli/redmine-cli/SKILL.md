---
name: redmine-cli
description: "Manage Redmine issues/tickets from the command line via the Redmine REST API using a `red-cli`-style interface. Uses `~/.red/config.json` for auth (server + api-key) with optional local overrides in `./.red/config.json`. Use when you need to list issues/projects, view issues (with journals), add journal notes/comments (public or private), update issue description, update/remove existing comments (journals) by journal id, filter/sort/paginate lists, or troubleshoot Redmine CLI configuration (project-id/user-id, multi-instance `--rid`). Triggers on Redmine, red-cli, issue list/view/note/edit/comment, `--rid`, `.red/config.json`, `api-key`, `project-id`, `user-id`, or requests to automate Redmine from a CLI."
---

# Redmine CLI

Use the bundled `scripts/redmine_cli.py` (no external dependencies) to interact with Redmine from the terminal. It reads auth/config from `~/.red/config.json` (and optionally `./.red/config.json` as an override).

## Quick start

1. Create a Redmine API key (Redmine UI: *My account* -> *API access key*).
2. Create `~/.red/config.json` (v1 / single-instance format):

```json
{
  "api-key": "YOUR_API_KEY",
  "editor": "",
  "pager": "",
  "project": "",
  "project-id": 0,
  "server": "https://redmine.example.com",
  "user-id": 0
}
```

3. Verify connectivity:

```bash
python scripts/redmine_cli.py project list --json | head
```

## Multi-instance (`--rid`) (optional)

If your `~/.red/config.json` uses a v2 / multi-server structure (like the reference `red-cli`), select a server with `--rid`:

```bash
python scripts/redmine_cli.py issue list --rid prod
python scripts/redmine_cli.py issue list --rid 1
```

## Common tasks

List projects (default output is TSV; use `--json` for automation):

```bash
python scripts/redmine_cli.py project list
python scripts/redmine_cli.py project list --json
```

List issues (uses `project-id` from config unless `--all` or `issue list all`):

```bash
python scripts/redmine_cli.py issue list
python scripts/redmine_cli.py issue list --json --limit 10 --page 1
python scripts/redmine_cli.py issue list --query "login fails" --status_id 1 --sort priority
python scripts/redmine_cli.py issue list --issue-urls
python scripts/redmine_cli.py issue list --project   # include project column in output
```

Get an issue:

```bash
python scripts/redmine_cli.py issue view 12345
python scripts/redmine_cli.py issue view 12345 --journals
```

List all issues across projects:

```bash
python scripts/redmine_cli.py issue list all
python scripts/redmine_cli.py issue list --all
```

List only issues assigned to the current user:

```bash
python scripts/redmine_cli.py issue list me
```

Add a journal note to an issue:

```bash
python scripts/redmine_cli.py issue note 12345 -m "Fixed in commit abc123"
python scripts/redmine_cli.py issue note 12345 -m "Customer-visible" --private
```

Update issue description:

```bash
python scripts/redmine_cli.py issue edit 12345 --description "New description"
python scripts/redmine_cli.py issue edit 12345 --description-file ./description.md
python scripts/redmine_cli.py issue edit 12345 --description-file - < ./description.md
```

Update/remove an existing comment (journal):

1. Find the journal id in `issue view --journals` output: `issue.journals[].id`
2. Update or remove:

```bash
python scripts/redmine_cli.py issue comment update 5993 -m "Updated comment text"
python scripts/redmine_cli.py issue comment update 5993 --message-file ./comment.md
python scripts/redmine_cli.py issue comment remove 5993
```

Show current user info:

```bash
python scripts/redmine_cli.py user me
```

## Troubleshooting

- `HTTP 401/403`: API key missing/invalid, REST API disabled, or insufficient permissions.
- `HTTP 404`: wrong base URL (ensure it is the Redmine root, not a sub-path like `/projects`).
- Config not found: ensure `~/.red/config.json` exists and is valid JSON.

## References

- Redmine REST API notes (endpoints, payloads, filters): `references/rest-api.md`
