---
name: searching-sourcegraph
description: Search Sourcegraph-indexed codebases for patterns, examples, and system understanding. Triggers on implementation questions, debugging, or "how does X work" queries.
---

# Searching Sourcegraph

Search before you build. Existing patterns reduce tokens, ensure consistency, and surface tested solutions.

## Tool Selection Logic

**Start here:**

1. **Know the exact symbol or pattern?** → `sg_keyword_search`
2. **Know the concept, not the code?** → `sg_nls_search`
3. **Need to understand how/why?** → `sg_deepsearch_read`
4. **Tracing a symbol's usage?** → `sg_find_references`
5. **Need full implementation?** → `sg_go_to_definition` → `sg_read_file`

| Goal | Tool |
|------|------|
| Concepts/semantic search | `sg_nls_search` |
| Exact code patterns | `sg_keyword_search` |
| Trace usage | `sg_find_references` |
| See implementation | `sg_go_to_definition` |
| Understand systems | `sg_deepsearch_read` |
| Read files | `sg_read_file` |
| Browse structure | `sg_list_files` |
| Find repos | `sg_list_repos` |
| Search commits | `sg_commit_search` |
| Track changes | `sg_diff_search` |
| Compare versions | `sg_compare_revisions` |

## Scoping (Always Do This)

```
repo:^github.com/ORG/REPO$           # Exact repo (preferred)
repo:github.com/ORG/                 # All repos in org
file:.*\.ts$                         # TypeScript only
file:src/api/                        # Specific directory
file:.*\.test\.ts$ -file:__mocks__   # Tests, exclude mocks
```

Start narrow. Expand only if results are empty.

Combine filters: `repo:^github.com/myorg/backend$ file:src/handlers lang:typescript`

## Context-Aware Behaviour

**When the user provides a file path or error message:**
- Extract symbols, function names, or error codes
- Search for those exact terms first
- Trace references if the error involves a known symbol

**When the user asks "how does X work":**
- Prefer `sg_deepsearch_read` for architectural understanding
- Follow up with `sg_read_file` on key files mentioned in the response

**When the user is implementing a new feature:**
- Search for similar existing implementations first
- Read tests for usage examples
- Check for shared utilities before creating new ones

**When debugging:**
- Search for the exact error string
- Trace the symbol where the error is thrown
- Check recent changes with `sg_diff_search`

## Workflows

For detailed step-by-step workflows, see:
- `workflows/implementing-feature.md` — when building new features
- `workflows/understanding-code.md` — when exploring unfamiliar systems
- `workflows/debugging-issue.md` — when tracking down bugs

## Efficiency Rules

**Minimise tool calls:**
- Chain searches logically: search → read → references → definition
- Don't re-search for the same pattern; use results from prior calls
- Prefer `sg_keyword_search` over `sg_nls_search` when you have exact terms (faster, more precise)

**Batch your understanding:**
- Read 2-3 related files before synthesising, rather than reading one and asking questions
- Use `sg_deepsearch_read` for "how does X work" instead of multiple keyword searches

**Avoid common token waste:**
- Don't search all repos when you know the target repo
- Don't use `sg_deepsearch_read` for simple "find all" queries
- Don't re-read files you've already seen in this conversation

## Query Patterns

| Intent | Query |
|--------|-------|
| React hooks | `file:.*\.tsx$ use[A-Z].*= \(` |
| API routes | `file:src/api app\.(get\|post\|put\|delete)` |
| Error handling | `catch.*Error\|\.catch\(` |
| Type definitions | `file:types/ export (interface\|type)` |
| Test setup | `file:.*\.test\. beforeEach\|beforeAll` |
| Config files | `file:(webpack\|vite\|rollup)\.config` |
| CI/CD | `file:\.github/workflows deploy` |

For more patterns, see `query-patterns.md`.

## Output Formatting

**Search results:**
- Present as a brief summary, not raw tool output
- Highlight the most relevant file and line
- Include a code snippet only if it directly answers the question

**Code explanations:**
- Start with a one-sentence summary
- Use the codebase's own terminology
- Reference specific files and functions

**Recommendations:**
- Present as numbered steps if actionable
- Link to specific patterns found in the codebase
- Note any existing utilities that should be reused

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Searching all repos | Add `repo:^github.com/org/repo$` |
| Too many results | Add `file:` pattern or keywords |
| Missing relevant code | Try `sg_nls_search` for semantic matching |
| Not understanding context | Use `sg_deepsearch_read` |
| Guessing patterns | Read implementations with `sg_read_file` |

## Principles

- Start narrow, expand if needed
- Chain tools: search → read → find references → definition
- Check tests for usage examples
- Read before generating
