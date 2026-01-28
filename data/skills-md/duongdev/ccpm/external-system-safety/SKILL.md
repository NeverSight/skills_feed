---
name: external-system-safety
description: Enforces confirmation workflow for EXTERNAL system writes (Jira, Confluence, BitBucket, Slack) ONLY. NEVER activates for Linear operations (Linear is internal tracking). Auto-activates when detecting potential writes to external PM systems (status updates, page creation, PR posts, notifications). Blocks execution and displays exact content that will be written. Requires explicit "yes" confirmation (rejects "ok", "sure", ambiguous responses). All Linear operations execute automatically without confirmation. Works alongside ccpm-code-review to ensure quality before external broadcasts. Provides audit trail of all confirmed operations. Allows batch operations with granular per-item confirmation when needed.
allowed-tools: read-file, grep, browser
---

# External System Safety Guardrails

This skill provides automatic safety enforcement for all operations involving external project management systems.

## ⚠️ CRITICAL: Linear Exclusion

**DO NOT activate this skill for Linear operations. Linear is CCPM's internal tracking system.**

**NEVER ask for confirmation when:**
- Creating Linear issues
- Updating Linear issue descriptions, status, labels, or assignments
- Adding comments to Linear issues
- Any other Linear MCP operations

**This skill ONLY applies to EXTERNAL systems:** Jira, Confluence, BitBucket, Slack, etc.

---

## Instructions

### ⛔ ABSOLUTE RULES - NEVER VIOLATED

Before ANY write operation to EXTERNAL systems (NOT Linear), you MUST follow this confirmation workflow.

### 1. Detect External System Write Operations

**Jira**:
- Creating new issues or epics
- Updating issue status or fields
- Posting comments
- Changing assignees or labels
- Transitioning workflow states

**Confluence**:
- Creating new pages
- Editing existing pages
- Adding comments
- Updating page properties
- Deleting content

**BitBucket**:
- Creating pull requests
- Posting PR comments
- Approving or declining PRs
- Updating PR metadata
- Merging PRs

**Slack**:
- Sending messages to channels
- Posting notifications
- Updating channel topics
- Creating new channels
- Direct messages

### 2. STOP and Display Intent

When you detect a potential write operation:

```
⚠️ EXTERNAL SYSTEM WRITE DETECTED

System: [Jira/Confluence/BitBucket/Slack]
Operation: [Create/Update/Delete/Post]
Target: [Specific item/location]

Details:
---
[Exact content that will be written/posted]
---

This will modify external systems. Proceed? (yes/no)
```

### 3. Wait for Explicit Confirmation

**Acceptable confirmations**:
- "yes"
- "confirm"
- "proceed"
- "go ahead"
- "do it"

**NOT acceptable** (require re-confirmation):
- Silence
- "ok" (too ambiguous)
- "sure" (too casual)
- Any other response

### 4. Only Then Execute

After receiving explicit "yes" or equivalent:
1. Execute the operation
2. Log what was done
3. Provide confirmation of success
4. Show link to updated item if available

### Examples

#### Example 1: Jira Status Update

```
User: "Update Jira ticket ABC-123 to Done"

Claude: ⚠️ EXTERNAL SYSTEM WRITE DETECTED

System: Jira
Operation: Update Status
Target: ABC-123

Details:
---
Status: In Progress → Done
---

This will modify external systems. Proceed? (yes/no)

User: yes

Claude: ✅ Updated Jira ABC-123 status to Done
Link: https://jira.company.com/browse/ABC-123
```

#### Example 2: Confluence Page Creation

```
User: "Create a Confluence page documenting the new API"

Claude: ⚠️ EXTERNAL SYSTEM WRITE DETECTED

System: Confluence
Operation: Create Page
Target: Engineering Space

Details:
---
Title: "New Payment API Documentation"
Parent: API Documentation
Content: [First 200 characters of content...]
---

This will modify external systems. Proceed? (yes/no)

User: no, not yet

Claude: Understood. I won't create the Confluence page. Let me know when you're ready.
```

#### Example 3: Slack Notification

```
User: "Let the team know the feature is deployed"

Claude: ⚠️ EXTERNAL SYSTEM WRITE DETECTED

System: Slack
Operation: Post Message
Target: #engineering channel

Details:
---
Message: "✅ Payment gateway integration deployed to production. All tests passing."
---

This will modify external systems. Proceed? (yes/no)

User: yes

Claude: ✅ Posted message to #engineering
```

