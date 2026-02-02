---
name: prd-analyzer
description: Analyzes PRD documents, concept briefs, or feature specs and creates structured implementation plans with visual kanban tracking. Breaks requirements into epics, stories, and tasks with dependencies and estimates. Outputs to `.claude/` folder for integration with project-harness and other skills. Generates PROJECT.md for shared project context.
---

# PRD Analyzer & Implementation Planner

Transform product requirements into actionable implementation plans with visual kanban tracking.

**Integrates with:**
- `product-manager` — Audits completeness, adds remediation tasks
- `project-harness` — Reads PROJECT.md, manages work sessions
- `api-design`, `database-design`, etc. — Assigned to specific features

## Process Overview

```
PRD/Brief → Analysis → Task Breakdown → .claude/ Output
    │           │            │              │
 Upload    Extract       Epic →         PROJECT.md
  doc      scope &      Story →         tasks.db
          features      Task            features.json
                                        kanban.html
```

## Output Location

All outputs go to `.claude/` folder in the project root:

```
.claude/
├── PROJECT.md          ← Project context (all skills read this)
├── tasks.db            ← SQLite database (source of truth)
├── features.json       ← Feature definitions with skill assignments
├── kanban.html         ← Interactive board
├── progress.md         ← Session progress tracking
└── implementation-plan.md  ← Markdown summary
```

---

## Quick Start

### 1. Analyze the Document

When given a PRD or concept brief:

```
1. Read the entire document
2. Extract: Goals, Features, Constraints, Dependencies
3. Identify scope boundaries (in/out)
4. Note technical requirements and assumptions
5. Assign skills to features based on type
```

### 2. Create Task Breakdown

Structure work hierarchically:

```
Epic (large feature area)
├── Story (user-facing capability)
│   ├── Task (implementable unit, 1-8 hours)
│   ├── Task
│   └── Task
└── Story
    └── Tasks...
```

### 3. Generate Outputs

Create all files in `.claude/`:
- `PROJECT.md` — Shared context for all skills
- `tasks.db` — SQLite database with full task structure
- `features.json` — Feature list with metadata
- `kanban.html` — Interactive board (open in browser)

---

## PROJECT.md Generation

The most important output — shared context for all skills.

### Template

```markdown
# Project: [Name]

## Overview
[1-2 sentence description from PRD]

## Status
- **Phase**: Planning | Design | Implementation | Polish | Launch
- **Created**: [Date]
- **Last Updated**: [Date]
- **Overall Progress**: 0/[N] stories complete

## Metrics
| Metric | Count |
|--------|-------|
| Epics | [N] |
| Stories | [N] |
| Estimated Hours | [N] |
| Estimated Days | [N] |

## Tech Stack
- **Frontend**: [Framework]
- **Backend**: [Framework]
- **Database**: [Database]
- **Hosting**: [Platform]

## Feature Overview

| ID | Feature | Priority | Skill | Status |
|----|---------|----------|-------|--------|
| F001 | [Name] | P0 | [skill] | planned |
| F002 | [Name] | P0 | [skill] | planned |
| ... | ... | ... | ... | ... |

## Skill Assignments

| Skill | Features | Status |
|-------|----------|--------|
| api-design | F001, F002, F003 | pending |
| database-design | F004, F005, F007 | pending |
| testing-strategy | F008, F009 | blocked by api-design |

## Current Gaps
[Updated by product-manager after audit]

## Next Actions
1. [First recommended action]
2. [Second recommended action]

## Key Files
- PRD: [path or "uploaded"]
- Tasks DB: `.claude/tasks.db`
- Kanban: `.claude/kanban.html`

## Session Log
| Date | Session | Completed | Notes |
|------|---------|-----------|-------|
| [Date] | prd-analyzer | PROJECT.md, tasks.db | Initial setup |
```

---

## Skill Assignment

Assign skills to features based on their nature.

### Skill Mapping

| Feature Type | Primary Skill | Secondary Skills |
|--------------|---------------|------------------|
| REST/GraphQL APIs | `api-design` | `api-testing` |
| Database schemas | `database-design` | — |
| SDK/library creation | `sdk-development` | — |
| Data processing pipelines | `api-design` | `database-design` |
| Authentication/Security | `api-design` | — |
| Integrations (Slack, etc.) | `api-design` | — |
| Testing infrastructure | `testing-strategy` | — |

### Assignment Rules

