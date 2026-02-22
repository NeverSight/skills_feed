---
name: x402-stacks
description: Use when implementing HTTP 402 payment-required endpoints on Stacks blockchain, setting up micropayment clients with STX or sBTC tokens, handling x402 protocol wallet setup, building browser/frontend dApps with @stacks/connect wallet signing, or integrating x402 payments in React apps
---

# x402-stacks SDK

## Overview

x402-stacks enables **automatic HTTP-level payments** for APIs using STX or sBTC tokens on Stacks blockchain. Two client paths: **server/CLI** (axios interceptor with private key) and **frontend/browser** (wallet extension signing via `@stacks/connect`). Server protects endpoints with Express middleware.

**Core principle:** HTTP 402 Payment Required becomes a working protocol.

## Installation

```bash
# Server/CLI
npm i x402-stacks

# Frontend (Browser) — additional deps
npm i x402-stacks @stacks/connect @stacks/transactions axios
```

## Wallet Setup

**Choose your path based on environment:**

- **Server/CLI** → Option 1 or 2 (private key in env)
- **Frontend (Browser)** → Option 3 (wallet extension, no private keys)

### Option 1: Load Existing Wallet (Server/CLI)
**When:** You have a private key already

```typescript
import { privateKeyToAccount } from 'x402-stacks';

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY!,
  'testnet'  // or 'mainnet'
);
```

### Option 2: Generate New Wallet (Server/CLI)
**When:** You don't have a wallet yet

```typescript
import { generateKeypair, privateKeyToAccount } from 'x402-stacks';

// Generate once, save the private key
const keypair = generateKeypair('testnet');
console.log('Save this:', keypair.privateKey);
console.log('Fund at:', `https://explorer.stacks.co/sandbox/faucet?chain=testnet`);

// Use it
const account = privateKeyToAccount(keypair.privateKey, 'testnet');
```

**Important:** After generating, save private key to `.env` file and fund via faucet before making payments.

### Option 3: Connect Browser Wallet (Frontend)
**When:** Building a browser dApp — keys never leave the wallet extension

```typescript
// Always dynamic import (SSR/bundler safe)
const { connect, disconnect, isConnected } = await import('@stacks/connect');

// Connect wallet (opens popup)
await connect();

// Check connection
if (isConnected()) {
  // Read stored wallet data
  const walletData = getLocalStorage();
  // walletData contains addresses, public keys, etc.
}

// Disconnect
await disconnect();
```

**Never store or request private keys in the browser.** The wallet extension manages signing.

## Quick Start: Server/CLI Client (Pays Automatically)

```typescript
import axios from 'axios';
import { wrapAxiosWithPayment, privateKeyToAccount } from 'x402-stacks';

const account = privateKeyToAccount(process.env.PRIVATE_KEY!, 'testnet');

const api = wrapAxiosWithPayment(
  axios.create({ baseURL: 'http://localhost:3000', timeout: 60000 }),
  account
);

// Payment happens automatically on 402 response
const response = await api.get('/api/premium-data');
```

## Quick Start: Frontend Client (Browser)

Three steps: parse the 402, sign via wallet, retry with payment header.

### Step 1: Parse 402 Response

```typescript
import type { AxiosError } from 'axios';
import { X402_HEADERS, type PaymentRequiredV2 } from 'x402-stacks';

function decodePaymentRequired(header: string): PaymentRequiredV2 | null {
  try {
    return JSON.parse(atob(header));    // btoa/atob — browser-safe, no Buffer
  } catch {
    return null;
  }
}

function parse402Response(error: AxiosError): PaymentRequiredV2 {
  // Try header first (base64 encoded)
  const headerValue = error.response?.headers?.[X402_HEADERS.PAYMENT_REQUIRED];
  const fromHeader = decodePaymentRequired(headerValue);
  if (fromHeader && fromHeader.accepts?.length > 0) return fromHeader;

  // Fall back to response body
  const data = error.response?.data as Record<string, unknown> | undefined;
  if (data && Array.isArray(data.accepts) && data.accepts.length > 0) {
    return data as unknown as PaymentRequiredV2;
  }

  throw new Error('No valid payment requirements in 402 response');
}
```

### Step 2: Sign Payment via Wallet (No Broadcast)

```typescript
import type {
  PaymentRequiredV2, PaymentRequirementsV2, PaymentPayloadV2,
} from 'x402-stacks';

