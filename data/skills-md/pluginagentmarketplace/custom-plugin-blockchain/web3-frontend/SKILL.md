---
name: web3-frontend
description: Master Web3 frontend development with wallet integration, viem/wagmi, and dApp UX
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 05-web3-frontend
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: web3_frontend

# Parameter Validation
parameters:
  topic:
    type: string
    required: true
    enum: [wallet, transactions, signing, hooks, errors]
  framework:
    type: string
    default: react
    enum: [react, next, vue, vanilla]

# Retry & Error Handling
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

# Logging & Observability
logging:
  level: info
  include_timestamps: true
  track_usage: true
---

# Web3 Frontend Skill

> Master Web3 frontend development with wallet integration, modern libraries (viem/wagmi), and production dApp patterns.

## Quick Start

```python
# Invoke this skill for Web3 frontend development
Skill("web3-frontend", topic="wallet", framework="react")
```

## Topics Covered

### 1. Wallet Integration
Connect users to Web3:
- **RainbowKit**: Beautiful wallet modal
- **WalletConnect**: Mobile support
- **Account Abstraction**: ERC-4337
- **Multi-chain**: Network switching

### 2. Transaction Management
Handle blockchain interactions:
- **Write Operations**: Contract writes
- **State Tracking**: Pending, confirmed
- **Gas Estimation**: Fee display
- **Error Handling**: User-friendly messages

### 3. Signing & Auth
Verify user identity:
- **EIP-712**: Typed data signing
- **SIWE**: Sign-In with Ethereum
- **Permit**: Gasless approvals
- **Message Signing**: Personal sign

### 4. React Hooks
Modern patterns with wagmi:
- **useAccount**: Connection state
- **useWriteContract**: Transactions
- **useReadContract**: Data fetching
- **useWaitForTransactionReceipt**: Confirmations

## Code Examples

### Connect Wallet
```tsx
'use client';

import { ConnectButton } from '@rainbow-me/rainbowkit';
import { useAccount } from 'wagmi';

export function WalletConnect() {
  const { address, isConnected } = useAccount();

  return (
    <div>
      <ConnectButton />
      {isConnected && <p>Connected: {address}</p>}
    </div>
  );
}
```

### Write Contract
```tsx
import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi';
import { parseEther } from 'viem';

export function MintButton() {
  const { writeContract, data: hash, isPending } = useWriteContract();
  const { isLoading, isSuccess } = useWaitForTransactionReceipt({ hash });

  const mint = () => {
    writeContract({
      address: '0x...',
      abi: [...],
      functionName: 'mint',
      args: [1n],
      value: parseEther('0.08'),
    });
  };

  return (
    <button onClick={mint} disabled={isPending || isLoading}>
      {isPending ? 'Confirm in wallet...' :
       isLoading ? 'Minting...' :
       isSuccess ? 'Minted!' : 'Mint NFT'}
    </button>
  );
}
```

### Sign Typed Data (EIP-712)
```tsx
import { useSignTypedData } from 'wagmi';

const DOMAIN = {
  name: 'My App',
  version: '1',
  chainId: 1,
  verifyingContract: '0x...',
};

export function useSignOrder() {
  const { signTypedDataAsync } = useSignTypedData();

  const sign = async (order: Order) => {
    return await signTypedDataAsync({
      domain: DOMAIN,
      types: { Order: [...] },
      primaryType: 'Order',
      message: order,
    });
  };

  return { sign };
}
```

### Error Handling
```typescript
export function parseError(error: unknown): string {
  const msg = error instanceof Error ? error.message : String(error);

  if (msg.includes('user rejected')) return 'Transaction cancelled';
  if (msg.includes('insufficient funds')) return 'Insufficient balance';
  if (msg.includes('execution reverted')) {
    const reason = msg.match(/reason="([^"]+)"/)?.[1];
    return reason || 'Transaction would fail';
  }

  return 'Transaction failed';
}
```

## Package Setup

```bash
npm install wagmi viem @rainbow-me/rainbowkit @tanstack/react-query
```

```tsx
// providers/Web3.tsx
import { WagmiProvider } from 'wagmi';
import { RainbowKitProvider } from '@rainbow-me/rainbowkit';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { config } from './config';

const queryClient = new QueryClient();

export function Web3Provider({ children }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>{children}</RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

## Common Patterns

| Pattern | Use Case | Hook |
|---------|----------|------|
| Connect wallet | User auth | `useAccount` |
| Read data | Display balances | `useReadContract` |
| Write tx | Mint, transfer | `useWriteContract` |
| Wait for tx | Confirm state | `useWaitForTransactionReceipt` |
| Sign message | Auth, permit | `useSignMessage` |

## Common Pitfalls

| Pitfall | Issue | Solution |
|---------|-------|----------|
| Hydration error | SSR mismatch | Use `dynamic` with `ssr: false` |
| BigInt serialization | JSON.stringify | Custom serializer |
| Stale data | Cache issues | Use `refetchInterval` |

## Troubleshooting

### "Wallet not connecting"
```tsx
// Ensure client-side only
import dynamic from 'next/dynamic';

const ConnectButton = dynamic(
  () => import('./ConnectButton'),
  { ssr: false }
);
```

### "Transaction pending forever"
Check gas settings or speed up:
```typescript
await wallet.sendTransaction({
  ...tx,
  maxFeePerGas: tx.maxFeePerGas * 120n / 100n,
});
```

## Security Checklist

- [ ] Never expose private keys
- [ ] Validate contract addresses
- [ ] Sanitize user inputs
- [ ] Use proper error boundaries
- [ ] Implement CSP headers

## Cross-References

- **Bonded Agent**: `05-web3-frontend`
- **Related Skills**: `ethereum-development`, `solidity-development`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade with wagmi v2, viem |
| 1.0.0 | 2024-12 | Initial release |
