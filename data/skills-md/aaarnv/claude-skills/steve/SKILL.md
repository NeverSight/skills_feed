---
name: steve
description: The ultimate autonomous dev pipeline. Combines wavybaby (CoVe verification, skill discovery, MCP tooling) + GSD (roadmaps, phases, plans, discovery, state tracking) + Ralph (autonomous loop with circuit breakers). Generates a PRD, equips itself with the best tools, bootstraps a full GSD .planning/ structure, then runs Ralph to autonomously execute each plan with CoVe-verified code until the milestone is complete.
disable-model-invocation: false
user-invocable: true
argument-hint: "[project description or path]"
---

# Steve — wavybaby + GSD + Ralph Autonomous Execution

Combines three systems:
- **wavybaby**: Self-equipping toolchain (CoVe verification, skill discovery via skills.sh, MCP server setup, project config)
- **GSD**: Structured project management (`.planning/`, roadmaps, phases, plans, discovery, verification, state tracking)
- **Ralph**: Autonomous while-true loop (circuit breakers, dual-condition exit, session persistence, rate limiting)

The result: describe what you want. Steve equips itself with the best tools for the job, generates a PRD, builds a full GSD project structure, and runs an autonomous loop that executes every plan with verified code until the milestone is done.

```
User's description
    |
    v
PHASE 0: Equip (wavybaby)
    |  - Detect project type and stack
    |  - Search skills.sh for relevant skills, install missing ones
    |  - Install missing MCP servers (Context7, Supabase, Sentry, etc.)
    |  - Set up project config (settings.local.json, CLAUDE.md)
    |  - Now the agent has the best tools for THIS specific project
    |
    v
PHASE 1: PRD Generation
    |  - Clarifying questions
    |  - Full PRD at .planning/specs/PRD.md
    |
    v
PHASE 2: GSD Project Bootstrap
    |  - PROJECT.md, ROADMAP.md, STATE.md, config.json
    |  - codebase/ docs (STACK, ARCHITECTURE, STRUCTURE, CONVENTIONS)
    |  - Phase directories with DISCOVERY.md per phase
    |
    v
PHASE 3: Plan Generation
    |  - Break each phase into {NN}-{NN}-PLAN.md files
    |  - Each plan: 1-4 hours, atomic, with verification steps
    |
    v
PHASE 4: Loop Configuration
    |  - .ralphrc tuned for GSD execution
    |  - PROMPT.md with GSD execution + CoVe verification logic
    |  - AGENT.md with build/test/lint commands
    |
    v
PHASE 5: Autonomous Execution
    - ralph --monitor
    - Each loop iteration: read STATE.md -> execute next plan (with CoVe on non-trivial code) -> write SUMMARY.md -> update STATE.md
    - Circuit breaker halts if stuck
    - Exits when all phases complete
```

---

## PHASE 0: EQUIP (wavybaby)

Before generating anything, equip the agent with the best tools for this specific project. This is what separates Steve from raw GSD+Ralph — the agent isn't flying blind.

### Step 1: Detect project type

Scan for: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pubspec.yaml`, `Podfile`, `build.gradle`. Determine:
- Language(s)
- Framework(s)
- Package manager
- Existing dependencies

### Step 2: Search and install relevant skills

```bash
# Search skills.sh for skills matching the detected stack
npx skills find "[detected framework]"
npx skills find "[detected language]"
npx skills find "[project domain from user description]"
```

**Auto-install recommendations based on stack:**

| Stack | Skills to Install |
|-------|------------------|
| React / Next.js | `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code -y` |
| React Native / Expo | `npx skills add expo/skills --agent claude-code -y` |
| Supabase | `npx skills add supabase/agent-skills --agent claude-code -y` |
| Stripe payments | `npx skills add stripe/skills --agent claude-code -y` |
| Cloudflare | `npx skills add cloudflare/skills --agent claude-code -y` |
| Any web project | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines --agent claude-code -y` |
| Security-critical | `npx skills add trailofbits/skills --agent claude-code -y` |

