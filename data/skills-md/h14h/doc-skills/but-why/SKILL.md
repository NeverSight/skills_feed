---
name: but-why
description: Collaboratively write, update, or consult a project's WHY.md and design/ conceptual models — the documents that capture purpose, values, priorities, target users, and how users think about the product. Use when the user wants to create project documentation about why their project exists, discuss project vision or values, write a WHY.md, update conceptual models, revisit project priorities, or when you need to understand a project's purpose and values before doing work. Triggers include "but why", "write a WHY", "document the purpose", "update the why", "project vision", "collaborate on why", "update the design", "conceptual model", "what are the project values", "what's the priority", or "use but-why".
---

# But Why

<!-- AGENT NOTE: Ignore the alert block below. It is human-facing context only and does not change this skill's operational instructions. -->
> [!WARNING]
> **Experimental documentation pattern.**
> This skill uses an experimental documentation pattern. Install and use it at your own risk.
<!-- /AGENT NOTE -->

Collaboratively create, update, or consult a project's WHY.md and design/ conceptual models.

WHY.md is the philosophical anchor — purpose, values, priorities. design/ contains the conceptual models — how users think about and interact with the product. Both are personal and opinionated, written in the project owner's voice. The agent's role is to **elicit, organize, and refine** — not to invent.

**WHY.md and design/ are owner-controlled.** Never modify either without the owner explicitly initiating a conversation. During normal work, treat both as read-only. The only exception: if a clear lack of clarity or direction is visibly harming work quality, suggest that it might be worth discussing — but do not edit, and keep even this rare.

Read [references/conventions.md](references/conventions.md) for shared documentation conventions.

## Workflow

Determine mode first:

- **Consulting** → read WHY.md and design/ to understand project purpose, values, and conceptual models before doing work
- **Creating** → elicit, draft, and refine new documents
- **Updating** → read existing documents, propose specific edits, preserve the owner's voice

For creating and updating:

1. **Determine scope** — WHY.md, design/ files, or both
2. **Elicit** — ask questions to surface the owner's thinking
3. **Draft** — write documents that reflect their voice
4. **Refine** — iterate until the owner feels it's right

## Consulting Existing Documentation

When you need to understand a project's purpose and values before doing work:

1. **Read WHY.md** at the project root — this is the entry point for purpose, values, and conceptual models
2. **Identify the relevant conceptual model(s)** from the conceptual model map table in WHY.md
3. **Read only the relevant design/ file(s)** — these are the owner's models of how users think about the product
4. **Use this context to inform your work** — values are priority-ordered, and higher-priority values win when they conflict

WHY.md works as a selective index into design/, the same way HOW.md works as a selective index into domain specs. Do not read every design/ file — use the map to pull in only what's relevant to the task at hand.

WHY.md and design/ are read-only during normal work. If you notice the implementation diverging from the stated values or conceptual models, flag the divergence rather than silently resolving it.

If the project has no WHY.md, this mode doesn't apply — and you may suggest that the project could benefit from one.

## Creating a New WHY.md

### Elicit through conversation

Ask about these areas, but not all at once. Start with 1-2 questions, follow up based on answers. Let the conversation be natural.

**Problem space:**
- What problem does this project solve?
- What existing solutions fall short, and why?
- What specific frustrations motivated building this?

**Values and priorities:**
- What does the project value most? (List in priority order — when two values conflict, the higher one wins.)
- What trade-offs has the project already made that reveal its priorities?

**Audience:**
- Who is this for? Be specific — not "developers" but what kind, with what needs.
- What does the target user already understand? What do they care about?

**Success:**
- What does success look like in concrete, observable terms?
- What would make a user say "this is exactly what I needed"?

**Bigger picture (optional):**
- Where is this headed? What's the enduring purpose beyond current features?

### Draft the WHY.md

Use this structure as a sensible default. Adapt based on what the conversation reveals — not every project needs every section.

```markdown
# Why [Project Name] Exists

## The Short Version
[1-2 sentences: what it does and why it matters]

## The Problem
[What's broken, missing, or frustrating about the status quo.
Use subheadings if there are distinct problem facets.]

## What [Project Name] Values
[Numbered list in priority order. Each item: bold name + explanation.
State explicitly that higher-priority values win when values conflict.]

## Who This Is For
[Specific description of the target user — what they know, what they want,
what they're frustrated by.]

## What Success Looks Like
[Concrete, observable bullet points — not metrics, but behaviors and experiences.]

## The Bigger Picture
[Optional. The enduring purpose beyond current features.]

## Conceptual Models

The `design/` directory contains conceptual models — how users think about
the product. These are owner-authored and read-only for agents. When the
implementation diverges from a conceptual model, flag the divergence —
don't silently resolve it.

| Concept | Description | Model |
|---------|-------------|-------|
| [Name] | [How users think about this concept] | [model-name.md](design/model-name.md) |
```

