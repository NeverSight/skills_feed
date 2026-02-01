---
name: avnu
description: >
  Integrate avnu SDK for Starknet DeFi: token swaps with best-price routing,
  DCA recurring buys, native staking, gasless transactions via paymaster,
  and market data. Use when building Starknet trading, DEX aggregation,
  or DeFi automation features.
keywords:
  - avnu
  - starknet
  - defi
  - swap
  - dca
  - staking
  - paymaster
  - gasless
  - l2
  - dex
  - aggregator
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Task
user-invocable: true
---

# avnu SDK Integration

avnu is the leading DEX aggregator on Starknet, providing optimized swaps across multiple liquidity sources, DCA orders, staking, gasless transactions, and market data APIs.

## Installation

```bash
npm install @avnu/avnu-sdk starknet
```

## Account Setup

The SDK requires a Starknet account. Two patterns depending on your use case:

### Direct Account (Scripts/Backend)

```typescript
import { Account, RpcProvider } from 'starknet';

const provider = new RpcProvider({
  nodeUrl: process.env.STARKNET_RPC_URL || 'https://rpc.starknet.lava.build'
});

const account = new Account(
  provider,
  process.env.STARKNET_ACCOUNT_ADDRESS!,
  process.env.STARKNET_PRIVATE_KEY!
);
```

### Wallet Account (Frontend/dApps)

```typescript
import { WalletAccount } from 'starknet';

// User connects their wallet (Argent, Braavos)
const account = await WalletAccount.connect(provider, walletProvider);
```

## Common Token Addresses

```typescript
const TOKENS = {
  ETH: '0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7',
  STRK: '0x04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d',
  USDC: '0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8',
  USDT: '0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8',
};
```

---

## Swap Operations

Get optimized quotes from multiple DEXs and execute swaps with best-price routing.

### Get Quotes

```typescript
import { getQuotes } from '@avnu/avnu-sdk';

const quotes = await getQuotes({
  sellTokenAddress: TOKENS.ETH,
  buyTokenAddress: TOKENS.USDC,
  sellAmount: BigInt(1e18), // 1 ETH
  takerAddress: account.address,
  size: 3, // Get top 3 quotes
});

const best = quotes[0];
console.log('Buy amount:', best.buyAmount);
console.log('Price impact:', `${(best.priceImpact / 100).toFixed(2)}%`); // basis points to %
console.log('Gas fees USD:', best.gasFeesInUsd);
```

### Execute Swap

```typescript
import { executeSwap } from '@avnu/avnu-sdk';

const result = await executeSwap({
  provider: account,
  quote: quotes[0],
  slippage: 0.01, // 1%
  executeApprove: true,
});

console.log('Tx hash:', result.transactionHash);
```

### Build Calls Only (for custom execution)

```typescript
import { quoteToCalls } from '@avnu/avnu-sdk';

const { calls } = await quoteToCalls({
  quote: quotes[0],
  takerAddress: account.address,
  slippage: 0.01,
  includeApprove: true,
});

// Execute manually
const tx = await account.execute(calls);
```

### Slippage Strategies

| Token Type | Recommended Slippage |
|------------|---------------------|
| Stablecoins | 0.1% - 0.5% |
| Major tokens (ETH, STRK) | 0.5% - 1% |
| Low liquidity | 1% - 3% |

> See [references/swap-guide.md](references/swap-guide.md) for advanced routing and multi-quote analysis.

---

## DCA (Dollar Cost Averaging)

Create recurring buy orders that execute automatically at specified intervals.

### Create DCA Order

```typescript
import { executeCreateDca, createDcaToCalls } from '@avnu/avnu-sdk';
import moment from 'moment';

const dcaOrder = {
  sellTokenAddress: TOKENS.USDC,
  buyTokenAddress: TOKENS.ETH,
  sellAmount: '100000000', // Total 100 USDC (6 decimals)
  sellAmountPerCycle: '10000000', // 10 USDC per execution
  frequency: moment.duration(1, 'day'),
  traderAddress: account.address,
};

const result = await executeCreateDca({
  provider: account,
  order: dcaOrder,
});

console.log('DCA created:', result.transactionHash);
```

### Get User's DCA Orders

```typescript
import { getDcaOrders, DcaOrderStatus } from '@avnu/avnu-sdk';

const orders = await getDcaOrders({
  traderAddress: account.address,
  status: DcaOrderStatus.ACTIVE,
  page: 0,
  size: 20,
});

orders.content.forEach(order => {
  console.log('Order:', order.orderAddress);
  console.log('Progress:', order.executedTradesCount, '/', order.iterations);
  console.log('Sold:', order.amountSold, '/ Bought:', order.amountBought);
});
```

### Cancel DCA Order

```typescript
import { executeCancelDca } from '@avnu/avnu-sdk';

const result = await executeCancelDca({
  provider: account,
  orderAddress: '0xorder...',
});
```

### DCA Frequency Options

