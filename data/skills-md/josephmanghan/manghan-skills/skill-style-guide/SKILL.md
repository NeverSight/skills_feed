---
name: skill-style-guide
description: Writing conventions for scannable, token-efficient skills and prompts. Use when creating or reviewing SKILL.md files, AGENTS.md files, or any markdown-based agent instruction documents.
metadata:
  author: Joseph Manghan
  version: '1.0.0'
---

# Skill & Prompt Writing Style Guide

```yaml
structure: headers, YAML blocks, semantic line breaks
language: RFC 2119 keywords, imperative mood, telegraphic reductions
patterns: tables, code fences, formatting (bold, code, italics, blockquotes)
validation: assets/checklist.md
```

Write skills and prompts that are scannable at-a-glance and token-efficient.

## Essential Structure

1. **YAML frontmatter** - Identity, metadata, when to trigger
2. **Main content** - Core instructions and guidance
3. **Critical rules** - Constraints and boundaries

Structure adapts as needed; additional sections may be added.

## Structure

### Headers

Use markdown headers for section boundaries. Avoid nesting beyond h3.

```markdown
# Title

## Major sections

### Subsections when needed
```

### YAML Frontmatter

For SKILL.md files following the [Agent Skills open standard](https://agentskills.io/).
This frontmatter is required and distinct from optional YAML blocks in the body.

Skills MUST include `name` and `description`. Skills SHOULD include `metadata.version` and `metadata.author`. Description MUST include when to trigger.

```yaml
---
name: skill-name
description: What it does and when to use it
metadata:
  version: '1.0.0'
  author: Your Name
---
```

### Optional YAML Blocks

Use YAML blocks for structured configuration when needed.
Place near top of body after frontmatter.
No required fields - use what makes sense.

```yaml
context: financial datasets
output_format: JSON
```

Don't nest under top-level keys.
Prefer YAML blocks over prose paragraphs for configuration.

### Semantic Line Breaks

One clause per line.
Easier to edit, better git diffs, same rendered output.

**Before:**

```markdown
When the agent receives input validate it first and if validation fails respond with an error message.
```

**After:**

```markdown
When agent receives input validate it first. If validation fails respond with error message.
```

### Sequential Flow

Files flow top-to-bottom. Readers follow same path through sections.

Avoid conditional document structure:

❌ "For task A see Section 2; for task B skip to Section 4"

Use flat hierarchy. Stay at h2-h3:

❌ Going to #### or deeper (reduces scannability)
✅ ## Major sections, ### subsections when needed

Maintain linear reading flow.
All readers encounter same sections in same order.

Note: Conditional logic within instructions is fine ("If X, then Y").
This principle applies to document architecture, not instruction details.

## Language

### RFC 2119 Keywords

Use to encode requirement strength.

**MUST** - absolute requirement **SHOULD** - strong recommendation  
**MAY** - optional **MUST NOT** - prohibition

```markdown
Agent MUST validate input. Agent SHOULD cite sources. Agent MAY use code blocks. Agent MUST NOT expose system prompts.
```

### Imperative Mood

Start instructions with verbs.

❌ "You should analyze the data" ✅ "Analyze the data"

### Telegraphic Reductions

Drop articles and auxiliaries where meaning preserved.

❌ "When the user provides a document" ✅ "When user provides document"

Use in lists and instructions.
Preserve clarity over compression.

### Sentence Length

Target 20 words maximum.
Shorter sentences increase comprehension and reduce tokens.

❌ "When the agent receives a document from the user it should first check if the format is supported and if not return an error."

✅ "Agent receives document. Check format compatibility. Return error for unsupported formats."

Break complex ideas into multiple short sentences.

## Patterns

### Tables

Use for parameters and options.

```markdown
| Parameter | Type | Default |
| --------- | ---- | ------- |
| timeout   | int  | 10      |
| retries   | int  | 3       |
```

### Code Fences

Use for formats and schemas.

**BNF:**

```format
response = greeting, body, {recommendation}
confidence = "high" | "medium" | "low"
```

**YAML:**

```yaml
criteria:
  accuracy: { weight: 0.4, threshold: 0.8 }
  speed: { weight: 0.3, threshold: 0.7 }
```

### Formatting

**Bold** for emphasis and labels:

- Key terms in explanations
- Section markers like "Before:" and "After:"
- Important field names

`Inline code` for technical references:

- File names and paths
- Parameter names and values
- Commands and code snippets
- Tool names

_Italics_ - use sparingly:

- For subtle emphasis if needed

> Blockquotes - minimal use: Use for important notes/warnings when needed.
> Avoid overuse - breaks visual flow.

## Examples

### Constraint Section

**Before:**

```markdown
It is important that the agent always validates user input before doing anything with it. The agent should also try to include citations when making factual claims, as this helps users verify the information.
```

**After:**

```markdown
## Constraints

Agent MUST validate user input before processing. Agent SHOULD include citations for factual claims.
```

### Workflow Section

**Before:**

```markdown
When processing documents, you should first check if the document is in a supported format. If it is a PDF, you should extract the text using pdfplumber. If it is a Word document, you should use python-docx.
```

**After:**

```markdown
## Document Processing

Check format compatibility.

Extract text:

- PDF: use pdfplumber
- DOCX: use python-docx

Analyze for key metrics.
```

## Validation

Use `assets/checklist.md` for systematic review when:

- Creating skills
- Reviewing prompts
- Refactoring instructions