async function signX402Payment(
  paymentRequired: PaymentRequiredV2,
  accepted: PaymentRequirementsV2,
  network: 'mainnet' | 'testnet',
): Promise<string> {
  const { request } = await import('@stacks/connect');
  const { makeUnsignedSTXTokenTransfer } = await import('@stacks/transactions');

  // 1. Get public key from wallet
  const addrResponse = await request('stx_getAddresses') as {
    addresses?: Array<{ symbol?: string; publicKey?: string }>;
  };
  const stxEntry = addrResponse.addresses?.find((a) => a.symbol === 'STX');
  if (!stxEntry?.publicKey) throw new Error('Could not get public key from wallet');

  // 2. Build unsigned transaction
  const unsignedTx = await makeUnsignedSTXTokenTransfer({
    publicKey: stxEntry.publicKey,
    recipient: accepted.payTo,
    amount: BigInt(accepted.amount),
    network,
  });
  const txHex = unsignedTx.serialize();

  // 3. Sign WITHOUT broadcasting — facilitator will broadcast
  const signResult = await request('stx_signTransaction', {
    transaction: txHex,
    broadcast: false,
  }) as { transaction: string };
  if (!signResult.transaction) throw new Error('No signed transaction from wallet');

  // 4. Build payload and base64 encode (browser-safe)
  const payload: PaymentPayloadV2 = {
    x402Version: 2,
    resource: paymentRequired.resource,
    accepted,
    payload: { transaction: signResult.transaction },
  };
  return btoa(JSON.stringify(payload));
}
```

### Step 3: Two-Request Flow

```typescript
import axios from 'axios';
import { X402_HEADERS } from 'x402-stacks';

async function fetchWithPayment(url: string, network: 'mainnet' | 'testnet') {
  try {
    return await axios.get(url);
  } catch (error) {
    if (!axios.isAxiosError(error) || error.response?.status !== 402) throw error;

    const paymentRequired = parse402Response(error);
    const accepted = paymentRequired.accepts[0];  // first accepted scheme

    const paymentHeader = await signX402Payment(paymentRequired, accepted, network);

    return axios.get(url, {
      headers: { [X402_HEADERS.PAYMENT_SIGNATURE]: paymentHeader },
      timeout: 60000,
    });
  }
}
```

## React Integration

For React apps, wrap the frontend primitives above in a Context + typed request helper. Four files to create:

| File | Purpose | Reusable? |
|------|---------|-----------|
| `StacksWalletContext.tsx` | Wallet state, connect/disconnect | Copy as-is |
| `x402.ts` | `parse402Response` + `signX402Payment` | Copy as-is (code in Steps 1-2 above) |
| `x402Request.ts` | Generic typed two-step request | Swap URL/body for your API |
| `WalletButton.tsx` | Connect/disconnect UI | Adapt styling to your app |

### Wallet Context (`StacksWalletContext.tsx`)

```tsx
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

export type Network = 'mainnet' | 'testnet';

interface StacksWalletContextType {
  isLoading: boolean;
  isWalletConnected: boolean;
  network: Network;
  stxAddress: string | undefined;
  connectWallet: () => Promise<void>;
  disconnectWallet: () => Promise<void>;
}

const StacksWalletContext = createContext<StacksWalletContextType | undefined>(undefined);

function extractStxAddress(data: unknown): string | undefined {
  if (!data || typeof data !== 'object') return undefined;
  const obj = data as Record<string, unknown>;
  const addresses = obj.addresses;
  if (!addresses || typeof addresses !== 'object') return undefined;
  const stx = (addresses as Record<string, unknown>).stx;
  if (!Array.isArray(stx) || stx.length === 0) return undefined;
  return stx[0]?.address as string | undefined;
}

export function StacksWalletProvider({ children }: { children: React.ReactNode }) {
  const [walletData, setWalletData] = useState<unknown>(undefined);
  const [isLoading, setIsLoading] = useState(true);
  const [network] = useState<Network>('mainnet');

  useEffect(() => {
    const check = async () => {
      try {
        const { isConnected, getLocalStorage } = await import('@stacks/connect');
        if (isConnected()) setWalletData(getLocalStorage());
      } catch { /* wallet not installed */ }
      finally { setIsLoading(false); }
    };
    check();
  }, []);

  const connectWallet = useCallback(async () => {
    const { connect, getLocalStorage } = await import('@stacks/connect');
    await connect();
    setWalletData(getLocalStorage());
  }, []);

  const disconnectWallet = useCallback(async () => {
    const { disconnect } = await import('@stacks/connect');
    disconnect();
    setWalletData(undefined);
  }, []);

  return (
    <StacksWalletContext.Provider value={{
      isLoading, isWalletConnected: !!walletData, network,
      stxAddress: extractStxAddress(walletData), connectWallet, disconnectWallet,
    }}>
      {children}
    </StacksWalletContext.Provider>
  );
}

