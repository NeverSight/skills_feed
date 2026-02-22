---
name: validation-testing
description: >
  Use after migrating a route or completing a migration phase to verify
  correctness. Also use when the build breaks, tests fail, or you suspect
  migration regressions.
---

# Validation & Testing

Run comprehensive validation checks on migrated code to ensure correctness and catch common migration issues.

```
NO MIGRATION IS COMPLETE WITHOUT A PASSING BUILD
```

"It compiles" is not "it works." "The validator passes" is not "the build succeeds." Run every step below. A migration claimed as complete without a passing build is not complete.

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

### 1. Run Migration Validator

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" validate <appDir>
```

This checks for:
- No `next/router` imports in app/ files (must use `next/navigation`)
- No old data-fetching exports (getStaticProps, getServerSideProps, etc.)
- Missing `'use client'` directives on files using client features
- Orphaned files not following App Router conventions

### 2. Check Import Consistency

For each migrated file:
```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform imports <file> --dry-run
```

Verify all imports use App Router-compatible modules.

### 3. Check Router Usage

For each migrated file:
```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform router <file>
```

Verify no breaking router patterns remain (router.query, router.pathname, router.events, etc.).

### 4. Verify Build

Run the Next.js build to catch compilation errors:
```bash
npx next build
```

Common build errors after migration:
- Type errors from changed APIs
- Missing exports (generateStaticParams, metadata)
- Client/server boundary violations

### 5. Run Existing Tests

```bash
npm test
```

If tests exist, run them to verify behavior is preserved. Common test failures:
- Router mocking needs updating (next/router → next/navigation)
- Data fetching tests need restructuring
- Component render tests may need `'use client'` handling

### 6. Manual Smoke Test Checklist

Verify in the browser:
- [ ] All routes render without errors
- [ ] Navigation between pages works
- [ ] Dynamic routes resolve correctly
- [ ] Data fetching produces correct data
- [ ] Client-side interactions work (forms, buttons, modals)
- [ ] API routes respond correctly
- [ ] Images load properly
- [ ] Metadata/SEO tags are present

### 7. Report Results

Generate a validation report summarizing:
- Validator results (pass/fail per rule)
- Build status
- Test results
- Remaining manual checks

Save to `.migration/validation-report.md`.
