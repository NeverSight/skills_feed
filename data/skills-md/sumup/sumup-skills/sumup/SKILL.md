---
name: sumup
description: Guide for building SumUp payment integrations that cover both terminal (card-present) and online (card-not-present) checkout flows using SumUp SDKs and APIs. Use when implementing or debugging SumUp checkout creation, payment processing, reader pairing, Card Widget integrations, Cloud API reader checkouts, or authorization setup with API keys/OAuth and Affiliate Keys.
license: Apache-2.0
---

# SumUp Checkout Integrations

Knowledge and APIs can change. Always prefer the latest SumUp docs in markdown format over stale memory.

- Docs root: `https://developer.sumup.com/`
- LLM entrypoint: `https://developer.sumup.com/llms.txt`
- Markdown page format example: `https://developer.sumup.com/terminal-payments/cloud-api/index.md`

Use this skill to implement end-to-end SumUp checkouts for:

- Terminal payments (native mobile SDKs, Cloud API for Solo, or Payment Switch)
- Online payments (Card Widget and API-orchestrated checkout flow)

## Quick Decision Tree

```text
Need to accept a payment?
├─ In-person (card-present) → terminal
│  ├─ Native mobile app + direct reader flow → terminal/mobile (iOS SDK or Android Reader SDK)
│  ├─ Non-native POS/backend controls Solo reader → terminal/platform-agnostic (Cloud API)
│  └─ Legacy app handoff to SumUp app explicitly required → terminal/legacy-lightweight (Payment Switch)
└─ Online (card-not-present) → online
   ├─ Fastest secure integration, hosted/embedded UI acceptable → online/low-complexity (Card Widget)
   └─ Custom orchestration and async lifecycle handling required → online/custom (Checkouts API + 3DS + webhooks)
```

## Start Here

1. Classify the requested flow:
   - `terminal`: in-person card-present payment
   - `online`: e-commerce/web/app card-not-present payment
   - `hybrid`: both (for example, web checkout + in-store Solo)
2. Pick integration path:
   - `terminal/mobile`: iOS SDK or Android Reader SDK
   - `terminal/platform-agnostic`: Cloud API with Solo readers
   - `terminal/legacy-lightweight`: Payment Switch
   - `online/low-complexity`: Card Widget
   - `online/custom`: Checkouts API + 3DS + webhooks
3. Confirm credentials and environment:
   - API key or OAuth access token
   - Affiliate Key for card-present flows
   - Merchant code and currency alignment
   - Sandbox merchant account for non-production testing
4. Ask for missing critical inputs before implementation:
   - integration channel (mobile SDK, Cloud API, Card Widget, or API-orchestrated)
   - target market/currency and merchant code
   - auth model (API key vs OAuth)
   - webhook endpoint and idempotency strategy
   - existing constraints (legacy compatibility, migration, PCI scope)
5. Apply the implementation pattern from `references/checkout-playbook.md`.
6. Use `references/README.md` and open only the single most relevant entrypoint for the request.

## Non-Negotiable Rules

- Keep secret API keys and OAuth client secrets server-side only.
- Never handle raw PAN/card data directly.
- Create online checkouts server-to-server.
- Prefer Card Widget and SDK-provided checkout experiences to avoid handling raw card details.
- For card-present integrations, include the Affiliate Key and ensure app identifiers match the key setup.
- Avoid Payment Switch unless the user explicitly requests it or has a hard legacy constraint.
- Use unique transaction references (`checkout_reference`, `foreignTransactionId`, or equivalent) to prevent duplicates and improve reconciliation.
- Do not use endpoints marked as deprecated.
- Prefer endpoints that accept `merchant_code` as an explicit parameter when equivalent alternatives exist.
- Treat webhook events as notifications only; verify state through API reads.
- After a widget/client callback reports success, always verify final checkout state on the backend before confirming order/payment success.

## Implementation Workflow

1. Set up auth and merchant context.
2. Create checkout request with unique reference and correct currency.
3. Complete checkout via chosen channel:
   - terminal SDK checkout call
   - Cloud API reader checkout
   - Card Widget
   - direct checkout processing flow
4. Handle async outcomes:
   - SDK callback / activity result / event stream
   - 3DS `next_step` redirect flow
   - webhook delivery + API verification
5. Return normalized result (status, transaction identifiers, retry guidance).

## Required Response Contract

Every solution should state:

1. Chosen integration path and why.
2. End-to-end sequence (server, client, webhook/async verification).
3. Exact endpoint set, confirming no deprecated endpoints and preference for `merchant_code`-accepting endpoints.
4. Failure and retry handling (timeouts, duplicate refs, webhook retries).
5. Test plan for success, deliberate failure, and reconciliation checks.

## Validation Checklist

- Test and capture both successful payment and deliberate failure case (`amount = 11` in test mode).
- Verify behavior for duplicate transaction references.
- Verify timeout/session expiry behavior in the selected checkout path.
- Verify webhook retries and idempotent processing.
- Verify reconciliation fields are stored (checkout id, transaction id/code, merchant code, reference).

## References

- Use `references/README.md` to pick the right reference file.
- Each reference file includes its own canonical markdown docs URL. Prefer that URL over stale memory.
