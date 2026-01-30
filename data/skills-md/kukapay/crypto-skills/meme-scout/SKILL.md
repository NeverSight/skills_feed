---
name: meme-scout
description: Comprehensive tool for scouting trending meme coins on DEX platforms like DexScreener. Use for discovering trending tokens, analyzing price movements, volume data, and risk assessments. Supports multiple timeframes (5m, 1h, 6h, 24h) and includes risk checking capabilities for specific tokens.
---

# Meme Scout

This skill provides workflows for finding and analyzing trending meme coins on decentralized exchanges.

## Trending Tokens Discovery

### Timeframes Available

- 5 minutes: https://dexscreener.com/?rankBy=trendingScoreM5&order=desc
- 1 hour: https://dexscreener.com/?rankBy=trendingScoreH1&order=desc  
- 6 hours (default): https://dexscreener.com/
- 24 hours: https://dexscreener.com/?rankBy=trendingScoreH24&order=desc

### How to Fetch Trending Data

1. Use curl to fetch the HTML from the appropriate URL
2. Extract the __SERVER_DATA from the script tag using sed
3. Parse the JSON with Node.js VM to get the pairs array
4. Each pair contains: baseToken (name, symbol, address), priceUsd, priceChange (m5, h1, h6, h24), volume, liquidity, etc.

Example command for top 10 trending:

```bash
curl -s "https://dexscreener.com/?rankBy=trendingScoreH24&order=desc" | sed -n 's/.*window\.__SERVER_DATA\s*=\s*\(.*\);.*/\1/p' | node -e "
const fs = require('fs');
const input = fs.readFileSync(0, 'utf-8').trim();
const code = 'data = ' + input;
const vm = require('vm');
const sandbox = {data: null, URL: URL, Date: Date, undefined: undefined};
vm.runInNewContext(code, sandbox);
const pairs = sandbox.data.route.data.dexScreenerData.pairs.slice(0,10);
pairs.forEach(p => console.log(\`\${p.baseToken.name} | \${p.chainId} | $\${p.priceUsd} | \${p.priceChange.h24}% | \${p.baseToken.address}\`));
"
```

## Risk Assessment for Specific Tokens

### Steps to Check Risk

1. **DexScreener Audit**: Visit the pair page (https://dexscreener.com/{chainId}/{pairAddress}) and check the "Audit" section
2. **RugCheck.xyz**: For Solana tokens, use https://rugcheck.xyz/tokens/{tokenAddress}
3. **On-chain Analysis**: Check creator wallet, liquidity locks, token distribution
4. **General Red Flags**: Anonymous teams, Pump.fun origin, extreme volatility, no utility

### Risk Levels

- **Low**: Verified team, audited contracts, locked liquidity
- **Medium**: Some transparency, basic audit, moderate volatility  
- **High**: Anonymous creator, no locks, Pump.fun token, high volatility
- **Extreme**: Recent creation, suspicious patterns, social hype without substance

## References

See references/ for detailed guides:

- [DEX Screener API](references/dexscreener-api.md)
- [Risk Assessment Guide](references/risk-assessment.md)  
- [Pump.fun Risks](references/pump-fun-risks.md)

## Scripts

- scripts/fetch-trending.js: Node.js script for fetching trending data
- scripts/check-risk.sh: Bash script for basic risk checks</content>
<parameter name="filePath">./skills/meme-scout/SKILL.md