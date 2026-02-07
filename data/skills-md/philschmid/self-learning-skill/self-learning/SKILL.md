---
name: self-learning
description: "Autonomous skill generator that learns new technologies from the web. Use when, users want to learn about a new library/framework/tool, need to create a skill for an unfamiliar technology, want to research and document a technology's usage patterns, or invoke with `/learn <topic>`. This skill uses web search and browser tools to discover, extract, and synthesize documentation into a reusable skill."
---

# Self-Learning Skill Generator

Autonomously research and learn new technologies from the web, then generate a reusable skill.

## Usage

```
/learn <topic>
```

If `<topic>` is missing, show usage. If topic is ambiguous, ask to clarify:

- "react" → "React for web, React Native, or a specific library like react-query?"
- "apollo" → "Apollo GraphQL client, Apollo Server, or Apollo Federation?"
- "aws" → "Which AWS service? (S3, Lambda, DynamoDB, etc.)"

Normalize to **kebab-case** for filenames.

### 2. Discover Sources (Web Search)

Use web search tool to find authoritative documentation:

**Search queries to try:**
1. `<topic> official documentation`
2. `<topic> getting started guide`
3. `<topic> API reference`
4. `<topic> GitHub repository`

**Source prioritization:**
1. Official docs sites (e.g., docs.*, *.dev)
2. Official GitHub repositories (README, /docs)
3. Official blogs/announcements

Select **3–5 high-quality URLs** maximum.

If no credible sources found, ask user to provide a URL.

---

### 3. Extract Content (URL Reading)

For each selected URL, read the content:

**Extract only relevant sections:**
- Installation / setup
- Core concepts
- API reference / key functions
- Common patterns / examples
- Version information

**Skip irrelevant content:**
- Navigation, ads, login prompts
- Unrelated sidebar content
- Comments, forums

If reading the content fails (JavaScript-heavy sites), fall back to browser agent:

```
Task: Navigate to <URL> and extract the main content including:
- Installation instructions
- Core concepts and API reference
- Code examples
Return the extracted content as markdown.
```

Record scrape timestamp for each source (use current date: YYYY-MM-DD format).

---

### 4. Generate Skill

Skills are modular, self-contained packages. Every skill consists of a required `SKILL.md` file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

1. Read `references/skill_creation_guide.md` to understand the format and principles.
2. Synthesize the learned and extracted information into a new skill.
    - **Trigger:** Write a description that clearly defines when to use it.
    - **Workflow:** Create step-by-step instructions.
    - **Format:** Ensure valid YAML frontmatter and proper file structure.

### 5. Save the Skill

Antigravity supports two types of skills, save a global-workspace if asked. 

- `.agent/skills/<skill-folder>/`	Workspace-specific
- `~/.gemini/antigravity/skills/<skill-folder>/`	Global (all workspaces)

Create directory if it doesn't exist, warn user before overwriting existing skill.

---

### 6. Confirm to User

Report:
```
✓ Created skill: <topic>
  Sources scraped: <N>
  Saved to: .agent/skills/<topic>/SKILL.md
  This skill will auto-trigger when working with <topic>.
```

---

## Tool Reference

- `search_web`: Discover documentation URLs
- `read_url_content`: Extract content from static pages
- `browser_subagent`: Extract content from JavaScript-heavy sites
- `write_to_file`: Save the generated skill

## Critical Rules

1. **Never hallucinate documentation:** Only include information from scraped sources.
2. **Never invent APIs:** If documentation is unclear, ask the user what to do.
3. **Ask for URLs:** If automated discovery fails, ask user for specific URLs.
4. **Verify sources:** Prefer official sources over third-party tutorials.
