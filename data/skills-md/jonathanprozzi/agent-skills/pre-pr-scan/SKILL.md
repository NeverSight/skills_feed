---
name: pre-pr-scan
description: Pre-PR compliance and security scan. Checks diff against CLAUDE.md guidelines and security best practices before creating a pull request.
license: MIT
metadata:
  author: jonathanprozzi
  version: "1.0.0"
context: fork
agent: general-purpose
disable-model-invocation: true
argument-hint: "[base-branch] [--validate] [--all] [--quick] [--run-checks] [--output <path>] [--guidelines <paths...>]"
allowed-tools: "Read, Grep, Glob, Bash(git *), Task, Write"
---

# Pre-PR Scan

You are performing a pre-PR compliance and security scan. Your goal is to catch issues BEFORE a pull request is created, mimicking what the Claude PR review bot would flag.

**IMPORTANT: Static analysis by default.** Do NOT run tests, linters, or build commands unless `--run-checks` flag is provided. Running tests is the user's responsibility. Your job is to analyze code and diffs to identify potential issues - not to execute anything.

If `--run-checks` is provided, run the project's lint, test, and build commands (matching what CI would run) and include results in the report.

## Dynamic Context

### Changed Files
!`git diff --name-only main...HEAD 2>/dev/null || git diff --name-only HEAD~5`

### Diff Stats
!`git diff --stat main...HEAD 2>/dev/null || git diff --stat HEAD~5`

**Note on context:** The agent will fetch the full diff and locate CLAUDE.md files during execution. If the diff is large (>1000 lines), parallel mode will be used automatically.

**To find project guidelines**, look for CLAUDE.md in the repo root and subdirectories. Read any found guidelines before scanning.

**Note**: If `--guidelines <paths...>` is provided, read those files instead of auto-discovering. Example:
```bash
/pre-pr-scan --guidelines ./CLAUDE.md ./packages/api/CLAUDE.md
```
This is useful for monorepos where each package has its own guidelines.

---

## Flags

Parse the arguments passed to this skill. Set these variables based on what's present:

| Flag | Variable | Effect |
|------|----------|--------|
| `--validate` | `VALIDATE_HIGH=true` | Run validation pass on HIGH issues |
| `--all` | `SHOW_ALL=true` | Include issues below 80% confidence |
| `--quick` | `QUICK_MODE=true` | Use Haiku for all agents (fastest) |
| `--run-checks` | `RUN_CHECKS=true` | Run lint/test/build commands (like CI) |
| `--output <path>` | `OUTPUT_PATH` | Write report to file (in addition to stdout) |
| `--guidelines <paths...>` | `GUIDELINES_PATHS` | Explicit CLAUDE.md file paths |

**Default behavior** (no flags): Static analysis only, ≥80% confidence threshold, no validation pass, auto-discover CLAUDE.md.

**Flag combinations:**
- `--validate` alone: Full scan + validation (~300k tokens, 80% precision on HIGH)
- `--quick` alone: Fast scan, Haiku everywhere (~80-100k tokens)
- `--all` alone: See speculative issues for awareness
- `--quick --validate`: Not recommended (defeats purpose of quick)
- `--output ./scan-results.md`: Save report to file for later reference
- `--guidelines ./CLAUDE.md ./packages/core/CLAUDE.md`: Explicit guideline files (monorepos)

---

## No CLAUDE.md?

If no CLAUDE.md is found in the project, the skill automatically falls back to:
- Bug detection (logic errors, missing error handling, race conditions)
- Security scanning (OWASP + Web3 + AI/LLM)
- TypeScript/code quality checks

This makes the skill portable to any repo, even without project-specific guidelines.

---

## Mode Selection

Based on the **Diff Stats** above (look at the summary line showing files changed and insertions/deletions), select the appropriate mode:

### Small PR Mode (< 1000 total changes AND < 15 files)
Run the scan sequentially as a single agent. Skip to **Sequential Scan Process** below.

### Large PR Mode (≥ 1000 total changes OR ≥ 15 files)
Spawn 4 parallel agents with **partitioned responsibilities** (no overlap). Follow **Parallel Scan Process** below.

**Token efficiency**: Each agent analyzes the diff first, only reading max 5 full files. This prevents duplicate file reads across agents.

**To get the full diff for analysis**, run: `git diff main...HEAD` (or `git diff HEAD~5` if no main branch).

