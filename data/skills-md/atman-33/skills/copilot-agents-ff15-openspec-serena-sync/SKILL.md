---
name: copilot-agents-ff15-openspec-serena-sync
description: Sync GitHub Copilot agents for FF15-inspired OpenSpec workflow. Team includes Noctis (orchestrator + OpenSpec creator), Iris (issue management), Gladiolus (implementation), Prompto (code quality), Ignis (documentation), and Lunafreya (PR creation). Supports multiple OpenSpec workflows (new, continue, ff, explore, verify).
---

# FF15 Copilot Agents - OpenSpec + Serena Edition

Manages GitHub Copilot agent definitions and prompts based on Final Fantasy XV team dynamics, optimized for OpenSpec workflow with Serena MCP tools.

## Quick Start

Sync all agents, prompts, and docs to a project:

```bash
python skills/copilot-agents-ff15-openspec-serena-sync/scripts/sync_agents.py --target /path/to/project
```

## The FF15 Team (OpenSpec Edition)

| Agent | Role | Specialization |
|-------|------|----------------|
| **Noctis** | **Orchestrator + Spec Creator** | **OpenSpec creation, workflow coordination, user collaboration** |
| **Iris** | **Issue Management** | **GitHub Issue creation and management based on requirements** |
| Gladiolus | Implementation | Code writing, feature building based on OpenSpec, executes to completion |
| Prompto | Code Quality | OpenSpec compliance, review-policy enforcement, refactoring |
| Ignis | Documentation | README, CHANGELOG, documentation updates |
| Lunafreya | PR Creation | Pull request creation and finalization |

## Workflow

The streamlined workflow minimizes user intervention and supports multiple approaches:

### Standard Workflow (New Change)
1. **Noctis** collaborates with user to create OpenSpec documents (artifact-based: proposal → tasks → design → specs)
2. ⏸️ **User approves specification**
3. **Iris** creates GitHub Issue (if requested)
4. **Gladiolus** implements based on OpenSpec
5. **Prompto** improves code quality (OpenSpec + review-policy)
6. **Ignis** updates documentation
7. **Noctis** verifies tasks completion and archives OpenSpec
8. **Lunafreya** creates PR
9. **Noctis** notifies user and requests verification
10. ⏸️ **User verifies implementation**

### Alternative Workflows
- **Continue**: Resume incomplete change, create next artifact
- **Fast-Forward**: Create all artifacts at once, skip iterative steps
- **Explore**: Collaborative exploration before creating change
- **Verify**: Validate implementation before archiving

## Team Philosophy

The FF15 OpenSpec team focuses on **autonomous execution with minimal interruptions**:
- **Noctis** creates specifications collaboratively with flexible workflows (new/continue/ff/explore), orchestrates execution, verifies completion, and archives work
- **Iris** manages the issue lifecycle
- **Gladiolus** delivers solid implementations
- **Prompto** ensures quality autonomously
- **Ignis** keeps documentation current
- **Lunafreya** completes the journey with pull request creation

## Invocation Methods

### Slash Command

| Command | Description |
|---------|-------------|
| **/noctis** | **Start OpenSpec-based implementation workflow** |

### Individual Agent Calls

Each agent can be invoked directly:
- `@Noctis` - Create OpenSpec and orchestrate workflow
- `@Iris` - Create/manage GitHub Issues
- `@Gladiolus` - Implement features
- `@Prompto` - Improve code quality
- `@Ignis` - Update documentation
- `@Lunafreya` - Archive and create PR

## Usage

### Sync All (agents, prompts, and docs)

```bash
python skills/copilot-agents-ff15-openspec-serena-sync/scripts/sync_agents.py --target /path/to/project
```

### Sync Specific Agents

```bash
python skills/copilot-agents-ff15-openspec-serena-sync/scripts/sync_agents.py \
  --target /path/to/project \
  --agents noctis,iris,gladiolus,prompto,ignis,lunafreya
```

### Sync Prompts Only

