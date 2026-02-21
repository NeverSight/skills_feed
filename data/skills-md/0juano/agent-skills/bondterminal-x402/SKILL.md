---
name: bondterminal-x402
description: >
  Query BondTerminal API using x402 keyless payments. No API key needed —
  pay $0.01 USDC per request on Base mainnet. Use when users ask for Argentine
  bond data, analytics, cashflows, history, riesgo país, or ISIN/ticker lookups
  (e.g. AL30, GD30, US040114HS26). Supports automatic 402 → payment → retry.
metadata:
  author: 0juano
  version: "2.1.0"
---

# BondTerminal x402

Query the BondTerminal API with x402 pay-per-call auth. No API key, no subscription — just sign and pay per request.

**Cost:** $0.01 USDC per request on Base mainnet.

## API Endpoints

Base URL: `https://bondterminal.com/api/v1`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/treasury-curve` | US Treasury yield curve | Free |
| GET | `/bonds` | List all bonds (60+) | x402 |
| GET | `/bonds/:id` | Bond details by ISIN or local ticker | x402 |
| GET | `/bonds/:id/analytics` | Price, YTM, duration, spreads | x402 |
| GET | `/bonds/:id/cashflows` | Cashflow schedule | x402 |
| GET | `/bonds/:id/history` | Historical price/yield/spread | x402 |
| POST | `/calculate` | Bond analytics from custom price | x402 |
| GET | `/riesgo-pais` | Current Argentina country risk | x402 |
| GET | `/riesgo-pais/history` | Historical riesgo país series | x402 |
| POST | `/calculate/batch` | Batch calculations | Bearer only |

**Identifier formats:** ISIN (`US040114HS26`), local ticker with D/C suffix (`AL30D`, `GD30D`).

Full docs: https://bondterminal.com/developers
Endpoint reference in this skill: `references/endpoints.md`

## How x402 Works

1. Call any x402 endpoint without auth → server returns `402` with `PAYMENT-REQUIRED` header
2. Decode the header (base64 JSON) to get payment requirements (amount, asset, network, payTo)
3. Sign an EIP-3009 `transferWithAuthorization` via the x402 client library
4. Retry the request with the signed payment in the `PAYMENT-SIGNATURE` header (v2), with `X-PAYMENT` as legacy fallback
5. Server verifies payment via Coinbase facilitator, returns data + `PAYMENT-RESPONSE` header

## Setup

### 1. Install dependencies

```bash
npm install @x402/core @x402/evm viem
```

> **Note:** The code examples use ES modules. Use `.mjs` file extension or add `"type": "module"` to your `package.json`.

### 2. Configure a signer

The x402 payment flow requires an EVM signer on Base mainnet with USDC balance. Configure your signer following the [x402 EVM documentation](https://github.com/coinbase/x402/tree/main/packages/evm).

The signer must implement `{ address, signTypedData }` — any viem-compatible wallet client works (hardware wallet, KMS, injected provider, etc).

See `references/signer-setup.md` for a complete signer configuration example.

### 3. Register the x402 client

```javascript
import { x402Client } from '@x402/core/client';
import { x402HTTPClient } from '@x402/core/http';
import { ExactEvmScheme } from '@x402/evm'; // exact export name

// signer = { address, signTypedData } — see references/signer-setup.md
const scheme = new ExactEvmScheme(signer);
const client = new x402Client();
client.register('eip155:8453', scheme); // Base mainnet
const httpClient = new x402HTTPClient(client);
```

## Fetching Bond Data

```javascript
async function fetchBT(path) {
  const url = `https://bondterminal.com/api/v1${path}`;
  let res = await fetch(url);

  if (res.status === 402) {
    const paymentRequired = httpClient.getPaymentRequiredResponse(
      (name) => res.headers.get(name),
      await res.json()
    );
    const payload = await httpClient.createPaymentPayload(paymentRequired);

    // Preferred v2 header
    res = await fetch(url, {
      headers: httpClient.encodePaymentSignatureHeader(payload),
    });

    // Legacy fallback for servers still expecting X-PAYMENT
    if (res.status === 402) {
      const encoded = Buffer.from(JSON.stringify(payload)).toString('base64');
      res = await fetch(url, { headers: { 'X-PAYMENT': encoded } });
    }
  }

  if (!res.ok) {
    throw new Error(`BondTerminal request failed (${res.status})`);
  }

  return res.json();
}

// Examples
const bonds = await fetchBT('/bonds');
const analytics = await fetchBT('/bonds/AL30D/analytics');
const riesgo = await fetchBT('/riesgo-pais');
```

## Quick Test

Validate both free and paid flows:

```javascript
await fetchBT('/treasury-curve'); // free route (no payment)
await fetchBT('/riesgo-pais');    // paid route (triggers x402 flow)
```

## Wallet Requirements

The signing wallet needs:
- **USDC on Base** — for the $0.01 payment per request

No ETH for gas is required — x402 uses EIP-3009 (off-chain signature), not on-chain transactions.

## Notes

- `POST /calculate/batch` requires a Bearer API key subscription — not available via x402
- Local tickers require D/C suffix: `AL30D` (USD), `AL30C` (ARS) — not `AL30`
- Settlement is on-chain: each paid call produces a verifiable transaction hash
- The `PAYMENT-RESPONSE` header contains settlement metadata (payer, tx hash, network)
