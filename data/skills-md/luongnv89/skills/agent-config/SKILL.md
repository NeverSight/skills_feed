---
name: agent-config
description: Create or update CLAUDE.md and AGENTS.md files following official best practices. Use when asked to create, update, audit, or improve project configuration files for AI agents, or when users mention "CLAUDE.md", "AGENTS.md", "agent config", or "agent instructions".
---

## User Input

```text
$ARGUMENTS
```

Consider user input for:
- `create` - Create new file from scratch
- `update` - Improve existing file
- `audit` - Analyze and report on current file quality
- A specific path (e.g., `src/api/CLAUDE.md` for directory-specific instructions)

## Step 1: Determine Target File

If not specified in user input, ask the user which file type to work with:

**CLAUDE.md** - Project context file loaded at the start of every conversation. Contains:
- Bash commands Claude cannot guess
- Code style rules that differ from defaults
- Testing instructions and preferred test runners
- Repository etiquette (branch naming, PR conventions)
- Architectural decisions specific to the project
- Developer environment quirks (required env vars)
- Common gotchas or non-obvious behaviors

**AGENTS.md** - Custom subagent definitions file. Contains:
- Specialized assistant definitions
- Tool permissions for each agent
- Model preferences (opus, sonnet, haiku)
- Focused instructions for isolated tasks

## CLAUDE.md Guidelines

Based on official Claude Code documentation.

### Core Principle

CLAUDE.md is a special file Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context **it cannot infer from code alone**.

### What to Include

| ✅ Include | ❌ Exclude |
|-----------|-----------|
| Bash commands Claude cannot guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

### Quality Test

For each line, ask: *"Would removing this cause Claude to make mistakes?"* If not, cut it.

If Claude keeps ignoring a rule, the file is probably too long and the rule is getting lost. If Claude asks questions answered in CLAUDE.md, the phrasing might be ambiguous.

### Example Format

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

### File Locations

- **Home folder (`~/.claude/CLAUDE.md`)**: Applies to all Claude sessions
- **Project root (`./CLAUDE.md`)**: Check into git to share with your team
- **Local only (`CLAUDE.local.md`)**: Add to `.gitignore` for personal overrides
- **Parent directories**: Useful for monorepos where both `root/CLAUDE.md` and `root/foo/CLAUDE.md` are pulled in automatically
- **Child directories**: Claude pulls in child CLAUDE.md files on demand

### Import Syntax

CLAUDE.md files can import additional files using `@path/to/import` syntax:

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

### Emphasis for Critical Rules

Add emphasis (e.g., "IMPORTANT" or "YOU MUST") to improve adherence for critical rules.

## AGENTS.md Guidelines

Custom subagents run in their own context with their own set of allowed tools. Useful for tasks that read many files or need specialized focus.

### Agent Definition Format

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

### Required Fields

- **name**: Identifier to invoke the agent
- **description**: What the agent does (helps Claude decide when to use it)
- **tools**: Comma-separated list of allowed tools (Read, Grep, Glob, Bash, Edit, Write, etc.)

### Optional Fields

- **model**: Preferred model (opus, sonnet, haiku)

### Best Practices for Agents

1. Keep agent instructions focused on a single domain
2. Be specific about what the agent should look for
3. Request concrete output formats (line references, specific fixes)
4. Limit tool access to what's actually needed

## Execution Flow

### For `create` or default:

1. Ask which file type (CLAUDE.md or AGENTS.md) if not specified
2. Analyze the project:
   - Check for existing files at standard locations
   - Identify technology stack, project type, development tools
   - Review README.md, CONTRIBUTING.md, package.json, etc.
3. Draft the file following guidelines above
4. Present draft for review
5. Write to appropriate location after approval

### For `update`:

1. Read existing file
2. Audit against best practices
3. Identify:
   - Content to remove (redundant, obvious, style rules)
   - Content to condense
   - Missing essential information
4. Present changes for review
5. Apply changes after approval

### For `audit`:

1. Read existing file
2. Generate a report with:
   - Assessment of content quality
   - List of anti-patterns found
   - Percentage of truly useful vs redundant content
   - Specific recommendations for improvement
3. Do NOT modify the file, only report

## Anti-Patterns to Avoid

**DO NOT include:**
- Code style guidelines (use linters/formatters)
- Generic best practices Claude already knows
- Long explanations of obvious patterns
- Copy-pasted code examples
- Information that changes frequently
- Instructions for specific one-time tasks
- File-by-file codebase descriptions

## Notes

- Run `/init` to generate a starter CLAUDE.md based on current project structure
- Treat CLAUDE.md like code: review it when things go wrong, prune it regularly
- Check CLAUDE.md into git so your team can contribute
- The file compounds in value over time as you refine it
