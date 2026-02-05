---
name: yellow-best-practices
description: Yellow Network and Nitrolite (ERC-7824) development best practices for building state channel applications. Use when building apps with Yellow SDK, implementing state channels, connecting to ClearNodes, managing off-chain transactions, or working with application sessions.
---

# Yellow Network & Nitrolite Best Practices

Guidelines for building high-performance decentralized applications using Yellow Network's state channel infrastructure and the Nitrolite SDK (ERC-7824).

## Quick Start

```bash
npm install @erc7824/nitrolite
```

**ClearNode WebSocket URL**: `wss://clearnet.yellow.com/ws`

## Core Concepts

### What is Yellow Network?

Yellow Network is a decentralized clearing and settlement network that connects brokers, exchanges, and applications across multiple blockchains using state channels. Key features:

- **Chain Abstraction**: Unified balance across multiple chains
- **Off-chain Processing**: Up to 100,000 transactions per second
- **Non-custodial**: User funds are governed by smart contracts
- **ERC-7824 Protocol**: Challenge-dispute mechanism for fund recovery

### Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Your App      │────▶│   ClearNode     │
│  (Nitrolite SDK)│◀────│   (Broker)      │
└─────────────────┘     └─────────────────┘
        │                       │
        └───────────┬───────────┘
                    ▼
            ┌───────────────┐
            │  Blockchain   │
            │  (Settlement) │
            └───────────────┘
```

## Rules by Category

For detailed rules, see the `rules/` directory:

- [01-connection.md](rules/01-connection.md) - ClearNode connection patterns (Critical)
- [02-authentication.md](rules/02-authentication.md) - Authentication flow (Critical)
- [03-app-sessions.md](rules/03-app-sessions.md) - Application session management (High)
- [04-state-management.md](rules/04-state-management.md) - State and balance management (High)
- [05-security.md](rules/05-security.md) - Security best practices (Critical)
- [06-error-handling.md](rules/06-error-handling.md) - Error handling patterns (Medium)

## Essential Patterns

### 1. ClearNode Connection

Always implement reconnection logic with exponential backoff:

```javascript
class ClearNodeConnection {
  constructor(url) {
    this.url = url;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 3000;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      // Proceed with authentication
    };
    this.ws.onclose = () => this.attemptReconnect();
  }

  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;
    this.reconnectAttempts++;
    const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);
    setTimeout(() => this.connect(), delay);
  }
}
```

### 2. Authentication Flow

Use EIP-712 structured data signatures:

```javascript
import {
  createAuthRequestMessage,
  createAuthVerifyMessage,
  createEIP712AuthMessageSigner,
  parseRPCResponse,
  RPCMethod,
} from '@erc7824/nitrolite';

// 1. Send auth_request
const authRequest = await createAuthRequestMessage({
  address: walletAddress,
  session_key: signerAddress,
  application: 'YourAppDomain',
  expires_at: (Math.floor(Date.now() / 1000) + 3600).toString(),
  scope: 'console',
  allowances: [],
});

// 2. Handle auth_challenge and send auth_verify
// 3. Store JWT token for reconnection
```

### 3. Message Signing

Sign plain JSON payloads (NOT EIP-191):

```javascript
const messageSigner = async (payload) => {
  const wallet = new ethers.Wallet(privateKey);
  const messageBytes = ethers.utils.arrayify(
    ethers.utils.id(JSON.stringify(payload))
  );
  const flatSignature = await wallet._signingKey().signDigest(messageBytes);
  return ethers.utils.joinSignature(flatSignature);
};
```

### 4. Application Sessions

```javascript
import { createAppSessionMessage } from '@erc7824/nitrolite';

const appDefinition = {
  protocol: 'nitroliterpc',
  participants: [participantA, participantB],
  weights: [100, 0],
  quorum: 100,
  challenge: 0,
  nonce: Date.now(),
};

const allocations = [
  { participant: participantA, asset: 'usdc', amount: '1000000' },
  { participant: participantB, asset: 'usdc', amount: '0' },
];

const message = await createAppSessionMessage(signer, [{
  definition: appDefinition,
  allocations,
}]);
```

## Critical Rules

### DO

1. **Always use `wss://`** - Never use unencrypted WebSocket connections
2. **Implement timeouts** - Add timeouts to all async operations (10-30 seconds)
3. **Store JWT tokens** - Reuse tokens for reconnection instead of re-authenticating
4. **Clean up listeners** - Remove message event listeners to prevent memory leaks
5. **Verify signatures** - Always verify received message signatures
6. **Use session keys** - Generate temporary keys for signing, not main wallet keys

### DON'T

1. **Don't expose private keys** - Never hardcode or log private keys
2. **Don't skip error handling** - Always handle WebSocket errors and auth failures
3. **Don't ignore timeouts** - Implement proper timeout handling for all operations
4. **Don't use EIP-191 prefix** - Sign plain JSON, not prefixed messages
5. **Don't forget to close sessions** - Always properly close app sessions when done

## SDK Components

| Component | Purpose |
|-----------|---------|
| `NitroliteRPC` | Message construction and signing |
| `NitroliteClient` | High-level channel management |
| `createAuthRequestMessage` | Auth request creation |
| `createAuthVerifyMessage` | Challenge response |
| `createAppSessionMessage` | App session creation |
| `createCloseAppSessionMessage` | Session closure |
| `createGetLedgerBalancesMessage` | Balance queries |
| `parseRPCResponse` | Response parsing |

## Additional Resources

- [Full LLM Documentation](https://erc7824.org/llms-full.txt)
- [Yellow Network Docs](https://docs.yellow.org/)
- [ERC-7824 Quick Start](https://erc7824.org/quick_start)
- [Nitrolite GitHub](https://github.com/erc7824/nitrolite)
