---
name: near-connect-hooks
description: React hooks for NEAR Protocol wallet integration using @hot-labs/near-connect. Use when building React/Next.js apps that need NEAR wallet connection, smart contract calls (view and change methods), token transfers, access key management, or NEP-413 message signing. Triggers on queries about NEAR wallet hooks, NearProvider setup, useNearWallet hook, or NEAR dApp React integration.
---

# near-connect-hooks

React hooks library for NEAR wallet integration built on `@hot-labs/near-connect`.

## Installation

```bash
npm install near-connect-hooks @hot-labs/near-connect near-api-js
```

## Quick Start

### 1. Wrap App with NearProvider

```tsx
import { NearProvider } from 'near-connect-hooks';

function App() {
  return (
    <NearProvider config={{ network: 'mainnet' }}>
      <YourApp />
    </NearProvider>
  );
}
```

### 2. Use the Hook

```tsx
import { useNearWallet } from 'near-connect-hooks';

function WalletButton() {
  const { signedAccountId, loading, signIn, signOut } = useNearWallet();
  
  if (loading) return <div>Loading...</div>;
  if (!signedAccountId) return <button onClick={signIn}>Connect</button>;
  return <button onClick={signOut}>Disconnect {signedAccountId}</button>;
}
```

## Core API

### Hook Properties

| Property | Type | Description |
|----------|------|-------------|
| `signedAccountId` | `string` | Connected account ID or empty string |
| `loading` | `boolean` | Initialization state |
| `network` | `"mainnet" \| "testnet"` | Current network |
| `provider` | `JsonRpcProvider` | Direct RPC provider access |
| `connector` | `NearConnector` | Direct connector access |

### Authentication

```tsx
const { signIn, signOut } = useNearWallet();

await signIn();   // Opens wallet selector
await signOut();  // Disconnects wallet
```

### View Functions (Read-Only)

```tsx
const { viewFunction } = useNearWallet();

const result = await viewFunction({
  contractId: 'contract.near',
  method: 'get_data',
  args: { key: 'value' }  // optional
});
```

### Call Functions (State Changes)

```tsx
const { callFunction } = useNearWallet();

await callFunction({
  contractId: 'contract.near',
  method: 'set_data',
  args: { key: 'value' },
  gas: '30000000000000',      // optional, default: 30 TGas
  deposit: '1000000000000000000000000'  // optional, 1 NEAR in yoctoNEAR
});
```

### Transfers

```tsx
const { transfer } = useNearWallet();

await transfer({
  receiverId: 'recipient.near',
  amount: '1000000000000000000000000'  // 1 NEAR in yoctoNEAR
});
```

### Account Info

```tsx
const { getBalance, getAccessKeyList, signedAccountId } = useNearWallet();

const balance = await getBalance(signedAccountId);  // bigint in yoctoNEAR
const keys = await getAccessKeyList(signedAccountId);  // AccessKeyList
```

### NEP-413 Message Signing

```tsx
const { signNEP413Message } = useNearWallet();

const signed = await signNEP413Message({
  message: 'Verify ownership',
  recipient: 'app.near',
  nonce: crypto.getRandomValues(new Uint8Array(32))
});
```

### Access Key Management

```tsx
const { addFunctionCallKey, deleteKey } = useNearWallet();

// Add function call key
await addFunctionCallKey({
  publicKey: 'ed25519:...',
  contractId: 'contract.near',
  methodNames: ['method1', 'method2'],  // empty = all methods
  allowance: '250000000000000000000000'  // optional
});

// Delete key
await deleteKey({ publicKey: 'ed25519:...' });
```

## Advanced Usage

### Low-Level Transactions

```tsx
import { useNearWallet, Actions } from 'near-connect-hooks';

const { signAndSendTransaction, signAndSendTransactions } = useNearWallet();

// Single transaction with multiple actions
await signAndSendTransaction({
  receiverId: 'contract.near',
  actions: [
    Actions.functionCall('method', { arg: 'value' }, '30000000000000', '0'),
    Actions.transfer('1000000000000000000000000')
  ]
});

// Multiple transactions
await signAndSendTransactions([
  { receiverId: 'contract1.near', actions: [Actions.transfer('1000')] },
  { receiverId: 'contract2.near', actions: [Actions.functionCall('m', {}, '30000000000000', '0')] }
]);
```

### Action Builders

```tsx
import { Actions } from 'near-connect-hooks';

Actions.transfer(amount)
Actions.functionCall(methodName, args, gas, deposit)
Actions.addFullAccessKey(publicKey)
Actions.addFunctionCallKey(publicKey, receiverId, methodNames, allowance)
Actions.deleteKey(publicKey)
```

## Provider Configuration

```tsx
<NearProvider config={{
  network: 'mainnet',  // 'testnet' | 'mainnet'
  providers: {
    mainnet: ['https://free.rpc.fastnear.com'],
    testnet: ['https://test.rpc.fastnear.com']
  }
}}>
```

## Reference Files

- [API Reference](references/api-reference.md) - Full type definitions and method signatures
- [Examples](references/examples.md) - Complete integration examples
