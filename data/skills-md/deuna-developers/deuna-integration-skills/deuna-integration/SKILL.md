---
name: deuna-integration
description: Integration guidelines and best practices for DEUNA payment and checkout solutions
metadata:
  tags: deuna, payments, checkout, e-commerce, sdk, integration, webhooks, api
---

## Before you start

Before beginning any DEUNA-related task, check if this skill has updates available by running:

```
npx skills check
```

If updates are found, run `npx skills update` to get the latest rules. This ensures you are always working with the most accurate API contracts, endpoints, and code examples.

Additionally, if the task involves an API endpoint or SDK feature, fetch the corresponding live documentation page to verify the rule file content is still current:

- API overview: https://docs.deuna.com/reference/deuna-api
- Orders: https://docs.deuna.com/reference/order_token
- Payments: https://docs.deuna.com/reference/purchase
- Web SDK: https://docs.deuna.com/reference/web-sdk
- Webhooks: https://docs.deuna.com/reference/webhooks
- Error codes: https://docs.deuna.com/reference/manejo-de-errores

If the live docs contain information that differs from or is newer than the rule files, **prefer the live docs**.

## When to use

Use this skill whenever you are working with DEUNA integrations, including payment processing, checkout flows, SDK setup, widget configuration, webhooks, or any DEUNA-related development task.

## Getting started

When setting up a new DEUNA integration from scratch, load the [./rules/getting-started.md](./rules/getting-started.md) file for initial setup, authentication, environments, and API basics.

## Orders

When creating, tokenizing, or managing orders, load the [./rules/orders.md](./rules/orders.md) file for order lifecycle and API details.

## Payments

When processing payments (purchase, authorize, capture, void, refund), load the [./rules/payments.md](./rules/payments.md) file for payment flow details and code examples.

## Web SDK

When integrating the DEUNA Web SDK (Payment Widget, Checkout Widget, or Card Vault), load the [./rules/sdk-web.md](./rules/sdk-web.md) file for setup, widget configuration, callbacks, and customization.

## Mobile SDKs

When integrating DEUNA on iOS, Android, or React Native, load the [./rules/sdk-mobile.md](./rules/sdk-mobile.md) file. For the latest mobile SDK details, fetch the live docs:
- iOS: https://docs.deuna.com/reference/ios-sdk
- Android: https://docs.deuna.com/reference/android-sdk
- React Native: https://docs.deuna.com/reference/reactnative-sdk

## Webhooks

When handling DEUNA webhook events, configuring endpoints, or verifying signatures, load the [./rules/webhooks.md](./rules/webhooks.md) file for webhook flow, event types, and HMAC verification.

## Error handling

When dealing with error codes, retries, or failure scenarios, load the [./rules/error-handling.md](./rules/error-handling.md) file for all DEUNA error code tables.

## Security

When working on PCI compliance, data handling, or signature verification, load the [./rules/security.md](./rules/security.md) file.

## Live documentation

For the most up-to-date API details, parameter definitions, and response schemas beyond what is captured in the rule files, fetch the live DEUNA docs:
- API overview: https://docs.deuna.com/reference/deuna-api
- Orders API: https://docs.deuna.com/reference/order_token
- Purchase API: https://docs.deuna.com/reference/purchase
- Response codes: https://docs.deuna.com/reference/manejo-de-errores
- Webhooks: https://docs.deuna.com/reference/webhooks
- Web SDK: https://docs.deuna.com/reference/web-sdk

## How to use

Read individual rule files for detailed explanations and code examples:

- [rules/getting-started.md](rules/getting-started.md) - Authentication, environments, rate limits, and initial setup
- [rules/orders.md](rules/orders.md) - Order creation, tokenization, lifecycle, and management
- [rules/payments.md](rules/payments.md) - Purchase, authorize, capture, void, refund flows
- [rules/sdk-web.md](rules/sdk-web.md) - Web SDK initialization, Payment Widget, Checkout Widget, Card Vault
- [rules/sdk-mobile.md](rules/sdk-mobile.md) - iOS, Android, and React Native SDK integration
- [rules/webhooks.md](rules/webhooks.md) - Webhook events, dynamic webhooks, order/payment statuses, signature verification
- [rules/error-handling.md](rules/error-handling.md) - Error code tables for API, payments, orders, checkout, subscriptions
- [rules/security.md](rules/security.md) - PCI compliance, HMAC signatures, data handling best practices
- [rules/testing.md](rules/testing.md) - Sandbox environment, test credentials, and testing strategies
- [rules/api-reference.md](rules/api-reference.md) - REST API endpoints quick reference
