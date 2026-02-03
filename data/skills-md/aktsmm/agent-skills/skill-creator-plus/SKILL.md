---
name: skill-creator-plus
description: Guide for creating and reviewing effective skills. Use when creating a new skill, updating an existing skill, or reviewing SKILL.md files for quality. Triggers on "create skill", "review skill", "スキル作成".
license: Apache-2.0
metadata:
  author: yamapan (based on Anthropic)
---

# Skill Creator+

Guide for creating and reviewing effective skills.

## When to Use

- **Create skill**, **new skill**, **review skill**, **スキル作成**
- Creating a new skill from scratch
- Updating or refactoring an existing skill
- **Reviewing existing SKILL.md files** → See [references/skill-review-checklist.md](references/skill-review-checklist.md)

## Core Principles

| Principle                  | Description                                                          |
| -------------------------- | -------------------------------------------------------------------- |
| **Concise is Key**         | Context window is shared. Only add what Claude doesn't already know. |
| **Degrees of Freedom**     | Match specificity to task fragility (high/medium/low freedom)        |
| **Progressive Disclosure** | Split into 3 levels: Metadata → Body → References                    |

> **Default assumption:** Claude is already very smart. Challenge each piece: "Does this justify its token cost?"

## Skill Structure

→ **[references/skill-structure.md](references/skill-structure.md)** for details

```
skill-name/
├── SKILL.md (required)        # < 150 lines
├── scripts/                   # Executable code
├── references/                # Documentation loaded on demand
└── assets/                    # Output resources (templates, images)
```

→ See [skill-structure.md > What NOT to Include](references/skill-structure.md#what-not-to-include) for excluded files.

## Creation Process

→ **[references/creation-process.md](references/creation-process.md)** for details

| Step | Action                                                  |
| ---- | ------------------------------------------------------- |
| 1    | Understand with concrete examples                       |
| 2    | Plan reusable contents (scripts/references/assets)      |
| 3    | Initialize: `scripts/init_skill.py <name> --path <dir>` |
| 4    | Edit skill and implement resources                      |
| 5    | Package: `scripts/package_skill.py <path>`              |
| 6    | Iterate based on real usage                             |

## SKILL.md Guidelines

### Size Target

→ See [skill-review-checklist.md > Line Count Target](references/skill-review-checklist.md#line-count-target) for size guidelines.

**Quick rule:** < 150 lines is good, > 300 lines must split to references.

### Frontmatter

```yaml
---
name: skill-name
description: "What it does. Use when [trigger conditions]. Triggers on 'keyword', 'phrase'."
---
```

**Description must include:** What the skill does AND when to trigger it.

> ⚠️ **Why this matters:** Skills may not be invoked if descriptions lack clear triggers. Include user phrases to improve routing accuracy.

| ✅ Good                                                                                                                                                                 | ❌ Bad               |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| Extract text and tables from PDF files, fill forms, merge documents. **Use when** working with PDF files or when the user mentions PDFs, forms, or document extraction. | Helps with documents |
| Set up book writing workspace. **Triggers on** "book writing", "執筆ワークスペース", "technical writing project".                                                       | Creates workspaces   |

### When to Use Section

Start with **generic keywords** users are likely to say:

```markdown
## When to Use

- **PDF**, **extract text**, **form filling** ← Keywords first
- Processing documents with embedded images
- Filling PDF forms programmatically
```

### Body

- Use imperative/infinitive form
- Link to references for details
- Keep essential workflow only

## Review Checklist

→ **[references/skill-review-checklist.md](references/skill-review-checklist.md)**

```markdown
- [ ] SKILL.md under 150 lines?
- [ ] Description has trigger conditions?
- [ ] Details moved to references/?
- [ ] No README.md or auxiliary docs?
```

## Key References

| Topic            | Reference                                                                    |
| ---------------- | ---------------------------------------------------------------------------- |
| Skill Structure  | [references/skill-structure.md](references/skill-structure.md)               |
| Creation Process | [references/creation-process.md](references/creation-process.md)             |
| Review Checklist | [references/skill-review-checklist.md](references/skill-review-checklist.md) |
| Workflows        | [references/workflows.md](references/workflows.md)                           |
| Output Patterns  | [references/output-patterns.md](references/output-patterns.md)               |

## Done Criteria

- [ ] SKILL.md created and under 150 lines
- [ ] Frontmatter has name + description with trigger conditions
- [ ] Details moved to references/ (Progressive Disclosure)
- [ ] Review checklist passed
