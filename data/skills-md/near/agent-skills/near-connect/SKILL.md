---
name: near-connect
description: Zero-dependency, lightweight wallet connector for NEAR blockchain using secure sandbox isolation. Use when working with NEAR wallet integration, supporting multiple wallets (HOT, Meteor, Intear, MyNearWallet, Nightly, NEAR Mobile, Unity, OKX, WalletConnect), transaction signing, message signing, or implementing wallet connection features in NEAR dApps. Also use when creating custom wallet integrations or debugging wallet executor scripts.
---

# Near-Connect

Zero-dependency, secure, and lightweight wallet connector for the NEAR blockchain with easily updatable wallet code through sandboxed execution.

## Overview

Near-Connect provides a **secure sandbox execution environment** for wallet integrations, eliminating the need for a monolithic registry of wallet code. Unlike near-wallet-selector, wallets host their own executor scripts which run in isolated sandboxed iframes, enabling independent updates without dApp code changes.

### Key Features

- **Zero Dependencies**: Lightweight library with no external dependencies
- **Sandbox Security**: Wallets execute in isolated iframes with granular permissions
- **Auto-Updates**: Wallets update independently via manifest without dApp changes
- **Multi-Wallet Support**: 8+ wallets including custom WalletConnect support
- **Dual Action Format**: Supports both near-wallet-selector and near-api-js action formats
- **Feature Filtering**: Filter wallets by capabilities (signMessage, testnet support, etc.)
- **Injected Wallets**: Support for browser extension wallets via EIP-6963-like standard

## Installation

```bash
yarn add @hot-labs/near-connect
```

**CDN Usage** (zero build step):

```html
<script type="importmap">
  { "imports": { "@hot-labs/near-connect": "https://esm.sh/@hot-labs/near-connect" } }
</script>
<script type="module">
  import { NearConnector } from "@hot-labs/near-connect";
</script>
```

## Quick Start

### Basic Dapp Integration

```typescript
import { NearConnector } from "@hot-labs/near-connect";

const connector = new NearConnector({
  network: "mainnet",
  walletConnect: {  // Optional, enables WalletConnect-based wallets
    projectId: "your-project-id",
    metadata: {
      name: "My App",
      description: "My NEAR App",
      url: window.location.origin,
      icons: ["https://example.com/icon.png"]
    }
  }
});

// Listen for sign in
connector.on("wallet:signIn", async ({ wallet, accounts }) => {
  const address = accounts[0].accountId;
  console.log("Connected:", address);
});

connector.on("wallet:signOut", async () => {
  console.log("Disconnected");
});

// Connect wallet (shows selection popup)
await connector.connect();

// Or connect to specific wallet
await connector.connect("hot-wallet");
```

### Check Existing Connection

```typescript
try {
  const wallet = await connector.wallet();
  const accounts = await wallet.getAccounts();
  console.log("Already connected:", accounts[0].accountId);
} catch (e) {
  // Not connected yet
}
```

### Send Transaction

```typescript
const wallet = await connector.wallet();

// Using near-wallet-selector action format
const result = await wallet.signAndSendTransaction({
  receiverId: "contract.near",
  actions: [{
    type: "FunctionCall",
    params: {
      methodName: "ft_transfer",
      args: { receiver_id: "bob.near", amount: "1000000000000000000000000" },
      gas: "30000000000000",
      deposit: "1"
    }
  }]
});

// OR using near-api-js action format (recommended)
import { transactions } from "near-api-js";

const result = await wallet.signAndSendTransaction({
  receiverId: "contract.near",
  actions: [
    transactions.functionCall(
      "ft_transfer",
      { receiver_id: "bob.near", amount: "1000000000000000000000000" },
      "30000000000000",
      "1"
    )
  ]
});
```

### Sign NEP-413 Message

```typescript
const signedMessage = await wallet.signMessage({
  message: "Hello NEAR!",
  recipient: "app.near",
  nonce: new Uint8Array(32) // Random nonce
});

console.log(signedMessage.signature);
```

## Core Concepts

### NearConnector Options

```typescript
interface NearConnectorOptions {
  network?: "mainnet" | "testnet";              // Default: "mainnet"
  features?: Partial<WalletFeatures>;            // Filter wallets by features
  excludedWallets?: string[];                    // Wallet IDs to exclude
  autoConnect?: boolean;                         // Default: true
  walletConnect?: { projectId: string; metadata: any };
  manifest?: string | { wallets: WalletManifest[]; version: string };
}
```

### Feature Filtering

Filter available wallets by required capabilities:

```typescript
const connector = new NearConnector({
  features: {
    signMessage: true,  // Require NEP-413 support
    testnet: true       // Require testnet support
  }
});
```

Available features:
- `signMessage` - NEP-413 message signing
- `signTransaction` - Transaction signing without sending
- `signAndSendTransaction` - Sign and send single transaction
- `signAndSendTransactions` - Sign and send multiple transactions
- `signInWithoutAddKey` - Connect without adding function call access key
- `mainnet` - Mainnet network support
- `testnet` - Testnet network support

### NearConnector Methods

