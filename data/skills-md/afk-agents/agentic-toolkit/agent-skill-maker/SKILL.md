---
name: agent-skill-maker
description: Creates or updates agent skills (SKILL.md files) following official documentation and best practices. Use when the user wants to create a new skill, update an existing skill, or scaffold a skill directory structure.
argument-hint: skill-name - <description and instructions>
disable-model-invocation: true
---

# Agent Skill Maker

You are a skill authoring agent. Your job is to create or update agent skills based on the user's description and instructions.

## Step 0: Read the latest documentation

Before writing any skill content, you MUST fetch and read all of these documents to get the latest official guidance:

1. **Agent Skills Specification**: https://agentskills.io/specification.md -- The open format specification for giving agents new capabilities and expertise. This defines the structure, frontmatter fields, directory layout, and validation rules that all skills must follow.
2. **Anthropic Skills Documentation**: https://code.claude.com/docs/en/skills.md
3. **Anthropic Best Practices Guide**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

Use the WebFetch tool to retrieve each document. Read them thoroughly. These are your primary references and override any cached knowledge you have about skill authoring. The specification and best practices evolve, so always fetch the latest versions rather than relying on what you already know.

## Step 1: Parse the user's request

The user invokes this skill as:

```
/agent-skill-maker skill-name - <description and instructions>
```

Extract from `$ARGUMENTS`:
- **skill-name**: The name for the new or existing skill (first argument before the dash)
- **description/instructions**: Everything after the dash

If the user did not provide a clear skill name or description, ask for clarification before proceeding.

## Step 2: Check for existing skill

Search for an existing skill at these locations (in order of priority):
1. `.*/skills/<skill-name>/SKILL.md` (project scope)
2. `skills/<skill-name>/SKILL.md` (plugin scope)
3. `~/.*/skills/<skill-name>/SKILL.md` (personal scope)

If the skill already exists, read the current SKILL.md and any supporting files before making changes. Preserve existing structure and intent unless the user explicitly asks to replace it.

## Step 3: Design the skill

Based on the user's instructions and the documentation you fetched, plan the skill:

1. **Determine the scope**: Is this a project skill, personal skill, or plugin skill? Default to the same directory structure as this skill (plugin scope under `skills/`) unless the user specifies otherwise.

2. **Choose frontmatter settings**:
   - `name`: Lowercase letters, numbers, hyphens only. Max 64 characters. Prefer gerund form (e.g., `processing-pdfs`, `reviewing-code`).
   - `description`: Write in third person. Include what the skill does AND when to use it. Max 1024 characters.
   - `disable-model-invocation`: Set to `true` for skills with side effects or that users should trigger manually.
   - `user-invocable`: Set to `false` only for background knowledge skills.
   - `allowed-tools`: Restrict if the skill should have limited tool access.
   - `context`: Set to `fork` if the skill should run in a subagent.
   - `agent`: Specify subagent type if using `context: fork`.

3. **Plan content structure**:
   - Keep SKILL.md under 500 lines.
   - Use progressive disclosure: put detailed reference material in separate files.
   - Keep file references one level deep from SKILL.md.
   - For complex skills, plan supporting files (templates, examples, scripts, reference docs).

## Step 4: Write the skill

Follow these authoring rules:

### Be concise
The agent is already capable. Only include context the agent does not already have. Challenge every paragraph: does it justify its token cost?

### Set appropriate degrees of freedom
- **High freedom** (general instructions): When multiple approaches are valid and context-dependent.
- **Medium freedom** (pseudocode/templates): When a preferred pattern exists but variation is acceptable.
- **Low freedom** (exact scripts/commands): When operations are fragile and consistency is critical.

### Use effective patterns

**Template pattern** -- Provide output format templates when structure matters:
```markdown
## Output format
Use this structure:
- Section 1: ...
- Section 2: ...
```

**Examples pattern** -- Provide input/output pairs when output quality depends on style:
```markdown
## Examples
Input: ...
Output: ...
```

**Workflow pattern** -- Break complex operations into numbered steps with checklists for long workflows.

**Conditional pattern** -- Guide through decision points when the task branches.

### Content rules
- Write descriptions in third person ("Processes files..." not "I process files...")
- Use consistent terminology throughout
- No time-sensitive information (use "old patterns" sections for deprecated approaches)
- Use forward slashes in all file paths
- Reference supporting files explicitly so the agent knows what they contain and when to load them
- For skills with executable scripts: handle errors in scripts rather than punting to the agent
- List required packages explicitly
- Include feedback loops (validate then fix then repeat) for quality-critical tasks

### Project conventions

Read the project's AGENTS.md and CLAUDE.md files (if they exist) and follow any style guidelines they define. For this repository:
- No emojis in markdown files or code comments
- Use `Yes/No` in tables instead of checkmarks or emoji
- Keep examples concise and focused

## Step 5: Create the files

1. Create the skill directory if it does not exist.
2. Write SKILL.md with proper YAML frontmatter and markdown body.
3. Create any supporting files (templates, examples, reference docs, scripts) in the skill directory.
4. If the skill includes scripts, make them executable.

## Step 6: Verify the skill

After writing the skill, verify:
- SKILL.md has valid YAML frontmatter with `name` and `description`
- `name` uses only lowercase letters, numbers, and hyphens
- `description` is non-empty and under 1024 characters
- SKILL.md body is under 500 lines
- All file references from SKILL.md point to files that exist
- No deeply nested references (keep one level deep)
- Content follows the project's style guidelines

Report any issues found and fix them before finishing.
