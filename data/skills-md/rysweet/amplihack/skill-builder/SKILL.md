---
name: skill-builder
version: 1.0.0
description: Creates, refines, and validates Claude Code skills following amplihack philosophy and official best practices. Automatically activates when building, creating, generating, or designing new skills.
---

# Skill Builder

## Purpose

Helps users create production-ready Claude Code skills that follow best practices from official Anthropic documentation and amplihack's ruthless simplicity philosophy.

## When I Activate

I automatically load when you mention:

- "build a skill" or "create a skill"
- "generate a skill" or "make a skill"
- "design a skill" or "develop a skill"
- "skill builder" or "new skill"
- "skill for [purpose]"

## What I Do

I orchestrate the skill creation process using amplihack's specialized agents:

1. **Clarify Requirements** (prompt-writer agent)
   - Understand skill purpose and scope
   - Define target users and use cases
   - Identify skill type (agent, command, scenario)

2. **Design Structure** (architect agent)
   - Plan YAML frontmatter fields
   - Design skill organization (single vs multi-file)
   - Calculate token budget allocation
   - Choose appropriate templates

3. **Generate Skill** (builder agent)
   - Create SKILL.md with proper YAML frontmatter
   - Write clear instructions and examples
   - Include supporting files if needed
   - Follow progressive disclosure pattern

4. **Validate Quality** (reviewer agent)
   - Check YAML frontmatter syntax
   - Verify token budget (<5,000 tokens core)
   - Ensure philosophy compliance (>85% score)
   - Test description quality for discovery

5. **Create Tests** (tester agent)
   - Define activation test cases
   - Create edge case validations
   - Document expected behaviors

## Skill Types Supported

- **skill**: Claude Code skills in `~/.amplihack/.claude/skills/` (auto-discovery)
- **agent**: Specialized agents in `~/.amplihack/.claude/agents/amplihack/specialized/`
- **command**: Slash commands in `~/.amplihack/.claude/commands/amplihack/`
- **scenario**: Production tools in `~/.amplihack/.claude/scenarios/`

See [examples.md](./examples.md) for detailed examples of each type.

## Command Interface

For explicit invocation:

```bash
/amplihack:skill-builder <skill-name> <skill-type> <description>
```

Examples in [examples.md](./examples.md).

## Documentation

**Supporting Files** (progressive disclosure):

- [reference.md](./reference.md): Architecture, patterns, YAML spec, best practices
- [examples.md](./examples.md): Real-world usage, testing, troubleshooting

**Original Documentation Sources** (embedded in reference.md):

1. **Official Claude Code Skills**: https://code.claude.com/docs/en/skills
2. **Anthropic Agent SDK Skills**: https://docs.claude.com/en/docs/agent-sdk/skills
3. **Agent Skills Engineering Blog**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
4. **Claude Cookbooks - Skills**: https://github.com/anthropics/claude-cookbooks/tree/main/skills
5. **Skills Custom Development Notebook**: https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/03_skills_custom_development.ipynb
6. **metaskills/skill-builder** (Reference): https://github.com/metaskills/skill-builder

All documentation is embedded in reference.md for offline access. Links provided for updates and verification.

---

**Note**: This skill automatically loads when Claude detects skill building intent. For explicit control, use `/amplihack:skill-builder`.
