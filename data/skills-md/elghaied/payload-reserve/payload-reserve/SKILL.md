---
name: payload-reserve
description: >
  Integration guide for the payload-reserve plugin — a reservation and booking system for Payload CMS 3.x.
  Use when a user is installing, configuring, or extending the plugin in their Payload project.
  Covers all plugin options, collection schemas, the configurable status machine, the public REST API,
  plugin hook callbacks (email, Stripe, etc.), duration types, multi-resource bookings, capacity modes,
  and real-world examples (salon, hotel, restaurant, event venue, multi-tenant, Stripe payment gate).
  Triggers on: "payload-reserve", "payloadReserve", "reservation plugin", "booking plugin",
  "how do I add reservations to Payload", "booking system payload", "availability endpoint".
---

# payload-reserve

A full-featured reservation/booking plugin for Payload CMS 3.x. Adds scheduling with conflict
detection, a configurable status machine, multi-resource bookings, capacity tracking, 5 public
REST endpoints, and admin UI components (calendar view, dashboard widget, availability grid).

## Install

```bash
pnpm add payload-reserve
# or
npm install payload-reserve
```

Peer dependency: `payload ^3.37.0`

## Quick Start

```typescript
import { buildConfig } from 'payload'
import { payloadReserve } from 'payload-reserve'

export default buildConfig({
  collections: [/* your collections */],
  plugins: [
    payloadReserve(), // zero-config — all defaults apply
  ],
})
```

## What Gets Created (defaults)

**5 collections:** `services`, `resources`, `schedules`, `customers` (auth), `reservations`

**3 admin components:** Calendar view (replaces reservations list), Dashboard widget (today's stats), Availability overview at `/admin/reservation-availability`

**5 REST endpoints:** `GET /api/reserve/availability`, `GET /api/reserve/slots`, `POST /api/reserve/book`, `POST /api/reserve/cancel`, `GET /api/reserve/customers`

**Default status flow:** `pending` -> `confirmed` -> `completed | cancelled | no-show`

## Extend Your Own Users Collection

```typescript
payloadReserve({
  userCollection: 'users', // injects phone, notes, bookings join into your existing collection
})
```

## Common Config Options

```typescript
payloadReserve({
  adminGroup: 'Reservations',       // admin panel group label
  defaultBufferTime: 0,             // buffer minutes between bookings
  cancellationNoticePeriod: 24,     // minimum hours notice to cancel
  userCollection: 'users',          // extend existing auth collection
  disabled: false,                  // set true to disable plugin
})
```

## Key Patterns

- **Escape hatch** — bypass all validation hooks: `context: { skipReservationHooks: true }` on any `payload.create/update` call
- **Status machine** — fully configurable; `blockingStatuses` control conflict detection, `terminalStatuses` lock records
- **Idempotency** — pass `idempotencyKey` on POST /api/reserve/book to prevent duplicate submissions
- **endTime** — always auto-calculated from `startTime + service.duration`; do not set manually for `fixed` services

## Reference Files

Load the relevant file when the user's question is about that topic:

| Topic | File |
|-------|------|
| All plugin options, slugs, access, full config example | `references/configuration.md` |
| Collection schemas (fields, types, examples) | `references/collections.md` |
| Status machine config, custom statuses, transitions | `references/status-machine.md` |
| Duration types, multi-resource bookings, capacity modes | `references/booking-features.md` |
| Plugin hook callbacks (afterBookingCreate, afterStatusChange, etc.) | `references/hooks-api.md` |
| REST API endpoints (params, responses, fetch examples) | `references/rest-api.md` |
| Real-world examples: salon, hotel, restaurant, Stripe, email, multi-tenant | `references/examples.md` |
