---
name: secure-mcp-install
description: 'This skill should be used when the user asks to install or audit an MCP server, especially from third-party sources. Security-focused: clones at pinned commits, runs security scans.'
---

# Secure MCP Server Installation

This skill provides a security-focused workflow for installing MCP servers from third-party sources. It implements a "trust but verify" approach: clone the repository at a specific commit, run automated security scans, perform manual review of critical areas, then install with updates disabled.

## When to Use This Skill

Use this workflow when:
- Installing MCP servers from community maintainers (not official Anthropic packages)
- The repository has popularity/stars but unknown maintainers
- Security is a concern but full code review isn't practical
- Pinning to a specific version is desired

## Core Workflow

### Step 1: Clone at Specific Commit

Clone the repository and check out the target commit:

```bash
# Create audit directory
mkdir -p ~/.claude/mcp-audits
cd ~/.claude/mcp-audits

# Clone the repository
git clone <REPO_URL> <SERVER_NAME>
cd <SERVER_NAME>

# Check out specific commit (or latest if user doesn't specify)
git checkout <COMMIT_SHA>

# Record the commit for the audit report
git log -1 --format="%H %ci %s" > ../<SERVER_NAME>-audit-commit.txt
```

### Step 2: Run Automated Security Scan

Execute the audit script to scan for red flags:

```bash
~/.claude/skills/secure-mcp-install/scripts/audit-mcp-server.sh ~/.claude/mcp-audits/<SERVER_NAME>
```

The script scans for:
- Dangerous code patterns (eval, exec, dynamic imports)
- Obfuscated or minified source code
- Suspicious network calls and hardcoded URLs
- Environment variable access patterns
- Credential harvesting indicators
- Known malware signatures

Review the output. Any HIGH severity findings require manual investigation before proceeding.

### Step 3: Audit Dependencies

For Node.js projects:
```bash
cd ~/.claude/mcp-audits/<SERVER_NAME>
npm audit --audit-level=high
# Or with yarn:
yarn audit --level high
```

For Python projects:
```bash
cd ~/.claude/mcp-audits/<SERVER_NAME>
pip-audit -r requirements.txt 2>/dev/null || pip install pip-audit && pip-audit -r requirements.txt
```

Check for:
- Known vulnerabilities in dependencies
- Typosquatted package names (check suspicious packages manually)
- Unusually low download counts on dependencies
- Recent ownership transfers on critical packages

### Step 4: Manual Review (Focus Areas)

Perform targeted manual review of these critical areas:

1. **Entry points**: Main file, server initialization
2. **Tool handlers**: What each MCP tool actually does
3. **Network code**: Any HTTP clients, WebSocket connections
4. **File system access**: Read/write operations, paths accessed
5. **Environment handling**: What env vars are read and how used
6. **Build scripts**: postinstall hooks, build commands

Refer to `references/audit-checklist.md` for the complete checklist.

### Step 5: Generate Audit Report

Create a report documenting the audit:

```bash
# Create report
cat > ~/.claude/mcp-audits/<SERVER_NAME>-audit-report.md << 'EOF'
# MCP Server Audit Report

## Server Details
- **Name**: <SERVER_NAME>
- **Repository**: <REPO_URL>
- **Commit**: <COMMIT_SHA>
- **Audit Date**: $(date -I)

## Automated Scan Results
<PASTE_SCAN_OUTPUT>

## Dependency Audit
<PASTE_DEPENDENCY_AUDIT>

## Manual Review Notes
<YOUR_NOTES>

## Decision
- [ ] APPROVED - Safe to install
- [ ] REJECTED - Security concerns identified
- [ ] CONDITIONAL - Safe with restrictions (document below)

## Restrictions/Notes
<ANY_RESTRICTIONS>
EOF
```

### Step 6: Install with Pinned Version

If approved, install the MCP server at the audited commit.

For npm-based servers, install from the local clone:
```bash
cd ~/.claude/mcp-audits/<SERVER_NAME>
npm install
npm run build  # if needed
```

Then register with Claude Code using the CLI (required - manual file edits don't persist):

```bash
# For Node.js servers
claude mcp add-json <SERVER_NAME> '{
  "type": "stdio",
  "command": "node",
  "args": ["'$HOME'/.claude/mcp-audits/<SERVER_NAME>/dist/index.js"],
  "env": {
    "API_KEY": "your-key"
  }
}'

# For Python servers
claude mcp add-json <SERVER_NAME> '{
  "type": "stdio",
  "command": "'$HOME'/.claude/mcp-audits/<SERVER_NAME>/.venv/bin/python",
  "args": ["-m", "<module_name>"],
  "cwd": "'$HOME'/.claude/mcp-audits/<SERVER_NAME>",
  "env": {
    "API_KEY": "your-key"
  }
}'
```

For Python servers, first create the venv:
```bash
cd ~/.claude/mcp-audits/<SERVER_NAME>
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Important**: Use `claude mcp add-json` - manually editing `~/.claude.json` gets overwritten on restart.

### Step 7: Disable Automatic Updates

Since the server is installed from a local clone (not npm/pip registry), updates won't happen automatically. To upgrade later:

1. Pull new changes: `git fetch origin`
2. Review diff: `git diff HEAD origin/main`
3. Re-run the full audit workflow
4. Checkout new commit if approved

## Quick Reference

| Step | Command/Action |
|------|----------------|
| Clone | `git clone <url> && git checkout <sha>` |
| Scan | `~/.claude/skills/secure-mcp-install/scripts/audit-mcp-server.sh <path>` |
| Deps (npm) | `npm audit --audit-level=high` |
| Deps (pip) | `pip-audit -r requirements.txt` |
| Install | From local clone, not registry |
| Config | `claude mcp add-json <name> '<json>'` |

## Claude Code MCP Configuration Reference

### Adding MCP Servers (Use CLI)

**Always use the CLI** - manually editing `~/.claude.json` gets overwritten on restart:

```bash
# Add from JSON config
claude mcp add-json <name> '{"type": "stdio", "command": "...", "args": [...]}'

# Add stdio server with flags
claude mcp add <name> --transport stdio -- <command> <args>

# List configured servers
claude mcp list

# Remove a server
claude mcp remove <name>
```

### Config Scopes

| Scope | Method | Use Case |
|-------|--------|----------|
| **User** | `claude mcp add-json` | Personal servers, all projects |
| **Project** | `.mcp.json` file in project root | Team-shared, committed to git |

**Note**: For project scope, you CAN edit `.mcp.json` directly - only `~/.claude.json` gets overwritten.

### After Adding

1. **Restart Claude Code** - Required for new servers
2. **Verify with `/mcp`** - Shows connected servers
3. **Or use**: `claude mcp list`

### Common Issues

- **Windows**: Wrap npx with `cmd /c npx ...`
- **Project scope**: Requires approval on first use
- **Environment vars**: Support `${VAR}` and `${VAR:-default}` expansion
- **Manual edits to ~/.claude.json**: Get overwritten - use CLI instead

## Security Principles

1. **Pin versions**: Never use `latest` or auto-updating installs
2. **Local installs**: Install from audited local clone, not registry
3. **Minimal env**: Only pass required environment variables
4. **Document decisions**: Keep audit reports for future reference
5. **Re-audit on upgrade**: Treat updates as new installs

## Additional Resources

### Reference Files
- **`references/red-flags.md`** - Detailed patterns the scanner looks for
- **`references/audit-checklist.md`** - Complete manual review checklist

### Scripts
- **`scripts/audit-mcp-server.sh`** - Automated security scanner
