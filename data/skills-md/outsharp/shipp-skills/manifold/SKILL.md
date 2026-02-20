---
name: manifold
description: >
  Manifold is a prediction market platform where users trade on the outcomes
  of real-world events using play-money (mana) and prize-cash. Use this skill
  to interact with the Manifold API for market discovery, trading, market
  creation, portfolio management, WebSocket streaming, and comments.

metadata:
  author: Outsharp Inc.
  version: 0.1.0

compatibility:
  requirements:
    - Internet access
    - Any HTTP client (curl, Python requests, fetch, etc.)
  notes:
    - Most read endpoints are public and require no authentication.
    - All write endpoints require an API key passed via the `Authorization: Key {key}` header.
    - Requests and responses are JSON.
    - All timestamps are UNIX milliseconds (JavaScript-style).
    - In the codebase and API, a "question" is called a "contract" (or sometimes "market"), and a "topic" is called a "group".
    - Mana (M$) is play-money. Some markets use prize-cash (CASH) which has real monetary value.

allowed-tools:
  - Bash(curl:*)
  - Bash(jq:*)
  - Bash(python*:*)
  - Bash(pip*:*)
  - Bash(npm*:*)
  - Bash(npx*:*)

---

# Manifold API

[Manifold](https://manifold.markets) is a prediction market platform where users create and trade on questions about real-world events. It uses a combination of play-money (mana) and prize-cash, with automated market makers (CPMM) and a rich API for programmatic access.

Check this skill and the [official documentation](https://docs.manifold.markets/api) _FREQUENTLY_ for updates. The API is still in alpha and may change without notice.

> **Community:** Join the [Manifold Discord](https://discord.com/invite/eHQBNBqXuh) for questions, bug reports, and to share what you build.

> **Source code:** Manifold is open source. Type definitions live at [common/src/api/schema.ts](https://github.com/manifoldmarkets/manifold/tree/main/common/src/api/schema.ts).

---

## Key Concepts (Glossary)

| Term | Definition |
|---|---|
| **Market** (Contract) | A single tradeable question. Called "contract" in the codebase, "market" in the API. Has an outcome type (BINARY, MULTIPLE_CHOICE, PSEUDO_NUMERIC, BOUNTIED_QUESTION, POLL). |
| **Mana (M$)** | Play-money currency used for most markets. Cannot be withdrawn for real money. |
| **Prize Cash (CASH)** | Real-money currency available on select markets. Can be withdrawn. Identified by `token: "CASH"` on a market. |
| **Sibling Contract** | The mana or prize-cash counterpart of a market. Toggle between them via `siblingContractId`. |
| **Topic (Group)** | A tag applied to markets for categorization. Called "group" in the codebase and API. |
| **CPMM** | Constant Product Market Maker. The automated market maker used for binary (`cpmm-1`) and multi-answer (`cpmm-multi-1`) markets. |
| **DPM** | Dynamic Parimutuel Market — a legacy mechanism (`dpm-2`) used for older free-response markets. |
| **Probability** | A number between 0 and 1 representing the market's current implied probability of YES. |
| **Pool** | The liquidity pool of shares backing the market maker. For CPMM markets, shows YES and NO share counts. |
| **Liquidity** | Mana deposited into the AMM pool. More liquidity means less price impact per trade. |
| **Bet** | A trade on a market. Can be a market order or a limit order (when `limitProb` is specified). |
| **Limit Order** | A bet that only executes at a specified probability price or better. Remains open until filled, cancelled, or expired. |
| **Shares** | Units of a position. Winning YES shares pay out M$1 each; losing shares pay M$0. |
| **Resolution** | The final outcome of a market: YES, NO, MKT (probability), or CANCEL. |
| **Answer** | A possible outcome in a MULTIPLE_CHOICE or FREE_RESPONSE market. Each answer has its own probability. |
| **Bounty** | A BOUNTIED_QUESTION market where the creator distributes mana rewards to the best comments/answers. |
| **Poll** | A non-trading market type where users simply vote on options. |

---

## Base URLs

| Environment | REST API | WebSocket |
|---|---|---|
| **Production** | `https://api.manifold.markets` | `wss://api.manifold.markets/ws` |
| **Dev** | `https://api.dev.manifold.markets` | `wss://api.dev.manifold.markets/ws` |

> **Important:** The API was recently moved from `https://manifold.markets/api` to `https://api.manifold.markets`. The old domain will be removed in the future. Always use the new domain.

All REST endpoints are prefixed with `/v0/`.

---

## Documentation & References

| Resource | URL |
|---|---|
| API Documentation | <https://docs.manifold.markets/api> |
| Platform | <https://manifold.markets> |
| Source Code (GitHub) | <https://github.com/manifoldmarkets/manifold> |
| API Type Definitions | <https://github.com/manifoldmarkets/manifold/tree/main/common/src/api/schema.ts> |
| Discord Community | <https://discord.com/invite/eHQBNBqXuh> |
| Terms of Service | <https://docs.manifold.markets/terms> |
| Data Downloads & Licensing | <https://docs.manifold.markets/data> |

---

## Authentication

Some endpoints are public (no auth required). Write endpoints and user-specific reads require authentication via an API key.

### Generating an API Key

1. Log in to [Manifold](https://manifold.markets).
2. Go to your user profile and click "edit".
3. Scroll to the API key field at the bottom.
4. Click the "refresh" button to generate a new key.
5. Copy and store the key securely. Clicking refresh again will invalidate the old key and generate a new one.

### Using the API Key

Include the key in the `Authorization` header:

```
Authorization: Key {your_api_key}
```

Alternatively, the API accepts Firebase JWTs via `Authorization: Bearer {jwt}`, but this is intended for the web client and not recommended for third-party use.

### Example Authenticated Request

```bash
curl "https://api.manifold.markets/v0/me" \
  -H "Authorization: Key YOUR_API_KEY"
```

---

## Rate Limits

There is a rate limit of **500 requests per minute per IP address**. Do not use multiple IP addresses to circumvent this limit.

Implement exponential backoff on HTTP 429 responses.

---

## Fees

- **Comments placed through the API** incur a M$1 transaction fee.
- **Market creation** costs mana (see the market creation endpoint for current costs per type).

---

## Licensing

- **Permitted:** Bots, automated trading, algorithmic tools, integrations.
- **Prohibited:** Scraping through means other than the API; circumventing rate limits.
- **AI training data:** Not permitted for commercial use without a data license. Academic and personal/non-commercial use is allowed. Contact `api@manifold.markets` for commercial licensing.

---

## REST API Endpoints Overview

All endpoints are relative to `https://api.manifold.markets/v0`.

### Users

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/user/[username]` | GET | No | Get a user by username. Returns `User`. |
| `/user/[username]/lite` | GET | No | Get basic display info by username. Returns `DisplayUser`. |
| `/user/by-id/[id]` | GET | No | Get a user by unique ID. Returns `User`. |
| `/user/by-id/[id]/lite` | GET | No | Get display info by ID. Returns `DisplayUser`. |
| `/me` | GET | Yes | Get the authenticated user. Returns `User`. |
| `/users` | GET | No | List all users, ordered by creation date desc. Params: `limit` (max 1000, default 500), `before` (user ID for pagination). |

#### User Type

```
User {
  id: string
  createdTime: number
  name: string              // display name
  username: string           // used in URLs
  url: string
  avatarUrl?: string
  bio?: string
  bannerUrl?: string
  website?: string
  twitterHandle?: string
  discordHandle?: string
  isBot?: boolean
  isAdmin?: boolean
  isTrustworthy?: boolean    // moderator
  isBannedFromPosting?: boolean
  userDeleted?: boolean
  balance: number
  totalDeposits: number
  lastBetTime?: number
  currentBettingStreak?: number
}
```

#### DisplayUser Type

```
DisplayUser {
  id: string
  name: string
  username: string
  avatarUrl?: string
}
```

### Portfolio

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/get-user-portfolio` | GET | No | Get a user's live portfolio metrics. Param: `userId`. |
| `/get-user-portfolio-history` | GET | No | Get portfolio history over a period. Params: `userId`, `period` (`daily`, `weekly`, `monthly`, `allTime`). |
| `/get-user-contract-metrics-with-contracts` | GET | No* | Get a user's positions and their contracts. Params: `userId` (required), `limit` (required), `offset`, `order` (`lastBetTime` or `profit`), `perAnswer`. *When authenticated, may include private market metrics visible to you. |

#### PortfolioMetrics Type

```
PortfolioMetrics {
  investmentValue: number
  cashInvestmentValue: number
  balance: number
  cashBalance: number
  spiceBalance: number
  totalDeposits: number
  totalCashDeposits: number
  loanTotal: number
  timestamp: number
  profit?: number
  userId: string
}

LivePortfolioMetrics = PortfolioMetrics & {
  dailyProfit: number
}
```

### Markets — Discovery & Listing

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/markets` | GET | No | List markets by creation date desc. Params: `limit` (max 1000, default 500), `sort` (`created-time`, `updated-time`, `last-bet-time`, `last-comment-time`), `order` (`asc`/`desc`), `before` (market ID for cursor pagination), `userId`, `groupId`. Returns `LiteMarket[]`. |
| `/market/[marketId]` | GET | No | Get a single market by ID. Returns `FullMarket` (includes answers, but not bets/comments). |
| `/slug/[marketSlug]` | GET | No | Get a market by slug (URL path after username). Returns `FullMarket`. |
| `/search-markets` | GET | No | Search/filter markets (similar to browse page). Returns `LiteMarket[]`. See parameters below. |

#### Search Markets Parameters

| Parameter | Description |
|---|---|
| `term` | Search query string. Can be empty. |
| `sort` | `most-popular` (default), `newest`, `score`, `daily-score`, `freshness-score`, `24-hour-vol`, `liquidity`, `subsidy`, `last-updated`, `close-date`, `start-time`, `resolve-date`, `random`, `bounty-amount`, `prob-descending`, `prob-ascending`. |
| `filter` | `all` (default), `open`, `closed`, `resolved`, `news`, `closing-90-days`, `closing-week`, `closing-month`, `closing-day`. |
| `contractType` | `ALL` (default), `BINARY`, `MULTIPLE_CHOICE`, `DEPENDENT_MULTIPLE_CHOICE`, `INDEPENDENT_MULTIPLE_CHOICE`, `BOUNTY`, `POLL`. |
| `topicSlug` | Only markets tagged with this topic slug. |
| `creatorId` | Only markets by this creator. |
| `limit` | 0–1000 (default 100). |
| `offset` | Number to skip (max 1000 when `sort=newest`). |
| `beforeTime` | Millisecond timestamp cursor for efficient pagination with `sort=newest`. Pass `createdTime` of last result. |
| `liquidity` | Minimum liquidity per contract/answer. |

### Markets — Probabilities

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/market/[marketId]/prob` | GET | No | Get current probability (max 1s cache). Returns `{ prob }` for binary or `{ answerProbs: { answerId: prob } }` for multi. |
| `/market-probs` | GET | No | Batch probabilities for multiple markets (max 1s cache). Param: `ids` (array, up to 100). Returns `{ marketId: { prob } | { answerProbs } }`. |

### Markets — Positions

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/market/[marketId]/positions` | GET | No | Get position data for a market. Params: `order` (`shares`/`profit`, default `profit`), `top`, `bottom`, `userId`, `answerId`. Returns `ContractMetric[]`. |

#### ContractMetric Type

```
ContractMetric {
  contractId: string
  from: {
    [period: string]: {     // day, week, month
      profit: number
      profitPercent: number
      invested: number
      prevValue: number
      value: number
    }
  } | undefined
  hasNoShares: boolean
  hasShares: boolean
  hasYesShares: boolean
  invested: number
  loan: number
  maxSharesOutcome: string | null
  payout: number
  profit: number
  profitPercent: number
  totalShares: { [outcome: string]: number }
  userId: string
  userUsername: string
  userName: string
  userAvatarUrl: string
  lastBetTime: number
}
```

### Markets — Creation & Management

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/market` | POST | Yes | Create a new market. Returns `LiteMarket`. See parameters below. |
| `/market/[marketId]/answer` | POST | Yes | Add an answer to a MULTIPLE_CHOICE market. Param: `text`. |
| `/market/[marketId]/add-liquidity` | POST | Yes | Add mana to liquidity pool (does not boost). Param: `amount`. |
| `/market/[marketId]/add-bounty` | POST | Yes | Add mana to a bounty question's reward. Param: `amount`. |
| `/market/[marketId]/award-bounty` | POST | Yes | Distribute bounty reward. Params: `amount`, `commentId`. |
| `/market/[marketId]/close` | POST | Yes | Set close time. Param: `closeTime` (ms since epoch; omit to close immediately). |
| `/market/[marketId]/group` | POST | Yes | Add/remove a topic tag. Params: `groupId`, `remove` (optional, `true` to untag). |
| `/market/[marketId]/resolve` | POST | Yes | Resolve a market. See resolution format below. |

#### Market Creation Parameters

**Common parameters (all market types):**

| Parameter | Required | Description |
|---|---|---|
| `outcomeType` | Yes | `BINARY`, `MULTIPLE_CHOICE`, `PSEUDO_NUMERIC`, `POLL`, `BOUNTIED_QUESTION`. |
| `question` | Yes | The headline question. |
| `description` | No | Plain text description. Or use `descriptionHtml`, `descriptionMarkdown`, or `descriptionJson` (stringified TipTap JSON). |
| `closeTime` | No | When the market closes (ms since epoch). Defaults to 7 days from now. |
| `visibility` | No | `public` (default) or `unlisted`. |
| `groupIds` | No | Array of topic IDs to tag. |
| `extraLiquidity` | No | Additional liquidity to add. |

**Additional parameters by type:**

| Type | Extra Parameters |
|---|---|
| BINARY | `initialProb` (1–99, required) |
| PSEUDO_NUMERIC | `min`, `max`, `isLogScale`, `initialValue` (all required) |
| MULTIPLE_CHOICE | `answers` (string[], required), `addAnswersMode` (`DISABLED`/`ONLY_CREATOR`/`ANYONE`, default `DISABLED`), `shouldAnswersSumToOne` (boolean) |
| BOUNTIED_QUESTION | `totalBounty` (required) |
| POLL | `answers` (string[], required) |

**Creation costs:**

| Type | Cost |
|---|---|
| BINARY | M$50 |
| PSEUDO_NUMERIC | M$250 |
| MULTIPLE_CHOICE | M$25/answer or M$25 for no preset answers |

#### Resolution Formats

**Binary markets:**
- `outcome`: `YES`, `NO`, `MKT`, or `CANCEL`.
- `probabilityInt`: Optional, used when resolving to `MKT`.

**Multiple Choice (shouldAnswersSumToOne = true):**
```
{
  "outcome": "MKT",
  "resolutions": [
    { "answer": <index>, "pct": <weight> }
  ]
}
```
Weights must sum to 100. Or use `outcome` as a number for a single answer index, or `CANCEL`.

**Multiple Choice (shouldAnswersSumToOne = false):**
Resolve each answer independently with separate requests:
```
{
  "outcome": "YES",    // or "NO"
  "answerId": "<answer_id>"
}
```

**Numeric markets:**
- `outcome`: `CANCEL` or a numeric bucket ID.
- `value`: The resolution value.
- `probabilityInt`: Required if `value` is provided.

### Trading

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/bet` | POST | Yes | Place a bet or limit order. Returns `Bet`. |
| `/multi-bet` | POST | Yes | Place multiple YES bets on a sums-to-one multi-choice market, targeting equal shares per answer. Returns `Bet[]`. |
| `/bet/cancel/[id]` | POST | Yes | Cancel an open limit order. |
| `/market/[marketId]/sell` | POST | Yes | Sell shares. Params: `outcome` (`YES`/`NO`, defaults to kind held), `shares` (optional, defaults to all), `answerId` (required for multi-choice). |

#### Bet Parameters

| Parameter | Required | Description |
|---|---|---|
| `amount` | Yes | Amount in mana to bet, before fees. |
| `contractId` | Yes | The market ID. |
| `outcome` | No | `YES` (default) or `NO`. |
| `limitProb` | No | Makes this a limit order. A number from 0.01 to 0.99 (whole percentage points only, e.g., 0.01 = 1%). |
| `expiresAt` | No | Timestamp (ms) when the limit order auto-cancels. |
| `expiresMillisAfter` | No | Milliseconds after creation for auto-cancel. |
| `dryRun` | No | If `true`, simulates without placing. |

#### Multi-Bet Parameters

| Parameter | Required | Description |
|---|---|---|
| `contractId` | Yes | Market ID. Must be `cpmm-multi-1` with `shouldAnswersSumToOne=true`. |
| `answerIds` | Yes | Array of answer IDs (min 2). |
| `amount` | Yes | Total mana to spend across selected answers. |
| `limitProb` | No | Per-leg limit price (0.01–0.99, two decimal places). |
| `expiresAt` | No | Timestamp (ms) for auto-cancel of unfilled portions. |

### Comments

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/comment` | POST | Yes | Create a top-level comment on a market. Params: `contractId`, plus one of `content` (TipTap JSON), `html`, or `markdown`. Fee: M$1. |
| `/comments` | GET | No | List comments for a market or user. Params: `contractId`, `contractSlug`, `limit` (max 1000), `page`, `userId`, `order` (`likes`/`newest`/`oldest`). |

### Bets

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/bets` | GET | No | List bets. Params: `userId`, `username`, `contractId` (can be multiple), `contractSlug`, `limit` (max 1000), `before`/`after` (bet ID cursors), `beforeTime`/`afterTime` (timestamps), `kinds` (`open-limit`), `order` (`asc`/`desc`). |

#### Bet Type

```
Bet {
  id: string
  contractId: string
  userId: string
  amount: number            // mana spent (filled portion for limits)
  orderAmount: number       // original order amount
  shares: number
  outcome: "YES" | "NO"
  probBefore: number
  probAfter: number
  createdTime: number
  fees: {
    creatorFee: number
    platformFee: number
    liquidityFee: number
  }
  isFilled: boolean
  isCancelled: boolean
  loanAmount: number
  limitProb?: number        // present for limit orders
  fills: Fill[]
  answerId?: string         // for multi-choice markets
}

Fill {
  matchedBetId: string | null
  amount: number
  shares: number
  timestamp: number
  fees: { creatorFee: number; platformFee: number; liquidityFee: number }
}
```

### Topics (Groups)

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/groups` | GET | No | List public topics, 500 at a time, newest first. Params: `beforeTime`, `availableToUserId`. |
| `/group/[slug]` | GET | No | Get a topic by slug. |
| `/group/by-id/[id]` | GET | No | Get a topic by ID. |

### Mana Transfers

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/managram` | POST | Yes | Send mana to other users. Params: `toIds` (array of user IDs), `amount` (>= 10, sent to each), `message` (optional). |

### Transactions

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/txns` | GET | No | List transactions, newest first. Params: `token` (`CASH`/`MANA`), `offset`, `limit` (max 100), `before`/`after` (timestamps), `toId`, `fromId`, `category`. |

### Leagues

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/leagues` | GET | No | Get league standings. Params: `userId`, `season` (number), `cohort` (string). |

---

## Market Types

| `outcomeType` | `mechanism` | Description |
|---|---|---|
| `BINARY` | `cpmm-1` | Yes/No market with a single probability (0–1). Most common type. |
| `MULTIPLE_CHOICE` | `cpmm-multi-1` | Multiple answers, each with its own probability. Can be dependent (sum to 100%) or independent. |
| `FREE_RESPONSE` | `dpm-2` | Legacy. Anyone can add answers. Uses DPM mechanism. |
| `PSEUDO_NUMERIC` | `cpmm-1` | Maps probability to a numeric range [min, max]. Can be linear or log scale. |
| `BOUNTIED_QUESTION` | — | No trading. Creator distributes bounty to best comments. |
| `POLL` | — | No trading. Users vote on options. |

---

## LiteMarket Type

```
LiteMarket {
  id: string
  creatorId: string
  creatorUsername: string
  creatorName: string
  creatorAvatarUrl?: string
  createdTime: number
  closeTime?: number
  question: string
  url: string                      // always points to manifold.markets
  outcomeType: string
  mechanism: string
  probability: number
  pool: { [outcome: string]: number }
  p?: number                       // CPMM probability constant
  totalLiquidity?: number          // CPMM only
  value?: number                   // PSEUDO_NUMERIC only
  min?: number                     // PSEUDO_NUMERIC only
  max?: number                     // PSEUDO_NUMERIC only
  isLogScale?: boolean             // PSEUDO_NUMERIC only
  volume: number
  volume24Hours: number
  isResolved: boolean
  resolutionTime?: number
  resolution?: string
  resolutionProbability?: number   // for MKT resolution
  uniqueBettorCount: number
  lastUpdatedTime?: number
  lastBetTime?: number
  token?: "MANA" | "CASH"
  siblingContractId?: string       // toggle between mana/cash version
}
```

## FullMarket Type

```
FullMarket = LiteMarket & {
  answers?: Answer[]                          // multi markets only
  shouldAnswersSumToOne?: boolean             // multi markets only
  addAnswersMode?: "ANYONE" | "ONLY_CREATOR" | "DISABLED"
  options?: { text: string; votes: number }[] // poll only
  totalBounty?: number                        // bounty only
  bountyLeft?: number                         // bounty only
  description: JSONContent                    // TipTap rich text
  textDescription: string                     // plain text
  coverImageUrl?: string
  groupSlugs?: string[]                       // topic tags
}
```

---

## WebSocket API

Manifold provides a real-time WebSocket server for subscribing to live updates.

### Connection

```
wss://api.manifold.markets/ws         (production)
wss://api.dev.manifold.markets/ws     (dev)
```

No authentication is required to connect. Authentication is optional (for user-specific topics).

### Message Format

All messages are JSON. Client messages must include:

- `type`: `identify`, `subscribe`, `unsubscribe`, or `ping`.
- `txid`: A unique number identifying the message.

The server acknowledges each message:
```
{ "type": "ack", "txid": 123, "success": true }
```

### Subscribing to Topics

Send a subscribe message:
```
{
  "type": "subscribe",
  "txid": 1,
  "topics": ["global/new-bet", "contract/[marketId]"]
}
```

### Available Topics

#### Global Topics

| Topic | Description |
|---|---|
| `global/new-bet` | All new bets across all markets. |
| `global/new-contract` | All new markets being created. |
| `global/new-comment` | All new comments across all markets. |
| `global/new-subsidy` | All new liquidity subsidies. |
| `global/updated-contract` | Updates to any public market. |

#### Per-Market Topics (replace `[marketId]` with actual ID)

| Topic | Description |
|---|---|
| `contract/[marketId]` | General market updates. |
| `contract/[marketId]/new-bet` | New bets on this market. |
| `contract/[marketId]/new-comment` | New comments on this market. |
| `contract/[marketId]/new-subsidy` | New liquidity subsidies. |
| `contract/[marketId]/new-answer` | New answers added (multi-choice). |
| `contract/[marketId]/updated-answers` | Updates to existing answers. |
| `contract/[marketId]/orders` | Limit order updates. |
| `contract/[marketId]/chart-annotation` | Chart annotations. |
| `contract/[marketId]/user-metrics/[userId]` | User position updates in this market. |

#### Other Topics

| Topic | Description |
|---|---|
| `user/[userId]` | Updates to a user's public info. |
| `answer/[answerId]/update` | Updates to a specific answer. |
| `tv_schedule` | Updates to the TV schedule. |

### Keep-Alive

Send periodic pings (every 30–60 seconds) to keep the connection alive. If no ping is received for 60 seconds, the server terminates the connection.

```
{ "type": "ping", "txid": 42 }
```

### Broadcast Messages

The server sends updates as broadcast messages:
```
{
  "type": "broadcast",
  "topic": "global/new-bet",
  "data": { ... }
}
```

---

## Common Patterns

### List Recent Markets

```bash
curl -s "https://api.manifold.markets/v0/markets?limit=5" | jq '.[].question'
```

### Get a Single Market by ID

```bash
curl -s "https://api.manifold.markets/v0/market/3zspH9sSzMlbFQLn9GKR" | jq '{question, probability, volume, isResolved}'
```

### Get a Market by Slug

```bash
curl -s "https://api.manifold.markets/v0/slug/will-carrick-flynn-win-the-general" | jq '{question, probability}'
```

### Search for Open Binary Markets

```bash
curl -s "https://api.manifold.markets/v0/search-markets?term=AI&sort=liquidity&filter=open&contractType=BINARY&limit=10" | jq '.[].question'
```

### Get Current Probability

```bash
curl -s "https://api.manifold.markets/v0/market/9t61v9e7x4/prob" | jq '.'
```

### Get Batch Probabilities

```bash
curl -s "https://api.manifold.markets/v0/market-probs?ids=9t61v9e7x4&ids=ZNlNdzz690" | jq '.'
```

### Place a YES Bet

```bash
curl -X POST "https://api.manifold.markets/v0/bet" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10, "contractId": "MARKET_ID", "outcome": "YES"}'
```

### Place a Limit Order

```bash
curl -X POST "https://api.manifold.markets/v0/bet" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100,
    "contractId": "MARKET_ID",
    "outcome": "YES",
    "limitProb": 0.40,
    "expiresMillisAfter": 86400000
  }'
```

### Sell All Shares in a Market

```bash
curl -X POST "https://api.manifold.markets/v0/market/MARKET_ID/sell" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"outcome": "YES"}'
```

### Cancel a Limit Order

```bash
curl -X POST "https://api.manifold.markets/v0/bet/cancel/BET_ID" \
  -H "Authorization: Key YOUR_API_KEY"
```

### Create a Binary Market

```bash
curl -X POST "https://api.manifold.markets/v0/market" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "outcomeType": "BINARY",
    "question": "Will it rain in SF tomorrow?",
    "descriptionMarkdown": "Resolves YES if measurable rainfall is recorded at SFO weather station.",
    "initialProb": 30,
    "closeTime": 1735689600000
  }'
```

### Create a Multiple Choice Market

```bash
curl -X POST "https://api.manifold.markets/v0/market" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "outcomeType": "MULTIPLE_CHOICE",
    "question": "Who will win the award?",
    "answers": ["Alice", "Bob", "Charlie"],
    "shouldAnswersSumToOne": true,
    "addAnswersMode": "ONLY_CREATOR"
  }'
