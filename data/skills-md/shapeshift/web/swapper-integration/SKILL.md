---
name: swapper-integration
description: Integrate new DEX aggregators, swappers, or bridge protocols (like Bebop, Portals, Jupiter, 0x, 1inch, etc.) into ShapeShift Web. Activates when user wants to add, integrate, or implement support for a new swapper. Guides through research, implementation, and testing following established patterns. (project)
allowed-tools: Read, Write, Edit, Grep, Glob, WebFetch, WebSearch, Bash(yarn test:*), Bash(yarn lint:*), Bash(yarn type-check), Bash(yarn build:*), Bash(gh pr:*), AskUserQuestion
---

# Swapper Integration Skill

You are an expert at integrating DEX aggregators, swappers, and bridge protocols into ShapeShift Web. This skill guides you through the complete process from API research to production-ready implementation.

## When This Skill Activates

Use this skill when the user wants to:
- "Integrate [SwapperName] swapper"
- "Add support for [Protocol]"
- "Implement [DEX] integration"
- "Add [Aggregator] as a swapper"
- "Integrate [new swapper]"

## Overview

ShapeShift Web is a decentralized crypto exchange aggregator that supports multiple swap providers through a unified interface. Each swapper implements standardized TypeScript interfaces (`Swapper` and `SwapperApi`) but has variations based on blockchain type (EVM, UTXO, Solana, Sui, Tron) and swapper model (direct transaction, deposit-to-address, gasless order-based).

**Core Architecture**:
- **Location**: `packages/swapper/src/swappers/`
- **Interfaces**: `Swapper` (execution) + `SwapperApi` (quotes/rates/status)
- **Types**: Strongly typed with chain-specific adaptations
- **Feature Flags**: All swappers behind runtime flags for gradual rollout

**Your Role**: Research → Implement → Test → Document, following battle-tested patterns from 13+ existing swapper integrations.

---

## Workflow

### Phase 0: Pre-Research (Use WebFetch / WebSearch)

**BEFORE asking the user for anything**, proactively research the swapper online:

1. **Search for official documentation**:
   ```text
   Search: "[SwapperName] API documentation"
   Search: "[SwapperName] developer docs"
   Search: "[SwapperName] swagger api"
   ```

2. **Find their website and look for**:
   - API docs link
   - Developer portal
   - GitHub repos with examples
   - Public API endpoints
   - Known integrations

3. **Fetch their API docs** using `WebFetch`:
   - Main documentation page
   - Swagger/OpenAPI spec (if available)
   - Example requests/responses

4. **Research chain support**:
   ```text
   Search: "[SwapperName] supported chains"
   Search: "[SwapperName] which blockchains"
   ```

5. **Find existing integrations**:
   ```text
   Search: "github [SwapperName] integration example"
   Search: "[SwapperName] typescript sdk"
   ```

**Then**, compile what you found and ask the user ONLY for what you couldn't find or need confirmation on.

---

### Phase 1: Information Gathering

**Use the `AskUserQuestion` tool to gather missing information with structured prompts.**

Based on your Phase 0 research, ask the user for:

1. **API Access** (if needed):
   - API key for production (or staging)
   - Any authentication requirements you found
   - Confirmation of API endpoints you discovered

2. **Chain Support Confirmation**:
   - Verify the chains you found are correct
   - Ask about any limitations or special requirements per chain
   - Confirm chain naming convention (ethereum vs 1 vs mainnet)

3. **Critical API Behaviors** (if not clear from docs):
   - **Slippage format**: percentage (1=1%), decimal (0.01=1%), or basis points (100=1%)?
   - **Address format**: checksummed required?
   - **Native token handling**: marker address? which one?
   - Min/max trade amounts?
   - Quote expiration time?

4. **Brand Assets**:
   - Confirm official name and capitalization
   - Request logo/icon (128x128+ PNG preferred)

5. **Known Issues**:
   - Any quirks they're aware of?
   - Previous integration attempts or examples?

**Example Multi-Question Prompt**:
```typescript
AskUserQuestion({
  questions: [
    {
      question: "Do we have an API key for [Swapper]?",
      header: "API Key",
      multiSelect: false,
      options: [
        { label: "Yes, I have it", description: "I'll provide the API key" },
        { label: "No, but we can get one", description: "I'll obtain an API key" },
        { label: "No API key needed", description: "API is public/unauthenticated" }
      ]
    },
    {
      question: "Which chains should we support initially?",
      header: "Chain Support",
      multiSelect: true,
      options: [
        { label: "Ethereum", description: "Ethereum mainnet" },
        { label: "Polygon", description: "Polygon PoS" },
        { label: "Arbitrum", description: "Arbitrum One" },
        { label: "All supported chains", description: "Enable all chains the API supports" }
      ]
    }
  ]
})
```

---

### Phase 2: Deep Research & Pattern Analysis

**IMPORTANT**: Study existing swappers BEFORE writing any code. This prevents reimplementing solved problems.

#### Step 1: Identify Swapper Category

Based on API research, determine the swapper type:

**EVM Direct Transaction** (Most Common):
- Characteristics: Single EVM chain, returns transaction data, user signs & broadcasts
- Examples: Bebop, 0x, Portals
- Key Files: `bebopTransactionMetadata`, `zrxTransactionMetadata`, `portalsTransactionMetadata`
- **Choose this if**: API returns `{to, data, value, gas}` transaction object

**Deposit-to-Address (Cross-Chain/Async)**:
- Characteristics: User sends to deposit address, swapper handles execution asynchronously
- Examples: Chainflip, NEAR Intents, THORChain
- Key Files: Uses `[swapper]Specific` metadata with `depositAddress`
- **Choose this if**: API returns deposit address and swap ID for tracking

**Gasless Order-Based**:
- Characteristics: Sign message not transaction, relayer executes, no gas
- Examples: CowSwap
- Key Files: Uses `cowswapQuoteResponse`, custom `executeEvmMessage`
- **Choose this if**: Uses EIP-712 message signing + order submission

**Solana-Only**:
- Characteristics: Solana transaction with instructions and ALTs
- Examples: Jupiter
- Key Files: `jupiterQuoteResponse`, `solanaTransactionMetadata`
- **Choose this if**: Solana ecosystem only