Install all relevant skills immediately — don't ask, just do it. The `-y` flag auto-confirms.

### Step 3: Install missing MCP servers

Check which MCP servers are already configured, then install all relevant ones directly:

| Server | When to Install | Command |
|--------|----------------|---------|
| Context7 | Always (prevents doc hallucinations) | `claude mcp add context7 -- npx -y @upstash/context7-mcp` |
| GitHub | If using GitHub | `claude mcp add github --transport http https://api.githubcopilot.com/mcp/` |
| Supabase | If Supabase in stack | `claude mcp add supabase -- npx -y @supabase/mcp-server` |
| Sentry | If error tracking needed | `claude mcp add sentry --transport http https://mcp.sentry.dev/mcp` |
| Notion | If docs workflow | `claude mcp add notion --transport http https://mcp.notion.com/mcp` |
| Sequential Thinking | Complex architecture | `claude mcp add thinking -- npx -y mcp-sequentialthinking-tools` |

### Step 4: Set up project config

If missing, create `settings.local.json` with appropriate permissions:

**Full-Stack (Node/React):**
```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "Bash(npm *)", "Bash(pnpm *)",
      "Bash(git *)", "Bash(gh *)",
      "Bash(docker *)",
      "mcp__plugin_context7_context7__*",
      "Skill(*)"
    ]
  }
}
```

**Python:**
```json
{
  "permissions": {
    "allow": [
      "Bash(python *)", "Bash(pip *)", "Bash(poetry *)",
      "Bash(pytest *)", "Bash(docker-compose *)",
      "Bash(git *)"
    ]
  }
}
```

Adjust per detected stack.

### Step 5: Report equip status

```
Equipped for: [project type]

Skills installed:
  - [skill 1] (from [repo])
  - [skill 2] (from [repo])

MCP servers configured:
  - [server 1]: [purpose]
  - [server 2]: [purpose]

Project config: settings.local.json [created/updated/already exists]
```

---

## PHASE 1: PRD GENERATION

### Deep-dive questioning (MANDATORY)

Before writing the PRD, conduct a thorough interview. Ask questions in **multiple rounds** using AskUserQuestion. Do NOT rush to generate the PRD — the quality of the PRD depends entirely on how well you understand the project. Keep asking until you have a clear picture.

**Round 1: Vision & Users**
- "What problem does this solve? What's the pain point today?"
- "Who are the primary users? Describe 2-3 distinct personas."
- "What does success look like? How will you know this is working?"
- "Are there existing products/competitors? What do they get wrong?"

**Round 2: Core Experience**
- "Walk me through the ideal user journey from first open to daily use."
- "What are the 3 features that MUST exist for this to be useful? What's the single most important one?"
- "What should the user feel when using this? (fast, calm, powerful, fun, simple)"
- "Are there any workflows that need to feel instant vs. ones that can load?"

**Round 3: Technical & Platform**
- "What's the target platform? (iOS, Android, both, web, desktop, CLI)"
- "Any existing backend, database, auth system, or APIs to integrate with?"
- "Do you have preferences on stack/framework, or should I recommend?"
- "Does this need real-time features? (live updates, collaboration, notifications)"
- "Offline support needed? What should work without internet?"
- "Any third-party services? (payments, maps, analytics, AI/ML, messaging)"

**Round 4: Data & Business Logic**
- "What are the core entities/objects in this system? (users, posts, orders, etc.)"
- "What are the key relationships between them? (a user has many X, an X belongs to Y)"
- "Are there different user roles or permission levels? Describe each."
- "Any complex business rules? (pricing tiers, approval workflows, calculations)"
- "What data is sensitive? (PII, financial, health)"

