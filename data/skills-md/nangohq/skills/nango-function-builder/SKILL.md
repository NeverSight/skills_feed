---
name: nango-function-builder
description: Build Nango Functions (TypeScript createAction/createSync/createOnEvent) using the Nango Runner SDK. Includes project/root checks, endpoint conventions, retries/pagination, deletion detection, metadata, and a docs-aligned dryrun/test workflow.
---

# Nango Function Builder
Build deployable Nango functions (actions, syncs, on-event hooks) with repeatable patterns and validation steps.

## When to use
- User wants to build or modify a Nango function
- User wants to build an action in Nango
- User wants to build a sync in Nango
- User wants to build an on-event hook (validate-connection, post-connection-creation, pre-connection-deletion)

## Useful Nango docs (quick links)
- Functions runtime SDK reference: https://nango.dev/docs/reference/functions
- Implement an action: https://nango.dev/docs/implementation-guides/use-cases/actions/implement-an-action
- Implement a sync: https://nango.dev/docs/implementation-guides/use-cases/syncs/implement-a-sync
- Implement an event handler (lifecycle hooks): https://nango.dev/docs/implementation-guides/use-cases/implement-event-handler
- Testing integrations (dryrun, --save, Vitest): https://nango.dev/docs/implementation-guides/platform/functions/testing
- Deletion detection (full vs incremental): https://nango.dev/docs/implementation-guides/use-cases/syncs/deletion-detection
- Migrate from nango.yaml (Zero YAML): https://nango.dev/docs/implementation-guides/platform/migrations/migrate-to-zero-yaml

## Workflow (recommended)
1. Verify this is a Zero YAML TypeScript project (no `nango.yaml`) and you are in the Nango root (`.nango/` exists).
2. Compile as needed with `nango compile` (one-off).
3. Create/update the function file under `{integrationId}/actions/`, `{integrationId}/syncs/`, or `{integrationId}/on-events/`.
4. Register the file in `index.ts` (side-effect import).
5. Validate with `nango dryrun ... --validate`.
6. Record mocks with `nango dryrun ... --save` and generate tests with `nango generate:tests`.
7. Run `npm test`.
8. Deploy with `nango deploy dev`.

## Preconditions (Do Before Writing Code)

### Confirm TypeScript Project (No nango.yaml)

This skill only supports TypeScript projects using createAction()/createSync()/createOnEvent().

```bash
ls nango.yaml 2>/dev/null && echo "YAML PROJECT DETECTED" || echo "OK - No nango.yaml"
```

If you see YAML PROJECT DETECTED:
- Stop immediately.
- Tell the user to upgrade to the TypeScript format first.
- Do not attempt to mix YAML and TypeScript.

Reference: https://nango.dev/docs/implementation-guides/platform/migrations/migrate-to-zero-yaml

### Verify Nango Project Root

Do not create files until you confirm the Nango root:

```bash
ls -la .nango/ 2>/dev/null && pwd && echo "IN NANGO PROJECT ROOT" || echo "NOT in Nango root"
```

If you see NOT in Nango root:
- cd into the directory that contains .nango/
- Re-run the check
- Do not use absolute paths as a workaround

All file paths must be relative to the Nango root. Creating files with extra prefixes while already in the Nango root will create nested directories that break the build.

## Project Structure and Naming

```
./
|-- .nango/
|-- index.ts
|-- hubspot/
|   |-- actions/
|   |   `-- create-contact.ts
|   |-- on-events/
|   |   `-- validate-connection.ts
|   `-- syncs/
|       `-- fetch-contacts.ts
`-- slack/
    `-- actions/
        `-- post-message.ts
