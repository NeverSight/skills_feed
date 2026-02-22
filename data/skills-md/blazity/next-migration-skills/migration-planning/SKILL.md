---
name: migration-planning
description: >
  Use when the user asks to plan a Next.js migration, create a migration
  roadmap, decide migration order, schedule migration phases, or asks "what
  order should I migrate routes?" Analyzes routes via AST and generates a
  phased migration plan (.migration/plan.md). Requires migration-assessment
  first.
---

# Migration Planning

Create a detailed, phased migration plan based on the assessment data. The plan prioritizes low-risk routes first and handles dependencies between components.

**Note:** This skill creates a *migration-specific* plan for ordering route conversions. It is NOT the same as generic plan mode (which is for designing implementation approaches). Use THIS skill when the user says "plan this migration" in a Next.js context.

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

## Prerequisites

- Run `migration-assessment` first to generate `.migration/assessment.md` and `.migration/target-version.txt`.
- The target Next.js version must be determined. If `.migration/target-version.txt` doesn't exist, ask the user before proceeding.

## Steps

### 1. Gather Route and Component Data

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze routes <pagesDir>
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze components <srcDir>
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze dependencies <packageJsonPath>
```

### 2. Classify Routes by Migration Difficulty

Group routes into migration waves:

**Wave 1 — Static pages (lowest risk)**
- Pages with no data fetching
- Pages using only getStaticProps without revalidate
- Server-compatible components only

**Wave 2 — ISR pages**
- Pages with getStaticProps + revalidate
- Pages with getStaticPaths

**Wave 3 — Dynamic pages**
- Pages with getServerSideProps
- Pages requiring client-side features

**Wave 4 — API routes**
- Convert API routes to route handlers
- Handle middleware migration

**Wave 5 — Complex pages**
- Pages with getInitialProps
- Pages with heavy client-side logic
- Pages depending on replaced packages

### 3. Identify Shared Dependencies

For each wave, identify:
- Shared components that need migration first
- Shared layouts that can be extracted
- Packages that need replacement before routes can migrate

### 4. Generate Migration Plan

Create a structured plan document with:
- **Phase 0: Preparation** — Install App Router deps, create app/ directory, set up root layout
- **Phase 1-N: Route waves** — Each wave with specific files to migrate and order
- **Per-route checklist**: Data fetching conversion, import updates, component classification, validation
- **Rollback strategy**: How to revert if issues arise (parallel pages/ and app/ directories)

### 5. Save Plan

Write the plan to `.migration/plan.md` in the target project.
Initialize progress tracking with the state management module.
