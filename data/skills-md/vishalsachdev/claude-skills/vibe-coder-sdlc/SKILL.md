---
name: vibe-coder-sdlc
description: This skill should be used when users want professional SDLC practices with automated git workflows, intelligent code review, and project management without rigid processes. Orchestrates specialized agents for feature development, branch management, language-specific code review, and GitHub integration. Ideal for developers who want to stay in flow while maintaining code quality.
license: MIT
metadata:
  agents: orchestrator,git-workflow,code-review,project-manager
  tech-stacks: python,typescript,javascript,go,rust,java,ruby,php
  auto-detection: true
---

# Vibe Coder SDLC

A flexible SDLC workflow system designed for developers who want professional practices without rigid processes. This skill orchestrates specialized agents to handle git workflows, code reviews, and project documentation while you stay in the zone.

## Purpose

This skill provides a complete SDLC workflow that:
- Manages feature branches and pull requests automatically
- Reviews code with language-specific best practices
- Tracks work in GitHub issues
- Maintains documentation
- Keeps you in flow without bureaucratic overhead

## When to Use This Skill

Use this skill when:
- Starting a new feature or bug fix
- Want automatic branch management and PR creation
- Need code review before merging to main
- Want to track work in GitHub issues automatically
- Building projects that need documentation but don't want to write it manually
- Working solo but want team-level quality practices
- Want git best practices without thinking about them

## Philosophy

**Stay in flow, ship quality code.** This skill handles the SDLC busywork so you can focus on building. It's opinionated enough to guide you, flexible enough to not get in your way.

## Core Components

This skill uses 4 specialized agents working together:

1. **Orchestrator Agent** - The conductor that coordinates everything
2. **Git Workflow Agent** - Handles branches, commits, and PRs
3. **Code Review Agent** - Reviews your code with tech-stack awareness
4. **Project Manager Agent** - Documents work and updates GitHub issues

## How It Works

### The Flow

```
1. You: "I want to add dark mode"
   ↓
2. Orchestrator: Creates plan, detects tech stack
   ↓
3. Git Agent: Creates feature branch 'feat/dark-mode'
   ↓
4. You + Claude: Build the feature
   ↓
5. Git Agent: Commits, pushes, creates PR
   ↓
6. Review Agent: Reviews code with language-specific checks
   ↓
7. PM Agent: Updates docs, creates/updates GitHub issue
   ↓
8. Git Agent: Merges PR if review passes
```

### Tech Stack Awareness

**Key Feature**: The orchestrator and review agent are tech-stack aware:

- **Auto-detection**: Checks `package.json`, `requirements.txt`, `go.mod`, etc.
- **Smart reviews**: Applies Python PEP 8 to Python, Go patterns to Go, TypeScript best practices to TS
- **Multi-language**: Handles microservices with different languages in same PR
- **Ask when unclear**: If detection fails, ask the user once
- **Remember for session**: Store tech stack info to avoid repeated questions

## Workflow Phases

### 1. Plan Phase
- Understand what needs to be built
- Break it down into steps
- Create a todo list
- Detect or ask about tech stack (if not already known)

### 2. Setup Phase
- Use git-workflow-agent to create feature branch
- Branch name format: `feat/`, `fix/`, `refactor/`, `docs/`

### 3. Development Phase
- Help user build the feature
- Make commits with clear messages
- Keep the user in flow - don't over-document

### 4. Review Phase
- Use git-workflow-agent to push and create PR
- Use code-review-agent to review the code
  - Agent detects tech stack from repo/PR
  - Applies language-specific best practices
- If issues found: fix them before merge
- Add review comments to the PR

### 5. Documentation Phase
- Use project-manager-agent to:
  - Create/update GitHub issue tracking this work
  - Update relevant documentation
  - Add summary comments to PR

### 6. Merge Phase
- If review passes: use git-workflow-agent to merge
- Delete feature branch
- Celebrate! 🎉

## Agent Setup

To use this skill, set up the 4 agents in your project's `.claude/agents/` directory:

### Required Agents

1. **sdlc-orchestrator** - See [Orchestrator Agent Guide](references/orchestrator-agent.md)
2. **git-workflow-agent** - See [Git Workflow Agent Guide](references/git-workflow-agent.md)
3. **code-review-agent** - See [Code Review Agent Guide](references/code-review-agent.md)
4. **project-manager-agent** - See [Project Manager Agent Guide](references/project-manager-agent.md)

Each reference guide contains the complete agent definition ready to copy into your `.claude/agents/` directory.

## Quick Start

### Step 1: Copy Agent Files

```bash
# In your project root
mkdir -p .claude/agents

# Copy the 4 agent definitions from this skill's references/ folder
# to your project's .claude/agents/ folder
```

### Step 2: Install GitHub CLI

```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli

# Authenticate
gh auth login
```

### Step 3: Start Using

```
"Hey Claude, let's use the vibe-coder-sdlc skill to add [feature]"
```

The agents handle the process, you handle the code.

## Usage Examples

### Example 1: Simple Feature Addition

**User**: "Add a search bar to the homepage"

**Workflow**:
1. Git Agent: Create branch 'feat/homepage-search'
2. [User builds the feature]
3. Git Agent: Commit and push, create PR
4. Review Agent: Review code (approved)
5. PM Agent: Create issue #45, update README, update CHANGELOG
6. Git Agent: Merge PR, close issue

