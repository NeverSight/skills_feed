---
name: vercel-ai-gateway-setup
description: Set up Claude Code to route requests through Vercel AI Gateway for monitoring and observability
compatibility: Designed for Claude Code
---

# Vercel AI Gateway Setup Skill

## Description

This skill sets up Claude Code to route requests through Vercel AI Gateway for monitoring and observability. It supports two modes: API Key mode (using a Vercel AI Gateway API key) and Claude Max mode (using an existing Claude Code Max subscription through the gateway).

## Instructions

When the user invokes this skill, guide them through the Vercel AI Gateway setup interactively. **Never ask for or handle API keys directly.** The user must enter their own keys. **Never read the user's shell config file** (`~/.zshrc`, `~/.bashrc`, `~/.bash_profile`, `~/.profile`, etc.) during setup — it may already contain secrets. Only append to it.

### Step 1: Check prerequisites

Run the following to confirm Claude Code CLI is installed:

```bash
command -v claude
```

If not found, tell the user to install it with `npm install -g @anthropic-ai/claude-code`.

### Step 2: Ask the user which mode they want

Present two options:

1. **API Key mode** — Uses a Vercel AI Gateway API key for all requests. The user provides their own API key in their shell config.
2. **Claude Max mode** — Uses the user's existing Claude Code Max subscription, routing through the gateway for observability only.

### Step 3: Ask about macOS Keychain (macOS only)

If the platform is macOS (`darwin`), ask if they want to store the key in macOS Keychain for extra security.

### Step 4: Run the setup script

Execute the setup script using **named arguments** based on the user's choices from Steps 2 and 3. Always use named arguments — never run the script without them.

**Available arguments:**
- `--mode apikey` or `--mode max` — the setup mode chosen by the user
- `--keychain` or `--no-keychain` — whether to use macOS Keychain (macOS only)
- `--confirm` — auto-confirm appending config to the shell profile
- `--logout` or `--no-logout` — whether to log out of Claude Code (API key mode)

**Examples:**

```bash
# API Key mode with Keychain
bash scripts/setup-vercel-ai-gateway.sh --mode apikey --keychain --confirm --logout

# Claude Max mode without Keychain
bash scripts/setup-vercel-ai-gateway.sh --mode max --no-keychain --confirm
```

The script will:
- Detect the user's shell config file (`~/.zshrc`, `~/.bashrc`, etc.)
- Generate the appropriate environment variable block
- Show the user what will be added
- Append it to their shell config
- Optionally log out of Claude Code (for API key mode)

### Step 5: Remind the user of manual steps

After the script completes, remind the user they need to:

1. **Replace the placeholder** `<YOUR_AI_GATEWAY_API_KEY>` in their shell config with their actual key (or store it in Keychain if they chose that option). **Claude Code must never see or handle the actual API key.**
2. **Reload their shell**: `source ~/.zshrc` (or their shell config)
3. **Start Claude Code**: `claude`

### Environment variables reference

**API Key mode:**
```
ANTHROPIC_BASE_URL="https://ai-gateway.vercel.sh"
ANTHROPIC_AUTH_TOKEN="<key>"
ANTHROPIC_API_KEY=""           # must be empty so AUTH_TOKEN is used
```

**Claude Max mode:**
```
ANTHROPIC_BASE_URL="https://ai-gateway.vercel.sh"
ANTHROPIC_CUSTOM_HEADERS="x-ai-gateway-api-key: Bearer <key>"
```

**macOS Keychain storage:**
```bash
security add-generic-password -a "$USER" -s "ANTHROPIC_AUTH_TOKEN" -w "<key>"
```

**macOS Keychain retrieval (used in shell config):**
```bash
export ANTHROPIC_AUTH_TOKEN=$(security find-generic-password -a "$USER" -s "ANTHROPIC_AUTH_TOKEN" -w)
```

### Important security notes

- **Never** ask the user to paste their API key into the chat or any tool call.
- **Never** read, echo, or log the value of `ANTHROPIC_AUTH_TOKEN` or any API key variable.
- **Never** read the user's shell config file (e.g. `~/.zshrc`) — it may contain existing secrets. Only append new config blocks to it.
- The script uses `<YOUR_AI_GATEWAY_API_KEY>` as a placeholder. The user replaces it manually.
- If using Keychain, the user runs the `security add-generic-password` command themselves in their terminal.