```typescript
moment.duration(1, 'hour')   // Hourly
moment.duration(1, 'day')    // Daily
moment.duration(1, 'week')   // Weekly
moment.duration(1, 'month')  // Monthly
```

> See [references/dca-guide.md](references/dca-guide.md) for pricing strategies and order lifecycle.

---

## Staking

Stake tokens to earn rewards. Supports STRK and BTC variants.

### Stake Tokens

```typescript
import { executeStake } from '@avnu/avnu-sdk';

const result = await executeStake({
  provider: account,
  poolAddress: '0xpool...',
  amount: BigInt(100e18), // 100 STRK
});

console.log('Staked:', result.transactionHash);
```

### Get Staking Info

```typescript
import { getUserStakingInfo, getAvnuStakingInfo } from '@avnu/avnu-sdk';

// Get pool info
const stakingInfo = await getAvnuStakingInfo();
console.log('Total staked:', stakingInfo.totalStaked);
console.log('APY:', stakingInfo.apy);

// Get user position
const userInfo = await getUserStakingInfo(
  TOKENS.STRK,
  account.address
);
console.log('Staked:', userInfo.stakedAmount);
console.log('Rewards:', userInfo.pendingRewards);
```

### Claim Rewards

```typescript
import { executeClaimRewards } from '@avnu/avnu-sdk';

// Claim and withdraw
await executeClaimRewards({
  provider: account,
  poolAddress: '0xpool...',
  restake: false,
});

// Claim and restake
await executeClaimRewards({
  provider: account,
  poolAddress: '0xpool...',
  restake: true,
});
```

### Unstake (Two-Step Process)

```typescript
import { executeInitiateUnstake, executeUnstake } from '@avnu/avnu-sdk';

// Step 1: Initiate unstake (starts cooldown)
await executeInitiateUnstake({
  provider: account,
  poolAddress: '0xpool...',
  amount: BigInt(50e18),
});

// Step 2: After cooldown period (7-21 days), complete withdrawal
await executeUnstake({
  provider: account,
  poolAddress: '0xpool...',
});
```

> See [references/staking-guide.md](references/staking-guide.md) for pool discovery and unbonding periods.

---

## Paymaster (Gasless Transactions)

Enable gasless transactions where users pay fees in ERC-20 tokens instead of ETH.

### Setup PaymasterRpc

```typescript
import { PaymasterRpc } from 'starknet';

const paymaster = new PaymasterRpc({
  nodeUrl: 'https://starknet.api.avnu.fi/paymaster/v1',
});
```

### Gasless Swap (User Pays in Token)

```typescript
import { PaymasterRpc, type PaymasterDetails } from 'starknet';
import { executeSwap } from '@avnu/avnu-sdk';

const paymaster = new PaymasterRpc({
  nodeUrl: 'https://starknet.api.avnu.fi/paymaster/v1',
});

const result = await executeSwap({
  provider: account,
  quote: quotes[0],
  slippage: 0.01,
  paymaster: {
    active: true,
    provider: paymaster,
    params: {
      feeMode: { mode: 'default', gasToken: TOKENS.USDC },
    },
  },
});
```

### With Fee Estimation (Recommended)

```typescript
import { PaymasterRpc, type PaymasterDetails } from 'starknet';
import { quoteToCalls } from '@avnu/avnu-sdk';

const paymaster = new PaymasterRpc({
  nodeUrl: 'https://starknet.api.avnu.fi/paymaster/v1',
});

// Build calls from quote
const { calls } = await quoteToCalls({
  quote: quotes[0],
  takerAddress: account.address,
  slippage: 0.01,
  includeApprove: true,
});

// Estimate fees
const feeDetails: PaymasterDetails = {
  feeMode: { mode: 'default', gasToken: TOKENS.USDC },
};
const estimation = await account.estimatePaymasterTransactionFee(calls, feeDetails);

// Execute with estimated max fee
const result = await account.executePaymasterTransaction(
  calls,
  feeDetails,
  estimation.suggested_max_fee_in_gas_token
);
```

> See [references/paymaster-guide.md](references/paymaster-guide.md) for supported tokens and best practices.

---

## Gasfree (Sponsored Transactions)

