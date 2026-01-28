---
name: ralphie-spec
description: Generate project specifications in V2 format through structured user interviews. Requires user presence.
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
license: MIT
metadata:
  author: ralphie
  version: "3.0.0"
  argument-hint: <project-description>
  install-hint: npx add-skill skylarbarrera/ralphie --skill ralphie-spec
---

# Ralphie Spec Generation (V2 Format)

Generate comprehensive specs using the V2 format with task IDs, status tracking, and size-based budgeting through structured interviews with the user.

## When to Use

- User is present and can answer questions
- Complex projects needing clarification
- When requirements need discussion

## 80/20 Integration

This skill works with Ralphie's compound engineering features:

- **Research Phase (optional):** If Ralphie ran `ralphie spec` with research, findings are in `.ralphie/research-context.md`
- **Analysis Phase (optional):** After spec generation, Ralphie may analyze for gaps (saved to `.ralphie/analysis.md`)
- **Interactive Review:** Since user is present, gaps are discussed and resolved in real-time

The skill checks for these files and incorporates findings, but doesn't trigger research/analysis itself (that's the CLI's job).

## Output Location

Write specs to `.ralphie/specs/active/{name}.md`:

- Generate a kebab-case filename from the description
- Example: "user authentication" → `.ralphie/specs/active/user-authentication.md`
- Only one spec allowed in `.ralphie/specs/active/` at a time

## Workflow

```
Check Research → Interview User → Explore Codebase → Draft Tasks → Size Review → Write V2 Spec → Check Analysis → Review Gaps → Present for Approval
```

**80/20 Philosophy:** Research and analysis are part of the 80% (planning). Incorporate their findings to make specs thorough.

---

## Step 0: Check for Research Context (Optional)

Before interviewing, check if Ralphie ran research:

```bash
cat .ralphie/research-context.md 2>/dev/null
```

If the file exists:
- Read it to understand codebase patterns, conventions, and framework best practices
- Use findings to inform your interview questions
- Reference research in Context section of final spec

If it doesn't exist, skip this step—interview will gather requirements directly from user.

---

## Step 1: Interview User

Use AskUserQuestion to gather requirements in batches of 2-4 questions.

### Batch 1: Project Foundation

```
AskUserQuestion({
  questions: [
    {
      question: "What type of project is this?",
      header: "Type",
      multiSelect: false,
      options: [
        { label: "CLI tool", description: "Command-line application" },
        { label: "Web API", description: "REST/GraphQL backend" },
        { label: "Library", description: "Reusable package" },
        { label: "Full-stack", description: "Frontend + backend" }
      ]
    },
    {
      question: "What language/framework?",
      header: "Stack",
      multiSelect: false,
      options: [
        { label: "TypeScript/Node.js (Recommended)", description: "Modern JS with types" },
        { label: "Python", description: "Great for data, ML, scripting" },
        { label: "Go", description: "Fast, good for systems" },
        { label: "Rust", description: "Memory-safe systems" }
      ]
    }
  ]
})
```

### Batch 2: Requirements

```
AskUserQuestion({
  questions: [
    {
      question: "What is the primary use case?",
      header: "Use Case",
      multiSelect: false,
      options: [
        { label: "Internal tool", description: "Used by your team" },
        { label: "Public product", description: "External users" },
        { label: "Library/SDK", description: "For other developers" },
        { label: "Learning/experiment", description: "Personal project" }
      ]
    },
    {
      question: "What's the testing expectation?",
      header: "Testing",
      multiSelect: false,
      options: [
        { label: "Unit tests only (Recommended)", description: "Test individual functions" },
        { label: "Unit + Integration", description: "Test components together" },
        { label: "Full coverage", description: "Unit + Integration + E2E" },
        { label: "Minimal/none", description: "Prototype or spike" }
      ]
    }
  ]
})
```

### Batch 3: Scope

Follow up based on previous answers:
- "What external services or APIs does this integrate with?"
- "Are there auth requirements? (none / basic / OAuth)"
- "What's the priority: MVP or full feature set?"

### Interview Tips

- If answers are vague, ask for specific examples
- Clarify: "Is X a must-have or nice-to-have?"
- Don't proceed until core requirements are clear

---

## Step 2: Explore Codebase

If this is a brownfield project (existing code), explore it:

### 2.1 Check for Existing Code

```bash
ls package.json pyproject.toml go.mod Cargo.toml 2>/dev/null
```

### 2.2 Understand Structure

```
Glob("src/**/*")
Glob("lib/**/*")
```

### 2.3 Read Context

- `README.md` - Project description
- `CLAUDE.md` - AI instructions
- `specs/lessons.md` - Past learnings to apply
- Main entry points

### 2.4 Detect Patterns

```
Grep("export function", path="src/")
Grep("(describe|test)\\(", path="tests/")
```

---

## Step 3: Draft Tasks with Sizes

Before writing the spec, draft tasks and estimate sizes.

### Size Guidelines

| Size | Points | Criteria | Examples |
|------|--------|----------|----------|
| S | 1 | Single file, simple logic, < 50 lines | Config setup, type definition, simple util |
| M | 2 | Multiple files, moderate logic, 50-200 lines | CRUD endpoint, feature module |
| L | 4 | Complex feature, architectural changes, 200+ lines | Auth system, major refactor |

### Draft Format

Create a mental or written draft:

```
T001: Setup project structure [S]
T002: Implement core data model [M]
T003: Add authentication [L]
T004: Create API endpoints [M]
T005: Add tests [M]
```

---

## Step 4: Size Review with User

