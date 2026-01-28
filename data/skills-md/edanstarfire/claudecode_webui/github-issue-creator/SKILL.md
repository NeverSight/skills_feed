---
name: github-issue-creator
description: Create well-structured GitHub issues focused on user problems and outcomes, not implementation. Use when user reports bugs or requests features to ensure clear, testable requirements without premature implementation details.
---

# GitHub Issue Creator

## Instructions

### When to Invoke This Skill
- User reports a bug or problem
- User requests a new feature
- User suggests quality of life improvement
- Need to document user need before implementation
- Converting vague request into clear issue

### Core Principle

**Issues describe WHAT and WHY, not HOW.**

Issues are contracts between user needs and development outcomes. They should enable:
- Clear understanding of the problem/need
- Objective evaluation of completeness
- Testing whether solution succeeds
- Flexibility in implementation approach

**Separate concerns:**
- **Issue** = User problem, expected outcome, acceptance criteria
- **Implementation Plan** = Technical approach (comes later, in comments or design docs)
- **PR Description** = What was actually implemented
- **Code Comments** = Why specific code decisions were made

### Issue Structure

#### Template

```markdown
## Problem / Need

<Clear description of what's wrong or what's needed from user perspective>

### Current Behavior (for bugs)
<What happens now that shouldn't>

### Expected Behavior
<What should happen instead, from user's point of view>

## Impact

### User Impact
<Who is affected and how?>
<What can't users do? What's frustrating?>

### Business/Project Impact
<Why does this matter?>
<What's the cost of not fixing this?>

## User Perspective

### User Story (optional but recommended)
As a [type of user]
I want to [action/capability]
So that [benefit/outcome]

### User Journey
1. User does X
2. [Current: System does Y / Expected: System should do Z]
3. User experiences [problem/benefit]

## Quality Standards

### Backward Compatibility
- [ ] Must not break existing functionality
- [ ] Can break existing functionality (explain why)
- [ ] New feature (no compatibility concern)

### Data Persistence
- [ ] Changes must persist across restarts
- [ ] Changes must persist across sessions
- [ ] Transient state (no persistence needed)

### Performance
- [ ] No performance requirements
- [ ] Must complete within [time]
- [ ] Must handle [scale] concurrent users/operations

### Security
- [ ] No security implications
- [ ] Requires authentication/authorization
- [ ] Handles sensitive data

## Acceptance Criteria

### Definition of Done
- [ ] <Testable outcome 1>
- [ ] <Testable outcome 2>
- [ ] <Testable outcome 3>

### Test Scenarios
1. **Scenario:** <Description>
   - **Given:** <Initial state>
   - **When:** <User action>
   - **Then:** <Expected result>

2. **Scenario:** <Another scenario>
   - **Given:** <Initial state>
   - **When:** <User action>
   - **Then:** <Expected result>

### Edge Cases to Consider
- <Edge case 1>
- <Edge case 2>

### Out of Scope (for this issue)
- <Related feature that's NOT included>
- <Future enhancement that's separate>

## Additional Context

### Related Issues
- Fixes #<issue>
- Related to #<issue>
- Blocks #<issue>

### References
- <Links to user feedback>
- <Links to documentation>
- <Screenshots/recordings>

### Notes
<Any additional context that helps understand the need>

---

## ⚠️ Implementation Details

**Implementation planning happens AFTER issue is approved.**

Once this issue is accepted:
1. Create implementation plan in comments or design doc
2. Break down into technical tasks
3. Identify files/functions to modify
4. Plan testing approach
5. Execute implementation

**Do NOT include in initial issue:**
- Specific files to modify
- Specific function names
- Exact variable names
- Detailed code structure
- UI mockups (unless critical to understanding the need)
```

### Conversation Flow to Create Issue

#### 1. Extract User Need

**Ask clarifying questions:**
- What are you trying to accomplish?
- What happens currently?
- What should happen instead?
- Who is affected by this?
- Why is this important?

**Avoid asking:**
- How should we implement this? (too early)
- Which files should we change? (not user concern)
- What should we name variables? (implementation detail)

