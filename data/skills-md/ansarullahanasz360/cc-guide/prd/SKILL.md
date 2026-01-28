---
name: prd
description: Create self-verifying PRDs for autonomous execution. Interviews users to gather requirements, then generates structured prd.json with phased implementation and appropriate testing strategies. Supports 7 task categories with type-specific workflows. Use when user says "create a prd", "prd for", "plan a feature", "plan this", "write prd", or wants to plan any multi-step implementation work.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - TodoWrite
  - AskUserQuestion
  - Bash
  - Task
---

# PRD Creation Skill

Create self-verifying PRDs for autonomous execution. This skill guides you through interviewing users and generating structured PRDs.

## Core Philosophy

You are intelligent. These guidelines inform your thinking - they don't constrain it.

- **Adapt to the user** - Every project is different. Adjust your approach.
- **Think independently** - You decide what questions to ask and when to stop.
- **Verify, don't assume** - Challenge assumptions and uncover edge cases.
- **Principles over prescriptions** - Apply mental models, not rigid scripts.

## Important Guardrails

- **Do NOT start implementing** - Your job is to create the PRD, not write code.
- **Ask questions one set at a time** - Don't overwhelm with multiple question blocks.
- **Always ask about quality gates** - This is REQUIRED for every PRD.
- **Get explicit approval before generating** - Present your understanding first.

For comprehensive reference material, read `AGENTS.md`. For specific guidance, reference the `interview/` and `categories/` directories.

---

## The Interview Process

Your goal: Extract enough information to create a PRD that an AI agent can execute successfully.

### Phase 1: Identify Task Type

Start by understanding what kind of work this is. Use AskUserQuestion with these categories:

| Category | Use For |
|----------|---------|
| Feature Development | New features, enhancements, integrations |
| Bug Fixing | Single bugs, multiple bugs, regressions |
| Research & Planning | Exploration, architecture decisions, spikes |
| Quality Assurance | Testing, code review, security audits |
| Maintenance | Docs, cleanup, refactoring, optimization |
| DevOps | Deployment, CI/CD, infrastructure |
| General | Anything else |

For detailed category guidance, see `categories/_overview.md` and individual category files.

### Phase 2: Brain Dump

Ask the user to share everything they know. Let information flow without imposing structure.

What you need to understand:
- The problem or goal
- Context and background
- Constraints and requirements
- Who benefits and how
- Files, systems, or areas involved
- Sources to reference (docs, APIs, existing code)

For guidance on gathering initial information, see `interview/brain-dump.md`.

### Phase 3: Clarifying Questions

This is where you think independently. Based on what they told you:

- What gaps remain in your understanding?
- What assumptions should you challenge?
- What could go wrong that they haven't mentioned?
- What decisions need their input vs. your judgment?

The number of rounds depends on complexity. Simple tasks: 2-3 rounds. Complex features: 6-10 rounds. You decide when you have enough.

**Ask questions one set at a time.** After each answer, decide whether to:
- Ask follow-up questions (if answers reveal complexity)
- Ask about a new aspect (if current area is clear)
- Move to confirmation phase (if you have enough context)

For guidance on formulating questions, see `interview/clarifying-questions.md`.

#### Lettered Multiple Choice Format

When appropriate, use lettered options to speed up responses:

```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Other: [please specify]

2. Who is the target user?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only
```

This lets users respond with "1A, 2C" for quick iteration.

#### Quality Gates Question (REQUIRED)

Always ask about quality gates - these follow a **two-tiered testing approach**:

**Tier 1: Story-Level Testing** (every story must do this)
- Write ALL tests for the feature being implemented (no tests left out)
- Run lint, typecheck, build verification
- Run ALL tests related to that story: unit tests, integration tests for the code touched, E2E tests if the story has UI
- All tests must be written AND pass before the story is complete

**Tier 2: Dedicated Testing Sessions** (end of phase or PRD)
- Run the complete test suite to ensure nothing broke
- Verify all E2E tests pass
- For features with UI: comprehensive browser verification

