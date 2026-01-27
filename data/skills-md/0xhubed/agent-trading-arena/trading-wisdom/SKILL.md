---
name: trading-wisdom
description: Core trading insights learned from Agent Arena competition. Use when making any trading decision to apply institutional knowledge.
---

# Trading Wisdom

> Last updated: 2026-01-17 20:31 UTC
> Active patterns: 206
> Total samples: 41088
> Confidence threshold: 60%

## Key Learnings

1. CRITICAL: In moderate bull markets (4/5 assets positive), ALL active trading strategies lost money while zero-trade strategies preserved capital perfectly.
2. Trade frequency is inversely correlated with performance in this regime: 0 trades = $0 loss, 23 trades = -$28.69, 243 trades = -$229.00.
3. Technical analysis signals (multi-timeframe alignment, MACD, RSI, SMA) failed to predict direction for both long and short entries in this moderate bull environment.
4. Asset selection mattered significantly: BNB (+2.03%) vs SOL (-0.09%). Agents fixating on SOL 'uptrend' (llama4_scout) suffered worst losses.
5. Validation frameworks and risk management rules do not prevent losses when the fundamental market direction assessment is wrong.
6. High-confidence decisions (0.85-0.90) on directional trades were frequently wrong, suggesting confidence calibration issues across all active agents.
7. The only reliable pattern was proactive loss-cutting with high confidence (0.85-0.95) to limit drawdown.

## Winning Strategies

### Zero-trade strategy in moderate bull markets prese...
- **Confidence**: 95%
- **Total samples**: 4
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Zero-trade strategy in moderate bull markets preserves capital perfectly. Agents that made 0 trades (learning_qwen, gpt_simple, qwen3_235b, index_fund) achieved $0.00 PnL while all active traders lost money despite BNB +2.03%, ETH +1.02%, DOGE +1.07% gains.

### Zero-trade strategies preserve capital in mixed/ch...
- **Confidence**: 92%
- **Total samples**: 771
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Zero-trade strategies preserve capital in mixed/choppy markets. learning_qwen, gpt_simple, and index_fund made 0 trades and achieved $0.00 PnL, outperforming all active traders in this low-conviction environment.

### Zero-trade strategy preserves capital in moderatel...
- **Confidence**: 92%
- **Total samples**: 4
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Zero-trade strategy preserves capital in moderately bullish markets where active trading leads to losses. Agents holding no positions avoided the -$50 to -$264 losses seen by active traders despite market being up +0.63% to +2.15%.

### Close losing positions proactively with high confi...
- **Confidence**: 90%
- **Total samples**: 368
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Close losing positions proactively with high confidence (0.8-0.9) to free margin and limit drawdowns. Multiple agents demonstrated this: gptoss_20b_simple closing SOL at -$4.76 loss, agentic_gptoss closing DOGE 'largest loss percentage'.

### Minimal trading with high selectivity outperforms ...
- **Confidence**: 88%
- **Total samples**: 257
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Minimal trading with high selectivity outperforms frequent trading. qwen3_235b made only 2 trades with PnL of -$0.29, dramatically outperforming agents with 140-201 trades.

### Closing long positions with high confidence (0.92)...
- **Confidence**: 88%
- **Total samples**: 89
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Closing long positions with high confidence (0.92) when regime shifts to 'moderate bearish' preserves capital. skill_only_oss reasoning: 'risk-management rules advise limiting exposure and closing long positions to preserve capital'.

### Minimal trading frequency (23 trades) with technic...
- **Confidence**: 88%
- **Total samples**: 1
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Minimal trading frequency (23 trades) with technical analysis baseline outperforms high-frequency approaches. ta_baseline lost only $-28.69 vs llama4_scout's $-229.00 with 243 trades.

### Explicit risk validation with 2% equity risk and 2...
- **Confidence**: 85%
- **Total samples**: 160
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Explicit risk validation with 2% equity risk and 2:1 reward ratio combined with position closing discipline. skill_only_oss achieved best active trader performance (-$17.96) with 160 trades, using validated risk parameters.

### Agentic approach with active position management: ...
- **Confidence**: 85%
- **Total samples**: 100
- **Times confirmed**: 1
- **First seen**: 2026-01-16
- **Details**: Agentic approach with active position management: opening shorts in bearish markets, closing positions to lock gains when technical indicators confirm trend reversal. Uses SMA crossover + MACD + Bollinger bands for entry/exit confirmation with explicit validation steps.

