---
name: skill-creator
description: "Guide for creating effective skills"
license: Complete terms in LICENSE.txt
progressive_disclosure:
  entry_point:
    summary: "Create modular skills that extend Claude with specialized knowledge, workflows, and tools through structured components"
    when_to_use: "When users want to create or update skills with specialized domain knowledge, workflows, or tool integrations. Focus on progressive disclosure for skills >150 lines."
    quick_start: "1. Understand skill with concrete examples 2. Plan reusable components (scripts/references/assets) 3. Initialize with init_skill.py 4. Edit SKILL.md and resources 5. Package and validate 6. Iterate based on usage"
  references:
    - skill-structure.md
    - creation-workflow.md
    - progressive-disclosure.md
    - best-practices.md
    - examples.md
---

# Skill Creator

## Overview

Create effective skills that extend Claude's capabilities through specialized knowledge, workflows, and tools. Skills are modular packages that transform Claude from a general-purpose agent into a specialized agent with procedural knowledge for specific domains.

**This skill exemplifies its own teachings** by using progressive disclosure to keep the entry point lean while providing deep detail in reference files.

## When to Use This Skill

Activate when:
- Creating a new skill from scratch
- Updating or refactoring an existing skill
- Adding progressive disclosure to monolithic skills
- Understanding skill structure and best practices
- Planning skill components (scripts, references, assets)
- Packaging skills for distribution

## Core Principles

1. **Example-Driven Design**: Start with concrete usage examples, not abstract concepts
2. **Progressive Disclosure**: Keep entry point <200 lines (optimal: 140-160), detailed content in references
3. **Reusable Components**: Extract scripts for repeated code, references for knowledge, assets for templates
4. **Imperative Voice**: Use verb-first instructions throughout (not second person)
5. **Purpose-Built Resources**: Each component should solve specific repetitive needs

## What Skills Provide

**Four Core Capabilities:**
1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

**Three-Level Loading System:**
1. Metadata (name + description) - Always in context (~100 words)
2. SKILL.md body - When skill triggers (<200 lines, optimal: 140-160)
3. Bundled resources - As needed by Claude (unlimited)

## Quick Start

### Six-Step Creation Process

