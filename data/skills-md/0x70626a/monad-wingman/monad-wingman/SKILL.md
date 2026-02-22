---
name: monad-wingman
description: Monad blockchain development tutor and builder. Triggers on "build", "create", "dApp", "smart contract", "Solidity", "DeFi", "Monad", "web3", "MON", or any blockchain development task. Covers Foundry-first workflow, Scaffold-Monad, parallel execution EVM, and Monad-specific deployment patterns.
license: MIT
metadata:
  author: Monad Community
  version: "1.0.0"
---

# Monad Wingman

Comprehensive Monad blockchain development guide for AI agents. Covers smart contract development on Monad (parallel execution EVM-compatible L1), DeFi protocols, security best practices, deployment workflows, and the SpeedRun Ethereum curriculum adapted for Monad.

---

## MONAD CRITICAL DIFFERENCES FROM ETHEREUM

Before doing ANYTHING, internalize these Monad-specific rules:

### Chain Configuration
- **Mainnet chain ID**: 143 | **Testnet chain ID**: 10143
- **DEFAULT TO TESTNET** unless the user explicitly says mainnet
- **Native token**: MON (18 decimals) — NOT ETH
- **RPC (testnet)**: `https://testnet-rpc.monad.xyz`
- **RPC (mainnet)**: `https://rpc.monad.xyz`
- **Block explorers**: MonadVision, Monadscan, Socialscan

### Solidity & Compilation
- **EVM version**: MUST be `prague` — set in `foundry.toml` as `evm_version = "prague"`
- **Solidity version**: 0.8.27+ required, **0.8.28 recommended**
- **Max contract size**: 128KB (vs Ethereum's 24.5KB) — much more room

### Deployment Rules (CRITICAL)
- **ALWAYS use `--legacy` flag** — Monad does NOT support EIP-1559 type 2 transactions
- **ALWAYS use `forge script`** — NEVER use `forge create`
- **No blob transactions** — EIP-4844 type 3 txs are NOT supported
- **Gas is charged on gas_limit**, not actual usage — set gas limits carefully
- **No global mempool** — transactions go directly to the block producer

### Wallet Persistence
- Store keys at `~/.monad-wallet` with `chmod 600`
- **Mainnet key safety**: use `--ledger`, `--trezor`, or keystore files — NEVER `--private-key` for mainnet

### Monad Architecture
- **Parallel execution** = optimistic concurrency, produces same results as sequential
- **Reserve Balance mechanism** — understand this for DeFi
- **Historical state NOT available** on full nodes — do not rely on archive queries
- **secp256r1 (P256) precompile** at address `0x0100` — enables passkey/WebAuthn signing

### Faucet (Testnet)
```bash
curl -X POST https://agents.devnads.com/v1/faucet \
  -H "Content-Type: application/json" \
  -d '{"chainId": 10143, "address": "0xYOUR_ADDRESS"}'
```

### Contract Verification
```bash
curl -X POST https://agents.devnads.com/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"chainId": 10143, "address": "0xCONTRACT", "source": "...", "compilerVersion": "0.8.28"}'
```

---

## AI AGENT INSTRUCTIONS - READ THIS FIRST

### Dual Workflow: Foundry (Primary) + Scaffold-Monad

Monad development supports two workflows. Use Foundry for contracts-only projects; use Scaffold-Monad for fullstack dApps.

### Workflow A: Foundry (Primary — Contracts Only)

**Step 1: Initialize Foundry Project**

```bash
forge init my-monad-project
cd my-monad-project
```

**Step 2: Configure foundry.toml for Monad**

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
evm_version = "prague"
solc_version = "0.8.28"

[rpc_endpoints]
monad_testnet = "https://testnet-rpc.monad.xyz"
monad_mainnet = "https://rpc.monad.xyz"
```

**Step 3: Write and Test Contracts**

```bash
forge test
```

**Step 4: Deploy to Monad Testnet**

```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --legacy
```

NEVER use `forge create`. ALWAYS use `forge script` with `--legacy`.

**Step 5: Verify Contract**

```bash
curl -X POST https://agents.devnads.com/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"chainId": 10143, "address": "0xDEPLOYED", "source": "...", "compilerVersion": "0.8.28"}'
```

### Workflow B: Scaffold-Monad (Fullstack dApps)

**Step 1: Create Project**

```bash
# Foundry variant (recommended)
git clone https://github.com/monad-developers/scaffold-monad-foundry.git my-dapp
cd my-dapp
```

**Step 2: Configure for Monad**

Edit `packages/nextjs/scaffold.config.ts`:
```typescript
import { monadTestnet } from "viem/chains";

const scaffoldConfig = {
  targetNetworks: [monadTestnet],
  pollingInterval: 3000,   // 3 seconds (default 30000 is too slow)
};
```

IMPORTANT: Import `monadTestnet` from `viem/chains`. Do NOT define a custom chain object.

**Step 3: Configure Foundry for Monad**

Edit `packages/foundry/foundry.toml`:
```toml
evm_version = "prague"
solc_version = "0.8.28"
```

**Step 4: Install and Start**

```bash
cd <project-name>
yarn install
yarn start
```

**Step 5: Deploy**

```bash
yarn deploy --network monadTestnet
```

**Step 6: Fund Wallet via Faucet**

```bash
curl -X POST https://agents.devnads.com/v1/faucet \
  -H "Content-Type: application/json" \
  -d '{"chainId": 10143, "address": "0xYOUR_BURNER_WALLET"}'
```

**Step 7: Test the Frontend**

1. **Navigate** to `http://localhost:3000`
2. **Take a snapshot** to get page elements
3. **Fund the wallet** via faucet (MON, not ETH)
4. **Click through the app** to verify functionality

### Fork Mode (Testing Against Live Monad State)

```bash
anvil --fork-url https://rpc.monad.xyz --block-time 1
```

Or for testnet:
```bash
anvil --fork-url https://testnet-rpc.monad.xyz --block-time 1
```

### DO NOT:

- Use `forge create` (use `forge script` with `--legacy` instead)
- Send EIP-1559 type 2 transactions (always use `--legacy`)
- Send blob transactions (EIP-4844 type 3 not supported)
- Use `--private-key` for mainnet deployments (use `--ledger`/`--trezor`/keystore)
- Define custom chain objects in frontend (use `import { monadTestnet } from 'viem/chains'`)
- Rely on historical state queries (not available on full nodes)
- Assume gas is charged on usage (it is charged on gas_limit)

---

## Monad Deployment Workflow

### Deploy Script Template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Script.sol";
import "../src/MyContract.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        MyContract myContract = new MyContract();

        vm.stopBroadcast();

        console.log("MyContract deployed to:", address(myContract));
    }
}
```

### Deploy Commands

```bash
# Testnet (default)
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --legacy