**Chain-Specific (Sui/Tron/etc.)**:
- Characteristics: Custom transaction format for specific blockchain
- Examples: Cetus (Sui)
- Key Files: Chain-specific adapters and transaction metadata
- **Choose this if**: Non-EVM, non-Solana blockchain with custom SDK

#### Step 2: Study 2-3 Similar Swappers IN DEPTH

**Read these files for your chosen swapper type**:

```bash
# For EVM Direct Transaction (e.g., Bebop):
packages/swapper/src/swappers/BebopSwapper/
├── BebopSwapper.ts                # Swapper interface (usually just executeEvmTransaction)
├── endpoints.ts                   # SwapperApi implementation
├── types.ts                       # API request/response types
├── getBebopTradeQuote/
│   └── getBebopTradeQuote.ts     # Quote logic (WITH fee estimation)
├── getBebopTradeRate/
│   └── getBebopTradeRate.ts      # Rate logic (withOUT wallet, may use dummy address)
└── utils/
    ├── constants.ts               # Supported chains, native marker, defaults
    ├── bebopService.ts            # HTTP client with cache + API key injection
    ├── fetchFromBebop.ts          # API wrappers (fetchQuote, fetchPrice)
    └── helpers/
        └── helpers.ts             # Validation, rate calc, address helpers
```

**Read these files for deposit-to-address (e.g., NEAR Intents)**:
```bash
packages/swapper/src/swappers/NearIntentsSwapper/
├── endpoints.ts                   # checkTradeStatus uses depositAddress from metadata
├── swapperApi/
│   ├── getTradeQuote.ts          # Stores depositAddress in nearIntentsSpecific
│   └── getTradeRate.ts
└── utils/
    ├── oneClickService.ts         # OneClick SDK initialization
    └── helpers/
        └── helpers.ts             # Asset mapping, status translation
```

**Critical things to note while reading**:
1. How do they call the API? (HTTP service pattern? SDK? Direct axios?)
2. How do they handle errors? (Monadic `Result<T, SwapErrorRight>` pattern)
3. How do they calculate rates? (`getInputOutputRate` util vs custom)
4. What metadata do they store in `TradeQuoteStep`?
5. How do they validate inputs? (Supported chains? Asset compatibility?)
6. How do they handle native tokens? (Marker address vs special field)
7. How do they convert API responses to our types?

#### Step 3: Review Common Patterns

### Key Pattern: Monadic Error Handling

```typescript
import { Err, Ok } from '@sniptt/monads'
import { makeSwapErrorRight } from '../../../utils'

// ALWAYS return Result<T, SwapErrorRight>, NEVER throw
const result = await someOperation()
if (result.isErr()) {
  return Err(makeSwapErrorRight({
    message: 'What went wrong',
    code: TradeQuoteError.QueryFailed,
    details: { context: 'here' }
  }))
}
return Ok(result.unwrap())
```

### Key Pattern: HTTP Service with Caching

```typescript
import { createCache, makeSwapperAxiosServiceMonadic } from '../../../utils'

const maxAge = 5 * 1000 // 5 seconds
const cachedUrls = ['/quote', '/price'] // which endpoints to cache

const serviceBase = createCache(maxAge, cachedUrls, {
  timeout: 10000,
  headers: {
    'Accept': 'application/json',
    'x-api-key': config.VITE_XYZ_API_KEY
  }
})

export const xyzService = makeSwapperAxiosServiceMonadic(serviceBase)
```

### Key Pattern: Rate Limiting and Throttling

For chain adapters and swappers that directly interact with RPC endpoints or APIs:

```typescript
import PQueue from 'p-queue'

// In constructor or module scope:
private requestQueue: PQueue = new PQueue({
  intervalCap: 1,    // 1 request per interval
  interval: 50,      // 50ms between requests
  concurrency: 1,    // 1 concurrent request at a time
})

// Wrap all external API/RPC calls:
const quote = await this.requestQueue.add(() =>
  swapperService.get('/quote', { params })
)

// For provider calls in chain adapters:
const balance = await this.requestQueue.add(() =>
  this.provider.getBalance(address)
)
```

**When to use**: Any swapper or chain adapter making direct RPC/API calls (especially public endpoints)
**Example implementations**: MonadChainAdapter, PlasmaChainAdapter

### Key Pattern: Rate Calculation

```typescript
import { getInputOutputRate } from '../../../utils'

const rate = getInputOutputRate({
  sellAmountCryptoBaseUnit,
  buyAmountCryptoBaseUnit,
  sellAsset,
  buyAsset
})
```

---

### Phase 3: Implementation (Step by Step)

Follow this EXACT order to avoid rework:

#### Step 1: Create Directory Structure

```bash
mkdir -p packages/swapper/src/swappers/[SwapperName]Swapper/{get[SwapperName]TradeQuote,get[SwapperName]TradeRate,utils/helpers}
```

**Standard structure** (EVM swappers):
```
[SwapperName]Swapper/
├── index.ts
├── [SwapperName]Swapper.ts
├── endpoints.ts
├── types.ts
├── get[SwapperName]TradeQuote/
│   └── get[SwapperName]TradeQuote.ts
├── get[SwapperName]TradeRate/
│   └── get[SwapperName]TradeRate.ts
└── utils/
    ├── constants.ts
    ├── [swapperName]Service.ts
    ├── fetchFrom[SwapperName].ts
    └── helpers/
        └── helpers.ts
```

#### Step 2: Implement Files in Order

**2a. `types.ts` - API TypeScript Types**

Define types EXACTLY matching the API response (log actual API responses to verify!):

```typescript
import type { Address, Hex } from 'viem'

// Request types
export type [Swapper]QuoteRequest = {
  sellToken: Address
  buyToken: Address
  sellAmount: string
  slippage: number  // NOTE: document what format! (percentage, decimal, basis points)
  takerAddress: Address
  receiverAddress?: Address
  chainId: number
}

// Response types (match API exactly!)
export type [Swapper]QuoteResponse = {
  // Copy structure from actual API response
  buyAmount: string
  sellAmount: string
  transaction: {
    to: Address
    data: Hex
    value: Hex
    gas?: Hex
  }
  // ... rest of response
}

// Constants
export const [SWAPPER]_SUPPORTED_CHAIN_IDS: Record<number, string> = {
  1: 'ethereum',
  137: 'polygon',
  42161: 'arbitrum',
  // ...
}
```

