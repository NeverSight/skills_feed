---
name: robot-expert
description: Robot Framework expert for SnapLogic pipeline testing conventions. Use when the user asks about best practices, naming conventions, tags, variable patterns, or database/messaging test patterns.
user-invocable: true
---

# Robot Framework Expert Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/robot-expert/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Best practices for writing tests?
- Naming conventions?
- Tags system help?
- Variable patterns?
- Database/messaging test patterns?

### Step 3: Follow the Guide
Use the detailed instructions from the file you loaded in Step 1 to:
- Provide accurate Robot Framework conventions
- Reference project-specific patterns
- Show relevant examples from the guide

### Step 4: Respond to User
Provide clear, actionable guidance based on the complete guide.

---

## Quick Reference

This guide covers:
- File structure and organization
- Test file conventions
- Naming conventions
- Tags system
- Common keywords
- Variable patterns
- Best practices
- Database and messaging test patterns
