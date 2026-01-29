---
name: ai-review-validator
description: Autonomously validate and execute AI Review suggestions from PR comments. Use when users provide AI Review comments (from GitHub Copilot, CodeRabbit, etc.) that suggest code changes, API migrations, or fixes. The skill verifies suggestions against official docs, tests compilation, calculates confidence scores, and auto-applies changes when verified. Triggers on phrases like "verify this AI Review", "apply this suggestion", "validate AI Review comment", or when users paste AI Review URLs/content.
---

# Ai Review Validator

## Overview

Automate validation and execution of AI Review suggestions. This skill verifies AI-generated code review comments by checking official documentation, analyzing the codebase, testing compilation, and calculating confidence scores before automatically applying verified changes.

## ⚠️ CRITICAL REQUIREMENT

**EVERY commit that applies an AI Review suggestion MUST include the original comment URL in the commit message.**

This is NON-NEGOTIABLE. The commit message format MUST be:

```
git commit -m "fix: <summary>

Apply AI Review suggestion
Verified with confidence: <score>/100

AI-Review: <original_github_url>
Resolves: <original_github_url>"
```

Without this link, the commit loses all traceability. This is one of the primary purposes of this skill - maintaining the connection between code changes and AI Review suggestions.

## Workflow

### Step 0: Fetch GitHub PR Comment (if URL provided)

If user provides a GitHub PR comment URL, convert it to API format and fetch content:

**URL Conversion Examples:**
```
Input:  https://github.com/UniClipboard/UniClipboard/pull/158#discussion_r2734386595
Output: https://api.github.com/repos/UniClipboard/UniClipboard/pulls/comments/2734386595

Input:  https://github.com/owner/repo/pull/123#issuecomment-456789
Output: https://api.github.com/repos/owner/repo/issues/comments/456789
```

**Implementation:**
```bash
# Use the included script to convert URL
api_url=$(python3 scripts/github_url_converter.py "<user_provided_url>")

# Fetch comment content from GitHub API
web_fetch "$api_url"

# API response structure:
# {
#   "body": "⚠️ MouseEvent removed...",  # AI Review comment text
#   "path": "src/window.rs",              # Affected file
#   "diff_hunk": "@@ -10,7 +10,7...",   # Code context
#   "user": {"login": "github-copilot"}, # AI tool identifier
#   "html_url": "...",                    # Original URL for commit reference
#   "created_at": "2024-01-28T..."
# }
```

**Supported URL formats:**
- PR review comments: `#discussion_r{comment_id}` → `/pulls/comments/{comment_id}`
- Issue/PR comments: `#issuecomment-{comment_id}` → `/issues/comments/{comment_id}`
- Already API URLs: Pass through unchanged

**Extract key information from API response:**
```python
# Parse the fetched comment
comment_data = {
    "body": response["body"],           # Full AI Review text
    "affected_file": response["path"],  # File to modify
    "original_url": response["html_url"], # For commit reference
    "diff_context": response.get("diff_hunk", "")  # Code context
}
```

### Step 1: Parse AI Review Comment

Extract structured information from the comment (either from fetched API response or user-pasted content):

```python
# Expected AI Review format:
# 1. Risk warning/description
# 2. Code example (before/after)
# 3. Modification prompt

comment_structure = {
    "risk_warning": str,      # e.g., "MouseEvent removed in Tauri v2"
    "deprecated_api": str,    # e.g., "MouseEvent.position()"
    "suggested_api": str,     # e.g., "LogicalPosition::new(x, y)"
    "code_examples": {
        "before": str,
        "after": str
    },
    "modification_prompt": str,  # Instructions for applying the change
    "affected_files": [str],
    "comment_url": str        # CRITICAL: Save this for commit message!
}
```

**IMPORTANT:** The `comment_url` field MUST be preserved throughout the entire workflow. This URL will be used in the commit message to link the code change back to the AI Review suggestion. Never lose track of this URL.

### Step 2: Multi-Dimensional Verification

Run verification in parallel, scoring each dimension:

#### 2.1 Official Documentation (Weight: 40%)

