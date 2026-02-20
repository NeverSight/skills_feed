---
name: bugzilla
description: Interact with Mozilla Bugzilla (bugzilla.mozilla.org) via REST API. Use when the user asks to search bugs, view bug details, create bugs, update bugs, add comments, or attach files. Triggers on "bugzilla", "bmo", "file a bug", "bug report", "mozilla bug".
---

# Bugzilla CLI

Requires: `export BUGZILLA_API_KEY="your-key"` (get from https://bugzilla.mozilla.org/userprefs.cgi?tab=apikey)

Read-only ops work without auth.

Use this local skills checkout path for commands in this file:

```bash
SKILLS_ROOT=/Users/jwmoss/github_moz/agent-skills/skills
BZ="$SKILLS_ROOT/bugzilla/scripts/bz.py"
```

## Usage

```bash
uv run "$BZ" <command> [options]
```

Run `uv run "$BZ" --help` for full options.

## Commands

| Command | Purpose |
|---------|---------|
| `search` | Find bugs by product, component, status, assignee, etc. |
| `get` | View bug details, comments, history |
| `create` | File a new bug (requires: product, component, summary, version) |
| `update` | Modify status, assignee, priority, add comments |
| `comment` | Add comment to a bug |
| `attachment` | Attach files to a bug |
| `needinfo` | Request or clear needinfo flags |
| `products` | List products and components |
| `whoami` | Verify authentication |

## Quick Examples

```bash
# Search
uv run "$BZ" search --quicksearch "crash" --limit 10
uv run "$BZ" search --product Firefox --status NEW,ASSIGNED --priority P1

# View
uv run "$BZ" get 1234567 -v --include-comments
uv run "$BZ" get 1234567 --include-comments --full-comments
uv run "$BZ" get 1234567 --include-comments --include-history --format json

# Update
uv run "$BZ" update 1234567 --status RESOLVED --resolution FIXED
uv run "$BZ" needinfo 1234567 --request user@mozilla.com

# Create
uv run "$BZ" create --product Firefox --component General --summary "Title" --version unspecified
```

## References

- [examples.md](references/examples.md) - Workflow examples and user request mappings
- [api-reference.md](references/api-reference.md) - REST API endpoints and fields
