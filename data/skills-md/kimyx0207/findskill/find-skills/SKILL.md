---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills (Windows Compatible Version)

This skill helps you discover and install skills from the open agent skills ecosystem.

**This is a Windows-compatible fork that fixes the empty output issue in Claude Code on Windows.**

## ⚠️ CRITICAL: Windows Compatibility

**On Windows, you MUST use PowerShell to run skills commands!**

The default Bash/Git Bash environment on Windows does NOT work with `npx skills` - commands will return empty output.

**Always use this format on Windows:**
```bash
powershell -Command "npx skills find '[query]'"
powershell -Command "npx skills add [package] -g -y"
powershell -Command "npx skills list -g"
```

**Example:**
```bash
# ❌ WRONG - will return empty on Windows
npx skills find "react"

# ✅ CORRECT - works on Windows
powershell -Command "npx skills find 'react'"
```

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands (Windows format):**

- `powershell -Command "npx skills find '[query]'"` - Search for skills
- `powershell -Command "npx skills add [package] -g -y"` - Install a skill
- `powershell -Command "npx skills list -g"` - List installed skills
- `powershell -Command "npx skills check"` - Check for skill updates
- `powershell -Command "npx skills update"` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Search for Skills

Run the find command with a relevant query.

**On Windows (REQUIRED):**
```bash
powershell -Command "npx skills find '[query]'"
```

**On macOS/Linux:**
```bash
npx skills find [query]
```

For example (Windows format):

- User asks "how do I make my React app faster?" → `powershell -Command "npx skills find 'react performance'"`
- User asks "can you help me with PR reviews?" → `powershell -Command "npx skills find 'pr review'"`
- User asks "I need to create a changelog" → `powershell -Command "npx skills find 'changelog'"`
- User asks "数据分析" (data analysis in Chinese) → `powershell -Command "npx skills find 'data analysis'"` (Note: Search only supports English keywords!)

The command will return results like:

```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 3: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install command they can run (Windows format!)
3. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "vercel-react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

To install it (Windows):
powershell -Command "npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -y"

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 4: Offer to Install

If the user wants to proceed, you can install the skill for them.

**On Windows (REQUIRED):**
```bash
powershell -Command "npx skills add <owner/repo@skill> -g -y"
```

**On macOS/Linux:**
```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |
| Data Analysis   | data analysis, pandas, jupyter           |

## Chinese to English Keyword Reference

**Important: Search only supports English keywords!**

| Chinese (中文) | English Keywords |
| ------------- | ---------------- |
| 数据分析 | data analysis |
| 做PPT | ppt, presentation |
| 写文章 | writing |
| 代码审查 | code review |
| 部署上线 | deploy, deployment |
| 写测试 | testing |
| 做视频 | video, remotion |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`
4. **Use English keywords**: Chinese search will return empty results

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
powershell -Command "npx skills init my-xyz-skill"
```

## Troubleshooting

### Q: Search returns empty on Windows?
A: Make sure you're using `powershell -Command "npx skills find '...'"` format, not direct `npx skills find`.

### Q: Chinese search returns nothing?
A: Search only supports English keywords. Translate your query to English first.

### Q: How to verify installation?
A: Run `powershell -Command "npx skills list -g"` to see all installed skills.

---

**Original skill by Vercel Labs: https://github.com/vercel-labs/skills**
**Windows fix by: https://github.com/KimYx0207/findskill**
