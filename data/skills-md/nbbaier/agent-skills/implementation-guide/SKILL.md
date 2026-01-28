---
name: implementation-guide
description: Generate comprehensive implementation guides for coding tasks instead of writing code directly. Use when the user requests detailed implementation documentation, step-by-step development guides, or when they want to implement features themselves using tools like Cursor. Creates exhaustive guides with background context, architecture decisions, milestones with verification points, and rationale for a "build-it-yourself" workflow.
---

# Implementation Guide Generator

This skill generates detailed implementation guides for coding tasks, designed to help developers implement features themselves rather than receiving completed code. The guides provide deep context, teach underlying concepts, explain architectural decisions, and break work into verifiable milestones.

## When to Use This Skill

Use this skill when:

-  User asks for an "implementation guide" or "guide to implement X"
-  User wants to implement something themselves using Cursor, Windsurf, or similar tools
-  User explicitly mentions wanting detailed documentation instead of code
-  User asks for a "tutorial" or "step-by-step guide" for implementing a feature
-  Context suggests the user wants to stay connected to the implementation process

## Core Principles

### Educational Depth

Implementation guides should teach, not just instruct. Explain:

-  **Why** decisions are made, not just what to do
-  Background context about technologies and patterns used
-  Tradeoffs between different approaches
-  How the feature fits into the larger system

### Verifiable Milestones

Every milestone must include:

-  Clear goal statement
-  Specific changes required
-  Detailed implementation steps
-  Concrete verification method (tests, visible behavior, commands to run)
-  Common pitfalls to avoid

### Assume Mid-Level Developer

Default to mid-level developer experience unless specified otherwise:

-  Explain concepts that might not be familiar
-  Don't over-explain basics
-  Include enough detail to implement successfully
-  Provide links for deeper learning

### Customizable Experience Level

The user can specify experience level:

-  **Junior**: More detailed explanations, simpler terminology, more examples
-  **Mid-level** (default): Balanced detail, assumes familiarity with common patterns
-  **Senior**: Higher-level guidance, focus on architecture and tradeoffs

## Guide Structure

Implementation guides should follow this overall structure, though sections can be adapted based on the specific task:

### Opening Sections

1. **Title and Introduction** - What you're building and why it matters
2. **What You're Building** - Concrete description with bullet points of key features
3. **Why These Features Matter** - Explain the reasoning behind feature choices
4. **Tech Stack** (if applicable) - Each technology with "What it is", "Why we're using it", "The tradeoff"
5. **Time Estimate** - Realistic time breakdown (be specific: "6-8 hours for core features")
6. **Cost** (if applicable) - Monthly costs broken down by service
7. **Prerequisites** - What needs to be installed/configured with verification commands

### Core Implementation Sections

8. **Milestone 1, 2, 3...** - Each milestone with:
   -  Goal statement
   -  "Why start here?" or rationale
   -  Numbered steps (Step X.1, X.2, etc.)
   -  Embedded checkpoints throughout
   -  "Milestone X Complete!" summary

### Closing Sections

9. **Summary** - Table or list of what was built with why it matters
10. **Architecture Overview** (if helpful) - ASCII diagram or high-level explanation
11. **Key Learnings** - 3-5 important takeaways from the implementation
12. **What's Next?** - Optional enhancements with time estimates
13. **Useful Commands Reference** (if applicable) - Quick reference of common commands

See `references/template.md` for a template structure and `references/example-rate-limiting.md` for a complete example following these patterns.

## Writing Implementation Guides

### Start with Context

Before diving into implementation:

1. Ask clarifying questions about:
   -  The specific feature or task to implement
   -  Existing codebase context (tech stack, architecture patterns)
   -  Constraints or requirements
   -  Developer experience level (if not specified, use mid-level)
2. Once you understand the task, generate the guide directly

### Writing Style

**Be conversational and engaging:**

-  Write like you're pair programming with someone, not writing documentation
-  Use questions to engage: "Notice how fast that was?", "What just happened?"
-  Include reactions and observations: "This is where it gets interesting..."
-  Use "we" to create partnership: "We're building..." not "You will build..."

**Structure within milestones:**

-  Number steps within each milestone: Step 1.1, Step 1.2, etc.
-  After each command or code block, explain "What just happened?"
-  Embed checkpoints immediately after verification steps
-  Use bold callouts: **Checkpoint**, **Why**, **The tradeoff**, **What it is**

**Make tradeoffs explicit:**

-  Every significant decision should include "**The tradeoff:**" section
-  Discuss alternatives inline where decisions are made, not in separate section
-  Be honest about downsides: "This is newer, so you might hit edge cases"

**Write verificiation steps clearly:**

-  Use "**Checkpoint:**" before verification steps
-  Use checkmarks (✓) for expected results in lists
-  Include specific expected results: "You should see..." not "Verify it works"
-  Give concrete metrics when possible: "Should complete in < 500ms"
-  List multiple verification methods (visual, command output, tests)
-  Include troubleshooting for common issues right after checkpoints

