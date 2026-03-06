---
name: agentbox
description: "Provision dedicated AI agents on AgentBox via x402 payment ($5 USDC on Solana). Use when creating cloud instances running OpenClaw AI gateways with HTTPS and web terminal. Requires Node.js and a Solana wallet.json with USDC funds. Covers: provisioning new instances, polling status, interacting via OpenAI-compatible chat completions, extending, and listing instances."
metadata: {"openclaw": {"emoji": "📦", "requires": {"anyBins": ["node", "npx"]}}}
---

# AgentBox

Provision a dedicated AI agent by paying $5 USDC (Solana) via x402. Each agent runs an OpenClaw AI gateway with HTTPS, web terminal, and Solana wallet. Instances last 7 days (extendable).

Base URL: `https://api.agentbox.fyi`

## Prerequisites

```bash
npm install @x402/fetch @x402/svm @solana/kit
```

Requires a Solana wallet file (`solana-keygen` JSON format: 64-byte array) with USDC funds.

## 1. Provision

Create `provision.mjs` and run with `node provision.mjs /path/to/wallet.json [name]`:

```javascript
import { readFileSync } from "node:fs";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { registerExactSvmScheme } from "@x402/svm/exact/client";

const keypairBytes = new Uint8Array(
  JSON.parse(readFileSync(process.argv[2], "utf8")),
);
const signer = await createKeyPairSignerFromBytes(keypairBytes);

const client = new x402Client();
registerExactSvmScheme(client, { signer });
const x402Fetch = wrapFetchWithPayment(fetch, client);

const res = await x402Fetch("https://api.agentbox.fyi/provision", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(process.argv[3] ? { name: process.argv[3] } : {}),
});
console.log(JSON.stringify(await res.json(), null, 2));
```

Pays $5 USDC automatically via x402. Name is optional (auto-generated if omitted), must be DNS-safe: lowercase alphanumeric + hyphens, 3-63 chars.

**Response (201):**
```json
{
  "id": 12345678,
  "name": "boreal-enigma",
  "status": "provisioning",
  "gatewayToken": "pending",
  "accessToken": "eyJhbGci...",
  "expiresAt": "2026-03-11T10:00:00.000Z"
}
```

Save `id`, `name`, and `accessToken`.

## 2. Poll until running

```javascript
const { id, name, accessToken } = await res.json();

let instance;
for (let elapsed = 0; elapsed < 600; elapsed += 15) {
  await new Promise((r) => setTimeout(r, 15000));
  const poll = await fetch(`https://api.agentbox.fyi/provision/${id}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  instance = await poll.json();
  console.log(`[${elapsed}s] status=${instance.status} step=${instance.provisioningStep || "-"}`);
  if (instance.status === "running") break;
  if (instance.status === "error" || instance.status === "deleted") {
    throw new Error(`Provisioning failed: ${instance.status}`);
  }
}
```

Poll every 15 seconds. Boot takes 2-4 minutes, timeout after 10 minutes.

Status progression: `provisioning` -> `minting` -> `running`. The `minting` state is brief (SATI NFT minting). The response also includes a `provisioningStep` field with granular sub-states (`vm_created`, `configuring`, `wallet_created`, `openclaw_ready`, `services_starting`).

When `status` is `"running"`, the response includes the real `gatewayToken`:

```json
{
  "status": "running",
  "gatewayToken": "a58310a5f1f07...",
  "chatUrl": "https://boreal-enigma.agentbox.fyi/chat#token=...",
  "terminalUrl": "https://boreal-enigma.agentbox.fyi/terminal/..."
}
```

Save `gatewayToken` for API interaction.

## 3. Chat completions

Send messages using the OpenAI-compatible API on the VM:

```bash
curl -s https://NAME.agentbox.fyi/v1/chat/completions \
  -H "Authorization: Bearer GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello, what can you do?"}]}'
```

Replace `NAME` with the instance name and `GATEWAY_TOKEN` with `gatewayToken` from the poll response. Returns standard OpenAI chat completions JSON (non-streaming).

Each request is stateless. For multi-turn conversations, include the full message history:

```bash
curl -s https://NAME.agentbox.fyi/v1/chat/completions \
  -H "Authorization: Bearer GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages": [
    {"role": "user", "content": "What is 2+2?"},
    {"role": "assistant", "content": "4"},
    {"role": "user", "content": "Multiply that by 10"}
  ]}'
```

The response also includes additional fields beyond those shown in examples (`ownerWallet`, `ip`, `vmWallet`, `nftMint`, `terminalToken`, `provisioningStep`, `createdAt`). These can be safely ignored or stored as needed.

`terminalUrl` from the poll response opens a web terminal with shell access to the VM.

## Extend

Add 7 more days ($5 USDC). Reuse the x402 client from step 1:

```javascript
const res = await x402Fetch("https://api.agentbox.fyi/provision/INSTANCE_ID/extend", {
  method: "POST",
  headers: { Authorization: "Bearer ACCESS_TOKEN" },
});
```

Returns updated instance with new `expiresAt` and `accessToken`. Maximum lifetime: 90 days.

## List instances

List all instances owned by your wallet via Ed25519 signature:

```javascript
import { readFileSync } from "node:fs";
import { createKeyPairFromBytes, signBytes, getAddressFromPublicKey } from "@solana/kit";

const keypairBytes = new Uint8Array(JSON.parse(readFileSync("/path/to/wallet.json", "utf8")));
const keyPair = await createKeyPairFromBytes(keypairBytes);
const address = await getAddressFromPublicKey(keyPair.publicKey);
const timestamp = Date.now();
const message = `List AgentBox instances\nTimestamp: ${timestamp}`;
const signature = await signBytes(keyPair.privateKey, new TextEncoder().encode(message));
const sig64 = Buffer.from(signature).toString("base64");

const res = await fetch(
  `https://api.agentbox.fyi/provision?wallet=${address}&signature=${encodeURIComponent(sig64)}&timestamp=${timestamp}`
);
```

Returns `{ instances: [...] }` including `gatewayToken` and `terminalToken` for running instances (authenticated by wallet signature - only the wallet owner can list their own instances). Timestamp must be within 5 minutes of server time.

## Errors

| HTTP | Meaning |
|------|---------|
| 402 | Payment required (handled automatically by x402) |
| 409 | Instance name already taken |
| 502 | Provisioning failed (you are NOT charged) |
| 401 | Missing or invalid access token |
| 404 | Instance not found |

## Payment details

- **Network:** Solana mainnet (`solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`)
- **Amount:** $5 USDC per 7-day period
- **Asset:** USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`)

If provisioning fails (502), the payment is NOT settled.