---

## Parallel Scan Process

For large PRs, use the Task tool to spawn 4 parallel agents. Each agent has a **distinct responsibility** with **no overlap** to minimize token usage.

### Token Efficiency Rules

1. **Analyze diff FIRST** - Look for issues in the diff before reading full files
2. **Max 5 deep-dives per agent** - Only read full files when diff shows a potential issue
3. **No responsibility overlap** - Each agent owns specific issue types exclusively

### Agent Prompts

**Agent 1: CI Failures + CLAUDE.md Compliance**
```
You detect issues that will BREAK CI (compilation, tests) and CLAUDE.md violations.

STEP 1: Get the diff
git diff main...HEAD

STEP 2: Scan diff for CI-breaking patterns (DO NOT read files yet)
- Duplicate imports/exports (same name imported twice)
- Duplicate function definitions
- Missing imports (used but not imported)
- Type errors visible in diff (wrong types passed)

STEP 2.5: Check for duplicate definitions in codebase
- Extract function/const/class names ADDED in diff (lines starting with +)
- For each name, grep codebase: git grep -n "function <name>\|const <name>\|class <name>" -- '*.ts' '*.tsx'
- Flag: If name exists elsewhere AND is being added (not moved), it's a duplicate
- This catches compilation errors the diff alone won't show

STEP 3: Check test coherence
- Get test files: git diff --name-only main...HEAD | grep -E '\.(test|spec)\.(ts|tsx)$'
- For each test file, identify its subject (e.g., foo.test.ts tests foo.ts)
- Compare test assertions to actual implementation
- Flag: tests expecting states/functions that don't exist

STEP 4: Read CLAUDE.md, scan diff for violations
- Only read CLAUDE.md once
- Check diff against guidelines (don't read implementation files)

STEP 5: Deep-dive (MAX 5 FILES)
- Only read full files if diff shows a likely issue
- Confirm or reject the issue with full context

EXCLUSIVE FOCUS: CI failures (compilation, test mismatches) + CLAUDE.md
DO NOT CHECK: Security, null access, error handling (other agents handle these)

Output format:
### [HIGH|MEDIUM|LOW]: [Title]
**Confidence:** [80-100]%
**File:** `path:line`
**Category:** [CI Failure | CLAUDE.md Compliance | Test Coherence]
**Issue:** [description]
**Impact:** [CI will fail because...]
**Fix:** [recommendation]
```

**Agent 2: Security Vulnerabilities**
```
You detect SECURITY issues only. No type checking, no error handling.

STEP 1: Get the diff
git diff main...HEAD

STEP 2: Grep diff for security patterns (DO NOT read files yet)
- Hardcoded secrets: API keys, tokens, passwords in strings
- Injection: User input in SQL/commands/HTML without sanitization
- Web3: Addresses without checksum validation, private key handling
- Auth: Missing authorization checks, IDOR patterns

STEP 3: Deep-dive (MAX 5 FILES)
- Only read files where diff shows a security-relevant pattern
- Confirm the vulnerability with full context

EXCLUSIVE FOCUS: Security vulnerabilities (OWASP + Web3)
DO NOT CHECK: Type errors, null access, error handling, CLAUDE.md (other agents)

Output format:
### [HIGH|MEDIUM|LOW]: [Title]
**Confidence:** [80-100]%
**File:** `path:line`
**Category:** Security
**Vulnerability:** [OWASP category or Web3 issue type]
**Issue:** [description]
**Impact:** [what an attacker could do]
**Fix:** [recommendation]
```

**Agent 3: Logic Bugs + Error Handling**
```
You detect RUNTIME BUGS. No security, no type checking.

STEP 1: Get the diff
git diff main...HEAD

STEP 2: Scan diff for bug patterns (DO NOT read files yet)
- Null/undefined access: obj.property without null check
- Array bounds: arr[index] without length check
- Race conditions: async operations without proper ordering
- Missing error handling: .then() without .catch(), no try/catch
- Resource leaks: opened but never closed

STEP 3: Deep-dive (MAX 5 FILES)
- Only read files where diff shows a likely bug
- Check surrounding context to confirm

EXCLUSIVE FOCUS: Runtime bugs, error handling, logic errors
DO NOT CHECK: Security, type mismatches, CLAUDE.md (other agents)

Output format:
### [HIGH|MEDIUM|LOW]: [Title]
**Confidence:** [80-100]%
**File:** `path:line`
**Category:** Bug Detection
**Issue:** [description]
**Impact:** [what will crash/fail at runtime]
**Fix:** [recommendation]
```

