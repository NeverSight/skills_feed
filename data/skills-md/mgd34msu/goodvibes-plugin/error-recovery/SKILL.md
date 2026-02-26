---
name: error-recovery
description: "ALWAYS load before starting any task. Defines systematic recovery procedures when things go wrong during execution. Covers tool failures, build errors, test failures, type errors, and unexpected runtime results. Includes tiered escalation (retry, fallback, memory-informed diagnosis, orchestrator escalation) and post-recovery logging to prevent recurrence."
metadata:
  version: 1.0.0
  category: protocol
  tags: [error, recovery, escalation, debugging, failure, retry]
---

## Resources
```
scripts/
  validate-error-recovery.sh
references/
  common-errors.md
```

# Error Recovery Protocol

When tasks fail, agents must follow a systematic recovery process that balances efficiency with thoroughness. This skill defines how to categorize errors, leverage institutional memory, apply multi-source recovery strategies, and know when to escalate.

## Immediate Response

When an error occurs during task execution:

1. **DO NOT retry blindly**. Read the full error message, stack trace, and any diagnostic output.

2. **Categorize the error** into one of six types:
   - **TOOL_FAILURE** -- Precision tool or MCP tool returned an error
   - **BUILD_ERROR** -- Build/compile command failed (npm, tsc, vite, etc.)
   - **TEST_FAILURE** -- Test suite failed (vitest, jest, etc.)
   - **TYPE_ERROR** -- TypeScript type checking failed
   - **RUNTIME_ERROR** -- Code crashed during execution
   - **EXTERNAL_ERROR** -- Third-party service or API failure

3. **Check `.goodvibes/memory/failures.json`** for matching keywords using precision_read:
   - Search for keywords from the error message
   - If a matching failure is found, apply the documented `resolution`
   - If the resolution doesn't work, note it and proceed to recovery phases
   - If not found, proceed directly to recovery phases

## Error Categories: Detailed Guidance

### TOOL_FAILURE