**2b. `utils/constants.ts` - Configuration**

```typescript
import type { AssetId, ChainId } from '@shapeshiftoss/caip'
import { ethChainId, polygonChainId, arbitrumChainId } from '@shapeshiftoss/caip'
import type { Address } from 'viem'

export const SUPPORTED_CHAIN_IDS = [
  ethChainId,
  polygonChainId,
  arbitrumChainId,
] as const

export type [Swapper]SupportedChainId = (typeof SUPPORTED_CHAIN_IDS)[number]

// Native token marker (if API uses one)
export const NATIVE_TOKEN_MARKER = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE' as Address

// Dummy address for rates (when no wallet connected)
export const DUMMY_ADDRESS = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045' as Address

// Default slippage if none provided
export const DEFAULT_SLIPPAGE_PERCENTAGE = '0.5' // 0.5%
```

**2c. `utils/helpers/helpers.ts` - Helper Functions**

```typescript
import { fromAssetId, type AssetId } from '@shapeshiftoss/caip'
import { isToken } from '@shapeshiftoss/utils'
import { getAddress, type Address } from 'viem'
import { NATIVE_TOKEN_MARKER, SUPPORTED_CHAIN_IDS } from '../constants'

// Check if chain is supported
export const isSupportedChainId = (chainId: string): boolean => {
  return SUPPORTED_CHAIN_IDS.includes(chainId as any)
}

// Convert assetId to token address (with native token handling)
export const assetIdToToken = (assetId: AssetId): Address => {
  if (!isToken(assetId)) {
    return NATIVE_TOKEN_MARKER // Native token (ETH, MATIC, etc.)
  }
  const { assetReference } = fromAssetId(assetId)
  return getAddress(assetReference) // Checksum ERC20 address
}

// Convert ShapeShift chainId to API chain identifier
export const chainIdToChainRef = (chainId: string): string => {
  switch (chainId) {
    case ethChainId:
      return 'ethereum' // or '1' or 'mainnet' depending on API
    case polygonChainId:
      return 'polygon'
    // ...
    default:
      throw new Error(`Unsupported chainId: ${chainId}`)
  }
}

// Calculate rate from amounts
import { getInputOutputRate } from '../../../../utils'
export { getInputOutputRate } // Re-export for use in quote/rate files
```

**2d. `utils/[swapperName]Service.ts` - HTTP Service**

```typescript
import { createCache, makeSwapperAxiosServiceMonadic } from '../../../utils'
import type { SwapperConfig } from '../../../types'

// Cache for 5 seconds (adjust based on API)
const maxAge = 5 * 1000

// Which endpoints to cache (usually /quote and /price)
const cachedUrls = ['/quote', '/price']

export const [swapperName]ServiceFactory = (config: SwapperConfig) => {
  const axiosConfig = {
    timeout: 10000,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      ...(config.VITE_[SWAPPER]_API_KEY && {
        'x-api-key': config.VITE_[SWAPPER]_API_KEY
      })
    }
  }

  const serviceBase = createCache(maxAge, cachedUrls, axiosConfig)
  return makeSwapperAxiosServiceMonadic(serviceBase)
}

export type [Swapper]Service = ReturnType<typeof [swapperName]ServiceFactory>
```

**2e. `utils/fetchFrom[SwapperName].ts` - API Wrappers**

```typescript
import { type AssetId } from '@shapeshiftoss/caip'
import { bn } from '@shapeshiftoss/utils'
import { Err, Ok, type Result } from '@sniptt/monads'
import { getAddress, type Address } from 'viem'
import { makeSwapErrorRight } from '../../../utils'
import { TradeQuoteError, type SwapErrorRight } from '../../../types'
import type { [Swapper]Service } from './[swapperName]Service'
import type { [Swapper]QuoteRequest, [Swapper]QuoteResponse } from '../types'
import { assetIdToToken, chainIdToChainRef } from './helpers/helpers'

// Base URL for API
const BASE_URL = 'https://api.[swapper].com'

export type FetchQuoteParams = {
  sellAssetId: AssetId
  buyAssetId: AssetId
  sellAmountCryptoBaseUnit: string
  chainId: string
  takerAddress: string
  receiverAddress: string
  slippageTolerancePercentageDecimal: string
  affiliateBps: string
}

export const fetchQuote = async (
  params: FetchQuoteParams,
  service: [Swapper]Service
): Promise<Result<[Swapper]QuoteResponse, SwapErrorRight>> => {
  try {
    const {
      sellAssetId,
      buyAssetId,
      sellAmountCryptoBaseUnit,
      chainId,
      takerAddress,
      receiverAddress,
      slippageTolerancePercentageDecimal,
      affiliateBps
    } = params

    // Convert to API format
    const sellToken = assetIdToToken(sellAssetId)
    const buyToken = assetIdToToken(buyAssetId)
    const chainRef = chainIdToChainRef(chainId)

    // CRITICAL: Convert slippage to API format
    // ShapeShift format: 0.005 = 0.5%
    // Check API docs for their format!
    const slippagePercentage = bn(slippageTolerancePercentageDecimal)
      .times(100) // If API expects 0.5 for 0.5%
      .toNumber()

    // Checksum addresses (CRITICAL for many APIs)
    const checksummedTakerAddress = getAddress(takerAddress)
    const checksummedReceiverAddress = getAddress(receiverAddress)

    const requestBody: [Swapper]QuoteRequest = {
      sellToken,
      buyToken,
      sellAmount: sellAmountCryptoBaseUnit,
      slippage: slippagePercentage,
      takerAddress: checksummedTakerAddress,
      receiverAddress: checksummedReceiverAddress,
      chainId: chainRef,
      // Add affiliate if supported
      ...(affiliateBps !== '0' && { affiliateBps })
    }

    const maybeResponse = await service.post<[Swapper]QuoteResponse>(
      `${BASE_URL}/quote`,
      requestBody
    )

    if (maybeResponse.isErr()) {
      return Err(maybeResponse.unwrapErr())
    }

    const { data: response } = maybeResponse.unwrap()

    // Validate response has required fields
    if (!response.buyAmount || !response.transaction) {
      return Err(
        makeSwapErrorRight({
          message: 'Invalid response from API',
          code: TradeQuoteError.InvalidResponse,
          details: { response }
        })
      )
    }

    return Ok(response)
  } catch (error) {
    return Err(
      makeSwapErrorRight({
        message: 'Failed to fetch quote',
        code: TradeQuoteError.QueryFailed,
        cause: error
      })
    )
  }
}

// For rates (no wallet needed)
export type FetchPriceParams = Omit<FetchQuoteParams, 'takerAddress' | 'receiverAddress'> & {
  receiveAddress: string | undefined
}

export const fetchPrice = async (
  params: FetchPriceParams,
  service: [Swapper]Service
): Promise<Result<[Swapper]QuoteResponse, SwapErrorRight>> => {
  // Use dummy address if no wallet connected
  const address = params.receiveAddress
    ? getAddress(params.receiveAddress)
    : DUMMY_ADDRESS

  // IMPORTANT: Use same affiliate for both quote and rate to avoid delta!
  return fetchQuote(
    {
      ...params,
      takerAddress: address,
      receiverAddress: address
    },
    service
  )
}
```