**Agent 4: History Analyzer** (use Haiku - no file reads needed)
```
You analyze COMMIT PATTERNS only. No file reading.

STEP 1: Get commit history
git log --oneline main...HEAD

STEP 2: For each commit, check the stat
git show <hash> --stat

STEP 3: Look for patterns
- Flip-flopping: Code added then removed across commits
- Incomplete: Feature without tests, API without client update
- Contradictions: Commits that undo earlier work
- Large commits: Should be split for reviewability
- Vague messages: "fix", "update", "changes" without context

NO FILE READS - History analysis only.

Output format:
### [HIGH|MEDIUM|LOW]: [Title]
**Confidence:** [80-100]%
**Commits:** `abc123`, `def456`
**Category:** History Analysis
**Issue:** [description]
**Pattern:** [what the history shows]
**Fix:** [recommendation]
```

### Spawning Agents

Use the Task tool with these parameters for each agent:
- `subagent_type`: "general-purpose" (Agents 1-3) or "Explore" (Agent 4)
- `description`: "[Agent name]"
- `prompt`: [The prompt above]
- `model`: See model selection below

**Why general-purpose for Agents 1-3?** These agents need to read files for deep-dives. The `Explore` subagent type has restricted permissions when running in parallel/background, causing tool access to be denied. `general-purpose` agents have full tool access.

**Agent 4 uses Explore** because it only runs git commands (no file reads needed).

**Model selection:**
- **Default**: Haiku for Agent 4 only, Sonnet for Agents 1-3
- **`--quick` mode**: Haiku for ALL agents (fastest, ~50% token savings)

**IMPORTANT:** Spawn all 4 agents in a SINGLE message to run them in parallel.

### Aggregating Results

After all agents complete:
1. Collect all issues from all 4 agents
2. Deduplicate (same file + same issue = keep one)
3. Sort by severity (HIGH → MEDIUM → LOW), then by confidence (highest first)
4. **If `--validate` flag**: Run validation pass on HIGH issues (see below)
5. **If `--all` flag**: Include issues below 80% confidence (mark as "SPECULATIVE")
6. Output in the standard format below

### Validating HIGH Issues

**Skip this section unless `--validate` flag is set.**

For each HIGH severity issue, spawn a validation agent to confirm:

```
You are validating a potential HIGH severity issue.

ISSUE: [description from original agent]
FILE: [file path]
CLAIMED PROBLEM: [what the agent said is wrong]

Your job:
1. Read the file and surrounding context
2. Determine if this is a REAL issue or false positive
3. Return: CONFIRMED or REJECTED with brief explanation

Be strict - only CONFIRM if you are certain the issue exists.
If the code might be intentional or context-dependent, REJECT.
```

Use the Task tool with:
- `subagent_type`: "general-purpose" (needs file read access)
- `model`: "sonnet" (for thorough validation)
- `description`: "Validate: [issue title]"

**Spawn validators in parallel** for all HIGH issues, then filter to only CONFIRMED issues.

This multi-pass validation reduces false positives on critical issues.

---

## Sequential Scan Process

For small PRs, perform all checks yourself. Work from the diff (provided above) first.

### Phase 1: CI Failure Detection (HIGHEST PRIORITY)

Check for issues that will **break the build**:

1. **Duplicate definitions**: Same import/function/variable defined twice
2. **Duplicate definitions in codebase**:
   - Extract function/const/class names ADDED in diff
   - Grep codebase to check if name already exists elsewhere
   - Flag if adding a name that already exists (compilation will fail)
3. **Missing imports**: Used but not imported
4. **Type errors in diff**: Wrong types visible in the changed code
5. **Test coherence**: Test files expecting states/functions that don't exist
   - For each `*.test.ts` or `*.spec.ts` in changed files, verify assertions match implementation

### Phase 2: CLAUDE.md Compliance Audit

If CLAUDE.md exists, audit changes against its guidelines:

1. **Read CLAUDE.md once** - understand the guidelines
2. **Scan diff for violations** - check patterns in the diff itself
3. **Deep-dive only if needed** - read full files only to confirm issues
4. **Cite the specific guideline** being violated

### Phase 3: Security Scan (OWASP + Web3 + AI)

