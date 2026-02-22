---
name: check-bsv-price
description: This skill should be used when the user asks "what is BSV price", "BSV to USD", "current BSV rate", "BSV market cap", or needs to fetch current BSV price and exchange rate information.
allowed-tools: "Bash(bun:*)"
---

# Check BSV Price

Get current BSV price from WhatsOnChain API.

## Status

**Complete** - All tests passing

## When to Use

- Check current BSV/USD exchange rate
- Calculate transaction values in USD
- Monitor BSV price movements
- Display market information

## Usage

```bash
# Get price in human-readable format
bun run skills/check-bsv-price/scripts/price.ts

# Get price in JSON format
bun run skills/check-bsv-price/scripts/price.ts --json

# Show help
bun run skills/check-bsv-price/scripts/price.ts --help
```

## API Endpoint

WhatsOnChain Exchange Rate API:
- `GET https://api.whatsonchain.com/v1/bsv/main/exchangerate`

## Response

Returns current price information including:
- Rate (USD)
- Currency
- Timestamp

## No Authentication Required

WhatsOnChain API is public and doesn't require API keys for basic queries.
