---
name: nextjs-migration-toolkit
description: "Required dependency for all next-migration-skills. Provides AST analysis and transform tools powered by ts-morph for analyzing routes, components, dependencies, and generating App Router code."
---

# Next.js Migration Toolkit

AST-powered analysis and transform tools for Next.js Pages Router to App Router migration. This skill is a dependency for all other migration skills — install it alongside them.

## Setup

Before using any migration skill, run the setup script to install toolkit dependencies:

```bash
TOOLKIT_DIR="$(cd "$(dirname "$SKILL_PATH")" && pwd)"
if [ ! -d "$TOOLKIT_DIR/node_modules" ]; then
  cd "$TOOLKIT_DIR" && npm install --silent 2>/dev/null
fi
```

## Available Commands

All commands output structured JSON to stdout.

### Analyzers

```bash
# Extract all routes from pages/ directory
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze routes <pagesDir>

# Inventory components and classify as server/client
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze components <srcDir>

# Map dependencies to App Router equivalents
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze dependencies <packageJsonPath>

# Find unused exports
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze dead-code <srcDir>

# Audit next.config.js for migration issues
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze config <nextConfigPath>

# Extract props from a component
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze props <componentFile>
```

### Transforms (dry-run by default)

```bash
# Rewrite imports (next/router → next/navigation, etc.)
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform imports <file> --dry-run

# Migrate data fetching patterns
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform data-fetching <file>

# Update router usage patterns
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform router <file>
```

### Validation

```bash
# Validate migrated app/ directory for common issues
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" validate <appDir>
```

## Output Format

All commands return JSON. Example route analysis output:

```json
{
  "routes": [
    {
      "file": "pages/blog/[slug].tsx",
      "route": "/blog/:slug",
      "type": "dynamic",
      "dataFetching": ["getStaticProps", "getStaticPaths"]
    }
  ],
  "summary": { "total": 1, "static": 0, "dynamic": 1, "api": 0 }
}
```
