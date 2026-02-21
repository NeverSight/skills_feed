---
name: client-dev
description: Build MCP clients that connect to ContextVM servers over Nostr. Use when creating clients, discovering servers, connecting to remote servers, handling encrypted connections, or implementing the proxy pattern for existing MCP clients.
---

# ContextVM Client Development

Build MCP clients that connect to ContextVM servers over the Nostr network.

## Quick Start

Connect to a ContextVM server:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client";
import {
  NostrClientTransport,
  PrivateKeySigner,
  ApplesauceRelayPool,
  EncryptionMode,
} from "@contextvm/sdk";

const signer = new PrivateKeySigner(process.env.CLIENT_PRIVATE_KEY!);
const relayPool = new ApplesauceRelayPool([
  "wss://relay.contextvm.org",
  "wss://cvm.otherstuff.ai",
]);

const SERVER_PUBKEY = "server-public-key-hex";

const transport = new NostrClientTransport({
  signer,
  relayHandler: relayPool,
  serverPubkey: SERVER_PUBKEY,
  encryptionMode: EncryptionMode.OPTIONAL,
});

const client = new Client({
  name: "my-client",
  version: "1.0.0",
});

await client.connect(transport);

// Use the client
const tools = await client.listTools();
const result = await client.callTool({
  name: "echo",
  arguments: { message: "Hello" },
});
```

## Server Discovery

### Direct Connection (Known Pubkey)

Connect when you know the server's public key:

```typescript
const transport = new NostrClientTransport({
  signer,
  relayHandler: relayPool,
  serverPubkey: "known-server-pubkey",
});
```

### Discovery via Announcements

Find servers broadcasting on the network:

```typescript
import { CTXVM_MESSAGES_KIND, SERVER_ANNOUNCEMENT_KIND } from "@contextvm/sdk";

// Query relays for server announcements
await relayPool.subscribe([{ kinds: [SERVER_ANNOUNCEMENT_KIND] }], (event) => {
  const serverInfo = JSON.parse(event.content);
  console.log(`Found server: ${serverInfo.serverInfo.name}`);
  console.log(`Pubkey: ${event.pubkey}`);
});
```

## NostrClientTransport Options

| Option           | Type                       | Description                                     |
| ---------------- | -------------------------- | ----------------------------------------------- |
| `signer`         | `NostrSigner`              | Required. Signs all Nostr events                |
| `relayHandler`   | `RelayHandler \| string[]` | Required. Relay connection manager              |
| `serverPubkey`   | `string`                   | Required. Target server's public key            |
| `encryptionMode` | `EncryptionMode`           | `OPTIONAL`, `REQUIRED`, or `DISABLED`           |
| `isStateless`    | `boolean`                  | Skip initialization handshake. Default: `false` |
| `logLevel`       | `LogLevel`                 | Logging verbosity                               |

## Stateless Mode

Skip the initialization handshake for faster connections:

```typescript
const transport = new NostrClientTransport({
  signer,
  relayHandler: relayPool,
  serverPubkey: SERVER_PUBKEY,
  isStateless: true, // Skip initialize roundtrip
});
```

## Proxy Pattern

Use `NostrMCPProxy` to connect existing MCP clients to ContextVM servers:

```typescript
import { NostrMCPProxy } from "@contextvm/sdk";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const proxy = new NostrMCPProxy({
  // Local transport for existing client to connect to
  mcpHostTransport: new StdioServerTransport(),

  // Remote server connection
  nostrTransportOptions: {
    signer,
    relayHandler: relayPool,
    serverPubkey: SERVER_PUBKEY,
  },
});

await proxy.start();
```

This allows any standard MCP client to use ContextVM servers without native support.

## Encryption

Control encryption behavior:

```typescript
// Require encrypted connections only
encryptionMode: EncryptionMode.REQUIRED;

// Use encryption if server supports it (default)
encryptionMode: EncryptionMode.OPTIONAL;

// Never use encryption
encryptionMode: EncryptionMode.DISABLED;
```

## Client Templates

See [`assets/client-template.ts`](assets/client-template.ts) for a complete boilerplate.

## Tooling: ctxcn (generate a typed TypeScript client)

If you are building a TypeScript app and want remote ContextVM tools to feel like local functions, use `ctxcn`.

High-level behavior:

- Connects to a ContextVM server.
- Reads `tools/list` schemas.
- Generates TypeScript client code into your repo (shadcn-style: you own the generated code).

From ContextVM docs/blog references, the basic flow is:

```bash
npx @contextvm/ctxcn init
npx @contextvm/ctxcn add <server-pubkey>
npx @contextvm/ctxcn update
```

Use this when:

- You want end-to-end type safety.
- You want IDE autocomplete for server tools.
- You want to avoid hand-writing tool interfaces.

## Reference Materials

- [`references/nostr-way-without-sdks.md`](references/nostr-way-without-sdks.md) - The Nostr primitives behind CVM (raw events, JSON-RPC, manual implementation)
- [`references/discovery.md`](references/discovery.md) - Server discovery patterns
- [`references/proxy-pattern.md`](references/proxy-pattern.md) - Using NostrMCPProxy
- [`references/stateless-mode.md`](references/stateless-mode.md) - Stateless connection details
