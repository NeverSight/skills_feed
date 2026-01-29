---
name: check-bitcoin
description: |
  Audit Bitcoin payment integration. Checks node connectivity, wallet health,
  address management, UTXO hygiene, and network configuration. Use when:
  reviewing Bitcoin setup, diagnosing payment issues, or pre-launch audit.
  Keywords: bitcoin, btc, on-chain, wallet, utxo, node.
---

# /check-bitcoin

Audit Bitcoin integration. Output findings as structured report.

## What This Does

1. Check node connectivity and sync status
2. Audit wallet health and key security
3. Verify address derivation (BIP84)
4. Validate network config (testnet vs mainnet)
5. Check fee estimation settings
6. Review UTXO consolidation status
7. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-production-issues` to create issues or `/check-production` for infra review.

## Process

### 1. Node Connectivity Check

```bash
# bitcoin-cli installed?
command -v bitcoin-cli >/dev/null && echo "✓ bitcoin-cli" || echo "✗ bitcoin-cli missing"

# Node reachable?
bitcoin-cli getblockchaininfo 2>/dev/null | head -20 || echo "✗ Node not reachable"

# Sync status
bitcoin-cli getblockchaininfo 2>/dev/null | grep -E "blocks|headers|verificationprogress|initialblockdownload"
```

### 2. Wallet Health

```bash
# Wallet loaded?
bitcoin-cli listwallets 2>/dev/null || echo "✗ No wallets loaded"

# Wallet info
bitcoin-cli getwalletinfo 2>/dev/null | grep -E "balance|unconfirmed_balance|immature_balance|txcount|private_keys_enabled|keypoolsize"
```

### 3. Address Derivation

```bash
# BIP84 descriptors present?
bitcoin-cli listdescriptors 2>/dev/null | grep -E "wpkh|84h" | head -5

# Address info sanity (replace with a sample address if known)
bitcoin-cli getaddressinfo "<btc_address>" 2>/dev/null | grep -E "ismine|iswatchonly|solvable|desc|hdkeypath"
```

### 4. Network Config

```bash
# Chain: main/test/regtest?
bitcoin-cli getblockchaininfo 2>/dev/null | grep -E "\"chain\"|\"pruned\""

# Ensure separation of configs
ls -1 ~/.bitcoin 2>/dev/null | grep -E "bitcoin.conf|testnet3|regtest" || true
```

### 5. Fee Estimation Settings

```bash
# Fee estimates for ~6 blocks
bitcoin-cli estimatesmartfee 6 2>/dev/null || echo "✗ Fee estimator unavailable"

# Mempool info
bitcoin-cli getmempoolinfo 2>/dev/null | grep -E "mempoolminfee|minrelaytxfee"
```

### 6. UTXO Consolidation Status

```bash
# Count UTXOs (rough)
bitcoin-cli listunspent 2>/dev/null | grep -c "\"txid\"" || echo "✗ listunspent failed"

# Small UTXO warning sample (replace threshold as needed)
bitcoin-cli listunspent 2>/dev/null | grep -E "\"amount\"" | head -20
```

### 7. Deep Audit

Spawn `bitcoin-auditor` agent for comprehensive review:
- Wallet descriptor correctness (BIP84)
- Address reuse risk
- Fee policy and fallback behavior
- UTXO set health and dust exposure
- Node security and RPC exposure

## Output Format

```markdown
## Bitcoin Audit

### P0: Critical (Payment Failures)
- Node unreachable - `bitcoin-cli getblockchaininfo` fails
- Wallet not loaded - cannot receive or spend
- Mainnet/testnet mismatch between node and app

### P1: Essential (Must Fix)
- Private keys disabled on hot wallet (unexpected)
- No BIP84 descriptors found for receive addresses
- Fee estimator unavailable - risk of stuck txs

### P2: Important (Should Fix)
- Excess small UTXOs - consolidation needed
- Address reuse detected in deposit flow
- Keypool low - risk of address gap
- Mempool min fee not handled in fee logic

### P3: Nice to Have
- Add scheduled UTXO consolidation
- Add fee bumping (RBF/CPFP) automation
- Add monitoring for node sync drift

## Current Status
- Node: Reachable, synced
- Wallet: Loaded, private keys enabled
- Derivation: BIP84 present
- Fees: Estimator healthy
- UTXO hygiene: Needs attention
- Network separation: Enforced

## Summary
- P0: 1 | P1: 3 | P2: 4 | P3: 3
- Recommendation: Fix node connectivity and fee estimation gaps
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Node unreachable | P0 |
| Wallet not loaded | P0 |
| Network mismatch | P0 |
| Private keys disabled unexpectedly | P1 |
| Missing BIP84 descriptors | P1 |
| Fee estimator unavailable | P1 |
| Excess small UTXOs | P2 |
| Address reuse risk | P2 |
| Low keypool | P2 |
| Fee floor not handled | P2 |
| Automation/monitoring | P3 |

## Related

- `/log-bitcoin-issues` - Create GitHub issues from findings
- `/fix-bitcoin` - Fix Bitcoin issues
- `/bitcoin` - Full Bitcoin lifecycle management
- `/check-lightning` - Lightning setup review
- `/check-btcpay` - BTCPay Server audit
- `/check-payments` - Multi-provider payment audit