```

- Provider directories: lowercase (hubspot, slack)
- Action files: kebab-case (create-contact.ts)
- Event handler files: kebab-case in `on-events/` (validate-connection.ts)
- Sync files: kebab-case (many teams use a `fetch-` prefix, but it's optional)
- One function per file (action, sync, or on-event)
- All actions, syncs, and on-event hooks must be imported in index.ts

### Register scripts in `index.ts` (required)

Use side-effect imports only (no default/named imports). Include the `.js` extension.

```typescript
// index.ts
import './github/actions/get-top-contributor.js';
import './github/syncs/fetch-issues.js';
import './github/on-events/validate-connection.js';
```

Symptom of incorrect registration: the file compiles but you see `No entry points found in index.ts...` or the function never appears.

## Decide: Action vs Sync vs OnEvent

Action:
- One-time request, user-triggered
- CRUD operations and small lookups
- Thin API wrapper

Sync:
- Continuous data sync on a schedule
- Fetches all records or incremental changes
- Uses batchSave/batchDelete

OnEvent:
- Runs on connection lifecycle events (e.g., validate credentials)
- Good for verification and setup/cleanup hooks

If unclear, ask the user which behavior they want (one-time vs scheduled vs lifecycle hook).

## Required Inputs (Ask User if Missing)

Always:
- Integration ID (provider name)
- Connection ID (for dryrun)
- Function name (kebab-case)
- API reference URL or sample response

Action-specific:
- Use case summary
- Input parameters
- Output fields
- Metadata JSON if required
- Test input JSON for dryrun/mocks

Sync-specific:
- Model name (singular, PascalCase)
- Sync type (full or incremental)
- Frequency (every hour, every 5 minutes, etc.)
- Metadata JSON if required (team_id, workspace_id)

OnEvent-specific:
- Event type (validate-connection, post-connection-creation, pre-connection-deletion)
- Expected behavior (what to validate/change)

If any of these are missing, ask the user for them before writing code. Use their values in dryrun commands and tests.

### Prompt Templates (Use When Details Are Missing)

Action prompt:

```
Please provide:
Integration ID (required):
Connection ID (required):
Use Case Summary:
Action Inputs:
Action Outputs:
Metadata JSON (if required):
Action Name (kebab-case):
API Reference URL:
Test Input JSON:
```

Sync prompt:

```
Please provide:
Integration ID (required):
Connection ID (required):
Model Name (singular, PascalCase):
Endpoint Path (for Nango endpoint):
Frequency (every hour, every 5 minutes, etc.):
Sync Type (full or incremental):
Metadata JSON (if required):
API Reference URL:
```

## Non-Negotiable Rules (Shared)

### Platform constraints (docs-backed)

- Zero YAML TypeScript projects do not use `nango.yaml`. Define functions with `createAction()`, `createSync()`, or `createOnEvent()`.
- Register every action/sync/on-event in `index.ts` via side-effect import (`import './<path>.js'`) or it will not load.
- You cannot install/import arbitrary third-party packages in Functions. Relative imports inside the Nango project are supported. Pre-included dependencies include `zod`, `crypto`/`node:crypto`, and `url`/`node:url`.
- Sync records must include a stable string `id`.
- Action outputs cannot exceed 2MB.
- `deleteRecordsFromPreviousExecutions()` is for full refresh syncs only. Call it only after you successfully fetched + saved the full dataset; do not swallow errors and still call it.
- HTTP request retries default to `0`. Set `retries` intentionally (and be careful retrying non-idempotent writes).

### Conventions (recommended)

- Prefer explicit parameter names (`user_id`, `channel_id`, `team_id`).
- Add `.describe()` examples for IDs, timestamps, enums, and URLs.
- Avoid `any`; use inline types when mapping responses.
- Prefer static Nango endpoint paths (avoid `:id` / `{id}` in the exposed endpoint); pass IDs in input/params.
- Add an API doc link comment above each provider API call.
- Standardize list actions on `cursor`/`next_cursor`.
- For optional outputs, return `null` only when the output schema models `null`.
- Use `nango.zodValidateInput()` when you need custom input validation/logging; otherwise rely on schemas + `nango dryrun --validate`.

Symptom of missing index.ts import: file compiles without errors but does not appear in the build output.

### Parameter Naming Rules

- IDs: suffix with _id (user_id, channel_id)
- Names: suffix with _name (channel_name)
- Emails: suffix with _email (user_email)
- URLs: suffix with _url (callback_url)
- Timestamps: use *_at or *_time (created_at, scheduled_time)

Mapping example (API expects a different parameter name):

```typescript
const InputSchema = z.object({
    user_id: z.string()
});