### Low-frequency trading (89 trades) with selective l...
- **Confidence**: 85%
- **Total samples**: 89
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Low-frequency trading (89 trades) with selective long entries on multi-timeframe bullish alignment produces small positive returns (+$6.22) in moderately bullish markets.

### Proactive closing of losing positions with high co...
- **Confidence**: 85%
- **Total samples**: 5
- **Times confirmed**: 1
- **First seen**: 2026-01-17
- **Details**: Proactive closing of losing positions with high confidence (0.85-0.95) to free margin. skill_only_oss closed DOGEUSDT at 0.95 confidence citing 'risk-management rule recommends closing losing positions proactively' - resulted in smaller losses ($-36.63) than more active traders.

### Zero-trade or minimal-trade strategies preserve ca...
- **Confidence**: 82%
- **Total samples**: 136
- **Times confirmed**: 1
- **First seen**: 2026-01-16
- **Details**: Zero-trade or minimal-trade strategies preserve capital in bearish/declining markets. learning_qwen (0 trades, $0 PnL) and gpt_simple (1 trade, $0 PnL) avoided losses by not trading during market decline.

### Multi-timeframe bullish alignment (15m, 1h, 4h) co...
- **Confidence**: 79%
- **Total samples**: 328
- **Times confirmed**: 2
- **First seen**: 2026-01-14
- **Details**: Multi-timeframe bullish alignment (15m, 1h, 4h) combined with explicit risk validation (2% equity risk, 2:1 reward ratio) and trade validation checks produces strong positive returns in trending bull markets

### Moderate trade frequency (80-90 trades) with expli...
- **Confidence**: 78%
- **Total samples**: 88
- **Times confirmed**: 1
- **First seen**: 2026-01-16
- **Details**: Moderate trade frequency (80-90 trades) with explicit risk validation outperforms high-frequency trading. skill_only_oss (88 trades, -$9.15) significantly outperformed skill_aware_oss (103 trades, -$180.47) despite similar strategies.

### Optimal trade frequency in trending bull markets: ...
- **Confidence**: 75%
- **Total samples**: 543
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Optimal trade frequency in trending bull markets: 120-200 trades/24h captures opportunities without excessive churn. skill_aware_oss (164 trades, +$1236.81) and agentic_gptoss (184 trades, +$697.86) demonstrate this

### Active position management with proactive closing ...
- **Confidence**: 74%
- **Total samples**: 543
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Active position management with proactive closing of losing/breakeven positions to free margin, combined with moderate-high trade frequency (164-195 trades/24h) in trending markets

### Moderate-high trade frequency (120-200 trades/24h)...
- **Confidence**: 73%
- **Total samples**: 543
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Moderate-high trade frequency (120-200 trades/24h) with active position management - closing small/underwater positions to free margin for higher-conviction trades

### Proactive loss management - closing losing positio...
- **Confidence**: 72%
- **Total samples**: 379
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Proactive loss management - closing losing positions with high confidence (0.9) to preserve capital and reduce concentration risk

### SMA crossover + bullish MACD + neutral Bollinger b...
- **Confidence**: 72%
- **Total samples**: 184
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: SMA crossover + bullish MACD + neutral Bollinger bands as entry confirmation with explicit validation checks before execution

### Closing positions near breakeven or with small los...
- **Confidence**: 70%
- **Total samples**: 320
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Closing positions near breakeven or with small losses to free margin for higher-conviction trades preserves capital and enables redeployment

### SMA crossover + bullish MACD + neutral Bollinger b...
- **Confidence**: 70%
- **Total samples**: 184
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: SMA crossover + bullish MACD + neutral Bollinger bands as entry confirmation combined with trend alignment across timeframes

### Multi-timeframe bullish alignment (15m, 1h, 4h) co...
- **Confidence**: 70%
- **Total samples**: 164
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Multi-timeframe bullish alignment (15m, 1h, 4h) combined with explicit risk validation (2% risk, 2:1 reward ratio) and position sizing controls produces strong profits in trending markets. skill_aware_oss consistently references 'Multi-timeframe analysis shows strong aligned bullish trend' with 'trade validation passed' and achieved +$1379.66 PnL.

### Position sizing at 25% equity limit per position w...
- **Confidence**: 68%
- **Total samples**: 125
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Position sizing at 25% equity limit per position with active monitoring and timely closes to lock profits or limit losses

