---
name: skill-creator-thepexcel
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Apache 2.0 (see LICENSE.txt)
---

# Skill Creator (ThepExcel Edition)

> **Based on [Anthropic's official skill-creator](https://github.com/anthropics/skills)** — Licensed under Apache 2.0. Enhanced by ThepExcel with additional best practices and practical insights from real-world skill development.

This skill provides comprehensive guidance for creating effective skills that Claude can discover and use successfully.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** — Multi-step procedures for specific domains
2. **Tool integrations** — Instructions for working with specific file formats or APIs
3. **Domain expertise** — Company-specific knowledge, schemas, business logic
4. **Bundled resources** — Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple approaches valid, context-dependent | Code review guidelines |
| **Medium** (pseudocode/params) | Preferred pattern exists, some variation OK | Report generation template |
| **Low** (specific scripts) | Fragile operations, consistency critical | Database migrations |

**Analogy**: A narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Test with All Target Models

Skills effectiveness depends on the underlying model. Test with all models you plan to use:

| Model | Consideration |
|-------|---------------|
| **Haiku** | Does the skill provide enough guidance? |
| **Sonnet** | Is the skill clear and efficient? |
| **Opus** | Does the skill avoid over-explaining? |

What works for Opus might need more detail for Haiku. Aim for instructions that work across models.

## Skill Structure

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      — Executable code (Python/Bash)
    ├── references/   — Documentation loaded as needed
    └── assets/       — Files used in output (templates, images)
```

### Naming Conventions

Use **action-oriented names** that clearly describe what the skill does. Lowercase letters, numbers, and hyphens only.

**Multiple patterns are acceptable — ask user preference if unclear:**

| Pattern | Examples | When to Use |
|---------|----------|-------------|
| **Gerund (verb-ing)** | `processing-pdfs`, `analyzing-data` | Traditional, widely used |
| **Verb-noun** | `prompt-ai-image-video`, `design-business-model` | Clear action + object |
| **Noun-verb-ing** | `power-query-coaching`, `problem-solving` | Domain + activity |
| **Recognized terms** | `triz`, `deep-research` | Widely known concepts |

| Good | Avoid |
|------|-------|
| `prompt-ai-image-video` | `pdf` (too vague) |
| `processing-pdfs` | `helper`, `utils` |
| `create-visualization` | `anthropic-*`, `claude-*` |

### Writing Effective Descriptions

The `description` field enables skill discovery. **Always write in third person.**

| Good | Avoid |
|------|-------|
| "Processes Excel files and generates reports" | "I can help you process Excel files" |
| "Extracts text from PDF documents" | "You can use this to extract PDF text" |

Include both **what** the skill does and **when** to use it:

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### SKILL.md Components

#### YAML Frontmatter (required)

| Field | Rules |
|-------|-------|
| `name` | Max 64 chars, lowercase + numbers + hyphens only |
| `description` | Max 1024 chars, non-empty, third person |

No other fields in frontmatter.

#### Body (Markdown)

Instructions and guidance for using the skill. Only loaded AFTER the skill triggers.

**Important**: "When to Use" sections in the body are useless — Claude only sees the description when deciding to trigger.

### Bundled Resources

#### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability.

- **When to include**: Same code rewritten repeatedly, or deterministic reliability needed
- **Benefits**: Token efficient, deterministic, can execute without loading into context

#### References (`references/`)

Documentation loaded as needed into context.

- **When to include**: Large documentation Claude should reference while working
- **Best practice**: If files >10k words, include grep patterns in SKILL.md
- **Avoid duplication**: Info lives in SKILL.md OR references, not both

#### Assets (`assets/`)

Files used in output, not loaded into context.

- **Examples**: Templates, logos, fonts, boilerplate code

### What NOT to Include

Do NOT create extraneous documentation:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md

Skills are for AI agents, not humans. No auxiliary context about creation process.

## Progressive Disclosure

Skills use a three-level loading system:

| Level | When Loaded | Size Limit |
|-------|-------------|------------|
| Metadata (name + description) | Always | ~100 words |
| SKILL.md body | When triggered | <500 lines |
| Bundled resources | As needed | Unlimited |

### Progressive Disclosure Patterns

See [references/progressive-disclosure.md](references/progressive-disclosure.md) for detailed patterns:

- **Pattern 1**: High-level guide with references
- **Pattern 2**: Domain-specific organization
- **Pattern 3**: Conditional details

**Key rules**:
- Keep references **one level deep** from SKILL.md
- For files >100 lines, include table of contents at top

## Skill Creation Process

### Overview

1. **Understand** — Gather concrete usage examples
2. **Plan** — Identify reusable resources
3. **Initialize** — Run `init_skill.py`
4. **Edit** — Implement resources and SKILL.md
5. **Package** — Run `package_skill.py`
6. **Iterate** — Refine based on real usage

### Step 1: Understanding with Concrete Examples

Skip only when usage patterns are already clearly understood.

**Ask clarifying questions:**
- "What functionality should this skill support?"
- "Can you give examples of how this would be used?"
- "What would a user say that should trigger this skill?"

**Related skill**: For extracting expertise from domain experts, consider using `/extract-expertise` — it provides structured conversations to capture mental models, workflows, and best practices that can inform skill development.

### Step 2: Planning Reusable Contents

Analyze each example by:
1. How would you execute this from scratch?
2. What scripts/references/assets would help when doing this repeatedly?

| Task Type | Analysis | Resource |
|-----------|----------|----------|
| PDF rotation | Same code each time | `scripts/rotate_pdf.py` |
| Frontend webapp | Same boilerplate | `assets/hello-world/` |
| BigQuery queries | Rediscovering schemas | `references/schema.md` |

### Step 3: Initializing the Skill

Always run `init_skill.py` for new skills:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates:
- Skill directory with proper structure
- SKILL.md template with frontmatter
- Example `scripts/`, `references/`, `assets/` directories

### Step 4: Editing the Skill

Remember: you're creating this for another Claude instance to use. Include non-obvious procedural knowledge.

**Consult design patterns:**
- **Multi-step processes**: See [references/workflows.md](references/workflows.md)
- **Output formats**: See [references/output-patterns.md](references/output-patterns.md)
- **Anti-patterns**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Evaluation**: See [references/evaluation.md](references/evaluation.md)

**Implementation order:**
1. Start with reusable resources (scripts, references, assets)
2. Test scripts by actually running them
3. Delete unused example files
4. Update SKILL.md

### Step 5: Packaging the Skill

```bash
scripts/package_skill.py <path/to/skill-folder>
```

The script validates then packages:
- YAML frontmatter format
- Naming conventions
- Description quality
- File organization

### Step 6: Iteration

**Iteration workflow:**
1. Use the skill on real tasks
2. Observe struggles or inefficiencies
3. Identify improvements
4. Implement and test again

See [references/evaluation.md](references/evaluation.md) for the Claude A/B iteration pattern.

## Content Guidelines

### Avoid Time-Sensitive Information

Don't include info that becomes outdated:

```markdown
# Bad
If you're doing this before August 2025, use the old API.

# Good — use "old patterns" section
## Current method
Use the v2 API endpoint.

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: api.example.com/v1/messages
</details>
```

### Use Consistent Terminology

Choose one term and use it throughout:

| Good (consistent) | Bad (inconsistent) |
|-------------------|-------------------|
| Always "API endpoint" | Mix "endpoint", "URL", "route", "path" |
| Always "field" | Mix "field", "box", "element", "control" |
| Always "extract" | Mix "extract", "pull", "get", "retrieve" |

## Quality Checklist

Before sharing a skill:

### Core Quality
- [ ] Description is specific with key terms
- [ ] Description includes what + when (third person)
- [ ] SKILL.md body under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references one level deep
- [ ] Workflows have clear steps

### Code and Scripts
- [ ] Scripts handle errors (don't punt to Claude)
- [ ] No magic constants (all values justified)
- [ ] Required packages listed and verified
- [ ] No Windows-style paths (use forward slashes)
- [ ] Validation steps for critical operations

### Testing
- [ ] At least three evaluations created
- [ ] Tested with target models (Haiku/Sonnet/Opus)
- [ ] Tested with real usage scenarios

## Related Skills

| When | Suggest |
|------|---------|
| Extract expertise from domain expert | `/extract-expertise` — structured conversations to capture mental models |
| Research domain knowledge | `/deep-research` — gather facts before building skill |

These skills are optional but highly valuable for skill development.

---

**References:**
- [workflows.md](references/workflows.md) — Sequential, conditional, feedback loops
- [output-patterns.md](references/output-patterns.md) — Templates, examples, terminology
- [anti-patterns.md](references/anti-patterns.md) — Common mistakes to avoid
- [evaluation.md](references/evaluation.md) — Evaluation-driven development, Claude A/B pattern
