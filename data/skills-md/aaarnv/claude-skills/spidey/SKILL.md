---
name: spidey
description: Sets up a Ralph autonomous development loop for any project. First generates a full PRD from the user's description, then derives a task plan from it. Wraps Claude Code in an intelligent while-true loop with circuit breakers, exit detection, session persistence, and progress tracking. Use when you want Claude to autonomously work through a task list until done.
disable-model-invocation: true
user-invocable: true
argument-hint: "[project description or path]"
---

# Spidey — Autonomous Development Loop

Sets up a Ralph autonomous development loop. Unlike raw Ralph which just takes a checklist, Spidey first generates a full PRD, then derives all tasks from it.

## The Spidey Pipeline

```
User's lazy description
    ↓
┌─────────────────────────────────┐
│ PHASE 0: PRD GENERATION         │
│ Full product requirements doc   │
│ from a one-line description     │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ PHASE 1: TASK DERIVATION        │
│ fix_plan.md derived FROM the    │
│ PRD, not invented from nothing  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ PHASE 2: LOOP CONFIGURATION     │
│ .ralphrc, PROMPT.md, AGENT.md   │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ PHASE 3: AUTONOMOUS EXECUTION   │
│ ralph --monitor                 │
└─────────────────────────────────┘
```

---

## PHASE 0: PRD GENERATION

This is what separates spidey from raw Ralph. Before any code, generate a proper PRD.

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

### Generate `.ralph/specs/PRD.md`

Write a complete PRD with ALL of these sections:

```markdown
# PRD: [Project Name]

## 1. Overview
One paragraph describing what this product does and why it exists.

## 2. Target Users
| User Type | Description | Primary Need |
|-----------|-------------|--------------|
| [Persona 1] | [Who they are] | [What they need] |
| [Persona 2] | [Who they are] | [What they need] |

## 3. User Stories

### Epic: [Feature Area 1]
- **US-001**: As a [user], I want to [action] so that [benefit]
  - Acceptance Criteria:
    - [ ] [Specific, testable criterion]
    - [ ] [Specific, testable criterion]
    - [ ] [Specific, testable criterion]

- **US-002**: As a [user], I want to [action] so that [benefit]
  - Acceptance Criteria:
    - [ ] ...

### Epic: [Feature Area 2]
- **US-003**: ...

(Continue for all features)

## 4. Technical Requirements

### Stack
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | [e.g., React Native / Expo] | [Why] |
| Backend | [e.g., Supabase] | [Why] |
| Auth | [e.g., Supabase Auth] | [Why] |
| State | [e.g., TanStack Query] | [Why] |
| Navigation | [e.g., Expo Router] | [Why] |

### Architecture
- [Key architectural decisions]
- [Data flow description]
- [API structure]

### Data Model
| Entity | Key Fields | Relationships |
|--------|-----------|---------------|
| User | id, email, name, avatar | has_many: workouts |
| Workout | id, user_id, date, type | belongs_to: user, has_many: sets |
| ... | ... | ... |

### API Endpoints / Procedures
| Method | Path / Name | Purpose | Auth |
|--------|------------|---------|------|
| POST | /auth/signup | Create account | Public |
| GET | /workouts | List user workouts | Authenticated |
| ... | ... | ... | ... |

## 5. Screens & Navigation

### Screen Map
```
App
├── Auth Stack (unauthenticated)
│   ├── Welcome
│   ├── Sign Up
│   ├── Login
│   └── Forgot Password
└── Main Tabs (authenticated)
    ├── Home / Dashboard
    ├── [Feature Screen 1]
    ├── [Feature Screen 2]
    └── Profile / Settings
```

### Screen Descriptions
| Screen | Purpose | Key Components |
|--------|---------|----------------|
| Home | [What it shows] | [Cards, lists, charts, etc.] |
| ... | ... | ... |

## 6. Non-Functional Requirements

### Performance
- App launch < [X] seconds
- Screen transitions < [X]ms
- API response time < [X]ms

### Security
- [Auth requirements]
- [Data encryption requirements]
- [RLS / permission model]

### Accessibility
- [WCAG level target]
- [Screen reader support]
- [Minimum touch targets]

### Offline Support
- [What works offline]
- [Sync strategy]

## 7. MVP Scope

### In Scope (MVP)
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Out of Scope (Post-MVP)
- [Deferred feature 1]
- [Deferred feature 2]

## 8. Success Metrics
| Metric | Target | How Measured |
|--------|--------|--------------|
| [e.g., DAU] | [e.g., 100 in first month] | [Analytics tool] |
| ... | ... | ... |

## 9. Open Questions
- [Anything unresolved]
- [Decisions that need user input later]
```

