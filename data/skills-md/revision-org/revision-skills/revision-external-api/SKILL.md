---
name: revision-external-api
description: Manages architecture components, diagrams, attributes, tags, and templates via the Revision External API. Triggers when Revision API, architecture components, C4 diagrams, or syncing architecture data with Revision are mentioned.
---

# Revision External API

REST API for managing architecture documentation in Revision workspaces.

## Prerequisites

Before making any API calls, the user must provide two things:

1. **Organization URL**: Each organization has its own subdomain, e.g. `https://acme-company.revision.app/`. This is the base URL for all API requests. **Always ask the user for their organization URL** — there is no default.
2. **API key**: A Bearer token from the workspace settings.

## Authentication

All requests require a Bearer token (API key from workspace settings):

```
Authorization: Bearer <api-key>
```

## Base URL

The base URL is the organization's own Revision URL. Every organization has a unique subdomain:

```
https://{organization}.revision.app
```

For example: `https://acme-company.revision.app`

**Important**: Do not use a generic URL. Always use the organization-specific subdomain provided by the user.

## Resources

| Resource | Endpoints | Description |
|----------|-----------|-------------|
| Components | CRUD + batch upsert | Architecture components (services, databases, etc.) |
| Diagrams | CRUD + batch upsert | Architecture diagrams with component instances, relations, textareas |
| Attributes | CRUD + batch upsert | Custom attribute definitions on components |
| Tags | CRUD + batch upsert | Tags for categorizing diagrams |
| Types | Read-only | Component type definitions |
| Template | POST | Bulk sync of components + diagrams in a single transaction |
| Search | GET | Search components, diagrams, and dependencies |

## Quick Start

### List components

```bash
curl -H "Authorization: Bearer $API_KEY" \
  https://acme-company.revision.app/api/external/components
```

### Create a component

```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "User Service", "state": "ACTIVE"}' \
  https://acme-company.revision.app/api/external/components
```

### Create a component with a predictable ID

```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "user-service", "name": "User Service", "state": "ACTIVE"}' \
  https://acme-company.revision.app/api/external/components
```

### Update a component

```bash
curl -X PATCH -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "User Service", "state": "ACTIVE", "desc": "Handles user auth"}' \
  https://acme-company.revision.app/api/external/components/component-id
```

## Standard CRUD Pattern

Every resource (components, diagrams, attributes, tags) follows the same pattern:

| Method | Path | Action |
|--------|------|--------|
| GET | `/api/external/{resource}` | List all |
| POST | `/api/external/{resource}` | Create (single item) |
| GET | `/api/external/{resource}/{id}` | Get by ID |
| PATCH | `/api/external/{resource}/{id}` | Update by ID |
| PATCH | `/api/external/{resource}/upsert-batch` | Batch upsert (items with `id` are updated, without are created) |

**Note**: DELETE endpoints exist but are **not yet implemented** (return 501).

**ID behavior**: If you provide an `id` when creating, that exact ID is used (predictable). If you omit `id`, one is auto-generated. Providing a predictable `id` is useful when you need to reference the resource elsewhere (e.g. a component's `id` in a component instance's `componentId`).

**Create requests** accept a single object (not an array). Returns 201 on success.

**Batch upsert** is the most powerful pattern: send items with `id` to update, without `id` to create, all in one request.

## Component Schema

```json
{
  "id": "string",
  "name": "string",
  "state": "DRAFT | ACTIVE | ARCHIVED",
  "ref": "string | null",
  "desc": "string | null",
  "inlineDesc": false,
  "typeId": "string | null",
  "apiContext": "string",
  "attributes": [{ "id": "string", "value": "boolean | number | string | null" }],
  "linksTo": ["diagram-id-1", "diagram-id-2"]
}
```

- `id`: Optional on create — provide it for a predictable ID, omit for auto-generated
- `ref`: External reference identifier
- `apiContext`: Opaque string for API-managed metadata
- `linksTo`: Array of diagram IDs this component links to
- `attributes`: Component attribute values (reference attribute definitions by `id`)

## Diagram Schema

```json
{
  "id": "string",
  "name": "string",
  "state": "DRAFT | ACTIVE | ARCHIVED",
  "url": "string",
  "desc": "string | null",
  "level": "C0 | C1 | C2 | C3 | C4 | D1 | P0 | null",
  "tags": ["tag-id-1"],
  "apiContext": "string",
  "componentInstances": [],
  "relations": [],
  "textareas": []
}
```

### Diagram Levels

| Level | Meaning |
|-------|---------|
| C0 | Landscape |
| C1 | System Context |
| C2 | Container |
| C3 | Component |
| C4 | Code |
| D1 | Deployment |
| P0 | Process |

### Component Instances

A **component** is part of the architecture model — a reusable entity that can be referenced across many diagrams. A **component instance** is a visual placeholder on a diagram. It can optionally link to a component via `componentId`, but it doesn't have to — unlinked instances are just standalone placeholders with a name and type.

Two types:

**Important**: `position`, `width`, and `height` are all optional. When omitted, Revision will automatically lay out and size the instances. **Prefer omitting them** unless the user explicitly asks for specific positioning or sizing — auto-layout produces better results.

**Non-container** (default):
```json
{
  "ref": "unique-ref",
  "componentId": "component-id | null",
  "parent": "container-ref",
  "isContainer": false,
  "placeholder": { "text": "Name", "typeId": "type-id" }
}
```

**Container** (groups other instances):
```json
{
  "ref": "unique-ref",
  "componentId": "component-id | null",
  "isContainer": true,
  "placeholder": { "text": "Name", "typeId": "type-id" }
}
```

