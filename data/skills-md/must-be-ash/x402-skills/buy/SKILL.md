---
name: buy
description: Pay for x402-protected API endpoints with USDC. Use when calling APIs that return HTTP 402 Payment Required, integrating payments into agents, handling x402 payment requirements, building autonomous agents that pay for API access, or discovering paid services via Bazaar. Supports EVM (Base, Ethereum, Avalanche) and Solana networks.
---

# x402 Buy Skill

Enable AI agents to autonomously pay for HTTP resources using the x402 payment protocol.

## Overview

x402 is an open payment standard that enables programmatic payments over HTTP. When an agent requests a paid resource, the server responds with HTTP 402 (Payment Required) containing payment details. The agent signs a payment authorization and retries the request.

## CRITICAL: Pre-Flight Check (Do This First!)

**ALWAYS check the endpoint's x402 version BEFORE writing any payment code.**

```bash
curl -i "https://example.com/api/paid-endpoint"
```

Look at the 402 response to determine which version and packages to use:

### How to Identify Version

| Check This | v1 (Legacy) | v2 (Current) |
|------------|-------------|--------------|
| `x402Version` field | `1` | `2` |
| Network format | `"base"`, `"base-sepolia"` | `"eip155:8453"`, `"eip155:84532"` (CAIP-2) |
| Requirements location | Body only | `PAYMENT-REQUIRED` header |
| Payment header to send | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| Response header | `X-PAYMENT-RESPONSE` | `PAYMENT-RESPONSE` |

**Example v1 response:**
```json
{"x402Version":1,"accepts":[{"network":"base","maxAmountRequired":"2000",...}]}
```

**Example v2 response:**
```
PAYMENT-REQUIRED: <base64-encoded>
{"x402Version":2,"accepts":[{"network":"eip155:8453","maxAmountRequired":"2000",...}]}
```

## Quick Start

### 1. Setup Wallet

**Non-interactive CLI commands (for AI agents):**

```bash
# EVM wallet (Base, Ethereum, Avalanche) - pipes "1" to select EOA
echo "1" | npx add-wallet evm

# Solana wallet
npx add-wallet sol

# Top up with testnet USDC
npx add-wallet topup testnet
```

This creates a `.env` file with `WALLET_ADDRESS` and `WALLET_PRIVATE_KEY`.

### 2. Install Packages (Based on Version)

**For v1 endpoints:**
```bash
npm install x402-fetch viem
```

**For v2 endpoints:**
```bash
npm install @x402/fetch @x402/evm viem
# Optional for Solana: npm install @x402/svm @solana/kit @scure/base
```

### 3. Make Paid Requests

#### For v1 Endpoints (Legacy)

```typescript
import { wrapFetchWithPayment, createSigner, decodeXPaymentResponse } from "x402-fetch";

const privateKey = process.env.WALLET_PRIVATE_KEY as `0x${string}`;

// Use network string from 402 response: "base", "base-sepolia", "solana", etc.
const signer = await createSigner("base", privateKey);
const fetchWithPayment = wrapFetchWithPayment(fetch, signer);

const response = await fetchWithPayment("https://api.example.com/paid", { method: "GET" });
const data = await response.json();

// Check payment receipt
const paymentResponse = response.headers.get("x-payment-response");
if (paymentResponse) {
  const receipt = decodeXPaymentResponse(paymentResponse);
  console.log("Payment settled:", receipt);
}
```

#### For v2 Endpoints (Current)

```typescript
import { wrapFetchWithPayment, x402Client } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const signer = privateKeyToAccount(process.env.WALLET_PRIVATE_KEY as `0x${string}`);
const client = new x402Client();
registerExactEvmScheme(client, { signer });

const fetchWithPayment = wrapFetchWithPayment(fetch, client);
const response = await fetchWithPayment("https://api.example.com/paid", { method: "GET" });

// Check payment receipt
const paymentResponse = response.headers.get("PAYMENT-RESPONSE");
```

## Package Reference

| Purpose | v1 (Legacy) | v2 (Current) |
|---------|-------------|--------------|
| Fetch wrapper | `x402-fetch` | `@x402/fetch` |
| Axios wrapper | `x402-axios` | `@x402/axios` |
| Core types | `x402` | `@x402/core` |
| EVM support | Built into x402-fetch | `@x402/evm` |
| Solana support | Built into x402-fetch | `@x402/svm` |

## Network Identifiers