const config: ProxyConfiguration = {
    endpoint: 'users.info',
    params: {
        user: input.user_id
    },
    retries: 3
};
```

## Action Template (createAction)

Notes:
- `input` is required even for "no input" actions. Use `z.object({})`.
- Do not import `ActionError` as a value from `nango` (it is a type-only export in recent versions). Throw `new nango.ActionError(payload)` using the `nango` exec parameter.
- `ProxyConfiguration` typing is optional. Only import it if you explicitly annotate a variable.

```typescript
import { z } from 'zod';
import { createAction } from 'nango';

const InputSchema = z.object({
    user_id: z.string().describe('User ID. Example: "123"')
    // For no-input actions use: z.object({})
});

const OutputSchema = z.object({
    id: z.string(),
    name: z.union([z.string(), z.null()])
});

const action = createAction({
    description: 'Brief single sentence',
    version: '1.0.0',

    endpoint: {
        method: 'GET',
        path: '/user',
        group: 'Users'
    },

    input: InputSchema,
    output: OutputSchema,
    scopes: ['required.scope'],

    exec: async (nango, input): Promise<z.infer<typeof OutputSchema>> => {
        const response = await nango.get({
            // https://api-docs-url
            endpoint: '/api/v1/users',
            params: {
                userId: input.user_id
            },
            retries: 3 // safe for idempotent GETs; be careful retrying non-idempotent writes
        });

        if (!response.data) {
            throw new nango.ActionError({
                type: 'not_found',
                message: 'User not found',
                user_id: input.user_id
            });
        }

        return {
            id: response.data.id,
            name: response.data.name ?? null
        };
    }
});

export type NangoActionLocal = Parameters<(typeof action)['exec']>[0];
export default action;
```

### Action Metadata (When Required)

Use metadata when the action depends on connection-specific values.

```typescript
const MetadataSchema = z.object({
    team_id: z.string()
});

const action = createAction({
    metadata: MetadataSchema,

    exec: async (nango, input) => {
        const metadata = await nango.getMetadata<{ team_id?: string }>();
        const teamId = metadata?.team_id;

        if (!teamId) {
            throw new nango.ActionError({
                type: 'invalid_metadata',
                message: 'team_id is required in metadata.'
            });
        }
    }
});
```

### Action CRUD Patterns

| Operation | Method | Config Pattern |
|-----------|--------|----------------|
| Create | nango.post(config) | data: { properties: {...} } |
| Read | nango.get(config) | endpoint: `resource/${id}`, params: {...} |
| Update | nango.patch(config) | endpoint: `resource/${id}`, data: {...} |
| Delete | nango.delete(config) | endpoint: `resource/${id}` |
| List | nango.get(config) | params: {...} with pagination |

Note: These endpoint examples are for ProxyConfiguration (provider API). The createAction endpoint path must stay static.

Recommended in most configs:
- API doc link comment above endpoint
- retries: set intentionally (often `3` for idempotent GET/LIST; avoid retries for non-idempotent POST unless the API supports idempotency)

Optional input fields pattern:

```typescript
data: {
    required_field: input.required_field,
    ...(input.optional_field && { optional_field: input.optional_field })
}
```

### Action Error Handling (ActionError)

Use ActionError for expected failures (not found, validation, rate limit). Use standard Error for unexpected failures.

```typescript
if (response.status === 429) {
    throw new nango.ActionError({
        type: 'rate_limited',
        message: 'API rate limit exceeded',
        retry_after: response.headers['retry-after']
    });
}
```

Do not return null-filled objects to indicate "not found". Use ActionError instead.

ActionError response format:

```json
{
  "error_type": "action_script_failure",
  "payload": {
    "type": "not_found",
    "message": "User not found",
    "user_id": "123"
  }
}
```

### Action Pagination Standard (List Actions)

All list actions must use cursor/next_cursor regardless of provider naming.

Schema pattern:

```typescript
const ListInput = z.object({
    cursor: z.string().optional().describe('Pagination cursor from previous response. Omit for first page.')
});

