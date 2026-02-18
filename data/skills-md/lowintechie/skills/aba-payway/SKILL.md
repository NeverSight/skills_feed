---
name: aba-payway
description: ABA PayWay checkout integration and troubleshooting across modern web stacks including Next.js, React, Vue, Nuxt, and similar frameworks. Use when implementing or debugging purchase payload signing, checkout form fields, callback handling, sandbox or production config, or client modal integration. Prefer Next.js patterns first in this version, then adapt to other frameworks.
---

# ABA PayWay

Implement and troubleshoot ABA PayWay checkout flows across frameworks, using Next.js as the primary profile in this version.

## Quick Workflow

1. Confirm server configuration and runtime.
2. Build or verify purchase payload fields in the exact PayWay hash order.
3. Sign payload server-side only.
4. Open checkout from the hidden form after script readiness.
5. Verify callback parsing and logging behavior.

## Framework Profiles (Next.js First)

1. Next.js (primary profile): implement signing and callback routes with App Router route handlers.
2. React SPA / Vue SPA: implement a separate backend endpoint for signing and callback handling, then call it from the client.
3. Nuxt: implement signing and callback handlers with Nuxt server routes.
4. Any framework: keep identical unsigned fields, field order, and hash algorithm.

## Implement Server Checkout Endpoint

1. Keep checkout signing in a server endpoint running in a Node-compatible runtime.
2. Validate `amount` early and return `400` for invalid input.
3. Resolve required env vars: `ABA_PAYWAY_API_KEY`, `ABA_PAYWAY_MERCHANT_ID`, `ABA_PAYWAY_API_URL`.
4. Build unsigned fields using normalized values from user payload.
5. Build hash input in canonical field order and sign with `HMAC-SHA512` plus base64.
6. Return `{ apiUrl, formFields }` to the client for hidden-form submission.

Use canonical field order from `.agents/skills/aba-payway/references/integration.md`.

## Implement Client Checkout UI

1. Load jQuery before the PayWay checkout script.
2. Ensure only one checkout form instance exists on the page (fixed PayWay ids).
3. POST checkout data to your server checkout endpoint (for example, `/api/payway/checkout`).
4. Fill hidden input fields from `formFields`.
5. Call `AbaPayway.checkout()` only after script readiness.
6. Surface user-facing errors when script load or payload prep fails.

## Implement Callback Endpoint

1. Accept both `application/json` and `application/x-www-form-urlencoded` payloads.
2. Support both `POST` and `GET` callback shapes.
3. Keep logging guarded by `PAYWAY_DEBUG_LOG` so production logs stay clean.
4. Replace temporary `{ ok: true }` response with domain-specific reconciliation once available.

## Debugging

Use the hash debugger when signatures mismatch:

```bash
node .agents/skills/aba-payway/scripts/payway-purchase-hash-debug.js \
  --payload /absolute/path/to/purchase-fields.json
```

The script prints `hashInput` and `hash` so you can compare with server route output.

## References

- Integration details and field map: `.agents/skills/aba-payway/references/integration.md`
- Framework adaptation notes: `.agents/skills/aba-payway/references/framework-profiles.md`
- Next.js checkout route example: `src/app/api/payway/checkout/route.ts`
- Next.js callback route example: `src/app/api/payway/callback/route.ts`
- Next.js client component example: `src/components/payway/payway.tsx`
