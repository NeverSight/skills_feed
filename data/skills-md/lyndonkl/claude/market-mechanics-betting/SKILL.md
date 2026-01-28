---
name: market-mechanics-betting
description: Use to convert probabilities into decisions (bet/pass/hedge) and optimize scoring. Invoke when need to calculate edge, size bets optimally (Kelly Criterion), extremize aggregated forecasts, or improve Brier scores. Use when user mentions betting strategy, Kelly, edge calculation, Brier score, extremizing, or translating belief into action.
---

# Market Mechanics & Betting

## Table of Contents
- [What is Market Mechanics?](#what-is-market-mechanics)
- [When to Use This Skill](#when-to-use-this-skill)
- [Interactive Menu](#interactive-menu)
- [Quick Reference](#quick-reference)
- [Resource Files](#resource-files)

---

## What is Market Mechanics?

**Market mechanics** translates beliefs (probabilities) into actions (bets, decisions, resource allocation) using quantitative frameworks.

**Core Principle:** If you believe something with X% probability, you should be willing to bet at certain odds.

**Why It Matters:**
- Forces intellectual honesty (would you bet on this?)
- Optimizes resource allocation (how much to bet?)
- Improves calibration (betting reveals true beliefs)
- Provides scoring framework (Brier, log score)
- Enables aggregation (extremizing, market prices)

---

## When to Use This Skill

Use when:
- Converting belief to action - Have probability, need decision
- Betting decisions - Should I bet? How much?
- Resource allocation - How to distribute finite resources?
- Scoring forecasts - Measuring accuracy (Brier score)
- Aggregating forecasts - Combining multiple predictions
- Finding edge - Is my probability better than market?

Do NOT use when:
- No market/betting context exists
- Non-quantifiable outcomes
- Pure strategic analysis (no probability needed)

---

## Interactive Menu

**What would you like to do?**

### Core Workflows

**1. [Calculate Edge](#1-calculate-edge)** - Determine if you have an advantage
**2. [Optimize Bet Size (Kelly Criterion)](#2-optimize-bet-size-kelly-criterion)** - How much to bet
**3. [Extremize Aggregated Forecasts](#3-extremize-aggregated-forecasts)** - Adjust crowd wisdom
**4. [Optimize Brier Score](#4-optimize-brier-score)** - Improve forecast scoring
**5. [Hedge and Portfolio Betting](#5-hedge-and-portfolio-betting)** - Manage multiple bets
**6. [Learn the Framework](#6-learn-the-framework)** - Deep dive into methodology
**7. Exit** - Return to main forecasting workflow

---

## 1. Calculate Edge

**Determine if you have a betting advantage.**

```
Edge Calculation Progress:
- [ ] Step 1: Identify market probability
- [ ] Step 2: State your probability
- [ ] Step 3: Calculate edge
- [ ] Step 4: Apply minimum threshold
- [ ] Step 5: Make bet/pass decision
```

### Step 1: Identify market probability

**Sources:** Prediction markets (Polymarket, Kalshi), betting odds, consensus forecasts, base rates

**Converting betting odds to probability:**
```
Decimal odds: Probability = 1 / Odds
American (+150): Probability = 100 / (150 + 100) = 40%
American (-150): Probability = 150 / (150 + 100) = 60%
Fractional (3/1): Probability = 1 / (3 + 1) = 25%
```

### Step 2: State your probability

After running your forecasting process, state: **Your probability:** ___%

### Step 3: Calculate edge

```
Edge = Your Probability - Market Probability
```

**Interpretation:**
- **Positive edge:** More bullish than market → Consider betting YES
- **Negative edge:** More bearish than market → Consider betting NO
- **Zero edge:** Agree with market → Pass

### Step 4: Apply minimum threshold

**Minimum Edge Thresholds:**

| Context | Minimum Edge | Reasoning |
|---------|--------------|-----------|
| Prediction markets | 5-10% | Fees ~2-5%, need buffer |
| Sports betting | 3-5% | Efficient markets |
| Private bets | 2-3% | Only model uncertainty |
| High conviction | 8-15% | Substantial edge needed |

### Step 5: Make bet/pass decision

```
If Edge > Minimum Threshold → Calculate bet size (Kelly)
If 0 < Edge < Minimum → Pass (edge too small)
If Edge < 0 → Consider opposite bet or pass
```

**Next:** Return to [menu](#interactive-menu) or continue to Kelly sizing

---

## 2. Optimize Bet Size (Kelly Criterion)

**Calculate optimal bet size to maximize long-term growth.**

```
Kelly Criterion Progress:
- [ ] Step 1: Understand Kelly formula
- [ ] Step 2: Calculate full Kelly
- [ ] Step 3: Apply fractional Kelly
- [ ] Step 4: Consider bankroll constraints
- [ ] Step 5: Execute bet
```

### Step 1: Understand Kelly formula

```
f* = (bp - q) / b

Where:
f* = Fraction of bankroll to bet
b  = Net odds received (decimal odds - 1)
p  = Your probability of winning
q  = Your probability of losing (1 - p)
```

Maximizes expected logarithm of wealth (long-term growth rate).

### Step 2: Calculate full Kelly

**Example:**
- Your probability: 70% win
- Market odds: 1.67 (decimal) → Net odds (b): 0.67
- p = 0.70, q = 0.30

```
f* = (0.67 × 0.70 - 0.30) / 0.67 = 0.252 = 25.2%
```

Full Kelly says: **Bet 25.2% of bankroll**

### Step 3: Apply fractional Kelly

**Problem with full Kelly:** High variance, model error sensitivity, psychological difficulty

**Solution: Fractional Kelly**

```
Actual bet = f* × Fraction

Common fractions:
- 1/2 Kelly: f* / 2
- 1/3 Kelly: f* / 3
- 1/4 Kelly: f* / 4
```

**Recommendation:** Use 1/4 to 1/2 Kelly for most bets.

**Why:** Reduces variance by 50-75%, still captures most growth, more robust to model error.

### Step 4: Consider bankroll constraints

**Practical considerations:**
1. Define dedicated betting bankroll (money you can afford to lose)
2. Minimum bet size (market minimums)
3. Maximum bet size (market/liquidity limits)
4. Round to practical amounts

### Step 5: Execute bet

**Final check:**
- [ ] Confirmed edge > minimum threshold
- [ ] Calculated Kelly size
- [ ] Applied fractional Kelly (1/4 to 1/2)
- [ ] Checked bankroll constraints
- [ ] Verified odds haven't changed

**Place bet.**

**Next:** Return to [menu](#interactive-menu)

---

## 3. Extremize Aggregated Forecasts

**Adjust crowd wisdom when aggregating multiple predictions.**

```
Extremizing Progress:
- [ ] Step 1: Understand why extremizing works
- [ ] Step 2: Collect individual forecasts
- [ ] Step 3: Calculate simple average
- [ ] Step 4: Apply extremizing formula
- [ ] Step 5: Validate and finalize
```

### Step 1: Understand why extremizing works

**The Problem:** When you average forecasts, you get regression to 50%.

**The Research:** Good Judgment Project found aggregated forecasts are more accurate than individuals BUT systematically too moderate. Extremizing (pushing away from 50%) improves accuracy because multiple forecasters share common information, and simple averaging "overcounts" shared information.

### Step 2: Collect individual forecasts

Gather predictions from multiple sources. Ensure forecasts are independent, forecasters used good process, and have similar information available.

### Step 3: Calculate simple average

```
Average = Sum of forecasts / Number of forecasts
```

### Step 4: Apply extremizing formula

```
Extremized = 50% + (Average - 50%) × Factor

Where Factor typically ranges from 1.2 to 1.5
```

**Example:**
- Average: 77.6%
- Factor: 1.3

```
Extremized = 50% + (77.6% - 50%) × 1.3 = 85.88% ≈ 86%
```

**Choosing the Factor:**

| Situation | Factor | Reasoning |
|-----------|--------|-----------|
| Forecasters highly correlated | 1.1-1.2 | Weak extremizing |
| Moderately independent | 1.3-1.4 | Moderate extremizing |
| Very independent | 1.5+ | Strong extremizing |
| High expertise | 1.4-1.6 | Trust the signal |

**Default: Use 1.3 if unsure.**

### Step 5: Validate and finalize

**Sanity checks:**
1. **Bounded [0%, 100%]:** Cap at 99%/1% if needed
2. **Reasonableness:** Does result "feel" right?
3. **Compare to best individual:** Extremized should be close to best forecaster

**Next:** Return to [menu](#interactive-menu)

---

## 4. Optimize Brier Score

**Improve forecast accuracy scoring.**

```
Brier Score Optimization Progress:
- [ ] Step 1: Understand Brier score formula
- [ ] Step 2: Calculate your Brier score
- [ ] Step 3: Decompose into calibration and resolution
- [ ] Step 4: Identify improvement strategies
- [ ] Step 5: Avoid gaming the metric
```

### Step 1: Understand Brier score formula

```
Brier Score = (1/N) × Σ(Probability - Outcome)²

Where:
- Probability = Your forecast (0 to 1)
- Outcome = Actual result (0 or 1)
- N = Number of forecasts
```

**Range:** 0 (perfect) to 1 (worst). **Lower is better.**

### Step 2: Calculate your Brier score

**Interpretation:**

| Brier Score | Quality |
|-------------|---------|
| < 0.10 | Excellent |
| 0.10 - 0.15 | Good |
| 0.15 - 0.20 | Average |
| 0.20 - 0.25 | Below average |
| > 0.25 | Poor |

**Baseline:** Random guessing (always 50%) gives Brier = 0.25

### Step 3: Decompose into calibration and resolution

**Brier Score = Calibration Error + Resolution + Uncertainty**

**Calibration Error:** Do your 70% predictions happen 70% of the time? (measures bias)
**Resolution:** How often do you assign different probabilities to different outcomes? (measures discrimination)

### Step 4: Identify improvement strategies

**Strategy 1: Fix Calibration**
- If overconfident: Widen confidence intervals, be less extreme
- If underconfident: Be more extreme when you have strong evidence
- Tool: Calibration plot (X: predicted probability, Y: actual frequency)

**Strategy 2: Improve Resolution**
- Avoid being stuck at 50%
- Differentiate between easy and hard forecasts
- Be bold when evidence is strong

**Strategy 3: Gather Better Information**
- Do more research, use reference classes, decompose with Fermi, update with Bayes

### Step 5: Avoid gaming the metric

**Wrong approach:** "Never predict below 10% or above 90%" (gaming)

**Right approach:** Predict your TRUE belief. If that's 5%, say 5%. Accept that you'll occasionally get large Brier penalties. Over many forecasts, honesty wins.

**The rule:** Minimize Brier score by being **accurate**, not by being **safe**.

**Next:** Return to [menu](#interactive-menu)

---

## 5. Hedge and Portfolio Betting

**Manage multiple bets and correlations.**

```
Portfolio Betting Progress:
- [ ] Step 1: Identify correlations between bets
- [ ] Step 2: Calculate portfolio Kelly
- [ ] Step 3: Assess hedging opportunities
- [ ] Step 4: Optimize across all positions
- [ ] Step 5: Monitor and rebalance
```

### Step 1: Identify correlations between bets

**The problem:** If bets are correlated, true exposure is higher than sum of individual bets.

**Correlation examples:**
- **Positive:** "Democrats win House" + "Democrats win Senate"
- **Negative:** "Team A wins" + "Team B wins" (playing each other)
- **Uncorrelated:** "Rain tomorrow" + "Bitcoin price doubles"

### Step 2: Calculate portfolio Kelly

**Simplified heuristic:**
- If correlation > 0.5: Reduce each bet size by 30-50%
- If correlation < -0.5: Can increase total exposure slightly (partial hedge)

### Step 3: Assess hedging opportunities

**When to hedge:**
1. **Probability changed:** Lock in profit when beliefs shift
2. **Lock in profit:** Event moved in your favor, odds improved
3. **Reduce exposure:** Too much capital on one outcome

**Hedging example:**
- Bet $100 on A at 60% (1.67 odds) → Payout: $167
- Odds change: A now 70%, B now 30% (3.33 odds)
- Hedge: Bet $50 on B at 3.33 → Payout if B wins: $167
- **Result:** Guaranteed $17 profit regardless of outcome

### Step 4: Optimize across all positions

View portfolio holistically. Reduce correlated bets, maintain independence where possible.

### Step 5: Monitor and rebalance

**Weekly review:** Check if probabilities changed, assess hedging opportunities, rebalance if needed
**After major news:** Update probabilities, consider hedging, recalculate Kelly sizes
**Monthly audit:** Portfolio correlation check, bankroll adjustment, performance review

**Next:** Return to [menu](#interactive-menu)

---

## 6. Learn the Framework

**Deep dive into the methodology.**

### Resource Files

📄 **[Betting Theory Fundamentals](resources/betting-theory.md)**
- Expected value framework, variance and risk, bankroll management, market efficiency

📄 **[Kelly Criterion Deep Dive](resources/kelly-criterion.md)**
- Mathematical derivation, proof of optimality, extensions and variations, common mistakes

📄 **[Scoring Rules and Calibration](resources/scoring-rules.md)**
- Brier score deep dive, log score, calibration curves, resolution analysis, proper scoring rules

**Next:** Return to [menu](#interactive-menu)

---

## Quick Reference

### The Market Mechanics Commandments

1. **Edge > Threshold** - Don't bet small edges (5%+ minimum)
2. **Use Fractional Kelly** - Never full Kelly (use 1/4 to 1/2)
3. **Extremize aggregates** - Push away from 50% when combining forecasts
4. **Minimize Brier honestly** - Be accurate, not safe
5. **Watch correlations** - Portfolio risk > sum of individual risks
6. **Hedge strategically** - When probabilities change or lock profit
7. **Track calibration** - Your 70% should happen 70% of the time

### One-Sentence Summary

> Convert beliefs into optimal decisions using edge calculation, Kelly sizing, extremizing, and proper scoring.

### Integration with Other Skills

- **Before:** Use after completing forecast (have probability, need action)
- **Companion:** Works with `bayesian-reasoning-calibration` for probability updates
- **Feeds into:** Portfolio management and adaptive betting strategies

---

## Resource Files

📁 **resources/**
- [betting-theory.md](resources/betting-theory.md) - Fundamentals and framework
- [kelly-criterion.md](resources/kelly-criterion.md) - Optimal bet sizing
- [scoring-rules.md](resources/scoring-rules.md) - Calibration and accuracy measurement

---

**Ready to start? Choose a number from the [menu](#interactive-menu) above.**
