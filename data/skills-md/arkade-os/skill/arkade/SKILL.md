---
name: arkade
description: Send and receive Bitcoin over Arkade (offchain), onchain (via onboard/offboard), and Lightning. Swap USDC/USDT stablecoins.
read_when:
  - user wants to send or receive Bitcoin
  - user mentions Arkade, Ark, or offchain Bitcoin
  - user wants to use Lightning Network
  - user wants to swap BTC for stablecoins (USDC, USDT)
  - user wants to on-ramp or off-ramp Bitcoin
  - user wants to get paid onchain or pay someone onchain
  - user mentions boarding address or VTXOs
  - user wants instant Bitcoin payments
requires: []
metadata:
  emoji: "₿"
---

# Arkade Skill

Send and receive Bitcoin over Arkade (offchain), onchain (via onboard/offboard), and Lightning Network.
Swap between BTC and stablecoins (USDC/USDT) via LendaSwap.

**Payment methods:**
- **Offchain (Arkade)**: Instant transactions between Arkade wallets
- **Onchain**: Get paid onchain via boarding address (onboard), pay onchain via offboard
- **Lightning**: Pay and receive via Boltz submarine swaps

**Default Server:** https://arkade.computer

## Agent Safety Rules

**IMPORTANT: The following commands move real funds. The agent MUST always ask the user for explicit confirmation before executing them, displaying the amount and destination:**

- `send` — sends sats to an Ark address
- `offboard` — moves offchain BTC to an onchain Bitcoin address
- `onboard` — moves onchain BTC into Arkade
- `ln-pay` — pays a Lightning invoice
- `swap-to-stable` / `swap-to-btc` — executes a stablecoin swap
- `swap-claim` / `swap-refund` / `swap-evm-refund` — claims or refunds a swap

Read-only commands (`address`, `balance`, `history`, `ln-invoice`, `ln-fees`, `ln-limits`, `ln-pending`, `swap-quote`, `swap-pairs`, `swap-status`, `swap-pending`, `swap-evm-refund`, `boarding-address`) are safe to run without confirmation.

**Refund behavior:**

- **BTC→EVM swaps** (`swap-refund`): Refunds BTC back to your Ark address (or a custom address). The destination defaults to your Ark address if not specified.
- **EVM→BTC swaps** (`swap-evm-refund`): Returns the EVM contract call data needed to refund locked EVM tokens. The user must execute this transaction from their EVM wallet.

**Wallet initialization:** `init` creates a new private key stored at `~/.arkade-wallet/config.json` (permissions `0600`). All other commands require `init` to have been run first. The agent MUST inform the user and get confirmation before running `init` for the first time.

## Installation

### Quick Start (no install required)

```bash
# Using pnpm (recommended)
pnpm dlx @arkade-os/skill init
pnpm dlx @arkade-os/skill address

# Using npx
npx -y -p @arkade-os/skill arkade init
npx -y -p @arkade-os/skill arkade address
```

### Global Install

```bash
# Install globally
npm install -g @arkade-os/skill
# or
pnpm add -g @arkade-os/skill

# Then use directly
arkade init
arkade address
```

### As a dependency

```bash
npm install @arkade-os/skill
# or
pnpm add @arkade-os/skill
```

## CLI Commands

> **Note:** Examples below use `arkade` directly (assumes global install).
> For pnpm: `pnpm dlx @arkade-os/skill <command>`
> For npx: `npx -y -p @arkade-os/skill arkade <command>`

### Wallet Management

```bash
# Initialize wallet (auto-generates private key, default server: arkade.computer)
arkade init

# Initialize with custom server
arkade init https://custom-server.com

# Show Ark address (for receiving offchain Bitcoin)
arkade address

# Show boarding address (for onchain deposits)
arkade boarding-address

# Show balance breakdown
arkade balance
```

### Bitcoin Transactions

```bash
# Send sats to an Ark address
arkade send <ark-address> <amount-sats>

# Example: Send 50,000 sats
arkade send ark1qxyz... 50000

# View transaction history
arkade history
```

### Onchain Payments (Onboard/Offboard)

```bash
# Get paid onchain: Receive BTC to your boarding address, then onboard to Arkade
# Step 1: Get your boarding address
arkade boarding-address

# Step 2: Have someone send BTC to your boarding address

# Step 3: Onboard the received BTC to make it available offchain
arkade onboard

# Pay onchain: Send offchain BTC to any onchain Bitcoin address
arkade offboard <btc-address>

# Example: Pay someone at bc1 address
arkade offboard bc1qxyz...
```

### Lightning Network

```bash
# Create a Lightning invoice to receive payment
arkade ln-invoice <amount-sats> [description]

# Example: Create invoice for 25,000 sats
arkade ln-invoice 25000 "Coffee payment"

# Pay a Lightning invoice
arkade ln-pay <bolt11-invoice>

# Show swap fees
arkade ln-fees

# Show swap limits
arkade ln-limits

# Show pending swaps
arkade ln-pending
```

### Stablecoin Swaps (LendaSwap)

