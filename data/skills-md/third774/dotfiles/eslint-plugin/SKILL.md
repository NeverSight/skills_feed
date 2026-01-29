---
name: eslint-plugin
description: Author custom ESLint plugins and rules with test-driven development. Supports flat config (ESLint 9+) and legacy formats. Uses @typescript-eslint/rule-tester for testing. Covers problem, suggestion, and layout rules including auto-fixers and type-aware rules. Use when creating or modifying ESLint rules, plugins, custom linting logic, or authoring auto-fixers.
---

# ESLint Plugin Author

Write custom ESLint rules using TDD. This skill covers rule creation, testing, and plugin packaging.

<IMPORTANT>
1. Write tests BEFORE implementing rules (TDD)
2. ASK about edge cases before writing any code
3. Fixes MUST be idempotent (running twice = running once)
</IMPORTANT>

## When to Use

- Enforcing project-specific coding standards
- Creating rules with auto-fix or suggestions
- Building TypeScript-aware rules using type information
- Migrating from deprecated rules

## Workflow

Copy and track:

```
ESLint Rule Progress:
- [ ] Clarify transformation (before/after examples)
- [ ] Ask edge case questions (see below)
- [ ] Detect project setup (config format, test runner)
- [ ] Write failing tests first
- [ ] Implement rule to pass tests
- [ ] Add edge case tests
- [ ] Document the rule
```

## Edge Case Discovery

**CRITICAL: Ask these BEFORE writing code.**

### Always Ask

1. Should the rule apply to all file types or specific extensions?
2. Should it be auto-fixable, provide suggestions, or just report?
3. Are any patterns exempt (test files, generated code)?

### By Rule Type

| Type | Key Questions |
|------|---------------|
| **Identifiers** | Variables, functions, classes, or all? Destructured? Renamed imports? |
| **Imports** | Re-exports? Dynamic imports? Type-only? Side-effect imports? |
| **Functions** | Arrow vs declaration? Methods vs standalone? Async? Generators? |
| **JSX** | JSX and createElement? Fragments? Self-closing? Spread props? |
| **TypeScript** | Require type info? Handle `any`? Generics? Type assertions? |

## Project Setup Detection

### Config Format

| Files Present | Format |
|---------------|--------|
| `eslint.config.js/mjs/cjs/ts` | Flat config (ESLint 9+) |
| `.eslintrc.*` or `eslintConfig` in package.json | Legacy |

### Test Runner

Check `package.json` devDependencies:
- **Bun**: `bun:test` or `bun`
- **Vitest**: `vitest`
- **Jest**: `jest`

## Rule Template

```typescript
// src/rules/rule-name.ts
import { ESLintUtils } from "@typescript-eslint/utils";

const createRule = ESLintUtils.RuleCreator(
  (name) => `https://example.com/rules/${name}`
);

type Options = [{ optionName?: boolean }];
type MessageIds = "errorId" | "suggestionId";

export default createRule<Options, MessageIds>({
  name: "rule-name",
  meta: {
    type: "problem",  // "problem" | "suggestion" | "layout"
    docs: { description: "What this rule does" },
    fixable: "code",  // Only if auto-fixable
    hasSuggestions: true,  // Only if has suggestions
    messages: {
      errorId: "Error: {{ placeholder }}",
      suggestionId: "Try this instead",
    },
    schema: [{
      type: "object",
      properties: { optionName: { type: "boolean" } },
      additionalProperties: false,
    }],
  },
  defaultOptions: [{ optionName: false }],

  create(context, [options]) {
    return {
      // Use AST selectors - see references/code-patterns.md
      "CallExpression[callee.name='forbidden']"(node) {
        context.report({
          node,
          messageId: "errorId",
          fix(fixer) {
            return fixer.replaceText(node, "replacement");
          },
        });
      },
    };
  },
});
```

## Test Template

```typescript
// src/rules/__tests__/rule-name.test.ts
import { afterAll, describe, it } from "bun:test";  // or vitest
import { RuleTester } from "@typescript-eslint/rule-tester";
import rule from "../rule-name";

