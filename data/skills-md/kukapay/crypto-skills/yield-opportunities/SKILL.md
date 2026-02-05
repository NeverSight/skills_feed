---
name: yield-opportunities
description: Comprehensive tool for finding and analyzing DeFi yield opportunities across protocols, chains, and asset types. Use when users want to earn yield on crypto assets (staking, lending, liquidity farming, aggregators). Supports exhaustive parallel research using librarian agents, direct web searches, and GitHub repository analysis.
---

# Yield Opportunities

This skill provides comprehensive workflows for discovering and analyzing DeFi yield opportunities across multiple protocols, blockchains, and yield-generating strategies.

## Core Research Methodology

### Parallel Exploration Strategy (MAXIMIZE EFFORT)

When researching yield opportunities, launch multiple background agents IN PARALLEL:

1. **Librarian Agents** (3-6 concurrent) - Best for external research:
   - Protocol-specific yield documentation
   - Yield aggregator platforms
   - GitHub repositories for yield trackers
   - Liquidity mining programs
   - Staking/restaking opportunities
   - Cross-chain bridging options (if applicable)

2. **Direct Tools** - Use in parallel with librarian agents:
   - `websearch_web_search_exa` - For current APYs, platform comparisons
   - `grep_app_searchGitHub` - For open-source yield trackers
   - `webfetch` - To fetch specific documentation pages

## Yield Categories to Research

### 1. Staking (Delegation)

**What to find:**
- Native chain staking (validator delegation)
- Liquid staking protocols (LSTs)
- Restaking opportunities (EigenLayer, etc.)
- Minimum staking amounts
- Lock-up periods and unbonding times
- Current APY ranges
- Validator selection criteria

**Key Platforms by Chain:**
- **ETH:** Lido (stETH), Rocket Pool (rETH), EigenLayer
- **BNB:** Native BSC delegation, Ankr, Trust Wallet staking
- **SOL:** Marinade, Jito, Lido
- **Other Chain-Specific:** Research native staking options

### 2. Lending Protocols

**What to find:**
- Major lending platforms on the chain
- Supply APYs for the asset
- Borrow APYs (for leverage strategies)
- Protocol TVL and security/audit status
- Collateral factors and LTV limits
- Liquidation risks

**Top Platforms:**
- **ETH:** Aave, Compound, Morpho, Euler
- **BSC:** Venus, Alpaca Finance, Cream
- **Arbitrum/Optimism:** Aave V3, Radiant

### 3. Liquidity Farming (LP Pools)

**What to find:**
- Major DEXs on the chain (Uniswap, PancakeSwap, Curve, etc.)
- Top LP pools involving the asset
- APR/APY breakdown (trading fees + farm rewards)
- Impermanent loss risk assessment
- Pool liquidity and volume data
- Reward token quality

**Pool Types:**
- **Stablecoin pairs:** Lower impermanent loss, lower yields
- **Token pairs:** Higher impermanent loss, higher yields
- **V3 vs V2:** Different mechanics, active vs passive management

### 4. Yield Aggregators (Auto-Compounding)

**What to find:**
- Aggregator platforms supporting the chain
- Vault strategies for the asset
- Auto-compounding frequency
- Performance fee structure
- Vault TVL and track record
- Strategy description (what they do with your funds)

**Top Aggregators:**
- **Multi-chain:** Beefy Finance, Yearn Finance, Autofarm, Harvest
- **Chain-specific:** ACryptoS (BSC), Idle Finance (ETH)

### 5. Cross-Chain Opportunities (If applicable)

**What to find:**
- Can asset be bridged to other chains?
- Bridge options and fees
- Yield opportunities on destination chains
- Bridge security track record
- Whether bridging is worth the risk/cost

**Decision Framework:**
- Bridging only recommended if yield differential >5-10%
- Verify bridge security (official bridges preferred)
- Consider gas costs + bridge fees

## Reference Sources

### Primary Aggregators (Start Here)

| Platform | Coverage | Daily Updates |
|----------|----------|---------------|
| **DefiLlama** | 14,149 pools, 495 protocols, 110 chains | Yes |
| **Vaults.fyi** | 500+ vaults | Yes |
| **DexLender** | Stablecoin lending rates | Yes |
| **CoinMarketCap Yield** | Multi-asset, DeFi & CeFi | Yes |

### Protocol Documentation

Always reference official docs:
- Aave: https://docs.aave.com/
- Venus: https://docs-v4.venus.io/
- Beefy: https://docs.beefy.finance/
- PancakeSwap: https://docs.pancakeswap.finance/
- Curve: https://docs.curve.fi/

## Workflow for Single Asset Request

### Example: "I have BNB, how to earn?"

```
Step 1: Launch 5-6 librarian agents in parallel:
  - BNB staking options (delegation, liquid staking)
  - BSC lending protocols (Venus, Alpaca)
  - BNB liquidity farming (PancakeSwap, Biswap pools)
  - BSC yield aggregators (Beefy, Autofarm vaults)
  - BNB bridging options (if worth exploring)

Step 2: Run parallel websearch queries:
  - Current APYs for BNB staking
  - Venus Protocol BNB supply rates
  - PancakeSwap BNB pool APRs
  - Beefy BNB vault performance

Step 3: Collect and synthesize findings:
  - Organize by risk tolerance (Low/Medium/High)
  - Include current rates, requirements, risks
  - Provide decision framework

Step 4: Output structured recommendations:
  - Safest options (staking, single-token vaults)
  - Medium risk (lending, stablecoin LP)
  - High risk (volatile LP, farming)
  - Risk assessment for each option
```

