---
name: sharing-skills
description: Use when you've developed a broadly useful skill and want to contribute it upstream via pull request - guides process of branching, committing, pushing, and creating PR to contribute skills back to upstream repository
---

# Sharing Skills

## Core Principles

1. **Test before share** - Only share skills validated via creating-skills TDD process
2. **One skill per PR** - Each skill independently reviewable
3. **Broadly useful** - Not project-specific or experimental

## Quick Reference

```bash
# 1. Sync
git checkout main && git pull upstream main

# 2. Branch
git checkout -b "add-${skill_name}-skill"

# 3. Work
# Edit skills/your-skill-name/SKILL.md

# 4. Commit
git add skills/your-skill-name/
git commit -m "Add ${skill_name} skill"

# 5. Push + PR
git push -u origin "add-${skill_name}-skill"
gh pr create --repo <UPSTREAM_ORG>/<UPSTREAM_REPO> \
  --title "Add ${skill_name} skill" \
  --body "## Summary\n...\n## Testing\n..."
```

## When to Share vs Keep Personal

| Share | Keep Personal |
|-------|---------------|
| Applies broadly | Project-specific |
| Well-tested | Experimental/unstable |
| Others benefit | Contains sensitive info |
| Documented | Too narrow/niche |

## Prerequisites

- `gh` CLI installed and authenticated
- Working directory is your local skills clone
- Skill tested using creating-skills TDD process

## Anti-Patterns

- ❌ **Batching** - Multiple skills in one PR
- ❌ **Untested** - Sharing without baseline testing
- ❌ **Project-specific** - Personal conventions as universal skills
- ❌ **Incomplete docs** - Missing Overview, Quick Reference, Common Mistakes

## References

- [Workflow Example](references/workflow-example.md) - Complete async-patterns example

## Related

- [creating-skills](../creating-skills/SKILL.md) - REQUIRED: Create well-tested skills before sharing
- [maestro-core](../maestro-core/SKILL.md) - Workflow routing and skill hierarchy
