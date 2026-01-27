---
name: wagmi
description: React hooks for Ethereum and EVM blockchain interactions using Wagmi v3. Use when building React or Next.js apps with wallet connections, contract reads/writes, or blockchain state. Triggers on useAccount, useConnect, useContractRead, useContractWrite, WagmiProvider, ConnectKit, RainbowKit, or any React blockchain hooks. Do NOT use for Node scripts or non-React code (use viem skill instead).
version: "3.x"
docs: https://wagmi.sh
---

# Wagmi Skill

> **Version:** Wagmi 3.x | [Official Docs](https://wagmi.sh) | Requires TypeScript 5.7.3+

Wagmi provides React hooks for Ethereum. This skill ensures correct patterns for provider setup, hooks usage, and React-specific pitfalls.

## Quick Setup (Wagmi v3)

### 1. Config Setup

```typescript
// config.ts
import { http, createConfig } from 'wagmi'
import { mainnet, polygon, arbitrum } from 'wagmi/chains'
// v3: Install connectors separately: npm i @wagmi/connectors
import { injected, coinbaseWallet, walletConnect } from '@wagmi/connectors'

export const config = createConfig({
  chains: [mainnet, polygon, arbitrum],
  connectors: [
    injected(),
    coinbaseWallet({ appName: 'My App' }),
    walletConnect({ projectId: 'YOUR_PROJECT_ID' }),
  ],
  transports: {
    [mainnet.id]: http('https://eth-mainnet.g.alchemy.com/v2/KEY'),
    [polygon.id]: http('https://polygon-mainnet.g.alchemy.com/v2/KEY'),
    [arbitrum.id]: http('https://arb-mainnet.g.alchemy.com/v2/KEY'),
  },
})
```

> **v3 Note:** Connectors are now in `@wagmi/connectors` package for better dependency control.

### 2. Provider Setup

```tsx
// providers.tsx
'use client' // Required for Next.js App Router

import { WagmiProvider } from 'wagmi'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { config } from './config'

const queryClient = new QueryClient()

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

## Core Hooks

### useAccount
```tsx
import { useAccount } from 'wagmi'

function Profile() {
  const { address, isConnected, isConnecting, chain } = useAccount()
  
  if (isConnecting) return <div>Connecting...</div>
  if (!isConnected) return <div>Not connected</div>
  
  return <div>Connected: {address} on {chain?.name}</div>
}
```

### useConnect / useDisconnect / useConnectors
```tsx
import { useAccount, useConnect, useDisconnect, useConnectors } from 'wagmi'

function ConnectButton() {
  // v3: Use useConnectors() hook instead of getting from useConnect()
  const connectors = useConnectors()
  const { connect, isPending } = useConnect()
  const { disconnect } = useDisconnect()
  const { isConnected } = useAccount()

  if (isConnected) {
    return <button onClick={() => disconnect()}>Disconnect</button>
  }

  return (
    <div>
      {connectors.map((connector) => (
        <button
          key={connector.id}
          onClick={() => connect({ connector })}
          disabled={isPending}
        >
          {connector.name}
        </button>
      ))}
    </div>
  )
}
```

### useReadContract (REPLACES useContractRead)
```tsx
import { useReadContract } from 'wagmi'

function Balance() {
  const { data, isLoading, error, refetch } = useReadContract({
    address: '0x...',
    abi, // Use `as const` for type safety
    functionName: 'balanceOf',
    args: ['0x...'],
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return <div>Balance: {data?.toString()}</div>
}
```

### useWriteContract (REPLACES useContractWrite)
```tsx
import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi'

function Transfer() {
  const { data: hash, writeContract, isPending, error } = useWriteContract()
  
  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  })

  async function handleTransfer() {
    writeContract({
      address: '0x...',
      abi,
      functionName: 'transfer',
      args: ['0x...', 1000n],
    })
  }

  return (
    <div>
      <button onClick={handleTransfer} disabled={isPending}>
        {isPending ? 'Confirming...' : 'Transfer'}
      </button>
      {isConfirming && <div>Waiting for confirmation...</div>}
      {isSuccess && <div>Transaction confirmed!</div>}
      {error && <div>Error: {error.message}</div>}
    </div>
  )
}
```

## Critical Patterns

### ABI Type Safety (CRITICAL)
```typescript
// ✅ CORRECT - as const for full type inference
const abi = [
  {
    name: 'transfer',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'to', type: 'address' },
      { name: 'amount', type: 'uint256' },
    ],
    outputs: [{ name: '', type: 'bool' }],
  },
] as const

// ❌ WRONG - no type inference
const abi = [{ ... }] // Missing `as const`
```

### Conditional Hook Calls (NEVER conditional)
```tsx
// ❌ WRONG - Violates Rules of Hooks
function BadComponent({ shouldFetch }) {
  if (shouldFetch) {
    const { data } = useReadContract({ ... })
  }
}

// ✅ CORRECT - Use enabled option
function GoodComponent({ shouldFetch }) {
  const { data } = useReadContract({
    ...params,
    query: { enabled: shouldFetch },
  })
}
```

### Stale Closure Prevention
```tsx
// ❌ WRONG - Captures stale values
function BadComponent() {
  const [amount, setAmount] = useState(0n)
  
  const { writeContract } = useWriteContract()
  
  // This captures `amount` at render time!
  const handleClick = () => {
    writeContract({
      ...params,
      args: [amount], // May be stale!
    })
  }
}

// ✅ CORRECT - Pass fresh values
function GoodComponent() {
  const [amount, setAmount] = useState(0n)
  const { writeContract } = useWriteContract()

  const handleClick = () => {
    writeContract({
      ...params,
      args: [amount], // Fresh from closure
    })
  }
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| useContractRead (v1) | Use `useReadContract` |
| useContractWrite (v1) | Use `useWriteContract` |
| `connectors` from useConnect (v2) | Use `useConnectors()` hook (v3) |
| `chains` from useSwitchChain (v2) | Use `useChains()` hook (v3) |
| Conditional hooks | Use `query: { enabled: bool }` |
| Missing QueryClientProvider | Wagmi requires TanStack Query |
| Not awaiting hash | Use `useWaitForTransactionReceipt` |
| String amounts | Use BigInt: `1000n` |
| Connectors from `wagmi/connectors` | Use `@wagmi/connectors` package (v3) |

## References

For detailed patterns, see:
- `references/hooks-guide.md` - Complete hooks reference
- `references/react-patterns.md` - React-specific patterns and SSR
- [Wagmi Documentation](https://wagmi.sh) - Official docs
- [Wagmi GitHub](https://github.com/wevm/wagmi) - Source and releases
- [v2 to v3 Migration](https://wagmi.sh/react/guides/migrate-from-v2-to-v3) - Breaking changes
