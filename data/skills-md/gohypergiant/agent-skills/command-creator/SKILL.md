---
name: command-creator
description: Guide for creating Claude Code commands with skill integration. Use when users want to create a new Claude Code command specification, whether skill-based or standalone. Assists with command definition, skill discovery, argument specification, and command generation.
---

# Command Creator

## Overview

This skill guides the creation of Claude Code commands through a structured workflow that ensures proper skill integration, argument definition, and command specification. Commands can leverage existing skills or operate standalone.

**Target Audience:** This skill is designed for agents creating Claude Code command specifications. It provides procedural knowledge for gathering requirements, discovering relevant skills, and generating well-structured command definitions that other agents will execute.

## Command Creation Workflow

Follow these steps sequentially to create a well-defined Claude Code command:

### Step 1: Understand Command Purpose

Ask the user what the command should do. Gather specific details about:
- The task or operation the command will perform
- Expected inputs and outputs
- Any special requirements or constraints

**Example questions:**
- "What should this command do?"
- "Can you describe a typical use case for this command?"
- "What would trigger the use of this command?"

### Step 2: Identify Skill Dependencies

Ask if the command relates to existing skills:
- "Is this command based on any existing skills?"
- "Does this command use specific file formats, workflows, or domain knowledge?"

If the user mentions skills, note them. If not, proceed to Step 3.

### Step 3: Discover Relevant Skills

Check available skills to identify potentially relevant ones the user may have missed:

```bash
view .claude/skills    # Current project skills (if available)
view ~/.claude/skills  # Global skills (if available)
```

Look for skills related to:
- File types the command will process (docx, pdf, xlsx, pptx)
- Domain expertise (frontend-design, product-self-knowledge)
- Workflows or patterns (skill-creator, mcp-builder)

Present relevant skills to the user:
- "I found these skills that might be relevant: [list]. Should any of these be included?"
- Be concise; only mention skills with clear relevance

### Step 4: Verify Command Specification

If the command is not skill-based or after skill selection is complete, verify the command specification:
- Summarize what the command will do
- Confirm the workflow or operation sequence
- Verify any constraints or requirements

Ask for confirmation:
- "To confirm, the command will [summary]. Is this correct?"
- "Are there any other requirements I should know about?"

### Step 5: Define Command Arguments

Determine the command arguments through discussion:
- "What arguments should this command accept?"
- "Are any arguments required vs optional?"
- "What are the valid values or types for each argument?"

For each argument, specify:
- Name and type
- Required vs optional status
- Default value (if optional)
- Description of purpose
- Valid values or validation rules

### Step 6: Generate Command Specification

Create the command specification as a **single Markdown file with YAML front matter**.

For detailed format specification, patterns, and examples, see:
- `references/command-patterns.md` - Complete format guide, argument types, validation patterns, and multiple command pattern examples
- `references/optimize-images-example.md` - Production-ready example with full workflow, error handling, and statistics
- `../../commands/audit/js-ts-docs.md` - Real production command for reference

## Best Practices

**Command Naming:**
- Use lowercase with hyphens: `audit-performance`, `create-component`
- Be descriptive but concise
- Avoid generic names like `process` or `handle`

**Argument Design:**
- Minimize required arguments
- Provide sensible defaults for optional arguments
- Use clear, unambiguous argument names
- Validate argument values when possible

**Skill Integration:**
- Reference skills by name in the `skills` array
- Include skill names in command description when relevant
- Ensure referenced skills actually exist in `/mnt/skills/`

**Documentation:**
- Provide at least 2 usage examples
- Document argument constraints clearly
- Include implementation notes for complex commands
