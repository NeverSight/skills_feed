---
name: web3-viem
description: This skill should be used when the user asks about "viem", "viem client", "viem actions", "TypeScript Ethereum", "createPublicClient", "createWalletClient", "parseEther", "formatEther", "readContract", "writeContract", or mentions using viem for blockchain interactions.
---

# Viem

## Overview

Viem is a TypeScript interface for Ethereum that provides low-level stateless primitives for interacting with the blockchain. It focuses on developer experience, stability, bundle size, and performance.

Key features:

- Automatic type safety and inference
- Tree-shakable lightweight modules
- Optimized encoding/parsing
- Composable APIs

## Core Concepts

| Concept        | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| **Clients**    | `PublicClient`, `WalletClient`, `TestClient` - entry points   |
| **Transports** | Connection layer (`http`, `webSocket`, `custom`)              |
| **Actions**    | Operations like `getBlockNumber`, `sendTransaction`           |
| **Chains**     | Chain configurations (`mainnet`, `sepolia`, `arbitrum`, etc.) |

## Constants

Viem exports useful constants for common values:

```typescript
import { maxUint256, maxUint128, maxInt256, zeroAddress, zeroHash } from "viem";

// Max values for uint types
maxUint256; // 2n ** 256n - 1n
maxUint128; // 2n ** 128n - 1n

// Zero values
zeroAddress; // 0x0000000000000000000000000000000000000000
zeroHash; // 0x0000000000000000000000000000000000000000000000000000000000000000
```

## Utilities

### Unit Conversion

Convert between wei and human-readable values:

```typescript
import { parseEther, formatEther, parseUnits, formatUnits } from "viem";

// ETH <-> Wei (18 decimals)
parseEther("1"); // 1000000000000000000n
formatEther(1000000000000000000n); // "1"

// Custom decimals (e.g., USDC with 6 decimals)
parseUnits("100", 6); // 100000000n
formatUnits(100000000n, 6); // "100"
```

### ABI Utilities

Parse human-readable ABIs:

```typescript
import { parseAbi, parseAbiItem } from "viem";

const abi = parseAbi([
  "function balanceOf(address owner) view returns (uint256)",
  "function transfer(address to, uint256 amount) returns (bool)",
  "event Transfer(address indexed from, address indexed to, uint256 amount)",
]);

const item = parseAbiItem("function name() view returns (string)");
```

### Address Utilities

```typescript
import { getAddress, isAddress, isAddressEqual } from "viem";

// Checksum address
getAddress("0xabc..."); // "0xAbc..." (checksummed)

// Validation
isAddress("0x..."); // true/false
isAddressEqual("0xAbc...", "0xabc..."); // true (case-insensitive)
```

## Clients

### Public Client (Read Operations)

For querying blockchain state:

```typescript
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(), // or http("https://eth-mainnet.g.alchemy.com/v2/...")
});

// Read operations
const blockNumber = await publicClient.getBlockNumber();
const balance = await publicClient.getBalance({ address: "0x..." });
const block = await publicClient.getBlock();
```

### Wallet Client (Write Operations)

For signing and sending transactions:

```typescript
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const account = privateKeyToAccount("0x...");

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(),
});

// Send transaction
const hash = await walletClient.sendTransaction({
  to: "0x...",
  value: parseEther("0.1"),
});
```

### Browser Wallet Client

For browser environments with injected wallets:

```typescript
import "viem/window";
import { createWalletClient, custom } from "viem";
import { mainnet } from "viem/chains";

const walletClient = createWalletClient({
  chain: mainnet,
  transport: custom(window.ethereum!),
});

// Request accounts
const [address] = await walletClient.requestAddresses();
```

### Extending Clients

Combine capabilities using `.extend()`:

```typescript
import { createWalletClient, http, publicActions } from "viem";
import { mainnet } from "viem/chains";

const client = createWalletClient({
  chain: mainnet,
  transport: http(),
}).extend(publicActions);

// Now supports both wallet and public actions
const balance = await client.getBalance({ address: "0x..." });
const hash = await client.sendTransaction({ to: "0x...", value: 1n });
```

## Contract Interactions

### Reading from Contracts

```typescript
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(),
});

const abi = [
  {
    inputs: [{ name: "owner", type: "address" }],
    name: "balanceOf",
    outputs: [{ name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
] as const;

const balance = await publicClient.readContract({
  address: "0x...", // Contract address
  abi,
  functionName: "balanceOf",
  args: ["0x..."], // Owner address
});
```

### Writing to Contracts

```typescript
const hash = await walletClient.writeContract({
  address: "0x...",
  abi,
  functionName: "transfer",
  args: ["0x...", parseUnits("100", 18)],
});
```

### Simulating Before Writing

Simulate a transaction before sending:

```typescript
const { request } = await publicClient.simulateContract({
  address: "0x...",
  abi,
  functionName: "transfer",
  args: ["0x...", parseUnits("100", 18)],
  account: "0x...",
});

const hash = await walletClient.writeContract(request);
```

## Account Types

### Local Accounts

For server-side or controlled environments:

```typescript
import { privateKeyToAccount, mnemonicToAccount } from "viem/accounts";

// From private key
const account = privateKeyToAccount("0x...");

// From mnemonic
const account = mnemonicToAccount("legal winner thank year wave sausage ...");
```

### JSON-RPC Accounts

For browser wallets:

```typescript
import "viem/window";

const [account] = await window.ethereum!.request({
  method: "eth_requestAccounts",
});
```

## Chain Configuration

### Built-in Chains

```typescript
import { mainnet, sepolia, arbitrum, optimism, polygon, base } from "viem/chains";

const client = createPublicClient({
  chain: arbitrum,
  transport: http(),
});
```

### Custom Chains

```typescript
import { defineChain } from "viem";

const customChain = defineChain({
  id: 123456,
  name: "My Chain",
  nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: ["https://rpc.mychain.com"] },
  },
  blockExplorers: {
    default: { name: "Explorer", url: "https://explorer.mychain.com" },
  },
});
```

## Documentation

This skill provides a reference for common operations. For comprehensive documentation, fetch the full viem docs using context7 MCP:

```
Library ID: /wevm/viem
```

Use context7 to query specific topics:

- `clients` - Client types and configuration
- `actions` - Available actions (read, write, wallet)
- `accounts` - Local and JSON-RPC accounts
- `contract` - Contract interactions (`readContract`, `writeContract`)
- `abi` - ABI encoding/decoding utilities
- `chains` - Supported chains and custom chain configuration

### Fetching Documentation

To fetch viem documentation for a specific topic:

1. Resolve the library ID with `mcp__context7__resolve-library-id` (or use `/wevm/viem` directly)
2. Call `mcp__context7__get-library-docs` with the topic parameter

Example topics: `"getting started"`, `"wallet client"`, `"send transaction"`, `"read contract"`.
