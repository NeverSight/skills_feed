---
name: viem
description: TypeScript patterns for low-level EVM blockchain interactions using Viem. Use when writing Node scripts, CLI tools, or backend services that read/write to Ethereum or EVM chains. Triggers on contract interactions, wallet operations, transaction signing, event watching, ABI encoding, or any non-React blockchain TypeScript code. Do NOT use for React/Next.js apps with hooks (use wagmi skill instead).
version: "2.x"
docs: https://viem.sh
---

# Viem Skill

> **Version:** Viem 2.x | [Official Docs](https://viem.sh)

Viem is the modern TypeScript interface for Ethereum. This skill ensures correct patterns for contract interactions, client setup, and type safety.

## Quick Reference

```typescript
import { createPublicClient, createWalletClient, http } from 'viem'
import { mainnet } from 'viem/chains'
import { privateKeyToAccount } from 'viem/accounts'
```

## Critical Patterns

### 1. Client Setup

**Public Client** (read-only operations):
```typescript
const publicClient = createPublicClient({
  chain: mainnet,
  transport: http('https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY'),
})
```

**Wallet Client** (write operations):
```typescript
const account = privateKeyToAccount('0x...')
const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http('https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY'),
})
```

### 2. ABI Type Safety (CRITICAL)

Always use `as const` for ABIs to get full type inference:

```typescript
// ✅ CORRECT - Full type safety
const abi = [
  {
    name: 'balanceOf',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: 'owner', type: 'address' }],
    outputs: [{ name: '', type: 'uint256' }],
  },
] as const

// ❌ WRONG - No type inference
const abi = [{ name: 'balanceOf', ... }] // Missing `as const`
```

### 3. Contract Read Pattern

```typescript
const balance = await publicClient.readContract({
  address: '0x...', // Contract address
  abi,
  functionName: 'balanceOf',
  args: ['0x...'], // Args are fully typed when using `as const`
})
```

### 4. Contract Write Pattern (Simulate First!)

Always simulate before writing to catch errors early:

```typescript
// Step 1: Simulate
const { request } = await publicClient.simulateContract({
  account,
  address: '0x...',
  abi,
  functionName: 'transfer',
  args: ['0x...', 1000000n], // Use BigInt for uint256
})

// Step 2: Execute
const hash = await walletClient.writeContract(request)

// Step 3: Wait for receipt
const receipt = await publicClient.waitForTransactionReceipt({ hash })
```

### 5. Event Watching

```typescript
const unwatch = publicClient.watchContractEvent({
  address: '0x...',
  abi,
  eventName: 'Transfer',
  onLogs: (logs) => {
    for (const log of logs) {
      console.log(log.args.from, log.args.to, log.args.value)
    }
  },
})

// Clean up
unwatch()
```

### 6. Multicall for Batch Reads

```typescript
const results = await publicClient.multicall({
  contracts: [
    { address: '0x...', abi, functionName: 'balanceOf', args: ['0x...'] },
    { address: '0x...', abi, functionName: 'totalSupply' },
  ],
})
// results[0].result, results[1].result
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `as const` on ABI | Add `as const` for type inference |
| Using `Number` for amounts | Use `BigInt` literals: `1000000n` |
| Writing without simulate | Always `simulateContract` first |
| Hardcoding gas | Let viem estimate, or use `gas: await publicClient.estimateGas(...)` |
| Not awaiting receipts | Use `waitForTransactionReceipt` for confirmation |

## Chain Configuration

```typescript
import { mainnet, polygon, arbitrum, optimism, base } from 'viem/chains'

// Custom chain
const customChain = {
  id: 123,
  name: 'My Chain',
  nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://rpc.mychain.com'] },
  },
}
```

## Error Handling

```typescript
import { BaseError, ContractFunctionRevertedError } from 'viem'

try {
  await publicClient.simulateContract({ ... })
} catch (err) {
  if (err instanceof BaseError) {
    const revertError = err.walk(e => e instanceof ContractFunctionRevertedError)
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName
      // Handle specific revert reason
    }
  }
}
```

## References

For detailed patterns, see:
- `references/contract-patterns.md` - Advanced contract interaction patterns
- `references/common-errors.md` - Error handling and debugging guide
- [Viem Documentation](https://viem.sh) - Official docs
- [Viem GitHub](https://github.com/wevm/viem) - Source and releases
