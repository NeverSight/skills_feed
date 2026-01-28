---
name: exa-search
version: 1.0.0
author: BenedictKing
description: "Semantic search skill using Exa API for embeddings-based search, similar content discovery, and structured research. Use when you need semantic search, find similar pages, or category-specific searches. Triggers: exa, semantic search, find similar, research paper, github search, 语义搜索, 相似内容"
allowed-tools:
  - Task
  - Bash
  - Read
  - Write
user-invocable: true
---

# Exa Search Skill

## Trigger Conditions & Endpoint Selection

Choose Exa endpoint based on user intent:

- **search**: Need semantic search / find web pages / research topics
- **contents**: Given result IDs, need to extract full content
- **findsimilar**: Given URL, need to find similar pages
- **answer**: Need direct answer to a question
- **research**: Need structured research output following given `output_schema`

## Recommended Architecture (Main Skill + Sub-skill)

This skill uses a two-phase architecture:

1. **Main skill (current context)**: Understand user question → Choose endpoint → Assemble JSON payload
2. **Sub-skill (fork context)**: Only responsible for HTTP call execution, avoiding conversation history token waste

## Execution Method

Use Task tool to invoke `exa-fetcher` sub-skill, passing command and JSON (stdin):

```
Task parameters:
- subagent_type: Bash
- description: "Call Exa API"
- prompt: cat <<'JSON' | node .claude/skills/exa-search/exa-api.js <search|contents|findsimilar|answer|research>
  { ...payload... }
  JSON
```

## Payload Examples

### 1) Search

```bash
cat <<'JSON' | node .claude/skills/exa-search/exa-api.js search
{
  "query": "Latest research in LLMs",
  "type": "auto",
  "numResults": 10,
  "category": "research paper",
  "includeDomains": [],
  "excludeDomains": [],
  "startPublishedDate": "2025-01-01",
  "endPublishedDate": "2025-12-31",
  "includeText": [],
  "excludeText": [],
  "context": true,
  "contents": {
    "text": true,
    "highlights": true,
    "summary": true
  }
}
JSON
```

**Search Types:**
- `neural`: Semantic search using embeddings
- `fast`: Quick keyword-based search
- `auto`: Automatically choose best method (default)
- `deep`: Comprehensive deep search

**Categories:**
- `company`, `people`, `research paper`, `news`, `pdf`, `github`, `tweet`, etc.

### 2) Contents

```bash
cat <<'JSON' | node .claude/skills/exa-search/exa-api.js contents
{
  "ids": ["result-id-1", "result-id-2"],
  "text": true,
  "highlights": true,
  "summary": true
}
JSON
```

### 3) Find Similar

```bash
cat <<'JSON' | node .claude/skills/exa-search/exa-api.js findsimilar
{
  "url": "https://example.com/article",
  "numResults": 10,
  "category": "news",
  "includeDomains": [],
  "excludeDomains": [],
  "startPublishedDate": "2025-01-01",
  "contents": {
    "text": true,
    "summary": true
  }
}
JSON
```

### 4) Answer

```bash
cat <<'JSON' | node .claude/skills/exa-search/exa-api.js answer
{
  "query": "What is the capital of France?",
  "numResults": 5,
  "includeDomains": [],
  "excludeDomains": []
}
JSON
```

### 5) Research

```bash
cat <<'JSON' | node .claude/skills/exa-search/exa-api.js research
{
  "input": "What are the latest developments in AI?",
  "model": "auto",
  "stream": false,
  "output_schema": {
    "properties": {
      "topic": {
        "type": "string",
        "description": "The main topic"
      },
      "key_findings": {
        "type": "array",
        "description": "List of key findings",
        "items": {
          "type": "string"
        }
      }
    },
    "required": ["topic"]
  },
  "citation_format": "numbered"
}
JSON
```

## Environment Variables & API Key

Two ways to configure API Key (priority: environment variable > `.env`):

1. Environment variable: `EXA_API_KEY`
2. `.env` file: Place in `.claude/skills/exa-search/.env`, can copy from `.env.example`

## Response Format

All endpoints return JSON with:
- `requestId`: Unique request identifier
- `results`: Array of search results
- `searchType`: Type of search performed (for search endpoint)
- `context`: LLM-friendly context string (if requested)
- `costDollars`: Detailed cost breakdown