```typescript
// Show wallet selector and connect
await connector.connect(walletId?: string): Promise<NearWalletBase>

// Disconnect current wallet
await connector.disconnect(): Promise<void>

// Get current or specific wallet instance
await connector.wallet(id?: string): Promise<NearWalletBase>

// Show wallet selector popup (returns wallet ID)
await connector.selectWallet(): Promise<string>

// Switch network (disconnects current wallet)
await connector.switchNetwork(network: "mainnet" | "testnet"): Promise<void>

// Get filtered list of available wallets
connector.availableWallets: NearWalletBase[]
```

### Wallet Interface

All wallets implement `NearWalletBase`:

```typescript
interface NearWalletBase {
  manifest: WalletManifest;
  
  signIn(data?: {
    network?: Network;
    contractId?: string;
    methodNames?: string[];
  }): Promise<Account[]>;
  
  signOut(data?: { network?: Network }): Promise<void>;
  
  getAccounts(data?: { network?: Network }): Promise<Account[]>;
  
  signAndSendTransaction(params: {
    signerId?: string;
    receiverId: string;
    actions: Action[];
    network?: Network;
  }): Promise<FinalExecutionOutcome>;
  
  signAndSendTransactions(params: {
    transactions: Transaction[];
    network?: Network;
  }): Promise<FinalExecutionOutcome[]>;
  
  signMessage(params: {
    message: string;
    recipient: string;
    nonce: Uint8Array;
    network?: Network;
  }): Promise<SignedMessage>;
}
```

## Advanced Features

### Limited Access Keys (Deprecated)

```typescript
// Add limited-access key during sign in (not recommended for UX)
const connector = new NearConnector({
  signIn: { 
    contractId: "game.near",
    methodNames: ["play_move", "end_game"]
  }
});
```

**Better approach**: Add limited-access key after user starts interacting with your app, not during initial connection.

### Debug Wallet Integration

Test custom wallet implementations without modifying the manifest:

```typescript
// Register debug wallet
await connector.registerDebugWallet({
  id: "my-wallet",
  name: "My Custom Wallet",
  version: "1.0.0",
  executor: "http://localhost:3000/wallet-executor.js",
  type: "sandbox",
  icon: "...",
  website: "...",
  features: { signMessage: true, signAndSendTransaction: true },
  permissions: { storage: true }
});

// Remove debug wallet
await connector.removeDebugWallet("my-wallet");
```

### Custom Manifest Source

```typescript
// Use custom manifest URL
const connector = new NearConnector({
  manifest: "https://my-server.com/wallets.json"
});

// Or provide manifest directly
const connector = new NearConnector({
  manifest: {
    version: "1.0.0",
    wallets: [/* custom wallet manifests */]
  }
});
```

### Events

```typescript
connector.on("wallet:signIn", ({ wallet, accounts, success }) => {
  // Handle sign in
});

connector.on("wallet:signOut", ({ success }) => {
  // Handle sign out
});

connector.on("selector:walletsChanged", () => {
  // Available wallets changed (e.g., extension installed)
});

connector.on("selector:manifestUpdated", () => {
  // Manifest reloaded
});

// Also available: once(), off(), removeAllListeners()
```

## Wallet Integration Guide

To integrate your wallet with near-connect, see [references/wallet_integration.md](references/wallet_integration.md) for detailed instructions on:

- Writing executor scripts
- Manifest specification and permissions
- Sandbox API and limitations
- Testing and debugging

## Action Types Reference

Near-connect supports two action formats. See [references/action_types.md](references/action_types.md) for:

- Detailed action type specifications
- Examples of both formats
- Migration guide from near-wallet-selector

## Sandbox Security Model

Wallet executor scripts run in sandboxed iframes. See [references/sandbox_security.md](references/sandbox_security.md) for:

- Security architecture
- Permission system
- Isolation guarantees
- Audit scope

## Integration Examples

See [references/integration_examples.md](references/integration_examples.md) for complete code examples:

- React integration with hooks
- Multiple account management
- Transaction batching
- Error handling patterns

## Supported Wallets

- **HOT Wallet** - Multichain wallet with gas refueling
- **Meteor Wallet** - Simple and secure DeFi wallet
- **Intear Wallet** - Fast wallet for dApp interactions
- **MyNearWallet** - Web wallet for NEAR
- **Nightly Wallet** - Multichain metaverse wallet
- **NEAR Mobile** - Official NEAR mobile wallet
- **Unity Wallet** - Self-custodial Web3 wallet
- **OKX Wallet** - OKX ecosystem wallet
- **WalletConnect** - Connect any WalletConnect-compatible wallet

## Troubleshooting

**Connection Issues**: Check browser console for detailed logs with `logger` option:

```typescript
const connector = new NearConnector({
  logger: { log: console.log }
});
```

**Wallet Not Appearing**: Verify feature requirements and network match wallet capabilities.

**Transaction Failures**: Ensure actions use correct format (see action_types.md) and adequate gas/deposit values.

## Migration from near-wallet-selector

Near-connect is designed as a drop-in replacement for most near-wallet-selector use cases:

1. Replace `setupWalletSelector()` with `new NearConnector()`
2. Use `connector.connect()` instead of `selector.show()`
3. Actions can remain unchanged (backward compatible format supported)
4. Event names align with near-wallet-selector patterns

See [references/integration_examples.md](references/integration_examples.md) for migration examples.
