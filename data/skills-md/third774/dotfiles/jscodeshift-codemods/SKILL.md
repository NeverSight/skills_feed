---
name: jscodeshift-codemods
description: Write and debug AST-based codemods using jscodeshift for automated code transformations. Use when creating migrations, API upgrades, pattern standardization, or large-scale refactoring.
---

# jscodeshift Codemods

**Core Philosophy:** Transform AST nodes, not text. Let recast handle printing to preserve formatting and structure.

<IMPORTANT>
1. Always use TDD - write failing tests before implementing transforms
2. Transform the minimal AST necessary - surgical changes preserve formatting
3. Handle edge cases explicitly - codemods run on thousands of files
</IMPORTANT>

## When to Use

Use codemods for:

- **API migrations** - Library upgrades (React Router v5→v6, enzyme→RTL)
- **Pattern standardization** - Enforce coding conventions across codebase
- **Deprecation removal** - Remove deprecated APIs systematically
- **Large-scale refactoring** - Rename functions, restructure imports, update patterns

**Don't use codemods for:**

- One-off changes (faster to do manually)
- Changes requiring semantic understanding (business logic)
- Non-deterministic transformations

## Codemod Workflow

Copy this checklist and track your progress:

```
Codemod Progress:
- [ ] Phase 1: Identify Patterns
  - [ ] Collect before/after examples from real code
  - [ ] Document transformation rules
  - [ ] Identify edge cases
- [ ] Phase 2: Create Test Fixtures
  - [ ] Create input fixture with pattern to transform
  - [ ] Create expected output fixture
  - [ ] Verify test fails (TDD)
- [ ] Phase 3: Implement Transform
  - [ ] Find target nodes
  - [ ] Apply transformation
  - [ ] Return modified source
- [ ] Phase 4: Handle Edge Cases
  - [ ] Add fixtures for edge cases
  - [ ] Handle already-transformed code (idempotency)
  - [ ] Handle missing dependencies
- [ ] Phase 5: Validate at Scale
  - [ ] Dry run on target codebase
  - [ ] Review sample of changes
  - [ ] Run with --fail-on-error
```

## Project Structure

Standard codemod project layout:

```
codemods/
├── my-transform.ts                    # Transform implementation
├── __tests__/
│   └── my-transform-test.ts           # Test file
└── __testfixtures__/
    ├── my-transform.input.ts          # Input fixture
    ├── my-transform.output.ts         # Expected output
    ├── edge-case.input.ts             # Additional fixtures
    └── edge-case.output.ts
```

## Transform Module Anatomy

Every transform exports a function with this signature:

```typescript
import type { API, FileInfo, Options } from "jscodeshift";

export default function transform(
  fileInfo: FileInfo,
  api: API,
  options: Options
): string | null | undefined {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // Find and transform nodes
  root
    .find(j.Identifier, { name: "oldName" })
    .forEach((path) => {
      path.node.name = "newName";
    });

  // Return transformed source, null to skip, or undefined for no change
  return root.toSource();
}
```

**Return values:**

| Return | Meaning |
|--------|---------|
| `string` | Transformed source code |
| `null` | Skip this file (no output) |
| `undefined` | No changes made |

**Key objects:**

| Object | Purpose |
|--------|---------|
| `fileInfo.source` | Original file contents |
| `fileInfo.path` | File path being transformed |
| `api.jscodeshift` | The jscodeshift library (usually aliased as `j`) |
| `api.stats` | Collect statistics during dry runs |
| `api.report` | Print to stdout |

## Testing with defineTest

jscodeshift provides fixture-based testing utilities:

```typescript
// __tests__/my-transform-test.ts
jest.autoMockOff();
const defineTest = require("jscodeshift/dist/testUtils").defineTest;

// Basic test - uses my-transform.input.ts → my-transform.output.ts
defineTest(__dirname, "my-transform");

// Named fixtures for edge cases
defineTest(__dirname, "my-transform", null, "already-transformed");
defineTest(__dirname, "my-transform", null, "missing-import");
defineTest(__dirname, "my-transform", null, "multiple-occurrences");
```

**Fixture naming:**

```
__testfixtures__/
├── my-transform.input.ts              # Default input
├── my-transform.output.ts             # Default output
├── already-transformed.input.ts       # Named fixture input
├── already-transformed.output.ts      # Named fixture output
```

**Running tests:**