```
1. What quality commands should run for story-level testing?
   A. pnpm typecheck && pnpm lint && pnpm test --related
   B. npm run typecheck && npm run lint && npm test -- --findRelatedTests
   C. bun run typecheck && bun run lint && bun test --related
   D. Other: [specify your commands]

2. Does this project have E2E tests?
   A. Yes - Playwright
   B. Yes - Cypress
   C. Yes - Other framework
   D. No E2E tests yet (we should add them)

3. For UI stories, should we include browser verification?
   A. Yes, use agent-browser skill to verify visually
   B. No, automated tests are sufficient
```

### Phase 4: Confirm Understanding

Before generating, present your understanding:

- What you think they want (problem + solution)
- Your proposed approach
- Rough phase breakdown
- Testing and verification strategy

Get explicit approval. If they want changes, adapt and re-present.

For guidance on confirmation, see `interview/confirmation.md`.

---

## Category-Specific Guidance

Each task type has different priorities and workflows. These are thinking frameworks, not templates.

| Category | Key Focus | Reference |
|----------|-----------|-----------|
| Feature Development | Spec → Dependencies → Implementation → Verification | `categories/feature-development.md` |
| Bug Fixing | Reproduce → Investigate → Fix → Verify | `categories/bug-fixing.md` |
| Research & Planning | Requirements → Exploration → Design → Plan | `categories/research-planning.md` |
| Quality Assurance | Scan → Test → Review → Improve | `categories/quality-assurance.md` |
| Maintenance | Review → Identify → Clean → Verify | `categories/maintenance.md` |
| DevOps | Plan → Test → Execute → Verify | `categories/devops.md` |
| General | Understand → Break Down → Implement → Document | `categories/general.md` |

---

## Agent Browser CLI

Use Agent Browser CLI throughout your work for any visual or interactive components.

**When to use it:**
- Research: Explore documentation, validate approaches
- Features: Verify UI as you build, final validation against spec
- Bugs: Reproduce issues, verify fixes
- QA: Test user flows, visual validation

**Quick reference:**
```bash
agent-browser open http://localhost:3000    # Start session
agent-browser snapshot -i                   # Get interactive elements
agent-browser click @e5                     # Click element
agent-browser fill "[name='email']" "test"  # Fill input
agent-browser screenshot verify.png         # Capture state
agent-browser close                         # Clean up
```

This is emphasized throughout all category guidance - browser verification is essential for UI work.

---

## Story Structure

Every story in the PRD needs these elements:

### Required Components

1. **Description** - WHAT is this and WHY does it matter? Not HOW.

2. **Tasks** - Step-by-step instructions. Start with context gathering, end with verification.

3. **Acceptance Criteria** - How do we know it's done? Specific, verifiable statements.

4. **Notes** - File paths, patterns to follow, warnings about pitfalls.

### Common Story Types

| Type | Purpose |
|------|---------|
| Context Gathering | First story of any phase - read, understand, document approach |
| Implementation | The actual work with verification steps |
| Checkpoint | End of phase - verify everything, document learnings |
| Browser Verification | For UI work - validate visually and interactively |
| Final Validation | Run full test suite, build, ensure passing |
| Report | Document what was done, decisions, issues |

### Ralph Loop Optimization

When creating stories, keep in mind that Ralph loops operate with these constraints:

**Each iteration starts with no memory** - The agent must read `.ralph-tui/progress.md` to understand prior work. This means:
- Story notes should include file paths, function names, and specific locations
- Reference existing patterns that the agent should follow
- Include gotchas or edge cases discovered during planning

**Progress entries must be verbose** - The template instructs agents to write detailed progress entries with:
- What was implemented (specific function names, class names)
- Files changed (with descriptions)
- Learnings (patterns, gotchas, architecture insights)
- Quality gate results

**Include this context in story notes** when relevant:
- Which files are likely to be modified
- What existing patterns to follow
- What the agent should document for future iterations

