---
name: chain-integration
description: Integrate a new blockchain as a second-class citizen in ShapeShift Web. HDWallet packages live in the monorepo under packages/hdwallet-*. Covers everything from HDWallet native/Ledger support to Web chain adapter, asset generation, and feature flags. Activates when user wants to add basic support for a new blockchain.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Chain Integration Skill

You are helping integrate a new blockchain as a **second-class citizen** into ShapeShift Web and HDWallet. This means basic support (native asset send/receive, account derivation, swaps to/from the chain) using the "poor man's" approach similar to Monad, Tron, and Sui - public RPC, no microservices, minimal features.

## When This Skill Activates

Use this skill when the user wants to:
- "Add support for [ChainName]"
- "Integrate [ChainName] as second-class citizen"
- "Implement basic [ChainName] support"
- "Add [ChainName] with native wallet only"

## Critical Understanding

### Second-Class Citizen Pattern
Recent examples: **Monad** (EVM), **Tron** (UTXO-like), **Sui** (non-EVM)

**What it includes:**
- ✅ Native asset sends/receives
- ✅ Account derivation (Native wallet required, Ledger optional)
- ✅ Swap to/from the chain
- ✅ Poor man's balance updates (public RPC polling)
- ✅ Poor man's tx status (RPC polling with eth_getTransactionReceipt or equivalent)
- ✅ Feature flag gating

**What it DOESN'T include:**
- ❌ Full transaction history (no microservices)
- ❌ First-class Unchained API support
- ❌ Advanced features (staking, DeFi, etc.)
- ❌ All wallet support (usually just Native initially)

### Development Flow

**ALWAYS follow this order:**

1. **HDWallet Native Support** (workspace packages under `packages/hdwallet-*`)
2. **Web Basic Support** (poor man's chain adapter)
3. **Web Plugin & Integration** (wire everything up)
4. **Ledger Support** (`packages/hdwallet-ledger` - if chain is supported by Ledger)

## Phase 0: Deep Research & Information Gathering

**CRITICAL**: This phase determines the entire integration strategy. Take time to research thoroughly.

### Step 0.1: Initial Chain Discovery

**First, search for basic chain information:**

1. **Search for official chain website and docs**
   - Use WebSearch to find: "[ChainName] blockchain official website"
   - Look for: developer docs, whitepaper, GitHub repos

2. **Determine chain architecture**
   - **CRITICAL QUESTION**: Is this an EVM-compatible chain?
   - Search: "[ChainName] EVM compatible"
   - Look for keywords: "Ethereum Virtual Machine", "Solidity", "EVM-compatible", "Ethereum fork"
   - Check if they mention Metamask compatibility

3. **Find RPC endpoints**
   - Search: "[ChainName] public RPC endpoint"
   - Check official docs for RPC URLs
   - Look for ChainList entry: https://chainlist.org
   - Check: https://github.com/arddluma/awesome-list-rpc-nodes-providers

**Why this matters:**
- **EVM chains** (like Monad): 90% less code! Just add to EVM chains list. Auto-supported by all EVM wallets.
- **Non-EVM chains** (like Tron, Sui): Need full custom implementation with crypto adapters.

### Step 0.2: Interactive Information Gathering

**Use the `AskUserQuestion` tool with the Claude inquiry UI to gather information.**

**Question 1 - Chain Architecture** (MOST IMPORTANT):
```
Does the user know if this is an EVM-compatible chain?

Options:
1. "Yes, it's EVM-compatible" → Proceed with EVM integration path (much simpler!)
2. "No, it's a custom blockchain" → Proceed with non-EVM integration path
3. "Not sure - can you research it?" → Perform web research (search for EVM compatibility indicators)

Context: EVM-compatible chains like Monad require minimal code changes (just add to supported chains list). Non-EVM chains like Tron/Sui require full custom crypto adapters.
```

**Question 2 - RPC Endpoint**:
```
Do you have a public RPC endpoint URL?

Options:
1. "Yes, here's the URL: [input]" → Use provided URL
2. "No, can you find one?" → Search ChainList.org, official docs, and GitHub for public RPC
3. "Need both HTTP and WebSocket" → Search for both endpoint types

Context: We need a reliable public RPC for the poor man's chain adapter. WebSocket is optional but nice for real-time updates.
```

**Question 3 - SLIP44 Coin Type**:
```
Do you know the SLIP44 coin type (BIP44 derivation path)?

Options:
1. "Yes, it's [number]" → Use provided coin type
2. "No, can you look it up?" → Search SLIP44 registry: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
3. "Use the same as Ethereum (60)" → Common for EVM chains

Context: This determines the BIP44 derivation path: m/44'/[TYPE]'/0'/0/0
```

### Step 0.3: Structured Information Collection

After determining chain type (EVM or non-EVM), collect remaining details:

**Use `AskUserQuestion` to ask:**

**For ALL chains:**

1. **Chain Basic Info**
   - Chain name (exact capitalization, e.g., "Monad", "Tron", "Sui")
   - SLIP44 coin type (from Step 0.2 above)
   - Chain ID (numeric or string, e.g., "1" for Ethereum, "monad-1", etc.)

2. **Documentation Links**
   - Official website URL
   - Developer documentation URL
   - Block explorer URL
   - GitHub repository (if available)

3. **Asset Information**
   - Native asset symbol (e.g., MON, TRX, SUI)
   - Native asset name (e.g., "Monad", "Tron", "Sui")
   - Decimals/precision (usually 18 for EVM, varies for others)
   - CoinGecko ID (search: "coingecko [chainname]" or ask user)

**For EVM chains only:**

4. **EVM-Specific Info**
   - Network/Chain ID (numeric, e.g., 41454 for Monad)
   - Token standard: ERC20 (always)
   - Block explorer API (etherscan-like)?
   - Any non-standard behavior vs Ethereum?

**For non-EVM chains only:**

5. **Chain Architecture Details**
   - Transaction structure/format (link to docs)
   - Signing algorithm (secp256k1, ed25519, etc.)
   - Address format (base58, bech32, hex, etc.)
   - Official SDK (npm package name if available)
   - Token standard name (e.g., "TRC20", "SUI Coin", "SPL")

6. **Ledger Hardware Wallet Support**
   - Search: "Ledger [ChainName] support"
   - Check: https://www.ledger.com/supported-crypto-assets
   - Ask user: "Does Ledger support [ChainName]?"
   - If yes, note the Ledger app name

**Action**: Don't proceed until you have:
- ✅ Confirmed EVM vs non-EVM architecture
- ✅ At least one working RPC endpoint
- ✅ SLIP44 coin type
- ✅ Official documentation links
- ✅ Basic asset information (symbol, name, decimals)

**Pro Tips:**
- For EVM chains: Integration is 10x easier. You mostly just add constants.
- For non-EVM: Budget extra time for crypto adapter implementation.
- Missing RPC? Check ChainList.org, official Discord, or GitHub repos.
- Missing SLIP44? Check if it's in SLIP-0044 registry or propose one.
- Can't find CoinGecko ID? Search their API or website directly.

---

## Integration Path Decision

**Based on Phase 0 research, choose your path:**

### Path A: EVM Chain Integration (SIMPLE)
**Examples**: Monad, Base, Arbitrum, Optimism

**Characteristics:**
- ✅ Uses Ethereum Virtual Machine
- ✅ Solidity smart contracts
- ✅ ERC20 token standard
- ✅ Web3/ethers.js compatible
- ✅ Auto-supported by MetaMask, Ledger Ethereum app

**What you'll do:**
1. HDWallet: Just add chain ID to EVM chains list (~10 lines of code)
2. Web: Extend EvmBaseAdapter (~100 lines)
3. Everything else: Add constants and config

**Time estimate**: 2-4 hours for basic integration

### Path B: Non-EVM Chain Integration (COMPLEX)
**Examples**: Tron, Sui, Cosmos, Solana

**Characteristics:**
- ❌ Custom virtual machine (not EVM)
- ❌ Custom smart contract language
- ❌ Custom token standard
- ❌ Custom transaction format
- ❌ Requires chain-specific crypto implementation

**What you'll do:**
1. HDWallet: Implement full chain module with crypto adapters (~500-1000 lines)
2. Web: Implement full IChainAdapter interface (~500-1000 lines)
3. Everything else: Add constants and config

**Time estimate**: 1-2 days for basic integration

---

## Phase 1: HDWallet Native Support

**Working Directory**: Same monorepo — hdwallet packages are at `packages/hdwallet-*`

### Step 1.0: Choose Implementation Strategy

**If EVM chain**: Continue with Step 1.2-EVM below (MINIMAL hdwallet work - ~30 minutes)
**If non-EVM chain**: Continue with Step 1.1 below (COMPLEX - 1-2 days)

### ⚡ EVM Chains: Minimal HDWallet Work Required

For EVM-compatible chains (like Monad, HyperEVM, Base), you need **MINIMAL changes** to hdwallet:

**What EVM chains DON'T need:**
- ❌ No new core interfaces (TronWallet, SuiWallet, etc.)
- ❌ No crypto adapters (address derivation, signing)
- ❌ No wallet mixins
- ✅ Use existing Ethereum crypto (secp256k1, Keccak256)

**What EVM chains DO need:**
- ✅ Wallet support flags (`_supportsChainName: boolean`)
- ✅ Support function (`supportsChainName()`)
- ✅ Set flags on all wallet implementations (~14 files)
- ✅ Build and verify with `yarn hdwallet:build`

**Why?** Each wallet type (Native, Ledger, MetaMask, etc.) needs to explicitly declare support for the chain, even though the crypto is identical. This enables wallet-specific gating in the UI.

**Reference PRs:**
- Monad hdwallet: <https://github.com/shapeshift/hdwallet/pull/753>
- HyperEVM hdwallet: <https://github.com/shapeshift/hdwallet/pull/756>

**Time estimate**: 30 minutes for hdwallet changes (vs 1-2 days for non-EVM)

### Step 1.1: Research HDWallet Patterns (Non-EVM Only)

Examine existing implementations to understand patterns:

**For non-EVM chains** (like Tron, Sui):
```bash
# In the monorepo
cat packages/hdwallet-core/src/tron.ts
cat packages/hdwallet-native/src/tron.ts
cat packages/hdwallet-native/src/crypto/isolation/adapters/tron.ts
```

Key pattern: Need new core interfaces, native implementation, and crypto adapters for signing.

### Step 1.2-EVM: EVM Chain Implementation (SIMPLE PATH)

**For EVM chains only** (like Monad):

**File**: `packages/hdwallet-core/src/ethereum.ts`
Add your chain to supported EVM chains:

```typescript
// Find the list of supported chain IDs and add yours
export const SUPPORTED_EVM_CHAINS = [
  1,      // Ethereum
  10,     // Optimism
  // ... other chains
  41454,  // Add your chain ID here (example: Monad)
]
```

**File**: `packages/hdwallet-core/src/utils.ts`
Register SLIP44 if not using Ethereum's (60):

```typescript
// If your chain uses a different SLIP44 than Ethereum
{ slip44: YOUR_SLIP44, symbol: 'SYMBOL', name: 'ChainName' }
```

**That's it for hdwallet!** EVM chains don't need crypto adapters. Skip to Step 1.6 (Version Bump).

### Step 1.2-EVM: EVM Chain HDWallet Support (MINIMAL WORK - ~30 minutes)

**For EVM chains only** (like Monad, HyperEVM). Follow these PRs as reference:
- **Monad hdwallet**: <https://github.com/shapeshift/hdwallet/pull/753>
- **HyperEVM hdwallet**: <https://github.com/shapeshift/hdwallet/pull/756>

**File**: `packages/hdwallet-core/src/ethereum.ts`

Add your chain's support flag to the ETHWalletInfo interface:

```typescript
export interface ETHWalletInfo extends HDWalletInfo {
  // ... existing flags
  readonly _supportsMonad: boolean;
  readonly _supportsHyperEvm: boolean;  // ADD THIS
  // ...
}
```

**File**: `packages/hdwallet-core/src/wallet.ts`

Add support function after `supportsMonad`:

```typescript
export function supportsMonad(wallet: HDWallet): wallet is ETHWallet {
  return isObject(wallet) && (wallet as any)._supportsMonad;
}

export function supports[ChainName](wallet: HDWallet): wallet is ETHWallet {
  return isObject(wallet) && (wallet as any)._supports[ChainName];
}
```

**Set flags on ALL wallet implementations** (~12 files):

**For second-class EVM chains (HyperEVM, Monad, Plasma):**

Set `readonly _supports[ChainName] = true` on:
- packages/hdwallet-native/src/ethereum.ts
- packages/hdwallet-metamask-multichain/src/shapeshift-multichain.ts (uses standard EVM cryptography)
- packages/hdwallet-ledger/src/ledger.ts (uses Ethereum app, supports all EVM chains)
- packages/hdwallet-trezor/src/trezor.ts (uses Ethereum app, supports all EVM chains)
- packages/hdwallet-walletconnectv2/src/walletconnectv2.ts (chain-agnostic, supports all EVM chains)

Set `readonly _supports[ChainName] = false` on:
- packages/hdwallet-coinbase/src/coinbase.ts
- packages/hdwallet-gridplus/src/gridplus.ts
- packages/hdwallet-keepkey/src/keepkey.ts
- packages/hdwallet-keplr/src/keplr.ts
- packages/hdwallet-phantom/src/phantom.ts
- packages/hdwallet-vultisig/src/vultisig.ts

**For non-EVM chains:**

Set `readonly _supports[ChainName] = true` for Native only:
- packages/hdwallet-native/src/ethereum.ts (or appropriate chain file)

Set `readonly _supports[ChainName] = false` on all other wallet types listed above.

**Then**: Skip to Step 1.6 (Build & Verify)

---

### Step 1.2-NonEVM: Non-EVM Core Interfaces (COMPLEX PATH)

**File**: `packages/hdwallet-core/src/[chainname].ts`

Create core TypeScript interfaces following the pattern:

```typescript
import { addressNListToBIP32, slip44ByCoin } from "./utils";
import { BIP32Path, HDWallet, HDWalletInfo, PathDescription } from "./wallet";

export interface [Chain]GetAddress {
  addressNList: BIP32Path;
  showDisplay?: boolean;
  pubKey?: string;
}

export interface [Chain]SignTx {
  addressNList: BIP32Path;
  // Chain-specific tx data fields
  rawDataHex?: string; // or other fields
}

export interface [Chain]SignedTx {
  serialized: string;
  signature: string;
}

export interface [Chain]TxSignature {
  signature: string;
}

export interface [Chain]GetAccountPaths {
  accountIdx: number;
}

export interface [Chain]AccountPath {
  addressNList: BIP32Path;
}

export interface [Chain]WalletInfo extends HDWalletInfo {
  readonly _supports[Chain]Info: boolean;
  [chainLower]GetAccountPaths(msg: [Chain]GetAccountPaths): Array<[Chain]AccountPath>;
  [chainLower]NextAccountPath(msg: [Chain]AccountPath): [Chain]AccountPath | undefined;
}

export interface [Chain]Wallet extends [Chain]WalletInfo, HDWallet {
  readonly _supports[Chain]: boolean;
  [chainLower]GetAddress(msg: [Chain]GetAddress): Promise<string | null>;
  [chainLower]SignTx(msg: [Chain]SignTx): Promise<[Chain]SignedTx | null>;
}

export function [chainLower]DescribePath(path: BIP32Path): PathDescription {
  const pathStr = addressNListToBIP32(path);
  const unknown: PathDescription = {
    verbose: pathStr,
    coin: "[ChainName]",
    isKnown: false,
  };

  if (path.length != 5) return unknown;
  if (path[0] != 0x80000000 + 44) return unknown;
  if (path[1] != 0x80000000 + slip44ByCoin("[ChainName]")) return unknown;
  if ((path[2] & 0x80000000) >>> 0 !== 0x80000000) return unknown;
  if (path[3] !== 0) return unknown;
  if (path[4] !== 0) return unknown;

  const index = path[2] & 0x7fffffff;
  return {
    verbose: `[ChainName] Account #${index}`,
    accountIdx: index,
    wholeAccount: true,
    coin: "[ChainName]",
    isKnown: true,
  };
}