const ListOutput = z.object({
    items: z.array(ItemSchema),
    next_cursor: z.union([z.string(), z.null()])
});
```

Provider mapping:

| Provider | Native Input | Native Output | Map To |
|----------|--------------|---------------|--------|
| Slack | cursor | response_metadata.next_cursor | cursor -> next_cursor |
| Notion | start_cursor | next_cursor | cursor -> next_cursor |
| HubSpot | after | paging.next.after | cursor -> next_cursor |
| GitHub | page | Link header | cursor -> next_cursor |
| Google | pageToken | nextPageToken | cursor -> next_cursor |

Example:

```typescript
exec: async (nango, input): Promise<z.infer<typeof ListOutput>> => {
    const config: ProxyConfiguration = {
        endpoint: 'api/items',
        params: {
            ...(input.cursor && { cursor: input.cursor })
        },
        retries: 3
    };

    const response = await nango.get(config);

    return {
        items: response.data.items.map((item: { id: string; name: string }) => ({
            id: item.id,
            name: item.name
        })),
        next_cursor: response.data.next_cursor || null
    };
}
```

## OnEvent Template (createOnEvent)

Use on-event functions for connection lifecycle hooks:
- `validate-connection`: verify credentials/scopes on connection creation
- `post-connection-creation`: run setup after a connection is created
- `pre-connection-deletion`: cleanup before a connection is deleted

File location convention: `{integrationId}/on-events/<name>.ts` and import it from `index.ts`.

```typescript
import { createOnEvent } from 'nango';
import { z } from 'zod';

export default createOnEvent({
    description: 'Validate connection credentials',
    version: '1.0.0',
    event: 'validate-connection',
    metadata: z.void(),

    exec: async (nango) => {
        // https://api-docs-url
        await nango.get({ endpoint: '/me', retries: 3 });
    }
});
```

## Sync Template (createSync)

```typescript
import { createSync } from 'nango';
import { z } from 'zod';

const RecordSchema = z.object({
    id: z.string(),
    name: z.union([z.string(), z.null()])
});

const sync = createSync({
    description: 'Brief single sentence',
    version: '1.0.0',
    endpoints: [{ method: 'GET', path: '/provider/records', group: 'Records' }],
    frequency: 'every hour',
    autoStart: true,
    syncType: 'full',

    models: {
        Record: RecordSchema
    },

    exec: async (nango) => {
        // Sync logic here
    }
});

export type NangoSyncLocal = Parameters<(typeof sync)['exec']>[0];
export default sync;
```

### Sync Deletion Detection

- Do not use trackDeletes. It is deprecated.
- Full syncs: call deleteRecordsFromPreviousExecutions at the end of exec after all batchSave calls.
- Incremental syncs: if the API supports it, detect deletions and call batchDelete.

Important: deletion detection is a soft delete. Records remain in the cache but are marked as deleted in metadata.

Safety: only call deleteRecordsFromPreviousExecutions when the run successfully fetched the full dataset. Do not catch and swallow errors and still call it (false deletions).

Reference: https://nango.dev/docs/implementation-guides/use-cases/syncs/deletion-detection

```typescript
await nango.deleteRecordsFromPreviousExecutions('Record');
```

### Full Sync (Recommended)

```typescript
exec: async (nango) => {
    const proxyConfig = {
        // https://api-docs-url
        endpoint: 'api/v1/records',
        paginate: { limit: 100 },
        retries: 3
    };

    for await (const batch of nango.paginate(proxyConfig)) {
        const records = batch.map((r: { id: string; name: string }) => ({
            id: r.id,
            name: r.name ?? null
        }));

        if (records.length > 0) {
            await nango.batchSave(records, 'Record');
        }
    }

    await nango.deleteRecordsFromPreviousExecutions('Record');
}
```

### Incremental Sync

```typescript
const sync = createSync({
    syncType: 'incremental',
    frequency: 'every 5 minutes',

    exec: async (nango) => {
        const lastSync = nango.lastSyncDate;

        const proxyConfig = {
            // https://api-docs-url
            endpoint: '/api/records',
            params: {
                sort: 'updated',
                ...(lastSync && { since: lastSync.toISOString() })
            },
            paginate: { limit: 100 },
            retries: 3
        };

        for await (const batch of nango.paginate(proxyConfig)) {
            const records = batch.map((record: { id: string; name?: string }) => ({
                id: record.id,
                name: record.name ?? null
            }));
            await nango.batchSave(records, 'Record');
        }

        if (lastSync) {
            const deleted = await nango.get({
                // https://api-docs-url
                endpoint: '/api/records/deleted',
                params: { since: lastSync.toISOString() },
                retries: 3
            });
            if (deleted.data.length > 0) {
                await nango.batchDelete(
                    deleted.data.map((d: { id: string }) => ({ id: d.id })),
                    'Record'
                );
            }
        }
    }
});
```

### Sync Metadata (When Required)

```typescript
const MetadataSchema = z.object({
    team_id: z.string()
});