1. **Database before API**: Data-dependent features get `database-design` first
2. **API before Integration**: Service features get `api-design` first
3. **Audit at end**: All features get `product-manager` audit
4. **Testing last**: Critical features get `testing-strategy` review

### In features.json

```json
{
  "features": [
    {
      "id": "F001",
      "title": "Data Pipeline",
      "priority": "P0",
      "assigned_skills": ["database-design", "api-design"],
      "skill_order": ["database-design", "api-design"],
      "current_skill": null,
      "audit_level": 0,
      "stories": ["story-001-01", "story-001-02", ...]
    }
  ]
}
```

---

## Analysis Framework

### Document Parsing

Extract these elements from any PRD/brief:

| Element | What to Find | Output |
|---------|--------------|--------|
| **Vision** | Why build this? Problem solved? | 1-2 sentence summary |
| **Users** | Who uses it? Personas? | User types list |
| **Features** | What does it do? | Feature list with priority |
| **Scope** | What's included/excluded? | In/Out lists |
| **Constraints** | Tech stack, timeline, budget? | Constraint list |
| **Dependencies** | External systems, APIs, teams? | Dependency map |
| **Success Metrics** | How measured? | KPI list |
| **Risks** | What could go wrong? | Risk register |

### Scope Classification

For each feature, classify:

```
P0 - Must Have (MVP, launch blocker)
P1 - Should Have (important, not blocking)
P2 - Nice to Have (future iteration)
P3 - Out of Scope (explicitly excluded)
```

### Ambiguity Detection

Flag unclear requirements:

```markdown
## Ambiguities Identified

1. **User authentication** — SSO required? Which providers?
2. **Data export** — Format not specified (CSV? JSON? Excel?)
3. **Mobile support** — Responsive web or native apps?

Recommend: Clarify before implementation planning.
```

---

## Database Schema

### Updated Schema with Audit Fields

```sql
-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    phase TEXT DEFAULT 'planning' 
        CHECK(phase IN ('planning', 'design', 'implementation', 'polish', 'launch')),
    tech_stack TEXT,  -- JSON: {frontend, backend, database, hosting}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Epics: Large feature areas
CREATE TABLE IF NOT EXISTS epics (
    id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES projects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT CHECK(priority IN ('P0', 'P1', 'P2', 'P3')) DEFAULT 'P1',
    status TEXT CHECK(status IN ('planned', 'in_progress', 'completed', 'cancelled')) DEFAULT 'planned',
    
    -- Skill assignment
    assigned_skills TEXT,      -- JSON array: ["database-design", "api-design"]
    skill_order TEXT,          -- JSON array: order to run skills
    current_skill TEXT,        -- Currently active skill
    
    -- Audit fields (updated by product-manager)
    audit_level INTEGER DEFAULT 0 
        CHECK(audit_level BETWEEN 0 AND 5),
    audit_date TEXT,
    audit_gaps TEXT,           -- JSON array: ["no_frontend", "no_navigation"]
    
    color TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stories: User-facing capabilities
CREATE TABLE IF NOT EXISTS stories (
    id TEXT PRIMARY KEY,
    epic_id TEXT REFERENCES epics(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    user_story TEXT,
    acceptance_criteria TEXT,
    estimate_days REAL,
    status TEXT CHECK(status IN ('backlog', 'ready', 'in_progress', 'review', 'done')) DEFAULT 'backlog',
    assigned_skill TEXT,       -- Which skill handles this story
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks: Implementable units
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    story_id TEXT REFERENCES stories(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT CHECK(task_type IN ('frontend', 'backend', 'database', 'design', 'devops', 'qa', 'documentation', 'other')) DEFAULT 'other',
    estimate_hours REAL,
    status TEXT DEFAULT 'todo' 
        CHECK(status IN ('todo', 'in_progress', 'review', 'done', 'blocked')),
    assignee TEXT,
    column_id TEXT DEFAULT 'todo',
    sort_order INTEGER DEFAULT 0,
    blocked_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Dependencies between tasks
CREATE TABLE IF NOT EXISTS dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blocker_task_id TEXT REFERENCES tasks(id) ON DELETE CASCADE,
    blocked_task_id TEXT REFERENCES tasks(id) ON DELETE CASCADE,
    dependency_type TEXT CHECK(dependency_type IN ('blocks', 'related')) DEFAULT 'blocks',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(blocker_task_id, blocked_task_id)
);

-- Session log (for project-harness integration)
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    skill_used TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    stories_completed TEXT,    -- JSON array of story IDs
    notes TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_epics_priority ON epics(priority);
CREATE INDEX IF NOT EXISTS idx_epics_audit ON epics(audit_level);
CREATE INDEX IF NOT EXISTS idx_stories_epic ON stories(epic_id);
CREATE INDEX IF NOT EXISTS idx_stories_status ON stories(status);
CREATE INDEX IF NOT EXISTS idx_tasks_story ON tasks(story_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);

-- Useful views
CREATE VIEW IF NOT EXISTS v_epic_progress AS
SELECT 
    e.id,
    e.title,
    e.priority,
    e.audit_level,
    e.assigned_skills,
    COUNT(s.id) as total_stories,
    SUM(CASE WHEN s.status = 'done' THEN 1 ELSE 0 END) as done_stories,
    ROUND(100.0 * SUM(CASE WHEN s.status = 'done' THEN 1 ELSE 0 END) / COUNT(s.id), 1) as progress_pct
FROM epics e
LEFT JOIN stories s ON s.epic_id = e.id
GROUP BY e.id;

CREATE VIEW IF NOT EXISTS v_skill_workload AS
SELECT 
    e.assigned_skills,
    COUNT(DISTINCT e.id) as epic_count,
    COUNT(s.id) as story_count,
    SUM(CASE WHEN s.status != 'done' THEN 1 ELSE 0 END) as pending_stories
FROM epics e
LEFT JOIN stories s ON s.epic_id = e.id
GROUP BY e.assigned_skills;
```

