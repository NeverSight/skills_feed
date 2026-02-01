---
name: synpress-e2e
description: End-to-end testing with wallet automation using Synpress. Use this skill for testing dApp flows that require MetaMask/wallet interactions, transaction signing, and on-chain verification.
---

# Synpress E2E Testing

This skill guides E2E testing of Web3 dApps using Synpress, which extends Playwright with MetaMask automation capabilities.

## When to Use This Skill

Invoke this skill when:
- Testing wallet connection flows
- Testing transaction signing
- Testing on-chain state changes
- Automating multi-step DeFi interactions
- Testing wallet-dependent UI states

## Prerequisites

### Installation

```bash
cd apps/web
pnpm add -D @synthetixio/synpress
```

### Environment Setup

Create `.env.e2e`:

```bash
# Test wallet (DO NOT use with real funds)
TEST_PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
TEST_NETWORK_NAME=Base Sepolia
TEST_NETWORK_RPC=https://sepolia.base.org
TEST_CHAIN_ID=84532
```

## Synpress Test Structure

### Basic Test Template

```typescript
// apps/web/e2e/wallet-connect.spec.ts
import { testWithSynpress } from '@synthetixio/synpress';
import { MetaMask, metaMaskFixtures } from '@synthetixio/synpress/playwright';

const test = testWithSynpress(metaMaskFixtures);

test.describe('Wallet Connection', () => {
  test('should connect wallet', async ({ page, metamask }) => {
    // Navigate to app
    await page.goto('http://localhost:5173');
    
    // Click connect button
    await page.click('[data-testid="connect-wallet"]');
    
    // Approve connection in MetaMask
    await metamask.connectToDapp();
    
    // Verify connected state
    await expect(page.locator('[data-testid="wallet-address"]')).toBeVisible();
  });
});
```

### Transaction Test Template

```typescript
test('should place an order', async ({ page, metamask }) => {
  // Setup: Connect wallet
  await page.goto('http://localhost:5173/market/1');
  await page.click('[data-testid="connect-wallet"]');
  await metamask.connectToDapp();
  
  // Action: Fill order form
  await page.fill('[data-testid="order-amount"]', '100');
  await page.click('[data-testid="place-order-btn"]');
  
  // Handle MetaMask confirmation
  await metamask.confirmTransaction();
  
  // Verify: Check transaction success
  await expect(page.locator('text=Order placed')).toBeVisible({ timeout: 30000 });
});
```

## Synpress Commands Reference

### Wallet Setup

```typescript
// Import wallet from private key
await metamask.importWallet(process.env.TEST_PRIVATE_KEY);

// Add custom network
await metamask.addNetwork({
  name: 'Base Sepolia',
  rpcUrl: 'https://sepolia.base.org',
  chainId: 84532,
  symbol: 'ETH',
});

// Switch network
await metamask.switchNetwork('Base Sepolia');
```

### Transaction Handling

```typescript
// Confirm transaction (approve gas)
await metamask.confirmTransaction();

// Confirm with custom gas
await metamask.confirmTransaction({ gasLimit: 500000 });

// Reject transaction
await metamask.rejectTransaction();

// Sign message
await metamask.confirmSignature();
```

### Token Approval

```typescript
// Handle ERC20 approval popup
await metamask.approveTokenPermission();

// Or with specific amount
await metamask.approveTokenPermission({ spendLimit: '1000' });
```

## Sooth-Specific Test Patterns

### Market Creation Flow

```typescript
test('should create a market', async ({ page, metamask }) => {
  await page.goto('http://localhost:5173/create');
  await metamask.connectToDapp();
  
  // Fill market details
  await page.fill('[data-testid="market-question"]', 'Will ETH reach $5000?');
  await page.fill('[data-testid="creator-deposit"]', '100');
  await page.selectOption('[data-testid="resolution-date"]', '2025-12-31');
  
  // Submit creation
  await page.click('[data-testid="create-market-btn"]');
  
  // Approve USDC spend
  await metamask.approveTokenPermission();
  await metamask.confirmTransaction();
  
  // Verify creation
  await expect(page.locator('[data-testid="market-created-success"]')).toBeVisible();
});
```

### Order Placement Flow

```typescript
test('should place YES order', async ({ page, metamask }) => {
  await page.goto('http://localhost:5173/market/1');
  await metamask.connectToDapp();
  
  // Select YES outcome
  await page.click('[data-testid="outcome-yes"]');
  
  // Enter order details
  await page.fill('[data-testid="order-amount"]', '50');
  await page.fill('[data-testid="limit-price"]', '0.65');
  
  // Place order
  await page.click('[data-testid="place-order"]');
  
  // Handle approvals
  await metamask.approveTokenPermission();
  await metamask.confirmTransaction();
  
  // Verify order in book
  await expect(page.locator('[data-testid="open-orders"]')).toContainText('50 USDC');
});
```

## Test Configuration

### playwright.config.ts

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 60000, // Longer timeout for blockchain
  retries: 2,
  workers: 1, // Serial execution for wallet state
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Running Tests

```bash
# Run all E2E tests
pnpm test:e2e

# Run with UI
pnpm test:e2e:ui

# Run specific test
pnpm test:e2e -- --grep "wallet connect"

# Debug mode
pnpm test:e2e -- --debug
```

## Best Practices

### Wait for Blockchain State

```typescript
// Wait for transaction confirmation
await expect(async () => {
  const balance = await page.locator('[data-testid="balance"]').textContent();
  expect(parseFloat(balance)).toBeGreaterThan(0);
}).toPass({ timeout: 30000 });
```

### Handle Network Delays

```typescript
// Retry pattern for chain state
await page.waitForFunction(
  () => document.querySelector('[data-testid="tx-confirmed"]'),
  { timeout: 45000 }
);
```

### Clean State Between Tests

```typescript
test.beforeEach(async ({ metamask }) => {
  // Reset to known state
  await metamask.switchNetwork('Base Sepolia');
});
```

## Troubleshooting

### MetaMask Not Loading
- Ensure Chrome extension path is correct
- Check that no other MetaMask instances are running
- Clear extension cache

### Transaction Stuck
- Increase gas limit in `confirmTransaction()`
- Check RPC endpoint health
- Verify test wallet has sufficient balance

### Flaky Tests
- Add explicit waits for blockchain state
- Use `toPass()` with timeout for async checks
- Run tests serially (`workers: 1`)
