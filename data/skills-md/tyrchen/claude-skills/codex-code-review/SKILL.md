---
name: codex-code-review
description: Perform comprehensive code reviews using OpenAI Codex CLI. This skill should be used when users request code reviews, want to analyze diffs/PRs, need security audits, performance analysis, or want automated code quality feedback. Supports reviewing staged changes, specific files, entire directories, or git diffs.
---

# Codex Code Review

## Overview

To perform thorough, automated code reviews using the OpenAI Codex CLI agent, use this skill. Codex runs locally and can analyze code changes, identify issues, suggest improvements, and provide security/performance insights through non-interactive automation.

> **⚠️ CRITICAL**: When reviewing code that involves dependency versions, latest releases, or current best practices, you MUST use the WebSearch tool to verify information before making any claims. Never assume version numbers or release status - always search first to avoid false positives. See the "Web Search Verification" section for details.

## Prerequisites

Ensure Codex CLI is installed and authenticated:

```bash
# Install via npm
npm install -g @openai/codex

# Or via Homebrew (macOS)
brew install --cask codex

# Authenticate (recommended: ChatGPT account)
codex
# Follow authentication prompts
```

## Decision Tree: Choosing Review Type

```text
Code review request → What scope?
    ├─ Git changes (staged/unstaged) → Use: Git Diff Review
    │
    ├─ Pull Request → Use: PR Review Workflow
    │
    ├─ Specific files → Use: File Review
    │
    ├─ Entire directory/project → Use: Directory Review
    │
    └─ Special focus needed?
        ├─ Security concerns → Use: Security Audit
        ├─ Performance issues → Use: Performance Review
        └─ Architecture/Design → Use: Architecture Review
```

## Headless Execution (Required)

When running codex for automated code reviews, you MUST use the `--full-auto` flag to grant all necessary permissions for headless operation. Without this flag, codex may hang waiting for user approval.

**Always use `--full-auto` for non-interactive reviews:**

```bash
# CORRECT: Full automation mode - grants all permissions automatically
codex --full-auto exec "Review the staged git changes..."

# WRONG: May hang waiting for approval in automated contexts
codex exec "Review the staged git changes..."
```

**Why this matters:**

- Codex requires approval for file reads, command execution, and other operations
- In headless/automated mode, there's no user to approve these actions
- `--full-auto` auto-approves all safe operations, enabling true automation

**Alternative: Granular approval flags:**

```bash
# Auto-approve specific operation types
codex --auto-approve-read --auto-approve-execute exec "..."
```

## Quick Start

To perform a basic code review on staged changes:

```bash
codex --full-auto exec "Review the staged git changes. Analyze code quality, identify bugs, suggest improvements, and check for security issues. Provide a structured review with severity levels."
```

## Review Workflows

### 1. Git Diff Review

To review uncommitted changes in the current repository:

**Staged changes only:**

```bash
codex --full-auto exec "Review all staged changes (git diff --cached). For each file:
1. Summarize what changed
2. Identify potential bugs or logic errors
3. Check for security vulnerabilities
4. Suggest code quality improvements
5. Rate severity: critical/high/medium/low

Format as a structured review report."
```

**All uncommitted changes:**

```bash
codex --full-auto exec "Review all uncommitted changes (git diff HEAD). Provide:
- Summary of changes per file
- Bug identification with line numbers
- Security concerns
- Code style issues
- Suggested fixes with code examples"
```

**Changes between branches:**

```bash
codex --full-auto exec "Review changes between main and current branch (git diff main...HEAD). Focus on:
1. Breaking changes
2. API compatibility
3. Test coverage gaps
4. Documentation needs"
```

### 2. PR Review Workflow

To review a GitHub Pull Request:

```bash
# First, fetch PR diff
gh pr diff <PR_NUMBER> > /tmp/pr_diff.txt

# Then review with codex (--full-auto for headless operation)
codex --full-auto exec "Review the code changes in /tmp/pr_diff.txt as a thorough PR reviewer. Provide:

## Summary
Brief description of what this PR accomplishes

## Code Review
For each file changed:
- Purpose of changes
- Potential issues (bugs, edge cases)
- Security considerations
- Performance implications

## Recommendations
- Required changes (blocking)
- Suggested improvements (non-blocking)
- Questions for the author

## Verdict
APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION"
```

