---
name: cosmos-planning
description: Create structured, actionable implementation plans that serve as both human documentation and agent-executable specs. Use when creating new plans, converting ideas into implementation roadmaps, or when asked to plan a feature, refactor, or multi-phase project. Plans include detailed technical tasks with file paths, acceptance criteria, dependencies, and context blocks for autonomous agent execution.
---

# Planning Skill

Create consistent, dual-purpose implementation plans that are readable by humans and executable by AI agents.

## Quick Start

When creating a new plan, copy the template from [assets/PLAN_TEMPLATE.md](assets/PLAN_TEMPLATE.md) and fill in the sections. The template includes all required structure with placeholder text to replace.

## Plan Structure

Every plan follows this structure:

```markdown
# {NNN}: {Title}

**Status**: Draft | In Progress | Complete | Blocked  
**Created**: YYYY-MM-DD  
**Author**: {author or "AI-assisted planning session"}

---

## Overview
{2-3 sentences: What does this plan accomplish? Why does it matter?}

## Goals
{Numbered list with bold goal names and brief explanations}

## Architecture
{High-level design: diagrams, data flow, component relationships}

## Dependencies
{External packages, internal modules, other plans this depends on}

## References
{Links to docs, issues, related files, external resources}

---

## Implementation Phases

### Phase N: {Phase Title}

**Status**: Not Started | In Progress | Complete  
**Depends on**: None | Phase N

#### Context
{Background info: relevant files, current state, patterns to follow, code snippets}

#### Tasks

##### N.1 {Task Title}
**Status**: ☐ Not Started | ◐ In Progress | ✓ Complete  
**Requires**: None | Task N.M  
**Acceptance Criteria**: {What "done" looks like - specific, testable}

**Context**:
- File: `src/path/to/file.ts`
- Pattern: {Existing pattern to follow or reference}

**Sub-tasks**:
- [ ] {Specific technical step with file/function names}
- [ ] {Implementation detail}
- [ ] {Verification step - test, lint, build}
```

## Section Guidelines

### Header
- **NNN**: Zero-padded 3-digit number (e.g., `001`, `042`)
- **Status values**: `Draft` (initial), `In Progress` (active work), `Complete` (all phases done), `Blocked` (waiting on external dependency)

### Overview
- 2-3 sentences maximum
- Answer: What? Why? Impact?
- No implementation details here

### Goals
Format:
```markdown
1. **Goal Name** - Why this matters, what success looks like
2. **Another Goal** - Brief explanation
```

### Architecture
- Include ASCII diagrams for data/control flow
- Document key design decisions
- Show component relationships
- Keep diagrams under 30 lines

### Dependencies
Split into categories when helpful:
```markdown
**External Packages**:
- `package-name@^version` - Purpose

**Internal Modules**:
- `src/module/` - What it provides

**Related Plans**:
- [Plan 001](001-plan-name.md) - Why it's related
```

### References
- External documentation links
- GitHub issues/PRs
- Related workspace files (use relative paths)

## Phase Guidelines

### Phase Structure
- Phases are **sequential** - later phases assume earlier ones complete
- Keep phases focused: 3-7 tasks per phase
- Name phases by outcome: "Core Infrastructure", "API Integration", "CLI Commands"

### Phase Context Block
Include information agents need to execute tasks:
- Relevant file paths in the codebase
- Existing patterns to follow (with code snippets if short)
- Current state of the system
- Design constraints or decisions

Example:
```markdown
#### Context
The workflow executor is in `src/workflows/executor.ts`. Node execution 
happens in the `executeNode()` function starting at line 45. Follow the 
existing pattern of returning `NodeResult` objects.

Current signature:
\`\`\`typescript
async function executeNode(node: WorkflowNode, ctx: Context): Promise<NodeResult>
\`\`\`
```

## Task Guidelines

