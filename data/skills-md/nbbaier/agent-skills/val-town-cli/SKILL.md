---
name: val-town-cli
description: Manage Val Town projects using the vt CLI. Use when working with Vals (Val Town serverless functions), syncing code to Val Town, creating HTTP endpoints, streaming logs, or managing Val Town branches. Triggers on tasks involving Val Town development, val creation/editing, or when user mentions "vt", "val town", or "vals".
---

# Val Town CLI

The `vt` CLI manages Val Town projects locally. Key concepts:
- **Val**: A serverless function/project hosted on Val Town
- **HTTP Val**: A val that serves HTTP requests (filename must contain "http", e.g., `index.http.tsx`)
- **Branch**: Version control within a val (not git branches)

## Quick Reference

| Task | Command |
|------|---------|
| Create new val | `vt create my-val` |
| Clone existing | `vt clone username/valName` |
| Push changes | `vt push` |
| Pull updates | `vt pull` |
| Auto-sync | `vt watch` |
| View in browser | `vt browse` |
| Stream logs | `vt tail` |
| Check status | `vt status` |
| List your vals | `vt list` |

## Common Workflows

### Create and develop a new val

```bash
vt create my-api
cd my-api
# Edit files...
vt push
vt browse  # Open in browser
```

### Clone and modify existing val

```bash
vt clone username/valName
cd valName
# Edit files...
vt push
```

### Live development with auto-sync

```bash
cd my-val
vt watch  # Syncs on every file save
```

### Work on a feature branch

```bash
cd my-val
vt checkout -b my-feature
# Make changes...
vt push
vt checkout main
```

## File Naming Conventions

Val Town detects file types by naming patterns:

| Pattern | Val Type |
|---------|----------|
| `*.http.ts`, `*.http.tsx` | HTTP endpoint |
| `*.cron.ts` | Scheduled cron job |
| `*.email.ts` | Email handler |
| Other `.ts`/`.tsx` files | Script val |

Example: To create an HTTP API, name the file `api.http.ts` or `index.http.tsx`.

## Command Details

### Create

```bash
vt create my-val                    # New val in ./my-val
vt create my-val ./existing-folder  # Upload existing files
vt create my-val --private          # Private val
vt create my-val --org-name myorg   # Under an organization
```

### Clone

```bash
vt clone                                    # Interactive selection
vt clone username/valName                   # By name
vt clone https://www.val.town/x/user/val    # By URL
vt clone username/valName .                 # Into current directory
```

### Remix

Fork someone else's val:
```bash
vt remix std/reactHonoStarter myWebsite
cd myWebsite
vt watch
```

### Branches

```bash
vt branch              # List branches
vt checkout main       # Switch branch
vt checkout -b feature # Create new branch
vt branch -D feature   # Delete branch
```

### Logs

```bash
vt tail                          # Stream current val's logs
vt tail @user/valName            # Stream specific val
vt tail --print-headers          # Include HTTP headers
vt tail --reverse-logs           # Latest first
```

### Configuration

```bash
vt config options                           # List options
vt config set dangerousOperations.confirmation false  # Disable confirmations
vt config ignore                            # Edit global .vtignore
```

## Project Structure

After cloning/creating, a val directory contains:
- `.vt/` - Metadata (like .git)
- `.vtignore` - Files to exclude from sync
- `deno.json` - Deno LSP configuration
- Source files (`.ts`, `.tsx`, etc.)

## Tips

- Use `vt push --dry-run` to preview changes before pushing
- Use `vt checkout --dry-run` to preview branch switch effects
- HTTP vals require "http" in the filename to be recognized as endpoints
- The `vt watch` command enables live reloading with the browser companion extension
