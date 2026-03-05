---
name: manifold-nft-minting
description: "Build NFT minting experiences with Manifold's client-sdk. Guides agents through campaign setup, custom minting websites (React/Next.js), minting bots (Node.js), and SDK integration into existing projects. Supports [`Edition`](https://docs.manifold.xyz/client-sdk/sdk/product/edition-product) and [`Blind Mint`](https://docs.manifold.xyz/client-sdk/sdk/product/blind-mint) products across Ethereum, Base, Optimism, Shape, Sepolia, and ApeChain. Use when building minting pages, mint bots, integrating Manifold NFT products, or helping users set up Manifold campaigns. NOT for deploying smart contracts, managing Manifold Studio settings, or non-minting blockchain operations."
---

# Manifold NFT Minting Skill

Build custom NFT minting experiences using [`@manifoldxyz/client-sdk`](https://github.com/manifoldxyz/client-sdk).

## References

Load lazily — only when the current step needs them. **Never load all at once.**

| Reference | When to Load |
|-----------|-------------|
| `getting-started.md` | First SDK setup in any project |
| `product-types.md` | Working with Edition vs BlindMint products |
| `purchase-flow.md` | Implementing preparePurchase → purchase |
| `transaction-steps.md` | Multi-step transactions, ERC-20 approvals |
| `adapters.md` | Setting up wallet + provider adapters (ethers5/viem/wagmi) |
| `product-data.md` | Querying status, allocations, inventory, rules |
| `error-handling.md` | Error codes, pitfalls — **always load before writing purchase code** |
| `networks.md` | Multi-chain setup or non-mainnet deployments |
| `react-minting-app.md` | Building a React/Next.js minting page |
| `rainbowkit-setup.md` | RainbowKit installation, wagmi config, ConnectButton, providers |
| `rpc-setup-guide.md` | Setting up an RPC provider (Alchemy/Infura/QuickNode) |
| `minting-bot.md` | Building a headless minting bot |
| `studio-setup-guide.md` | User needs to create a Manifold campaign first |
| `full-docs.md` | Fallback only — 128KB complete SDK docs with TOC for grep |

## Workflow

Follow in order. Ask questions — don't assume.

### Step 1: Check if they have a Manifold campaign

Ask: **"Do you already have a Manifold product/campaign deployed with an instance ID?"**

- **No** → Read `references/studio-setup-guide.md`. Guide them through product type selection and Studio setup. Return when they have an instance ID.
- **Yes** → Continue.

### Step 2: Determine project context

Ask: **"Do you have an existing project to add minting to, or building from scratch?"**

**Existing project:**
1. Ask their framework
2. Ask if they already have a wallet connection library set up (e.g., RainbowKit, Web3Modal, ConnectKit, custom)
   - **Yes, already set up** → Ask which library they use. Read `references/getting-started.md` + `references/adapters.md`. Match adapter setup to their stack — integrate, don't scaffold.
   - **No wallet connection yet** → Proceed to Step 2a
3. Proceed to Step 2b (RPC setup)

**From scratch:**
1. Ask what they're building:
   - **Web minting page** → Proceed to Step 2a (Wallet Connection), then Step 2b (RPC Setup)
   - **Server-side bot** → Read `references/minting-bot.md`. Proceed to Step 2b (RPC Setup)
   - **Data query script** → Read `references/getting-started.md` only. Proceed to Step 2b (RPC Setup)

### Step 2a: Wallet connection (web apps only)

Ask: **"Would you like to use [RainbowKit](https://www.rainbowkit.com/) for wallet connection? It's the most common choice for React/Next.js minting apps."**

**RainbowKit (yes):**
1. Read `references/rainbowkit-setup.md` + `references/react-minting-app.md` + `references/getting-started.md` + `references/networks.md` + `references/adapters.md`
2. Follow RainbowKit's setup patterns for wagmi config, providers, and `<ConnectButton />`

**Other library (no):**
1. Ask: **"Which wallet connection library would you like to use?"** (e.g., Web3Modal, ConnectKit, Dynamic, Privy, custom)
2. Ask the user to describe their library's provider/config pattern, then adapt the SDK integration accordingly.
3. Read `references/getting-started.md` + `references/networks.md` + `references/adapters.md`
4. Adapt the SDK integration to work with their chosen wallet library instead of RainbowKit

### Step 2b: RPC node setup

Ask: **"Do you have an RPC node URL you can provide (e.g., from Alchemy, Infura, QuickNode)?"**

**Yes** → Store the RPC URL in a `.env` file and reference via `process.env.*` in configuration. Ensure `.gitignore` includes `.env`. Proceed to Step 3.

**No, but willing to set one up** → Read `references/rpc-setup-guide.md` and guide them through creating an Alchemy account and getting an RPC endpoint. Proceed to Step 3.

**No, skip (use public RPC)** → Use viem's built-in public transport. In code, use `http()` with no URL argument:

```typescript
import { http } from 'viem';
// Public RPC — no URL needed
transport: http()
```

> **Note:** Public RPCs have rate limits and may be slower. Recommend upgrading to a dedicated RPC for production apps.

Proceed to Step 3.

### Step 3: Implement product interaction

1. Read `references/product-types.md` — use type guards (`isEditionProduct`, `isBlindMintProduct`)
2. Read `references/product-data.md` — status, allocations, metadata display
3. Read `references/purchase-flow.md` — two-step prepare → purchase
4. If ERC-20 pricing → also read `references/transaction-steps.md`

### Step 4: Error handling

**Always before finalizing:**

1. Read `references/error-handling.md` — ClientSDKError handling + common pitfalls
2. If multi-chain → read `references/networks.md`

## Rules

- **When using RainbowKit, ALWAYS install `wagmi@^2.9.0` — NEVER run `npm install wagmi` without the version pin.** The correct command is `npm install wagmi@^2.9.0` (or `yarn add wagmi@^2.9.0` / `pnpm add wagmi@^2.9.0`). Running `npm install wagmi` or `npm install wagmi@latest` will install wagmi 3.x, which is incompatible with RainbowKit and will cause build/runtime errors. This is the #1 mistake agents make — always include the `@^2.9.0` version specifier.
- **Always use environment variables for RPC URLs and private keys** — generate `.env` files for secrets and ensure `.gitignore` includes `.env`. Never inline credentials in source code. Reference values via `process.env.*` (e.g., `process.env.RPC_URL!`, `process.env.WALLET_PRIVATE_KEY!`).
- **Always display cost and confirm before executing transactions.** Before calling `purchase()` or `step.execute()`, display the total cost (`prepared.cost.total.native.formatted`), network, and quantity to the user and ask for explicit confirmation.
- **Prefer viem over ethers** for new projects. Only use ethers v5 if the user explicitly requests it or has an existing ethers codebase.
- **Never fabricate SDK method signatures or field names.** Verify against references.
- **Always confirm wallet connection choice** before scaffolding a web minting app. Never assume RainbowKit.
- **Always read wallet library docs** before writing integration code — read `references/rainbowkit-setup.md` for RainbowKit, or ask the user to describe their library's config pattern for other libraries.
- **Always use type guards** before accessing product-specific methods.
- **Always check `getStatus()`** before purchases.
- **Use `preparePurchase` → `purchase`** for simple flows. Manual `step.execute()` only for granular UI control.
- **Never hardcode chain IDs** — use configuration.
- **Never commit private keys** — use environment variables.
- Verify code against official docs at [docs.manifold.xyz/client-sdk](https://docs.manifold.xyz/client-sdk/).
- For issues beyond SDK scope → [Manifold Help](https://help.manifold.xyz/) or [Forum](https://forum.manifold.xyz).
