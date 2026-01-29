---
name: tidbx-kysely
description: Set up Kysely with TiDB Cloud (TiDB X), including @tidbcloud/kysely over the TiDB Cloud serverless HTTP driver for serverless or edge environments, plus standard TCP usage. Use for Kysely + TiDB Cloud connection setup, demo snippets, and environment-specific guidance.
---

# TiDB Cloud + Kysely

Use this skill when a user wants to connect Kysely to TiDB Cloud (TiDB X). Default to
standard TCP (Node server/runtime). Only use the TiDB Cloud serverless driver over
HTTP for serverless or edge runtimes.

## Workflow

1. Confirm runtime and deployment target (Node server vs serverless/edge).
2. Confirm cluster type. The serverless HTTP driver applies to Starter/Essential clusters.
3. Collect connection info (prefer a `mysql://` URL in `DATABASE_URL`).
4. Choose the path:
   - Normal usage (default): TCP + `mysql2` pool + Kysely `MysqlDialect`.
   - Serverless/edge: `@tidbcloud/kysely` dialect over HTTP.
5. Show only the matching snippet first. Include the other path only if the user asks.
   Use `references/kysely-usage.md` for full examples.

## Normal usage (default)

Use this for Node servers, long-lived runtimes, or when TCP is available. This is the
primary path unless the user explicitly needs serverless/edge. Uses TCP with a `mysql2`
pool.

```ts
import { Kysely, MysqlDialect } from 'kysely'
import { createPool } from 'mysql2'

const pool = createPool({ uri: process.env.DATABASE_URL })
const db = new Kysely({ dialect: new MysqlDialect({ pool }) })
```

## Serverless/edge usage (HTTP)

Use this only when the runtime cannot keep TCP connections (serverless/edge). Requires
the TiDB Cloud serverless driver and Starter/Essential clusters. Use from backend
services only (browser origins may be blocked by CORS). See
`references/serverless-kysely-tutorial.md` for the full walkthrough.

```ts
import { Kysely } from 'kysely'
import { TiDBCloudServerlessDialect } from '@tidbcloud/kysely'

const db = new Kysely({
  dialect: new TiDBCloudServerlessDialect({ url: process.env.DATABASE_URL }),
})
```

## Notes

- Many users say "instance" to mean "cluster"; treat them as the same.
- Keep instructions concise; move any long docs into references.
