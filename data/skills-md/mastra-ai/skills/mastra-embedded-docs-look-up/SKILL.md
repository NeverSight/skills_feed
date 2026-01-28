---
name: mastra-embedded-docs-look-up
# prettier-ignore
description: Mastra packages ship with embedded docs in node_modules/@mastra/*/dist/docs/. Use these for accurate API signatures that match your installed version.
license: Apache-2.0
metadata:
  author: Mastra
  version: "1.0.0"
  repository: https://github.com/mastra-ai/skills
---

# Mastra Embedded Docs Lookup

Look up API signatures from embedded docs in `node_modules/@mastra/*/dist/docs/` - these match the installed version.

---

## Documentation Structure

```
node_modules/@mastra/core/dist/docs/
├── SKILL.md           # Package overview, exports
├── SOURCE_MAP.json    # Export→file mappings
└── [topics]/          # Feature docs (agents/, workflows/, etc.)
```

---

## Lookup Process

**1. Find the export:**
```bash
cat node_modules/@mastra/core/dist/docs/SOURCE_MAP.json | grep '"Agent"'
```

Returns: `{ "Agent": { "types": "dist/agent/agent.d.ts", ... } }`

**2. Read type definition:**
```bash
cat node_modules/@mastra/core/dist/agent/agent.d.ts
```

**3. Check topic docs:**
```bash
cat node_modules/@mastra/core/dist/docs/agents/01-overview.md
```

---

## Common Packages

| Package | Path | Contains |
|---------|------|----------|
| `@mastra/core` | `node_modules/@mastra/core/dist/docs/` | Agents, Workflows, Tools |
| `@mastra/memory` | `node_modules/@mastra/memory/dist/docs/` | Memory systems |
| `@mastra/rag` | `node_modules/@mastra/rag/dist/docs/` | RAG features |

---

## Quick Commands

```bash
# List installed packages
ls node_modules/@mastra/

# Find export in SOURCE_MAP
cat node_modules/@mastra/core/dist/docs/SOURCE_MAP.json | grep '"ExportName"'

# Read type definition
cat node_modules/@mastra/core/dist/[path-from-source-map]

# List available topics
ls node_modules/@mastra/core/dist/docs/
```

---

## Why Use This

- Embedded docs match installed version exactly
- Mastra evolves quickly — installed docs stay in sync
- Training data may be outdated
- Type definitions include JSDoc and examples
