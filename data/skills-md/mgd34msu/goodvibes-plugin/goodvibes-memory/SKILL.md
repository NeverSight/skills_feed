---
name: goodvibes-memory
description: "ALWAYS load before starting any task. Provides persistent cross-session memory for learning from past work. Read memory at task start to avoid repeating mistakes; write memory at task end to record what worked. Covers decisions.json (architectural choices), patterns.json (proven approaches), failures.json (past errors and fixes), preferences.json (project conventions), and session activity logs."
metadata:
  version: 1.0.0
  category: protocol
  tags: [memory, logging, decisions, patterns, failures, cross-session]
---

## Resources
```
scripts/
  validate-memory-usage.sh
references/
  schemas.md
```

# GoodVibes Memory Protocol

The memory system enables cross-session learning by capturing decisions, patterns, failures, and preferences in structured JSON files. Every agent must read memory before starting work and write to it after completing work.

## Why This Matters

Without memory:
- Agents repeat known failures
- Proven patterns are rediscovered each session
- Architectural decisions are forgotten or violated
- Project-specific preferences aren't applied

With memory:
- Failures are logged with prevention strategies
- Patterns are reused consistently
- Decisions guide future work
- Preferences ensure consistency

## File Structure

```
.goodvibes/
|-- memory/           # Structured JSON (machine-readable)
|   |-- decisions.json    # Architectural decisions
|   |-- patterns.json     # Proven approaches
|   |-- failures.json     # Past errors + resolutions
|   |-- preferences.json  # Project conventions
|   +-- index.json        # Index file (optional)
+-- logs/             # Markdown logs (human-readable)
    |-- activity.md       # Completed work log
    |-- decisions.md      # Decision log with context
    +-- errors.md         # Error log with resolution
```

---

## BEFORE Starting Work (Read Phase)

Always check memory files before implementing ANY task. Use keyword-based searches to find relevant entries.

### 1. Check `failures.json`

**Purpose**: Avoid repeating known failures.

**How**:
```yaml
# Use precision_read to read the file
precision_read:
  files:
    - path: .goodvibes/memory/failures.json
  verbosity: standard

# Search for keywords matching your task
# Example keywords: "precision_fetch", "config", "auth", "API", "build"
```

**What to look for**:
- `keywords` field matches your task (e.g., searching for "auth" finds authentication failures)
- `error` field describes a similar problem
- `context` field matches your current situation

**If found**:
- Read `resolution` -- how was it fixed?
- Read `prevention` -- how to avoid it?
- Apply the prevention strategy

### 2. Check `patterns.json`

**Purpose**: Use proven approaches instead of inventing new ones.

**How**:
```yaml
precision_read:
  files:
    - path: .goodvibes/memory/patterns.json
  verbosity: standard
```

**What to look for**:
- `keywords` matches your task type
- `when_to_use` describes your situation
- `name` suggests a relevant pattern

**If found**:
- Read `description` -- what's the pattern?
- Check `example_files` -- where is it used?
- Follow the pattern unless there's a compelling reason not to

### 3. Check `decisions.json`

**Purpose**: Respect prior architectural decisions.

**How**:
```yaml
precision_read:
  files:
    - path: .goodvibes/memory/decisions.json
  verbosity: standard
```

**What to look for**:
- `scope` includes files you'll modify
- `category` matches your domain (e.g., "architecture", "pattern", "library")
- `status` is "active" (not "superseded" or "reverted")

**If found**:
- Read `what` and `why` -- understand the decision
- If your task conflicts with the decision: flag to orchestrator before proceeding
- If your task aligns with the decision: follow it

### 4. Check `preferences.json`

**Purpose**: Apply project-specific conventions.

**How**:
```yaml
precision_read:
  files:
    - path: .goodvibes/memory/preferences.json
  verbosity: standard
```

**What to look for**:
- `key` matches your domain (e.g., "category.preference_name")

