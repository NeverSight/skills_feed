---
name: griffin-monitors
description: Teaches LLM agents how to create effective Griffin API monitors for endpoints in a codebase. Use when the user wants to add or design API monitors, health checks, or scheduled endpoint tests; when evaluating which endpoints to monitor; or when writing monitor definitions in __griffin__ using the Griffin Core DSL.
---

# Griffin API Monitors

This skill teaches you how to create **effective API monitors** with Griffin: scheduled checks that run HTTP requests against endpoints and assert on responses. Monitors are defined in TypeScript using `@griffin-app/griffin` and live in `__griffin__` directories. The goal is to add monitors that **provide value**—catching real failures and reflecting real business behavior—not just "200 OK" checks.

---

## 1. When to use this skill

- User asks to add, create, or design API monitors or health checks.
- User wants to evaluate which endpoints in their codebase should be monitored.
- User is writing or editing monitor files in `__griffin__` and needs correct DSL usage and assertion patterns.
- User mentions Griffin monitors, scheduled API tests, or endpoint monitoring in the context of this project.

---

## 2. Evaluating endpoints: what to monitor

Prioritize **user-facing or critical path** (login, checkout, core reads/writes), **dependencies** other services rely on, and **contract** endpoints (public/partner APIs). Assert on **behavior, not only status**: status plus key body fields, headers, and (when relevant) latency. Match business logic (e.g. list shape `data.items[]` with `id`, `name`). Use high frequency (e.g. 1 min) for critical health/auth, lower (5–15 min) elsewhere.

To design assertions, infer response shape from **route handlers**, **response types / DTOs / OpenAPI**, and error handling. Assert required fields, contract structure (e.g. pagination `items` + `total`), and for latency-sensitive endpoints use `Assert(state["node"].latency).lessThan(ms)`.

---

## 3. Monitor structure (Griffin Core DSL)

Monitors are defined in TypeScript. Use the **sequential builder** for almost all cases: linear flows of request → assert (optional) → request → … .

### Response templating (using prior response data)

**You can use a previous step's response in a later request** by passing a **callback** to `.request()` instead of a static config. The callback receives the same `state` as `.assert()`; use `state["step_name"].body["field"]` or `state["step_name"].headers["name"]` in that step's `path`, `base`, `headers`, or `body`. Only **body** and **headers** from prior responses may be referenced (not status or latency). The DSL serializes these references to `$nodeRef`; the executor resolves them at runtime.

Example: create a resource, then GET it by the ID from the first response:

```typescript
.request("create_order", {
  method: POST,
  path: "/api/v1/orders",
  base: variable("api-service"),
  response_format: Json,
  body: { items: [{ product_id: "ABC", quantity: 1 }] },
})
.assert((state) => [
  Assert(state["create_order"].status).equals(201),
  Assert(state["create_order"].body["order_id"]).isDefined(),
])
.request("get_order", (state) => ({
  method: GET,
  path: `/api/v1/orders/${state["create_order"].body["order_id"]}`,
  base: variable("api-service"),
  response_format: Json,
}))
```

Do not use string placeholders like `"${create_order.body.order_id}"` in path/body—they are not interpolated. Use the callback form and reference the state proxy.


### File location and export

- Create monitor files under a `__griffin__` directory (e.g. `__griffin__/api.ts` or next to the code they test).
- Each file should **export a default**: the result of `createMonitorBuilder(...).build()` (or `createGraphBuilder(...).build()` for rare branching cases).

### Sequential builder pattern

```typescript
import {
  GET,
  POST,
  createMonitorBuilder,
  Json,
  Frequency,
  Assert,
  variable,
  WaitDuration,
} from "@griffin-app/griffin";

const monitor = createMonitorBuilder({
  name: "monitor-name",           // Unique, descriptive (e.g. "auth-login-check")
  frequency: Frequency.every(5).minute(),
  locations: ["us-east-1", "eu-west-1"],  // Optional: where the monitor runs
})
  .request("step_name", {
    method: GET,
    path: "/path",
    base: variable("api-service"),  // Base URL from environment
    response_format: Json,
    // Optional: headers, body
  })
  .assert((state) => [
    Assert(state["step_name"].status).equals(200),
    Assert(state["step_name"].body["field"]).not.isNull(),
  ])
  .wait("pause", WaitDuration.seconds(2))   // Optional
  .request("next_step", { ... })
  .assert((state) => [ ... ])
  .build();

export default monitor;
```

