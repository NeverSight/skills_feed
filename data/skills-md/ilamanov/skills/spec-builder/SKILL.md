---
name: spec-builder
description: Transform vague product or feature ideas into concrete, detailed specification documents through an interactive interview process. Use when the user wants to flesh out an idea, create a spec, write requirements, plan a product/feature/prototype, or go from "I have this idea..." to a concrete document. Works for software products, physical products, services, or any concept that needs specification.
---

# Spec Builder

Transform vague ideas into concrete, actionable spec documents through structured interviews.

## Workflow

### Phase 1: Gather Initial Context

First, prompt for the idea:

```
What's the idea you'd like to turn into a spec?
Describe it however it exists in your head right now - it can be vague.
```

Then ask background questions to calibrate the interview depth:

```
AskUserQuestion:
1. "What's your background?"
   - Technical (developer/engineer)
   - Semi-technical (PM, designer, technical founder)
   - Non-technical (business, creative, general user)

2. "What's the goal for this spec?"
   - MVP/prototype to test the idea
   - Full product spec for development
   - Pitch document for stakeholders
   - Personal reference to clarify my thinking
```

### Phase 2: Deep Interview

Conduct the interview using AskUserQuestion with **batched questions** (2-4 related questions per batch).

**Rules:**
- Never assume - if something is ambiguous, ask
- Provide sensible default options for every question
- Add "(Recommended)" to the best default option
- Anticipate needs the user hasn't considered
- Adapt question depth based on user's technical level

**Question calibration by user background:**

| Topic | Technical User | Non-Technical User |
|-------|---------------|-------------------|
| Architecture | "REST vs GraphQL vs tRPC?" | Skip - decide yourself |
| Data storage | "SQL vs NoSQL? Which DB?" | "Does it need to remember data between sessions?" |
| UI framework | "React, Vue, or Svelte?" | Skip - decide yourself |
| Hosting | "Serverless, containers, or VMs?" | Skip - decide yourself |
| Auth | "OAuth, magic links, or password?" | "How should users log in?" (plain language options) |
| Scale | "Expected concurrent users?" | "How many people might use this at once?" |

**Interview domains to cover** (adapt based on product type):

For **software products**:
- Core functionality (what does it do?)
- User types and permissions
- Key user flows (step by step)
- Data model (what entities exist?)
- UI/UX preferences (style, layout, interactions)
- Integrations (external services, APIs)
- Edge cases and error handling
- Security and privacy requirements
- Platform (web, mobile, desktop, CLI)

For **physical products**:
- Core functionality
- Materials and form factor
- User interaction (how do you use it?)
- Manufacturing considerations
- Safety requirements
- Packaging and delivery

For **all products**:
- Success criteria (how do we know it works?)
- Constraints (budget, timeline, must-haves)
- Anti-goals (what it explicitly should NOT do)

**Example batched question:**

```
AskUserQuestion (batch):
1. "Who are the main users of this product?"
   - Single user type (just me / general public)
   - Two distinct roles (e.g., admin + regular user)
   - Multiple user types (need to define each)

2. "Do users need accounts?"
   - No accounts needed (Recommended for MVP)
   - Simple accounts (email/password)
   - Social login (Google, GitHub, etc.)
   - Enterprise SSO
```

### Phase 3: Draft Review

After covering core questions (~10-15 batches), present a **draft outline**:

```
Here's the spec outline based on our conversation so far:

## [Product Name] - Spec Outline

**Overview:** [1-2 sentences]

**Core Features:**
1. [Feature A]
2. [Feature B]
...

**User Types:** [list]

**Key Flows:** [list main workflows]

**Technical Approach:** [high-level decisions]

**Open Questions:** [things still unclear]

---

Does this capture your vision? What's missing or wrong?
```

Then use AskUserQuestion to get feedback:

```
1. "How does this outline look?"
   - Looks good, continue with details
   - Missing something important (I'll explain)
   - Some parts are wrong (I'll clarify)
   - Let's pivot direction
```

### Phase 4: Deep Dive

Based on feedback, ask detailed follow-up questions on:
- Unclear areas from the outline
- Edge cases and error states
- Specific UI/UX details
- Technical constraints
- Anything marked as "Open Questions"

Continue until confident all ambiguity is resolved.

### Phase 5: Write Spec

Write the final spec to `spec-<product-name>.md` in the current directory.

**Spec format principles:**
- Detailed enough for an AI coding agent to implement
- Skimmable for human review (use headers, bullets, tables)
- No vague language - every requirement must be concrete
- Include explicit anti-goals and out-of-scope items
- Write as a standalone document - never mention the interview process or reference "our conversation"

**Spec structure** (adapt sections based on product type):

```markdown
# [Product Name] Spec

## Overview
[2-3 sentences: what it is, who it's for, core value prop]

## Goals & Non-Goals

### Goals
- [Concrete goal 1]
- [Concrete goal 2]

### Non-Goals (explicitly out of scope)
- [What this product will NOT do]

## User Types
[Table or list of user types and their permissions/capabilities]

## Core Features

### Feature 1: [Name]
**Purpose:** [Why this feature exists]
**Behavior:**
- [Specific behavior 1]
- [Specific behavior 2]
**UI:** [Description or wireframe reference]

[Repeat for each feature]

## User Flows

### Flow 1: [Name]
1. User does X
2. System responds with Y
3. User sees Z
...

[Repeat for key flows]

## Data Model
[Tables, entities, relationships - for software]
[Components, materials - for physical products]

## Technical Decisions
[Architecture choices, technologies, integrations]
[Skip for non-technical users or physical products]

## Edge Cases & Error Handling
- When X happens, the system should Y
- If Z fails, show error message: "..."

## Open Questions
[Anything that still needs resolution before building]

## Future Considerations
[Ideas mentioned but explicitly deferred]
```

## Key Principles

1. **Be thorough** - Ask many questions. 10-20 batches is normal for a complex product.
2. **Never assume** - If two interpretations are possible, ask which one.
3. **Provide defaults** - Every question should have reasonable options with a recommended choice.
4. **Adapt depth** - Technical users get technical questions; non-technical users get plain language.
5. **Surface unknowns** - Ask about things the user probably hasn't considered yet.
6. **Stay concrete** - The final spec should have zero vague requirements.

