---
name: zscore
description: Register agents on the zScore ERC-8004 Identity Registry, manage wallets and metadata, and read on-chain state. Use when an agent needs to register on-chain, check fees, read agent info, set metadata, or manage agent wallets on Base Mainnet or Base Sepolia.
user-invocable: true
metadata: {"zScore":{"requires":{"env":["PRIVATE_KEY"],"bins":["node","npx"]},"primaryEnv":"PRIVATE_KEY"}}
---
# zScore ERC-8004 Identity Registry

Register and manage AI agents on the zScore Identity Registry. Defaults to Base Mainnet (0.0025 ETH fee). Use `--chain 84532` for Base Sepolia testnet.

## Install this skill

Install the latest version of this skill from the official repo:

```bash
npx skills add zerufinance/zscore -y
```

This installs the same skill that is published in the skills ecosystem (e.g. skills.sh). Use this command to get updates when the skill is updated.

## One-Time Setup

After installing the skill, run once to install dependencies (from the skill directory, e.g. `.cursor/skills/zscore/` or `~/.cursor/skills/zscore/`):

```bash
npm install
```

## Non-Negotiable Rule: No User Input, No Progress

This skill must be strictly interactive.

* **Do not create any JSON file** unless the user has provided (or explicitly skipped, where allowed) every required input.
* **Do not assume or invent values** (names, descriptions, URLs, versions, tool lists, skills, domains, trust models, etc.).
* **Do not proceed “using defaults”** unless the user explicitly agrees to each default you plan to use.
* **Do not reuse data from earlier chats, memory, or prior runs** unless the user explicitly provides it again (e.g. pastes the previous JSON or confirms the exact values).
* If any required value is missing, you must **ask for it and stop**. Do not produce a partial JSON, do not write files, and do not run commands.

This is the core safety/quality gate: **missing input blocks the workflow**.

## Agent Instructions: Registration Flow (Hard Gated)

When the user wants to **register an agent**, you must follow the gated flow below. The workflow has three phases:

1. **Collect inputs** (ask, then wait).
2. **Validate and summarise** (show what you will do).
3. **Proceed only after explicit approval** (create file, then run registration).

### Phase 1 — Collect inputs (ask, then stop)

You must ask the user for the inputs below. You may not move to Phase 2 until each item is resolved.

#### Required inputs (must be provided)

| Input           | Required? | Gate behaviour                                                                                                                |
| --------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Name**        | Yes       | Ask: “What should the agent name be?” (1–256 chars). If not provided, stop.                                                   |
| **Description** | Yes       | Ask: “What description should the agent have?” (max 2048 chars). If not provided, stop.                                       |
| **Services**    | Yes       | Ask: “Which service types do you want to publish?” Then collect full details for at least one service. If not provided, stop. |

#### Optional inputs (must be explicitly provided or explicitly skipped)

For every optional field, you must ask whether the user wants to set it. Only treat it as omitted if the user explicitly says **skip** (or equivalent).

| Input              | Required? | What to ask                                                                                                                                                           |
| ------------------ | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Image**          | No        | “Do you want to include an image URL (avatar/logo)? If yes, paste it. If no, say ‘skip’.”                                                                             |
| **x402Support**    | No        | “Does the agent support x402 payments? (true/false) Or say ‘skip’.”                                                                                                   |
| **active**         | No        | “Should the agent be marked as active? (true/false) Or say ‘skip’.”                                                                                                   |
| **supportedTrust** | No        | “Which trust models should be listed? (e.g. reputation, ERC-8004, crypto-economic, tee-attestation) Or say ‘skip’.”                                                   |

**Owner:** Do **not** ask the user for an owner address. The owner is always derived from the signer (the wallet that holds `PRIVATE_KEY`). The script sets it automatically; the API requires the document owner to match the signer so that the same wallet can update the document after minting.

#### Private key / funding gate (must be resolved before running registration)

* **Registration fee:** Base Mainnet (default): **0.0025 ETH**. Base Sepolia: **0.001 ETH**.
* The wallet must also have enough ETH for gas (recommend ~0.003 ETH total on mainnet).
* **Private key:** Registration requires a wallet. Ask the user to confirm one of these:

  * “`PRIVATE_KEY` is already set in the environment / OpenClaw config”, or
  * “I will provide `PRIVATE_KEY` for this run”.
