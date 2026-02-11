---
name: registry
version: 1.0.0
description: Pay-per-call API gateway for AI agents. 4 services available via x402 — no API keys, no subscriptions.
homepage: https://registry.mcpay.tech
metadata:
  category: api-gateway
  api_base: https://registry.mcpay.tech/api
  x402:
    supported: true
    chains:
      - evm
      - solana
    networks:
    - eip155:8453
    - eip155:84532
    - solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp
    - solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1
    tokens:
      - USDC
      - USDT
      - CASH
  services:
    count: 4
    slugs:
    - twitter
    - ai-gen
    - test
    - exa
    endpoints:
    twitter: /api/service/twitter
    ai-gen: /api/service/ai-gen
    test: /api/service/test
    exa: /api/service/exa
    skill_docs: /api/service/{slug}/skill.md
  wallet:
    recommended: agentwallet
    skill: https://agentwallet.mcpay.tech/skill.md
    endpoint: /x402/fetch
---

# Frames Registry

Pay-per-call API gateway for AI agents. 4 services available via the x402 payment protocol. No API keys, no subscriptions — just pay per request with crypto.

## Base URL

```
https://registry.mcpay.tech
```

## Prerequisites

A crypto wallet funded with USDC is required to use paid endpoints. Two options:

- **[AgentWallet](https://agentwallet.mcpay.tech/skill.md) (recommended for agents)** — server-side wallet that handles 402 detection, payment signing, and retries automatically via a single `POST /x402/fetch` call. No private key management needed on your side.
- **Self-managed wallet** — any EVM wallet (Base) or Solana wallet with USDC. You sign x402 payment headers directly.

## Quick Start

1. **Set up a wallet** — create an [AgentWallet](https://agentwallet.mcpay.tech/skill.md) or fund your own wallet with USDC
2. **Discover services:** `GET https://registry.mcpay.tech/api/services`
3. **Read service docs:** `GET https://registry.mcpay.tech/api/service/{slug}/skill.md`
4. **Check pricing:** `GET https://registry.mcpay.tech/api/pricing`
5. **Make a paid request** — via AgentWallet's `/x402/fetch` or directly with x402 headers (see Payment Protocol below)

## Services (4)

| Service | Slug | Description | Endpoints | Price Range |
|---------|------|-------------|-----------|-------------|
| [Twitter API](https://registry.mcpay.tech/api/service/twitter/skill.md) | `twitter` | Full Twitter API access - users, tweets, search, trends, and more via twitterapi.io | 17 | $0.005 - $0.02 |
| [AI Generation API](https://registry.mcpay.tech/api/service/ai-gen/skill.md) | `ai-gen` | Run AI models for image generation (FLUX, SDXL) and video generation (Minimax, Kling) | 1 | $0.01 |
| [x402 Test Service](https://registry.mcpay.tech/api/service/test/skill.md) | `test` | Test x402 payment flows on Base Sepolia (EVM) and Solana Devnet. Use this service to verify your x402 client integration is working correctly. | 2 | $0.001 |
| [Exa API](https://registry.mcpay.tech/api/service/exa/skill.md) | `exa` | Semantic web search via Exa | 4 | $0.002 - $0.01 |

## Service Endpoints

Each service lives at `https://registry.mcpay.tech/api/service/{slug}` and exposes:

| Endpoint | Description |
|----------|-------------|
| `GET /` | Service info |
| `GET /health` | Health check |
| `GET /docs` | Interactive API docs |
| `GET /openapi.json` | OpenAPI 3.x spec |
| `GET /skill.md` | Agent-friendly documentation |

## Pricing Details

### Twitter API (`twitter`)

Base: `https://registry.mcpay.tech/api/service/twitter` | [Docs](https://registry.mcpay.tech/api/service/twitter/docs) | [OpenAPI](https://registry.mcpay.tech/api/service/twitter/openapi.json) | [Skill](https://registry.mcpay.tech/api/service/twitter/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/user-info` | $0.005 | Get user info by username |
| `POST /api/user-tweets` | $0.01 | Get user's recent tweets |
| `POST /api/user-followers` | $0.01 | Get user's followers |
| `POST /api/user-following` | $0.01 | Get users that user follows |
| `POST /api/search-users` | $0.01 | Search for users by keyword |
| `POST /api/user-mentions` | $0.01 | Get tweets mentioning a user |
| `POST /api/check-follow` | $0.005 | Check if one user follows another |
| `POST /api/batch-users` | $0.02 | Batch get users by IDs |
| `POST /api/tweets-by-ids` | $0.01 | Get tweets by their IDs |
| `POST /api/tweet-replies` | $0.01 | Get replies to a tweet |
| `POST /api/search-tweets` | $0.01 | Advanced tweet search with filters |
| `POST /api/tweet-quotes` | $0.01 | Get quote tweets of a tweet |
| `POST /api/tweet-thread` | $0.01 | Get tweet thread context |
| `POST /api/list-tweets` | $0.01 | Get tweets from a Twitter List |
| `POST /api/trends` | $0.01 | Get trending topics by location |
| `POST /api/invoke` | $0.01 | Search tweets (legacy, use /api/search-tweets) |
| `POST /api/search` | $0.01 | Search tweets (legacy, use /api/search-tweets) |

### AI Generation API (`ai-gen`)

Base: `https://registry.mcpay.tech/api/service/ai-gen` | [Docs](https://registry.mcpay.tech/api/service/ai-gen/docs) | [OpenAPI](https://registry.mcpay.tech/api/service/ai-gen/openapi.json) | [Skill](https://registry.mcpay.tech/api/service/ai-gen/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/invoke` | $0.01 | Run AI model prediction (price varies by model) |

### x402 Test Service (`test`)

Base: `https://registry.mcpay.tech/api/service/test` | [Docs](https://registry.mcpay.tech/api/service/test/docs) | [OpenAPI](https://registry.mcpay.tech/api/service/test/openapi.json) | [Skill](https://registry.mcpay.tech/api/service/test/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/invoke` | $0.001 | Test x402 payment flow (Base Sepolia & Solana Devnet) |
| `POST /api/echo` | $0.001 | Echo data with payment verification |

### Exa API (`exa`)

Base: `https://registry.mcpay.tech/api/service/exa` | [Docs](https://registry.mcpay.tech/api/service/exa/docs) | [OpenAPI](https://registry.mcpay.tech/api/service/exa/openapi.json) | [Skill](https://registry.mcpay.tech/api/service/exa/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/search` | $0.01 | Semantic web search |
| `POST /api/find-similar` | $0.01 | Find similar pages |
| `POST /api/contents` | $0.002 | Extract URL contents |
| `POST /api/answer` | $0.01 | AI-powered answer |

### AI Model Pricing (`ai-gen`)

Price is set dynamically based on the `model` field in the request body.

**Image Models:**

| Model | Price |
|-------|-------|
| `flux/schnell` | $0.004/image |
| `flux/dev` | $0.03/image |
| `flux/pro` | $0.05/image |
| `flux/2-max` | $0.05/image |
| `flux/1.1-pro-ultra` | $0.08/image |
| `flux/kontext-max` | $0.10/image |
| `flux/kontext-pro` | $0.05/image |
| `sdxl/base` | $0.003 |
| `sdxl/lightning` | $0.003 |
| `stability/sd-3.5-medium` | $0.05/image |
| `stability/sd-3.5-large` | $0.08/image |
| `stability/sd-3.5-large-turbo` | $0.05/image |
| `google/imagen-4` | $0.05/image |
| `google/imagen-4-fast` | $0.03/image |
| `google/imagen-4-ultra` | $0.08/image |
| `google/imagen-3` | $0.06/image |
| `google/imagen-3-fast` | $0.03/image |
| `bytedance/seedream-4.5` | $0.05/image |
| `bytedance/seedream-4` | $0.04/image |
| `bytedance/seedream-3` | $0.04/image |
| `ideogram/v3-turbo` | $0.04/image |
| `ideogram/v3-quality` | $0.11/image |
| `ideogram/v3-balanced` | $0.08/image |
| `ideogram/v2a-turbo` | $0.03/image |
| `ideogram/v2a` | $0.05/image |
| `ideogram/v2-turbo` | $0.06/image |
| `ideogram/v2` | $0.10/image |
| `recraft/v3` | $0.05/image |
| `recraft/v3-svg` | $0.10/image |
| `minimax/image-01` | $0.02/image |
| `luma/photon` | $0.04/image |
| `luma/photon-flash` | $0.02/image |
| `tencent/hunyuan-image-3` | $0.10/image |
| `nvidia/sana` | $0.23 |
| `nvidia/sana-sprint` | $0.002 |
| `qwen/qwen-image` | $0.03/image |
| `leonardoai/lucid-origin` | $0.03/image |
| `prunaai/flux-fast` | $0.006/image |

**Video Models:**

| Model | Price |
|-------|-------|
| `minimax/video-01` | $0.60 |
| `minimax/video-01-director` | $0.60 |
| `minimax/video-01-live` | $0.60 |
| `minimax/hailuo-02` | $0.33 |
| `minimax/hailuo-2.3` | $0.34 |
| `minimax/hailuo-2.3-fast` | $0.23 |
| `kling-ai/kling-video` | $0.09/sec |
| `kling-ai/v2.5-turbo-pro` | $0.09/sec |
| `kling-ai/v2.1` | $0.06/sec |
| `kling-ai/v2.1-master` | $0.34/sec |
| `kling-ai/v2.0` | $0.34/sec |
| `kling-ai/v1.6-pro` | $0.12/sec |
| `google/veo-2` | $0.60/sec |
| `google/veo-3` | $0.48/sec |
| `google/veo-3-fast` | $0.18/sec |
| `google/veo-3.1` | $0.48/sec |
| `google/veo-3.1-fast` | $0.18/sec |
| `openai/sora-2` | $0.12/sec |
| `openai/sora-2-pro` | $0.36/sec |
| `bytedance/seedance-1-pro` | $0.08/sec |
| `bytedance/seedance-1-lite` | $0.05/sec |
| `bytedance/seedance-1-pro-fast` | $0.03/sec |
| `pixverse/v5` | $0.10/sec |
| `pixverse/v4.5` | $0.10/sec |
| `luma/ray` | $0.54 |
| `luma/ray-2-720p` | $0.22/sec |
| `luma/ray-2-540p` | $0.12/sec |
| `luma/ray-flash-2-720p` | $0.08/sec |
| `luma/ray-flash-2-540p` | $0.04/sec |
| `wan-video/wan-2.5-t2v` | $0.12/sec |
| `wan-video/wan-2.5-i2v` | $0.12/sec |
| `wan-video/wan-2.5-t2v-fast` | $0.09/sec |
| `wan-video/wan-2.5-i2v-fast` | $0.09/sec |
| `wan-video/wan-2.2-t2v-fast` | $0.12 |
| `wan-video/wan-2.2-i2v-fast` | $0.07 |
| `wavespeedai/wan-2.1-t2v-720p` | $0.29/sec |
| `wavespeedai/wan-2.1-i2v-720p` | $0.30/sec |
| `leonardoai/motion-2.0` | $0.36 |
| `tencent/hunyuan-video` | $1.52 |
| `lightricks/ltx-video` | $0.10 |

## Payment Protocol (x402)

All paid endpoints use the [x402](https://www.x402.org/) payment protocol. No API keys needed.

**Flow:**

1. Call any paid endpoint without a payment header
2. Receive `402 Payment Required` with a `PAYMENT-REQUIRED` header (Base64 JSON with price, network, payTo address)
3. Sign a payment for the requested amount on your chosen network
4. Retry the same request with the `PAYMENT-SIGNATURE` header
5. Receive the response plus a `PAYMENT-RESPONSE` confirmation header

Failed requests are automatically refunded.

**Supported Networks:**

| Network | ID | Type | Environment |
|---------|----|------|-------------|
| Base | `eip155:8453` | EVM | Mainnet |
| Base Sepolia | `eip155:84532` | EVM | Testnet |
| Solana | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana | Mainnet |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | Solana | Devnet |

**Accepted Tokens:** USDC, USDT, CASH (availability varies by network)

## Platform Endpoints (FREE)

| Endpoint | Description |
|----------|-------------|
| `GET https://registry.mcpay.tech/api` | Platform info and version |
| `GET https://registry.mcpay.tech/api/services` | List all services with metadata |
| `GET https://registry.mcpay.tech/api/services/:slug` | Single service details |
| `GET https://registry.mcpay.tech/api/pricing` | All pricing policies |
| `GET https://registry.mcpay.tech/api/networks` | Supported payment networks |
| `GET https://registry.mcpay.tech/api/health` | Health check |
| `GET https://registry.mcpay.tech/api/packages` | Skill/agent package catalog |
| `GET https://registry.mcpay.tech/api/packages/:slug/bundle` | Download package bundle |
| `GET https://registry.mcpay.tech/.well-known/x402` | x402 discovery document |
| `GET https://registry.mcpay.tech/docs` | Interactive docs (HTML) |

## Agent Integration

### With AgentWallet (recommended)

[AgentWallet](https://agentwallet.mcpay.tech/skill.md) is a server-side wallet for AI agents. It manages keys, balances, and x402 payment signing so agents don't need to handle crypto directly.

1. Authenticate with AgentWallet (email OTP → API token)
2. Fund your wallet with USDC on Base or Solana
3. Call any Frames Registry endpoint through AgentWallet's proxy:

```
POST https://agentwallet.mcpay.tech/x402/fetch
{
  "url": "https://registry.mcpay.tech/api/service/twitter/api/search-tweets",
  "method": "POST",
  "body": { "query": "AI agents" }
}
```

AgentWallet detects the 402 response, signs payment, and retries automatically.

### Direct x402 (self-managed wallet)

Requires an EVM or Solana wallet with USDC and the ability to sign EIP-3009 or SPL transfers.

1. Make the request to the paid endpoint
2. Parse the `PAYMENT-REQUIRED` header from the 402 response (Base64 JSON with price, network, payTo)
3. Sign a payment authorization for the exact amount
4. Retry with the `PAYMENT-SIGNATURE` header