**If found**:
- Apply the `value` preference
- Respect the `reason` rationale

### Search Strategy

**Manual keyword matching**: Read the file and scan for keywords related to your task.

**Example**:
- Task: "Add authentication with Clerk"
- Keywords to search: `auth`, `clerk`, `authentication`, `login`, `session`
- Check `failures.json` for past auth failures
- Check `patterns.json` for auth patterns
- Check `decisions.json` for auth library decisions

**Scope filtering**: Focus on entries where `scope` includes files you'll modify.

---

## AFTER Completing Work (Write Phase)

Log to memory after completing a task, resolving an error, or making a decision. Always write to BOTH JSON (machine-readable) and Markdown (human-readable).

### When to Write

| Situation | Write to |
|-----------|----------|
| Task passes review | `activity.md` + optionally `patterns.json`/`decisions.json` |
| Error resolved | `errors.md` + `failures.json` |
| Decision made | `decisions.md` + `decisions.json` |
| Never write | Trivial fixes, no new patterns, no decisions |

### After Task Passes Review

**1. Always log to `activity.md`**

Format:
```markdown
## YYYY-MM-DD: [Brief Title]

**Task**: [What was the goal?]

**Plan**: [Approach taken, or N/A]

**Status**: COMPLETE

**Completed Items**:
- [List of what was accomplished]

**Files Modified**:
- [List of changed files with brief description]

**Review Score**: [X/10]

**Commit**: [commit SHA]

---
```

**2. Optionally add to `patterns.json`** (if a reusable pattern emerged)

Only add if:
- The approach is reusable across multiple files/tasks
- It's non-obvious (not standard practice)
- It solves a specific problem well

Schema:
```json
{
  "id": "pat_YYYYMMDD_HHMMSS",
  "name": "PatternNameInPascalCase",
  "description": "What the pattern does and why it works",
  "when_to_use": "Situation where this pattern applies",
  "example_files": ["path/to/file.ts", "another/example.ts"],
  "keywords": ["searchable", "terms"]
}
```

**3. Optionally add to `decisions.json`** (if an architectural decision was made)

Only add if:
- A choice was made between multiple approaches
- The decision affects future work
- It has scope beyond this single task

Schema:
```json
{
  "id": "dec_YYYYMMDD_HHMMSS",
  "date": "YYYY-MM-DDTHH:MM:SSZ",
  "category": "library|architecture|pattern|convention",
  "what": "What was decided",
  "why": "Rationale for the decision",
  "scope": ["files/directories affected"],
  "confidence": "high | medium | low",
  "status": "active|superseded|reverted"
}
```

### After Error Resolved

**1. Always log to `errors.md`**

Format:
```markdown
## YYYY-MM-DD HH:MM - [ERROR_CATEGORY]

**Error**: [Brief description]

**Context**:
- Task: [What were you doing?]
- Agent: [Which agent encountered it?]
- File(s): [Affected files]

**Root Cause**: [Why did it happen?]

**Resolution**: [How was it fixed? Or UNRESOLVED]

**Prevention**: [How to avoid it in the future?]

**Status**: RESOLVED | UNRESOLVED

---
```

**2. Always add to `failures.json`** (with full context)

Schema:
```json
{
  "id": "fail_YYYYMMDD_HHMMSS",
  "date": "YYYY-MM-DDTHH:MM:SSZ",
  "error": "Brief error description",
  "context": "What task was being performed",
  "root_cause": "Technical explanation of why it failed",
  "resolution": "How it was fixed (or UNRESOLVED)",
  "prevention": "How to avoid this failure in the future",
  "keywords": ["searchable", "error-related", "terms"]
}
```

