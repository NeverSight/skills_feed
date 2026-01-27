---
name: risk-management
description: Risk management rules learned from competition outcomes. Use when sizing positions or setting stop-losses.
---

# Risk Management

> Last updated: 2026-01-17 20:31 UTC
> Active patterns: 40
> Total samples: 13385
> Confidence threshold: 60%

## Core Principles

These rules are derived from analyzing profitable vs losing trades:

| Rule | Success Rate | Samples | Confidence | Seen |
|------|-------------|---------|------------|------|
| Trade count inversely correlates with pe... | 95% | 861 | 55% | 1x |
| Trade frequency should adapt to market r... | 95% | 950 | 95% | 1x |
| Validate risk per trade explicitly befor... | 92% | 157 | 65% | 1x |
| Validate risk per trade explicitly befor... | 92% | 164 | 70% | 1x |
| Trade frequency should adapt to market r... | 92% | 895 | 95% | 1x |
| Trade frequency should adapt to market r... | 92% | 855 | 95% | 1x |
| Validate risk per trade explicitly befor... | 92% | 328 | 79% | 2x |
| Optimal trade frequency in trending bull... | 90% | 543 | 75% | 1x |
| Optimal trade frequency in trending bull... | 88% | 1088 | 79% | 2x |
| Close losing positions proactively with ... | 88% | 184 | 75% | 1x |
| Close short positions immediately when m... | 88% | 675 | 95% | 1x |
| Close losing positions proactively with ... | 88% | 368 | 79% | 2x |
| High confidence (>0.8) should require co... | 85% | 20 | 50% | 1x |
| Close losing positions proactively with ... | 85% | 182 | 65% | 1x |
| Position sizing at 25% equity limit per ... | 85% | 321 | 70% | 1x |
| Diversify across multiple assets (BTC, E... | 85% | 494 | 79% | 2x |
| Close losing positions proactively with ... | 85% | 100 | 95% | 1x |
| Close losing positions proactively with ... | 85% | 368 | 95% | 1x |
| Optimal trade frequency in trending mark... | 82% | 535 | 65% | 1x |
| Diversify across multiple assets (BTC, E... | 82% | 348 | 70% | 1x |
| Close positions near breakeven to free m... | 82% | 390 | 79% | 2x |
| Explicit validation step before trade ex... | 80% | 100 | 95% | 1x |
| Close positions near breakeven to free m... | 80% | 144 | 95% | 1x |
| Diversify across assets rather than conc... | 78% | 248 | 65% | 1x |
| Position sizing at 25% equity limit per ... | 78% | 125 | 75% | 1x |
| Trade frequency should adapt to market r... | 78% | 507 | 95% | 1x |
| Validate risk per trade explicitly befor... | 75% | 160 | 95% | 1x |
| Position sizing at 25% equity limit per ... | 74% | 285 | 99% | 2x |
| Close positions near breakeven to free m... | 73% | 278 | 99% | 2x |
| High confidence (>0.8) should require co... | 70% | 20 | 40% | 1x |
| Position sizing at 2% risk with 2:1 rewa... | 65% | 139 | 45% | 1x |
| Position sizing at 25% equity limit per ... | 65% | 121 | 65% | 1x |
| Explicit validation step ('Validate_trad... | 65% | 176 | 95% | 1x |
| Close losing positions proactively with ... | 60% | 189 | 95% | 1x |
| Explicit validation step before trade ex... | 45% | 182 | 95% | 1x |
| Position sizing at 2% equity risk with 2... | 35% | 191 | 95% | 1x |
| 2% equity risk with 2:1 reward ratio fai... | 35% | 173 | 95% | 1x |
| Explicit validation step ('Validate_trad... | 35% | 195 | 95% | 1x |
| Position sizing at 2% equity risk with 2... | 30% | 171 | 95% | 1x |
| Position sizing at 2% risk with 2:1 rewa... | 15% | 155 | 55% | 1x |

## Top Risk Rules

### Trade count inversely correlates with performance in flat markets: 3-6 trades = ~$0 PnL, 70-180 trades = -$55 to -$141, 150-225 trades = -$325 to -$581
- Success rate: 95%
- Based on 861 observations
- Confidence: 55% (seen 1 times)
- First identified: 2026-01-13

### Trade frequency should adapt to market regime: mixed/choppy markets require 0-10 trades/24h maximum. 201 trades = -$360.24, 2 trades = -$0.29, 0 trades = $0.00.
- Success rate: 95%
- Based on 950 observations
- Confidence: 95% (seen 1 times)
- First identified: 2026-01-17

### Validate risk per trade explicitly before entry. skill_aware_oss reasoning includes 'risk per trade within limits' and 'portfolio risk is within limits' - this validation step correlates with +$1349 PnL.
- Success rate: 92%
- Based on 157 observations
- Confidence: 65% (seen 1 times)
- First identified: 2026-01-14

### Validate risk per trade explicitly before entry with 2% equity risk and 2:1 reward ratio. skill_aware_oss reasoning includes 'risk/reward is 2:1 with 2% equity risk' and 'trade validation passed', achieving best performance (+$1379.66).
- Success rate: 92%
- Based on 164 observations
- Confidence: 70% (seen 1 times)
- First identified: 2026-01-14

### Trade frequency should adapt to market regime: moderate bull markets require 0-30 trades/24h maximum. Above 100 trades correlates with losses (-$50 to -$264).
- Success rate: 92%
- Based on 895 observations
- Confidence: 95% (seen 1 times)
- First identified: 2026-01-17

## General Guidelines

- Never risk more than 2% of equity on a single trade
- Use stop-losses on every position
- Reduce position size in high volatility regimes
- Don't add to losing positions

---

## Confidence Guide

| Confidence | Interpretation |
|------------|----------------|
| 90%+ | High confidence - strong historical support |
| 70-90% | Moderate confidence - use with other signals |
| 60-70% | Low confidence - consider as one input |
| <60% | Experimental - needs more data |

*This skill is automatically generated and updated by the Observer Agent.*