---

## Task Breakdown Methodology

### Epic Definition

Epics are large feature areas (1-4 weeks of work):

```markdown
## Epic: User Authentication

**ID**: epic-001 (or F001)
**Priority**: P0
**Assigned Skills**: ["database-design", "api-design", "testing-strategy"]
**Skill Order**: database-design → api-design → testing-strategy

**Goal**: Users can create accounts and log in securely
**Scope**: Email/password, OAuth (Google, GitHub), password reset
**Out of Scope**: SSO, 2FA (P2)
**Dependencies**: Email service, OAuth provider setup
**Estimate**: 2 weeks
```

### Story Definition

Stories are user-facing capabilities (1-5 days):

```markdown
### Story: Email/Password Registration

**ID**: story-001-01
**Epic**: epic-001
**Assigned Skill**: api-design (backend-heavy story)

**As a** new user
**I want to** create an account with email and password
**So that** I can access the application

**Acceptance Criteria**:
- [ ] Email validation (format, uniqueness)
- [ ] Password requirements (8+ chars, complexity)
- [ ] Email verification flow
- [ ] Error handling for duplicates

**Estimate**: 3 days
```

### Task Definition

Tasks are implementable units (1-8 hours):

```markdown
#### Task: Create registration form component

**ID**: task-001-01-01
**Story**: story-001-01
**Type**: Frontend
**Estimate**: 4h

**Description**: 
- Email input with validation
- Password input with strength indicator
- Confirm password field
- Submit button with loading state

**Acceptance**: Form validates and submits to API
**Blocked By**: None
**Blocks**: Registration API integration
```

---

## Workflow

### Step-by-Step Process

1. **Receive PRD/Brief**
   - Read full document
   - Ask clarifying questions if critical gaps

2. **Create Analysis Summary**
   - Vision, users, features, constraints
   - Scope classification (P0-P3)
   - Flag ambiguities
   - Assign skills to features

3. **Break Down Tasks**
   - Define epics from major features
   - Break epics into stories
   - Break stories into tasks (≤8h each)
   - Map dependencies

4. **Generate Outputs to `.claude/`**
   - Create PROJECT.md (shared context)
   - Create SQLite database (tasks.db)
   - Generate features.json
   - Generate kanban HTML
   - Write implementation plan markdown
   - Create progress.md template

5. **Deliver Files**
   - All files in `.claude/` folder
   - Present kanban.html for interactive use
   - Explain next steps (which skill to run first)

---

## features.json Format