const sync = createSync({
    metadata: MetadataSchema,

    exec: async (nango) => {
        const metadata = await nango.getMetadata();
        const teamId = metadata?.team_id;

        if (!teamId) {
            throw new Error('team_id is required in metadata.');
        }

        const response = await nango.get({
            // https://api-docs-url
            endpoint: `/v1/teams/${teamId}/projects`,
            retries: 3
        });
    }
});
```

Note: nango.getMetadata() is cached for up to 60 seconds during a sync execution. Metadata updates may not be visible until the next run.

### Realtime Syncs (Webhooks)

Use webhookSubscriptions + onWebhook when the provider supports webhooks.

```typescript
const sync = createSync({
    webhookSubscriptions: ['contact.propertyChange'],

    exec: async (nango) => {
        // Optional periodic polling
    },

    onWebhook: async (nango, payload) => {
        if (payload.subscriptionType === 'contact.propertyChange') {
            const updated = {
                id: payload.objectId,
                [payload.propertyName]: payload.propertyValue
            };
            await nango.batchSave([updated], 'Contact');
        }
    }
});
```

Optional merge strategy:

```typescript
await nango.setMergingStrategy({ strategy: 'ignore_if_modified_after' }, 'Contact');
```

### Key SDK Methods (Sync)

| Method | Purpose |
|--------|---------|
| nango.paginate(config) | Iterate through paginated responses |
| nango.batchSave(records, model) | Save records to cache |
| nango.batchDelete(records, model) | Mark as deleted (incremental) |
| nango.deleteRecordsFromPreviousExecutions(model) | Auto-detect deletions (full) |
| nango.lastSyncDate | Last sync timestamp (incremental) |

### Pagination Helper (Advanced Config)

Nango preconfigures pagination for some APIs. Override when needed.

Pagination types: cursor, link, offset.

```typescript
const proxyConfig = {
    endpoint: '/tickets',
    paginate: {
        type: 'cursor',
        cursor_path_in_response: 'next',
        cursor_name_in_request: 'cursor',
        response_path: 'tickets',
        limit_name_in_request: 'limit',
        limit: 100
    },
    retries: 3
};

for await (const page of nango.paginate(proxyConfig)) {
    await nango.batchSave(page, 'Ticket');
}
```

Link pagination uses link_rel_in_response_header or link_path_in_response_body. Offset pagination uses offset_name_in_request.

### Manual Cursor-Based Pagination (If Needed)

```typescript
let cursor: string | undefined;
while (true) {
    const res = await nango.get({
        endpoint: '/api',
        params: { cursor },
        retries: 3
    });
    const records = res.data.items.map((item: { id: string; name?: string }) => ({
        id: item.id,
        name: item.name ?? null
    }));
    await nango.batchSave(records, 'Record');
    cursor = res.data.next_cursor;
    if (!cursor) break;
}
```

## Dryrun Command Reference

Basic syntax (action or sync):

```
nango dryrun <script-name> <connection-id>
```

Actions: pass input:

```
nango dryrun <action-name> <connection-id> --input '{"key":"value"}'

