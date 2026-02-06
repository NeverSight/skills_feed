---
name: framer
description: Interact with Framer projects programmatically via the Framer Server API. Execute code to manage collections (CMS), canvas nodes, images, styles, code files, and more. Run `npx framer-dalton skill` for complete documentation.
---

## Quick Start

```bash
# Get a session ID first (use @latest for first command)
npx framer-dalton@latest session new "<projectUrl>" "<apiKey>"
# => 1

# Look up the API before writing code
npx framer-dalton docs Collection
npx framer-dalton docs Collection.getItems

# Execute code with your session
npx framer-dalton -s 1 -e "state.collections = await framer.getCollections(); console.log(state.collections.map(c => c.name))"
```

Use `npx framer-dalton@latest` for the first command to ensure you're using the latest version. Subsequent commands can omit `@latest`.

## Full Documentation

**Always run `npx framer-dalton skill` to get the complete, up-to-date skill instructions.**

The skill command outputs detailed docs on:
- Session management
- Context variables (`framer`, `state`, `console`)
- Code execution patterns and escaping
- API documentation lookup
- Working with Collections (CMS)
- Working with Nodes (canvas layers)
- Working with Images and SVGs
- Working with Styles (color, text, fonts)
- Working with Code Files
- Component Instances
- Storing plugin data
- Localization
- Screenshots and SVG export
- Publishing and deployments
- Change tracking
- And more...

```bash
npx framer-dalton skill
```