### Present PRD for approval

After generating the PRD, show the user a summary and ask for approval before proceeding. Use AskUserQuestion:

- "PRD generated. Review `.ralph/specs/PRD.md`. Ready to proceed, or want changes?"

---

## PHASE 1: TASK DERIVATION (from PRD)

Once the PRD is approved, derive `fix_plan.md` directly from it.

### Derivation Rules

1. **Every user story** becomes one or more tasks
2. **Every acceptance criterion** becomes a verification step
3. **Infrastructure/setup** tasks come first (Critical)
4. **Core user flows** are High priority
5. **Enhancement features** are Medium
6. **Polish/nice-to-have** is Low
7. **Each task must be completable in a single loop iteration** (~15 min of Claude work)

### Generate `.ralph/fix_plan.md`

```markdown
# Fix Plan
Derived from: .ralph/specs/PRD.md

## Critical (Infrastructure & Setup)
- [ ] Project scaffolding (init, deps, config)
- [ ] Data model / database schema (from PRD §4 Data Model)
- [ ] Auth setup (from PRD §4 Auth)
- [ ] Navigation skeleton (from PRD §5 Screen Map)

## High (Core User Stories)
- [ ] US-001: [User story title] (from PRD §3)
  - Verify: [acceptance criteria 1]
  - Verify: [acceptance criteria 2]
- [ ] US-002: [User story title]
  - Verify: [acceptance criteria]
- [ ] US-003: ...

## Medium (Enhancement User Stories)
- [ ] US-004: [Enhancement feature]
  - Verify: [acceptance criteria]
- [ ] US-005: ...

## Low (Polish & Post-MVP prep)
- [ ] Dark mode / theming
- [ ] Onboarding flow
- [ ] Error states & empty states
- [ ] Performance optimization
- [ ] App store assets / metadata

## Verification Gate
After all tasks complete, verify:
- [ ] All acceptance criteria from PRD met
- [ ] All screens from §5 implemented
- [ ] Non-functional requirements from §6 checked
- [ ] Tests passing
```

Every task traces back to a specific PRD section. No orphan tasks.

---

## PHASE 2: LOOP CONFIGURATION

### Step 1: Check Ralph installation

```bash
which ralph-loop 2>/dev/null || which ralph 2>/dev/null
```

If not installed:
```bash
git clone https://github.com/frankbria/ralph-claude-code.git /tmp/ralph-claude-code
cd /tmp/ralph-claude-code && ./install.sh
```

Dependencies:
```bash
# macOS
brew install jq tmux coreutils
# Linux
sudo apt install jq tmux coreutils
```

### Step 2: Create directory structure

```bash
mkdir -p .ralph/specs .ralph/examples .ralph/logs .ralph/docs/generated
```

### Step 3: Generate .ralphrc

Detect project type from package.json / pyproject.toml / Cargo.toml / go.mod and generate:

```bash
PROJECT_NAME="$ARGUMENTS"
PROJECT_TYPE="[detected]"
MAX_CALLS_PER_HOUR=100
CLAUDE_TIMEOUT_MINUTES=15
CLAUDE_OUTPUT_FORMAT="json"
ALLOWED_TOOLS="Write,Read,Edit,Bash(git *),Bash(npm *),Bash(npx *)"
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

### Step 4: Generate PROMPT.md

```markdown
# Project: [PROJECT_NAME]

## Your Mission
You are working autonomously in a Ralph loop. Each iteration:
1. Read `.ralph/specs/PRD.md` for full requirements context
2. Read `.ralph/fix_plan.md` for the current priority list
3. Implement the HIGHEST PRIORITY unchecked item
4. Run tests after implementation
5. Update fix_plan.md (check off completed items, note any verify: criteria met)
6. Output a RALPH_STATUS block (REQUIRED)

## Project Context
[GENERATED FROM PRD §1 Overview and §4 Technical Requirements]

