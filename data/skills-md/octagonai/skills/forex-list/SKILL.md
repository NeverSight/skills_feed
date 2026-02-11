---
name: forex-list
description: Retrieve a full listing of actively traded currency pairs in the global forex market using Octagon MCP. Use when researching forex markets, understanding currency pair categories, analyzing major/minor/exotic pairs, and identifying trading opportunities.
---

# Forex List

Retrieve comprehensive information about actively traded currency pairs in the global forex market using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Define Scope

Determine which currency pair categories you want to explore:
- **Majors**: USD paired with major currencies
- **Crosses**: Major currencies without USD
- **Exotics**: Emerging market currencies

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve a full listing of actively traded currency pairs in the global forex market.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve a full listing of actively traded currency pairs in the global forex market."
  }
}
```

### 3. Expected Output

The agent returns categorized currency pair information:

| Currency Pair | Description/Reason for Activity |
|---------------|--------------------------------|
| EUR/USD | Most liquid pair, Eurozone and U.S. economic interdependence |
| GBP/USD | High liquidity, sensitive to U.K./U.S. macroeconomic data |
| USD/JPY | Japanese Yen safe-haven status, U.S. interest rates |
| AUD/USD | Commodity price trends, Australian/U.S. economic cycles |
| USD/CHF | Swiss Franc safe-haven, U.S. monetary policy |
| CAD/USD | Oil prices, North American economic indicators |
| EUR/CHF | Range-bound markets, Euro-Swiss Franc correlations |
| AUD/NZD | Cross-Pacific trade, commodity-linked volatility |

**Data Sources**: octagon-crypto-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding currency pair categories
- Analyzing liquidity and volatility
- Identifying key drivers
- Selecting pairs for trading

## Example Queries

**Full Listing:**
```
Retrieve a full listing of actively traded currency pairs in the global forex market.
```

**Major Pairs:**
```
List the major currency pairs with USD.
```

**Cross Pairs:**
```
What are the most liquid cross currency pairs?
```

**Exotic Pairs:**
```
List emerging market currency pairs.
```

**Specific Focus:**
```
Which currency pairs are most sensitive to oil prices?
```

## Currency Pair Categories

### Major Pairs (USD Based)

| Pair | Base/Quote | Nickname |
|------|------------|----------|
| EUR/USD | Euro / US Dollar | Fiber |
| GBP/USD | British Pound / US Dollar | Cable |
| USD/JPY | US Dollar / Japanese Yen | Gopher |
| USD/CHF | US Dollar / Swiss Franc | Swissie |
| AUD/USD | Australian Dollar / US Dollar | Aussie |
| USD/CAD | US Dollar / Canadian Dollar | Loonie |
| NZD/USD | New Zealand Dollar / US Dollar | Kiwi |

### Cross Pairs (Non-USD)

| Pair | Base/Quote | Category |
|------|------------|----------|
| EUR/GBP | Euro / British Pound | Euro Cross |
| EUR/JPY | Euro / Japanese Yen | Euro Cross |
| EUR/CHF | Euro / Swiss Franc | Euro Cross |
| GBP/JPY | British Pound / Japanese Yen | Pound Cross |
| AUD/JPY | Australian Dollar / Japanese Yen | Yen Cross |
| AUD/NZD | Australian Dollar / New Zealand Dollar | Commodity Cross |

### Exotic Pairs

| Pair | Base/Quote | Region |
|------|------------|--------|
| USD/MXN | US Dollar / Mexican Peso | Americas |
| USD/ZAR | US Dollar / South African Rand | Africa |
| USD/TRY | US Dollar / Turkish Lira | Europe/Asia |
| USD/SGD | US Dollar / Singapore Dollar | Asia |
| EUR/PLN | Euro / Polish Zloty | Europe |
| USD/HKD | US Dollar / Hong Kong Dollar | Asia |

## Understanding Currency Pairs

### Base vs. Quote Currency

```
EUR/USD = 1.10
```

| Component | In Example |
|-----------|------------|
| Base Currency | EUR (first) |
| Quote Currency | USD (second) |
| Meaning | 1 EUR = 1.10 USD |
| If pair rises | Base strengthens |
| If pair falls | Base weakens |

### Bid/Ask Spread

| Concept | Description |
|---------|-------------|
| Bid | Price to sell base |
| Ask | Price to buy base |
| Spread | Ask - Bid (cost to trade) |

## Liquidity and Volume

### By Daily Volume

| Tier | Pairs | Typical Volume |
|------|-------|----------------|
| Tier 1 | EUR/USD | Highest |
| Tier 2 | USD/JPY, GBP/USD | Very High |
| Tier 3 | AUD/USD, USD/CAD, USD/CHF | High |
| Tier 4 | Cross Pairs | Moderate |
| Tier 5 | Exotic Pairs | Lower |

### Spread Implications

| Liquidity | Typical Spread |
|-----------|----------------|
| Very High (EUR/USD) | 0.5-1 pips |
| High (USD/JPY) | 1-2 pips |
| Moderate (Crosses) | 2-5 pips |
| Low (Exotics) | 5-50+ pips |

## Key Drivers by Pair

### EUR/USD Drivers

| Factor | Impact |
|--------|--------|
| ECB Policy | Euro direction |
| Fed Policy | USD direction |
| EU Economic Data | Growth, inflation |
| US Economic Data | Employment, GDP |
| Risk Sentiment | Dollar haven flows |

### USD/JPY Drivers

| Factor | Impact |
|--------|--------|
| BoJ Policy | Yen direction |
| Fed Policy | USD direction |
| Risk Appetite | Yen weakens on risk-on |
| Yield Differentials | Carry trade flows |
| Intervention Risk | BoJ action |

### Commodity Currency Drivers

| Pair | Key Commodity Link |
|------|-------------------|
| AUD/USD | Iron ore, gold |
| USD/CAD | Oil prices |
| NZD/USD | Dairy, agriculture |

## Trading Sessions

### Session Times (UTC)

| Session | Hours | Key Pairs |
|---------|-------|-----------|
| Sydney | 21:00-06:00 | AUD, NZD |
| Tokyo | 00:00-09:00 | JPY pairs |
| London | 07:00-16:00 | EUR, GBP |
| New York | 12:00-21:00 | USD pairs |

### Overlap Periods

| Overlap | Highest Volatility Pairs |
|---------|-------------------------|
| London/New York | EUR/USD, GBP/USD |
| Tokyo/London | EUR/JPY, GBP/JPY |
| Sydney/Tokyo | AUD/JPY, NZD/JPY |

## Volatility Characteristics

### By Pair Type

| Type | Volatility | Predictability |
|------|------------|----------------|
| Majors | Moderate | Higher |
| Crosses | Variable | Moderate |
| Exotics | High | Lower |

### Typical Daily Ranges

| Pair | Avg Daily Range |
|------|-----------------|
| EUR/USD | 50-100 pips |
| GBP/USD | 80-150 pips |
| USD/JPY | 50-100 pips |
| GBP/JPY | 100-200 pips |
| Exotics | 100-500+ pips |

## Common Use Cases

### Market Overview
```
What are the most actively traded forex pairs?
```

### Trading Selection
```
Which pairs have the tightest spreads?
```

### Risk Analysis
```
Which currency pairs are most volatile?
```

### Correlation Study
```
What pairs move together with oil prices?
```

### Session Planning
```
What pairs are most active during Asian session?
```

## Analysis Tips

1. **Start with majors**: Most liquid, tightest spreads.

2. **Understand correlations**: EUR/USD and USD/CHF often inverse.

3. **Match session to pair**: Trade pairs during their active hours.

4. **Consider spreads**: Exotics cost more to trade.

5. **Know the drivers**: Central banks, data releases, geopolitics.

6. **Monitor risk sentiment**: Affects safe-haven flows.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| forex-quote | Real-time pair prices |
| commodities-quote | Commodity currency context |
| stock-historical-index | Risk sentiment context |
| sector-performance-snapshot | Global macro view |