| Network | v1 ID | v2 CAIP-2 ID | Environment |
|---------|-------|--------------|-------------|
| Base Mainnet | `base` | `eip155:8453` | Production |
| Base Sepolia | `base-sepolia` | `eip155:84532` | Testnet |
| Avalanche C-Chain | `avalanche` | `eip155:43114` | Production |
| Avalanche Fuji | `avalanche-fuji` | `eip155:43113` | Testnet |
| Solana Mainnet | `solana` | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Production |
| Solana Devnet | `solana-devnet` | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | Testnet |

## USDC Token Addresses

| Network | USDC Address |
|---------|-------------|
| Base Mainnet | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Base Sepolia | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| Avalanche | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |
| Solana Mainnet | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

## Complete Working Examples

### Example 1: Calling a v1 Endpoint

```typescript
// call-v1-endpoint.ts
import { wrapFetchWithPayment, createSigner, decodeXPaymentResponse } from "x402-fetch";

const privateKey = "0x..." as `0x${string}`; // Your private key
const walletAddress = "0x..."; // Your wallet address

async function main() {
  // Step 1: Check what version the endpoint uses
  const checkResponse = await fetch("https://example.com/api/data");
  if (checkResponse.status === 402) {
    const body = await checkResponse.json();
    console.log("x402 Version:", body.x402Version);
    console.log("Network:", body.accepts[0].network);
    console.log("Price:", body.accepts[0].maxAmountRequired, "atomic units");
  }

  // Step 2: Create signer with v1 network string
  const signer = await createSigner("base", privateKey); // Use network from response

  // Step 3: Wrap fetch and make paid request
  const fetchWithPayment = wrapFetchWithPayment(fetch, signer);
  const response = await fetchWithPayment("https://example.com/api/data");
  const data = await response.json();
  console.log("Response:", data);

  // Step 4: Check payment receipt
  const receipt = response.headers.get("x-payment-response");
  if (receipt) {
    console.log("Payment settled:", decodeXPaymentResponse(receipt));
  }
}

main().catch(console.error);
```

### Example 2: Calling a v2 Endpoint

```typescript
// call-v2-endpoint.ts
import { wrapFetchWithPayment, x402Client, x402HTTPClient } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const privateKey = "0x..." as `0x${string}`;

async function main() {
  // Step 1: Check what version the endpoint uses
  const checkResponse = await fetch("https://example.com/api/data");
  if (checkResponse.status === 402) {
    const hasV2Header = checkResponse.headers.get("PAYMENT-REQUIRED");
    console.log("Is v2:", !!hasV2Header);
  }

  // Step 2: Setup v2 client
  const signer = privateKeyToAccount(privateKey);
  const client = new x402Client();
  registerExactEvmScheme(client, { signer });

  // Step 3: Make paid request
  const fetchWithPayment = wrapFetchWithPayment(fetch, client);
  const response = await fetchWithPayment("https://example.com/api/data");
  const data = await response.json();
  console.log("Response:", data);

  // Step 4: Check payment receipt
  const receipt = response.headers.get("PAYMENT-RESPONSE");
  if (receipt) {
    console.log("Payment settled");
  }
}

main().catch(console.error);
```

## Service Discovery (Bazaar)

Find x402-enabled services without knowing URLs in advance.

```bash
# Quick discovery via curl
curl -s "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources?type=http&limit=50" | jq '.items[] | {url: .resource, price: .accepts[0].maxAmountRequired, version: .x402Version}'
```

### Programmatic Discovery

```typescript
import { HTTPFacilitatorClient } from "@x402/core/http";
import { withBazaar } from "@x402/extensions";

const facilitatorClient = new HTTPFacilitatorClient({
  url: "https://api.cdp.coinbase.com/platform/v2/x402"
});
const client = withBazaar(facilitatorClient);

const response = await client.extensions.discovery.listResources({ type: "http" });

// Filter by price (under $0.01 = 10000 atomic units)
const affordable = response.items.filter(item =>
  Number(item.accepts[0].maxAmountRequired) < 10000
);
```

## Payment Amounts

| Amount (atomic) | USDC Value |
|-----------------|------------|
| `1000` | $0.001 (0.1 cents) |
| `2000` | $0.002 |
| `10000` | $0.01 (1 cent) |
| `100000` | $0.10 (10 cents) |
| `1000000` | $1.00 |

## Extracting Endpoint Requirements (Method, Body, Schema)

Many x402 endpoints include detailed input/output schemas in their 402 response. This tells you:
- What HTTP method to use (GET, POST, etc.)
- What body format (JSON, form-data)
- Required and optional fields

### Step 1: Get the 402 Response

```bash
# Try GET first
curl -i "https://example.com/api/endpoint"

# If you get 405 Method Not Allowed, try POST
curl -i -X POST "https://example.com/api/endpoint" -H "Content-Type: application/json"
```

