---
name: polymarket-prediction-market
description: "Understand Polymarket prediction markets for sports and esports betting. Use when working with Polymarket API, sports arbitrage, binary contracts, CLOB pricing, or cross-platform trading with Kalshi. Triggers on: polymarket, prediction market, sports betting, esports betting, arbitrage, CLOB."
---

# polymarket-prediction-market

> Understand Polymarket's prediction markets—binary event contracts, CLOB pricing, order books, conditional tokens, and API integration.

## Allowed Tools

- Read
- Grep
- Glob
- WebFetch

---

## Core Mental Model

Polymarket operates as a **decentralized prediction market** on Polygon using USDC:

- **Binary Outcomes**: Each market has YES and NO tokens that settle at $1.00 or $0.00
- **Price = Probability**: A YES token at $0.65 implies 65% probability of the outcome
- **CLOB (Central Limit Order Book)**: Prices determined by limit orders, not AMM
- **Conditional Token Framework (CTF)**: Outcomes represented as ERC-1155 tokens
- **USDC Collateral**: All trading uses USDC on Polygon network

---

## Data Hierarchy

```
Condition (Event)
  └── Market
        ├── YES Token (token_id)
        └── NO Token (token_id)
```

- **Condition**: The overarching question/event (e.g., "Will Team Liquid win?")
- **Market**: A specific tradeable contract with YES/NO outcomes
- **Tokens**: Each outcome is a separate ERC-1155 token with unique token_id

---

## Market Objects

Key fields in Polymarket market data:

| Field | Description |
|-------|-------------|
| `condition_id` | Unique identifier for the condition/event |
| `question` | The market question text |
| `tokens` | Array of outcome tokens (YES/NO) |
| `token_id` | Unique ID for each outcome token |
| `outcome` | Token outcome name ("Yes" or "No") |
| `price` | Current mid-market price ($0.00-$1.00) |
| `volume` | Total trading volume in USDC |
| `liquidity` | Available liquidity in the order book |
| `end_date_iso` | When the market closes for trading |
| `active` | Whether market is currently tradeable |
| `closed` | Whether market has been resolved |
| `resolved` | Settlement status |
| `resolution` | Final outcome if resolved |

---

## Order Book Structure

Polymarket uses a **Central Limit Order Book (CLOB)**:

```
Order Book for "YES" Token
--------------------------
BIDS (Buy Orders)     |  ASKS (Sell Orders)
$0.62 - 500 shares    |  $0.64 - 300 shares
$0.61 - 1000 shares   |  $0.65 - 800 shares
$0.60 - 2000 shares   |  $0.66 - 1500 shares
```

- **Bid**: Highest price buyers will pay
- **Ask**: Lowest price sellers will accept
- **Spread**: Difference between best bid and ask
- **Mid Price**: (Best Bid + Best Ask) / 2

---

## Trading Mechanics

### Order Types

| Type | Description |
|------|-------------|
| **GTC** | Good-Til-Cancelled - stays until filled or cancelled |
| **GTD** | Good-Til-Date - expires at specified time |
| **FOK** | Fill-Or-Kill - must fill entirely or cancel |

### Position Management

- **Buy YES**: Profit if outcome is true (settles at $1.00)
- **Buy NO**: Profit if outcome is false (settles at $1.00)
- **Sell**: Close position by selling tokens back to order book
- **Merge**: Combine YES + NO tokens to redeem $1.00 USDC

### Fees

- **Maker Fee**: ~0% (providing liquidity)
- **Taker Fee**: ~1-2% (taking liquidity)
- Fees may vary; check current fee schedule

---

## Settlement & Resolution

1. **Trading Closes**: Market stops accepting orders at `end_date_iso`
2. **Resolution**: Oracle determines the outcome
3. **Settlement**:
   - Winning tokens redeem for $1.00 USDC
   - Losing tokens become worthless ($0.00)
4. **Redemption**: Users claim winnings via smart contract

---

## API Conventions

### Base URLs

| Environment | URL |
|-------------|-----|
| **CLOB API** | `https://clob.polymarket.com` |
| **Gamma API** | `https://gamma-api.polymarket.com` |

### Public Endpoints (No Auth)

| Endpoint | Description |
|----------|-------------|
| `GET /markets` | List all markets |
| `GET /markets/{condition_id}` | Get specific market |
| `GET /book` | Get order book for a token |
| `GET /price` | Get current prices |
| `GET /midpoint` | Get mid-market price |

### Authenticated Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /order` | Place a new order |
| `DELETE /order/{order_id}` | Cancel an order |
| `GET /orders` | Get user's open orders |
| `GET /trades` | Get user's trade history |

### Authentication

Polymarket uses **EIP-712 signatures** for authentication:

```
Headers:
  POLY_ADDRESS: <wallet_address>
  POLY_SIGNATURE: <eip712_signature>
  POLY_TIMESTAMP: <unix_timestamp>
  POLY_NONCE: <random_nonce>
```

### WebSocket (Real-time Updates)

Connect to `wss://ws-subscriptions-clob.polymarket.com/ws/` for:
- `price` - Real-time price updates
- `book` - Order book changes
- `trades` - Trade execution notifications

---

## API Response Examples

### Market Object

```json
{
  "condition_id": "0x1234...",
  "question": "Will Team Liquid win the CS2 Major?",
  "tokens": [
    {
      "token_id": "12345",
      "outcome": "Yes",
      "price": 0.65
    },
    {
      "token_id": "12346",
      "outcome": "No",
      "price": 0.35
    }
  ],
  "volume": "150000.00",
  "liquidity": "25000.00",
  "end_date_iso": "2024-03-15T00:00:00Z",
  "active": true,
  "closed": false
}
```

### Order Book Response

```json
{
  "token_id": "12345",
  "bids": [
    {"price": "0.64", "size": "500"},
    {"price": "0.63", "size": "1000"}
  ],
  "asks": [
    {"price": "0.66", "size": "300"},
    {"price": "0.67", "size": "800"}
  ]
}
```

---

## Sports & Esports Markets

Polymarket hosts various sports and esports betting markets. Understanding the naming conventions and market structures is critical for matching markets across platforms.

### Supported Categories

| Category | Examples |
|----------|----------|
| **Esports** | CS2, League of Legends, Valorant, Dota 2, Call of Duty |
| **Basketball** | NBA games, playoffs, championships |
| **Soccer** | Premier League, UEFA, Champions League, World Cup |
| **American Football** | NFL games, Super Bowl |
| **Tennis** | ATP, WTA, Grand Slams (Wimbledon, US Open, etc.) |
| **MMA/Fighting** | UFC events, Bellator |

### Market Naming Conventions

Polymarket sports markets typically follow these patterns:

```
Match Winner:
  "Will [Team A] beat [Team B]?"
  "Will [Team A] win against [Team B]?"
  "[Team A] vs [Team B] - Winner"

Tournament Winner:
  "Will [Team/Player] win [Tournament]?"
  "[Tournament] Winner: [Team/Player]"

Player Props:
  "Will [Player] score [X] points?"
  "Will [Player] get [X] kills?"
```

### Common Name Variations

When matching markets across platforms, watch for these variations:

| Polymarket | Kalshi | Notes |
|------------|--------|-------|
| Team Liquid | Team Liquid, TL | Abbreviations |
| G2 Esports | G2, G2 eSports | Spacing/capitalization |
| FaZe Clan | FaZe, Faze Clan | Case sensitivity |
| Natus Vincere | NaVi, Na'Vi | Common nicknames |
| Manchester United | Man United, Man U | Shortened names |
| Los Angeles Lakers | LA Lakers, Lakers | City abbreviations |

### Esports-Specific Patterns

#### CS2 (Counter-Strike 2)

```
Market formats:
  "Will Team Liquid win vs FaZe Clan?"
  "Team Liquid vs FaZe - CS2 Major"
  "CS2 Major Champion: Team Liquid"

Common tournaments:
  - Major Championships (Copenhagen, Shanghai)
  - ESL Pro League
  - BLAST Premier
  - IEM (Intel Extreme Masters)
```

#### League of Legends

```
Market formats:
  "Will T1 win Worlds 2024?"
  "T1 vs Gen.G - LCK Finals"
  "League of Legends World Champion"

Common tournaments:
  - Worlds (World Championship)
  - MSI (Mid-Season Invitational)
  - LCK, LEC, LCS (Regional leagues)
```

#### Valorant

```
Market formats:
  "Will Sentinels win VCT Champions?"
  "Sentinels vs LOUD - VCT Finals"

Common tournaments:
  - VCT Champions
  - VCT Masters
  - Regional Challengers
```

#### Call of Duty

```
Market formats:
  "Will OpTic win CDL Championship?"
  "OpTic vs FaZe - CDL Major"

Common tournaments:
  - CDL (Call of Duty League) Majors
  - CDL Championship
  - Warzone events
```

### Traditional Sports Patterns

#### NBA Basketball

```
Market formats:
  "Will the Lakers beat the Celtics?"
  "Lakers vs Celtics - NBA Finals Game 1"
  "NBA Champion 2024"

Identifiers:
  - Team city + name (Los Angeles Lakers)
  - Just team name (Lakers)
  - Abbreviations (LAL)
```

#### Soccer/Football

