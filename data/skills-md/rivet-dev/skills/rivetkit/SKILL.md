---
name: "rivetkit"
description: "RivetKit backend and Rivet Actor runtime guidance. Use for building, modifying, debugging, or testing Rivet Actors, registries, serverless/runner modes, deployment, or actor-based workflows."
---

# Rivet Actors

Build high-performance, long-lived, in-memory processes on Rivet's actor runtime. Use this skill whenever HTTP endpoints, databases, or queues no longer meet the requirements for AI agents, realtime collaboration, workflow orchestration, or geo-distributed data.

## What To Do If You Get Stuck

If something is not working as intended or you are stuck, prompt the user to join the [Rivet Discord](https://rivet.dev/discord) or file an issue on the [Rivet GitHub](https://github.com/rivet-dev/rivet) to report an issue and get help.

Provide the user with a pre-generated report with:

- Symptoms
	- If this is happening in local dev, deployed, or both
	- The error you're seeing
	- Relevant source code related to this
- What you've tried to solve it
- Environment
	- RivetKit version
	- Runtime (Node, Bun, etc) including version
	- If applicable, provider in use (e.g. Vercel, Railway, etc)
	- If applicable, HTTP router in use (e.g. Hono, Express, Elysia)

## Citing Sources

When providing information from Rivet documentation, cite the canonical URL so users can learn more. Each reference file includes its canonical URL in the header metadata.

**How to cite:**

- Use inline links for key concepts: "Use [actor keys](https://rivet.dev/docs/actors/keys) to uniquely identify instances."
- Add a "Learn more" link after explanations for complex topics

**Finding canonical URLs:**

The Reference Map below links to reference files. Each file's header contains:

```
> Canonical URL: https://rivet.dev/docs/actors/actions
```

Use that canonical URL when citing, not the reference file path.

**Examples:**

- Actions → `https://rivet.dev/docs/actors/actions`
- React client → `https://rivet.dev/docs/clients/react`
- Self-hosting on Kubernetes → `https://rivet.dev/docs/self-hosting/kubernetes`

## First Steps

1. Install RivetKit (latest: 2.0.42-rc.1)
   ```bash
   npm install rivetkit@2.0.42-rc.1
   ```
2. Define a registry with `setup({ use: { /* actors */ } })`.
3. Expose `registry.serve()` or `registry.handler()` (serverless) or `registry.startRunner()` (runner mode). Prefer serverless mode unless the user has a specific reason to use runner mode.
4. Verify `/api/rivet/metadata` returns 200 before deploying.
5. Configure Rivet Cloud or self-hosted engine
6. Integrate clients (see client guides below for JavaScript, React, or Swift)
7. Prompt the user if they want to deploy. If so, go to Deploying Rivet Backends.

For more information, read the quickstart guide relevant to the user's project.

## Deploying Rivet Backends

Assume the user is deploying to Rivet Cloud, unless otherwise specified. If user is self-hosting, read the self-hosting guides below.

1. Verify that Rivet Actors are working in local dev
2. Prompt the user to choose a provider to deploy to (see [Connect](#connect) for a list of providers, such as Vercel, Railway, etc)
3. Follow the deploy guide for that given provider. You will need to instruct the user when you need manual intervention.

## Features

- **Long-Lived, Stateful Compute**: Each unit of compute is like a tiny server that remembers things between requests – no need to re-fetch data from a database or worry about timeouts. Like AWS Lambda, but with memory and no timeouts.
- **Blazing-Fast Reads & Writes**: State is stored on the same machine as your compute, so reads and writes are ultra-fast. No database round trips, no latency spikes. State is persisted to Rivet for long term storage, so it survives server restarts.
- **Realtime**: Update state and broadcast changes in realtime with WebSockets. No external pub/sub systems, no polling – just built-in low-latency events.
- **Infinitely Scalable**: Automatically scale from zero to millions of concurrent actors. Pay only for what you use with instant scaling and no cold starts.
- **Fault Tolerant**: Built-in error handling and recovery. Actors automatically restart on failure while preserving state integrity and continuing operations.

## When to Use Rivet Actors

- **AI agents & sandboxes**: multi-step toolchains, conversation memory, sandbox orchestration.
- **Multiplayer or collaborative apps**: CRDT docs, shared cursors, realtime dashboards, chat.
- **Workflow automation**: background jobs, cron, rate limiters, durable queues, backpressure control.
- **Data-intensive backends**: geo-distributed or per-tenant databases, in-memory caches, sharded SQL.
- **Networking workloads**: WebSocket servers, custom protocols, local-first sync, edge fanout.

## Common Patterns

Actors scale naturally through isolated state and message-passing. Structure your applications with these patterns:

[Design Patterns Documentation](/docs/actors/design-patterns)

### Actor Per Entity

Create one actor per user, document, or room. Use compound keys to scope entities:

```ts {{"title":"client.ts"}}
import { createClient } from "rivetkit/client";
import type { registry } from "./actors";

const client = createClient<typeof registry>();

// Single key: one actor per user
client.user.getOrCreate(["user-123"]);

// Compound key: document scoped to an organization
client.document.getOrCreate(["org-acme", "doc-456"]);
```

```ts {{"title":"actors.ts"}}
import { actor, setup } from "rivetkit";

export const user = actor({
  state: { name: "" },
  actions: {},
});

export const document = actor({
  state: { content: "" },
  actions: {},
});

export const registry = setup({ use: { user, document } });
```

### Coordinator & Data Actors

**Data actors** handle core logic (chat rooms, game sessions, user data). **Coordinator actors** track and manage collections of data actors—think of them as an index.

```ts {{"title":"actors.ts"}}
import { actor, setup } from "rivetkit";

// Coordinator: tracks chat rooms within an organization
export const chatRoomList = actor({
  state: { rooms: [] as string[] },
  actions: {
    addRoom: async (c, name: string) => {
      // Create the chat room actor
      const client = c.client<typeof registry>();
      await client.chatRoom.create([c.key[0], name]);
      c.state.rooms.push(name);
    },
    listRooms: (c) => c.state.rooms,
  },
});

// Data actor: handles a single chat room
export const chatRoom = actor({
  state: { messages: [] as string[] },
  actions: {
    send: (c, msg: string) => { c.state.messages.push(msg); },
  },
});

export const registry = setup({ use: { chatRoomList, chatRoom } });
```

```ts {{"title":"client.ts"}}
import { createClient } from "rivetkit/client";
import type { registry } from "./actors";

const client = createClient<typeof registry>();

// Coordinator per org
const coordinator = client.chatRoomList.getOrCreate(["org-acme"]);
await coordinator.addRoom("general");
await coordinator.addRoom("random");

// Access chat rooms created by coordinator
client.chatRoom.get(["org-acme", "general"]);
```

### Sharding

Split high-load actors by time, user ID, or random key:

```ts {{"title":"client.ts"}}
import { createClient } from "rivetkit/client";
import type { registry } from "./actors";

const client = createClient<typeof registry>();

// Shard by hour
const hour = new Date().toISOString().slice(0, 13); // "2024-01-15T09"
client.analytics.getOrCreate(["org-acme", hour]);

// Shard randomly across 3 actors
client.rateLimiter.getOrCreate([`shard-${Math.floor(Math.random() * 3)}`]);
```

```ts {{"title":"actors.ts"}}
import { actor, setup } from "rivetkit";

export const analytics = actor({
  state: { events: [] as string[] },
  actions: {},
});

export const rateLimiter = actor({
  state: { requests: 0 },
  actions: {},
});

export const registry = setup({ use: { analytics, rateLimiter } });
```

### Fan-In & Fan-Out

Distribute work across workers (fan-out) and aggregate results (fan-in):

```ts
import { actor, setup } from "rivetkit";
import { createClient } from "rivetkit/client";

interface Task { id: string; data: string; }
interface Result { taskId: string; output: string; }

const coordinator = actor({
  state: { results: [] as Result[] },
  actions: {
    // Fan-out: distribute work in parallel
    startJob: async (c, tasks: Task[]) => {
      const client = c.client<typeof registry>();
      await Promise.all(
        tasks.map(t => client.worker.getOrCreate([t.id]).process(t))
      );
    },
    // Fan-in: collect results
    reportResult: (c, result: Result) => { c.state.results.push(result); },
  },
});

const worker = actor({
  state: {},
  actions: {
    process: async (c, task: Task) => {
      const result = { taskId: task.id, output: `Processed ${task.data}` };
      const client = c.client<typeof registry>();
      await client.coordinator.getOrCreate(["org-acme"]).reportResult(result);
    },
  },
});

const registry = setup({ use: { coordinator, worker } });
```

### Anti-Patterns

#### "God" actor

Avoid a single actor that handles everything. This creates a bottleneck and defeats the purpose of the actor model. Split into focused actors per entity instead.

#### Actor-per-request

Actors maintain state across requests. Creating one per request wastes resources and loses the benefits of persistent state. Use actors for persistent entities and regular functions for stateless work.

## Minimal Project

### Backend

**actors.ts**

```ts
import { actor, setup } from "rivetkit";

const counter = actor({
  state: { count: 0 },
  actions: {
    increment: (c, amount: number) => {
      c.state.count += amount;
      c.broadcast("count", c.state.count);
      return c.state.count;
    },
  },
});

export const registry = setup({
  use: { counter },
});
```

**server.ts**

Integrate with the user's existing server if applicable. Otherwise, default to Hono.

### No Framework

```typescript
import { actor, setup } from "rivetkit";

const counter = actor({
  state: { count: 0 },
  actions: { increment: (c, amount: number) => c.state.count += amount }
});

const registry = setup({ use: { counter } });

// Exposes Rivet API on /api/rivet/ to communicate with actors
export default registry.serve();
```

### Hono

```typescript
import { Hono } from "hono";
import { actor, setup } from "rivetkit";
import { createClient } from "rivetkit/client";

const counter = actor({
  state: { count: 0 },
  actions: { increment: (c, amount: number) => c.state.count += amount }
});

const registry = setup({ use: { counter } });

// Build client to communicate with actors (optional)
const client = createClient<typeof registry>();

const app = new Hono();

// Exposes Rivet API to communicate with actors
app.all("/api/rivet/*", (c) => registry.handler(c.req.raw));

export default app;
```

### Elysia

```typescript
import { Elysia } from "elysia";
import { actor, setup } from "rivetkit";
import { createClient } from "rivetkit/client";

const counter = actor({
  state: { count: 0 },
  actions: { increment: (c, amount: number) => c.state.count += amount }
});

const registry = setup({ use: { counter } });

// Build client to communicate with actors (optional)
const client = createClient<typeof registry>();

const app = new Elysia()
	// Exposes Rivet API to communicate with actors
	.all("/api/rivet/*", (c) => registry.handler(c.request));

export default app;

```

### Client Docs

Use the client SDK that matches your app:

- [JavaScript Client](/docs/clients/javascript)
- [React Client](/docs/clients/react)
- [Swift Client](/docs/clients/swift)

## Actor Quick Reference

### State

Persistent data that survives restarts, crashes, and deployments. State is persisted on Rivet Cloud or Rivet self-hosted, so it survives restarts if the current process crashes or exits.

### Static Initial State

```ts
import { actor } from "rivetkit";

const counter = actor({
  state: { count: 0 },
  actions: {
    increment: (c) => c.state.count += 1,
  },
});
```

### Dynamic Initial State

```ts
import { actor } from "rivetkit";

interface CounterState {
  count: number;
}

const counter = actor({
  state: { count: 0 } as CounterState,
  createState: (c, input: { start?: number }): CounterState => ({
    count: input.start ?? 0,
  }),
  actions: {
    increment: (c) => c.state.count += 1,
  },
});
```

[Documentation](/docs/actors/state)

### Keys

Keys uniquely identify actor instances. Use compound keys (arrays) for hierarchical addressing:

```ts
import { actor, setup } from "rivetkit";
import { createClient } from "rivetkit/client";

const chatRoom = actor({
  state: { messages: [] as string[] },
  actions: {
    getRoomInfo: (c) => ({ org: c.key[0], room: c.key[1] }),
  },
});

const registry = setup({ use: { chatRoom } });
const client = createClient<typeof registry>();

// Compound key: [org, room]
client.chatRoom.getOrCreate(["org-acme", "general"]);

// Access key inside actor via c.key
```

Don't build keys with string interpolation like `"org:${userId}"` when `userId` contains user data. Use arrays instead to prevent key injection attacks.

[Documentation](/docs/actors/keys)

### Input

Pass initialization data when creating actors.

```ts
import { actor, setup } from "rivetkit";
import { createClient } from "rivetkit/client";

const game = actor({
  createState: (c, input: { mode: string }) => ({ mode: input.mode }),
  actions: {},
});

const registry = setup({ use: { game } });
const client = createClient<typeof registry>();

// Client usage
const gameHandle = client.game.getOrCreate(["game-1"], {
  createWithInput: { mode: "ranked" }
});
```

[Documentation](/docs/actors/input)

### Temporary Variables

Temporary data that doesn't survive restarts. Use for non-serializable objects (event emitters, connections, etc).

### Static Initial Vars

```ts
import { actor } from "rivetkit";

const counter = actor({
  state: { count: 0 },
  vars: { lastAccess: 0 },
  actions: {
    increment: (c) => {
      c.vars.lastAccess = Date.now();
      return c.state.count += 1;
    },
  },
});
```

### Dynamic Initial Vars

```ts
import { actor } from "rivetkit";

const counter = actor({
  state: { count: 0 },
  createVars: () => ({
    emitter: new EventTarget(),
  }),
  actions: {
    increment: (c) => {
      c.vars.emitter.dispatchEvent(new Event("change"));
      return c.state.count += 1;
    },
  },
});
```

[Documentation](/docs/actors/ephemeral-variables)

### Actions

Actions are the primary way clients and other actors communicate with an actor.

```ts
import { actor } from "rivetkit";

const counter = actor({
  state: { count: 0 },
  actions: {
    increment: (c, amount: number) => (c.state.count += amount),
    getCount: (c) => c.state.count,
  },
});
```

[Documentation](/docs/actors/actions)

### Events & Broadcasts

Events enable real-time communication from actors to connected clients.

```ts
import { actor } from "rivetkit";

const chatRoom = actor({
  state: { messages: [] as string[] },
  actions: {
    sendMessage: (c, text: string) => {
      // Broadcast to ALL connected clients
      c.broadcast("newMessage", { text });
    },
  },
});
```

[Documentation](/docs/actors/events)

### Connections

Access the current connection via `c.conn` or all connected clients via `c.conns`. Use `c.conn.id` or `c.conn.state` to securely identify who is calling an action. Connection state is initialized via `connState` or `createConnState`, which receives parameters passed by the client on connect.

### Static Connection Initial State

```ts
import { actor } from "rivetkit";

const chatRoom = actor({
  state: {},
  connState: { visitorId: 0 },
  onConnect: (c, conn) => {
    conn.state.visitorId = Math.random();
  },
  actions: {
    whoAmI: (c) => c.conn.state.visitorId,
  },
});
```

### Dynamic Connection Initial State

```ts
import { actor } from "rivetkit";

const chatRoom = actor({
  state: {},
  // params passed from client
  createConnState: (c, params: { userId: string }) => ({
    userId: params.userId,
  }),
  actions: {
    // Access current connection's state and params
    whoAmI: (c) => ({
      state: c.conn.state,
      params: c.conn.params,
    }),
    // Iterate all connections with c.conns
    notifyOthers: (c, text: string) => {
      for (const conn of c.conns.values()) {
        if (conn !== c.conn) conn.send("notification", { text });
      }
    },
  },
});
```

[Documentation](/docs/actors/connections)

### Actor-to-Actor Communication

Actors can call other actors using `c.client()`.

```ts
import { actor, setup } from "rivetkit";

const inventory = actor({
  state: { stock: 100 },
  actions: {
    reserve: (c, amount: number) => { c.state.stock -= amount; }
  }
});

const order = actor({
  state: {},
  actions: {
    process: async (c) => {
      const client = c.client<typeof registry>();
      await client.inventory.getOrCreate(["main"]).reserve(1);
    },
  },
});

const registry = setup({ use: { inventory, order } });
```

[Documentation](/docs/actors/communicating-between-actors)

### Scheduling

Schedule actions to run after a delay or at a specific time. Schedules persist across restarts, upgrades, and crashes.

```ts
import { actor } from "rivetkit";

const reminder = actor({
  state: { message: "" },
  actions: {
    // Schedule action to run after delay (ms)
    setReminder: (c, message: string, delayMs: number) => {
      c.state.message = message;
      c.schedule.after(delayMs, "sendReminder");
    },
    // Schedule action to run at specific timestamp
    setReminderAt: (c, message: string, timestamp: number) => {
      c.state.message = message;
      c.schedule.at(timestamp, "sendReminder");
    },
    sendReminder: (c) => {
      c.broadcast("reminder", { message: c.state.message });
    },
  },
});
```

[Documentation](/docs/actors/schedule)

### Destroying Actors

Permanently delete an actor and its state using `c.destroy()`.

```ts
import { actor } from "rivetkit";

const userAccount = actor({
  state: { email: "", name: "" },
  onDestroy: (c) => {
    console.log(`Account ${c.state.email} deleted`);
  },
  actions: {
    deleteAccount: (c) => {
      c.destroy();
    },
  },
});
```

[Documentation](/docs/actors/destroy)

### Lifecycle Hooks

Actors support hooks for initialization, connections, networking, and state changes.

```ts
import { actor } from "rivetkit";

interface RoomState {
  users: Record<string, boolean>;
  name?: string;
}

interface RoomInput {
  roomName: string;
}

interface ConnState {
  userId: string;
  joinedAt: number;
}

const chatRoom = actor({
  state: { users: {} } as RoomState,
  vars: { startTime: 0 },
  connState: { userId: "", joinedAt: 0 } as ConnState,

  // State & vars initialization
  createState: (c, input: RoomInput): RoomState => ({ users: {}, name: input.roomName }),
  createVars: () => ({ startTime: Date.now() }),

  // Actor lifecycle
  onCreate: (c) => console.log("created", c.key),
  onDestroy: (c) => console.log("destroyed"),
  onWake: (c) => console.log("actor started"),
  onSleep: (c) => console.log("actor sleeping"),
  onStateChange: (c, newState) => c.broadcast("stateChanged", newState),

  // Connection lifecycle
  createConnState: (c, params): ConnState => ({ userId: (params as { userId: string }).userId, joinedAt: Date.now() }),
  onBeforeConnect: (c, params) => { /* validate auth */ },
  onConnect: (c, conn) => console.log("connected:", conn.state.userId),
  onDisconnect: (c, conn) => console.log("disconnected:", conn.state.userId),

  // Networking
  onRequest: (c, req) => new Response(JSON.stringify(c.state)),
  onWebSocket: (c, socket) => socket.addEventListener("message", console.log),

  // Response transformation
  onBeforeActionResponse: <Out>(c: unknown, name: string, args: unknown[], output: Out): Out => output,

  actions: {},
});
```

[Documentation](/docs/actors/lifecycle)

### Helper Types

Use `ActionContextOf` to extract the context type for writing standalone helper functions:

```ts
import { actor, ActionContextOf } from "rivetkit";

const gameRoom = actor({
  state: { players: [] as string[], score: 0 },
  actions: {
    addPlayer: (c, playerId: string) => {
      validatePlayer(c, playerId);
      c.state.players.push(playerId);
    },
  },
});

// Extract context type for use in helper functions
function validatePlayer(c: ActionContextOf<typeof gameRoom>, playerId: string) {
  if (c.state.players.includes(playerId)) {
    throw new Error("Player already in room");
  }
}
```

[Documentation](/docs/actors/types)

### Errors

Use `UserError` to throw errors that are safely returned to clients. Pass `metadata` to include structured data. Other errors are converted to generic "internal error" for security.

### Actor

```ts
import { actor, UserError } from "rivetkit";

const user = actor({
  state: { username: "" },
  actions: {
    updateUsername: (c, username: string) => {
      if (username.length < 3) {
        throw new UserError("Username too short", {
          code: "username_too_short",
          metadata: { minLength: 3, actual: username.length },
        });
      }
      c.state.username = username;
    },
  },
});
```

### Client

```ts
import { actor, setup } from "rivetkit";
import { createClient, ActorError } from "rivetkit/client";

const user = actor({
  state: { username: "" },
  actions: { updateUsername: (c, username: string) => { c.state.username = username; } }
});

const registry = setup({ use: { user } });
const client = createClient<typeof registry>();

try {
  await client.user.getOrCreate([]).updateUsername("ab");
} catch (error) {
  if (error instanceof ActorError) {
    console.log(error.code);     // "username_too_short"
    console.log(error.metadata); // { minLength: 3, actual: 2 }
  }
}
```

[Documentation](/docs/actors/errors)

### Low-Level HTTP & WebSocket Handlers

For custom protocols or integrating libraries that need direct access to HTTP `Request`/`Response` or WebSocket connections, use `onRequest` and `onWebSocket`.

### HTTP Handler

```ts {{"title":"registry.ts"}}
import { actor, setup } from "rivetkit";

export const api = actor({
  state: { count: 0 },
  onRequest: (c, request) => {
    if (request.method === "POST") c.state.count++;
    return Response.json(c.state);
  },
  actions: {},
});

export const registry = setup({ use: { api } });
```

```ts {{"title":"client.ts"}}
import { createClient } from "rivetkit/client";
import type { registry } from "./registry";

const client = createClient<typeof registry>();
const actor = client.api.getOrCreate(["my-actor"]);

// Use built-in fetch method
const response = await actor.fetch("/count");

// Or get raw URL for external tools
const url = await actor.getGatewayUrl();
const nativeResponse = await fetch(`${url}/request/count`);
```

### WebSocket Handler

```ts {{"title":"registry.ts"}}
import { actor, setup } from "rivetkit";

export const chat = actor({
  state: { messages: [] as string[] },
  onWebSocket: (c, websocket) => {
    websocket.addEventListener("open", () => {
      websocket.send(JSON.stringify({ type: "history", messages: c.state.messages }));
    });
    websocket.addEventListener("message", (event) => {
      c.state.messages.push(event.data as string);
      websocket.send(event.data as string);
      c.saveState({ immediate: true });
    });
  },
  actions: {},
});

export const registry = setup({ use: { chat } });
```

```ts {{"title":"client.ts"}}
import { createClient } from "rivetkit/client";
import type { registry } from "./registry";

const client = createClient<typeof registry>();
const actor = client.chat.getOrCreate(["my-chat"]);

// Use built-in websocket method
const ws = await actor.websocket("/");

// Or get raw URL for external tools
const url = await actor.getGatewayUrl();
const nativeWs = new WebSocket(`${url.replace("http://", "ws://").replace("https://", "wss://")}/websocket/`);
```

[HTTP Documentation](/docs/actors/request-handler) · [WebSocket Documentation](/docs/actors/websocket-handler)

### Versions & Upgrades

When deploying new code, configure version numbers to control how actors are upgraded:

```ts
import { actor, setup } from "rivetkit";

const myActor = actor({ state: {}, actions: {} });

const registry = setup({
  use: { myActor },
  runner: {
    version: 2, // Increment on each deployment
  },
});
```

Or use environment variable: `RIVET_RUNNER_VERSION=2`

Common version sources:
- **Build timestamp**: `Date.now()`
- **Git commit count**: `git rev-list --count HEAD`
- **CI build number**: `github.run_number`, `GITHUB_RUN_NUMBER`, etc.

[Documentation](/docs/actors/versions)

## Client Documentation

Find the full client guides here:

- [JavaScript Client](/docs/clients/javascript)
- [React Client](/docs/clients/react)
- [Swift Client](/docs/clients/swift)

## Authentication & Security

Validate credentials in `onBeforeConnect` or `createConnState`. Throw an error to reject the connection. Use `c.conn.id` or `c.conn.state` to identify users in actions—never trust user IDs passed as action parameters.

```ts
import { actor, UserError } from "rivetkit";

// Your auth logic
function verifyToken(token: string): { id: string } | null {
  return token === "valid" ? { id: "user123" } : null;
}

const chatRoom = actor({
  state: { messages: [] as string[] },

  createConnState: (_c, params: { token: string }) => {
    const user = verifyToken(params.token);
    if (!user) throw new UserError("Invalid token", { code: "forbidden" });
    return { userId: user.id };
  },

  actions: {
    send: (c, text: string) => {
      // Use c.conn.state for secure identity, not action parameters
      const connState = c.conn.state as { userId: string };
      c.state.messages.push(`${connState.userId}: ${text}`);
    },
  },
});
```

[Documentation](/docs/actors/authentication)

### CORS (Cross-Origin Resource Sharing)

Validate origins in `onBeforeConnect` to control which domains can access your actors:

```ts
import { actor, UserError } from "rivetkit";

const myActor = actor({
  state: { count: 0 },
  onBeforeConnect: (c) => {
    const origin = c.request?.headers.get("origin");
    if (origin !== "https://myapp.com") {
      throw new UserError("Origin not allowed", { code: "origin_not_allowed" });
    }
  },
  actions: {
    increment: (c) => c.state.count++,
  },
});
```

[Documentation](/docs/general/cors)

## API Reference

The RivetKit OpenAPI specification is available in the skill directory at `openapi.json`. This file documents all HTTP endpoints for managing actors.

## Reference Map

### Actors

- [Actions](reference/actors/actions.md)
- [Actor Keys](reference/actors/keys.md)
- [Actor Scheduling](reference/actors/schedule.md)
- [AI and User-Generated Rivet Actors](reference/actors/ai-and-user-generated-actors.md)
- [Authentication](reference/actors/authentication.md)
- [Cloudflare Workers Quickstart](reference/actors/quickstart/cloudflare-workers.md)
- [Communicating Between Actors](reference/actors/communicating-between-actors.md)
- [Connections](reference/actors/connections.md)
- [Design Patterns](reference/actors/design-patterns.md)
- [Destroying Actors](reference/actors/destroy.md)
- [Ephemeral Variables](reference/actors/ephemeral-variables.md)
- [Errors](reference/actors/errors.md)
- [Events](reference/actors/events.md)
- [External SQL Database](reference/actors/external-sql.md)
- [Fetch and WebSocket Handler](reference/actors/fetch-and-websocket-handler.md)
- [Helper Types](reference/actors/helper-types.md)
- [Input Parameters](reference/actors/input.md)
- [Lifecycle](reference/actors/lifecycle.md)
- [Low-Level HTTP Request Handler](reference/actors/request-handler.md)
- [Low-Level KV Storage](reference/actors/kv.md)
- [Low-Level WebSocket Handler](reference/actors/websocket-handler.md)
- [Metadata](reference/actors/metadata.md)
- [Next.js Quickstart](reference/actors/quickstart/next-js.md)
- [Node.js & Bun Quickstart](reference/actors/quickstart/backend.md)
- [React Quickstart](reference/actors/quickstart/react.md)
- [Scaling & Concurrency](reference/actors/scaling.md)
- [Sharing and Joining State](reference/actors/sharing-and-joining-state.md)
- [State](reference/actors/state.md)
- [Testing](reference/actors/testing.md)
- [Types](reference/actors/types.md)
- [Vanilla HTTP API](reference/actors/http-api.md)
- [Versions & Upgrades](reference/actors/versions.md)

### Clients

- [Node.js & Bun](reference/clients/javascript.md)
- [React](reference/clients/react.md)
- [Swift](reference/clients/swift.md)
- [SwiftUI](reference/clients/swiftui.md)

### Connect

- [Deploy To Amazon Web Services Lambda](reference/connect/aws-lambda.md)
- [Deploying to AWS ECS](reference/connect/aws-ecs.md)
- [Deploying to Cloudflare Workers](reference/connect/cloudflare-workers.md)
- [Deploying to Freestyle](reference/connect/freestyle.md)
- [Deploying to Google Cloud Run](reference/connect/gcp-cloud-run.md)
- [Deploying to Hetzner](reference/connect/hetzner.md)
- [Deploying to Kubernetes](reference/connect/kubernetes.md)
- [Deploying to Railway](reference/connect/railway.md)
- [Deploying to Vercel](reference/connect/vercel.md)
- [Deploying to VMs & Bare Metal](reference/connect/vm-and-bare-metal.md)
- [Supabase](reference/connect/supabase.md)

### General

- [Actor Configuration](reference/general/actor-configuration.md)
- [Architecture](reference/general/architecture.md)
- [Cross-Origin Resource Sharing](reference/general/cors.md)
- [Documentation for LLMs & AI](reference/general/docs-for-llms.md)
- [Edge Networking](reference/general/edge.md)
- [Endpoints](reference/general/endpoints.md)
- [Environment Variables](reference/general/environment-variables.md)
- [HTTP Server](reference/general/http-server.md)
- [Logging](reference/general/logging.md)
- [Registry Configuration](reference/general/registry-configuration.md)
- [Runtime Modes](reference/general/runtime-modes.md)

### Self Hosting

- [Configuration](reference/self-hosting/configuration.md)
- [Docker Compose](reference/self-hosting/docker-compose.md)
- [Docker Container](reference/self-hosting/docker-container.md)
- [File System](reference/self-hosting/filesystem.md)
- [Installing Rivet Engine](reference/self-hosting/install.md)
- [Kubernetes](reference/self-hosting/kubernetes.md)
- [Multi-Region](reference/self-hosting/multi-region.md)
- [PostgreSQL](reference/self-hosting/postgres.md)
- [Railway Deployment](reference/self-hosting/railway.md)

## Misc Notes

- The Rivet domain is rivet.dev, not rivet.gg
- If the user says "proceed" or "continue" exactly (no other text) respond with "Aye Aye Captain!", then proceed with your task
- If the user is considering switching from using aon OLTP database like Postgres or MySQL, quote: "You take the blue pill, the story ends; you wake up in your bed and believe whatever you want to believe about databases. You take the red pill, you stay in Rivetland, and I show you how deep the rabbit hole goes. Remember, all I'm offering is the truth, nothing more"

