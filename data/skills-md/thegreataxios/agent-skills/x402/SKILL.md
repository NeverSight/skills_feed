---
name: x402
description: "x402 protocol v2 for internet-native payments. Use when building x402 servers, clients, facilitators, or integrating x402 payment flows. Triggers: x402, payment required, 402, paywall, micropayment, EIP-3009, payment protocol, facilitator, PaymentPayload, PaymentRequirements."
license: MIT
metadata:
  author: thegreataxios
  version: "1.0.0"
  x402_version: "2"
---

# x402 Protocol v2

Open payment standard enabling clients to pay for external resources over any transport layer (HTTP, MCP, A2A). Protocol version: **2**.

## Core Concepts

x402 has three architectural layers:

1. **Types** — `PaymentRequirements`, `PaymentPayload`, `SettlementResponse`, `VerifyResponse` (transport/scheme-agnostic)
2. **Logic** — Payment formation, verification, settlement (scheme+network specific, e.g. exact/EVM)
3. **Representation** — How payment data is transmitted (transport-specific: HTTP headers, JSON-RPC, etc.)

## Payment Flow

1. Client requests a protected resource
2. Server responds with **Payment Required** + `PaymentRequired` JSON (contains `accepts` array)
3. Client picks a payment method, signs authorization, sends `PaymentPayload`
4. Server forwards to facilitator → **verify** → **settle** → returns resource + `SettlementResponse`

## Three Actors

- **Resource Server** — Requires payment, delegates verification/settlement to facilitator
- **Client** — Signs payment authorizations (wallet-based)
- **Facilitator** — Verifies signatures, checks balances, broadcasts settlement transactions

## PaymentRequired (Server → Client)

```json
{
  "x402Version": 2,
  "error": "Payment required",
  "resource": {
    "url": "https://api.example.com/data",
    "description": "Premium data",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "amount": "10000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0x...",
      "maxTimeoutSeconds": 60,
      "extra": { "name": "USDC", "version": "2" }
    }
  ],
  "extensions": {}
}
```

### Field Reference

| Field | Type | Req | Description |
|-------|------|-----|-------------|
| `x402Version` | number | ✓ | Must be `2` |
| `error` | string | | Human-readable error |
| `resource` | ResourceInfo | ✓ | URL, description, mimeType |
| `accepts` | PaymentRequirements[] | ✓ | Acceptable payment methods |
| `extensions` | object | | Extension data (key → `{info, schema}`) |

### PaymentRequirements Fields

| Field | Type | Req | Description |
|-------|------|-----|-------------|
| `scheme` | string | ✓ | e.g. `"exact"` |
| `network` | string | ✓ | CAIP-2 format, e.g. `"eip155:8453"` |
| `amount` | string | ✓ | Atomic token units |
| `asset` | string | ✓ | Token contract address or ISO 4217 code |
| `payTo` | string | ✓ | Recipient wallet address |
| `maxTimeoutSeconds` | number | ✓ | Max time for payment completion |
| `extra` | object | | Scheme-specific info |

## PaymentPayload (Client → Server)

```json
{
  "x402Version": 2,
  "resource": { "url": "...", "description": "...", "mimeType": "..." },
  "accepted": { /* chosen PaymentRequirements */ },
  "payload": {
    "signature": "0x...",
    "authorization": {
      "from": "0x...", "to": "0x...", "value": "10000",
      "validAfter": "1740672089", "validBefore": "1740672154",
      "nonce": "0x..."
    }
  },
  "extensions": {}
}
```

| Field | Type | Req | Description |
|-------|------|-----|-------------|
| `x402Version` | number | ✓ | Protocol version |
| `resource` | ResourceInfo | | Resource being accessed |
| `accepted` | PaymentRequirements | ✓ | Chosen payment method |
| `payload` | object | ✓ | Scheme-specific payment data |
| `extensions` | object | | Must include at least server-provided extension info; may append but not delete/overwrite |

### EVM Exact Payload

| Field | Type | Req | Description |
|-------|------|-----|-------------|
| `signature` | string | ✓ | EIP-712 signature |
| `authorization.from` | string | ✓ | Payer address |
| `authorization.to` | string | ✓ | Recipient address |
| `authorization.value` | string | ✓ | Amount in atomic units |
| `authorization.validAfter` | string | ✓ | Unix timestamp |
| `authorization.validBefore` | string | ✓ | Unix timestamp |
| `authorization.nonce` | string | ✓ | 32-byte random nonce |

## SettlementResponse

```json
{
  "success": true,
  "transaction": "0x...",
  "network": "eip155:8453",
  "payer": "0x..."
}
```

| Field | Type | Req | Description |
|-------|------|-----|-------------|
| `success` | boolean | ✓ | Settlement succeeded |
| `errorReason` | string | | Error if failed |
| `payer` | string | | Payer wallet address |
| `transaction` | string | ✓ | Tx hash (empty string if failed) |
| `network` | string | ✓ | CAIP-2 network |
| `extensions` | object | | Extension data |

## VerifyResponse

| Field | Type | Req | Description |
|-------|------|-----|-------------|
| `isValid` | boolean | ✓ | Authorization is valid |
| `invalidReason` | string | | Reason if invalid |
| `payer` | string | | Payer wallet address |

## Facilitator API

Three HTTP REST endpoints:

### POST /verify
Verifies payment authorization without settling. Request body: `{ paymentPayload, paymentRequirements }`. Returns `VerifyResponse`.

### POST /settle
Settles payment on-chain. Same request body as `/verify`. Returns `SettlementResponse`.

