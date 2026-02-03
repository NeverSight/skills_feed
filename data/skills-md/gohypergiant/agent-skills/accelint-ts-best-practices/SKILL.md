---
name: accelint-ts-best-practices
description: Comprehensive TypeScript/JavaScript coding standards focusing on type safety, defensive programming, and code correctness. Use when (1) Writing or reviewing TS/JS code, (2) Fixing type errors or avoiding any/enum/null, (3) Implementing control flow, state management, or error handling, (4) Applying zero-value pattern or immutability, (5) Code review for TypeScript anti-patterns. Covers naming conventions, function design, return values, bounded iteration, input validation. For performance optimization, use accelint-ts-performance skill. For documentation, use accelint-ts-documentation skill.
license: Apache-2.0
metadata:
  author: accelint
  version: "1.0"
---

# JavaScript and TypeScript Best Practices

Comprehensive coding standards for JavaScript and TypeScript applications, designed for AI agents and LLMs working with modern JavaScript/TypeScript codebases.

**Note:** This skill focuses on general best practices, TypeScript patterns, and safety. For performance optimization, use the `accelint-ts-performance` skill instead.

## When to Use This Skill

This skill provides expert-level patterns for JavaScript and TypeScript code. Load [AGENTS.md](AGENTS.md) to scan rule summaries and identify relevant optimizations for your task.

## How to Use

This skill uses a **progressive disclosure** structure to minimize context usage:

### 1. Start with the Overview (AGENTS.md)
Read [AGENTS.md](AGENTS.md) for a concise overview of all rules with one-line summaries organized by category.

### 2. Load Specific Rules as Needed
When you identify a relevant pattern or issue, load the corresponding reference file for detailed implementation guidance:

**Quick Start:**
- [quick-start.md](references/quick-start.md) - Complete workflow examples with before/after code

**General Best Practices:**
- [naming-conventions.md](references/naming-conventions.md) - Descriptive names, qualifier ordering, boolean prefixes
- [functions.md](references/functions.md) - Function size, parameters, explicit values
- [control-flow.md](references/control-flow.md) - Early returns, flat structure, block style
- [state-management.md](references/state-management.md) - const vs let, immutability, pure functions
- [return-values.md](references/return-values.md) - Return zero values instead of null/undefined
- [misc.md](references/misc.md) - Line endings, defensive programming, technical debt
- [code-duplication.md](references/code-duplication.md) - Extract common patterns, DRY principle, when to consolidate

**TypeScript:**
- [any.md](references/any.md) - Avoid any, use unknown or generics
- [enums.md](references/enums.md) - Use as const objects instead of enum
- [type-vs-interface.md](references/type-vs-interface.md) - Prefer type over interface

**Safety:**
- [input-validation.md](references/input-validation.md) - Validate external data with schemas
- [assertions.md](references/assertions.md) - Split assertions, include values
- [error-handling.md](references/error-handling.md) - Handle all errors explicitly
- [error-messages.md](references/error-messages.md) - User-friendly vs developer-specific messages

**Performance:**
- **For performance optimization tasks**, use the `accelint-ts-performance` skill for comprehensive profiling workflows and optimization patterns

**Documentation:**
- **For documentation tasks**, use the `accelint-ts-documentation` skill for comprehensive JSDoc and comment guidance

### 3. Apply the Pattern
Each reference file contains:
- ❌ Incorrect examples showing the anti-pattern
- ✅ Correct examples showing the optimal implementation
- Explanations of why the pattern matters

### 4. Use the Audit Report Template (For Explicit Audit Requests)
When users explicitly request a code correctness audit or invoke the skill directly (`/accelint-ts-best-practices <path>`), use the standardized report format:

**Template:** [`assets/audit-report-template.md`](assets/audit-report-template.md)
**Example:** [`assets/audit-report-example.md`](assets/audit-report-example.md)

The audit report format provides:
- Executive Summary with impact assessment
- Severity levels (Critical, High, Medium, Low) for prioritization
- Impact analysis (potential bugs, type safety, maintainability, runtime failures)
- Categorization (Type Safety, Safety, State Management, Return Values, Code Quality)
- Pattern references linking to detailed guidance in references/
- Phase 2 summary table for tracking all issues

**When to use the audit template:**
- Skill invoked directly via `/accelint-ts-best-practices <path>`
- User explicitly requests "code audit", "audit code correctness", or "check for best practices violations"
- User asks to "review code quality" across file(s)

**When NOT to use the audit template:**
- User asks to "fix this type error" (direct implementation)
- User asks "what's wrong with this code?" (answer the question)
- User requests specific fixes (apply fixes directly without formal report)

