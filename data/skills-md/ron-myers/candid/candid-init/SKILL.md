---
name: candid-init
description: Generate Technical.md and config.json by deeply analyzing your codebase structure, architecture, and patterns
---

# Technical.md and Config Generator

You are a senior technical architect conducting a thorough codebase audit. Your job is to generate a Technical.md that:

1. **References specific files and paths** from this project
2. **Captures architecture decisions** and how to enforce them
3. **Documents actual patterns** found in the code with examples
4. **Identifies gaps** between current state and best practices

The output should feel like it was written by someone who spent days understanding THIS specific codebase - not a generic template.

## Effort Levels

| Level | Time | Analysis | Output |
|-------|------|----------|--------|
| `quick` | ~30 sec | Grep/find pattern detection | ~50 lines |
| `medium` | ~1-2 min | + Read 5-8 key files | ~150 lines |
| `thorough` | ~5-10 min | + Sub-agents read ALL files | ~500 lines |

**Default: thorough**

### Thorough Mode Architecture

**Phase 1: Analysis Sub-Agents (parallel)**
Launch 5 Explore agents to analyze the entire codebase:
- **Architecture Agent**: Reads all controllers/services/repos, maps dependencies
- **Naming Agent**: Reads 20-30 files, extracts conventions
- **Error/Security Agent**: Reads all error handling and auth code
- **Testing Agent**: Reads all test files
- **Framework Agent**: Reads all React components or API routes

**Phase 2: Generation Sub-Agents (parallel)**
Launch 5 generation agents, each writing one section (~80-120 lines):
- Architecture Section (~100 lines)
- Naming & Style Section (~80 lines)
- Error Handling & Logging Section (~80 lines)
- Testing Section (~80 lines)
- Security & Framework Section (~100 lines)

**Phase 3: Synthesis**
Combine all sections + header/footer = ~500 line Technical.md

This two-phase approach works well with Claude Code because:
- Opus handles complex synthesis and generation
- Sonnet (via Explore agents) handles efficient file reading
- Parallel execution maximizes throughput
- Each agent has focused scope, preventing context overload

---

## Workflow

### Step 1: Check for Existing Files (Fail-Fast)

```bash
ls .candid/Technical.md .candid/config.json 2>/dev/null
```

If Technical.md exists, ask user: "Overwrite", "Create as .new", or "Cancel"
If config.json exists, ask user: "Overwrite", "Keep existing", or "Cancel"

### Step 2: Determine Effort Level

Check for `--effort` flag. Default is `thorough`.

### Step 3: Detect Framework

```bash
cat package.json 2>/dev/null | head -50
ls requirements.txt pyproject.toml go.mod Cargo.toml 2>/dev/null
```

| Detection | Framework |
|-----------|-----------|
| package.json with react/next/vue | React |
| package.json without frontend | Node.js |
| requirements.txt or pyproject.toml | Python |
| go.mod | Go |
| Cargo.toml | Rust |
| None | Minimal |

### Step 4: Detect Existing Tooling

```bash
ls .eslintrc* eslint.config.* .prettierrc* biome.json tsconfig.json .flake8 ruff.toml 2>/dev/null
```

**Critical:** If linters exist, SKIP all rules they enforce. Focus Technical.md on what linters CANNOT check: architecture, domain rules, patterns.

---

## Step 5: Deep Codebase Analysis

This is the core of generating project-specific rules. Execute based on effort level.

### 5.1 Directory Structure Analysis (All Levels)

```bash
# Get full directory tree (3 levels)
find . -type d -maxdepth 3 | grep -v node_modules | grep -v .git | grep -v __pycache__ | grep -v venv | grep -v dist | grep -v build | sort

# Identify key directories
ls -d src/*/ lib/*/ app/*/ packages/*/ 2>/dev/null | head -20
```

**Extract:**
- Layer structure: Are there `controllers/`, `services/`, `repositories/`, `models/`?
- Feature structure: Are there `features/`, `modules/`, domain directories?
- Shared code: Is there `shared/`, `common/`, `utils/`, `lib/`?

### 5.2 File Naming Patterns (All Levels)

```bash
# File suffixes
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" \) 2>/dev/null | grep -v node_modules | sed 's/.*\///' | grep -oE '\.[a-z]+\.(ts|tsx|js)$' | sort | uniq -c | sort -rn | head -15

# Class/component naming
grep -rhoE "^export (default )?(class|function|const) [A-Z][a-zA-Z]+" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v node_modules | head -30
```

