---
name: pluggy-integration
description: Core Pluggy integration patterns and best practices. Use when setting up Pluggy SDK, implementing Connect Widget, managing Items, or configuring webhooks.
license: MIT
metadata:
  author: pluggy
  version: "1.0.0"
---

# Pluggy Integration

Comprehensive integration guide for Pluggy Open Finance API. Contains rules across 5 categories, prioritized by impact to guide accurate implementation.

## When to Apply

Reference these guidelines when:

- Setting up Pluggy SDK and authentication
- Implementing the Connect Widget in frontend applications
- Creating, updating, or managing Items (connections)
- Handling MFA (Multi-Factor Authentication) flows
- Configuring webhooks for real-time data sync
- Managing API keys and tokens
- Handling connection errors and edge cases

## Rule Categories by Priority

| Priority | Category               | Impact   | Prefix    |
| -------- | ---------------------- | -------- | --------- |
| 1        | Authentication         | CRITICAL | `auth-`   |
| 2        | Connect Widget         | CRITICAL | `widget-` |
| 3        | Webhook Configuration  | CRITICAL | `webhook-`|
| 4        | Item Lifecycle         | HIGH     | `item-`   |
| 5        | Error Handling         | MEDIUM   | `error-`  |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/auth-api-keys.md
rules/widget-integration.md
rules/item-lifecycle.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
- Pluggy-specific notes

## Key Concepts

### Connection Sync vs Data Sync

| Responsibility | Who Handles | How |
| -------------- | ----------- | --- |
| Connection sync | **Pluggy** | Auto-sync every 24/12/8h |
| Triggering updates | **User** | Only when user explicitly requests |
| Entity data sync | **You** | Fetch all on `item/updated` webhook |
| Transaction sync | **You** | Use `transactions/*` webhook events |

### API Key vs Connect Token

- **API Key**: Backend token (2h expiration) for accessing user data
- **Connect Token**: Frontend token (30min expiration) for Connect Widget only

### Item Lifecycle

1. User opens Connect Widget with Connect Token
2. User selects connector and authenticates
3. Pluggy creates Item and starts data sync
4. Webhook notifies when sync completes
5. Backend retrieves data using API Key
6. Pluggy auto-syncs daily; webhook triggers data refresh

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
