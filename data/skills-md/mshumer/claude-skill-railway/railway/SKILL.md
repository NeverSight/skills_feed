---
name: railway
description: "Manage Railway deployments, view logs, check status, and manage environment variables. Use when working with Railway hosting, deployments, or infrastructure."
argument-hint: "<command> (status, logs, deploy, vars, health, switch, db, link)"
allowed-tools: Bash, WebFetch
---

# Railway CLI Skill

Manage Railway deployments and infrastructure using the Railway CLI.

## Pre-flight Check

Current status: !`railway status 2>&1 || echo "NOT_LINKED"`

## Auto-Recovery

Before running any command, check the pre-flight status above:

1. **If "command not found"**: Run `npm install -g @railway/cli`
2. **If "Not logged in"**: Tell user to run `railway login` manually (requires browser)
3. **If "NOT_LINKED" or "No project linked"**:
   - Run `railway list` to show available projects
   - Ask user which project to link, or auto-detect from package.json name
   - Link with `railway link -p <project-id>`

## Command Routing

Based on `$ARGUMENTS`, execute the appropriate workflow:

### "status" (default when no args)
```bash
railway status
railway domain
railway deployment list --limit 1
```
Report: project info, URL, and last deployment status/time.

### "logs" [options]
Parse natural language options:
- "errors" → `--filter "@level:error"`
- "last hour" / "1h" → `--since 1h`
- "build" → `--build`
- Number like "100" → `--lines 100`

Default: `railway logs --lines 30`

Summarize output - highlight errors, warnings, or interesting patterns.

### "deploy" / "up"
```bash
railway up
```
Then wait and check:
1. Run `railway deployment list --limit 1` to get status
2. If SUCCESS, fetch the domain URL and verify it responds: `curl -s -o /dev/null -w "%{http_code}" <domain>`
3. If FAILED, show build logs: `railway logs --build --lines 50`

### "redeploy"
```bash
railway redeploy
```
Redeploys without rebuilding. Useful for env var changes.

### "restart"
```bash
railway restart
```
Restarts the service without rebuild or redeploy.

### "vars" / "env" [action]
```bash
railway variables
```
**IMPORTANT**: When displaying variables, redact sensitive values:
- API keys: show first 8 chars + "..."
- Passwords: show "********"
- Tokens: show first 8 chars + "..."

For setting: `railway variables set KEY=value`
For deleting: `railway variables delete KEY` (ask for confirmation first!)

### "deployments" / "history"
```bash
railway deployment list --limit 10
```
Format as a table with: ID (short), Status, Time ago, Commit message (truncated)

### "domain"
```bash
railway domain
```
Show the public URL. If none exists, offer to create one.

### "health"
```bash
railway domain
```
Then curl the domain to check HTTP status:
```bash
curl -s -o /dev/null -w "%{http_code}" -m 10 <domain-url>
```
Report if healthy (2xx), unhealthy, or unreachable.

### "open"
```bash
railway open
```
Opens the Railway dashboard in browser.

### "switch <project-name>"
Switch to a different Railway project by name (fuzzy match).
```bash
# List all projects
railway list
```
Find the project ID that matches the name, then:
```bash
railway link -p <project-id>
```
Confirm the switch with `railway status`.

### "db" / "connect"
Connect to the project's database shell (Postgres, MongoDB, Redis, etc.)
```bash
railway connect
```
If multiple databases exist, Railway will prompt to select one.

### "link"
List available projects and link one:
```bash
railway list
```
Show projects in a numbered list. Ask user which to link, then:
```bash
railway link -p <project-id>
```

## Safety Guards

**Before destructive operations, ask for confirmation:**
- `railway down` - removes deployment
- `railway variables delete` - removes env var
- `railway unlink` - unlinks project

Format: "This will [action]. Are you sure? (y/n)"

## Response Format

Always provide:
1. **Summary**: One-line status (✓ success / ✗ failure / ⚠ warning)
2. **Details**: Relevant information in a clean table or list
3. **URL**: Public URL if applicable
4. **Next steps**: If something failed, suggest how to fix it

## Example Responses

**Status check:**
```
✓ MyApp is deployed and healthy

| Project     | MyApp                                    |
| Environment | production                               |
| Service     | MyApp                                    |
| URL         | https://myapp-production.up.railway.app  |
| Last deploy | 2 hours ago (SUCCESS)                    |
```

**After deploy:**
```
✓ Deployment successful

Build completed in 45s
URL: https://myapp-production.up.railway.app
Health check: 200 OK
```

**On error:**
```
✗ Deployment failed

Build error at line 23: Module not found 'xyz'

Suggested fix: Run `npm install xyz` and redeploy
```