```bash
python skills/copilot-agents-ff15-openspec-serena-sync/scripts/sync_agents.py \
  --target /path/to/project \
  --prompts-only
```

## Script Options

| Option | Description |
|--------|-------------|
| `--target` | Target project directory (required) |
| `--agents` | Comma-separated list of agents to sync (noctis,iris,gladiolus,prompto,ignis,lunafreya) |
| `--prompts-only` | Sync only prompts |
| `--docs-only` | Sync only documentation |
| `--agents-only` | Sync only agent definitions |

## Agent Details

### 🎯 Noctis (Orchestrator + Spec Creator)

**Primary Responsibilities:**
- Create OpenSpec documents through user dialogue
- Coordinate implementation workflow
- Notify users at key milestones

**When to use:**
```
@Noctis Implement feature: user authentication with JWT
```

### 📋 Iris (Issue Management)

**Primary Responsibilities:**
- Create and manage GitHub Issues
- Refine requirements and specifications

**When to use:**
```
@Iris Create issue for the performance optimization we discussed
```

### 💪 Gladiolus (Implementation)

**Primary Responsibilities:**
- Implement features based on OpenSpec
- Follow TDD principles
- Execute until completion

**When to use:**
```
@Gladiolus Implement the feature according to OpenSpec change-001
```

### ✨ Prompto (Code Quality)

**Primary Responsibilities:**
- Verify OpenSpec compliance
- Enforce review-policy guidelines
- Refactor for clarity and maintainability

**When to use:**
```
@Prompto Improve the code quality of the recent implementation
```

### 📚 Ignis (Documentation + Archiving)

**Primary Responsibilities:**
- Update README and CHANGELOG
- Maintain project documentation
- Document new features and changes
- Archive OpenSpec changes

**When to use:**
```
@Ignis Update documentation for the new authentication feature
```

### 🌙 Lunafreya (PR Creation)

**Primary Responsibilities:**
- Create pull requests
- Ensure CI passes
- Finalize implementation delivery

**When to use:**
```
@Lunafreya Create a PR for the completed implementation
```

## Example Workflows

### Simple Workflow - User Describes → Noctis Orchestrates

```
User: @Noctis Add user profile page with avatar upload

Noctis:
  1. Creates OpenSpec (proposal, tasks, design)
  2. Requests user approval
  3. Delegates to Iris (Issue creation)
  4. Delegates to Gladiolus (Implementation)
  5. Delegates to Prompto (Quality improvement)
  6. Delegates to Ignis (Documentation + Archiving)
  7. Delegates to Lunafreya (PR creation)
  8. Notifies user with PR link

Result: Feature implemented with PR ready for merge
```

### Direct Agent Usage

```
@Iris Create an issue for the CSV export feature
→ Direct to Iris for issue creation

@Gladiolus Implement according to OpenSpec change-042
→ Direct implementation

@Prompto Review and improve the authentication code
→ Direct quality improvement
```

## Key Differences from Standard FF15

| Aspect | Standard FF15 | OpenSpec Edition |
|--------|--------------|------------------|
| Planning | Ignis creates plan | Noctis creates OpenSpec |
| Review | Aranea reviews | Prompto reviews + improves |
| Issue Creation | Lunafreya | Iris |
| Documentation | Part of implementation | Ignis specializes |
| Archiving | N/A | Ignis archives OpenSpec |
| PR Creation | Ardyn | Lunafreya |
| User Interruptions | Multiple | Minimal (2 points) |
| Serena MCP | Optional | Integrated throughout |

## Notes

- All agents leverage Serena MCP tools for efficient code navigation
- OpenSpec workflow ensures clear specifications before implementation
- Minimal user intervention (approval + verification only)
- Autonomous quality assurance through Prompto
- Complete workflow from specification to PR

## Related Files

- `agents/` - Agent definitions
- `prompts/` - Noctis prompts
- `docs/policies/` - Policy documents (deployment, development, review, testing)
- `scripts/sync_agents.py` - Synchronization script