export function useStacksWallet() {
  const ctx = useContext(StacksWalletContext);
  if (!ctx) throw new Error('useStacksWallet must be used within StacksWalletProvider');
  return ctx;
}
```

### Generic x402 Request (`x402Request.ts`)

Typed wrapper over the two-step pattern. Uses `parse402Response` and `signX402Payment` from `x402.ts` (Steps 1-2 above).

```tsx
import axios, { AxiosError } from 'axios';
import { parse402Response, signX402Payment, X402_HEADERS } from './x402';
import type { Network } from './StacksWalletContext';

export async function x402Request<T>(
  method: 'get' | 'post',
  url: string,
  body: unknown,
  network: Network,
): Promise<T> {
  let encodedPayload: string;

  try {
    const { data } = await axios({ method, url, data: body });
    return data as T;  // didn't 402 — return directly
  } catch (err) {
    if (err instanceof AxiosError && err.response?.status === 402) {
      const paymentReq = parse402Response(err);
      const accepted = paymentReq.accepts[0];
      if (!accepted) throw new Error('No accepted payment methods');
      encodedPayload = await signX402Payment(paymentReq, accepted, network);
    } else {
      throw err;
    }
  }

  // Retry with payment proof
  const { data } = await axios({
    method, url, data: body,
    headers: { [X402_HEADERS.PAYMENT_SIGNATURE]: encodedPayload },
  });
  return data as T;
}
```

**Usage with any endpoint:**

```tsx
const job = await x402Request('post', '/api/v1/exports', { id: '123' }, 'mainnet');
const article = await x402Request('get', '/api/v1/premium/456', null, 'mainnet');
```

### Provider Setup

```tsx
import { StacksWalletProvider } from './StacksWalletContext';

function App() {
  return (
    <StacksWalletProvider>
      {/* routes, components, etc. */}
    </StacksWalletProvider>
  );
}
```

### Component Usage

```tsx
import { useStacksWallet } from './StacksWalletContext';
import { x402Request } from './x402Request';