**Round 5: Scope & Constraints**
- "What's MVP vs. nice-to-have vs. definitely-not-now?"
- "Any hard deadlines or constraints?"
- "Any design preferences? (dark mode, specific brand colors, reference apps you love)"
- "What about accessibility? (screen reader support, color blindness, motor impairment)"
- "Internationalization needed? Which languages/locales?"
- "Any compliance requirements? (GDPR, HIPAA, SOC2, PCI)"

**Round 6: Edge Cases & Polish**
- "What happens when something goes wrong? (no internet, server error, invalid input)"
- "What empty states exist? (new user, no data yet, search with no results)"
- "What notifications/emails/alerts should the system send?"
- "Onboarding flow — how does a new user learn the app?"
- "Any admin/backoffice needs? (dashboards, moderation, analytics)"

You do NOT need to ask every single question. Skip ones that are obviously irrelevant to the project. But you MUST ask across at least 4 of these 6 rounds. Use your judgment — if the user's description is vague, ask more. If it's detailed, focus on gaps.

After each round, acknowledge what you've learned and explain what you still need to know before asking the next round. Stop when you have enough to write a comprehensive PRD.

### Generate `.planning/specs/PRD.md`

Write a complete PRD with ALL sections:

```markdown
# PRD: [Project Name]

## 1. Overview
One paragraph: what this does and why.

## 2. Target Users
| User Type | Description | Primary Need |
|-----------|-------------|--------------|
| ... | ... | ... |

## 3. User Stories

### Epic: [Feature Area 1]
- **US-001**: As a [user], I want to [action] so that [benefit]
  - Acceptance Criteria:
    - [ ] [Specific, testable criterion]
    - [ ] [Specific, testable criterion]

(Continue for all epics/stories)

## 4. Technical Requirements

### Stack
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| ... | ... | ... |

### Architecture
- Key architectural decisions
- Data flow
- API structure

### Data Model
| Entity | Key Fields | Relationships |
|--------|-----------|---------------|
| ... | ... | ... |

### API Endpoints
| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| ... | ... | ... | ... |

## 5. Screens & Navigation

### Screen Map
(Tree diagram of all screens/routes)

### Screen Descriptions
| Screen | Purpose | Key Components |
|--------|---------|----------------|
| ... | ... | ... |

## 6. Non-Functional Requirements
- Performance targets
- Security requirements
- Accessibility
- Offline support

## 7. MVP Scope
### In Scope (MVP)
### Out of Scope (Post-MVP)

## 8. Success Metrics
| Metric | Target | How Measured |
|--------|--------|--------------|
| ... | ... | ... |

## 9. Open Questions
```

### Get approval before proceeding

Use AskUserQuestion: "PRD generated at `.planning/specs/PRD.md`. Ready to proceed, or want changes?"

---

## PHASE 2: GSD PROJECT BOOTSTRAP

Once the PRD is approved, create the full `.planning/` structure.

### Step 1: Create directory structure

```bash
mkdir -p .planning/specs .planning/codebase .planning/phases
```

### Step 2: Generate PROJECT.md (from PRD sections 1, 4, 7)

```markdown
# Project: [Name]

## Vision
[From PRD §1 Overview]

## Requirements

### Validated
[From PRD §7 MVP In Scope — these are confirmed requirements]

### Active (Under Discussion)
[From PRD §9 Open Questions — unresolved items]

### Out of Scope
[From PRD §7 Out of Scope]

## Constraints
[From PRD §4 Stack rationale and §6 Non-Functional Requirements]

## Key Decisions
| Decision | Status | Rationale |
|----------|--------|-----------|
| [Stack choice from PRD §4] | Approved | [Rationale] |
| ... | ... | ... |
```

### Step 3: Generate ROADMAP.md (from PRD sections 3, 4, 5)

Derive phases from the PRD. Every phase traces to user stories or technical requirements.

