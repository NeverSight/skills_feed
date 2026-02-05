---
name: blog-post
description: Create pcstyle.dev developer blog posts in the dual-author (ME MYSELF + MY AI AGENT) format, including MDX structure, custom components, and API/CLI publishing steps.
---

# pcstyle.dev Blog Post Skill

Create developer blog posts that match the pcstyle.dev cybernetic aesthetic and the dual-author voice split.

## When to use
- User asks for a devlog, blog post, shipping report, or AI/human split write-up for pcstyle.dev.
- User needs MDX content with custom components or curl-based posting instructions.

## Output requirements
- Two sections, in this order:
  1) **ME MYSELF** (human/pcstyle voice)
  2) **MY AI AGENT** (agent voice)
- Cybernetic minimalism: short, uppercase headers, neon-magenta/terminal phrasing.
- Include at least one actionable posting method (JSON API or MDX upload via curl).

## Structure template (MDX)
- **Lead**: 1-2 sentence summary of the build/update.
- **ME MYSELF**: intent, goals, human priorities, 2-4 bullets of what was decided.
- **MY AI AGENT**: execution, outcomes, measurable results, 2-4 bullets.
- **Ship status**: 1-2 lines of next steps or open tasks.

## Custom MDX components
Use these components directly in MDX posts when available:
- `Callout`: highlight important context.
  - Props: `title`, `tone` (magenta|cyan|neutral)
- `StatusChip`: compact tags.
  - Props: `label`, `tone`
- `CommandBlock`: CLI/curl commands.
  - Props: `title`

## Bundled resources
- Template: `assets/dual-author-template.mdx`
- API reference: `references/blog-api.md`

## API + CLI posting (curl)
Use these fields when posting to the API:
- `title` (string, required)
- `summary` (string, optional)
- `content` (string or file contents, required)
- `authorType`: `human` | `agent`
- `source`: `api` | `markdown` | `cli`
- `slug` (optional; otherwise derived from title)

Auth
- Required header: `Authorization: Bearer $BLOG_API_TOKEN`
- Agents should load env vars with: `source /Users/pcstyle/.env.blog`

### JSON example
```bash
curl -X POST https://blog.pcstyle.dev/api/posts \
  -H "Authorization: Bearer $BLOG_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Me Myself // Devlog",
    "summary": "Human authored update from pcstyle.",
    "content": "## ME MYSELF\nI post via the API when speed matters.",
    "authorType": "human",
    "source": "api"
  }'
```

### MDX upload example
```bash
curl -X POST https://blog.pcstyle.dev/api/posts \
  -H "Authorization: Bearer $BLOG_API_TOKEN" \
  -F "title=Agent Report // MDX" \
  -F "summary=CLI upload from the agent" \
  -F "authorType=agent" \
  -F "source=cli" \
  -F "file=@agent-report.mdx"
```

## Style notes
- Prefer short sentences and punchy fragments.
- Mix lowercase narrative with ALL-CAPS protocol labels.
- Avoid fluff; make outcomes and next steps explicit.

## References (Agent Skills spec)
- https://agentskills.io/home.md
- https://agentskills.io/integrate-skills.md
- https://agentskills.io/specification.md
- https://agentskills.io/what-are-skills.md
