---
name: tkr-skill-writer
description: Guide for creating and structuring skills with consistent formatting, clear documentation, and proper reference organization. Use when creating new skills or updating existing skill documentation.
---

# TKR Skill Writer

## Description and Goals

This skill provides guidelines and templates for creating well-structured skills that follow consistent patterns. Skills should be clear, discoverable, and provide actionable guidance for developers. The goal is to ensure all skills in the repository follow the same structure and quality standards.

### Goals

- Standardize skill structure across all skills in the repository
- Ensure skills are discoverable and easy to navigate
- Provide clear "when to use" guidance for each skill
- Maintain consistent reference file organization
- Enable efficient skill creation and maintenance

## What This Skill Should Do

When creating or updating a skill, this skill guides you to:

1. **Structure the SKILL.md file** with three main Header 1 sections:
   - Description and Goals
   - What This Skill Should Do
   - Information About the Skill (with subcategories)

2. **Create reference files** that are:
   - One level deep from SKILL.md (e.g., `references/filename.md`)
   - Use relative paths from the skill root
   - Avoid deeply nested reference chains

3. **Organize component/system references** in tables with:
   - Component/System name as a clickable link: `[ComponentName](references/componentname.md)`
   - "When to Use" descriptions that clearly explain when to load each reference

4. **Follow consistent formatting**:
   - Use markdown links for file references
   - Keep tables readable and scannable
   - Provide clear, actionable descriptions

## Information About the Skill

### Skill Structure Template

Every SKILL.md should follow this structure with three Header 1 sections:

```markdown
---
name: skill-name
description: Brief description of what the skill does and when to use it.
---

# Skill Name

## Description and Goals

[Description of the skill, its purpose, and goals]

### Goals

- Goal 1
- Goal 2
- Goal 3

## What This Skill Should Do

[Clear explanation of what the skill accomplishes and how it should be used]

## Information About the Skill

### Core Concepts

[Important concepts and principles]

### Reference Tables

[Tables organizing references with clickable links and "When to Use" descriptions]

### Implementation Patterns

[Code examples and patterns]

### Pitfalls and Checks

[Common mistakes and things to watch for]
```

### File Reference Guidelines

- **Use relative paths** from the skill root directory
- **Keep references one level deep**: `references/filename.md`
- **Avoid nested chains**: Don't create references that point to other references that point to more references
- **Use markdown links**: `[ComponentName](references/componentname.md)`

### Table Format

Reference tables should use this format:

```markdown
| Component | When to Use |
|-----------|-------------|
| [`ComponentName`](references/componentname.md) | Clear description of when to use this component. |
```

### Reference File Naming

- Component files: `{name}component.md` (e.g., `modelcomponent.md`)
- System files: `system.md` (consolidate all system info in one file)
- Other references: Use descriptive, lowercase names with hyphens

### Best Practices

- Keep "When to Use" descriptions concise but informative
- Group related components/systems into logical categories
- Provide code examples in implementation patterns sections
- Document common pitfalls and how to avoid them
- Update the skill description in the frontmatter to match the content
