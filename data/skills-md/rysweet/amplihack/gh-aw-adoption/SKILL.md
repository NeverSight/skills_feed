---
name: gh-aw-adoption
version: 1.0.0
description: Adopt GitHub Agentic Workflows (gh-aw) in any repository. Investigates existing workflows, identifies gaps, creates agentic workflows, and handles CI/merge issues. Auto-activates for gh-aw adoption, agentic workflow setup, or workflow automation requests.
source_urls:
  - https://github.com/github/gh-aw
  - https://github.com/github/gh-aw/blob/main/.github/aw/github-agentic-workflows.md
  - https://github.com/github/gh-aw/blob/main/.github/aw/create-agentic-workflow.md
auto_activates:
  - "adopt GitHub Agentic Workflows"
  - "implement gh-aw"
  - "add agentic workflows"
  - "automate repository workflows"
  - "set up gh-aw"
token_budget: 2000
---

# GitHub Agentic Workflows Adoption Skill

## Purpose

Guides you through adopting GitHub Agentic Workflows (gh-aw) in any repository by:

1. **Investigating** existing workflows and automation opportunities
2. **Prioritizing** which workflows to create based on repository needs
3. **Creating** production-ready agentic workflows in parallel
4. **Resolving** CI issues, merge conflicts, and integration problems
5. **Validating** workflows compile and follow best practices

This skill orchestrates the complete gh-aw adoption process, from zero to production-ready agentic automation.

## When to Use This Skill

Activate this skill when you want to:

- Adopt gh-aw in a repository that doesn't have agentic workflows
- Learn about available gh-aw workflow patterns from the gh-aw repository
- Create multiple agentic workflows efficiently
- Automate repetitive repository tasks (issue triage, PR labeling, security scans, etc.)
- Debug or upgrade existing agentic workflows
- **Troubleshoot workflow failures** (MCP server errors, permission issues, CI failures)

## Quick Start

**Basic usage:**

```
Adopt GitHub Agentic Workflows in this repository
```

**With specific goals:**

```
Adopt gh-aw to automate:
- Issue triage and labeling
- PR review reminders
- Security scanning
- Deployment automation
```

**Investigation only:**

```
Investigate what agentic workflows the gh-aw team uses
```

**Troubleshooting:**

```
My workflow is failing with "MCP server(s) failed to launch: docker-mcp"
```

```
Help me fix the "lockdown mode without custom token" error
```

## How It Works

### Phase 1: Investigation (15-20 minutes)

**Goal**: Understand what agentic workflows exist and what gaps your repository has.

**Steps**:

1. **Query gh-aw repository**: Use `gh api` to list all workflows in `github/gh-aw`
2. **Analyze workflows**: Read 5-10 diverse workflow files to understand patterns
3. **Categorize workflows**: Group by purpose (security, maintenance, automation, etc.)
4. **Identify gaps**: Compare against your repository's current automation
5. **Create priority list**: Rank workflows by impact and feasibility

**Output**: Markdown report with:

- List of all available workflow patterns
- Gap analysis for your repository
- Prioritized implementation plan (15-20 recommended workflows)

### Phase 2: Parallel Workflow Creation (30-45 minutes)

**Goal**: Create multiple production-ready agentic workflows simultaneously.

**Architecture**:

- Launch separate agent threads for each workflow
- Each agent creates workflow independently
- Central coordinator tracks progress and handles conflicts
- All workflows created in feature branches

**Workflow Creation Process** (per workflow):

1. Read reference workflow from gh-aw repository
2. Adapt to your repository's context and requirements
3. Create workflow file in `.github/workflows/[name].md`
4. Add comprehensive error resilience (API failures, rate limits, network issues)
5. Configure safe-outputs, permissions, tools appropriately
6. Create feature branch and commit
7. Report completion to coordinator

**Example parallel execution:**

```
Agent 1 → issue-classifier.md
Agent 2 → pr-labeler.md
Agent 3 → security-scanner.md
Agent 4 → stale-pr-manager.md
Agent 5 → weekly-summary.md
... (up to N agents in parallel)
```

### Phase 3: CI Diagnostics and Integration (15-30 minutes)

**Goal**: Ensure all workflows compile and pass CI checks.

**Common issues and resolutions**:

**Issue: Workflow compilation failures**

- Solution: Run `gh aw compile` and fix YAML syntax errors
- Common errors: Missing required fields, invalid tool names, permission issues

**Issue: Merge conflicts**

- Solution: Rebase feature branches on latest main/integration
- Strategy: Merge integration → feature branches in sequence

**Issue: CI/CodeQL failures**

- Solution: Ensure external checks pass before merging
- Use `gh pr checks` to monitor status

**Issue: Safe-output validation errors**

- Solution: Configure appropriate limits for each safe-output type
- Reference: Check gh-aw documentation for safe-output syntax

### Phase 4: Validation and Deployment (10-15 minutes)

