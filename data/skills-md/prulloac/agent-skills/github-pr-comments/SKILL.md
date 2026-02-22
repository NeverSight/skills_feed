---
name: github-pr-comments
description: Analyze and manage GitHub pull request comments with automated categorization, severity assessment, and intelligent response handling. Use when working with PR comments to understand feedback patterns, prioritize issues, or automatically address reviewer concerns. Leverages GitHub MCP Server, GitHub CLI (gh), or GitHub REST API in order of precedence.
---

# GitHub PR Comments

## Overview

This skill enables systematic analysis and management of GitHub pull request comments. It categorizes comments by type (Security, Code Changes, Documentation, Clarifications, Bugs & Code Smells, Other), assigns severity levels (Critical, High, Medium, Info), and helps automate responses and fixes based on user preferences.

## Workflow

Follow these steps when handling PR comment analysis and management:

### Step 1: Retrieve PR Comments

Use available tools in order of precedence:

1. **GitHub MCP Server** (if available): Use GitHub MCP tools to fetch PR comments
2. **GitHub CLI (`gh`)**: Use `gh pr view <pr-number> --json comments` or `gh api repos/{owner}/{repo}/pulls/{pr-number}/comments`
3. **GitHub REST API**: Use `curl` with GitHub API endpoints

Retrieve all comments including:
- Review comments (inline code comments)
- General PR comments
- Comment metadata (author, timestamp, line numbers)

### Step 2: Categorize and Assign Severity

For each comment, determine:

**Category** (one of six types):
- **Security**: Vulnerabilities, authentication, data exposure, unsafe practices
- **Code Changes**: Logic modifications, refactoring, implementation changes
- **Documentation**: Code comments, README, API docs, explanations
- **Clarifications**: Questions, requests for explanation
- **Bugs & Code Smells**: Identified bugs, quality issues, anti-patterns
- **Other**: Praise, meta-discussion, process notes

**Severity** (one of four levels):
- **Critical**: Blocking issues requiring immediate fix before merge
- **High**: Important issues that should be addressed
- **Medium**: Improvements and suggestions worth considering
- **Info**: Minor notes, questions, or acknowledgments

Refer to `references/examples.md` for detailed categorization guidelines and sample comments.

### Step 3: Present Summary Table

Show the user a comprehensive summary using one or more formats:

**Format Option A - Severity Distribution:**
```
| Category              | Critical | High | Medium | Info | Total |
|-----------------------|----------|------|--------|------|-------|
| Security              |    1     |  2   |   1    |  0   |   4   |
| Code Changes          |    0     |  1   |   3    |  2   |   6   |
| Documentation         |    0     |  1   |   2    |  1   |   4   |
| Clarifications        |    0     |  0   |   2    |  5   |   7   |
| Bugs & Code Smells    |    1     |  3   |   2    |  0   |   6   |
| Other                 |    0     |  0   |   0    |  3   |   3   |
```

**Format Option B - Grouped by Severity:**
List comments grouped by severity level (Critical → High → Medium → Info), showing category and brief description for each.

**Format Option C - Action Required:**
Summarize what must be fixed, what should be fixed, and what's optional.

Choose the format(s) that best fit the number and distribution of comments.

### Step 4: Ask User How to Proceed

Present clear options for handling comments:

```
How would you like to proceed with these comments?

1. 🤖 Auto-fix: Which comments should I attempt to fix automatically?
2. ✋ Won't Fix: Which comments should be marked as "won't fix"?
3. 👤 Manual: Which comments will you handle manually?

You can specify by:
- Comment numbers: "Auto-fix comments 1, 3, 5"
- Categories: "Auto-fix all Security and Bugs"
- Severity: "Auto-fix all Critical and High"
- Combinations: "Auto-fix all Critical Security and Bugs"
```

Wait for user response before proceeding to implementation.

### Step 5: Implement Auto-Fix Comments

For each comment marked for auto-fix:

**Before making changes:**
1. Post response on GitHub: "🤖 Working on this comment, please be patient."
2. Use appropriate GitHub tool to add the comment

**Implement the fix:**
1. Analyze the requested change
2. Make necessary code modifications
3. Test the change if possible
4. Commit the changes with descriptive message

**After successful fix:**
1. Post completion response on GitHub: "✅ Fixed in commit [hash]. [Brief description]"

**If unable to auto-fix:**
1. Post explanation: "⚠️ Unable to automatically fix this. [Reason]. Manual intervention needed."

**For "won't fix" comments:**
1. Post explanation: "Thanks for the feedback! After consideration, we've decided not to implement this change because [reason]."

### Step 6: Provide Summary Report

After processing all auto-fix comments, show the user:

```
Summary Report
═══════════════════════════════════════════════════════════════

✅ Auto-fixed (X comments):
  • [List of successfully fixed comments with commit hashes]

⚠️  Unable to auto-fix (Y comments):
  • [List with reasons]

✋ Marked as won't fix (Z comments):
  • [List with posted explanations]

👤 Left for manual handling (W comments):
  • [List of comments user will handle]
```

## Important Considerations

**Tool Selection:**
- Always try GitHub MCP Server first (most reliable)
- Fall back to `gh` CLI if MCP unavailable
- Use REST API as last resort
- Check tool availability before starting workflow

**Categorization Guidelines:**
- Some comments may fit multiple categories - choose the primary focus
- When uncertain about severity, err on the side of higher severity
- Security and Bugs with Critical/High severity should generally be auto-fixed unless complex
- Clarifications usually need manual responses with context

**Auto-Fix Limitations:**
- Don't auto-fix if the change requires architectural decisions
- Don't auto-fix if unclear about the requested change
- Don't auto-fix documentation that requires domain knowledge
- Always inform the user before posting "won't fix" responses

**GitHub Posting:**
- Always post status updates to maintain communication
- Include commit hashes in completion messages for traceability
- Be professional and constructive in all responses
- Tag the original commenter if appropriate: `@username`

## Resources

### references/

**examples.md**: Comprehensive examples including:
- Category definitions with severity indicators
- 13+ sample PR comments with categorization explanations
- Multiple summary table format examples
- User interaction flow examples
- Agent response templates for GitHub posting

Read this file to understand how to categorize comments and format outputs effectively.
