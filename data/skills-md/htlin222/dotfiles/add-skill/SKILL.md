---
name: add-skill
description: Create new Claude Code skills with proper structure. Use when user wants to add a skill, create a slash command, or automate a workflow. Fetches official docs and guides through skill creation.
---

# Add Skill (Meta Skill)

Create new Claude Code skills by fetching the latest official documentation and generating properly structured skill files.

## Workflow

### Step 1: Fetch Latest Documentation

Always fetch official docs first to ensure compliance with current spec:

```
WebFetch: https://code.claude.com/docs/en/skills
Prompt: Extract skill file format, required fields, naming rules, and best practices
```

If WebFetch fails due to length, use WebSearch:

```
WebSearch: "Claude Code skills SKILL.md format site:code.claude.com"
```

### Step 2: Gather Requirements

Ask user (use AskUserQuestion tool):

1. **Name**: What should this skill be called? (lowercase, hyphens only)
2. **Purpose**: What does it do? (1-2 sentences)
3. **Trigger**: When should Claude use it? (keywords, scenarios)
4. **Complexity**: Does it need scripts, or just instructions?

### Step 3: Create Skill Structure

```
~/.claude/skills/{skill-name}/
├── SKILL.md           # Required: Main instructions
├── scripts/           # Optional: Executable code
└── references/        # Optional: Detailed documentation
```

### Step 4: Generate SKILL.md

Use this template:

```markdown
---
name: {skill-name}
description: {What it does}. Use when {trigger conditions}.
---

# {Skill Title}

{Brief overview - what this skill helps accomplish}

## When to Use

- {Scenario 1}
- {Scenario 2}

## Instructions

{Step-by-step guidance for Claude to follow}

## Examples

**Input:** {example user request}
**Output:** {expected Claude behavior}
```

### Step 5: Validate

Before creating, verify:

- [ ] Name: 1-64 chars, lowercase letters/numbers/hyphens only
- [ ] Name: No leading/trailing `-`, no consecutive `--`
- [ ] Description: States WHAT + WHEN clearly
- [ ] SKILL.md: Under 500 lines (put details in references/)
- [ ] Directory name matches `name` field exactly

### Step 6: Create Files

```bash
mkdir -p ~/.claude/skills/{skill-name}
# Write SKILL.md using Write tool
```

### Step 7: Verify

```bash
ls -la ~/.claude/skills/{skill-name}/
cat ~/.claude/skills/{skill-name}/SKILL.md
```

Test with: `claude --debug` to check for loading errors.

## Naming Rules

| Rule                       | Valid           | Invalid       |
| -------------------------- | --------------- | ------------- |
| Lowercase only             | `my-skill`      | `My-Skill`    |
| Hyphens OK                 | `test-runner`   | `test_runner` |
| Numbers OK                 | `v2-helper`     | -             |
| No leading/trailing hyphen | `skill`         | `-skill-`     |
| No consecutive hyphens     | `my-skill`      | `my--skill`   |
| 1-64 characters            | `a` to 64 chars | empty or 65+  |

## Best Practices

1. **Description is key**: Claude uses it to decide when to invoke the skill
2. **Progressive disclosure**: Keep SKILL.md light, put reference docs in `references/`
3. **Always include examples**: Shows expected input/output
4. **Scripts must be referenced**: Mention them explicitly in SKILL.md
5. **Test immediately**: Use `claude /your-skill` to verify

## Quick Mode

For rapid creation, user can provide all info at once:

```
/add-skill name=my-skill purpose="Does X" trigger="when user asks for Y"
```

Parse and generate without interactive prompts.

## Resources

- Official docs: https://code.claude.com/docs/en/skills
- Anthropic skills repo: https://github.com/anthropics/skills
