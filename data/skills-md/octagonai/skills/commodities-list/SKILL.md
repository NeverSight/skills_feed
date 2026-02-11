---
name: commodities-list
description: Retrieve the full catalog of tradable commodities across energy, metals, and agriculture using Octagon MCP. Use when researching commodity markets, identifying trading firms, understanding market participants, and analyzing commodity sector coverage.
---

# Commodities List

Retrieve comprehensive information about tradable commodities and commodity trading companies across sectors using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Define Scope

Determine which commodity categories you want to explore:
- **Energy**: Oil, natural gas, power, coal
- **Metals**: Precious metals, base metals, industrial metals
- **Agriculture**: Grains, softs, livestock

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve the full catalog of tradable commodities across energy, metals, and agriculture.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve the full catalog of tradable commodities across energy, metals, and agriculture."
  }
}
```

### 3. Expected Output

The agent returns categorized commodity market information:

**Energy Commodities:**

| Company | Commodities Traded | Key Markets/Services |
|---------|-------------------|---------------------|
| Six One Commodities LLC | Natural gas, LNG, power | Wholesale trading, physical marketing |
| Freepoint Commodities LLC | Natural gas, power, oil, coal | Physical supply, risk management |
| ACT Commodities Group B.V. | Renewable energy, carbon emissions | Climate projects, emission allowances |

**Metals Commodities:**

| Company | Commodities Traded | Key Markets/Services |
|---------|-------------------|---------------------|
| Metallica Commodities | Non-ferrous/ferrous metals | PCB recycling, mineral development |
| Javelin Global Commodities | Metallurgical coal, iron ore | Dry bulk trading |

**Agriculture Commodities:**

| Company | Commodities Traded | Key Markets/Services |
|---------|-------------------|---------------------|
| Global Tea & Commodities | Tea, coffee, macadamia nuts | Wholesale production, distribution |

**Data Sources**: octagon-companies-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding commodity categories
- Evaluating market participants
- Analyzing trading services
- Researching specific commodities

## Example Queries

**Full Catalog:**
```
Retrieve the full catalog of tradable commodities across energy, metals, and agriculture.
```

**Energy Focus:**
```
List all energy commodities and trading companies.
```

**Metals Focus:**
```
What metals are traded and by which companies?
```

**Agriculture Focus:**
```
Show agricultural commodities and market participants.
```

**Specific Commodity:**
```
What companies trade natural gas?
```

**Service Focus:**
```
Which companies offer commodity risk management services?
```

## Commodity Categories

### Energy Commodities

| Commodity | Description |
|-----------|-------------|
| Crude Oil | WTI, Brent, Dubai |
| Natural Gas | Henry Hub, NBP, TTF |
| LNG | Liquefied natural gas |
| Power/Electricity | Wholesale electricity |
| Coal | Thermal, metallurgical |
| Emissions | Carbon credits, allowances |
| Refined Products | Gasoline, diesel, jet fuel |

### Metals Commodities

| Category | Examples |
|----------|----------|
| Precious Metals | Gold, silver, platinum, palladium |
| Base Metals | Copper, aluminum, zinc, nickel, lead |
| Ferrous Metals | Iron ore, steel, scrap |
| Minor Metals | Lithium, cobalt, rare earths |
| Metal Concentrates | Copper concentrate, zinc concentrate |

### Agricultural Commodities

| Category | Examples |
|----------|----------|
| Grains | Wheat, corn, soybeans, rice |
| Softs | Coffee, cocoa, sugar, cotton |
| Oilseeds | Palm oil, rapeseed, sunflower |
| Livestock | Cattle, hogs, poultry |
| Dairy | Milk, cheese, butter |
| Tropical | Tea, rubber, spices |

## Market Participants

### Trading Companies

| Type | Description |
|------|-------------|
| Physical Traders | Buy/sell actual commodities |
| Financial Traders | Derivatives and futures |
| Merchant Traders | Both physical and financial |
| Brokers | Facilitate transactions |

### Trading Services

| Service | Description |
|---------|-------------|
| Physical Marketing | Buying/selling physical goods |
| Wholesale Trading | Large-scale transactions |
| Risk Management | Hedging, derivatives |
| Price Discovery | Market intelligence |
| Logistics | Transportation, storage |

## Key Market Concepts

### Trading Types

| Type | Description |
|------|-------------|
| Spot | Immediate delivery |
| Forward | Future delivery, OTC |
| Futures | Exchange-traded contracts |
| Options | Right to buy/sell |
| Swaps | Exchange cash flows |

### Market Structure

| Element | Description |
|---------|-------------|
| Exchanges | CME, ICE, LME |
| OTC Markets | Direct counterparty |
| Physical Markets | Actual goods |
| Financial Markets | Derivatives |

## Company Analysis

### Evaluating Traders

| Factor | Consideration |
|--------|---------------|
| Commodities Covered | Range of products |
| Geographic Reach | Markets served |
| Services Offered | Trading, logistics, risk |
| Market Position | Size, reputation |
| Specialization | Focus areas |

### Business Models

| Model | Description |
|-------|-------------|
| Pure Trading | Buy/sell spread |
| Integrated | Trading + assets |
| Service Provider | Risk management, advisory |
| Technology | Data, analytics platforms |

## Sector Trends

### Energy Trends

| Trend | Impact |
|-------|--------|
| Energy Transition | Renewables, carbon markets |
| LNG Growth | Global gas trade |
| Electrification | Power market expansion |
| Emissions Trading | Carbon pricing |

### Metals Trends

| Trend | Impact |
|-------|--------|
| EV Battery Metals | Lithium, cobalt demand |
| Decarbonization | Green steel |
| Recycling | Circular economy |
| Supply Chain | Critical minerals |

### Agriculture Trends

| Trend | Impact |
|-------|--------|
| Climate Impact | Supply volatility |
| Sustainability | Traceability |
| Food Security | Strategic importance |
| Technology | Precision agriculture |

## Common Use Cases

### Market Research
```
What commodities are actively traded in the energy sector?
```

### Competitor Analysis
```
Who are the major players in metals trading?
```

### Supply Chain
```
Which companies handle agricultural commodity logistics?
```

### Risk Management
```
What firms offer commodity hedging services?
```

### Sector Overview
```
Give me an overview of the commodity trading landscape.
```

## Analysis Tips

1. **Understand categories**: Energy, metals, agriculture have different dynamics.

2. **Consider integration**: Physical vs. financial trading.

3. **Check geographic focus**: Regional vs. global players.

4. **Evaluate services**: Trading vs. risk management vs. logistics.

5. **Track trends**: Energy transition, sustainability, technology.

6. **Note specialization**: Generalist vs. specialist firms.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| sector-performance-snapshot | Commodity sector metrics |
| industry-performance-snapshot | Daily commodity moves |
| stock-quote | Commodity company stocks |
| financial-metrics-analysis | Trader financials |