**2f. `get[SwapperName]TradeQuote/get[SwapperName]TradeQuote.ts` - Quote Logic**

This is the MEAT of the implementation. It must:
1. Validate inputs (chain support, asset compatibility)
2. Fetch quote from API
3. Estimate network fees using chain adapter
4. Build complete TradeQuote object with all required fields
5. Handle errors monadic-ally

```typescript
import { type AssetId } from '@shapeshiftoss/caip'
import { bn } from '@shapeshiftoss/utils'
import { Err, Ok, type Result } from '@sniptt/monads'
import { makeSwapErrorRight } from '../../../utils'
import {
  type CommonTradeQuoteInput,
  type GetEvmTradeQuoteInput,
  type SwapErrorRight,
  type SwapperDeps,
  type TradeQuote,
  TradeQuoteError
} from '../../../types'
import { fetchQuote } from '../utils/fetchFromBebop'
import { [swapperName]ServiceFactory } from '../utils/[swapperName]Service'
import {
  getInputOutputRate,
  isSupportedChainId
} from '../utils/helpers/helpers'
import { DUMMY_ADDRESS } from '../utils/constants'

export const get[SwapperName]TradeQuote = async (
  input: GetEvmTradeQuoteInput | CommonTradeQuoteInput,
  deps: SwapperDeps
): Promise<Result<TradeQuote, SwapErrorRight>> => {
  try {
    const {
      sellAsset,
      buyAsset,
      sellAmountIncludingProtocolFeesCryptoBaseUnit,
      sendAddress,
      receiveAddress,
      accountNumber,
      affiliateBps,
      slippageTolerancePercentageDecimal
    } = input

    const { config, assertGetEvmChainAdapter } = deps

    // Validation: Check chain support
    if (!isSupportedChainId(sellAsset.chainId)) {
      return Err(
        makeSwapErrorRight({
          message: `[${SwapperName.[SwapperName]}] Unsupported chainId: ${sellAsset.chainId}`,
          code: TradeQuoteError.UnsupportedChain,
          details: { chainId: sellAsset.chainId }
        })
      )
    }

    // Validation: Must be same chain
    if (sellAsset.chainId !== buyAsset.chainId) {
      return Err(
        makeSwapErrorRight({
          message: `[${SwapperName.[SwapperName]}] Cross-chain not supported`,
          code: TradeQuoteError.CrossChainNotSupported
        })
      )
    }

    // Validation: Prevent executable quotes with dummy address
    const takerAddress = sendAddress ?? receiveAddress
    if (takerAddress === DUMMY_ADDRESS) {
      return Err(
        makeSwapErrorRight({
          message: 'Cannot execute trade with dummy address',
          code: TradeQuoteError.UnknownError
        })
      )
    }

    // Fetch quote from API
    const service = [swapperName]ServiceFactory(config)
    const maybeQuoteResponse = await fetchQuote(
      {
        sellAssetId: sellAsset.assetId,
        buyAssetId: buyAsset.assetId,
        sellAmountCryptoBaseUnit: sellAmountIncludingProtocolFeesCryptoBaseUnit,
        chainId: sellAsset.chainId,
        takerAddress,
        receiverAddress: receiveAddress,
        slippageTolerancePercentageDecimal:
          slippageTolerancePercentageDecimal ?? DEFAULT_SLIPPAGE_PERCENTAGE,
        affiliateBps
      },
      service
    )

    if (maybeQuoteResponse.isErr()) {
      return Err(maybeQuoteResponse.unwrapErr())
    }

    const quoteResponse = maybeQuoteResponse.unwrap()

    // Get chain adapter for fee estimation
    const adapter = assertGetEvmChainAdapter(sellAsset.chainId)

    // Estimate network fees
    const { average: { gasPrice } } = await adapter.getGasFeeData()

    const networkFeeCryptoBaseUnit = bn(quoteResponse.transaction.gas ?? '0')
      .times(gasPrice)
      .toFixed(0)

    // Calculate rate
    const rate = getInputOutputRate({
      sellAmountCryptoBaseUnit: sellAmountIncludingProtocolFeesCryptoBaseUnit,
      buyAmountCryptoBaseUnit: quoteResponse.buyAmount,
      sellAsset,
      buyAsset
    })

    // Build TradeQuote
    const tradeQuote: TradeQuote = {
      id: crypto.randomUUID(),
      quoteOrRate: 'quote',
      rate,
      slippageTolerancePercentageDecimal,
      receiveAddress,
      affiliateBps,
      steps: [
        {
          buyAmountBeforeFeesCryptoBaseUnit: quoteResponse.buyAmount,
          buyAmountAfterFeesCryptoBaseUnit: quoteResponse.buyAmount, // or minus protocol fees
          sellAmountIncludingProtocolFeesCryptoBaseUnit,
          feeData: {
            networkFeeCryptoBaseUnit,
            protocolFees: {}, // or add protocol fees if any
          },
          rate,
          source: SwapperName.[SwapperName],
          buyAsset,
          sellAsset,
          accountNumber,
          allowanceContract: isNativeEvmAsset(sellAsset.assetId)
            ? undefined
            : quoteResponse.approvalTarget, // or constant approval contract
          estimatedExecutionTimeMs: undefined, // or from API
          // Store transaction metadata
          [swapperName]TransactionMetadata: {
            to: quoteResponse.transaction.to,
            data: quoteResponse.transaction.data,
            value: quoteResponse.transaction.value,
            gas: quoteResponse.transaction.gas
          }
        }
      ],
      swapperName: SwapperName.[SwapperName]
    }

    return Ok(tradeQuote)
  } catch (error) {
    return Err(
      makeSwapErrorRight({
        message: 'Failed to get trade quote',
        code: TradeQuoteError.UnknownError,
        cause: error
      })
    )
  }
}
```

