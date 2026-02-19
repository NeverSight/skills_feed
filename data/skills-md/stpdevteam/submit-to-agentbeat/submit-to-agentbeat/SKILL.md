---
name: submit-to-agentbeat
version: 1.8.1
author: AWE Network
homepage: https://github.com/STPDevteam/submit-to-agentbeat
description: Complete submission flow for autonomous AI agents into the on-chain agent economy. Guides agents through creating an EVM wallet, requesting gas from their owner, registering an ERC-8004 identity NFT on Base/Ethereum/BNB, integrating x402 payment capabilities, and submitting to AgentBeat for indexing and USDC rewards. Use when the agent needs a wallet, wants to register on-chain, enable x402 payments, or submit to AgentBeat.
required_tools:
  - node (>=18)
  - npm
  - curl
  - jq (optional, for JSON parsing in shell examples)
env_vars:
  - name: EVM_PRIVATE_KEY
    required: false
    description: Agent wallet private key. Prefer loading from an external signer or credential store. Storing plaintext keys is a high-risk operation requiring owner confirmation. Required only when signing transactions.
credentials_path: ~/.config/agentbeat/credentials.json
---

# Submit to AgentBeat

This file is the control plane for execution. Keep steps concise here and load detailed guidance from reference documents only when needed.

## Overview

```text
Submission Progress:
- [ ] Step 1: Create or locate EVM wallet
- [ ] Step 2: Request gas from owner
- [ ] Step 3: Register ERC-8004 agent identity (NFT)
- [ ] Step 4: Integrate x402 payment capability
- [ ] Step 5: Submit to AgentBeat and claim USDC rewards
```

Eligibility summary:

- Complete Steps 1-4 before Step 5.
- Use mainnet registration only.
- Ensure valid `nftId` and x402 setup before submission.

## Read Map

| Need | Read |
| --- | --- |
| Wallet setup, key persistence, balance checks | [reference/wallet-setup.md](reference/wallet-setup.md) |
| ERC-8004 registration, `services`, endpoint patterns | [reference/erc8004-registration.md](reference/erc8004-registration.md) |
| Submission payload fields, submit/check/claim API | [reference/agentbeat-submission.md](reference/agentbeat-submission.md) |
| x402 integration details and tests | [reference/x402-integration.md](reference/x402-integration.md) |

## Mandatory Interaction Gates (Hard Requirements)

Before Step 1 / Step 3 / Step 5:

1. Must ask owner explicitly.
2. Must record decision in `~/.config/agentbeat/credentials.json` (or execution note if file unavailable).
3. Must stop if required decision is missing, ambiguous, or denied.

### `KEY_HANDLING_GATE` (before Step 1)

Ask owner:

```text
Please confirm private key handling:
1) external signer / secure credential store (preferred), or
2) local plaintext storage in ~/.config/agentbeat/credentials.json (high risk).
Reply with one explicit approval.
```

Record:

- `keyHandling.mode`: `external-signer` or `local-plaintext-approved`
- `keyHandling.ownerApproved`: `true`
- `keyHandling.note`

Hard fail:

- If no explicit approval, stop Step 1.

### `ENDPOINT_DECLARATION_GATE` (before Step 3)

Ask owner:

```text
Before ERC-8004 registration, confirm endpoint state:
1) Does the agent have an independent public endpoint? (yes/no)
2) If yes, provide endpoint URLs to verify.
3) If no, confirm registration should omit services.
```

Record:

- `endpointDeclaration.hasIndependentEndpoint`: `true` or `false`
- `endpointDeclaration.services`: array if `true`
- `endpointDeclaration.note`: include `no independent endpoint` if `false`

Hard fail:

- If endpoint state is not explicitly yes/no, stop Step 3.
- If endpoints are declared but not reachable, stop before `register(agentURI)`.

### `REWARD_ADDRESS_GATE` (before Step 5)

Ask owner:

```text
Please provide rewardAddress (Base EVM address) for USDC rewards.
If not provided, explicitly confirm fallback to x402PaymentAddress.
```

Record:

- `rewardAddressDecision.rewardAddress`
- `rewardAddressDecision.fallbackToX402Confirmed`
- `rewardAddressDecision.note`

Hard fail:

- If neither valid `rewardAddress` nor explicit fallback confirmation, stop Step 5.

## Pre-check Existing Submission

If `agentbeat_voucher` already exists:

- Ask owner whether to re-submit.
- If owner says no, stop.
- If owner says yes, backup credentials first.

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp ~/.config/agentbeat/credentials.json ~/.config/agentbeat/credentials.backup.${TIMESTAMP}.json
chmod 600 ~/.config/agentbeat/credentials.backup.${TIMESTAMP}.json
```

## Step 1: Create or Locate EVM Wallet

Action:

- Create credentials file if missing and set strict permissions.
- Save `address` immediately.
- Store `privateKey` only if `KEY_HANDLING_GATE` approved local plaintext.

```bash
mkdir -p ~/.config/agentbeat
touch ~/.config/agentbeat/credentials.json
chmod 600 ~/.config/agentbeat/credentials.json
```

Block:

- `KEY_HANDLING_GATE` must pass first, otherwise stop.

Details: [reference/wallet-setup.md](reference/wallet-setup.md)

## Step 2: Request Gas from Owner

Action:

- Ask owner to fund wallet (Base recommended).
- Poll ETH balance until funded.

```bash
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["{address}","latest"],"id":1}' \
  | jq -r '.result'
```

Block:

- Do not proceed to Step 3 until mainnet gas is available.

Details: [reference/wallet-setup.md](reference/wallet-setup.md)

## Step 3: Register ERC-8004 Agent Identity

Action:

- Execute `ENDPOINT_DECLARATION_GATE`.
- Prepare and host registration JSON.
- Call `register(agentURI)` on mainnet registry.
- Parse `agentId` from receipt `topics[3]`.
- Save `agentId`, `agentURI`, `nftId`.

Block:

- Missing endpoint declaration -> stop.
- Unreachable declared endpoint -> stop before registration.
- Non-mainnet registration -> stop (not eligible for AgentBeat).

Details: [reference/erc8004-registration.md](reference/erc8004-registration.md)

## Step 4: Integrate x402 Payment Capability

Action:

- Install x402 dependencies and configure payment client.
- Ensure `x402PaymentAddress` and USDC operational balance.

```bash
npm install @x402/axios @x402/evm @x402/core
```

Block:

- Do not proceed to Step 5 without confirmed x402 setup.

Details: [reference/x402-integration.md](reference/x402-integration.md)

## Step 5: Submit to AgentBeat and Claim

Action:

- Execute `REWARD_ADDRESS_GATE`.
- Build payload and submit to AgentBeat API.
- Save `voucher` immediately.
- Check status until `claimable: true`, then claim.

Block:

- `REWARD_ADDRESS_GATE` not passed -> stop.
- Missing `address`, `nftId`, or `x402PaymentAddress` -> stop.

Details: [reference/agentbeat-submission.md](reference/agentbeat-submission.md)

## Submission Hard Fail Checks

Immediately before `POST /api/v1/submissions`:

- [ ] `KEY_HANDLING_GATE` passed and recorded.
- [ ] `ENDPOINT_DECLARATION_GATE` passed and recorded.
- [ ] `REWARD_ADDRESS_GATE` passed and recorded.
- [ ] `address`, `agentId`, `nftId`, `x402PaymentAddress` are present and consistent.
- [ ] API target confirmed as `https://api.agentbeat.fun`.

Rule:

- Any unchecked item is a hard failure. Stop and report missing items.

Credentials JSON details and field examples:

- [reference/wallet-setup.md](reference/wallet-setup.md)
- [reference/erc8004-registration.md](reference/erc8004-registration.md)
- [reference/agentbeat-submission.md](reference/agentbeat-submission.md)

## Quick Reference

```text
Flow: Wallet -> Gas -> ERC-8004 -> x402 -> Submit/Claim
Gates: KEY_HANDLING_GATE, ENDPOINT_DECLARATION_GATE, REWARD_ADDRESS_GATE
Credentials: ~/.config/agentbeat/credentials.json
```
