---
name: generate-prd
description: Generates Product Requirements Documents for new features through guided discovery. Use when starting a new feature, creating specifications, or when user needs help defining requirements with clarifying questions.
model: claude-opus-4-5
context: fork
---

<objective>
Generate detailed, actionable Product Requirements Documents (PRDs) for new features. Guide users through clarifying questions, then produce specifications suitable for implementation by developers or AI agents.

**Important**: This skill creates PRDs only—it does NOT begin implementation.
</objective>

<quick_start>
1. Ask 3-5 clarifying questions with lettered options (A, B, C, D)
2. Generate structured PRD based on answers
3. Save to `tasks/prd-[feature-name].md`
</quick_start>

<process>

<step name="1_clarifying_questions">
Ask 3-5 essential questions using AskUserQuestion tool. Cover:

- **Problem/Goal**: What problem does this solve? Who benefits?
- **Core Functionality**: What are the must-have features?
- **Scope/Boundaries**: What is explicitly NOT included?
- **Success Criteria**: How will we know this worked?

Each question should have 3-4 concrete options (A, B, C, D format) plus "Other" for custom input.
</step>

<step name="2_generate_prd">
Create the PRD document with these sections:

1. **Introduction/Overview** – Brief feature description and problem statement
2. **Goals** – Specific, measurable objectives
3. **User Stories** – Each with title, description, and verifiable acceptance criteria
4. **Functional Requirements** – Numbered explicitly (FR-1, FR-2, etc.)
5. **Non-Goals** – Clear scope boundaries
6. **Design Considerations** – UI/UX requirements (if applicable)
7. **Technical Considerations** – Constraints and dependencies (if applicable)
8. **Success Metrics** – Measurable outcomes
9. **Open Questions** – Remaining clarifications needed
</step>

<step name="3_save_document">
Save the PRD to: `tasks/prd-[feature-name].md`

Use kebab-case for feature name (e.g., `prd-user-authentication.md`).
</step>

</process>

<principles>

<principle name="explicitness">
Avoid jargon or explain it. Provide concrete examples. A junior developer should understand every requirement without additional context.
</principle>

<principle name="verifiability">
Acceptance criteria must be testable and specific.

**Good**: "Login button redirects to /dashboard on success"
**Bad**: "Login works correctly"
</principle>

<principle name="ui_stories">
Every UI-focused user story MUST include this acceptance criterion:
`"Verify in browser using dev-browser skill"`
</principle>

<principle name="atomic_stories">
Each user story should be small enough to implement in one session. If a story feels too large, break it into smaller stories.
</principle>

</principles>

<prd_template>
```markdown
# PRD: {{Feature Name}}

## 1. Introduction

{{Brief description of the feature and the problem it solves}}

## 2. Goals

- {{Goal 1: Specific, measurable objective}}
- {{Goal 2: Specific, measurable objective}}

## 3. User Stories

### US-1: {{Story Title}}
**As a** {{user type}}, **I want** {{feature}} **so that** {{benefit}}.

**Acceptance Criteria:**
- {{Specific, testable criterion}}
- {{Specific, testable criterion}}
- Verify in browser using dev-browser skill (for UI stories)

### US-2: {{Story Title}}
...

## 4. Functional Requirements

- **FR-1**: {{Explicit requirement}}
- **FR-2**: {{Explicit requirement}}
- **FR-3**: {{Explicit requirement}}

## 5. Non-Goals

- {{What this feature explicitly does NOT do}}
- {{Scope boundary}}

## 6. Design Considerations

{{UI/UX requirements, wireframe references, design patterns}}

## 7. Technical Considerations

{{Constraints, dependencies, integration points, performance requirements}}

## 8. Success Metrics

- {{Measurable outcome 1}}
- {{Measurable outcome 2}}

## 9. Open Questions

- [ ] {{Unresolved question needing clarification}}
```
</prd_template>

<examples>

<example name="good_acceptance_criteria">
**Good:**
- "Search results display within 2 seconds"
- "Error message shows 'Invalid email format' for malformed input"
- "Clicking 'Save' disables button and shows spinner until complete"

**Bad:**
- "Search is fast"
- "Shows appropriate error messages"
- "Good UX on save"
</example>

<example name="good_functional_requirements">
- **FR-1**: System shall validate email format using RFC 5322 pattern
- **FR-2**: Password must be minimum 8 characters with at least one number
- **FR-3**: Session expires after 30 minutes of inactivity
</example>

</examples>

<success_criteria>
PRD is complete when:

- [ ] 3-5 clarifying questions were asked and answered
- [ ] All 9 PRD sections are filled with concrete content
- [ ] User stories have verifiable acceptance criteria
- [ ] UI stories include browser verification criterion
- [ ] Functional requirements are numbered (FR-1, FR-2, etc.)
- [ ] Non-goals clearly define scope boundaries
- [ ] Document saved to `tasks/prd-[feature-name].md`
- [ ] No implementation has begun (PRD only)
</success_criteria>