**2g. `get[SwapperName]TradeRate/get[SwapperName]TradeRate.ts` - Rate Logic**

Similar to quote but:
- No wallet address required (use dummy or undefined)
- accountNumber is undefined
- May skip network fee estimation (or use cached/estimated)

```typescript
import { Err, Ok, type Result } from '@sniptt/monads'
import { makeSwapErrorRight } from '../../../utils'
import {
  type GetTradeRateInput,
  type SwapErrorRight,
  type SwapperDeps,
  type TradeRate,
  TradeQuoteError
} from '../../../types'
import { fetchPrice } from '../utils/fetchFromBebop'
import { [swapperName]ServiceFactory } from '../utils/[swapperName]Service'
import { getInputOutputRate, isSupportedChainId } from '../utils/helpers/helpers'
import { DEFAULT_SLIPPAGE_PERCENTAGE } from '../utils/constants'

export const get[SwapperName]TradeRate = async (
  input: GetTradeRateInput,
  deps: SwapperDeps
): Promise<Result<TradeRate, SwapErrorRight>> => {
  try {
    const {
      sellAsset,
      buyAsset,
      sellAmountIncludingProtocolFeesCryptoBaseUnit,
      receiveAddress,
      affiliateBps,
      slippageTolerancePercentageDecimal
    } = input

    const { config } = deps

    // Same validation as quote
    if (!isSupportedChainId(sellAsset.chainId)) {
      return Err(
        makeSwapErrorRight({
          message: `[${SwapperName.[SwapperName]}] Unsupported chainId: ${sellAsset.chainId}`,
          code: TradeQuoteError.UnsupportedChain
        })
      )
    }

    if (sellAsset.chainId !== buyAsset.chainId) {
      return Err(
        makeSwapErrorRight({
          message: `[${SwapperName.[SwapperName]}] Cross-chain not supported`,
          code: TradeQuoteError.CrossChainNotSupported
        })
      )
    }

    // Fetch rate (uses dummy address if no receiveAddress)
    const service = [swapperName]ServiceFactory(config)
    const maybeRateResponse = await fetchPrice(
      {
        sellAssetId: sellAsset.assetId,
        buyAssetId: buyAsset.assetId,
        sellAmountCryptoBaseUnit: sellAmountIncludingProtocolFeesCryptoBaseUnit,
        chainId: sellAsset.chainId,
        receiveAddress,
        slippageTolerancePercentageDecimal:
          slippageTolerancePercentageDecimal ?? DEFAULT_SLIPPAGE_PERCENTAGE,
        affiliateBps
      },
      service
    )

    if (maybeRateResponse.isErr()) {
      return Err(maybeRateResponse.unwrapErr())
    }

    const rateResponse = maybeRateResponse.unwrap()

    // Calculate rate
    const rate = getInputOutputRate({
      sellAmountCryptoBaseUnit: sellAmountIncludingProtocolFeesCryptoBaseUnit,
      buyAmountCryptoBaseUnit: rateResponse.buyAmount,
      sellAsset,
      buyAsset
    })

    // Build TradeRate (similar to quote but accountNumber = undefined)
    const tradeRate: TradeRate = {
      id: crypto.randomUUID(),
      quoteOrRate: 'rate',
      rate,
      slippageTolerancePercentageDecimal,
      receiveAddress,
      affiliateBps,
      steps: [
        {
          buyAmountBeforeFeesCryptoBaseUnit: rateResponse.buyAmount,
          buyAmountAfterFeesCryptoBaseUnit: rateResponse.buyAmount,
          sellAmountIncludingProtocolFeesCryptoBaseUnit,
          feeData: {
            networkFeeCryptoBaseUnit: undefined, // Unknown for rate
            protocolFees: {}
          },
          rate,
          source: SwapperName.[SwapperName],
          buyAsset,
          sellAsset,
          accountNumber: undefined, // CRITICAL: Must be undefined for rate
          allowanceContract: isNativeEvmAsset(sellAsset.assetId)
            ? undefined
            : rateResponse.approvalTarget,
          estimatedExecutionTimeMs: undefined
        }
      ],
      swapperName: SwapperName.[SwapperName]
    }

    return Ok(tradeRate)
  } catch (error) {
    return Err(
      makeSwapErrorRight({
        message: 'Failed to get trade rate',
        code: TradeQuoteError.UnknownError,
        cause: error
      })
    )
  }
}
```

**2h. `endpoints.ts` - SwapperApi Implementation**

