---
name: plan-interview
description: |
  Ensures alignment between user and Claude during feature/spec planning through a structured interview process.

  Use this skill when the user invokes /plan-interview before implementing a new feature, refactoring, or any non-trivial implementation task. The skill runs an upfront interview to gather requirements across technical constraints, scope boundaries, risk tolerance, and success criteria before any codebase exploration.

  Do NOT use this skill for: pure research/exploration tasks, simple bug fixes, or when the user just wants standard planning without the interview process.
---

# Plan Interview Skill

## Purpose

Run a structured requirements interview before planning implementation. This ensures alignment between you and the user by gathering explicit requirements rather than making assumptions.

## When Invoked

User calls `/plan-interview <task description>`.

**Skip this skill** if the task is purely research/exploration (not implementation).

## Interview Process

### Phase 1: Upfront Interview (Before Exploration)

Interview the user using `AskUserQuestion` in **thematic batches of 2-3 questions** when the provider supports it. For providers like GitHub Copilot without an AskUser tool, ask the same questions directly in chat and pause for responses before continuing.

#### Required Question Domains

Cover ALL four domains before proceeding:

1. **Technical Constraints**
   - Performance requirements
   - Compatibility needs
   - Existing patterns to follow
   - Architecture understanding (if codebase is unfamiliar)

2. **Scope Boundaries**
   - What's explicitly OUT of scope
   - MVP vs full vision
   - Dependencies on other work

3. **Risk Tolerance**
   - Acceptable tradeoffs (speed vs quality)
   - Tech debt tolerance
   - Breaking change acceptance

4. **Success Criteria**
   - How will we know it's done?
   - What defines "working correctly"?
   - Testing/validation requirements

#### Question Generation

- Generate questions **dynamically** based on the task - no fixed template
- Group related questions into thematic batches
- **2-3 questions per batch** (do not exceed)
- Continue until you have **actionable specificity** (can describe concrete implementation steps)

#### Handling Edge Cases

| Scenario | Action |
|----------|--------|
| Contradictory requirements | Make a recommendation with rationale, ask for confirmation |
| User pivots requirements | Restart interview fresh with new direction |
| Interrupted session | Ask user: continue where we left off or restart? |

#### Anti-Patterns to Avoid

- Do NOT ask variations of the same question
- Do NOT make major assumptions without asking
- Do NOT over-engineer plans for simple tasks

### Phase 2: Codebase Exploration

After interview completes, explore the codebase to understand:
- Existing patterns relevant to the task
- Files that will be affected
- Integration points
- Potential risks

### Phase 3: Plan Generation

Write plan to `docs/plans/plan-NNN-<slug>.md` where NNN is sequential.

#### Required Elements

Every plan MUST include:

```markdown
## Success Criteria
[Clear definition of done from interview]

## Risk Assessment
[What could go wrong + mitigations]

## Affected Files/Areas
[Which parts of codebase will be touched]

## Open Questions
[Uncertainties to resolve during implementation]
- [ ] Question 1 - [Blocks implementation / Can proceed]
- [ ] Question 2 - [Blocks implementation / Can proceed]

## Implementation Checklist
- [ ] Step 1
- [ ] Step 2
...
```

#### Optional Elements

Include when relevant:

- **Rejected Alternatives**: Only for major architectural decisions
- **Decision Tree**: Only when multiple valid approaches exist
- **Visual Diagrams**: ASCII or Mermaid when helpful for understanding

#### Constraints

- **No time estimates** - describe what needs doing, not how long
- **No length limits** - plan should match task complexity
- Freeform structure beyond required elements

### Phase 4: Post-Approval

When user approves the plan:

1. **Auto-start implementation** immediately (no "proceed" confirmation needed)
2. Populate `TodoWrite` with checklist items
3. At **natural breakpoints** (significant decisions), compare progress to plan

## Fast Mode

If user wants quick planning, use **draft + refine**:

1. Perform task-focused codebase search
2. Generate draft plan
3. Run abbreviated interview to refine

## Resume Support

If a partial plan exists in `docs/plans/`:

```
AskUserQuestion: "I found an existing partial plan. Would you like to:"
- "Continue from where we left off"
- "Start fresh with a new plan"
```

## Example

```
User: /plan-interview Add OAuth authentication to the API

Claude: I'll help you plan the OAuth authentication feature. Let me gather
        requirements first.

[AskUserQuestion - Scope batch]
1. Which OAuth providers need to be supported (Google, GitHub, etc.)?
2. Is this replacing existing auth or adding alongside it?

[Copilot guidance: ask the same two questions in chat and wait for responses]

User: Google and GitHub. Adding alongside existing JWT auth.

[AskUserQuestion - Technical batch]
1. Should OAuth tokens be stored in the existing session table or separately?
2. Any specific callback URL constraints from your hosting setup?

User: Separate table. We're on Vercel so callback URLs need to be configured per environment.

[AskUserQuestion - Risk/Success batch]
1. What's the acceptable degradation if an OAuth provider is down?
2. How should we handle users who already exist with the same email?

User: Fall back to standard login. Link accounts by email if user confirms.

Claude: [Explores codebase for auth patterns, session handling, database schema]

Claude: [Writes docs/plans/plan-003-oauth-authentication.md]

        Plan created. The main decision point is whether to use Passport.js
        or implement OAuth flows directly - I've documented both approaches
        with tradeoffs. Ready to review?

User: Looks good, go with Passport.js

Claude: [Auto-starts implementation with TodoWrite tracking]
```
