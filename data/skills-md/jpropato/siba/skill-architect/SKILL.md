---
name: skill-architect
description: A meta-skill for creating, documenting, and refining other Antigravity skills. Use this when the user wants to codify a workflow, automate a repetitive task, or save a successful interaction pattern as a permanent capability.
---

# Skill Architect

You are an expert at capturing "latent knowledge" and turning it into structured "agent skills." Your goal is to make the agent more capable by documenting successful procedures into reusable `.agent/skills/` folders.

## 1. Discovery & Scoping
When the user asks to "make a skill" or "save this process," first determine:
- **Scope:** Should this be `Global` (~/.gemini/antigravity/skills/) for general tools, or `Workspace` (.agent/skills/) for project-specific logic?
- **Trigger:** What specific keywords or context should cause the agent to "activate" this new skill in the future?

## 2. Structure Standards
Every skill you create must follow this directory structure:
- `SKILL.md`: The core instructions (mandatory).
- `scripts/`: Any shell, Python, or ADB scripts required to execute the task.
- `examples/`: Markdown files showing "Before" and "After" or successful output logs.

## 3. Drafting the SKILL.md
Follow this template strictly:

### Frontmatter
- **name:** lowercase-with-hyphens.
- **description:** Third-person perspective (e.g., "Manages...", "Automates..."). Focus on the *utility* so the agent knows when to pick it.

### Body Content
- **Goal:** A 1-sentence summary of the skill’s purpose.
- **Workflow:** A numbered list of logical steps.
- **Constraints/Conventions:** Specific rules (e.g., "Always use `adb shell` for this," "Always maintain organic certification formatting").
- **Error Handling:** What the agent should do if a step fails.

## 4. Automation Protocol
If the skill requires automation:
1. Write the necessary script (e.g., a `.sh` or `.py` file).
2. Ensure the script is executable (`chmod +x`).
3. In the `SKILL.md`, instruct the agent to run the script with the `--help` flag first to understand its parameters.

## 5. Deployment
Once the user approves the draft:
1. Create the directory.
2. Write the files.
3. Confirm to the user: "Skill [name] is now live and will be active for future relevant tasks."
