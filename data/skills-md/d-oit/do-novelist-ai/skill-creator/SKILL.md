---
name: skill-creator
description: Create new Claude Code skills with proper directory structure, SKILL.md file, and YAML frontmatter. Use this skill when you need to create a new reusable knowledge module for Claude Code.
---

# Skill Creator

Create new Claude Code skills following the official format and best practices.

## Quick Reference

- **[Templates and Examples](templates-and-examples.md)** - Skill templates and complete creation examples

## When to Use

- Creating a new reusable knowledge module
- Adding specialized guidance for specific tasks
- Building domain-specific expertise into Claude Code
- Need to ensure proper skill format and structure

## Skill Structure

A Claude Code skill consists of:

```
.claude/skills/
└── skill-name/
    └── SKILL.md
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Clear description of what this skill does and when to use it (max 1024 chars)
---

# Skill Title

[Skill content in Markdown]
```

## Naming Requirements

**Skill Name Rules**:
- Lowercase letters only
- Numbers allowed
- Hyphens for word separation (no underscores)
- No spaces
- Max 64 characters
- Descriptive and clear

**Examples**:
- ✅ `episode-management`
- ✅ `test-debugging`
- ✅ `api-integration`
- ✗ `Episode_Management` (no uppercase, no underscores)
- ✗ `test debugging` (no spaces)

## Description Best Practices

The description is **critical** - Claude uses it to decide when to invoke the skill.

**Good Description Structure**:
```
[Action verb] [what it does] [when to use it]
```

**Examples**:

✅ Good:
```yaml
description: Debug and fix failing tests in Rust projects. Use this skill when tests fail and you need to diagnose root causes, fix async/await issues, or handle race conditions.
```

✅ Good:
```yaml
description: Implement new features systematically with proper testing and documentation. Use when adding new functionality to the codebase.
```

✗ Too vague:
```yaml
description: Helps with testing
```

✗ Missing when-to-use:
```yaml
description: Provides guidance on building APIs
```

## Skill Creation Process

### Step 1: Define Purpose

```markdown
What problem does this skill solve?
- Specific task: [e.g., "Deploy to production"]
- Domain: [e.g., "deployment", "testing", "documentation"]
- User need: [e.g., "Ensure safe deployments"]
```

### Step 2: Choose Name

```markdown
Skill name: [lowercase-with-hyphens]
- Descriptive: Clearly indicates purpose
- Concise: Not too long
- Unique: Doesn't conflict with existing skills
```

### Step 3: Write Description

```markdown
description: [Action] [what it does]. Use this when [specific scenarios].

Key elements:
1. Clear action (verb)
2. What problem it solves
3. When to invoke it
4. Keywords Claude can match on
```

### Step 4: Structure Content

**Recommended Sections**:

1. **Introduction**: Brief overview of skill purpose
2. **When to Use**: Specific scenarios for invocation
3. **Core Concepts**: Key knowledge needed
4. **Process/Workflow**: Step-by-step guidance
5. **Examples**: Concrete usage examples
6. **Best Practices**: Do's and don'ts
7. **Integration**: How this works with other skills/agents

**Content Guidelines**:
- Clear, concise language
- Actionable instructions
- Concrete examples
- Code snippets where helpful
- Checklists for processes
- Visual diagrams (ASCII art) for complex flows

### Step 5: Create Files

```bash
# Create directory
mkdir -p .claude/skills/skill-name

# Create SKILL.md with content
cat > .claude/skills/skill-name/SKILL.md << 'EOF'
---
name: skill-name
description: Your description here
---

# Skill Title

[Your skill content]
EOF
```

### Step 6: Test and Validate

**Validation Checklist**:
- [ ] Directory name matches skill name
- [ ] SKILL.md file exists
- [ ] YAML frontmatter is valid
- [ ] Name follows naming rules (lowercase, hyphens)
- [ ] Description is clear and specific (< 1024 chars)
- [ ] Content is well-structured
- [ ] Examples are provided
- [ ] Markdown is properly formatted

## Skill Templates

See **[templates-and-examples.md](templates-and-examples.md)** for complete templates including:

### Available Templates
1. **Process Skill** - Step-by-step workflows
2. **Knowledge Skill** - Domain expertise and concepts
3. **Tool Skill** - Tool usage and best practices

