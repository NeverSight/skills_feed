---
name: "Dependency Updater"
description: "Orchestrates comprehensive dependency updates by delegating research, impact analysis, code changes, and validation to specialized agents. Invoked when users request package updates, dependency updates, version bumps, or mention 'ncu' or npm-check-updates."
version: "1.1.0"
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash(npm:*)
  - Bash(yarn:*)
  - Bash(pnpm:*)
  - Bash(ncu:*)
  - Bash(npx:*)
  - Task
  - WebSearch
  - WebFetch
---

# Dependency Updater

Coordinates automated package updates through specialized agent delegation and quality assurance.

## Core Mission

Execute comprehensive dependency updates by orchestrating specialized agents. **NEVER implement updates or conduct research yourself** - coordinate, delegate, and validate.

## Execution Protocol

### 1. Initialize with TodoWrite

- Break dependency update workflow into discrete, testable phases
- Create todos for analysis, research, impact assessment, updates, and validation
- Refer to [Agent Coordination Standards](~/.claude/standards/agent-coordination.md) for parallel vs sequential execution patterns

### 2. Delegate All Tasks

Available agents:

- `research-subagent`: Researches individual package changelogs, release notes, breaking changes
- `architect`: Analyzes breaking change impact, assesses migration complexity
- `developer`: Applies updates, implements code changes, fixes compatibility issues
- `quality-reviewer`: Reviews security implications, performance impacts
- `technical-writer`: Creates comprehensive PR documentation

**Delegation Format:**

```md
Task for [agent]: [Specific update task]
Context: [Package update details and research findings]
Requirements:

- [Compatibility requirement]
- [Breaking change handling]

Acceptance: [Quality gates to verify success]
```

### 3. Dependency Update Workflow

#### Phase 1: Update Analysis

1. Run `ncu --jsonUpgraded` to detect available updates
2. Parse output to identify packages with version changes
3. Filter packages based on user criteria (`--filter`, `--dry-run`)

#### Phase 1.5: Semver Classification

**CRITICAL**: Properly classify ALL version changes according to [Semantic Versioning Standards](~/.claude/standards/semver.md) before proceeding. Incorrect classification leads to wrong research depth and documentation.

**Reference**: Follow the comprehensive semver classification rules in `~/.claude/standards/semver.md` which includes:

- Detailed classification examples
- Common error patterns to avoid
- Version range notation handling
- Pre-release version rules

**Quick Classification:**

- **MAJOR** (X.y.z → X+1.y.z): Breaking changes, incompatible API changes
- **MINOR** (x.Y.z → x.Y+1.z): New functionality, backward compatible
- **PATCH** (x.y.Z → x.y.Z+1): Bug fixes, backward compatible

**Process:**

1. Apply semver standards for parsing and classification
2. Group packages by classification: MAJOR, MINOR, PATCH
3. Verify classification matches semver standards before delegating

#### Phase 2: Parallel Research (Independent Tasks)

**CRITICAL**: Launch ALL package research tasks in a single parallel batch using one message with multiple Task tool calls. Target 10-20 parallel research-subagents for maximum efficiency.

Research each package concurrently based on **semver classification from Phase 1.5**:

- **MAJOR changes** (X.y.z → X+1.y.z): Full research including changelogs, breaking changes, upgrade or migration guides
- **MINOR changes** (x.Y.z → x.Y+1.z): Minimal research - check for new features and deprecated APIs only. **If release notes aren't found, continue with the update anyway**
- **PATCH changes** (x.y.Z → x.y.Z+1): Skip research entirely - assume safe bug fixes. **Always proceed even without release information**
- Document any security advisories regardless of change type

**Verification**: Ensure research depth matches the actual semver classification, not package names or assumed importance.

**Parallelism Requirement**: Never research packages sequentially - always batch all research tasks simultaneously.

#### Phase 3: Impact Assessment (Sequential)

1. **Architect**: Analyze breaking changes across all packages
2. **Architect**: Assess migration complexity and code impact
3. Search codebase for package usage patterns
4. Identify files requiring updates due to breaking changes

#### Phase 4: Apply Updates (Sequential)

1. **Developer**: Update package.json files (`ncu -u`)
2. **Developer**: Install dependencies (`yarn install`)
3. **Developer**: Implement required code changes for breaking changes
4. Handle dependency conflicts and version mismatches

#### Phase 5: Quality Validation (Parallel)

Run quality checks concurrently:

- TypeScript compilation (`yarn typecheck`)
- Linting with fixes (`yarn lint:fix`)
- Test suite execution (`yarn test`)
- **Quality-reviewer**: Security and performance validation

#### Phase 6: PR Creation (Sequential)

1. **Check existing PR status**:
   - Run `gh pr status` to check if current branch has an open PR
   - If PR exists: Continue with existing branch and update existing PR
   - If no PR exists: Create feature branch with timestamp

2. **Technical-writer**: Generate comprehensive commit message
3. **Technical-writer**: Create or update PR description including:
   - Package update summary grouped by semver classification in markdown tables
   - Table columns: Package, Current, Target, and relevant details (Breaking Changes/New Features/Fixes)
   - Breaking change impact analysis for major version updates
   - Migration steps performed for major version changes
   - Quality validation results
   - Links to changelogs and release notes

4. **Push and handle PR**:
   - If existing PR: Push commits to existing branch, update PR description via `gh pr edit`
   - If new PR: Push branch and create PR via `gh pr create`
5. **REQUIRED**: Provide the GitHub PR link in the final output for easy user review

## Usage Options

- No arguments: Full automated workflow
- `--dry-run`: Preview changes without applying them
- `--filter <pattern>`: Only update packages matching the pattern

## Error Handling

When encountering errors:

1. **Evidence First**: Capture exact error messages and dependency conflicts
2. **Delegate Investigation**: Use appropriate agents (`architect` for design issues, `developer` for implementation)
3. **Quality Gates**: All tests must pass before PR creation
4. **Rollback Plan**: Document steps to revert changes if issues arise

## Quality Standards

Each phase must meet:

- ✅ All existing tests pass
- ✅ No new linting violations
- ✅ TypeScript compilation succeeds
- ✅ Security vulnerabilities addressed
- ✅ Breaking changes properly migrated

## Success Criteria

Dependency update succeeds when:

- [ ] All package updates applied successfully
- [ ] Breaking changes resolved with code updates
- [ ] Quality validation passes completely
- [ ] Comprehensive PR created with documentation
- [ ] No regression in functionality

## Key Principles

1. **Coordinate, Don't Execute**: Delegate all specialized work to appropriate agents
2. **Parallel Where Possible**: Research packages concurrently for efficiency
3. **Quality First**: Never compromise on testing and validation
4. **Evidence-Based**: Use agent research for all decisions
5. **Comprehensive Documentation**: Ensure PR provides complete context

## Important Notes

- **Always use `ncu` command directly** - NEVER use `npx npm-check-updates`
- Ensure `ncu` is globally installed: `npm install -g npm-check-updates`
- Use `ncu` for all update detection and application operations

Remember: Your strength is in orchestration, delegation, and ensuring safe dependency updates.
