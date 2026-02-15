---
name: swarm-vault-manager-trading
description: "This skill enables you to execute swaps and transactions on behalf of Swarm Vault swarm members. You are acting as a manager's AI trading assistant.  When the user asks to execute a trade or make a transaction, you should use this skill to execute the trade or transaction across the swarm member wallets."
---

# Swarm Vault Manager Trading Skill

This skill enables you to execute swaps and transactions on behalf of Swarm Vault swarm members. You are acting as a manager's AI trading assistant.

## Overview

**Swarm Vault** is a platform where managers create "swarms" - groups of users who deposit funds into smart wallets. As a manager, you can execute transactions across all swarm member wallets simultaneously.

### Key Concepts

- **Swarm**: A group managed by you containing multiple users
- **Agent Wallet**: Each user's smart wallet within a swarm (ZeroDev Kernel wallet)
- **Holdings**: Aggregate token balances across all swarm members
- **Swap**: Exchange one token for another across all member wallets
- **Transaction**: Execute arbitrary smart contract calls across all member wallets

## Authentication

Before using this skill, ensure the environment is configured:

```bash
export SWARM_VAULT_API_KEY="svk_your_api_key_here"
export SWARM_VAULT_API_URL="https://api.swarmvault.xyz"  # Optional, defaults to production
```

Get your API key from the Swarm Vault settings page at https://swarmvault.xyz/settings

## Available Commands

### 1. Check Holdings

View aggregate token holdings across all swarm members.

```bash
pnpm check-holdings [swarmId] [--members]
```

**Arguments:**
- `swarmId`: Optional - if not provided, lists all swarms you manage
- `--members`: Optional - show per-member balances with membership IDs

**Output:** JSON with ETH balance, token balances, member count, and common tokens. When using `--members`, also includes per-member balance breakdown.

**Example - view all member balances:**
```bash
pnpm check-holdings abc-123 --members
```

This will output each member's:
- Membership ID (use with `--members` flag on swap commands for targeted swaps)
- Agent wallet address
- User wallet address
- ETH balance
- Token balances

### 2. Preview Swap

Preview a swap without executing it. Always preview before executing!

```bash
pnpm preview-swap <swarmId> <sellToken> <buyToken> [sellPercentage] [slippagePercentage] [--members id1,id2,...]
```

**Arguments:**
- `swarmId`: The swarm ID (UUID)
- `sellToken`: Token address to sell (or symbol like "USDC", "WETH", "ETH")
- `buyToken`: Token address to buy (or symbol)
- `sellPercentage`: Percentage of balance to sell (1-100, default: 100)
- `slippagePercentage`: Slippage tolerance (default: 1)
- `--members`: Optional comma-separated list of membership IDs to include (defaults to all active members)

**Output:** Per-member breakdown showing sell amounts, expected buy amounts, and any errors.

### 3. Execute Swap

Execute a swap across swarm member wallets.

```bash
pnpm execute-swap <swarmId> <sellToken> <buyToken> [sellPercentage] [slippagePercentage] [--members id1,id2,...]
```

**Arguments:**
- Same as preview-swap, including optional `--members` flag to target specific members

**Output:** Transaction ID that can be monitored with `check-transaction`.

**Example - swap for specific members only:**
```bash
pnpm execute-swap abc-123 USDC WETH 50 1 --members member-id-1,member-id-2
```

### 4. Execute Transaction

Execute a raw transaction template with placeholder support.

```bash
pnpm execute-transaction <swarmId> <templateJsonFile>
```

The template JSON file should contain an ABI-mode or raw-mode transaction template.

### 5. Check Transaction

Monitor a transaction's status.

```bash
pnpm check-transaction <transactionId> [--wait]
```

**Flags:**
- `--wait`: Poll until transaction completes (default: just check current status)

---

## Token Addresses

### Base Mainnet (Chain ID: 8453)

| Symbol | Address |
|--------|---------|
| ETH (Native) | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` |
| WETH | `0x4200000000000000000000000000000000000006` |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| DAI | `0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb` |
| USDbC | `0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA` |
| cbETH | `0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22` |

### Base Sepolia Testnet (Chain ID: 84532)

| Symbol | Address |
|--------|---------|
| ETH (Native) | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` |
| WETH | `0x4200000000000000000000000000000000000006` |
| USDC | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

---

## Template Placeholders

When constructing raw transactions, use these placeholders that get resolved per-member:

| Placeholder | Description | Example Output |
|-------------|-------------|----------------|
| `{{walletAddress}}` | Agent wallet address | `0x1234...abcd` |
| `{{ethBalance}}` | Current ETH balance in wei | `1000000000000000000` |
| `{{tokenBalance:0xAddress}}` | ERC20 token balance (raw units) | `500000000` |
| `{{percentage:ethBalance:50}}` | 50% of ETH balance | `500000000000000000` |
| `{{percentage:tokenBalance:0xAddr:100}}` | 100% of token balance | `500000000` |
| `{{blockTimestamp}}` | Current block timestamp | `1704567890` |
| `{{deadline:300}}` | Timestamp + N seconds (for swap deadlines) | `1704568190` |
| `{{slippage:amount:5}}` | Amount minus 5% (for minAmountOut) | `950000000` |