```typescript
import { isNativeEvmAsset } from '@shapeshiftoss/utils'
import { bn } from '@shapeshiftoss/utils'
import { fromHex, type Hex } from 'viem'
import { checkEvmSwapStatus } from '../../utils'
import type {
  CommonTradeQuoteInput,
  GetEvmTradeQuoteInput,
  GetTradeRateInput,
  GetUnsignedEvmTransactionArgs,
  SwapperApi,
  SwapperDeps,
  TradeQuote,
  TradeRate,
  TradeQuoteResult,
  TradeRateResult
} from '../../types'
import { get[SwapperName]TradeQuote } from './get[SwapperName]TradeQuote/get[SwapperName]TradeQuote'
import { get[SwapperName]TradeRate } from './get[SwapperName]TradeRate/get[SwapperName]TradeRate'

export const [swapperName]Api: SwapperApi = {
  getTradeQuote: async (
    input: GetEvmTradeQuoteInput | CommonTradeQuoteInput,
    deps: SwapperDeps
  ): Promise<TradeQuoteResult> => {
    const maybeTradeQuote = await get[SwapperName]TradeQuote(input, deps)
    return maybeTradeQuote.map(quote => [quote])
  },

  getTradeRate: async (
    input: GetTradeRateInput,
    deps: SwapperDeps
  ): Promise<TradeRateResult> => {
    const maybeTradeRate = await get[SwapperName]TradeRate(input, deps)
    return maybeTradeRate.map(rate => [rate])
  },

  getUnsignedEvmTransaction: async (
    args: GetUnsignedEvmTransactionArgs
  ) => {
    const {
      tradeQuote,
      chainId,
      from,
      stepIndex,
      assertGetEvmChainAdapter
    } = args

    const step = tradeQuote.steps[stepIndex]
    const metadata = step.[swapperName]TransactionMetadata

    if (!metadata) {
      throw new Error('Missing transaction metadata')
    }

    const adapter = assertGetEvmChainAdapter(chainId)

    // Convert hex values to decimal strings (CRITICAL!)
    const value = metadata.value
      ? fromHex(metadata.value as Hex, 'bigint').toString()
      : '0'

    const gasLimit = metadata.gas
      ? fromHex(metadata.gas as Hex, 'bigint').toString()
      : undefined

    // Build EVM transaction
    return {
      chainId: Number(fromChainId(chainId).chainReference),
      to: metadata.to,
      from,
      data: metadata.data,
      value,
      gasLimit, // or use adapter.getFeeData() if not provided
    }
  },

  getEvmTransactionFees: async (args: GetUnsignedEvmTransactionArgs) => {
    const { tradeQuote, chainId, assertGetEvmChainAdapter, stepIndex } = args

    const step = tradeQuote.steps[stepIndex]
    const adapter = assertGetEvmChainAdapter(chainId)

    // Get current gas price
    const { average: { gasPrice } } = await adapter.getGasFeeData()

    // Use API gas estimate or node estimate
    const metadata = step.[swapperName]TransactionMetadata
    const apiGasEstimate = metadata?.gas
      ? fromHex(metadata.gas as Hex, 'bigint').toString()
      : '0'

    // Take max of API and node estimates (with buffer)
    const networkFeeCryptoBaseUnit = bn
      .max(step.feeData.networkFeeCryptoBaseUnit ?? '0', apiGasEstimate)
      .times(1.15) // 15% buffer
      .toFixed(0)

    return networkFeeCryptoBaseUnit
  },

  checkTradeStatus: checkEvmSwapStatus // Standard EVM status check
}
```

**2i. `[SwapperName]Swapper.ts` - Swapper Interface**

For most EVM swappers, this is simple:

```typescript
import { executeEvmTransaction } from '../utils'
import type { Swapper } from '../../types'

export const [swapperName]Swapper: Swapper = {
  executeEvmTransaction
}
```

For deposit-to-address or custom execution, implement custom logic here.

**2j. `index.ts` - Exports**

```typescript
export { [swapperName]Api } from './endpoints'
export { [swapperName]Swapper } from './[SwapperName]Swapper'
export * from './types'
export * from './utils/constants'
```

#### Step 3: Add Swapper-Specific Metadata (ONLY if needed!)

**Skip this step if your swapper is a direct transaction swapper** (like Bebop, 0x, Portals).

**Implement this step if**:
- Swapper uses deposit-to-address model (Chainflip, NEAR Intents)
- Need to track order IDs or swap IDs between quote and execution
- Status polling requires data beyond transaction hash

**Three places to modify**:

**a. `packages/swapper/src/types.ts` - Add to TradeQuoteStep**:
```typescript
export type TradeQuoteStep = {
  // ... existing fields
  [swapperName]Specific?: {
    depositAddress: string
    swapId: string | number
    memo?: string
    deadline?: string
    // ... other tracking fields
  }
}
```

**b. `packages/swapper/src/types.ts` - Add to SwapperSpecificMetadata**:
```typescript
export type SwapperSpecificMetadata = {
  chainflipSwapId: number | undefined
  nearIntentsSpecific?: { ... }
  // Add your swapper:
  [swapperName]Specific?: {
    depositAddress: string
    swapId: string | number
    memo?: string
    deadline?: string
  }
  relayTransactionMetadata: RelayTransactionMetadata | undefined
  // ...
}
```

**c. Populate in quote** (`get[SwapperName]TradeQuote.ts`):
```typescript
const tradeQuote: TradeQuote = {
  // ...
  steps: [{
    // ...
    [swapperName]Specific: {
      depositAddress: quoteResponse.depositAddress,
      swapId: quoteResponse.id,
      memo: quoteResponse.memo,
      deadline: quoteResponse.deadline
    }
  }]
}
```

**d. Extract into swap** (TWO places - BOTH required!):

**Place 1**: `src/components/MultiHopTrade/components/TradeConfirm/hooks/useTradeButtonProps.tsx`
```typescript
// Around line 114-126
metadata: {
  chainflipSwapId: firstStep?.chainflipSpecific?.chainflipSwapId,
  nearIntentsSpecific: firstStep?.nearIntentsSpecific,
  [swapperName]Specific: firstStep?.[swapperName]Specific, // ADD THIS
  relayTransactionMetadata: firstStep?.relayTransactionMetadata,
  // ...
}
```

**Place 2**: `src/lib/tradeExecution.ts`
```typescript
// Around line 156-161
metadata: {
  ...swap.metadata,
  chainflipSwapId: tradeQuote.steps[0]?.chainflipSpecific?.chainflipSwapId,
  nearIntentsSpecific: tradeQuote.steps[0]?.nearIntentsSpecific,
  [swapperName]Specific: tradeQuote.steps[0]?.[swapperName]Specific, // ADD THIS
  relayTransactionMetadata: tradeQuote.steps[0]?.relayTransactionMetadata,
  // ...
}
```

