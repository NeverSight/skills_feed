---
name: precision-mastery
description: "ALWAYS load before starting any task. Maximizes token efficiency for all file operations, searches, and command execution. Covers extract modes (content, outline, symbols, ast, lines), verbosity tuning, multi-file batching, and discover tool orchestration. Ensures agents spend tokens on outcomes, not overhead."
metadata:
  version: 1.0.0
  category: protocol
  tags: [precision, tools, verbosity, batching, token-efficiency, extract-modes]
---

## Resources
```
scripts/
  validate-precision-usage.sh
references/
  tool-reference.md
```

# Precision Mastery

The precision engine provides token-efficient alternatives to native tools (Read, Edit, Write, Grep, Glob, WebFetch). When used correctly, you save 75-95% of tokens on file operations. This skill teaches optimal usage.

## Verbosity Cheat Sheet

Use the lowest verbosity that meets your needs. Verbosity directly impacts token consumption.

| Operation | Default | Recommended | Why |
|----------|---------|-------------|-----|
| `precision_write` | standard | **count_only** | You provided the content; just confirm success |
| `precision_edit` | with_diff | **minimal** | Confirm applied; skip diffs unless debugging |
| `precision_read` | standard | **standard** | You need the content |
| `precision_grep` (discovery) | standard | **files_only** via output.format | Discovery phase, not content phase |
| `precision_grep` (content) | standard | **matches** via output.format | Need actual matched lines |
| `precision_glob` | standard | **paths_only** via output.format | You need file paths, not stats |
| `precision_exec` (verify) | standard | **minimal** | Unless you need full stdout/stderr |
| `precision_exec` (debug) | standard | **standard** | Need output to diagnose |
| `precision_fetch` | standard | **standard** | You need the content |
| `discover` | files_only (verbosity param) | **files_only** | Discovery phase, not content phase |
| `precision_symbols` | locations (verbosity param) | **locations** | File:line is usually enough |

**Token Multipliers**:
- `count_only`: ~0.05x tokens
- `minimal`: ~0.2x tokens
- `standard`: ~0.6x tokens
- `verbose`: 1.0x tokens

**Golden Rule**: Use `count_only` for writes/edits where you don't need to read back what you just wrote.

## Extract Mode Selection (`precision_read`)

Before reading a file, decide what you need from it. Extract modes reduce tokens by 60-95% compared to full content.

| Mode | When to Use | Token Savings | Example Use Case |
|------|------------|--------------|----------------|
| `content` | Need full file to read/understand | 0% | Reading config files, reading code to edit |
| `outline` | Need structure without content | 60-80% | Understanding file organization, finding functions |
| `symbols` | Need exported symbols for imports | 70-90% | Building import statements, API surface analysis |
| `ast` | Need structural patterns | 50-70% | Refactoring, pattern detection |
| `lines` | Need specific line ranges | 80-95% | Reading specific functions after grep |

**Best Practices**:
1. Start with `outline` to understand file structure
2. Use `symbols` when building imports or understanding API surface
3. Use `lines` with `range: { start, end }` after grep finds a location
4. Only use `content` when you actually need the full file

<!-- Example: Understanding a component file -->
```yaml
# Step 1: Get structure
precision_read:
  files: [{ path: "src/components/Button.tsx", extract: outline }]
  verbosity: standard

# Step 2: If you need full content, read it
precision_read:
  files: [{ path: "src/components/Button.tsx", extract: content }]
  verbosity: standard
```

## Batching Patterns

Batching is the single most important token saving technique. Always batch operations when possible.

### 1. Multi-File Read (Single Call)

Read 5-10 files in one `precision_read` call instead of 5-10 separate calls.

```yaml
# Bad (5 separate calls)
precision_read:
  files: [{ path: "file1.ts" }]
precision_read:
  files: [{ path: "file2.ts" }]
# ...

# Good (1 batched call)
precision_read:
  files: [
    { path: "file1.ts", extract: outline },
    { path: "file2.ts", extract: outline },
    { path: "file3.ts", extract: outline },
    { path: "file4.ts", extract: outline },
    { path: "file5.ts", extract: outline }
  ]
  verbosity: minimal
```

### 2. Multi-Query Discover (Single Call)

Run grep + glob + symbols queries simultaneously in one `discover` call. This is the most powerful discovery pattern.

```yaml
discover:
  queries:
    - id: find_components
      type: glob
      patterns: ["src/components/**/*.tsx"]
    - id: find_api_routes
      type: glob
      patterns: ["src/api/**/*.ts", "src/app/api/**/*.ts"]
    - id: find_auth_usage
      type: grep
      pattern: "useAuth|getSession|withAuth"
      glob: "src/**/*.{ts,tsx}"
    - id: find_hooks
      type: symbols
      query: "use"
      kinds: ["function"]
  verbosity: files_only
```

