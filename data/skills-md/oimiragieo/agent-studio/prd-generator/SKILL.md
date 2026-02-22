---
name: prd-generator
description: Generate structured Product Requirements Documents using hypothesis-driven methodology with Implementation Phases tracking.
version: 1.0
model: sonnet
invoked_by: agent
user_invocable: false
tools: [Read, Write, AskUserQuestion]
assigned_agents: [pm]
best_practices:
  - Problem-first before solution
  - Evidence-backed hypothesis
  - MoSCoW prioritization for scope
  - Implementation Phases table for traceability
error_handling: standard
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# PRD Generator Skill

## Overview

Generate structured Product Requirements Documents (PRDs) using problem-first, hypothesis-driven methodology. Ensures clear problem statements, evidence-backed decisions, and traceable implementation phases.

**Core principle:** Validate "why" before "how". Problem → Evidence → Hypothesis → Solution.

## When to Use

**Always:**

- New features requiring product definition
- Product changes requiring stakeholder alignment
- Requirements gathering for HIGH/EPIC complexity features
- Feature requests needing structured analysis

**Use specifically for:**

- Features with unclear requirements (progressive disclosure)
- Multi-phase implementations needing tracking
- Features requiring decision documentation
- Product initiatives needing success metrics

**Don't use for:**

- Simple bug fixes (no PRD needed)
- Trivial configuration changes
- Code-only refactors without product impact

## Purpose

1. **Problem-First**: Define problem with evidence before proposing solutions
2. **Hypothesis-Driven**: State measurable hypothesis for validation
3. **MoSCoW Prioritization**: Prevent scope creep with Must/Should/Could/Won't
4. **Implementation Phases**: Track progress with phases table (Status, Dependencies, Plan Links)
5. **Decision Log**: Record "why we chose X over Y" for future reference
6. **Traceability**: PRD → Planner → Developer with full context

## Workflow

### Step 1: Gather Requirements

**Interactive Mode (when requirements unclear):**

```javascript
// Use AskUserQuestion for structured gathering
const problem = await AskUserQuestion({
  question: 'What problem does this solve? (Be specific about user pain points)',
});

const evidence = await AskUserQuestion({
  question: 'What evidence shows this problem exists? (Data, feedback, metrics)',
});

const hypothesis = await AskUserQuestion({
  question: 'What measurable outcome will prove this feature solves the problem?',
});
```

**Prompt Mode (when requirements provided):**

```
Extract requirements from user prompt or task description
```

**Progressive Disclosure (for ambiguous features):**

If requirements are unclear, use 8-phase questioning workflow:

1. **Initiate**: Clarify feature goal and scope
2. **Foundation**: Understand problem context
3. **Grounding (Market)**: Research similar solutions
4. **Deep Dive**: Explore capabilities and user flows
5. **Grounding (Technical)**: Assess feasibility
6. **Decisions**: Document choices and trade-offs
7. **Generate**: Create PRD from gathered context

**When to use Progressive Disclosure:**

- HIGH/EPIC complexity features
- Ambiguous user requests ("make it better")
- New product areas without existing patterns
- Features requiring stakeholder alignment

**When to skip:**

- Clear requirements provided
- Similar features already built
- Small scope changes

### Step 2: Load Template

```javascript
// Read PRD template
const template = Read({ file_path: '.claude/templates/prd-template.md' });
```

Template includes these sections (required):

- Problem Statement
- Evidence
- Key Hypothesis
- What We're NOT Building (scope exclusions)
- Success Metrics table
- Core Capabilities (MoSCoW)
- Users & Context
- Solution Detail (MVP Scope, User Flow)
- Technical Approach
- Implementation Phases table
- Decisions Log table
- Research Summary
- Risks table
- Open Questions

### Step 3: Fill Template Sections

**Problem Statement (Evidence-Backed):**

