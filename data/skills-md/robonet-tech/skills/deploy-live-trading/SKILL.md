---
name: deploy-live-trading
description: "Deploy and manage live trading agents on Hyperliquid. ⚠️ HIGH RISK - REAL CAPITAL AT STAKE ⚠️ Provides deployment_create (launch agent, $0.50), deployment_list (monitor), deployment_start/stop (control), and account tools (credit management). Supports EOA (1 deployment max) and Hyperliquid Vault (200+ USDC required, unlimited deployments). CRITICAL: NEVER deploy without thorough backtesting (6+ months, Sharpe >1.0, drawdown <20%). Start small, monitor daily, define exit criteria before deploying."
persona: ["trader"]
risk_level: "HIGH"
cost_profile: "$0.50 to create deployment, free for management"
tools:
  - mcp__workbench__deployment_create
  - mcp__workbench__deployment_list
  - mcp__workbench__deployment_start
  - mcp__workbench__deployment_stop
  - mcp__workbench__get_credit_balance
  - mcp__workbench__get_credit_transactions
related_skills:
  prerequisites:
    - test-trading-strategies
    - browse-robonet-data
  fallback: improve-trading-strategies
---

# Deploy Live Trading

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          ⚠️  LIVE TRADING RISKS REAL CAPITAL  ⚠️           ║
║                                                          ║
║  • You can lose ALL deployed capital                    ║
║  • Bugs in strategy code cause significant losses       ║
║  • Market conditions change - backtest ≠ live           ║
║  • NEVER deploy without thorough backtesting            ║
║  • Start with small capital to validate live behavior   ║
║  • Monitor deployments actively (daily minimum)         ║
║  • Define exit criteria BEFORE deploying                ║
║                                                          ║
║            THIS IS NOT A SIMULATION                      ║
║           REAL MONEY WILL BE TRADED                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

## Quick Start

This skill deploys strategies to live trading on Hyperliquid. Use ONLY after thorough backtesting and validation.

**Load the tools first**:
```
Use MCPSearch to select: mcp__workbench__deployment_create
Use MCPSearch to select: mcp__workbench__deployment_list
Use MCPSearch to select: mcp__workbench__deployment_stop
```

**BEFORE deploying, complete this checklist**:
- [ ] Backtested on 6+ months of data
- [ ] Sharpe ratio >1.0, max drawdown <20%
- [ ] Tested on multiple time periods
- [ ] Code reviewed for bugs
- [ ] Risk management validated (stop loss, position sizing)
- [ ] Credit balance sufficient
- [ ] Monitoring plan established
- [ ] Exit criteria defined
- [ ] Starting with small capital (<10% of intended final size)

**If ANY item unchecked, DO NOT DEPLOY**

**When to use this skill**:
- After extensive backtesting shows consistent profitability
- When ready to risk real capital
- When you can monitor the deployment actively

**When NOT to use this skill**:
- Strategy not thoroughly tested (use `test-trading-strategies` first)
- Haven't reviewed strategy code
- Don't have monitoring plan
- Can't check deployment daily for first week
- Haven't defined when to stop deployment

## Available Tools (6)

### deployment_create

**Purpose**: Deploy strategy to live trading on Hyperliquid

**Parameters**:
- `strategy_name` (required): Name of strategy to deploy
- `symbol` (required): Trading pair (e.g., "BTC-USDT")
- `timeframe` (required): Candle interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d)
- `leverage` (optional, 1-5): Position multiplier (default: 1)
- `deployment_type` (optional): "eoa" (wallet, default) or "vault"
- `vault_name` (required for vault): Unique vault name
- `vault_description` (optional): Vault description

**Returns**: Deployment ID, status, wallet address, configuration

**Pricing**: $0.50 per deployment

**Constraints**:
- **EOA**: Max 1 active deployment per wallet
- **Vault**: Requires 200+ USDC in wallet, unlimited deployments

**Use when**: All pre-deployment criteria met (see checklist)