#### 2. Understand Impact

**Explore:**
- How often does this happen?
- How severe is the impact?
- Who experiences this?
- What's the workaround (if any)?
- What happens if we don't fix this?

#### 3. Define Expected Behavior

**Focus on observable outcomes:**
- ✅ "User should see error message explaining what went wrong"
- ❌ "Display error in a red div with class 'error-message'"

- ✅ "Data should persist across browser sessions"
- ❌ "Store data in localStorage using JSON.stringify()"

- ✅ "Response time should be under 2 seconds"
- ❌ "Implement caching using Redis"

#### 4. Establish Acceptance Criteria

**Use Given-When-Then format:**
```
Given: <starting state>
When: <user action>
Then: <observable result>
```

**Make criteria testable:**
- ✅ "Submit button is disabled when form is invalid"
- ❌ "Form validation should work properly"

- ✅ "Clicking 'Delete' shows confirmation dialog before deletion"
- ❌ "Add confirmation for delete"

#### 5. Identify Quality Standards

**Ask about:**
- Can this break existing features?
- Does data need to persist?
- Are there performance requirements?
- Are there security concerns?

#### 6. Clarify Scope

**What's included:**
- Core functionality needed

**What's excluded (out of scope):**
- Nice-to-haves for future
- Related but separate features
- Edge cases that can wait

### Issue Quality Checklist

Before creating the issue, verify:

**Problem/Need is Clear:**
- [ ] Anyone can understand what's wrong or needed
- [ ] Current vs expected behavior is obvious
- [ ] Context is sufficient

**Impact is Explained:**
- [ ] Who is affected
- [ ] Why it matters
- [ ] Severity/priority is justified

**User Perspective is Maintained:**
- [ ] Written from user's viewpoint
- [ ] Focuses on outcomes, not internals
- [ ] Describes behavior, not code

**Acceptance Criteria are Testable:**
- [ ] Each criterion is objective
- [ ] Can verify each with test
- [ ] No ambiguous terms ("better", "improved", "nice")

**Quality Standards are Defined:**
- [ ] Backward compatibility addressed
- [ ] Data persistence specified
- [ ] Performance needs stated (if any)

**Implementation Details are Absent:**
- [ ] No specific file names
- [ ] No function/class names
- [ ] No UI mockups (unless essential)
- [ ] No technical architecture

**Scope is Bounded:**
- [ ] Focus is narrow enough
- [ ] Out of scope is documented
- [ ] Related issues are linked

### Creating the Issue

**Command:**
```bash
gh issue create --title "<type>: <brief description>" --body "$(cat <<'EOF'
<issue content using template above>
EOF
)"
```

**Title Format:**
- `feat: <user-facing feature>`
- `fix: <problem being fixed>`
- `chore: <maintenance task>`
- `docs: <documentation improvement>`
- `perf: <performance improvement>`

**Title Guidelines:**
- Brief (50 chars or less)
- User-focused ("Add dark mode toggle")
- Not implementation-focused ("Refactor CSS variables")
- Descriptive without being technical

### Common Anti-Patterns to Avoid

#### ❌ Anti-Pattern 1: Implementation in Disguise
```markdown
## Problem
We need to add a new endpoint POST /api/users/avatar

## Solution
1. Add route in web_server.py
2. Create upload handler in storage.py
3. Update User model with avatar_url field
```

**Why it's wrong:** This is an implementation plan, not a user need.

**Better version:**
```markdown
## Problem
Users cannot upload profile avatars

### Current Behavior
User profiles display only default avatar

### Expected Behavior
Users can upload custom avatar image that displays on their profile

## Acceptance Criteria
- User can select image file from device
- Uploaded avatar displays immediately
- Avatar persists across sessions
- Avatar size is limited to 2MB
```

#### ❌ Anti-Pattern 2: Vague Requirements
```markdown
## Problem
Make the UI better

## Expected
Better user experience
```

**Why it's wrong:** "Better" is subjective, not testable.

