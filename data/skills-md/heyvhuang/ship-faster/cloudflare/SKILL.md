---
name: cloudflare
description: "Infrastructure operations for Cloudflare: Workers, KV, R2, D1, Hyperdrive, observability, builds, audit logs. Triggers: worker/KV/R2/D1/logs/build/deploy/audit. Three permission tiers: Diagnose (read-only), Change (write requires confirmation), Super Admin (isolated environment). Write operations follow read-first, confirm, execute, verify pattern. MCP is optional — works with Wrangler CLI/Dashboard too."
allowed-tools:
  - Read
  - Bash
  - WebFetch
---

# Cloudflare Infrastructure Operations

Manage Cloudflare services: Workers, KV, R2, D1, Hyperdrive, Observability, Builds, and Audit Logs.

> **MCP is optional.** This skill works with MCP (auto), Wrangler CLI, or Dashboard. See [BACKENDS.md](BACKENDS.md) for execution options.

## Permission Tiers

| Tier | Purpose | Scope | Risk Control |
|------|---------|-------|--------------|
| **Diagnose** | Read-only/query/troubleshoot | Observability, Builds, Audit | Default entry, no writes |
| **Change** | Create/modify/delete resources | KV, R2, D1, Hyperdrive | Requires confirmation + verification |
| **Super Admin** | Highest privileges | All + Container Sandbox | Only in isolated/test environments |

## Security Rules

### Read Operations
1. **Define scope first** — account / worker / resource ID
2. **No account set?** — List accounts first, then set active
3. **Evidence required** — Conclusions must have logs/screenshots/audit records

### Write Operations (Three-step Flow)
```
1. Plan: Read current state first (list/get)
2. Confirm: Output precise change (name/ID/impact), await user confirmation
3. Execute: create/delete/update
4. Verify: audit logs + observability confirm no new errors
```

### Prohibited Actions
- ❌ Execute create/delete/update without confirmation
- ❌ Delete production resources (unless user explicitly says "delete production xxx")
- ❌ Use Super Admin privileges in non-isolated environments
- ❌ Use container sandbox as persistent environment

## Operation Categories

### Diagnose Tier (Read-only)

| Category | What You Can Do |
|----------|-----------------|
| **Observability** | Query worker logs/metrics, discover fields, explore values |
| **Builds** | List build history, get build details, view build logs |
| **Browser** | Fetch page HTML, convert to markdown, take screenshots |
| **Audit** | Pull change history by time range |
| **Workers** | List workers, get details, view source code |

### Change Tier (Write Operations)

| Resource | Operations |
|----------|------------|
| **KV** | List, get, create ⚠️, update ⚠️, delete ⚠️ |
| **R2** | List, get, create ⚠️, delete ⚠️ |
| **D1** | List, get, query, create ⚠️, delete ⚠️ |
| **Hyperdrive** | List, get, create ⚠️, edit ⚠️, delete ⚠️ |

⚠️ = Requires confirmation

### Super Admin Tier (Container Sandbox)

Temporary container for isolated tasks (~10 min lifecycle):
- Initialize, execute commands, read/write/delete files
- Use for: running tests, reproducing issues, parsing data
- NOT for: persistent state, production workloads

## Common Workflows

### Troubleshooting Flow
```
1. Clarify symptoms → worker name / time range / error type
2. Query observability to pull logs/metrics
3. If build-related → get build logs
4. If page-related → take screenshot to reproduce
5. Trace changes → pull audit logs
6. Summarize: root cause + evidence + fix recommendations
```

### Resource Management Flow
```
1. List accounts → set active account
2. List resources (KV / R2 / D1)
3. Plan changes → present to user
4. Execute after confirmation
5. Verify: audit logs + observability shows no errors
```

## Output Format

- **Language**: English
- **Structure**: Conclusion → Key data/evidence → Tool call summary → Next steps
- **Write operations**: Must clearly list operations and impact scope

Example:
```
✅ Investigation complete: worker `api-gateway` experienced 5xx spike between 18:00-18:30

Root cause: New code deployed threw TypeError when processing /v2/users
Evidence:
- Logs: 18:02 first occurrence of "Cannot read property 'id' of undefined"
- Audit: 18:00 user dev@example.com deployed new version
- Metrics: error_rate jumped from 0.1% to 12%

Recommendation: Roll back to previous version, or fix /v2/users handler
```

## File-based Pipeline

When integrating into multi-step workflows:

```
runs/<workflow>/active/<run_id>/
├── proposal.md                # Symptoms/objectives
├── context.json               # Account/worker/resource/time_range
├── tasks.md                   # Checklist + approval gate
├── evidence/observability.md
├── evidence/audit.md
├── evidence/screenshots/
├── evidence/change-plan.md    # Write operations written here first
├── evidence/report.md         # Conclusion + evidence + next steps
└── logs/events.jsonl          # Optional tool call summary
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Account not set | Run accounts_list → set_active_account first |
| Resource doesn't exist | Verify ID/name, list available resources |
| Insufficient permissions | Explain required permissions, check API token scope |
| Observability query too broad | Split into smaller time ranges |

## Related Files

- [BACKENDS.md](BACKENDS.md) — Execution options (MCP/CLI/Dashboard)
- [SETUP.md](SETUP.md) — MCP configuration (optional)
- [scenarios.md](scenarios.md) — 20 real-world scenario examples
