---
name: auto-claude-spec
description: Auto-Claude spec creation and management. Use when creating feature specs, understanding spec pipeline phases, modifying requirements, or managing spec lifecycle.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude Spec Creation

Master the spec creation pipeline for autonomous builds.

## Overview

Specs are the foundation of Auto-Claude builds. They define:
- What needs to be built
- Acceptance criteria
- Context from existing codebase
- Implementation plan

## Spec Pipeline Phases

### Dynamic Phase Selection

Auto-Claude automatically selects phases based on task complexity:

| Complexity | Phases | Description |
|------------|--------|-------------|
| **SIMPLE** | 3 | Discovery → Quick Spec → Validate |
| **STANDARD** | 6-7 | Discovery → Requirements → [Research] → Context → Spec → Plan → Validate |
| **COMPLEX** | 8 | Full pipeline with Research and Self-Critique phases |

### Phase Breakdown

#### 1. Discovery Phase
- Gathers user requirements interactively
- Asks clarifying questions
- Identifies scope and constraints

#### 2. Requirements Phase
- Structures requirements into JSON format
- Defines acceptance criteria
- Lists technical constraints

#### 3. Research Phase (Standard/Complex)
- Validates external integrations
- Checks API compatibility
- Researches best practices

#### 4. Context Phase
- Analyzes existing codebase
- Identifies relevant files
- Maps dependencies

#### 5. Spec Writing Phase
- Creates detailed spec.md
- Documents technical approach
- Lists affected components

#### 6. Planning Phase
- Creates implementation plan
- Breaks work into subtasks
- Defines phase dependencies

#### 7. Critique Phase (Complex only)
- Self-review using ultrathink
- Identifies potential issues
- Suggests improvements

#### 8. Validation Phase
- Validates all artifacts
- Checks completeness
- Prepares for build

## Creating Specs

### Interactive Mode (Recommended)

```bash
cd apps/backend
python spec_runner.py --interactive
```

The system will:
1. Ask about your feature/task
2. Clarify requirements
3. Analyze your codebase
4. Generate complete spec

### From Task Description

```bash
# Quick spec creation
python spec_runner.py --task "Add dark mode toggle to settings page"

# With forced complexity
python spec_runner.py --task "Add payment integration" --complexity complex
```

### Continue Interrupted Spec

```bash
# Resume from where it stopped
python spec_runner.py --continue 001-feature-name
```

## Spec Structure

### Directory Layout

```
.auto-claude/specs/001-feature-name/
├── spec.md                    # Main specification document
├── requirements.json          # Structured requirements
├── context.json               # Codebase context
├── implementation_plan.json   # Subtask-based plan
├── discovery.json             # Initial discovery data
├── research.json              # Research findings (if applicable)
└── validation_report.json     # Validation results
```

### spec.md Format

```markdown
# Feature: [Feature Name]

## Overview
[Description of what this feature does]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Approach
[How the feature will be implemented]

## Affected Components
- Component 1: [changes]
- Component 2: [changes]

## Dependencies
- [External dependencies if any]

## Testing Strategy
[How to verify the feature works]
```

### requirements.json Format

```json
{
  "title": "Feature Title",
  "description": "Detailed description",
  "acceptance_criteria": [
    "User can do X",
    "System responds with Y"
  ],
  "constraints": [
    "Must work on mobile",
    "Must be accessible"
  ],
  "priority": "high",
  "complexity": "standard"
}
```

### implementation_plan.json Format

```json
{
  "spec_id": "001-feature-name",
  "subtasks": [
    {
      "id": 1,
      "title": "Create data model",
      "description": "Add User schema to database",
      "status": "pending",
      "dependencies": [],
      "files": ["src/models/user.ts"]
    },
    {
      "id": 2,
      "title": "Implement API endpoint",
      "description": "Create /api/users route",
      "status": "pending",
      "dependencies": [1],
      "files": ["src/routes/users.ts"]
    }
  ],
  "total_subtasks": 2,
  "completed": 0
}
```

## Best Practices

### Writing Good Requirements

**Good:**
```
"Add user authentication using Google OAuth with:
- Login button in header
- Protected routes for /dashboard/*
- User profile stored in database
- Session management with cookies"
```

**Bad:**
```
"Add login feature"
```

### Complexity Selection

| Choose | When |
|--------|------|
| **Simple** | 1-2 files, UI tweaks, text changes, simple bug fixes |
| **Standard** | 3-10 files, new features, component additions |
| **Complex** | 10+ files, external integrations, architectural changes |

### Spec Review Tips

Before running build:

1. **Check acceptance criteria** - Are they testable?
2. **Review affected components** - Are all files identified?
3. **Validate dependencies** - Are external services available?
4. **Confirm scope** - Is the scope appropriate?

## Managing Specs

### List All Specs

```bash
python run.py --list
```

Output:
```
Specs:
  001-user-auth [COMPLETE] - User authentication
  002-dark-mode [BUILDING] - Dark mode toggle
  003-search [PENDING] - Search functionality
```

### View Spec Status

```bash
# Check spec details
cat .auto-claude/specs/001-feature/spec.md

# Check implementation progress
cat .auto-claude/specs/001-feature/implementation_plan.json
```

### Modify Spec

Edit the spec.md file directly:

```bash
# Edit spec
nano .auto-claude/specs/001-feature/spec.md

# Re-validate
python validate_spec.py --spec-dir .auto-claude/specs/001-feature --checkpoint all
```

### Delete Spec

```bash
# Remove spec directory
rm -rf .auto-claude/specs/001-feature

# Or discard via CLI (includes worktree cleanup)
python run.py --spec 001 --discard
```

## Advanced Usage

### Custom Prompts

Modify prompts in `apps/backend/prompts/`:
- `spec_gatherer.md` - Discovery phase
- `spec_researcher.md` - Research phase
- `spec_writer.md` - Spec writing
- `spec_critic.md` - Self-critique
- `spec_quick.md` - Simple spec creation

### Batch Spec Creation

```bash
# Create specs from a file
while IFS= read -r task; do
  python spec_runner.py --task "$task" --complexity standard
done < tasks.txt
```

### Spec Templates

Create custom templates in `apps/backend/templates/` (if needed):

```bash
mkdir -p templates
cat > templates/api-feature.md << 'EOF'
# API Feature: {{name}}

## Endpoints
- GET /api/{{resource}}
- POST /api/{{resource}}

## Data Model
[Define schema]

## Authentication
[Required auth level]
EOF
```

## Troubleshooting

### Spec Creation Fails

```bash
# Enable debug mode
DEBUG=true python spec_runner.py --interactive

# Check logs
cat .auto-claude/logs/spec_runner.log
```

### Invalid Requirements

```bash
# Validate spec structure
python validate_spec.py --spec-dir .auto-claude/specs/001-feature --checkpoint requirements
```

### Context Discovery Issues

```bash
# Re-run context analysis
python spec_runner.py --continue 001-feature

# Or manually trigger context phase
# (Edit implementation_plan.json to reset context phase)
```

## Related Skills

- **auto-claude-cli**: CLI command reference
- **auto-claude-build**: Running builds
- **auto-claude-workspace**: Workspace management