**e. Use in status check** (`endpoints.ts`):
```typescript
checkTradeStatus: async ({ swap, config }) => {
  const { [swapperName]Specific } = swap?.metadata ?? {}

  if (![swapperName]Specific?.depositAddress) {
    throw new Error('Missing depositAddress in swap metadata')
  }

  // Poll API using metadata
  const status = await pollSwapStatus(
    [swapperName]Specific.depositAddress,
    [swapperName]Specific.swapId,
    config
  )

  return {
    status: mapApiStatusToTxStatus(status.state),
    buyTxHash: status.outputTxHash,
    message: status.message
  }
}
```

#### Step 4: Register the Swapper

**4a. `packages/swapper/src/types.ts` - Add Config Fields**

```typescript
export type SwapperConfig = {
  // ... existing fields
  VITE_[SWAPPER]_API_KEY: string
  VITE_[SWAPPER]_BASE_URL?: string // if configurable
}
```

**4b. `packages/swapper/src/constants.ts` - Register Swapper**

```typescript
export enum SwapperName {
  // ... existing
  [SwapperName] = '[Display Name]',
}

export const swappers: Record<SwapperName, { swapper: Swapper; swapperApi: SwapperApi }> = {
  // ... existing
  [SwapperName.[SwapperName]]: {
    swapper: [swapperName]Swapper,
    swapperApi: [swapperName]Api
  }
}

export const DEFAULT_SLIPPAGE_DECIMAL_PERCENTAGE_BY_SWAPPER: Record<
  SwapperName,
  string | undefined
> = {
  // ... existing
  [SwapperName.[SwapperName]]: '0.005', // 0.5%
}
```

**4c. `packages/swapper/src/index.ts` - Export**

```typescript
export { [swapperName]Api, [swapperName]Swapper } from './swappers/[SwapperName]Swapper'
```

**4d. CSP Headers** (if swapper calls external API)

Create `headers/csps/defi/swappers/[SwapperName].ts`:
```typescript
import type { Csp } from '../../../types'

export const csp: Csp = {
  'connect-src': [
    'https://api.[swapper].com',
    'https://api.[swapper].io', // add all API domains
  ]
}
```

Register in `headers/csps/index.ts`:
```typescript
import { csp as [swapperName] } from './defi/swappers/[SwapperName]'

export const csps = [
  // ... other csps
  [swapperName],
]
```

#### 4e. UI - Feature Flag

Add to `src/state/slices/preferencesSlice/preferencesSlice.ts`:
```typescript
export type FeatureFlags = {
  // ... existing
  BebopSwap: boolean  // Example: use PascalCase swapper name + "Swap" suffix
}

const initialState: Preferences = {
  featureFlags: {
    // ... existing
    BebopSwap: getConfig().VITE_FEATURE_BEBOP_SWAP
  }
}
```

#### 4f. Wire Feature Flag

In `src/state/helpers.ts`:

Add to `isCrossAccountTradeSupported` (if supported):
```typescript
export const isCrossAccountTradeSupported = (swapperName: SwapperName): boolean => {
  switch (swapperName) {
    case SwapperName.Bebop:  // Use enum value, not placeholder
      return true // or false if not supported
    // ...
  }
}
```

Add to `getEnabledSwappers`:
```typescript
export const getEnabledSwappers = (
  {
    BebopSwap,  // ADD THIS - destructure the flag directly
    // ... other existing flags like ChainflipSwap, ThorSwap, etc.
  }: FeatureFlags,
  isCrossAccountTrade: boolean,
  isSolBuyAssetId: boolean
): Record<SwapperName, boolean> => {
  return {
    // ... existing
    [SwapperName.Bebop]:
      BebopSwap &&
      (!isCrossAccountTrade || isCrossAccountTradeSupported(SwapperName.Bebop))
  }
}
```

#### 4g. Test Mocks

In `src/test/mocks/store.ts`:

```typescript
featureFlags: {
  // ... existing
  BebopSwap: false  // Use actual flag name, not placeholder
}
```

#### 4h. Swapper Icon

In UI:

Add icon: `src/components/MultiHopTrade/components/TradeInput/components/SwapperIcon/[swapper]-icon.png`

Update `SwapperIcon.tsx`:
```typescript
import [swapperName]Icon from './[swapper]-icon.png'

const SwapperIcon = ({ swapperName }: Props) => {
  switch (swapperName) {
    // ... existing
    case SwapperName.[SwapperName]:
      return <Image src={[swapperName]Icon} />
  }
}
```

#### 4i. Environment Variables

`.env` (production - both OFF):
```bash
# [Swapper Name]
VITE_[SWAPPER]_API_KEY=
VITE_FEATURE_[SWAPPER]_SWAP=false
```

`.env.development` (development - flag ON):
```bash
# [Swapper Name]
VITE_[SWAPPER]_API_KEY=your-dev-api-key-here
VITE_FEATURE_[SWAPPER]_SWAP=true
```

Add to `src/config.ts`:
```typescript
export const getConfig = (): Config => ({
  // ... existing
  VITE_[SWAPPER]_API_KEY: import.meta.env.VITE_[SWAPPER]_API_KEY || '',
  VITE_FEATURE_[SWAPPER]_SWAP: parseBoolean(import.meta.env.VITE_FEATURE_[SWAPPER]_SWAP)
})
```

#### Step 5: Proactive Gotcha Review

**BEFORE testing**, check for these critical bugs:

1. **Slippage Format**: Verify API format (percentage, decimal, basis points)
2. **Address Checksumming**: Use `getAddress()` from viem
3. **Hex Conversion**: Use `fromHex()` for `tx.value`, `tx.gas`, `tx.gasPrice`
4. **Response Parsing**: Log actual API response, verify structure matches types
5. **Affiliate Fees**: Pass same `affiliateBps` to BOTH quote and rate endpoints
6. **Native Token Marker**: Verify marker address matches API requirements
7. **Gas Estimation**: Take max of API and node estimates, add buffer
8. **Dummy Address**: Block executable quotes with dummy address
9. **Error Handling**: Don't reject quote if some routes fail (e.g., dual routing)
10. **Type Safety**: Use `Address` and `Hex` types from viem, not strings

---

### Phase 4: Testing & Validation

**4a. Automated Checks**

