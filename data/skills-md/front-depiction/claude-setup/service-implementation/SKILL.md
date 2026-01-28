---
name: service-implementation
description: Implement Effect services as fine-grained capabilities avoiding monolithic designs
---

# Service Implementation Skill

Design and implement Effect services as focused capabilities that compose into complete solutions.

## Anti-Pattern: Monolithic Services

```typescript
import { Context, Effect } from "effect"

// ❌ WRONG - Mixed concerns in one service
export class PaymentService extends Context.Tag("PaymentService")<
  PaymentService,
  {
    readonly processPayment: Effect.Effect<void>
    readonly validateWebhook: Effect.Effect<void>
    readonly refund: Effect.Effect<void>
    readonly sendReceipt: Effect.Effect<void>       // Notification concern
    readonly generateReport: Effect.Effect<void>    // Reporting concern
  }
>() {}
```

## Pattern: Capability-Based Services

Each service represents ONE cohesive capability:

```typescript
import { Context, Effect } from "effect"

declare const Doc: unique symbol
type Doc<T extends string> = { readonly [Doc]: T }

interface HandoffResult {
  readonly status: string
}

interface HandoffError {
  readonly _tag: "HandoffError"
  readonly message: string
}

interface WebhookPayload {
  readonly signature: string
  readonly data: unknown
}

interface WebhookValidationError {
  readonly _tag: "WebhookValidationError"
  readonly message: string
}

interface PaymentId {
  readonly value: string
}

interface Cents {
  readonly value: number
}

interface RefundResult {
  readonly status: string
}

interface RefundError {
  readonly _tag: "RefundError"
  readonly message: string
}

// ✅ CORRECT - Focused capabilities

export class PaymentGateway extends Context.Tag(
  "@services/payment/PaymentGateway"
)<
  PaymentGateway,
  {
    readonly handoff: (
      intent: Doc<"paymentIntents">
    ) => Effect.Effect<HandoffResult, HandoffError, never>
    //                                                 // ▲
    //                                    // No requirements leaked
  }
>() {}

export class PaymentWebhookGateway extends Context.Tag(
  "@services/payment/PaymentWebhookGateway"
)<
  PaymentWebhookGateway,
  {
    readonly validateWebhook: (
      payload: WebhookPayload
    ) => Effect.Effect<void, WebhookValidationError, never>
  }
>() {}

export class PaymentRefundGateway extends Context.Tag(
  "@services/payment/PaymentRefundGateway"
)<
  PaymentRefundGateway,
  {
    readonly refund: (
      paymentId: PaymentId,
      amount: Cents
    ) => Effect.Effect<RefundResult, RefundError, never>
  }
>() {}
```

## Pattern: No Requirement Leakage

Service operations should **never** have requirements:

```typescript
import { Context, Effect } from "effect"

interface QueryResult {
  readonly rows: ReadonlyArray<unknown>
}

interface QueryError {
  readonly _tag: "QueryError"
  readonly message: string
}

// The service interface stays clean
export class Database extends Context.Tag("Database")<
  Database,
  {
    readonly query: (
      sql: string
    ) => Effect.Effect<QueryResult, QueryError, never>
    //                                             // ▲
    //                                  // Requirements = never
  }
>() {}
```

Dependencies are handled during **layer construction**, not in the service interface:

```typescript
import { Context, Effect, Layer } from "effect"

declare const Database: Context.Tag<
  Database,
  {
    readonly query: (sql: string) => Effect.Effect<QueryResult, QueryError, never>
  }
>

declare const Config: Context.Tag<
  Config,
  {
    readonly getConfig: Effect.Effect<{ connection: string }>
  }
>

declare const Logger: Context.Tag<
  Logger,
  {
    readonly log: (message: string) => Effect.Effect<void>
  }
>

interface QueryResult {
  readonly rows: ReadonlyArray<unknown>
}

interface QueryError {
  readonly _tag: "QueryError"
  readonly message: string
}

declare function executeQuery(
  connection: string,
  sql: string
): Effect.Effect<QueryResult, QueryError>

// Dependencies live in the layer
export const DatabaseLive = Layer.effect(
  Database,
  Effect.gen(function* () {
    const config = yield* Config    // Dependency
    const logger = yield* Logger    // Dependency

    return Database.of({
      query: (sql) =>
        Effect.gen(function* () {
          yield* logger.log(`Executing: ${sql}`)
          const { connection } = yield* config.getConfig
          return executeQuery(connection, sql)
        })
    })
  })
)
```