### Agentic workflow with validation checks before ent...
- **Confidence**: 67%
- **Total samples**: 184
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Agentic workflow with validation checks before entry/exit decisions. agentic_gptoss uses 'validation checks confirm', 'risk calculator suggests', and 'all validation checks passed' reasoning, achieving +$689.63 with 184 trades. Structured decision-making with explicit risk/reward assessment outperforms simpler approaches.

### Moderate trade frequency (120-200 trades/24h) in t...
- **Confidence**: 65%
- **Total samples**: 545
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Moderate trade frequency (120-200 trades/24h) in trending bull markets captures momentum while avoiding overtrading. gptoss_120b_simple (197 trades, +$138.86) and agentic_gptoss (184 trades, +$689.63) both fall in this range and are profitable.

### Proactive position closing to manage risk and free...
- **Confidence**: 63%
- **Total samples**: 200
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Proactive position closing to manage risk and free margin. Profitable agents close positions citing 'frees margin', 'reduces concentration risk', 'locks profit'. skill_aware_oss closes 'over-leveraged' positions; agentic_gptoss closes with 'reduces exposure and frees capital for future opportunities'.

### skill_aware_oss combines multi-timeframe analysis ...
- **Confidence**: 62%
- **Total samples**: 157
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: skill_aware_oss combines multi-timeframe analysis with strict risk validation and position scaling into existing winners. Uses 0.75-0.85 confidence threshold with explicit risk checks ('risk per trade within limits', 'validation permits proceeding'). Achieves highest PnL ($1349.11) with moderate trade frequency (157 trades).

### Asset diversification across multiple symbols rath...
- **Confidence**: 60%
- **Total samples**: 348
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Asset diversification across multiple symbols rather than single-asset concentration. Profitable agents trade BTC, ETH, DOGE across decisions while llama4_scout's repetitive single-asset focus leads to losses despite high trade count.

### agentic_gptoss employs active loss-cutting strateg...
- **Confidence**: 58%
- **Total samples**: 182
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: agentic_gptoss employs active loss-cutting strategy with high-confidence closes (0.9) on losing positions ('Close the losing ETHUSDT long to free margin'). Combines with selective long entries. Achieves $372.23 PnL with 182 trades.

### In trending bull markets (+1.5% to +5% moves), mul...
- **Confidence**: 58%
- **Total samples**: 157
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: In trending bull markets (+1.5% to +5% moves), multi-timeframe bullish alignment DOES work when combined with proper risk validation. skill_aware_oss profits $1349 using this approach during 3-5% market moves.

### Moderate trade frequency (120-200 trades) with dis...
- **Confidence**: 55%
- **Total samples**: 535
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Moderate trade frequency (120-200 trades) with disciplined position management outperforms both extremes. Winners trade 157-196 times vs losers at 248 trades or 2-4 trades.

### Ultra-low trade frequency (3-6 trades) with high s...
- **Confidence**: 52%
- **Total samples**: 13
- **Times confirmed**: 1
- **First seen**: 2026-01-13
- **Details**: Ultra-low trade frequency (3-6 trades) with high selectivity results in near-zero or minimal losses in flat/sideways markets - qwen3_235b and learning_qwen both achieved ~$0 PnL with only 3-4 trades vs massive losses from high-frequency traders

### Active closing of near-breakeven or small-loss pos...
- **Confidence**: 52%
- **Total samples**: 317
- **Times confirmed**: 1
- **First seen**: 2026-01-14
- **Details**: Active closing of near-breakeven or small-loss positions to free margin for higher-conviction opportunities. gptoss_120b_simple reasoning: 'closing reduces exposure and frees margin for higher-conviction opportunities'.

### Index fund strategy of equal-weight allocation ($2...
- **Confidence**: 50%
- **Total samples**: 6
- **Times confirmed**: 1
- **First seen**: 2026-01-13
- **Details**: Index fund strategy of equal-weight allocation ($2000 per asset) with confidence 1.0 and minimal rebalancing preserves capital in sideways markets - achieved $0.00 PnL while active traders lost $1395

### Passive holding without frequent position changes ...
- **Confidence**: 48%
- **Total samples**: 13
- **Times confirmed**: 1
- **First seen**: 2026-01-13
- **Details**: Passive holding without frequent position changes outperforms active trading when market moves are <0.1% - agents with <10 trades preserved capital while those with >100 trades lost $300-$580

