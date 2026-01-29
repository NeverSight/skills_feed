---
name: solodit
description: Search 50,000+ smart contract vulnerabilities from Cyfrin Solodit. 8 MCP tools with intelligent caching for searching, filtering, and analyzing blockchain security findings.
mcp:
  - name: solodit-api
    command: npx
    args: ["-y", "BowTiedSwan/solodit-api-skill"]
    env:
      CYFRIN_API_KEY: "${CYFRIN_API_KEY}"
---

# Solodit API Skill

Search and retrieve smart contract security vulnerabilities from Cyfrin Solodit - the world's largest database of blockchain security findings.

## Overview

Solodit aggregates 50,000+ security findings from top audit firms including Cyfrin, Sherlock, Code4rena, Trail of Bits, OpenZeppelin, and more. This skill provides 8 MCP tools with intelligent caching:

- **search_vulnerabilities** - Search by keywords, severity, audit firm, tags, protocol, and more
- **get_finding** - Retrieve a specific finding by ID or slug
- **list_audit_firms** - List all available audit firms (cached 24h)
- **list_tags** - List all vulnerability tags (cached 24h)
- **list_protocol_categories** - List protocol categories (DeFi, NFT, Lending, etc.)
- **list_languages** - List supported languages (Solidity, Rust, Cairo, etc.)
- **get_statistics** - Database statistics and cache status
- **clear_cache** - Clear cached data for fresh results

## Setup

### 1. Get Your API Key

1. Create an account at [solodit.cyfrin.io](https://solodit.cyfrin.io)
2. Click your profile dropdown in the top right corner
3. Open "API Keys" modal and generate a new API key

### 2. Set Environment Variable

```bash
export CYFRIN_API_KEY="sk_your_api_key_here"
```

Add to your shell profile (`~/.bashrc`, `~/.zshrc`) for persistence.

## MCP Tools Reference

### search_vulnerabilities

Search and filter security findings from the Solodit database.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `keywords` | string | Search terms (e.g., "reentrancy", "oracle manipulation") |
| `impact` | string[] | Severity filter: `["HIGH"]`, `["HIGH", "MEDIUM"]`, etc. |
| `audit_firms` | string[] | Filter by auditor: `["Cyfrin", "Sherlock"]` |
| `tags` | string[] | Vulnerability tags: `["Reentrancy", "Oracle", "Access Control"]` |
| `protocol_categories` | string[] | Protocol types: `["DeFi", "NFT", "Lending"]` |
| `languages` | string[] | Programming language: `["Solidity", "Rust", "Cairo"]` |
| `protocol` | string | Protocol name (partial match) |
| `min_quality` | number | Minimum quality score (1-5) |
| `sort` | string | Sort by: `"recency"`, `"quality"`, `"rarity"` |
| `page` | number | Page number (default: 1) |
| `page_size` | number | Results per page (max: 100, default: 20) |

### get_finding

Retrieve a specific vulnerability by its ID or slug.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Finding ID (numeric) or slug (URL-friendly identifier) |
| `verbose` | boolean | Include full content and summary (default: true) |

### list_audit_firms

List all available audit firms in the database. Cached for 24 hours.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `refresh` | boolean | Force refresh the cached list (default: false) |

### list_tags

List all available vulnerability tags. Cached for 24 hours.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `refresh` | boolean | Force refresh the cached list (default: false) |

### list_protocol_categories

List all protocol categories (DeFi, NFT, Lending, DEX, Bridge, etc.).

### list_languages

List all supported programming languages (Solidity, Rust, Cairo, Vyper, Move, Huff, Fe, Ink!).

### get_statistics

Get database statistics including total findings, cache status, and rate limit info.

### clear_cache

Clear cached data to fetch fresh results.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Cache type: `"all"`, `"search"`, `"findings"`, `"metadata"` |

## Caching

The MCP server implements intelligent caching to reduce API calls:

| Cache Type | TTL | Purpose |
|------------|-----|---------|
| Search Results | 5 minutes | Recent search queries |
| Individual Findings | 1 hour | Findings by ID/slug |
| Metadata | 24 hours | Audit firms, tags lists |

## Curl Fallback

For environments without MCP support, use curl directly:

### Basic Search

```bash
curl -X POST https://solodit.cyfrin.io/api/v1/solodit/findings \
  -H "Content-Type: application/json" \
  -H "X-Cyfrin-API-Key: $CYFRIN_API_KEY" \
  -d '{
    "page": 1,
    "pageSize": 20
  }'
```

### Search with Filters

```bash
curl -X POST https://solodit.cyfrin.io/api/v1/solodit/findings \
  -H "Content-Type: application/json" \
  -H "X-Cyfrin-API-Key: $CYFRIN_API_KEY" \
  -d '{
    "page": 1,
    "pageSize": 20,
    "filters": {
      "keywords": "reentrancy",
      "impact": ["HIGH", "MEDIUM"],
      "sortField": "Quality",
      "sortDirection": "Desc"
    }
  }'
```

### Filter by Audit Firm

```bash
curl -X POST https://solodit.cyfrin.io/api/v1/solodit/findings \
  -H "Content-Type: application/json" \
  -H "X-Cyfrin-API-Key: $CYFRIN_API_KEY" \
  -d '{
    "page": 1,
    "pageSize": 20,
    "filters": {
      "firms": [{"value": "Cyfrin"}, {"value": "Sherlock"}],
      "impact": ["HIGH"]
    }
  }'
```

## Example Workflows

### Security Audit Preparation

```
Search for all HIGH severity findings in lending protocols from the last 90 days, sorted by quality score
```

### Vulnerability Research

```
Find oracle manipulation vulnerabilities in DeFi protocols with quality score 4 or higher
```

### Learning Specific Attack Patterns

```
Search for flash loan attack examples with tag "Flash Loan" sorted by rarity
```

### Exploring the Database

```
List all audit firms available in the database
```

```
Get database statistics
```

## Rate Limiting

- **Limit**: 20 requests per 60-second window
- **Headers**: Check `X-RateLimit-Remaining` in responses
- **Caching**: Significantly reduces API calls
- **Warnings**: Alerts when ≤5 requests remaining

## Common Tags

- Reentrancy
- Oracle
- Access Control
- Integer Overflow/Underflow
- Front-running
- Price Manipulation
- Flash Loan
- Griefing
- DOS
- Logic Error

## Common Audit Firms

- Cyfrin
- Sherlock
- Code4rena
- Trail of Bits
- OpenZeppelin
- Consensys Diligence
- Spearbit
- Pashov Audit Group
- Hacken
- ChainSecurity

## Protocol Categories

- DeFi
- NFT / NFT Marketplace
- Lending / NFT Lending
- DEX
- Staking / Liquid Staking
- Governance / DAO
- Bridge / Cross-Chain
- Yield Aggregator
- Options / Options Vault
- Oracles
- Gaming
- RWA

## Support

- **API Docs**: [Cyfrin Notion](https://cyfrin.notion.site/Cyfrin-Solodit-Findings-API-Specification)
- **Website**: [solodit.cyfrin.io](https://solodit.cyfrin.io)
- **Support**: support@cyfrin.io
