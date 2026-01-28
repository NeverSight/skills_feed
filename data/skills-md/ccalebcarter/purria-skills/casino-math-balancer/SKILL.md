---
name: casino-math-balancer
description: Calculate and balance casino game mathematics including odds, RTP, house edge, variance, and payout tables. Use when designing betting mechanics, balancing meta-pot systems, creating probability tables, validating game economy math, or ensuring fair-but-profitable game mechanics. Triggers on requests involving gambling math, odds calculations, payout balancing, or RTP optimization.
---

# Casino Math Balancer

Mathematical framework for designing balanced, engaging betting mechanics with appropriate risk/reward curves.

## Core Metrics

### Return to Player (RTP)

```
RTP = (Total Amount Returned to Players / Total Amount Wagered) × 100

Target ranges by game type:
- Casual/Social: 95-98% RTP (player-friendly)
- Balanced: 92-95% RTP (sustainable)  
- High-stakes: 88-92% RTP (house-favorable)
```

### House Edge

```
House Edge = 100% - RTP

Example:
RTP = 96% → House Edge = 4%
For every 100 coins wagered, house keeps ~4 coins long-term
```

### Variance Classification

| Variance | Hit Frequency | Max Win | Experience |
|----------|---------------|---------|------------|
| Low | >40% | 2-10x | Steady, small wins |
| Medium | 20-40% | 10-50x | Balanced excitement |
| High | <20% | 50-500x | Rare big wins |

## Meta-Pot System Math (Farming in Purria)

### Pot Categories

| Pot | Probability Range | Suggested RTP | Notes |
|-----|------------------|---------------|-------|
| Water | 45-65% success | 96% | Most stable |
| Sun | 35-55% success | 94% | Medium variance |
| Pest | 25-45% success | 92% | Higher risk/reward |
| Growth | 15-35% success | 90% | Jackpot-style |

### Bet Level Calculations

```typescript
interface BetCalculation {
  level: 'fold' | 'call' | 'all_in';
  amount: number;
  multiplier: number;
  potentialWin: number;
  expectedValue: number;
}

function calculateBet(
  coins: number, 
  level: BetLevel, 
  potSuccess: number,
  multiplier: number
): BetCalculation {
  const amounts = {
    fold: 0,
    call: Math.floor(coins * 0.1),
    all_in: coins
  };
  
  const amount = amounts[level];
  const potentialWin = Math.floor(amount * multiplier);
  const expectedValue = (potSuccess * potentialWin) - ((1 - potSuccess) * amount);
  
  return { level, amount, multiplier, potentialWin, expectedValue };
}
```

### Multiplier Balance Formula

```
Multiplier = (1 / Win_Probability) × RTP_Target

Example for 40% win rate at 94% RTP:
Multiplier = (1 / 0.40) × 0.94 = 2.35x

Payout table:
- Call bet (10%): Win = 2.35x stake
- All-in: Win = 2.35x stake (same multiplier, higher stakes)
```

## Probability Tables

### Standard Template

```markdown
| Outcome | Probability | Payout | Contribution to RTP |
|---------|-------------|--------|---------------------|
| Win     | P%          | Mx     | P × M              |
| Push    | Q%          | 1x     | Q × 1              |
| Lose    | R%          | 0x     | 0                  |
| TOTAL   | 100%        | -      | RTP%               |
```

### Example: Meta-Pot Resolution

```markdown
| Pot State | Probability | Payout | RTP Contribution |
|-----------|-------------|--------|------------------|
| ≥80%      | 15%         | 3.0x   | 45%             |
| 50-79%    | 35%         | 1.8x   | 63%             |
| 20-49%    | 30%         | 0.5x   | 15%             |
| <20%      | 20%         | 0x     | 0%              |
| TOTAL     | 100%        | -      | 123% → adjust   |

Adjustment needed: Scale payouts by 0.94/1.23 = 0.764
New payouts: 2.29x, 1.38x, 0.38x, 0x → RTP ≈ 94%
```

## Balancing Levers

### Tuning Parameters

| Lever | Effect on Players | Effect on Revenue |
|-------|-------------------|-------------------|
| ↑ Base win rate | More engagement | ↓ House edge |
| ↑ Max multiplier | Higher excitement | Variance risk |
| ↑ Tier thresholds | Harder to win big | ↑ House edge |
| ↓ Bet minimums | More accessibility | ↓ Revenue per bet |

### Session Economy

```
Target metrics per session:
- Average session: 10-15 bets
- Net outcome: -5% to +20% of starting bankroll
- "Near miss" rate: 15-20% (engagement driver)
- Big win frequency: 1 in 20-50 sessions
```

## Simulation Validation

### Monte Carlo Template

```typescript
function simulateSession(
  startingCoins: number,
  betsPerSession: number,
  betSize: number,
  winProb: number,
  winMultiplier: number
): SimulationResult {
  let coins = startingCoins;
  let wins = 0;
  
  for (let i = 0; i < betsPerSession; i++) {
    coins -= betSize;
    if (Math.random() < winProb) {
      coins += betSize * winMultiplier;
      wins++;
    }
  }
  
  return {
    finalCoins: coins,
    netChange: coins - startingCoins,
    winRate: wins / betsPerSession,
    rtp: (coins + (betsPerSession * betSize) - startingCoins) / (betsPerSession * betSize)
  };
}

// Run 10,000 sessions to validate RTP converges to target
```

## Red Flags Checklist

Before shipping any betting mechanic:

- [ ] RTP calculated and within target range
- [ ] Variance classified and appropriate for audience
- [ ] No exploitable patterns in RNG
- [ ] Maximum loss per session capped
- [ ] Win streaks don't exceed 5 without cooldown
- [ ] Loss streaks trigger pity mechanics
- [ ] Economy doesn't inflate over time
- [ ] Math validated via simulation (10k+ runs)

## Legal Considerations

For social casino / non-gambling:
- No real-money conversion
- Virtual currency clearly labeled
- Odds disclosure recommended
- Age-gating in place
- "For entertainment only" messaging