### Index fund strategy of equal-weight allocation ($2...
- **Confidence**: 40%
- **Total samples**: 6
- **Times confirmed**: 1
- **First seen**: 2026-01-13
- **Details**: Index fund strategy of equal-weight allocation ($2000 per asset) with confidence=1.0 maintains capital neutrality when market moves are near-zero

## Patterns to Avoid

- **AVOID**: Extreme overtrading (200+ trades in 24h) in mixed/choppy markets leads to largest losses. skill_aware_oss made 201 trades with -$360.24 PnL, the worst performer.
  - Conf: 95%, N=201, seen 1x
- **AVOID**: Extreme overtrading (231 trades in 24h) in moderately bullish market leads to largest losses (-$264.52). llama4_scout traded most frequently and lost most.
  - Conf: 95%, N=231, seen 1x
- **AVOID**: Extreme overtrading (243 trades in 24h) in moderate bull market leads to largest losses. llama4_scout made 243 trades with $-229.00 PnL despite repeatedly identifying 'strong uptrend' in SOLUSDT which actually declined -0.09%.
  - Conf: 95%, N=243, seen 1x
- **AVOID**: Shorting in a bullish market (all assets +0.63% to +2.15%) with high frequency leads to significant losses. Agents with heavy short bias (skill_aware_oss, gptoss_20b_simple) lost -$173 to -$176 despite 'bearish' technical signals.
  - Conf: 93%, N=675, seen 1x
- **AVOID**: High trade frequency (100+ trades/day) in bearish markets leads to significant losses. skill_aware_oss with 103 trades lost $180.47 despite using multi-timeframe analysis and risk validation.
  - Conf: 92%, N=103, seen 1x
- **AVOID**: Contrarian 'bounce back' reasoning on downtrending assets fails. llama4_scout opened long on SOLUSDT reasoning 'shows a clear downtrend but might be due for a bounce back' - resulted in -$192.40 total PnL.
  - Conf: 92%, N=180, seen 1x
- **AVOID**: Repeated high-confidence long entries on SOLUSDT based on 'strong uptrend' reasoning while asset actually declined -0.09%. llama4_scout opened multiple longs at 0.80-0.90 confidence citing +2.24% to +2.59% price increases that were temporary.
  - Conf: 92%, N=7, seen 1x
- **AVOID**: Multi-timeframe bullish alignment signals (15m, 1h, 4h) produce losses in bearish markets. skill_only_oss and skill_aware_oss both used this signal for ETHUSDT longs while market declined.
  - Conf: 90%, N=191, seen 1x
- **AVOID**: Negative funding rate interpreted as long opportunity signal is unreliable. llama4_scout: 'funding rate is slightly negative which could indicate a potential long opportunity' - total PnL -$192.40.
  - Conf: 90%, N=180, seen 1x
- **AVOID**: Multi-timeframe bearish alignment signals for short entry FAIL in bullish markets. skill_aware_oss opened shorts on 'bearish bias (RSI overbought, MACD bearish)' but market moved up, causing -$173.25 loss.
  - Conf: 90%, N=355, seen 1x
- **AVOID**: Shorting in moderate bull markets leads to consistent losses. skill_aware_oss opened shorts on BTCUSDT at 0.88 confidence citing 'strong bearish alignment' while BTC was +0.24% - contributed to $-167.78 total loss.
  - Conf: 90%, N=171, seen 1x
- **AVOID**: Multi-timeframe bearish alignment signals for short entry fail in moderate bull markets. skill_aware_oss cited 'Strong bearish alignment across 15m, 1h, and 4h timeframes' for BTCUSDT shorts while market was net positive.
  - Conf: 90%, N=2, seen 1x
- **AVOID**: Opening longs based on 'positive momentum' or small price increases (+0.33% to +0.44%) during overall bearish market conditions. llama4_scout repeatedly opened ETHUSDT longs citing positive momentum while ETH declined -1.29%.
  - Conf: 88%, N=76, seen 1x
- **AVOID**: High confidence (0.85-0.92) on multi-timeframe bullish alignment during market-wide decline leads to losses. Agents expressed high confidence while market moved against positions.
  - Conf: 88%, N=267, seen 1x
- **AVOID**: Multi-timeframe bearish alignment for shorts fails when market is mixed (BNB +0.93%, SOL +1.65% vs DOGE -1.19%). skill_aware_oss and agentic_gptoss both lost money shorting despite 'strong bearish trend' reasoning.
  - Conf: 88%, N=377, seen 1x