### deployment_list

**Purpose**: Monitor active deployments

**Parameters**: None

**Returns**: List of all deployments with status, performance, configuration

**Pricing**: Free

**Use when**: Checking deployment status, monitoring performance

### deployment_start

**Purpose**: Resume stopped deployment

**Parameters**:
- `deployment_id` (required): ID of deployment to resume

**Returns**: Updated deployment status

**Pricing**: Free

**Use when**: Restarting previously stopped deployment after validation/fixes

### deployment_stop

**Purpose**: Halt live trading

**Parameters**:
- `deployment_id` (required): ID of deployment to stop

**Returns**: Updated deployment status

**Pricing**: Free

**Use when**:
- Live performance degrades significantly
- Need to update strategy code
- Market conditions change fundamentally
- ANY red flag triggered (see Red Flags section)

### get_credit_balance

**Purpose**: Check available USDC credits

**Parameters**: None

**Returns**: Current credit balance

**Pricing**: Free

**Use when**: Before deployment (verify sufficient credits), monitoring spending

### get_credit_transactions

**Purpose**: View credit transaction history

**Parameters**: None

**Returns**: List of credit transactions

**Pricing**: Free

**Use when**: Auditing spending, tracking costs

## Core Concepts

### Deployment Types

**EOA (Externally Owned Account)**:
```
Type: Direct wallet trading
Setup: Immediate (no additional requirements)
Limit: Max 1 active deployment per wallet
Complexity: Lower
Best for: Testing, personal trading, single strategy
Cost: $0.50 to create

Advantages:
✓ Simple setup
✓ Immediate deployment
✓ No minimum balance requirement

Disadvantages:
✗ Only 1 deployment per wallet
✗ No public performance tracking
✗ Personal wallet at risk
```

**Hyperliquid Vault**:
```
Type: Professional vault setup
Setup: Requires 200+ USDC in wallet
Limit: Unlimited deployments
Complexity: Higher
Best for: Multiple strategies, professional trading, public showcasing
Cost: $0.50 per deployment

Advantages:
✓ Unlimited deployments
✓ Public TVL and performance tracking
✓ Professional infrastructure
✓ Separate from personal wallet

Disadvantages:
✗ Requires 200+ USDC setup
✗ More complex configuration
✗ Public performance visibility
```

**Which to choose**:
```
Choose EOA if:
- First deployment (testing live behavior)
- Running single strategy
- Want simple setup
- Don't need multiple simultaneous strategies

Choose Vault if:
- Running multiple strategies
- Want professional setup
- Need public performance tracking
- Trading with significant capital
- Building track record
```

### Leverage Guidelines

**Understanding leverage**:
```
Leverage = Position size / Available capital

1x leverage: $1000 capital → $1000 position
2x leverage: $1000 capital → $2000 position
3x leverage: $1000 capital → $3000 position

Key points:
- Leverage multiplies BOTH gains AND losses
- Higher leverage = higher risk
- Liquidation risk increases with leverage
- Start conservative (1-2x)
```

**Recommended leverage by risk profile**:
```
Conservative (1x):
- No amplification
- Lower returns, lower risk
- Recommended for first deployments
- Drawdown ≈ backtest drawdown

Moderate (2-3x):
- 2-3× returns and risk
- Requires careful monitoring
- Only after 1x deployment validated
- Drawdown ≈ 2-3× backtest drawdown

Aggressive (4-5x):
- 4-5× returns and risk
- Very risky, high liquidation chance
- NOT recommended for most users
- Drawdown ≈ 4-5× backtest drawdown
- Can lose entire capital quickly
```

**Leverage and drawdown**:
```
Backtest: 15% max drawdown
1x deployment: 15% expected drawdown
2x deployment: 30% expected drawdown (may hit margin call)
3x deployment: 45% expected drawdown (very likely liquidation)

Rule: Keep leverage low enough that backtest drawdown × leverage < 25%
```

### Risk Management in Live Trading