### Task Structure
Every task includes:
1. **Status marker**: `☐` (not started), `◐` (in progress), `✓` (complete)
2. **Requires**: Explicit dependencies on other tasks
3. **Acceptance Criteria**: Specific, testable definition of done
4. **Context**: Files, patterns, relevant code
5. **Sub-tasks**: Checkable technical steps

### Writing Effective Tasks
- Start task titles with action verbs: Create, Implement, Add, Update, Refactor
- Make acceptance criteria measurable: "Tests pass", "Exports function X", "Handles error case Y"
- Include specific file paths in context
- Reference existing patterns when applicable

### Sub-task Guidelines
Each sub-task should be:
- **Atomic**: One specific action
- **Technical**: Include file/function names
- **Verifiable**: Clear when done

Example sub-tasks:
```markdown
- [ ] Create `src/telemetry/provider.ts` with `initTracer()` function
- [ ] Export `getTracer()` from `src/telemetry/index.ts`
- [ ] Add unit tests in `tests/telemetry/provider.test.ts`
- [ ] Verify: `npm test telemetry` passes
```

## Verification Requirements

Verification is **mandatory** at both task and phase levels to ensure quality and catch AI hallucinations early.

### Task-Level Verification

Every task **must** end with a verification sub-task that proves the work is complete:

```markdown
**Sub-tasks**:
- [ ] Create `src/plugins/loader.ts`
- [ ] Implement `loadPlugin()` function
- [ ] Add unit tests in `tests/plugins/loader.test.ts`
- [ ] **Verify**: `npm test loader` passes
```

**Verification types** (use at least one per task):
- `npm test {pattern}` - Unit tests pass
- `npm build` - Code compiles without errors
- `npm lint` - No lint errors introduced
- Manual check: {specific behavior to observe}

### Phase-Level Verification

Every phase **must** end with a verification task that integrates and tests all phase work:

```markdown
##### 1.X Phase 1 Verification
**Status**: ☐ Not Started  
**Requires**: All previous phase tasks  
**Acceptance Criteria**: All Phase 1 features work together

**Sub-tasks**:
- [ ] Run full test suite: `npm test`
- [ ] Run build: `npm build`
- [ ] Run lint: `npm lint`
- [ ] Manual integration test: {describe end-to-end behavior}
- [ ] Document any issues found in task notes
```

### Why Verification Matters

1. **Catches hallucinations** - AI must prove work is complete with passing tests
2. **Incremental quality** - Issues found early, not at the end
3. **Clear done state** - No ambiguity about task completion
4. **TDD alignment** - Tests are written as part of implementation, not afterthought

### Dependency Format
```markdown
**Requires**: 1.2, 1.3
```
Use task numbers from the same plan. For cross-plan dependencies:
```markdown
**Requires**: Plan 001 Phase 2 complete
```

## Context Block Patterns

### For File Modifications
```markdown
**Context**:
- File: `src/commands/index.ts`
- Add command to `commands` array at line 23
- Follow pattern of existing commands (see `init.ts`)
```

### For New Features
```markdown
**Context**:
- Create new directory: `src/feature/`
- Pattern: Follow structure of `src/workflows/`
- Exports: Re-export from `src/feature/index.ts`
```

### For Integrations
```markdown
**Context**:
- API docs: https://example.com/api
- Auth: Use token from `ctx.config.apiKey`
- Error handling: Wrap in `try/catch`, return `Result<T>` type
```

## Status Tracking

### Plan-Level Status
Update in header as work progresses:
- `Draft` → initial creation
- `In Progress` → at least one phase started
- `Complete` → all phases complete
- `Blocked` → external blocker documented in Overview

### Phase-Level Status
```markdown
**Status**: Not Started | In Progress | Complete
```

### Task-Level Status
Use status markers for quick scanning:
- `☐` - Not started
- `◐` - In progress
- `✓` - Complete

### Sub-task Checkboxes
```markdown
- [ ] Not done
- [x] Complete
```

