---
name: auto-claude-cli
description: Auto-Claude CLI command reference and usage patterns. Use when running specs, managing builds, checking status, or using CLI commands for autonomous coding tasks.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude CLI

Complete command-line interface reference for Auto-Claude autonomous coding framework.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python spec_runner.py --interactive` | Create spec interactively |
| `python spec_runner.py --task "..."` | Create spec from description |
| `python run.py --spec 001` | Run autonomous build |
| `python run.py --list` | List all specs |
| `python run.py --spec 001 --review` | Review changes |
| `python run.py --spec 001 --merge` | Merge to project |

## Setup

All CLI commands run from `apps/backend/`:

```bash
cd Auto-Claude/apps/backend

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

## Core Commands

### Creating Specs

```bash
# Interactive spec creation (recommended for complex tasks)
python spec_runner.py --interactive

# Quick spec from task description
python spec_runner.py --task "Add user authentication with OAuth"

# Force complexity level
python spec_runner.py --task "Fix button color" --complexity simple
python spec_runner.py --task "Add dark mode" --complexity standard
python spec_runner.py --task "Implement payment system" --complexity complex

# Continue an interrupted spec creation
python spec_runner.py --continue 001-feature-name
```

### Complexity Tiers

| Tier | Phases | When Used |
|------|--------|-----------|
| **SIMPLE** | 3 | 1-2 files, single service, no integrations (UI fixes, text changes) |
| **STANDARD** | 6-7 | 3-10 files, 1-2 services, minimal integrations (features, bug fixes) |
| **COMPLEX** | 8 | 10+ files, multiple services, external integrations |

### Running Builds

```bash
# List all specs and their status
python run.py --list

# Run a specific spec (by number or full name)
python run.py --spec 001
python run.py --spec 001-feature-name

# Limit iterations for testing
python run.py --spec 001 --max-iterations 5

# Skip automatic QA
python run.py --spec 001 --skip-qa
```

### QA Validation

```bash
# Run QA validation manually
python run.py --spec 001 --qa

# Check QA status
python run.py --spec 001 --qa-status
```

The QA loop:
1. **QA Reviewer** checks acceptance criteria
2. If issues found → creates `QA_FIX_REQUEST.md`
3. **QA Fixer** applies fixes
4. Loop repeats until approved (up to 50 iterations)

### Workspace Management

```bash
# Test the feature in isolated workspace
cd .worktrees/auto-claude/{spec-name}/
npm run dev  # or your project's run command

# Return to backend for management commands
cd apps/backend

# See what was changed
python run.py --spec 001 --review

# Merge changes into your project
python run.py --spec 001 --merge

# Discard if you don't like it
python run.py --spec 001 --discard
```

### Spec Validation

```bash
# Validate a spec against all checkpoints
python validate_spec.py --spec-dir specs/001-feature --checkpoint all

# Validate specific checkpoint
python validate_spec.py --spec-dir specs/001-feature --checkpoint requirements
```

## Interactive Controls

### During Build

```bash
# Pause and add instructions (press once)
Ctrl+C

# Exit immediately (press twice)
Ctrl+C Ctrl+C
```

### File-Based Control

```bash
# Pause after current session
touch specs/001-name/PAUSE

# Add human instructions
echo "Focus on fixing the login bug first" > specs/001-name/HUMAN_INPUT.md

# Remove pause to continue
rm specs/001-name/PAUSE
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | - | OAuth token from `claude setup-token` |
| `AUTO_BUILD_MODEL` | No | claude-opus-4-5-20251101 | Model override |
| `DEFAULT_BRANCH` | No | auto-detect | Base branch for worktrees |
| `DEBUG` | No | false | Enable debug logging |
| `DEBUG_LEVEL` | No | 1 | Debug verbosity (1-3) |
| `GRAPHITI_ENABLED` | No | true | Enable memory system |
| `LINEAR_API_KEY` | No | - | Linear integration |

## Command Options

### spec_runner.py

| Option | Description |
|--------|-------------|
| `--interactive` | Interactive spec creation mode |
| `--task "..."` | Create spec from task description |
| `--complexity LEVEL` | Force complexity (simple/standard/complex) |
| `--continue SPEC` | Continue interrupted spec creation |

### run.py

| Option | Description |
|--------|-------------|
| `--spec SPEC` | Run or manage specific spec |
| `--list` | List all specs with status |
| `--review` | Show changes in worktree |
| `--merge` | Merge changes to project |
| `--discard` | Delete build (with confirmation) |
| `--qa` | Run QA validation |
| `--qa-status` | Check QA status |
| `--skip-qa` | Skip automatic QA |
| `--max-iterations N` | Limit build iterations |

## Workflow Examples

### Complete Feature Development

```bash
# 1. Create spec
python spec_runner.py --task "Add user profile page with avatar upload"

# 2. Run build (finds latest spec automatically)
python run.py --spec 001

# 3. Review changes in isolated workspace
python run.py --spec 001 --review

# 4. Test in worktree
cd .worktrees/auto-claude/001-user-profile/
npm run dev

# 5. Merge to project
cd ../../../apps/backend
python run.py --spec 001 --merge
```

### Quick Bug Fix

```bash
# Simple fix with minimal phases
python spec_runner.py --task "Fix login button alignment" --complexity simple

# Run and merge
python run.py --spec 002
python run.py --spec 002 --merge
```

### Batch Processing

```bash
# Create multiple specs
python spec_runner.py --task "Add search functionality"
python spec_runner.py --task "Add filters to search"
python spec_runner.py --task "Add search history"

# Run them in sequence
python run.py --spec 001
python run.py --spec 002
python run.py --spec 003
```

## Spec Directory Structure

Each spec creates a directory in `.auto-claude/specs/XXX-name/`:

```
001-feature-name/
├── spec.md                    # Feature specification
├── requirements.json          # Structured requirements
├── context.json               # Discovered codebase context
├── implementation_plan.json   # Subtask-based plan
├── qa_report.md              # QA validation results
├── QA_FIX_REQUEST.md         # Issues to fix (if rejected)
├── PAUSE                      # Pause file (if present)
└── HUMAN_INPUT.md            # Human instructions
```

## Tips for Effective Use

### Writing Good Task Descriptions

```bash
# Good: Specific and actionable
python spec_runner.py --task "Add user authentication with Google OAuth, including login button on header and protected routes for /dashboard/*"

# Bad: Vague
python spec_runner.py --task "Add login"
```

### Choosing Complexity

- **Simple**: Single file changes, UI tweaks, text updates
- **Standard**: Most features, bug fixes, component additions
- **Complex**: Multi-service changes, external integrations, architectural changes

### Debugging Failed Builds

```bash
# Enable verbose logging
DEBUG=true DEBUG_LEVEL=3 python run.py --spec 001

# Check spec status
python run.py --list

# Review QA report
cat .auto-claude/specs/001-feature/qa_report.md
```

## Related Skills

- **auto-claude-spec**: Detailed spec creation workflow
- **auto-claude-build**: Build process deep dive
- **auto-claude-workspace**: Workspace management
- **auto-claude-troubleshooting**: Debugging issues