```markdown
# Roadmap — Milestone 1: MVP

## Progress
| Phase | Name | Status | Plans |
|-------|------|--------|-------|
| 1 | Infrastructure & Setup | Not Started | TBD |
| 2 | Auth & User Management | Not Started | TBD |
| 3 | [Core Feature 1] | Not Started | TBD |
| ... | ... | ... | ... |

---

### Phase 1: Infrastructure & Setup
**Goal**: Project scaffolding, database schema, auth config, navigation skeleton
**Depends on**: None
**Research**: Likely
**Research topics**: [Stack from PRD §4]
**Traces to**: PRD §4 (Technical Requirements)

### Phase 2: Auth & User Management
**Goal**: Sign up, login, forgot password, session management
**Depends on**: Phase 1
**Research**: Unlikely
**Traces to**: PRD §3 Epic: Auth, PRD §5 Auth Stack screens

### Phase 3: [Core Feature from PRD §3]
**Goal**: [From user story epic]
**Depends on**: Phase 1, Phase 2
**Research**: [Likely/Unlikely]
**Traces to**: PRD §3 Epic: [Name], US-001 through US-00N

(Continue for all phases derived from PRD)

### Phase N: Polish & Verification
**Goal**: Error states, empty states, performance, accessibility
**Depends on**: All previous phases
**Traces to**: PRD §6 Non-Functional Requirements
```

**Derivation rules:**
1. Infrastructure/setup is always Phase 1
2. Auth is Phase 2 (if applicable)
3. Each PRD Epic becomes one or more phases
4. PRD §5 Screen Map informs navigation phases
5. PRD §6 Non-Functional becomes a final polish phase
6. Every phase traces back to a PRD section

### Step 4: Generate STATE.md

```markdown
# Project State

## Current Position
- **Phase**: 1 of N (Infrastructure & Setup)
- **Plan**: Not started
- **Status**: Not started
- **Progress**: [░░░░░░░░░░] 0%

## Performance Metrics
- Plans completed: 0
- Average duration: N/A
- Total execution time: 0

## Accumulated Context
- Decisions: See PROJECT.md
- Deferred issues: None
- Blockers: None

## Session
- Last activity: [date] — Project initialized
- Mode: Autonomous (Ralph loop)
```

### Step 5: Generate config.json

```json
{
  "mode": "yolo",
  "depth": "comprehensive",
  "gates": {
    "confirm_project": false,
    "confirm_phases": false,
    "confirm_roadmap": false,
    "confirm_breakdown": false,
    "confirm_plan": false,
    "execute_next_plan": true,
    "issues_review": false,
    "confirm_transition": false
  },
  "safety": {
    "always_confirm_destructive": true,
    "always_confirm_external_services": true
  }
}
```

Gates are set to `false` for autonomous execution — Ralph doesn't stop to ask. Safety gates remain `true`.

### Step 6: Generate codebase docs

If the project directory already has code, run the equivalent of `gsd:map-codebase`:
- `.planning/codebase/STACK.md` — technologies, deps, versions
- `.planning/codebase/ARCHITECTURE.md` — patterns, layers, data flow
- `.planning/codebase/STRUCTURE.md` — directory layout
- `.planning/codebase/CONVENTIONS.md` — naming, style, patterns

If it's a new project, create skeleton versions that get populated during Phase 1.

---

## PHASE 3: PLAN GENERATION

For **Phase 1 only** (the first phase to execute), generate full plans now. Subsequent phases get planned just-in-time by the loop, since earlier phases inform later decisions.

### For each plan in Phase 1, generate `{NN}-{NN}-PLAN.md`:

```xml
<plan>
  <phase>1</phase>
  <plan-number>01</plan-number>
  <type>execute</type>
  <name>[Descriptive name]</name>
</plan>

<objective>
[What this plan delivers and why, traced to PRD section]
</objective>

<context>
- PRD: .planning/specs/PRD.md
- Project: .planning/PROJECT.md
- Stack: .planning/codebase/STACK.md
</context>

<tasks>
  <task type="auto">
    <name>[Task name]</name>
    <files>[Files to create/modify]</files>
    <action>
      [Detailed implementation instructions]
    </action>
    <verify>
      - [ ] [Verification step]
      - [ ] [Verification step]
    </verify>
    <done>[Success indicator]</done>
  </task>

  <!-- More tasks -->
</tasks>

<verification>
  - [ ] All files created/modified as specified
  - [ ] Tests pass
  - [ ] No TypeScript/lint errors
  - [ ] Acceptance criteria from PRD met
</verification>

<success_criteria>
[Definition of done for this plan]
</success_criteria>
```

