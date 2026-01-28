---
name: creating-skills
description: Guide for creating, testing, and deploying effective skills. Use when users want to create a new skill, update an existing skill, verify skills work before deployment, or extend Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Creating Skills

This skill provides guidance for creating effective skills using TDD methodology.

## Core Principles

### Skills ARE TDD for Documentation

1. **Write failing test first** - Run pressure scenario WITHOUT skill, document rationalizations
2. **Write minimal skill** - Address those specific failures
3. **Watch pass, refactor** - Find new loopholes, plug them, re-test

If you didn't watch an agent fail without it, you don't know what to teach.

### Concise is Key

The context window is a public good. **Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece: "Does Claude really need this explanation?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Examples |
|---------------|-------------|----------|
| High (text) | Multiple valid approaches, context-dependent | Heuristics, guidelines |
| Medium (pseudocode) | Preferred pattern exists, some variation OK | Configurable scripts |
| Low (scripts) | Fragile operations, consistency critical | Specific sequences |

## Quick Reference

| Phase | Action |
|-------|--------|
| RED | Run pressure scenario WITHOUT skill, document rationalizations |
| GREEN | Write minimal skill addressing those failures |
| REFACTOR | Find new loopholes, plug them, re-test |

| Skill Type | Test Focus |
|------------|------------|
| Technique | Recognition + application under pressure |
| Pattern | When to apply + when NOT to apply |
| Reference | Can agent find and use information? |

## When to Create

**Create when:** Technique wasn't obvious, applies broadly, others benefit
**Don't create for:** One-offs, standard practices, project-specific (use CLAUDE.md)

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded as needed
    └── assets/           - Files used in output (templates, icons, fonts)
```

### Frontmatter

```yaml
---
name: skill-name-with-hyphens
description: Use when [triggering conditions only, never workflow summary]
---
```

- **name**: Letters, numbers, hyphens only
- **description**: Primary triggering mechanism. Start "Use when...", max 1024 chars, third person
  - Include what the Skill does AND specific triggers/contexts for when to use it
  - Include ALL "when to use" here - NOT in the body (body loads only after triggering)
  - ❌ Workflow summaries create shortcuts - agent skips body

### Bundled Resources

| Directory | Purpose | When to Include |
|-----------|---------|-----------------|
| `scripts/` | Executable code | Same code rewritten repeatedly, deterministic reliability needed |
| `references/` | Documentation | Information Claude should reference while working |
| `assets/` | Output files | Templates, images, fonts used in final output |

**Avoid duplication**: Information lives in SKILL.md OR references, not both. Keep SKILL.md lean (<500 lines).

### What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- Setup/testing procedures, user-facing documentation
- Auxiliary context about creation process

## Skill Creation Process

1. **Understand** - Gather concrete usage examples
2. **Plan** - Identify reusable resources (scripts, references, assets)
3. **Initialize** - Run `scripts/init_skill.py <name> --path <dir>`
4. **Edit** - Implement resources, write SKILL.md
5. **Package** - Run `scripts/package_skill.py <path>`
6. **Iterate** - Test and refine based on real usage

### Step 1: Understanding with Examples

Ask questions like:
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

### Step 2: Planning Resources

For each example, analyze:
1. How to execute from scratch
2. What scripts, references, assets would help when repeating

### Step 3: Initializing

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates skill directory with SKILL.md template and example resource directories.

### Step 4: Editing

1. Start with reusable resources identified in planning
2. Test scripts by actually running them
3. Delete unused example files
4. Update SKILL.md (always use imperative/infinitive form)

### Step 5: Packaging

```bash
scripts/package_skill.py <path/to/skill-folder> [output-dir]
```

Validates and creates `.skill` file (zip with .skill extension).

### Step 6: Iterate

**STOP Before Next Skill**: After writing ANY skill, complete deployment before creating another. Untested skills = untested code.

## Progressive Disclosure

Keep SKILL.md body to essentials (<500 lines). Split content into separate files when approaching limit.

**Pattern 1: High-level guide with references**
```markdown
## Quick start
[code example]

## Advanced features
- **Feature A**: See [A.md](references/A.md)
```

**Pattern 2: Domain-specific organization**
```
references/
├── finance.md
├── sales.md
└── product.md
```

**Pattern 3: Conditional details**
```markdown
For simple edits, modify directly.
**For advanced feature**: See [ADVANCED.md](references/ADVANCED.md)
```

**Guidelines:**
- Avoid deeply nested references - keep one level deep from SKILL.md
- Structure longer files (>100 lines) with table of contents

## Anti-Patterns

| Pattern | Problem |
|---------|---------|
| ❌ Narrative | "In session 2025-10-03, we found..." (too specific) |
| ❌ Multi-language | example-js.js, example-py.py (maintenance burden) |
| ❌ Workflow in description | Creates shortcut, agent skips body |
| ❌ Batching skills | Test each before moving to next |

## References

### TDD & Testing
- [TDD Mapping](references/tdd-mapping.md) - RED-GREEN-REFACTOR cycle for skills
- [Skill Types](references/skill-types.md) - Technique, Pattern, Reference testing
- [Testing Methodology](references/testing-methodology.md) - Full checklist
- [Bulletproofing](references/bulletproofing.md) - Closing rationalization loopholes

### Structure & Design
- [Skill Structure](references/skill-structure.md) - Directory layout and template
- [CSO](references/cso.md) - Claude Search Optimization for discovery
- [Workflows](references/workflows.md) - Sequential workflows and conditional logic
- [Output Patterns](references/output-patterns.md) - Template and example patterns

## Related

- [sharing-skills](../sharing-skills/SKILL.md) - Contributing skills upstream
- [maestro-core](../maestro-core/SKILL.md) - Workflow routing and skill hierarchy
