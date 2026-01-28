---
name: claude-md-authoring
description: Creates and reviews CLAUDE.md configuration files for Claude Code. Applies HumanLayer guidelines including instruction budgets (~50 user-level, ~100 project-level), WHAT/WHY/HOW framework, and progressive disclosure. Identifies anti-patterns like using Claude as a linter for style rules.
---

# CLAUDE.md Authoring

## Quickstart

1. **Determine scope**: User-level (`~/.claude/`) or project-level (`.claude/`)?
2. **Apply WHAT/WHY/HOW framework** (project-level only)
3. **Keep instructions under budget**: ~50 for user-level, ~100 for project-level
4. **Never use Claude as a linter**: Style rules belong in tooling, not CLAUDE.md
5. **Validate with quality checklist** before finalizing

## Core Principle

> "The only thing that the model knows about your codebase is the tokens you put into it."

CLAUDE.md is the highest-leverage point for context transfer. Every instruction competes for limited attention. Include only what Claude cannot infer and must apply universally.

## Scope Decision

### User-Level (`~/.claude/CLAUDE.md`)

Applies to ALL projects. Include only:
- Personal working style preferences
- Relationship dynamics (pushback, honesty, communication)
- Universal philosophy (YAGNI, root-cause debugging)
- Proactiveness boundaries

Never include:
- Project-specific commands (build, test, lint)
- Tech stack details
- Style rules that vary by project
- Tool/framework references that don't exist everywhere

### Project-Level (`.claude/CLAUDE.md`)

Applies to ONE project. Use the WHAT/WHY/HOW framework:

**WHAT** (2-5 lines)
- Project purpose in one sentence
- Primary language/framework
- Key directories and their purposes

**WHY** (optional, 2-3 lines)
- Non-obvious architectural decisions
- Constraints that affect implementation choices

**HOW** (3-7 lines)
- Essential commands: build, test, lint, run
- Any project-specific workflows
- Where to find more documentation

## Instruction Budget

LLMs reliably follow ~150-200 instructions. Claude Code's system prompt uses ~50, leaving limited budget.

| Scope | Target | Maximum |
|-------|--------|---------|
| User-level | ~30-40 | 60 |
| Project-level | ~50-80 | 120 |
| Combined | ~80-120 | 150 |

**Counting instructions**: Each actionable directive counts as one instruction.
- "NEVER skip tests" = 1 instruction
- "Use TypeScript for new files" = 1 instruction
- A 5-item list = 5 instructions

## Anti-Pattern: Claude as Linter

❌ **Never rely on Claude for style enforcement:**
- Naming conventions with specific examples
- Comment formatting rules
- Whitespace/indentation requirements
- File header requirements (ABOUTME, copyright)

✓ **Use deterministic tools instead:**
- ESLint/Biome for JavaScript/TypeScript style
- Black/Ruff for Python formatting
- Pre-commit hooks for file headers
- Claude Code Hooks to run formatters

**Why this matters**: LLMs follow style rules inconsistently. A linter fails deterministically; Claude fails silently and unpredictably.

**Exception**: High-level philosophy is acceptable:
- ✓ "Names should describe purpose, not implementation"
- ❌ "Never use names like ZodValidator or MCPWrapper"

## Progressive Disclosure

For complex guidance, don't embed everything in CLAUDE.md.

**Pattern**: Reference external docs, let Claude decide relevance.

```markdown
## Reference Documentation
- Code conventions: See `docs/conventions.md`
- API patterns: See `docs/api-design.md`
- Testing philosophy: See `docs/testing.md`

Read these when the task involves the relevant area.
```

**Benefits**:
- Keeps CLAUDE.md focused
- Claude reads docs only when relevant
- Easier to maintain separate concerns

## Structure Template

### User-Level

```markdown
[Opening persona/philosophy - 1-2 lines]

## Working Together
[Relationship dynamics, communication preferences]

## Proactiveness
[When to proceed vs. pause for confirmation]

## Development Philosophy
[Universal principles: YAGNI, debugging approach, etc.]

## Guardrails
[Version control, testing principles - kept brief]
```

### Project-Level

```markdown
## Project Overview
[WHAT: Purpose, stack, structure]

## Development
[HOW: Build, test, lint commands]

## Architecture
[WHY: Key decisions, constraints - if non-obvious]

## Conventions
[Brief pointers to detailed docs if needed]
```

## Quality Checklist

Before finalizing, verify:

### Universal Applicability
- [ ] Every instruction applies to every session (user-level) or every task in project (project-level)
- [ ] No project-specific commands in user-level config
- [ ] No tool references that may not exist

### Instruction Economy
- [ ] Under instruction budget (count them)
- [ ] No redundancy with Claude Code's built-in behaviors
- [ ] Examples trimmed or moved to reference docs

### No LLM-as-Linter
- [ ] No specific naming convention examples
- [ ] No comment formatting rules
- [ ] No file header requirements
- [ ] Style guidance limited to philosophy, not specifics

### Progressive Disclosure
- [ ] Complex topics reference external docs
- [ ] Main file under 100 lines (user) or 150 lines (project)
- [ ] Examples in reference files, not inline

### Clarity
- [ ] Consistent heading hierarchy
- [ ] No conflicting instructions
- [ ] Actionable directives, not vague guidance

## Common Pitfalls

1. **Over-specification**: Including every preference instead of universally critical ones
2. **Style enforcement**: Detailed naming/comment rules that Claude follows inconsistently
3. **Stale commands**: Build/test commands that drift from actual tooling
4. **Auto-generation**: Using `/init` instead of hand-crafting
5. **Tool assumptions**: Referencing MCP servers or tools that aren't always available
6. **Conflicting rules**: "Match surrounding style" + "Never use X pattern"
7. **Instruction inflation**: Adding rules after each frustration instead of fixing root cause

## When to Skip This Skill

- Quick one-off projects (just use defaults)
- Projects with existing, well-maintained CLAUDE.md
- When the team already has established patterns

## Example: Before/After

**Before** (problematic user-level):
```markdown
## Naming
NEVER use names like ZodValidator, MCPWrapper, JSONParser...
[20 more lines of specific examples]

## Comments
All files MUST start with ABOUTME: header...
```

**After** (improved user-level):
```markdown
## Code Style
Names should describe purpose, not implementation details.
Use project linters for formatting; don't rely on manual enforcement.
```

*Why better*: Philosophy over specifics. Linter handles enforcement deterministically.

## Integration

After authoring CLAUDE.md:
- **User-level**: Symlink to `~/.claude/CLAUDE.md` or place directly
- **Project-level**: Commit to `.claude/CLAUDE.md` in repository root
- **Validation**: Start a new Claude Code session and observe if instructions are followed