---

## PHASE 4: LOOP CONFIGURATION

### Step 1: Check Ralph installation

```bash
which ralph-loop 2>/dev/null || which ralph 2>/dev/null
```

If not installed:
```bash
git clone https://github.com/frankbria/ralph-claude-code.git /tmp/ralph-claude-code
cd /tmp/ralph-claude-code && ./install.sh
```

### Step 2: Generate .ralphrc

```bash
PROJECT_NAME="$ARGUMENTS"
PROJECT_TYPE="[detected]"
MAX_CALLS_PER_HOUR=100
CLAUDE_TIMEOUT_MINUTES=20
CLAUDE_OUTPUT_FORMAT="json"
ALLOWED_TOOLS="Write,Read,Edit,Bash(git *),Bash(npm *),Bash(npx *),Skill(gsd:*)"
SESSION_CONTINUITY=true
SESSION_EXPIRY_HOURS=24
TASK_SOURCES="local"
CB_NO_PROGRESS_THRESHOLD=3
CB_SAME_ERROR_THRESHOLD=5
CB_OUTPUT_DECLINE_THRESHOLD=70
```

Adjust `ALLOWED_TOOLS` per project type:
- **TypeScript/Node**: `Bash(npm *),Bash(npx *),Bash(node *)`
- **Python**: `Bash(python *),Bash(pip *),Bash(pytest *)`
- **Rust**: `Bash(cargo *),Bash(rustc *)`
- **Go**: `Bash(go *)`
- Add `Bash(docker *)` if Dockerfile present

### Step 3: Generate PROMPT.md

This is the critical file — it tells the loop how to execute GSD plans with CoVe verification.

```markdown
# Project: [PROJECT_NAME]

## Your Mission

You are working autonomously in a Ralph loop executing GSD plans. You are equipped with wavybaby tools — use them. Each iteration:

### 0. Use your tools

You have been equipped with skills and MCP servers for this project. USE THEM:
- **Context7**: Query up-to-date docs before using any library. Don't guess APIs.
- **Installed skills**: Follow best practices from installed skill files.
- **CoVe verification**: For any non-trivial code (stateful, async, database, auth, security), run the 4-stage CoVe protocol from /rnv before committing.

### 1. Read current state
- Read `.planning/STATE.md` to find current phase and plan
- Read `.planning/ROADMAP.md` for phase context and dependencies

### 2. Determine next action

Follow this decision tree:

```
Is current phase's DISCOVERY.md missing?
  YES → Run research: read PRD, explore codebase, write DISCOVERY.md
        Use Context7 to look up docs for any unfamiliar tech.
  NO  ↓

Are there ungenerated plans for current phase?
  YES → Generate next {NN}-{NN}-PLAN.md from DISCOVERY.md + PRD
  NO  ↓

Is there an unexecuted plan in current phase?
  YES → Execute it (see "Execute a Plan" below)
  NO  ↓

Are all plans in current phase complete?
  YES → Complete phase: update ROADMAP.md, advance STATE.md to next phase
  NO  → Something is wrong. Set STATUS: BLOCKED.

Are all phases complete?
  YES → Run verification gate. If passing, set EXIT_SIGNAL: true
  NO  → Continue to next phase (loop back to top)
