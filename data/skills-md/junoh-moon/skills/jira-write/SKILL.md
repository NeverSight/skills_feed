---
name: jira-write
description: |
  Create, edit, and transition Jira issues in COREPL project with proper epic linking, sprint assignment, and required fields.
  Use when user asks to create or modify a Jira ticket (e.g., "jira 이슈 만들어", "jira 티켓 생성", "이슈 상태 변경", "create jira issue", "COREPL 티켓").
  Covers: issue creation, parent epic linking, status transitions, adding comments.
context: fork
model: sonnet
---

# Jira Issue Creation

## CRITICAL: Scope Limitation

**This skill is ONLY for Jira operations. NEVER perform any of the following:**
- Code modifications or refactoring
- File creation or editing
- Git operations (branch, commit, etc.)
- Any development work

If the user's request involves both Jira ticket creation AND code work, **ONLY create the Jira ticket** and report back. Let the parent conversation handle the code work separately.

## Pre-Creation Checklist

Before calling `createJiraIssue`, gather ALL required information:

| Item | How to Get |
|------|------------|
| Assignee accountId | `lookupJiraAccountId` (default: current user) |
| Sprint ID | JQL: `project = COREPL AND sprint is not EMPTY ORDER BY created DESC` → extract `customfield_10020[0].id` |
| Parent Epic | JQL: `project = COREPL AND issuetype = Epic AND status != Done ORDER BY updated DESC` → suggest to user |

**Cloud ID**: `0d334135-ec08-4c00-8411-7a081dce39ca`

## Issue Type Names (CRITICAL)

Use **English names** in API calls, not Korean:

| Korean | English (use this) |
|--------|-------------------|
| 에픽 | Epic |
| 작업 | Task |
| 버그 | Bug |
| Feature Request | Feature Request |
| Internal Cleanup | Internal Cleanup |
| Customer Issue | Customer Issue |

## Create Issue

Required fields for `createJiraIssue`:

```
cloudId: "0d334135-ec08-4c00-8411-7a081dce39ca"
projectKey: "COREPL"
issueTypeName: "<English name>"
summary: "<title>"
description: "<content in Markdown>"
customfield_10468: {"value": "NO"}  # Security & Privacy Review
customfield_10020: <sprint_id>
assignee_account_id: "<accountId>"
```

**For Epics only**, add:
- `customfield_10011`: Epic Name
- `labels`: Reference similar epics (e.g., `["26H1", "Core", "CorePlatform"]`)

**WARNING**: Do NOT include `parent` field in createJiraIssue - it won't work.

## Link to Parent Epic

**IMPORTANT: Always display the epic key AND summary (title) so the user can make an informed decision.**

Example output before calling `editJiraIssue`:
```
상위 Epic 연결: COREPL-YYYY "Epic 제목/이름"
```

Then use `editJiraIssue`:

```
issueIdOrKey: "COREPL-XXXX"
fields: {"parent": {"key": "COREPL-YYYY"}}
```

## Post-Creation

Report with clickable link: `[COREPL-XXXX](https://ohouse.atlassian.net/browse/COREPL-XXXX)`

## Issue Transition

To change issue status:

1. Get transitions: `getTransitionsForJiraIssue`
2. Call `transitionJiraIssue` with:
   ```
   transition: {"id": "<transition_id>"}
   ```
   - NOT `transitionId: "281"` (wrong param name)
   - NOT `transition: "281"` (must be object)

## Add Comment

Use `addCommentToJiraIssue`:

```
cloudId: "0d334135-ec08-4c00-8411-7a081dce39ca"
issueIdOrKey: "COREPL-XXXX"
commentBody: "<content in Markdown>"
```

Optional visibility restriction:
```
commentVisibility: {"type": "group", "value": "developers"}
```
