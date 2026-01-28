---
name: skill-builder
description: Use when the user wants to create a new Claude Code skill, build a custom skill, or needs help structuring skill instructions. Guides users through creating properly formatted skills with YAML frontmatter, clear descriptions, and comprehensive instructions.
allowed-tools: Read, Write, Edit, Grep, Glob
model: sonnet
---

# Skill Builder Skill

## Purpose

This skill helps users create professional, well-structured Claude Code skills that follow official best practices. It guides through:
- Proper YAML frontmatter structure
- Effective skill descriptions (critical for auto-invocation)
- Complete instruction templates
- Tool restrictions and model selection
- File structure and organization

## When to Use

This skill should be invoked when:
- User says "create a skill", "build a skill", "make a new skill"
- User wants to convert documentation or prompts into a skill
- User needs help structuring skill instructions
- User asks about skill best practices
- User wants to improve an existing skill's description
- User mentions "skill template" or "skill example"

## Process

### 1. Understand the Intent

Ask the user:
- **What should the skill do?** (Purpose and capabilities)
- **When should it be invoked?** (Trigger conditions - critical!)
- **What scope?** (Personal or project)
- **Any tool restrictions?** (Security/safety)

### 2. Generate Skill Name

Based on the purpose, suggest a name that is:
- Lowercase with hyphens
- Descriptive and clear
- Max 64 characters
- Examples: `code-reviewer`, `api-builder`, `database-optimizer`

### 3. Craft Effective Description

**This is the most critical part!** The description determines when Claude invokes the skill.

**Requirements:**
- Max 1024 characters
- Must include WHAT the skill does
- Must include WHEN to use it
- Should include specific trigger keywords
- Should be action-oriented

**Good Example:**
```
Use when reviewing code for security vulnerabilities, performance issues, and best practices. Automatically checks for SQL injection, XSS, CSRF, and common bugs. Invoke for pull request reviews or code audits.
```

**Bad Example:**
```
Reviews code
```

### 4. Create Skill Structure

Generate a complete `SKILL.md` file with:

```markdown
---
name: skill-name
description: [Effective description with WHAT and WHEN]
allowed-tools: [Optional - only if restrictions needed]
model: [Optional - sonnet/opus/haiku, or omit for default]
---

# [Skill Name]

## Purpose

[Clear explanation of what this skill does and why it's useful]

## When to Use

This skill should be invoked when:
- [Specific trigger condition 1]
- [Specific trigger condition 2]
- [Specific trigger condition 3]

## Process

1. **Step 1**: [First action]
   - [Detail or substep]

2. **Step 2**: [Second action]
   - [Detail or substep]

3. **Step 3**: [Final action]
   - [Detail or substep]

## Output Format

[Describe what format the output should take]

## Best Practices

- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

## Examples

### Example 1: [Scenario name]

**Input**: [What the user provides]

**Process**: [How the skill handles it]

**Output**: [What the skill produces]

## Error Handling

- **[Error type]**: [How to handle]
- **[Error type]**: [How to handle]

## Notes

[Any additional context, warnings, or tips]
```

### 5. Determine File Location

**Personal skills** (available across all projects):
```
~/.claude/skills/skill-name/SKILL.md
```

**Project skills** (team-shared, version controlled):
```
.claude/skills/skill-name/SKILL.md
```

### 6. Create Supporting Files

If needed, create:
- `README.md` - Installation and usage docs
- `scripts/` - Executable scripts
- `materials/` - Reference materials, templates
- `.gitignore` - For project skills

### 7. Validate the Skill

Check:
- ✓ Name is lowercase-with-hyphens, max 64 chars
- ✓ Description includes WHAT and WHEN, max 1024 chars
- ✓ YAML frontmatter is valid
- ✓ Instructions are clear and comprehensive
- ✓ Examples are provided
- ✓ "When to Use" section has specific triggers

## Output Format

When creating a skill, provide:

1. **Skill metadata:**
   - Name: `skill-name`
   - Location: `path/to/skill/`
   - Scope: Personal or Project

2. **Complete SKILL.md file content**

3. **README.md content** (for documentation)

4. **Installation instructions:**
   ```bash
   # Commands to create the skill
   ```

5. **Testing guidance:**
   - How to verify it loaded
   - Example requests that should trigger it
   - How to refine if not auto-invoked

## Best Practices

### Description Writing

**Include trigger keywords:**
- "Use when...", "For...", "Invoke when..."
- Specific verbs: "reviewing", "building", "analyzing", "generating"
- Domain terms: "API", "database", "security", "tests"

**Be specific:**
- ❌ "Helps with code"
- ✅ "Use when reviewing JavaScript code for security vulnerabilities, performance issues, and React best practices"

### Tool Restrictions

Only restrict tools when necessary:

```yaml
# Read-only analysis skill
allowed-tools: Read, Grep, Glob

# Can modify files
allowed-tools: Read, Write, Edit, Grep, Glob

# Needs to run commands
allowed-tools: Read, Write, Edit, Bash

# Full access (omit field)
```

### Model Selection

```yaml
# Fast, efficient (simple tasks)
model: haiku

# Balanced (most tasks)
model: sonnet

# Most capable (complex reasoning)
model: opus

# Inherit from session (omit field)
```

### Scope Selection

**Choose Personal when:**
- Experimental or personal workflow
- Not relevant to team
- Contains personal preferences

**Choose Project when:**
- Team should use it
- Part of development workflow
- Standardizes team practices

## Examples

### Example 1: Create Code Review Skill

**User Request**: "Create a skill for reviewing pull requests"

**Response:**

I'll create a `code-reviewer` skill for comprehensive pull request reviews.

**Skill Metadata:**
- Name: `code-reviewer`
- Scope: Project (for team use)
- Location: `.claude/skills/code-reviewer/`

**Creating SKILL.md:**

[Generate complete SKILL.md with frontmatter and all sections]

**Installation:**
```bash
mkdir -p .claude/skills/code-reviewer
# [Write SKILL.md content]
```

**Testing:**
After restarting Claude Code, try:
- "Review this pull request"
- "Check this code for security issues"
- "Analyze this PR for problems"

**Refinement:**
If not auto-invoked, add more trigger keywords to the description like "code review", "PR review", "security audit".

### Example 2: Create Database Migration Skill

**User Request**: "I need a skill for generating database migrations"

**Response:**

I'll create a `db-migration-generator` skill that creates safe database migration files.

[Follow same pattern as Example 1]

### Example 3: Improve Existing Skill

**User Request**: "My skill isn't being invoked automatically"

**Response:**

Let me check your skill's description. The description is how Claude decides when to invoke the skill.

**Current description:** [Read from SKILL.md]

**Issues:**
- Too vague - doesn't specify WHEN to use
- Missing trigger keywords
- Doesn't explain capabilities

**Improved description:**
```yaml
description: Use when [specific trigger]. Handles [capabilities]. Invoke for [use cases].
```

**Next steps:**
1. Update description with these changes
2. Restart Claude Code
3. Test with requests containing trigger keywords

## Error Handling

- **Name conflicts**: Suggest alternative names
- **Description too vague**: Provide examples of specific descriptions
- **Invalid YAML**: Show correct format with proper spacing
- **Missing sections**: Add template sections
- **Too complex**: Break into multiple skills
- **Tool access issues**: Recommend appropriate `allowed-tools`

## Notes

- The description is THE MOST IMPORTANT field - it determines auto-invocation
- Skills are discovered automatically when Claude Code starts
- Use `/skills` command to see loaded skills
- Restart Claude Code after creating/modifying skills
- Test with explicit requests first: "Use the [skill-name] skill to..."
- Project skills override personal skills with same name
- Skills can reference files using relative paths
- Use forward slashes (/) for cross-platform compatibility

## Common Skill Types

### Analysis Skills (Read-only)
```yaml
allowed-tools: Read, Grep, Glob
```
Examples: code-reviewer, security-auditor, performance-analyzer

### Generation Skills (Write access)
```yaml
# Omit allowed-tools or include Write
```
Examples: api-builder, test-generator, migration-creator

### Automation Skills (With scripts)
```yaml
# Include Bash for script execution
```
Examples: deployment-helper, build-optimizer

### Reference Skills (With materials)
```yaml
# Include materials/ directory with templates
```
Examples: brand-checker, style-guide-validator

## Validation Checklist

Before finishing, verify:

- [ ] Name is valid (lowercase-hyphens, max 64 chars)
- [ ] Description is effective (includes WHAT and WHEN, max 1024 chars)
- [ ] YAML frontmatter is properly formatted
- [ ] "When to Use" section has 3+ specific triggers
- [ ] At least 1 detailed example provided
- [ ] Instructions are clear and actionable
- [ ] File paths use forward slashes
- [ ] Supporting files created if needed
- [ ] Installation instructions provided
- [ ] Testing guidance included

## Templates Available

Reference these templates from this skill's directory:

1. **code-reviewer** - Security and quality reviews
2. **api-builder** - REST/GraphQL endpoint creation
3. **test-generator** - Test suite generation
4. **documentation-writer** - Technical documentation
5. **performance-optimizer** - Performance analysis

Access templates at: `.claude/skills/skill-builder/templates/`

## Resources

- Official Skills Documentation: `../../docs/claude/skills/overview.md`
- Skill Builder Tools: `.claude/skills/skill-builder/build-skill.sh`
- Validator: `.claude/skills/skill-builder/utils/validate-skill.sh`
- Quick Start Guide: `.claude/skills/skill-builder/QUICK_START.md`