---

## Verification & Testing

Use the **two-tiered testing approach** for all PRDs:

### Tier 1: Story-Level Testing (REQUIRED for every story)

Every story must:
1. **Write tests first** - All tests related to the feature being implemented
2. **Run story-specific tests** - No test is left out from the implementation:
   - Lint and typecheck
   - Unit tests for new code
   - Integration tests for touched code paths
   - E2E tests if the story has UI components
3. **All tests must pass** - Story is not complete until tests are written AND passing

| What to Run | When |
|-------------|------|
| Lint + Typecheck | Every story |
| Unit tests for new code | Every story with new functions/components |
| Integration tests for touched code | Every story that modifies existing behavior |
| E2E tests for the feature | Every story with UI or user-facing changes |
| Build verification | Every story |

### Tier 2: Dedicated Testing Sessions (End of phase/PRD)

Include dedicated testing stories at:
- End of each implementation phase
- Final validation before PRD completion

These sessions:
- Run the **complete test suite** (not just related tests)
- Ensure **all E2E tests pass** (full coverage, not just new ones)
- Fix any regressions discovered
- For features: verify E2E tests exist and pass for all user flows

**UI work always gets browser verification** - if there's a visual component, verify it with Agent Browser CLI.

---

## Output Format

Generate two files in `docs/prds/[name]/`:

### PRD.md (Human-readable)

```markdown
# [Project Name]

## Overview
[What and why]

## Goals
[Specific outcomes]

## Quality Gates

### Story-Level Testing (every story)
- `[lint command]` - Lint check
- `[typecheck command]` - Type verification
- `[test command --related]` - Run tests related to changed files
- `[build command]` - Build verification

For stories with UI:
- Run E2E tests for the specific feature
- Verify in browser using agent-browser skill

### Dedicated Testing Sessions (end of phase)
- `[full test command]` - Complete test suite
- `[e2e test command]` - All E2E tests
- Fix any regressions before proceeding

## Non-Goals
[Out of scope]

## Technical Approach
[High-level strategy]

## Phases
[Phase breakdown with objectives]

## Testing Strategy
[How verification happens]

## Risks & Mitigations
[What could go wrong and how to handle it]

## Success Criteria
[How we know it's complete]
```

**IMPORTANT:** Wrap the final PRD.md content in `[PRD]...[/PRD]` markers for parsing:

```
[PRD]
# PRD: [Project Name]

## Overview
...

## Quality Gates
...

## User Stories
...
[/PRD]
```

### prd.json (Machine-readable)

```json
{
  "name": "kebab-case-name",
  "description": "Context for all tasks. Motivation, goals, reference CLAUDE.md.",
  "branchName": "type/feature-name",
  "userStories": [
    {
      "id": "US-001",
      "title": "Short descriptive title",
      "description": "WHAT and WHY - not HOW. Include tasks embedded here:\n\n**Tasks:**\n1. First task\n2. Second task\n3. Third task",
      "acceptanceCriteria": ["First criterion", "Second criterion", "Third criterion"],
      "dependsOn": [],
      "notes": "File paths, patterns, warnings",
      "passes": false
    }
  ]
}
```

**Key points:**
- `tasks`: Embed formatted tasks in `description` (not available as separate field to template)
- `acceptanceCriteria`: Use array - Ralph TUI's template engine converts it to string automatically
- Template receives `{{acceptanceCriteria}}` as a pre-formatted string with checkboxes

---

## After Generation

Provide the user with:

### 1. What Was Created
- File locations for PRD.md and prd.json
- Number of stories and phases

### 2. Pre-Flight Check

**IMPORTANT:** Before starting a Ralph loop, run the pre-flight check:

```
/ralph-preflight
```

This verifies:
- No global CLAUDE.md conflict
- Config and template paths are correct
- prd.json structure is valid
- Template variables will map correctly
- Template uses optimized v2 format (no `{{recentProgress}}`, has gibberish cleanup)
- Template has verbose progress entry format for cross-iteration context