### 5.3 Import Graph Analysis (Medium + Thorough)

**This is critical for architecture rules.**

```bash
# What imports what - build mental model of dependencies
grep -rh "^import.*from" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v node_modules | grep -oE "from ['\"][^'\"]+['\"]" | sort | uniq -c | sort -rn | head -30

# Check for layer violations (controllers importing repos, etc.)
# If src/controllers/ exists, check what it imports
grep -rh "^import.*from" src/controllers/ --include="*.ts" 2>/dev/null | grep -v node_modules | head -20

# If src/services/ exists, check what it imports
grep -rh "^import.*from" src/services/ --include="*.ts" 2>/dev/null | grep -v node_modules | head -20

# Check for cross-module imports (feature A importing from feature B)
grep -rh "^import.*from.*features/" --include="*.ts" 2>/dev/null | grep -v node_modules | head -20

# Path aliases in use
grep -rh "from '@/\|from '~/\|from 'src/\|from '#" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v node_modules | head -10
```

### 5.4 Architecture Pattern Detection (Thorough Only)

```bash
# Barrel exports (index.ts files)
find . -name "index.ts" -o -name "index.js" 2>/dev/null | grep -v node_modules | wc -l
# Sample a few to see export patterns
find . -name "index.ts" 2>/dev/null | grep -v node_modules | head -3 | xargs cat 2>/dev/null

# Dependency injection patterns
grep -rh "@Injectable\|@Inject\|constructor.*private\|createContext" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v node_modules | head -15

# Middleware/decorator patterns
grep -rh "@.*Middleware\|@Guard\|@Interceptor\|@UseGuards\|@Auth" --include="*.ts" 2>/dev/null | grep -v node_modules | head -10

# Domain boundaries (look for domain-specific directories)
find . -type d -name "billing" -o -name "auth" -o -name "users" -o -name "payments" -o -name "orders" 2>/dev/null | grep -v node_modules | head -10
```

### 5.5 Error Handling Analysis (Medium + Thorough)

```bash
# Custom error classes
grep -rh "class.*Error\|extends Error\|extends.*Error" --include="*.ts" 2>/dev/null | grep -v node_modules | head -15

# Error response patterns
grep -rh "res.status.*json\|throw new\|catch.*error" --include="*.ts" 2>/dev/null | grep -v node_modules | head -20

# Error handling location (where are errors caught?)
grep -rl "try.*catch\|\.catch(" --include="*.ts" 2>/dev/null | grep -v node_modules | head -20
```

### 5.6 Testing Patterns (Medium + Thorough)

```bash
# Test file locations
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" 2>/dev/null | grep -v node_modules | head -20

# Test organization (colocated vs separate)
ls -d **/__tests__/ **/tests/ test/ tests/ 2>/dev/null | head -10

# Test naming patterns
grep -rh "describe(\|it(\|test(" --include="*.test.*" --include="*.spec.*" 2>/dev/null | grep -v node_modules | head -15

# Mock patterns
grep -rh "jest.mock\|vi.mock\|sinon\|@Mock" --include="*.test.*" --include="*.spec.*" 2>/dev/null | grep -v node_modules | head -10
```

### 5.7 API Patterns (Medium + Thorough, for Node/Backend)

```bash
# Route definitions
grep -rh "router\.\|app\.\(get\|post\|put\|patch\|delete\)\|@Get\|@Post\|@Put\|@Delete" --include="*.ts" 2>/dev/null | grep -v node_modules | head -20

# Validation patterns
grep -rh "from 'zod'\|from 'yup'\|from 'joi'\|@IsString\|@IsNumber\|z\.object\|Joi\.object" --include="*.ts" 2>/dev/null | grep -v node_modules | head -10

# Auth middleware
grep -rh "auth.*middleware\|isAuthenticated\|requireAuth\|@Auth\|@UseGuards" --include="*.ts" 2>/dev/null | grep -v node_modules | head -10
```

### 5.8 React Patterns (Medium + Thorough, for React)

```bash
# Hook patterns
find . -name "use*.ts" -o -name "use*.tsx" 2>/dev/null | grep -v node_modules | head -15

# State management
grep -rh "from 'redux'\|from 'zustand'\|from '@tanstack/react-query'\|from 'swr'\|createContext\|useReducer" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v node_modules | head -10

# Component patterns
grep -rh "React.memo\|forwardRef\|React.lazy\|Suspense" --include="*.tsx" 2>/dev/null | grep -v node_modules | head -10

# Event handler naming
grep -rhoE "(handle|on)[A-Z][a-zA-Z]*" --include="*.tsx" 2>/dev/null | grep -v node_modules | sort | uniq -c | sort -rn | head -15
```