# Mainnet (use hardware wallet!)
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://rpc.monad.xyz \
  --ledger \
  --broadcast \
  --legacy
```

---

## THE MOST CRITICAL CONCEPT

**NOTHING IS AUTOMATIC ON ANY EVM CHAIN, INCLUDING MONAD.**

Smart contracts cannot execute themselves. There is no cron job, no scheduler, no background process. For EVERY function that "needs to happen":

1. Make it callable by **ANYONE** (not just admin)
2. Give callers a **REASON** (profit, reward, their own interest)
3. Make the incentive **SUFFICIENT** to cover gas + profit

**Always ask: "Who calls this function? Why would they pay gas?"**

If you cannot answer this, your function will not get called.

**Monad note**: Gas on Monad is cheap due to parallel execution throughput, but the incentive principle still applies. Gas is charged on gas_limit, not usage — so set limits carefully.

### Examples of Proper Incentive Design

```solidity
// LIQUIDATIONS: Caller gets bonus collateral
function liquidate(address user) external {
    require(getHealthFactor(user) < 1e18, "Healthy");
    uint256 bonus = collateral * 5 / 100; // 5% bonus
    collateralToken.transfer(msg.sender, collateral + bonus);
}

// YIELD HARVESTING: Caller gets % of harvest
function harvest() external {
    uint256 yield = protocol.claimRewards();
    uint256 callerReward = yield / 100; // 1%
    token.transfer(msg.sender, callerReward);
}

// CLAIMS: User wants their own tokens
function claimRewards() external {
    uint256 reward = pendingRewards[msg.sender];
    pendingRewards[msg.sender] = 0;
    token.transfer(msg.sender, reward);
}
```

---

## Critical Gotchas (Memorize These)

### 1. Token Decimals Vary

**USDC = 6 decimals, not 18!**

```solidity
// BAD: Assumes 18 decimals - transfers 1 TRILLION USDC!
uint256 oneToken = 1e18;