- `ref` is required and must be unique within the diagram
- `componentId` links the instance to a component definition (null for placeholders)
- Non-containers can reference a `parent` container via the container's `ref`
- Containers cannot have a parent
- `position`, `width`, `height` are optional — omit them to let Revision auto-layout and auto-size

### Relations

Directed edges between component instances:
```json
{
  "fromRef": "instance-ref-1",
  "toRef": "instance-ref-2",
  "label": "string | null",
  "desc": "string | null",
  "linksTo": ["diagram-id"]
}
```

### Textareas

Free text on diagrams:
```json
{
  "position": { "x": 100, "y": 100 },
  "width": 300,
  "text": "string | null"
}
```

## Attribute Schema

Custom fields on components:
```json
{
  "id": "string",
  "name": "string",
  "desc": "string | null",
  "type": "STRING | NUMBER | BOOLEAN | LINK | USERLIST | LIST",
  "list": ["option1", "option2"],
  "forTypes": ["type-id-1"],
  "required": false,
  "apiContext": "string"
}
```

- `list` is only valid when `type` is `LIST` (and required for LIST)
- `forTypes`: Restrict attribute to specific component types

## Tag Schema

```json
{
  "id": "string",
  "name": "string",
  "desc": "string | null",
  "color": "gray | red | orange | yellow | green | blue | purple",
  "apiContext": "string"
}
```

## Type Schema (Read-Only)

```json
{
  "id": "string",
  "name": "string"
}
```

Types are managed in the Revision UI. The API can only list them via `GET /api/external/types`.

## Template Sync

Bulk sync components and diagrams in a single transaction:

```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"components": [...], "diagrams": [...]}' \
  https://acme-company.revision.app/api/external/template
```

Accepts both JSON and YAML. Components and diagrams follow their standard schemas.

## Search

### Search Diagrams

```
GET /api/external/search/diagrams?componentId=...&tagId=...&name=...&level=...&state=...
```

At least one filter required.

### Search Components

```
GET /api/external/search/components?name=...&typeId=...&tagId=...&attributeId=...&attributeValue=...&state=...
```

At least one filter required. `attributeValue` requires `attributeId`.

### Search Dependencies

```
GET /api/external/search/dependencies?componentId=...
```

Returns upstream and downstream direct dependencies for a component.

## Workflow: Create a Diagram with Components

A typical end-to-end flow: search for duplicates, create components, then create a diagram that references them.

1. **Search for existing duplicates** — MUST do this before creating anything:
   - For each component you plan to create, search by name: `GET /api/external/search/components?name=<name>`
   - For the diagram, search by name: `GET /api/external/search/diagrams?name=<name>`
   - If matches are found → ask the user whether to **reuse the existing** resource or **create a new** one
   - If the user chooses to reuse → use the existing resource's `id` instead of creating a new one
   - If no matches → proceed to create
   - Skip ONLY when the user explicitly says "create a new..." or "update the existing..."

2. **List types** to find the right `typeId` values:
```bash
curl -H "Authorization: Bearer $API_KEY" \
  https://acme-company.revision.app/api/external/types
```

3. **Create components** (skip any that the user chose to reuse from step 1):
```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "user-service", "name": "User Service", "state": "ACTIVE"}' \
  https://acme-company.revision.app/api/external/components
```
```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "user-db", "name": "User Database", "state": "ACTIVE"}' \
  https://acme-company.revision.app/api/external/components
```

4. **Create a diagram** with component instances and a relation:
```bash
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Service Context",
    "level": "C2",
    "state": "ACTIVE",
    "componentInstances": [
      { "ref": "us", "componentId": "user-service" },
      { "ref": "udb", "componentId": "user-db" }
    ],
    "relations": [
      { "fromRef": "us", "toRef": "udb", "label": "Reads/writes" }
    ]
  }' \
  https://acme-company.revision.app/api/external/diagrams
```

5. **Verify** by fetching the diagram back:
```bash
curl -H "Authorization: Bearer $API_KEY" \
  https://acme-company.revision.app/api/external/diagrams/<returned-id>
```

For bulk operations, use the **template endpoint** to sync everything in a single transaction instead.

## Output Summary

After every mutation (create, update, batch upsert, or template sync), print a summary that clearly separates what was created from what was updated.

Format:

```
Created:
  - Component "User Service" (id: user-service)
  - Diagram "System Context" (id: system-context)

Updated:
  - Component "Auth Service" (id: auth-service) — updated name, desc
```

Rules:
- Use **Created** for POST (201) responses and batch upsert items that had no `id` provided
- Use **Updated** for PATCH (200) responses and batch upsert items that had an `id` provided
- Always include the resource type, name, and ID
- For updates, briefly note which fields changed
- Omit a section if it's empty (e.g. don't print "Updated:" if nothing was updated)

## Error Responses

All errors return:
```json
{ "error": "description" }
```

| Status | Meaning |
|--------|---------|
| 400 | Validation error |
| 401 | Missing or invalid API key |
| 404 | Resource not found |
| 405 | Method not allowed |
| 501 | Not implemented (e.g. DELETE endpoints) |

### Error Recovery

When an API call fails:

1. **401**: Confirm the API key is correct and the Authorization header uses `Bearer` prefix.
2. **400**: Read the `error` field — it describes the validation issue. Fix the request body and retry.
3. **404**: Verify the resource ID. Use the list endpoint (`GET /api/external/{resource}`) to confirm the resource exists.
4. **501**: DELETE is not implemented. Use PATCH to set `state: "ARCHIVED"` instead.

Always verify mutations by fetching the resource back after create/update to confirm the change took effect.

## Full OpenAPI Spec

For the complete OpenAPI 3.0.3 specification with all request/response schemas, see [OPENAPI.md](OPENAPI.md).
