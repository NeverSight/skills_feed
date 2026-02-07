---
name: prediction-arbitrage-scout
description: Scout price discrepancies between Polymarket and Kalshi for discovery and comparison. Read-only; no execution.
version: "1.0.0"
license: MIT
allowed-tools: Read,Write,Bash(python:*),Glob,Grep,WebFetch
---

# Prediction Arbitrage Scout (Polymarket ↔ Kalshi)

Read-only scouting tool that identifies potential price discrepancies between Polymarket and Kalshi prediction markets.

## Purpose

Surface candidate markets where pricing diverges across Polymarket and Kalshi.  
This skill is intended for discovery, research, and prioritization, not automated trading or execution.

## Non-Goals

- No trade execution
- No guarantees of profitability
- No slippage, depth, or liquidity modeling
- No position sizing or risk management

Outputs from this skill must be validated against Kalshi orderbooks and market rules before any action.

## Overview

Workflow:
1. Fetch current public market prices from Polymarket
2. Fetch open public markets from Kalshi
3. Match events using fuzzy string similarity
4. Compute theoretical price discrepancies after basic fees
5. Generate CSV and Markdown reports for review

Results are ranked by headline price discrepancy, not tradable edge.

## Prerequisites

Tools:
- Read
- Write
- Bash (python)
- Glob
- Grep
- WebFetch

Environment:
- Python 3.x

Packages:
- requests
- pandas

Install:
pip install requests pandas

## Instructions

Step 1: Fetch Polymarket Data
Command:
python {baseDir}/scripts/fetch_polymarket.py

Output:
- polymarket_data.json

Step 2: Fetch Kalshi Data
Command:
python {baseDir}/scripts/fetch_kalshi.py

Output:
- kalshi_data.json

Step 3: Detect Price Discrepancies
Command:
python {baseDir}/scripts/detect_arbitrage.py

Notes:
- Uses fuzzy string similarity (default threshold: 0.7)
- Compares YES/NO prices across platforms
- Estimates theoretical spread after basic fees

Output:
- arbitrage_opportunities.csv

Step 4: Generate Summary Report
Command:
python {baseDir}/scripts/generate_report.py

Output:
- arbitrage_report.md

## Outputs

- polymarket_data.json: Raw Polymarket market data
- kalshi_data.json: Raw Kalshi market data
- arbitrage_opportunities.csv: Ranked discrepancy list
- arbitrage_report.md: Summary report for review

## Error Handling

Polymarket API Error:
- Verify Polymarket API availability
- Retry after a short delay

Kalshi API Error:
- Verify public endpoint availability
- Some endpoints may require auth; this skill uses public data only

No Matching Events Found:
- Increase fuzzy match threshold
- Manually map high-value series

Insufficient Price Data:
- Ensure both YES and NO prices exist on both platforms

## Interpretation Guidance

- Treat all outputs as signals, not decisions
- Validate market resolution rules
- Check liquidity and orderbook depth
- Consider timing and volatility
- Prefer manually mapped events over fuzzy matches for action

## Resources

- Polymarket fetcher: {baseDir}/scripts/fetch_polymarket.py
- Kalshi fetcher: {baseDir}/scripts/fetch_kalshi.py
- Discrepancy analyzer: {baseDir}/scripts/detect_arbitrage.py
- Report generator: {baseDir}/scripts/generate_report.py

## Usage

Run the full scouting pipeline:
python {baseDir}/scripts/fetch_polymarket.py
python {baseDir}/scripts/fetch_kalshi.py
python {baseDir}/scripts/detect_arbitrage.py
python {baseDir}/scripts/generate_report.py

This skill may be invoked to execute the full workflow automatically.
