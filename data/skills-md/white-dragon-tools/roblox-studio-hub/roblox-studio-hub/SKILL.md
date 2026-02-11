---
name: roblox-studio-hub
description: This skill should be used when the user asks to "execute Lua code in Roblox Studio", "run code in Studio", "test Lua script", "connect to Studio Hub", "manage Studio instances", "check Studio status", "install Studio Hub", "setup Studio Hub service", or mentions Roblox Studio remote execution, Studio Hub API, or Lua code testing.
version: 1.0.0
---

# Roblox Studio Hub

A tool for managing multiple Roblox Studio instances and executing Lua code remotely via CLI and HTTP API.

## Overview

Roblox Studio Hub provides:
- **Multi-Studio Management** - Connect and manage multiple Roblox Studio instances simultaneously
- **Remote Code Execution** - Execute Lua code in Studio with three modes (eval, run, play)
- **CLI Interface** - Full-featured command line interface for all operations
- **System Service** - Run as background service with auto-start on boot

## Architecture

```
┌─────────────────┐     HTTP Long Polling     ┌─────────────────┐
│  Roblox Studio  │ ◄──────────────────────► │   Studio Hub    │
│    (Plugin)     │                           │    (Server)     │
└─────────────────┘                           └────────┬────────┘
                                                       │
                                              ┌────────▼────────┐
                                              │    CLI / API    │
                                              │  localhost:35888│
                                              └─────────────────┘
```

## Quick Start

### 1. Install Hub Server

必须保证当前运行在 `管理员` 权限中, 否则提醒用户并中断本次会话.

```bash
# Configure GitHub npm registry
npm config set @white-dragon-tools:registry https://npm.pkg.github.com

# Install globally
npm install -g @white-dragon-tools/roblox-studio-hub
```

### 2. Register as System Service (Recommended)

```bash
# Register as system service (auto-start on boot)
# Windows: Run as Administrator
# Mac/Linux: Use sudo
roblox-studio-hub install

# Check service status
roblox-studio-hub status
```

### 3. Install Studio Plugin

```bash
roblox-studio-hub install-plugin
```

### 4. Verify Setup

```bash
roblox-studio-hub status
```

## CLI Commands Reference

All commands support `-h` or `--help` for detailed help.

### Service Management

| Command | Description |
|---------|-------------|
| `roblox-studio-hub serve` | Run server in foreground (for debugging) |
| `roblox-studio-hub install` | Register as system service (auto-start) |
| `roblox-studio-hub uninstall` | Uninstall system service |
| `roblox-studio-hub start` | Start system service |
| `roblox-studio-hub stop` | Stop system service |
| `roblox-studio-hub status` | Check Hub service status |
| `roblox-studio-hub update` | Update to latest version (auto-handles service restart) |

### Studio Management

| Command | Description |
|---------|-------------|
| `roblox-studio-hub list` | List all connected Studios |
| `roblox-studio-hub info <studioId>` | Show Studio details |
| `roblox-studio-hub logs <studioId> [-n limit]` | View Studio logs |

### Code Execution

```bash
# Basic usage
roblox-studio-hub exec <studioId> <file> [-m mode]

# Examples
roblox-studio-hub exec place:123456 script.lua           # Execute with eval mode
roblox-studio-hub exec local:MyGame test.lua -m run      # Server-side test
roblox-studio-hub exec path:D:/Projects/MyGame test.lua --mode play  # Full play mode
```

### Plugin Management

```bash
roblox-studio-hub install-plugin    # Install Studio plugin
```

### Update Hub

```bash
roblox-studio-hub update
```

The update command automatically:
1. Stops running service
2. Executes npm update
3. Restarts service

## Execution Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `eval` | Direct execution via `loadstring` (default) | Quick scripts, simple tests |
| `run` | Server-side test via `StudioTestService` | Server logic testing |
| `play` | Full Play mode (server + client) | Complete game testing |

## Studio ID Format

- Cloud place: `place:{placeId}` (e.g., `place:123456`)
- Local file: `local:{placeName}` (e.g., `local:MyGame`)
- Custom path: `path:{localPath}` (e.g., `path:D:/Projects/MyGame`)

## Common Workflows

### Check Connected Studios

```bash
# List all connected Studios
roblox-studio-hub list

# Get details of a specific Studio
roblox-studio-hub info place:123456
```

### Execute Lua Script

```bash
# Create a test script
echo "print('Hello from Hub!'); return 42" > test.lua

# Execute on a connected Studio
roblox-studio-hub exec place:123456 test.lua
```

### View Studio Logs

```bash
# View last 100 logs (default)
roblox-studio-hub logs place:123456

# View last 50 logs
roblox-studio-hub logs local:MyGame -n 50
```

### Update Hub to Latest Version

```bash
# Update with automatic service handling
roblox-studio-hub update

# Update plugin if needed
roblox-studio-hub install-plugin
```

## API Reference (for programmatic access)

### Check Hub Status

```
GET /api/status
```

### List Connected Studios

```
GET /api/studios
```

### Get Studio Details

```
GET /api/studios/:id
```

### Get Studio Logs

```
GET /api/studios/:id/logs?limit=100
```

### Execute Code

```
POST /api/execute
Content-Type: application/json

{
  "studioId": "place:123456",
  "code": "print('Hello'); return 42",
  "mode": "eval",
  "timeout": 30
}
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STUDIO_HUB_PORT` | `35888` | Server port |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Studio not connecting | Enable HTTP requests in Studio Settings → Security |
| Connection timeout | Check firewall, verify port 35888 is open |
| Code execution fails | Check Lua syntax, review error in response |
| Studio disconnects | Hub removes inactive Studios after 35s without heartbeat |
| Service not starting | Run `roblox-studio-hub install` with admin/sudo privileges |
| Update fails | Run with admin/sudo privileges |

## Additional Resources

### Reference Files

For detailed API documentation and patterns:
- **`references/api-reference.md`** - Complete API specification
- **`references/lua-patterns.md`** - Common Lua code patterns for testing
