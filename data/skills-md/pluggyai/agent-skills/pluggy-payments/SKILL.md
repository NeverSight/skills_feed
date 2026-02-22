---
name: pluggy-payments
description: Payment initiation with PIX, Boleto, and Smart Transfers. Use when implementing payment flows, PIX transfers, or preauthorized payments.
license: MIT
metadata:
  author: pluggy
  version: "1.0.0"
---

# Pluggy Payments

Comprehensive guide for implementing payment initiation through Pluggy. Contains rules across 5 categories, prioritized by impact.

## When to Apply

Reference these guidelines when:

- Initiating PIX payments
- Creating and managing Boletos
- Setting up Smart Transfers with preauthorization
- Managing payment intents lifecycle
- Handling scheduled payments (PIX Agendado)
- Implementing PIX Automático

## Rule Categories by Priority

| Priority | Category            | Impact   | Prefix       |
| -------- | ------------------- | -------- | ------------ |
| 1        | PIX Integration     | CRITICAL | `pix-`       |
| 2        | Smart Transfers     | HIGH     | `smart-`     |
| 3        | Payment Lifecycle   | HIGH     | `payment-`   |
| 4        | Boleto Management   | MEDIUM   | `boleto-`    |
| 5        | Scheduled Payments  | MEDIUM   | `schedule-`  |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/pix-initiation.md
rules/smart-preauthorization.md
rules/payment-lifecycle.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
- Pluggy-specific notes

## Payment Flow Overview

```
1. Create Payment Request (with recipient details)
2. Create Payment Intent (for specific Item/account)
3. User authorizes in Connect Widget
4. Monitor payment status via webhook
5. Handle success/failure
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