### 5.9 TypeScript Analysis (Thorough Only)

```bash
# Strictness
cat tsconfig.json 2>/dev/null | grep -E "strict|noImplicit"

# Any usage (red flag)
grep -rc ": any\|as any" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v node_modules | grep -v ":0$" | awk -F: '{sum+=$2} END {print "any/as any count:", sum}'

# Interface vs type preference
grep -rc "^interface \|^export interface " --include="*.ts" 2>/dev/null | grep -v node_modules | awk -F: '{sum+=$2} END {print "interfaces:", sum}'
grep -rc "^type \|^export type " --include="*.ts" 2>/dev/null | grep -v node_modules | awk -F: '{sum+=$2} END {print "types:", sum}'
```

---

## Step 6: File Analysis

How files are analyzed depends on effort level.

### Medium Mode: Read 5-8 Key Files

Use the Read tool to examine representative files:
- Entry points (1-2): `src/index.ts`, `app/layout.tsx`
- Most-imported modules (2-3): from import analysis
- One file per layer (2-3): controller, service, repository

Extract: naming patterns, error handling, import organization, examples to cite.

### Thorough Mode: Sub-Agent Comprehensive Analysis

**Launch 3-5 sub-agents IN PARALLEL** to analyze ALL files in the codebase. Each agent focuses on a specific domain and returns proposed rules with evidence.

Use the Task tool with `subagent_type: "Explore"` for each agent.

#### Agent 1: Architecture & Imports Agent

**Prompt:**
```
Analyze the architecture and import patterns in this codebase.

READ all files in these directories (or equivalent):
- src/controllers/, src/routes/, app/api/
- src/services/, src/usecases/
- src/repositories/, src/data/
- src/models/, src/entities/

For each file, examine:
1. What does this file import?
2. What layer is it in?
3. Are there violations (controller importing repo directly)?

Return:
- Layer structure diagram (what directories = what layers)
- Dependency rules (what can import what)
- Violations found (specific file:line examples)
- 3-5 proposed architecture rules with file path examples
```

#### Agent 2: Naming & Style Agent

**Prompt:**
```
Analyze naming conventions and code style across the codebase.

READ 20-30 representative files across:
- Components/UI files
- Services/business logic
- Utilities/helpers
- Tests

For each file, extract:
1. Class/function/variable naming patterns
2. File naming patterns
3. Event handler naming (handle* vs on*)
4. Boolean naming (is*, has*, should*)

Return:
- Detected naming conventions with consistency %
- Specific file examples for each pattern
- 5-8 proposed naming rules with examples from actual files
```

#### Agent 3: Error Handling & Security Agent

**Prompt:**
```
Analyze error handling and security patterns.

READ all files that:
- Define custom error classes
- Have try/catch blocks
- Handle API responses
- Deal with authentication/authorization
- Process user input

For each file, examine:
1. Error class hierarchy
2. Error response format
3. Where errors are caught (boundary vs distributed)
4. Input validation patterns
5. Auth patterns

Return:
- Error handling approach summary
- Security patterns found (or gaps)
- Specific file:line examples
- 5-8 proposed error/security rules with evidence
```

#### Agent 4: Testing Patterns Agent

**Prompt:**
```
Analyze testing patterns across the codebase.

READ all test files (*.test.*, *.spec.*, *_test.*).

For each test file, examine:
1. Test organization (describe/it patterns)
2. Setup patterns (beforeEach, fixtures, factories)
3. Mocking approach
4. Assertion patterns
5. What's tested vs what's not

Return:
- Test organization pattern
- Naming conventions
- Coverage gaps (directories without tests)
- 3-5 proposed testing rules with examples
```

#### Agent 5: Framework-Specific Agent (React/Node/Python)

**For React:**
```
Analyze React patterns across all components.

READ all .tsx files and custom hooks.

Examine:
1. Component structure patterns
2. Hook usage patterns
3. State management approach
4. Props patterns
5. Performance patterns (memo, useCallback, useMemo)

Return:
- Component architecture patterns
- State management approach
- 5-8 proposed React rules with component examples
```

