---
name: skill-gen
description: Generates new Claude Code skills with proper structure and best practices. Use when user asks to create a new skill, slash command, or wants to automate a workflow. Guides through requirements gathering, structure generation, and validation.
---

# Skill Generator

Generates properly structured Claude Code skills from user requirements.

## Quick Start

To create a new skill, gather from the user:

1. What should this skill do?
2. A short name (e.g., `processing-pdfs`, `testing-code`)
3. When should Claude use it?
4. Does it need scripts or just instructions?

## Workflow

### Step 1: Gather Requirements

- **Purpose**: What does the skill do?
- **Triggers**: When should it activate? (keywords, scenarios)
- **Complexity**: Instructions-only, or needs scripts/references?
- **Freedom level**: Rigid (exact steps) vs flexible (general guidance)?

### Step 2: Generate Skill Structure

Create directory: `~/.claude/skills/{skill-name}/`

```
{skill-name}/
├── SKILL.md           # Required: Main instructions (<500 lines)
├── scripts/           # Optional: Executable code
│   └── main.py
└── references/        # Optional: Detailed docs (one level deep)
    └── examples.md
```

### Step 3: Write SKILL.md

```markdown
---
name: {skill-name}
description: {What it does in third person}. Use when {trigger conditions}.
---

# {Skill Title}

{Brief overview - assume Claude is smart, only add context it doesn't already have}

## Quick Start

{Minimal working example or first step}

## Instructions

{Step-by-step guidance with appropriate freedom level}

## Advanced Features

**Feature A**: See [references/feature-a.md](references/feature-a.md)
**Feature B**: See [references/feature-b.md](references/feature-b.md)
```

### Step 4: Check Line Count & Apply Progressive Disclosure

After drafting SKILL.md, count its lines. If approaching or exceeding **500 lines**:

1. **Inform the user**: "The SKILL.md is {N} lines — exceeding the recommended 500-line limit for optimal performance."
2. **Identify splittable sections**: detailed references, long examples, advanced features, API docs
3. **Move to reference files**: `references/{topic}.md` — keep links one level deep
4. **Replace in SKILL.md** with a short summary + link:
   ```markdown
   **Advanced feature X**: See [references/feature-x.md](references/feature-x.md)
   ```
5. **Add table of contents** to any reference file over 100 lines

Even under 500 lines, prefer splitting if a section is self-contained and only needed in specific scenarios.

### Step 5: Validate

Run through the [validation checklist](#validation-checklist) before finalizing.

## Naming Rules

- **Length**: 1-64 characters
- **Format**: lowercase letters, numbers, hyphens only
- **Prefer gerund form**: `processing-pdfs`, `testing-code`, `writing-documentation`
- **Acceptable alternatives**: `pdf-processing`, `process-pdfs`
- **Not allowed**: start/end with `-`, consecutive `--`, reserved words (`anthropic`, `claude`), XML tags
- **Avoid**: vague names (`helper`, `utils`, `tools`), overly generic (`documents`, `data`)
- **Must match**: folder name

## Description Rules

- **Maximum**: 1024 characters, non-empty, no XML tags
- **Always third person**: "Processes Excel files" not "I can help you" or "You can use this"
- **Include both**: what it does AND when to use it
- **Be specific with key terms**: Claude uses descriptions to choose from 100+ skills

**Good examples**:
```yaml
description: Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```
```yaml
description: Generates descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**Avoid**: "Helps with documents", "Processes data", "Does stuff with files"

## Core Principles

### Conciseness

The context window is shared. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

Only add context Claude doesn't already have.

### Degrees of Freedom

Match specificity to the task's fragility:

| Freedom | Use When | Example |
|---------|----------|---------|
| **High** (text instructions) | Multiple valid approaches, context-dependent | Code review guidelines |
| **Medium** (pseudocode/params) | Preferred pattern exists, some variation ok | Report generation template |
| **Low** (exact scripts) | Fragile operations, consistency critical | Database migrations |

### Progressive Disclosure

- SKILL.md = overview + navigation (table of contents)
- Reference files = detailed content (loaded on-demand)
- Keep SKILL.md body under **500 lines**
- Keep references **one level deep** from SKILL.md (no nested references)
- Structure long reference files (100+ lines) with a table of contents

### Consistent Terminology

Pick one term and use it throughout. Don't mix "API endpoint" / "URL" / "API route" / "path".

## Patterns

### Workflow with Checklist

For complex multi-step operations:

````markdown
## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Analyze input
- [ ] Step 2: Generate plan
- [ ] Step 3: Validate plan
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```
````

### Feedback Loop

Run validator → fix errors → repeat:

```markdown
1. Make changes
2. Validate: `python scripts/validate.py`
3. If validation fails: fix issues, return to step 2
4. Only proceed when validation passes
```

### Template Pattern

Provide output format templates, matching strictness to requirements.

### Examples Pattern

Provide input/output pairs for output-quality-dependent skills.

### Conditional Workflow

Guide through decision points:

```markdown
**Creating new?** → Follow "Creation workflow"
**Editing existing?** → Follow "Editing workflow"
```

## Scripts Best Practices

- **Handle errors explicitly** — don't punt to Claude
- **No voodoo constants** — justify and document all values
- **List dependencies** — specify packages to install
- **Make execution intent clear**:
  - "Run `script.py` to extract fields" (execute)
  - "See `script.py` for the algorithm" (read as reference)
- **Use forward slashes** in all file paths (`scripts/helper.py` not `scripts\helper.py`)
- **MCP tool references** — use fully qualified names: `ServerName:tool_name`

## Anti-Patterns

- Explaining things Claude already knows (what PDFs are, how libraries work)
- Offering too many tool/library options — provide a default with escape hatch
- Time-sensitive information — use "old patterns" section with `<details>` tag
- Deeply nested references (file → file → file)
- Windows-style paths
- Assuming packages are installed without explicit install instructions

## Validation Checklist

### Core Quality
- [ ] Name: lowercase, numbers, hyphens only, 1-64 chars, no reserved words
- [ ] Description: third person, specific, includes what + when, under 1024 chars
- [ ] SKILL.md body under 500 lines
- [ ] Additional details in separate files (one level deep)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Concrete examples (not abstract)
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps

### Scripts (if applicable)
- [ ] Scripts handle errors explicitly
- [ ] No voodoo constants (all values justified)
- [ ] Required packages listed with install instructions
- [ ] Forward slashes in all paths
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops for quality-critical tasks

### Testing
- [ ] Tested with real usage scenarios
- [ ] Works across target models (Haiku needs more guidance, Opus needs less)

## Further Reading

**Eval-driven development**: See [references/eval-driven-development.md](references/eval-driven-development.md) for the build → test → observe → iterate cycle, two-Claude iterative development, and observation patterns for refining skills after initial creation.