```bash
# Run all codemod tests
npx jest codemods/__tests__/

# Run specific transform tests
npx jest codemods/__tests__/my-transform-test.ts

# Run with verbose output
npx jest codemods/__tests__/my-transform-test.ts --verbose
```

## Collection API Quick Reference

The jscodeshift Collection API provides chainable methods:

| Method | Purpose | Example |
|--------|---------|---------|
| `find(type, filter?)` | Find nodes by type | `root.find(j.CallExpression, { callee: { name: 'foo' } })` |
| `filter(predicate)` | Filter collection | `.filter(path => path.node.arguments.length > 0)` |
| `forEach(callback)` | Iterate and mutate | `.forEach(path => { path.node.name = 'new' })` |
| `replaceWith(node)` | Replace matched nodes | `.replaceWith(j.identifier('newName'))` |
| `remove()` | Remove matched nodes | `.remove()` |
| `insertBefore(node)` | Insert before each match | `.insertBefore(j.importDeclaration(...))` |
| `insertAfter(node)` | Insert after each match | `.insertAfter(j.expressionStatement(...))` |
| `closest(type)` | Find nearest ancestor | `.closest(j.FunctionDeclaration)` |
| `get()` | Get first path | `.get()` |
| `paths()` | Get all paths as array | `.paths()` |
| `size()` | Count matches | `.size()` |

**Chaining pattern:**

```typescript
root
  .find(j.CallExpression, { callee: { name: "oldFunction" } })
  .filter((path) => path.node.arguments.length === 2)
  .forEach((path) => {
    path.node.callee.name = "newFunction";
  });
```

## Common Node Types

| Node Type | Represents | Example Code |
|-----------|------------|--------------|
| `Identifier` | Variable/function names | `foo`, `myVar` |
| `CallExpression` | Function calls | `foo()`, `obj.method()` |
| `MemberExpression` | Property access | `obj.prop`, `arr[0]` |
| `ImportDeclaration` | Import statements | `import { x } from 'y'` |
| `ImportSpecifier` | Named imports | `{ x }` in import |
| `ImportDefaultSpecifier` | Default imports | `x` in `import x from` |
| `VariableDeclaration` | Variable declarations | `const x = 1` |
| `VariableDeclarator` | Individual variable | `x = 1` part |
| `FunctionDeclaration` | Named functions | `function foo() {}` |
| `ArrowFunctionExpression` | Arrow functions | `() => {}` |
| `ObjectExpression` | Object literals | `{ a: 1, b: 2 }` |
| `ArrayExpression` | Array literals | `[1, 2, 3]` |
| `Literal` | Primitive values | `'string'`, `42`, `true` |
| `StringLiteral` | String values | `'hello'` |

## Common Transformation Patterns

### Rename Import Source

```typescript
// Change: import { x } from 'old-package'
// To:     import { x } from 'new-package'

root
  .find(j.ImportDeclaration, { source: { value: "old-package" } })
  .forEach((path) => {
    path.node.source.value = "new-package";
  });
```

### Rename Named Import

```typescript
// Change: import { oldName } from 'package'
// To:     import { newName } from 'package'

root
  .find(j.ImportSpecifier, { imported: { name: "oldName" } })
  .forEach((path) => {
    path.node.imported.name = "newName";
    // Also rename local if not aliased
    if (path.node.local.name === "oldName") {
      path.node.local.name = "newName";
    }
  });
```

### Add Import If Missing

```typescript
// Add: import { newThing } from 'package'

const existingImport = root.find(j.ImportDeclaration, {
  source: { value: "package" },
});

if (existingImport.size() === 0) {
  // Add new import at top of file
  const newImport = j.importDeclaration(
    [j.importSpecifier(j.identifier("newThing"))],
    j.literal("package")
  );

  root.find(j.Program).get("body", 0).insertBefore(newImport);
}
```

### Rename Function Calls

```typescript
// Change: oldFunction(arg)
// To:     newFunction(arg)

root
  .find(j.CallExpression, { callee: { name: "oldFunction" } })
  .forEach((path) => {
    path.node.callee.name = "newFunction";
  });
```

### Transform Function Arguments