// Standard BIP44 derivation: m/44'/SLIP44'/<account>'/0/0
export function [chainLower]GetAccountPaths(msg: [Chain]GetAccountPaths): Array<[Chain]AccountPath> {
  const slip44 = slip44ByCoin("[ChainName]");
  return [{ addressNList: [0x80000000 + 44, 0x80000000 + slip44, 0x80000000 + msg.accountIdx, 0, 0] }];
}
```

**Export from core**:
```typescript
// In packages/hdwallet-core/src/index.ts
export * from './[chainname]'
```

**Register SLIP44**:
```typescript
// In packages/hdwallet-core/src/utils.ts
// Add to slip44Table
{ slip44: SLIP44, symbol: '[SYMBOL]', name: '[ChainName]' }
```

### Step 1.3: Implement Native Wallet Support

**File**: `packages/hdwallet-native/src/[chainname].ts`

```typescript
import * as core from "@shapeshiftoss/hdwallet-core";
import { Isolation } from "./crypto";
import { [Chain]Adapter } from "./crypto/isolation/adapters/[chainname]";
import { NativeHDWalletBase } from "./native";

export function MixinNative[Chain]WalletInfo<TBase extends core.Constructor<core.HDWalletInfo>>(Base: TBase) {
  return class MixinNative[Chain]WalletInfo extends Base implements core.[Chain]WalletInfo {
    readonly _supports[Chain]Info = true;

    [chainLower]GetAccountPaths(msg: core.[Chain]GetAccountPaths): Array<core.[Chain]AccountPath> {
      return core.[chainLower]GetAccountPaths(msg);
    }

    [chainLower]NextAccountPath(msg: core.[Chain]AccountPath): core.[Chain]AccountPath | undefined {
      throw new Error("Method not implemented");
    }
  };
}

export function MixinNative[Chain]Wallet<TBase extends core.Constructor<NativeHDWalletBase>>(Base: TBase) {
  return class MixinNative[Chain]Wallet extends Base {
    readonly _supports[Chain] = true;

    [chainLower]Adapter: [Chain]Adapter | undefined;

    async [chainLower]InitializeWallet(masterKey: Isolation.Core.BIP32.Node): Promise<void> {
      const nodeAdapter = await Isolation.Adapters.BIP32.create(masterKey);
      this.[chainLower]Adapter = new [Chain]Adapter(nodeAdapter);
    }

    [chainLower]Wipe() {
      this.[chainLower]Adapter = undefined;
    }

    async [chainLower]GetAddress(msg: core.[Chain]GetAddress): Promise<string | null> {
      return this.needsMnemonic(!!this.[chainLower]Adapter, () => {
        return this.[chainLower]Adapter!.getAddress(msg.addressNList);
      });
    }

    async [chainLower]SignTx(msg: core.[Chain]SignTx): Promise<core.[Chain]SignedTx | null> {
      return this.needsMnemonic(!!this.[chainLower]Adapter, async () => {
        const address = await this.[chainLower]GetAddress({
          addressNList: msg.addressNList,
          showDisplay: false,
        });

        if (!address) throw new Error("Failed to get [ChainName] address");

        const signature = await this.[chainLower]Adapter!.signTransaction(
          msg.rawDataHex,
          msg.addressNList
        );

        return {
          serialized: msg.rawDataHex + signature,
          signature,
        };
      });
    }
  };
}
```

**Integrate into NativeHDWallet**:
```typescript
// In packages/hdwallet-native/src/native.ts
// Add mixin to class hierarchy
// Add initialization in initialize() method
// Add wipe in wipe() method
```

### Step 1.4: Create Crypto Adapter (Non-EVM only)

**File**: `packages/hdwallet-native/src/crypto/isolation/adapters/[chainname].ts`

Implement chain-specific cryptography:
- Address generation algorithm
- Transaction signing
- Any chain-specific encoding

Reference: See `tron.ts` adapter for a complete example

**Export adapter**:
```typescript
// In packages/hdwallet-native/src/crypto/isolation/adapters/index.ts
export * from './[chainname]'
```

### Step 1.5: Update Core Wallet Interface

**File**: `packages/hdwallet-core/src/wallet.ts`

Add support check function:
```typescript
export function supports[Chain](wallet: HDWallet): wallet is [Chain]Wallet {
  return !!(wallet as any)._supports[Chain]
}
```

### Step 1.6: Build & Verify

```bash
# Build hdwallet packages to verify
yarn hdwallet:build