```markdown
## Problem Statement

[Specific problem description with user impact]

## Evidence

- User feedback: [quotes or summary]
- Data: [metrics showing problem scale]
- Business impact: [why this matters now]
```

**Key Hypothesis:**

```markdown
## Key Hypothesis

We believe [capability] will [solve problem] for [users].
We'll know we're right when [measurable outcome].

Example:
We believe adding JWT refresh tokens will reduce user re-authentication friction for mobile users.
We'll know we're right when session timeout complaints drop by 50% and mobile DAU increases by 10%.
```

**Success Metrics:**

| Metric                     | Target | How Measured            |
| -------------------------- | ------ | ----------------------- |
| Session timeout complaints | -50%   | Support ticket analysis |
| Mobile DAU                 | +10%   | Analytics dashboard     |
| Token refresh success rate | >95%   | Backend logs            |

**Core Capabilities (MoSCoW):**

| Priority | Capability                 | Rationale                                    |
| -------- | -------------------------- | -------------------------------------------- |
| Must     | JWT refresh token endpoint | Required for MVP - enables session extension |
| Must     | Token rotation on refresh  | Security best practice                       |
| Should   | Refresh token revocation   | Allows user logout from all devices          |
| Could    | Token usage analytics      | Nice to have for monitoring                  |
| Won't    | Biometric auth integration | Out of scope - future consideration          |

**MoSCoW Definitions:**

- **Must**: MVP blocker - without this, feature fails
- **Should**: High value, include if time permits
- **Could**: Nice to have, defer if needed
- **Won't**: Explicitly excluded from current scope

**Users & Context:**

```markdown
## Users & Context

**Primary User**: Mobile app user (iOS/Android) who experiences session expiration mid-workflow

**Current Behavior**: User logs in → session expires after 1 hour → forced to re-login → loses context

**Trigger**: Session expiration during active use

**Success State**: User stays logged in seamlessly, only re-authenticates when truly needed

**Job to Be Done**: When my session expires, I want to continue my work without re-entering credentials, so I can maintain my workflow momentum.
```

**Implementation Phases Table:**

| #   | Phase         | Description                                      | Status  | Parallel | Depends | Plan Link |
| --- | ------------- | ------------------------------------------------ | ------- | -------- | ------- | --------- |
| 1   | Design        | Auth architecture design with refresh token flow | pending | No       | -       | -         |
| 2   | Backend API   | Implement /refresh endpoint with token rotation  | pending | No       | 1       | -         |
| 3   | Mobile Client | Add refresh logic to mobile SDK                  | pending | No       | 2       | -         |
| 4   | Testing       | E2E tests for refresh flows                      | pending | Yes      | 2,3     | -         |
| 5   | Monitoring    | Add refresh metrics to dashboard                 | pending | Yes      | 2       | -         |

**Phase Columns Explained:**

- **#**: Phase number
- **Phase**: Short phase name
- **Description**: What gets built in this phase
- **Status**: pending | in_progress | completed | blocked
- **Parallel**: Can this run in parallel with other phases?
- **Depends**: Which phase(s) must complete first? (comma-separated numbers)
- **Plan Link**: Link to planner's implementation plan (.claude/context/plans/impl-{phase}-{date}.md)

**Decisions Log:**

| Decision         | Choice                             | Alternatives                   | Rationale                                   |
| ---------------- | ---------------------------------- | ------------------------------ | ------------------------------------------- |
| Token storage    | Secure storage (Keychain/KeyStore) | Local storage, Session storage | Security requirement - tokens are sensitive |
| Refresh strategy | Automatic on 401                   | Manual user action             | Better UX - transparent to user             |
| Token lifetime   | Access: 1hr, Refresh: 30 days      | Access: 5min, Refresh: 90 days | Balance security and UX                     |

**Research Summary:**

```markdown
## Research Summary

**Market Context:**

- Auth0, Firebase use similar refresh token patterns
- Industry standard: short-lived access + long-lived refresh
- OWASP recommends token rotation on refresh

**Technical Context:**

- Existing JWT library supports refresh
- Mobile SDK has secure storage
- Backend already has session management
```