### Step 2: Decode and Inspect the Payment Header

For v2 endpoints, decode the `PAYMENT-REQUIRED` header:

```bash
# Extract and decode the header (save full header value to a file or variable)
echo "<base64-payment-required-value>" | base64 -d | jq '.'
```

### Step 3: Find the Input Schema

Look for `extensions.bazaar.schema.properties.input` in the decoded response:

```json
{
  "x402Version": 2,
  "accepts": [...],
  "extensions": {
    "bazaar": {
      "info": {
        "input": {
          "type": "http",
          "method": "POST",        // <-- HTTP method
          "bodyType": "json",      // <-- Body format
          "body": {}
        }
      },
      "schema": {
        "properties": {
          "input": {
            "properties": {
              "body": {
                "properties": {
                  "urls": { "type": "array", "items": { "type": "string" } },  // Required field
                  "text": { "type": "boolean" }  // Optional field
                },
                "required": ["urls"]  // <-- Required fields listed here
              }
            }
          }
        }
      }
    }
  }
}
```

### Step 4: Build Your Request

Based on the schema above:

```typescript
const response = await fetchWithPayment("https://example.com/api/endpoint", {
  method: "POST",  // From info.input.method
  headers: { "Content-Type": "application/json" },  // From info.input.bodyType
  body: JSON.stringify({
    urls: ["https://example.com"],  // Required field
    text: true  // Optional field
  })
});
```

### Quick Schema Extraction (One-liner)

```bash
curl -s -X POST "https://example.com/api/endpoint" -H "Content-Type: application/json" | \
  jq -r 'if .accepts then . else empty end' 2>/dev/null || \
  echo "Check PAYMENT-REQUIRED header for v2"
```

For v2 with header:
```bash
curl -si -X POST "https://example.com/api/endpoint" -H "Content-Type: application/json" | \
  grep -i "payment-required:" | cut -d' ' -f2 | base64 -d | \
  jq '{method: .extensions.bazaar.info.input.method, bodyType: .extensions.bazaar.info.input.bodyType, required: .extensions.bazaar.schema.properties.input.properties.body.required}'
```

### Common Patterns

| If you see... | Then use... |
|---------------|-------------|
| `"method": "GET"` | `fetch(url)` |
| `"method": "POST"` + `"bodyType": "json"` | `fetch(url, { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({...}) })` |
| `"method": "POST"` + `"bodyType": "form-data"` | `fetch(url, { method: "POST", body: formData })` |
| No `extensions.bazaar` | Try GET first, then POST if 405 |

## Setup Checklist

1. **Create wallet** - Run `echo "1" | npx add-wallet evm` (non-interactive)
2. **Note the address** - Check `.env` for `WALLET_ADDRESS`
3. **Fund wallet** - Send USDC on Base mainnet (or `npx add-wallet topup testnet`)
4. **Check endpoint** - `curl -i <url>` to see:
   - x402 version (v1 or v2)
   - Price (amount field)
   - Network (mainnet or testnet)
   - If 405, try `curl -i -X POST <url>`
5. **Extract schema** - Decode `PAYMENT-REQUIRED` header to find method, body format, required fields
6. **Install correct packages** - v1: `x402-fetch`, v2: `@x402/fetch @x402/evm`
7. **Use correct code pattern** - v1: `createSigner()`, v2: `registerExactEvmScheme()`
8. **Build request** - Use method/body from schema, SDK handles 402 → payment → retry

## Troubleshooting

### HTTP 405 Method Not Allowed
The endpoint requires a different HTTP method. Try POST instead of GET:
```bash
curl -i -X POST "https://example.com/api/endpoint" -H "Content-Type: application/json"
```

### "EIP-712 domain parameters required" Error
You're using v2 packages (`@x402/fetch`) on a v1 endpoint. Check the 402 response - if `x402Version: 1`, use `x402-fetch` instead.

### "No scheme registered" Error
The network in the 402 response isn't registered. For v2, make sure you called `registerExactEvmScheme(client, { signer })`.

### Payment succeeds but response is empty or error
You might be missing required body fields. Decode the `PAYMENT-REQUIRED` header and check `extensions.bazaar.schema` for required fields.

### Payment not going through
1. Check wallet has sufficient USDC balance on the correct network
2. Verify you're using the right network (mainnet vs testnet)
3. Check the `network` field in the 402 response matches your setup

## Protocol References

For detailed protocol schemas, see:
- [references/wallet-setup.md](references/wallet-setup.md)
- [references/v1-protocol.md](references/v1-protocol.md)
- [references/v2-protocol.md](references/v2-protocol.md)