**Code explanations:**

-  Add extensive inline comments explaining "why" within code blocks
-  After code blocks, include "Understanding the implementation:" or "What's happening here?" sections
-  Use rhetorical questions: "Why IndexedDB?" followed by the answer
-  Add "Note" paragraphs after code for important observations
-  Include JSDoc-style comments for functions and interfaces when showing complete implementations

**Visual elements:**

-  Use ASCII diagrams for architecture (box drawing characters work well)
-  Use ✓ checkmarks in checkpoint lists
-  Consider using emojis sparingly for visual markers (✓ ⚠️ etc.)

### Milestone Design

**Structure each milestone as:**

1. **Goal statement** - One sentence, what this achieves
2. **Why start here?** (or "Why this matters:") - Rationale for doing this now
3. **Numbered steps** (Step X.1, X.2, etc.) with:
   -  Command or code with extensive inline comments
   -  "What just happened?" or "Understanding X:" explanation
   -  "Why X?" rhetorical questions with answers
   -  "Note" observations about important details
   -  Embedded checkpoints with ✓ marks for expected results
   -  Troubleshooting tips if things go wrong
4. **Milestone complete marker** - Clear completion statement with bullet list of achievements

Each milestone should:

-  Be completable in 15-60 minutes
-  Build on previous milestones naturally
-  Have multiple verification points throughout
-  Feel like meaningful progress
-  Include time estimates when helpful

Break down complex features into 3-7 milestones. Too few milestones and the steps are overwhelming; too many and it feels fragmented.

### Code Snippets

Include code snippets that:

-  Show the actual implementation, not pseudocode
-  Include extensive inline comments explaining "why", not just "what"
-  Are complete enough to be copy-pastable with minor adjustments
-  Follow the project's conventions (infer from context)
-  Have accompanying "Understanding X:" or "What's happening here?" sections

Pattern for code snippets:

```
[Code block with inline comments]

**Understanding the implementation:**
- Bullet point explanation of key concepts
- Bullet point about important details
- Bullet point about edge cases

[Optional: Note paragraph about a specific detail]
```

Don't write complete implementations—show the key parts and explain how to fill in the rest.

### Upfront Information

Include near the beginning of guides:

-  **Time estimate** - How long each phase or the total will take
-  **Cost estimate** - Monthly costs for any services (be specific: "$2-3/month")
-  **Prerequisites** - What needs to be installed/configured before starting
-  **What you're building** - Concrete description of the end result

### Technical Decisions

When explaining technology choices, use this pattern:

```
**What it is:** Brief explanation of the technology
**Why we're using it:** Specific benefits relevant to this project
**The tradeoff:** Honest discussion of downsides or alternatives
```

This pattern makes guides scannable while ensuring every decision is justified.

## Handling Different Task Types

### Backend Features

Focus on:

-  Database schema changes
-  API design and endpoints
-  Business logic architecture
-  Integration points with existing systems
-  Migration strategies

### Frontend Components

Focus on:

-  Component architecture and composition
-  State management approach
-  Accessibility requirements
-  Responsive design considerations
-  Performance (rendering, bundle size)

### Refactoring Tasks

Focus on:

-  Current state analysis
-  Incremental migration path
-  Backward compatibility
-  Testing strategy to prevent regressions
-  Rollback approach

### Infrastructure/DevOps

Focus on:

-  Configuration management
-  Deployment pipeline changes
-  Monitoring and observability
-  Disaster recovery
-  Cost implications

### Performance Optimization

Focus on:

-  Profiling and measurement
-  Specific bottlenecks
-  Optimization strategies with benchmarks
-  Tradeoffs (complexity vs speed)
-  How to validate improvements

## Reference Files

-  **template.md**: Complete template structure for implementation guides
-  **example-rate-limiting.md**: Full example showing all sections in action

Refer to these files when creating guides to ensure consistency and completeness.

## Examples

### User Request: "I need to add authentication to my API"

Generate a guide covering:

-  Authentication strategies (JWT vs sessions vs OAuth)
-  Chosen approach with rationale
-  Milestones: Setup auth library → Implement login endpoint → Add middleware → Secure existing routes → Add refresh tokens
-  Security considerations
-  Testing strategy
-  Migration path for existing users

### User Request: "Build a real-time notification system"

Generate a guide covering:

-  Real-time technology options (WebSockets, SSE, polling)
-  Architecture (pub/sub, message queue, direct connection)
-  Milestones: WebSocket server setup → Connection management → Event publishing → Client integration → Persistence → Scaling
-  Performance and connection handling
-  Fallback strategies

### User Request: "Refactor our monolith to use microservices"

Generate a guide covering:

-  Current monolith analysis
-  Service boundary identification
-  Incremental extraction strategy
-  Milestones: Identify first service → Extract with dual-write → Data migration → Switch traffic → Remove from monolith
-  Inter-service communication
-  Transaction handling
-  Monitoring and debugging distributed system