```
Market formats:
  "Will Manchester City beat Arsenal?"
  "Man City vs Arsenal - Premier League"
  "Champions League Winner 2024"

Leagues/Tournaments:
  - Premier League (England)
  - La Liga (Spain)
  - Serie A (Italy)
  - Bundesliga (Germany)
  - UEFA Champions League
  - UEFA Europa League
  - World Cup
```

#### NFL Football

```
Market formats:
  "Will the Chiefs beat the Eagles?"
  "Chiefs vs Eagles - Super Bowl"
  "Super Bowl LVIII Winner"

Identifiers:
  - City + name (Kansas City Chiefs)
  - Just name (Chiefs)
  - Abbreviations (KC)
```

#### Tennis

```
Market formats:
  "Will Djokovic win Wimbledon?"
  "Djokovic vs Alcaraz - Wimbledon Final"
  "US Open Men's Singles Winner"

Tournaments:
  - Grand Slams: Australian Open, French Open, Wimbledon, US Open
  - ATP/WTA Masters events
```

#### MMA/UFC

```
Market formats:
  "Will Jon Jones beat Stipe Miocic?"
  "Jones vs Miocic - UFC 309"
  "UFC Heavyweight Champion after UFC 309"

Identifiers:
  - Fighter full name
  - Last name only
  - Nickname ("Bones" for Jon Jones)
```

### API Filtering for Sports Markets

To find sports markets programmatically:

```javascript
// Filter by tags/categories
GET /markets?tag=sports
GET /markets?tag=esports
GET /markets?tag=nba
GET /markets?tag=cs2

// Search by keywords in question
GET /markets?search=NBA
GET /markets?search=Team%20Liquid
GET /markets?search=UFC

// Filter active sports markets
GET /markets?active=true&tag=sports
```

### Market Matching Strategy

For cross-platform arbitrage, use this matching approach:

1. **Normalize team/player names**
   - Remove special characters: `FaZe Clan` → `faze clan`
   - Handle abbreviations: `TL` → `team liquid`
   - Map nicknames: `NaVi` → `natus vincere`

2. **Extract key entities**
   - Team A name
   - Team B name
   - Tournament/League name
   - Match date/time

3. **Match by similarity**
   - Levenshtein distance for fuzzy matching
   - Token overlap for multi-word names
   - Date proximity for same matchup

4. **Verify market type**
   - Both markets must be "match winner" type
   - Same teams/players involved
   - Same event timeframe

### Example: Cross-Platform Match

```
Polymarket Market:
  Question: "Will Team Liquid beat G2 Esports?"
  YES price: $0.55
  End date: 2024-03-15

Kalshi Market:
  Title: "Team Liquid vs G2 - CS2 Major Semifinal"
  YES price: $0.52
  NO price: $0.51

Matching confidence: HIGH
- Same teams (Team Liquid, G2)
- Similar timeframe
- Both match-winner markets

Arbitrage check:
  Polymarket NO: $0.45
  Kalshi YES: $0.52
  Total: $0.97 → $0.03 profit potential
```

---

## Application Guidance

When answering questions about Polymarket:

1. **Clarify terminology**: Explain that prices represent implied probabilities
2. **Highlight CLOB**: Unlike AMMs, Polymarket uses limit orders
3. **Explain tokens**: YES/NO are separate tradeable ERC-1155 tokens
4. **Note fees**: Taker fees reduce profit margins
5. **Mention settlement**: Winning tokens redeem at exactly $1.00
6. **Stay neutral**: Do not provide financial advice or predictions

---

## Arbitrage Context (ArbiBot)

For cross-platform arbitrage with Kalshi:

| Concept | Polymarket | Kalshi |
|---------|------------|--------|
| Settlement | $1.00 USDC | $1.00 USD |
| Order Type | CLOB | CLOB |
| Currency | USDC (Polygon) | USD |
| Auth | EIP-712 Signatures | RSA Signatures |
| Fees | ~1-2% taker | Variable/Quadratic |

### Valid Arbitrage Strategy

Buy opposing outcomes across platforms when total cost < $1.00:

```
Example:
  Polymarket YES @ $0.45
  Kalshi NO @ $0.48
  Total Cost: $0.93
  Guaranteed Profit: $0.07 (one side pays $1.00)
```

---

## Examples

### Explaining a Price

> "The YES token trading at $0.72 means the market collectively estimates a 72% probability of this outcome occurring."

### Describing Order Execution

> "Your limit order to buy 100 YES shares at $0.65 will sit in the order book until someone sells at that price or lower."

### Settlement Explanation

> "If Team Liquid wins, your YES tokens settle at $1.00 each. If they lose, those tokens become worthless, but any NO tokens would pay out $1.00."

---

## References

- [Polymarket CLOB Documentation](https://docs.polymarket.com)
- [Polymarket API Reference](https://docs.polymarket.com/#api-reference)
- [Conditional Token Framework](https://docs.gnosis.io/conditionaltokens/)
