---
name: PR Review Integration
description: >-
  Review pull requests by integrating GitHub operations with Linear issue
  tracking. Use when: (1) Validating PR changes against Linear issue
  requirements, (2) Checking if PR addresses all acceptance criteria from Linear
  issues, (3) Creating comprehensive PR reviews that link code changes to
  project requirements, (4) Identifying gaps between PR changes and issue
  requirements, or (5) Posting review findings to both GitHub PRs and Linear
  issues. Combines GitHub CLI operations with Linear MCP functions for end-to-end
  PR review workflows.
---

# PR Review Integration

Review pull requests by integrating GitHub operations with Linear issue tracking. Validate code changes against project requirements and provide comprehensive reviews.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Linear MCP server configured and available
- Access to both GitHub repository and Linear workspace

## Complete PR Review Workflow

### Step 1: Extract Context from PR

Get PR details:
```bash
gh pr view <pr-number> --json title,body,author,state,baseRefName,headRefName
```

Get changed files:
```bash
gh pr view <pr-number> --json files --jq '.files[].path'
```

Get PR diff:
```bash
gh pr diff <pr-number>
```

Extract Linear issue references:
```bash
gh pr view <pr-number> --json body --jq '.body' | grep -oE 'LIN-[0-9]+'
```

### Step 2: Fetch Linear Issue Requirements

Get issue details:
```typescript
mcp_Linear_get_issue({
  id: "LIN-123", // extracted from PR
  includeRelations: true // get related/blocking issues
})
```

Extract requirements from issue:
- Parse issue `description` for acceptance criteria
- Check `labels` for feature tags
- Review `comments` for additional context
- Check `relatedTo` and `blocks` for dependencies

### Step 3: Analyze PR Changes

Review code changes:
```bash
gh pr diff <pr-number>
gh pr diff <pr-number> -- path/to/file
gh pr view <pr-number> --json files --jq '.files[] | "\(.path): +\(.additions) -\(.deletions)"'
```

Check PR status:
```bash
gh pr checks <pr-number>
gh pr view <pr-number> --json mergeable,mergeStateStatus
```

### Step 4: Validate Against Requirements

Compare PR changes to issue requirements:

1. **Check Feature Completeness:**
   - Does PR implement all acceptance criteria?
   - Are all required features present?
   - Are edge cases handled?

2. **Check Code Quality:**
   - Follows project standards (AGENTS.md, Cursor rules)
   - Proper error handling
   - Tests included (if required)
   - Documentation updated

3. **Check Dependencies:**
   - Related issues addressed?
   - Blocking issues resolved?
   - Integration points considered?

4. **Identify Gaps:**
   - Missing requirements
   - Incomplete implementations
   - Additional work needed

### Step 5: Document Review Findings

**Option A: GitHub PR Comment**
```bash
gh pr comment <pr-number> --body "
## PR Review Summary

### ✅ Requirements Met
- [Requirement 1] - Implemented in [file]
- [Requirement 2] - Complete

### ⚠️ Gaps Identified
- [Gap 1] - Missing from issue LIN-123
- [Gap 2] - Needs additional work

### 📝 Code Quality
- Follows project standards
- [Additional notes]

### 🔗 Related Issues
- LIN-123 (main issue)
- LIN-124 (related)
"
```

**Option B: Linear Issue Comment**
```typescript
mcp_Linear_create_comment({
  issueId: "LIN-123",
  body: `
## PR Review: #${prNumber}

### Status: ${reviewStatus}

### Requirements Coverage
${requirementsChecklist}

### Code Quality
${qualityNotes}

### Next Steps
${nextSteps}
  `
})
```

**Option C: Update Linear Issue**
```typescript
mcp_Linear_update_issue({
  id: "LIN-123",
  state: "In Review", // or appropriate status
})
```

## Best Practices

1. **Always link PRs to Linear issues** for traceability
2. **Extract issue IDs early** to fetch requirements
3. **Validate against requirements first**, then code quality
4. **Document gaps clearly** with specific file/line references
5. **Update Linear issues** with review findings
6. **Use consistent review format** for readability
7. **Handle edge cases gracefully** (no issue, multiple issues, etc.)

## Reference Documentation

- **Review Patterns**: See [patterns.md](references/patterns.md) for detailed patterns, edge cases, and checklist templates
- **GitHub CLI Operations**: `.codex/skills/github-cli-operations/SKILL.md` - GitHub CLI patterns
- **Linear MCP Integration**: `.codex/skills/linear-mcp-integration/SKILL.md` - Linear MCP functions