**Goal**: Verify workflows are production-ready and merge to main.

**Validation checklist**:

- [ ] All workflows compile to `.lock.yml` files
- [ ] No YAML syntax errors
- [ ] Permissions follow least-privilege principle
- [ ] Safe-outputs configured with appropriate limits
- [ ] Network firewall rules specified
- [ ] Error resilience patterns implemented
- [ ] Workflows tested with `workflow_dispatch` events
- [ ] Documentation includes purpose and usage

**Deployment strategy**:

1. Merge feature branches to integration branch first (if exists)
2. Run CI checks on integration branch
3. Merge integration → main when all checks pass
4. Monitor first workflow executions for runtime errors

## Navigation Guide

### When to Read Supporting Files

**reference.md** - Read when you need:

- Complete gh-aw CLI command reference
- Detailed workflow schema and configuration options
- Security best practices and sandboxing details
- MCP server integration patterns
- Repo-memory configuration and usage

**examples.md** - Read when you need:

- Real workflow creation examples from actual adoption sessions
- Step-by-step implementation guides for specific workflow types
- Troubleshooting common errors with solutions
- Parallel agent orchestration patterns
- CI/CD integration examples

**patterns.md** - Read when you need:

- Production workflow architecture patterns
- Error resilience strategies (retries, fallbacks, circuit breakers)
- Safe-output configuration best practices
- Security hardening techniques
- Performance optimization tips

## Key Concepts

### GitHub Agentic Workflows (gh-aw)

**What it is**: CLI extension for GitHub that enables creating AI-powered workflows in natural language using markdown files with YAML frontmatter.

**Key features**:

- Write workflows in markdown, compile to GitHub Actions YAML
- AI engines: Copilot, Claude, Codex, or custom
- MCP server integration for additional tools
- Safe-outputs for structured GitHub API communication
- Sandboxed execution with bash and edit tools enabled by default
- Repo-memory for persistent agent state

### Workflow Structure

```markdown
---
on: [trigger events]
permissions: [required permissions]
engine: copilot | claude-code | claude-sonnet-4-5 | codex
tools: [tool configuration]
safe-outputs: [GitHub API output limits]
network: [firewall configuration]
---

# Workflow Name

[Natural language prompt for AI agent]
```

### Critical Configuration Elements

**Permissions**: Always use least-privilege

```yaml
permissions:
  contents: read
  issues: write
  pull-requests: write
```

**Safe-outputs**: Limit GitHub API mutations

```yaml
safe-outputs:
  add-comment:
    max: 5
    expiration: 1d
  close-issue:
    max: 3
```

**Network**: Explicit firewall rules

```yaml
network:
  firewall: true
  allowed:
    - defaults
    - github
```

### Error Resilience Patterns

**Always implement**:

- API rate limit handling (exponential backoff)
- Network failure retries (3 attempts with delays)
- Partial failure recovery (continue on error)
- Comprehensive audit trails (log all actions to repo-memory)
- Safe-output limit awareness (prioritize critical actions)

## Prerequisites

Before using this skill, ensure:

1. **gh CLI installed**: `gh --version`
2. **gh-aw extension installed**: `gh extension install github/gh-aw`
3. **Repository access**: Write permissions to create branches and PRs
4. **Authentication**: GitHub token with appropriate scopes
5. **Optional: Integration branch**: For staging workflow changes before main

## Repo Guardian: Featured First Workflow

**Repo Guardian** is the recommended first workflow to adopt in any repository. Ready-to-copy
templates are included in this skill directory:

- **`repo-guardian.md`** — The gh-aw agentic workflow (natural language prompt for the AI agent)
- **`repo-guardian-gate.yml`** — Standard GitHub Actions workflow that enforces agent findings as a blocking CI check

### What It Does

Reviews every PR for **ephemeral content that doesn't belong in the repo**:

- Meeting notes, sprint retrospectives, status updates
- Temporary scripts (`fix-thing.sh`, `one-off-migration.py`)
- Point-in-time documents that will become stale
- Files with date prefixes suggesting snapshots

Posts a PR comment with findings. Collaborators can override with `repo-guardian:override <reason>`.

### Quick Setup

```bash
# 1. Copy templates
mkdir -p .github/workflows
cp .claude/skills/gh-aw-adoption/repo-guardian.md .github/workflows/repo-guardian.md
cp .claude/skills/gh-aw-adoption/repo-guardian-gate.yml .github/workflows/repo-guardian-gate.yml

# 2. Compile the agentic workflow (pins the gh-aw version)
cd .github/workflows
gh aw compile repo-guardian

# 3. Add COPILOT_GITHUB_TOKEN secret (PAT with read:org + repo scopes)
# Repository Settings → Secrets and variables → Actions → New repository secret

# 4. Commit and push all three files
git add .github/workflows/repo-guardian.md \
        .github/workflows/repo-guardian.lock.yml \
        .github/workflows/repo-guardian-gate.yml
git commit -m "feat: Add Repo Guardian agentic workflow"
git push
```

