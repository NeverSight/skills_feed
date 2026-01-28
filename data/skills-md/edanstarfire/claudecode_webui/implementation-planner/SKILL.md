---
name: implementation-planner
description: Create structured implementation plans from validated requirements. Use when requirements are clear and you need to break down implementation into actionable steps with testing approach.
---

# Implementation Planner

## Instructions

### When to Invoke This Skill
- After requirements are validated and clear
- Before starting implementation work
- User asks for implementation plan
- Complex feature requiring structured approach
- Need to communicate approach to stakeholders

### Planning Principles

1. **Top-Down Decomposition** - Break complex tasks into smaller steps
2. **Dependency Ordering** - Plan steps in logical sequence
3. **Risk Identification** - Flag potential issues early
4. **Testing Strategy** - Define how to verify each step
5. **Rollback Plan** - Consider how to undo if needed

### Standard Workflow

#### 1. Understand the Goal

From validated requirements, extract:
- **Primary objective**: The main thing being accomplished
- **Success criteria**: How to know it's done
- **Constraints**: Technical or business limitations
- **Scope boundaries**: What's included/excluded

#### 2. Analyze Current State

Investigate existing codebase:
- **Related files**: What code exists in this area?
- **Architecture patterns**: How is similar functionality implemented?
- **Dependencies**: What does this interact with?
- **Tests**: What test coverage exists?

Use these tools:
- `Grep` - Search for related code
- `Glob` - Find relevant files
- `Read` - Understand existing implementation

#### 3. Identify Components to Modify

List specific files and components:
- **Backend changes**: API endpoints, business logic, data models
- **Frontend changes**: UI components, state management
- **Database changes**: Schema, migrations
- **Configuration changes**: Settings, environment variables
- **Documentation changes**: README, API docs

#### 4. Create Step-by-Step Plan

Break down into discrete steps:

**Format:**
```
## Implementation Plan

### Step 1: <Component/Area>
**Files to modify:**
- `path/to/file.py` - <what changes>
- `path/to/other.js` - <what changes>

**Changes:**
- <Specific change 1>
- <Specific change 2>

**Testing:**
- <How to test this step>

### Step 2: <Next Component/Area>
...
```

**Guidelines:**
- Each step should be independently testable
- Order steps by dependency (do foundation first)
- Estimate complexity: Simple/Moderate/Complex
- Flag risks or unknowns

#### 5. Define Testing Approach

For each type of change:

**Backend Changes:**
- Unit tests for business logic
- Integration tests for API endpoints
- Manual testing with test server (`--port 8001`)

**Frontend Changes:**
- Visual verification in browser
- User interaction testing
- Cross-browser if significant UI change

**Data Changes:**
- Test migration up and down
- Verify data integrity
- Test with production-like data

#### 6. Identify Risks and Considerations

**Common Risks:**
- Breaking changes to existing functionality
- Performance impact
- Security implications
- Backward compatibility
- Data migration issues

**Document:**
- What could go wrong?
- How to mitigate?
- Rollback strategy if needed?

### Plan Templates

#### Feature Addition Template
```
## Implementation Plan: <Feature Name>

### Overview
<1-2 sentence summary of what's being added>

### Architecture Decision
<Key design choice and rationale>

### Step 1: Data Layer
**Files:**
- `src/models.py` - Add new model
- `src/storage.py` - Add persistence methods

**Changes:**
- Define data structure
- Add CRUD operations
- Add validation

**Testing:**
- Unit tests for model
- Test storage operations

### Step 2: Business Logic
**Files:**
- `src/manager.py` - Add business logic

**Changes:**
- Implement core functionality
- Handle edge cases
- Add error handling

**Testing:**
- Unit tests for logic
- Integration tests

### Step 3: API Layer
**Files:**
- `src/web_server.py` - Add endpoints

**Changes:**
- Add REST endpoints
- Add input validation
- Add error responses

**Testing:**
- Test with curl/Postman
- Verify error cases

### Step 4: Frontend
**Files:**
- `frontend/src/components/...` - Add UI

**Changes:**
- Create component
- Wire up API calls
- Add user feedback

**Testing:**
- Manual browser testing
- Test all user flows

### Risks
- <Potential issue 1>
- <Potential issue 2>

### Rollback Plan
<How to undo if needed>
```

