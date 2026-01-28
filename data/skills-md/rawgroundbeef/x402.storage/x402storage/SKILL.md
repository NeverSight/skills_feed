---
name: x402storage
description: Store files permanently on IPFS via x402.storage. Save and retrieve files across Claude Code sessions.
---

# x402.storage

Permanent file storage for Claude Code sessions using IPFS.

## Commands

- `/x402storage:setup` - Configure the MCP server and add a wallet
- `/x402storage:wallet` - Show all wallets with addresses and balances
- `/x402storage:switch-wallet` - Switch active wallet between EVM and Solana
- `/x402storage:store <file>` - Upload a file and get a permanent URL
- `/x402storage:fetch <url>` - Fetch content from an x402.storage URL
- `/x402storage:recall` - Restore context from last saved memory

## How It Works

Files uploaded via x402.storage are stored permanently on IPFS with branded URLs like `https://x402.storage/{cid}`. These URLs work forever - use them to persist artifacts between sessions.

$0.01 per file. $1 = 100 uploads. Pay once, store forever.

## Agent Memory Convention

x402.storage uses the `.agent/` directory convention for persistent memory:

```
.agent/
  x402storage/
    memory/
      INDEX.md      # Table of all stored memories with dates, descriptions, URLs
```

This convention allows:
- **Team sharing**: Commit `.agent/x402storage/memory/INDEX.md` to share context across team members
- **Interoperability**: Other agent tools can use `.agent/<tool-name>/` for their own storage
- **Simple recovery**: Read INDEX.md to see all stored memories and fetch the latest

INDEX.md contains a markdown table tracking all stored sessions.

## Multi-Wallet Support

x402.storage supports both EVM (Base/USDC) and Solana wallets. You can:
- Have wallets for both chains configured simultaneously
- Switch between them with `/x402storage:switch-wallet`
- Add additional wallets anytime with `/x402storage:setup`

Wallet configuration is stored in `~/.x402-config.json`.

## Setup Flow

When user runs `/x402storage:setup`:

1. **Check if MCP is configured**
   - Run: `claude mcp list | grep x402storage`
   - If found, proceed to check which wallets exist

2. **Check existing config**
   - Check if `~/.x402-config.json` exists
   - Parse to see which wallets are already configured

3. **Ask which chain to add** (use AskUserQuestion)
   - Options: "Base (USDC)" or "Solana (SOL)"
   - If that chain's wallet already exists, ask for confirmation before regenerating

4. **Generate wallet silently (NEVER output private keys)**
   - Base:
     ```bash
     npx -y @x402storage/mcp --generate-evm-wallet
     ```
   - Solana:
     ```bash
     npx -y @x402storage/mcp --generate-sol-wallet
     ```
   - IMPORTANT: Never cat, echo, or display the config file contents

5. **Add MCP (only if not already configured)**
   - If MCP not in list:
     ```bash
     claude mcp add x402storage -- npx @x402storage/mcp
     ```

6. **Output ONLY this**:
   ```
   {chain} wallet created!

   Send {USDC/SOL} to: {address}

   Pays for permanent IPFS storage. ~$0.01/MB.

   After restart, run /x402storage:wallet to verify.
   ```

No seed phrases, no verbose output. Just the address and next step.

## Store Flow

When user runs `/x402storage:store <file>`:

1. Check if `mcp__x402storage__store_file` tool is available
2. If not available, tell user to run `/x402storage:setup` first
3. Upload the file using the MCP tool
4. Create `.agent/x402storage/memory/` directory if it doesn't exist
5. Update INDEX.md with date, description, and URL
6. Return the permanent URL

## Recall Flow

When user runs `/x402storage:recall`:

1. Check if `.agent/x402storage/memory/INDEX.md` exists
2. If not found, tell user "No memory found. Store context first."
3. Read INDEX.md to get the last stored URL
4. Fetch that URL using WebFetch
5. Display the restored content

## Fetch Flow

When user runs `/x402storage:fetch <url>`:

1. Validate URL is an x402.storage URL
2. Fetch content using WebFetch
3. Display or offer to save to file

## Wallet Flow

When user runs `/x402storage:wallet`:

1. Check if MCP is configured
2. Call `mcp__x402storage__wallet` tool
3. Display all configured wallets with balances
4. Active wallet is marked with `[ACTIVE]`
5. If multiple wallets, mention `/x402storage:switch-wallet`

## Switch Wallet Flow

When user runs `/x402storage:switch-wallet`:

1. Check which wallets are configured in `~/.x402-config.json`
2. If only one wallet, tell user to add another with `/x402storage:setup`
3. Ask which wallet to make active
4. Call `mcp__x402storage__set_active_wallet` tool
5. Tell user to restart Claude Code for changes to take effect
