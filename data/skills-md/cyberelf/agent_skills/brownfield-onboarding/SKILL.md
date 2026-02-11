---
name: brownfield-onboarding
description: This skill helps users get started with existing (brownfield) projects by scanning the codebase, documenting structure and purpose, analyzing architecture and technical stack, identifying design flaws, suggesting improvements for testing and CI/CD pipelines, and generating AI agent constitution files (AGENTS.md) with project-specific context, coding principles, and UI/UX guidelines.
metadata:
  author: cyberelf
  version: "1.0"
---

# Brownfield Project Onboarding

## Overview

This skill provides a systematic approach to understand and document existing projects. It helps developers quickly get up to speed with unfamiliar codebases by generating comprehensive documentation about the project's structure, architecture, design decisions, identifying areas for improvement, and creating AI agent constitution files (AGENTS.md) that encode project-specific knowledge, coding principles, and UI/UX guidelines for effective AI-assisted development.

## When to Use This Skill

Invoke this skill when:
- Starting work on an unfamiliar or inherited codebase
- Joining a new team or project
- Conducting a technical audit of an existing system
- User requests "help me understand this project"
- Need to document an undocumented or poorly documented project
- Preparing for a major refactoring or modernization effort
- Setting up AI agent constitution files for better AI-assisted development
- Establishing coding principles and standards for a team
- Creating comprehensive context for AI agents working on the project

## How This Skill Works

Upon invocation, this skill:

1. **Analyzes the project** to determine its documentation state
2. **Selects the appropriate workflow** based on project maturity
3. **Executes the workflow** to generate comprehensive documentation
4. **Creates or enhances AGENTS.md files** for AI agent context
5. **Provides actionable recommendations** for improvements

---

## Workflow Selection

This skill uses **different workflows** based on the project's current state:

### Project State Detection

The AI agent automatically analyzes the project to determine its documentation maturity level.

**Detection Process**:
1. Search for AGENTS.md files using `file_search`
2. Search for constitution/guideline files (.cursorrules, CONTRIBUTING.md, etc.)
3. Read and analyze README for depth and quality
4. Apply classification rules with intelligent judgment

**Classification States**:
- **MATURE**: AGENTS.md exists
- **ESTABLISHED**: Constitution files + substantial README (>100 lines)
- **PARTIAL**: Basic README (>50 lines) only
- **VANILLA**: Minimal/no documentation (default)

**Detection Logic**:
- Has AGENTS.md → `MATURE`
- Has constitution files + README >100 lines with depth → `ESTABLISHED`
- Has README >50 lines of meaningful content → `PARTIAL`
- Otherwise → `VANILLA` (default)

The agent uses its intelligence to assess quality, not just quantity. A 60-line README with architecture details is better than a 150-line changelog.

### Workflow Files

Based on the agent's assessment, one of these workflows is executed:

| Project State | Workflow File | Time | Use When |
|--------------|---------------|------|----------|
| **Vanilla** | [vanilla-project.md](./references/vanilla-project.md) | 15-25 min | No/minimal docs, no constitutions |
| **Partial Docs** | [partial-documentation.md](./references/partial-documentation.md) | 10-20 min | Has README, no constitutions |
| **Established** | [established-project.md](./references/established-project.md) | 10-15 min | Good docs, has constitutions, no AGENTS.md |
| **Mature** | [mature-project.md](./references/mature-project.md) | 5-10 min | Already has AGENTS.md files |

📖 **For detailed workflow selection logic**, see [decision-guide.md](./references/decision-guide.md)

---

## Core Workflow Phases

All workflows execute these five phases (adapted to project state):

### Phase 1: Project Discovery
- Scan codebase structure
- Identify technologies and frameworks
- Discover features and entry points
- **Output**: `.onboard/overview.md`

### Phase 2: Architecture Analysis
- Document technical stack
- Identify architectural patterns
- Map data flow
- **Output**: `.onboard/architecture.md`

### Phase 3: Design Assessment
- Evaluate code quality
- Identify technical debt
- Propose improvements
- **Output**: `.onboard/design_suggestions.md`

### Phase 4: Quality & Automation Review
- Assess testing coverage
- Evaluate CI/CD maturity
- Recommend improvements
- **Output**: `.onboard/guardrail_suggestions.md`