**For Node.js:**
```
Analyze API and backend patterns.

READ all route handlers, middleware, and API files.

Examine:
1. Route organization
2. Middleware patterns
3. Validation approach
4. Response format
5. Database access patterns

Return:
- API design patterns
- Middleware usage
- 5-8 proposed API rules with endpoint examples
```

#### Synthesizing Agent Results

After all agents complete, **synthesize their findings**:

1. **Collect all proposed rules** from each agent
2. **Deduplicate** similar rules (keep the one with best evidence)
3. **Prioritize** rules by:
   - How many files follow the pattern (consistency)
   - Security impact
   - Architecture importance
4. **Select top 40-60 rules** for the Technical.md
5. **Organize by category** (Architecture, Naming, Error Handling, etc.)

---

## Step 7: Architecture Analysis (Thorough Only)

This creates the architecture rules that make Technical.md valuable.

### 7.1 Layer Boundary Analysis

Based on directory structure and import analysis, determine:

```
Layer Structure Detected:
├── src/controllers/  → HTTP layer (should only import services)
├── src/services/     → Business logic (can import repos, not controllers)
├── src/repositories/ → Data access (can import models, not services)
└── src/models/       → Data models (no internal imports)
```

**Generate rules like:**
- "Controllers in `src/controllers/` must not import from `src/repositories/` directly - go through services"
- "Services in `src/services/` must not import from `src/controllers/`"

### 7.2 Module Boundary Analysis

If feature-based structure detected:

```
Module Structure Detected:
├── src/features/auth/     → Authentication domain
├── src/features/billing/  → Billing domain
├── src/features/users/    → User management
└── src/shared/            → Shared utilities
```

**Check for cross-module imports and generate rules:**
- "Feature modules must not import from each other directly. Use `src/shared/` for cross-cutting concerns"
- "The `billing/` module must not import from `auth/` (separation of concerns)"

### 7.3 Detect Violations

Look for actual violations in the codebase:

```bash
# Example: Find files in controllers/ that import from repositories/
grep -rl "from.*repository\|from.*repositories" src/controllers/ 2>/dev/null
```

**If violations found, note them:**
- "Architecture violation found: `src/controllers/UserController.ts` imports directly from `UserRepository`. Refactor to use `UserService`."

---

## Step 8: Gap Analysis (Thorough Only)

Compare detected patterns to best practices. For each category, identify gaps.

### Security Gaps

| Best Practice | Check | If Missing |
|--------------|-------|------------|
| Input validation at boundary | Look for zod/joi/yup | "Consider adding Zod for input validation at API boundaries" |
| Parameterized queries | Check for raw SQL strings | "Found raw SQL in X. Use parameterized queries." |
| Auth middleware | Check route protection | "Not all routes appear to have auth checks" |
| Secret management | Check for hardcoded values | "Found potential hardcoded secret in X" |

### Error Handling Gaps

| Best Practice | Check | If Missing |
|--------------|-------|------------|
| Custom error classes | Look for extends Error | "No custom error classes found. Consider adding AppError hierarchy." |
| Consistent error format | Check response patterns | "Error responses use inconsistent formats across files" |
| Error logging | Check for logger usage | "Errors caught but not logged in X files" |

### Testing Gaps

| Best Practice | Check | If Missing |
|--------------|-------|------------|
| Tests exist | Find test files | "No tests found for `src/services/`" |
| Test organization | Check patterns | "Tests use inconsistent naming (mix of .test.ts and .spec.ts)" |

### TypeScript Gaps

| Best Practice | Check | If Missing |
|--------------|-------|------------|
| Strict mode | Check tsconfig | "strict mode not enabled. Consider enabling for new code." |
| No any | Count any usage | "Found 47 uses of `any`. Consider typing or using `unknown`." |

---

## Step 9: Generate Technical.md (Thorough Mode: Use Generation Sub-Agents)

For thorough mode, generate a comprehensive **~500 line** Technical.md by launching **generation sub-agents in parallel**. Each agent writes one major section with full detail.

### Generation Strategy for Claude Code

**Key insight:** Claude Code with Opus/Sonnet can generate long, detailed output when:
1. Each section is generated independently by a focused sub-agent
2. Agents have specific analysis results to work from
3. Final synthesis combines sections without truncation

### Launch 5 Generation Sub-Agents IN PARALLEL

Use the Task tool to launch these agents simultaneously. Each generates ~80-120 lines.

#### Generation Agent 1: Architecture Section (~100 lines)

