---
name: bmad-development-execution
description: Implements stories with code and tests.
allowed-tools: ["Read", "Write", "Grep", "Bash"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "implement story"
      - "develop this"
      - "let's code"
      - "write the code"
      - "start coding"
    keywords:
      - implement
      - code
      - develop
      - build
      - program
      - coding
      - implementation
  capabilities:
    - code-implementation
    - test-writing
    - debugging
    - code-review
  prerequisites:
    - user-stories
    - architecture-decisions
    - test-strategy-doc
  outputs:
    - source-code
    - test-files
    - implementation-notes
---

# Development Execution Skill

## When to Invoke

**Automatically activate when user:**
- Says "Implement story X", "Start coding", "Develop this"
- Asks "Write the code", "Let's code", "Build [feature]"
- Mentions "implement", "code", "develop"
- Story file ready (Phase 4)
- Uses words like: implement, code, develop, build, program, coding

**Specific trigger phrases:**
- "Implement story [X]"
- "Start coding [feature]"
- "Develop this story"
- "Let's code"
- "Write the implementation"
- "Build [feature]"

**Prerequisites:**
- Story file exists (from bmad-story-planning)
- Architecture patterns defined

**Do NOT invoke when:**
- No story file (use bmad-story-planning first)
- Planning needed (use bmad-product-planning first)
- Architecture not defined (use bmad-architecture-design first)

## Mission
Implement approved stories end-to-end, maintaining transparency, testing discipline, and traceability back to requirements and architecture decisions.

## Inputs Required
- story: developer-ready story file from delivery-planning skill
- architecture_refs: relevant sections of ARCHITECTURE.md or component notes
- ux_guidance: UX specs or validations tied to the story
- quality_plan: scenarios or gates supplied by quality-assurance skill

## Outputs
- Code diffs and test results captured in the working repository
- Updated story file (Dev Agent Record, status transitions, learnings)
- **implementation-notes.md** - Development summary (generated from `assets/implementation-notes-template.md.template`)
- Summary of changes, tests, and outstanding risks for stakeholders

**Template location:** `.claude/skills/bmad-development-execution/assets/implementation-notes-template.md.template`

## Process
1. Confirm prerequisites via `CHECKLIST.md` and restate story scope.
2. Plan implementation steps, identifying affected files and tests.
3. Apply small, reviewable code changes with explanations and references.
4. Execute required test suites and capture command output verbatim.
5. Update story documentation, including Dev Agent Record and status.
6. Summarize work, highlight follow-ups, and notify orchestrator for next steps.

## Quality Gates
All items in `CHECKLIST.md` must pass before code is considered complete. Never mark a story done without full testing evidence.

## Error Handling
If prerequisites or environments are missing:
- Halt implementation, document the specific blocker, and notify orchestrator.
- Provide recommended remediation steps (e.g., refresh artifacts, fix failing baseline tests).
- Avoid speculative changes; keep diffs scoped to the approved story.
