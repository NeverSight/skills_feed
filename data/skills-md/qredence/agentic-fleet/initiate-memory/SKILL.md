---
name: initiate-memory
description: Comprehensive guide for initializing or reorganizing agent memory and project context. Use when setting up a new project, when the user asks you to learn about the codebase, or when you need to create effective memory blocks for project conventions, preferences, and workflows.
---

# Initializing Memory

The user has requested that you initialize or reorganize your memory state for this project. This skill helps you systematically explore and document a codebase to build effective working memory.

## Understanding Your Context

**Important**: This skill is designed for stateful agents that work with users over extended periods. Your memory is not just a convenience; it's how you get better over time and maintain continuity across sessions.

This command may be run in different scenarios:

- **Fresh project**: Starting work on a new codebase
- **Existing project**: User wants you to reorganize or significantly update your understanding
- **Deep dive**: User wants comprehensive analysis of the project

Before making changes, inspect your current context and understand what already exists.

## What to Remember About a Project

### 1. Procedures (Rules & Workflows)

Explicit rules and workflows that should always be followed:

- "Never commit directly to main - always use feature branches"
- "Always run lint before running tests"
- "Use conventional commits format for all commit messages"
- "Always check for existing tests before adding new ones"

### 2. Preferences (Style & Conventions)

User and project coding style preferences:

- "Never use try/catch for control flow"
- "Always add JSDoc comments to exported functions"
- "Prefer functional components over class components"
- "Use early returns instead of nested conditionals"

### 3. History & Context

Important historical context that informs current decisions:

- "We fixed this exact pagination bug two weeks ago - check PR #234"
- "This monorepo used to have 3 modules before the consolidation"
- "The auth system was refactored in v2.0 - old patterns are deprecated"

## Memory Scope Considerations

Consider whether information is:

**Project-scoped**:

- Build commands, test commands, lint configuration
- Project architecture and key directories
- Team conventions specific to this codebase
- Technology stack and framework choices

**User-scoped**:

- Personal coding preferences that apply across projects
- Communication style preferences
- General workflow habits

**Session/Task-scoped**:

- Current branch or ticket being worked on
- Debugging context for an ongoing investigation
- Temporary notes about a specific task

## Recommended Memory Structure

### Core Information Categories

**Project Overview**: Your behavioral guidelines and project purpose

- Technology stack and architecture
- Key directories and their purposes
- Build/test/lint commands

**Conventions**: Project-specific rules and patterns

- Commit message format
- Code style preferences
- PR process and review guidelines

**User Preferences**: User-specific information

- Communication style preferences
- Cross-project preferences
- Working style and habits

### Optional Categories (Create as Needed)

**Current Task**: Scratchpad for current work item context

- Ticket ID, branch name, PR number
- Relevant links and context
- Current focus area

**Decisions**: Architectural decisions and their rationale

- Why certain approaches were chosen
- Trade-offs that were considered

## Research Depth

You can ask the user if they want a standard or deep research initialization:

**Standard initialization** (~5-20 tool calls):

- Scan README, package.json/config files, AGENTS.md, CLAUDE.md
- Review git status and recent commits
- Explore key directories and understand project structure
- Create/update your memory to contain the essential information

**Deep research initialization** (~100+ tool calls):

- Everything in standard initialization, plus:
- Use TodoWrite to create a systematic research plan
- Deep dive into git history for patterns, conventions, and context
- Analyze commit message conventions and branching strategy
- Explore multiple directories and understand architecture thoroughly
- Search for and read key source files to understand patterns

**What deep research can uncover:**

- **Contributors & team dynamics**: Who works on what areas? Who are the main contributors?
- **Coding habits**: When do people commit? What's the typical commit size?
- **Writing & commit style**: How verbose are commit messages? What conventions are followed?
- **Code evolution**: How has the architecture changed? What major refactors happened?
- **Pain points**: What areas have lots of bug fixes? What code gets touched frequently?

## Research Techniques

**File-based research:**

- README.md, CONTRIBUTING.md, AGENTS.md, CLAUDE.md
- Package manifests (package.json, Cargo.toml, pyproject.toml, go.mod)
- Config files (.eslintrc, tsconfig.json, .prettierrc)
- CI/CD configs (.github/workflows/, .gitlab-ci.yml)

**Git-based research** (if in a git repo):

- `git log --oneline -20` - Recent commit history and patterns
- `git branch -a` - Branching strategy
- `git log --format="%s" -50 | head -20` - Commit message conventions
- `git shortlog -sn --all | head -10` - Main contributors
- Recent PRs or merge commits for context on ongoing work

## How to Do Thorough Research

**Don't just collect data - analyze and cross-reference it.**

Shallow research (bad):

- Run commands, copy output
- Take everything at face value
- List facts without understanding

Thorough research (good):

- **Cross-reference findings**: If two pieces of data seem inconsistent, dig deeper
- **Resolve ambiguities**: Don't leave questions unanswered
- **Read actual content**: Don't just list file names - read key files to understand them
- **Look for patterns**: What do the commit messages tell you about workflow?
- **Form hypotheses and verify**: "I think this team uses feature branches" → check git branch patterns
- **Think like a new team member**: What would you want to know on your first day?

**Questions to ask yourself during research:**

- Does this make sense?
- What's missing?
- What can I infer?
- Am I just listing facts, or do I understand the project?

The goal isn't to produce a report - it's to genuinely understand the project and how to be an effective collaborator.

## Recommended Questions to Ask

Bundle these questions together when starting:

1. **Research depth**: "Standard or deep research (comprehensive, as long as needed)?"
2. **Identity**: "Which contributor are you?" (You can often infer from git logs)
3. **Related repos**: "Are there other repositories I should know about?"
4. **Communication style**: "Terse or detailed responses?"
5. **Any specific rules**: "Rules I should always follow?"

**What NOT to ask:**

- Things you can find by reading files ("What's your test framework?")
- Permission for obvious actions - just do them
- Questions one at a time - bundle them

## Your Task

1. **Ask upfront questions**: Bundle the recommended questions above
2. **Inspect existing context**: See what already exists in AGENTS.md, README, etc.
3. **Identify the user**: From git logs and their answers
4. **Research the project**: Explore based on chosen depth. Use TodoWrite for a systematic plan.
5. **Document findings**: Create notes or update project documentation
6. **Reflect and review**: Check for completeness and quality
7. **Ask user if done**: Check if they're satisfied or want you to continue

## Reflection Phase

Before finishing, do a reflection step:

1. **Completeness check**: Did you gather all relevant information?
2. **Quality check**: Are there gaps or unclear areas?
3. **Structure check**: Would this information make sense to your future self?

**After reflection**, summarize what you learned:

> "I've completed the initialization. Here's a brief summary of what I set up: [summary]. Should I continue refining, or is this good to proceed?"

Remember: Good memory management is an investment. The effort you put into organizing your knowledge now will pay dividends as you work with this user over time.