```bash
# Search official sources
web_search "<framework> <deprecated_api> deprecated removed"
web_search "<framework> <suggested_api> migration guide"
web_fetch "official migration documentation URL"

# Scoring:
# - Explicit confirmation: 40 points
# - Partial confirmation: 20 points
# - No evidence: 0 points
```

#### 2.2 Codebase Analysis (Weight: 20%)

```bash
# Examine project state
view <affected_file>
bash_tool "grep -rn '<deprecated_api>' ."
bash_tool "cat package.json | grep <framework>"  # Check version

# Scoring:
# - API found + version matches: 20 points
# - API found but version unclear: 10 points
# - API not found: 0 points
```

#### 2.3 Experimental Verification (Weight: 30%)

```bash
# Test the suggested change
create_file "/home/claude/test_change.ext" "<test code with new API>"
bash_tool "<compile command>"  # e.g., rustc, tsc, npm build

# Scoring:
# - Compiles + no type errors: 30 points
# - Compiles with warnings: 15 points
# - Fails: 0 points
```

#### 2.4 Test Suite (Weight: 10%)

```bash
bash_tool "<test command>"  # e.g., cargo test, npm test

# Scoring:
# - All tests pass: 10 points
# - Tests fail: 0 points
```

### Step 3: Calculate Confidence & Decide

```python
confidence_score = (
    docs_score +
    codebase_score +
    experimental_score +
    test_score
)

if confidence_score >= 80:
    decision = "AUTO_APPLY"
elif confidence_score >= 60:
    decision = "APPLY_WITH_REVIEW"
elif confidence_score >= 40:
    decision = "MANUAL_REVIEW"
else:
    decision = "REJECT"
```

### Step 4: Execute Based on Confidence

**Before proceeding, review `references/commit-checklist.md` to ensure all required fields are included in the commit message.**

#### AUTO_APPLY (≥80)

```bash
# Apply changes
str_replace(
    path=<file>,
    old_str=<deprecated_code>,
    new_str=<new_code>,
    description="Apply AI Review suggestion"
)

# Verify
bash_tool "<build_command>"
bash_tool "<test_command>"

# CRITICAL: Commit MUST include AI Review URL reference
# This is NON-NEGOTIABLE - the commit message MUST link to the original AI Review
bash_tool 'git add .'
bash_tool 'git commit -m "fix: <summary>

Apply AI Review suggestion
Verified with confidence: <score>/100

Verification:
- Docs: <status>
- Compilation: <status>  
- Tests: <status>

AI-Review: <original_comment_url>
Resolves: <original_comment_url>
Co-authored-by: AI Review Validator <agent@ai-review.dev>"'
```

**MANDATORY Commit Message Format:**

The commit message MUST include the original AI Review comment URL. This is essential for:
1. Traceability - linking code changes to the suggestion source
2. Accountability - showing what was verified
3. Context - future developers can see why the change was made

**Bad commit (NEVER do this):**
```
git commit -m "fix: sync pairing settings types and test env"
```
❌ Missing AI Review URL reference!

**Good commit (ALWAYS do this):**
```
git commit -m "fix: Replace MouseEvent with LogicalPosition

Apply AI Review suggestion
Verified with confidence: 85/100

AI-Review: https://github.com/user/repo/pull/123#discussion_r456
Resolves: https://github.com/user/repo/pull/123#discussion_r456"
```
✅ Includes AI Review URL - properly traceable!

Report format:
```markdown
✅ AI Review Suggestion Verified and Applied

Confidence Score: <score>/100

Verification Summary:
- ✓ Official Docs: <evidence>
- ✓ Compilation: Passes
- ✓ Tests: All passing

Changes: <file> (<n> replacements)
Commit: <hash>
Linked: <comment_url>
```

#### APPLY_WITH_REVIEW (60-79)

Apply changes but flag potential issues:

```bash
# Apply changes
str_replace(...)

# Verify
bash_tool "<build_command>"
bash_tool "<test_command>"

# Commit with AI Review URL (MANDATORY)
bash_tool 'git commit -m "fix: <summary>

Apply AI Review suggestion with review needed
Verified with confidence: <score>/100

⚠️ Please review:
- <concern 1>
- <concern 2>

AI-Review: <original_comment_url>
Resolves: <original_comment_url>"'
```

Report format:
```markdown
⚠️ AI Review Suggestion Applied - Please Review

Confidence Score: <score>/100

Concerns:
- <specific issue to check>

Changes applied but recommend reviewing:
1. <area of concern>
2. <edge case>

Commit: <hash>
AI Review: <original_url>
```

#### MANUAL_REVIEW (40-59)

```markdown
🔍 AI Review Suggestion Requires Manual Review

Confidence Score: <score>/100

Issues:
- <conflicting information>
- <uncertainty>

Recommendation: Do not auto-apply
```

#### REJECT (<40)

```markdown
❌ AI Review Suggestion Not Verified

Confidence Score: <score>/100

Evidence shows this suggestion may be incorrect:
- <contradicting evidence>

Recommendation: Do NOT apply
```

## Edge Cases

### Multiple Files

Process all files, create single atomic commit:

```bash
for file in affected_files:
    str_replace(...)

# MUST include AI Review URL
bash_tool 'git commit -m "fix: <summary>

Apply AI Review suggestion
Verified with confidence: <score>/100

Modified files:
- <file1>
- <file2>

AI-Review: <original_comment_url>
Resolves: <original_comment_url>"'
```

### Conflicting Information

```python
if docs_result != experimental_result:
    return "MANUAL_REVIEW", {
        "reason": "Conflicting evidence",
        "docs": docs_result,
        "experiments": experimental_result
    }
```

### Breaking Changes

```bash
# If tests fail after applying
bash_tool "git reset --hard HEAD"
return "REJECT", "Tests fail after applying suggestion"
```

## Safety Principles

1. **Never blindly trust AI Review** - Always verify before applying
2. **Provide evidence** - Show docs, compilation output, test results
3. **Be transparent** - Explain confidence scoring
4. **Safety first** - Verify builds/tests before committing
5. **MANDATORY: Link to AI Review in commit** - Every commit MUST include the original AI Review comment URL in the commit message. Use both `AI-Review:` and `Resolves:` fields.
6. **Human-in-loop** - Flag uncertain cases for review

**Critical Commit Message Requirement:**

EVERY commit that applies an AI Review suggestion MUST include:
```
AI-Review: <original_github_url>
Resolves: <original_github_url>
```

This is NON-NEGOTIABLE. Without this link, the commit loses all traceability to the AI Review that prompted it.

## Common Patterns

### Pattern 1: API Deprecation
```
⚠️ API deprecated in v2.0
Old: old_api()
New: new_api()
```

### Pattern 2: Security Risk
```
🔒 Security: Avoid unsafe code
Use: Safe alternative
```

### Pattern 3: Performance
```
⚡ Performance: Can be optimized
Use: Iterator instead of collect()
```

## When to Escalate

Escalate to human review when:
- Confidence < 60
- Breaking changes detected
- Tests fail after applying
- Conflicting information from sources
- Security-critical code
- Architectural changes

## Scripts

This skill includes a helper script for GitHub integration:

### scripts/github_url_converter.py

Converts GitHub PR comment URLs to GitHub API URLs for fetching comment content.

**Usage:**
```bash
python3 scripts/github_url_converter.py "https://github.com/owner/repo/pull/123#discussion_r456"
# Output: https://api.github.com/repos/owner/repo/pulls/comments/456
```

**Supported formats:**
- PR review comments: `#discussion_r{id}`
- Issue/PR comments: `#issuecomment-{id}`

The script handles URL conversion automatically so you can fetch AI Review content directly from GitHub's API.

## Detailed Examples

For comprehensive examples of different scenarios, see `references/examples.md`:
- GitHub URL with API fetching (complete workflow)
- Pasted comment content (manual input)
- Medium confidence with warnings (performance optimization)
- Low confidence rejection (false positive detection)
- Multiple file batch processing
- Conflicting information handling


