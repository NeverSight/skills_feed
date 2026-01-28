---
name: agents-md
description: Create or improve AGENTS.md files for AI coding agents. Use when user asks to create, improve, review, or optimize an AGENTS.md file (or CLAUDE.md). Also use when running /init on a new project, when asked about best practices for agent configuration files, or when troubleshooting agent behavior related to project context.
---

# AGENTS.md Skill

Create effective AGENTS.md files that onboard AI agents to codebases.

## Core Principles

### 1. AGENTS.md Is High-Leverage

AGENTS.md goes into every conversation with the agent. A bad line affects every task. Craft each line carefully.

### 2. Less Is More

- Frontier models follow ~150-200 instructions reliably
- Agent harnesses consume ~50 instructions in system prompts
- More instructions = uniform degradation across ALL instructions
- Target: <60 lines, <300 lines maximum

### 3. Universal Applicability Only

Include only what applies to EVERY task. Agents may ignore content deemed irrelevant to current task.

### 4. Agents Are In-Context Learners

Don't document what the agent can infer from code. Style, patterns, and conventions are learned from existing files.

### 5. Progressive Disclosure

Point to files instead of embedding everything. Let agents discover details when needed.

## Structure Template

```markdown
# AGENTS.md

## What This Is
[1-2 sentences: project purpose and type]

## Tech Stack
- **Runtime:** [e.g., Bun, Node, Python]
- **Framework:** [e.g., Astro, Next.js, Django]
- **Language:** [e.g., TypeScript strict mode]

## Quick Commands
```bash
[dev command]     # [description]
[build command]   # [description]
[test command]    # [description]
[lint command]    # [description]
```

## Project Map
```
[directory tree with brief annotations]
```

## Key Conventions
- [Only non-obvious, universally-applicable conventions]
- [Things the agent cannot infer from code]

## Verification
[How to verify changes are correct - primary feedback mechanism]
```

## What To Include

| Include | Why |
|---------|-----|
| Project purpose (WHY) | Agent needs to understand intent |
| Tech stack (WHAT) | Core tools and runtime |
| Essential commands (HOW) | Build, test, dev, lint |
| Project structure map | Navigation aid |
| Verification method | How to confirm success |
| Non-obvious conventions | Only what can't be inferred |

## What To Exclude

| Exclude | Why |
|---------|-----|
| Code style guidelines | Agent learns from existing code |
| Import patterns | Inferred from codebase |
| Formatting rules | Use linters, not LLMs |
| Detailed error handling | Context-dependent |
| Dependency descriptions | Agent reads package.json |
| Example code snippets | Become stale quickly |

## Workflow

### Creating New AGENTS.md

1. Read `package.json`, config files, and 2-3 representative source files
2. Identify: runtime, framework, language, key commands
3. Map project structure (top-level directories only)
4. Write draft using template above
5. Review: Is every line universally applicable?
6. Trim to essentials (<60 lines ideal)

### Improving Existing AGENTS.md

1. Read current AGENTS.md
2. Check line count - if >100 lines, needs trimming
3. Identify:
   - Style guidelines (REMOVE - agent learns from code)
   - Linter-like rules (REMOVE - use actual linters)
   - Task-specific instructions (MOVE to separate docs)
   - Stale/outdated info (REMOVE)
4. Verify remaining content is universally applicable
5. Ensure WHAT/WHY/HOW structure is clear

## Progressive Disclosure Pattern

For larger projects, keep AGENTS.md lean and point to detailed docs:

```markdown
## Documentation

For detailed information, read these files when relevant:
- `docs/architecture.md` - System design and data flow
- `docs/testing.md` - Test patterns and fixtures
- `docs/deployment.md` - CI/CD and release process
```

## Verification Checklist

Before finalizing, verify:

- [ ] Under 60 lines (strongly preferred) or under 100 lines (acceptable)
- [ ] Every line applies to ALL tasks
- [ ] No code style rules (agent learns from code)
- [ ] No formatting rules (use linters)
- [ ] Commands are correct and runnable
- [ ] Project map reflects current structure
- [ ] Clear verification method specified