# Run hdwallet tests
yarn hdwallet:test
```

No version bumps or publishing needed — hdwallet packages are workspace packages (`workspace:^`).

---

## Phase 2: Web Chain Adapter (Poor Man's Approach)

### Step 3.1: Add Chain Constants

**File**: `packages/caip/src/constants.ts`

```typescript
// Add chain ID constant
export const [chainLower]ChainId = '[caip19-format]' as const // e.g., 'eip155:1', 'tron:0x2b6653dc', etc.

// Add asset ID constant
export const [chainLower]AssetId = '[caip19-format]' as AssetId

// Add asset reference constant
export const ASSET_REFERENCE = {
  // ...
  [ChainName]: 'slip44:COINTYPE',
}

// Add to KnownChainIds enum
export enum KnownChainIds {
  // ...
  [ChainName]Mainnet = '[caip2-chain-id]',
}

// Add to asset namespace if needed (non-EVM chains)
export const ASSET_NAMESPACE = {
  // ...
  [tokenStandard]: '[namespace]', // e.g., trc20, suiCoin
}
```

**File**: `packages/types/src/base.ts`

```typescript
// Add to KnownChainIds enum (duplicate but required)
export enum KnownChainIds {
  // ...
  [ChainName]Mainnet = '[caip2-chain-id]',
}
```

**File**: `src/constants/chains.ts`

```typescript
// Add to second-class chains array
export const SECOND_CLASS_CHAINS = [
  // ...
  KnownChainIds.[ChainName]Mainnet,
]

// Add to feature-flag gated chains
```

### Step 3.2: Create Chain Adapter

**Directory**: `packages/chain-adapters/src/[adaptertype]/[chainname]/`

#### **For EVM Chains** (SIMPLE!)

Extend `SecondClassEvmAdapter` - you only need ~50 lines!

**File**: `packages/chain-adapters/src/evm/[chainname]/[ChainName]ChainAdapter.ts`

```typescript
import { ASSET_REFERENCE, [chainLower]AssetId } from '@shapeshiftoss/caip'
import type { AssetId } from '@shapeshiftoss/caip'
import type { RootBip44Params } from '@shapeshiftoss/types'
import { KnownChainIds } from '@shapeshiftoss/types'

import { ChainAdapterDisplayName } from '../../types'
import { SecondClassEvmAdapter } from '../SecondClassEvmAdapter'
import type { TokenInfo } from '../SecondClassEvmAdapter'

const SUPPORTED_CHAIN_IDS = [KnownChainIds.[ChainName]Mainnet]
const DEFAULT_CHAIN_ID = KnownChainIds.[ChainName]Mainnet

export type ChainAdapterArgs = {
  rpcUrl: string
  knownTokens?: TokenInfo[]
}

export const is[ChainName]ChainAdapter = (adapter: unknown): adapter is ChainAdapter => {
  return (adapter as ChainAdapter).getType() === KnownChainIds.[ChainName]Mainnet
}

export class ChainAdapter extends SecondClassEvmAdapter<KnownChainIds.[ChainName]Mainnet> {
  public static readonly rootBip44Params: RootBip44Params = {
    purpose: 44,
    coinType: Number(ASSET_REFERENCE.[ChainName]),
    accountNumber: 0,
  }

  constructor(args: ChainAdapterArgs) {
    super({
      assetId: [chainLower]AssetId,
      chainId: DEFAULT_CHAIN_ID,
      rootBip44Params: ChainAdapter.rootBip44Params,
      supportedChainIds: SUPPORTED_CHAIN_IDS,
      rpcUrl: args.rpcUrl,
      knownTokens: args.knownTokens ?? [],
    })
  }

  getDisplayName() {
    return ChainAdapterDisplayName.[ChainName]
  }

  getName() {
    return '[ChainName]'
  }

  getType(): KnownChainIds.[ChainName]Mainnet {
    return KnownChainIds.[ChainName]Mainnet
  }

  getFeeAssetId(): AssetId {
    return this.assetId
  }
}

export type { TokenInfo }
```

**That's it!** SecondClassEvmAdapter automatically provides:
- ✅ Account balance fetching (native + ERC-20 tokens via multicall)
- ✅ Fee estimation
- ✅ Transaction broadcasting
- ✅ Transaction parsing with ERC-20 event decoding (for execution price)
- ✅ Rate limiting via PQueue
- ✅ Multicall batching for token balances

Just follow the pattern from HyperEVM, Monad, or Plasma adapters.

#### **For Non-EVM Chains** (COMPLEX)

Implement `IChainAdapter` interface - requires custom crypto adapters and ~500-1000 lines.

**Key Methods to Implement:**
- `getAccount()` - Get balances (native + tokens)
- `getAddress()` - Derive address from wallet
- `getFeeData()` - Estimate transaction fees
- `broadcastTransaction()` - Submit signed tx to network
- `buildSendApiTransaction()` - Build unsigned tx
- `signTransaction()` - Sign with wallet
- `parseTx()` - Parse transaction (can stub out)
- `getTxHistory()` - Get tx history (stub out - return empty)

**Poor Man's Patterns:**
1. **No Unchained**: Use public RPC directly (@mysten/sui, tronweb, etc.)
2. **No TX History**: Stub out `getTxHistory()` to return empty array
3. **Direct RPC Polling**: Use chain-specific RPC for tx status

**File**: `packages/chain-adapters/src/[chainname]/[ChainName]ChainAdapter.ts`

See `SuiChainAdapter.ts` or `TronChainAdapter.ts` for complete examples.

**Export**:
```typescript
// In packages/chain-adapters/src/[adaptertype]/[chainname]/index.ts
export * from './[ChainName]ChainAdapter'
export * from './types'

// In packages/chain-adapters/src/[adaptertype]/index.ts
export * as [chainLower] from './[chainname]'

// In packages/chain-adapters/src/index.ts
export * from './[adaptertype]'
```

### Step 3.2a: Implement parseTx (Iterative Approach)

**CRITICAL**: The `parseTx()` method parses transaction data after broadcast. This determines:
- Whether the transaction shows in history (if applicable)
- Execution price calculation for swaps
- Transfer display (from/to/value)

**Reference Implementations** (use these as patterns):
- **EVM chains**: `SecondClassEvmAdapter.parseTx()` - handles ERC-20 Transfer events automatically
- **Sui**: `SuiChainAdapter.parseTx()` - parses SUI native and coin transfers
- **Tron**: `TronChainAdapter.parseTx()` - parses TRC-20 transfers
- **NEAR**: `NearChainAdapter.parseTx()` + `parseNep141Transfers()` - parses NEP-141 token logs

**Iterative Development Flow**:

1. **Start with naive implementation** - Parse native asset transfers only:
```typescript
async parseTx(txHash: string, pubkey: string): Promise<Transaction> {
  const result = await this.rpcCall('getTransaction', [txHash])

  // Basic structure
  const status = result.success ? TxStatus.Confirmed : TxStatus.Failed
  const fee = { assetId: this.assetId, value: result.fee.toString() }

  const transfers: Transfer[] = []

  // Parse native transfers (naive - just native asset)
  if (result.value) {
    transfers.push({
      assetId: this.assetId,
      from: [result.from],
      to: [result.to],
      type: result.from === pubkey ? TransferType.Send : TransferType.Receive,
      value: result.value.toString(),
    })
  }

  return { txid: txHash, status, fee, transfers, /* ... */ }
}
```

2. **User testing reveals issues** - User tests sends/swaps and reports:
   - "Native send works but tokens don't show"
   - "Swap execution price is wrong"
   - Provides RPC response from debugger

3. **Refine with actual RPC response** - User provides debugger scope:
```typescript
// Example: User provides RPC response showing token events in logs
// You then add token parsing logic based on actual data structure

private parseTokenTransfers(result: RpcResult, pubkey: string): Transfer[] {
  const transfers: Transfer[] = []

  // Parse token events from logs/events
  for (const event of result.events || []) {
    if (event.type === 'token_transfer') {
      // Token-specific parsing based on actual RPC structure
    }
  }

  return transfers
}
```

**Key considerations for parseTx**:

| Aspect | Native Asset | Tokens | Internal Transfers |
|--------|--------------|--------|-------------------|
| Where to find | Transaction value field | Event logs / receipts | Nested calls / traces |
| Asset ID | `this.assetId` | `chainId/namespace:contractAddress` | Varies |
| pubkey comparison | Usually sender field | Event old_owner/new_owner | May be nested |

**Common patterns by chain type**:

**EVM Chains** (SecondClassEvmAdapter handles automatically):
- Native: `tx.value`
- Tokens: ERC-20 Transfer events in logs
- Uses `ethers.Interface.parseLog()` to decode events

**Non-EVM Chains** (must implement manually):

```typescript
// NEAR pattern - EVENT_JSON logs
for (const log of receipt.outcome.logs) {
  if (!log.startsWith('EVENT_JSON:')) continue
  const event = JSON.parse(log.slice('EVENT_JSON:'.length))
  if (event.standard === 'nep141' && event.event === 'ft_transfer') {
    // Parse transfer from event.data
  }
}