**Step 1: Understand with Concrete Examples**
Gather 3-5 realistic usage examples. Ask: "What would users say to trigger this skill?" and "What tasks should it accomplish?" → [Complete guide](./references/creation-workflow.md#step-1-understanding-the-skill-with-concrete-examples)

**Step 2: Plan Reusable Components**
Analyze examples to identify: scripts (repeated code), references (domain knowledge), assets (templates). → [Planning guide](./references/creation-workflow.md#step-2-planning-the-reusable-skill-contents)

**Step 3: Initialize Skill**
Run `scripts/init_skill.py <skill-name> --path <output-directory>` to generate template structure. → [Initialization details](./references/creation-workflow.md#step-3-initializing-the-skill)

**Step 4: Edit Skill**
Implement scripts/references/assets, then update SKILL.md using imperative voice. Apply progressive disclosure if >150 lines. → [Editing guide](./references/creation-workflow.md#step-4-edit-the-skill)

**Step 5: Package and Validate**
Run `scripts/package_skill.py <path/to/skill-folder>` to validate and create distributable zip. → [Packaging guide](./references/creation-workflow.md#step-5-packaging-a-skill)

**Step 6: Iterate**
Use on real tasks, notice struggles, update skill accordingly. → [Iteration guide](./references/creation-workflow.md#step-6-iterate)

## Skill Anatomy

```
skill-name/
├── SKILL.md (required)           # Entry point with frontmatter + markdown
├── scripts/ (optional)           # Executable code (Python/Bash)
├── references/ (optional)        # Documentation loaded as needed
└── assets/ (optional)            # Templates, images, files for output
```

**Component Guidelines:**
- **Scripts**: When same code is repeatedly rewritten or deterministic execution needed
- **References**: For detailed specs, workflows, schemas, API docs (150-500 lines each)
- **Assets**: For templates, boilerplate, images, fonts used in outputs
- **Entry Point**: Core workflow, navigation, reminders (140-160 lines optimal)

→ [Complete structure guide](./references/skill-structure.md)

## Progressive Disclosure Pattern

**When to apply:** Skills >150 lines total

**Implementation:**
1. Add `progressive_disclosure` frontmatter with summary, when_to_use, quick_start
2. Reduce entry point to 140-160 lines (core workflow + navigation)
3. Create 3-5 reference files (150-500 lines each)
4. Organize by topic: structure, workflow, best practices, examples
5. Add navigation section linking all references

**Benefits:**
- Entry loads only essential content
- Deep detail available when needed
- Better organization and maintainability
- 20-30% reduction in entry point size

→ [Complete progressive disclosure guide](./references/progressive-disclosure.md)

**Meta-example:** This skill-creator demonstrates progressive disclosure:
- Entry: 150 lines (28% reduction from 209)
- References: 5 files with complete implementation details
- Recently optimized: mcp-builder (160 lines), testing-anti-patterns (140 lines)

## Navigation

### Core Concepts
- **[🏗️ Skill Structure](./references/skill-structure.md)** - Anatomy, components (scripts/references/assets), progressive disclosure architecture. Load when planning skill layout or understanding resource types.

### Step-by-Step Process
- **[🔄 Creation Workflow](./references/creation-workflow.md)** - Complete 6-step process from examples to iteration. Load when creating new skill or following structured workflow.

### Design Patterns
- **[📊 Progressive Disclosure](./references/progressive-disclosure.md)** - Three-level loading, implementation guide, anti-patterns, examples. Load when refactoring skills >150 lines or optimizing context usage.

### Quality Standards
- **[✅ Best Practices](./references/best-practices.md)** - Writing style, metadata quality, content organization, anti-patterns. Load when writing/reviewing skill content or ensuring quality.

### Real-World Examples
- **[📚 Examples](./references/examples.md)** - Complete skill examples: mcp-builder, testing-anti-patterns, pdf-editor, brand-guidelines, database-builder, frontend-builder. Load when starting new skill or seeking patterns.

## Key Reminders

- **Start with examples** - 3-5 concrete usage scenarios before designing
- **Use init script** - `scripts/init_skill.py` creates proper structure automatically
- **Imperative voice** - "To accomplish X, do Y" (not "should do X")
- **Progressive disclosure** - Entry <200 lines, details in references (for skills >150 lines)
- **Avoid duplication** - Information lives in ONE place (entry summary, reference detail)
- **Component clarity** - Scripts for code, references for knowledge, assets for templates
- **Validate before sharing** - `scripts/package_skill.py` validates and packages
- **Iterate continuously** - Use on real tasks, update based on struggles

## Red Flags - STOP

STOP when:
- "Let me write all the details in SKILL.md" → Move to references (progressive disclosure)
- "I'll use second person" → Switch to imperative voice
- "Same information in entry and reference" → Delete duplication
- Using generic description → Be specific about activation conditions
- Leaving example files from init script → Delete unused resources
- Skipping validation → Always run package_skill.py before sharing
- Creating skill without examples → Gather concrete usage scenarios first
- Entry point >200 lines → Apply progressive disclosure pattern

**ALL of these mean: STOP. Review principles and references.**

## Integration with Other Skills

**Meta-Skills:**
- **skill-creator** (this skill) - Creates other skills, demonstrates its own patterns

**Development Skills:**
- **mcp-builder** - Example of progressive disclosure implementation
- **testing-anti-patterns** - Example of ultra-lean entry point (140 lines)

**Workflow Skills:**
- **documentation** - Writing clear, structured content
- **verification-before-completion** - Testing skills before packaging

## Real-World Impact

From skill optimization experience:
- Progressive disclosure: 20-30% reduction in entry point size
- mcp-builder: 209 → 160 lines (23% reduction, 6 references)
- testing-anti-patterns: → 140 lines (ultra-lean with 4 references)
- skill-creator: 209 → 150 lines (28% reduction, 5 references)
- Context efficiency: Load only needed references (saves 50-80% context)
- Maintainability: Update specific references without touching entry point
- Clarity: Better organization improves discoverability and comprehension

---

**Remember:** Skills are modular packages that transform Claude into a specialized agent. Apply progressive disclosure for skills >150 lines. This skill demonstrates the pattern it teaches.
