---
name: install-mcp-servers
description: Automatically installs Apify MCP, Netlify MCP, and Context7 MCP servers to enable web scraping, deployment, and library documentation capabilities. Use when setting up a new project or when you need these MCP integrations.
---

# Install MCP Servers

This skill automatically installs three essential MCP servers for development workflows:

1. **Apify MCP** - Web scraping, data extraction, and automation
2. **Netlify MCP** - Deployment, hosting, and site management
3. **Context7 MCP** - Library documentation and code examples

## When to Use This Skill

Use this skill when:
- Setting up a new project that needs scraping capabilities
- You need to deploy to Netlify
- You want library documentation lookup within Claude Code
- The user asks to "install MCP servers" or "setup MCPs"
- You need Apify, Netlify, or Context7 integration

## Installation Options

The skill supports three installation modes:

1. **Project-level** (default) - Installs to current project only
2. **Global** - Installs for all projects
3. **Selective** - Install only specific servers

## How to Install

### Automatic Installation (Recommended)

Run the installation command to add all three MCP servers:

```bash
# Add to current project's MCP configuration
claude mcp add apify --transport http --url "https://mcp.apify.com/"
claude mcp add netlify --transport http --url "https://netlify-mcp.netlify.app/mcp"
claude mcp add context7 --transport http --url "https://mcp.context7.com/mcp"
```

### Alternative: NPX-based Installation

For stdio-based servers (useful if HTTP endpoints are unavailable):

```bash
# Context7 via NPX (requires API key from https://context7.com)
claude mcp add context7 -s user -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY

# Netlify via NPX
claude mcp add netlify -s user -- npx -y @netlify/mcp
```

### Global Installation

Add `-s user` flag to install globally for all projects:

```bash
claude mcp add apify -s user --transport http --url "https://mcp.apify.com/"
claude mcp add netlify -s user --transport http --url "https://netlify-mcp.netlify.app/mcp"
claude mcp add context7 -s user --transport http --url "https://mcp.context7.com/mcp"
```

## Server Capabilities

### Apify MCP
- **Tools**: `search-actors`, `call-actor`, `fetch-actor-details`, `apify-slash-rag-web-browser`
- **Use cases**: Web scraping, data extraction, lead generation, competitor analysis
- **Authentication**: Connects via Apify account (OAuth during first use)

### Netlify MCP
- **Tools**: Site deployment, DNS management, build triggers, environment variables
- **Use cases**: Deploy sites, manage hosting, configure builds
- **Authentication**: Connects via Netlify account

### Context7 MCP
- **Tools**: `resolve-library-id`, `get-library-docs`
- **Use cases**: Lookup library documentation, get code examples, understand APIs
- **Authentication**: Free tier available, API key for extended use

## Verification

After installation, verify the servers are connected:

```bash
# List all configured MCP servers
claude mcp list

# Or use /mcp command in Claude Code to see connection status
```

## Troubleshooting

### Server not connecting
1. Check if the HTTP endpoint is accessible
2. Verify authentication is complete
3. Try the NPX alternative if HTTP fails

### Permission errors
- Ensure you have write access to `~/.claude.json`
- Try running with appropriate permissions

### Removing servers
```bash
claude mcp remove apify
claude mcp remove netlify
claude mcp remove context7
```

## Quick Reference

| Server | HTTP URL | NPX Package |
|--------|----------|-------------|
| Apify | `https://mcp.apify.com/` | N/A (HTTP only) |
| Netlify | `https://netlify-mcp.netlify.app/mcp` | `@netlify/mcp` |
| Context7 | `https://mcp.context7.com/mcp` | `@upstash/context7-mcp` |
