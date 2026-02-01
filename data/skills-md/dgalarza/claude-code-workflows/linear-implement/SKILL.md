---
name: linear-implement
description: This skill should be used when implementing features from Linear issues with full TDD workflow, automated planning, parallel code reviews (security and Rails best practices), systematic feedback implementation, and automated PR creation with Linear integration. Use when the user provides a Linear issue ID (e.g., "TRA-9", "DEV-123") and wants a complete implementation workflow from issue to PR.
---

# Linear Issue Implementation

## Overview

This skill provides a comprehensive workflow for implementing Linear issues with professional software engineering practices. It automates the entire development lifecycle from issue analysis through PR creation, ensuring quality through test-driven development, parallel code reviews, and systematic validation.

## When to Use This Skill

Use this skill when:
- User provides a Linear issue ID (format: `TRA-9`, `DEV-123`, etc.)
- User requests implementation of a Linear issue
- User wants a structured TDD approach with code review
- User needs automated workflow from issue to PR

Examples:
- "Implement TRA-142"
- "Help me build the feature in DEV-89"
- "Work on Linear issue ABC-456"

## Core Workflow

The skill follows a 14-step process:

1. **Fetch Linear Issue** - Retrieve complete issue details via Linear MCP
2. **Gather Additional Context** - Search Obsidian, Sentry, and GitHub for related information
3. **Move to In Progress** - Update issue status to indicate active work
4. **Create Feature Branch** - Use Linear's suggested git branch naming
5. **Analyze & Plan** - Break down requirements and create implementation plan
6. **Save to Memory** - Store plan in memory graph for tracking
7. **Review Plan** - Present plan for user confirmation
8. **TDD Implementation** - Invoke `tdd-workflow` skill for test-driven development
9. **Parallel Code Reviews** - Invoke `parallel-code-review` skill for comprehensive analysis
10. **Address Feedback** - Invoke `code-review-implementer` skill to systematically fix issues
11. **Validation** - Ensure all tests and linters pass
12. **Logical Commits** - Create meaningful commit history
13. **Create PR** - Generate comprehensive pull request with Linear linking
14. **Final Verification** - Confirm CI/CD pipeline and Linear integration

## Workflow Implementation Details

### Step 1: Fetch Linear Issue Details

Retrieve the complete issue using Linear MCP tools:

```
mcp__linear__get_issue(id: <issue-id>)
```

Extract key information:
- Title and description
- Current status and priority
- Suggested git branch name (`branchName` field)
- Team and project context
- Attachments or related work
- Labels and assigned team members

### Step 2: Gather Additional Context

Before planning, gather related context from multiple sources to inform the implementation approach.

#### Search Obsidian Vault

Search for any existing notes that might be related to this issue:

```
# Search by issue ID
Search Obsidian vault for: "TRA-142"

# Search by issue summary/keywords
Search Obsidian vault for: "<keywords from issue title/description>"
```

Look for:
- Previous meeting notes discussing this feature
- Architecture decisions or technical notes
- Related implementation notes from similar work
- User research or requirements documentation

#### Fetch Sentry Context (if referenced)

If the Linear issue references any Sentry issues or error tracking:

```
mcp__sentry__get_issue(issue_id: <sentry-issue-id>)
```

Extract from Sentry:
- Error stack traces and frequency
- Affected users and environments
- Related events and breadcrumbs
- Any existing comments or assignments

This context helps understand:
- The root cause of bugs
- Which code paths are affected
- How frequently the issue occurs
- Environmental factors to consider

#### Fetch GitHub Context (if referenced)

If the Linear issue references GitHub pull requests, issues, or discussions:

```bash
# View PR details and discussion
gh pr view <pr-number>

# View PR comments and review threads
gh pr view <pr-number> --comments

# View issue details
gh issue view <issue-number>

# View issue comments
gh issue view <issue-number> --comments
```

Extract from GitHub:
- Previous implementation attempts
- Review feedback and concerns raised
- Design discussions and decisions
- Related code changes or context

**Context Summary:**

After gathering context, summarize:
- Relevant information found in Obsidian
- Sentry error details (if applicable)
- GitHub discussion insights (if applicable)
- How this context affects the implementation approach

### Step 3: Move Issue to In Progress

Update the issue status to reflect active development:

1. Identify the team ID from the issue
2. Retrieve "In Progress" state using `mcp__linear__list_issue_statuses(team: <team-id>)`
3. Update issue using `mcp__linear__update_issue(id: <issue-id>, state: <in-progress-state-id>)`

This provides visibility to team members that work has begun.

### Step 4: Create Feature Branch

Use Linear's suggested branch name for consistency:

```bash
# Ensure on main and up-to-date
git checkout main
git pull origin main

# Get branch name from Linear's branchName field
BRANCH_NAME="<from Linear branchName field>"

# Create branch if new, or checkout if exists (idempotent)
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

# Verify correct branch
git branch --show-current
```

This pattern ensures:
- Reuse of existing branches
- Consistent Linear-suggested naming
- Idempotent operations (safe to re-run)
- Always working from latest main

### Step 5: Analyze and Plan Solution

Break down the issue into an actionable implementation plan:

**Analysis Process:**
1. Extract specific requirements from issue description
2. Identify affected components and systems
3. Determine testing strategy (unit → integration → system)
4. Plan implementation approach following project patterns
5. Identify potential risks and dependencies

**Planning Output:**
- **Goal**: Clear statement of implementation objective
- **Requirements**: Specific functional and technical requirements
- **Architecture**: How solution fits existing codebase (models, services, controllers)
- **Test Strategy**: Comprehensive testing including system specs
- **Implementation Steps**: Ordered list of development tasks
- **Acceptance Criteria**: Definition of done

### Step 6: Save Plan to Memory

Store the implementation plan using memory MCP tools:

```
mcp__memory__create_entities(entities: [
  {
    name: "Linear Issue <issue-id>",
    entityType: "implementation-plan",
    observations: [
      "Requirements: <requirements>",
      "Architecture: <architecture-decisions>",
      "Test Strategy: <test-approach>",
      "Status: planning-complete"
    ]
  }
])
```

This creates permanent tracking of:
- Issue context and requirements
- Implementation approach and reasoning
- Progress throughout development
- Lessons learned for future work

### Step 7: Review Plan with User

Present the complete plan for confirmation:

**Plan Presentation:**
- Summary of what will be implemented
- Key technical decisions and rationale
- Testing strategy and expected coverage
- Estimated complexity and identified risks
- Explicit confirmation request

**User Options:**
- Approve to proceed with implementation
- Request modifications to approach
- Add requirements or constraints
- Ask clarifying questions

### Step 8: Test-Driven Development Implementation

Upon approval, invoke the TDD workflow skill:

```
Invoke the Skill tool with: tdd-workflow
```

The TDD workflow skill enforces:
- Red-Green-Refactor cycles
- Test pyramid strategy (unit → integration → system)
- Writing tests before implementation
- Comprehensive test coverage including system specs

**Expected Outcomes:**
- Complete test coverage for new functionality
- Implementation following project POODR principles
- Result pattern for operations that can fail
- Clean, maintainable code structure

### Step 9: Parallel Subagent Code Reviews

After implementation, invoke the parallel code review skill:

```
Invoke the Skill tool with: parallel-code-review
```

This launches specialized review subagents in parallel:

**Security Review:**
- OWASP Top 10 vulnerabilities
- Multi-tenant security (ActsAsTenant verification)
- XSS, CSRF, SQL injection prevention
- Authentication and authorization checks
- Sensitive data handling