**Error categories** (for `errors.md`):
- `TOOL_FAILURE` -- Precision tool or native tool failed
- `AGENT_FAILURE` -- Agent crashed or failed to complete task
- `BUILD_ERROR` -- TypeScript compilation, build step failed
- `TEST_FAILURE` -- Test suite failed
- `VALIDATION_ERROR` -- Validation, linting, or format checking failed
- `EXTERNAL_ERROR` -- API, network, dependency issue
- `UNKNOWN` -- Error category could not be determined

### After Decision Made

**1. Always log to `decisions.md`**

Format:
```markdown
## YYYY-MM-DD: [Decision Title]

**Context**: [What situation required a decision?]

**Options Considered**:
1. **[Option A]**: [Description + trade-offs]
2. **[Option B]**: [Description + trade-offs]

**Decision**: [What was chosen]

**Rationale**: [Why this option was best]

**Implications**: [What this means for future work]

---
```

**2. Always add to `decisions.json`**

See schema in "After Task Passes Review" section above.

---

## ID Format

Use timestamp-based IDs to avoid needing to read existing entries before writing:

```
dec_YYYYMMDD_HHMMSS   # Decisions
pat_YYYYMMDD_HHMMSS   # Patterns
fail_YYYYMMDD_HHMMSS  # Failures
pref_YYYYMMDD_HHMMSS  # Preferences
```

**Example**: `dec_20260215_143022` for a decision made on 2026-02-15 at 14:30:22

**Collision risk**: Negligible unless two agents write to the same file in the same second. The timestamp provides sufficient uniqueness.

---

## First Write Check

Before first write to any memory/log file, check if it exists:

### For JSON files

If file doesn't exist, create with bare array:
```json
[]
```

### For Markdown files

If file doesn't exist, create with header:
```markdown
# [File Name]

Log of [description].

---

```

**Use precision_read first**:
```yaml
precision_read:
  files:
    - path: .goodvibes/memory/decisions.json
  verbosity: count_only  # Just check existence
```

If `exists: false`, create the file before appending.

---

## Common Mistakes

### Don't Do This

- **Don't skip reading memory** -- You'll repeat failures and violate decisions
- **Don't write for trivial work** -- Only log meaningful patterns/decisions/failures
- **Don't use random IDs** -- Use timestamp-based IDs (no need to read existing entries)
- **Don't forget prevention field** -- Failures without prevention strategies aren't useful
- **Don't log to JSON only** -- Always write to BOTH JSON and Markdown
- **Don't create duplicate entries** -- Search keywords first to check if pattern/failure already exists

### Do This

- **Do read failures.json first** -- Check for known issues before starting
- **Do search by keywords** -- Manual keyword matching is fast and effective
- **Do include full context** -- Root cause + resolution + prevention for failures
- **Do use timestamp IDs** -- No collision risk, no need to read existing entries
- **Do log to both formats** -- JSON for machines, Markdown for humans
- **Do update last_updated** -- Update timestamp when modifying index.json

---

## Validation

Use the `scripts/validate-memory-usage.sh` script to verify compliance:

```bash
# Validate memory protocol usage
bash plugins/goodvibes/skills/protocol/goodvibes-memory/scripts/validate-memory-usage.sh \
  session-transcript.jsonl \
  .goodvibes/memory/

# Exit code 0 = compliant
# Exit code 1 = violations found
```

The script checks:
- Memory files read at task start
- Activity logged after task completion
- Failures logged when errors resolved
- Patterns logged when reusable approaches discovered

---

## Quick Reference

### Read Phase Checklist

- [ ] Read `failures.json` -- keyword search for similar errors
- [ ] Read `patterns.json` -- keyword search for proven approaches
- [ ] Read `decisions.json` -- scope search for relevant decisions
- [ ] Read `preferences.json` -- apply project conventions

### Write Phase Checklist

- [ ] Log to `activity.md` after task completion
- [ ] Add to `patterns.json` if reusable pattern discovered
- [ ] Add to `decisions.json` if architectural decision made
- [ ] Log to `errors.md` + `failures.json` if error resolved
- [ ] Log to `decisions.md` + `decisions.json` if choice made
- [ ] Update `last_updated` timestamp in JSON files
- [ ] Use timestamp-based IDs (no collisions)

