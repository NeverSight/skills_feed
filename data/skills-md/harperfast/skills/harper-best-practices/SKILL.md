---
name: harper-best-practices
description: 
  Best practices for building Harper applications, covering schema definition,
  automatic APIs, authentication, custom resources, and data handling.
  Triggers on tasks involving Harper database design, API implementation,
  and deployment.
license: MIT
metadata:
  author: harper
  version: '1.0.0'
---

# Harper Best Practices

Guidelines for building scalable, secure, and performant applications on Harper. These practices cover everything from initial schema design to advanced deployment strategies.

## When to Use

Reference these guidelines when:

- Defining or modifying database schemas
- Implementing or extending REST/WebSocket APIs
- Handling authentication and session management
- Working with custom resources and extensions
- Optimizing data storage and retrieval (Blobs, Vector Indexing)
- Deploying applications to Harper Fabric

## Steps

1. Review the requirements for the task (schema design, API needs, or infrastructure setup).
2. Consult the relevant category under "Rule Categories by Priority" to understand the impact of your decisions.
3. Apply specific rules from the "Quick Reference" section below by reading their detailed rule files.
4. If you're building a new table, prioritize the `schema-` rules.
5. If you're extending functionality, consult the `logic-` and `api-` rules.
6. Validate your implementation against the `ops-` rules before deployment.

## Rule Categories by Priority

| Priority | Category                | Impact | Prefix          |
| -------- | ----------------------- | ------ | --------------- |
| 1        | Schema & Data Design    | HIGH   | `schema-`       |
| 2        | API & Communication     | HIGH   | `api-`          |
| 3        | Logic & Extension       | MEDIUM | `logic-`        |
| 4        | Infrastructure & Ops    | MEDIUM | `ops-`          |

## Quick Reference

### 1. Schema & Data Design (HIGH)

- `adding-tables-with-schemas` - Define tables using GraphQL schemas and directives
- `defining-relationships` - Link tables using the `@relationship` directive
- `vector-indexing` - Efficient similarity search with vector indexes
- `using-blob-datatype` - Store and retrieve large data (Blobs)
- `handling-binary-data` - Manage binary data like images or MP3s

### 2. API & Communication (HIGH)

- `automatic-apis` - Leverage automatically generated CRUD endpoints
- `querying-rest-apis` - Filters, sorting, and pagination in REST requests
- `real-time-apps` - WebSockets and Pub/Sub for live data updates
- `checking-authentication` - Secure apps with session-based identity verification

### 3. Logic & Extension (MEDIUM)

- `custom-resources` - Define custom REST endpoints using JS/TS
- `extending-tables` - Add custom logic to generated table resources
- `programmatic-table-requests` - Advanced filtering and sorting in code
- `typescript-type-stripping` - Use TypeScript without build tools
- `caching` - Implement and define caching for performance

### 4. Infrastructure & Ops (MEDIUM)

- `deploying-to-harper-fabric` - Scale globally with Harper Fabric
- `serving-web-content` - Ways to serve web content from Harper

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/adding-tables-with-schemas.md
rules/automatic-apis.md
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