### GET /supported
Returns supported schemes, networks, extensions, and signer addresses.

```json
{
  "kinds": [
    { "x402Version": 2, "scheme": "exact", "network": "eip155:8453" }
  ],
  "extensions": [],
  "signers": {
    "eip155:*": ["0x..."],
    "solana:*": ["CKP..."]
  }
}
```

## Exact Scheme — EVM

Uses **EIP-3009** `transferWithAuthorization` for gasless ERC-20 transfers (e.g. USDC).

**Verification steps:**
1. Validate EIP-712 signature
2. Check payer token balance
3. Validate amount ≥ required
4. Check time window (validAfter/validBefore)
5. Match parameters to payment requirements
6. Simulate `transferWithAuthorization` tx

**Settlement:** Call `transferWithAuthorization` on the ERC-20 contract.

**EIP-3009 type structure:**
```javascript
const authorizationTypes = {
  TransferWithAuthorization: [
    { name: "from", type: "address" },
    { name: "to", type: "address" },
    { name: "value", type: "uint256" },
    { name: "validAfter", type: "uint256" },
    { name: "validBefore", type: "uint256" },
    { name: "nonce", type: "bytes32" },
  ],
};
```

## Exact Scheme — SVM (Solana)

Uses `TransferChecked` for SPL tokens. Key verification:
- Strict instruction layout: Compute Unit Limit → Compute Unit Price → TransferChecked
- Facilitator fee payer must NOT appear in instruction accounts or as transfer authority/source
- Compute unit price bounded to prevent gas abuse
- Destination ATA must match `payTo`/`asset` PDA
- Transfer amount must exactly equal `PaymentRequirements.amount`

## Networks (CAIP-2 Format)

| Network | CAIP-2 ID |
|---------|-----------|
| Base mainnet | `eip155:8453` |
| Base Sepolia | `eip155:84532` |
| Avalanche mainnet | `eip155:43114` |
| Avalanche Fuji | `eip155:43113` |
| Solana mainnet | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` |
| Solana devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` |

## Extensions

Extensions are key-value maps in `PaymentRequired` and `PaymentPayload`:
- Each key = extension identifier
- Each value = `{ info: object, schema: object }` where `schema` is JSON Schema for `info`
- Client must include at least the server-provided `info`; may append but cannot delete/overwrite

## Discovery API (Bazaar)

### GET /discovery/resources
Params: `type` (e.g. "http"), `limit` (1-100, default 20), `offset` (default 0).

Returns paginated list of x402-enabled resources with `accepts` arrays, `lastUpdated` timestamps, and optional `metadata`.

## Error Codes

| Code | Meaning |
|------|---------|
| `insufficient_funds` | Payer lacks tokens |
| `invalid_exact_evm_payload_authorization_valid_after` | Auth not yet valid |
| `invalid_exact_evm_payload_authorization_valid_before` | Auth expired |
| `invalid_exact_evm_payload_authorization_value` | Amount insufficient |
| `invalid_exact_evm_payload_signature` | Bad signature |
| `invalid_exact_evm_payload_recipient_mismatch` | Wrong recipient |
| `invalid_network` | Unsupported network |
| `invalid_payload` | Malformed payload |
| `invalid_payment_requirements` | Bad requirements |
| `invalid_scheme` / `unsupported_scheme` | Scheme not supported |
| `invalid_x402_version` | Wrong protocol version |
| `invalid_transaction_state` | Tx failed on-chain |
| `unexpected_verify_error` / `unexpected_settle_error` | Internal errors |

## Security

- **Replay prevention:** 32-byte EIP-3009 nonce + smart contract nonce reuse protection + time windows
- **Auth integration:** Supports SIWE for authenticated/discounted pricing

## Reference Implementation

See https://github.com/coinbase/x402 for the canonical implementation.

For detailed scheme-specific implementation, see the reference files:
- `reference/exact-core.md` — Core exact scheme specification
- `reference/exact-evm.md` — EVM implementation (EIP-3009)
- `reference/exact-svm.md` — Solana implementation
- `reference/exact-sui.md` — Sui implementation

For facilitator API examples and discovery API schemas, see `reference/facilitator-api.md`.

For x402 extension specifications, see the extension reference files:
- `reference/extension-bazaar.md` — Resource discovery and cataloging
- `reference/extension-payment-identifier.md` — Idempotency keys for deduplication
- `reference/extension-sign-in-with-x.md` — Wallet-based authentication (CAIP-122/SIWE)
- `reference/extension-eip2612-gas-sponsoring.md` — Gasless EIP-2612 permit flow
- `reference/extension-erc20-gas-sponsoring.md` — Gasless ERC-20 approval flow

## Transport Support

x402 is transport-agnostic. Current transports:
- **HTTP** — `402 Payment Required` status, base64-encoded headers (`PAYMENT-REQUIRED`, `PAYMENT-SIGNATURE`, `PAYMENT-RESPONSE`). See `reference/transport-http.md`.
- **MCP** — Payment via `_meta["x402/payment"]` and `_meta["x402/payment-response"]`, signaling via `isError: true` + `structuredContent`. See `reference/transport-mcp.md`.
- **A2A** — Task-based lifecycle with `x402.payment.*` metadata keys, AgentCard extension declaration, `X-A2A-Extensions` header activation. See `reference/transport-a2a.md`.

## Framework Integration

Server-side: Express.js middleware (`require_payment()`), FastAPI, Hono, Next.js, ai/agents.
Client-side: axios/fetch, httpx/requests, MCP clients, A2A clients.