```bash
# Type checking (MUST pass)
yarn type-check

# Linting (MUST pass)
yarn lint

# Build swapper package (MUST pass)
yarn build:swapper

# Build web (SHOULD pass, may have unrelated errors)
yarn build:web
```

Fix ALL type errors and lint errors before manual testing.

**4b. Manual Testing Checklist**

- [ ] Can fetch quotes for supported chain
- [ ] Rates display without wallet connected
- [ ] Approval flow works (if needed)
- [ ] Can execute swap and transaction succeeds
- [ ] Native token swaps work (ETH→USDC, USDC→ETH)
- [ ] Wrapped token swaps work (WETH→USDC)
- [ ] Error handling works (unsupported chain, insufficient liquidity)
- [ ] UI shows swapper icon correctly
- [ ] Feature flag toggles swapper on/off
- [ ] Cross-account trades work (if supported)
- [ ] Rate vs quote delta < 0.1%

**4c. Edge Cases**

- [ ] Very small amounts (near minimum)
- [ ] Very large amounts (near maximum)
- [ ] High slippage scenarios
- [ ] Low liquidity pairs
- [ ] Gas price spikes
- [ ] API timeouts/errors

---

### Phase 5: Documentation

Create `packages/swapper/src/swappers/[SwapperName]Swapper/INTEGRATION.md`:

```markdown
# [Swapper Name] Integration

## Overview
- **Website**: https://[swapper].com
- **API Docs**: https://docs.[swapper].com
- **Supported Chains**: Ethereum, Polygon, Arbitrum, ...
- **Type**: EVM Direct Transaction / Deposit-to-Address / Gasless

## API Details
- **Base URL**: `https://api.[swapper].com`
- **Authentication**: API key in `x-api-key` header
- **Rate Limiting**: X requests per second
- **Endpoints**:
  - `POST /quote` - Get executable quote
  - `GET /price` - Get rate without wallet

## Implementation Notes

### Slippage Format
API expects **percentage** (1 = 1%). ShapeShift internal format is decimal (0.01 = 1%), so we multiply by 100.

### Address Format
API requires **EIP-55 checksummed** addresses. We use `getAddress()` from viem.

### Native Token Handling
API uses marker address `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` for native tokens (ETH, MATIC, etc.).

### Response Format
```json
{
  "buyAmount": "1000000",
  "sellAmount": "500000000",
  "transaction": {
    "to": "0x...",
    "data": "0x...",
    "value": "0x0",
    "gas": "0x5208"
  }
}
```

### Gotchas
1. Gas estimates are in **hex**, must convert to decimal with `fromHex()`
2. Affiliate fees must be passed to BOTH `/quote` and `/price` to avoid rate delta
3. Some routes may fail (dual routing), this is normal - use `bestPrice` route

## Testing Notes
- Use USDC/USDT pairs for testing (high liquidity)
- Test both native (ETH) and ERC20 swaps
- Verify slippage is applied correctly (check on-chain vs quoted amount)

## Known Issues
- None currently

## References
- [API Docs](https://docs.[swapper].com)
- [Example Integration](https://github.com/example/integration)
```

---

## Critical Success Factors

1. **Research First**: Understand API thoroughly BEFORE coding
2. **Copy Patterns**: Adapt proven patterns from similar swappers
3. **Type Safety**: Use strict TypeScript types, avoid `any`
4. **Monadic Errors**: ALWAYS return `Result<T, SwapErrorRight>`, never throw
5. **Test Gotchas**: Proactively fix known bugs (slippage, checksumming, hex conversion)
6. **Feature Flag**: Always behind flag for gradual rollout
7. **Documentation**: Write INTEGRATION.md with quirks and gotchas

## Completion Checklist

Before considering integration complete:

**Code Quality**:
- [ ] All type checks pass (`yarn type-check`)
- [ ] All lint checks pass (`yarn lint`)
- [ ] Build succeeds (`yarn build:swapper`)
- [ ] No `any` types used
- [ ] All errors handled monadically

**Functionality**:
- [ ] Can fetch quotes successfully
- [ ] Can fetch rates without wallet
- [ ] Approval flow works (if needed)
- [ ] Transaction execution succeeds
- [ ] Status polling works (if applicable)
- [ ] Native token swaps work
- [ ] Error cases handled gracefully

**Integration**:
- [ ] Registered in constants.ts
- [ ] Exported from index.ts
- [ ] CSP headers added
- [ ] Feature flag implemented
- [ ] Test mocks updated
- [ ] Swapper icon added to UI
- [ ] Environment variables configured

**Documentation**:
- [ ] INTEGRATION.md created
- [ ] API quirks documented
- [ ] Known issues listed
- [ ] Testing notes included

**Testing**:
- [ ] Manual testing completed
- [ ] Rate vs quote delta verified (< 0.1%)
- [ ] Cross-account trades tested (if supported)
- [ ] Edge cases tested (min/max amounts, errors)

## Common Errors & Solutions

**"Taker address not checksummed"**
→ Use `getAddress(address)` from viem before sending to API

**"Number '0x...' is not a valid decimal"**
→ Convert hex to decimal: `fromHex(value as Hex, 'bigint').toString()`

**"Sell amount lower than fee"**
→ Check response parsing, likely accessing wrong field structure

**Large rate vs quote delta**
→ Pass same `affiliateBps` to both `/quote` and `/price` endpoints

**"$0 showing in UI"**
→ Response parsing bug, log actual response and verify structure

**"Transaction fails with slippage exceeded"**
→ Wrong slippage format sent to API (check docs for percentage/decimal/bps)

**Type error: "Property 'xyz' does not exist on type"**
→ Define proper TypeScript types matching actual API response

**"Cannot read property 'chainId' of undefined"**
→ Check null safety, add optional chaining or validation

---

## Need Help?

1. Read similar swapper implementations in packages/swapper/src/swappers/
2. Review the gotchas and patterns documented throughout this skill
3. Grep for similar patterns: `grep -r "pattern" packages/swapper/src/swappers/`
4. Ask user for API behavior clarification
5. Test with curl to verify API responses

---

**Remember**: Most bugs come from assumptions about API behavior. ALWAYS verify with actual API calls and log responses!