## Example Plan Skeleton

```markdown
# 015: Add Plugin System

**Status**: Draft  
**Created**: 2026-01-27  
**Author**: AI-assisted planning session

---

## Overview

Implement a plugin system for cosmos-cli that allows users to extend 
functionality with custom commands and workflows without modifying core code.

## Goals

1. **Extensibility** - Users can add commands without forking
2. **Discoverability** - Plugins auto-register and appear in help
3. **Isolation** - Plugin errors don't crash the CLI

## Architecture

\`\`\`
┌─────────────────┐     ┌─────────────────┐
│   Core CLI      │────▶│  Plugin Loader  │
└─────────────────┘     └────────┬────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ~/.cosmos/     │     │  node_modules/  │     │  ./plugins/     │
│  plugins/       │     │  cosmos-plugin-*│     │  (local)        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
\`\`\`

## Dependencies

**External Packages**:
- None required (use dynamic import)

**Internal Modules**:
- `src/commands/` - Command registration pattern
- `src/core/project.ts` - Project root discovery

## References

- [Commander.js Plugin Pattern](https://github.com/tj/commander.js)
- [Related: Plan 006](006-project-root-discovery.md)

---

## Implementation Phases

### Phase 1: Plugin Loader

**Status**: Not Started  
**Depends on**: None

#### Context
Commands are registered in `src/commands/index.ts`. Each command exports 
a function that receives the Commander program instance. Plugins should 
follow this same pattern.

#### Tasks

##### 1.1 Create Plugin Discovery Module
**Status**: ☐ Not Started  
**Requires**: None  
**Acceptance Criteria**: Finds plugins in ~/.cosmos/plugins/ and node_modules/

**Context**:
- File: Create `src/plugins/discovery.ts`
- Pattern: Similar to `src/workflows/discovery.ts`

**Sub-tasks**:
- [ ] Create `src/plugins/discovery.ts`
- [ ] Implement `discoverPlugins()` function
- [ ] Search ~/.cosmos/plugins/ for plugin.json files
- [ ] Search node_modules/ for cosmos-plugin-* packages
- [ ] Return array of `PluginManifest` objects
- [ ] Add unit tests in `tests/plugins/discovery.test.ts`

**TDD**:
- [ ] `tests/plugin/discovery.test.ts` created first with failing tests
- [ ] `tests/plugin/discovery.test.ts` passes after implemenation integrated

##### 1.2 Create Plugin Loader
**Status**: ☐ Not Started  
**Requires**: 1.1  
**Acceptance Criteria**: Loads and validates plugin modules safely

**Context**:
- File: Create `src/plugins/loader.ts`
- Use dynamic import() for loading
- Wrap in try/catch for isolation

**Sub-tasks**:
- [ ] Create `src/plugins/loader.ts`
- [ ] Implement `loadPlugin(manifest: PluginManifest)` function
- [ ] Validate plugin exports required interface
- [ ] Handle load errors gracefully (log warning, continue)
- [ ] Add unit tests with mock plugins
- [ ] **Verify**: `npm test loader` passes

**TDD**:
- [ ] `tests/plugin/loader.test.ts` created first with failing tests
- [ ] `tests/plugin/loader.test.ts` passes after mock plugins integrated

##### 1.3 Phase 1 Verification
**Status**: ☐ Not Started  
**Requires**: 1.1, 1.2  
**Acceptance Criteria**: Plugin discovery and loading work end-to-end

**Sub-tasks**:
- [ ] Run full test suite: `npm test`
- [ ] Run build: `npm build`
- [ ] Manual test: Create mock plugin, verify it loads and registers
```

## Naming Convention

Plan files: `{NNN}-{kebab-case-title}.md`

Examples:
- `001-opentelemetry-observability.md`
- `015-add-plugin-system.md`
- `042-migrate-to-esm.md`

Place all plans in the `plans/` directory at the project root.