```typescript
// Change: doThing(a, b, c)
// To:     doThing({ a, b, c })

root
  .find(j.CallExpression, { callee: { name: "doThing" } })
  .filter((path) => path.node.arguments.length === 3)
  .forEach((path) => {
    const [a, b, c] = path.node.arguments;
    path.node.arguments = [
      j.objectExpression([
        j.property("init", j.identifier("a"), a),
        j.property("init", j.identifier("b"), b),
        j.property("init", j.identifier("c"), c),
      ]),
    ];
  });
```

### Track Variable Usage Across Scope

```typescript
// Find what variable an import is bound to, then find all usages

root.find(j.ImportSpecifier, { imported: { name: "useHistory" } }).forEach((path) => {
  const localName = path.node.local.name; // Could be aliased

  // Find all calls using this variable
  root
    .find(j.CallExpression, { callee: { name: localName } })
    .forEach((callPath) => {
      // Transform each usage
    });
});
```

### Replace Entire Expression

```typescript
// Change: history.push('/path')
// To:     navigate('/path')

root
  .find(j.CallExpression, {
    callee: {
      type: "MemberExpression",
      object: { name: "history" },
      property: { name: "push" },
    },
  })
  .replaceWith((path) => {
    return j.callExpression(j.identifier("navigate"), path.node.arguments);
  });
```

## Anti-Patterns

### Over-Matching

```typescript
// BAD: Matches ANY identifier named 'foo'
root.find(j.Identifier, { name: "foo" });

// GOOD: Match specific context (function calls named 'foo')
root.find(j.CallExpression, { callee: { name: "foo" } });
```

### Ignoring Scope

```typescript
// BAD: Assumes 'history' always means the router history
root.find(j.Identifier, { name: "history" });

// GOOD: Verify it came from the expected import
const historyImport = root.find(j.ImportSpecifier, {
  imported: { name: "useHistory" },
});
if (historyImport.size() === 0) return; // Skip file
```

### Not Checking Idempotency

```typescript
// BAD: Adds import every time, even if already present
root.find(j.Program).get("body", 0).insertBefore(newImport);

// GOOD: Check first
const existingImport = root.find(j.ImportDeclaration, {
  source: { value: "package" },
});
if (existingImport.size() === 0) {
  root.find(j.Program).get("body", 0).insertBefore(newImport);
}
```

### Destructive Transforms

```typescript
// BAD: Rebuilds node from scratch, loses comments and formatting
path.replace(
  j.callExpression(j.identifier("newFn"), [j.literal("arg")])
);

// GOOD: Mutate existing node to preserve metadata
path.node.callee.name = "newFn";
```

### Testing Only Happy Path

```typescript
// BAD: Only one test fixture
defineTest(__dirname, "my-transform");

// GOOD: Cover edge cases
defineTest(__dirname, "my-transform");
defineTest(__dirname, "my-transform", null, "already-transformed");
defineTest(__dirname, "my-transform", null, "aliased-import");
defineTest(__dirname, "my-transform", null, "no-matching-code");
```

## Debugging Transforms

### Dry Run with Print

```bash
# See output without writing files
npx jscodeshift -t my-transform.ts target/ --dry --print
```

### Log Node Structure

```typescript
root.find(j.CallExpression).forEach((path) => {
  console.log(JSON.stringify(path.node, null, 2));
});
```

### Verbose Mode

```bash
# Show transformation stats
npx jscodeshift -t my-transform.ts target/ --verbose=2
```

### Fail on Errors

```bash
# Exit with code 1 if any file fails
npx jscodeshift -t my-transform.ts target/ --fail-on-error
```

## CLI Quick Reference

```bash
# Basic usage
npx jscodeshift -t transform.ts src/

# TypeScript/TSX files
npx jscodeshift -t transform.ts src/ --parser=tsx --extensions=ts,tsx

# Dry run (no changes)
npx jscodeshift -t transform.ts src/ --dry

# Print output to stdout
npx jscodeshift -t transform.ts src/ --print

# Limit parallelism
npx jscodeshift -t transform.ts src/ --cpus=4

# Ignore patterns
npx jscodeshift -t transform.ts src/ --ignore-pattern="**/*.test.ts"
```

## Integration

**Complementary skills:**

- **writing-tests** - For test-first codemod development
- **systematic-debugging** - When transforms produce unexpected results
- **verification-before-completion** - Verify codemod works before claiming done

**Language-specific patterns:**

- **React/TypeScript**: See [references/react-typescript.md](references/react-typescript.md) for JSX transforms, hook migrations, and component patterns