// Configure BEFORE creating instance
RuleTester.afterAll = afterAll;
RuleTester.describe = describe;
RuleTester.it = it;
RuleTester.itOnly = it.only;

const ruleTester = new RuleTester({
  languageOptions: {
    parserOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
  },
});

ruleTester.run("rule-name", rule, {
  valid: [
    `const allowed = 1;`,
    {
      code: `const exempt = 1;`,
      name: "ignores exempt pattern",
    },
  ],
  invalid: [
    {
      code: `const bad = 1;`,
      output: `const good = 1;`,
      errors: [{ messageId: "errorId" }],
      name: "fixes main case",
    },
  ],
});
```

For other test runners and patterns, see [references/test-patterns.md](references/test-patterns.md).

## Type-Aware Rules

For rules needing TypeScript type information:

```typescript
import { ESLintUtils } from "@typescript-eslint/utils";

create(context) {
  const services = ESLintUtils.getParserServices(context);

  return {
    CallExpression(node) {
      // v6+ simplified API - direct call
      const type = services.getTypeAtLocation(node);

      if (type.symbol?.flags & ts.SymbolFlags.Enum) {
        context.report({ node, messageId: "enumError" });
      }
    },
  };
}
```

**Test config for type-aware rules:**

```typescript
import parser from "@typescript-eslint/parser";

const ruleTester = new RuleTester({
  languageOptions: {
    parser,
    parserOptions: {
      projectService: { allowDefaultProject: ["*.ts*"] },
      tsconfigRootDir: import.meta.dirname,
    },
  },
});
```

## Plugin Structure (Flat Config)

```typescript
// src/index.ts
import { defineConfig } from "eslint/config";
import rule1 from "./rules/rule1";

const plugin = {
  meta: { name: "eslint-plugin-my-plugin", version: "1.0.0" },
  configs: {} as Record<string, unknown>,
  rules: { "rule1": rule1 },
};

Object.assign(plugin.configs, {
  recommended: defineConfig([{
    plugins: { "my-plugin": plugin },
    rules: { "my-plugin/rule1": "error" },
  }]),
});

export default plugin;
```

For legacy and dual-format plugins, see [references/plugin-templates.md](references/plugin-templates.md).

## Required Test Coverage

| Category | Purpose |
|----------|---------|
| Main case | Core transformation |
| No-op | Unrelated code unchanged |
| Idempotency | Already-fixed code stays fixed |
| Edge cases | Variations from spec |
| Options | Different configurations |

## Quick Reference

### Rule Types

| Type | Use Case |
|------|----------|
| `problem` | Code that causes errors |
| `suggestion` | Style improvements |
| `layout` | Whitespace/formatting |

### Fixer Methods

```typescript
fixer.replaceText(node, "new")
fixer.insertTextBefore(node, "prefix")
fixer.insertTextAfter(node, "suffix")
fixer.remove(node)
fixer.replaceTextRange([start, end], "new")
```

### Common Selectors

```typescript
"CallExpression[callee.name='target']"     // Function call by name
"MemberExpression[property.name='prop']"   // Property access
"ImportDeclaration[source.value='pkg']"    // Import from package
"Identifier[name='forbidden']"             // Identifier by name
":not(CallExpression)"                     // Negation
"FunctionDeclaration:exit"                 // Exit visitor
```

## References

- [Code Patterns](references/code-patterns.md) - AST selectors, fixer API, reporting, context API
- [Test Patterns](references/test-patterns.md) - RuleTester setup for Bun/Vitest/Jest, test cases
- [Plugin Templates](references/plugin-templates.md) - Flat config, legacy, dual-format structures
- [Troubleshooting](references/troubleshooting.md) - Common issues, debugging techniques

## External Tools

- **AST Explorer**: https://astexplorer.net (select @typescript-eslint/parser)
- **ast-grep**: `sg --lang ts -p 'pattern'` for structural searches