**Prompt:**
```
Generate the Architecture section of a Technical.md file.

Use these analysis results:
[Paste layer structure, import graph, violations from analysis agents]

Write ~100 lines covering:

## Architecture

### Project Structure Overview
- Full directory tree with annotations explaining each directory's purpose
- Which directories are entry points, which are internal

### Layer Architecture
- Detailed layer diagram with all detected layers
- What each layer is responsible for
- Dependencies between layers (what can import what)

### Dependency Rules (15-20 specific rules)
For each layer/directory, specify:
- What it CAN import (with path examples)
- What it CANNOT import (with reasoning)
- Example: "`src/controllers/` can import from `src/services/` and `src/middleware/`, NOT from `src/repositories/` or `src/models/` directly"

### Module Boundaries
- Feature/domain boundaries if detected
- Cross-module communication rules
- Shared code location and usage rules

### Current Violations
- List each detected violation with file:line
- Recommended fix for each

### Reference Implementation
- Point to 1-2 files that exemplify correct architecture
```

#### Generation Agent 2: Naming & Code Style Section (~80 lines)

**Prompt:**
```
Generate the Naming Conventions and Code Style section of a Technical.md file.

Use these analysis results:
[Paste naming patterns from analysis agents]

Write ~80 lines covering:

## Naming Conventions

### File Naming (10-15 rules)
For each file type, specify:
- Pattern with regex or glob
- Examples from this codebase
- Counter-examples (what NOT to do)

### Class & Component Naming (10-15 rules)
- Suffixes by type (Service, Controller, Repository, etc.)
- Prefixes if used
- Examples from actual files

### Function & Method Naming (10-15 rules)
- Verb prefixes by purpose (get, set, fetch, handle, on, is, has, etc.)
- Async function naming
- Event handler naming

### Variable Naming (10-15 rules)
- Boolean prefixes
- Constants style
- Collection naming (plural vs singular)
- Destructuring conventions

### Import Organization
- Import ordering rules
- Path alias usage
- Barrel export rules

### Code Examples
Include 2-3 annotated code snippets showing correct naming in context
```

#### Generation Agent 3: Error Handling & Logging Section (~80 lines)

**Prompt:**
```
Generate the Error Handling and Logging section of a Technical.md file.

Use these analysis results:
[Paste error handling patterns from analysis agents]

Write ~80 lines covering:

## Error Handling

### Error Class Hierarchy
- Full hierarchy diagram if exists
- When to use each error type
- How to create new error types

### Error Handling Patterns (15-20 rules)
- Where to catch errors (boundary vs distributed)
- How to wrap errors
- How to add context
- What to log vs what to return

### API Error Responses
- Standard error response format with JSON schema
- HTTP status code mapping
- Error code conventions
- Example responses for common scenarios

### Error Logging
- What context to include
- Log levels by error type
- Sensitive data redaction rules

## Logging

### Log Levels
- When to use each level
- Examples for each

### Structured Logging Format
- Required fields
- Optional fields by context
- Example log entries

### What NOT to Log
- Sensitive data list
- PII handling
```

#### Generation Agent 4: Testing Section (~80 lines)

**Prompt:**
```
Generate the Testing section of a Technical.md file.

Use these analysis results:
[Paste testing patterns from analysis agents]

Write ~80 lines covering:

## Testing

### Test Organization
- File location rules (colocated vs separate)
- Directory structure for different test types
- Naming conventions

### Test Naming (10-15 rules)
- Describe block naming
- Test case naming patterns
- Example test names from codebase

### Unit Tests
- What to unit test
- What NOT to unit test
- Mocking rules
- Assertion patterns

### Integration Tests
- When required
- Setup/teardown patterns
- Database handling
- API testing patterns

### E2E Tests (if applicable)
- Critical paths that require E2E
- Test data management
- Environment setup

### Test Data
- Factory patterns
- Fixture usage
- Test data cleanup

### Coverage Requirements
- Minimum coverage by directory/type
- What's exempt from coverage

### Example Test Structure
Include 1-2 annotated test file examples showing correct patterns
```

#### Generation Agent 5: Security & Framework Section (~100 lines)

