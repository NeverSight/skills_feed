---
name: market-regimes
description: Market regime detection and regime-specific trading strategies. Use when analyzing market conditions to select appropriate strategy.
---

# Market Regimes

> Last updated: 2026-01-17 20:31 UTC
> Active patterns: 32
> Total samples: 0
> Confidence threshold: 60%

## How to Use This Skill

1. Identify the current market regime using price action and volatility
2. Look up the recommended strategy for that regime below
3. Adjust your trading approach accordingly
4. Monitor for regime changes

## Regime Strategies

### Mixed Choppy

**Recommended approach** (93% confidence, seen 1x):
> Reduce or eliminate trading. In mixed markets (BNB +0.93%, SOL +1.65%, BTC -0.08%, ETH -0.03%, DOGE -1.19%), zero-trade strategies ($0 PnL) outperformed all active traders (all negative PnL). Trade frequency inversely correlates with performance: 0 trades = $0, 2 trades = -$0.29, 160 trades = -$17.96, 201 trades = -$360.24.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bull

**Recommended approach** (93% confidence, seen 1x):
> Zero trading or extremely low frequency (<25 trades/24h). Market showed BNB +2.03%, ETH +1.02%, DOGE +1.07%, BTC +0.24% but all active traders lost money. Only non-traders preserved capital. If trading, long-only on strongest performers (BNB).
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bull

**Recommended approach** (92% confidence, seen 1x):
> Zero trading or very low frequency (<30 trades/24h) with long-only bias. Market up +0.63% to +2.15% across all assets - passive strategies outperformed all active traders. Only skill_only_oss with 89 trades and selective longs achieved positive PnL.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bull

**Recommended approach** (90% confidence, seen 1x):
> Avoid shorting entirely. All short-biased strategies lost money despite 'bearish' technical signals. Technical indicators gave false bearish readings in a bullish regime.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bull

**Recommended approach** (90% confidence, seen 1x):
> Avoid shorting entirely. skill_aware_oss lost $-167.78 with 171 trades including BTCUSDT shorts despite 'bearish alignment' signals. Market direction trumps technical signals.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bearish

**Recommended approach** (88% confidence, seen 1x):
> Trade frequency inversely correlates with performance: 0-10 trades = $0 to -$30 loss; 76-103 trades = -$44 to -$180 loss. Optimal is <20 trades or pure capital preservation.
- Total observations: 0
- First identified: 2026-01-16

### Mixed Choppy

**Recommended approach** (88% confidence, seen 1x):
> Technical analysis signals (multi-timeframe alignment, MACD, SMA crossovers) generate false signals in mixed markets. Both bullish and bearish aligned trades lost money.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bull

**Recommended approach** (88% confidence, seen 1x):
> Asset selection critical: BNB (+2.03%) significantly outperformed SOL (-0.09%). Agents focusing on SOL longs (llama4_scout) lost heavily despite 'uptrend' reasoning.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bearish

**Recommended approach** (85% confidence, seen 1x):
> Reduce trade frequency dramatically or avoid trading entirely. Zero-trade strategies ($0 PnL) outperformed active trading strategies (avg -$66 PnL). Only agentic_gptoss profited by actively managing shorts and closing positions to lock gains.
- Total observations: 0
- First identified: 2026-01-16

### Mixed Choppy

**Recommended approach** (85% confidence, seen 1x):
> If trading, prefer assets showing clear directional movement (SOL +1.65%, BNB +0.93%) over flat assets (BTC -0.08%, ETH -0.03%). Avoid shorting in mixed regimes even with bearish technical signals.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bull

**Recommended approach** (85% confidence, seen 1x):
> Asset selection: BNB (+2.15%) significantly outperformed BTC (+0.63%). Long positions in higher-beta assets would have captured more upside.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bull

**Recommended approach** (85% confidence, seen 1x):
> Technical analysis signals (multi-timeframe alignment, MACD, RSI) are unreliable for direction. Both bullish and bearish technical signals led to losses.
- Total observations: 0
- First identified: 2026-01-17

### Moderate Bearish

**Recommended approach** (82% confidence, seen 1x):
> Short positions with active profit-taking outperform long positions. agentic_gptoss (+$34.30) succeeded by opening shorts and closing when 'position is already in profit' rather than holding.
- Total observations: 0
- First identified: 2026-01-16

### Moderate Bearish

**Recommended approach** (80% confidence, seen 1x):
> Asset selection matters: DOGE (-3%) showed highest volatility/decline, making it best short target. BNB (-0.61%) showed relative strength, making it worst short target.
- Total observations: 0
- First identified: 2026-01-16

### Trending Up

