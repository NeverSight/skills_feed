---
name: mirrord-quickstart
description: Guide users from zero to their first working mirrord session. Use when a user is new to mirrord, wants to install it, or needs help running their first session connecting to a Kubernetes cluster.
metadata:
  author: MetalBear
  version: "1.0"
---

# Mirrord Quickstart Skill

## Purpose

Help new users get mirrord running quickly:
- **Check** system requirements
- **Install** mirrord (CLI, VS Code, or IntelliJ)
- **Connect** to their first Kubernetes target
- **Verify** the connection works

## Critical First Steps

**Step 1: Detect user's environment**
Ask or detect:
- Operating system (macOS, Linux, Windows)
- Preferred workflow (CLI, VS Code, IntelliJ)
- Do they have kubectl configured?

**Step 2: Verify requirements**
```bash
# Check kubectl access
kubectl cluster-info
kubectl get pods -A | head -5
```

If kubectl fails, help them configure it first.

## Installation Paths

### CLI (recommended for getting started)

**macOS/Linux:**
```bash
brew install metalbear-co/mirrord/mirrord
```

Or without brew:
```bash
curl -fsSL https://raw.githubusercontent.com/metalbear-co/mirrord/main/scripts/install.sh | bash
```

**Windows:**
```bash
choco install mirrord
```

**Verify installation:**
```bash
mirrord --version
```

### VS Code Extension

1. Open VS Code Extensions (Cmd/Ctrl+Shift+X)
2. Search "mirrord"
3. Install "mirrord" by MetalBear
4. Look for mirrord icon in status bar

### IntelliJ Plugin

1. Open Settings → Plugins → Marketplace
2. Search "mirrord"
3. Install and restart IDE
4. Find mirrord in navigation toolbar

## First Session

### CLI approach

```bash
# List available targets
mirrord ls

# Run a local process with mirrord
mirrord exec --target pod/<pod-name> -- <your-command>

# Example: Node.js app
mirrord exec --target pod/api-server-7c8d9 -- node app.js

# Example: Python app
mirrord exec --target pod/backend-abc123 -- python main.py
```

### IDE approach

1. Enable mirrord (click status bar icon / toolbar button)
2. Select target pod when prompted
3. Run/debug your application normally
4. mirrord intercepts and connects automatically

## Verification

After running, verify the connection:

1. **Check logs** - You should see mirrord initialization messages
2. **Test environment** - Remote env vars should be available locally
3. **Test network** - Make a request to your remote service; it should reach your local process

```bash
# Quick test: print remote env vars
mirrord exec --target pod/<pod-name> -- env | grep -i database
```

## Common First-Timer Issues

| Issue | Solution |
|-------|----------|
| "kubectl not found" | Install kubectl and configure cluster access |
| "No pods found" | Check namespace: `kubectl get pods -n <namespace>` |
| "Permission denied" | Check RBAC permissions for your kubectl context |
| "Agent failed to start" | Ensure cluster runs Linux kernel 4.20+ |

## Response Guidelines

1. **Ask about their setup** - OS, IDE preference, existing kubectl access
2. **Go step by step** - Don't overwhelm with all options at once
3. **Verify each step** - Confirm installation worked before moving on
4. **Celebrate success** - When they connect, explain what just happened

## Example Interaction

**User:** "I want to try mirrord"

**Response:**
1. Ask: macOS/Linux/Windows? CLI or IDE?
2. Check: `kubectl cluster-info` working?
3. Install: One command based on their OS
4. Run: `mirrord ls` to see targets
5. Connect: `mirrord exec --target pod/X -- <their-app>`
6. Verify: Show them it's working
