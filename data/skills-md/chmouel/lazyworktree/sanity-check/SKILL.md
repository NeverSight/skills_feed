---
name: sanity-check
description: Run full quality check with live results
---

# Sanity Check

Run comprehensive quality checks and report results.

## Current Git Status
!`git status --short`

## Lint Results
!`make lint 2>&1 | head -30`

## Test Results
!`go test ./... -short 2>&1 | tail -20`

## Coverage
!`go test ./... -cover 2>&1 | grep coverage`

---

Analyse these results and report:
1. Any blocking issues that must be fixed
2. Files that need attention
3. Coverage gaps in tested packages
4. Summary of overall project health
