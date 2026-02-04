---
name: looking-up-docs
description: Look up library documentation using Context7. Use when needing API reference, library docs, framework documentation, or technical documentation lookup. Provides up-to-date, version-specific docs and code examples.
allowed-tools: Read, Grep, Glob, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
---

# Documentation Lookup with Context7

Context7 provides up-to-date, version-specific documentation and code examples directly from source libraries.

## Why Context7

- **Current APIs**: No hallucinated or outdated patterns
- **Version-specific**: Gets docs for exact library versions
- **Code examples**: Real, working code from actual documentation

## Workflow

1. **Resolve library ID**: `mcp__context7__resolve-library-id` with `libraryName`
2. **Get documentation**: `mcp__context7__get-library-docs` with `context7CompatibleLibraryID` and `topic`

## Modes

| Mode   | Use For                                    |
| ------ | ------------------------------------------ |
| `code` | API references, code examples (default)    |
| `info` | Conceptual guides, architecture, tutorials |

## Examples

```
# React hooks
resolve-library-id: "react"
get-library-docs: context7CompatibleLibraryID="/facebook/react", topic="hooks", mode="code"

# Next.js middleware
resolve-library-id: "next.js"
get-library-docs: context7CompatibleLibraryID="/vercel/next.js", topic="middleware"

# Go net/http
resolve-library-id: "go net/http"
get-library-docs: context7CompatibleLibraryID="/golang/go", topic="http server"

# Kubernetes API
resolve-library-id: "kubernetes"
get-library-docs: context7CompatibleLibraryID="/kubernetes/kubernetes", topic="deployment"
```

## Tips

- Use `topic` parameter to narrow results to specific features
- Try `mode="info"` for architectural questions
- Paginate with `page=2`, `page=3` if initial results insufficient