**Position sizing**:
```
Strategy controls position size via code (85-95% margin usage)
Deployment leverage multiplies available margin
Total risk = Strategy position size × Deployment leverage

Example:
- Capital: $1000
- Strategy uses 90% margin
- Deployment leverage: 2x
- Actual position: $1000 × 0.90 × 2 = $1800

Position size is LARGER than capital (risk of liquidation)
```

**Mental stop loss** (define BEFORE deploying):
```
Example thresholds:
- Stop if down 10% from starting capital
- Stop if down 15% from peak
- Stop if drawdown >1.5× backtest max drawdown

Write down your threshold:
"I will stop this deployment if capital drops to $______"

DO NOT move this threshold once deployed (discipline is critical)
```

**Monitoring frequency**:
```
First 24-48 hours: Check every 2-4 hours
First week: Check daily minimum
First month: Check every 2-3 days
After 1 month: Weekly check acceptable (if performing well)

NEVER:
- Deploy and forget
- Ignore for >1 week during first month
- Assume backtest = live performance
```

## Pre-Deployment Checklist

**Complete ALL items before deploying**:

### Strategy Validation
- [ ] **Backtested on 6+ months** (12+ months preferred)
- [ ] **Sharpe ratio >1.0** (preferably >1.5)
- [ ] **Max drawdown <20%** (acceptable risk level)
- [ ] **Win rate 45-65%** (realistic range)
- [ ] **Profit factor >1.5** (sufficient edge)
- [ ] **50+ trades in test** (statistical significance)
- [ ] **Multi-period validation** (consistent across different time ranges)
- [ ] **Out-of-sample test passed** (performed well on unseen data)

### Code and Logic Review
- [ ] **Strategy code reviewed** (no obvious bugs)
- [ ] **No look-ahead bias** (not using future data)
- [ ] **Indicators validated** (all indicators available and correct)
- [ ] **Risk management present** (stop loss and position sizing)
- [ ] **Realistic assumptions** (fees, slippage accounted for)

### Operational Readiness
- [ ] **Credit balance sufficient** (check with `get_credit_balance`)
- [ ] **Deployment type selected** (EOA vs Vault)
- [ ] **Leverage set conservatively** (1-2x for first deployment)
- [ ] **Monitoring plan established** (how often will you check?)
- [ ] **Exit criteria defined** (when will you stop?)
- [ ] **Starting capital decided** (how much to deploy?)
- [ ] **Capital is risk capital** (can afford to lose 100%)

**IF ANY ITEM UNCHECKED: DO NOT DEPLOY**

## Deployment Best Practices

### Start Small

**Initial deployment sizing**:
```
WRONG approach:
- Backtest shows 50% annual return
- Deploy $10,000 immediately
- If strategy fails, lose significant capital

RIGHT approach:
- Deploy $500-1000 initially (5-10% of intended size)
- Monitor for 1-2 weeks
- Validate live behavior matches backtest
- If successful, scale up gradually
- Reduce risk during validation phase

Scaling schedule example:
Week 1-2: $1,000 (test)
Week 3-4: $2,000 (if performing well)
Week 5-6: $4,000 (if still performing well)
Month 2+: Scale to full size gradually
```

**Why start small**:
- Live market is different from backtest
- Slippage may be higher
- Execution may differ
- Bugs may only appear in live trading
- Can stop with minimal loss if issues arise

### Monitoring Protocol

**What to track**:
```
1. P&L vs backtest expectation:
   - Is live performance similar to backtest?
   - Track daily, weekly, monthly returns
   - Compare to backtest metrics

2. Drawdown:
   - Current drawdown from peak
   - Compare to backtest max drawdown
   - If exceeds backtest max × 1.5, be concerned

3. Trade execution:
   - Are trades executing as expected?
   - Check fill prices (slippage)
   - Verify trade frequency matches backtest

4. Win rate and profit factor:
   - Track live win rate
   - Should be close to backtest win rate
   - If diverges >20%, investigate

5. Market regime:
   - Has market character changed?
   - Trending → ranging or vice versa
   - Strategy may stop working if regime shifts
```

