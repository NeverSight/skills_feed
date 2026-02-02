---
name: skill-creator
description: Guide for creating effective skills that extend Claude's capabilities. This skill provides the framework for creating new skills with specialized knowledge, workflows, or tool integrations. Use when building a new skill from scratch or updating an existing skill.
---

# Skill Creator

Create effective skills that extend Claude's capabilities with specialized knowledge, workflows, and tools.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks - they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts)
```

---

## Bundled Resources

### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or repeated execution.

- **When to include:** Same code rewritten repeatedly, or deterministic reliability needed
- **Example:** `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits:** Token efficient, deterministic, may execute without loading into context

### References (`references/`)

Documentation and reference material loaded as needed into context.

- **When to include:** Documentation Claude should reference while working
- **Examples:** Database schemas, API docs, domain knowledge, company policies
- **Best practice:** If >10k words, include grep search patterns in SKILL.md
- **Avoid duplication:** Information lives in SKILL.md OR references, not both

### Assets (`assets/`)

Files used within output Claude produces (not loaded into context).

- **When to include:** Files needed in final output
- **Examples:** Templates, images, icons, boilerplate code, fonts
- **Benefits:** Separates output resources from documentation

---

## Progressive Disclosure Design

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited*)

*Unlimited because scripts can execute without reading into context.

---

## Skill Creation Process

Follow these steps in order, skipping only if clearly not applicable.

### Step 1: Understand the Skill with Concrete Examples

**Goal:** Clearly understand how the skill will be used.

Ask questions like:
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

**Conclude when:** You have a clear sense of the functionality the skill should support.

### Step 2: Plan the Reusable Skill Contents

**Goal:** Identify what scripts, references, and assets would be helpful.

For each example use case:
1. Consider how to execute it from scratch
2. Identify what would be helpful when executing repeatedly

**Example analysis:**

| Skill | Use Case | Reusable Resource |
|-------|----------|-------------------|
| pdf-editor | "Rotate this PDF" | `scripts/rotate_pdf.py` |
| frontend-builder | "Build me a todo app" | `assets/hello-world/` template |
| big-query | "How many users logged in?" | `references/schema.md` documentation |

**Conclude with:** A list of reusable resources to include (scripts, references, assets).

### Step 3: Initialize the Skill

Run the initialization script to create the skill structure:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates:
- Skill directory at specified path
- SKILL.md template with proper frontmatter and TODO placeholders
- Example resource directories: `scripts/`, `references/`, `assets/`
- Example files that can be customized or deleted

**Skip this step if:** Updating an existing skill (proceed to Step 4).

### Step 4: Edit the Skill

**Remember:** The skill is for another Claude instance to use. Include information that would be beneficial and non-obvious.

#### Start with Reusable Contents

1. Create the identified scripts, references, and assets
2. Delete example files/directories not needed
3. Request user input if needed (e.g., brand assets, documentation)

#### Update SKILL.md

**Writing Style:** Use **imperative/infinitive form** (verb-first instructions), not second person.
- ✅ "To accomplish X, do Y"
- ❌ "You should do X"

**Answer these questions:**
1. What is the purpose of the skill? (few sentences)
2. When should the skill be used?
3. How should Claude use the skill? (reference all bundled resources)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude uses the skill. Be specific about what the skill does and when to use it. Use third-person:
- ✅ "This skill should be used when..."
- ❌ "Use this skill when..."

### Step 5: Package the Skill

Package into a distributable zip file:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory:
```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The script will:
1. **Validate** - Check YAML frontmatter, naming conventions, structure
2. **Package** - Create zip file with proper directory structure

If validation fails, fix errors and run again.

### Step 6: Iterate

After testing the skill:
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or resources should be updated
4. Implement changes and test again

---

## SKILL.md Template

```markdown
---
name: skill-name
description: Brief description of what this skill does and when to use it. Use third-person (e.g., "This skill should be used when..."). Be specific about triggers and use cases.
---

# Skill Name

[One paragraph explaining the skill's purpose and core philosophy]

## Purpose

[What this skill accomplishes]

## When to Use This Skill

- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

**Not for:** [What this skill should NOT be used for]

---

## Workflow

### Step 1: [First Step]
[Instructions]

### Step 2: [Second Step]
[Instructions]

[Continue as needed]

---

## Bundled Resources

- `scripts/[name].py` - [What it does]
- `references/[name].md` - [What it contains]
- `assets/[name]/` - [What it includes]

---

## Related Skills

- **skill-name** - [How it relates]

---

*[Brief closing note or key reminder]*
```

---

## Best Practices

### SKILL.md Guidelines

- **Keep it focused:** One clear purpose per skill
- **Be specific about triggers:** When should this skill activate?
- **Use imperative voice:** "To do X, do Y" not "You should do X"
- **Reference all resources:** Explain how to use bundled scripts/references/assets
- **Include examples:** Show expected inputs and outputs
- **Add quality checks:** Checklists for validating output

### Frontmatter Best Practices

- **name:** Lowercase, hyphenated (e.g., `anti-ai-writing`)
- **description:** 1-3 sentences, third-person, specific triggers
  - ✅ "This skill transforms raw transcripts into polished documents. Use when processing podcast or interview recordings."
  - ❌ "A transcript processing skill"

### Resource Organization

- **scripts/:** Executable code only, no documentation
- **references/:** Documentation only, loaded as needed
- **assets/:** Output resources only, never loaded into context

### Context Management

- Keep SKILL.md under 5k words
- Move detailed reference material to `references/`
- Include grep patterns for large reference files
- Avoid duplication between SKILL.md and references

---

## Common Patterns

### Workflow Skills
```markdown
## Workflow

### Phase 1: [Name]
**Goal:** [What this phase accomplishes]

#### Step 1: [Action]
[Instructions]

#### Step 2: [Action]
[Instructions]

### Phase 2: [Name]
[Continue...]
```

### Reference Skills (Knowledge Base)
```markdown
## Key Concepts

### [Concept 1]
[Explanation]

### [Concept 2]
[Explanation]

## When to Apply

[Guidance on when to use this knowledge]
```

### Tool Integration Skills
```markdown
## Setup

[Prerequisites and installation]

## Usage

### [Command/Function 1]
```bash
[Example command]
```

[Explanation]

### [Command/Function 2]
[Continue...]
```

---

## Bundled Scripts

This skill includes helper scripts:

- `scripts/init_skill.py` - Initialize new skill with template structure
- `scripts/package_skill.py` - Validate and package skill for distribution
- `scripts/quick_validate.py` - Quick validation check

### Usage

```bash
# Initialize new skill
./scripts/init_skill.py my-new-skill --path ./skills/

# Package for distribution
./scripts/package_skill.py ./skills/my-new-skill

# Quick validation
./scripts/quick_validate.py ./skills/my-new-skill
```

---

## Related Skills

- **voice-analyzer** - Create voice style skills
- **anti-ai-writing** - Example of a well-structured skill

---

*Skills are modular, self-contained, and focused. One clear purpose, specific triggers, and all resources referenced in SKILL.md.*