// Sui pattern - coin type from object changes
for (const change of result.objectChanges) {
  if (change.type === 'mutated' && change.objectType.includes('::coin::Coin<')) {
    // Extract coin type and amount
  }
}

// Tron pattern - TRC20 logs
for (const log of result.log || []) {
  if (log.topics[0] === TRC20_TRANSFER_TOPIC) {
    // Decode TRC20 transfer
  }
}
```

**pubkey vs account ID gotcha**:
- Some chains pass `pubkey` as hex public key
- But logs/events use account addresses (e.g., `alice.near`, base58, etc.)
- May need to convert: `const accountId = pubKeyToAddress(pubkey)`

**When to ask user for debugger scope**:
- Initial naive implementation doesn't catch tokens
- Swap execution prices are wrong
- Internal transfers missing

**Example request to user**:
> "The parseTx implementation needs refinement for token transfers. Can you:
> 1. Make a token send/swap
> 2. Set a breakpoint in parseTx()
> 3. Share the `result` variable from the RPC response
> This will help me see the actual data structure for token events."

### Step 3.3: Add Utility Functions

**File**: `packages/utils/src/getAssetNamespaceFromChainId.ts`

```typescript
case [chainLower]ChainId:
  return ASSET_NAMESPACE.[tokenStandard]
```

**File**: `packages/utils/src/getChainShortName.ts`

```typescript
case KnownChainIds.[ChainName]Mainnet:
  return '[SHORT]'
```

**File**: `packages/utils/src/getNativeFeeAssetReference.ts`

```typescript
case KnownChainIds.[ChainName]Mainnet:
  return ASSET_REFERENCE.[ChainName]
```

**File**: `packages/utils/src/chainIdToFeeAssetId.ts`

```typescript
[chainLower]ChainId: [chainLower]AssetId,
```

**File**: `packages/utils/src/assetData/baseAssets.ts`

```typescript
// Add base asset
export const [chainLower]BaseAsset: Asset = {
  assetId: [chainLower]AssetId,
  chainId: [chainLower]ChainId,
  name: '[ChainName]',
  symbol: '[SYMBOL]',
  precision: [DECIMALS],
  icon: '[iconUrl]',
  explorer: '[explorerUrl]',
  // ... other fields
}
```

**File**: `packages/utils/src/assetData/getBaseAsset.ts`

```typescript
case [chainLower]ChainId:
  return [chainLower]BaseAsset
```

### Step 3.4: Create Chain Utils (Transaction Status)

**File**: `src/lib/utils/[chainname].ts`

```typescript
import { [chainLower]ChainId } from '@shapeshiftoss/caip'
import type { ChainAdapter } from '@shapeshiftoss/chain-adapters'
import { assertUnreachable } from '@/lib/utils'
import type { TxStatus } from '@/state/slices/txHistorySlice/txHistorySlice'

export const is[Chain]ChainAdapter = (adapter: unknown): adapter is [ChainAdapter] => {
  return (adapter as ChainAdapter).getChainId() === [chainLower]ChainId
}

export const assertGet[Chain]ChainAdapter = (
  adapter: ChainAdapter,
): asserts adapter is [ChainAdapter] => {
  if (!is[Chain]ChainAdapter(adapter)) {
    throw new Error('[ChainName] adapter required')
  }
}

// Implement getTxStatus using chain-specific RPC calls
export const get[Chain]TransactionStatus = async (
  txHash: string,
  adapter: [ChainAdapter],
): Promise<TxStatus> => {
  // Use chain client to check transaction status
  // Return 'confirmed', 'failed', or 'unknown'
  // See monad.ts / sui.ts for examples
}
```

### Step 3.5: Wire Up Transaction Status Polling

**File**: `src/hooks/useActionCenterSubscribers/useSendActionSubscriber.tsx`

Add case for your chain:
```typescript
case KnownChainIds.[ChainName]Mainnet:
  txStatus = await get[Chain]TransactionStatus(txHash, adapter)
  break
```

### Step 3.6: Add Account Derivation

**File**: `src/lib/account/[chainname].ts`

```typescript
import { [chainLower]ChainId, toAccountId } from '@shapeshiftoss/caip'
import type { AccountMetadata, AccountMetadataByAccountId } from '@shapeshiftoss/types'
import { KnownChainIds } from '@shapeshiftoss/types'
import { assertGet[Chain]ChainAdapter, is[Chain]ChainAdapter } from '@/lib/utils/[chainname]'

export const derive[Chain]AccountIdsAndMetadata = async (
  args: // standard args
): Promise<AccountMetadataByAccountId> => {
  const { accountNumber, chainIds, wallet } = args

  const adapter = adapterManager.get([chainLower]ChainId)
  if (!adapter) throw new Error('[ChainName] adapter not available')
  assertGet[Chain]ChainAdapter(adapter)

  const address = await adapter.getAddress({
    wallet,
    accountNumber,
  })

  const accountId = toAccountId({ chainId: [chainLower]ChainId, account: address })
  const account = await adapter.getAccount(address)

  const metadata: AccountMetadata = {
    accountType: 'native',
    bip44Params: adapter.getBip44Params({ accountNumber }),
  }

  return {
    [accountId]: metadata,
  }
}
```

**Wire into account dispatcher**:
```typescript
// In src/lib/account/account.ts
case KnownChainIds.[ChainName]Mainnet:
  return derive[Chain]AccountIdsAndMetadata(args)
```

### Step 3.7: Add Wallet Support Detection

**File**: `src/hooks/useWalletSupportsChain/useWalletSupportsChain.ts`

```typescript
// Add to switch statement
case KnownChainIds.[ChainName]Mainnet:
  return supports[Chain](wallet) // from hdwallet-core
```

### Step 3.8: Add Asset Support Detection (CRITICAL!)

**IMPORTANT**: This was missing for recent chains (Tron, SUI, Monad, HyperEVM, Plasma) and caused assets not to show up properly!

**File**: `src/state/slices/portfolioSlice/utils/index.ts`

Add your chain to the `isAssetSupportedByWallet` function around line 367:

```typescript
// 1. Import your chain ID at the top
import {
  // ... existing imports
  [chainLower]ChainId,
} from '@shapeshiftoss/caip'

// 2. Import the support function from hdwallet-core
import {
  // ... existing imports
  supports[ChainName],
} from '@shapeshiftoss/hdwallet-core'

// 3. Add case to the switch statement in isAssetSupportedByWallet
export const isAssetSupportedByWallet = (assetId: AssetId, wallet: HDWallet): boolean => {
  if (!assetId) return false
  const { chainId } = fromAssetId(assetId)
  switch (chainId) {
    // ... existing cases
    case [chainLower]ChainId:
      return supports[ChainName](wallet)
    // ... rest of cases
    default:
      return false
  }
}
```

**Why this matters**: This function determines if a wallet can use a particular asset. Without it, assets for your chain won't appear in wallet UIs even if everything else is configured correctly!

**Example**: For HyperEVM, add:
```typescript
case hyperEvmChainId:
  return supportsHyperEvm(wallet)
```

---

## Phase 4: Web Plugin & Feature Flags

### Step 4.1: Create Plugin

**File**: `src/plugins/[chainname]/index.tsx`

```typescript
import { [chainLower]ChainId } from '@shapeshiftoss/caip'
import { [chainLower] } from '@shapeshiftoss/chain-adapters'
import { KnownChainIds } from '@shapeshiftoss/types'
import { getConfig } from '@/config'
import type { Plugins } from '@/plugins/types'

export default function register(): Plugins {
  return [
    [
      '[chainLower]ChainAdapter',
      {
        name: '[chainLower]ChainAdapter',
        featureFlag: ['[ChainName]'],
        providers: {
          chainAdapters: [
            [
              KnownChainIds.[ChainName]Mainnet,
              () => {
                return new [chainLower].ChainAdapter({
                  rpcUrl: getConfig().VITE_[CHAIN]_NODE_URL,
                  // Add other config as needed
                })
              },
            ],
          ],
        },
      },
    ],
  ]
}
```

**Register plugin**:
```typescript
// In src/plugins/activePlugins.ts
import [chainLower] from './[chainname]'

export const activePlugins = [
  // ...
  [chainLower],
]
```

**Gate in provider**:
```typescript
// In src/context/PluginProvider/PluginProvider.tsx
// Add feature flag check for your chain
```

### Step 4.2: Environment Variables

**File**: `.env`

```bash
VITE_[CHAIN]_NODE_URL=[default-public-rpc]
VITE_FEATURE_[CHAIN]=false
```

**File**: `.env.development`

```bash
VITE_[CHAIN]_NODE_URL=[dev-rpc]
VITE_FEATURE_[CHAIN]=true
```

**File**: `.env.production`

```bash
VITE_[CHAIN]_NODE_URL=[prod-rpc]
VITE_FEATURE_[CHAIN]=false
```

### Step 4.3: Config Validation

**File**: `src/config.ts`

```typescript
const validators = {
  // ...
  VITE_[CHAIN]_NODE_URL: url(),
  VITE_FEATURE_[CHAIN]: bool({ default: false }),
}
```

### Step 4.4: Feature Flag State

**File**: `src/state/slices/preferencesSlice/preferencesSlice.ts`

```typescript
export type FeatureFlags = {
  // ...
  [ChainName]: boolean
}

const initialState: PreferencesState = {
  featureFlags: {
    // ...
    [ChainName]: getConfig().VITE_FEATURE_[CHAIN],
  },
}
```

**Add to test mocks**:
```typescript
// In src/test/mocks/store.ts
featureFlags: {
  // ...
  [ChainName]: false,
}
```

### Step 4.5: CSP Headers

**File**: `headers/csps/chains/[chainname].ts`

```typescript
const [chainLower]: Csp = {
  'connect-src': [env.VITE_[CHAIN]_NODE_URL],
}