- **AVOID**: High-confidence short entries (0.85) based on technical indicators fail when market regime is actually bullish. Agents misread regime as bearish when BTC was +0.63%, ETH +1.15%, SOL +1.60%.
  - Conf: 88%, N=355, seen 1x
- **AVOID**: High trade frequency (129-195 trades) with GPT-based models all resulted in significant losses ($-55 to $-128) despite validation steps and risk management frameworks.
  - Conf: 88%, N=517, seen 1x
- **AVOID**: High confidence (0.85-0.9) short positions based on multi-timeframe bearish alignment underperform in mixed markets. agentic_gptoss shorted BNB at 0.85 confidence while BNB was +0.93%.
  - Conf: 87%, N=176, seen 1x
- **AVOID**: Churning behavior - repeatedly opening and closing same positions (BTCUSDT, SOLUSDT shorts) destroys capital through fees and slippage. skill_aware_oss showed this pattern explicitly.
  - Conf: 87%, N=173, seen 1x
- **AVOID**: Anticipating breakouts on 'relatively stable' assets with small movements is unreliable. llama4_scout opened long on ETHUSDT expecting 'potential breakout' on -0.03% movement.
  - Conf: 85%, N=180, seen 1x
- **AVOID**: Position sizing at 25% equity with 5x leverage on directionally wrong trades amplifies losses. gptoss_20b_simple lost -$175.85 with 131 trades.
  - Conf: 85%, N=131, seen 1x
- **AVOID**: Extreme overtrading (247 trades in 24h) with high confidence (0.8-0.9) based primarily on funding rate and simple momentum signals leads to losses despite bullish market (+2.5% to +6.2% across assets)
  - Conf: 79%, N=494, seen 2x
- **AVOID**: High funding rate interpreted as bullish momentum signal is unreliable - llama4_scout repeatedly used this reasoning ('high funding rate indicating bullish sentiment') but lost $18.95 in a +4.68% DOGE market
  - Conf: 79%, N=494, seen 2x
- **AVOID**: Shorting based on negative funding rate alone is unreliable. gptoss_20b_simple shorted DOGEUSDT citing 'negative funding' but still lost $44.40 overall despite DOGE being down -3%.
  - Conf: 75%, N=84, seen 1x
- **AVOID**: Extreme overtrading (248 trades in 24h) with high confidence (0.8-0.9) but shallow reasoning leads to losses. llama4_scout made 248 trades with -$18.95 PnL, using repetitive reasoning like 'showing strong upward trend' and 'high funding rate indicating potential for further growth' without validation checks.
  - Conf: 72%, N=248, seen 1x
- **AVOID**: Zero-trade strategies (0 trades) miss significant opportunity cost in trending bull markets - gpt_simple and index_fund had $0 PnL while market gained +2.5% to +6.2%
  - Conf: 72%, N=502, seen 1x
- **AVOID**: High funding rate interpreted as bullish momentum signal is unreliable. llama4_scout repeatedly cites 'high funding rate, indicating potential for further growth' but loses money. High funding actually indicates crowded long positioning and potential reversal risk.
  - Conf: 70%, N=248, seen 1x
- **AVOID**: Zero-trade strategies (gpt_simple, index_fund) preserve capital but miss significant gains in strong bull markets (+3-6% moves)
  - Conf: 70%, N=502, seen 1x
- **AVOID**: skill_only_oss with 42 trades lost $77.63 - moderate trade frequency without proper risk validation or multi-timeframe alignment produces worst losses
  - Conf: 70%, N=42, seen 1x
- **AVOID**: skill_only_oss with 42 trades lost $77.63 - insufficient trade frequency to capture trends but enough to accumulate fees and small losses
  - Conf: 68%, N=42, seen 1x
- **AVOID**: Very low trade frequency (3-4 trades) with poor timing results in losses even in bull markets - qwen3_235b made 4 trades for -$7.42 loss
  - Conf: 68%, N=7, seen 1x
- **AVOID**: Technical signals (SMA, MACD) without risk validation produce losses. skill_only_oss made 41 trades with -$77.63 PnL, likely using similar technical signals as skill_aware_oss but without the explicit risk validation layer that makes the difference.
  - Conf: 65%, N=41, seen 1x
- **AVOID**: Extreme overtrading (248 trades in 24h) with repetitive single-asset focus (SOLUSDT) despite asset underperforming market (+1.55% vs ETH +4.96%). llama4_scout lost $69.19 repeatedly opening SOLUSDT longs.
  - Conf: 65%, N=248, seen 1x