function BuyButton({ resourceId }: { resourceId: string }) {
  const { isWalletConnected, connectWallet, network } = useStacksWallet();
  const [loading, setLoading] = useState(false);

  const handlePurchase = async () => {
    if (!isWalletConnected) await connectWallet();
    setLoading(true);
    try {
      const result = await x402Request('post', '/api/v1/buy', { id: resourceId }, network);
      console.log('Paid!', result);
    } catch (err) {
      console.error('Payment failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return <button onClick={handlePurchase} disabled={loading}>
    {loading ? 'Processing...' : 'Buy'}
  </button>;
}
```

## Quick Start: Server (Requires Payment)

```typescript
import express from 'express';
import { paymentMiddleware, STXtoMicroSTX, STACKS_NETWORKS } from 'x402-stacks';

const app = express();

app.get('/api/premium-data',
  paymentMiddleware({
    amount: STXtoMicroSTX(0.00001),
    payTo: process.env.SERVER_ADDRESS!,
    network: STACKS_NETWORKS.TESTNET,  // or STACKS_NETWORKS.MAINNET
    asset: 'STX',
    facilitatorUrl: 'https://facilitator.stacksx402.com',  // Free facilitator
  }),
  (req, res) => {
    res.json({ data: 'Premium content' });
  }
);
```

## Registering on x402scan

**Make your service discoverable** by registering it on x402scan.

### Registration Endpoint

```bash
POST https://scan.stacksx402.com/api/v1/resources
Content-Type: application/json

{
  "url": "https://your-service.com/api/your-endpoint"
}
```

### Your Endpoint Must Return

When x402scan validates your URL, it expects HTTP 402 (or 200) with:

```json
{
  "x402Version": 1,
  "name": "My AI Service",
  "image": "https://your-service.com/logo.png",
  "accepts": [{
    "scheme": "exact",
    "network": "stacks",
    "asset": "STX",
    "maxAmountRequired": "1000000",
    "resource": "https://your-service.com/api/your-endpoint",
    "description": "What this service does",
    "mimeType": "application/json",
    "payTo": "SP2...YOUR_ADDRESS",
    "maxTimeoutSeconds": 60,
    "outputSchema": {
      "input": {
        "type": "https",
        "method": "GET",
        "queryParams": {
          "q": { "type": "string", "required": true, "description": "Query param" }
        }
      },
      "output": {
        "type": "object",
        "properties": { "result": { "type": "string" } }
      }
    }
  }]
}
```

### Validation Requirements

| Must Have | Error if Missing |
|-----------|------------------|
| HTTPS URL | `invalid_url` |
| Non-empty `name` | `invalid_name` |
| At least 1 `accepts` entry | `empty_accepts` |
| `network: "stacks"` in all accepts | `invalid_network` |
| `outputSchema` in all accepts | `missing_output_schema` |

### Why outputSchema Matters

The `outputSchema` tells agents HOW to call your service:
- `input.method` - HTTP method (GET/POST)
- `input.queryParams` - Query parameters (for GET)
- `input.bodyFields` - Body structure (for POST)
- `output` - Response format

This is the contract agents use to call your service programmatically.

### Quick Registration Example

```bash
curl -X POST https://scan.stacksx402.com/api/v1/resources \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-service.com/api/endpoint"}'
```

**After registration:** Your service appears in the x402scan directory and gets re-validated every 24h.

## Quick Reference

| Function | Path | Purpose | Returns |
|----------|------|---------|---------|
| `privateKeyToAccount(key, network)` | Server | Load wallet from key | `{ address, privateKey, network }` |
| `generateKeypair(network)` | Server | Create new wallet | `{ privateKey, publicKey, address }` |
| `wrapAxiosWithPayment(axios, account)` | Server | Auto-pay on 402 | axios instance |
| `paymentMiddleware(config)` | Server | Protect endpoint | Express middleware |
| `STXtoMicroSTX(amount)` | Both | Convert STX to microSTX | bigint |
| `decodePaymentResponse(header)` | Both | Get payment details | `{ transaction, payer, network }` |
| `X402_HEADERS` | Both | Header name constants | `{ PAYMENT_REQUIRED, PAYMENT_SIGNATURE, ... }` |
| `connect()` | Frontend | Open wallet popup | void |
| `request('stx_getAddresses')` | Frontend | Get wallet public key | `{ addresses }` |
| `request('stx_signTransaction', opts)` | Frontend | Sign tx (no broadcast) | `{ transaction }` |
| `makeUnsignedSTXTokenTransfer(opts)` | Frontend | Build unsigned STX tx | Transaction object |
| `useStacksWallet()` | React | Wallet state hook | `{ isWalletConnected, stxAddress, connectWallet, ... }` |
| `x402Request<T>(method, url, body, network)` | React | Typed two-step payment request | `Promise<T>` |

## Payment Flow

### Server/CLI (automatic)

```
1. Client → GET /api/data → Server
2. Server → 402 + payment-required header → Client
3. Client signs tx (not broadcast)
4. Client → GET + payment-signature → Server
5. Server → Facilitator settles tx → Blockchain
6. Server → 200 + data + payment-response → Client
```

### Frontend (Browser)

```
1. Browser → GET /api/data → Server
2. Server → 402 + payment-required header → Browser
3. Browser parses 402, opens wallet popup
4. User approves → wallet signs tx (no broadcast)
5. Browser → GET + payment-signature header → Server
6. Server → Facilitator settles tx → Blockchain
7. Server → 200 + data → Browser
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generating wallet every run | Save private key to `.env` and load it |
| Using plain "mainnet" instead of CAIP-2 | Use `STACKS_NETWORKS.MAINNET` or `"stacks:1"` |
| Not funding testnet wallet | Get tokens from faucet first |
| Forgetting timeout for settlement | Set `timeout: 60000` (60 seconds minimum) |
| Mixing STX and microSTX amounts | Use `STXtoMicroSTX()` converter |
| Hardcoding private keys | Always use environment variables |
| Using `Buffer` for base64 in browser | Use `btoa()` / `atob()` — Buffer is Node-only |
| Broadcasting tx from client | Set `broadcast: false` — facilitator broadcasts |
| Static imports of `@stacks/connect` | Always use dynamic `await import(...)` (SSR/bundler safe) |
| Not validating `accepts` array | Check `accepts?.length > 0` before accessing `[0]` |
| Storing private keys in browser | Use wallet extension — keys never leave it |
| Using `useStacksWallet` outside provider | Wrap app root with `<StacksWalletProvider>` |
| Not checking `isWalletConnected` before payment | Call `connectWallet()` first if not connected |

## Token Support

- **STX** (default): Native Stacks token
- **sBTC**: Bitcoin on Stacks (add `tokenType: 'sBTC'` and `tokenContract`)

## Environment Variables

```bash
# Server/CLI Client
PRIVATE_KEY=your-private-key-hex
NETWORK=testnet

# Server
SERVER_ADDRESS=ST1...
FACILITATOR_URL=https://facilitator.stacksx402.com
```

**Frontend:** No env vars needed. Network is set in code; wallet extension manages keys.

## When NOT to Use

- Traditional payment flows (use Stripe/PayPal)
- Subscription models (x402 is for pay-per-use)
- High-frequency micro-transactions (<$0.001 - fees make it impractical)
- When users don't have crypto wallets

## Resources

- Testnet Faucet: https://explorer.stacks.co/sandbox/faucet?chain=testnet
- Stacks Explorer: https://explorer.stacks.co/
- Free Facilitator: https://facilitator.stacksx402.com
- x402scan Registry: https://scan.stacksx402.com
- @stacks/connect Docs: https://docs.stacks.co/stacks/connect