export default [chainLower]
```

**Register CSP**:
```typescript
// In headers/csps/index.ts
import [chainLower] from './chains/[chainname]'

export default [
  // ...
  [chainLower],
]
```

---

## Phase 5: Asset Generation

### Step 5.1: CoinGecko Adapter Integration

**CRITICAL**: This step is required for asset discovery and pricing! See PR #11257 for Monad example.

**File**: `packages/caip/src/adapters/coingecko/index.ts`

Add your chain to the CoingeckoAssetPlatform enum and import the chain ID:

```typescript
// Add import at top
import {
  // ... existing imports
  [chainLower]ChainId,
} from '../../constants'

// Add platform constant
export enum CoingeckoAssetPlatform {
  // ... existing platforms
  [ChainName] = '[coingecko-platform-id]', // e.g., 'hyperevm' for HyperEVM
}
```

**File**: `packages/caip/src/adapters/coingecko/utils.ts`

Add chain ID to platform mapping in the `chainIdToCoingeckoAssetPlatform` function:

```typescript
// For EVM chains, add to the EVM switch statement
case CHAIN_REFERENCE.[ChainName]Mainnet:
  return CoingeckoAssetPlatform.[ChainName]

// For non-EVM chains, add separate case in outer switch
```

**File**: `packages/caip/src/adapters/coingecko/utils.test.ts`

Add test case for your chain:

```typescript
it('returns correct platform for [ChainName]', () => {
  expect(chainIdToCoingeckoAssetPlatform([chainLower]ChainId)).toEqual(
    CoingeckoAssetPlatform.[ChainName]
  )
})
```

**File**: `packages/caip/src/adapters/coingecko/index.test.ts`

Add test asset for your chain:

```typescript
// Add example asset from your chain to test fixtures
const [chainLower]UsdcAssetId: AssetId = 'eip155:[CHAIN_ID]/erc20:[USDC_ADDRESS]'

// Update test expectations to include your chain's asset
```

### Step 5.2: Create Asset Generator

**File**: `scripts/generateAssetData/[chainname]/index.ts`

Follow the pattern from monad/tron/sui:

```typescript
import { [chainLower]ChainId } from '@shapeshiftoss/caip'
import type { Asset } from '@shapeshiftoss/types'
import { [chainLower], unfreeze } from '@shapeshiftoss/utils'

import * as coingecko from '../coingecko'

export const getAssets = async (): Promise<Asset[]> => {
  const assets = await coingecko.getAssets([chainLower]ChainId)

  return [...assets, unfreeze([chainLower])]
}
```

**Wire into generator**:

1. **Import** in `scripts/generateAssetData/generateAssetData.ts`:
```typescript
import * as [chainLower] from './[chainname]'
```

2. **Fetch assets** in the `generateAssetData()` function:
```typescript
const [chainLower]Assets = await [chainLower].getAssets()
```

3. **Add to unfilteredAssetData array**:
```typescript
  ...[chainLower]Assets,
```

**Add chain to CoinGecko script**:

**File**: `scripts/generateAssetData/coingecko.ts`

Import your chain:
```typescript
import {
  // ... existing imports
  [chainLower]ChainId,
} from '@shapeshiftoss/caip'

import {
  // ... existing imports
  [chainLower],
} from '@shapeshiftoss/utils'
```

Add case in the switch statement (around line 133+):
```typescript
case [chainLower]ChainId:
  return {
    assetNamespace: ASSET_NAMESPACE.erc20, // or trc20, suiCoin, etc.
    category: adapters.chainIdToCoingeckoAssetPlatform(chainId),
    explorer: [chainLower].explorer,
    explorerAddressLink: [chainLower].explorerAddressLink,
    explorerTxLink: [chainLower].explorerTxLink,
  }
```

### Step 5.3: Swapper Support Discovery & Integration

**CRITICAL**: Add your chain to supported swappers so users can actually trade!

#### Step 5.3a: Research Which Swappers Support Your Chain

**Use `AskUserQuestion` to ask:**

**Question**: Which swappers support [ChainName]?

**Options**:
1. "I know which swappers" → User provides list
2. "Can you research it?" → Search swapper docs and supported chains lists
3. "Just add Relay for now" → Start with Relay, add others later

**Context**: Different swappers support different chains. We need to add your chain to each swapper that supports it.

**Search for swapper support:**
1. **Relay**: Check <https://docs.relay.link/resources/supported-chains>
2. **0x/Matcha**: Check <https://0x.org/docs/introduction/0x-cheat-sheet>
3. **OneInch**: Check <https://docs.1inch.io/docs/aggregation-protocol/introduction>
4. **CowSwap**: Check <https://docs.cow.fi/cow-protocol/reference/contracts/deployments>
5. **Jupiter**: Solana-only
6. **THORChain**: Check <https://docs.thorchain.org/chain-clients/overview>

**Common patterns:**
- Most EVM chains: Relay, 0x, possibly OneInch
- Ethereum L2s: Relay, 0x, CowSwap, OneInch
- Non-EVM: Relay (if supported), chain-specific DEXes

#### Step 5.3b: Relay Swapper Integration (Most Common)

**For Relay Swapper** (supports most chains):

**IMPORTANT - Check viem chain definitions first:**

1. **Search viem's chain definitions**: Check if your chain exists in viem:
   - Browse: <https://github.com/wevm/viem/tree/main/src/chains/definitions>
   - Look for `[chainname].ts` file (e.g., `hyperEvm.ts` for HyperEVM)
   - Note the exact export name (may differ from chain name, e.g., `hyperEvm` not `hyperliquid`)

2. **Update viem if needed**: For new/recent chains, update viem to latest version first:
   ```bash
   # Check current version
   yarn why viem

   # Update to latest pinned version
   yarn up viem@latest

   # Rebuild packages
   yarn build:packages
   ```

3. **Only define manually if unavailable**: If the chain doesn't exist in viem, use `defineChain()` pattern (see viem docs)

**File**: `packages/swapper/src/swappers/RelaySwapper/constant.ts`

Add your chain to the Relay chain ID mapping:

```typescript
import {
  // ... existing imports
  [chainLower]ChainId,
} from '@shapeshiftoss/caip'

// Add to viem chain imports if EVM (check viem/chains for exact export name!)
import {
  // ... existing chains
  [chainLower], // e.g., hyperEvm from viem/chains (note: hyperEvm not hyperliquid!)
} from 'viem/chains'

export const chainIdToRelayChainId = {
  // ... existing mappings
  [[chainLower]ChainId]: [chainLower].id, // For EVM chains using viem
  // OR
  [[chainLower]ChainId]: [RELAY_CHAIN_ID], // For non-EVM (get from Relay docs)
}
```

**File**: `packages/swapper/src/swappers/RelaySwapper/utils/relayTokenToAssetId.ts`

Add native asset case in the `relayTokenToAssetId` function:

```typescript
// Add to the switch statement for native assets (around line 100+)
case CHAIN_REFERENCE.[ChainName]Mainnet:
  return {
    assetReference: ASSET_REFERENCE.[ChainName],
    assetNamespace: ASSET_NAMESPACE.slip44,
  }
```

**IMPORTANT**: Make sure ALL chains that are in the `chainIdToRelayChainId` mapping in `constant.ts` have a corresponding case in the switch statement in `relayTokenToAssetId.ts`. Missing cases will cause runtime errors like `chainId 'XX' not supported`.

**Check Relay docs** for your chain:
- <https://docs.relay.link/resources/supported-chains>
- Verify chain ID and native token address

### Step 5.4: Generate Assets (Step-by-Step Approach)

**IMPORTANT**: Asset generation requires a Zerion API key for related asset indexing.

**Ask user for Zerion API key** using `AskUserQuestion`:

**Question**: Do you have a Zerion API key to run asset generation?

**Options**:
1. "Yes, here it is" → User provides key (NEVER store in VCS!)
2. "No, skip for now" → Skip asset generation, user can run manually later

**Context**: Asset generation fetches token metadata and requires a Zerion API key.
The key is passed via environment variable and should NEVER be committed to VCS.

**Ask user how they want to run generation** using `AskUserQuestion`:

**Question**: How do you want to run the asset generation pipeline?

**Options**:
1. "I'll run it myself" → Copy command to clipboard (echo | pbcopy), user runs it, better visibility of progress
2. "Claude runs it" → Claude runs all steps in background. ⚠️ WARNING: May take 5-10 minutes with limited visibility. You'll see less progress output.

**Context**: Asset generation has 5 steps (caip-adapters, color-map, asset-data, tradable-asset-map, thor-longtail).
Running manually gives full visibility of progress (you'll see "chain_id: hyperevm" tokens being processed).
Claude running it is hands-off but you won't see detailed progress, and it may appear stuck for several minutes while processing thousands of tokens.

**Run generation scripts ONE AT A TIME** (better visibility than `generate:all`):

```bash
# Step 1: Generate CoinGecko CAIP adapters (JSON mappings from our code)
yarn generate:caip-adapters
# ✓ Generates packages/caip/src/adapters/coingecko/generated/eip155_999/adapter.json
# ✓ Takes ~10 seconds

# Step 2: Generate color map (picks up new assets)
yarn generate:color-map
# ✓ Updates scripts/generateAssetData/color-map.json
# ✓ Takes ~5 seconds

# Step 3: Generate asset data (fetches tokens from CoinGecko)
ZERION_API_KEY=<user-provided-key> yarn generate:asset-data
# ✓ Fetches all HyperEVM ERC20 tokens from CoinGecko platform 'hyperevm'
# ✓ Updates src/assets/generated/
# ✓ Takes 2-5 minutes - YOU SHOULD SEE:
#   - "Total Portals tokens fetched for ethereum: XXXX"
#   - "Total Portals tokens fetched for base: XXXX"
#   - "chain_id": "hyperevm" appearing in output (means HyperEVM tokens found!)
#   - "Generated CoinGecko AssetId adapter data."
#   - "Asset data generated successfully"