**Why this matters**: Parallel execution means all 4 queries finish in ~50ms instead of ~200ms sequential.

### 3. Multi-Edit Atomic Transaction (Single Call)

Apply multiple edits across files in one `precision_edit` call with atomic transaction. If any edit fails, all roll back.

```yaml
precision_edit:
  edits:
    - path: "src/components/Button.tsx"
      find: "export default Button"
      replace: "export { Button as default }"
    - path: "src/components/index.ts"
      find: "export { default as Button } from './Button'"
      replace: "export { Button } from './Button'"
  transaction:
    mode: "atomic"
  verbosity: minimal
```

### 4. Multi-File Write (Single Call)

Create multiple files in one `precision_write` call.

```yaml
precision_write:
  files:
    - path: "src/features/user/index.ts"
      content: |
        export * from './types';
        export * from './api';
        export * from './hooks';
    - path: "src/features/user/types.ts"
      content: |
        export interface User {
          id: string;
          email: string;
          name: string;
        }
    - path: "src/features/user/api.ts"
      content: |
        import type { User } from './types';
        export const getUser = async (id: string): Promise<User> => { /* ... */ };
  verbosity: count_only
```

### 5. Batching Precision Tools (Optimal)

The highest form of batching: wrap multiple precision calls in a single transaction.

Each operation type (read, write, exec, query) uses the corresponding precision_engine tool's schema. For example:
- `read` operations use precision_read schema (with `files` array)
- `write` operations use precision_write schema (with `files` array)
- `exec` operations use precision_exec schema (with `commands` array)
- `query` operations use precision_grep/precision_glob schemas

```yaml
batch:
  operations:
    read:
      - files:
          - path: "src/types.ts"
            extract: symbols
    write:
      - files:
          - path: "src/features/auth/types.ts"
            content: |
              export interface User {
                id: string;
                email: string;
                name: string;
              }
    exec:
      - commands:
          - cmd: "npm run typecheck"
            expect:
              exit_code: 0
  config:
    transaction:
      mode: atomic
  verbosity: minimal
```

## Token Budget & Pagination

For large files or batch reads, use `token_budget` to control output size.

```yaml
# Read up to 20 files, but cap total output at 5K tokens
precision_read:
  files: [
    { path: "file1.ts" },
    { path: "file2.ts" },
    # ...
  ]
  token_budget: 5000
  page: 1  # Start with page 1
  verbosity: standard
```

If results are truncated, increment `page` to get the next batch.

## Output Format Selection (`precision_grep`)

`precision_grep` has multiple output formats: `count_only`, `files_only`, `locations`, `matches`, `context`.

| Format | Use Case | Token Cost |
|-------|----------|------------|
| `count_only` | Gauge scope | Very Low |
| `files_only` | Discovery phase | Low |
| `locations` | Find where something exists | Medium |
| `matches` | Need actual matched lines | High |
| `context` | Need surrounding code | Very High |

**Progressive Disclosure**: Start with `count_only` to gauge scope, then `files_only` to build a target list, then `matches` to get content.

## Discover Tool Orchestration

The `discover` tool is a meta-tool that runs multiple queries (grep, glob, symbols) in parallel. Always use it BEFORE implementation.

**Discovery Pattern**:
1. Run `discover` with multiple queries
2. Analyze results to understand scope
3. Plan work based on discovery findings
4. Execute with batching

```yaml
# Step 1: Discover
discover:
  queries:
    - id: existing_files
      type: glob
      patterns: ["src/features/auth/**/*.ts"]
    - id: existing_patterns
      type: grep
      pattern: "export (function|const|class)"
      glob: "src/features/**/*.ts"
  verbosity: files_only

# Step 2: Read key files with outline based on discovery
precision_read:
  files: [{ path: "src/features/auth/index.ts", extract: outline }]
  verbosity: minimal

# Step 3: Execute based on what was discovered
precision_write:
  files:
    - path: "src/features/auth/middleware.ts"
      content: "..."
  verbosity: count_only
```

## `precision_exec` Patterns

### 1. Background Processes

Run long-running processes in the background to avoid blocking.

```yaml
precision_exec:
  commands:
    - cmd: "npm run dev"
      background: true
  verbosity: minimal
```

### 2. Retry Patterns

Automatically retry flaky commands.

```yaml
precision_exec:
  commands:
    - cmd: "npm install"
      retry:
        max: 3
        delay_ms: 1000
  verbosity: minimal
```

### 3. Until Patterns

Poll until a condition is met.

```yaml
precision_exec:
  commands:
    - cmd: "curl http://localhost:3000/api/health"
      until:
        pattern: "ok"
        timeout_ms: 30000
  verbosity: minimal
```

## `precision_fetch` Patterns

