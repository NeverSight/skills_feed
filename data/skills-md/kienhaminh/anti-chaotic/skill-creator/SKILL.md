---
name: skill-creator
description: Use when creating new skills, updating existing skills, or packaging skills for distribution.
---

# Skill Creation Standards

Create and manage Agent Skills for Antigravity/Gemini CLI.

## About Agent Skills

Skills are modular packages that extend Antigravity with specialized expertise and workflows. They follow the open [Agent Skills specification](https://agentskills.io/specification).

**Skill Locations:**

- **Workspace skills**: `.agent/skills/` - project-specific, committed to version control
- **Global skills**: `~/.gemini/skills/` - personal skills across all workspaces

## Skill Structure

```
skill-name/
├── SKILL.md          # Required - instructions and metadata
├── scripts/          # Optional - executable scripts
├── references/       # Optional - documentation to load as needed
└── assets/           # Optional - templates, images, data files
```

## SKILL.md Format

### Frontmatter (required)

```yaml
---
name: skill-name # Required: 1-64 chars, lowercase, hyphens only
description: What skill does # Required: 1-1024 chars, include trigger keywords
license: MIT # Optional: license identifier
compatibility: Requires git # Optional: 1-500 chars, environment requirements
metadata: # Optional: custom key-value pairs
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Read # Experimental: pre-approved tools
---
```

**Name rules:**

- Lowercase alphanumeric and hyphens only (`a-z`, `0-9`, `-`)
- No starting/ending hyphens, no consecutive hyphens (`--`)
- Must match parent directory name

**Description tips:**

- Include WHEN to use: specific scenarios, file types, or tasks
- Add keywords that help agents identify relevant tasks

### Body Content

Markdown instructions for the agent. Keep under **5000 tokens** for optimal context usage.

Include:

- **Tool Usage Standards**: Standard patterns for using Antigravity tools (`run_command`, `read_file`) within this domain.
- Step-by-step workflows (Procedures, not Lifecycle Workflows)
- Code examples
- Edge cases and troubleshooting

## Skill Design Principles

**Strict Separation of Concerns**:

- **Skill = Knowledge**: Capabilities, Standards, Best Practices, Reference Data.
- **Workflow = Process**: Steps, Sequences, Lifecycles, Timelines.

> [!WARNING]
> **Do NOT embed Workflows in Skills.**
>
> - ❌ Bad: A `backend-developer` skill defining a "Feature Implementation" lifecycle.
> - ✅ Good: A `backend-developer` skill defining "API Design Standards" and asking the user to use a generic Workflow to execute it.

## Progressive Disclosure

Skills use three-level loading to manage context efficiently:

1. **Metadata** (~100 tokens): `name` + `description` loaded at startup
2. **Instructions** (<5000 tokens): Full SKILL.md body when skill activates
3. **Resources** (as needed): scripts/, references/, assets/ loaded on demand

## Creating a Skill

### Step 1: Clarify Scope (Required)

**Always ask the user** to clarify the skill's scope before proceeding:

- What specific tasks should this skill handle?
- What tools, APIs, or frameworks does it involve?
- What are the expected inputs and outputs?
- Are there any existing workflows or patterns to follow?

### Step 2: Research & Analysis

Use available tools to understand the full picture:

1. **Search tools**: Use `search_web`, `read_url_content` to research official documentation
2. **Codebase analysis**: Use `grep_search`, `find_by_name` to understand existing patterns

**Analyze step-by-step:**

- What are the core capabilities needed?
- **What standard Antigravity tools are most relevant?** (e.g., read_file for docs, run_command for CLI)
- What are common use cases and edge cases?
- What scripts or references would be reusable?

### Step 3: Initialize

```bash
python scripts/init_skill.py <skill-name> --path .agent/skills
```

### Step 4: Edit SKILL.md

1. Complete the frontmatter metadata with accurate description
2. Write clear, actionable instructions based on research
3. Add scripts/references/assets as identified in analysis

### Step 5: Validate

```bash
python scripts/quick_validate.py .agent/skills/<skill-name>
```

## Resource Directories

### scripts/

Executable code (Python/Node/Bash) for automation tasks.

- Include error handling and helpful messages
- Document dependencies in requirements.txt

### references/

Documentation loaded into context when needed.

- API references, schemas, detailed guides
- Keep files focused (<5000 tokens each)

### assets/

Files used in output, not loaded into context.

- Templates, images, fonts, boilerplate code

---

## Expert Questioning Framework

When a user requests to create or upgrade a skill, the agent **MUST** gather requirements through 5 phases.

> [!IMPORTANT]
> **Do NOT just provide a generic questionnaire.** You must generate **domain-specific questions** based on:
>
> - The skill's domain (frontend, backend, AI, etc.)
> - The user's specific request
> - Your expert knowledge in that domain

**Workflow:**

1. **Analyze the request** - Identify the skill domain and user's goal
2. **Generate custom questionnaire** - Create an **Artifact** for the user to fill out.
   - **MUST** customize questions for the specific domain/task.
   - Use the template as a base but rewrite questions to be specific.
3. **Notify User** - Use `notify_user` with `PathsToReview` pointing to the artifact.
4. **Wait for Input** - User will edit the artifact directly.
5. **Read & Proceed** - Read the filled artifact and start implementation.

**Example - Designer Skill Upgrade:**

Instead of generic "What constraints?", ask specific questions like:

- "Should the skill focus on Web, Mobile, or both?"
- "Which design systems to reference? (Material, Ant, custom)"
- "Accessibility standards: WCAG 2.1 AA or AAA?"
- "Dark mode support required?"

### Phase 1: Discovery (Understand WHY & WHO)

- What specific problem needs to be solved?
- Who will use this skill? (agent, human, or both)
- What triggers the need to create/upgrade this skill?

### Phase 2: Context (Understand WHAT & WHERE)

- What is the specific domain? (frontend, backend, devops, AI, etc.)
- What tech stack or frameworks are involved?
- **What standard tool patterns apply?** (e.g., File system ops vs Command line ops)
- What constraints must be followed? (time, resources, team size)

### Phase 3: Scope (Define Boundaries)

> [!CAUTION]
> **⚠️ NEVER decide scope on your own** - always ask user for confirmation

- What is IN scope? What is OUT of scope?
- Minor update or Major upgrade?
- Dependencies with other skills/tools?

### Phase 4: Quality (Define Quality Standards)

- What level of expertise to embody? (junior, senior, expert 20+ years)
- Which best practices must be followed?
- What edge cases need to be handled?

### Phase 5: Validation (Define Success)

- What are the acceptance criteria?
- How do we know the skill works correctly?
- What metrics measure improvement?

**Key Principles:**

- 🔍 **Research before asking** - use tools to understand context
- 🎯 **Purpose-driven questions** - each question leads to a specific decision
- 📝 **Document answers** - record for reference during implementation

---

## Upgrading Existing Skills

### Step 1: Clarify User Intent

Apply the **Expert Questioning Framework** above. Position yourself as an expert in the skill's domain to ask guiding questions.

### Step 2: Analyze Current Skill

```bash
# Backup current skill
cp -r .agent/skills/<skill-name> .agent/skills/<skill-name>.backup

# View structure
ls -la .agent/skills/<skill-name>/
```

Analyze:

- Read SKILL.md: frontmatter, body, sections
- Check scripts/, references/, assets/
- Count tokens, sections, capabilities

### Step 3: Gap Analysis

Compare **current state** vs **new requirements**:

| Requirement | Current State | Gap                          |
| ----------- | ------------- | ---------------------------- |
| ...         | Yes/No        | Need to add/Exists/Duplicate |

**If duplicate**: Notify user and ask if they want to enhance further

### Step 4: Propose Changes

Present proposal and **ask user for confirmation**:

- Minor Update: Add notes, small fixes in SKILL.md
- Major Upgrade: Restructure, add scripts/references
- Restructure: Change architecture

### Step 5: Implement & Report

After implementation, run:

```bash
python scripts/compare_skill.py .agent/skills/<skill-name>.backup .agent/skills/<skill-name>
```

---

## Change Report Template

After upgrading a skill, report using this format:

```markdown
## Skill Upgrade Report: [skill-name]

### Summary

- **Type**: Minor Update / Major Upgrade / Restructure
- **Date**: YYYY-MM-DD

### Changes Made

| File           | Action   | Description            |
| -------------- | -------- | ---------------------- |
| SKILL.md       | Modified | Added X, Y, Z sections |
| scripts/new.py | Added    | Script for ...         |

### Before vs After

| Metric   | Before | After | Change |
| -------- | ------ | ----- | ------ |
| Tokens   | X      | Y     | +Z%    |
| Sections | X      | Y     | +Z     |

### Validation

- [ ] `quick_validate.py` passed
- [ ] Structure verified
- [ ] User reviewed
```
