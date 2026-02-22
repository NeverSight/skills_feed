---
name: minimax-web-search
description: Search the web for current information using the web_search tool
---

# MiniMax Web Search Skill

Use this skill when you need to find current, real-time, or authoritative information that may have changed since my knowledge cutoff.

## How to Use

Call the `web_search` tool directly with a query:

```
web_search({ query: "your search query" })
```

## When to Use

Use `web_search` when:

- **Current events**: News, recent developments, latest releases
- **Fact verification**: Checking if information is still accurate
- **Technical updates**: New versions, patches, breaking changes
- **Dynamic content**: Prices, availability, schedules
- **Authoritative sources**: Official documentation, API references

## When NOT to Use

Do NOT use `web_search` when:

- **General knowledge** I likely know (historical facts, basic concepts)
- **Coding help** for common patterns (unless asking about latest practices)
- **Opinion-based questions** without specific recent information needs
- **Files already in context** or accessible via `read` tool

## Usage

```
web_search({
  query: "your search query here"
})
```

## API Details

**Endpoint**: `POST {api_host}/v1/coding_plan/search`

**Request Body**:
```json
{
  "q": "your search query"
}
```

**Response Format**:
```json
{
  "organic": [
    {
      "title": "Result Title",
      "link": "https://example.com",
      "snippet": "Brief description...",
      "date": "2025-01-15"
    }
  ],
  "related_searches": [
    {"query": "related query 1"},
    {"query": "related query 2"}
  ],
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

## Tips for Better Results

1. **Be specific**: "TypeScript 5.4 new features" vs "TypeScript updates"
2. **Include context**: "React 19 server components vs client components"
3. **Use recent keywords**: "2024" or "2025" when timing matters
4. **Target authoritative sources**: Include product names, official sites
5. **Use 3-5 keywords** for optimal results

## Examples

### Good Queries
- "Node.js 22 new features"
- "Claude Code vs pi coding agent 2025"
- "React 19 release date official"
- "Docker desktop alternatives 2024"
- "TypeScript 5.4 generics tutorial"

### Poor Queries
- "how to use TypeScript" (too general)
- "is Python popular" (opinion, not time-sensitive)
- "help me debug my code" (not a search task)
- "best programming language" (opinion-based)

## Response Format

Results include:
- **Titles** and **URLs** for each result
- **Snippets** with relevant context
- **Dates** when available
- **Related searches** for follow-up queries

You can use the suggestions to refine your search or ask the user which direction they'd like to explore.

## Error Handling

- **Status code 1004**: Authentication error - check API key and region
- **Status code 2038**: Real-name verification required
- **Other errors**: Check Trace-Id in error message for support
