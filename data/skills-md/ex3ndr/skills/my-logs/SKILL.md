---
name: my-logs
description: Explain how to do logging
---

# Logging Standards

When writing or reviewing logging code, follow these principles.

## Library

- **TypeScript/Node.js**: use `pino`

## Log Format

Show only three fields in the visible line: **time**, **module**, and **message**.

```
HH:mm:ss MODULE_NAME  message text here
```

- **Time**: hours, minutes, seconds only — no milliseconds
- **Module**: fixed-width string (pad shorter names with spaces) so messages align vertically
- **Message**: human-readable text

### Pino Configuration Example

```typescript
import pino from "pino";

const MODULE_WIDTH = 12;

function createLogger(module: string) {
  return pino({
    transport: {
      target: "pino-pretty",
      options: {
        ignore: "pid,hostname",
        translateTime: "HH:MM:ss",
        messageFormat: `${module.padEnd(MODULE_WIDTH)}  {msg}`,
        customColors: getModuleColor(module),
      },
    },
  });
}
```

## Module Colors

Each module gets a deterministic color derived from its name via MurmurHash3. No manual color assignment — the hash picks from a fixed palette automatically. Results are cached so each module hashes only once.

```typescript
// ANSI 256-color palette — 28 visually distinct colors
const COLORS = [
  196, // red
  202, // orange
  208, // dark orange
  214, // orange-gold
  220, // gold
  226, // yellow
  190, // yellow-green
  154, // chartreuse
  118, // bright green
  82,  // green
  48,  // spring green
  50,  // teal
  51,  // cyan
  45,  // turquoise
  39,  // deep sky blue
  33,  // dodger blue
  27,  // blue
  21,  // deep blue
  57,  // blue-violet
  93,  // purple
  129, // medium purple
  165, // magenta
  201, // hot pink
  213, // pink
  177, // violet
  141, // light purple
  105, // slate blue
  69,  // cornflower blue
] as const;

const colorCache = new Map<string, string>();

function murmurhash3(key: string, seed = 0): number {
  let h = seed ^ key.length;
  for (let i = 0; i < key.length; i++) {
    h ^= key.charCodeAt(i);
    h = Math.imul(h ^ (h >>> 16), 0x85ebca6b);
    h = Math.imul(h ^ (h >>> 13), 0xc2b2ae35);
    h ^= h >>> 16;
  }
  return h >>> 0;
}

function getModuleColor(module: string): number {
  let color = colorCache.get(module);
  if (!color) {
    color = `\x1b[38;5;${COLORS[murmurhash3(module) % COLORS.length]}m`;
    colorCache.set(module, color);
  }
  return color;
}
```

## Self-Contained Messages

Every log message must be understandable on its own — assume only the text part is visible (no structured fields are shown). Include all relevant identifiers directly in the message string.

**Good** — all IDs are in the text:

```typescript
log.info(`order:create orderId=${orderId} userId=${userId} items=${items.length}`);
log.error(`payment:charge orderId=${orderId} stripeId=${stripeId} failed amount=${amount}`);
log.info(`user:login userId=${userId} email=${email} method=oauth`);
```

**Bad** — IDs hidden in structured fields that won't appear in the console:

```typescript
log.info({ orderId, userId }, "order created");
log.error({ orderId, stripeId }, "payment failed");
```

## Prefix Notation

Structure messages with **prefix notation**: place the most common/general word on the left, narrowing to the specific action on the right. This groups related messages visually when scanning logs.

```
domain:action  detail
```

**Good** — common prefix groups related lines together:

```
order:create   orderId=abc-123 userId=u-456 items=3
order:pay      orderId=abc-123 amount=59.99 method=card
order:ship     orderId=abc-123 carrier=ups tracking=1Z999
order:cancel   orderId=abc-123 reason=user-request

user:login     userId=u-456 email=j@example.com method=oauth
user:logout    userId=u-456 sessionDuration=3600s
user:update    userId=u-456 field=email

cache:hit      key=user:u-456 ttl=120s
cache:miss     key=product:p-789
cache:evict    key=session:s-012 reason=expired
```

**Bad** — specific word first scatters related entries:

```
createOrder  ...
payOrder     ...
loginUser    ...
shipOrder    ...
```

## Summary

1. Use `pino` for TypeScript
2. Display only `HH:mm:ss`, fixed-width module, and message
3. Assign distinct colors per module
4. Put all IDs in the message text — assume no structured fields are visible
5. Use `domain:action` prefix notation with the general word first
