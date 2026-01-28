---
name: voltagent-docs-bundle
# prettier-ignore
description: Look up VoltAgent documentation embedded in node_modules/@voltagent/core/docs for version-matched docs. Use for API signatures, guides, and examples.
license: MIT
metadata:
  author: VoltAgent
  version: "1.0.0"
  repository: https://github.com/VoltAgent/skills
---

# VoltAgent Embedded Docs Lookup

Look up VoltAgent docs embedded in `node_modules/@voltagent/core/docs`. This bundle mirrors the website docs plus additional doc sets, so it is safe to use for version-matched answers.

---

## Where the Docs Live

```
node_modules/@voltagent/core/docs/
|-- actions.md
|-- agents/
|-- api/
|-- blog/
|-- community/
|-- deployment-docs/
|-- deployment.md
|-- evals.md
|-- evaluation-docs/
|-- getting-started/
|-- guardrails/
|-- integrations/
|-- models-docs/
|-- observability/
|-- observability-platform/
|-- prompt-engineering-docs/
|-- rag/
|-- recipes/
|-- repo-docs/
|-- site-examples/
|-- tools/
|-- triggers.md
|-- troubleshooting/
|-- ui/
|-- utils/
`-- workflows/
```

If you are inside the VoltAgent monorepo, the same content exists at:

```
packages/core/docs/
```


---

## Lookup Flow

1) List available sections:
```bash
ls node_modules/@voltagent/core/docs
```

2) Search for a topic:
```bash
rg -n "workflow" node_modules/@voltagent/core/docs -g"*.md"
```

3) Read the file:
```bash
cat node_modules/@voltagent/core/docs/workflows/overview.md
```

---

## Quick Commands

```bash
# List docs
ls node_modules/@voltagent/core/docs

# Find a keyword
rg -n "memory" node_modules/@voltagent/core/docs -g"*.md"

# Open a section
cat node_modules/@voltagent/core/docs/getting-started/quick-start.md
```

---

## Why This Works

- Docs are bundled with the installed version
- Avoids web drift and outdated content
- Covers the full doc surface (guides, recipes, platform docs)