* Never write the private key into any file. Never echo it back.

If the user does not confirm how `PRIVATE_KEY` will be provided, you must stop.

### Phase 2 — Validate and summarise (no file creation yet)

Once all required inputs are provided (and optional inputs are either provided or explicitly skipped):

1. Construct the JSON object in-memory using the **full** structure (see “Agent JSON Structure” below).
2. Validate:

   * `name` present and 1–256 chars
   * `description` present and ≤2048 chars
   * `services` has at least 1 item
   * each service matches its type-specific shape
3. Present a concise summary of what will be written (name, description length, services list, chain choice, fee).
4. Ask for explicit approval with a blocking question:
   **“Approve writing `agent.json` with these exact details? (yes/no)”**
   If the user does not say yes, stop.

### Phase 3 — Create the file and run registration (only after approval)

Only after the user explicitly approves:

1. Write the JSON to a file (e.g. `agent.json`).
2. Ask for the final explicit go-ahead:
   **“Proceed to register on-chain now? (yes/no)”**
   If not yes, stop.
3. Run registration:

   * Base Mainnet (default):
     `npx tsx ./scripts/zscore.ts register --json agent.json`
   * Base Sepolia:
     `npx tsx ./scripts/zscore.ts register --json agent.json --chain 84532`

Do not run the register command until all gating requirements are satisfied and the user has approved both:

* writing the JSON file, and
* executing the on-chain registration.

## Agent JSON Structure (ERC-8004 registration-v1)

Registration accepts **only** a JSON file. Use the **full** structure below when collecting user input and building the file. Do not default to a minimal structure.

**Full JSON (MCP + A2A + OASF + web + x402):**

```json
{
  "name": "DataAnalyst Pro",
  "description": "Enterprise-grade blockchain data analysis agent. Performs on-chain forensics, wallet profiling, and transaction pattern detection.",
  "image": "https://cdn.example.com/agents/analyst.png",
  "services": [
    {
      "name": "MCP",
      "endpoint": "https://api.dataanalyst.ai/mcp",
      "version": "2025-06-18",
      "mcpTools": ["analyze_wallet", "trace_transactions", "detect_anomalies"],
      "capabilities": []
    },
    {
      "name": "A2A",
      "endpoint": "https://api.dataanalyst.ai/.well-known/agent-card.json",
      "version": "0.3.0",
      "a2aSkills": ["analytical_skills/data_analysis/blockchain_analysis"]
    },
    {
      "name": "OASF",
      "endpoint": "https://github.com/agntcy/oasf/",
      "version": "0.8.0",
      "skills": ["analytical_skills/data_analysis/blockchain_analysis"],
      "domains": ["technology/blockchain"]
    },
    {
      "name": "web",
      "endpoint": "https://dataanalyst.ai"
    }
  ],
  "x402Support": true,
  "active": true,
  "supportedTrust": ["reputation", "ERC-8004"]
}
```

**All fields:**

| Field            | Type     | Required | Default                 | Description                                                                          |
| ---------------- | -------- | -------- | ----------------------- | ------------------------------------------------------------------------------------ |
| `name`           | string   | Yes      | —                       | Agent name (1–256 chars)                                                             |
| `description`    | string   | Yes      | —                       | What the agent does (max 2048 chars)                                                 |
| `image`          | string   | No       | omitted unless provided | Avatar URL (HTTPS, IPFS, or Arweave)                                                 |
| `services`       | array    | Yes      | —                       | Service endpoints (1–64 items, see below)                                            |
| `x402Support`    | boolean  | No       | omitted unless provided | Supports x402 payment protocol                                                       |
| `active`         | boolean  | No       | omitted unless provided | Agent is actively accepting requests                                                 |
| `supportedTrust` | string[] | No       | omitted unless provided | Trust models: `"reputation"`, `"crypto-economic"`, `"tee-attestation"`, `"ERC-8004"` |
| `owner`          | string   | No       | signer address          | Always set from signer (PRIVATE_KEY). Do not ask the user; the script sets it so the API allows update after mint. |

**Service types:**

