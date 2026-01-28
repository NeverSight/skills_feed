---
name: skill-creator
description: Guide for creating custom skills in SaaS Factory. Use when you need to create a new skill to extend Claude's capabilities with specialized knowledge, workflows, or tools.
license: MIT
---

# Skill Creator - SaaS Factory Edition

This skill provides guidance for creating custom skills following SaaS Factory standards.

## Purpose

To create specialized skills that extend Claude's capabilities with domain-specific knowledge and reusable workflows.

## When to Use

- Creating new domain-specific skills
- Building reusable tools for your team
- Extending Claude Code functionality
- Documenting specialized procedures

## How to Create a Skill

### Step 1: Initialize
```bash
python scripts/init_skill.py my-skill --path ./my-skill
```

This creates:
```
my-skill/
├── SKILL.md           # Edit this with your skill
├── scripts/           # Add executable code
├── references/        # Add documentation
└── assets/           # Add resources
```

### Step 2: Edit SKILL.md

Follow this template:

```yaml
---
name: my-skill
description: What this skill does and when to use it (3-5 sentences)
license: MIT
---

# My Skill Title

## Purpose
Describe what the skill does in 1-2 paragraphs.

## When to Use
Explain when Claude should activate this skill.

## How to Use

### Step 1: First action
Instructions for step one.

### Step 2: Second action
Instructions for step two.

## Examples
- Example usage 1
- Example usage 2

## Reference Files
- See `references/` for detailed documentation
- Use `scripts/` for executable code
```

### Step 3: Add Content

**For scripts/** (executable code):
```bash
scripts/
├── helper.py          # Reusable code
├── processor.sh       # Shell utilities
└── validator.py       # Input validation
```

**For references/** (documentation):
```bash
references/
├── api_docs.md        # API specifications
├── schemas.md         # Data schemas
└── best_practices.md  # Guidelines
```

**For assets/** (output resources):
```bash
assets/
├── template.html      # HTML templates
├── icon.png          # Images
└── style.css         # Styles
```

### Step 4: Validate
```bash
python scripts/quick_validate.py ./my-skill
```

Check:
- ✅ SKILL.md has valid YAML frontmatter
- ✅ Required fields: name, description
- ✅ Correct file structure
- ✅ Naming conventions followed

### Step 5: Package
```bash
python scripts/package_skill.py ./my-skill
```

Output: `my-skill.zip` ready for distribution

### Step 6: Install in Claude Code
```bash
/plugin install ./my-skill.zip
```

## Best Practices

### ✅ DO
- **Write imperative instructions**: "To create X, do Y"
- **Keep SKILL.md <5k words**: Move large docs to references/
- **Name scripts descriptively**: `rotate_pdf.py`, not `util.py`
- **Include --help in scripts**: For user guidance
- **Document everything**: Clear examples and use cases

### ❌ DON'T
- Use vague names: "tool", "helper", "util"
- Write in second person: "You should do X"
- Include thousands of lines of code in SKILL.md
- Forget error handling in scripts
- Hardcode configurations

## Naming Conventions

```
Skills:      kebab-case (my-skill)
Scripts:     action_noun.py (rotate_pdf.py)
References:  descriptive.md (api_docs.md)
Files:       kebab-case.extension (config-template.json)
```

## Example Structure

```
pdf-processor/
├── SKILL.md
│   ---
│   name: pdf-processor
│   description: Process and manipulate PDF files.
│              Use when users need to rotate, merge, or
│              extract data from PDFs.
│   ---
│
│   # PDF Processor
│
│   ## Purpose
│   Advanced PDF manipulation for common tasks.
│
│   ## How to Use
│   1. Prepare input PDF
│   2. Execute relevant script
│   3. Output is saved
│
├── scripts/
│   ├── rotate_pdf.py
│   ├── merge_pdfs.py
│   └── extract_text.py
│
└── references/
    ├── pdf_formats.md
    └── library_guide.md
```

## Validation Checklist

```
□ SKILL.md structure
  □ Valid YAML frontmatter
  □ name in kebab-case
  □ description is descriptive

□ File organization
  □ Scripts in scripts/
  □ Docs in references/
  □ Resources in assets/

□ Quality
  □ SKILL.md <5k words
  □ Scripts have docstrings
  □ Clear examples included
  □ All paths relative

□ Ready to distribute
  □ Validated: ✓ All OK!
  □ Packaged: skill-name.zip
  □ Can install: /plugin install
```

## References

See `references/` for:
- Anthropic Skills Specification
- Best Practices Guide
- Example Skills

---

**Create skills following SaaS Factory standards for consistency and quality.**