### 1. Batched URLs

Fetch multiple URLs in one call.

```yaml
precision_fetch:
  urls:
    - url: "https://api.example.com/users"
    - url: "https://api.example.com/posts"
    - url: "https://api.example.com/comments"
  verbosity: standard
```

### 2. Extract Modes

Extract specific data from JSON responses.

```yaml
precision_fetch:
  urls:
    - url: "https://api.example.com/users"
      extract: json  # Extract mode: raw, text, json, markdown, structured, etc.
  verbosity: standard
```

### 3. Service Registry Auth

Use pre-configured services for automatic authentication.

```yaml
precision_fetch:
  urls:
    - url: "https://api.openai.com/v1/models"
      service: "OpenAI"  # Auto-applies bearer token from config
  verbosity: standard
```

## Anti-Patterns (NEVER DO THESE)

1. **Using native tools**: Read, Edit, Write, Glob, Grep, WebFetch should be avoided. Use precision equivalents.

2. **Setting verbosity to "verbose" for writes/edits**: Wastes tokens. You just wrote the content, why read it back?

3. **Reading entire files when you only need outline/symbols**: Use extract modes.

4. **Running discover queries one at a time**: Batch them.

5. **Using `precision_read` when `precision_grep` would find it faster**: Grep is optimized for search.

6. **Reading a file you just wrote**: You already know the content.

7. **Not using discover before implementation**: Blind implementation leads to mismatched patterns.

8. **Making multiple sequential precision tool calls that could be batched**: If 3+ calls to the same tool, batch them.

9. **Using `verbosity: verbose` as default**: Only use it when debugging.

10. **Ignoring token_budget for large batch reads**: Without a budget, you might get truncated results.

## Escalation Procedure

If a precision tool fails:

1. **Check the error**: Is it user error (wrong path, bad syntax)? Fix and retry.

2. **If tool genuinely fails**: Use native tool for THAT SPECIFIC TASK only.

3. **Return to precision tools**: For the next operation.

4. **Log the failure**: To `.goodvibes/memory/failures.json`.

**Example**:
- `precision_read` fails on a specific file => Use `Read` for that file only, return to `precision_read` for other files.
- `precision_edit` fails on a specific edit => Use `Edit` for that edit only, return to `precision_edit` for other edits.

**NEVER**: Abandon precision tools entirely because one call failed.

## Decision Tree: Which Tool?

```
Do I know the exact file paths?
  |-- Yes -- precision_read (with appropriate extract mode)
  +-- No -- Do I know a pattern?
      |-- Yes -- precision_glob
      +-- No -- Am I searching for content?
         |-- Yes -- precision_grep
         +-- No -- Am I searching for symbols?
            |-- Yes -- precision_symbols
            +-- No -- Use discover with multiple query types
```

**Special-purpose tools** (not in tree above):
- `precision_notebook` — Jupyter notebook cell operations (replace/insert/delete with cell_id targeting)
- `precision_agent` — Spawn headless Claude sessions with dossier-based context injection
- `precision_config` — Runtime configuration (get/set/reload)

## Performance Benchmarks

**Token Savings**:
- `outline` vs `content`: 60-80% savings
- `symbols` vs `content`: 70-90% savings
- `count_only` vs `verbose`: 95% savings
- Batched 5 files vs 5 separate calls: 40-60% savings (overhead reduction)
- Parallel discover 4x vs sequential: 75% speedup, similar token cost

**Time Savings**:
- Parallel discover (4 queries): ~50ms vs ~200ms sequential
- Batched writes (5 files): ~80ms vs ~400ms separate
- Batched edits with transaction: atomic rollback on failure

## Quick Reference

**Most common patterns**:

```yaml
# 1. Discover before implementing
discover:
  queries:
    - id: files
      type: glob
      patterns: ["pattern"]
    - id: patterns
      type: grep
      pattern: "regex"
  verbosity: files_only

# 2. Read with outline first
precision_read:
  files: [{ path: "file.ts", extract: outline }]
  verbosity: minimal

# 3. Batch writes with count_only
precision_write:
  files:
    - { path: "file1.ts", content: "..." }
    - { path: "file2.ts", content: "..." }
  verbosity: count_only

# 4. Batch edits with atomic transaction
precision_edit:
  edits:
    - { path: "f1.ts", find: "...", replace: "..." }
    - { path: "f2.ts", find: "...", replace: "..." }
  transaction: { mode: "atomic" }
  verbosity: minimal

# 5. Verify with minimal output
precision_exec:
  commands:
    - { cmd: "npm run typecheck", expect: { exit_code: 0 } }
  verbosity: minimal
```

---

**Remember**: The precision engine saves tokens, but only when you choose the right verbosity, extract modes, and batching patterns. Use this skill as a cheat sheet for efficient tool usage.
