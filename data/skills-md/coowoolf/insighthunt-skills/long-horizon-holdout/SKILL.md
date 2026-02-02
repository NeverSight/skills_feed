---
name: long-horizon-holdout
description: Use when running experiments on platforms where user value compounds over time, when growth teams claim credit for revenue that would have happened anyway, or when short-term wins don't translate to long-term value
---

# The Long-Horizon Holdout Protocol

## Overview

A measurement framework that challenges short-term growth wins by maintaining **long-term control groups (holdouts)** to verify if immediate lifts translate to sustainable value over 1-3 years.

**Core principle:** 30-40% of short-term "wins" show neutral or zero impact long-term.

## The Process

```
┌─────────────────────────────────────────────────────────────────┐
│  T-0 (Launch)                                                   │
│  Split Traffic: 90% Treatment / 10% Long-term Holdout           │
├─────────────────────────────────────────────────────────────────┤
│  T+3 Weeks                                                      │
│  Initial Decision: Ship if short-term positive/neutral          │
│  Keep holdout running                                           │
├─────────────────────────────────────────────────────────────────┤
│  T+6 Months                                                     │
│  Automated Ping: Check retention and emerging GMV patterns      │
├─────────────────────────────────────────────────────────────────┤
│  T+12-18 Months                                                 │
│  Final Reckoning: Compare Cohort GMV                            │
│  If neutral/negative: deprecate feature or pivot strategy       │
└─────────────────────────────────────────────────────────────────┘
```

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Long holdout** | Keep control group for 12-18 months |
| **Automated pings** | System reminds team to check at 6, 12 months |
| **Cohort GMV focus** | Long-term value, not short-term conversion |
| **Accept reversals** | Be willing to deprecate "successful" features |

## Common Mistakes

- Declaring victory after 2 weeks of significance
- Assuming neutral short-term = failure (might compound later)
- Not setting up infrastructure for long-term tracking

---

*Source: Archie Abrams (Shopify VP Product & Growth) via Lenny's Podcast*
