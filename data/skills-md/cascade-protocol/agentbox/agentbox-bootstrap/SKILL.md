---
name: agentbox-bootstrap
description: "AgentBox agent operating instructions and provider configuration. Services, config, x402 payments, skill updates, OpenRouter setup, troubleshooting. Loads automatically on every AgentBox session."
metadata: {"internal": true, "openclaw": {"always": true, "emoji": "🤖"}}
user-invocable: true
---

# AgentBox Operating Instructions

You are running on a dedicated AgentBox agent - a single-tenant cloud instance with OpenClaw gateway, HTTPS, web terminal, and a Solana wallet for x402 micropayments.

## Services

| Service | Port | Managed by |
|---------|------|------------|
| OpenClaw gateway | :18789 (loopback) | `openclaw gateway restart` |
| Caddy (HTTPS reverse proxy) | :443 | `sudo systemctl restart caddy` |
| ttyd (web terminal) | :7681 (loopback) | `sudo systemctl restart ttyd` |

Caddy routes HTTPS traffic to the gateway and terminal. Do NOT modify Caddy or systemd configs directly.

## Key paths

| What | Path |
|------|------|
| OpenClaw config | `~/.openclaw/openclaw.json` |
| Solana wallet | `~/.openclaw/agentbox/wallet-sol.json` |
| EVM wallet | `~/.openclaw/agentbox/wallet-evm.key` |
| Mnemonic (root secret) | `~/.openclaw/agentbox/mnemonic` |
| Workspace | `~/.openclaw/workspace/` |
| Skills (managed) | `~/.openclaw/skills/` |
| x402 plugin | `~/.openclaw/extensions/openclaw-x402/` |
| Gateway logs | `~/.openclaw/logs/` |

## x402 payment plugin

The `openclaw-x402` plugin patches `globalThis.fetch` to handle HTTP 402 Payment Required responses automatically. When an LLM inference call returns 402, the plugin signs a USDC payment on Solana and retries. This is transparent - you don't need to do anything special.

The wallet at `~/.openclaw/agentbox/wallet-sol.json` must have USDC balance for payments to work. Check balance with `/x_wallet` or:
```bash
spl-token balance --owner $(solana address) EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

## Commands and tools

**Slash commands:**
- `/x_wallet` - wallet dashboard with balance, token holdings, recent transactions
- `/x_wallet send <amount|all> <address>` - send USDC to a Solana address
- `/x_wallet history [page]` - paginated transaction history
- `/x_status` - system overview (version, model, pricing, wallet summary)
- `/x_update` - update plugin and skills, restart gateway

**Agent tools:**
- `x_balance` - check wallet SOL and USDC balances
- `x_swap` - swap any Solana token for another (SOL, USDC, meme tokens, any SPL token)
- `x_launch_token` - launch a new token on pump.fun
- `x_token_info` - look up token price, market cap, volume, liquidity
- `x_payment` - call any x402-enabled paid API

Swaps use Jupiter aggregator for best routing, with automatic fallback to PumpPortal for bonding curve tokens. Amount is in input token units, slippage in basis points (default: 250 = 2.5%).

## Default model provider

This instance comes with a preconfigured LLM provider (blockrun) that uses x402 for payments. To use a different provider like OpenRouter, see the OpenRouter Setup section below.

## OpenRouter Setup

To configure OpenRouter as LLM provider (access to Claude, GPT, Gemini, and more via a single API key):

1. **Get an API key**: Sign up at https://openrouter.ai, go to https://openrouter.ai/keys, create a key (starts with `sk-or-`)

2. **Configure OpenClaw**:
```bash
jq --arg key "sk-or-USER_KEY_HERE" \
   --arg model "openrouter/anthropic/claude-sonnet-4-5" \
   '.env.OPENROUTER_API_KEY = $key | .agents.defaults.model.primary = $model' \
   ~/.openclaw/openclaw.json > /tmp/openclaw-update.json \
   && mv /tmp/openclaw-update.json ~/.openclaw/openclaw.json
```

3. **Restart gateway**: `openclaw gateway restart`

**Popular models**: `openrouter/anthropic/claude-sonnet-4-5`, `openrouter/anthropic/claude-opus-4-6`, `openrouter/openai/gpt-4o`, `openrouter/google/gemini-2.5-pro`. Full list at https://openrouter.ai/models.

**Switch model later** (without re-entering API key):
```bash
jq --arg model "openrouter/anthropic/claude-opus-4-6" \
   '.agents.defaults.model.primary = $model' \
   ~/.openclaw/openclaw.json > /tmp/openclaw-update.json \
   && mv /tmp/openclaw-update.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

## Restarting the gateway

After any config change to `~/.openclaw/openclaw.json`:
```bash
openclaw gateway restart
```

Check status:
```bash
openclaw status
```

## Updating skills

To get the latest AgentBox skills:
```bash
npx skills add -g cascade-protocol/agentbox
```

Skills are installed to `~/.openclaw/skills/` (OpenClaw's managed skills path, auto-discovered). Changes take effect on the next new session.

## Troubleshooting

- **Gateway won't start**: Check `openclaw status` and gateway logs at `~/.openclaw/logs/`
- **x402 payments failing**: Check USDC balance (see above). Wallet needs USDC on Solana mainnet.
- **Config changes not taking effect**: Run `openclaw gateway restart` after editing `~/.openclaw/openclaw.json`
- **Skills not showing**: Check `ls ~/.openclaw/skills/`. Run `npx skills add -g cascade-protocol/agentbox` to refresh.
- **"Invalid API key" (OpenRouter)**: Verify the key starts with `sk-or-` and has credit on https://openrouter.ai/credits
- **Model not responding (OpenRouter)**: Check model availability on https://openrouter.ai/models
- **Config broken after edit**: Check JSON syntax with `cat ~/.openclaw/openclaw.json | jq .`

## Important rules

- Always use `openclaw gateway restart` to restart the gateway. Never use systemctl directly for the gateway.
- When editing `~/.openclaw/openclaw.json`, read the current file first, modify it, write it back. Don't write partial configs.
- The wallet keys are at `~/.openclaw/agentbox/` (wallet-sol.json, wallet-evm.key, mnemonic). Never share them or display them to users.
