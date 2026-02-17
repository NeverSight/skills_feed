---
name: starknet-anonymous-wallet
description: Create an anonymous Starknet wallet via Typhoon and interact with Starknet contracts. Privacy-focused wallet creation for agents requiring anonymity.
license: Apache-2.0
metadata: {"author":"starknet-agentic","version":"1.0.0","org":"keep-starknet-strange"}
keywords: [starknet, wallet, anonymous, transfer, balance, anonymous-agent-wallet, strk, eth, privacy, typhoon]
allowed-tools: [Bash, Read, Write, Glob, Grep, Task]
user-invocable: true
---

# starknet-anonymous-wallet

This skill provides **agent-facing scripts** for:
- Creating/loading a Starknet account (Typhoon flow)
- Discovering ABI / functions
- Reading & writing to contracts
- Preflight (simulate + fee estimate)
- Allowance checks with human amounts

## Prerequisites

```bash
npm install starknet@^9.2.1 typhoon-sdk@^1.1.13
```

### RPC setup (required for onchain reads/writes)

These scripts talk to Starknet via JSON-RPC. Configure one of:

- Set `STARKNET_RPC_URL` in your environment (recommended), OR
- Pass `rpcUrl` in the JSON input for scripts that support it.

If neither is provided, scripts fall back to the public Lava mainnet RPC:
- `https://rpc.starknet.lava.build:443`

## CRITICAL: Account Creation Flow

When the user asks to create a anonymous Starknet account (in any form like "create an anonymous account", "create a Starknet anonymous account for my agent", "I need a anonymous wallet", etc.), **ALWAYS follow this flow**:

### Step 1: Check if account already exists

```bash
node scripts/check-account.js
```

**If `hasAccount: false`:**
- Proceed to Step 2

### Step 2: Provide funding instructions

Tell the user:

---

**To create your Starknet account, you need to fund it through Typhoon:**

1. Go to the Typhoon website: https://www.typhoon-finance.com/app
2. Make a deposit and download your deposit note
   - **Recommended:** Make a STRK deposit (this will be used to deploy and fund your agent account)
3. Copy **all the content** of your downloaded note file and paste it here

---

Then **wait for the user to paste the note content**.

### Step 3: Create the account

> Note: **Account creation can take a few minutes**. Typhoon proof generation + Starknet deployment/finality are not instant; tell the user to wait and avoid retrying unless it fails.

Once the user pastes the note JSON, run:

```bash
node scripts/create-account.js '<paste the note JSON here>'
```

The note format is:
```json
{
  "secret": "0x...",
  "nullifier": "0x...",
  "txHash": "0x...",
  "pool": "0x...",
  "day": "0x..."
}
```

### Step 4: Confirm success

After successful creation, show the user:
- Their new account address
- Explorer link (Voyager/Starkscan)
- Remind them the private key is stored securely

---

## Show Account Address

When user asks "what's my address", "show my wallet", "my account address", etc.:

```bash
node scripts/show-address.js
```

