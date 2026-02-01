---
name: mcp-security-scanner
description: Scan for unprotected MCP servers using @contextware/mcp-scan package. Enables security auditing of local AI tools and network endpoints.
version: 1.0.0
author: ContextWare
mcp-servers: []
tags: [security, mcp, audit, scanning, contextware]
---

# MCP Security Scanner Skill

This skill enables agents to audit MCP servers for security issues. Use when user wants to scan for unprotected MCP endpoints.

## When to Use

- User asks to "scan for MCP servers"
- User wants to "audit MCP security"
- User asks to "check if MCP servers are protected"
- User mentions "unprotected" or "exposed" MCP servers

## Prerequisites

### Package Dependency
Uses `@contextware/mcp-scan` npm package.

**Installation:**
```bash
npm install -g @contextware/mcp-scan
```

Or run directly:
```bash
npx @contextware/mcp-scan <command>
```

### Runtime
- Node.js 18+
- Network access (for network scanning)
- Read access to config directories

## Workflow

### Phase 1: Assess Request

Clarify:
1. What to scan - localhost, local network, or specific targets?
2. Scope - network scan, config scan, or both?
3. Purpose - security audit, troubleshooting, or general discovery?
4. Very important - do not go into a loop calling this scanning tool. Never. And explain to the user that its not recommended to do scanning in a never ending loop.

### Phase 2: Execute Scans

**Network Scan:**
```bash
mcp-scan network <target>
```
Targets: localhost, local, CIDR (e.g., 192.168.1.0/24), or IP/domain

Options: -p <ports>, -t <timeout>, --https

**Config Scan:**
```bash
mcp-scan configs
```
Checks: Claude Desktop, Cursor, Continue.dev, Windsurf, Zed configs

**Full Scan:**
```bash
mcp-scan all <target>
```

### Phase 3: Present Results

- List servers with host, port, type, auth status
- Flag unprotected servers (requiresAuth: false)
- Provide remediation recommendations

### Phase 4: Safety Review

**Verify permission:** Only scan networks you own or have explicit authorization.

**Decline requests** to scan unknown targets. Offer to scan owned systems instead.

## Safety Guidelines

**What This Tool Does:**
- Sends HTTP requests to detect MCP endpoints
- Reads local config files
- Reports authentication status
- Read-only (no modifications)

**What This Tool Does NOT Do:**
- Does not modify any files
- Does not execute commands from configs
- Does not send data to external servers
- Does not exploit vulnerabilities

## Troubleshooting

**"mcp-scan: command not found"**
-> Install: npm install -g @contextware/mcp-scan

**"No servers found" but one is running**
-> Try custom ports: -p 8080,9000
-> Or use --https flag

**Scan times out**
-> Increase timeout: -t 5000

## References

- Package: https://npmjs.com/package/@contextware/mcp-scan
- Source: https://github.com/contextware/mcp-scan
- MCP Protocol: https://modelcontextprotocol.io