---

## Examples

### Example: Reading Failures Before Starting Auth Task

```yaml
# Step 1: Read failures.json
precision_read:
  files:
    - path: .goodvibes/memory/failures.json
  verbosity: standard

# Step 2: Manually search for keywords
# Keywords: "auth", "authentication", "clerk", "oauth", "token"
# Found: fail_20260210_160000 - "Service registry reads empty services"
# Context: OAuth token configuration issue
# Prevention: "Always use nested config format for services"

# Step 3: Apply prevention strategy
# Use nested format when configuring auth service
```

### Example: Writing Pattern After Implementing Feature

```yaml
# Step 1: Check if file exists
precision_read:
  files:
    - path: .goodvibes/memory/patterns.json
  verbosity: count_only

# Step 2: Read existing patterns to avoid duplicates
precision_read:
  files:
    - path: .goodvibes/memory/patterns.json
  verbosity: standard

# Step 3: Add new pattern (if not duplicate)
precision_edit:
  files:
    - path: .goodvibes/memory/patterns.json
      operations:
        - type: insert
          search: '"patterns": ['
          content: |
            {
              "id": "pat_20260215_143022",
              "name": "AuthServiceNesting",
              "description": "Auth services require nested config structure",
              "when_to_use": "When configuring auth providers in goodvibes.json",
              "example_files": [".goodvibes/goodvibes.json"],
              "keywords": ["auth", "config", "nested", "services"]
            },
```

### Example: Logging Error Resolution

```yaml
# Step 1: Log to errors.md
precision_edit:
  files:
    - path: .goodvibes/logs/errors.md
      operations:
        - type: insert_at_line
          line: 1
          content: |
            ## 2026-02-15 14:30 - BUILD_ERROR
            
            **Error**: TypeScript compilation failed with "Cannot find module 'clerk'"
            
            **Context**:
            - Task: Add Clerk authentication
            - Agent: Engineer
            - File(s): src/auth/clerk.ts
            
            **Root Cause**: Missing @clerk/nextjs package in dependencies
            
            **Resolution**: RESOLVED - Added package with `npm install @clerk/nextjs`
            
            **Prevention**: Always check package.json before importing new libraries
            
            **Status**: RESOLVED
            
            ---
            

# Step 2: Add to failures.json
precision_edit:
  files:
    - path: .goodvibes/memory/failures.json
      operations:
        - type: insert
          search: '['
          content: |
            {
              "id": "fail_20260215_143022",
              "date": "2026-02-15T14:30:22Z",
              "error": "TypeScript compilation failed - Cannot find module 'clerk'",
              "context": "Adding Clerk authentication to Next.js app",
              "root_cause": "Missing @clerk/nextjs package in package.json dependencies",
              "resolution": "RESOLVED - Installed package with npm install @clerk/nextjs",
              "prevention": "Before importing from a new package, verify it exists in package.json. Use precision_read to check package.json before adding imports.",
              "keywords": ["typescript", "clerk", "module", "dependency", "package.json", "build-error"]
            },
```

---

## Integration with Other Skills

- **precision-mastery**: Use precision_read/precision_edit for memory file operations
- **error-recovery**: Check failures.json as first step in error recovery
- **gather-plan-apply**: Include memory read in discovery phase
- **review-scoring**: Reviewers check if memory was consulted before work started

---

## File Location

All memory files are relative to project root:

```
.goodvibes/
|-- memory/
|   |-- decisions.json
|   |-- patterns.json
|   |-- failures.json
|   +-- preferences.json
+-- logs/
    |-- activity.md
    |-- decisions.md
    +-- errors.md
```

Always use `.goodvibes/memory/` and `.goodvibes/logs/` as paths (relative to project root).
