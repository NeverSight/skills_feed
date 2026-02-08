---
name: code-examples
description: Find real-world code examples across millions of GitHub repositories. Use when the user wants to see how others implement something, find usage patterns, or discover code examples in the wild.
---

# Code Examples

Find real-world code examples across millions of public GitHub repositories using grep.app.

**When to activate:**

- User wants to see real-world code examples
- User asks "how do others implement X?"
- User wants to find usage patterns for a library/API
- User needs production code examples (not docs)

**API endpoint:**

```bash
curl -s "https://grep.app/api/search?q={query}&page=1" | jq '.hits.hits[:5]'
```

**Parameters:**

| Parameter        | Description                                                           |
| ---------------- | --------------------------------------------------------------------- |
| `q`              | Search query (required)                                               |
| `page`           | Page number for pagination                                            |
| `regexp`         | `true` for regex search                                               |
| `case`           | `true` for case-sensitive                                             |
| `f.lang`         | Language filter (**capitalized**, e.g., `TypeScript`, `Go`, `Python`) |
| `f.repo.pattern` | Filter by repository pattern                                          |
| `f.path.pattern` | Filter by file path pattern                                           |

**Examples:**

Search for useEffect usage in TypeScript:

```bash
curl -s "https://grep.app/api/search?q=useEffect&f.lang=TypeScript&page=1" | jq '.hits.hits[:3]'
```

Search for Go error handling patterns:

```bash
curl -s "https://grep.app/api/search?q=if%20err%20!=%20nil&f.lang=Go&page=1" | jq '.hits.hits[:3]'
```

Search within a specific repo:

```bash
curl -s "https://grep.app/api/search?q=createContext&f.repo.pattern=facebook/react&page=1" | jq '.hits.hits[:3]'
```

**Response format:**

- `hits.hits[]` - Array of search results
- Each hit contains: `repo.raw` (repo name), `path.raw` (file path), `content.snippet` (code snippet)

**Note:** Returns max 1000 results. For documentation, use the documentation-lookup skill instead.
