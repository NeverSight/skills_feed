---
name: initializer-agent
description: First-session agent for autonomous coding projects. Use when starting a new autonomous project, generating feature lists, setting up environments, or scaffolding project structure.
version: 1.0.0
category: autonomous-coding
layer: core-workflow
---

# Initializer Agent

First-session agent that sets up the foundation for autonomous coding projects.

## Quick Start

### Initialize a Project
```python
from scripts.initializer import InitializerAgent

agent = InitializerAgent(project_dir)
result = await agent.initialize_project(
    spec="Build a task management app with user auth",
    tech_stack=["nextjs", "typescript", "prisma"]
)
```

### Generate Feature List
```python
from scripts.feature_generator import generate_features

features = await generate_features(
    spec="E-commerce platform with cart and checkout",
    count=100  # Generate 100 features
)
```

## Initialization Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                  INITIALIZER WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. READ PROJECT SPECIFICATION                               │
│     ├─ Parse requirements                                   │
│     ├─ Identify technology stack                            │
│     └─ Determine project structure                          │
│                                                              │
│  2. GENERATE FEATURE LIST                                   │
│     ├─ Create 100-200 features                              │
│     ├─ Categorize (functional, UI, API, etc.)              │
│     ├─ Add verification steps                               │
│     └─ Set initial priority                                 │
│                                                              │
│  3. CREATE ENVIRONMENT SCRIPT                               │
│     ├─ Dependency installation                              │
│     ├─ Database setup                                       │
│     ├─ Environment variables                                │
│     └─ Development server                                   │
│                                                              │
│  4. SCAFFOLD PROJECT                                        │
│     ├─ Create directory structure                           │
│     ├─ Initialize package.json/pyproject.toml              │
│     ├─ Create base configuration                            │
│     └─ Set up testing framework                             │
│                                                              │
│  5. MAKE INITIAL COMMIT                                     │
│     ├─ git init                                             │
│     ├─ Add all files                                        │
│     └─ Commit: "Initial project setup"                      │
│                                                              │
│  6. SAVE STATE                                              │
│     ├─ Write feature_list.json                              │
│     ├─ Write init.sh                                        │
│     └─ Create claude-progress.txt                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Output Artifacts

### feature_list.json
```json
[
  {
    "id": "auth-001",
    "category": "functional",
    "description": "User can sign up with email and password",
    "steps": [
      "Navigate to signup page",
      "Enter email address",
      "Enter password (min 8 chars)",
      "Click submit",
      "Verify account created"
    ],
    "passes": false,
    "priority": 1
  }
]
```

### init.sh
```bash
#!/bin/bash
set -e

# Install dependencies
npm install

# Set up database
npx prisma migrate dev

# Start development server
npm run dev &
```

### claude-progress.txt
```markdown
# Session Progress

## Session 1 - 2025-01-15 10:00

### Accomplishments
- Analyzed project specification
- Generated 150 feature requirements
- Created project structure
- Set up development environment

### Next Steps
- Begin implementing auth-001: User signup
```

## Feature Categories

| Category | Description | Example |
|----------|-------------|---------|
| `functional` | Core functionality | User login, CRUD operations |
| `ui` | User interface | Forms, modals, navigation |
| `api` | API endpoints | REST routes, GraphQL |
| `database` | Data layer | Models, migrations |
| `integration` | External services | OAuth, payments |
| `performance` | Speed/efficiency | Caching, optimization |
| `security` | Protection | Input validation, auth |
| `accessibility` | A11y compliance | WCAG, ARIA |
| `testing` | Test coverage | Unit, integration, E2E |

## Integration Points

- **autonomous-session-manager**: Detects INIT session type
- **context-state-tracker**: Creates initial state artifacts
- **coding-agent**: Picks up from initializer output

## References

- `references/INITIALIZER-WORKFLOW.md` - Detailed workflow
- `references/FEATURE-CATEGORIES.md` - Category guidelines

## Templates

- `templates/init.sh.template` - Environment setup
- `templates/feature_list.json.template` - Feature structure
- `templates/progress.txt.template` - Progress file

## Scripts

- `scripts/initializer.py` - Main InitializerAgent
- `scripts/feature_generator.py` - Feature list generation
- `scripts/environment_setup.py` - Init script creation
- `scripts/project_scaffold.py` - Project scaffolding
