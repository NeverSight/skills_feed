---
name: skill-creator
description: Create new Agent Skills for Claude Code. Use when user wants to create a skill, add a new capability, document a CLI workflow, or asks how skills work.
---

# Skill Creator

Create modular Agent Skills that extend Claude's capabilities. Skills package expertise into discoverable folders containing instructions, scripts, and resources.

## When to Use

- "Create a skill for..."
- "Make a new skill"
- "Add a skill that..."
- "How do I create a skill?"
- "Document this workflow as a skill"

---

## Quick Start: Create a Skill

### 1. Choose Location

```bash
# Personal skill (all projects)
mkdir -p ~/.claude/skills/my-skill

# Project skill (shared via git)
mkdir -p .claude/skills/my-skill
```

### 2. Create SKILL.md

```markdown
---
name: my-skill
description: Brief description of what it does and when to use it.
---

# My Skill

## Instructions
Step-by-step guidance for Claude.

## Examples
Concrete usage examples.
```

### 3. Test It

Ask Claude a question that matches your description. Skills activate automatically based on context.

---

## SKILL.md Structure

### Required: YAML Frontmatter

```yaml
---
name: lowercase-with-hyphens    # Max 64 chars, [a-z0-9-] only
description: What it does AND when to use it. Include trigger keywords.
---
```

**Critical**: The `description` field determines when Claude discovers and uses your skill.

### Optional: Tool Permissions

```yaml
---
name: safe-reader
description: Read-only file access. Use for code review without modifications.
allowed-tools: Read, Grep, Glob
---
```

When `allowed-tools` is set, Claude can only use those tools without asking permission.

### Content Sections

```markdown
# Skill Name

Brief overview.

## Prerequisites
Installation or setup if needed.

## CLI Reference
Commands with examples.

## Common Workflows
Step-by-step procedures.

## Best Practices
Guidelines and tips.
```

---

## Skill Types

| Type | Location | Scope | Shared |
|------|----------|-------|--------|
| Personal | `~/.claude/skills/` | All your projects | No |
| Project | `.claude/skills/` | This repo | Yes (git) |
| Plugin | Via installed plugins | Per plugin | Via marketplace |

---

## Supporting Files

Add files alongside SKILL.md:

```
my-skill/
├── SKILL.md           # Required
├── reference.md       # Optional docs
├── examples/          # Optional examples
├── scripts/           # Optional utilities
│   └── helper.ts
└── templates/         # Optional templates
```

Reference from SKILL.md:
```markdown
See [reference.md](reference.md) for details.

Run the helper:
` ` `bash
bun scripts/helper.ts
` ` `
```

Claude reads supporting files only when needed (progressive disclosure).

---

## Writing Good Descriptions

**Bad** (too vague):
```yaml
description: Helps with data
```

**Good** (specific triggers):
```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when working with Excel files, .xlsx format, or spreadsheet analysis.
```

Include:
- What the skill does
- When to use it
- Key trigger words users might say

---

## Complete Example

### Create `~/.claude/skills/api-testing/SKILL.md`

```markdown
---
name: api-testing
description: Test REST APIs with curl and analyze responses. Use when testing endpoints, debugging APIs, or validating HTTP requests.
---

# API Testing

Test and debug REST APIs from the command line.

## Prerequisites

` ` `bash
# Verify curl is available
curl --version
` ` `

## CLI Reference

### Basic Requests
` ` `bash
curl -X GET "https://api.example.com/users"
curl -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John"}'
` ` `

### With Authentication
` ` `bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/protected"
` ` `

### Save Response
` ` `bash
curl -o response.json "https://api.example.com/data"
` ` `

## Common Workflows

### Test Endpoint Health
` ` `bash
# Check status code
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health

# Measure response time
curl -w "Time: %{time_total}s\n" -o /dev/null -s https://api.example.com
` ` `

## Best Practices

1. **Use -s for scripts** - Silent mode hides progress
2. **Use -f to fail** - Exit non-zero on HTTP errors
3. **Use jq for JSON** - Pipe to `jq` for pretty output
```

---

## Validation Checklist

Before considering complete:

- [ ] SKILL.md has valid YAML frontmatter
- [ ] Name is lowercase-with-hyphens (max 64 chars)
- [ ] Description includes what AND when (max 1024 chars)
- [ ] Instructions are clear and actionable
- [ ] CLI commands have explanatory comments
- [ ] Tested that Claude discovers and uses the skill

---

## Troubleshooting

### Claude doesn't use my skill

1. **Description too vague** - Add specific trigger keywords
2. **Wrong location** - Check path exactly matches conventions
3. **Invalid YAML** - Validate frontmatter syntax
4. **Restart needed** - Restart Claude Code after changes

### Check skill loads

```bash
# Verify file exists
cat ~/.claude/skills/my-skill/SKILL.md

# List all skills
ls ~/.claude/skills/*/SKILL.md
ls .claude/skills/*/SKILL.md
```

### Debug frontmatter

```bash
# View first 10 lines
head -n 10 ~/.claude/skills/my-skill/SKILL.md
```

Ensure:
- Opening `---` on line 1
- Closing `---` before content
- No tabs (use spaces)
- Strings with special chars are quoted

---

## Study Existing Skills

```bash
# See all personal skills
ls ~/.claude/skills/*/SKILL.md

# Good examples to study
cat ~/.claude/skills/beads/SKILL.md     # Task tracking CLI
cat ~/.claude/skills/gemini/SKILL.md    # AI research CLI
cat ~/.claude/skills/github/SKILL.md    # gh CLI patterns
```
