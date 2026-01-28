---
name: skill-finder
description: Search for and install new skills from the open-source community (GitHub/SkillsMP) to extend capabilities.
---

# Skill Finder

This skill enables the agent (Antigravity) to autonomously find and install new skills from the internet (primarily GitHub, which feeds SkillsMP).

## Workflow

When the user asks to "find a skill" or "install a skill" for a specific task (e.g., "find a skill for python"), follow these steps:

### 1. Search for the Skill
Use the `search_web` tool to find a relevant `SKILL.md` file hosted on GitHub.
*   **Query Template**: `site:github.com filename:SKILL.md <TOPIC>`
    *   *Example*: `site:github.com filename:SKILL.md python`
    *   *Example*: `site:github.com filename:SKILL.md visual design`

### 2. Evaluate Results
Review the search results. Look for repositories that seem to be dedicated skills or well-maintained projects with a `SKILL.md`.
*   Prefer repositories that explicitly mention "Agent Skill" or "MCP".
*   Avoid random files that just happen to be named SKILL.md but aren't instructions.

### 3. Fetch Content
Use `read_url_content` (or `curl` if needed) to read the raw content of the `SKILL.md` file.
*   If you found a GitHub file page (e.g., `blob/main/SKILL.md`), convert it to the "Raw" URL (e.g., `raw.githubusercontent.com/...`).

### 4. Install the Skill
Create a new directory in `.agent/skills/` with a descriptive name.
*   *Path*: `.agent/skills/<skill-name>/`
*   Write the content to `.agent/skills/<skill-name>/SKILL.md`.

### 5. Activate
Use the `view_file` tool to read the newly created `SKILL.md` so you understand how to use it immediately.

### 6. Verification
Inform the user that the skill has been installed and is ready to use. Briefly describe what the skill allows you to do based on the file content.