### 3. File Review

To review specific files:

**Single file:**

```bash
codex --full-auto exec "Perform a comprehensive code review of src/utils/auth.ts. Analyze:
1. Code correctness and logic
2. Error handling completeness
3. Security vulnerabilities (OWASP Top 10)
4. Performance bottlenecks
5. Code maintainability
6. Test coverage recommendations"
```

**Multiple files:**

```bash
codex --full-auto exec "Review these files as a cohesive unit: src/api/handler.ts, src/api/middleware.ts, src/api/routes.ts. Focus on:
- Consistency across files
- Proper separation of concerns
- Error propagation
- Request validation"
```

### 4. Directory Review

To review an entire directory or project:

```bash
codex --full-auto exec "Perform a code review of the src/services/ directory. For each file:
- Identify the file's purpose
- List any bugs or issues
- Note security concerns
- Suggest improvements

Provide a summary with prioritized action items."
```

### 5. Security Audit

To perform a security-focused review:

```bash
codex --full-auto exec "Perform a security audit of the codebase. Check for:

**Critical:**
- SQL injection vulnerabilities
- Command injection risks
- Authentication/authorization flaws
- Sensitive data exposure
- Insecure deserialization

**High:**
- XSS vulnerabilities
- CSRF issues
- Insecure dependencies
- Hardcoded secrets/credentials
- Improper input validation

**Medium:**
- Missing rate limiting
- Verbose error messages
- Insecure configurations
- Missing security headers

Report findings with:
- Severity level
- File and line number
- Description of vulnerability
- Remediation steps
- Code fix examples"
```

### 6. Performance Review

To analyze code for performance issues:

```bash
codex --full-auto exec "Analyze the codebase for performance issues:

1. **Algorithm Complexity**
   - O(n^2) or worse operations
   - Unnecessary nested loops
   - Inefficient data structures

2. **Resource Usage**
   - Memory leaks
   - Unclosed resources
   - Large object allocations

3. **I/O Operations**
   - N+1 query patterns
   - Synchronous blocking calls
   - Missing caching opportunities

4. **Concurrency**
   - Race conditions
   - Deadlock potential
   - Thread safety issues

Provide specific file locations and optimization suggestions."
```

### 7. Architecture Review

To review code architecture and design:

```bash
codex --full-auto exec "Review the codebase architecture:

1. **Design Patterns**
   - Identify patterns in use
   - Suggest missing patterns
   - Flag anti-patterns

2. **SOLID Principles**
   - Single Responsibility violations
   - Open/Closed principle adherence
   - Dependency Inversion issues

3. **Code Organization**
   - Module boundaries
   - Circular dependencies
   - Coupling analysis

4. **Maintainability**
   - Code duplication
   - Complex functions (cyclomatic complexity)
   - Missing abstractions

Provide architectural recommendations with examples."
```

## Advanced Options

### Model Selection

To use a specific model (if need to use the latest model - make sure do web search first to find the latest and most suitable model) for deeper analysis:

```bash
codex --full-auto exec --model gpt-5.1-codex "Perform thorough code review of src/..."
```

### Reasoning Depth

To adjust reasoning effort (available: minimal, low, medium, high, xhigh):

Configure in `~/.codex/config.toml`:

```toml
model_reasoning_effort = "high"
```

### Output to File

To save review results:

```bash
codex --full-auto exec -o review_report.md "Review src/api/..."
```

### JSON Output

To get structured JSON output for CI integration:

```bash
codex --full-auto exec --json "Review staged changes. Return JSON with structure:
{
  \"summary\": \"...\",
  \"files_reviewed\": [...],
  \"issues\": [{\"severity\": \"...\", \"file\": \"...\", \"line\": N, \"message\": \"...\"}],
  \"recommendations\": [...]
}" 2>/dev/null | jq '.item.content'
```

## CI/CD Integration

To integrate code review in CI pipelines:

```bash
#!/bin/bash
# ci-review.sh

# Get changed files
CHANGED_FILES=$(git diff --name-only origin/main...HEAD)

if [ -z "$CHANGED_FILES" ]; then
    echo "No files changed"
    exit 0
fi

# Run codex review (--full-auto required for CI/headless operation)
codex --full-auto exec --skip-git-repo-check -o review.md "Review these changed files: $CHANGED_FILES

Provide a structured review. If any critical or high severity issues are found, clearly indicate BLOCKING_ISSUES=true at the end."

# Check for blocking issues
if grep -q "BLOCKING_ISSUES=true" review.md; then
    echo "Critical issues found in code review"
    cat review.md
    exit 1
fi

echo "Code review passed"
exit 0
```

## Prompt Templates

### Standard Review Template

```text
Review the following code changes. For each issue found:

1. **Location**: File path and line number
2. **Severity**: Critical / High / Medium / Low / Info
3. **Category**: Bug / Security / Performance / Style / Documentation
4. **Description**: Clear explanation of the issue
5. **Suggestion**: How to fix it with code example

Organize by severity, starting with Critical issues.
```

### PR Approval Template

```text
As a senior engineer, review this PR for merge readiness:

## Checklist
- [ ] Code correctness verified
- [ ] No security vulnerabilities
- [ ] Performance acceptable
- [ ] Error handling complete
- [ ] Tests adequate
- [ ] Documentation updated

## Issues Found
[List any blocking or non-blocking issues]

## Verdict
[APPROVE / REQUEST_CHANGES with specific required changes]
```

## Best Practices

- **Be specific**: Narrow the scope of reviews for better results
- **Use context**: Provide relevant context about the codebase or requirements
- **Iterate**: Run multiple focused reviews rather than one broad review
- **Verify**: Always verify critical security findings manually
- **Document**: Save review outputs for future reference

## CRITICAL: Web Search Verification

**IMPORTANT**: Before making ANY claims about version numbers, latest releases, or current best practices, you MUST perform a web search to verify the information. This prevents false positives in reviews.

### Why This Matters

Code reviews often involve checking if dependencies are up-to-date or if code follows current best practices. Without verification, you may provide incorrect information. For example:

- Claiming "ArgoCD latest version is 2.x" when it's actually 3.2.x (with 3.3.0 in RC)
- Stating a library is deprecated when it's actively maintained
- Recommending outdated security practices

### When to Web Search

**Always search before commenting on:**

1. **Version numbers** - Latest versions of any tool, library, or framework
2. **Deprecation status** - Whether APIs, functions, or libraries are deprecated
3. **Security advisories** - Current CVEs or security recommendations
4. **Best practices** - Current recommended patterns (they evolve over time)
5. **Feature availability** - When features were introduced in specific versions

### How to Verify

Before finalizing any review that mentions versions or current practices:

```bash
# Use WebSearch tool to verify current information
# Example queries:
# - "ArgoCD latest version 2025"
# - "React 19 release date"
# - "Node.js LTS current version"
# - "[library name] latest stable release"
```

### Review Output Template with Verification

When your review includes version-related findings, format them as:

```text
**Dependency Check** (verified via web search on YYYY-MM-DD):
- Package X: Using v1.2.3, latest stable is v2.0.1 ✓
- Package Y: Using v3.0.0, this IS the latest version ✓
- Package Z: Using v0.9.0, latest is v1.0.0 (breaking changes - review release notes)
```

**Never guess or assume version information. When in doubt, search first.**

## Reference Files

- **[Codex CLI Reference](./references/codex_cli.md)** - Complete command reference and configuration options
- **[Review Prompts Library](./references/review_prompts.md)** - Collection of specialized review prompts

## Troubleshooting

**Codex not finding files:**

- Ensure running from the correct directory
- Use absolute paths when needed
- Check that the Git repository is initialized

**Authentication issues:**

- Run `codex` interactively to re-authenticate
- Check `~/.codex/` for credential files

**Timeout on large reviews:**

- Break into smaller file sets
- Use `--full-auto` for longer operations
- Consider directory-by-directory reviews
