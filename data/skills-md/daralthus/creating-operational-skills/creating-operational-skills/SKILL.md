---
name: creating-operational-skills
description: Create new Claude Code skills following best practices. Use when the user asks to create a new skill, make a skill, or automate a workflow as a skill.
---

# Creating Operational Skills

## References

| Reference | Content |
|-----------|---------|
| [SKILL_STRUCTURE.md](references/SKILL_STRUCTURE.md) | File structure, YAML frontmatter, naming, examples |
| [BEST_PRACTICES.md](references/BEST_PRACTICES.md) | Authoring guidelines, degrees of freedom, patterns |
| [OPERATIONAL_TOOLS.md](references/OPERATIONAL_TOOLS.md) | Feature engineering: transforming knowledge into usable formats |

## Process

1. **Identify the workflow** - What task? What inputs/outputs? What references needed?
2. **Create folder** - `mkdir -p .claude/skills/<skill-name>/references`
3. **Write SKILL.md** - Keep under 500 lines, point to references
4. **Create reference files** - Split long content, add Contents sections
5. **Apply feature engineering** - Transform principles into usable formats ([OPERATIONAL_TOOLS.md](references/OPERATIONAL_TOOLS.md))
6. **Add scripts** - Place in `scripts/` folder if needed
7. **Update CLAUDE.md** - Add to Skills table
8. **Iterate with feedback** - Test, get user feedback, improve

## Iteration

Skills improve through use. After creating:

1. **Test with real tasks** - Does Claude use the skill? Does output meet expectations?
2. **Get user feedback** - Where did it fall short? What was confusing?
3. **Identify failure modes** - Generic output? Wrong decisions? Missed steps?
4. **Apply fixes**
5. **Repeat** - Skills evolve; first version is rarely final
