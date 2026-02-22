---
name: handoff
description: Create a handoff message to continue work in a new AI session. Use when the user wants to save context for later, create a handoff document, or prepare work for continuation in a fresh session. Captures relevant files, context, and goals so the next session can start immediately without rediscovering the codebase.
---

# Handoff

Create handoff messages to continue work seamlessly in new AI sessions.

## Getting Started

If you have no prior context of a conversation, this is likely a new session. Read any existing HANDOFF.md file in the current directory and follow its instructions to continue the work.

## When to Create a Handoff

Create a handoff when:
- The user wants to save work for a future session
- A session is ending and work needs to continue later
- The user explicitly asks to "create a handoff" or "save context"

## Creating a Handoff

### 1. Analyze the Conversation

Extract what matters for continuing the work:

**Identify relevant files (8-15 files, up to 20 for complex work):**
- Files that will be edited
- Dependencies being touched
- Relevant tests, configs, key reference docs
- Be generous—missing a critical file means rediscovery

**Draft context and goal description:**
- Describe what we're working on
- Preserve: decisions, constraints, user preferences, technical patterns
- Exclude: conversation back-forth, dead ends, meta-commentary

### 2. Respect User Input

The user controls what context matters. If they mentioned something to preserve, include it.

### 3. Output Format

Save the handoff to `HANDOFF.md` in the current working directory:

```markdown
# Handoff: [Brief Title]

## Goal
[Clear description of what needs to be done]

## Context
[Relevant background, decisions, constraints]

## Key Files
- `path/to/file1.ts` - [why it matters]
- `path/to/file2.ts` - [why it matters]
...

## Next Steps
1. [Step one]
2. [Step two]
...
```

## Example Handoff Structure

```markdown
# Handoff: Add User Authentication

## Goal
Implement JWT-based authentication for the API endpoints.

## Context
- Decided to use `jsonwebtoken` library
- Tokens expire after 24 hours
- Refresh tokens stored in httpOnly cookies
- User model already has `password_hash` field

## Key Files
- `src/routes/auth.ts` - Main auth routes (login, register, refresh)
- `src/middleware/auth.ts` - JWT verification middleware
- `src/models/user.ts` - User schema with password methods
- `tests/auth.test.ts` - Auth endpoint tests
- `.env.example` - JWT_SECRET configuration

## Next Steps
1. Install jsonwebtoken dependency
2. Implement register endpoint with password hashing
3. Implement login endpoint with token generation
4. Add auth middleware to protected routes
5. Write tests for all auth flows
```
