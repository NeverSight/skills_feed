---
name: qdrant-patterns
description: Store and retrieve documents using Qdrant for RAG workflows. Use for persistent memory, research storage, and semantic search.
---

# Qdrant Patterns

Use the `qdrant` MCP server tools for persistent vector storage and semantic retrieval.

## Available Tools

| Tool | Purpose |
|------|---------|
| `qdrant-store` | Store information with automatic embedding |
| `qdrant-find` | Semantic search for stored information |

## Collection Configuration

The collection name is configured via environment variable:
- `COLLECTION_NAME` - Set to `${WORKSPACE_PROFILE:-default}_memories`

This provides workspace isolation - each profile gets its own collection.

## Storing Documents

Store information with the `qdrant-store` tool:

```
Tool: qdrant-store
Information: "GitHub REST API uses OAuth tokens for authentication. Personal access tokens (PATs) provide scoped access to repositories, issues, and other resources. Fine-grained PATs offer more granular permissions than classic tokens."
Metadata:
  source: "https://docs.github.com/rest/authentication"
  type: "documentation"
  harvested_at: "2025-01-04"
  tags: "github,api,authentication"
```

### Metadata Best Practices

Always include:
- `source` - Original URL or file path
- `type` - Content type (documentation, code, article, etc.)
- `harvested_at` - ISO date of collection
- `tags` - Comma-separated searchable keywords

Optional but useful:
- `project` - Related project name
- `language` - Programming language if code
- `version` - API or library version
- `summary` - Brief content summary

## Querying Documents

### Semantic Search

Find related content by meaning:

```
Tool: qdrant-find
Query: "how to authenticate with OAuth"
```

The tool returns the most semantically similar stored information.

### Search Tips

- Use natural language queries
- Be specific about what you're looking for
- The embedding model (fastembed) handles semantic matching

## RAG Workflow

### 1. Check Existing Knowledge

Before researching, query for existing content:

```
Tool: qdrant-find
Query: "GitHub Actions workflow syntax"
```

If results are relevant and recent (check metadata), use them. Otherwise, harvest fresh content.

### 2. Harvest and Store

When gathering new information:

1. Fetch the content (WebFetch, Read, etc.)
2. Extract key information
3. Store in Qdrant with metadata
4. Reference the stored content

```
Tool: qdrant-store
Information: "<extracted content here>"
Metadata:
  source: "<url or path>"
  type: "documentation"
  harvested_at: "<today's date>"
  tags: "<relevant,keywords>"
```

### 3. Retrieve for Context

When answering questions or implementing features:

1. Query Qdrant for relevant documents
2. Include top results in context
3. Cite sources from metadata

## Example: Research Workflow

1. **Check existing**: Query for topic with `qdrant-find`
2. **Assess freshness**: Check `harvested_at` in results
3. **Harvest if needed**: Fetch new content
4. **Store with metadata**: Add via `qdrant-store`
5. **Use for response**: Include relevant chunks

## Tips

- Keep stored information focused (one topic per entry)
- Use consistent metadata schemas
- Include enough context in each entry to be useful standalone
- Use descriptive tags for easier filtering
- Check existing knowledge before harvesting new content