# Step 4: Generate tradable asset map (for swapper support)
yarn generate:tradable-asset-map
# ✓ Generates src/lib/swapper/constants.ts mappings
# ✓ Takes ~10 seconds

# Step 5: Generate Thor longtail tokens (Thor-specific, optional for most chains)
yarn generate:thor-longtail-tokens
# ✓ Updates Thor longtail token list
# ✓ Takes ~5 seconds
```

**Why step-by-step is better than `generate:all`**:
- ✅ See exactly which step is running
- ✅ Catch errors immediately
- ✅ See progress output (like "chain_id": "hyperevm" tokens being processed)
- ✅ Can skip irrelevant steps (e.g., thor-longtail for non-Thor chains)

**Commit generated assets**:
```bash
git add src/assets/generated/ packages/caip/src/adapters/coingecko/generated/ scripts/generateAssetData/color-map.json
git commit -m "feat: generate [chainname] assets and mappings"
```

**⚠️ CRITICAL**: NEVER commit the Zerion API key. Only use it in the command line.

### Step 5.4: Research & Add Swapper Support

**IMPORTANT**: After assets are generated, check which swappers support your new chain!

#### Step 5.4a: Ask User About Swapper Support

Use `AskUserQuestion` to determine swapper support:

```
Which swappers support [ChainName]?

Options:
1. "I know which swappers support it" → User provides list
2. "Research it for me" → AI will search swapper docs
3. "Skip for now" → Can add swapper support later

Context: Different DEX aggregators support different chains. We need to add your chain to each swapper that supports it so users can trade.
```

#### Step 5.4b: Research Common Swapper Support (if needed)

If user chooses "Research it for me", check these sources:

**Relay** (most common, supports most chains):
- Docs: https://docs.relay.link/resources/supported-chains
- Usually supports: Ethereum, Base, Arbitrum, Optimism, Polygon, Avalanche, BSC, Gnosis, and many new EVM chains
- Check if your chain's viem chain definition exists (e.g., `plasma` from 'viem/chains')

**Other swappers to check**:
- **0x/Matcha**: https://0x.org/docs/introduction/0x-cheat-sheet
- **CowSwap**: https://docs.cow.fi/cow-protocol/reference/contracts/deployments
- **Jupiter**: Solana-only
- **THORChain**: Check https://docs.thorchain.org/chain-clients/overview
- **ChainFlip**: Check supported chains in their docs

#### Step 5.4c: Add Relay Swapper Support (Most Common)

If Relay supports your chain:

**File**: `packages/swapper/src/swappers/RelaySwapper/constant.ts`

```typescript
// 1. Add imports
import {
  // ... existing imports
  plasmaChainId,
} from '@shapeshiftoss/caip'

import {
  // ... existing chains
  plasma,  // Check if viem/chains exports your chain
} from 'viem/chains'

// 2. Add to chainIdToRelayChainId mapping
export const chainIdToRelayChainId = {
  // ... existing mappings
  [plasmaChainId]: plasma.id,  // Uses viem chain ID
}
```

**File**: `packages/swapper/src/swappers/RelaySwapper/utils/relayTokenToAssetId.ts`

```typescript
// Add native asset case in switch statement (around line 124):
case CHAIN_REFERENCE.PlasmaMainnet:
  return {
    assetReference: ASSET_REFERENCE.Plasma,
    assetNamespace: ASSET_NAMESPACE.slip44,
  }
```

#### Step 5.4d: Add Other Swapper Support (As Needed)

Follow similar patterns for other swappers (CowSwap, 0x, etc.) - see `swapper-integration` skill for detailed guidance.

**Reference**: Plasma added to Relay swapper for swap support

### Step 5.5: Add Native Asset to Popular Assets

**CRITICAL**: Second-class citizen chains are not in CoinGecko's top 100 by market cap, so they won't appear in the popular assets list by default. This causes the native asset to be missing when users filter by that chain.

**File**: `src/components/TradeAssetSearch/hooks/useGetPopularAssetsQuery.tsx`

```typescript
// Add import at the top
import {
  hyperEvmAssetId,
  mayachainAssetId,
  monadAssetId,
  plasmaAssetId,  // example for Plasma
  [chainLower]AssetId,  // Add your chain's asset ID
  thorchainAssetId,
  tronAssetId,
  suiAssetId,
} from '@shapeshiftoss/caip'

// Add to the queryFn, after the mayachain check (around line 37)
// add second-class citizen chains to popular assets for discoverability
if (enabledFlags.HyperEvm) assetIds.push(hyperEvmAssetId)
if (enabledFlags.Monad) assetIds.push(monadAssetId)
if (enabledFlags.Plasma) assetIds.push(plasmaAssetId)
if (enabledFlags.[ChainName]) assetIds.push([chainLower]AssetId)  // Add your chain
if (enabledFlags.Tron) assetIds.push(tronAssetId)
if (enabledFlags.Sui) assetIds.push(suiAssetId)
```

**Why this is needed:**
- Popular assets are fetched from CoinGecko's top 100 by market cap
- New/small chains aren't in the top 100
- Without this, when filtering by your chain, only tokens appear (via relatedAssetIds)
- The native asset won't show up, which is confusing for users
- Example: Searching "monad" in MetaMask (doesn't support Monad) shows Monad tokens but not MON itself

**Reference PRs:**
- See how Monad, Tron, Sui, Plasma, and HyperEVM were added in the same PR

---

## Phase 6: Ledger Support (Optional)

**Only if chain is supported by Ledger hardware**

### Step 6.1: Check Ledger Support

1. Visit https://www.ledger.com/supported-crypto-assets
2. Search for your chain
3. Note the Ledger app name

**For EVM chains**: Automatically supported via Ethereum app
**For non-EVM**: Needs chain-specific Ledger app

### Step 6.2: Add Ledger Support in HDWallet

**File**: `packages/hdwallet-ledger/src/ledger.ts`

Add chain support following existing patterns.

**For EVM**: Just add to supported chains list
**For non-EVM**: Implement chain-specific Ledger transport

### Step 6.3: Add to Web Ledger Constants

**File**: `src/context/WalletProvider/Ledger/constants.ts`

```typescript
import { [chainLower]AssetId } from '@shapeshiftoss/caip'

export const availableLedgerAppAssetIds = [
  // ...
  [chainLower]AssetId,
]
```

### Step 6.4: Test Ledger Integration

1. Connect Ledger device
2. Open chain-specific app
3. Test address derivation
4. Test transaction signing

---

## Phase 7: Testing & Validation

### Step 7.1: Type Check

```bash
yarn type-check

# Fix any TypeScript errors
```

### Step 7.2: Lint

```bash
yarn lint --fix
```

### Step 7.3: Build

```bash
yarn build

# Verify no build errors
# Check bundle size didn't explode
```

### Step 7.4: Manual Testing Checklist

- [ ] Connect native wallet
- [ ] Derive account address
- [ ] View account balance
- [ ] Send native asset
- [ ] View transaction status
- [ ] Check balance updates after send
- [ ] Test swap TO chain from another chain
- [ ] Test swap FROM chain to another chain
- [ ] Verify error handling (insufficient balance, network errors, etc.)

If Ledger supported:
- [ ] Connect Ledger
- [ ] Open chain app
- [ ] Derive address
- [ ] Sign transaction
- [ ] Broadcast transaction

---

## Phase 8: Clean Up & Commit

### Step 8.1: Create Feature Commits

Everything is in the same monorepo now — hdwallet packages are workspace packages under `packages/hdwallet-*`.

```bash
# Commit everything together
git add -A
git commit -m "feat: implement [chainname]

- Add [ChainName] hdwallet core interfaces and native wallet support
- Add [ChainName] chain adapter with poor man's RPC
- Support native asset sends/receives
- Add account derivation
- Add feature flag VITE_FEATURE_[CHAIN]
- Add asset generation for [chain] from CoinGecko
- Wire transaction status polling
- Add [chain] plugin with feature flag gating

Behind feature flag for now."
```

### Step 8.2: Open PR

```bash
git push origin HEAD

# Open PR to develop
gh pr create --title "feat: implement [chainname]" \
  --body "Adds basic [ChainName] support as second-class citizen..."
```

---

## Phase 9: Common Gotchas & Troubleshooting

### Gotcha 1: Token Precision Issues

**Problem**: Token balances display incorrectly
**Solution**: Verify decimals/precision match chain metadata
**Example**: Tron TRC20 tokens hardcoded precision caused display issues (#11222)

### Gotcha 2: Address Validation

**Problem**: Invalid addresses accepted or valid ones rejected
**Solution**: Use chain-specific validation (checksumming for EVM, base58 for Tron, etc.)
**Example**: Tron address parsing issues (#11229)

### Gotcha 3: Transaction Broadcasting

**Problem**: Signed transactions fail to broadcast
**Solution**: Check serialization format matches chain expectations
**Example**: Ensure proper hex encoding, network byte for Tron, etc.

### Gotcha 4: Bundle Size

**Problem**: Build size explodes after adding chain SDK
**Solution**: Extract large dependencies to separate chunk
**Example**: Sui SDK needed code splitting (#11238 comments)

### Gotcha 5: Minimum Trade Amounts

**Problem**: Small swaps fail without clear error
**Solution**: Add minimum amount validation in swapper
**Example**: Tron tokens need minimum amounts (#11253)

### Gotcha 6: Token Grouping

**Problem**: Tokens don't group with related assets in UI
**Solution**: Check asset namespace and ID generation
**Example**: Tron/Sui tokens grouping issues (#11252)

### Gotcha 7: Ledger App Mismatch

**Problem**: Ledger transactions fail with unclear error
**Solution**: Verify correct Ledger app is mapped
**Example**: Use Ethereum app for EVM chains, not chain-specific app

### Gotcha 8: Missing walletSupportsChain Case (CRITICAL - BLOCKS ACCOUNT DISCOVERY!)

**Problem**: Assets appear but no accounts are derived/discovered for the chain
**Symptoms**:
- Chain adapter is registered
- Assets show up in asset list
- But wallet shows no accounts for the chain
- Logs show account derivation never runs for chainId
**Root Cause**: Missing case in `walletSupportsChain()` switch statement
**Solution**: Add your chain to the switch statement in `src/hooks/useWalletSupportsChain/useWalletSupportsChain.ts`:
```typescript
// 1. Import chain ID
import { [chainLower]ChainId } from '@shapeshiftoss/caip'

