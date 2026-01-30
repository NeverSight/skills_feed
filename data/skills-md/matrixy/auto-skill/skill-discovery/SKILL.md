---
name: skill-discovery
description: Search for and offer to load auto-generated skills that match the user's current task. Use when the user's request might benefit from a previously learned workflow pattern - especially multi-step tasks like "search and fix", "find and update", "read and edit".
user-invocable: false
---

# Auto-Skill Discovery

When the user requests a task that might match a previously learned workflow, search for relevant skills and offer to load them.

## When to Invoke This Skill

Use this skill when the user's request:
- Involves multiple steps (search + edit, read + modify, find + fix)
- Sounds like a repeatable workflow
- Mentions patterns like "the usual way" or "like before"
- Could benefit from a structured approach

Do NOT use for:
- Simple single-step tasks
- Questions or explanations
- Tasks the user wants done a specific way

## Instructions

### Step 1: Discover matching skills

Run the discovery script with the user's intent:

```bash
python scripts/discover_skill.py "<2-4 word summary of user's task>"
```

This outputs a formatted prompt showing:
- Best matching skill name and confidence
- What the skill does
- How it runs (inline vs isolated)
- A question asking if user wants to load it

### Step 2: Present to user

Show the discovery output to the user. Wait for their response.

### Step 3: If user approves, load the skill

```bash
python scripts/discover_skill.py "<same query>" --auto-load
```

This outputs the full skill content with clear delimiters. Display it directly - the formatted output contains the instructions you should follow.

### Step 4: Follow the loaded skill

The skill content between the `======` delimiters contains your instructions. Follow them to complete the user's task.

### Step 5: If user declines or no match

Proceed with the task normally using your standard approach.

## Example Flow

```
User: "Find all the TODO comments and update them"

You: [Run discover_skill.py "find update todos"]

Output:
  ## Skill Discovery
  I found an auto-generated skill that matches your task:
  **search-and-fix-workflow** (confidence: 85%)
  > Search for issues in codebase and fix them systematically
  Would you like me to load this skill?

User: "Yes"

You: [Run discover_skill.py "find update todos" --auto-load]

Output:
  ======================================
  SKILL LOADED: search-and-fix-workflow
  ...instructions...
  ======================================

You: [Follow those instructions to complete the task]
```