If multiple accounts exist, it returns all. Pass index to get specific one:
```bash
node scripts/show-address.js 0
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `check-account.js` | Check if account(s) exist |
| `show-address.js` | Show account address(es) |
| `load-account.js` | Load an existing local account artifact |
| `create-account.js` | Create + deploy a new account via Typhoon |
| `get-abi.js` | Fetch ABI summary + list functions (+ optional candidate ranking) |
| `call-contract.js` | Call a view function |
| `invoke-contract.js` | Call an external function |
| `check-allowance.js` | Check ERC20 allowance (supports human amount) |
| `multicall.js` | Execute multiple calls in one tx |
| `estimate-fee.js` | Preflight fee estimate for a call/multicall |
| `simulate.js` | Preflight simulate for a call/multicall |
| `token-info.js` | Token metadata (decodes felt short strings) |
| `decode-felt.js` | Decode felt short strings |
| `sign-typed-data.js` | Sign typedData (for SIWS / Starkbook-style auth) |
| `sign-invoke-tx.js` | Sign an INVOKE transaction (one or more calls) without broadcasting |

---
## Core Agent Workflow (no hardcoding)

### 1) Address & docs discovery (agent planning)
If the user mentions protocols/tokens/apps (e.g. "Ekubo", "STRK", "ETH"), the **agent must first search** for:
- The relevant contract addresses
- The protocol documentation

**Research constraint:** all agent research must be done through **MCP** (Model Context Protocol) — no interactive browser/UI. Use machine-readable sources (APIs, docs URLs, GitHub raw files) via agent fetch tools.

This skill does **not** do web search by itself; it provides the onchain tooling once addresses are known.

### 2) Load account
```bash
node scripts/load-account.js
```

### 3) ABI discovery (+ optional ranking)
```bash
node scripts/get-abi.js '{"contractAddress":"0x..."}'
```

If you want the script to return **ranked candidates** (to help the agent decide), pass a `query`:
```bash
node scripts/get-abi.js '{"contractAddress":"0x...","query":"swap exact tokens for tokens"}'
```

### 4) Read
```bash
node scripts/call-contract.js '{"contractAddress":"0x...","method":"<view_fn>","args":[...]}'
```

Optional: decode felt short strings:
```bash
node scripts/call-contract.js '{"contractAddress":"0x...","method":"symbol","args":[],"decodeShortStrings":true}'
```

### 5) Allowance check (raw or human)
Raw base units:
```bash
node scripts/check-allowance.js '{"tokenAddress":"0x...","ownerAddress":"0x...","spenderAddress":"0x...","requiredAmount":"20000000000000000000"}'
```
Human amount (script fetches decimals):
```bash
node scripts/check-allowance.js '{"tokenAddress":"0x...","ownerAddress":"0x...","spenderAddress":"0x...","requiredAmountHuman":"20"}'
```

### 6) Preflight (recommended)
Fee estimate:
```bash
node scripts/estimate-fee.js '{"privateKeyPath":"...","accountAddress":"0x...","calls":[{"contractAddress":"0x...","method":"...","args":[...]}]}'
```
Simulation:
```bash
node scripts/simulate.js '{"privateKeyPath":"...","accountAddress":"0x...","calls":[{"contractAddress":"0x...","method":"...","args":[...]}]}'
```

### 7) Execute
Single write:
```bash
node scripts/invoke-contract.js '{"privateKeyPath":"...","accountAddress":"0x...","contractAddress":"0x...","method":"...","args":[...]}'
```

---

## Sign typedData (for Starkbook / SIWS)

When you need a Starknet account to sign a SIWS challenge (typedData) **without ever exposing the private key**, use:

```bash
node scripts/sign-typed-data.js '{
  "accountAddress":"0x...",
  "typedData": { "domain": { }, "types": { }, "primaryType": "Message", "message": { } }
}'
```

Or if you saved the typedData to a file:

```bash
node scripts/sign-typed-data.js '{
  "accountAddress":"0x...",
  "typedDataPath":"/tmp/typedData.json"
}'
```

Output is a signature array (hex strings) that can be submitted to verification endpoints (e.g. Starkbook `/api/auth/verify`).

---

## Sign an INVOKE transaction (no broadcast)

To sign a transaction **without sending it**, use:

```bash
node scripts/sign-invoke-tx.js '{
  "accountAddress":"0x...",
  "calls":[
    {"contractAddress":"0xTOKEN","entrypoint":"transfer","calldata":["0xTO","<uint256_low>","<uint256_high>"]}
  ]
}'
```

Or with ABI args (the script will fetch ABI and compile calldata for you):

```bash
node scripts/sign-invoke-tx.js '{
  "accountAddress":"0x...",
  "calls":[
    {"contractAddress":"0xTOKEN","method":"transfer","args":["0xTO","123"]}
  ]
}'
```

This returns an `invokeTransaction` payload suitable for RPC `starknet_addInvokeTransaction` (signature included) plus a fee estimate.

⚠️ Not broadcast: this script only signs. To actually send, you must submit the payload to an RPC endpoint (and you should confirm before broadcasting).

### Starkbook end-to-end helper (recommended)
If you want a single command that does challenge → sign locally → verify → (optional) post **without Starkbook ever touching a private key**:

```bash
node scripts/starkbook-client.js '{
  "base":"http://localhost:3000",
  "accountAddress":"0x...",
  "action":"post",
  "body":"hello from agent",
  "linkUrl":"https://example.com"
}'
```

Approve + action in one tx:
```bash
node scripts/multicall.js '{"privateKeyPath":"...","accountAddress":"0x...","calls":[{"contractAddress":"0x...","method":"approve","args":["0xspender","123"]},{"contractAddress":"0x...","method":"...","args":[...]}]}'
```