- **name**: Short, unique, descriptive (e.g. `health-check`, `orders-create-and-fetch`).
- **frequency**: `Frequency.every(n).minute()`, `.minutes()`, `.hour()`, `.hours()`, `.day()`, `.days()`.
- **locations** (optional): Array of location identifiers where the monitor runs (e.g. `["us-east-1", "eu-west-1"]`).
- **request(id, config)**: `method` (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, etc.), `path`, `base`, `response_format`, optional `headers`, `body`. `config` may be a static object or a callback `(state) => config`. `path` and `base` may use `variable("key")`, `template` (see [String templates](#string-templates)), or state refs in a callback. Both `headers` and `body` may contain `secret("...")` references.
- **response_format**: `Json`, `Xml`, or `NoContent`. Use `NoContent` (import from `@griffin-app/griffin-core`) for endpoints that return **204 with no body**; assert only on `state["node"].status` (e.g. `.equals(204)`). Do not assert on body for NO_CONTENT.
- **assert(callback)**: Callback receives `state`; use `state["step_name"]` to refer to a prior request. Return an array of `Assert(...)` results. **When an assertion fails, the monitor run fails and no later steps execute.**
- **wait(id, duration)**: `WaitDuration.seconds(n)`, `WaitDuration.minutes(n)`, or a number (milliseconds, e.g. `2000`).

### Base URL and variables

- **Base URL**: Use `variable("key")` for the base URL (e.g. `variable("api-service")`). The key is resolved per environment when the monitor is run.
- **Combining multiple refs**: Use the **`template`** tagged template literal (see [String templates](#string-templates)), e.g. `` path: template`/api/${variable("api-version")}/health` ``. The two-argument `variable("key", "template")` form has been **removed**; use `template` for any string that combines variables, secrets, or state refs.

### String templates

Use the **`template`** tagged template literal when `path` or `base` (or any string field that accepts refs) must combine multiple variables, secrets, or node refs. Import `template` from `@griffin-app/griffin`. Each interpolation must be a `variable("key")`, `secret("REF")`, or a state proxy reference (e.g. `state["node"].body["id"]`). Example: `` path: template`/api/${variable("api-version")}/health` ``, `` base: template`https://${variable("env")}.api.example.com` ``. Only variable(), secret(), and state refs are allowed inside template; plain strings or numbers throw at build time.

### Secrets

- Use `secret("REF")` in `headers` or `body` (e.g. `headers: { "Authorization": secret("API_TOKEN") }`, or `body: { apiKey: secret("API_KEY") }`). Use `template` in `path`/`base` when you need to mix secrets with variables or state refs. Optional: `secret("REF", { field: "key" })` for a field from a JSON secret; `secret("REF", { version: "x" })` to pin a version when the provider supports it.
- **Secret refs must match** `^[A-Za-z_][A-Za-z0-9_]*$`: start with a letter or underscore, then only letters, numbers, and underscores. Use `API_TOKEN` or `my_api_key`, not `my-api-key` (hyphens are invalid).

---

## 4. Assertions

Assertions run after the corresponding request(s). Use the **state** object keyed by request id: `state["step_name"]` gives you `.body`, `.headers`, `.status`, `.latency`.

### Accessors

| What to assert on | Usage |
|-------------------|--------|
| HTTP status       | `state["id"].status` |
| Response body     | `state["id"].body["a"]["b"]` (nested keys; use `.at(0)` for first array element) |
| Response headers  | `state["id"].headers["content-type"]` |
| Latency (ms)      | `state["id"].latency` |

**Status and latency** support only **binary** predicates (e.g. `.equals(200)`, `.lessThan(500)`). Do not use unary predicates (`.isNull()`, `.isDefined()`, `.isEmpty()`) on `status` or `latency`—they will throw at build time. For body and headers, both unary and binary predicates are supported.

### Common predicates

- **Equality**: `Assert(x).equals(value)`, `Assert(x).not.equals(value)`
- **Null/defined** (body, headers only): `Assert(x).not.isNull()`, `Assert(x).isDefined()`, `Assert(x).isEmpty()` / `.not.isEmpty()`
- **Booleans** (body, headers): `Assert(x).isTrue()`, `Assert(x).isFalse()`
- **Numbers**: `Assert(x).lessThan(n)`, `Assert(x).lessThanOrEqual(n)`, `Assert(x).greaterThan(n)`, `Assert(x).greaterThanOrEqual(n)`
- **Strings**: `Assert(x).contains(sub)`, `Assert(x).startsWith(prefix)`, `Assert(x).endsWith(suffix)`

Use `.not` before the predicate to negate (e.g. `Assert(x).not.equals(500)`).

### Examples

```typescript
// Status and key body fields
Assert(state["create_user"].status).equals(201),
Assert(state["create_user"].body["data"]["id"]).not.isNull(),
Assert(state["create_user"].body["data"]["email"]).equals("test@example.com"),

// Header and latency
Assert(state["health"].headers["content-type"]).contains("application/json"),
Assert(state["api"].latency).lessThan(500),

// Array and nested
Assert(state["list"].body["items"]).not.isEmpty(),
Assert(state["list"].body["items"].at(0)["id"]).isDefined(),
```

See [reference.md](reference.md) for the full assertion list.

---

## 5. Multi-step flows and value

- **Create-then-read**: POST to create a resource, then GET by id or path. Use the **callback form** of `.request()` for the second step and reference the first response, e.g. `` path: `/api/v1/orders/${state["create_order"].body["order_id"]}` `` or `body: { order_id: state["create_order"].body["order_id"] }`. Use a short `.wait()` between steps if the system needs a moment to be consistent.
- **Auth then protected**: One request can obtain a token (or use `secret("...")` in headers), the next calls the protected endpoint; assert on both.
- **Order of steps**: Requests run in sequence.

Keep each monitor focused on one flow. Split "login" and "checkout" into separate monitors if they are separate concerns.

---

## 6. Optional: notifications

Use the **`notify`** builder from `@griffin-app/griffin` to add alerts. Pass a `notifications` array into `createMonitorBuilder({ ... })`. Each entry is built by choosing a trigger, optionally `.withCooldown(minutes)`, then a routing method. Omit `notifications` if the user does not need alerts.

### Triggers

- `notify.onFailure()` — any run failure
- `notify.onRecovery()` — run succeeds after a previous failure
- `notify.onConsecutiveFailures(threshold)` — e.g. 3 failures in a row
- `notify.onSuccessRateBelow(threshold, window_minutes)` — e.g. below 95% over 30 minutes
- `notify.onLatencyAbove({ threshold_ms, percentile, window_minutes })` — e.g. `{ threshold_ms: 2000, percentile: "p95", window_minutes: 10 }` (percentile: `"p50"` | `"p95"` | `"p99"`)

### Routing (chain after trigger, or after `.withCooldown(n)`)

- `.toSlack(channel, integration?)` — e.g. `.toSlack("#alerts")`
- `.toEmail(toAddresses, integration?)` — e.g. `.toEmail(["team@example.com"])`
- `.toWebhook(integration)` — integration name required

### Example

```typescript
import { createMonitorBuilder, GET, Json, Frequency, Assert, variable, notify } from "@griffin-app/griffin";

const monitor = createMonitorBuilder({
  name: "health-check",
  frequency: Frequency.every(5).minute(),
  notifications: [
    notify.onFailure().toSlack("#alerts"),
    notify.onConsecutiveFailures(3).withCooldown(15).toEmail(["oncall@example.com"]),
    notify.onRecovery().toSlack("#alerts"),
  ],
})
  .request("health", { method: GET, path: "/health", base: variable("api-service"), response_format: Json })
  .assert((state) => [Assert(state["health"].status).equals(200)])
  .build();

export default monitor;
```

---

## 7. Checklist before finishing

- [ ] Monitor has a clear, unique `name` and sensible `frequency` (and optional `locations` if needed).
- [ ] Base URL uses `variable("...")`; no hardcoded production URLs.
- [ ] Secret refs use valid names (letters, numbers, underscores only; start with letter or underscore).
- [ ] Assertions cover status and at least one meaningful aspect (body field, header, or latency). Status/latency use only binary predicates (e.g. `.equals()`, `.lessThan()`).
- [ ] Assertions match the endpoint’s documented or implemented behavior.
- [ ] File lives under `__griffin__` and exports the monitor as `default`. If alerts are needed, use the `notify` builder in `notifications`.

---

## Summary

1. **Evaluate** which endpoints are critical or user-facing and deserve a monitor.
2. **Understand** the endpoint’s behavior and response shape from handlers, types, or specs.
3. **Design** assertions that verify status, key body/headers, and (if relevant) latency.
4. **Implement** with `createMonitorBuilder`, `.request()`, `.assert()`, optional `.wait()`, using `variable()` and `secret()` where needed; use `notify` for alerts.
5. **Keep** each monitor focused and valuable, not just "200 OK."