Enable zero-gas-fee transactions where your dApp pays gas on behalf of users. Requires an API key from [portal.avnu.fi](https://portal.avnu.fi).

### Setup (Backend/Scripts)

```typescript
import { PaymasterRpc } from 'starknet';

const paymaster = new PaymasterRpc({
  nodeUrl: 'https://starknet.paymaster.avnu.fi',
  headers: {
    'x-paymaster-api-key': process.env.AVNU_PAYMASTER_API_KEY!,
  },
});
```

### Gasfree Swap

```typescript
import { executeSwap } from '@avnu/avnu-sdk';

const result = await executeSwap({
  provider: account,
  quote: quotes[0],
  slippage: 0.01,
  paymaster: {
    active: true,
    provider: paymaster,
    params: {
      feeMode: { mode: 'sponsored' },
    },
  },
});
// User paid $0 in gas!
```

### Frontend Integration (Next.js)

The API key must never be exposed client-side. Use a 3-phase pattern:

```typescript
// Server Action (API key protected)
'use server';
import { buildPaymasterTransaction, executePaymasterTransaction } from '@avnu/avnu-sdk';

export async function buildSponsoredTx(userAddress: string, calls: Call[]) {
  return buildPaymasterTransaction({
    takerAddress: userAddress,
    paymaster: { provider: getPaymaster(), params: { feeMode: { mode: 'sponsored' } } },
    calls,
  });
}

// Client-side
const prepared = await buildSponsoredTx(account.address, calls);  // 1. Build on server
const signed = await signPaymasterTransaction({ provider: account, typedData: prepared.typed_data });  // 2. Sign on client
const result = await executeSponsoredTx(account.address, signed);  // 3. Execute on server
```

> See [references/gasfree-frontend.md](references/gasfree-frontend.md) for complete Next.js integration with hooks and error handling.
> See [scripts/gasfree-swap.ts](scripts/gasfree-swap.ts) for a runnable backend example.

### Gasless vs Gasfree

| Mode | Who Pays | API Key | Best For |
|------|----------|---------|----------|
| Gasless | User (in token) | No | Users without ETH |
| Gasfree | dApp | Yes | Zero-friction UX |

---

## Tokens & Prices

Fetch token lists and real-time market data.

### Fetch Tokens

```typescript
import { fetchTokens, fetchVerifiedTokenBySymbol } from '@avnu/avnu-sdk';

// Get paginated token list
const page = await fetchTokens({
  page: 0,
  size: 50,
  tags: ['Verified'],
});

page.content.forEach(token => {
  console.log(token.symbol, token.address, token.decimals);
});

// Get verified token by symbol
const eth = await fetchVerifiedTokenBySymbol('ETH');
const strk = await fetchVerifiedTokenBySymbol('STRK');
```

### Get Token Prices

```typescript
import { getPrices } from '@avnu/avnu-sdk';

const prices = await getPrices([
  TOKENS.ETH,
  TOKENS.STRK,
  TOKENS.USDC,
]);

prices.forEach(p => {
  console.log('Address:', p.address);
  console.log('Global USD:', p.globalMarket?.usd);
  console.log('Starknet USD:', p.starknetMarket?.usd);
});
```

Token tags: `Verified`, `Community`, `Unruggable`, `AVNU`, `Unknown`. See [references/tokens-prices.md](references/tokens-prices.md) for OHLCV data.

---

## Error Quick Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `INSUFFICIENT_LIQUIDITY` | No route found | Reduce amount or try different pair |
| `SLIPPAGE_EXCEEDED` | Price moved during execution | Increase slippage or refresh quote |
| `QUOTE_EXPIRED` | Quote too old (>30s) | Fetch new quote before executing |
| `PAYMASTER_REJECTED` | Transaction not eligible | Check token/amount eligibility |
| `INSUFFICIENT_BALANCE` | Not enough tokens | Validate balance before execute |

> See [references/error-handling.md](references/error-handling.md) for complete error taxonomy.

---

## Configuration

### Environment Variables

```bash
# Required for direct account
STARKNET_ACCOUNT_ADDRESS=0x...
STARKNET_PRIVATE_KEY=0x...         # NEVER commit!

# Optional
STARKNET_RPC_URL=https://rpc.starknet.lava.build
```

### SDK Options

```typescript
import { AvnuOptions } from '@avnu/avnu-sdk';

const options: AvnuOptions = {
  baseUrl: 'https://starknet.api.avnu.fi', // Default
  impulseBaseUrl: 'https://starknet.impulse.avnu.fi', // DCA API
  abortSignal: controller.signal, // Request cancellation
};

// Pass to any SDK call
const quotes = await getQuotes(request, options);
```

### Networks

| Network | Base URL |
|---------|----------|
| Mainnet | `https://starknet.api.avnu.fi` |
| Sepolia | `https://sepolia.api.avnu.fi` |

> See [references/configuration.md](references/configuration.md) for complete setup guide.

---

## References & Examples

**Guides:** [swap-guide](references/swap-guide.md) | [dca-guide](references/dca-guide.md) | [staking-guide](references/staking-guide.md) | [paymaster-guide](references/paymaster-guide.md) | [gasfree-frontend](references/gasfree-frontend.md) | [tokens-prices](references/tokens-prices.md) | [error-handling](references/error-handling.md) | [configuration](references/configuration.md)

**Scripts:** [swap-example.ts](scripts/swap-example.ts) | [dca-example.ts](scripts/dca-example.ts) | [staking-example.ts](scripts/staking-example.ts) | [gasless-swap.ts](scripts/gasless-swap.ts) | [gasfree-swap.ts](scripts/gasfree-swap.ts)

**Links:** [Docs](https://docs.avnu.fi) | [SDK GitHub](https://github.com/avnu-labs/avnu-sdk) | [App](https://app.avnu.fi)