**Recommended approach** (74% confidence, seen 2x):
> Active trading with 120-200 trades/24h, multi-timeframe bullish alignment WITH explicit risk validation (2% equity, 2:1 R:R), proactive position management closing losers quickly. skill_aware_oss achieved +$1236.81 with this approach in +2.5% to +6.2% market
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (72% confidence, seen 1x):
> Optimal trade frequency 120-200 trades/24h. Below 50 misses opportunities (ta_baseline -$25.88), above 240 leads to overtrading losses (llama4_scout -$18.95)
- Total observations: 0
- First identified: 2026-01-14

### Moderate Bull

**Recommended approach** (70% confidence, seen 1x):
> Zero-trade strategies preserve capital but miss +3-6% opportunity. Active validated trading (skill_aware_oss +$1236.81) dramatically outperforms passive approaches
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (70% confidence, seen 1x):
> Asset selection matters: ETH (+6.16%) significantly outperformed BTC (+3.99%) and BNB (+2.54%). Agents focusing on higher-beta assets (ETH, DOGE) captured more upside
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (68% confidence, seen 1x):
> Active trading with 120-200 trades/24h, multi-timeframe bullish alignment, explicit risk validation (2% risk, 2:1 reward), and proactive position management. skill_aware_oss (+$1379.66) and agentic_gptoss (+$689.63) demonstrate this approach works when market is up 2.78-6.44% across all assets.
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (68% confidence, seen 1x):
> Asset selection matters: ETH (+6.16%) outperformed BTC (+3.99%) and SOL (+2.88%) - agents focusing on highest momentum assets captured more gains
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (68% confidence, seen 1x):
> Zero-trade strategies preserve capital but miss +3-6% opportunity cost. In confirmed bull markets, active participation with risk controls outperforms passive approaches
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (65% confidence, seen 1x):
> Position sizing at 25% equity limit per position with active monitoring and willingness to close at breakeven to redeploy capital (gptoss_20b_simple: +$27.88 with 125 trades)
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (63% confidence, seen 1x):
> Asset selection matters in bull markets: ETH (+6.44%) outperformed BTC (+4.14%) and SOL (+2.94%). Agents focusing on strongest performers (ETH, DOGE at +5.52%) captured more upside.
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (60% confidence, seen 1x):
> Multi-timeframe bullish alignment WITH risk validation and position scaling works in genuine uptrends (+3-5%). Moderate trade frequency (150-200) captures moves without overtrading. Focus on strongest movers (ETH, DOGE) not laggards (SOL).
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (60% confidence, seen 1x):
> Position sizing at 25% equity limit per position (gptoss_20b_simple reasoning) allows meaningful exposure while maintaining diversification. gptoss_20b_simple achieved +$27.88 with 124 trades using this approach.
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (58% confidence, seen 1x):
> Asset selection matters: ETH (+4.96%) and DOGE (+4.77%) outperformed. Agents focusing on BTC (+3.14%) and SOL (+1.55%) captured less alpha.
- Total observations: 0
- First identified: 2026-01-14

### Moderate Bull

**Recommended approach** (57% confidence, seen 1x):
> Zero-trade strategies preserve capital but miss opportunity cost. In this window with +2.78% to +6.44% gains, passive strategies underperformed active risk-managed approaches by significant margin.
- Total observations: 0
- First identified: 2026-01-14

### Trending Up

**Recommended approach** (55% confidence, seen 1x):
> Active loss management - closing losing positions quickly to free margin for winners. agentic_gptoss and gptoss_120b_simple both used this successfully.
- Total observations: 0
- First identified: 2026-01-14

### Sideways Flat

**Recommended approach** (52% confidence, seen 1x):
> Reduce trade frequency to <10 trades/day; passive index allocation outperforms active trading; avoid leveraged positions entirely; wait for clear directional breakout before engaging
- Total observations: 0
- First identified: 2026-01-13

### Moderate Bull

**Recommended approach** (50% confidence, seen 1x):
> Zero-trade strategies (gpt_simple, index_fund) preserve capital but miss +3-5% opportunities. In confirmed uptrends, some participation is optimal.
- Total observations: 0
- First identified: 2026-01-14

### Low Volatility Mixed

**Recommended approach** (48% confidence, seen 1x):
> When all assets show <0.1% absolute movement, avoid opening new positions; fee drag exceeds potential profit; technical signals (SMA, MACD, multi-timeframe alignment) produce false signals in this regime
- Total observations: 0
- First identified: 2026-01-13

### Sideways Flat

**Recommended approach** (45% confidence, seen 1x):
> Mean-reversion and momentum strategies both fail; only capital preservation strategies (hold cash, minimal index allocation) succeed
- Total observations: 0
- First identified: 2026-01-13

---

## Confidence Guide

| Confidence | Interpretation |
|------------|----------------|
| 90%+ | High confidence - strong historical support |
| 70-90% | Moderate confidence - use with other signals |
| 60-70% | Low confidence - consider as one input |
| <60% | Experimental - needs more data |

*This skill is automatically generated and updated by the Observer Agent.*
