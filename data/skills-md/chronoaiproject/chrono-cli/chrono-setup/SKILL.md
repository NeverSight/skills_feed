---
name: chrono-setup
description: Chrono CLI reference and setup guide. Use when installing chrono-cli, setting up a new project, running chrono init, or configuring MCP integration. Covers installation (curl script), authentication, project initialization, and common workflows.
---

# Chrono CLI

Chrono CLI allows you to interact with the Developer Platform without accessing the dashboard.

## Quick Start

Get started with chrono-cli in minutes:

```bash
# 1. Check if chrono is installed
chrono --version

# 2. If not installed, install via curl
curl -sSL https://raw.githubusercontent.com/ChronoAIProject/chrono-cli/main/install.sh | sh

# 3. Navigate to your project and initialize
cd /path/to/project
chrono init

# 4. Login to authenticate
chrono login

# 5. Setup MCP integration with your AI editor
chrono mcp-setup
```

## Installation

### Via curl (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/ChronoAIProject/chrono-cli/main/install.sh | sh
```

### Verify Installation

```bash
chrono --version
```

## Available Commands

### Authentication

**Login** - Authenticate via Keycloak device flow
```bash
chrono login
```

**Logout** - Clear local credentials
```bash
chrono logout
```

**Status** - Show current login status
```bash
chrono status
```

### Project Setup

**Init** - Initialize Chrono configuration for your project
```bash
chrono init
```
Creates `.chrono/config.yaml` with project settings.

**Detect** - Analyze project and detect tech stack
```bash
chrono detect [--save]
```
- `--save` - Save detected configuration as metadata

### AI Editor Integration

**MCP Setup** - Configure AI editor to use Chrono as an MCP server
```bash
chrono mcp-setup [editor]
```

Supported editors:
- `cursor` (default) - Cursor IDE
- `claude-code` - Claude Code
- `codex` - Codex
- `gemini` - Gemini CLI

This command:
1. Creates API token automatically
2. Configures editor's MCP settings
3. Verifies MCP connection

## Configuration Files

```
~/.chrono/config.yaml     # Main CLI config
.chrono/config.yaml       # Project-specific config
.chrono/metadata.yaml      # Auto-generated project metadata
.cursor/mcp.json          # Cursor MCP config (auto-generated)
.mcp.json                 # Claude Code MCP config (auto-generated)
```

## Common Workflows

### First-time setup for a new project:
```bash
1. cd /path/to/project
2. chrono init
3. chrono login
4. chrono detect --save
5. chrono mcp-setup
```

### Deploy current project:
```bash
# Use the MCP tools via your AI editor
- list_projects
- create_pipeline
- trigger_pipeline_run
- get_run_status
```

## Global Flags

- `--api-url string` - API server URL (overrides config)
- `--config string` - Config file path
- `--debug` - Enable debug output
- `-h, --help` - Help for any command
- `-v, --version` - Show version
