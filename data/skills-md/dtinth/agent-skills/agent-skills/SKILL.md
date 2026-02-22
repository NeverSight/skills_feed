---
name: agent-skills
description: 'Use this when: (1) Creating a new project-specific skill to document project patterns, (2) Improving or updating an existing project skill, (3) Writing skill descriptions that will trigger other agents, (4) Organizing skill content for progressive disclosure, or (5) Learning what project-specific skills exist in .claude/skills/. Ensures skills follow project conventions and provide effective progressive disclosure.'
---

## What Skills Are

Skills are **maps, not territory**. They load relevant knowledge into context at the right moment without bloating the initial system prompt. A skill should provide enough context to work effectively without trying to be comprehensive documentation.

- **Purpose**: Progressive disclosure - load context on demand
- **Length**: Usually 60-100 lines of focused content
- **Structure**: Minimal front matter, practical content, pointers to where knowledge lives

## Project-Specific vs Global Skills

**Project-specific skills** (in repository `.claude/skills/`):
- Live in this project's repository
- Scope: Document this project's specific patterns, tools, and conventions (not generic best practices)
- Freely create, update, and maintain these skills
- To see what's available: `ls -la .claude/skills/`

**Globally-installed skills** (system-wide):
- Broader scope: Generic tools and workflows
- May be used across different projects and harnesses

**Finding a skill's base path**: When you invoke any skill, the skill harness prints the base directory at the start (e.g., "Base directory for this skill: /path/to/skill-name"). Use this to navigate to and edit the skill's files.

**Workflow for improving skills**:
- **Project-specific skills**: Update directly as needed to improve the project
- **Globally-installed skills**: Suggest improvements to the user and ask for confirmation before modifying, since these skills may be used across different projects and environments

## When to Create or Update a Project-Specific Skill

Create a project-specific skill when:
- Multiple agents will benefit from the same specialized knowledge
- The knowledge is project-specific (not generic tutorials)
- It addresses a common workflow or pattern (testing, i18n, deployment, etc.)
- It would otherwise be repeated across multiple system prompts

Update a project-specific skill when:
- Important patterns or workflows change
- Configuration files are updated
- New project conventions are established
- Existing guidance is incorrect or outdated

## Core Principles

### 1. Point to Real Code, Not Examples

- **DO**: "Study existing tests in `spec/controllers/` to understand patterns"
- **DON'T**: Include code examples that can become outdated
- **Exception**: Very short, unchanging snippets (bash commands, command syntax) are OK
- **Why**: Live code is authoritative; examples rot

### 2. Cite Sources with Traceability

- **DO**: Point to files where patterns are defined (`spec/rails_helper.rb`, `playwright.config.ts`, etc.)
- **DO**: Note important configuration details from actual files
- **DON'T**: Include line numbers (they change, create false precision)
- **Why**: Readers can verify and understand context

### 3. Verify Against Reality

- **Before writing**: Read actual configuration files and code
- **When uncertain**: Check the implementation rather than making assumptions
- **Test claims**: Ensure stated behavior matches actual behavior
- **Why**: Misinformation spreads through skills; verification prevents it

### 4. Accuracy Over Brevity

- **DO**: Use more words if it increases clarity
- **DO**: Distinguish between similar concepts clearly
- **DON'T**: Sacrifice precision for snappiness
- **Why**: "Queuing without executing" is clearer than "just queuing them"

### 5. Project-Specific Over Generic

- **DO**: Document how YOUR project does things ("we access helpers via App getters")
- **DON'T**: Include generic best practices ("separate your concerns")
- **DO**: Explain implementation details that aren't obvious from code
- **Why**: Generic advice is everywhere; project specifics are valuable

### 6. Scaffold Exploration

- **DO**: Say "study X to understand conventions"
- **DO**: Explain where to find patterns ("study existing files in in `spec/controllers/`")
- **DON'T**: Prescribe rules as if they're laws
- **Why**: Real learning happens when agents explore actual code

## Skill Structure

### Front Matter
```yaml
---
name: skill-name
description: 'Description that will be loaded into the system prompt. Must clearly state specific trigger points for when agents should use this skill. The description is the primary mechanism for triggering skill usage, so avoid generic statements like "use this for testing" and instead specify: "Use this when: (1) Running RSpec tests, (2) Debugging test failures, (3) Writing new test files."'
---
```

**Important**: The `name` must exactly match the folder name (e.g., folder `playwright-testing` → name `playwright-testing`).

### Content Organization

- **Start with context** - What is this skill about? When should it be used? What problems does it solve?
- **Organize by workflow or concept** - Use clear section headers, group related information, build from simple to complex
- **Point to implementation** - Reference actual files, directories, and where configuration lives
- **Suggest what to study** - Direct readers to real code patterns before working
- **End with important details** - Configuration notes, common patterns, edge cases, or constraints

## Common Mistakes to Avoid

1. **Over-Specification** - Don't include line numbers or overly specific implementation details that will change. Point to files and patterns instead.
2. **Stale Examples** - Don't include code examples in the body. Point readers to actual implementations to study.
3. **Generic Advice** - Don't include universal best practices. Document domain-specific patterns and conventions.
4. **Missing Context** - Always clarify why something is done a certain way, not just what to do.
5. **Ignoring Reality** - Verify all claims against actual code before writing. Misinformation spreads through skills.

## Writing Process

1. **Study existing skills** - Before creating a new skill, review existing skills in the project to understand conventions, style, and structure. This ensures consistency and prevents duplicating existing content.
2. **Understand the domain** - Study existing code, configuration, and patterns in the project
3. **Identify scope** - What specific knowledge should this skill contain?
4. **Map to sources** - Where in the codebase or documentation does this knowledge live?
5. **Write minimally** - What's the smallest amount of context needed?
6. **Verify claims** - Check that everything stated matches reality by reading actual code
7. **Cite sources** - Point readers to where they can learn more (files, directories, configurations)
8. **Study-driven guidance** - Direct people to real implementations, don't prescribe rules

## Maintenance

Skills should be updated when:
- Configuration files change (update file references, configuration notes)
- Patterns evolve (update guidance on how things are done)
- New tools or approaches are adopted (add sections for new workflows)
- Guidance is found to be incorrect (verify, fix, and understand why it was wrong)

Always verify changes against actual code before updating a skill.