### Phase 5: Agent Constitution Generation
- Detect/read existing constitutions
- Generate or enhance AGENTS.md files
- Create project-specific guidelines
- **Outputs**: `AGENTS.md` files + `.onboard/agent_constitution.md`

---

## Execution Instructions

### Step 1: Detect Project State

Analyze the project to determine its documentation maturity:

1. **Search for AGENTS.md**: Use `file_search` with pattern `**/AGENTS.md`
   - If found → State is **MATURE**

2. **Search for constitution files**: Use `file_search` to look for:
   - `.cursorrules`
   - `CONTRIBUTING.md`
   - `.github/CONSTITUTION.md`
   - Linter configs (`.eslintrc`, `.prettierrc`, etc.)
   - Style guides

3. **Analyze README**: Use `read_file` to check README.md
   - Count lines of meaningful content (exclude headers, badges, empty lines)
   - Assess depth: Does it explain architecture, setup, contribution guidelines?

4. **Classify based on findings**:
   - Has AGENTS.md → **MATURE**
   - Has constitution files + substantial README (>100 lines) → **ESTABLISHED**
   - Has basic README (>50 lines) but no constitution → **PARTIAL**
   - Minimal/no README (<50 lines) → **VANILLA** (default)

### Step 2: Load Appropriate Workflow

Based on your assessment, read and execute the corresponding workflow:

- **MATURE** → [references/mature-project.md](./references/mature-project.md)
- **ESTABLISHED** → [references/established-project.md](./references/established-project.md)
- **PARTIAL** → [references/partial-documentation.md](./references/partial-documentation.md)
- **VANILLA** → [references/vanilla-project.md](./references/vanilla-project.md)

### Step 3: Execute Workflow

Follow the instructions in the selected workflow file:
- Each workflow provides detailed, phase-by-phase instructions
- Each workflow adapts phases to the project's current state
- Each workflow includes specific tool usage recommendations

### Step 4: Validate Outputs

Ensure all expected files are generated:
- [ ] `.onboard/overview.md`
- [ ] `.onboard/architecture.md`
- [ ] `.onboard/design_suggestions.md`
- [ ] `.onboard/guardrail_suggestions.md`
- [ ] `.onboard/agent_constitution.md`
- [ ] `./AGENTS.md` (created or enhanced)
- [ ] Subdirectory AGENTS.md files (if applicable)

### Step 5: Provide Summary

Give user a comprehensive completion summary based on workflow type.

---

## AGENTS.md Templates

This skill includes template files for generating AGENTS.md:

### Available Templates

1. **[root-agents-template.md](./templates/root-agents-template.md)**
   - Project-wide context and coding principles
   - Placed at project root

2. **[frontend-agents-template.md](./templates/frontend-agents-template.md)**
   - Frontend-specific guidelines
   - UI/UX design system and accessibility
   - Placed in frontend directory

3. **[backend-agents-template.md](./templates/backend-agents-template.md)**
   - Backend-specific guidelines
   - API design and security principles
   - Placed in backend directory


### Template Adaptation

Templates are adapted based on:
- Actual project structure and patterns
- Discovered design tokens and conventions
- Existing constitution file content
- Tech stack and framework conventions

---

## Key Principles

### 1. Non-Destructive Enhancement
- Never overwrite existing documentation
- Enhance and complement, don't replace
- Preserve existing constitution files
- Mark all additions clearly

### 2. Context-Aware Generation
- Generate content based on actual code analysis
- Use project-specific examples
- Adapt to detected patterns
- Match existing documentation style

### 3. Workflow Adaptation
- Different approaches for different project maturities
- Respect existing work and conventions
- Focus effort where value is highest
- Minimize disruption to established projects

### 4. AI Agent Optimization
- Create machine-readable guidelines
- Include validation checklists
- Provide quick reference formats
- Synthesize across multiple docs

---

## Common Tools Used

Across all workflows, these tools are commonly used:

### Discovery Tools
- `list_dir` - Explore directory structure
- `file_search` - Find specific files by pattern (e.g., `**/AGENTS.md`, `**/.cursorrules`)
- `read_file` - Read documentation and config files (README, CONTRIBUTING, etc.)

### Analysis Tools
- `semantic_search` - Find features and concepts
- `grep_search` - Pattern-based code search
- `list_code_usages` - Understand code relationships

