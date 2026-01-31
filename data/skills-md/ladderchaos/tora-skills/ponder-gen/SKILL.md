---
name: ponder-gen
description: Generate Ponder indexer handlers from contract ABIs and schema definitions. Use this skill when setting up new event indexing, adding handlers for new contracts, or updating the indexer after contract changes.
---

# Ponder Generator

This skill guides the generation and maintenance of Ponder indexer code for the Sooth Protocol, leveraging Ponder's type-safe, no-codegen approach.

## When to Use This Skill

Invoke this skill when:
- Adding indexing for new contracts
- Updating handlers after ABI changes
- Setting up event listeners for new events
- Debugging indexer sync issues
- Optimizing indexer performance

## Ponder Project Structure

```
packages/indexer/
├── ponder.config.ts      # Network and contract configuration
├── ponder.schema.ts      # Database schema (Drizzle-like)
├── src/
│   └── index.ts          # Event handlers
├── abis/                  # Contract ABIs (JSON)
└── .env                   # RPC endpoints
```

## Handler Generation Workflow

### Step 1: Add Contract ABI

Copy ABI from Foundry build:

```bash
cp packages/contracts-core/out/TickBookPoolManager.sol/TickBookPoolManager.json \
   packages/indexer/abis/
```

### Step 2: Configure Contract in ponder.config.ts

```typescript
import { createConfig } from 'ponder';
import { http } from 'viem';

import TickBookPoolManagerAbi from './abis/TickBookPoolManager.json';

export default createConfig({
  networks: {
    baseSepolia: {
      chainId: 84532,
      transport: http(process.env.PONDER_RPC_URL_84532),
    },
  },
  contracts: {
    TickBookPoolManager: {
      network: 'baseSepolia',
      abi: TickBookPoolManagerAbi.abi,
      address: '0x8e14f863109cc93ec91540919287556cc368ff0b',
      startBlock: 12345678,
    },
  },
});
```

### Step 3: Define Schema in ponder.schema.ts

```typescript
import { createSchema } from 'ponder';

export default createSchema((p) => ({
  // Markets table
  Market: p.createTable({
    id: p.string(),           // marketId as string
    question: p.string(),
    creator: p.string(),
    createdAt: p.bigint(),
    isSettled: p.boolean(),
    outcome: p.int().optional(),
  }),
  
  // Orders table
  Order: p.createTable({
    id: p.string(),           // txHash-logIndex
    marketId: p.string(),
    trader: p.string(),
    outcome: p.int(),         // 0=NO, 1=YES
    price: p.bigint(),
    amount: p.bigint(),
    timestamp: p.bigint(),
  }),
  
  // Positions table
  Position: p.createTable({
    id: p.string(),           // marketId-trader-outcome
    marketId: p.string(),
    trader: p.string(),
    outcome: p.int(),
    shares: p.bigint(),
  }),
}));
```

### Step 4: Generate Handlers in src/index.ts

```typescript
import { ponder } from 'ponder:registry';
import schema from '../ponder.schema';

// Handle MarketCreated event
ponder.on('LaunchpadEngine:MarketCreated', async ({ event, context }) => {
  const { marketId, creator, question } = event.args;
  
  await context.db.insert(schema.Market).values({
    id: marketId.toString(),
    question,
    creator,
    createdAt: event.block.timestamp,
    isSettled: false,
  });
});

// Handle RangeOrderPlaced event
ponder.on('TickBookPoolManager:RangeOrderPlaced', async ({ event, context }) => {
  const { marketId, trader, outcome, priceLow, priceHigh, amount, orderId } = event.args;
  
  await context.db.insert(schema.Order).values({
    id: `${event.transaction.hash}-${event.log.logIndex}`,
    marketId: marketId.toString(),
    trader,
    outcome: Number(outcome),
    price: priceLow, // or use midpoint
    amount,
    timestamp: event.block.timestamp,
  });
});

// Handle OrderFilled event (update position)
ponder.on('TickBookPoolManager:OrderFilled', async ({ event, context }) => {
  const { marketId, trader, outcome, shares } = event.args;
  const positionId = `${marketId}-${trader}-${outcome}`;
  
  // Upsert position
  await context.db
    .insert(schema.Position)
    .values({
      id: positionId,
      marketId: marketId.toString(),
      trader,
      outcome: Number(outcome),
      shares,
    })
    .onConflictDoUpdate({
      shares: (existing) => existing.shares + shares,
    });
});

// Handle MarketSettled event
ponder.on('LaunchpadEngine:MarketSettled', async ({ event, context }) => {
  const { marketId, outcome } = event.args;
  
  await context.db
    .update(schema.Market)
    .set({
      isSettled: true,
      outcome: Number(outcome),
    })
    .where({ id: marketId.toString() });
});
```

## Event-to-Handler Mapping

| Contract Event | Handler Action | Schema Table |
|----------------|----------------|--------------|
| `MarketCreated` | Insert | `Market` |
| `MarketSettled` | Update | `Market` |
| `RangeOrderPlaced` | Insert | `Order` |
| `SpotOrderPlaced` | Insert | `Order` |
| `OrderFilled` | Upsert | `Position` |
| `OrderCancelled` | Delete | `Order` |
| `Claimed` | Update | `Position` |

## Type Safety

Ponder provides full type inference:

```typescript
// event.args is fully typed based on ABI
ponder.on('TickBookPoolManager:RangeOrderPlaced', async ({ event }) => {
  // TypeScript knows these fields exist
  const { marketId, trader, outcome, priceLow, priceHigh, amount } = event.args;
  
  // event.block and event.transaction also typed
  const blockNumber = event.block.number;
  const txHash = event.transaction.hash;
});
```

## Running the Indexer

```bash
cd packages/indexer

# Development (with hot reload)
pnpm dev

# Production
pnpm start

# Check sync status
curl http://localhost:42069/status
```

## GraphQL API

Ponder auto-generates GraphQL API:

```graphql
# Get all markets
query {
  markets(first: 10, orderBy: "createdAt", orderDirection: "desc") {
    items {
      id
      question
      creator
      isSettled
    }
  }
}

# Get orders for a market
query {
  orders(where: { marketId: "1" }) {
    items {
      trader
      outcome
      price
      amount
    }
  }
}
```

## Common Patterns

### Handling BigInt

```typescript
// Convert to string for storage
marketId: marketId.toString(),

// Keep as bigint for numeric ops
shares: shares, // bigint column
```

### Composite IDs

```typescript
// Create unique IDs from multiple fields
const id = `${marketId}-${trader}-${outcome}`;
const txId = `${event.transaction.hash}-${event.log.logIndex}`;
```

### Upsert Pattern

```typescript
await context.db
  .insert(schema.Position)
  .values(newPosition)
  .onConflictDoUpdate({
    shares: (existing) => existing.shares + newShares,
  });
```

## Debugging

```bash
# Verbose logging
DEBUG=ponder:* pnpm dev

# Reset and resync
rm -rf .ponder && pnpm dev

# Check indexed blocks
curl http://localhost:42069/metrics
```

## Best Practices

1. **Start Block**: Set `startBlock` to contract deployment block
2. **Batch Inserts**: Use `context.db.insert().values([...])` for bulk
3. **Error Handling**: Ponder retries failed handlers automatically
4. **Schema Migrations**: Delete `.ponder/` when changing schema
5. **RPC Rate Limits**: Use paid RPC for production
