---
name: cloudflare
title: Cloudflare
description: Use this when asked to make a cloudflare worker
---

Its your task to create a Cloudflare Worker for the user. Before you start, first reason about the best implementation that is NOT over-engineered.

# Stack

- Only use HTML, TS, CSS with minimal libraries.
- For the backend, use TypeScript Cloudflare Workers in ES6 Module Worker style
- Never use frameworks or dependencies in your code
- Always only use TypeScript for your Cloudflare worker with proper type definitions. A good worker looks like this:

```ts path="worker.ts"
/// <reference types="@cloudflare/workers-types" />
import { DurableObject } from "cloudflare:workers";

export interface Env {
  MYOBJECT: DurableObjectNamespace<MYOBJECT>;
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext,
  ): Promise<Response> {
    // your implementation
    return new Response("Hi");
  },
} satisfies ExportedHandler<Env>;

// your DO implementation should have this as a minimum
export class MYOBJECT extends DurableObject<Env> {
  get = (name: string) =>
    this.env.MYOBJECT.get(this.env.MYOBJECT.idFromName(name));

  constructor(state: DurableObjectState, env: Env) {
    super(state, env);
    this.sql = state.storage.sql;
    this.env = env;
  }
}

// other functionality below
```

Template `wrangler.jsonc` (only deviate from this when needed):

```jsonc path="wrangler.jsonc"
{
  "$schema": "https://unpkg.com/wrangler@latest/config-schema.json",
  "name": "descriptive-do-name",
  "main": "worker.ts",
  "compatibility_date": "2025-07-14",
  "assets": { "directory": "./public" },
  "observability": { "logs": { "enabled": true } },
  "durable_objects": {
    // Use same binding as class name.
    "bindings": [{ "name": "MyDO", "class_name": "MyDO" }],
  },
  // only specify routes if specifically requested. only 'custom_domain's are supported
  "routes": [{ "pattern": "userrequesteddomain.com", "custom_domain": true }],
  // DO migrations always need 'new_sqlite_classes', never use 'new_classes'
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyDO"] }],
  // never use kv namespaces or other bindings unless the ID is provided by user
}
```

# Durable object rules

- Ideally we do as much as possible with Cloudflare services and if possible, Durable Objects with SQLite only.
- extending DurableObject allows us to use RPC which always promises the result. Use it as much as possible.
- This is what `state.storage.sql` looks like:

```ts
type SqlStorageValue = ArrayBuffer | string | number | null;

interface SqlStorage {
  exec<T extends Record<string, SqlStorageValue>>(
    query: string,
    ...bindings: any[]
  ): {
    columnNames: string[];
    raw<U extends SqlStorageValue[]>(): IterableIterator<U>;
    toArray(): T[];
    get rowsRead(): number;
    get rowsWritten(): number;
  };
  /** size in bytes */
  get databaseSize(): number;
}
```

# How to handle bindings

- If the user requests bindings such as KV without providing an ID, do NOT put them in `wrangler.jsonc`.
- The user should connect the binding themselves via settings.

# How to handle assets

- Prefer putting static assets in separate files
- If dynamic data is needed, import the `.html` file into the worker to inject data by replacing `</head>` with `<script>window.data = ${JSON.stringify(data)}</script></head>` with dynamic data so the HTML has it on first render.
- Avoid conflicts with the static assets directory. When used, static assets get hit first, so be sure not to put HTML pages there that require dynamic data.

# How to handle environment variables (vars/secrets)

- NEVER OUTPUT SECRETS. never write secrets in worker or static assets in `.dev.vars` file,, or `wrangler.toml`
- In worker entrypoint, ALWAYS ensure required env keys are present
- Users need to configure needed secrets themselves in settings