**Risks:**

| Risk                         | Likelihood | Mitigation                               |
| ---------------------------- | ---------- | ---------------------------------------- |
| Token theft                  | Medium     | Use secure storage, rotate on refresh    |
| Refresh loop (invalid token) | Low        | Add exponential backoff, max retry limit |
| Clock skew issues            | Low        | Use 5min grace period for exp validation |

**Open Questions:**

```markdown
## Open Questions

- [ ] What happens to active refresh tokens on password change?
- [ ] How do we handle token refresh during network outage?
- [ ] Should we notify user on refresh token expiration?
```

### Step 4: Validate Completeness

**Required Sections Checklist:**

```javascript
const requiredSections = [
  'Problem Statement',
  'Evidence',
  'Key Hypothesis',
  'Success Metrics',
  'Core Capabilities',
  'Implementation Phases',
  'Decisions Log',
];

// Verify all present
const missingRequiredSections = requiredSections.filter(section => !prdContent.includes(section));

if (missingRequiredSections.length > 0) {
  throw new Error(`Missing required sections: ${missingRequiredSections.join(', ')}`);
}
```

**Quality Checks:**

- [ ] Problem Statement is specific (not vague)
- [ ] Evidence includes data or user feedback
- [ ] Hypothesis is measurable (includes metrics)
- [ ] MoSCoW has at least 1 "Must" and 1 "Won't"
- [ ] Implementation Phases have dependencies mapped
- [ ] Decisions Log explains "why not X" for alternatives

### Step 5: Write PRD

```javascript
// Generate filename
const featureName = 'auth-refresh-tokens'; // from problem statement
const date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
const filename = `${featureName}-prd-${date}.md`;

// Write to specs directory
Write({
  file_path: `.claude/context/artifacts/specs/${filename}`,
  content: prdContent,
});
```

**Output Location:** `.claude/context/artifacts/specs/{feature-name}-prd-{YYYY-MM-DD}.md`

**Provenance Header:**

```markdown
<!-- Agent: pm | Task: #{task-id} | Session: {date} -->

# PRD: {Feature Name}

**Version**: 1.0
**Author**: PM Agent
**Date**: {YYYY-MM-DD}
**Status**: Draft
```

## Integration Points

### PRD → Planner → Developer Flow

**PM creates PRD:**

```markdown
## Implementation Phases

| #   | Phase   | Description       | Status  | Parallel | Depends | Plan Link |
| --- | ------- | ----------------- | ------- | -------- | ------- | --------- |
| 1   | Design  | Auth architecture | pending | No       | -       | -         |
| 2   | Backend | /refresh endpoint | pending | No       | 1       | -         |
```

**Planner reads PRD:**

1. TaskGet({ taskId: 'X' }) → Gets PRD location
2. Read PRD → Understands problem, decisions, phases
3. Selects next pending phase (dependencies met)
4. Creates implementation plan
5. Updates PRD with plan link:

```markdown
| 1 | Design | Auth architecture | completed | No | - | [Plan](.claude/context/plans/impl-phase1-2026-02-09.md) |
```

**Developer reads plan:**

1. Planner's plan links back to PRD
2. Developer has full context: problem, decisions, rationale
3. Implements with understanding of "why"

**Result:**

- Single source of truth: check PRD phases table for status
- Traceability: PRD → Plan → Implementation
- Context preservation: new devs can read PRD to understand feature

## Required Sections Checklist

Before writing PRD, verify:

- [ ] Problem Statement (specific, not vague)
- [ ] Evidence (data, feedback, metrics)
- [ ] Key Hypothesis (measurable outcome)
- [ ] Success Metrics table (Metric | Target | How Measured)
- [ ] Core Capabilities (MoSCoW with Must/Should/Could/Won't)
- [ ] Implementation Phases table (# | Phase | Status | Depends | Plan Link)
- [ ] Decisions Log (Decision | Choice | Alternatives | Rationale)
- [ ] Users & Context (Primary User, Job to Be Done)
- [ ] Technical Approach (Feasibility, dependencies)
- [ ] Risks table (Risk | Likelihood | Mitigation)
- [ ] Open Questions (unresolved items)

## Common Patterns

### Pattern 1: Feature Request → PRD

```
User: "Add dark mode to the app"

PM:
1. Problem: Users report eye strain in low-light conditions
2. Evidence: 200+ support tickets, 4.2 → 3.8 app rating mentions "too bright"
3. Hypothesis: Dark mode will reduce eye strain complaints by 60%
4. MoSCoW:
   - Must: System-default theme detection
   - Must: Manual toggle in settings
   - Should: Per-screen theme override
   - Won't: Automatic sunset-based switching (future)
5. Phases:
   - Phase 1: Design system color tokens
   - Phase 2: Implement theme provider
   - Phase 3: Update all screens
6. Write PRD → specs/dark-mode-prd-2026-02-09.md
```

### Pattern 2: Ambiguous Request → Progressive Disclosure

```
User: "Make the app faster"

PM:
1. [Progressive Disclosure: 8-phase questioning]
   - What specific slowness? (App launch? Navigation? Data load?)
   - Where is evidence? (Metrics showing 5s app launch vs 2s competitor)
   - What outcome? (Launch time < 2s for 95th percentile)
2. [After gathering context]
   - Problem: App launch time 5s vs industry 2s
   - Hypothesis: Lazy loading modules will reduce launch to <2s
3. Write PRD → specs/app-launch-performance-prd-2026-02-09.md
```

### Pattern 3: PRD Update During Implementation

```
Planner completes Phase 1 design:

Update PRD:
| 1 | Design | Auth architecture | completed | No | - | [Plan](.claude/context/plans/impl-phase1-2026-02-09.md) |
| 2 | Backend | /refresh endpoint | in_progress | No | 1 | [Plan](.claude/context/plans/impl-phase2-2026-02-09.md) |

Add decision to log:
| Token algorithm | RS256 | HS256 | RS256 for key rotation support |
```

## Best Practices

**DO:**

- Start with problem, not solution
- Include evidence (data, quotes, metrics)
- Make hypothesis measurable
- Document "Won't" explicitly (prevent scope creep)
- Map phase dependencies clearly
- Record decisions with alternatives considered
- Link phases to implementation plans
- Update PRD as phases complete

**DON'T:**

- Jump to solution without problem statement
- Skip evidence gathering
- Use vague success metrics ("make it better")
- Forget to prioritize (everything is "Must")
- Create phases without dependency mapping
- Skip decision rationale
- Let PRD become stale (update as phases progress)
- Write PRD for trivial changes

## Iron Law

```
NO SOLUTION BEFORE PROBLEM DEFINITION
```

If you don't understand the problem, you can't create a valid PRD. Use Progressive Disclosure for unclear requirements.

## Example: Complete PRD

```markdown
<!-- Agent: pm | Task: #42 | Session: 2026-02-09 -->

# PRD: JWT Refresh Token Implementation

**Version**: 1.0
**Author**: PM Agent
**Date**: 2026-02-09
**Status**: Draft

---

## Problem Statement

Mobile app users experience session expiration (1 hour timeout) during active use, forcing re-authentication and losing workflow context. This creates friction and frustration, particularly for users performing multi-step tasks.

## Evidence

- **Support Tickets**: 200+ complaints about "forced logout" in past 2 months
- **Analytics**: 35% of mobile sessions end with forced re-auth (vs 5% desktop)
- **User Feedback**: App store reviews mention "annoying login prompts" (4.2 → 3.8 rating)
- **Business Impact**: 15% cart abandonment rate correlates with session timeout

## Key Hypothesis

We believe adding JWT refresh tokens will reduce user re-authentication friction for mobile users.
We'll know we're right when session timeout complaints drop by 50% and mobile DAU increases by 10%.

## What We're NOT Building

- Biometric authentication integration (future Phase 2)
- Social login providers (separate initiative)
- Multi-device session management (v2.0)

## Success Metrics

| Metric                     | Target | How Measured            |
| -------------------------- | ------ | ----------------------- |
| Session timeout complaints | -50%   | Support ticket analysis |
| Mobile DAU                 | +10%   | Analytics dashboard     |
| Token refresh success rate | >95%   | Backend logs            |
| Forced re-auth rate        | <10%   | Analytics events        |

## Core Capabilities (MoSCoW)

| Priority | Capability                               | Rationale                                    |
| -------- | ---------------------------------------- | -------------------------------------------- |
| Must     | JWT refresh token endpoint               | Required for MVP - enables session extension |
| Must     | Token rotation on refresh                | Security best practice (OWASP)               |
| Must     | Secure token storage (Keychain/KeyStore) | Prevent token theft                          |
| Should   | Refresh token revocation                 | Allows user logout from all devices          |
| Should   | Token usage analytics                    | Monitoring and debugging                     |
| Could    | Configurable token lifetimes             | Admin flexibility                            |
| Won't    | Biometric auth integration               | Out of scope - future consideration          |
| Won't    | Push notification on token expiry        | Nice to have, defer to v2                    |

## Users & Context

**Primary User**: Mobile app user (iOS/Android) who experiences session expiration during active use (shopping, form filling, browsing)

**Current Behavior**: User logs in → performs task → session expires after 1 hour → forced to re-login → loses form data/cart context

**Trigger**: Session expiration during active use OR app returning from background after >1 hour

**Success State**: User stays logged in seamlessly for up to 30 days (refresh token lifetime), only re-authenticates when truly needed

**Job to Be Done**: When my session expires, I want to continue my work without re-entering credentials, so I can maintain my workflow momentum and complete my tasks.

## Solution Detail

### MVP Scope

**Phase 1**: Design auth architecture with refresh token flow
**Phase 2**: Implement backend /refresh endpoint with token rotation
**Phase 3**: Add refresh logic to mobile SDK (iOS/Android)
**Phase 4**: E2E tests for refresh flows
**Phase 5**: Add refresh metrics to monitoring dashboard

### User Flow

1. User logs in → receives access token (1 hour) + refresh token (30 days)
2. User makes API call → server validates access token
3. Access token expires → next API call returns 401
4. Mobile SDK detects 401 → calls /refresh with refresh token
5. Server validates refresh token → issues new access + refresh tokens
6. SDK retries original API call with new access token
7. User continues seamlessly (no re-login)

### Edge Cases

- Network failure during refresh → retry with exponential backoff
- Refresh token expired → force re-login with "session expired" message
- Refresh token revoked (password change) → force re-login
- Concurrent API calls during refresh → queue and retry after refresh completes

## Technical Approach

**Feasibility**: HIGH

**Dependencies**:

- Existing JWT library (jsonwebtoken) supports refresh
- Mobile SDK has secure storage (Keychain/KeyStore)
- Backend has session management infrastructure

**Integration Points**:

- Mobile SDK (iOS/Android) needs refresh interceptor
- Backend needs /refresh endpoint
- Database needs refresh token storage (w/ expiry)

**Architecture Notes**:

- Access token: 1 hour lifetime, stateless (JWT)
- Refresh token: 30 days lifetime, stateful (stored in DB)
- Token rotation: each refresh invalidates old token, issues new one
- Secure storage: Keychain (iOS), KeyStore (Android)

## Implementation Phases

| #   | Phase       | Description                                      | Status  | Parallel | Depends | Plan Link |
| --- | ----------- | ------------------------------------------------ | ------- | -------- | ------- | --------- |
| 1   | Design      | Auth architecture design with refresh token flow | pending | No       | -       | -         |
| 2   | Backend API | Implement /refresh endpoint with token rotation  | pending | No       | 1       | -         |
| 3   | Mobile SDK  | Add refresh logic to iOS/Android SDK             | pending | No       | 2       | -         |
| 4   | Testing     | E2E tests for refresh flows                      | pending | Yes      | 2,3     | -         |
| 5   | Monitoring  | Add refresh metrics to dashboard                 | pending | Yes      | 2       | -         |

## Decisions Log

| Decision         | Choice                             | Alternatives                           | Rationale                                               |
| ---------------- | ---------------------------------- | -------------------------------------- | ------------------------------------------------------- |
| Token storage    | Secure storage (Keychain/KeyStore) | Local storage, Session storage         | Security requirement - tokens are sensitive credentials |
| Refresh strategy | Automatic on 401                   | Manual user action, Proactive refresh  | Better UX - transparent to user, no extra UI            |
| Token lifetime   | Access: 1hr, Refresh: 30 days      | Access: 5min/90min, Refresh: 7/90 days | Balance security (short access) and UX (long refresh)   |
| Token algorithm  | RS256 (asymmetric)                 | HS256 (symmetric)                      | Enables key rotation, better for distributed systems    |
| Refresh rotation | Always rotate                      | Rotate on suspicious activity          | OWASP best practice, prevents token replay              |
| Storage location | Database                           | Redis, In-memory                       | Need persistent storage, DB already available           |

## Research Summary

**Market Context**:

- Auth0, Firebase, Okta all use refresh token pattern
- Industry standard: short-lived access + long-lived refresh
- OWASP recommends token rotation on every refresh
- JWT RFC 7519 and OAuth 2.0 RFC 6749 define patterns

**Technical Context**:

- Existing backend uses jsonwebtoken library (supports refresh)
- Mobile SDK has secure storage capabilities
- Backend has session management and database for token storage
- Average API latency: 100ms (refresh won't impact UX significantly)

**Feasibility Assessment**: HIGH

- All dependencies available
- No new infrastructure required
- Clear implementation path
- Low risk of scope creep

## Risks

| Risk                           | Likelihood | Mitigation                                                |
| ------------------------------ | ---------- | --------------------------------------------------------- |
| Token theft (XSS/MITM)         | Medium     | Use secure storage, HTTPS only, rotate on refresh         |
| Refresh loop (invalid token)   | Low        | Add exponential backoff, max 3 retries, fallback to login |
| Clock skew issues              | Low        | Use 5min grace period for exp validation                  |
| DB performance (token lookups) | Low        | Index refresh tokens, implement token cleanup job         |
| Concurrent refresh attempts    | Low        | Use mutex/lock during refresh, queue pending requests     |

## Open Questions

- [ ] What happens to active refresh tokens on password change? (Decision: revoke all)
- [ ] How do we handle token refresh during network outage? (Decision: retry with backoff)
- [ ] Should we notify user on refresh token expiration? (Decision: yes, with "session expired" message)
- [ ] Do we need per-device refresh tokens? (Decision: yes, for "logout all devices" feature)

---

_Generated: 2026-02-09_
_Status: Draft_
```

## Related Skills

- `progressive-disclosure` - 8-phase questioning for unclear requirements
- `task-breakdown` - Break PRD phases into implementation tasks
- `research-synthesis` - Gather evidence for problem statement

## Assigned Agents

This skill is invoked by:

- `pm` (Product Manager) - Primary user of this skill

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

Check for:

- Previously created PRDs
- Feature patterns in this codebase
- Common decisions and rationales

**After completing:**

- New PRD pattern → `.claude/context/memory/learnings.md`
- Recurring decision → `.claude/context/memory/decisions.md`
- PRD creation blocker → `.claude/context/memory/issues.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