```

### 3. Execute a Plan

When executing a `{NN}-{NN}-PLAN.md`:

1. Read the plan file completely
2. Execute each `<task>` in order
3. **For non-trivial tasks**, apply CoVe:
   - Generate code [UNVERIFIED]
   - Plan verification targets specific to THIS code
   - Independently verify each target
   - Apply fixes → [VERIFIED] code
4. After each task, run its `<verify>` checks
5. After all tasks, run the plan's `<verification>` section
6. Write `{NN}-{NN}-SUMMARY.md` with results
7. Commit changes with descriptive message
8. Update `.planning/STATE.md` (increment plan, update metrics)

### 4. CoVe triggers

Apply the full 4-stage CoVe protocol (from /rnv) for:
- Stateful code (useState, useReducer, context, stores)
- Async/concurrent logic (useEffect, mutations, subscriptions)
- Database operations (queries, transactions, migrations)
- Auth/security code
- Cache invalidation logic
- Financial or precision-critical calculations
- Any code where the bug would be subtle, not obvious

Skip CoVe only for: trivial one-liners, pure formatting, config files.

### 5. Generate plans for next phase (just-in-time)

When advancing to a new phase:
1. Read DISCOVERY.md for that phase (or create it first)
2. Read relevant PRD sections (the phase's "Traces to" field)
3. Use Context7 to look up any new tech introduced in this phase
4. Generate all {NN}-{NN}-PLAN.md files for the phase
5. Begin executing plan 01

## Key Rules

- ONE plan per loop iteration (stay focused)
- Always run tests after implementation tasks
- Write SUMMARY.md after every completed plan
- Update STATE.md after every completed plan
- Reference the PRD for acceptance criteria — don't guess
- Use Context7 for library docs — don't hallucinate APIs
- Apply CoVe on non-trivial code — don't ship unverified
- If blocked, set STATUS: BLOCKED and explain why
- Never skip verification steps
- Commit atomically per task when possible

## Required Output Format

At the END of every response, output EXACTLY:

---RALPH_STATUS---
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
PHASE: [current phase number and name]
PLAN: [current plan number or "generating" or "researching"]
TASKS_COMPLETED_THIS_LOOP: <number>
FILES_MODIFIED: <number>
TESTS_STATUS: PASSING | FAILING | NOT_RUN
WORK_TYPE: RESEARCH | PLANNING | IMPLEMENTATION | VERIFICATION
COVE_APPLIED: true | false | N/A
EXIT_SIGNAL: false
RECOMMENDATION: <what was done and what's next>
---END_RALPH_STATUS---

Set EXIT_SIGNAL: true ONLY when:
- ALL phases in ROADMAP.md are complete
- ALL SUMMARY.md files written
- Final verification gate passes
- STATE.md shows 100% progress
```

### Step 4: Generate AGENT.md

```markdown
# Agent Instructions

## Build
[detected build command]

## Test
[detected test command]

## Run
[detected run command]

## Lint
[detected lint command]

## Type Check
[detected type check command if applicable]

## Equipped Tools
- Context7: Use `mcp__plugin_context7_context7__resolve-library-id` then `query-docs` for any library docs
- Installed skills: [list skills installed in Phase 0]
- CoVe: Apply 4-stage verification on non-trivial code (see PROMPT.md §4)

## GSD Commands
- Execute plan: Read the PLAN.md and follow its tasks
- Write summary: Create SUMMARY.md after plan completion
- Update state: Modify STATE.md with progress
```

### Step 5: Add to .gitignore

```bash
echo -e "\n# Ralph loop state\n.ralph/logs/\n.ralph/status.json\n.ralph/progress.json\n.ralph/.call_count\n.ralph/.last_reset\n.ralph/.exit_signals\n.ralph/.response_analysis\n.ralph/.circuit_breaker_state\n.ralph/.claude_session_id\n.ralph/.ralph_session\n.ralph/.ralph_session_history" >> .gitignore
```

### Step 6: Print run instructions

