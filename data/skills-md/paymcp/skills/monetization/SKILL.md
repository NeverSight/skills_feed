---
name: monetization
description: Integrate PayMCP into an MCP server to monetize tools (pay-per-request pricing or subscriptions), configure payment providers (traditional and/or X402), choose an appropriate coordination mode, and validate the integration.
license: MIT
metadata:
  vendor: PayMCP
  domain: mcp-monetization
allowed-tools:
  - Read
  - Grep
  - Edit
  - Bash
---

# PayMCP: Monetize MCP Tools

You are an AI coding agent helping a developer add PayMCP monetization to an MCP server (TypeScript or Python).

## When to use this skill

Use this skill when the user asks to:
- add pricing to MCP tools (pay-per-request),
- gate tools behind subscriptions,
- make an MCP server paid or monetized,
- configure PayMCP providers (traditional or X402),
- choose a coordination mode,
- troubleshoot PayMCP integration issues.

## Guardrails (do this first)

1. **Never ship payment credentials to end users.** If the server runs in STDIO mode and would distribute secrets, stop and recommend a hosted deployment.
2. Prefer minimal diffs: integrate PayMCP without rewriting the server architecture.
3. Keep tool interfaces stable.
4. Use the project’s existing MCP framework and conventions.

## High-level integration checklist

### Step 1 — Identify environment
- Detect language: TypeScript/Node or Python.
- Detect MCP server library and how tools are registered.
- Confirm how the server is deployed and how env vars are provided.
- If the official MCP SDK is not installed yet, install it before proceeding.

### Step 2 — Add PayMCP dependency
- Python: ensure `paymcp` is installed and imported.
- TypeScript: ensure `paymcp` is installed and imported.

### Step 3 — Configure providers
Ask which provider(s) to use:
- Walleot (default recommendation if the user has no preference)
- Stripe, PayPal, etc. (if required)
- X402 (on-chain)

Rules:
- You can configure **one provider** or **two providers**.
- If two providers are configured, use **X402 + one traditional provider**.
- If X402 is used, the developer must provide a blockchain address to receive USDC.
- For traditional providers, require at least an API key; provider-specific settings may also be needed.

### Step 4 — Choose coordination mode
- **`mode` is optional.** If omitted, PayMCP defaults to `AUTO`.
- `AUTO` detects client capabilities and selects the best compatible flow.

If the developer insists on another mode, list the available options and warn that deviating from `AUTO` is not recommended unless they understand client capabilities:
- AUTO, RESUBMIT, ELICITATION, TWO_STEP, X402, PROGRESS, DYNAMIC_TOOLS
If the client setup is non-standard, read `references/coordination-modes.md` for compatibility details.

### Step 5 — Add pay-per-request pricing or subscription gating to tools
Support both:
- Pay-per-request (price)
- Subscription gating (subscription / plan id)

Rules:
- Apply pricing only to the tool(s) the user wants to monetize.
- Keep free tools free; do not blanket-charge everything.
- Ensure the tool handler receives the required context/extra parameter as per the framework.
- Pay-per-request does not require user identity; subscription gating does.
- Subscriptions require stable user identity (auth). Without authentication, subscription checks are unreliable.
  - Minimum auth checklist: stable user ID + verifiable token (e.g., JWT/session).
  - Auth guidance: https://modelcontextprotocol.io/docs/tutorials/security/authorization

### Step 6 — Test
- Add one small “test tool” that costs a tiny amount (e.g., $0.50 or $1.00) and verify the payment process.
- Confirm that a paid call succeeds after payment confirmation.
- Confirm that unpaid calls return the correct payment-required behavior.

### Step 7 — Document
- Add short run instructions, required env vars, and the selected provider/mode rationale.

## Concrete implementation playbooks

### Playbook A — TypeScript MCP server (recommended path)
1. Install dependencies:
   - `npm install paymcp` (or your package manager)
   - Ensure `zod` exists if you use it for schemas.
2. Import PayMCP.
```ts
import { installPayMCP } from 'paymcp';
import { WalleotProvider } from 'paymcp/providers';
```
3. Install PayMCP after configuring MCP instance and configure providers with a list.
```ts
installPayMCP(mcp, { providers: [new WalleotProvider({ apiKey: "sk_test_..." })] });
```
4. Optionally set `mode` (default is `AUTO` if omitted).
5. Add tool pricing via tool metadata:
   - `_meta: { price: { amount, currency } }`
6. For subscriptions, add:
   - `_meta: { subscription: { plan: "..." } }`
   - Requires auth; pay-per-request does not.

### Playbook B — Python FastMCP server
1. Install dependencies:
   - `pip install paymcp`
2. Import PayMCP
```python
from paymcp import PayMCP, price #or from paymcp import PayMCP, subscription
from paymcp.providers import WalleotProvider
```
3. Install PayMCP after configuring MCP instance and configure providers with a list.
```python
PayMCP(mcp, providers=[WalleotProvider(apiKey="sk_test_...")])
```
4. Optionally set `mode` (default is `AUTO` if omitted).
5. Apply `@price(amount=..., currency="USD")` to monetized tools.
6. For subscription gating, apply `@subscription(plan="...")`.
   - Requires auth; pay-per-request does not.

### Playbook C — X402 (on-chain)
Only do this when the user controls the MCP client or knows it supports x402-protocol.
- Configure X402 provider with a USDC receive address.
- Use `mode: X402` only when the client is x402-capable.

## References (load on demand)
- `references/paymcp-cheatsheet.md` — minimal code patterns for TS/Python, pricing/subscriptions, Redis state store.
- `references/coordination-modes.md` — how to choose `mode` (AUTO by default).
- `references/providers.md` — provider-specific configuration notes (Walleot/Stripe/PayPal/X402).
- `references/custom-providers.md` — custom provider examples (TypeScript/Python).
- `references/state-store.md` — RedisStateStore and durable state storage.
- `references/troubleshooting.md` — common errors and fixes.

## Output requirements
When making changes, produce:
- a concise summary of what changed,
- the exact files changed,
- how to run/test locally,
- which provider(s) and mode were selected and why,
- any secrets/env vars required (names only; never print real secrets).
