---
name: typesense
description: Search, index, and manage documents in Typesense collections. Use when the user mentions Typesense, asks about search indexing, needs help with search queries, collection schemas, or document import/export for Typesense.
---

# Typesense Skill

Schema management, document operations, search queries, and LLM-ready context generation for Typesense.

## Prerequisites

Set these environment variables (via `.env` or shell):

```bash
TYPESENSE_HOST=https://your-instance.typesense.net
TYPESENSE_API_KEY=your_admin_or_search_api_key
TYPESENSE_PORT=443        # optional, defaults to 443
TYPESENSE_PROTOCOL=https  # optional, defaults to https
```

Install dependencies:

```bash
cd scripts && npm install
```

## Primary Workflow: Natural Language to Typesense Query

**Step 1** -- Generate schema context for the target collections:

```bash
node scripts/generate_schema_context.js --collections products
```

This fetches collection schemas, identifies searchable/facetable/sortable fields, samples enum values via faceting, and formats output as a structured LLM prompt. Translated from the `generate_schema_prompt` function in `natural_language_search_model_manager.cpp`.

**Step 2** -- Use the generated context in a prompt:

```
Given this Typesense schema:
[paste generated context]

Convert this natural language query to Typesense search parameters:
"Show me laptops under $1000 from Apple or Dell, sorted by rating"
```

**Step 3** -- Execute the generated query:

```bash
node scripts/search.js products "laptop" \
  --filter "price:<1000 && brand:=[Apple,Dell]" \
  --sort "rating:desc"
```

## Core Operations

### Schema Introspection

```bash
# All collections
node scripts/generate_schema_context.js

# Specific collections with custom facet limit
node scripts/generate_schema_context.js \
  --collections products,articles \
  --max-facet-values 10

# Save to file
node scripts/generate_schema_context.js --output schema_context.txt
```

### Document Search

```bash
node scripts/search.js products "wireless headphones"
node scripts/search.js products "laptop" --filter "price:[500..2000]" --sort "rating:desc"
```

### Collection Management

```bash
# Create from schema file
node scripts/create_collection.js schema.json

# List collections
curl "${TYPESENSE_HOST}/collections" \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}"

# Delete collection
curl -X DELETE "${TYPESENSE_HOST}/collections/{collection}" \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}"
```

### Document Import

```bash
# Bulk import (JSONL, one JSON object per line)
./scripts/import_documents.sh products products.jsonl

# Single document
curl -X POST "${TYPESENSE_HOST}/collections/products/documents" \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"id":"prod-001","name":"Wireless Headphones","price":99.99}'
```

## Helper Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_schema_context.js` | LLM-friendly schema prompt | `node scripts/generate_schema_context.js` |
| `search.js` | Search with auto-detected fields | `node scripts/search.js <collection> <query>` |
| `create_collection.js` | Create collection from JSON | `node scripts/create_collection.js schema.json` |
| `import_documents.sh` | Bulk JSONL import | `./scripts/import_documents.sh <collection> <file>` |

## Debug Checklist

- Verify `TYPESENSE_HOST` includes protocol (`https://`)
- Confirm `TYPESENSE_API_KEY` has required permissions
- Check filter syntax (common: wrong operators, missing colons)
- Validate field names match schema exactly (case-sensitive)
- Ensure numeric fields use correct type (`float` vs `int32` vs `int64`)
- For import errors, validate JSONL format (one object per line, no trailing commas)

## Additional Resources

- For search parameters, filter syntax, field types, and best practices, see [api-reference.md](api-reference.md)
- For workflow examples (autocomplete, faceted search, semantic search, multi-tenant), see [examples.md](examples.md)
- Official docs: https://typesense.org/docs/
