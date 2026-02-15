---
name: payments
description: Implement CEP-8 payments in ContextVM using the @contextvm/sdk payments middleware. Use when building paid servers/clients, configuring priced capabilities, integrating payment processors/handlers, or troubleshooting payment notification flows.
---

# ContextVM Payments (CEP-8)

Use this skill when you want ContextVM servers to **charge for specific capabilities** and clients to **pay automatically** using the TypeScript SDK payments layer.

Payments are implemented as **middleware around transports**:

- **Server-side** middleware gates priced requests: it must not forward to the underlying MCP server until payment is verified.
- **Client-side** middleware listens for payment notifications, executes a handler, then continues the original request.

This skill documents *how to use* the SDK payments layer. For transport setup (signers, relays, encryption), see:

- [`../typescript-sdk/SKILL.md`](../typescript-sdk/SKILL.md)
- [`../server-dev/SKILL.md`](../server-dev/SKILL.md)
- [`../client-dev/SKILL.md`](../client-dev/SKILL.md)

## Quick start: charge for one tool (server + client)

### Server: price a capability and attach payments

```ts
import type { PricedCapability } from '@contextvm/sdk/payments';
import {
  LnBolt11NwcPaymentProcessor,
  withServerPayments,
} from '@contextvm/sdk/payments';

const pricedCapabilities: PricedCapability[] = [
  {
    method: 'tools/call',
    name: 'my-tool',
    amount: 10,
    currencyUnit: 'sats',
    description: 'Example paid tool',
  },
];

const processor = new LnBolt11NwcPaymentProcessor({
  nwcConnectionString: process.env.NWC_SERVER_CONNECTION!,
});

const paidTransport = withServerPayments(baseTransport, {
  processors: [processor],
  pricedCapabilities,
});
```

### Client: attach a handler and pay automatically

```ts
import {
  LnBolt11NwcPaymentHandler,
  withClientPayments,
} from '@contextvm/sdk/payments';

const handler = new LnBolt11NwcPaymentHandler({
  nwcConnectionString: process.env.NWC_CLIENT_CONNECTION!,
});

const paidTransport = withClientPayments(baseTransport, {
  handlers: [handler],
});
```

## Core concepts (what to understand once)

### Notifications and correlation

CEP-8 payments are expressed as correlated JSON-RPC notifications:

- `notifications/payment_required`
- `notifications/payment_accepted`
- `notifications/payment_rejected` (CEP-21: reject without charging)

They are correlated to the original request via an `e` tag (request event id). Your app should treat these as **notifications**, not responses.

### PMI (Payment Method Identifier)

Each payment rail is identified by a **PMI** string (example: `bitcoin-lightning-bolt11`).

- Server processors advertise which PMIs they can accept.
- Client handlers advertise which PMIs they can pay.
- A payment only works if there is an intersection.

### Amounts: advertise vs settle

`pricedCapabilities[].amount` + `currencyUnit` are what you *advertise* (discovery). The selected PMI determines how you *settle*.

If you use dynamic pricing via `resolvePrice`, the amount you return must match the unit expected by your chosen processor.

## Server patterns

- Fixed pricing via `pricedCapabilities`
- Dynamic pricing via `resolvePrice`
- Reject without charging (CEP-21) via `resolvePrice → { reject: true, message? }`

Read: [`references/server-setup.md`](references/server-setup.md)

## Client patterns

- Multiple handlers (multiple rails)
- Handling `payment_rejected` outcomes
- PMI advertisement via `pmi` tags (automatic when wrapping with `withClientPayments`)

Read: [`references/client-setup.md`](references/client-setup.md)

## Built-in rails (provided by the SDK)

The SDK currently ships multiple built-in payment rails under the same PMI:

- PMI: `bitcoin-lightning-bolt11`

Rails:

- **Lightning over NWC (NIP-47)**
  - Server: `LnBolt11NwcPaymentProcessor`
  - Client: `LnBolt11NwcPaymentHandler`
  - Read: [`references/lightning-nwc.md`](references/lightning-nwc.md)
- **Lightning via LNbits (REST API)**
  - Server: `LnBolt11LnbitsPaymentProcessor`
  - Client: `LnBolt11LnbitsPaymentHandler`
  - Read: [`references/lightning-lnbits.md`](references/lightning-lnbits.md)

More rails may be added over time (new PMIs and/or additional implementations under existing PMIs). Prefer selecting rails based on PMI compatibility and operational needs.

## Build your own rail (custom PMI)

Implement:

- a server-side `PaymentProcessor` (issue + verify)
- a client-side `PaymentHandler` (pay)

Read: [`references/custom-rails.md`](references/custom-rails.md)

## Troubleshooting pointers

- No `payment_required`: verify request matches `method` + `name` in `pricedCapabilities`.
- Payment succeeds but no `payment_accepted`: verify server relay connectivity and processor verification settings.
- Immediate rejection: handle `notifications/payment_rejected` and surface the optional `message`.

For general relay/encryption/connection issues, see [`../troubleshooting/SKILL.md`](../troubleshooting/SKILL.md).

## Reference index

- [`references/cep-8-overview.md`](references/cep-8-overview.md)
- [`references/server-setup.md`](references/server-setup.md)
- [`references/client-setup.md`](references/client-setup.md)
- [`references/lightning-nwc.md`](references/lightning-nwc.md)
- [`references/lightning-lnbits.md`](references/lightning-lnbits.md)
- [`references/custom-rails.md`](references/custom-rails.md)
