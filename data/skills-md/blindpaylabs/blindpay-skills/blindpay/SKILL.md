---
name: blindpay
description: Use when integrating with BlindPay for stablecoin-to-fiat payouts, fiat-to-stablecoin payins, receiver KYC management, bank accounts, blockchain wallets, virtual accounts, or offramp wallets.
license: MIT
metadata:
  author: blindpay
  version: "1.0"
  tags: payments, stablecoin, crypto, fiat, payout, payin, usdc, usdt
---

# BlindPay Integration

## Overview

BlindPay is a global payment infrastructure that enables worldwide money transfers using both traditional fiat currencies and stablecoins.

**Key Capabilities:**

| Feature | Description |
|---------|-------------|
| **Payouts** | Convert stablecoins (USDC, USDT) to fiat and send to bank accounts |
| **Payins** | Convert fiat to stablecoins and send to blockchain wallets |
| **Multi-Chain** | Supports Ethereum, Base, Polygon, Arbitrum, Stellar, Solana, Tron |
| **Multi-Currency** | USD, BRL, MXN, ARS, COP and more via ACH, Wire, PIX, SPEI, SWIFT |
| **Virtual Accounts** | Generate dedicated US bank accounts for receivers |
| **Offramp Wallets** | Auto-convert incoming stablecoins to fiat |

**Important:** BlindPay is non-custodial. Funds remain under user control throughout the process. Failed transactions are automatically returned to the originating wallet.

## Quick Start

### Authentication

All API calls require:
- **API Key**: Passed as `Authorization: Bearer YOUR_API_KEY`
- **Instance ID**: Included in the URL path

```bash
curl --request GET \
  --url https://api.blindpay.com/v1/instances/in_000000000000/receivers \
  --header 'Authorization: Bearer YOUR_API_KEY'
```

### Payout Flow (Stablecoin → Fiat)

1. **Accept Terms of Service** → Get `tos_id`
2. **Create Receiver** → KYC verification, get `receiver_id`
3. **Add Bank Account** → Get `bank_account_id`
4. **Create Payout Quote** → Get `quote_id` (valid for 5 minutes)
5. **Approve Tokens** → ERC20 approval for BlindPay contract
6. **Execute Payout** → Stablecoins collected, fiat sent to bank

See [references/getting-started/stable-to-fiat.md](references/getting-started/stable-to-fiat.md) for complete guide.

### Payin Flow (Fiat → Stablecoin)

1. **Accept Terms of Service** → Get `tos_id`
2. **Create Receiver** → KYC verification, get `receiver_id`
3. **Add Blockchain Wallet** → Get `blockchain_wallet_id`
4. **Create Payin Quote** → Get `payin_quote_id` (valid for 5 minutes)
5. **Execute Payin** → Get payment instructions (PIX code, CLABE, etc.)
6. **Send Fiat** → Once received, stablecoins sent to wallet

See [references/getting-started/fiat-to-stable.md](references/getting-started/fiat-to-stable.md) for complete guide.

## Payment Rails

| Type | Country | Speed |
|------|---------|-------|
| ACH | US | ~2 business days |
| Wire | US | ~1 business day |
| RTP | US | Instant |
| PIX | Brazil | Instant |
| SPEI | Mexico | Instant |
| ACH COP | Colombia | ~1 business day |
| Transfers 3.0 | Argentina | Instant |
| International SWIFT | Global | ~5 business days |

## Supported Networks

| Network | Instance Type | Tokens |
|---------|---------------|--------|
| Ethereum | Production | USDC, USDT |
| Base | Production | USDC, USDT |
| Polygon | Production | USDC, USDT |
| Arbitrum | Production | USDC, USDT |
| Stellar | Production | USDC |
| Solana | Production | USDC, USDT |
| Tron (beta) | Production | USDT |
| Sepolia, Base Sepolia, etc. | Development | USDB (test token) |

## Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| KYC | Auto-approved | Manual/automatic review |
| Payouts | Simulated (no real fiat) | Real bank transfers |
| Payins | Auto-completed after 30s | Real fiat deposits required |
| Token | USDB (fake stablecoin) | USDC, USDT |

## Testing Scenarios

| Amount | Result |
|--------|--------|
| Any amount | Success (default) |
| $666.00 | Failed |
| $777.00 | Refunded |

Use first name "Fail" when creating receivers to simulate KYC rejection.

## Error Handling

Always check API responses for errors:

```json
{
  "error": {
    "message": "please_accept_terms_of_service",
    "code": "TERMS_NOT_ACCEPTED"
  }
}
```

Common errors:
- `please_accept_terms_of_service` - Receiver needs to accept updated TOS
- `quote_expired` - Quote older than 5 minutes, create a new one
- `insufficient_balance` - Wallet doesn't have enough tokens
- `kyc_not_approved` - Receiver KYC still pending or rejected

## Reference Documentation

### Getting Started
- [Overview](references/getting-started/overview.md) - What is BlindPay
- [Stable to Fiat](references/getting-started/stable-to-fiat.md) - Payout quick start
- [Fiat to Stable](references/getting-started/fiat-to-stable.md) - Payin quick start

### Essentials
- [Instances](references/essentials/instances.md) - Dev vs production environments
- [Terms of Service](references/essentials/terms-of-service.md) - TOS acceptance flow
- [Receivers](references/essentials/receivers.md) - KYC/KYB for individuals and businesses
- [Bank Accounts](references/essentials/bank-accounts.md) - ACH, Wire, PIX, SPEI, SWIFT
- [Virtual Accounts](references/essentials/virtual-accounts.md) - US bank account generation
- [Blockchain Wallets](references/essentials/blockchain-wallets.md) - External wallet management
- [Offramp Wallets](references/essentials/offramp-wallets.md) - Auto-convert stablecoins
- [Payout Quotes](references/essentials/payout-quotes.md) - Quote creation for payouts
- [Payouts](references/essentials/payouts.md) - Executing stablecoin → fiat transfers
- [Payin Quotes](references/essentials/payin-quotes.md) - Quote creation for payins
- [Payins](references/essentials/payins.md) - Executing fiat → stablecoin transfers
- [API Keys](references/essentials/api-keys.md) - Authentication setup
- [Webhooks](references/essentials/webhooks.md) - Real-time event notifications
- [Partner Fees](references/essentials/partner-fees.md) - Revenue sharing configuration
- [Upload](references/essentials/upload.md) - Secure file uploads for KYC

### Guides
- [Smart Contracts](references/guides/smart-contracts.md) - Contract addresses
- [Cut-off Times](references/guides/cut-off-times.md) - Processing windows
- [Supported Countries](references/guides/supported-countries.md) - Country and payment rail coverage
- [Prohibited Activities](references/guides/prohibited-activities.md) - Compliance requirements
- [Payout Descriptor](references/guides/payout-descriptor.md) - Bank statement display names
- [KYC Best Practices](references/guides/kyc-best-practices.md) - Document submission tips
- [On Hold Transactions](references/guides/on-hold-transactions.md) - Handling flagged transactions
- [SWIFT Deliverability](references/guides/swift-deliverability.md) - International transfer requirements