#### Bug Fix Template
```
## Implementation Plan: Fix <Bug Description>

### Root Cause
<What's causing the bug>

### Impact Analysis
<What's affected by this bug>

### Fix Approach
<How to fix it>

### Step 1: Add Test to Reproduce
**Files:**
- `src/tests/test_<area>.py` - Add failing test

**Changes:**
- Create test case that reproduces bug
- Verify test fails with current code

### Step 2: Implement Fix
**Files:**
- `src/<area>.py` - Apply fix

**Changes:**
- <Specific code change>

**Testing:**
- Run test - should now pass
- Manual verification

### Step 3: Add Regression Tests
**Files:**
- Add edge case tests

**Changes:**
- Test boundary conditions
- Test related scenarios

### Verification
- All existing tests still pass
- New tests pass
- Manual testing confirms fix
```

#### Refactor Template
```
## Implementation Plan: Refactor <Component>

### Goal
<Why refactoring - what improves>

### Current Structure
<How it works now>

### Proposed Structure
<How it will work>

### Step 1: Add Tests for Current Behavior
**Files:**
- `src/tests/...` - Add comprehensive tests

**Changes:**
- Test all current behavior
- Ensure 100% coverage of what's being refactored

**Why:** Safety net - tests lock in current behavior

### Step 2: Extract <Component>
**Files:**
- `src/<new_file>.py` - Create new module

**Changes:**
- Extract functionality
- Keep interface same
- No behavior change

**Testing:**
- All existing tests still pass

### Step 3: Refactor Internals
**Files:**
- `src/<new_file>.py` - Improve internals

**Changes:**
- Clean up implementation
- Still same interface

**Testing:**
- All tests still pass

### Step 4: Update Callers (if needed)
**Files:**
- Files that use refactored code

**Changes:**
- Update imports
- Update calls if interface changed

### Verification
- All tests pass
- No behavior changes
- Code is cleaner/more maintainable
```

## Examples

### Example 1: New feature plan
```
Context: Add user profile page with avatar upload

Plan:
1. Backend - Add avatar storage endpoint
   - Files: web_server.py, storage.py
   - Accept file upload, validate size/type
   - Store in data/avatars/
   - Test: curl upload test

2. Backend - Add profile retrieval endpoint
   - Files: web_server.py
   - Return user data + avatar URL
   - Test: API response format

3. Frontend - Create ProfilePage component
   - Files: frontend/src/components/ProfilePage.vue
   - Display user info, avatar
   - Add upload button
   - Test: Manual browser testing

4. Frontend - Wire up upload
   - Handle file selection
   - Call API
   - Show upload progress
   - Update avatar on success
   - Test: Full upload flow
```

### Example 2: Bug fix plan
```
Context: Fix null pointer when login with empty email

Plan:
1. Add failing test
   - Files: test_auth.py
   - Test login with empty email
   - Verify it currently fails with null pointer

2. Add validation
   - Files: web_server.py (login endpoint)
   - Check email is not empty before processing
   - Return 400 error if empty
   - Test: Run test - should pass now

3. Add frontend validation
   - Files: frontend/src/components/LoginForm.vue
   - Disable submit if email empty
   - Show validation message
   - Test: Try to submit with empty email
```

### Example 3: Complex feature plan
```
Context: Add real-time session collaboration (multiple users in one session)

Plan - HIGH LEVEL:
1. Design phase (not implementation yet)
   - Research: How to handle concurrent edits?
   - Research: Conflict resolution strategy?
   - Research: WebSocket message format?
   - Decision: Document chosen approach

2. Data model phase
   - Add session membership concept
   - Add presence tracking
   - Add edit locking or OT/CRDT

3. Backend phase
   - WebSocket broadcast to session members
   - Handle join/leave
   - Conflict resolution

4. Frontend phase
   - Show active users
   - Merge incoming edits
   - Show who's typing

Note: This is MVP roadmap. Each phase needs detailed plan when ready.
```
