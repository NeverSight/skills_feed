---
name: notis-query
description: Use when agents need to query native Notis databases with direct structured filters, sorts, and pagination through `LOCAL_NOTIS_DATABASE_QUERY`.
feature_flag: store
mcp_resource: true
mcp_tool_patterns: ["LOCAL_NOTIS_DATABASE_*"]
mcp_references: ["references/database-discovery.md", "references/documents.md", "references/query.md"]
---

# Notis Query Skill

Use this skill when the user wants to search, filter, sort, or page through records in a native Notis database and the task is best handled with structured criteria instead of semantic search.

This skill is the single source of truth for `LOCAL_NOTIS_DATABASE_QUERY`.

## Canonical contract source

For custom view runtime usage, the canonical contract is always MCP `tools/list` `inputSchema` for `LOCAL_NOTIS_DATABASE_QUERY`.

- Use `notisView.listTools()` (or MCP `tools/list`) to read the live schema.
- Use `notisView.callTool("LOCAL_NOTIS_DATABASE_QUERY", args)` (or MCP `tools/call`) with arguments that match that schema exactly.
- If this skill text and `inputSchema` ever differ, follow `inputSchema`.

This keeps query arguments aligned with the same tool definitions used by agent runtime and avoids maintaining duplicate schema formats.

## When to use `LOCAL_NOTIS_DATABASE_QUERY`

Use `LOCAL_NOTIS_DATABASE_QUERY` when:

- you already know the target native database
- the user wants structured filtering or sorting
- you need predictable pagination over database rows
- you need to find records before reading or updating a specific document
- you need to find matching records before calling `LOCAL_NOTIS_DATABASE_GET_DOCUMENT` or a generated database upsert tool
- the task should use direct database criteria instead of semantic memory search

Do not use `LOCAL_NOTIS_DATABASE_QUERY` when:

- the relevant database is unknown
- semantic search over broad workspace context is better
- the task points to one known document by `document_id` or portal URL

Use these tools together:

- `LOCAL_NOTIS_DATABASE_LIST_DATABASES` to discover available databases and confirm the slug
- `LOCAL_NOTIS_DATABASE_GET_DATABASE` to inspect read-only schema detail, ordered properties, options, and relation targets
- `LOCAL_NOTIS_DATABASE_QUERY` to find matching records
- `LOCAL_NOTIS_DATABASE_GET_DOCUMENT` to inspect one specific matching document in full
- generated database upsert tools to update or create records after you know the right document or relation IDs

Follow the same workflow and use the exact canonical tool names available in the current runtime.

Every database has one owning app; inspect its identity/schema before schema writes.
Known document IDs/URLs use the document guide, not a broad query. For queries,
use the query guide for exact filter/property/pagination rules; live inputSchema
is authoritative. Dry-run writes and read back the resulting state.

## Task guides

Read only the guide needed for this task. Relative links resolve in the skill bundle.
For hosted MCP, fetch the matching `notis://docs/notis-query/references/<file>.md` URI
with resources/read or the available Notis resource-fetch tool; the root resource
also rewrites these links to their published URIs.

- [Native Database Workflow](references/database-discovery.md)
- [Reading documents](references/documents.md)
- [Supported execution mode](references/query.md)
