---
name: msgraph
description: Up-to-date Microsoft Graph API knowledge for AI agents. Instantly search 27,700 Graph APIs and curated community samples — all locally, no network calls needed. Bridges the gap between LLM training cutoffs and the weekly-updated Microsoft Graph API. Works alongside Graph MCP servers (like lokka.dev) for execution, or authenticates and calls the Microsoft Graph API directly when needed.
license: MIT
compatibility: Search tools run fully offline with no network access required. Direct API execution requires network access to login.microsoftonline.com and graph.microsoft.com. A system browser is used for interactive auth; falls back to device code flow in headless environments.
metadata:
  author: merill
  version: "1.0.16"
---

# Microsoft Graph Agent Skill

Up-to-date Microsoft Graph API knowledge for AI agents — bridging the gap between LLM training cutoffs and the latest API.

## The Problem

The Microsoft Graph API has **27,700 Graph APIs** and is **updated weekly**. LLM training data is months — sometimes over a year — old. Without current API knowledge, agents hallucinate endpoints that don't exist, use deprecated paths, miss required permissions, or get the `$filter` syntax wrong.

This skill solves that. It bundles the complete Microsoft Graph API surface as local indexes that the agent can search instantly — no network calls, no latency. Every search runs locally against pre-built indexes that are updated with each skill release.

**What's included:**

| Index | Count | What it contains |
|---|---|---|
| OpenAPI endpoints | 27,700+ | Path, method, summary, description, permission scopes |
| Endpoint docs | 6,200+ | Permissions (delegated/app), query parameters, required headers, default vs `$select`-only properties |
| Resource schemas | 4,200+ | All properties with types, supported `$filter` operators, default/select-only flags |
| Community samples | Growing | Hand-verified queries mapping natural-language tasks to exact API calls |

## How to Run

The `msgraph` CLI is bundled with this skill. Run all commands through the launcher script in this skill's directory:

- **macOS / Linux**: `bash <path-to-this-skill>/scripts/run.sh <command> [args...]`
- **Windows**: `powershell <path-to-this-skill>/scripts/run.ps1 <command> [args...]`

In all examples below, `msgraph` is shorthand for the full launcher invocation.

## Finding the Right API

This is the primary purpose of the skill. Follow this progressive lookup strategy — each level adds detail:

1. **Your own knowledge** — try first for well-known endpoints (`/me`, `/users`, `/groups`).
2. **`sample-search`** — curated, hand-verified samples. Highest quality. Use for common tasks and multi-step workflows.
3. **`api-docs-search`** — per-endpoint permissions, supported query parameters, required headers, default vs `$select`-only properties, and resource property details with filter operators.
4. **`openapi-search`** — full catalog of 27,700 Graph APIs. Use when you cannot find the endpoint any other way.
5. **Reference files** — concept docs on query parameters, advanced queries, paging, batching, throttling, errors, and best practices. Read only when you need specific guidance.

This order is guidance — adapt based on the task. For example, jump straight to `api-docs-search` if you already know the endpoint but need its permissions.

### sample-search

Search curated community samples that map natural-language tasks to exact Microsoft Graph API queries:

```
msgraph sample-search --query "conditional access policies"
msgraph sample-search --product entra
msgraph sample-search --query "managed devices" --product intune
```

| Flag | Description |
|---|---|
| `--query` | Free-text search (searches intent and query fields) |
| `--product` | Filter by product: `entra`, `intune`, `exchange`, `teams`, `sharepoint`, `security`, `general` |
| `--limit` | Max results (default 10) |

At least one of `--query` or `--product` is required. Results include multi-step workflows.

### api-docs-search

Look up detailed documentation for a specific endpoint or resource type:

```
msgraph api-docs-search --endpoint /users --method GET
msgraph api-docs-search --resource user
msgraph api-docs-search --query "ConsistencyLevel"
```

| Flag | Description |
|---|---|
| `--endpoint` | Search by endpoint path (e.g. `/users`, `/me/messages`) |
| `--resource` | Search by resource type name (e.g. `user`, `group`, `message`) |
| `--method` | Filter by HTTP method: `GET`, `POST`, `PUT`, `PATCH` |
| `--query` | Free-text search across all fields |
| `--limit` | Max results (default 10) |