## Risk Assessment Framework

### Risk Levels

| Level | Examples | Typical APY Range | Key Risks |
|-------|----------|------------------|-----------|
| **Low** | Native staking, liquid staking, CeFi vaults | 3-8% | Chain risks, price volatility |
| **Medium** | Lending, stablecoin LP, single-token vaults | 5-28% | Smart contract risk, liquidation |
| **High** | Token LP farming, yield aggregators | 20-100%+ | Impermanent loss, protocol risk |
| **Extreme** | New protocols, high-IL positions | 100%+ | Hack risks, rug scams |

### Must-Include Warnings

1. **Impermanent Loss (IL)**
   - Explain IL for liquidity pools
   - Note: Stablecoin pairs = minimal IL, Token pairs = high IL

2. **Smart Contract Risk**
   - Only recommend audited protocols with significant TVL
   - Check: Is this protocol audited? What's the TVL?

3. **Price Risk**
   - All yields are in the native asset
   - If asset drops, USD value drops

4. **Liquidation Risk**
   - For lending collateral positions
   - Keep LTV < 50% if borrowing

5. **Bridge Risk** (if bridging recommended)
   - Document bridge security
   - Note historical bridge hacks

## Output Structure

When presenting yield opportunities, use this format:

### 1. **Safest Options** (Low Risk)
- Method | APY | Requirements | Lock Period | Risk Notes

### 2. **Medium Risk** (Solid DeFi)
- Method | APY | Strategy | Trade-offs

### 3. **High Risk** (Maximum Yield)
- Method | APY | Strategy | Risks

### 4. **Risk Assessment**
- Detailed breakdown of each risk category
- What to watch out for

### 5. **Recommendation by Profile**
- Conservative / Balanced / Aggressive
- Best options for each user type

### 6. **Quick Start Guide**
- Step-by-step checklist
- Required tools (wallets, gas)
- Where to check current rates

## Agent Delegation Prompts

### Template for Librarian Agents

```
1. TASK: [Atomic task description]
2. EXPECTED OUTCOME: [Concrete deliverables with success criteria]
3. REQUIRED TOOLS: [Explicit tool whitelist]
4. MUST DO:
   - [Exhaustive requirements, leave nothing implicit]
   - [Get current 2025 information]
   - [Include URLs to official sources]
5. MUST NOT DO:
   - [Don't provide specific APY numbers - change too fast]
   - [Don't suggest protocols with known issues]
   - [Don't ignore risks]
6. CONTEXT: [User's situation and constraints]
```

### Example Prompt for Staking Research

```
1. TASK: Research [ASSET] staking options on [CHAIN]
2. EXPECTED OUTCOME: Complete list of staking options with validator info, APY ranges, how to stake, and requirements
3. REQUIRED TOOLS: websearch_web_search_exa, webfetch
4. MUST DO:
   - Research native chain staking validators (official docs)
   - Find current validator APYs and delegation process
   - Research liquid staking protocols
   - Document minimum amounts, lock periods, unbonding times
   - Include URLs to official staking interfaces
5. MUST NOT DO:
   - Don't recommend specific validators unless top-tier
   - Don't ignore staking risks (slashing, unbonding)
   - Don't speculate on future APY changes
6. CONTEXT: User has [ASSET] and wants safe staking yield
```

## Search Optimization

### Efficient Search Queries

Instead of broad queries, use specific patterns:

**Good:**
- "BNB BSC staking validators APY 2025"
- "Venus protocol BNB supply APY BSC"
- "PancakeSwap BNB liquidity pool APR"

**Avoid:**
- "yield opportunities" (too broad)
- "how to earn with BNB" (not specific enough)

### Time Management

- Stop searching when: Same info appearing across 3+ sources, or 2 iterations yielded no new data
- Parallel execution: Launch all librarian agents first, then direct tools
- Don't wait for librarian results - collect them all when needed

## Common Chains and Resources

### Ethereum
- **Staking:** Lido, Rocket Pool, EigenLayer
- **Lending:** Aave, Compound, Morpho
- **DEX:** Uniswap, Curve, Balancer
- **Aggregators:** Yearn, Beefy, Idle
- **Track yields:** DefiLlama /yields?chain=Ethereum

### BNB Smart Chain
- **Staking:** Native delegation (1 BNB min), Ankr, Trust Wallet
- **Lending:** Venus (largest), Alpaca Finance, Cream
- **DEX:** PancakeSwap (largest), Biswap
- **Aggregators:** Beefy BSC vaults, Autofarm, ACryptoS
- **Track yields:** DefiLlama /yields?chain=Bsc

### Solana
- **Staking:** Marinade, Jito, Lido
- **Lending:** Solend, Tulip
- **DEX:** Raydium, Orca, Jupiter
- **Track yields:** DefiLlama /yields?chain=Solana

### Arbitrum/Optimism
- **Lending:** Aave V3, Radiant
- **DEX:** Uniswap V3, Velodrome, Camelot
- **Track yields:** DefiLlama /yields?chain=Arbitrum

## References

See references/ for detailed guides:

- [Risk Assessment Framework](references/risk-assessment.md) - Detailed risk evaluation
- [Protocol Security Checklist](references/security-checklist.md) - Protocol vetting process
- [Yield Tracking Tools](references/yield-trackers.md) - Tools and APIs

## Scripts

- scripts/fetch-defillama-yields.py: Fetch current yields from DefiLlama API
- scripts/compare-protocols.sh: Compare yields across protocols
