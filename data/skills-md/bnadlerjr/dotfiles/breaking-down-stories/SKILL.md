---
name: breaking-down-stories
description: Breaks down user stories into small, actionable tasks. Use when decomposing user stories, planning sprint work, creating task lists from tickets, or when the user mentions story breakdown, task decomposition, or sprint planning.
argument-hint: [story or ticket reference]
allowed-tools:
  - AskUserQuestion
---

# Breaking Down Stories

Decompose a user story into small, actionable tasks using holistic brainstorming—consider all work categories at once rather than thinking sequentially through the story. Each task should be self-contained enough for a pair to pick up independently.

## Quick Start

Given a story, generate a flat task list where each task is small enough to complete in a single focused session:

```markdown
## Tasks for: [Story Title]

- [ ] Task description
- [ ] Task description -- (context: why this matters)
...
```

## Instructions

- Each task should be completable in a single pairing session (1-4 hours)
- Each task should be self-contained—a pair picking it up needs only the task description and context note
- Add a brief context note when the "why" is not obvious from the task description
- Include ALL work needed to complete the story (code, tests, builds, design, docs)
- Keep task descriptions brief—leave room for implementers to work out details
- Do NOT sequence tasks or assign owners—just brainstorm the work
- Focus on "what" not "how"

### TDD Guardrails

- NEVER create standalone test tasks—tests are implicit in every implementation task
- Implementers follow TDD: write failing test first, then implement
- Valid: "Add User class with validation" (tests written as part of implementation)
- Invalid: "Add User class" + "Write tests for User class" (redundant split)
- Invalid: "Set up test fixtures for users" (fixtures created when first test needs them)

### Story Quality Guardrails

Before breaking down a story, verify it's ready:

- **Missing acceptance criteria**: Ask for clarification or create a "Define acceptance criteria for [feature]" task
- **Too vague**: If you can't identify concrete work, the story needs refinement—flag this to the user
- **Too large** (spans multiple epics): Suggest splitting into smaller stories first
- **Feature-sized input** (spans multiple layers, multiple user roles, or lacks acceptance criteria): Suggest invoking `slicing-elephant-carpaccio` to produce thin vertical slices first, then `writing-agile-stories` for each slice, then return here for task decomposition
- **Missing user/value**: If "who" or "why" is unclear, ask before proceeding

### Input Classification

Before decomposing, classify the input:

| Signal | Classification | Action |
|--------|---------------|--------|
| Has acceptance criteria, single user role, bounded scope | **Story** | Proceed with task decomposition |
| Spans multiple layers, multiple roles, no acceptance criteria | **Feature** | Suggest `slicing-elephant-carpaccio` first |
| References an epic or multiple stories | **Epic** | Suggest splitting into stories with `writing-agile-stories` first |
| Single technical concern, already small | **Task** | No decomposition needed—inform the user |

If uncertain, ask the user whether to slice first or proceed directly.

### For Complex Stories

- If the story spans multiple systems or has unclear boundaries, invoke the `thinking-patterns` skill with `atomic` to decompose requirements first
- If verification keeps finding gaps, invoke the `thinking-patterns` skill with `self-consistency` to evaluate completeness from multiple perspectives

### For Modification-Heavy Stories

- If the story primarily modifies existing code (vs. greenfield), quickly scan relevant modules to identify integration points
- Keep reconnaissance lightweight—don't get pulled into implementation details

### Handling Open Questions

- If the story has open questions, create an explicit task: "Resolve: [question]"
- Skip tasks that depend on open questions—don't speculate on work that may not exist
- Note dependencies in the output so reviewers know the list is intentionally incomplete

## Workflow

1. **Gather the Story**
   - If input is a ticket reference (e.g., "PROJ-123"), use available tools to fetch details (e.g., `jira issue view PROJ-123`)
   - If input is prose, use it directly
   - Identify: who is the user, what do they want, why do they want it

2. **Brainstorm Tasks Holistically**
   - Consider all work categories at once: code changes, configuration, documentation, deployment, infrastructure
   - Include non-obvious work: "Update build script", "Add migration", "Update API docs"
   - Don't think sequentially through the story—capture all work regardless of order

3. **Right-Size Each Task**
   - Split tasks that span multiple concerns or would take multiple sessions
   - Combine trivial tasks that are always done together
   - Each task should be independently completable
   - Target 1-4 hours per task (one pairing session)
   - Add a context note when the task's purpose is not self-evident