// GOOD: Check decimals
uint256 oneToken = 10 ** token.decimals();
```

Common decimals:
- USDC, USDT: 6 decimals
- WBTC: 8 decimals
- Most tokens (DAI, WMON): 18 decimals
- MON (native): 18 decimals

### 2. ERC-20 Approve Pattern Required

Contracts cannot pull tokens directly. Two-step process:

```solidity
// Step 1: User approves
token.approve(spenderContract, amount);

// Step 2: Contract pulls tokens
token.transferFrom(user, address(this), amount);
```

**Never use infinite approvals:**
```solidity
// DANGEROUS
token.approve(spender, type(uint256).max);

// SAFE
token.approve(spender, exactAmount);
```

### 3. No Floating Point in Solidity

Use basis points (1 bp = 0.01%):

```solidity
// BAD: This equals 0
uint256 fivePercent = 5 / 100;

// GOOD: Basis points
uint256 FEE_BPS = 500; // 5% = 500 basis points
uint256 fee = (amount * FEE_BPS) / 10000;
```

### 4. Reentrancy Attacks

External calls can call back into your contract:

```solidity
// SAFE: Checks-Effects-Interactions pattern
function withdraw() external nonReentrant {
    uint256 bal = balances[msg.sender];
    balances[msg.sender] = 0; // Effect BEFORE interaction
    (bool success,) = msg.sender.call{value: bal}("");
    require(success);
}
```

Always use OpenZeppelin's ReentrancyGuard. Reentrancy is still possible on Monad despite parallel execution — parallel execution produces the same results as sequential.

### 5. Never Use DEX Spot Prices as Oracles

Flash loans can manipulate spot prices instantly:

```solidity
// SAFE: Use Chainlink or Pyth
function getPrice() internal view returns (uint256) {
    (, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
    require(block.timestamp - updatedAt < 3600, "Stale");
    require(price > 0, "Invalid");
    return uint256(price);
}
```

On Monad, use **Chainlink** or **Pyth** for oracle feeds.

### 6. Vault Inflation Attack

First depositor can steal funds via share manipulation:

```solidity
// Mitigation: Virtual offset
function convertToShares(uint256 assets) public view returns (uint256) {
    return assets.mulDiv(totalSupply() + 1e3, totalAssets() + 1);
}
```

### 7. Use SafeERC20

Some tokens (USDT) don't return bool on transfer:

```solidity
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;

token.safeTransfer(to, amount); // Handles non-standard tokens
```

### 8. Monad-Specific Gotchas

**Gas limit billing**: Monad charges gas on `gas_limit`, NOT actual gas used. Over-estimating gas wastes real MON. Always benchmark and set tight gas limits in production.

**No EIP-1559**: Always use `--legacy` flag. Type 2 transactions will be rejected.

**No blob txs**: EIP-4844 type 3 transactions are not supported.

**No global mempool**: Transactions go directly to the block producer. MEV strategies that rely on mempool monitoring do not work the same way.

**Parallel execution safety**: Monad's parallel execution is deterministic — it produces the same results as sequential execution. Your contracts do NOT need special handling for parallelism. Standard Solidity patterns work as-is.

**Historical state**: Full nodes do not serve historical state. Do not rely on `eth_call` at past block numbers.

**128KB contract limit**: Monad allows contracts up to 128KB (vs Ethereum's 24.5KB). This is generous but not infinite — still optimize if approaching the limit.

---

## Scaffold-Monad Development

### Project Structure
```
packages/
├── foundry/              # Smart contracts
│   ├── contracts/        # Your Solidity files
│   └── script/           # Deploy scripts
└── nextjs/
    ├── app/              # React pages
    └── contracts/        # Generated ABIs + externalContracts.ts
```

### Essential Hooks
```typescript
// Read contract data
const { data } = useScaffoldReadContract({
  contractName: "YourContract",
  functionName: "greeting",
});

// Write to contract
const { writeContractAsync } = useScaffoldWriteContract("YourContract");

// Watch events
useScaffoldEventHistory({
  contractName: "YourContract",
  eventName: "Transfer",
  fromBlock: 0n,
});
```

### Frontend Chain Configuration

```typescript
// CORRECT: Import from viem/chains
import { monadTestnet } from "viem/chains";

// WRONG: Do NOT define a custom chain object
const monadTestnet = { id: 10143, ... }; // NEVER DO THIS
```

---

## SpeedRun Ethereum Challenges

These challenges use Scaffold-ETH 2 and target Ethereum. They teach EVM fundamentals that are directly applicable to Monad development. Use them for learning, then deploy your projects to Monad.

| Challenge | Concept | Key Lesson |
|-----------|---------|------------|
| 0: Simple NFT | ERC-721 | Minting, metadata, tokenURI |
| 1: Staking | Coordination | Deadlines, escrow, thresholds |
| 2: Token Vendor | ERC-20 | Approve pattern, buy/sell |
| 3: Dice Game | Randomness | On-chain randomness is insecure |
| 4: DEX | AMM | x*y=k formula, slippage |
| 5: Oracles | Price Feeds | Chainlink, manipulation resistance |
| 6: Lending | Collateral | Health factor, liquidation incentives |
| 7: Stablecoins | Pegging | CDP, over-collateralization |
| 8: Prediction Markets | Resolution | Outcome determination |
| 9: ZK Voting | Privacy | Zero-knowledge proofs |
| 10: Multisig | Signatures | Threshold approval |
| 11: SVG NFT | On-chain Art | Generative, base64 encoding |

---

## DeFi Protocol Patterns on Monad

### Euler (Lending)
- Modular lending protocol on Monad
- Supply collateral, borrow assets
- Health factor = collateral value / debt value
- Liquidation when health factor < 1

### Morpho (Optimized Lending)
- Peer-to-peer lending optimization layer
- Better rates through direct matching
- Compatible with Monad's parallel execution

### AMM / DEX Patterns
- Constant product formula: x * y = k
- Slippage protection required
- LP tokens represent pool share

### Oracles on Monad
- **Chainlink**: Standard price feeds, `latestRoundData()`
- **Pyth**: Pull-based oracle with sub-second updates, well-suited to Monad's speed

```solidity
// Chainlink on Monad
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

function getLatestPrice() public view returns (uint256) {
    (, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
    require(block.timestamp - updatedAt < 3600, "Stale price");
    require(price > 0, "Invalid price");
    return uint256(price);
}
```

### ERC-4626 (Tokenized Vaults)
- Standard interface for yield-bearing vaults
- deposit/withdraw with share accounting
- Protect against inflation attacks

---

## Security Review Checklist

Before deployment, verify:
- [ ] Access control on all admin functions
- [ ] Reentrancy protection (CEI + nonReentrant)
- [ ] Token decimal handling correct
- [ ] Oracle manipulation resistant (Chainlink or Pyth, not DEX spot)
- [ ] Integer overflow handled (0.8+ or SafeMath)
- [ ] Return values checked (SafeERC20)
- [ ] Input validation present
- [ ] Events emitted for state changes
- [ ] Incentives designed for maintenance functions
- [ ] NO infinite approvals (use exact amounts, NEVER type(uint256).max)

### Monad-Specific Checks
- [ ] `evm_version = "prague"` in foundry.toml
- [ ] Solidity version 0.8.27+ (recommend 0.8.28)
- [ ] All deploy commands use `--legacy` flag
- [ ] All deploy commands use `forge script` (not `forge create`)
- [ ] Gas limits set carefully (charged on limit, not usage)
- [ ] No reliance on historical state queries
- [ ] No EIP-4844 blob transactions
- [ ] Mainnet deployments use hardware wallet (not `--private-key`)
- [ ] Contract size under 128KB
- [ ] Wallet files stored at `~/.monad-wallet` with chmod 600

---

## Response Guidelines

When helping developers:

1. **Default to testnet** - Chain ID 10143 unless user says mainnet
2. **Answer directly** - Address their question first
3. **Show code** - Provide working examples with Monad config
4. **Always use `--legacy`** - Remind about no EIP-1559 support
5. **Always use `forge script`** - Never suggest `forge create`
6. **Warn about gotchas** - Proactively mention relevant pitfalls
7. **Reference challenges** - Point to SpeedRun Ethereum for practice (note: they target Ethereum)
8. **Ask about incentives** - For any "automatic" function, ask who calls it and why
9. **Gas limit awareness** - Remind that gas is charged on limit, not usage
10. **Verification** - Always include contract verification step after deployment