```json
{
  "project": {
    "name": "VoiceForm AI",
    "description": "AI-powered voice survey platform",
    "created_at": "2026-01-10T10:00:00Z"
  },
  "summary": {
    "total_epics": 30,
    "total_stories": 150,
    "total_hours": 1972,
    "by_priority": {
      "P0": 5,
      "P1": 12,
      "P2": 10,
      "P3": 3
    }
  },
  "features": [
    {
      "id": "F001",
      "epic_id": "epic-001",
      "title": "Data Pipeline",
      "description": "Process and store data with efficient schemas",
      "priority": "P0",
      "assigned_skills": ["database-design", "api-design"],
      "skill_order": ["database-design", "api-design"],
      "dependencies": [],
      "audit_level": 0,
      "stories": ["story-001-01", "story-001-02", "story-001-03", "story-001-04", "story-001-05"]
    },
    {
      "id": "F002",
      "epic_id": "epic-002",
      "title": "RAG Pipeline",
      "description": "Document processing and semantic search",
      "priority": "P0",
      "assigned_skills": ["api-design"],
      "skill_order": ["api-design"],
      "dependencies": ["F001"],
      "audit_level": 0,
      "stories": ["story-002-01", "story-002-02", "story-002-03", "story-002-04", "story-002-05"]
    }
  ],
  "skill_summary": {
    "database-design": ["F001", "F003", "F011"],
    "api-design": ["F002", "F007", "F008"],
    "testing-strategy": ["F001", "F003", "F011"],
    "sdk-development": ["F005", "F006"]
  }
}
```

---

## Integration Points

### With product-manager

After implementation, product-manager:
1. Reads `tasks.db` and `features.json`
2. Scans codebase for implementation evidence
3. Updates `audit_level` and `audit_gaps` in epics table
4. Adds remediation tasks to `tasks.db`
5. Updates `PROJECT.md` with current gaps

### With project-harness

Project-harness:
1. Reads `PROJECT.md` for context
2. Checks `tasks.db` for next work
3. Logs sessions to `sessions` table
4. Updates `progress.md` after each session

### With Implementation Skills

Skills like `api-design`, `database-design`:
1. Read `PROJECT.md` for context
2. Check `features.json` for assigned work
3. Filter by `assigned_skills` containing their name
4. Update story status when complete

---

## Anti-Patterns

### Analysis Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Accepting vague requirements | Builds wrong thing | Flag ambiguities, ask questions |
| Scope creep in breakdown | Adds unspecified work | Stick to documented requirements |
| Ignoring constraints | Infeasible plan | Check tech stack, timeline, budget |
| Missing dependencies | Blocked work | Map all external dependencies |
| No skill assignment | Work not routed | Assign skills to every feature |

### Task Breakdown Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Tasks > 8 hours | Too vague to estimate | Split into smaller tasks |
| No acceptance criteria | Unclear "done" | Define measurable criteria |
| Missing task types | Can't assign properly | Tag: frontend, backend, design, etc. |
| Circular dependencies | Deadlock | Identify and break cycles |
| Everything P0 | No prioritization | Force-rank priorities |

### Output Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Output to random location | Skills can't find | Always use `.claude/` |
| No PROJECT.md | No shared context | Always generate PROJECT.md |
| No skill assignments | Manual routing needed | Assign skills during analysis |
| Missing features.json | No machine-readable list | Always generate features.json |

---

## Checklist: Complete PRD Analysis

### Before Starting
- [ ] Full PRD/brief received
- [ ] Clarifying questions asked (if needed)
- [ ] Tech stack identified
- [ ] `.claude/` folder created

### During Analysis
- [ ] All features extracted
- [ ] Priorities assigned (P0-P3)
- [ ] Skills assigned to features
- [ ] Ambiguities documented

### Task Breakdown
- [ ] Epics created (1 per feature)
- [ ] Stories created (achievable chunks)
- [ ] Tasks created (≤8h each)
- [ ] Dependencies mapped

### Output Generation
- [ ] PROJECT.md created
- [ ] tasks.db created with full schema
- [ ] features.json created
- [ ] kanban.html generated
- [ ] progress.md template created
- [ ] implementation-plan.md written

### Handoff
- [ ] Next steps explained
- [ ] First skill to run identified
- [ ] Files presented to user

---

## References

- [references/prd-analysis.md](references/prd-analysis.md) — Deep dive on document analysis
- [references/task-breakdown.md](references/task-breakdown.md) — Detailed breakdown methodology
- [references/kanban-setup.md](references/kanban-setup.md) — Database schema and HTML generation
- [references/skill-routing.md](references/skill-routing.md) — Skill assignment logic
- [templates/kanban.html](templates/kanban.html) — Kanban board template
