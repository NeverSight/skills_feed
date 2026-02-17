---
name: context7
description: A skill for retrieving the latest library documentation using Context7. Use when the user asks about how to use a library, requests code examples, or instructs to "use context7". Prevents hallucinations based on outdated training data and provides up-to-date API information.
---

# Context7

## Overview

Context7 is a service that provides LLMs with the latest library documentation. It prevents hallucinations from outdated training data or non-existent APIs, enabling retrieval of version-specific accurate documentation and code examples.

## When to Use

Use this skill in the following cases:

1. **Explicit instruction**: When the user instructs "use context7" or "check the latest documentation"
2. **Library usage questions**: When asked about how to use a specific library's API, hooks, or functions
3. **Code example requests**: When asked for code examples using a specific library
4. **Version-specific information**: When library information for a specific version is needed
5. **Uncertain API information**: When your knowledge might be outdated and latest information verification is needed

## Workflow

### Step 1: Resolve Library ID

First, obtain the Context7 ID for the target library.

**API call:**
```bash
curl "https://context7.com/api/v2/libs/search?libraryName=LIBRARY_NAME&query=CONTEXT_QUERY" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Example:**
```bash
# Search for React library
curl "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Criteria for selecting from response:**
- `trustScore`: Trust score (higher is better)
- `totalSnippets`: Number of available documents (more means richer information)
- `versions`: Verify that the required version is included

### Step 2: Retrieve Documentation

Use the resolved library ID to retrieve specific documentation.

**API call:**
```bash
curl "https://context7.com/api/v2/context?libraryId=LIBRARY_ID&query=SPECIFIC_QUERY" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Example:**
```bash
# Retrieve information about React's useEffect
curl "https://context7.com/api/v2/context?libraryId=/facebook/react&query=useEffect cleanup function" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Query best practices:**
- Use specific queries ("useEffect cleanup function" rather than "hooks")
- Be clear about the purpose ("authentication middleware", "form validation", etc.)

### Step 3: Respond to User

Respond to the user's question based on the retrieved documentation.

**Information to include in the response:**
- Retrieved code examples
- API explanations
- Documentation source URLs (for reference)

## Examples

### Example 1: React Hook Usage

**User:** "How do I write a cleanup function with React's useEffect?"

**Execution steps:**
1. Library search: `libraryName=react`, `query=useEffect cleanup`
2. Documentation retrieval: `libraryId=/facebook/react`, `query=useEffect cleanup function`
3. Respond with the latest code examples and best practices

### Example 2: Next.js Routing

**User:** "Use context7 to show me how to implement authentication middleware with Next.js App Router"

**Execution steps:**
1. Library search: `libraryName=next.js`, `query=middleware authentication`
2. Documentation retrieval: `libraryId=/vercel/next.js`, `query=middleware authentication route protection`
3. Respond with the latest App Router compatible middleware implementation

### Example 3: Multiple Libraries Combination

**User:** "How to create a button component using TailwindCSS and shadcn/ui"

**Execution steps:**
1. Resolve IDs for each library
2. Retrieve documentation for both
3. Respond with a combined implementation example

## Error Handling

| Error | Solution |
|-------|----------|
| 404 (Not Found) | Search again with a different library name (e.g., "nextjs" → "next.js") |
| 429 (Rate Limit) | Wait a moment and retry |
| Empty response | Retry with a more general query |

## Resources

For detailed API specifications, see `references/api_reference.md`.

- Endpoint details
- Response field descriptions
- Rate limit information
- Error code list