**Rails Best Practices Review:**
- POODR principles (SRP, dependency management, Tell Don't Ask)
- Rails 7+ conventions
- N+1 query prevention
- ActiveRecord optimization
- Service object patterns
- Result pattern usage

**Frontend Review (if applicable):**
- ViewComponent best practices
- Tailwind CSS conventions
- StimulusJS patterns
- Accessibility (ARIA attributes)

**Output:**
- Consolidated review report
- Decision tracking to prevent redundancy
- Prioritized feedback by severity and impact

### Step 10: Address Review Feedback

Invoke the code review implementer skill:

```
Invoke the Skill tool with: code-review-implementer
```

This skill systematically addresses feedback:

**Process:**
1. Parse and prioritize feedback by impact and effort
2. Identify common refactoring patterns
3. Implement fixes incrementally with test validation
4. Ensure backward compatibility
5. Update documentation as needed

**Architectural Feedback is MANDATORY:**
- Extract service objects if controllers/models have too many responsibilities
- Apply Result pattern for operations that can fail
- Refactor to improve testability and maintainability
- Add comprehensive specs for new service objects

**Note:** Do NOT create PR until all architectural feedback is implemented.

### Step 11: Validation and Quality Assurance

Before creating commits, ensure everything passes:

**Validation Steps:**
```bash
# Run full test suite
bundle exec rspec

# Run linting (Standard, ERB, Brakeman)
bin/lint

# Fix any failures or warnings
# Verify system specs pass in clean environment
```

**Quality Checks:**
- Code follows project POODR principles
- Result pattern used appropriately
- No security vulnerabilities
- Performance impact considered (no N+1 queries)
- All subagent feedback addressed
- Test coverage sufficient

**Linting Notes:**
- Yarn failures can be ignored if only working on Rails code
- Warnings about `MigratedSchemaVersion` and `ContextCreatingMethods` are harmless
- **Actual offenses must be addressed** (look for file paths and line numbers)

### Step 12: Create Logical Commits

Create meaningful commits that tell the implementation story:

**Commit Strategy:**
1. **Test commits**: Add failing tests for new functionality
2. **Implementation commits**: Add code to make tests pass
3. **Refactor commits**: Improve code structure
4. **Security fixes**: Address security review feedback
5. **Pattern improvements**: Implement OOP/Rails pattern suggestions
6. **Documentation commits**: Update docs if needed

**Commit Message Format:**
```
Present-tense summary under 50 characters

- Detailed explanation if needed (under 72 chars per line)
- Reference which review feedback was addressed
- Note any breaking changes or migration requirements

Linear issue: <Linear issue URL>
Implemented with Claude Code
```

**Use heredoc for proper formatting:**
```bash
git commit -m "$(cat <<'EOF'
Add user notification service

- Extract notification logic from controller
- Apply Result pattern for error handling
- Add comprehensive RSpec tests with edge cases

Linear issue: https://linear.app/company/issue/TRA-142
Implemented with Claude Code
EOF
)"
```

### Step 13: Create Pull Request

Generate comprehensive PR with Linear integration:

**PR Creation Command:**
```bash
gh pr create --title "<concise-title>" --body "$(cat <<'EOF'
## Summary
- Concise bullet points of what was implemented
- Key technical decisions made

## Implementation Details
- Architecture approach and patterns used
- Services/models/controllers added or modified
- Database changes (if applicable)

## Testing Strategy
- Test coverage added (unit, integration, system)
- Edge cases covered
- Manual testing performed

## Code Review Process
- Security review findings and resolutions
- Rails best practices review findings and resolutions
- Performance considerations addressed

## Breaking Changes
[None or list any breaking changes]

## Linear Issue
Closes <Linear issue URL>

---
Implemented with Claude Code following TDD methodology with parallel code reviews.
EOF
)"
```

**PR Description Includes:**
- Summary of implementation
- Technical approach and key decisions
- Testing strategy and coverage
- Code review findings and resolutions
- Security considerations addressed
- Breaking changes or migration notes
- Screenshots/demos if applicable

**Linear Integration:**
- Include `Closes <Linear-issue-URL>` in PR body
- Linear automatically links and updates issue status when PR merges

### Step 14: Final Verification

Verify PR setup and completion:

**Final Checks:**
- ✅ CI/CD pipeline triggered successfully
- ✅ Linear issue linked and updated
- ✅ All tests passing in CI environment
- ✅ Code review assignees notified
- ✅ Branch protection rules satisfied
- ✅ Security and pattern reviews documented

**Completion Summary:**
Present checklist to user:
- ✅ Linear issue analyzed and planned
- ✅ Solution implemented with TDD
- ✅ Comprehensive system specs added
- ✅ Security review completed
- ✅ Rails/OOP patterns review completed
- ✅ All review feedback addressed
- ✅ All tests and linting pass
- ✅ Logical commit history created
- ✅ PR created with Linear integration

## Integration with Other Skills

This skill orchestrates multiple specialized skills:

**tdd-workflow:**
- Enforces Red-Green-Refactor cycles
- Ensures test-first development
- Guides test pyramid strategy

**parallel-code-review:**
- Runs security and Rails reviews concurrently
- Consolidates findings to avoid redundancy
- Provides prioritized feedback

**code-review-implementer:**
- Systematically addresses all feedback
- Applies common refactoring patterns
- Validates fixes with tests

## Project-Specific Conventions

This skill adheres to project guidelines from `CLAUDE.md`:

**Rails Patterns:**
- Service objects for business logic
- Result pattern for operations that can fail
- POODR principles (SRP, Tell Don't Ask, Law of Demeter)

**Multi-Tenant Security:**
- ActsAsTenant automatic scoping
- Tenant isolation verification
- No need for explicit tenant scoping in queries

**Testing:**
- RSpec with shoulda-matchers
- System specs for user workflows
- Avoid stubbing the system under test
- Use backdoor middleware for auth in request specs

**Code Style:**
- i18n for all user-facing text
- Timestamp columns instead of booleans
- Postgres enums for static values
- `ENV.fetch` for required environment variables

## Requirements

**Linear MCP Integration:**
- Linear MCP server must be configured and available
- Required tools: `mcp__linear__get_issue`, `mcp__linear__update_issue`, etc.

**Git Repository:**
- Current directory must be a git repository
- `main` branch exists and is up-to-date
- Git configured with user credentials

**Testing and Linting:**
- `bundle exec rspec` available for testing
- `bin/lint` script available for linting
- Ruby/Rails development environment configured

**GitHub CLI:**
- `gh` CLI tool installed and authenticated
- Repository configured for PR creation

**Skills:**
- `tdd-workflow` skill available
- `parallel-code-review` skill available
- `code-review-implementer` skill available

## Error Handling

**Common Issues and Solutions:**

**Linear Issue Not Found:**
- Verify issue ID format (e.g., `TRA-9`, not `tra-9`)
- Confirm Linear MCP integration is working
- Check user has access to the team/issue

**Branch Already Exists:**
- Expected behavior - workflow checks out existing branch
- Ensures work can be resumed safely
- Verifies branch is synced with remote

**Tests or Linting Fail:**
- Review failures and fix before creating PR
- Common linting issues: StandardRB, ERB Lint, Brakeman
- Never use `standardrb --fix` blindly - review changes

**Code Review Identifies Issues:**
- MUST address architectural feedback before PR
- Extract service objects as recommended
- Apply Result pattern where suggested
- Only create PR after all feedback implemented

## Example Workflow

**User Request:**
```
Implement TRA-142
```

**Skill Response:**
1. Fetches TRA-142 from Linear
2. Gathers additional context:
   - Searches Obsidian vault for "TRA-142" and related keywords
   - Fetches Sentry issue details (if referenced in Linear issue)
   - Retrieves GitHub PR discussions (if referenced in Linear issue)
3. Updates issue to "In Progress"
4. Creates branch `dg/tra-142-user-notification-service`
5. Analyzes requirements and creates plan (informed by gathered context)
6. Saves plan to memory graph
7. Presents plan: "This will create a new service object for user notifications using the Result pattern..."
8. **Waits for user approval**
9. Upon approval, invokes `tdd-workflow` skill
10. After implementation, invokes `parallel-code-review` skill
11. Reviews identify: "Extract notification logic to service object, apply Result pattern"
12. Invokes `code-review-implementer` skill to address feedback
13. Runs validation: `bundle exec rspec` ✅, `bin/lint` ✅
14. Creates logical commits with proper messages
15. Creates PR with comprehensive description and Linear linking
16. Presents completion checklist

**Final Output:**
- Working feature branch with complete implementation
- All tests passing
- All linting passing
- Comprehensive PR with Linear integration
- Issue automatically updated when PR merges

## Best Practices

**Planning Phase:**
- Take time to understand requirements fully
- Identify edge cases and error conditions
- Consider multi-tenant implications
- Plan for comprehensive system specs

**Implementation Phase:**
- Follow TDD strictly - tests before code
- Keep commits small and logical
- Write self-documenting code
- Use i18n for all user-facing text

**Review Phase:**
- Address ALL architectural feedback
- Don't skip recommended refactoring
- Validate fixes with tests
- Consider performance implications

**PR Creation:**
- Write comprehensive descriptions
- Document review findings and resolutions
- Include manual testing notes
- Ensure Linear linking is correct

**Quality Gates:**
- Never create PR with failing tests
- Never create PR with linting errors
- Never create PR without addressing architectural feedback
- Never skip validation steps
