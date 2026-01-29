---
name: ralph-prd
description: Generate structured prd.json files for autonomous agent loops (Ralph Wiggum pattern). Use when planning bulk/batch tasks, migrations, refactoring campaigns, or any work that can be decomposed into independent items with verification steps.
---

# Ralph PRD Generation

Generate `prd.json` files that define scoped work items for autonomous agent execution. Each item has explicit completion criteria and verification steps.

## When to Use

- Batch migrations (API changes, library upgrades, lint fixes)
- Large-scale refactoring across many files
- Any task decomposable into independent, verifiable units
- Work that benefits from "done" being explicitly defined

## PRD Structure

```json
{
  "instructions": "<markdown with context, examples, constraints>",
  "items": [
    {
      "id": "<unique identifier>",
      "category": "<task category>",
      "description": "<what needs to be done>",
      "file": "<target file path>",
      "steps": [
        "<action step>",
        "<verification step>"
      ],
      "passes": false,
      "skipped": null
    }
  ]
}
```

### Field Reference

| Field | Purpose |
|-------|---------|
| `instructions` | Markdown embedded in PRD - transformation examples, docs links, constraints |
| `id` | Unique identifier (typically file path or task name) |
| `category` | Groups related items |
| `description` | Human-readable summary |
| `steps` | Actions + verification commands |
| `passes` | `false` initially, `true` when complete |
| `skipped` | `null` or `"<reason>"` if task cannot be completed |

## Generation Workflow

```
PRD Generation Progress:
- [ ] Step 1: Define scope (what files/items are affected?)
- [ ] Step 2: Gather input data (lint output, file list, API changes)
- [ ] Step 3: Design item granularity (per-file, per-error, per-component?)
- [ ] Step 4: Define verification steps (type-check, tests, lint)
- [ ] Step 5: Write instructions (examples, constraints, skip conditions)
- [ ] Step 6: Generate items (script or manual)
- [ ] Step 7: Review sample items
```

## Clarifying Questions

Before generating, resolve these with the user:

### Granularity
- Per-file? Per-error? Per-component?
- Trade-off: fewer items = less overhead, more items = finer progress tracking

### Verification Steps  
- What commands confirm completion?
- Type-check? Tests? Lint? Build?
- Which tests - related test file only, or broader?

### Instructions Content
- What context does the executing agent need?
- Before/after examples?
- Links to documentation?
- Type casting or naming conventions?

### Skip Conditions
- What should cause an item to be skipped rather than fixed?
- Example: "class component requires manual refactor"

### Path Format
- Relative or absolute paths?
- ID format (filename only risks collisions)

## Instructions Section Best Practices

The `instructions` field is markdown that the executing agent reads. Include:

1. **Violation/task types** with before/after examples
2. **Scope rules** - what's in bounds, what's out
3. **Skip conditions** - when to mark `skipped: "<reason>"` instead of fixing
4. **Links** to relevant documentation
5. **Type/naming conventions** specific to the codebase

Keep instructions focused. The agent discovers patterns; instructions provide guardrails.

## Verification Steps

Each item should have at least one verification step. Common patterns:

```json
"steps": [
  "Fix all N lint errors for rule-name",
  "Run yarn type-check:go - must pass",
  "Run yarn test <path> - if test exists"
]
```

For test detection, check:
- `__tests__/<filename>.test.{ts,tsx,js,jsx}`
- `<filename>.test.{ts,tsx,js,jsx}` sibling
- `__tests__/integration/<filename>.test.*`

## Example: Generating from Lint Output

Input: JSON array of lint errors grouped by file

```javascript
const prd = {
  instructions: `## Migration Instructions...`,
  items: lintErrors.map(entry => ({
    id: entry.filePath.replace(REPO_ROOT + '/', ''),
    category: 'migration',
    description: `Fix violations in ${path.basename(entry.filePath)}`,
    file: entry.filePath,
    errorCount: entry.errorCount,
    steps: [
      `Fix all ${entry.errorCount} lint errors`,
      'Run yarn type-check:go - must pass',
      ...(testExists ? [`Run yarn test ${testPath}`] : [])
    ],
    passes: false,
    skipped: null
  }))
};
```

## Anti-Patterns

### Vague verification
```json
// Bad
"steps": ["Fix the issue", "Make sure it works"]

// Good  
"steps": ["Fix lint error on line 42", "Run yarn type-check:go - must pass"]
```

### Missing skip conditions
If some items can't be completed (e.g., requires larger refactor), define skip conditions in instructions so agents mark `skipped` instead of attempting impossible fixes.

### Over-scoped items
Items that touch many files are harder to verify and resume. Prefer one file per item for file-based migrations.

### Under-specified instructions
The executing agent shouldn't have to guess conventions. Specify type casting, naming patterns, import sources.
