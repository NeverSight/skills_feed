---
name: dependency-mapping
description: >
  Use when checking npm package compatibility with App Router, replacing
  deprecated packages, or auditing dependencies before migration. Covers
  next/router, next/image legacy, and RSC-incompatible packages.
---

# Dependency Mapping

Analyze all project dependencies and create a mapping to their App Router equivalents with migration instructions.

## Toolkit Setup

This skill requires the `nextjs-migration-toolkit` skill to be installed. All migration skills depend on it for AST analysis.

```bash
TOOLKIT_DIR="$(cd "$(dirname "$SKILL_PATH")/../nextjs-migration-toolkit" && pwd)"
if [ ! -f "$TOOLKIT_DIR/package.json" ]; then
  echo "ERROR: nextjs-migration-toolkit is not installed." >&2
  echo "Run: npx skills add blazity/next-migration-skills -s nextjs-migration-toolkit" >&2
  echo "Then retry this skill." >&2
  exit 1
fi
bash "$TOOLKIT_DIR/scripts/setup.sh" >/dev/null
```

## Steps

### 1. Run Dependency Analysis

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze dependencies <packageJsonPath>
```

### 2. Review Each Category

From the analysis output, review each dependency classification:

**Core packages** (next, react, react-dom):
- Verify minimum versions: next@13.4+, react@18+
- Check if `next` version supports App Router features needed

**Replaceable packages**:
- For each package, review the suggested replacement and migration note
- Check if the replacement is already installed
- Determine migration effort per package

**Unknown packages**:
- Research each unknown package for App Router compatibility
- Check the package's documentation for RSC (React Server Component) support
- Classify as: compatible, needs update, needs replacement, or needs removal

**Dev tools**:
- Generally no changes needed
- Verify test frameworks support App Router patterns

### 3. Create Dependency Migration Map

For each package needing action, document:
- Current package and version
- Replacement package (if any)
- Installation command (`npm install <replacement>`)
- Code changes required (import paths, API differences)
- Files affected (grep for usage)

### 4. Generate Package Update Commands

Produce runnable commands:
```bash
# Remove deprecated packages
npm uninstall <package1> <package2>

# Install replacements
npm install <replacement1> <replacement2>

# Update existing packages
npm install <package>@latest
```

### 5. Save Mapping

Write the dependency mapping to `.migration/dependencies.md`.