**Daily monitoring checklist (first week)**:
- [ ] Check P&L (profit/loss today)
- [ ] Check position status (in trade or flat?)
- [ ] Check recent trades (executed as expected?)
- [ ] Check drawdown (within acceptable range?)
- [ ] Note any unusual behavior

### Red Flags - Stop Deployment Immediately

**STOP deployment if ANY of these occur**:

**1. Excessive drawdown**:
```
Live drawdown >30% OR >1.5× backtest max drawdown
Example:
- Backtest max drawdown: 15%
- Threshold to stop: 22.5% (1.5× backtest)
- Current live drawdown: 25%
→ STOP IMMEDIATELY

Why: Strategy may be broken or market changed
```

**2. Win rate collapse**:
```
Live win rate <50% of backtest win rate
Example:
- Backtest win rate: 55%
- Threshold to stop: 27.5% (50% of backtest)
- Live win rate after 20 trades: 25%
→ STOP IMMEDIATELY

Why: Strategy logic not working in live market
```

**3. Unexpected trade frequency**:
```
Much higher or lower trade frequency than backtest
Example:
- Backtest: 2-3 trades per day
- Live: 15 trades per day
→ STOP IMMEDIATELY

Why: Strategy may be malfunctioning
```

**4. Consistent losses**:
```
10+ consecutive losing trades (when backtest shows max 5-6)
→ STOP IMMEDIATELY

Why: Strategy edge may have disappeared
```

**5. Technical issues**:
```
- Orders not executing
- Repeated API errors
- Position sizing errors
- Strategy crashes/restarts frequently
→ STOP IMMEDIATELY

Why: Technical problems = unpredictable risk
```

**6. Market regime change**:
```
Market conditions fundamentally different from backtest period
Examples:
- Extreme volatility event (>3× normal)
- Major regulatory news
- Exchange issues
→ STOP, REASSESS, decide if/when to restart

Why: Strategy designed for different conditions
```

### Post-Deployment Analysis

**After 1 week of live trading**:
```
1. Compare metrics:
   | Metric         | Backtest | Live  | Variance |
   |----------------|----------|-------|----------|
   | Sharpe         | 1.5      | 1.3   | -13%     |
   | Drawdown       | 12%      | 15%   | +25%     |
   | Win rate       | 52%      | 49%   | -6%      |
   | Profit factor  | 1.8      | 1.6   | -11%     |

2. Evaluate variance:
   - Small variance (<20%) → Expected, continue ✓
   - Moderate variance (20-40%) → Monitor closely, may be temporary
   - Large variance (>40%) → Significant concern, consider stopping

3. Decision:
   - If metrics acceptable: Continue monitoring
   - If metrics concerning: Investigate cause
   - If red flags present: Stop deployment
```

**After 1 month**:
```
Review:
- Total return vs expectation
- Max drawdown experienced
- Trade execution quality
- Any technical issues

Decide:
- Scale up capital (if performing well)
- Continue same size (if acceptable)
- Scale down or stop (if underperforming)
```

## Common Workflows

### Workflow 1: First Deployment (EOA)

**Goal**: Deploy strategy for first time to validate live behavior

```
1. Final pre-deployment check:
   ☑ Backtested 6+ months (Sharpe 1.4, drawdown 14%)
   ☑ Code reviewed (no bugs found)
   ☑ Risk management validated
   ☑ Starting capital: $500 (can afford to lose)
   ☑ Monitoring plan: Check daily for first week
   ☑ Exit criteria: Stop if down >20% or drawdown >25%

2. Check credit balance:
   get_credit_balance()
   → Balance: 100 USDC ✓ (sufficient for deployment $0.50)

3. Deploy:
   deployment_create(
       strategy_name="RSIMeanReversion_M",
       symbol="BTC-USDT",
       timeframe="1h",
       leverage=1,  # Conservative for first deployment
       deployment_type="eoa"
   )
   → Deployment ID: abc123
   → Status: Active
   → Cost: $0.50

4. Monitor closely:
   Day 1: Check every 4 hours
   Day 2-7: Check daily
   Track: P&L, drawdown, trade execution

5. After 1 week:
   Review performance vs backtest
   If good: Continue and consider scaling up
   If poor: Stop and analyze what went wrong
```