Present the task breakdown and ask for size confirmation:

```
AskUserQuestion({
  questions: [
    {
      question: "Here's my task breakdown with size estimates. Do these sizes seem accurate?",
      header: "Sizes",
      multiSelect: false,
      options: [
        { label: "Looks good", description: "Proceed with these estimates" },
        { label: "Some too small", description: "I'll bump up specific tasks" },
        { label: "Some too large", description: "Let's split into smaller tasks" },
        { label: "Discuss changes", description: "I have specific feedback" }
      ]
    }
  ]
})
```

Show the summary:

```markdown
## Proposed Tasks

| ID | Task | Size | Points |
|----|------|------|--------|
| T001 | Setup project structure | S | 1 |
| T002 | Implement core data model | M | 2 |
| T003 | Add authentication | L | 4 |
| T004 | Create API endpoints | M | 2 |
| T005 | Add tests | M | 2 |

**Total: 11 points** (~3 iterations at 4 pts/iteration)
```

Adjust based on feedback before writing the spec.

---

## Step 5: Write V2 Spec

### Format

```markdown
# Feature Name

Goal: One-sentence description of what this achieves when complete.

## Context

Background information for the agent implementing this spec:
- What problem does this solve?
- What existing code/patterns should it follow?
- Any constraints or requirements?
- (If research was conducted) Key findings from codebase research

## Tasks

### T001: First task title
- Status: pending
- Size: S

**Deliverables:**
- What to build (WHAT, not HOW)
- Another deliverable

**Verify:** `npm test -- something`

---

### T002: Second task title
- Status: pending
- Size: M

**Deliverables:**
- Deliverable description
- Another deliverable

**Verify:** `curl localhost:3000/api` returns 200

---

### T003: Third task title
- Status: pending
- Size: S

**Deliverables:**
- Deliverable description

**Verify:** `npm run type-check` passes

---

## Acceptance Criteria

- WHEN user does X, THEN Y happens
- WHEN condition Z, THEN expected outcome

## Notes

<!-- AI updates this section during implementation -->

### Interview Summary
- Project type: [from interview]
- Stack: [from interview]
- Key decisions: [from interview]
```

### V2 Format Rules

| Element | Format | Example |
|---------|--------|---------|
| Task ID | `### T###:` | `### T001: Setup database` |
| Status | `- Status: pending` | Always `pending` for new specs |
| Size | `- Size: S\|M\|L` | `- Size: M` |
| Deliverables | `**Deliverables:**` + bullets | See template |
| Verify | `**Verify:**` + command | `**Verify:** \`npm test\`` |
| Separator | `---` between tasks | Required |

### Content Rules

| Rule | Do | Don't |
|------|-----|-------|
| Task count | 3-10 total | 20+ micro-tasks |
| IDs | Sequential T001, T002... | T1, Task-1, random |
| Status | Always `pending` for new specs | Leave blank |
| Size | User-confirmed estimates | Skip or guess |
| Sub-bullets | Deliverables (WHAT) | Instructions (HOW) |
| Code | Only in **Verify:** | In task descriptions |
| File paths | Never in tasks | `src/auth.ts:42` |
| Batching | Related work = 1 task | Split into tiny pieces |

---

## Step 6: Check for Analysis (Optional)

After writing the spec, check if Ralphie ran analysis:

```bash
cat .ralphie/analysis.md 2>/dev/null
```

If the file exists:
- Read it to identify any gaps, edge cases, or missing elements
- Analysis may include:
  - Missing error handling scenarios
  - Unclear user flows
  - Missing verify commands or test coverage
  - Tasks that should be split
  - Integration points not addressed

If gaps found:
1. Review each concern
2. Decide with user whether to:
   - Revise spec to address gaps
   - Accept as-is (document why in spec Notes)
   - Add follow-up tasks

If analysis doesn't exist, skip to Step 7.

---

## Step 7: Present for Approval

Write spec to `.ralphie/specs/active/{name}.md` and present summary:

```markdown
## Spec Created

`.ralphie/specs/active/{name}.md` created with X tasks (Y size points total).

### Task Summary
| ID | Task | Size |
|----|------|------|
| T001 | First task | S |
| T002 | Second task | M |
...

### Estimated Effort
- Total points: Y
- Iterations needed: ~Z (at 4 pts/iteration)

### Research Findings (if available)
- [Key pattern 1 from research-context.md]
- [Key pattern 2 from research-context.md]

### Analysis Results (if available)
- ✅ All critical flows covered
- ⚠️ [Gap 1] - [How we addressed it or why it's acceptable]
- ⚠️ [Gap 2] - [How we addressed it or why it's acceptable]

### Key Decisions from Interview
- [Decision 1]
- [Decision 2]

Please review the spec. Ready to start with `ralphie run`?
```

The user reviews and approves. Since user is present, analysis gaps are discussed and resolved during the interview—no additional automated review needed.

---

## Quick Reference

| Check | Pass | Fail |
|-------|------|------|
| Location | `specs/active/*.md` | Missing or wrong directory |
| Task IDs | `### T001:` | `- [ ]`, `### Task 1:` |
| Status | `- Status: pending` | Missing or blank |
| Size | `- Size: S\|M\|L` (user confirmed) | Missing or unconfirmed |
| Deliverables | `**Deliverables:**` + bullets | Missing section |
| Verify | `**Verify:** \`cmd\`` | Missing section |
| Separators | `---` between tasks | None |
| Code | Only in Verify | In task descriptions |
| Files | No paths | `src/file.ts:42` |