---

## Common Workflows to Adopt

Based on analysis of 100+ workflows in the gh-aw repository, these are high-impact workflows to consider:

**Security & Compliance** (High Priority):

- `repo-guardian.md` - Block PRs containing ephemeral content (included as template — see above)
- `secret-validation.md` - Monitor secrets for expiration and leaks
- `container-security-scanning.md` - Scan container images for vulnerabilities
- `license-compliance.md` - Verify dependency licenses
- `sbom-generation.md` - Generate Software Bill of Materials

**Development Automation** (High Priority):

- `pr-labeler.md` - Automatically label PRs based on content
- `issue-classifier.md` - Triage and label issues
- `stale-pr-manager.md` - Close stale PRs with grace period
- `changelog-generator.md` - Auto-generate changelogs from commits

**Quality Assurance** (Medium Priority):

- `test-coverage-enforcer.md` - Block PRs below coverage threshold
- `mutation-testing.md` - Run mutation tests and report survivors
- `performance-testing.md` - Automated performance regression tests

**Maintenance & Operations** (Medium Priority):

- `agentics-maintenance.md` - Hub for workflow health monitoring
- `workflow-health-dashboard.md` - Weekly metrics and status reports
- `dependency-updates.md` - Automated dependency update PRs

**Team Communication** (Lower Priority):

- `weekly-issue-summary.md` - Weekly issue digest with visualizations
- `team-status-reports.md` - Daily team status updates
- `pr-review-reminders.md` - Nudge reviewers for stale reviews

## Troubleshooting

**Problem: gh-aw extension not found**

```bash
gh extension install github/gh-aw
gh aw --help
```

**Problem: Compilation errors**

```bash
gh aw compile --validate
gh aw fix --write  # Auto-fix some issues
```

**Problem: Workflow not executing**

- Check workflow file is in `.github/workflows/`
- Verify workflow has valid trigger (`on:` field)
- Check GitHub Actions logs for execution errors
- Ensure required secrets are configured

**Problem: Safe-output limits exceeded**

- Review safe-output configuration in workflow frontmatter
- Increase limits if appropriate
- Add prioritization logic to stay within limits

**Problem: Permission denied errors**

- Verify `permissions:` block in workflow frontmatter
- Check GitHub token has required scopes
- Ensure workflow has necessary repository permissions

## Anti-Patterns to Avoid

**❌ Don't**: Create monolithic workflows that do everything
**✅ Do**: Create focused workflows with single responsibilities

**❌ Don't**: Skip error handling and assume APIs always succeed
**✅ Do**: Implement retries, fallbacks, and comprehensive error logging

**❌ Don't**: Use overly broad permissions (`contents: write` everywhere)
**✅ Do**: Apply least-privilege principle to each workflow

**❌ Don't**: Hardcode repository-specific values in workflows
**✅ Do**: Use GitHub context variables (`${{ github.repository }}`)

**❌ Don't**: Create workflows without testing them first
**✅ Do**: Test with `workflow_dispatch` before enabling automated triggers

## Success Criteria

Your gh-aw adoption is successful when:

1. ✅ Repository has 10-20 production agentic workflows
2. ✅ All workflows compile without errors
3. ✅ CI/CD pipeline includes workflow validation
4. ✅ Workflows follow security best practices
5. ✅ Team understands how to create and modify workflows
6. ✅ Workflows handle errors gracefully and provide audit trails
7. ✅ Maintenance hub monitors workflow health
8. ✅ Documentation explains each workflow's purpose and usage

## Next Steps After Adoption

1. **Monitor workflow health**: Use `workflow-health-dashboard.md`
2. **Iterate based on feedback**: Adjust workflows as team needs evolve
3. **Create custom workflows**: Use patterns learned to build new automation
4. **Share learnings**: Document successful patterns for other repositories
5. **Upgrade workflows**: Keep gh-aw extension updated and apply migrations

---

## Documentation Structure (Diátaxis Framework)

This skill follows the Diátaxis documentation framework with four complementary resources:

1. **SKILL.md** (Tutorial/Overview): Getting started guide, quick reference, high-level concepts
2. **examples.md** (How-to guides): Step-by-step practical examples and troubleshooting solutions
3. **patterns.md** (Explanation): Understanding patterns, anti-patterns, and best practices
4. **reference.md** (Reference): Technical specifications, detailed configurations, troubleshooting reference

**For troubleshooting**:

- Start with **reference.md** to understand the error and root cause
- Check **examples.md** for step-by-step fix instructions
- Review **patterns.md** to avoid the anti-pattern in future workflows

---

**Note**: This skill automates the complete gh-aw adoption process. For manual control or specific phases, invoke the skill with explicit instructions (e.g., "gh-aw-adoption: investigation only").
