---
name: roadmap
description: "Creates and manages project roadmaps with milestones and PRD queues. Use after architecture is defined for project planning. Triggers on: create roadmap, plan milestones, organize prds."
---

# Roadmap Skill

Plan project execution by creating milestones and organizing PRDs into an executable queue.

## Workspace Mode Note

When running in workspace mode, all paths are relative to `.aha-loop/` directory:
- Vision analysis: `.aha-loop/project.vision-analysis.md`
- Architecture: `.aha-loop/project.architecture.md`
- Roadmap: `.aha-loop/project.roadmap.json`
- PRD files: `.aha-loop/tasks/`

The orchestrator will provide the actual paths in the prompt context.

---

## The Job

1. Read `project.vision-analysis.md` and `project.architecture.md`
2. Decompose project into milestones
3. Break each milestone into PRDs
4. Order PRDs by dependencies
5. Output `project.roadmap.json`
6. Generate initial PRD files in `tasks/`

---

## Milestone Strategy

### Standard Milestone Structure

| Milestone | Focus | Goal |
|-----------|-------|------|
| **M0: Foundation** | Project scaffolding, CI/CD, tooling | Development environment ready |
| **M1: MVP** | Core features only | Minimal usable product |
| **M2: Essential** | Important features | Feature-complete for basic use |
| **M3: Enhanced** | Nice-to-have features | Polished product |
| **M4: Optimization** | Performance, UX polish | Production-ready |

### Milestone Sizing

Each milestone should:
- Be completable in a reasonable timeframe
- Have 3-7 PRDs (avoid too many or too few)
- Deliver tangible, testable value
- Build on previous milestones

---

## PRD Decomposition

### From Features to PRDs

For each milestone, break down features into PRDs:

```
Milestone: M1 - MVP
├── PRD-001: Project Scaffolding
├── PRD-002: Database Schema
├── PRD-003: Core Data Models
├── PRD-004: Basic API Endpoints
└── PRD-005: Minimal UI
```

### PRD Sizing

Each PRD should:
- Take 1-5 Aha Loop iterations (5-25 stories)
- Focus on one coherent feature area
- Be independently testable
- Not depend on unfinished PRDs

### PRD Ordering

Order PRDs by dependencies:

1. **Infrastructure first** - Project setup, database, auth
2. **Backend before frontend** - APIs before UI that uses them
3. **Core before optional** - Must-have before nice-to-have
4. **Data before presentation** - Models before views

---

## Roadmap JSON Structure

```json
{
  "version": 1,
  "projectName": "[From vision]",
  "status": "in_progress",
  "currentMilestone": "M1",
  "currentPRD": "PRD-002",
  "createdAt": "[timestamp]",
  "updatedAt": "[timestamp]",
  "milestones": [
    {
      "id": "M0",
      "title": "Foundation",
      "description": "Project setup and development environment",
      "status": "completed",
      "completedAt": "[timestamp]",
      "prds": [
        {
          "id": "PRD-001",
          "title": "Project Scaffolding",
          "description": "Initialize project structure, dependencies, and tooling",
          "status": "completed",
          "prdFile": "tasks/prd-scaffolding.md",
          "stories": 5,
          "completedAt": "[timestamp]"
        }
      ]
    },
    {
      "id": "M1",
      "title": "MVP",
      "description": "Minimum viable product with core functionality",
      "status": "in_progress",
      "prds": [
        {
          "id": "PRD-002",
          "title": "Database Schema",
          "description": "Design and implement database schema",
          "status": "in_progress",
          "prdFile": "tasks/prd-database.md",
          "stories": 8,
          "dependsOn": ["PRD-001"]
        },
        {
          "id": "PRD-003",
          "title": "Core API",
          "description": "Implement core API endpoints",
          "status": "pending",
          "prdFile": "tasks/prd-core-api.md",
          "stories": 12,
          "dependsOn": ["PRD-002"]
        }
      ]
    },
    {
      "id": "M2",
      "title": "Essential Features",
      "description": "Complete essential features for basic use",
      "status": "pending",
      "prds": []
    }
  ],
  "changelog": [
    {
      "timestamp": "[timestamp]",
      "action": "created",
      "description": "Initial roadmap created from vision and architecture"
    }
  ]
}
```

---

## Roadmap Creation Process

### Step 1: Analyze Requirements

From vision analysis, categorize features:

```markdown
## Feature Categories

### M1: MVP (Must ship)
- [Feature 1]
- [Feature 2]

### M2: Essential (Should ship)
- [Feature 3]
- [Feature 4]

### M3: Enhanced (Nice to ship)
- [Feature 5]
```

### Step 2: Create M0 Foundation

Every project starts with M0:

```markdown
## M0: Foundation PRDs

### PRD-001: Project Scaffolding
- Initialize project with chosen tech stack
- Set up directory structure
- Configure linting and formatting
- Set up basic CI (if applicable)
- Create initial README

### PRD-002: Development Environment
- Database setup (if applicable)
- Environment configuration
- Development scripts
- Basic testing infrastructure
```

### Step 3: Decompose Milestones into PRDs

For each milestone after M0:

1. List all features for this milestone
2. Group related features
3. Order by dependencies
4. Create PRD for each group
5. Estimate stories per PRD

### Step 4: Generate PRD Files

For each PRD, create a stub file in `tasks/`:

```markdown
# PRD: [Title]

**ID:** PRD-XXX
**Milestone:** M[N]
**Status:** Pending

## Overview

[Brief description from roadmap]

## Context

[How this relates to previous PRDs and the overall project]

## Goals

- [Goal 1]
- [Goal 2]

## User Stories

[To be generated when this PRD becomes active]

## Dependencies

- PRD-XXX: [What it depends on]

## Acceptance Criteria

- [ ] [High-level criterion]
- [ ] [Another criterion]

---

*This PRD will be fully expanded when it becomes the active PRD.*
```

---

## Dynamic Roadmap Updates

### When to Update Roadmap

The roadmap should be updated when:

1. **PRD Completed** - Mark as complete, update timestamps
2. **New Requirement Discovered** - Add new PRD
3. **Scope Change** - Modify or remove PRDs
4. **Better Approach Found** - Restructure PRDs
5. **Milestone Complete** - Update status, move to next

### Update Process

```json
{
  "changelog": [
    {
      "timestamp": "2026-01-29T12:00:00Z",
      "action": "prd_completed",
      "prdId": "PRD-002",
      "description": "Database schema implemented"
    },
    {
      "timestamp": "2026-01-29T14:00:00Z",
      "action": "prd_added",
      "prdId": "PRD-007",
      "description": "Added caching layer PRD based on performance research"
    }
  ]
}
```

### Automatic Triggers

The orchestrator should trigger roadmap review:

- After each PRD completion
- After each milestone completion
- When significant learnings are recorded
- When errors repeatedly occur

---

## Integration with Orchestrator

### Orchestrator Reads

```bash
# Get current PRD
jq '.currentPRD' project.roadmap.json

# Get PRD file path
jq -r '.milestones[].prds[] | select(.id == "PRD-002") | .prdFile' project.roadmap.json
```

### Orchestrator Updates

After PRD completion:

```bash
# Update PRD status
jq '.milestones[].prds[] |= if .id == "PRD-002" then .status = "completed" else . end' project.roadmap.json
```

---

## PRD Queue Management

### Getting Next PRD

```python
# Pseudocode for finding next PRD
def get_next_prd(roadmap):
    for milestone in roadmap.milestones:
        if milestone.status == "completed":
            continue
        for prd in milestone.prds:
            if prd.status == "pending":
                if all_dependencies_complete(prd):
                    return prd
    return None  # All complete or blocked
```

### Handling Blocked PRDs

If a PRD's dependencies aren't met:
1. Skip to next available PRD
2. If no PRDs available, report blocking issue
3. Consider if dependencies need reprioritization

---

## Example Roadmap

**Project:** Personal Finance Tracker (from vision example)

```json
{
  "version": 1,
  "projectName": "Finance Tracker",
  "status": "in_progress",
  "currentMilestone": "M0",
  "currentPRD": "PRD-001",
  "milestones": [
    {
      "id": "M0",
      "title": "Foundation",
      "status": "in_progress",
      "prds": [
        {
          "id": "PRD-001",
          "title": "SvelteKit Project Setup",
          "description": "Initialize SvelteKit project with TypeScript, Tailwind, PWA support",
          "status": "in_progress",
          "prdFile": "tasks/prd-project-setup.md",
          "stories": 6
        }
      ]
    },
    {
      "id": "M1",
      "title": "MVP - Core Expense Tracking",
      "status": "pending",
      "prds": [
        {
          "id": "PRD-002",
          "title": "Data Layer",
          "description": "Implement IndexedDB with Dexie for expense storage",
          "status": "pending",
          "prdFile": "tasks/prd-data-layer.md",
          "stories": 8,
          "dependsOn": ["PRD-001"]
        },
        {
          "id": "PRD-003",
          "title": "Quick Expense Entry",
          "description": "Fast expense input form (< 5 seconds goal)",
          "status": "pending",
          "prdFile": "tasks/prd-expense-entry.md",
          "stories": 10,
          "dependsOn": ["PRD-002"]
        },
        {
          "id": "PRD-004",
          "title": "Expense List View",
          "description": "View and manage recorded expenses",
          "status": "pending",
          "prdFile": "tasks/prd-expense-list.md",
          "stories": 8,
          "dependsOn": ["PRD-002"]
        }
      ]
    },
    {
      "id": "M2",
      "title": "Reports & PWA",
      "status": "pending",
      "prds": [
        {
          "id": "PRD-005",
          "title": "Monthly Reports",
          "description": "Auto-generated monthly expense reports",
          "status": "pending",
          "prdFile": "tasks/prd-reports.md",
          "stories": 10,
          "dependsOn": ["PRD-003", "PRD-004"]
        },
        {
          "id": "PRD-006",
          "title": "PWA Offline Support",
          "description": "Full offline capability with service worker",
          "status": "pending",
          "prdFile": "tasks/prd-pwa.md",
          "stories": 8,
          "dependsOn": ["PRD-002"]
        }
      ]
    }
  ]
}
```

---

## Checklist

Before completing roadmap:

- [ ] All milestones defined with clear goals
- [ ] PRDs created for at least M0 and M1
- [ ] Dependencies between PRDs mapped
- [ ] PRD stub files created in tasks/
- [ ] Roadmap JSON validates
- [ ] Current milestone and PRD set correctly
- [ ] Changelog initialized
- [ ] Saved to `project.roadmap.json`
