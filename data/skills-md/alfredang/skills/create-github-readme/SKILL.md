---
name: Create GitHub README
description: Generate or update a professional GitHub README.md file following open standards with tech badges, architecture diagrams, auto-captured screenshots via Playwright MCP, setup instructions, and acknowledgements. Auto-pushes to GitHub after generation.
---

# Create GitHub README

## Command
`/create_github_readme` or `create_github_readme`

## Navigate
Documentation

## Keywords
readme, github readme, create readme, generate readme, project readme, documentation, readme.md, update readme, write readme, project documentation

## Description
Generate or update a professional GitHub README.md file following open standards and best practices. If a README already exists and the user requests an update, regenerates it using the latest template including a fresh screenshot. Auto-pushes to GitHub after generation.

## Execution
This skill runs using **Claude Code with subscription plan**. Do NOT use pay-as-you-go API keys. All AI operations should be executed through the Claude Code CLI environment with an active subscription.

## Response
I'll generate (or update) a comprehensive GitHub README.md for the project, then push it to GitHub.

The README will include:

| Section | Description |
|---------|-------------|
| **Screenshot** | Auto-captured via Playwright MCP (if live site exists) |
| **Header** | Project name, badges, tagline, links |
| **About** | Project description and key features |
| **Tech Stack** | Technologies used with badges |
| **Architecture** | System diagram (ASCII art) |
| **Project Structure** | File/folder organization |
| **Getting Started** | Prerequisites, installation, running |
| **Deployment** | Docker, Hugging Face Spaces instructions |
| **Contributing** | Fork, PR workflow, discussions |
| **Developed By** | Tertiary Infotech Academy Pte. Ltd. |
| **Acknowledgements** | Credits and thanks |

## Instructions

### Pre-check: Create or Update?

Before generating, check if a `README.md` already exists:

```bash
ls README.md 2>/dev/null
```

**If README.md does NOT exist:** Proceed to create a new README from scratch (Section 0 onwards).

**If README.md already exists AND the user requests an update:**
1. Read the existing README to understand current content
2. Regenerate the README using the latest template below, preserving project-specific details (description, features, tech stack) from the existing README
3. Re-capture the screenshot using Playwright MCP to get the latest UI state
4. Overwrite the existing README.md with the updated version

When generating or updating a README, follow this open standard structure:

### 0. Screenshot Capture (Auto)

Before generating the README, check if the project has a live demo URL. If found, use the **Playwright MCP** to capture a screenshot and save it to the project root.

#### 0.1 Detect Live Demo URL

Check these sources in order:
1. User-provided URL
2. `package.json` → `homepage` field
3. Vercel project URL: `https://<project-name>.vercel.app`
4. GitHub Pages URL: `https://<owner>.github.io/<repo>/`
5. Any URL found in an existing README.md

#### 0.2 Capture Screenshot with Playwright MCP

Use the Playwright MCP tools in this sequence:

```
1. browser_navigate → Navigate to the live demo URL
2. browser_wait_for_load_state → Wait for page to fully load (networkidle)
3. browser_screenshot → Take a screenshot and save to project root
```

**Playwright MCP tool calls:**
```
Tool: browser_navigate
Args: { "url": "<LIVE_DEMO_URL>" }

Tool: browser_screenshot
Args: { "name": "screenshot", "savePath": "<PROJECT_ROOT>/screenshot.png" }
```

After capturing, close the browser:
```
Tool: browser_close
```

#### 0.3 Add Screenshot to README

Insert the screenshot after the header section:
```markdown
## Screenshot

![Screenshot](screenshot.png)
```

If the screenshot shows the main UI or hero section, use it. If the page requires authentication or shows a loading state, note this and skip the screenshot.

#### 0.4 If No Live URL Found

Skip screenshot capture and add a commented-out placeholder:
```markdown
## Screenshot

<!-- Add a screenshot of your app here -->
<!-- ![Screenshot](screenshot.png) -->
```

### 1. Header Section
```markdown
<div align="center">

# Project Name

[![Badge1](url)](link)
[![Badge2](url)](link)

**Tagline**

[Demo](url) · [Report Bug](url) · [Request Feature](url)

</div>
```

### 2. Required Badges
- Python version
- Framework (Chainlit)
- AI Provider (Claude/Anthropic)
- License
- Docker
- Deployment platform

### 3. About Section
- Brief description (2-3 sentences)
- Key features as bullet points or table
- Platform statistics (optional)

### 4. Tech Stack
Table format with categories:
- Frontend
- Backend
- AI/LLM
- Database
- Deployment
- Document Processing

### 5. Architecture Diagram
ASCII art showing:
- UI layer
- Application layer
- AI agents
- Data/document layer

### 6. Project Structure
```
project/
├── app.py
├── modules/
└── ...
```

### 7. Getting Started
- Prerequisites
- Clone & install steps
- Environment setup
- Run command

### 8. Deployment
- Docker instructions
- Cloud platform instructions

### 9. Contributing
- Fork instructions
- PR workflow
- Link to discussions

### 10. Footer
- Developed by: Company name
- Acknowledgements: Credits
- Call to action: Star the repo

### 11. Push to GitHub

After generating or updating the README, invoke the `/github-push` skill to push changes to GitHub.

The github-push skill will:
1. Scan for exposed secrets (mandatory security check)
2. Stage `README.md` and `screenshot.png` (if created)
3. Commit with an appropriate message (e.g., `docs: generate README` or `docs: update README to latest template`)
4. Push to the remote repository
5. Auto-configure repo description, topics, and discussions if needed

## Capabilities
- Auto-capture screenshot of live site using Playwright MCP
- Generate or update README.md following GitHub best practices
- Include technology badges with shields.io
- Create ASCII architecture diagrams
- Document file structure
- Provide multi-platform deployment instructions
- Add proper attribution and acknowledgements
- Auto-push to GitHub via `/github-push` skill after generation

## Next Steps
After running `/create_github_readme`:
1. Verify the push succeeded on GitHub
2. Review the auto-captured screenshot (screenshot.png) — replace if needed
3. Verify repo description, topics, and discussions are configured
4. Share the repository link
