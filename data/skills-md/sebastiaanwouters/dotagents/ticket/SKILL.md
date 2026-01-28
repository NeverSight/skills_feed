---
name: ticket
description: Manage tickets with tk CLI. Triggers on "create ticket", "list tickets", "what's next", "blocked", "close ticket", "ticket status", "work on next ticket/issue".
---

# Ticket Management with tk

## Installation

```bash
go install github.com/wedow/ticket/cmd/tk@latest
```

Tickets stored as markdown in `.tickets/`. Works from any subdirectory.

## What Makes a Complete Ticket

**A ticket MUST have ALL of:**

1. **Clear Acceptance Criteria** — Specific, testable "done" conditions
   - ✅ "User can login with email/password and receives JWT"
   - ❌ "Login works"

2. **Clear Requirements** — What exactly to build
   - ✅ "POST /api/login accepts {email, password}, returns {token, expiresAt}"
   - ❌ "Add login endpoint"

3. **Design/UI Info** (if applicable) — Visual specs, layouts
   - ✅ "Login form: email input, password input, submit button. Error in red below form."

4. **Atomic + Actionable** — One focused task, can start immediately
   - ✅ "Implement password reset email"
   - ❌ "Improve auth system"

5. **Testing Requirements** — What to test
   - ✅ "Test: valid login→200+token, invalid→401, missing fields→400"

**Ask yourself:** Can someone implement this without clarifying questions?

## Quick Reference

| Command | Purpose |
|---------|---------|
| `tk create "title"` | Create ticket |
| `tk ls` | List all |
| `tk ready` | Ready to work (deps resolved) |
| `tk blocked` | Waiting on deps |
| `tk show <id>` | View details |
| `tk edit <id>` | Open in $EDITOR |
| `tk start/close/reopen <id>` | Change status |
| `tk dep <id> <dep-id>` | Add dependency |
| `tk dep tree <id>` | Show dep tree |
| `tk undep <id> <dep-id>` | Remove dep |
| `tk link <id> <id>...` | Link related |
| `tk add-note <id> "text"` | Append note |

Supports partial ID matching: `tk show 5c4` matches `nw-5c46`.

## Creating Complete Tickets

```bash
tk create "Implement JWT login" -t feature -p 1 \
  --description "POST /api/login validates creds, returns JWT with 24h expiry" \
  --acceptance "- Valid creds → 200 + {token, expiresAt}
- Invalid password → 401
- Missing fields → 400
- Token expires in 24h" \
  --tags backend,auth
```

Options: `-t` type (bug/feature/task/epic/chore), `-p` priority (0-4), `-d` description, `--acceptance`, `--design`, `-a` assignee, `--parent`, `--tags`

## Dependencies

```bash
tk dep ticket-a ticket-b      # a depends on b
tk dep tree ticket-a          # view tree
tk undep ticket-a ticket-b    # remove
tk dep cycle                  # find cycles
```

## Workflow

```bash
tk create "Auth system" -t epic                    # auth-7f3a
tk create "Design schema" --parent auth-7f3a       # sch-2b1c
tk create "Login endpoint" --parent auth-7f3a \
  --acceptance "POST /login returns JWT"           # log-9d4e

tk dep log-9d4e sch-2b1c   # login depends on schema
tk ready                   # shows sch-2b1c
tk close sch-2b1c
tk ready                   # now shows log-9d4e
```