**Cost**: $0.50

### Workflow 2: Managing Multiple Strategies (Vault)

**Goal**: Deploy multiple strategies using Hyperliquid Vault

```
1. Setup vault (one-time):
   - Verify 200+ USDC in wallet
   - Decide vault name (unique, descriptive)

2. Deploy first strategy:
   deployment_create(
       strategy_name="TrendFollower_M",
       symbol="BTC-USDT",
       timeframe="4h",
       leverage=2,
       deployment_type="vault",
       vault_name="AlgoTrading_Vault_2025",
       vault_description="Multi-strategy algorithmic trading vault"
   )
   → Vault created successfully

3. Deploy second strategy (same vault):
   deployment_create(
       strategy_name="MeanReversion_L",
       symbol="ETH-USDT",
       timeframe="1h",
       leverage=1,
       deployment_type="vault",
       vault_name="AlgoTrading_Vault_2025"  # Same vault name
   )

4. Monitor all deployments:
   deployment_list()
   → Shows both strategies with individual performance

5. Manage independently:
   - Can stop one strategy without affecting other
   - Each strategy tracks separate P&L
   - Vault shows combined performance
```

**Cost**: $0.50 per deployment = $1.00 total

### Workflow 3: Stopping Underperforming Deployment

**Goal**: Stop deployment when red flags appear

```
1. Monitor deployment:
   deployment_list()
   → Strategy: MomentumBreakout_H
   → P&L: -18% (started $1000, now $820)
   → Drawdown: 28%
   → Red flag: Drawdown > 1.5× backtest max (15% × 1.5 = 22.5%)

2. Decision: STOP (red flag triggered)

3. Stop deployment:
   deployment_stop(deployment_id="abc123")
   → Status: Stopped
   → Final P&L: -$180 (-18%)

4. Analyze what went wrong:
   - Review trade history
   - Check market conditions during deployment
   - Compare to backtest assumptions
   - Identify issue (market regime change? bug? bad luck?)

5. Next steps:
   - Fix issues if identified (use improve-trading-strategies)
   - Re-backtest with improvements
   - Deploy again with smaller capital if confident
   - Or abandon strategy if fundamentally broken
```

**Cost**: Free to stop

### Workflow 4: Restarting After Market Change

**Goal**: Restart deployment after temporary stop

```
1. Previously stopped deployment due to high volatility event
   Stopped during extreme market conditions

2. Market stabilizes:
   - Check current market conditions
   - Compare to backtest environment
   - Decide conditions are favorable again

3. Review strategy:
   - Re-backtest on recent data
   - Verify strategy still works
   - Check no code changes needed

4. Restart deployment:
   deployment_start(deployment_id="abc123")
   → Status: Active (resumed)

5. Monitor closely:
   - First day: Check multiple times
   - Verify execution matches expectations
   - Be ready to stop again if issues recur
```

**Cost**: Free

## Troubleshooting

### "Insufficient Credits"

**Issue**: Cannot create deployment (balance too low)

**Solutions**:
```
1. Check balance:
   get_credit_balance() → Balance: 0.20 USDC

2. Purchase credits:
   - Visit Robonet dashboard
   - Add credits to account
   - Deployment costs $0.50

3. Retry deployment after purchase
```

### "Max 1 EOA Deployment"

**Issue**: Trying to create second EOA deployment

**Solutions**:
```
1. Stop existing EOA deployment:
   deployment_list() → Find existing deployment
   deployment_stop(deployment_id="existing_id")

2. Or switch to Hyperliquid Vault:
   - Requires 200+ USDC in wallet
   - Allows unlimited deployments
   - Use deployment_type="vault"

3. Or use different wallet (new EOA)
```

