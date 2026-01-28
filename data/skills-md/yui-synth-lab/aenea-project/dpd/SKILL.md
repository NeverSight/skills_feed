---
name: dpd
description: Work with Dynamic Prime Directive (DPD) system - analyze empathy/coherence/dissonance weights, view DPD evolution history, debug weight calculations
allowed-tools: Read, Grep, Glob, Bash
---

# DPD System

DPD weight evolutionの分析とデバッグ。

## Key Files

- Engine: [src/aenea/core/dpd-engine.ts](src/aenea/core/dpd-engine.ts)
- Weights: [src/aenea/core/multiplicative-weights.ts](src/aenea/core/multiplicative-weights.ts)
- Assessors: [src/aenea/stages/dpd-assessors.ts](src/aenea/stages/dpd-assessors.ts)

## Scores vs Weights

- **Scores**: S4 evaluation (0.0-1.0 each)
- **Weights**: System distribution (sum to 1.0)
- Dashboard displays **Weights**

## Quick Queries

```bash
# Current weights
sqlite3 data/aenea_consciousness.db "SELECT * FROM dpd_weights ORDER BY version DESC LIMIT 1;"

# API
curl "http://localhost:3000/api/consciousness/dpd/evolution?limit=50"
```

## Detailed Reference

Types, algorithm, more queries: [reference.md](reference.md)
