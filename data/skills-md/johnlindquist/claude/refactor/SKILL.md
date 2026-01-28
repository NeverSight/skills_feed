---
name: refactor
description: Code refactoring with AI assistance. Use for modernizing code, converting JavaScript to TypeScript, class to hooks conversions, and systematic renaming.
---

# Refactoring Assistant

Systematic code refactoring with AI guidance.

## Prerequisites

```bash
# Gemini for analysis and suggestions
pip install google-generativeai
export GEMINI_API_KEY=your_api_key

# AST-based tools
npm install -g jscodeshift
npm install -g typescript
```

## Refactoring Operations

### JavaScript to TypeScript

```bash
# Step 1: Rename file
mv file.js file.ts

# Step 2: AI assistance for types
CODE=$(cat file.ts)
gemini -m pro -o text -e "" "Convert this JavaScript to TypeScript with proper types:

$CODE

Requirements:
- Add explicit types for function parameters and returns
- Create interfaces for object shapes
- Use strict TypeScript (no any unless necessary)
- Preserve functionality exactly"
```

### Class to React Hooks

```bash
CODE=$(cat ClassComponent.tsx)
gemini -m pro -o text -e "" "Convert this React class component to functional component with hooks:

$CODE

Requirements:
- Convert state to useState
- Convert lifecycle methods to useEffect
- Convert class methods to functions
- Preserve all functionality
- Use proper TypeScript types"
```

### Modernize Code

```bash
CODE=$(cat legacy.ts)
gemini -m pro -o text -e "" "Modernize this code to current best practices:

$CODE

Apply:
- ES2023+ features where appropriate
- Modern TypeScript patterns
- Current framework idioms
- Better error handling
- Improved readability"
```

### Systematic Rename

```bash
# Using sed for simple renames
find src -name "*.ts" -exec sed -i '' 's/oldName/newName/g' {} +

# Using ripgrep to preview
rg "oldName" src/

# With jscodeshift for AST-safe rename
npx jscodeshift -t rename-transform.ts src/

# AI-assisted rename planning
gemini -m pro -o text -e "" "I want to rename 'oldName' to 'newName' across the codebase.

Files that use it:
$(rg -l "oldName" src/)

Suggest:
1. Order of changes to avoid breaks
2. Any tricky cases to watch for
3. Tests to run after"
```

## Analysis Commands

### Find Refactoring Opportunities

```bash
gemini -m pro -o text -e "" "Analyze this code for refactoring opportunities:

$(cat src/module.ts)

Look for:
- Code duplication
- Long functions
- Deep nesting
- Magic numbers/strings
- Poor naming
- Missing abstractions
- Tight coupling"
```

### Complexity Analysis

```bash
# Find complex functions
rg "function|=>\s*{" src/ -A 50 | head -200

# Ask AI to identify complexity
gemini -m pro -o text -e "" "Identify the most complex functions in this code and suggest simplifications:

$(cat src/complex-file.ts)"
```

## Safe Refactoring Workflow

### Step 1: Ensure Test Coverage

```bash
# Check coverage before refactoring
npm test -- --coverage

# Identify untested code
npx jest --coverage --coverageReporters=text | grep -E "^(File|.*\|)"
```

### Step 2: Plan the Refactoring

```bash
gemini -m pro -o text -e "" "Plan a safe refactoring for:

CURRENT CODE:
$(cat src/file.ts)

GOAL: [what you want to improve]

Provide:
1. Step-by-step plan
2. Risk assessment
3. Rollback strategy
4. Tests to add first"
```

### Step 3: Small, Tested Changes

```bash
# Make one small change
# Run tests
npm test

# Commit if green
git add -A && git commit -m "refactor: [specific change]"

# Repeat
```

### Step 4: Verify Behavior

```bash
# Compare before/after behavior
# Run integration tests
# Manual testing if needed
```

## Common Refactorings

### Extract Function

```bash
gemini -m pro -o text -e "" "Extract a reusable function from this code:

$(cat src/file.ts | sed -n '10,50p')

Create a well-named function with:
- Clear parameters
- Typed return value
- JSDoc comment
- Single responsibility"
```

### Simplify Conditionals

```bash
gemini -m pro -o text -e "" "Simplify these conditionals:

\`\`\`typescript
$(rg -A 10 "if.*{" src/file.ts)
\`\`\`

Use:
- Early returns
- Guard clauses
- Lookup tables where appropriate
- Optional chaining"
```

### Remove Duplication

```bash
# Find similar code
gemini -m pro -o text -e "" "Find duplicate or similar code patterns in:

$(cat src/*.ts)

Suggest how to DRY it up with:
- Shared functions
- Higher-order functions
- Generics if TypeScript"
```

## jscodeshift Transforms

### Create Transform

```typescript
// rename-transform.ts
export default function transformer(file, api) {
  const j = api.jscodeshift;
  return j(file.source)
    .find(j.Identifier, { name: 'oldName' })
    .replaceWith(j.identifier('newName'))
    .toSource();
}
```

### Run Transform

```bash
# Dry run
npx jscodeshift -d -p -t transform.ts src/

# Apply
npx jscodeshift -t transform.ts src/
```

## Best Practices

1. **Test first** - Don't refactor untested code
2. **Small steps** - One change at a time
3. **Commit often** - Each working state
4. **Preserve behavior** - Refactoring isn't rewriting
5. **Use tools** - AST transforms > find-replace
6. **Review diffs** - Verify each change
7. **Run tests continuously** - Catch breaks early