**Prompt:**
```
Generate the Security and Framework-Specific sections of a Technical.md file.

Use these analysis results:
[Paste security patterns and framework analysis from analysis agents]

Write ~100 lines covering:

## Security (30-40 rules)

### Input Validation
- Where validation must occur
- Validation library usage
- Schema definition rules
- Example validation code

### Authentication
- Auth middleware usage
- Protected route patterns
- Session/token handling
- Auth bypass (what's public)

### Authorization
- Permission checking patterns
- Role-based access rules
- Resource ownership verification

### Data Protection
- Sensitive data handling
- Encryption requirements
- PII rules

### API Security
- Rate limiting
- CORS configuration
- Request size limits

### Secrets Management
- Environment variable naming
- Secret rotation
- What never goes in code

## [Framework: React/Node/Python]

### [Framework-specific patterns - 30-40 rules]
[Detailed rules based on detected framework]

For React:
- Component patterns
- Hook rules
- State management
- Performance optimization
- Accessibility requirements

For Node:
- API design patterns
- Middleware patterns
- Database access patterns
- Async patterns

For Python:
- Type hints
- Class patterns
- Async patterns
- Documentation requirements
```

### Synthesizing Generated Sections

After all generation agents complete:

1. **Collect all sections** from each agent
2. **Add header and footer**:
   - Header: Project name, generation date, analysis summary
   - Footer: Gaps table, next steps, validation command

3. **Combine into single file** (~500 lines total):
```markdown
# Technical Standards

Standards for [project]. Generated [date] from comprehensive codebase analysis.

**Analysis Summary:**
- Files analyzed: [N]
- Patterns detected: [N]
- Violations found: [N]
- Gaps identified: [N]

---

[Architecture Section from Agent 1]

---

[Naming Section from Agent 2]

---

[Error Handling Section from Agent 3]

---

[Testing Section from Agent 4]

---

[Security & Framework Section from Agent 5]

---

## Gaps vs Best Practices

| Area | Current State | Recommended | Priority |
|------|--------------|-------------|----------|
[Gap table from analysis]

---

## Appendix: File Reference

Key files referenced in this document:
- `src/controllers/UserController.ts` - Example controller
- `src/services/AuthService.ts` - Example service
[etc.]

---

*Generated by candid-init. Run `/candid-validate-standards` to check rule quality.*
```

### Medium/Quick Mode: Condensed Output

For medium mode: Generate ~150 lines (condensed version of above)
For quick mode: Generate ~50 lines (essential rules only)

### Rule Quality Standards

**Every rule MUST:**

1. **Reference specific paths** from this project
   - Good: "Services in `src/services/` must not import from `src/controllers/`"
   - Bad: "Services should not import controllers"

2. **Include actual examples** from the codebase
   - Good: "Event handlers use `handle*` pattern (e.g., `handleUserLogin` in `src/components/LoginForm.tsx`)"
   - Bad: "Event handlers should use consistent naming"

3. **Be measurable/verifiable**
   - Good: "Functions must be under 50 lines"
   - Bad: "Keep functions small"

4. **Note current state if it differs from the rule**
   - Good: "Use custom error classes. (Currently not implemented - see gaps section)"
   - Bad: "Use custom error classes"

### What NOT to Include

- Rules that linters enforce (if ESLint/Prettier detected)
- Generic advice that applies to any project
- Vague terms: "proper", "appropriate", "clean", "good", "best practices"
- Rules without specific paths or examples

---

## Step 10: Generate config.json

Same as before - auto-detect settings from codebase analysis.

---

## Step 11: Write Files and Show Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Candid Initialization Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Technical.md
   Location: .candid/Technical.md
   Analysis: [effort level]

   Architecture rules: [N] (with [M] violations noted)
   Naming conventions: [N] patterns documented
   Error handling: [documented / gap identified]
   Testing: [patterns / gaps]
   Security: [N] rules

   Gaps identified: [N] areas for improvement

⚙️  Configuration
   Location: .candid/config.json

📝 Next Steps
   1. Review architecture rules - ensure they match your intent
   2. Address identified gaps if desired
   3. Run /candid-validate-standards to check rule quality
   4. Run /candid-review to test enforcement
```

---

## Quality Checklist

Before outputting, verify:

- [ ] Architecture section references actual directory paths
- [ ] At least 3 rules cite specific files from this project
- [ ] No vague language ("proper", "appropriate", "clean")
- [ ] Every rule is verifiable (has threshold or specific pattern)
- [ ] Gaps section identifies at least one improvement area
- [ ] Security section is present with project-specific details
- [ ] If linters detected, no rules duplicate their coverage
- [ ] File is 400-500 lines for thorough mode (150 for medium, 50 for quick)