#### Example 4: Multiple Operations

```
User: "Update Jira to Done and notify the team on Slack"

Claude: ⚠️ EXTERNAL SYSTEM WRITE DETECTED

I need to perform 2 write operations:

1. Jira - Update Status
   Target: ABC-123
   Change: In Progress → Done

2. Slack - Post Message
   Target: #engineering
   Message: "Task ABC-123 completed"

Proceed with both? (yes/no)

User: only the jira update

Claude: Got it. I'll update Jira ABC-123 but skip the Slack notification.

⚠️ Confirming: Update Jira ABC-123 to Done? (yes/no)

User: yes

Claude: ✅ Updated Jira ABC-123 to Done
❌ Skipped Slack notification as requested
```

### Always Allowed (No Confirmation Needed)

The following operations NEVER require confirmation:

✅ **Read operations**:
- Fetching Jira issues
- Searching Confluence pages
- Viewing BitBucket PRs
- Reading Slack message history
- Querying any external system

✅ **Linear operations**:
- All Linear operations (internal tracking)
- Creating/updating Linear issues
- Adding comments to Linear
- Changing Linear status

✅ **Local file operations**:
- Reading/writing files in `.claude/` directory
- Editing codebase files
- Creating local documentation
- Git operations (commit, branch, etc.)

✅ **Code operations**:
- Writing production code
- Writing tests
- Running builds
- Executing tests

### Special Cases

#### Case 1: User Explicitly Says "Without Confirmation"

If user explicitly requests bypassing confirmation:

```
User: "Update Jira ABC-123 to Done without asking me"
```

Still require ONE confirmation for safety:

```
Claude: I understand you want to skip confirmations, but for safety I need ONE confirmation:

Update Jira ABC-123 to Done? (yes/no)

[After yes, you can skip future confirmations in this session if user requests]
```

#### Case 2: Batch Operations

For multiple similar operations:

```
User: "Update all 5 tickets to Done"

Claude: ⚠️ EXTERNAL SYSTEM WRITE DETECTED

Batch operation: Update 5 Jira tickets to Done
- ABC-123
- ABC-124
- ABC-125
- ABC-126
- ABC-127

Proceed with all? (yes/no/show details)

User: yes

Claude: ✅ Updated all 5 tickets to Done
```

#### Case 3: User Seems Confused

If user response is unclear:

```
User: "maybe"
User: "I guess"
User: "if you think so"

Claude: I need explicit confirmation. Please respond with "yes" to proceed or "no" to cancel.
```

### Integration with CCPM Commands

This skill works alongside CCPM commands that write to external systems:

**Commands that trigger this skill**:
- `/ccpm:done` (creates BitBucket PR, sends Slack notification)
- `/ccpm:sync` (updates Jira status)
- Any command with external system integration

**How it works**:
1. User invokes command
2. Command prepares to write to external system
3. **This skill auto-activates**
4. Confirmation workflow runs
5. Only after "yes" does command proceed

### Error Handling

If external system write fails after confirmation:

```
Claude: ⚠️ Write operation failed

System: Jira
Error: "Insufficient permissions to update ABC-123"

Possible solutions:
1. Check your Jira permissions
2. Ensure you're on the correct project
3. Verify the ticket exists

Would you like me to retry? (yes/no)
```

### Audit Trail

After any confirmed external write:

```
Claude: ✅ Operation completed

Audit trail:
- Timestamp: 2025-11-19 14:32:15 UTC
- System: Jira
- Operation: Update Status
- Target: ABC-123
- User confirmed: Yes
- Result: Success

Logged to: .claude/audit-log.json
```

## Why This Skill Exists

**Problem**: Easy to accidentally write to external systems when:
- Using agents that bypass command safety checks
- Misunderstanding what a command does
- Quickly testing a workflow
- Copy-pasting commands without reading

**Solution**: This skill provides an automatic safety layer:
- ✅ Works even when using agents directly
- ✅ Catches writes regardless of how they're initiated
- ✅ Provides clear "what will happen" preview
- ✅ Gives user final control before execution

**Complements existing safety**:
- Commands have built-in safety rules (`SAFETY_RULES.md`)
- This skill adds automatic detection layer
- Works together for defense-in-depth

## Reference

For complete safety rules, see: `~/.claude/plugins/ccpm/commands/SAFETY_RULES.md`
