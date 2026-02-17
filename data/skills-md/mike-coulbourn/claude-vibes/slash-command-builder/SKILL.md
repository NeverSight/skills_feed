---
name: slash-command-builder
description: Create custom slash commands for Claude Code including syntax, arguments, bash execution, file references, and frontmatter configuration. Use when creating slash commands, custom commands, .md command files, or when asked about command creation, /command syntax, or command best practices.
---

# Slash Command Builder

Create effective custom slash commands for Claude Code with proper structure, dynamic features, and best practices.

## Quick Reference

**Command File Location**:
- Project (shared): `.claude/commands/name.md`
- Personal (individual): `~/.claude/commands/name.md`

**Dynamic Features**:
- Arguments: `$ARGUMENTS` (all) or `$1`, `$2`, `$3` (positional)
- Bash execution: [execute: command] (requires `allowed-tools: Bash(...)`)
- File references: `@path/to/file`

**Frontmatter**: Optional YAML with `description`, `allowed-tools`, `argument-hint`, `model`

## The Slash Command Creation Workflow

### Phase 1: Requirements Gathering

Use AskUserQuestion to understand what they need:

1. **What should the command do?**
   - What task or prompt does it automate?
   - What's the expected outcome?

2. **Who will use it?**
   - Just you (personal command)
   - Your team (project command)

3. **Does it need dynamic inputs?**
   - Fixed prompt (no arguments)
   - User-provided values (arguments needed)
   - Context from system (bash execution)
   - File contents (file references)

4. **What tools should it access?**
   - Read-only analysis (Read, Grep, Glob)
   - Git operations (Bash(git:*))
   - Full access (default, no restrictions)

### Phase 2: Choose Scope

**Personal Command** (`~/.claude/commands/`):
- Your individual shortcuts
- Experimental commands
- Personal workflow automation
- Not shared with team

**Project Command** (`.claude/commands/`):
- Team-shared commands
- Standardized workflows
- Committed to git
- Available to all team members

### Phase 3: Design the Structure

Basic command structure:

```markdown
---
description: Brief description for /help
allowed-tools: Optional tool restrictions
argument-hint: Optional argument guidance
---

[Your prompt here]
```

**Decision tree**:
1. Start with basic prompt
2. Add arguments if needed ($ARGUMENTS or $1/$2)
3. Add bash execution if context needed ([execute: command])
4. Add file references if analyzing files (@path)
5. Add frontmatter for description and restrictions

### Phase 4: Implementation

#### Step 1: Create the file

```bash
# For project commands
touch .claude/commands/your-command.md

# For personal commands
touch ~/.claude/commands/your-command.md
```

The filename (without .md) becomes the command name.

#### Step 2: Write the command

Use templates from [templates/](templates/) directory:
- [basic-command.md](templates/basic-command.md) - Simple prompt
- [with-arguments.md](templates/with-arguments.md) - With dynamic inputs
- [with-bash.md](templates/with-bash.md) - With bash execution
- [with-files.md](templates/with-files.md) - With file references
- [complex-command.md](templates/complex-command.md) - All features combined

#### Step 3: Add frontmatter (recommended)

```yaml
---
description: What this command does (appears in /help)
allowed-tools: Read, Grep, Glob  # Optional restrictions
argument-hint: [arg1] [arg2]     # Optional user guidance
---
```

### Phase 5: Testing

1. **Verify command appears**:
   ```
   /help
   ```
   Look for your command in the list.

2. **Test basic invocation**:
   ```
   /your-command
   ```

3. **Test with arguments** (if applicable):
   ```
   /your-command arg1 arg2
   ```

4. **Test bash execution** (if applicable):
   - Verify commands execute
   - Check output appears in prompt

5. **Test file references** (if applicable):
   - Verify files load correctly
   - Check paths resolve

6. **Team testing** (for project commands):
   - Have teammates try it
   - Gather feedback
   - Iterate based on usage

### Phase 6: Iteration

Start simple, add complexity incrementally:

1. **First**: Basic prompt without dynamic features
2. **Test**: Verify it works
3. **Add**: One feature (arguments OR bash OR files)
4. **Test**: Verify new feature works
5. **Repeat**: Add next feature if needed

Don't try to add all features at once. Build incrementally.

## Common Command Patterns

### Pattern 1: Code Analysis

```markdown
---
description: Analyze code for [specific criteria]
allowed-tools: Read, Grep, Glob
argument-hint: [file-or-directory]
---

Analyze @$1 for:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

Provide specific findings with examples.
```

### Pattern 2: Git Workflow

```markdown
---
description: [Git operation] with context
allowed-tools: Bash(git:*)
---

## Current State

Branch: [execute: git branch --show-current]
Status: [execute: git status --short]

## Task

[What to do with this context]
```

### Pattern 3: Code Generation

```markdown
---
description: Generate [artifact] following patterns
allowed-tools: Read, Grep, Glob, Write
argument-hint: [what-to-generate]
---

## Existing Patterns

@[relevant examples]

## Task

Generate $ARGUMENTS following the patterns above.
```

### Pattern 4: Deep Analysis

```markdown
---
description: Deep analysis of [topic]
---

Think deeply about $ARGUMENTS considering:
1. [Aspect 1]
2. [Aspect 2]
3. [Aspect 3]

[Extended thinking triggered by keywords]
```

## Real-World Examples

See [examples/](examples/) for complete working examples:
- [git-workflows.md](examples/git-workflows.md) - Commit, PR, branch commands
- [code-analysis.md](examples/code-analysis.md) - Review, security, performance
- [code-generation.md](examples/code-generation.md) - Tests, docs, boilerplate

## Advanced Features

### Arguments: $ARGUMENTS vs $1/$2

