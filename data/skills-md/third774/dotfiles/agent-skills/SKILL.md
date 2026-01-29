---
name: agent-skills
description: Author and improve Agent Skills following the agentskills.io specification. Use when creating new SKILL.md files, modifying existing skills, reviewing skill quality, or organizing skill directories with proper naming, descriptions, and progressive disclosure.
---

# Agent Skills

Agent Skills are folders of instructions, scripts, and resources that agents discover and load on demand. This skill covers creating, modifying, and reviewing skills to ensure they follow the specification and best practices.

## When to Use This Skill

- Creating a new skill from scratch
- Modifying or improving an existing skill
- Reviewing skill quality before sharing
- Reorganizing skill content for better progressive disclosure

## RFC 2119 Keywords

This skill and skills created with it use RFC 2119 keywords to indicate requirement levels.

| Keyword | Meaning |
|---------|---------|
| **MUST**, **REQUIRED**, **SHALL** | Absolute requirement. No exceptions. |
| **MUST NOT**, **SHALL NOT** | Absolute prohibition. No exceptions. |
| **SHOULD**, **RECOMMENDED** | Strong recommendation. Valid reasons to deviate may exist, but understand implications first. |
| **SHOULD NOT**, **NOT RECOMMENDED** | Strong discouragement. Valid reasons to do it may exist, but understand implications first. |
| **MAY**, **OPTIONAL** | Truly optional. Implement if useful for your context. |

Reference: [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119)

## Specification Quick Reference

### Required Frontmatter

Every `SKILL.md` MUST start with YAML frontmatter containing `name` and `description`:

```yaml
---
name: skill-name
description: What this skill does and when to use it.
---
```

### Name Field Rules

The `name` field:

- MUST be 1-64 characters
- MUST use only lowercase alphanumeric characters and hyphens (`a-z`, `0-9`, `-`)
- MUST NOT start or end with a hyphen
- MUST NOT contain consecutive hyphens (`--`)
- MUST match the parent directory name exactly

Valid: `pdf-processing`, `code-review`, `data-analysis`
Invalid: `PDF-Processing`, `-pdf`, `pdf--processing`, `my_skill`

### Description Field Rules

The `description` field:

- MUST be 1-1024 characters
- SHOULD be written in third person (not "I can help you" or "You can use this")
- MUST include a "Use when..." clause specifying trigger conditions
- SHOULD contain specific keywords that help agents identify relevant tasks

**Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad:**
```yaml
description: Helps with PDFs.
```

### Optional Frontmatter Fields

These fields are all OPTIONAL (MAY include):

| Field | Purpose |
|-------|---------|
| `license` | License name or reference to bundled LICENSE file |
| `compatibility` | Environment requirements (max 500 chars) |
| `metadata` | Arbitrary key-value pairs for custom properties |
| `allowed-tools` | Space-delimited list of pre-approved tools (experimental) |

## Directory Structure