4. **Verify Completeness**
   - Walk through the story end-to-end
   - Ask: "If all these tasks are done, is the story shippable?"
   - Add any missing tasks

5. **Check Task Quality**
   - Scan for any test-related tasks → remove them (tests are implicit)
   - Scan for "and" in task names → likely compound tasks, split them
   - Scan for vague tasks like "Implement feature" → add specificity
   - Scan for tasks missing context → add brief context notes where the "why" is not obvious
   - Confirm task count is reasonable (5-15 typical; fewer suggests tasks too large, more suggests story too large)
   - If task count exceeds 15, the input may be feature-sized → revisit Input Classification

## Anti-Patterns

Avoid these common mistakes:

| Bad Task | Problem | Better Task |
|----------|---------|-------------|
| "Write tests for login" | Separated test task | Remove—tests are implicit |
| "Set up test factories" | Test infrastructure task | Remove—created when first needed |
| "Implement authentication" | Too vague | "Add JWT token generation on login" |
| "Update code and fix bug" | Compound task | Split into two tasks |
| "Use bcrypt for passwords" | Implementation detail | "Add secure password hashing" |
| "Research options" | Not actionable | "Resolve: which auth library to use" |
| "Add password reset endpoint" | Missing context for non-obvious purpose | "Add password reset endpoint -- (entry point for the reset flow)" |

## Example

**Input Story:**

```markdown
## Story: User Resets Forgotten Password

When users cannot remember their password or suspect their account may be
compromised, they need a secure way to reset their credentials and regain
access. The process must verify their identity while remaining accessible.

### Context
Available from the login page when a user cannot authenticate.

### Acceptance Criteria

#### Scenario: Successful password reset
- Given a user with a verified email address
- When they request a password reset
- Then they receive an email with a secure reset link
- And the link expires after 1 hour
- And they can set a new password using the link

#### Scenario: Reset for unregistered email
- Given the email address is not in the system
- When someone requests a reset for that email
- Then the same "check your email" message is shown
- And no email is sent (prevents account enumeration)

#### Scenario: Expired reset link
- Given a user received a reset link more than 1 hour ago
- When they try to use the link
- Then they are informed the link has expired
- And they can request a new reset link

#### Scenario: Multiple reset requests
- Given a user has requested reset 3 times in 10 minutes
- When they request another reset
- Then they are asked to wait before trying again
```

**Output:**

```markdown
## Tasks for: User Resets Forgotten Password

- [ ] Add password reset request endpoint with email lookup
- [ ] Create reset token generation with secure random and 1-hour expiration
- [ ] Store reset tokens with user association and expiration timestamp
- [ ] Add email template for password reset link
- [ ] Integrate email sending for reset requests
- [ ] Add password reset confirmation endpoint with token validation
- [ ] Invalidate token after successful password change -- (prevents token reuse)
- [ ] Add rate limiting: max 3 requests per 10 minutes per email -- (prevents brute force)
- [ ] Return consistent response regardless of email existence -- (prevents account enumeration)
- [ ] Add error handling for expired tokens with re-request guidance
- [ ] Update login page with "Forgot password?" link
- [ ] Add password validation on reset -- (same rules as registration)
```

## Output Format

Output tasks as a simple list:

```markdown
## Tasks for: [Story Title]

- [ ] Task description
- [ ] Task description -- (context: why this matters)
- [ ] Task description
...
```

Keep descriptions to one line. No estimates, no assignments, no implementation details. Add context notes sparingly—only when the "why" is not obvious from the task description.

## Success Criteria

A well-decomposed story produces tasks where:
- Every task is independently completable in a single pairing session (1-4 hours)
- No task is a standalone test task (TDD is implicit)
- The task list covers ALL work needed to ship the story
- A pair can pick up any task using only its description and context note
- Task count is 5-15 (fewer = tasks too large, more = story too large or feature-sized)
- Walking through all completed tasks would make the story shippable

## Related Skills

### Upstream (use before this skill)
- `slicing-elephant-carpaccio` — Slice a feature into thin vertical increments. Use when input is feature-sized (see Input Classification). Each slice becomes a story candidate.
- `writing-agile-stories` — Write BDD stories with acceptance criteria. Use when input lacks acceptance criteria or clear scope.

### Downstream (use after this skill)
- `implementation-planning` — Create detailed implementation plans for individual tasks from the task list.

### Typical workflow
`Feature` → `slicing-elephant-carpaccio` → `writing-agile-stories` → `breaking-down-stories` → `implementation-planning`