**Better version:**
```markdown
## Problem
Users struggle to find the delete button for sessions

### Current Behavior
Delete button only appears on hover and users miss it

### Expected Behavior
Delete button should be visible at all times for easy access

### User Impact
Users accidentally accumulate old sessions, cluttering their workspace

## Acceptance Criteria
- Delete button is visible without hover
- Button placement is consistent across all session items
- Button has clear "Delete" label or icon
```

#### ❌ Anti-Pattern 3: Mixed Concerns
```markdown
## Feature Request
Add dark mode and refactor CSS to use variables and update
documentation and add unit tests for theme switching
```

**Why it's wrong:** Multiple separate concerns bundled together.

**Better version:**
Create separate issues:
1. `feat: Add dark mode toggle for user interface`
2. `chore: Update UI documentation for theming`
3. (CSS refactoring happens during implementation, not separate issue)
4. (Tests are part of acceptance criteria, not separate issue)

#### ❌ Anti-Pattern 4: Solution Instead of Problem
```markdown
## Feature Request
Add a Redis cache for session data
```

**Why it's wrong:** Proposes solution without explaining problem.

**Better version:**
```markdown
## Problem
Session list takes 5+ seconds to load when user has 100+ sessions

### Current Behavior
Every page load fetches all session data from disk
Page is unresponsive during loading

### User Impact
Users with many sessions experience slow, frustrating interface
Unable to work efficiently

## Acceptance Criteria
- Session list loads in under 1 second for 100 sessions
- UI shows loading indicator during fetch
- List remains responsive during load

## Performance Requirement
Support up to 500 sessions per user with sub-2-second load times

---
Note: Redis, caching, pagination, or other solutions can be explored
during implementation planning
```

## Examples

### Example 1: Bug Report
```markdown
## Problem

WebSocket connection fails to reconnect after network interruption

### Current Behavior
When user's network connection drops (WiFi disconnect, laptop sleep):
- WebSocket connection is lost
- Messages stop flowing
- UI shows "connected" status incorrectly
- User must refresh page to reconnect

### Expected Behavior
When network connection is restored:
- WebSocket automatically reconnects
- UI shows "reconnecting" status
- Messages resume flowing
- No page refresh required

## Impact

### User Impact
Users lose work when network drops and don't realize connection is broken.
Must manually refresh and potentially lose unsent messages.

### Frequency
Common for laptop users who move between locations or close laptop lid.

## Acceptance Criteria

- [ ] Connection automatically reconnects when network restored
- [ ] UI accurately reflects connection state (connected/reconnecting/disconnected)
- [ ] Unsent messages are queued and sent after reconnection
- [ ] No data loss during reconnection

### Test Scenarios

1. **Scenario:** Network interruption during active session
   - **Given:** User has active session with WebSocket connected
   - **When:** Network disconnects then reconnects after 10 seconds
   - **Then:** WebSocket reconnects automatically, queued messages sent

2. **Scenario:** Laptop sleep/wake cycle
   - **Given:** User has active session
   - **When:** User closes laptop lid then reopens after 1 hour
   - **Then:** WebSocket reconnects, session resumes without refresh
```

### Example 2: Feature Request
```markdown
## Problem / Need

Users cannot organize sessions into folders or categories

### Current Situation
All sessions appear in flat list within project.
Users with 20+ sessions struggle to find specific session.

## Impact

### User Impact
Users waste time scrolling through long session lists.
No way to separate active vs archived sessions.

### User Story
As a developer managing multiple features,
I want to organize sessions into folders,
So that I can quickly find sessions related to specific work areas.

## Quality Standards

### Backward Compatibility
- [ ] Must support existing flat session structure

### Data Persistence
- [ ] Folder structure must persist across restarts

## Acceptance Criteria

- [ ] Users can create named folders within projects
- [ ] Users can move sessions between folders
- [ ] Users can rename folders
- [ ] Users can delete empty folders
- [ ] Folder structure persists across browser sessions

### Out of Scope
- Folder-level settings (separate feature)
- Sharing folders between projects
```

## Summary

This skill creates issues that clearly describe user problems and expected outcomes without constraining implementation approach, enabling flexible technical solutions while maintaining clear success criteria.
