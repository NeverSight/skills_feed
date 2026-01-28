---
name: edge-cases
description: "Analyze a PRD for edge cases, failure modes, and scenarios that might be missed. Use after creating a PRD to strengthen it. Triggers on: analyze edge cases, find edge cases, what could go wrong, edge case analysis."
---

# Edge Case Analysis

Systematically analyze a PRD to identify edge cases, failure modes, race conditions, and scenarios that might be overlooked during implementation.

---

## The Job

1. Read the provided PRD thoroughly
2. Analyze each user story and functional requirement
3. Identify potential edge cases across multiple categories
4. Propose updates to the PRD (new acceptance criteria, new stories, or updates to existing stories)

**Output:** A list of edge cases with recommended PRD updates.

---

## Edge Case Categories

### 1. Input Edge Cases
- **Empty/null values:** What if required fields are empty?
- **Boundary values:** Max lengths, min/max numbers, date ranges
- **Invalid formats:** Wrong data types, malformed input
- **Unicode/special characters:** Emojis, RTL text, HTML injection attempts
- **Large data:** What if there are 10,000 items instead of 10?

### 2. State Edge Cases
- **Race conditions:** Two users editing the same thing simultaneously
- **Stale data:** Data changed by another process between read and write
- **Partial completion:** What if the operation fails halfway?
- **Concurrent operations:** Multiple tabs, multiple sessions
- **Offline/reconnection:** What happens when connection drops?

### 3. User Behavior Edge Cases
- **Rapid clicks:** User clicks submit multiple times quickly
- **Back button:** User navigates back during an operation
- **Browser refresh:** User refreshes during a multi-step flow
- **Abandoned flows:** User leaves in the middle of a process
- **Unexpected navigation:** User directly accesses URLs they shouldn't

### 4. Error Handling Edge Cases
- **Network failures:** API timeouts, server errors
- **Validation errors:** How are errors displayed and recovered from?
- **Permission errors:** User loses access mid-operation
- **Resource exhaustion:** Rate limits, storage limits

### 5. Data Edge Cases
- **First-time use:** No data exists yet (empty states)
- **Legacy data:** Old data that doesn't match new schema
- **Data migration:** What happens to existing data when schema changes?
- **Cascade effects:** Deleting something that other things depend on

### 6. Security Edge Cases
- **Authentication expiry:** Session times out during operation
- **Authorization changes:** Permissions change while user is active
- **Input sanitization:** XSS, SQL injection, command injection
- **Data leakage:** Error messages exposing sensitive info

### 7. Performance Edge Cases
- **Cold start:** First load performance
- **Large payloads:** Response times with lots of data
- **Memory leaks:** Long-running sessions
- **N+1 queries:** Database performance at scale

---

## Analysis Process

For each user story in the PRD:

### Step 1: Read the Story
Understand what the story is trying to accomplish.

### Step 2: Apply Category Checklist
Go through each edge case category above and ask:
- Does this category apply to this story?
- What specific edge cases might occur?

### Step 3: Rate Severity
For each identified edge case:
- **Critical:** Could cause data loss, security breach, or system crash
- **High:** User-facing error or broken functionality
- **Medium:** Poor UX or minor functionality issue
- **Low:** Minor annoyance or cosmetic issue

### Step 4: Propose PRD Update
For each edge case, propose one of:
- **New acceptance criteria** for existing story
- **New user story** if scope is significant
- **Update to functional requirements**
- **Note in Technical Considerations**

---

## Output Format

```markdown
# Edge Case Analysis for [PRD Name]

## Summary
- Total edge cases identified: X
- Critical: X | High: X | Medium: X | Low: X

## Edge Cases by Story

### US-001: [Story Title]

| Edge Case | Category | Severity | Recommended Action |
|-----------|----------|----------|-------------------|
| User submits empty form | Input | High | Add acceptance criteria: "Empty form shows validation errors" |
| User double-clicks submit | User Behavior | Medium | Add acceptance criteria: "Submit button disabled after first click" |

### US-002: [Story Title]
...

## New Stories Recommended

### US-NEW-001: Handle concurrent edits
**Description:** As a user, I want to see a warning if someone else has edited the item since I started editing.

**Acceptance Criteria:**
- [ ] System checks for updates before saving
- [ ] Warning shown if data has changed
- [ ] User can choose to overwrite or refresh

**Rationale:** Addresses race condition edge case in US-003 and US-004.

## Updated Functional Requirements

- FR-NEW-1: The system must validate all user input on both client and server side
- FR-NEW-2: All destructive operations must be idempotent

## Technical Considerations to Add

- Implement optimistic locking for concurrent edit detection
- Add retry logic with exponential backoff for network failures
- Use database transactions for multi-step operations
```

---

## Checklist Before Completing

- [ ] Analyzed each user story against all edge case categories
- [ ] Rated severity for each edge case
- [ ] Provided concrete, actionable recommendations
- [ ] Grouped related edge cases to avoid duplicate stories
- [ ] Kept recommendations focused (don't over-engineer)
- [ ] Prioritized critical and high severity items

---

## Tips

- **Don't go overboard:** Focus on likely scenarios, not every theoretically possible edge case
- **Be specific:** "User enters > 255 characters in name field" is better than "Input validation"
- **Consider the context:** A personal project needs less edge case handling than a banking app
- **Look for patterns:** If you find one race condition, there are probably more
- **Think like an attacker:** What would someone try to break the system?