### 3. Execution Setup

Once prd.json exists and pre-flight passes:

**Option A: Simple Branch (recommended for single feature)**
```bash
# 1. Create feature branch
git checkout -b [branch-name-from-prd]

# 2. Start Ralph in tmux
tmux new-session -d -s ralph-[name] "ralph-tui run --prd docs/prds/[name]/prd.json"
tmux attach-session -t ralph-[name]

# 3. Press 's' to start, then Ctrl+B D to detach
```

**Option B: Git Worktree (for parallel development)**
```bash
# 1. Create worktree with new branch
git worktree add ../[repo]-[name] -b [branch-name-from-prd]
cd ../[repo]-[name]

# 2. Copy .ralph-tui config if not using shared config
# (worktrees share git but have separate working directories)

# 3. Start Ralph in tmux
tmux new-session -d -s ralph-[name] "ralph-tui run --prd docs/prds/[name]/prd.json"
tmux attach-session -t ralph-[name]
```

**Ask user:**
```
AskUserQuestion: "How do you want to run this?"
├── "Simple branch" (Recommended) - Single feature in current directory
├── "Git worktree" - Parallel development in isolated directory
└── "Just show me the commands" - Manual setup
```

### 4. Monitoring Notes

**To check progress**:
```bash
# Reattach to tmux session
tmux attach-session -t prd-[name]

# Detach again (leave it running)
# Press Ctrl+B, then D

# Check progress file
cat .ralph-tui/progress.md

# Check iteration logs
ls -la .ralph-tui/iterations/
```

**Recommended check intervals**:
- Simple projects: Every 30-60 minutes
- Complex projects: Every 15-30 minutes initially, then as needed

**Understanding BLOCKED states**:
- BLOCKED means the AI needs human input
- Reattach and provide the needed information
- The loop will continue once you respond

**Where progress is tracked**:
| Location | Contains |
|----------|----------|
| `.ralph-tui/progress.md` | Accumulated learnings and patterns |
| `.ralph-tui/iterations/` | Detailed logs from each iteration |
| `.ralph-tui/state.json` | Current task and completion status |

### 5. Troubleshooting

**If ralphdui is not found**:
```bash
# Install ralph-tui globally
cargo install ralph-tui

# Or use via npx (if available)
npx ralph-tui --prd docs/prds/[name]/prd.json
```

**If the loop gets stuck**:
1. Reattach to tmux session
2. Check what state it's in
3. Provide input if BLOCKED
4. If truly stuck, Ctrl+C to stop and restart

**To start over**:
```bash
# Reset progress (keeps work, restarts loop)
rm -rf .ralph-tui/
ralphdui --prd docs/prds/[name]/prd.json
```

### 6. Important Reminders

- **Keep machine running** during execution - the loop operates autonomously
- **Check back at recommended intervals** - BLOCKED tasks need human input
- **Human input may be needed** for ambiguous situations or decisions
- **Work is committed automatically** after each completed task
- **All tests must pass** for a task to be marked COMPLETE
- **The loop continues** until all tasks are done or it encounters a BLOCKED state

---

## Completion Signals

When executing PRD tasks, use these signals:

| Signal | Meaning |
|--------|---------|
| `<promise>COMPLETE</promise>` | All criteria met, tests pass |
| `<promise>BLOCKED</promise>` | Need human input to proceed |
| `<promise>SKIP</promise>` | Non-critical, can't complete after genuine attempts |
| `<promise>EJECT</promise>` | Critical failure requiring human intervention |

---

## Key Reminders

- You are intelligent - use guidelines to think, not to follow blindly
- Adapt to the user and their specific situation
- Ask good questions, but know when to stop
- Agent Browser CLI is essential for visual/interactive work
- The goal is a PRD that an AI agent can execute successfully
- When in doubt, verify. When uncertain, ask.

For comprehensive guidance, read `AGENTS.md`.