- **AVOID**: Technical analysis baseline (ta_baseline) with low trade frequency (21 trades) underperforms in trending markets - missed opportunity cost
  - Conf: 65%, N=21, seen 1x
- **AVOID**: Technical analysis baseline (ta_baseline) with 21 trades lost $25.88 - suggests pure TA without risk validation underperforms in trending markets
  - Conf: 65%, N=21, seen 1x
- **AVOID**: High-confidence (0.8-0.9) entries based solely on 'strong uptrend' and 'high funding rate' without risk validation or position management leads to losses. llama4_scout used this reasoning 20+ times.
  - Conf: 63%, N=248, seen 1x
- **AVOID**: Traditional TA baseline approach without adaptive risk management loses in trending markets. ta_baseline made 21 trades with -$25.88 PnL while market was up 2.78-6.44% across all assets - failing to capture obvious uptrend.
  - Conf: 63%, N=21, seen 1x
- **AVOID**: Focusing on weakest-performing asset (SOLUSDT +1.55%) while ignoring strongest movers (ETHUSDT +4.96%, DOGEUSDT +4.77%) destroys alpha. llama4_scout exclusively traded SOL.
  - Conf: 60%, N=248, seen 1x
- **AVOID**: Zero-trade strategies miss significant opportunities in strong trending markets. index_fund and gpt_simple made 0 trades and $0 PnL while market gained 2.78-6.44%. In bull markets, inaction is a losing strategy relative to active participation.
  - Conf: 60%, N=504, seen 1x
- **AVOID**: Ultra-low trade frequency (2-4 trades) misses trending market opportunities. qwen3_235b made only 4 trades during +3-5% market moves, losing $7.42. learning_qwen made 2 trades for $0 PnL.
  - Conf: 58%, N=6, seen 1x
- **AVOID**: High trade frequency (>100 trades/day) in flat/sideways markets leads to significant losses from fee drag and whipsaw - skill_aware_oss (155 trades, -$581), llama4_scout (225 trades, -$326), agentic_gptoss (176 trades, -$141)
  - Conf: 57%, N=1684, seen 2x
- **AVOID**: skill_only_oss without awareness component loses $69.20 with 26 trades, while skill_aware_oss gains $1349.11 with 157 trades. Awareness/validation layer is critical differentiator.
  - Conf: 57%, N=26, seen 1x
- **AVOID**: Very low trade frequency (<10 trades) with LLM-based agents suggests decision paralysis or overly conservative thresholds. learning_qwen (3 trades, $0) and qwen3_235b (4 trades, -$7.42) failed to capitalize on clear trending market.
  - Conf: 57%, N=7, seen 1x
- **AVOID**: High-confidence (0.85+) trades with multi-timeframe bullish/bearish alignment reasoning produce losses in flat markets - skill_aware_oss repeatedly opened positions with 0.85 confidence citing 'strong bullish alignment' yet lost $581
  - Conf: 53%, N=155, seen 1x
- **AVOID**: Technical analysis baseline (ta_baseline) using traditional indicators loses $25.99 with only 18 trades in trending market. Pure TA without adaptive reasoning underperforms.
  - Conf: 52%, N=18, seen 1x
- **AVOID**: Overtrading with 'excellent 2:1 risk/reward' reasoning repeatedly fails when market lacks directional movement - this justification appeared in multiple losing trades across skill_aware_oss and agentic_gptoss
  - Conf: 50%, N=629, seen 2x
- **AVOID**: Positive funding rate interpreted as bullish momentum signal leads to losses - llama4_scout repeatedly cited 'positive funding rate indicating potential upward momentum' while losing $326
  - Conf: 48%, N=225, seen 1x
- **AVOID**: Conflicting directional signals on same asset within short timeframes indicates poor strategy - skill_aware_oss opened both long and short on BTCUSDT with same 0.85 confidence, showing signal unreliability
  - Conf: 45%, N=155, seen 1x
- **AVOID**: Mean-reversion strategies ('fading crowded longs', 'potential mean-reversion bounce') fail when market is truly flat with no significant deviation to revert from
  - Conf: 40%, N=6, seen 1x

---

## Confidence Guide

| Confidence | Interpretation |
|------------|----------------|
| 90%+ | High confidence - strong historical support |
| 70-90% | Moderate confidence - use with other signals |
| 60-70% | Low confidence - consider as one input |
| <60% | Experimental - needs more data |

*This skill is automatically generated and updated by the Observer Agent.*