A skill is a directory that MUST contain a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # REQUIRED - main instructions
├── scripts/          # MAY include - executable code
├── references/       # MAY include - additional documentation
└── assets/           # MAY include - static resources (templates, images, data)
```

### When to Add References

You SHOULD add separate reference files when:

- SKILL.md exceeds ~300 lines
- Content applies to specific contexts (language-specific patterns, domain-specific schemas)
- Details are needed only for certain tasks (advanced features, edge cases)

References MUST be one level deep from SKILL.md. Nested reference chains (SKILL.md → ref1.md → ref2.md) are NOT RECOMMENDED.

## Best Practices

The following are RECOMMENDED practices. They represent strong guidance with valid reasons to deviate in specific contexts.

### Conciseness is Key

The context window is shared with conversation history, system prompts, and other skills. Challenge every piece of information:

- Does the agent really need this explanation?
- Can the agent be assumed to know this?
- Does this paragraph justify its token cost?

**Target:** You SHOULD keep SKILL.md body under 500 lines. Move detailed reference material to separate files.

### Progressive Disclosure

Skills SHOULD be structured for efficient context usage:

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup for all skills
2. **Instructions** (<5000 tokens): Full SKILL.md loaded when skill activates
3. **Resources** (as needed): Reference files loaded only when required

SKILL.md SHOULD serve as an overview that points to detailed materials. Like a table of contents.

### Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches, context-dependent | Code review guidelines |
| **Medium** (templates/pseudocode) | Preferred pattern exists, some variation OK | Report generation template |
| **Low** (exact scripts) | Fragile operations, consistency critical | Database migrations |

### Workflow Checklists

For multi-step processes, you SHOULD provide a checklist the agent can copy and track:

```
Task Progress:
- [ ] Step 1: Analyze requirements
- [ ] Step 2: Create plan
- [ ] Step 3: Implement
- [ ] Step 4: Validate
```

### Feedback Loops

Quality-critical tasks SHOULD include validation steps:

1. Perform action
2. Run validation
3. If validation fails → fix and retry
4. Only proceed when validation passes

## Authoring Workflow

Copy this checklist when creating or modifying a skill:

```
Skill Authoring Progress:
- [ ] Step 1: Define purpose (what problem does this solve?)
- [ ] Step 2: Identify triggers (when should agent use this?)
- [ ] Step 3: Write frontmatter (name matches directory, description is specific)
- [ ] Step 4: Draft body (core instructions, workflows, examples)
- [ ] Step 5: Extract references (move detailed/contextual content)
- [ ] Step 6: Review against checklist (see references/best-practices-checklist.md)
- [ ] Step 7: Test with real tasks
```

### Writing Effective Descriptions

The description enables skill discovery. It SHOULD include:

1. **What it does**: Core capabilities in active voice
2. **When to use it**: Specific triggers and keywords
3. **Third person**: "Extracts text from PDFs" not "I extract text from PDFs"

### Required "Use when..." Clause

Every description MUST include a "Use when..." sentence. This phrase signals trigger conditions to agents scanning skill metadata.

**Pattern**: `[What it does]. Use when [trigger conditions].`

**Example**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### Using RFC 2119 in Skills

Skills created with this skill SHOULD use RFC 2119 keywords to indicate requirement levels.

**Choosing the right keyword:**

| Use This | When |
|----------|------|
| MUST / MUST NOT | Hard constraint. A validator could check this. Breaking it causes failure. |
| SHOULD / SHOULD NOT | Strong recommendation. Valid exceptions exist, but they're rare. |
| MAY | Truly optional. No preference either way. |

**Example transformations:**

```markdown
# Before (ambiguous)
Keep SKILL.md under 500 lines.
The name field must match the directory.
Consider adding a checklist for multi-step tasks.

# After (precise)
SKILL.md SHOULD be under 500 lines.
The name field MUST match the directory.
Multi-step tasks MAY include a checklist for tracking.
```

**Guideline:** If you're unsure between MUST and SHOULD, ask: "Would breaking this rule cause the skill to malfunction, or just be suboptimal?" Malfunction → MUST. Suboptimal → SHOULD.

## Common Anti-Patterns

### Vague Descriptions

Descriptions SHOULD NOT be vague or generic:

```yaml
# Bad - agent can't determine when to use this
description: Helps with documents.

# Good - specific capabilities and triggers
description: Extract text and tables from PDF files, fill PDF forms, merge multiple PDFs. Use when working with PDF files or document extraction.
```

### Over-Explaining Common Knowledge

Skills SHOULD NOT explain concepts agents already know:

```yaml
# Bad - agent knows what PDFs are
PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF...

# Good - get to the actionable content
Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

### Deeply Nested References

Reference chains MUST NOT exceed one level:

```markdown
# Bad - agent may partially read nested files
SKILL.md → references/advanced.md → references/details.md

# Good - one level deep
SKILL.md → references/advanced.md
SKILL.md → references/details.md
```

### Time-Sensitive Information

Skills SHOULD NOT include time-sensitive information:

```markdown
# Bad - becomes outdated
If you're doing this before August 2025, use the old API.

# Good - use "old patterns" section
## Current method
Use the v2 API endpoint.

## Old patterns (deprecated)
<details>
<summary>Legacy v1 API</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

### Too Many Options Without Defaults

Skills SHOULD NOT present options without clear defaults:

```markdown
# Bad - decision paralysis
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image...

# Good - clear default with escape hatch
Use pdfplumber for text extraction.
For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

### Inconsistent Terminology

Skills SHOULD NOT mix synonyms. Pick one term and use it throughout:

- Always "API endpoint" (not mixing with "URL", "route", "path")
- Always "field" (not mixing with "box", "element", "control")

## Quality Review

Before finalizing a skill, review against the full checklist in `references/best-practices-checklist.md`.

For example patterns and structures, see `references/examples.md`.

<IMPORTANT>
Every skill should answer two questions clearly:
1. What does this skill enable the agent to do?
2. When should the agent use this skill?

If your description doesn't answer both, revise it.
</IMPORTANT>