## Pattern: Composing Capabilities

Different implementations support different capabilities:

```typescript
import { Layer } from "effect"

declare const PaymentGateway: {
  of: (impl: { handoff: (intent: any) => any }) => any
}

declare const StripeHandoffLive: Layer.Layer<any>
declare const StripeWebhookLive: Layer.Layer<any>
declare const StripeRefundLive: Layer.Layer<any>

declare function fulfillCashPayment(intent: any): any

// Cash payments: Basic handoff only
export const CashGatewayLive = Layer.succeed(
  PaymentGateway,
  PaymentGateway.of({
    handoff: (intent) => fulfillCashPayment(intent)
  })
)

// Stripe: Full capability suite
export const StripeGatewayLive = Layer.mergeAll(
  StripeHandoffLive,      // Implements PaymentGateway
  StripeWebhookLive,      // Implements PaymentWebhookGateway
  StripeRefundLive        // Implements PaymentRefundGateway
)
```

## Pattern: Optional Capabilities

Use `Effect.serviceOption` for capabilities that may not be available:

```typescript
import { Effect, Option } from "effect"

declare const PaymentGateway: {
  handoff: (intent: any) => Effect.Effect<any>
}

declare const PaymentRefundGateway: {
  refund: (paymentId: any, amount: any) => Effect.Effect<any>
}

interface Order {
  readonly paymentIntent: any
  readonly id: string
}

declare function setupRefundPolicy(
  gateway: typeof PaymentRefundGateway,
  order: Order
): Effect.Effect<void>

const processPayment = (order: Order) =>
  Effect.gen(function* () {
    const handoff = yield* PaymentGateway
    const result = yield* handoff.handoff(order.paymentIntent)

    // Optional capability - check if available
    const refundGateway = yield* Effect.serviceOption(PaymentRefundGateway)

    if (Option.isSome(refundGateway)) {
      yield* setupRefundPolicy(refundGateway.value, order)
    }

    return result
  })
```

## Testing Benefits

Each capability can be tested in isolation:

```typescript
import { Effect, Layer, pipe } from "effect"

declare const PaymentWebhookGateway: {
  of: (impl: {
    validateWebhook: (payload: WebhookPayload) => Effect.Effect<void, WebhookValidationError>
  }) => any
}

interface WebhookPayload {
  readonly signature: string
  readonly data: unknown
}

interface WebhookValidationError {
  readonly _tag: "WebhookValidationError"
  readonly reason: string
}

declare function handleWebhook(payload: WebhookPayload): Effect.Effect<void, WebhookValidationError, any>

declare const payload: WebhookPayload

const TestWebhook = Layer.succeed(
  PaymentWebhookGateway,
  PaymentWebhookGateway.of({
    validateWebhook: (payload) =>
      payload.signature === "valid"
        ? Effect.succeed(undefined)
        : Effect.fail(new WebhookValidationError({ reason: "Invalid" }))
  })
)

// Test only webhook validation, no other payment concerns
const testProgram = handleWebhook(payload).pipe(
  Effect.provide(TestWebhook)
)
```

## Naming Convention

Use descriptive capability names:
- `*Gateway` - External system integration
- `*Repository` - Data persistence
- `*Domain` - Business logic
- `*Service` - General capability (use sparingly)

Tag identifiers should include namespace:
- `"@services/payment/PaymentGateway"`
- `"@repositories/user/UserRepository"`
- `"@domain/order/OrderDomain"`

## Quality Checklist

- [ ] Service represents single capability
- [ ] All operations have Requirements = never
- [ ] Tagged with descriptive namespace
- [ ] Dependencies handled in layer
- [ ] Can be tested in isolation
- [ ] Can be composed with other capabilities
- [ ] JSDoc with purpose and usage

Keep services focused, composable, and free of leaked requirements.
