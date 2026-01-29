---
name: jack-basics
description: >
  Essential Jack Cloud patterns for AI agents.
  Use when: working in any Jack project, querying databases, deploying, or managing services.
  Teaches: how to use Jack CLI and MCP tools effectively.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Jack Basics

This skill teaches you how to work effectively in Jack Cloud projects.

## What This Skill Provides

- How to query and modify Jack databases (D1)
- How to deploy and check status
- How to use Jack MCP tools when available
- Common patterns and troubleshooting

## Key Concept

Jack projects use **cloud infrastructure**. Databases run on Cloudflare's edge network, not locally. Use Jack tools for all operations.

---

## Database Operations

### Query Data

```bash
jack db execute "SELECT * FROM users LIMIT 10"
```

### Modify Data

```bash
jack db execute --write "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')"
```

### View Schema

```bash
jack db execute "SELECT name FROM sqlite_master WHERE type='table'"
jack db execute "PRAGMA table_info(users)"
```

### Create Table

```bash
jack db execute --write "CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
```

### MCP Tools (Preferred When Available)

Check if `mcp__jack__*` tools are in your available tools:

| Tool | Purpose |
|------|---------|
| `mcp__jack__execute_sql` | Query or modify database |
| `mcp__jack__list_databases` | List project databases |
| `mcp__jack__create_database` | Create new D1 database |

**Example MCP usage:**
```
mcp__jack__execute_sql
  sql: "SELECT * FROM users"
  allow_write: false
```

For writes, set `allow_write: true`.

---

## Deployment

### Deploy to Production

```bash
jack ship
```

### Check Deployment Status

```bash
jack info
```

Shows: live URL, last deploy time, attached services.

### Stream Production Logs

```bash
jack logs
```

### Local Development

```bash
jack dev
```

Runs locally with **remote bindings** (real D1, KV, R2).

### MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__jack__deploy_project` | Deploy to production |
| `mcp__jack__get_project_status` | Check deployment status |
| `mcp__jack__tail_logs` | Stream production logs |

---

## Services

### List All Services

```bash
jack services
```

### Create Services

```bash
jack services db create        # D1 database
jack services kv create        # KV namespace
jack services storage create   # R2 bucket
jack services vectorize create # Vector index
```

### MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__jack__create_database` | Create D1 database |
| `mcp__jack__create_storage_bucket` | Create R2 bucket |
| `mcp__jack__create_vectorize_index` | Create vector index |

---

## Secrets

### Set a Secret

```bash
jack secrets set STRIPE_SECRET_KEY
```

Prompts for value (hidden input).

### Set Multiple Secrets

```bash
jack secrets set API_KEY WEBHOOK_SECRET
```

### List Secrets

```bash
jack secrets list
```

---

## Project Structure

Typical Jack project:

```
my-project/
├── src/
│   └── index.ts          # Worker entry point
├── wrangler.jsonc        # Cloudflare config (bindings, routes)
├── package.json
└── .jack/
    └── project.json      # Jack project link
```

- **`wrangler.jsonc`** - Defines D1 bindings, KV namespaces, environment
- **`.jack/project.json`** - Links to Jack Cloud (managed) or your Cloudflare account (BYO)

---

## Troubleshooting

### "Database not found"

Create one:
```bash
jack services db create
```

### "Not a Jack project"

Link the directory:
```bash
jack link --byo
```

### MCP tools not available

Install MCP config:
```bash
jack mcp install
```

Then restart your AI assistant.

### Need to see what went wrong

Stream production logs:
```bash
jack logs
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Query database | `jack db execute "SELECT ..."` |
| Write to database | `jack db execute --write "INSERT ..."` |
| Deploy | `jack ship` |
| Check status | `jack info` |
| Stream logs | `jack logs` |
| Local dev | `jack dev` |
| Create database | `jack services db create` |
| Set secret | `jack secrets set KEY` |

---

## Summary

1. **Use `jack` commands** for all operations
2. **Use MCP tools when available** (`mcp__jack__*`)
3. **Databases are remote** - D1 runs on Cloudflare's edge
4. **Deploy with `jack ship`** - handles build and deployment
5. **Check logs with `jack logs`** - debug production issues