// 2. Import support function from hdwallet-core
import { supports[ChainName] } from '@shapeshiftoss/hdwallet-core'

// 3. Add to switch statement (around line 186+)
case [chainLower]ChainId:
  return supports[ChainName](wallet)
```
**Example**: HyperEVM was missing this - caused account discovery to skip it entirely
**Why it matters**: `useDiscoverAccounts` filters chains using `walletSupportsChain()`. If it returns false, the chain is never passed to `deriveAccountIdsAndMetadata()` → no accounts!
**Reference**: Same issue as Plasma PR #11361 but for wallet support instead of feature flag

### Gotcha 9: Feature Flag Not Working

**Problem**: Chain doesn't appear even with flag enabled
**Solution**: Check ALL places flags are checked:
- Plugin registration (featureFlag array)
- PluginProvider gating (add chainId filter)
- Asset service filtering
- Constants array (SECOND_CLASS_CHAINS)

### Gotcha 10: Balance Updates

**Problem**: Balances don't update after transactions
**Solution**: Implement polling in tx status subscriber
**Example**: Add chain case in useSendActionSubscriber

### Gotcha 11: RPC Rate Limiting

**Problem**: Requests fail intermittently
**Solution**: Add retry logic, use multiple RPC endpoints
**Example**: Implement fallback RPC URLs

### Gotcha 12: Missing CoinGecko Script Case

**Problem**: `yarn generate:asset-data` fails with "no coingecko token support for chainId"
**Solution**: Add your chain case to `scripts/generateAssetData/coingecko.ts`
**Files to update**:
- Import `[chainLower]ChainId` from caip
- Import `[chainLower]` base asset from utils
- Add case in switch statement with assetNamespace, category, explorer links
**Example**: See HyperEVM case (line ~143) for pattern

### Gotcha 13: Zerion API Key Required

**Problem**: Asset generation fails with "Missing Zerion API key"
**Solution**: Get key from user via `AskUserQuestion`, pass as env var
**Command**: `ZERION_API_KEY=<key> yarn generate:all`
**CRITICAL**: NEVER commit the Zerion API key to VCS!
**Example**: Always pass key via command line only

### Gotcha 14: AssetService Missing Feature Flag Filter

**Problem**: Assets for your chain appear even when feature flag is disabled
**Solution**: Add feature flag filter to AssetService
**File**: `src/lib/asset-service/service/AssetService.ts`
**Code**: `if (!config.VITE_FEATURE_[CHAIN] && asset.chainId === [chainLower]ChainId) return false`
**Example**: See line ~53 for Monad/Tron/Sui pattern
**Reference**: Fixed in PR #11241 (Monad) - was initially forgotten

### Gotcha 15: Missing from evmChainIds Array (EVM Chains Only)

**Problem**: TypeScript errors "Type 'KnownChainIds.[Chain]Mainnet' is not assignable to type EvmChainId"
**Solution**: Add your chain to the `evmChainIds` array in EvmBaseAdapter
**Files to update**:
- `packages/chain-adapters/src/evm/EvmBaseAdapter.ts` (line ~70)
- Add to `evmChainIds` array: `KnownChainIds.[Chain]Mainnet`
- Add to `targetNetwork` object (line ~210): network name, symbol, explorer
**Example**: HyperEVM added at lines 81 and 262-266
**Why**: The array defines which chains are EVM-compatible for type checking

### Gotcha 16: Missing ChainSpecific Type Mappings (ALL Chains - 4 Places!)

**Problem**: TypeScript errors like:
- "Property 'chainSpecific' does not exist on type 'Account<T>'"
- "Property 'chainSpecific' does not exist on type 'BuildSendApiTxInput<T>'"
- "Property 'chainSpecific' does not exist on type 'GetFeeDataInput<T>'"

**Solution**: Add your chain to FOUR type mapping objects in chain-adapters/src/types.ts

**File**: `packages/chain-adapters/src/types.ts`

**ALL FOUR mappings required**:
1. ~Line 45: `ChainSpecificAccount` → `[KnownChainIds.[Chain]Mainnet]: evm.Account`
2. ~Line 91: `ChainSpecificFeeData` → `[KnownChainIds.[Chain]Mainnet]: evm.FeeData`
3. ~Line 219: `ChainSpecificBuildTxInput` → `[KnownChainIds.[Chain]Mainnet]: evm.BuildTxInput`
4. ~Line 320: `ChainSpecificGetFeeDataInput` → `[KnownChainIds.[Chain]Mainnet]: evm.GetFeeDataInput`

**Example**: HyperEVM added at lines 45, 91, 219, 320

**Why**: TypeScript uses these to determine chain-specific data structures

**CRITICAL**: Missing even ONE of these causes cryptic type errors! All 4 are required for ALL chains (EVM and non-EVM).

### Gotcha 17: Missing accountIdToLabel Case (BLOCKS ADDRESS DISPLAY!)

**Problem**: Addresses don't display in:
- Account import UI (shows blank address in table)
- Send flow "from" address row (shows empty from address)
- Account dropdowns throughout the app

**Root Cause**: Missing chainId case in `accountIdToLabel()` function
**File**: `src/state/slices/portfolioSlice/utils/index.ts` (around line 80-125)

**Solution**:
1. Add chainId import: `import { [chainLower]ChainId } from '@shapeshiftoss/caip'`
2. Add case to switch statement: `case [chainLower]ChainId:`
3. Place it with other EVM chains (before thorchainChainId)

**Example**:
```typescript
case baseChainId:
case hyperEvmChainId:  // ← ADD THIS
case monadChainId:
case plasmaChainId:
```

**Why**: This function converts accountId to human-readable label. Without the case, it hits the `default` and returns `''` (empty string), causing blank addresses everywhere in the UI.

**Note**: This affects ALL wallet types (Native, Ledger, Trezor, MetaMask), not just one wallet.

### Gotcha 18: Missing getNativeFeeAssetReference Case (RUNTIME CRASH!)

**Problem**: App crashes with error:
```
Error: Chain namespace [chain] on mainnet not supported.
    at getNativeFeeAssetReference.ts:XX:XX
```

**Root Cause**: Missing chainNamespace case in `getNativeFeeAssetReference()` function
**File**: `packages/utils/src/getNativeFeeAssetReference.ts`

**Solution**:
Add case to the switch statement:
```typescript
case CHAIN_NAMESPACE.[ChainName]:
  switch (chainReference) {
    case CHAIN_REFERENCE.[ChainName]Mainnet:
      return ASSET_REFERENCE.[ChainName]
    default:
      throw new Error(`Chain namespace ${chainNamespace} on ${chainReference} not supported.`)
  }