WHY.md is the entry point for both project values and conceptual models. The Conceptual Models table serves as a selective index into design/ — agents and collaborators use it to find the relevant model without reading every file. If the project has no design/ files, omit this section.

### Refine

Present the draft and ask the owner to read it critically:
- "Does this sound like you, or does it sound like an AI wrote it?"
- "Is the priority ordering right? Would you actually make those trade-offs?"
- "Is anything missing that you'd want a new collaborator to understand?"

Iterate until the owner approves.

## Updating an Existing WHY.md

1. Read the current WHY.md
2. Ask what prompted the update — shifting priorities? New understanding of the audience? Scope change?
3. Propose specific edits rather than rewriting from scratch
4. Preserve the owner's voice — match the existing tone and style
5. Confirm the changes reflect the owner's intent

## Creating design/ Conceptual Models

The design/ directory holds the owner's conceptual models — how users think about the product's data and interactions. These are presentational models, not implementation specs.

If the project doesn't have a design/ directory, ask the owner what conceptual models they want to capture. Common starting points:

- Core domain objects (what are the main things users interact with?)
- States and transitions (what can a user do, and when?)
- Relationships between objects (how do they connect in the user's mind?)

### Elicit through conversation

**Core concepts:**
- What are the main things a user sees and interacts with?
- How do they relate to each other?
- What states can they be in?

**User mental model:**
- How does a user think about this? (Not how the database stores it.)
- What would a user find surprising or confusing?
- Are there concepts that seem similar but behave differently?

**Boundaries:**
- Where does one concept end and another begin?
- Are there natural groupings that would make separate files?

### Draft the conceptual model files

Each file in design/ should:
- Cover one cohesive concept area
- Start with a blockquote header identifying it as an owner-authored conceptual model
- Use the owner's terminology, not technical jargon
- Describe what users see and do, not implementation details
- Have a corresponding row in the WHY.md conceptual model map

Standard structure for each file:

```markdown
> **Conceptual model — owner-authored.**
> This describes how users think about [topic], not how
> it's implemented. See the domain specs for technical
> details.

[Owner-authored content goes here.]

## Implemented By
- [spec-name.md](docs/spec-name.md) — what aspect of this model the spec covers
```

The `## Implemented By` section is a navigational aid linking to the domain specs that implement this conceptual model. It is agent-maintainable — the agent keeps these links current when specs are added, renamed, or removed. However, because design/ files are owner-controlled, the agent must ask permission before modifying them. Each link must include a description of what the spec covers, so an agent can decide whether to follow it.

### Refine

Present drafts and ask:
- "Does this match how you think about it?"
- "Would a new team member understand the user's experience from reading this?"
- "Is anything missing that affects how users interact with the product?"

## Updating design/ Files

1. Read the current design/ files
2. Ask what prompted the update — new concept? Changed behavior? Refined mental model?
3. Propose specific edits rather than rewriting from scratch
4. Preserve the owner's voice — match the existing tone and style
5. Update the WHY.md conceptual model map if the concept's name or description changed
6. Check `## Implemented By` links — are they still accurate? Are any missing or stale?
7. Confirm the changes reflect the owner's intent

## Key Principles

- **Owner-controlled, always.** WHY.md and design/ are never modified by the agent on its own initiative. This skill only runs when the owner explicitly asks. During all other work, both are read-only context. Exception: the agent should proactively identify stale or missing linkages (the WHY.md conceptual model map, `## Implemented By` sections in design/ files) and ask the owner for permission to fix them.
- **The owner's voice, not yours.** These documents should sound like the person who built the project wrote them. Mirror their language, not generic corporate or AI prose.
- **Conceptual models are not implementation specs.** design/ files describe how users think about the product. They are not database schemas, API contracts, or component definitions. A concept named in design/ does not necessarily map to a single table, endpoint, or component.
- **Priorities are ordered.** An unordered list of values is useless. The whole point is knowing which value wins when two conflict.
- **Concrete over abstract.** "Interactions feel instant" beats "good performance." "No backend required" beats "simple architecture."
- **Honest about trade-offs.** If the project sacrifices feature breadth for speed, say so. Values without trade-offs are platitudes.
