---
name: paperless-ngx
description: Manages documents in Paperless-ngx via MCP tools. Searches, uploads, tags, organizes, and bulk-edits documents, correspondents, and document types. Use when working with Paperless-ngx, document management, OCR, or any mcp_paperless_* tool task.
license: MIT
compatibility: Requires a running Paperless-ngx instance with API token. MCP server must be connected with mcp_paperless_* tools available.
metadata:
  author: kjanat
  version: "2.0.1"
---

# Paperless-ngx Document Management

Orchestrate Paperless-ngx through 16 MCP tools across 4 domains.

## Tool Catalog

### Documents (5 tools)

| Tool                  | Operation        | Key Params                            |
| --------------------- | ---------------- | ------------------------------------- |
| `search_documents`    | Full-text search | `query`, `page`, `page_size`          |
| `get_document`        | Full details     | `id`                                  |
| `post_document`       | Upload file      | `file` (base64), `filename`, metadata |
| `download_document`   | Get file base64  | `id`, `original` (bool)               |
| `bulk_edit_documents` | Batch operations | `documents` (IDs), `method`, params   |

### Tags (5 tools)

| Tool             | Operation                    |
| ---------------- | ---------------------------- |
| `list_tags`      | All tags + colors + matching |
| `create_tag`     | New tag, optional auto-match |
| `update_tag`     | Modify name/color/matching   |
| `delete_tag`     | Remove permanently           |
| `bulk_edit_tags` | Batch permissions/deletion   |

### Correspondents (3 tools)

| Tool                       | Operation                |
| -------------------------- | ------------------------ |
| `list_correspondents`      | All correspondents       |
| `create_correspondent`     | New, optional auto-match |
| `bulk_edit_correspondents` | Batch permissions/delete |

### Document Types (3 tools)

| Tool                       | Operation                |
| -------------------------- | ------------------------ |
| `list_document_types`      | All document types       |
| `create_document_type`     | New, optional auto-match |
| `bulk_edit_document_types` | Batch permissions/delete |

## Decision Trees

### Find a Document

```txt
What do you know?
├─ Keywords/content     → search_documents(query="term1 term2")
├─ Document ID          → get_document(id=N)
├─ By tag               → search_documents(query="tag:tagname")
├─ By type              → search_documents(query="type:typename")
├─ By correspondent     → search_documents(query="correspondent:name")
├─ By date              → search_documents(query="created:[2024 to 2025]")
└─ Combined             → search_documents(query="tag:X correspondent:Y created:[2024 to 2025]")
```

### Organize Documents

```txt
What operation?
├─ Add tag         → bulk_edit_documents(method="add_tag", tag=ID)
├─ Remove tag      → bulk_edit_documents(method="remove_tag", tag=ID)
├─ Multi-tag       → bulk_edit_documents(method="modify_tags", add_tags=[...], remove_tags=[...])
├─ Set type        → bulk_edit_documents(method="set_document_type", document_type=ID)
├─ Set sender      → bulk_edit_documents(method="set_correspondent", correspondent=ID)
├─ Merge PDFs      → bulk_edit_documents(method="merge", metadata_document_id=ID)
├─ Rotate pages    → bulk_edit_documents(method="rotate", degrees=90|180|270)
├─ Delete pages    → bulk_edit_documents(method="delete_pages", pages="1,3,5-7")
├─ Reprocess OCR   → bulk_edit_documents(method="reprocess")
└─ Delete          → bulk_edit_documents(method="delete")  !! PERMANENT !!
```

### Upload a Document

```txt
1. Resolve metadata IDs first:
   ├─ list_tags            → find or create_tag
   ├─ list_correspondents  → find or create_correspondent
   └─ list_document_types  → find or create_document_type
2. post_document(file=<base64>, filename="name.pdf", tags=[...], correspondent=ID, ...)
```

### Manage Taxonomy (Tags/Correspondents/Types)

```txt
Need to change metadata objects?
├─ View all          → list_tags / list_correspondents / list_document_types
├─ Create new        → create_tag / create_correspondent / create_document_type
├─ Edit tag          → update_tag(id, name, color, match, matching_algorithm)
├─ Delete one tag    → delete_tag(id)
├─ Batch delete/perm → bulk_edit_tags / bulk_edit_correspondents / bulk_edit_document_types
```

## Critical Notes

- **search_documents strips `content`** to save tokens. Use `get_document` for
  full OCR text.
- **post_document requires base64** file content, not file paths.
- **matching_algorithm** is integer `0-6` across all endpoints (tags,
  correspondents, document types): `0`=none, `1`=any, `2`=all, `3`=exact,
  `4`=regex, `5`=fuzzy, `6`=auto. See [tools.md](references/tools.md).
- **Bulk delete is permanent and irreversible.**
- **download_document** returns base64 blob + filename from content-disposition.

## References

| Task                    | File                                          |
| ----------------------- | --------------------------------------------- |
| Tool parameters & types | [tools.md](references/tools.md)               |
| Search query syntax     | [query-syntax.md](references/query-syntax.md) |
| Multi-step workflows    | [workflows.md](references/workflows.md)       |