```

**Why**: This function maps chainId to the native fee asset reference. Without it, any selector that needs the fee asset for your chain will throw and crash the app.

**Note**: This is called early in the app initialization, so it will crash immediately when the app tries to load accounts for your chain.

### Gotcha 19: Missing accountToPortfolio Case (ACCOUNT NOT VISIBLE!)

**Problem**: Account discovery succeeds (getAccount returns valid data) but account doesn't appear in the UI anywhere.

**Root Cause**: Missing or placeholder implementation in `accountToPortfolio()` function
**File**: `src/state/slices/portfolioSlice/utils/index.ts`

**Symptom**: You can verify getAccount is returning correct data with console.log, but the account just doesn't show up in the portfolio UI.

**Solution**:
Find the switch statement for `chainNamespace` and implement your chain's case:
```typescript
case CHAIN_NAMESPACE.[ChainName]: {
  const chainAccount = account as Account<KnownChainIds.[ChainName]Mainnet>
  const { chainId, assetId, pubkey } = account
  const accountId = toAccountId({ chainId, account: pubkey })

  portfolio.accounts.ids.push(accountId)
  portfolio.accounts.byId[accountId] = { assetIds: [assetId], hasActivity }
  portfolio.accountBalances.ids.push(accountId)
  portfolio.accountBalances.byId[accountId] = { [assetId]: account.balance }

  // Add token support if applicable
  chainAccount.chainSpecific.tokens?.forEach(token => {
    if (!assetIds.includes(token.assetId)) return
    if (bnOrZero(token.balance).gt(0)) portfolio.accounts.byId[accountId].hasActivity = true
    portfolio.accounts.byId[accountId].assetIds.push(token.assetId)
    portfolio.accountBalances.byId[accountId][token.assetId] = token.balance
  })

  break
}
```

**Why**: This function converts chain adapter account data into the Redux portfolio state structure. Without it, the account data is fetched but never stored, making the account invisible.

### Gotcha 20: parseTx Doesn't Parse Token Transfers (SWAP EXECUTION PRICE WRONG!)

**Problem**:
- Native asset sends work fine
- Token sends/swaps show wrong execution price or $0
- Token transfers not appearing in transaction details

**Root Cause**: `parseTx()` only parses native transfers, not token events

**Symptom**: User reports swap worked but execution price shows as incorrect or zero.

**Solution**: Implement token parsing in parseTx. This is an iterative process:

1. **Start naive** - Parse native transfers only (initial implementation)
2. **User tests** - User makes a token send/swap
3. **Get RPC response** - User provides debugger scope with actual RPC data
4. **Refine parsing** - Add token event parsing based on real data structure

**Reference implementations**:
- `SecondClassEvmAdapter.parseTx()` - ERC-20 Transfer events
- `SuiChainAdapter.parseTx()` - SUI coin object changes
- `TronChainAdapter.parseTx()` - TRC-20 logs
- `NearChainAdapter.parseNep141Transfers()` - NEP-141 EVENT_JSON logs

**Common issues**:
1. **pubkey mismatch**: Logs use account address (e.g., `alice.near`) but function receives hex pubkey
   - Solution: Convert pubkey to account address before comparison
2. **Token contract ID extraction**: Token contract might be in receiver_id, Delegate action, or nested
   - Solution: Check actual RPC response structure
3. **Missing event parsing**: Chain-specific event format not handled
   - Solution: Parse EVENT_JSON, logs, or objectChanges based on chain type

**How to debug**:
```typescript
async parseTx(txHash: string, pubkey: string): Promise<Transaction> {
  const result = await this.rpcCall('tx', [txHash, 'dontcare'])
  console.log('parseTx result:', JSON.stringify(result, null, 2))
  console.log('pubkey:', pubkey)
  // ... rest of implementation
}
```

**Ask user for**: Breakpoint in parseTx, share `result` variable to see actual token event structure.

---

### Gotcha 21: Token Sends Build as Native Transfers (isToken missing new namespace)

**Problem**:
- Token send UI works, transaction broadcasts successfully
- But transaction is a native transfer to self, not a token transfer
- Token balance unchanged, only gas spent

**Root Cause**: `isToken()` in `packages/utils/src/index.ts` doesn't include the new chain's token namespace.

**Why it matters**: `contractAddressOrUndefined(assetId)` uses `isToken()` to determine if an asset is a token. If `isToken()` returns `false`, `contractAddressOrUndefined()` returns `undefined`, and the chain adapter builds a native transfer instead of a token transfer.

**EVM chains**: Not affected - EVM abstraction already handles `erc20`, `erc721`, `erc1155`.

**Non-EVM chains**: MUST add their token namespace to `isToken()`:
```typescript
// packages/utils/src/index.ts
export const isToken = (assetId: AssetId) => {
  switch (fromAssetId(assetId).assetNamespace) {
    case ASSET_NAMESPACE.erc20:
    case ASSET_NAMESPACE.erc721:
    case ASSET_NAMESPACE.erc1155:
    case ASSET_NAMESPACE.splToken:  // Solana
    case ASSET_NAMESPACE.trc20:     // Tron
    case ASSET_NAMESPACE.suiCoin:   // Sui
    case ASSET_NAMESPACE.nep141:    // NEAR <-- ADD YOUR NAMESPACE HERE
      return true
    default:
      return false
  }
}
```

**Symptom**: User sends token, tx succeeds, but token balance unchanged. Tx on block explorer shows native transfer to self.

**Debug**: Add logs in Send flow:
```typescript
console.log('[Send] assetId:', asset.assetId)
console.log('[Send] contractAddress:', contractAddressOrUndefined(asset.assetId))
// If contractAddress is undefined for a token, isToken() is missing the namespace
```

---

### Gotcha 22: Ledger "TypeError: coin" Error (Missing translateCoinAndMethod case)

**Problem**:
- Ledger connection works for other chains
- But new chain throws `TypeError: coin` when deriving address
- Error trace shows `translateCoinAndMethod` hitting `default: throw new TypeError("coin")`

**Root Cause**: For non-EVM chains, `translateCoinAndMethod` in Ledger WebHID/WebUSB transport needs a case for the new coin type.

**Files to update**:
1. `packages/hdwallet-ledger-webhid/src/transport.ts`
2. `packages/hdwallet-ledger-webusb/src/transport.ts`

**Solution**: Add import and case for the new chain's Ledger app:

```typescript
// 1. Add import at top
import Near from "@ledgerhq/hw-app-near";

// 2. Add case in translateCoinAndMethod switch
case "Near": {
  const near = new Near(transport as Transport);
  const methodInstance = near[method as LedgerTransportMethodName<"Near">].bind(near);
  return methodInstance as LedgerTransportMethod<T, U>;
}
```

**Prerequisites**:
- `@ledgerhq/hw-app-[chainname]` must exist as npm package
- Chain must be in `LedgerTransportCoinType` union in `packages/hdwallet-ledger/src/transport.ts`

**EVM chains**: Not affected - they use the Ethereum app via `case "Eth"`.

**Checklist for new non-EVM Ledger chain**:
- [ ] Add to `LedgerTransportCoinType` in `hdwallet-ledger/src/transport.ts`
- [ ] Add to `LedgerTransportMethodMap` type mapping in same file
- [ ] Add import + case in `hdwallet-ledger-webhid/src/transport.ts`
- [ ] Add import + case in `hdwallet-ledger-webusb/src/transport.ts`

---

## Quick Reference: File Checklist

### HDWallet Files (Required)
- [ ] `packages/hdwallet-core/src/[chainname].ts`
- [ ] `packages/hdwallet-core/src/index.ts` (export)
- [ ] `packages/hdwallet-core/src/utils.ts` (SLIP44)
- [ ] `packages/hdwallet-core/src/wallet.ts` (support function)
- [ ] `packages/hdwallet-native/src/[chainname].ts`
- [ ] `packages/hdwallet-native/src/native.ts` (integrate mixin)
- [ ] `packages/hdwallet-native/src/crypto/isolation/adapters/[chainname].ts` (if non-EVM)

### HDWallet Files (Optional - Ledger)
- [ ] `packages/hdwallet-ledger/src/ledger.ts`

### Web Files (Core)
- [ ] `packages/caip/src/constants.ts`
- [ ] `packages/types/src/base.ts`
- [ ] `src/constants/chains.ts`
- [ ] `packages/chain-adapters/src/[type]/[chainname]/[ChainName]ChainAdapter.ts`
- [ ] `packages/chain-adapters/src/[type]/[chainname]/types.ts`
- [ ] `packages/chain-adapters/src/[type]/[chainname]/index.ts`
- [ ] `src/lib/utils/[chainname].ts`
- [ ] `src/lib/account/[chainname].ts`
- [ ] `src/lib/account/account.ts` (wire into dispatcher)

### Web Files (Integration)
- [ ] `src/plugins/[chainname]/index.tsx`
- [ ] `src/plugins/activePlugins.ts`
- [ ] `src/context/PluginProvider/PluginProvider.tsx`
- [ ] `src/hooks/useWalletSupportsChain/useWalletSupportsChain.ts`
- [ ] `src/hooks/useActionCenterSubscribers/useSendActionSubscriber.tsx`
- [ ] `src/state/slices/portfolioSlice/utils/index.ts` (isAssetSupportedByWallet function)

### Web Files (Config)
- [ ] `.env`
- [ ] `.env.development`
- [ ] `.env.production`
- [ ] `src/config.ts`
- [ ] `src/state/slices/preferencesSlice/preferencesSlice.ts`
- [ ] `src/test/mocks/store.ts`
- [ ] `headers/csps/chains/[chainname].ts`
- [ ] `headers/csps/index.ts`

### Web Files (Utilities)
- [ ] `packages/utils/src/getAssetNamespaceFromChainId.ts`
- [ ] `packages/utils/src/getChainShortName.ts`
- [ ] `packages/utils/src/getNativeFeeAssetReference.ts`
- [ ] `packages/utils/src/chainIdToFeeAssetId.ts`
- [ ] `packages/utils/src/assetData/baseAssets.ts`
- [ ] `packages/utils/src/assetData/getBaseAsset.ts`

### Web Files (Assets & CoinGecko)
- [ ] `packages/caip/src/adapters/coingecko/index.ts` (add platform enum)
- [ ] `packages/caip/src/adapters/coingecko/utils.ts` (add chainId mapping and native asset)
- [ ] `packages/caip/src/adapters/coingecko/utils.test.ts` (add test)
- [ ] `packages/caip/src/adapters/coingecko/index.test.ts` (add asset fixture)
- [ ] `scripts/generateAssetData/coingecko.ts` (add chain case for token fetching)
- [ ] `scripts/generateAssetData/[chainname]/index.ts` (create asset generator)
- [ ] `scripts/generateAssetData/generateAssetData.ts` (wire in generator)
- [ ] `src/lib/asset-service/service/AssetService.ts` (add feature flag filter)

### Web Files (Swapper Integration)
- [ ] `packages/swapper/src/swappers/RelaySwapper/constant.ts` (add chain mapping)
- [ ] `packages/swapper/src/swappers/RelaySwapper/utils/relayTokenToAssetId.ts` (add native asset case)
- [ ] Other swappers as needed (CowSwap, OneInch, etc.)

### Web Files (Ledger - Optional)
- [ ] `src/context/WalletProvider/Ledger/constants.ts`

---

## Summary

This skill covers the COMPLETE process for adding a new blockchain as a second-class citizen:

1. ✅ HDWallet native support (workspace packages under `packages/hdwallet-*`)
2. ✅ Web poor man's chain adapter
3. ✅ Feature flags and configuration
4. ✅ Asset generation
5. ✅ Transaction status polling
6. ✅ Ledger support (optional)
7. ✅ Testing and validation
8. ✅ Clean commit workflow

**Key Principles:**
- HDWallet packages are in the monorepo — no separate repo, no Verdaccio, no version bumps
- Always start with HDWallet native (`packages/hdwallet-core` + `packages/hdwallet-native`)
- Follow existing patterns (Monad for EVM, Tron/Sui for non-EVM)
- Poor man's approach: public RPC, no microservices, minimal features
- Feature flag everything
- Clean, focused commits

**Remember**: Second-class citizen = basic support only. No fancy features, no microservices, just enough to send/receive and swap.