### Example 2: Bug Fix

**User**: "Login form not working on mobile"

**Workflow**:
1. Git Agent: Create branch 'fix/mobile-login'
2. [User fixes the bug]
3. Git Agent: Commit and push, create PR
4. Review Agent: Review code (request changes - missing test)
5. [User adds test]
6. Review Agent: Re-review (approved)
7. PM Agent: Create issue #46, add PR description
8. Git Agent: Merge PR, close issue

### Example 3: Multi-Language Project (Microservices)

**User**: "Add a new API endpoint in the Go service and update the TypeScript frontend to use it"

**Workflow**:
1. Git Agent: Create branch 'feat/new-api-endpoint'
2. [User builds Go API endpoint]
3. Review Agent: Detects Go, applies Go-specific checks
4. [User updates TypeScript frontend]
5. Review Agent: Detects TypeScript, applies TS-specific checks
6. Git Agent: Create PR
7. Review Agent: Reviews both Go and TypeScript changes
8. PM Agent: Updates docs for both services
9. Git Agent: Merge PR

### Example 4: First Time in a New Repo

**User**: "Add dark mode to the app"

**Workflow**:
1. Orchestrator detects tech stack:
   - Finds package.json → Node.js/TypeScript
   - Finds next.config.js → Next.js detected
   - Stores: "TypeScript + Next.js + React"
2. Git Agent: Create branch 'feat/dark-mode'
3. [User builds dark mode]
4. Review Agent: Uses TypeScript + React checklist
5. Git Agent: Create PR
6. PM Agent: Updates README with dark mode info
7. Git Agent: Merge PR

## Configuration

### Customize for Your Workflow

Create `.claude/sdlc-config.json`:

```json
{
  "branchNaming": {
    "feature": "feat/",
    "bugfix": "fix/",
    "refactor": "refactor/",
    "docs": "docs/"
  },
  "commitConvention": "conventional",
  "reviewRequired": true,
  "autoMerge": false,
  "documentation": {
    "updateChangelog": true,
    "updateReadme": true,
    "requireTests": true
  },
  "github": {
    "createIssues": true,
    "linkPRsToIssues": true,
    "addLabels": true
  }
}
```

## Supported Tech Stacks

The code review agent automatically detects and applies best practices for:

- **Python**: PEP 8, type hints, context managers
- **TypeScript/JavaScript**: ESLint, proper types, async patterns
- **Go**: Error handling, context usage, goroutine management
- **Rust**: Ownership, clippy lints, error handling
- **Java**: Exception handling, streams, null safety
- **Ruby**: RuboCop, ActiveRecord patterns
- **PHP**: PSR standards, prepared statements

See [Code Review Agent Guide](references/code-review-agent.md) for complete language-specific checklists.

## Best Practices

### 1. Keep PRs Small
- Easier to review
- Faster to merge
- Less risky

**Good**: "Add user avatar display"
**Bad**: "Redesign entire user profile system"

### 2. Write Commits for Future You
Six months from now, you'll want to know WHY you made changes.

**Good**: `fix(auth): handle expired tokens by redirecting to login`
**Bad**: `fix bug`

### 3. Review Your Own Code First
Before the review agent runs, do a self-review:
```bash
gh pr diff <number>
```

### 4. Document As You Go
Don't leave documentation for "later." Update docs in the same PR.

### 5. Use Labels Effectively
```
priority: high/medium/low
type: bug/feature/refactor
status: in-progress/review/blocked
area: frontend/backend/db
```

### 6. Link Everything
- PR mentions issue: "Closes #123"
- Commits reference issues: "feat: add search (ref #123)"
- Issues reference PRs: "Implemented in PR #456"

## Troubleshooting

### "Agent not responding"
Check that agent files exist in `.claude/agents/`

### "gh command not found"
Install GitHub CLI (see Quick Start)

### "Can't create PR"
Make sure you're authenticated:
```bash
gh auth status
gh auth login
```

### "Review agent too strict"
Adjust review agent instructions to match your needs. It's your workflow!

### "Too much overhead"
Skip steps that don't add value:
- Turn off auto-issue creation
- Skip changelog for small changes
- Disable review for docs-only changes

## Advanced Usage

### CI/CD Integration

Add to your `.github/workflows/pr-check.yml`:

```yaml
name: PR Checks
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test
      - name: Run linter
        run: npm run lint
```

### Custom Review Rules

Extend the review agent for your stack. See [Code Review Agent Guide](references/code-review-agent.md) for customization examples.

### Team Workflows

For teams, add these practices:
- Require PR approvals from teammates
- Add CODEOWNERS file
- Use branch protection rules
- Set up required status checks

## Philosophy Recap

This skill is built on these principles:

1. **Quality without bureaucracy** - Professional practices, minimal overhead
2. **Automation over documentation** - Let agents handle busywork
3. **Flexibility over rigidity** - Adapt to your style
4. **Flow over process** - Don't interrupt creative work
5. **Ship over perfect** - Done and good beats perfect and never

## Next Steps

Once you've used this skill:

1. **Customize the agents** - Make them match your workflow
2. **Add your own agents** - Create specialized agents for your stack
3. **Share with your team** - Adapt for team workflows
4. **Iterate** - This is a starting point, make it yours

---

**Built for vibe coders who want to ship quality code without the SDLC headaches.**