| `name`   | `endpoint`                                      | Extra fields                                                                |
| -------- | ----------------------------------------------- | --------------------------------------------------------------------------- |
| `"web"`  | Website URL                                     | —                                                                           |
| `"MCP"`  | MCP server URL                                  | `version`, `mcpTools[]`, `mcpPrompts[]`, `mcpResources[]`, `capabilities[]` |
| `"A2A"`  | Agent card URL (`/.well-known/agent-card.json`) | `version`, `a2aSkills[]`                                                    |
| `"OASF"` | OASF repo URL                                   | `version`, `skills[]`, `domains[]`                                          |
| custom   | Any URL                                         | `description`                                                               |

## Commands

### `/zscore register --json <file>`

Register a new agent **only** via a JSON file. There is no flag-based registration (no `--name` / `--description` / `--endpoint`). Creates hosted agent URI, mints NFT on-chain, and updates URI with the real agentId.

```
/zscore register --json agent.json
/zscore register --json agent.json --chain 84532
```

**Required gated steps (must be followed in order):**

1. Collect required inputs: **name**, **description**, **at least one service with full type-specific fields**, and confirm how `PRIVATE_KEY` will be provided.
2. Collect optional inputs or explicit “skip” decisions for each optional field.
3. Validate and summarise the exact JSON you will write.
4. Get explicit approval to write `agent.json` (yes/no).
5. Write `agent.json`.
6. Get explicit approval to register on-chain (yes/no).
7. Run the registration command.

The SDK automatically adds `type`, `registrations` (with `agentId: 0` placeholder), and defaults for missing optional fields. After minting, it updates the document with the real `agentId`.

### `/zscore read <agentId>`

Read an agent's on-chain data: owner, URI, wallet, name, services.

```
/zscore read 16
```

To run: `npx tsx ./scripts/zscore.ts read 16`

### `/zscore fee`

Check current registration fee and whether registration is open.

```
/zscore fee
```

To run: `npx tsx ./scripts/zscore.ts fee`

### `/zscore set-metadata <agentId> --key <key> --value <value>`

Set custom metadata on an agent. Only the owner can call.

```
/zscore set-metadata 16 --key "category" --value "trading"
```

Requires `PRIVATE_KEY`.

To run: `npx tsx ./scripts/zscore.ts set-metadata 16 --key "category" --value "trading"`

### `/zscore unset-wallet <agentId>`

Clear the agent wallet. Only the owner can call.

```
/zscore unset-wallet 16
```

Requires `PRIVATE_KEY`.

To run: `npx tsx ./scripts/zscore.ts unset-wallet 16`

## Setup

### Read-Only (no setup needed)

`read` and `fee` work without a private key.

### With Wallet (for registration and writes)

Add to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "skills": {
    "entries": {
      "zscore": {
        "enabled": true,
        "env": {
          "PRIVATE_KEY": "0xYourFundedPrivateKey"
        }
      }
    }
  }
}
```

Optional env:

* `RPC_URL` — override default RPC
* `CHAIN_ID` — override chain (default: `8453` for Base Mainnet, use `84532` for Base Sepolia)

## Contract Info

### Base Mainnet (default, chainId 8453)

* **Identity Registry:** `0xFfE9395fa761e52DBC077a2e7Fd84f77e8abCc41`
* **Reputation Registry:** `0x187d72a58b3BF4De6432958fc36CE569Fb15C237`
* **Registration Fee:** 0.0025 ETH
* **RPC:** [https://mainnet.base.org](https://mainnet.base.org)

### Base Sepolia (testnet, chainId 84532)

* **Identity Registry:** `0xF0682549516A4BA09803cCa55140AfBC4e5ed2E0`

* **Reputation Registry:** `0xaAC7557475023AEB581ECc8bD6886d1742382421`

* **Registration Fee:** 0.001 ETH

* **RPC:** [https://sepolia.base.org](https://sepolia.base.org)

* **Source:** `zscore`

## How It Works

1. **register** creates a hosted JSON document (ERC-8004 registration-v1 schema) via the Agent URI API, mints an NFT on the Identity Registry (paying the fee), then updates the document with the real agentId.
2. **read** queries the on-chain contract for owner, tokenURI, and agentWallet, then fetches and parses the URI JSON.
3. **fee** reads the current `registrationFee()` and `registrationEnabled()` from the contract.
4. **set-metadata** calls `setMetadata(agentId, key, value)` on the contract.
5. **unset-wallet** calls `unsetAgentWallet(agentId)` on the contract.
