---
name: skill-writer
description: Expert guide for creating, structuring, and documenting Agent Skills following the official specification. Use when you need to create a new Agent Skill, understand the Agent Skills format, or improve existing skill documentation.
license: MIT
compatibility: All platforms that support Agent Skills specification
metadata:
  author: kehwar
  version: "1.0"
  category: development
---

# Skill Writer Guide

## Overview

This skill provides comprehensive guidance for creating Agent Skills that follow the official [Agent Skills specification](https://agentskills.io/specification). Agent Skills are a simple, open format for giving agents new capabilities and expertise through folders of instructions, scripts, and resources.

## What are Agent Skills?

Agent Skills are:
- **Portable**: Work across different AI platforms (Claude, GPT, Copilot, etc.)
- **Filesystem-based**: Simple directory structure with markdown files
- **Modular**: Each skill is self-contained and reusable
- **Open format**: No vendor lock-in, community-driven standard

## Creating a New Agent Skill

### 1. Directory Structure

Every Agent Skill lives in its own directory:

```
skill-name/
├── SKILL.md           # Required: Main skill file with metadata and instructions
├── scripts/           # Optional: Helper scripts or tools
├── references/        # Optional: Supporting documentation
└── assets/            # Optional: Images, files, or other resources
```

### 2. SKILL.md Format

The `SKILL.md` file is the heart of every skill. It has two parts:

#### Part 1: YAML Frontmatter (Required)

At the top of `SKILL.md`, include YAML frontmatter with metadata:

```yaml
---
name: skill-name                    # Required: lowercase, max 64 chars, matches folder name
description: Brief description      # Required: max 1024 chars, explain what and when
license: MIT                        # Optional: license identifier or file path
compatibility: Linux, Python 3.10+  # Optional: system requirements
metadata:                           # Optional: custom key-value pairs
  author: your-name
  version: "1.0"
  category: development
allowed-tools: tool1 tool2         # Optional/Experimental: approved tools
---
```

**Required Fields:**
- `name`: Skill identifier (lowercase, hyphens allowed, no consecutive hyphens)
- `description`: Clear explanation of:
  - What the skill does
  - When to use it
  - Key capabilities

**Optional Fields:**
- `license`: License type (e.g., MIT, Apache-2.0) or path to LICENSE file
- `compatibility`: System requirements, dependencies
- `metadata`: Any additional info (author, version, tags, etc.)
- `allowed-tools`: List of tools the skill can use (experimental feature)

#### Part 2: Markdown Body (Instructions)

After the frontmatter, write clear instructions in markdown format:

```markdown
# Skill Name Guide

## Overview
Brief introduction to the skill's purpose and capabilities.

## Quick Start
Simple example to get started quickly.

## Main Instructions
Step-by-step guidance organized by task or feature.

## Common Tasks
Frequent use cases with examples.

## Examples
Real-world examples with input/output.

## Troubleshooting
Common issues and solutions.

## Reference
Additional details, edge cases, advanced usage.
```

### 3. Writing Effective Instructions

**Best Practices:**

1. **Be Clear and Specific**
   - Use simple, direct language
   - Provide step-by-step instructions
   - Include code examples where relevant

2. **Structure for Scannability**
   - Use headers to organize content
   - Break long sections into subsections
   - Use lists, tables, and code blocks

3. **Include Examples**
   - Show both input and output
   - Cover common use cases
   - Demonstrate edge cases

4. **Keep it Focused**
   - One skill = one capability domain
   - Aim for under 5000 tokens
   - Link to references for details

5. **Make it Actionable**
   - Provide complete, working examples
   - Include error handling patterns
   - Show command-line usage when relevant

### 4. Optional Subdirectories

**scripts/**
- Place executable scripts, tools, or programs
- Include installation instructions in SKILL.md
- Document each script's purpose and usage

**references/**
- Additional documentation
- API references
- Detailed guides
- Link from SKILL.md with relative paths

**assets/**
- Images, diagrams, or visual aids
- Sample files or templates
- Reference with relative paths from skill root

## Complete Example

Here's a minimal but complete skill:

```
hello-world/
└── SKILL.md
```

**hello-world/SKILL.md:**

```yaml
---
name: hello-world
description: Simple example skill that demonstrates the basic structure of an Agent Skill. Use this as a template when creating new skills.
license: MIT
metadata:
  author: example
  version: "1.0"
---

# Hello World Skill

## Overview

This is a minimal example skill that demonstrates the Agent Skills format.

## Instructions

To use this skill:

1. Create a file called `hello.txt`
2. Write "Hello, World!" to the file
3. Display the contents

## Example

```bash
echo "Hello, World!" > hello.txt
cat hello.txt
```

Expected output:
```
Hello, World!
```

## Next Steps

Use this template to create more complex skills with additional features.
```

## Skill Creation Checklist

When creating a new skill, verify:

- [ ] Skill name is lowercase with hyphens only
- [ ] Folder name matches the `name` field in frontmatter
- [ ] YAML frontmatter is valid and complete
- [ ] `name` field is present (required)
- [ ] `description` field is present and clear (required)
- [ ] Description explains WHAT the skill does
- [ ] Description explains WHEN to use it
- [ ] Description is under 1024 characters
- [ ] Instructions are clear and actionable
- [ ] Examples are provided for main use cases
- [ ] Code examples are complete and tested
- [ ] Relative paths are used for internal references
- [ ] Total content is reasonable size (aim for <5000 tokens)
- [ ] All optional files (scripts, references, assets) are documented

## Common Patterns

### Task-Oriented Skills
Focus on accomplishing specific tasks:
- File processing (PDF, Excel, images)
- System administration
- Testing and validation
- Code generation

### Domain Expertise Skills
Provide specialized knowledge:
- Programming languages
- Frameworks and libraries
- APIs and protocols
- Best practices and patterns

### Workflow Skills
Guide multi-step processes:
- Project setup
- Deployment procedures
- Review checklists
- Documentation workflows

## Tips for Success

1. **Start Simple**: Begin with core functionality, add advanced features later
2. **Test Instructions**: Verify examples work as documented
3. **Think Like a User**: What would someone need to know to use this skill?
4. **Iterate**: Skills can evolve—start with v1.0 and improve over time
5. **Be Consistent**: Follow conventions from existing skills in your domain
6. **Document Assumptions**: State prerequisites and dependencies clearly
7. **Handle Errors**: Include troubleshooting for common issues

## Naming Conventions

- Use lowercase letters
- Separate words with hyphens (kebab-case)
- Be descriptive but concise
- Avoid abbreviations unless widely known
- Match folder name to skill name

**Good names:**
- `pdf-processing`
- `web-testing`
- `api-documentation`
- `code-review`

**Avoid:**
- `PDFProcessing` (uppercase)
- `pdf_processing` (underscores)
- `pdfproc` (unclear abbreviation)
- `skill-1` (not descriptive)

## Validation

Before finalizing a skill:

1. **Check YAML Syntax**
   - Use a YAML validator
   - Ensure proper indentation
   - Verify no syntax errors

2. **Test Instructions**
   - Follow your own instructions step-by-step
   - Verify all examples work
   - Check all file paths

3. **Review Content**
   - Proofread for clarity
   - Remove unnecessary complexity
   - Ensure completeness

4. **Check Structure**
   - SKILL.md is at skill root
   - All referenced files exist
   - Paths are relative from skill root

## Resources

- **Specification**: https://agentskills.io/specification
- **Documentation**: https://agentskills.io
- **Examples**: https://github.com/anthropics/skills
- **Community**: https://github.com/agentskills/agentskills
- **Template**: See [references/template.md](references/template.md) for a ready-to-use skill template

## Advanced Features

### Multi-file Skills

For complex skills, organize content across multiple files:

```
advanced-skill/
├── SKILL.md           # Main instructions and quick start
├── references/
│   ├── api.md        # Detailed API documentation
│   ├── examples.md   # Extended examples
│   └── troubleshoot.md
├── scripts/
│   ├── setup.sh      # Installation script
│   └── helper.py     # Utility functions
└── assets/
    └── diagram.png   # Visual aids
```

Reference from SKILL.md:
```markdown
For detailed API documentation, see [references/api.md](references/api.md).
```

### Using Scripts

When including scripts:

1. **Document clearly** in SKILL.md
2. **Make executable** (`chmod +x script.sh`)
3. **Include shebang** (`#!/bin/bash` or `#!/usr/bin/env python3`)
4. **Add comments** explaining key steps
5. **Handle errors** gracefully

Example script reference:
```markdown
## Installation

Run the setup script:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The script will:
1. Check system requirements
2. Install dependencies
3. Configure the environment
```

### Tool Restrictions

Use the `allowed-tools` field (experimental) to specify approved tools:

```yaml
---
name: secure-skill
description: Skill with restricted tool access
allowed-tools: pdftotext qpdf
---
```

This helps ensure skills only use vetted, secure tools.

## Conclusion

Agent Skills provide a simple, powerful way to give AI agents specialized capabilities. By following this guide and the official specification, you can create high-quality skills that work across platforms and help agents perform better at specific tasks.

Start simple, iterate based on feedback, and share your skills with the community!
