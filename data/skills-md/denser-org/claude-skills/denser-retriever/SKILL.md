---
name: "denser-retriever"
description: "Build and search knowledge bases from documents using the Denser Retriever API. No-code RAG pipeline - upload PDFs, DOCX, PPTX, and other files, then search them with semantic search through natural conversation. Use this skill for: knowledge base creation, document upload, semantic search, document retrieval, PDF search, file indexing, RAG (retrieval-augmented generation), vector search, AI search, question answering over documents, text search API, document Q&A, knowledge management, and enterprise search. Trigger on: 'knowledge base', 'semantic search', 'document search', 'RAG', 'search my files', 'upload documents', 'PDF search', 'denser retriever', 'index documents', 'search knowledge base', 'document retrieval', 'vector search', or any request to search, query, or build a searchable collection of files."
---

# Denser Retriever API

Manage knowledge bases and perform semantic search over documents via the Denser Retriever REST API. All operations use `curl` commands.

## Setup

**API Key**: Read from `DENSER_API_KEY` environment variable. If not set, ask the user for their API key.

**Base URL**: `https://retriever.denser.ai/api/open/v1`

To check if the key is available:
```bash
echo $DENSER_API_KEY
```

If empty, ask the user: "Please provide your Denser Retriever API key (from your organization settings)."

## Quick Reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get usage | GET | `/v1/getUsage` |
| Get balance | GET | `/v1/getBalance` |
| Create KB | POST | `/v1/createKnowledgeBase` |
| List KBs | GET | `/v1/listKnowledgeBases` |
| Update KB | POST | `/v1/updateKnowledgeBase` |
| Delete KB | POST | `/v1/deleteKnowledgeBase` |
| Upload file (presign) | POST | `/v1/presignUploadUrl` |
| Import file | POST | `/v1/importFile` |
| Import text | POST | `/v1/importTextContent` |
| List documents | GET | `/v1/listDocuments` |
| Delete document | POST | `/v1/deleteDocument` |
| Check doc status | GET | `/v1/getDocumentStatus` |
| Search/query | POST | `/v1/query` |

For full request/response schemas, read `references/api_reference.md`.

## Common Workflows

### 1. Build a Knowledge Base from Files

This is a multi-step process: create KB, upload each file, wait for processing, then search.

**Step 1: Create a knowledge base**
```bash
curl -s -X POST "https://retriever.denser.ai/api/open/v1/createKnowledgeBase" \
  -H "x-api-key: $DENSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My KB", "description": "Optional description"}' | python3 -m json.tool
```

Save the returned `id` for subsequent operations.

**Step 2: For each file, do a 3-step upload**

a) Get a presigned upload URL:
```bash
curl -s -X POST "https://retriever.denser.ai/api/open/v1/presignUploadUrl" \
  -H "x-api-key: $DENSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledgeBaseId": "KB_ID", "fileName": "document.pdf", "size": FILE_SIZE_BYTES}' | python3 -m json.tool
```

b) Upload the file to the presigned URL (raw bytes, PUT request):
```bash
curl -s -X PUT "PRESIGNED_UPLOAD_URL" --data-binary @/path/to/document.pdf
```

c) Trigger import processing:
```bash
curl -s -X POST "https://retriever.denser.ai/api/open/v1/importFile" \
  -H "x-api-key: $DENSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fileId": "FILE_ID"}' | python3 -m json.tool
```

**Step 3: Poll until processed**
```bash
curl -s -X GET "https://retriever.denser.ai/api/open/v1/getDocumentStatus?documentId=DOC_ID" \
  -H "x-api-key: $DENSER_API_KEY" | python3 -m json.tool
```

Repeat every 2-3 seconds until `status` is `"processed"`. If `"failed"` or `"timeout"`, report the error.

**Step 4: Search**
```bash
curl -s -X POST "https://retriever.denser.ai/api/open/v1/query" \
  -H "x-api-key: $DENSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query", "knowledgeBaseIds": ["KB_ID"], "limit": 10}' | python3 -m json.tool
```

### 2. Import Text Content Directly

For plain text that doesn't need file upload:
```bash
curl -s -X POST "https://retriever.denser.ai/api/open/v1/importTextContent" \
  -H "x-api-key: $DENSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledgeBaseId": "KB_ID", "title": "My Document", "content": "Full text content here..."}' | python3 -m json.tool
```

### 3. Search Across All Knowledge Bases

Omit `knowledgeBaseIds` to search everything:
```bash
curl -s -X POST "https://retriever.denser.ai/api/open/v1/query" \
  -H "x-api-key: $DENSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query", "limit": 10}' | python3 -m json.tool
```

## Automation Patterns

### Batch Upload Multiple Files

When the user provides a directory of files, loop through them:

```bash
KB_ID="your-kb-id"
for file in /path/to/files/*; do
  FILE_NAME=$(basename "$file")
  FILE_SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)

  # Get presigned URL
  PRESIGN=$(curl -s -X POST "https://retriever.denser.ai/api/open/v1/presignUploadUrl" \
    -H "x-api-key: $DENSER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"knowledgeBaseId\": \"$KB_ID\", \"fileName\": \"$FILE_NAME\", \"size\": $FILE_SIZE}")

  UPLOAD_URL=$(echo "$PRESIGN" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['uploadUrl'])")
  FILE_ID=$(echo "$PRESIGN" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['fileId'])")

  # Upload file
  curl -s -X PUT "$UPLOAD_URL" --data-binary @"$file"

  # Trigger import
  curl -s -X POST "https://retriever.denser.ai/api/open/v1/importFile" \
    -H "x-api-key: $DENSER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"fileId\": \"$FILE_ID\"}"

  echo "Uploaded: $FILE_NAME (fileId: $FILE_ID)"
done
```

### Poll Document Status Until Ready

```bash
DOC_ID="your-document-id"
while true; do
  STATUS=$(curl -s -X GET "https://retriever.denser.ai/api/open/v1/getDocumentStatus?documentId=$DOC_ID" \
    -H "x-api-key: $DENSER_API_KEY" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['status'])")
  echo "Status: $STATUS"
  if [ "$STATUS" = "processed" ] || [ "$STATUS" = "failed" ] || [ "$STATUS" = "timeout" ]; then
    break
  fi
  sleep 3
done
```

## Response Format

All responses follow this structure:

**Success:** `{"success": true, "data": { ... }}`

**Error:** `{"success": false, "message": "Error details", "errorCode": "ERROR_CODE"}`

Common error codes: `STORAGE_LIMIT_EXCEEDED`, `KNOWLEDGE_BASE_LIMIT_EXCEEDED`, `INSUFFICIENT_CREDITS`, `INPUT_VALIDATION_FAILED`

## Supported File Types

PDF, DOCX, PPTX, XLS, XLSX, HTML, TXT, CSV, XML, Markdown. Max file size: 512MB.

## Important Notes

- Each search query costs 1 credit. Check balance with `getBalance` before bulk searches.
- Document processing is async — always poll `getDocumentStatus` before searching.
- The `presignUploadUrl` -> PUT upload -> `importFile` flow is required for file uploads.
- Search results include `score`, `content`, `title`, `document_id`, and `metadata`.