Each template includes:
- Full YAML frontmatter
- Recommended sections
- Example content
- Best practices structure

## Integration with Agent Creator

When creating skills that work with agents:

1. **Reference agents in skill**: Mention which agents use this skill
2. **Skill-agent coordination**: Ensure skill complements agent capabilities
3. **Invocation clarity**: Make clear when skill vs agent is appropriate

## Project-Specific Considerations

### For Rust Self-Learning Memory Project

**Domain-Specific Skills**:
- Episode management (start, log, complete)
- Pattern extraction and storage
- Memory retrieval optimization
- Turso/redb synchronization
- Async/Tokio patterns

**Skill Naming Convention**:
- `episode-[operation]` for episode-related skills
- `storage-[operation]` for storage operations
- `pattern-[operation]` for pattern handling
- `memory-[operation]` for memory operations

**Integration Requirements**:
- Reference AGENTS.md standards
- Include examples using project structure
- Consider self-learning memory tracking

## Skill Maintenance

### Updating Skills

When updating existing skills:
1. Preserve backward compatibility
2. Update description if scope changes
3. Add new sections without removing old ones
4. Update examples to reflect current best practices
5. Maintain clear version history in git

### Deprecating Skills

If a skill becomes obsolete:
1. Update description to indicate deprecation
2. Point to replacement skill
3. Keep file for backward compatibility
4. Consider removing after transition period

## Best Practices Summary

### DO:
✓ Write clear, specific descriptions
✓ Include concrete examples
✓ Structure content logically
✓ Use consistent formatting
✓ Test skill by using it
✓ Update README.md to list new skill
✓ Follow naming conventions

### DON'T:
✗ Use vague or generic descriptions
✗ Skip examples
✗ Make names too long or unclear
✗ Forget YAML frontmatter
✗ Use uppercase or underscores in names
✗ Exceed 1024 chars in description

## Validation Command

After creating a skill, validate it:

```bash
# Check structure
test -f .claude/skills/skill-name/SKILL.md && echo "✓ Structure correct"

# Check YAML frontmatter
head -n 5 .claude/skills/skill-name/SKILL.md | grep "^name:" && echo "✓ YAML valid"

# Check name format
[[ $(grep "^name:" .claude/skills/skill-name/SKILL.md | cut -d' ' -f2) =~ ^[a-z0-9-]+$ ]] && echo "✓ Name format correct"
```

## Quick Creation Script

```bash
#!/bin/bash
# create-skill.sh

SKILL_NAME=$1
DESCRIPTION=$2

if [ -z "$SKILL_NAME" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: ./create-skill.sh skill-name \"Skill description\""
    exit 1
fi

# Validate name format
if ! [[ "$SKILL_NAME" =~ ^[a-z0-9-]+$ ]]; then
    echo "Error: Skill name must be lowercase with hyphens only"
    exit 1
fi

# Create directory
mkdir -p ".claude/skills/$SKILL_NAME"

# Create SKILL.md
cat > ".claude/skills/$SKILL_NAME/SKILL.md" <<EOF
---
name: $SKILL_NAME
description: $DESCRIPTION
---

# ${SKILL_NAME^}

[Skill content goes here]

## When to Use

- [Scenario 1]
- [Scenario 2]

## Process

### Step 1: [Action]
[Instructions]

### Step 2: [Action]
[Instructions]

## Examples

### Example 1: [Name]
\`\`\`
[Example code or workflow]
\`\`\`

## Best Practices

✓ [Do this]
✗ [Don't do this]
EOF

echo "✓ Created skill: $SKILL_NAME"
echo "✓ Edit: .claude/skills/$SKILL_NAME/SKILL.md"
```

## Summary

Creating effective skills:
1. **Purpose**: Solve specific, well-defined problems
2. **Naming**: Clear, lowercase, hyphenated names
3. **Description**: Specific, actionable, includes when-to-use
4. **Structure**: Well-organized with clear sections
5. **Examples**: Concrete, realistic usage examples
6. **Testing**: Validate structure and use the skill

Skills are the foundation of Claude Code's knowledge. Well-designed skills make Claude more effective at autonomous task execution.

For complete templates and detailed examples, see **[templates-and-examples.md](templates-and-examples.md)**.