### Placeholder Examples

**Transfer 50% of USDC balance:**
```json
{
  "mode": "abi",
  "contractAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "abi": [{
    "name": "transfer",
    "type": "function",
    "inputs": [
      { "name": "to", "type": "address" },
      { "name": "amount", "type": "uint256" }
    ],
    "outputs": [{ "type": "bool" }]
  }],
  "functionName": "transfer",
  "args": ["0xRecipientAddress", "{{percentage:tokenBalance:0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913:50}}"],
  "value": "0"
}
```

**Approve max tokens for a DEX:**
```json
{
  "mode": "abi",
  "contractAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "abi": [{
    "name": "approve",
    "type": "function",
    "inputs": [
      { "name": "spender", "type": "address" },
      { "name": "amount", "type": "uint256" }
    ],
    "outputs": [{ "type": "bool" }]
  }],
  "functionName": "approve",
  "args": ["0xSpenderAddress", "115792089237316195423570985008687907853269984665640564039457584007913129639935"],
  "value": "0"
}
```

**Wrap ETH to WETH (50% of ETH balance):**
```json
{
  "mode": "abi",
  "contractAddress": "0x4200000000000000000000000000000000000006",
  "abi": [{
    "name": "deposit",
    "type": "function",
    "inputs": [],
    "outputs": []
  }],
  "functionName": "deposit",
  "args": [],
  "value": "{{percentage:ethBalance:50}}"
}
```

---

## Transaction Template Structure

### ABI Mode (Recommended)

Use ABI mode for type-safe contract interactions:

```json
{
  "mode": "abi",
  "contractAddress": "0x...",
  "abi": [{ "name": "functionName", "type": "function", "inputs": [...], "outputs": [...] }],
  "functionName": "functionName",
  "args": ["arg1", "{{placeholder}}", ...],
  "value": "0"
}
```

### Raw Calldata Mode (Advanced)

Use raw mode when you have pre-encoded calldata:

```json
{
  "mode": "raw",
  "contractAddress": "0x...",
  "data": "0xa9059cbb000000000000000000000000...",
  "value": "0"
}
```

---

## Common Operations

### Swap USDC to WETH

```bash
# Preview first
pnpm preview-swap <swarmId> USDC WETH 50 1

# If preview looks good, execute
pnpm execute-swap <swarmId> USDC WETH 50 1

# Monitor the transaction
pnpm check-transaction <transactionId> --wait
```

### Swap ETH to USDC

```bash
pnpm preview-swap <swarmId> ETH USDC 25 1
pnpm execute-swap <swarmId> ETH USDC 25 1
```

### Check What Tokens a Swarm Holds

```bash
pnpm check-holdings <swarmId>
```

---

## Error Handling

Common errors and solutions:

| Error Code | Meaning | Solution |
|------------|---------|----------|
| `AUTH_001` | Unauthorized | Check API key is set correctly |
| `RES_003` | Swarm not found | Verify swarm ID is correct |
| `PERM_002` | Not a manager | You can only trade for swarms you manage |
| `TX_003` | Insufficient balance | Members don't have enough tokens |
| `EXT_002` | 0x API error | Try again or check token addresses |

---

## Best Practices

1. **Always preview before executing** - Use `preview-swap` to see expected outcomes
2. **Start with small percentages** - Test with 10-25% before going to 100%
3. **Monitor transactions** - Use `check-transaction --wait` to ensure completion
4. **Check holdings first** - Know what tokens are available before swapping
5. **Use appropriate slippage** - 1% is usually fine, increase to 2-3% for volatile tokens

---

## Platform Fee

Swarm Vault charges a 0.5% fee on swaps, deducted from the buy token amount. This fee is displayed in swap previews.

---

## SDK Reference

This skill uses the `@swarmvault/sdk` package. For programmatic access beyond these scripts, you can use the SDK directly:

```typescript
import { SwarmVaultClient, BASE_MAINNET_TOKENS } from '@swarmvault/sdk';

const client = new SwarmVaultClient({
  apiKey: process.env.SWARM_VAULT_API_KEY,
});

// List your swarms
const swarms = await client.listSwarms();

// Get holdings
const holdings = await client.getSwarmHoldings(swarmId);

// Preview swap
const preview = await client.previewSwap(swarmId, {
  sellToken: BASE_MAINNET_TOKENS.USDC,
  buyToken: BASE_MAINNET_TOKENS.WETH,
  sellPercentage: 50,
});

// Execute swap
const result = await client.executeSwap(swarmId, {
  sellToken: BASE_MAINNET_TOKENS.USDC,
  buyToken: BASE_MAINNET_TOKENS.WETH,
  sellPercentage: 50,
});

// Wait for completion
const tx = await client.waitForTransaction(result.transactionId);
```