### Validation Tools
- `get_errors` - Identify existing issues
- Code analysis for patterns and anti-patterns

---

## Output Directory Structure

After execution, the workspace contains:

```
.onboard/
├── overview.md              # Project structure and features
├── architecture.md          # Technical stack and architecture
├── design_suggestions.md    # Improvement recommendations
├── guardrail_suggestions.md # Testing and CI/CD recommendations
└── agent_constitution.md    # Constitution generation summary

AGENTS.md                    # Root project constitution
[frontend]/AGENTS.md         # Frontend guidelines (if applicable)
[backend]/AGENTS.md          # Backend guidelines (if applicable)
```

---

## Notes & Best Practices

- **Comprehensive Analysis**: Take time to thoroughly explore before documenting
- **Be Specific**: Include file paths and concrete examples
- **Prioritize**: Rank suggestions by impact and effort
- **Actionable**: Provide implementable recommendations
- **Context-Aware**: Tailor to project size, domain, and maturity
- **Positive Framing**: Start with strengths before improvements
- **Realistic Estimates**: Provide effort estimates for planning
- **Agent-Friendly**: Enable AI agents to validate their work
- **Respect Existing Constitutions**: Enhance rather than replace
- **Non-Destructive**: Always preserve existing content when merging
- **Context-Rich Constitutions**: Make AGENTS.md comprehensive with project-specific details

## Common Pitfalls to Avoid

- ❌ Generating superficial documentation without deep analysis
- ❌ Making technology recommendations without understanding constraints
- ❌ Suggesting major rewrites instead of incremental improvements
- ❌ Ignoring existing documentation or architectural decisions
- ❌ Providing generic advice that doesn't apply to the specific project
- ❌ Overwhelming with too many suggestions without prioritization
- ❌ Missing critical security or performance issues
- ❌ Overwriting existing constitution files without preserving original content
- ❌ Creating generic AGENTS.md templates without project-specific context
- ❌ Skipping UI/UX principles analysis for frontend projects

---

## Extension Points

This skill can be extended to include:
- **Security Audit**: Dedicated security vulnerability assessment
- **Performance Profiling**: Performance bottleneck identification
- **Accessibility Review**: WCAG compliance checking for web apps
- **API Documentation**: Automated API documentation generation
- **Database Analysis**: Schema design review and optimization suggestions
- **UI/UX Deep Dive**: Integration with ui-ux-pro-max skill for comprehensive UI/UX principles
- **Dependency Audit**: Automated dependency security and license checking
- **Constitution Compliance**: Automated checking of code against AGENTS.md guidelines

## Related Skills

- **ui-ux-pro-max**: Can be invoked for comprehensive UI/UX analysis to enhance frontend AGENTS.md files
- **openspec-constitution-guard**: Can validate code changes against generated AGENTS.md constitutions
- **issue-fixer**: Uses project context from AGENTS.md files to fix issues more effectively
- **retrospect**: References AGENTS.md for project-specific context during retrospective analysis

---

## Reference Documentation

### Workflow References
- [decision-guide.md](./references/decision-guide.md) - How to choose the right workflow
- [vanilla-project.md](./references/vanilla-project.md) - Workflow for minimal documentation
- [partial-documentation.md](./references/partial-documentation.md) - Workflow for basic README projects
- [established-project.md](./references/established-project.md) - Workflow for well-documented projects
- [mature-project.md](./references/mature-project.md) - Workflow for projects with existing AGENTS.md

### Template References
- [templates/root-agents-template.md](./templates/root-agents-template.md) - Root constitution template
- [templates/frontend-agents-template.md](./templates/frontend-agents-template.md) - Frontend constitution template
- [templates/backend-agents-template.md](./templates/backend-agents-template.md) - Backend constitution template

---

## Quick Start

To use this skill:

1. **User invokes**: "Help me understand this project" or "Run brownfield onboarding"
2. **Detect project state**: Analyze project to determine maturity level (MATURE/ESTABLISHED/PARTIAL/VANILLA)
3. **Load workflow**: Read the appropriate workflow file from `references/`
4. **Execute phases**: Follow workflow instructions for all 5 phases
5. **Generate outputs**: Create all documentation and AGENTS.md files
6. **Provide summary**: Give user comprehensive results and next steps

The workflow files contain all detailed instructions - this main SKILL.md serves as the orchestration guide.
