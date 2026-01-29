---
name: payments
description: |
  Unified payment infrastructure audit and management. Orchestrates Stripe,
  Bitcoin, and Lightning checks. Use when: comprehensive payment review,
  multi-provider audit, or unified payment status.
  Keywords: payments, billing, stripe, bitcoin, lightning, multi-provider.
---

# /payments

Unified payment lifecycle. Audit, fix, verify—all providers, one skill.

## What This Does

Orchestrates all payment providers. Detects active systems, runs provider-specific skills, merges findings, drives fixes in priority order, verifies end-to-end payment flows.

## Branching

Before making code changes:

```bash
git checkout -b fix/payments-$(date +%Y%m%d)
```

Configuration-only changes (env vars, dashboard settings) don't require a branch.

## Process

### 1. Detect Active Providers

```bash
# Stripe
grep -q "stripe" package.json 2>/dev/null && echo "✓ Stripe SDK" || echo "○ No Stripe"
[ -n "$STRIPE_SECRET_KEY" ] && echo "✓ STRIPE_SECRET_KEY" || echo "○ No STRIPE_SECRET_KEY"

# Bitcoin
command -v bitcoin-cli >/dev/null && echo "✓ bitcoin-cli" || echo "○ No bitcoin-cli"
[ -n "$BITCOIN_RPC_URL" ] && echo "✓ BITCOIN_RPC_URL" || echo "○ No BITCOIN_RPC_URL"

# Lightning
command -v lncli >/dev/null && echo "✓ lncli (LND)" || echo "○ No lncli"
command -v lightning-cli >/dev/null && echo "✓ lightning-cli (CLN)" || echo "○ No lightning-cli"
[ -n "$LND_DIR" ] && echo "✓ LND_DIR" || echo "○ No LND_DIR"

# BTCPay
[ -n "$BTCPAY_URL" ] && echo "✓ BTCPAY_URL" || echo "○ No BTCPAY_URL"
[ -n "$BTCPAY_API_KEY" ] && echo "✓ BTCPAY_API_KEY" || echo "○ No BTCPAY_API_KEY"
```

### 2. Run Provider Lifecycles

For each detected provider, invoke the full lifecycle skill:

| Provider | Skill | Fallback |
|----------|-------|----------|
| Stripe | `/stripe` | `/check-stripe` if quick audit |
| Bitcoin | `/bitcoin` | `/check-bitcoin` if quick audit |
| Lightning | `/lightning` | `/check-lightning` if quick audit |
| BTCPay | `/check-btcpay` | N/A (audit only) |

Each skill produces prioritized findings (P0-P3).

### 3. Consolidate Findings

Merge all provider findings into unified report:

```markdown
## Unified Payment Audit

### P0: Critical (Cross-Provider)
- [Stripe] Webhook signature not verified
- [Bitcoin] Node unreachable
- [Lightning] No inbound liquidity

### P1: Essential
- [Stripe] No customer portal
- [Lightning] Watchtower not configured
- [BTCPay] Webhook URL uses HTTP

### P2: Important
- [Bitcoin] UTXO consolidation needed
- [Lightning] Low outbound liquidity
- [Stripe] Missing idempotency keys

### P3: Nice to Have
- [All] Add unified payment analytics
```

### 4. Execute Fixes

Fix in priority order across all providers:

1. **P0 first** — Any provider's P0 blocks payment acceptance
2. **Dependency chains** — Lightning depends on Bitcoin node; fix Bitcoin first
3. **Cross-provider issues** — Unified invoice tracking, reconciliation

Delegate code fixes to Codex:
```bash
codex exec --full-auto "Fix [issue]. Provider: [stripe|bitcoin|lightning]. \
File: [path]. Follow pattern in [ref]. Verify: pnpm typecheck" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

### 5. Verify All Flows

Test each provider end-to-end:

**Stripe:**
```bash
# Create test checkout, complete with 4242...4242, verify webhook
stripe trigger checkout.session.completed
```

**Bitcoin:**
```bash
# Generate address, send testnet coins, verify confirmation tracking
bitcoin-cli -testnet getnewaddress
```

**Lightning:**
```bash
# Create invoice, pay from another node, verify settlement
lncli --network=testnet addinvoice --amt=1000 --memo="Test"
```

Don't declare done until all active providers pass verification.

## Output Format

```markdown
## Payment Infrastructure Status

### Active Providers
- Stripe: Configured
- Bitcoin: Configured (testnet)
- Lightning: Configured (LND)
- BTCPay: Not detected

### Findings Summary
| Provider | P0 | P1 | P2 | P3 |
|----------|----|----|----|----|
| Stripe | 1 | 2 | 3 | 1 |
| Bitcoin | 0 | 1 | 2 | 2 |
| Lightning | 1 | 2 | 1 | 3 |
| **Total** | **2** | **5** | **6** | **6** |

### Fix Order
1. [P0] Stripe webhook verification
2. [P0] Lightning inbound liquidity
3. [P1] Bitcoin fee estimation
...

### Verification Status
- Stripe: PASSED
- Bitcoin: PASSED
- Lightning: PENDING (waiting for channel open)

### Next Steps
Run `/fix-stripe` to address Stripe P0.
```

## What You Get

When complete:
- All payment providers audited
- Unified findings prioritized
- Fixes implemented across providers
- End-to-end verification per provider
- Clear status and next steps

User can:
- Accept payments via any configured provider
- See unified payment health status
- Run provider-specific skills for deeper work

## Related

- `/stripe` - Stripe lifecycle
- `/bitcoin` - Bitcoin lifecycle
- `/lightning` - Lightning lifecycle
- `/check-payments` - Multi-provider audit (no fixes)
- `/groom` - Full backlog grooming
