---
name: seekdb-docs
description: Comprehensive SeekDB vector database documentation access. Use when answering questions about SeekDB development, Python SDK API usage, environment setup, coding standards, testing, debugging, or any SeekDB-related queries. Covers both developer guide (C++ core development) and user guide (Python SDK).
---

# SeekDB Documentation

Access comprehensive documentation for SeekDB vector database, including developer guides and Python SDK reference.

## Documentation Structure

### Developer Guide
Location: `seekdb-docs/developer-guide/{zh,en}/`

- **Environment Setup**: toolchain.md, build-and-run.md, ide-settings.md
- **Coding Standards**: coding-convention.md, coding-standard.md
- **Testing & Debugging**: unittest.md, mysqltest.md, debug.md
- **Core Systems**: memory.md, logging.md, container.md
- **Contributing**: contributing.md

### User Guide - Python SDK
Location: `seekdb-docs/user-guide/{zh,en}/pyseekdb-sdk.md`

Complete Python SDK API reference covering:
- Client objects (embedded/server/OceanBase modes)
- Collection management (create, get, delete)
- Data operations (add, update, upsert, delete)
- Query operations (query, get, hybrid_search)
- Filter conditions (where, where_document)
- Database management (AdminClient)
- Embedding functions

## Workflow

1. **Identify query type**:
   - Developer questions → Developer Guide
   - API/SDK questions → User Guide
   - Specific topics → Use doc index

2. **Locate documentation**:
   - Read `references/doc-index.md` for complete document index
   - All docs available in Chinese (zh/) and English (en/)

3. **Access relevant files**:
   - Read specific markdown files from seekdb-docs/ directory
   - Use grep to search across documentation if needed

## Quick Reference

For detailed document index with full content structure, see `references/doc-index.md`.
