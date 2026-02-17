---
name: pluggy-open-finance
description: Best practices for Open Finance data retrieval and management. Use when working with accounts, transactions, investments, loans, or identity data.
license: MIT
metadata:
  author: pluggy
  version: "1.0.0"
---

# Pluggy Open Finance

Comprehensive guide for retrieving and managing Open Finance data through Pluggy. Contains rules across 5 categories, prioritized by impact.

## When to Apply

Reference these guidelines when:

- Selecting appropriate connectors for financial institutions
- Retrieving account balances and details
- Fetching and processing transactions
- Accessing investment portfolios and holdings
- Retrieving loan information
- Fetching user identity data
- Implementing data synchronization strategies

## Rule Categories by Priority

| Priority | Category           | Impact      | Prefix         |
| -------- | ------------------ | ----------- | -------------- |
| 1        | Connectors         | CRITICAL    | `connector-`   |
| 2        | Sync Strategy      | HIGH        | `sync-`        |
| 3        | Data Retrieval     | HIGH        | `data-`        |
| 4        | Transactions       | HIGH        | `transaction-` |
| 5        | Accounts           | MEDIUM      | `account-`     |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/connector-selection.md
rules/data-pagination.md
rules/transaction-enrichment.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
- Pluggy-specific notes

## Data Products Available

| Product      | Endpoint           | Description                    |
| ------------ | ------------------ | ------------------------------ |
| Accounts     | `/accounts`        | Bank accounts, balances        |
| Transactions | `/transactions`    | Account movements              |
| Investments  | `/investments`     | Portfolios, holdings           |
| Identity     | `/identity`        | User personal data             |
| Loans        | `/loans`           | Loan details, payments         |
| Credit Cards | `/bills`           | Credit card bills              |

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