At least one of `--endpoint`, `--resource`, or `--query` is required.

**Endpoint results** include: required permissions (delegated work/school, delegated personal, application), supported OData query parameters, required headers, default properties, and endpoint-specific notes.

**Resource results** include: all properties with types, supported `$filter` operators (eq, ne, startsWith, etc.), and whether each property is returned by default or requires `$select`.

### openapi-search

Search the full OpenAPI catalog of 27,700 Microsoft Graph APIs:

```
msgraph openapi-search --query "send mail"
msgraph openapi-search --resource messages --method GET
```

| Flag | Description |
|---|---|
| `--query` | Free-text search (searches path, summary, description) |
| `--resource` | Filter by resource name (e.g. `users`, `groups`, `messages`) |
| `--method` | Filter by HTTP method |
| `--limit` | Max results (default 20) |

At least one of `--query`, `--resource`, or `--method` is required.

## Using with MCP Servers

If the agent has access to a Microsoft Graph MCP server (such as [lokka.dev](https://lokka.dev) or any other Graph MCP server), use the search tools above to find the right endpoint, permissions, and request syntax, then pass the information to the MCP server for execution.

In this mode, **no authentication through this skill is needed**. The skill acts purely as a knowledge layer — the MCP server handles authentication and API execution.

## Direct Microsoft Graph API Execution

When no Graph MCP server is available, this skill can authenticate to Microsoft 365 and execute Microsoft Graph API calls directly.

### Authentication

The tool supports **delegated (user)** and **app-only (application)** authentication, auto-detected from environment variables.

**Quick start:**

```
msgraph auth status          # check if signed in
msgraph auth signin          # sign in (opens browser)
msgraph auth signin --device-code  # sign in via device code (headless)
msgraph auth signout         # clear the session
```

- **Delegated auth** (default): Interactive browser sign-in, with device code fallback for headless environments. Supports incremental consent — on 403, the tool re-authenticates with required scopes and retries automatically.
- **App-only auth**: Auto-detected when `MSGRAPH_CLIENT_SECRET`, `MSGRAPH_CLIENT_CERTIFICATE_PATH`, `MSGRAPH_FEDERATED_TOKEN_FILE`, or `MSGRAPH_AUTH_METHOD=managed-identity` is set. Requires `MSGRAPH_TENANT_ID`.

For detailed authentication configuration including certificates, managed identity, workload identity federation, and all environment variables, see [references/docs/authentication.md](references/docs/authentication.md).

### Making Graph API Calls

**IMPORTANT**: Run `msgraph auth status` before the first `graph-call` in a session to verify authentication.

```
msgraph graph-call <METHOD> <URL> [flags]
```

#### Read Operations

```
msgraph graph-call GET /me
msgraph graph-call GET /users --select "displayName,mail" --top 10
msgraph graph-call GET /me/messages --filter "isRead eq false" --top 5 --select "subject,from,receivedDateTime"
msgraph graph-call GET /users --filter "startsWith(displayName,'John')"
```

#### Write Operations

**IMPORTANT**: YOU MUST ask the user for confirmation before any write operation. Write operations require the `--allow-writes` flag.

```
msgraph graph-call POST /me/sendMail --body '{"message":{"subject":"Hello","body":{"content":"Hi"},"toRecipients":[{"emailAddress":{"address":"user@example.com"}}]}}' --allow-writes
msgraph graph-call PATCH /me --body '{"jobTitle":"Engineer"}' --allow-writes
```

**DELETE is always blocked** regardless of flags.

#### graph-call Flags

| Flag | Description | Example |
|---|---|---|
| `--select` | OData $select | `--select "displayName,mail"` |
| `--filter` | OData $filter | `--filter "isRead eq false"` |
| `--top` | OData $top (limit results) | `--top 10` |
| `--expand` | OData $expand | `--expand "members"` |
| `--orderby` | OData $orderby | `--orderby "displayName desc"` |
| `--api-version` | `v1.0` or `beta` (default: beta) | `--api-version v1.0` |
| `--scopes` | Request additional permission scopes | `--scopes "Mail.Read"` |
| `--headers` | Custom HTTP headers | `--headers "ConsistencyLevel:eventual"` |
| `--body` | Request body (JSON) | `--body '{"key":"value"}'` |
| `--output` | `json` (default) or `raw` | `--output raw` |
| `--allow-writes` | Allow POST/PUT/PATCH (requires user confirmation) | |

## Critical Rules

### Always (search and knowledge)

1. **Use the progressive lookup strategy** — start with what you know, then sample-search, api-docs-search, openapi-search as needed.
2. **Use `--select`** to reduce response size — only request fields you need.
3. **Use `--top`** to limit results — avoid fetching thousands of records.
4. **ConsistencyLevel header** is required for `$count` and `$search` on directory objects (users, groups, etc.). Use `--headers "ConsistencyLevel:eventual"`.
5. **Default API version is beta** — use `--api-version v1.0` for production-stable endpoints.

### When using direct execution (graph-call)

6. **Check auth status** before the first `graph-call` in a session.
7. **GET is the default** — no special flags needed.
8. **Write operations require `--allow-writes`** — YOU MUST confirm with the user first.
9. **DELETE is always blocked** — inform the user this is not supported.
10. **403 triggers automatic re-auth** — the tool requests additional scopes and retries (delegated auth only).
11. **All output is JSON** — parse `statusCode` and `body` fields from the response.

## Error Handling

| Status | Meaning | Action |
|---|---|---|
| 401 | Token expired | Run `msgraph auth signin` again |
| 403 | Insufficient permissions | Tool auto-retries with incremental consent. If still fails, user needs admin consent. |
| 404 | Resource not found | Verify the endpoint path |
| 429 | Rate limited | Wait for Retry-After duration, then retry |

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `MSGRAPH_CLIENT_ID` | Custom Entra ID app client ID | Microsoft Graph CLI Tools app |
| `MSGRAPH_TENANT_ID` | Target tenant ID (required for app-only) | `common` |
| `MSGRAPH_API_VERSION` | Default API version | `beta` |
| `MSGRAPH_INDEX_PATH` | Path to OpenAPI index JSON | Auto-detected |
| `MSGRAPH_SAMPLES_PATH` | Path to samples index JSON | Auto-detected |
| `MSGRAPH_API_DOCS_PATH` | Path to API docs index JSON | Auto-detected |
| `MSGRAPH_NO_TOKEN_CACHE` | Disable persistent token cache (in-memory only) | `false` |

For the full list of authentication environment variables, see [references/docs/authentication.md](references/docs/authentication.md).

## Reference Files

Load these on demand when you need specific guidance. Do NOT load them preemptively.

| File | When to Read | Size |
|---|---|---|
| [references/REFERENCE.md](references/REFERENCE.md) | Common resource paths, OData patterns, permission scopes | Quick reference |
| [references/docs/authentication.md](references/docs/authentication.md) | Detailed auth configuration: certificates, managed identity, workload identity, all env vars | Concept doc |
| [references/docs/query-parameters.md](references/docs/query-parameters.md) | OData $select, $filter, $expand, $top, $orderby, $search syntax and gotchas | Concept doc |
| [references/docs/advanced-queries.md](references/docs/advanced-queries.md) | ConsistencyLevel header, $count, $search, ne/not/endsWith on directory objects | Concept doc |
| [references/docs/paging.md](references/docs/paging.md) | @odata.nextLink pagination, server-side vs client-side paging | Concept doc |
| [references/docs/batching.md](references/docs/batching.md) | $batch endpoint, combining multiple requests, dependsOn sequencing | Concept doc |
| [references/docs/throttling.md](references/docs/throttling.md) | 429 handling, Retry-After, backoff strategy | Concept doc |
| [references/docs/errors.md](references/docs/errors.md) | HTTP status codes, error response format, error codes | Concept doc |
| [references/docs/best-practices.md](references/docs/best-practices.md) | $select for performance, pagination, delta queries, batching | Concept doc |