## Specifications
- Full PRD: `.ralph/specs/PRD.md`
- Additional specs: `.ralph/specs/*`

## Key Architecture Rules
[EXTRACTED FROM PRD §4 Architecture section]

## Build & Test Instructions
See `.ralph/AGENT.md` for how to build, test, and run the project.

## Rules
- ONE task per loop iteration (stay focused)
- Always run tests after changes
- Never skip the RALPH_STATUS block
- If blocked, set STATUS: BLOCKED and explain why
- If all tasks are done, set EXIT_SIGNAL: true
- Reference the PRD for acceptance criteria — don't guess
- When implementing a user story, check ALL its acceptance criteria

## Required Output Format

At the END of every response, output EXACTLY:

---RALPH_STATUS---
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
TASKS_COMPLETED_THIS_LOOP: <number>
FILES_MODIFIED: <number>
TESTS_STATUS: PASSING | FAILING | NOT_RUN
WORK_TYPE: IMPLEMENTATION | TESTING | DOCUMENTATION | REFACTORING
EXIT_SIGNAL: false
RECOMMENDATION: <one line summary of what was done and what's next>
---END_RALPH_STATUS---

Set EXIT_SIGNAL: true ONLY when ALL tasks in fix_plan.md are complete
AND the Verification Gate at the bottom of fix_plan.md passes.
```

### Step 5: Generate AGENT.md

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
```

### Step 6: Initialize git repo (CRITICAL for circuit breaker)

Ralph's circuit breaker detects progress via `git diff --name-only`. **If there is no git repo, `files_changed` is always 0, and the circuit breaker will false-trip after `CB_NO_PROGRESS_THRESHOLD` loops.** You MUST ensure a git repo exists with an initial commit before launching the loop.

```bash
# Add Ralph state files to .gitignore FIRST
echo -e "\n# Ralph loop state files\n.ralph/logs/\n.ralph/status.json\n.ralph/progress.json\n.ralph/.call_count\n.ralph/.last_reset\n.ralph/.exit_signals\n.ralph/.response_analysis\n.ralph/.circuit_breaker_state\n.ralph/.claude_session_id\n.ralph/.ralph_session\n.ralph/.ralph_session_history" >> .gitignore

# Initialize git if not already a repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  git init
  git add -A
  git commit -m "Initial Spidey scaffold"
fi
```

**Why this matters:** Without git, every loop reports zero file changes → circuit breaker opens after a few loops even though tasks are completing successfully.

### Step 7: Print run instructions

```
Spidey setup complete.

PRD:          .ralph/specs/PRD.md     (review and edit before running)
Task plan:    .ralph/fix_plan.md      (derived from PRD)
Loop config:  .ralphrc                (edit rate limits, timeouts)
Loop prompt:  .ralph/PROMPT.md        (edit to add project-specific rules)
Build/test:   .ralph/AGENT.md         (edit if auto-detect was wrong)

To run:
  ralph --monitor      # Recommended: loop + live dashboard in tmux
  ralph                # Loop only

To review status:
  ralph-monitor        # Dashboard in separate terminal

The loop will work through fix_plan.md top to bottom, one task per iteration,
until all items are checked off and the verification gate passes.
```

---

## How the Loop Works

### Exit Detection (Dual-Condition Gate)
Ralph only stops when BOTH:
1. `completion_indicators >= 2` (accumulated across loops)
2. Claude outputs `EXIT_SIGNAL: true` in RALPH_STATUS

### Circuit Breaker
| Trigger | Result |
|---------|--------|
| 3 loops no file changes | OPEN (halted) |
| 5 loops same error | OPEN (halted) |
| 2 loops no progress | HALF_OPEN (monitoring) |
| Progress in HALF_OPEN | CLOSED (recovered) |

### Session Continuity
- Session persists via `--continue` flag
- 24-hour expiry (configurable)
- Claude remembers what it did across iterations

### Rate Limiting
- 100 calls per 5-hour window (configurable)
- Auto-waits with countdown when limit hit

---

## Quick Reference

```bash
ralph-enable          # Interactive wizard for existing project
ralph-setup my-proj   # Create new blank project
ralph-import prd.md   # Convert existing PRD to Ralph format
ralph --monitor       # Run loop + dashboard
ralph-monitor         # Dashboard only
```

---

Now setting up Spidey for: **$ARGUMENTS**