**Use `$ARGUMENTS`** when:
- You want all input as a single block
- Free-form text (messages, descriptions)
- Don't need to reference parts separately

**Use `$1`, `$2`, `$3`** when:
- You need structured parameters
- Different parts used in different places
- Want to provide defaults for missing args

Example:
```markdown
# $ARGUMENTS approach
Explain $ARGUMENTS in detail.

# Positional approach
Review PR #$1 with priority $2 assigned to $3.
```

### Bash Execution

Execute commands BEFORE the prompt runs:

```markdown
---
allowed-tools: Bash(git:*)
---

Current branch: [execute: git branch --show-current]
Recent commits: [execute: git log --oneline -5]
```

**Requirements**:
1. Must include `allowed-tools: Bash(...)`
2. Use [execute: command] syntax (backticks required)
3. Output is captured and included in prompt

**Security**: Limit bash access with specific tool patterns:
```yaml
allowed-tools: Bash(git:*)          # Git only
allowed-tools: Bash(npm:*), Bash(git:*)  # npm and git
```

### File References

Include file contents with `@` prefix:

```markdown
Review @src/auth/login.js for security issues.
```

**Features**:
- Automatic CLAUDE.md inclusion from file's directory hierarchy
- Works with relative or absolute paths
- Directories show listing (not contents)

### Frontmatter Configuration

Complete frontmatter options:

```yaml
---
description: Brief description (required for /help and SlashCommand tool)
allowed-tools: Read, Grep, Glob, Bash(git:*)  # Optional restrictions
argument-hint: [file] [priority]              # Optional guidance
model: claude-3-5-haiku-20241022              # Optional model override
disable-model-invocation: false               # Optional, prevent auto-calling
---
```

## Best Practices

1. **Always include description**
   - Helps team understand command purpose
   - Required for SlashCommand tool
   - Appears in `/help`

2. **Use argument-hint for clarity**
   - Shows expected inputs
   - Self-documenting commands
   - Reduces user confusion

3. **Limit allowed-tools when appropriate**
   - Read-only commands: `Read, Grep, Glob`
   - Git-only: `Bash(git:*)`
   - Enhances security and safety

4. **Structure complex commands**
   - Use sections (Context, Task, Constraints)
   - Makes prompts easier to understand
   - Follows clear flow

5. **Reference project conventions**
   - Include `@CLAUDE.md` for standards
   - Reference example files
   - Ensures consistency

6. **Test incrementally**
   - Start simple, add features one at a time
   - Test each addition before next
   - Don't debug multiple features simultaneously

7. **Organize with subdirectories**
   - Group related commands
   - Cleaner file structure
   - Easier to maintain

8. **Commit project commands**
   - Share with team via git
   - Version control for commands
   - Team benefits from your work

## Common Issues and Solutions

### Issue: Command doesn't appear in /help

**Causes**:
- File not in correct location
- Missing .md extension
- Filename has invalid characters

**Solutions**:
- Check file is in `.claude/commands/` or `~/.claude/commands/`
- Verify `.md` extension
- Use lowercase-with-hyphens for filename

### Issue: Arguments not replacing

**Causes**:
- Typo in placeholder (`$ARGUMENT` instead of `$ARGUMENTS`)
- Not passing arguments when invoking
- Wrong syntax

**Solutions**:
- Double-check spelling: `$ARGUMENTS`, `$1`, `$2`
- Test with: `/command arg1 arg2`
- Verify placeholder exists in template

### Issue: Bash commands not executing

**Causes**:
- Missing `allowed-tools: Bash(...)` in frontmatter
- Wrong syntax (missing backticks)
- Command fails when run

**Solutions**:
- Add frontmatter: `allowed-tools: Bash(command:*)`
- Use correct syntax: [execute: command]
- Test command in terminal first

### Issue: File references not working

**Causes**:
- Missing `@` prefix
- File doesn't exist
- Wrong path

**Solutions**:
- Use `@path/to/file` syntax
- Verify file exists: `ls path/to/file`
- Try absolute path if relative fails

## Slash Commands vs Skills

**When to use each**:

| Use Slash Commands | Use Skills |
|---|---|
| Manual invocation (you decide when) | Automatic discovery (Claude decides when) |
| Simple prompt templates | Complex multi-file workflows |
| Quick, focused operations | Broad capabilities |
| Single .md file | Directory with multiple files |

**Example**:
- Slash command: `/commit` - You invoke when ready to commit
- Skill: `skill-builder` - Claude discovers when you mention Skills

Both complement each other in your workflow.

## Complete Syntax Reference

For detailed syntax documentation, see [reference/syntax-guide.md](reference/syntax-guide.md).

For best practices and patterns, see [reference/best-practices.md](reference/best-practices.md).

For troubleshooting help, see [reference/troubleshooting.md](reference/troubleshooting.md).

## Tips for Effective Commands

1. **Start with the simplest version** that works
2. **Add complexity only when needed** (YAGNI principle)
3. **Test with real scenarios** before sharing
4. **Include clear descriptions** in frontmatter
5. **Use tool restrictions** for safety
6. **Reference project conventions** with file refs
7. **Gather context** with bash execution
8. **Structure prompts** with clear sections
9. **Provide examples** in argument-hint
10. **Iterate based on usage** - improve over time

## Next Steps

After creating a command:

1. **Test thoroughly** with various inputs
2. **Share with team** (if project command)
3. **Document in CLAUDE.md** if it's a pattern others should know
4. **Create related commands** for connected workflows
5. **Refine based on feedback** - commands improve with use

---

**Remember**: Slash commands are user-invoked prompt templates. Start simple, test frequently, and add features incrementally. The best commands are clear, focused, and solve real workflow problems.