# For actions with input: z.object({})
nango dryrun <action-name> <connection-id> --input '{}'
```

Stub metadata (when your function calls nango.getMetadata()):

```
nango dryrun <script-name> <connection-id> --metadata '{"team_id":"123"}'
nango dryrun <script-name> <connection-id> --metadata @fixtures/metadata.json
```

Save mocks for tests (implies validation; only saves if validation passes):

```
nango dryrun <script-name> <connection-id> --save
```

Notes:
- Connection ID is the second positional argument (no `--connection-id` flag).
- Use `--integration-id <integration-id>` when script names overlap across integrations.
- Common flags: `--validate`, `-e/--environment dev|prod`, `--no-interactive`, `--auto-confirm`, `--lastSyncDate "YYYY-MM-DD"`, `--variant <name>`.
- If you do not have `nango` on PATH, use `npx nango ...`.
- In CI/non-interactive runs always pass `-e dev|prod` (otherwise the CLI prompts for environment selection).
- CLI upgrade prompts can block non-interactive runs. Workaround: set `NANGO_CLI_UPGRADE_MODE=ignore`.

Common mistakes:
- Using `--connection-id` (does not exist)
- Using legacy flags like `--save-responses` or `-m` (use `--save` and `--metadata`)
- Putting integration ID as the second argument (it will be interpreted as connection ID)

## Testing and Validation Workflow

Recommended loop while coding:
1. Implement the function file under `{integrationId}/actions/` or `{integrationId}/syncs/`.
2. Register it via side-effect import in `index.ts`.
3. Dryrun with `nango dryrun ... --validate` until it passes.

Dryrun + validate:
- Action: `nango dryrun <action-name> <connection-id> --input '{...}' --validate`
- Sync: `nango dryrun <sync-name> <connection-id> --validate`
- Incremental sync testing: add `--lastSyncDate "YYYY-MM-DD"`

Record mocks + generate tests:
1. `nango dryrun <script-name> <connection-id> --save` (add `--input` for actions; add `--metadata` if the script reads metadata)
2. `nango generate:tests` (or narrow: `-i <integrationId>`, `-s <sync-name>`, `-a <action-name>`)
3. Run tests via `npm test` (Vitest) or `npx vitest run`

Reference: https://nango.dev/docs/implementation-guides/platform/functions/testing

## Mocks and Test Files (Current Format)

```
{integrationId}/tests/
|-- <script-name>.test.ts
`-- <script-name>.test.json
```

The `.test.json` file is generated by `nango dryrun ... --save` and contains the recorded API mocks + expected input/output.

## Deploy (Optional)

Deploy functions to an environment in your Nango account:

```
nango deploy dev

# Deploy only one function
nango deploy --action <action-name> dev
nango deploy --sync <sync-name> dev
```

Reference: https://nango.dev/docs/implementation-guides/use-cases/actions/implement-an-action

## When API Docs Do Not Render

If web fetching returns incomplete docs (JS-rendered):
- Ask the user for a sample response
- Use existing actions/syncs in the repo as a pattern
- Run dryrun with `--save` and build from the captured response

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing/incorrect index.ts import | Function not loaded | Add side-effect import (`import './<path>.js'`) |
| Using legacy dryrun flags (`--save-responses`, `-m`) | Dryrun/mocks fail | Use `--save` and `--metadata` |
| Calling deleteRecordsFromPreviousExecutions after partial fetch | False deletions | Let failures fail; only call after full successful save |
| trackDeletes: true | Deprecated | Use deleteRecordsFromPreviousExecutions (full) or batchDelete (incremental) |
| Retrying non-idempotent writes blindly | Duplicate side effects | Avoid retries or use provider idempotency keys |
| Using any in mapping | Loses type safety | Use inline types |
| Using --connection-id | Dryrun fails | Use positional connection id |

## Final Checklists

Action:
- [ ] Nango root verified
- [ ] Schemas + types are clear (inline or relative imports)
- [ ] createAction with endpoint/input/output/scopes
- [ ] Proxy config includes API doc link and intentional retries
- [ ] `nango.ActionError` used for expected failures
- [ ] Registered in index.ts
- [ ] Dryrun succeeds with --validate
- [ ] Mocks recorded with --save (if adding tests)
- [ ] Tests generated and npm test passes

Sync:
- [ ] Nango root verified
- [ ] Models map defined; record ids are strings
- [ ] createSync with endpoints/frequency/syncType
- [ ] paginate + batchSave in exec
- [ ] deleteRecordsFromPreviousExecutions at end for full sync
- [ ] Metadata handled if required
- [ ] Registered in index.ts
- [ ] Dryrun succeeds with --validate
- [ ] Mocks recorded with --save (if adding tests)
- [ ] Tests generated and npm test passes

OnEvent:
- [ ] Nango root verified
- [ ] createOnEvent with event + exec
- [ ] Registered in index.ts
- [ ] Deployed and verified by triggering the lifecycle event
