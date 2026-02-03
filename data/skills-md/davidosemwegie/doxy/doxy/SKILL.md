---
name: doxy
description: Generate skills from documentation websites. Use when asked to create skills from docs, convert documentation to agent skills, or crawl a docs site.
---

# Generate Skills from Documentation

Transform any documentation website into agent-ready skills.

## Input

Provide a documentation URL:
```
Create skills from https://docs.example.com
```

## Process

### Step 1: Extract Library Name and Navigation

Use WebFetch on the documentation URL with this prompt:

```
Extract two things from this documentation page:

1. LIBRARY NAME: The name of the library, framework, or technology being documented.
   Return as lowercase kebab-case (e.g., 'webgl', 'react', 'express-js').

2. NAVIGATION: The sidebar/navigation structure as a JSON array:
[
  {"title": "Page Title", "url": "/path/to/page"},
  {"title": "Another Page", "url": "/path/to/another"}
]

Format response as:
LIBRARY: [library-name]
NAVIGATION: [json-array]

Include ALL navigation links from the sidebar. Return relative URLs. Skip external links.
```

### Step 2: Create Output Directory

Create the skills folder:
```
.claude-plugin/skills/[library-name]/
```

Create a manifest file `doxy-manifest.json`:
```json
{
  "name": "[library-name]",
  "source_url": "[documentation-url]",
  "created_at": "[ISO 8601 timestamp]",
  "last_updated": "[ISO 8601 timestamp]"
}
```

### Step 3: Process Each Page

For each navigation item:

1. **Fetch content** using WebFetch with prompt:
   ```
   Extract the main documentation content. Return:
   1. The page title
   2. A concise summary (1-2 sentences)
   3. Key concepts, APIs, or instructions as markdown
   Focus on technical content. Skip navigation, footers, ads.
   ```

2. **Create skill** at `.claude-plugin/skills/[library-name]/[page-name]/SKILL.md`

### Step 4: Write SKILL.md Files

Use this format for each skill:

```markdown
---
name: [library-name]-[topic]
description: Use when working with [topic] in [library-name]. Covers [key concepts].
---

# [Page Title]

[Extracted content formatted as clear instructions]
```

**Skill naming:**
- Derive from URL path (e.g., `/docs/api/methods` → `api-methods`)
- Use kebab-case
- Remove common prefixes (`docs/`, `guide/`, `reference/`)

**Directory structure example:**
```
.claude-plugin/skills/webgl/
├── doxy-manifest.json
├── getting-started/
│   └── SKILL.md
├── best-practices/
│   └── SKILL.md
└── shaders/
    └── SKILL.md
```

### Step 5: Report Results

After processing, report:
- Folder created: `.claude-plugin/skills/[library-name]/`
- Number of skills generated
- List of skill names with purposes
- Any pages that failed to process

## Quality Rules

- Keep each SKILL.md under 200 lines
- If content exceeds limit, create `references/` subdirectory with detailed files
- Use imperative voice ("Configure X" not "This explains how to configure X")
- Include code examples from the documentation
- Focus on actionable guidance

## Error Handling

| Issue | Action |
|-------|--------|
| WebFetch fails for a page | Log error, continue with remaining pages |
| Empty navigation | Report issue, suggest checking URL structure |
| Content too minimal | Create stub skill noting limited content |
| Folder already exists | Report existing skills, suggest update or different name |

## Output Format Reference

See `references/skill-format.md` for complete SKILL.md specification.

---

**Note:** Claude Code users can install the full plugin for `/doxy` slash commands:
```
/plugin davidosemwegie/doxy
```
