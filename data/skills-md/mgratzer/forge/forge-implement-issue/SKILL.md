---
name: forge-implement-issue
description: Implement a feature or fix based on a GitHub issue, following project standards. Use when the user wants to start working on a GitHub issue, implement a feature, fix a bug, or begin coding from an issue number or URL.
disable-model-invocation: true
---

# Implement GitHub Issue

Implement a feature or fix based on a GitHub issue, following project standards.

## Input

The issue number or URL will be provided as: $ARGUMENTS

## Process

### Step 1: Fetch Issue Details

```bash
# Get issue details
gh issue view <ISSUE_NUMBER> --json number,title,body,labels,assignees,milestone,state,comments

# Check for sub-issues (tasks in the body with checkboxes)
# Look for patterns like: - [ ] task or - [x] completed task

# Check for linked issues or parent issues
gh api repos/{owner}/{repo}/issues/<ISSUE_NUMBER> --jq '.body'
```

### Step 2: Analyze the Issue

Parse and understand:
1. **Title**: What is being requested at a high level
2. **Description**: Detailed requirements, acceptance criteria
3. **Labels**: Use labels to understand the issue context:
   - **Type labels** (`bug`, `feature`, `enhancement`, `refactor`, `performance`, `security`, `testing`, `documentation`): What kind of work is this?
   - **Area labels** (e.g., `area: backend`, `area: frontend`, or project-specific areas): Which parts of the codebase are affected?
   - **Workflow labels** (`epic`, `discovery`, `blocked`): Special handling needed?
   - **Priority labels** (`priority: high`, `priority: low`): How urgent is this?
4. **Sub-issues/Tasks**: Checklist items that need to be completed
5. **Comments**: Additional context, clarifications, discussions
6. **Linked PRs/Issues**: Related work or dependencies

**If the issue is missing labels**, add appropriate ones before proceeding:
```bash
gh issue edit <ISSUE_NUMBER> --add-label "<type-label>" --add-label "<area-label>"
```

### Step 3: Assess Readiness

Evaluate if the issue is ready for implementation. Flag for user input if:

**Unclear Requirements:**
- Vague acceptance criteria
- Missing technical details
- Ambiguous scope

**Discovery Needed:**
- Issue has the `discovery` label (indicates research/spike work)
- Issue mentions "spike", "research", "investigate", "explore"
- Multiple valid implementation approaches
- Unknown technical feasibility

**Missing Information:**
- Referenced designs/specs not available
- Dependencies on other issues not completed
- Questions in comments not answered

**Scope Concerns:**
- Issue seems too large (should be broken down)
- Conflicting requirements
- Out of date with current codebase

If any flags are raised, use AskUserQuestion to clarify before proceeding:
```
Before implementing, I need clarification on:
1. <specific question>
2. <specific question>

How would you like to proceed?
```

### Step 4: Create Implementation Plan

Using TodoWrite, create a task list:
1. Break down the issue into discrete tasks
2. Identify files that need to be created/modified
3. Plan test coverage
4. Identify documentation updates needed

### Step 5: Validate Approach

Before writing code, confirm the implementation approach with the user:

1. **Present the planned approach** — Summarize in 3-5 bullet points:
   - Which files will be created or modified
   - Which libraries, APIs, or services will be used
   - Where configuration changes will live
   - Key design decisions (data flow, component boundaries)

2. **State scope boundaries** — Explicitly list what will NOT change to prevent scope creep

3. **Check the issue for implementation constraints** — If the issue includes an Implementation Constraints section (from `forge-create-issue`), follow those guardrails

4. **Get user confirmation** — Use AskUserQuestion:
   ```
   Here's my implementation approach:
   - <approach summary>

   Scope boundaries — I will NOT change:
   - <out-of-scope items>

   Does this look right, or should I adjust?
   ```

### Step 6: Create Feature Branch

```bash
# Detect the default branch (main, master, develop, etc.)
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'

# Ensure we're on the latest default branch
git fetch origin
git checkout <default-branch>
git pull origin <default-branch>

# Create feature branch with conventional naming
# Format: <type>/<issue-number>-<brief-description>
# Types: feat, fix, docs, refactor, test, chore
git checkout -b <type>/<issue-number>-<brief-description>
```

Branch naming examples:
- `feat/123-add-user-authentication`
- `fix/456-resolve-memory-leak`
- `docs/789-update-api-reference`

### Step 7: Implement the Solution

Follow CLAUDE.md guidelines strictly:

**Pre-flight Validation:**
Before writing feature code, verify your assumptions:
- If the project uses code generation (GraphQL codegen, OpenAPI generators, protobuf, etc.) — run it first and confirm the fields or types you plan to use actually exist
- If modifying configuration — grep the codebase for where the config is consumed to confirm you're placing values in the correct location
- If the implementation depends on external services or APIs — verify they're accessible and responding before building features on top of them
- If adding new environment variables — confirm they're set and accessible in the current environment

**Code Quality:**
- Follow the project's CLAUDE.md for architecture and layering conventions
- Run the project's lint/format commands (check CLAUDE.md or package.json scripts)
- Follow the project's type strictness conventions
- No hardcoded secrets - use environment variables

**Modularity & Reusability:**
- **Extract shared logic**: If the same logic appears in 2+ places, extract it to a utility function in `lib/`
- **Keep components focused**: Each component should do one thing well. If a file grows large (>200 lines) or handles multiple concerns, split it
- **Use named types**: Define types for function params/returns at API boundaries (3+ properties, used in multiple places)
- **Centralize constants**: Colors, thresholds, magic numbers → extract to shared constants or utility functions
- **Look for existing patterns**: Before writing new code, check if similar functionality exists that can be reused or extended

**Testability:**
- **Pure functions**: Extract logic into pure functions that are easy to unit test (no side effects, predictable outputs)
- **Dependency injection**: Pass dependencies as parameters rather than importing directly when it aids testing
- **Small, focused functions**: Functions that do one thing are easier to test than multi-purpose functions
- **Co-locate tests**: Place `*.test.ts(x)` files next to the code they test

**Avoid Over-Engineering:**
- Only make changes directly requested or clearly necessary
- Don't add features beyond what's asked
- Don't add comments/docstrings to unchanged code
- Minimum complexity for current task

**Granular Commits:**
After each logical unit of work:
```bash
git add <files>
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body explaining what and why>

Refs #<ISSUE_NUMBER>
EOF
)"
```

Commit types: feat, fix, docs, style, refactor, test, chore

Never add Co-Authored-By or any other attribution.

**Continuous Quality Checks:**
After each commit, run the project's test suite (or at minimum, tests for changed modules). Do not defer all testing to the Quality Gates step — catch failures early while context is fresh.

When writing tests, run each test immediately after writing it. Verify assertions match the actual output format exactly — do not assume output structure without checking.

### Step 8: Review for Modularity

Before moving on, review your implementation:

1. **Check for duplication**: Did you copy similar code in multiple places? Extract to a shared utility
2. **Component size**: Are any components >200 lines? Consider splitting into sub-components
3. **Utility candidates**: Are there pure functions that could live in `lib/` for reuse?
4. **Type definitions**: Are complex inline types repeated? Extract to named types
5. **Test coverage**: Can the core logic be unit tested independently?
6. **Pattern consistency**: If you changed a pattern in one file (e.g., error handling, component behavior, API call style), search for ALL files that use the same pattern and update them too. Do not fix one instance and leave others stale.
   ```bash
   grep -rn "<pattern-keyword>" src/
   ```

If refactoring is needed, do it now before tests lock in the structure.

### Step 9: Update Tests

- Co-locate `*.test.ts(x)` files next to implementations
- Mock external services at module boundaries
- Run the project's test command after adding tests
- Run coverage checks for substantial work (if available)
- **Test utilities separately**: If you extracted shared functions, add unit tests for them

### Step 10: Update Documentation

If behavior changed, update relevant docs:
- `/docs/*.md` files (architecture, API, etc.)
- `CHANGELOG.md` for user-facing features/fixes (write in plain language, skip internal changes)
- Code comments where logic isn't self-evident
- README if setup/usage changed
- CLAUDE.md if guidelines need updates

**Changelog Guidelines:**
- Only include user-facing changes (features users see, bugs they experienced)
- Write in plain language (no "API", "SSR", "cache" jargon)
- Use active voice: "Create shareable links" not "Shareable links were added"
- Group by category (e.g., Features, Fixes, Performance)
- Bold the feature name: **Feature name** - brief description

### Step 11: Quality Gates

Before creating PR, run all project quality checks. Discover available scripts from CLAUDE.md or `package.json` and run them. Typical checks include:
- Lint/format
- Type checking
- Tests
- Coverage (for substantial changes)

Fix any issues and commit the fixes.

### Step 11.5: Identify Manual Deployment Requirements

Review your changes and identify if ANY manual deployment steps are needed:

**Check for these indicators:**
- New entries in `.env.example` or references to new env vars → **Environment variable setup required**
- Changes to `docker-compose*.yml` → **Docker configuration changes required**
- New external service integrations → **API keys or service configuration required**
- Changes to routing, ports, or health checks → **Load balancer/proxy updates may be required**
- Database schema changes that can't auto-migrate → **Manual migration steps required**
- New dependencies on external services → **Infrastructure provisioning may be required**

