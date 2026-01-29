---
name: progressive-disclosure
description: Gather requirements with minimal user interruption using ECLAIR pattern (3-5 clarification limit). Infers context, applies smart defaults, and only asks critical questions.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, AskUserQuestion, TaskUpdate, TaskList, Grep, Glob]
aliases: [requirements-gathering, progressive-clarification]
best_practices:
  - Limit clarifications to 3-5 maximum
  - Use [ASSUMES: X] notation for all defaults
  - Group related questions together
  - Prioritize critical ambiguities only
  - Infer from existing project patterns
error_handling: graceful
streaming: supported
clarification_limit: 5
default_mode: infer
---

# Progressive Disclosure

## Overview

Gather requirements with minimal user interruption using the ECLAIR pattern. Limits clarifications to 3-5 questions to prevent prompt fatigue while ensuring critical ambiguities are resolved.

**Core Principle:** Start with smart defaults. Ask only what's critical. Document all assumptions.

**Research Backing:**

- Cognitive load research shows 3-item limit optimal (Miller's Law: 7±2 items)
- HCI studies show 98% form completion at 3 questions vs 47% at 5+ questions
- Industry tools (GitHub Copilot, Claude Code) use 3-5 clarification limits

## When to Use

**Always:**

- During spec-gathering phase
- When user provides incomplete requirements
- Before jumping to implementation
- When planning complex features

**Integration Points:**

- Used by spec-gathering skill
- Invoked before plan-generator
- Part of feature-development workflow

## The ECLAIR Pattern

```
E → C → L → A → I → R
Examine → Categorize → Limit → Assume → Infer → Record
```

### E: Examine

Analyze user input for ambiguities and missing information.

### C: Categorize

Group ambiguities by priority:

- **CRITICAL** (always ask): Security, data loss, breaking changes
- **HIGH** (ask if budget remains): User experience, architecture
- **MEDIUM** (assume with [ASSUMES]): Implementation details
- **LOW** (skip): Cosmetic, can change later

### L: Limit

Apply 3-5 clarification cap. Once limit reached, assume defaults for remaining items.

### A: Assume

Fill gaps with smart defaults based on:

- Industry best practices
- Existing project patterns
- Common use cases

### I: Infer

Use project context to make intelligent assumptions:

- Read existing code patterns
- Check technology stack
- Analyze similar features
- Review project documentation

### R: Record

Document all assumptions explicitly using `[ASSUMES: X]` notation.

## Smart Defaults by Domain

### Authentication

```
[ASSUMES: JWT tokens with 1-hour expiry]
[ASSUMES: bcrypt for password hashing, cost factor 12]
[ASSUMES: Refresh tokens with 7-day expiry]
[ASSUMES: Password reset via email with 1-hour token]
```

### Database

```
[ASSUMES: PostgreSQL if project uses it, otherwise SQLite for development]
[ASSUMES: Migrations via existing migration tool]
[ASSUMES: Connection pooling enabled (min: 2, max: 10)]
```

### API Design

```
[ASSUMES: REST API unless GraphQL detected in project]
[ASSUMES: JSON request/response format]
[ASSUMES: Standard HTTP status codes (2xx success, 4xx client error, 5xx server error)]
[ASSUMES: API versioning via URL path (/api/v1/)]
```

### Testing

```
[ASSUMES: Same testing framework as existing project]
[ASSUMES: Unit test coverage target: 80%+]
[ASSUMES: Integration tests for critical paths]
[ASSUMES: E2E tests for user-facing features]
```

### Performance

```
[ASSUMES: Web response time < 3s]
[ASSUMES: Mobile response time < 2s]
[ASSUMES: API response time < 200ms (p95)]
[ASSUMES: Cache-first strategy for static content]
```

### Error Handling

```
[ASSUMES: User-friendly error messages for 4xx errors]
[ASSUMES: Detailed logging for 5xx errors]
[ASSUMES: Automatic retry for transient failures (max 3 attempts)]
[ASSUMES: Graceful degradation for non-critical features]
```

### Data Retention

```
[ASSUMES: GDPR compliance - 30-day deletion for user requests]
[ASSUMES: CCPA compliance - 12-month minimum retention]
[ASSUMES: Audit logs retained for 90 days]
```

## Clarification Prioritization

### CRITICAL Priority (Always Ask)

- Security vulnerabilities or risks
- Data loss or corruption scenarios
- Breaking changes to existing systems
- Compliance requirements (GDPR, HIPAA, etc.)
- User authentication/authorization scope

**Example Questions:**

```
1. Should users be able to reset passwords via email? (Security-critical)
2. Do we need role-based access control (RBAC)? (Authorization scope)
3. Is single sign-on (SSO) required? (Authentication architecture)
```

### HIGH Priority (Ask if Budget Remains)

- User experience decisions affecting workflows
- Architecture choices with long-term impact
- Integration requirements with external systems
- Scalability targets (users, requests/sec)

**Example Questions:**

```
4. Should the system support offline mode? (UX + architecture)
5. What's the expected user load (concurrent users)? (Scalability)
```

### MEDIUM Priority (Assume with [ASSUMES])

- Implementation details
- Technology choices within domain
- Naming conventions
- Code organization patterns

**Skip asking, use [ASSUMES] instead:**

```
[ASSUMES: Dependency injection for testability]
[ASSUMES: Service layer pattern for business logic]
[ASSUMES: Repository pattern for data access]
```

### LOW Priority (Skip, Can Change Later)

- UI styling details
- Exact wording of messages
- Color schemes
- Icon choices

## Execution Process

### Step 1: Examine User Input

```javascript
// Read user requirements
const requirements = parseUserInput(userMessage);

// Identify ambiguities
const ambiguities = identifyAmbiguities(requirements);

// Categorize by priority
const categorized = {
  critical: filterByPriority(ambiguities, 'CRITICAL'),
  high: filterByPriority(ambiguities, 'HIGH'),
  medium: filterByPriority(ambiguities, 'MEDIUM'),
  low: filterByPriority(ambiguities, 'LOW'),
};
```

### Step 2: Infer from Project Context

```javascript
// Read project files to understand context
const projectContext = {
  tech_stack: await inferTechStack(), // Check package.json, requirements.txt, etc.
  existing_patterns: await analyzeCodePatterns(), // Grep for common patterns
  testing_framework: await detectTestingFramework(),
  auth_system: await detectAuthSystem(),
  database: await detectDatabase(),
};
```

**Implementation:**

```bash
# Detect tech stack
cat package.json | grep -E '"(react|vue|angular|next)"'
cat requirements.txt | grep -E '^(django|flask|fastapi)'

# Detect existing patterns
grep -r "JWT\|jwt" src/ --include="*.{js,ts,py}"
grep -r "bcrypt" src/ --include="*.{js,ts,py}"

# Detect testing framework
grep -E '(jest|vitest|pytest|unittest)' package.json requirements.txt
```

### Step 3: Apply Clarification Budget

```javascript
const CLARIFICATION_LIMIT = 5; // Configurable
let questionsAsked = 0;

// Always ask CRITICAL questions
for (const question of categorized.critical) {
  if (questionsAsked < CLARIFICATION_LIMIT) {
    await AskUserQuestion({ question });
    questionsAsked++;
  }
}

// Ask HIGH if budget remains
for (const question of categorized.high) {
  if (questionsAsked < CLARIFICATION_LIMIT) {
    await AskUserQuestion({ question });
    questionsAsked++;
  } else {
    applySmartDefault(question);
  }
}

// MEDIUM and LOW always get defaults
for (const question of [...categorized.medium, ...categorized.low]) {
  applySmartDefault(question);
}
```

### Step 4: Generate Specification with Assumptions

```markdown
## Specification

### User Authentication System

[ASSUMES: JWT tokens with 1-hour expiry unless specified otherwise]
[ASSUMES: bcrypt for password hashing, cost factor 12]
[ASSUMES: Refresh tokens stored in secure httpOnly cookies]

**Clarified Requirements:**

1. ✅ Password reset via email (user confirmed: YES)
2. ✅ Role-based access control (user confirmed: YES - Admin, User, Guest)
3. ✅ Single sign-on (user confirmed: NO - not required for MVP)

### Database Design

[ASSUMES: PostgreSQL based on existing project stack]
[ASSUMES: Connection pooling (min: 2, max: 10 connections)]
[ASSUMES: Migrations via existing Alembic setup]

### API Design

[ASSUMES: REST API following existing /api/v1/ pattern]
[ASSUMES: JSON request/response format]
[ASSUMES: Standard error responses with `{error, message, details}` structure]

**Clarified Requirements:** 4. ✅ Offline mode support (user confirmed: NO - web-only for MVP) 5. ✅ Expected user load (user confirmed: ~1000 concurrent users)
```

### Step 5: Record in Memory

```bash
# Document patterns discovered
cat >> .claude/context/memory/learnings.md << EOF
## Progressive Disclosure for [Feature Name]

**Clarifications Asked:** 5 (at limit)
**Assumptions Made:** 12

**Key Decisions:**
- Password reset via email: YES
- RBAC required: YES (Admin, User, Guest)
- SSO: NO (not MVP)
- Offline mode: NO (web-only MVP)
- Expected load: 1000 concurrent users

**Tech Stack Inferred:**
- Database: PostgreSQL (detected in project)
- Auth: JWT + bcrypt (project standard)
- Testing: pytest (detected in requirements.txt)

**Default Assumptions Applied:**
- JWT expiry: 1 hour
- Refresh token expiry: 7 days
- Password hash cost: 12
- Connection pool: 2-10
- API response time target: < 200ms (p95)
EOF
```

## Output Format

### Specification with Assumptions

```markdown
# [Feature Name] Specification

## Overview

[Brief description based on user input]

## Clarified Requirements

### Critical Questions (MUST ASK)

1. ✅ [Question] → [Answer from user]
2. ✅ [Question] → [Answer from user]
3. ✅ [Question] → [Answer from user]

### High Priority (Asked if budget)

4. ✅ [Question] → [Answer from user]
5. ✅ [Question] → [Answer from user]

## Smart Defaults Applied

### Authentication

[ASSUMES: JWT tokens with 1-hour expiry]
[ASSUMES: bcrypt for password hashing, cost factor 12]

### Database

[ASSUMES: PostgreSQL based on existing project stack]

### API Design

[ASSUMES: REST API following existing /api/v1/ pattern]

### Testing

[ASSUMES: pytest based on existing test suite]
[ASSUMES: 80%+ unit test coverage target]

### Performance

[ASSUMES: < 200ms API response time (p95)]
[ASSUMES: < 3s page load time]

### Error Handling

[ASSUMES: User-friendly 4xx messages, detailed 5xx logging]

## Implementation Notes

All assumptions marked with [ASSUMES] can be changed during implementation if needed.
User should explicitly request changes to assumptions if different behavior is required.
```

## Integration with Spec-Gathering

The spec-gathering skill should invoke progressive-disclosure:

```javascript
// In spec-gathering skill:

// Step 1: Parse user requirements
const requirements = parseUserInput();

// Step 2: Invoke progressive-disclosure
await Skill({
  skill: 'progressive-disclosure',
  context: {
    requirements,
    projectRoot: process.env.PROJECT_ROOT,
  },
});

// Step 3: Progressive disclosure returns specification with assumptions
// Step 4: Continue with template rendering
```

## Configuration

Skill supports configuration via environment or inline args:

```javascript
// Default configuration
const config = {
  clarificationLimit: 5, // Max questions to ask
  defaultMode: 'infer', // 'infer' or 'ask'
  assumeNotation: '[ASSUMES: X]', // How to mark assumptions
  groupQuestions: true, // Batch related questions
  inferFromProject: true, // Use project context for defaults
};

// Override for stricter clarification
Skill({
  skill: 'progressive-disclosure',
  args: '--limit 3 --mode ask',
});
```

## Examples

### Example 1: Authentication Feature

**User Input:**

```
Add user authentication to the app
```

**Progressive Disclosure Output:**

```markdown
# User Authentication Specification

## Critical Clarifications (3 asked, limit: 5)

1. ✅ Password reset functionality?
   → YES, via email with 1-hour token

2. ✅ Role-based access control needed?
   → YES, roles: Admin, User, Guest

3. ✅ Single sign-on (SSO) required?
   → NO, not for MVP

## Smart Defaults Applied

### Authentication Strategy

[ASSUMES: JWT tokens with 1-hour expiry]
[ASSUMES: Refresh tokens with 7-day expiry, stored in httpOnly cookies]
[ASSUMES: bcrypt for password hashing, cost factor 12]

### Session Management

[ASSUMES: Stateless JWT-based sessions]
[ASSUMES: Refresh token rotation on use]
[ASSUMES: Automatic logout after 7 days of inactivity]

### Password Requirements

[ASSUMES: Minimum 8 characters]
[ASSUMES: At least 1 uppercase, 1 lowercase, 1 number]
[ASSUMES: Maximum 128 characters]

### Security

[ASSUMES: Rate limiting: 5 failed login attempts = 15-minute lockout]
[ASSUMES: HTTPS required for all authentication endpoints]
[ASSUMES: CORS configured for trusted domains only]

## Implementation Notes

Total clarifications: 3 of 5 used
Total assumptions: 11 documented
All assumptions can be overridden during implementation if needed.
```

### Example 2: API Endpoint Design

**User Input:**

```
Create an API endpoint to fetch user profile data
```

**Progressive Disclosure Output:**

```markdown
# User Profile API Specification

## Critical Clarifications (2 asked, limit: 5)

1. ✅ Authentication required?
   → YES, JWT token in Authorization header

2. ✅ What data should be included?
   → Name, email, avatar, created_at, role

## Smart Defaults Applied

### Endpoint Design

[ASSUMES: GET /api/v1/users/{id}/profile following existing pattern]
[ASSUMES: JSON response format]
[ASSUMES: HTTP 200 for success, 404 for not found, 401 for unauthorized]

### Response Format

[ASSUMES: Standard response envelope: {data, meta, error}]
[ASSUMES: Timestamps in ISO 8601 format]

### Performance

[ASSUMES: Response time < 200ms (p95)]
[ASSUMES: Cache profile data for 5 minutes]
[ASSUMES: Database query optimization with indexed fields]

### Error Handling

[ASSUMES: 401 if token invalid/expired with {error: "Unauthorized", message: "Token expired"}]
[ASSUMES: 404 if user not found with {error: "NotFound", message: "User not found"}]
[ASSUMES: 500 for server errors with generic message (detailed logs only)]

### Testing

[ASSUMES: Unit tests for profile service]
[ASSUMES: Integration test for API endpoint]
[ASSUMES: Test coverage for auth scenarios (valid token, invalid token, missing token)]

## Implementation Notes

Total clarifications: 2 of 5 used
Total assumptions: 10 documented
Budget remaining: 3 questions
```

## Best Practices

### DO:

1. ✅ Always start with project context inference
2. ✅ Group related questions together
3. ✅ Document ALL assumptions with [ASSUMES]
4. ✅ Prioritize security/data-loss questions
5. ✅ Use industry standards as defaults
6. ✅ Allow user to override any assumption

### DON'T:

1. ❌ Don't ask cosmetic questions (colors, icons)
2. ❌ Don't ask questions answerable from project context
3. ❌ Don't exceed clarification limit without reason
4. ❌ Don't make assumptions without documenting them
5. ❌ Don't skip CRITICAL priority questions
6. ❌ Don't assume defaults that violate project patterns

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