```

### Resolve a Binary Market

```bash
curl -X POST "https://api.manifold.markets/v0/market/MARKET_ID/resolve" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"outcome": "YES"}'
```

### Get Your Portfolio

```bash
curl -s "https://api.manifold.markets/v0/get-user-portfolio?userId=YOUR_USER_ID" | jq '.'
```

### Get Top Positions on a Market

```bash
curl -s "https://api.manifold.markets/v0/market/MARKET_ID/positions?top=5&order=profit" | jq '.[].userName'
```

### Paginate Through All Markets (by newest)

```bash
# Page 1
curl -s "https://api.manifold.markets/v0/search-markets?sort=newest&limit=100" > page1.json

# Page 2: use createdTime of last result
BEFORE_TIME=$(jq '.[-1].createdTime' page1.json)
curl -s "https://api.manifold.markets/v0/search-markets?sort=newest&limit=100&beforeTime=$BEFORE_TIME" > page2.json
```

### Paginate Through Bets

```bash
# First page
curl -s "https://api.manifold.markets/v0/bets?contractId=MARKET_ID&limit=100" > bets1.json

# Next page: use ID of last bet
BEFORE=$(jq -r '.[-1].id' bets1.json)
curl -s "https://api.manifold.markets/v0/bets?contractId=MARKET_ID&limit=100&before=$BEFORE" > bets2.json
```

### Send Mana to Users

```bash
curl -X POST "https://api.manifold.markets/v0/managram" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"toIds": ["USER_ID_1", "USER_ID_2"], "amount": 100, "message": "Thanks!"}'
```

### Post a Comment

```bash
curl -X POST "https://api.manifold.markets/v0/comment" \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contractId": "MARKET_ID", "markdown": "Great question! I think YES is undervalued."}'
```

### WebSocket Subscription (Node.js)

```javascript
const ws = new WebSocket("wss://api.manifold.markets/ws");
let txid = 0;

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: "subscribe",
    txid: txid++,
    topics: ["global/new-bet"]
  }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.type === "broadcast") {
    console.log("New bet:", msg.data);
  }
};