```bash
# Get quote for BTC to stablecoin swap
arkade swap-quote <amount-sats> <from> <to>

# Example: Quote 100,000 sats to USDC on Polygon
arkade swap-quote 100000 btc_arkade usdc_pol

# Show available trading pairs
arkade swap-pairs

# Refund a BTC→EVM swap (defaults to your Ark address)
arkade swap-refund <swap-id> [destination-address]

# Get EVM refund call data for an EVM→BTC swap
arkade swap-evm-refund <swap-id>
```

**Supported Tokens:**
- `btc_arkade` - Bitcoin on Arkade
- `usdc_pol` - USDC on Polygon
- `usdc_eth` - USDC on Ethereum
- `usdc_arb` - USDC on Arbitrum
- `usdt_pol` - USDT on Polygon
- `usdt_eth` - USDT on Ethereum
- `usdt_arb` - USDT on Arbitrum

## SDK Usage

```typescript
import { Wallet, SingleKey } from "@arkade-os/sdk";
import {
  ArkadeBitcoinSkill,
  ArkaLightningSkill,
  LendaSwapSkill,
} from "@arkade-os/skill";

// Create wallet (default server: arkade.computer)
const wallet = await Wallet.create({
  identity: SingleKey.fromHex(privateKeyHex),
  arkServerUrl: "https://arkade.computer",
});

// === Bitcoin Operations ===
const bitcoin = new ArkadeBitcoinSkill(wallet);

// Get addresses
const arkAddress = await bitcoin.getArkAddress();
const boardingAddress = await bitcoin.getBoardingAddress();

// Check balance
const balance = await bitcoin.getBalance();
console.log("Total:", balance.total, "sats");
console.log("Offchain available:", balance.offchain.available, "sats");
console.log("Onchain pending:", balance.onchain.total, "sats");

// Send Bitcoin
const result = await bitcoin.send({
  address: recipientArkAddress,
  amount: 50000,
});
console.log("Sent! TX:", result.txid);

// === Lightning Operations ===
const lightning = new ArkaLightningSkill({
  wallet,
  network: "bitcoin",
});

// Create invoice
const invoice = await lightning.createInvoice({
  amount: 25000,
  description: "Coffee payment",
});
console.log("Invoice:", invoice.bolt11);

// Pay invoice
const payment = await lightning.payInvoice({
  bolt11: "lnbc...",
});
console.log("Paid! Preimage:", payment.preimage);

// === Stablecoin Swaps ===
const lendaswap = new LendaSwapSkill({ wallet });

// Get quote
const quote = await lendaswap.getQuoteBtcToStablecoin(100000, "usdc_pol");
console.log("You'll receive:", quote.targetAmount, "USDC");

// Execute swap
const swap = await lendaswap.swapBtcToStablecoin({
  targetAddress: "0x...", // EVM address
  targetToken: "usdc_pol",
  targetChain: "polygon",
  sourceAmount: 100000,
});
console.log("Swap ID:", swap.swapId);
```

## Configuration

**Data Storage:** `~/.arkade-wallet/config.json`

Private keys are auto-generated on first use and stored locally. They are never exposed via CLI arguments or stdout. No environment variables required. The LendaSwap API is publicly accessible.

## Skill Interfaces

### ArkadeBitcoinSkill

- `getArkAddress()` - Get Ark address for receiving offchain payments
- `getBoardingAddress()` - Get boarding address for receiving onchain payments
- `getBalance()` - Get balance breakdown
- `send(params)` - Send Bitcoin to Ark address (offchain)
- `getTransactionHistory()` - Get transaction history
- `onboard(params)` - Get paid onchain: convert onchain BTC to offchain
- `offboard(params)` - Pay onchain: send offchain BTC to any onchain address
- `waitForIncomingFunds(timeout?)` - Wait for incoming funds

### ArkaLightningSkill

- `createInvoice(params)` - Create Lightning invoice
- `payInvoice(params)` - Pay Lightning invoice
- `getFees()` - Get swap fees
- `getLimits()` - Get swap limits
- `getPendingSwaps()` - Get pending swaps
- `getSwapHistory()` - Get swap history
- `isAvailable()` - Check if Lightning is available

### LendaSwapSkill

- `getQuoteBtcToStablecoin(amount, token)` - Quote BTC to stablecoin
- `getQuoteStablecoinToBtc(amount, token)` - Quote stablecoin to BTC
- `swapBtcToStablecoin(params)` - Swap BTC to stablecoin
- `swapStablecoinToBtc(params)` - Swap stablecoin to BTC
- `getSwapStatus(swapId)` - Get swap status
- `getPendingSwaps()` - Get pending swaps
- `getSwapHistory()` - Get swap history
- `getAvailablePairs()` - Get available trading pairs
- `claimSwap(swapId)` - Claim completed swap
- `refundSwap(swapId)` - Refund expired swap

## Networks

Arkade supports multiple networks:
- `bitcoin` - Bitcoin mainnet
- `testnet` - Bitcoin testnet
- `signet` - Bitcoin signet
- `regtest` - Local regtest
- `mutinynet` - Mutiny signet

## Support

- GitHub: https://github.com/arkade-os/skill
- Documentation: https://docs.arkadeos.com
