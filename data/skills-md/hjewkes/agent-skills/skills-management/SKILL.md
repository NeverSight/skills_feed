---
name: skills-management
description: Use when creating, finding, installing, reviewing, or managing Claude Code skills — covers skill authoring, discovery, conventions, and lifecycle management
---

# Skills Management

Unified entry point for the entire skill lifecycle: finding existing skills, writing new ones, enforcing conventions, reviewing quality, and managing installations.

## Reference Files

Load the reference appropriate to your current task:

| Reference | When to load |
|-----------|-------------|
| [references/finding-skills.md](references/finding-skills.md) | Discovering and vetting skills from marketplaces and repos |
| [references/writing-skills.md](references/writing-skills.md) | TDD methodology for authoring new skills |
| [references/conventions.md](references/conventions.md) | Directory layout, naming rules, frontmatter requirements |
| [references/skill-manager-usage.md](references/skill-manager-usage.md) | CLI reference for the skill-manager script |
| [references/dispatch-prompt-template.md](references/dispatch-prompt-template.md) | 6-section template for agent dispatch prompts |
| [references/agent-skills-spec.md](references/agent-skills-spec.md) | Agent Skills open standard reference |
| [references/reviewing-skills.md](references/reviewing-skills.md) | Auditing skills for quality and portability |

## Writing-Skills Sub-References

The writing-skills reference has its own deep-dive files:

| Reference | Content |
|-----------|---------|
| [references/skill-structure.md](references/skill-structure.md) | SKILL.md structure, directory layout, file organization |
| [references/claude-search-optimization.md](references/claude-search-optimization.md) | CSO techniques, keyword coverage, token efficiency |
| [references/testing-methodology.md](references/testing-methodology.md) | Testing all skill types, rationalizations, bulletproofing |
| [references/skill-creation-checklist.md](references/skill-creation-checklist.md) | Complete TDD-adapted checklist |
| [references/anti-patterns.md](references/anti-patterns.md) | Anti-patterns with examples |
| [references/context-optimization-patterns.md](references/context-optimization-patterns.md) | Extracting oversized skills, plugin-to-skill conversion |

## Quick Decision

- **Need a capability?** Start with finding-skills to search before building
- **Building from scratch?** Use writing-skills (TDD methodology)
- **Unsure about structure?** Check conventions and agent-skills-spec
- **Auditing existing skills?** Use reviewing-skills
- **Managing installs?** Use skill-manager-usage
