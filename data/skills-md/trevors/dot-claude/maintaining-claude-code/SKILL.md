---
name: maintaining-claude-code
description: Validate and improve Claude Code configurations (CLAUDE.md, skills, commands, hooks). Use when auditing config quality, checking skill discoverability, organizing .claude directory, or deciding which entity type to use.
---

# Maintaining Claude Code

Validate, organize, and improve Claude Code configurations.

## Modes of Operation

### Audit Mode

**Use when**: Checking config quality, validating skills work

Checklist:

- CLAUDE.md: Specific, structured, actionable
- Skills: Valid YAML, good descriptions (What + When formula)
- Commands: Clear purpose, not duplicating skills
- Hooks: Proper exit codes, reasonable timeouts

### Organize Mode

**Use when**: .claude directory is messy, too many similar skills

Guidelines:

- Split CLAUDE.md into rules when >150 lines
- Consolidate similar skills (don't have 3 "code review" skills)
- Use subdirectories in rules/ for large projects

### Advise Mode

**Use when**: Deciding what entity type to create

Decision tree:

- Needs to run automatically before/after actions? -> **Hook**
- User explicitly triggers with /command? -> **Command**
- Claude should auto-detect and use? -> **Skill**
- Always-on behavioral guidance? -> **CLAUDE.md**
- Path-specific rules? -> **.claude/rules/**

## Quick Reference

### Entity Type Decision Matrix

| Need                       | Best Entity    | Alternative                    |
| -------------------------- | -------------- | ------------------------------ |
| Global behavior guidelines | CLAUDE.md      | Rules if >150 lines            |
| Path-specific rules        | .claude/rules/ | CLAUDE.md if universal         |
| User-invoked workflows     | Commands       | Skill if auto-detection wanted |
| Auto-detected capabilities | Skills         | Command if user should control |
| Pre/post action validation | Hooks          | Nothing else does this         |
| External API integration   | MCP Servers    | Bash calls if simple           |
| Task-specific personas     | Agents         | Skills for simpler cases       |

### Skill Description Formula

`<What it does>. Use when <trigger1>, <trigger2>, or <trigger3>.`

Good: "Extract text and tables from PDF files. Use when working with PDFs, forms, or document extraction."

Bad: "Helps with documents"

### YAML Validation

- `---` on line 1 (required)
- `name:` max 64 chars
- `description:` max 1024 chars, must include triggers
- `---` before content

### Common Anti-Patterns

- Vague descriptions: "Helps with stuff"
- Nested references: SKILL.md -> REF.md -> DETAILS.md
- Overloaded skills: Does 5 unrelated things
- Missing triggers: No "Use when..." clause

## Validation Steps

1. Check YAML syntax in all skills
2. Verify descriptions include trigger phrases
3. Ensure no duplicate capabilities across skills
4. Confirm CLAUDE.md content won't quickly grow stale
5. Check hooks have reasonable timeouts

## Resources

See [REFERENCE.md](REFERENCE.md) for detailed examples and troubleshooting.