Scan the diff for security patterns:

#### Traditional Security (OWASP Top 10)
- **Injection**: SQL, NoSQL, command injection patterns
- **Sensitive Data**: Hardcoded secrets, API keys in strings
- **XSS**: Unsanitized user input rendered in output

#### Web3/Blockchain Security (if applicable)
- **Address Validation**: Unchecksummed addresses (use `getAddress()`)
- **Transaction Safety**: Missing gas checks, unvalidated params

#### AI/LLM Security (if applicable)
- **Prompt Injection**: User input directly in prompts
- **PII Leakage**: Sensitive data in prompts or logs

### Phase 4: Logic Bugs + Error Handling

Scan the diff for runtime bug patterns:
- **Null/undefined access**: `obj.property` without null check
- **Array bounds**: `arr[index]` without length check
- **Missing error handling**: `.then()` without `.catch()`
- **Race conditions**: Async operations without proper ordering

### Phase 5: History Analysis

Analyze commit history for patterns:
- **Flip-flopping**: Code added then removed across commits
- **Incomplete changes**: Features without tests
- **Contradictions**: Commits that undo earlier work
- **Commit hygiene**: Large commits that should be split

---

## Confidence Scoring

Every issue MUST include a confidence score:

| Range | Meaning | Reported? |
|-------|---------|-----------|
| 95-100% | Definite issue, clear violation | Always |
| 90-94% | Very likely, strong evidence | Always |
| 85-89% | Probable, good evidence | Always |
| 80-84% | Possible, meets threshold | Always |
| 60-79% | Speculative, needs investigation | Only with `--all` |
| <60% | Low confidence, likely noise | Never |

**Default**: Only ≥80% issues reported.
**With `--all`**: 60-79% issues included, marked as "SPECULATIVE" in output.

---

## Output Format

```markdown
## Pre-PR Scan: [branch] vs main

**Mode:** [Sequential | Parallel (4 agents)]
**Flags:** [--validate, --all, --quick, or "none"]
**Files scanned:** X changed files
**Commits analyzed:** Y commits
**Issues found:** Z (A High, B Medium, C Low)
**Validated:** [If --validate: "X/Y HIGH confirmed" | else: "skipped"]

---

### HIGH: [Issue Title]
**Confidence:** [80-100]%
**File:** `path/to/file.ts:42` (or **Commits:** for history issues)
**Category:** [CLAUDE.md Compliance | Security | Bug | TypeScript | History]
**Guideline:** [If CLAUDE.md issue, cite specific lines]
**Issue:** [What's wrong]
**Impact:** [Why it matters]
**Fix:** [How to fix]

---

### MEDIUM: [Issue Title]
...

---

## Summary

[Brief summary of findings and recommended actions before creating PR]
```

---

## Rules

1. **Only scan changed files** - Don't flag pre-existing issues
2. **Cite guidelines explicitly** - For CLAUDE.md issues, quote the rule
3. **Be specific** - Include file path and line number
4. **Filter noise** - Don't report:
   - Issues linters would catch (ESLint, TypeScript compiler)
   - Style preferences not in CLAUDE.md
   - Hypothetical issues without concrete evidence
5. **Prioritize by impact** - HIGH = security/data loss, MEDIUM = bugs/maintainability, LOW = improvements
6. **Actionable fixes** - Every issue must have a clear fix recommendation

## Confidence Threshold

**Default (no `--all`)**: Only report issues ≥80% confidence. Skip:
- Speculative issues (60-79%)
- Context-dependent patterns that might be intentional
- Issues that require more context to verify

**With `--all`**: Include 60-79% issues, but mark them clearly:
```markdown
### SPECULATIVE: [Issue Title]
**Confidence:** 72%
**Note:** Below threshold - included due to --all flag
```

---

## Begin Scan

1. Check the **Diff Stats** to determine mode (Sequential vs Parallel)
2. If Parallel: spawn 4 agents using Task tool, aggregate results
3. If Sequential: run all 4 phases yourself
4. Output findings in the format above, sorted by severity then confidence
5. **If `--output <path>` flag**: Write the complete report to the specified file using the Write tool

### Output to File

If `OUTPUT_PATH` is set:
- Write the **complete markdown report** to the specified path
- Use the Write tool (not Bash)
- Include all sections: header, issues, summary
- The report is written **in addition to** stdout output (user sees both)