**Common Causes:**
- Wrong file path (absolute vs relative, typo, file doesn't exist)
- Bad syntax in tool parameters (malformed JSON, incorrect regex)
- Sandbox blocking external paths
- Missing required parameters
- Tool used incorrectly (wrong extract mode, wrong output format)

**Recovery Steps:**
1. Re-read the tool's schema and parameter descriptions
2. Check if the file/path exists using precision_glob
3. Verify sandbox settings with precision_config get (check `sandbox.enabled`)
4. For precision tools, check if you're using the right extract/output mode
5. Try the operation with minimal parameters first, then add complexity
6. If precision tool fails repeatedly, check if it's a user error vs actual tool bug:
   - User error: wrong params, bad path, misunderstood tool behavior
   - Tool bug: correct params but tool crashes or returns wrong result
7. For user errors, fix and retry with precision tools
8. For tool bugs, use native tool fallback ONLY for that specific operation, then return to precision tools

**Common Patterns from Memory:**
- **Format/mode mismatch**: MCP schema sends `output.format`, handlers read `output.mode`. Always check both with `??`.
- **Ripgrep glob failures**: Patterns like `src/**/*.ts` fail silently with ripgrep. Use regex to detect literal prefixes and force fast-glob.
- **Path normalization**: Ripgrep returns absolute OR relative paths. Always use `path.isAbsolute()` before `path.resolve()`.
- **Sandbox opt-in**: Only enable when `sandbox === true || sandbox === 'true'`. Never use `=== false` checks.

### BUILD_ERROR

**Common Causes:**
- Missing dependencies (not installed, wrong version)
- Type errors not caught during editing
- Import errors (wrong path, circular dependency)
- Configuration errors (tsconfig, vite.config, etc.)
- Environment variable missing

**Recovery Steps:**
1. Read the full build output (use precision_exec with expect.exit_code to capture stderr)
2. Identify the first error in the chain (subsequent errors are often cascading)
3. For missing deps: Check package.json, run `npm install`
4. For type errors: See TYPE_ERROR section below
5. For import errors: Verify file exists, check import path, look for circular deps
6. For config errors: Compare with working examples in the codebase
7. Search first-party docs for the framework/build tool being used

### TEST_FAILURE

**Common Causes:**
- Wrong test assertions (expected value changed)
- Missing mocks or stubs
- Changed API contract (function signature, return type)
- Test environment not set up correctly
- Async timing issues

**Recovery Steps:**
1. Read the test failure output (assertion error, expected vs actual)
2. Identify which test file and specific test case failed
3. Read the test file to understand what it's testing
4. Read the implementation to see if it matches the test expectations
5. Determine if the test is wrong or the implementation is wrong:
   - If implementation changed intentionally -> update the test
   - If implementation broke -> fix the implementation
6. For async issues, check for missing `await`, improper use of `done()`, or race conditions
7. For environment issues, check test setup files (vitest.config, jest.setup.js)

### TYPE_ERROR

**Common Causes:**
- Unsafe member access (`obj.prop` where `obj` could be null/undefined)
- Type mismatch in assignments (`string` assigned to `number`)
- Wrong function call signature (missing params, wrong types)
- Unsafe `any` usage escaping type system
- Generic constraints violated

**Recovery Steps:**
1. Read the TypeScript error message (it includes file, line, and specific type issue)
2. Use the `explain_type_error` analysis-engine tool if available
3. For member access: Add optional chaining (`?.`) or null check
4. For assignments: Fix the type at the source or use proper type assertion
5. For function calls: Check the function signature and provide correct arguments
6. For `any` escapes: Replace `any` with proper types
7. For generics: Ensure type parameters satisfy constraints

**Common Patterns:**
- Add type guards: `if (obj && 'prop' in obj)`
- Use optional chaining: `obj?.prop?.nestedProp`
- Narrow types with discriminated unions
- Use type predicates for custom guards

### RUNTIME_ERROR

**Common Causes:**
- Null/undefined access (property of null, calling undefined as function)
- Unhandled promise rejections
- Uncaught exceptions
- Missing environment variables
- Network failures (fetch, API calls)
- File system errors (ENOENT, EACCES)

**Recovery Steps:**
1. Read the stack trace to find the exact line that failed
2. Identify the root cause (null access, missing env var, network, etc.)
3. For null/undefined: Add runtime checks or use optional chaining
4. For promises: Add `.catch()` handlers or `try/catch` around `await`
5. For env vars: Check `.env` files, verify they're loaded
6. For network: Add retry logic, check credentials, verify URL
7. For file system: Verify paths exist, check permissions

**Common Patterns:**
- Add error boundaries in React components
- Use `try/catch` around all `await` expressions
- Validate env vars at startup
- Add defensive checks: `if (!value) throw new Error('...')`

### EXTERNAL_ERROR

**Common Causes:**
- Authentication expired or invalid (401)
- Rate limit exceeded (429)
- Service down or unreachable (503, ECONNREFUSED)
- Invalid API request (400)
- Quota exceeded

**Recovery Steps:**
1. Check the error status code or message
2. For auth errors (401): Check credentials in `.goodvibes/secrets/`, verify token hasn't expired
3. For rate limits (429): Implement exponential backoff, check if quota can be increased
4. For service down (503): Retry with backoff, check service status page
5. For bad requests (400): Read API docs, verify request format
6. For quota: Check usage dashboard, request increase, or wait for reset

**Common Patterns:**
- Exponential backoff: 1s, 2s, 4s, 8s
- Check service status via precision_fetch to status endpoint
- Rotate API keys if multiple are available
- Cache responses to reduce API calls

## Recovery Strategy: One-Shot Multi-Source

After categorizing the error and checking failures.json, use a **one-shot strategy** where you consult ALL knowledge sources simultaneously (not sequentially) and apply the best solution:

1. **Internal knowledge** -- your training data, codebase patterns (discover, precision_grep, precision_read), GoodVibes memory
2. **First-party docs** -- official documentation, API references, changelogs, migration guides
3. **Community knowledge** -- Stack Overflow, GitHub Issues, forums
4. **Open internet** -- broader web search for edge cases

### Applying the Best Solution

Once you've consulted all sources:
1. **Evaluate solutions** based on:
   - Recency (prefer solutions from similar versions)
   - Authority (official docs > community > random blog)
   - Specificity (exact error match > general guidance)
   - Project fit (matches your stack and patterns)

2. **Apply the solution** completely:
   - Don't half-apply a fix
   - Make all related changes at once
   - Use precision_edit for changes, not incremental tweaks

3. **Validate the fix**:
   - Re-run the failing operation
   - Run related tests with precision_exec
   - Check for new errors introduced

## After Resolution

Once you've successfully resolved the error:

### 1. Log to `.goodvibes/memory/failures.json`

Use precision_edit to append a new entry with:

```json
{
  "id": "fail_YYYYMMDD_HHMMSS",
  "date": "ISO-8601 timestamp",
  "error": "Brief description of the error",
  "context": "What was being attempted when error occurred",
  "root_cause": "Why it happened (technical explanation)",
  "resolution": "How it was fixed (specific steps taken)",
  "prevention": "How to avoid this in the future",
  "keywords": ["relevant", "search", "terms"]
}
```

**Example:**
```json
{
  "id": "fail_20260215_143000",
  "date": "2026-02-15T14:30:00Z",
  "error": "precision_read returns 'file not found' for valid path",
  "context": "Reading component file at src/components/Button.tsx",
  "root_cause": "Path was relative, but precision tools require absolute paths. Sandbox was enabled, blocking CWD resolution.",
  "resolution": "RESOLVED - Used absolute path with process.cwd() to create absolute path before calling precision_read.",
  "prevention": "Always use absolute paths with precision tools. Use path.resolve() to convert relative to absolute.",
  "keywords": ["precision_read", "path", "absolute", "relative", "sandbox", "file-not-found"]
}
```

### 2. Log to `.goodvibes/logs/errors.md`

Append a markdown entry using precision_edit:

```markdown
## [YYYY-MM-DD HH:MM] ERROR_CATEGORY: Brief Description

**Error**: Full error message

**Context**: What was being done

**Resolution**: How it was fixed

**Time to resolve**: X minutes

---
```

### 3. Continue with the task

Once logged, return to the original task. Don't wait for confirmation.

## After Max Attempts (3 attempts)

If you've tried to fix the error 3 times and it's still failing:

### 1. Log the unresolved failure

Add to failures.json with `"resolution": "UNRESOLVED - <what was tried>"`:

```json
{
  "id": "fail_20260215_143500",
  "date": "2026-02-15T14:35:00Z",
  "error": "Vitest tests hang indefinitely on CI",
  "context": "Running npm run test in CI pipeline",
  "root_cause": "Unknown - tests pass locally but hang in CI environment",
  "resolution": "UNRESOLVED - Tried: 1) Added --no-watch flag, 2) Increased timeout to 60s, 3) Disabled coverage collection. Tests still hang.",
  "prevention": "Need deeper investigation into CI environment differences",
  "keywords": ["vitest", "ci", "hang", "timeout", "unresolved"]
}
```

### 2. Report to orchestrator

Use structured format in your response:

```markdown
## Task Status: BLOCKED

### Error
[ERROR_CATEGORY] Brief description

### Attempts Made
1. **Attempt 1**: What was tried -> Result
2. **Attempt 2**: What was tried -> Result
3. **Attempt 3**: What was tried -> Result

### Root Cause Analysis
Best guess at why this is failing based on investigation.

### Suggested Next Steps
- Option 1: [Describe approach that requires different permissions/access]
- Option 2: [Describe alternative architecture/design decision]
- Option 3: [Describe manual intervention needed]

### Files Changed
- `path/to/file.ts` - [what was changed during troubleshooting]
```

### 3. Do NOT mark task as complete

Leave the task in BLOCKED state. The orchestrator will decide whether to:
- Escalate to user
- Try a different approach
- Assign to a different agent with different capabilities
- Defer the task

## Immediate Escalation (Skip Recovery)

For certain error types, **do NOT attempt recovery**. Escalate immediately to the orchestrator:

### 1. Permission Errors

```bash
EACCES: permission denied
EPERM: operation not permitted
```

**Why**: These require user intervention to grant permissions. Agents can't fix this.

**Escalate with**: "Permission error encountered. Need user to: [grant file access / run as sudo / change ownership]."

### 2. Missing Credentials/Secrets

```
Error: OPENAI_API_KEY is not defined
Error: Database connection failed: authentication error
401 Unauthorized
```

**Why**: Agents can't create or modify secrets. Only users can provide credentials.

**Escalate with**: "Missing credential: [ENV_VAR_NAME or service name]. User needs to provide via .env or secrets management."

### 3. Architectural Ambiguity

```
Context clues indicate multiple valid approaches:
- Use REST API vs GraphQL
- Use Prisma vs Drizzle
- Component composition pattern unclear
```

**Why**: These are design decisions that affect the broader system. Agents shouldn't make architectural choices unilaterally.

**Escalate with**: "Architectural decision required: [describe the choice]. Options: [list 2-3 options with tradeoffs]."

### 4. Scope Change Discovered

```
Original task: "Add user profile page"
Discovered: Requires new database schema, auth changes, API endpoints
```

**Why**: The task is larger than originally scoped. Orchestrator needs to re-plan.

**Escalate with**: "Scope expansion discovered. Original: [task]. Required: [new dependencies/changes]. Recommend: [break into subtasks / get user approval]."

## Summary

**When errors occur:**
1. Categorize immediately (TOOL_FAILURE, BUILD_ERROR, etc.)
2. Check failures.json for known patterns
3. Use one-shot multi-source recovery (internal + docs + community + web)
4. Apply the best solution completely
5. Log resolution to failures.json and errors.md
6. Continue with task

**After 3 attempts:**
1. Log as UNRESOLVED
2. Report to orchestrator with structured summary
3. Do NOT mark task complete

**Escalate immediately for:**
1. Permission errors
2. Missing credentials
3. Architectural ambiguity
4. Scope changes

**Remember:**
- Precision tools are the default, native tools are the fallback
- User error != tool failure
- Recovery attempts should be systematic, not random
- Memory is institutional knowledge -- use it and contribute to it