**Document all manual steps** - you'll need these for the PR warning block in Step 13.

### Step 12: Push Changes

```bash
git push -u origin <branch-name>
```

### Step 13: Create Pull Request

**PR titles MUST use conventional commit format:**
```
<type>(<scope>): <description>
```

**Types:** feat, fix, docs, refactor, test, chore, perf
**Scope:** The affected area (e.g., auth, templates, api, frontend)

**IMPORTANT: Manual Deployment Steps Warning**

If the implementation requires ANY manual steps for deployment, add a prominent warning at the TOP of the PR body. Manual steps include:
- Adding or updating environment variables
- Changes to load balancer or reverse proxy configuration
- Docker Compose modifications
- Database migrations that need manual intervention
- Infrastructure changes (DNS, CDN, certificates)
- Third-party service configuration (API keys, webhooks)
- Feature flags that need to be enabled

```bash
gh pr create --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
<INCLUDE WARNING BLOCK IF MANUAL STEPS REQUIRED - SEE BELOW>

## Summary

Closes #<ISSUE_NUMBER>

<1-3 bullet points describing what was done>

## Changes

- <file/component>: <what changed>
- <file/component>: <what changed>

## Test Plan

- [ ] <how to test change 1>
- [ ] <how to test change 2>

## Checklist

- [ ] Code follows project guidelines (CLAUDE.md)
- [ ] Tests added/updated
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated for user-facing changes
- [ ] Lint/format checks pass
- [ ] Tests pass

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

**Warning Block Format (add at TOP of PR body when manual steps are required):**

```markdown
> [!WARNING]
> ## Manual Deployment Steps Required
>
> This PR requires the following manual actions before/after deployment:
>
> ### Environment Variables
> - [ ] Add `NEW_API_KEY` to production environment
> - [ ] Update `DATABASE_URL` connection string
>
> ### Infrastructure
> - [ ] Update load balancer health check path to `/api/health`
> - [ ] Add new DNS record for `api.example.com`
>
> ### Docker/Compose
> - [ ] Add new volume mount in `docker-compose.prod.yml`
>
> **Do not merge until these steps are planned and assigned.**
```

Only include sections that are relevant. The warning ensures reviewers and deployers are aware of required manual steps before merging.

### Step 14: Summary

Provide implementation summary:
- Branch name and PR link
- List of commits made
- Files changed
- Tests added/modified
- Documentation updated
- Any follow-up items or known limitations

## Important Guidelines

1. **Read CLAUDE.md first**: Understand project-specific requirements
2. **Explore before coding**: Use codebase-locator/analyzer agents to understand existing patterns
3. **Match existing style**: Follow conventions already in the codebase
4. **Small commits**: Each commit should be one logical change
5. **Test as you go**: Don't leave testing for the end
6. **Ask when unsure**: Better to clarify than to implement wrong
7. **Update todos**: Keep TodoWrite in sync with progress
8. **Don't scope creep**: Implement exactly what the issue asks, nothing more
9. **DRY principle**: Extract duplicated code into shared utilities in `lib/`
10. **Keep it testable**: Prefer pure functions; extract logic that can be unit tested independently

## Sub-Issue Handling

If the issue is part of a parent/sub-issue hierarchy (using GitHub's built-in sub-issues feature):

1. Check if this issue has a parent or sub-issues:
   ```bash
   # View issue details including parent/sub-issue relationships
   gh issue view <ISSUE_NUMBER>
   ```

2. Treat each sub-issue as a separate task in TodoWrite
3. Commit after completing each logical unit of work
4. When a sub-issue is complete, close it to automatically update the parent's progress:
   ```bash
   gh issue close <SUB_ISSUE_NUMBER>
   ```

**Note:** GitHub's sub-issue feature automatically tracks progress on parent issues when sub-issues are closed. No need to manually update issue bodies.

## Related Skills

**Before:** Use `forge-create-issue` to plan and create the issue.
**After implementing:** Use `forge-reflect-pr` to self-review before requesting review.
**After review:** Use `forge-address-pr-feedback` to address reviewer comments.
**After merging:** Use `forge-update-changelog` to document user-facing changes.
**Full workflow:** `forge-setup-project` → `forge-create-issue` → `forge-implement-issue` → `forge-reflect-pr` → `forge-address-pr-feedback` → `forge-update-changelog`

## Example Usage

```
/forge-implement-issue 123
/forge-implement-issue https://github.com/owner/repo/issues/123
```