### "Vault Creation Failed"

**Issue**: Cannot create Hyperliquid Vault

**Solutions**:
```
1. Verify 200+ USDC in wallet:
   - Check wallet balance on Hyperliquid
   - Vault requires minimum balance

2. Check vault name unique:
   - Try different vault name
   - Vault names must be unique across Hyperliquid

3. Verify wallet permissions:
   - Ensure wallet connected properly
   - Check Hyperliquid account status
```

### "Live Performance Much Worse Than Backtest"

**Issue**: Strategy profitable in backtest, losing in live

**Common causes & solutions**:
```
1. Slippage higher than expected:
   - Market less liquid than backtest assumed
   - Solution: Use wider stops, lower frequency trades, or stop deployment

2. Fees not properly accounted:
   - Forgot to include fees in backtest
   - Solution: Re-backtest with realistic fees (0.05-0.1%)

3. Market regime changed:
   - Trending market → ranging market
   - Solution: Strategy may not work in current conditions, stop deployment

4. Execution delays:
   - Live trades execute slower than backtest assumed
   - Solution: Use longer timeframes (1h instead of 5m)

5. Overfitted strategy:
   - Strategy memorized past data
   - Solution: Simplify strategy, re-backtest, test on out-of-sample data

Decision: If performance -30% worse than backtest, STOP and fix issues
```

## Legal & Compliance

**Important disclaimers**:
```
⚠️ Trading crypto perpetuals is HIGH RISK
⚠️ Regulations vary by jurisdiction
⚠️ You are responsible for compliance with local laws
⚠️ This is NOT financial advice
⚠️ Trade at your own risk
⚠️ Only risk capital you can afford to lose 100%
```

**User responsibilities**:
- Verify trading is legal in your jurisdiction
- Understand tax implications of trading
- Report trading activity as required by law
- Comply with local financial regulations
- Maintain records of trading activity

**Platform disclaimers**:
- Robonet provides tools, not financial advice
- Past performance doesn't guarantee future results
- No warranty on strategy performance
- User bears all risk of capital loss

## Next Steps

**If deployment is performing well**:
- Continue monitoring regularly
- Track performance vs backtest expectations
- Consider gradual capital scaling after 1 month
- Document what's working for future strategies

**If deployment is underperforming**:
- Use `improve-trading-strategies` skill to refine
- Re-backtest improvements thoroughly
- Test with small capital again before scaling

**After successful deployment**:
- Share learnings (what worked, what didn't)
- Consider deploying additional strategies
- Build track record for future deployments

## Summary

This skill provides **live trading deployment and management**:

- **6 tools**: deployment_create ($0.50), deployment_list/start/stop (free), account tools (free)
- **Risk**: HIGH (real capital at risk)
- **Purpose**: Deploy validated strategies to live trading

**Core principle**: Thorough preparation → small initial deployment → active monitoring → gradual scaling. Never deploy without extensive backtesting and clear exit criteria.

**Critical warnings**:
- You can lose ALL deployed capital
- Backtest ≠ live performance (expect differences)
- Start small ($500-1000) to validate live behavior
- Monitor daily for first week, weekly thereafter
- Stop immediately if red flags appear (drawdown >1.5× backtest, win rate collapses, technical issues)
- Define exit criteria BEFORE deploying (don't move goalposts)

**Pre-deployment checklist must be 100% complete**: Backtest >6 months, Sharpe >1.0, drawdown <20%, code reviewed, monitoring plan, exit criteria, starting small, risk capital only.

**Best practice**: Treat first deployment as validation phase, not profit phase. Goal is to confirm strategy works live, not to make money immediately. Profits come after validation succeeds.

**Remember**: This is real money, real risk, real consequences. If uncomfortable with any aspect of deployment, DON'T DEPLOY. It's better to miss opportunity than lose capital.