```
Steve setup complete.

EQUIPPED:
  Skills:         [list installed skills]
  MCP servers:    [list configured servers]
  Config:         settings.local.json

PROJECT:
  PRD:            .planning/specs/PRD.md        (review before running)
  Project:        .planning/PROJECT.md          (derived from PRD)
  Roadmap:        .planning/ROADMAP.md          (phases derived from PRD)
  State:          .planning/STATE.md            (tracks progress)
  Phase 1 Plans:  .planning/phases/01-*/        (ready to execute)

LOOP:
  Config:         .ralphrc                      (rate limits, timeouts)
  Prompt:         .ralph/PROMPT.md              (GSD + CoVe execution logic)
  Build/test:     .ralph/AGENT.md               (edit if auto-detect wrong)

To run:
  ralph --monitor      # Recommended: loop + dashboard in tmux
  ralph                # Loop only

The loop will:
  1. Execute Phase 1 plans sequentially (with CoVe on non-trivial code)
  2. Write SUMMARY.md after each plan
  3. Use Context7 for library docs (no hallucinated APIs)
  4. Generate Phase 2 plans just-in-time
  5. Continue through all phases
  6. Run final verification gate
  7. Exit when milestone is complete

To check progress:
  cat .planning/STATE.md
  ralph-monitor
```

---

## HOW THE LOOP EXECUTES GSD

### Per-Iteration Flow

```
Loop iteration N:
  1. Read .planning/STATE.md
  2. Identify: Phase X, Plan Y
  3. If DISCOVERY.md missing → research phase (use Context7) → write DISCOVERY.md → done
  4. If plans not generated → generate plans from DISCOVERY + PRD → done
  5. Read .planning/phases/{X}-{name}/{XX}-{YY}-PLAN.md
  6. Execute all tasks in plan
     - Non-trivial code → CoVe 4-stage verification
     - Library usage → Context7 doc lookup
  7. Run verification checks
  8. Write {XX}-{YY}-SUMMARY.md
  9. Update STATE.md (plan Y+1, metrics)
  10. If last plan in phase → update ROADMAP.md, advance to Phase X+1
  11. If last phase → verification gate → EXIT_SIGNAL: true
  12. Output RALPH_STATUS block
```

### Circuit Breaker (from Ralph)

| Trigger | Result |
|---------|--------|
| 3 loops no file changes | OPEN (halted) |
| 5 loops same error | OPEN (halted) |
| 2 loops no progress in STATE.md | HALF_OPEN (monitoring) |
| Progress resumes | CLOSED (recovered) |

### Exit Detection (Dual-Condition Gate)

Ralph only stops when BOTH:
1. `completion_indicators >= 2` (from RALPH_STATUS blocks)
2. `EXIT_SIGNAL: true` (all phases complete, verification gate passed)

### Session Continuity

- Session persists via `--continue` flag
- `.planning/STATE.md` provides additional continuity beyond Ralph's built-in session
- Even if Ralph session resets, STATE.md tells the agent exactly where to resume

---

## COMPARISON

| Feature | Spidey | GSD only | Steve |
|---------|--------|----------|-------|
| Auto-equip (skills, MCP, config) | No | No | Yes (wavybaby) |
| PRD generation | Yes | No | Yes |
| Structured phases | No (flat checklist) | Yes | Yes |
| Discovery/research docs | No | Yes | Yes |
| Atomic plans with verification | No | Yes | Yes |
| CoVe code verification | No | No | Yes (wavybaby/rnv) |
| Context7 doc lookups | No | No | Yes (wavybaby) |
| State tracking | Basic | Detailed | Detailed |
| Autonomous execution | Yes (Ralph loop) | No (manual) | Yes (Ralph loop) |
| Circuit breakers | Yes | No | Yes |
| Session persistence | Ralph session | STATE.md | Both |
| Just-in-time planning | No (all upfront) | Yes | Yes |
| SUMMARY.md audit trail | No | Yes | Yes |
| Codebase documentation | No | Yes | Yes |
| Progress metrics/velocity | Basic | Detailed | Detailed |

---

Now setting up Steve for: **$ARGUMENTS**
