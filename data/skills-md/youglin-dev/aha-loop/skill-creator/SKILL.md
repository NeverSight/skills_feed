---
name: skill-creator
description: "Creates new Skills following Anthropic best practices. Use when discovering reusable workflows or repetitive patterns. Triggers on: create skill, new workflow, codify this process, standardize workflow."
---

# Skill Creator

Creates well-structured Skills following Anthropic's official best practices.

## When to Create a Skill

**Good candidates:**
- Repeated 3+ times
- Complex multi-step workflows
- Error-prone processes
- Domain-specific knowledge

**Not worth codifying:**
- One-off tasks
- Highly variable processes
- Trivial single-step actions

## SKILL.md Structure

### Required Frontmatter

```yaml
---
name: processing-documents
description: "Processes documents and extracts data. Use when working with PDF or Word files. Triggers on: process document, extract data."
---
```

**Field requirements:**

| Field | Rules |
|-------|-------|
| `name` | Max 64 chars, lowercase letters/numbers/hyphens only |
| `description` | Max 1024 chars, non-empty, **use third person** |

### Naming Convention

Use **gerund form** (verb + -ing):
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`

**Avoid:** `helper`, `utils`, `tools`, `anthropic-*`, `claude-*`

### Writing Descriptions

**Always use third person** (injected into system prompt):

```yaml
# Good
description: "Processes Excel files and generates reports"

# Avoid
description: "I can help you process Excel files"
description: "You can use this to process Excel files"
```

**Be specific and include triggers:**

```yaml
description: "Analyzes BigQuery data and generates reports. Use when querying sales metrics or creating dashboards. Triggers on: analyze data, bigquery report, sales metrics."
```

## Skill Body Template

```markdown
# [Skill Title]

[One sentence describing what this skill does]

## Quick Start

[Minimal example to get started - under 50 tokens]

## Process

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Advanced Features

**[Feature A]**: See [FEATURE_A.md](FEATURE_A.md)
**[Feature B]**: See [FEATURE_B.md](FEATURE_B.md)
```

## Best Practices

### Be Concise

Only add context Claude doesn't already have. Challenge each piece:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"

**Good** (~50 tokens):
```markdown
## Extract PDF text

Use pdfplumber:
\`\`\`python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
\`\`\`
```

**Bad** (~150 tokens): Explaining what PDFs are and how libraries work.

### Keep Under 500 Lines

If content exceeds 500 lines, split into separate files using progressive disclosure.

### One-Level Deep References

Keep all reference files linked directly from SKILL.md:

```markdown
# SKILL.md
**Basic usage**: [instructions here]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
```

### Avoid Time-Sensitive Info

Use "old patterns" section instead of dates:

```markdown
## Current method
Use the v2 API endpoint.

## Old patterns
<details>
<summary>Legacy v1 API (deprecated)</summary>
The v1 API used different endpoints...
</details>
```

### Use Consistent Terminology

Choose one term and stick with it:
- Always "API endpoint" (not mix with "URL", "route", "path")
- Always "extract" (not mix with "pull", "get", "retrieve")

## Directory Structure

```
skill-name/
├── SKILL.md              # Main instructions (< 500 lines)
├── ADVANCED.md           # Advanced features (loaded as needed)
├── REFERENCE.md          # API reference (loaded as needed)
└── scripts/
    └── utility.py        # Executed, not loaded into context
```

## Checklist

Before saving:

- [ ] Name uses gerund form and kebab-case
- [ ] Description is third person and specific
- [ ] Description includes what it does AND when to use it
- [ ] SKILL.md body under 500 lines
- [ ] No unnecessary explanations Claude already knows
- [ ] References are one level deep
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