// Keep-alive ping every 30 seconds
setInterval(() => {
  ws.send(JSON.stringify({ type: "ping", txid: txid++ }));
}, 30000);
```

---

## Usage Tips

- **All timestamps are UNIX milliseconds** (JavaScript `Date.now()` style), not seconds.
- **Never hardcode API keys** — use environment variables or secure key storage.
- **Market URLs** always point to `https://manifold.markets` regardless of which API instance you're using. The username in the URL path doesn't need to be correct (e.g., `manifold.markets/anyone/market-slug` works).
- **GET parameters** go in the query string. **POST/PUT parameters** go in the JSON body.
- **Limit orders** with `limitProb` crossing the current market price will partially fill immediately. Any unfilled remainder stays as a resting limit order.
- **`limitProb` precision**: Only whole percentage points (two decimal places, e.g., `0.01`, `0.50`, `0.99`).
- **Multi-choice markets** come in two flavors: dependent (`shouldAnswersSumToOne=true`, probabilities sum to 100%) and independent (each answer is effectively a separate binary market).
- **Combine REST + WebSocket** for best results: use REST for initial state, WebSocket for real-time deltas.
- **Paginate responsibly**: For `/search-markets` with `sort=newest`, use `beforeTime` for efficient deep pagination. For `/bets` and `/markets`, use cursor-based pagination with `before`/`after`.
- **Market token type** matters: check the `token` field (`MANA` or `CASH`) to know if a market uses play-money or prize-cash.
- **Dry run** bets by passing `dryRun: true` to simulate without placing.
- **Description formats**: You can provide market descriptions as plain text (`description`), HTML (`descriptionHtml`), Markdown (`descriptionMarkdown`), or TipTap JSON (`descriptionJson`). Only provide one.

---

## Error Handling

API responses are JSON. Successful requests return HTTP 200 with a JSON result. Error responses (4xx/5xx) return a JSON object with an error message.

| Status | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (missing or invalid API key) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |
| 429 | Rate limited (500 req/min exceeded) |
| 5xx | Server error |

Implement retry with exponential backoff for 429 and 5xx responses.

---

## Internal API

Manifold has some internal endpoints not part of the official API. These are undocumented and subject to change without notice.

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/unresolve` | POST | Yes | Unresolve a market. Param: `contractId`. |

Note: Internal endpoints are **not** prefixed with `/v0`.

---

## Versioning

The current API version is **v0** under `/v0/`. The API is still in alpha. Monitor the [official documentation](https://docs.manifold.markets/api) and the [Discord](https://discord.com/invite/eHQBNBqXuh) for breaking changes.