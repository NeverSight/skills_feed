---
name: config
description: View and modify fibx CLI configuration, such as setting custom RPC URLs to avoid rate limits.
license: MIT
compatibility: Requires Node.js 18+ and npx. Works with fibx CLI v0.3.7+.
metadata:
    version: 0.3.7
    author: ahmetenesdur
    category: utility
allowed-tools:
    - Bash(npx fibx@latest config *)
---

# Configuration Management

Manage local configuration for the `fibx` CLI. The primary use case is setting custom RPC URLs for supported chains to bypass public RPC rate limits or connection issues.

## Prerequisites

- None.

## Rules

1. **Rate Limits**: If a tool fail with a "Rate limit exceeded" or "429" error, use this skill to check the current RPC and set a new one.
2. **Persistence**: Settings are stored locally in `~/.config/fibx/config.json` (OS dependent) and persist across sessions.
3. **Validation**: The CLI validates URLs format but not connectivity. Ensure the RPC URL is valid before setting.

## Commands

```bash
# Set a custom RPC
npx fibx@latest config set-rpc <chain> <url>

# Get current RPC
npx fibx@latest config get-rpc <chain>

# List all configs
npx fibx@latest config list
```

## Parameters

| Parameter | Type   | Description                              | Required |
| --------- | ------ | ---------------------------------------- | -------- |
| `chain`   | string | `base`, `citrea`, `hyperevm`, or `monad` | Yes      |
| `url`     | string | The full HTTP(S) RPC endpoint URL        | Yes      |

## Examples

**User:** "I'm getting rate limit errors on Base."
**Agent:** "I will set a custom RPC for Base."

```bash
npx fibx@latest config set-rpc base https://mainnet.base.org
```

**User:** "Check my current configuration."

```bash
npx fibx@latest config list
```

**User:** "Reset Base RPC to default?"
**Agent:** (Currently no reset command, but user can overwrite or manually delete config) "I will set it to a known good public RPC."

```bash
npx fibx@latest config set-rpc base https://mainnet.base.org
```

## Error Handling

| Error               | Action                                         |
| ------------------- | ---------------------------------------------- |
| `Unsupported chain` | Check spelling of chain name.                  |
| `Invalid URL`       | Ensure URL starts with `http://` or `https://` |
