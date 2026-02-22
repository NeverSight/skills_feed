---
name: goose-blog-post
description: Write and publish blog posts for the block/goose open source project
author: angiejones
version: "1.0"
tags:
  - blog
  - writing
  - goose
  - documentation
  - content
---

# Goose Blog Post

Write blog posts for the [block/goose](https://github.com/block/goose) open source project blog powered by Docusaurus.

## Prerequisites

- The goose repo must be cloned locally
- Locate the blog directory at `<goose-repo>/documentation/blog/`
- Confirm the `authors.yml` and blog directory exist before proceeding

If the repo is not cloned, clone it:

```bash
gh repo clone block/goose
```

## Workflow

### Step 1: Determine the Writing Mode

Ask the user how they want to work. There are three modes:

1. **"I have a draft"** — The author has written (or will write) their own content. The agent scaffolds the directory, frontmatter, and image setup, then places the author's content into the correct format and reviews it against blog conventions.

2. **"I have notes/an outline"** — The author has rough ideas, bullet points, or an outline. The agent expands these into a full draft while preserving the author's voice and key points. Present the draft for the author's review before finalizing.

3. **"Write it for me"** — The author provides a topic and key points. The agent writes the full post. Present the draft for the author's review before finalizing.

**Important:** For modes 1 and 2, the author's voice and intent take priority. Do not rewrite their content unnecessarily. Focus on structure, conventions, and polish — not on replacing their words.

### Step 2: Gather the Blog Post Details

Ask the user for the following (do not assume any of these):

1. **Topic**: What is the blog post about?
2. **Author**: Who is the author? (needs to match a key in `authors.yml`)
3. **Target audience**: Who is this for? (developers, beginners, community, etc.)

For modes 2 and 3, also ask:
4. **Key points**: What are the main things the post should cover?
5. **Tone**: Technical deep-dive, casual walkthrough, announcement, etc.?

For mode 1, ask:
4. **Where is the draft?** A file path, or ask them to paste it in.

### Step 3: Verify Author Exists

Check `<goose-repo>/documentation/blog/authors.yml` for the author key.

If the author does **not** exist, create a new entry. The format is:

```yaml
authorkey:
  name: Full Name
  title: Job Title
  image_url: https://avatars.githubusercontent.com/u/<github-id>?v=4
  page: true
  socials:
    github: github-username
    x: x-username
    linkedin: linkedin-username
```

Ask the user for any missing details (name, title, GitHub username, social handles). The `image_url` can be derived from their GitHub profile: `https://avatars.githubusercontent.com/u/<id>?v=4`. Look up their GitHub user ID if needed:

```bash
gh api users/<username> --jq '.id'
```

### Step 4: Create the Blog Post Directory

Blog posts use the naming convention:

```
YYYY-MM-DD-slug-title/
  index.md
  banner.png
```

Rules:
- Use **today's date** (run `date +%Y-%m-%d` to get it)
- The slug should be lowercase, hyphen-separated, concise, and descriptive
- The directory lives inside `<goose-repo>/documentation/blog/`

```bash
mkdir -p documentation/blog/YYYY-MM-DD-slug-title
```

### Step 5: Assemble the Blog Post

Create `index.md` inside the new directory. The file structure is:

#### 1. Frontmatter

```markdown
---
title: "Your Blog Post Title"
description: "A concise summary of the post (1-2 sentences). Used in social previews and SEO."
authors:
  - authorkey
---
```

Frontmatter rules:
- `title` — wrap in quotes, use title case
- `description` — wrap in quotes, keep to 1-2 sentences, make it compelling for social sharing
- `authors` — a YAML list of author keys from `authors.yml` (supports multiple authors)
- Do **not** include a `date` field — Docusaurus extracts the date from the directory name
- Do **not** include `tags` in frontmatter — the blog does not use Docusaurus tags

#### 2. Banner Image

Every post **must** include a banner image immediately after the frontmatter:

```markdown
![blog banner](banner.png)
```

Banner image requirements:
- **Dimensions:** 1200×600 pixels
- **Location:** Same directory as `index.md`
- **Filename:** `banner.png` (or `.jpg`, `.webp`)
- **This same image is also used for social sharing** (Open Graph / Twitter cards) — there is no separate social image

If the user does not have an image ready, add the image reference as a placeholder and remind them to add the file before publishing. You can also offer to generate one if image generation tools are available.

#### 3. Introduction + Truncate Marker

The intro paragraph(s) appear before the truncate marker. This controls the preview on the blog index page:

```markdown
![blog banner](banner.png)

Your compelling introduction paragraph that hooks the reader.

<!--truncate-->
```

The intro should:
- Hook the reader — why should they care?
- Be 1-3 paragraphs max
- Give enough context to decide whether to click through

#### 4. Content Body

**For mode 1 (author's draft):** Place the author's content here. Adjust only what's needed to match the formatting conventions below. Flag any issues for the author rather than silently rewriting.

**For modes 2 and 3:** Write the content following the guidelines below, then present the full draft to the author for review.

**Formatting Conventions:**
- Use `##` for major sections and `###` for subsections
- Do **not** use `#` (h1) in the body — the title from frontmatter is the h1
- Include code blocks with language identifiers (` ```python `, ` ```bash `, etc.)
- Use bullet points and numbered lists to break up dense information
- Short paragraphs (2-4 sentences) for readability
- End with a clear takeaway, call-to-action, or next steps

**Voice & Style:**
- Write in first person when sharing personal experience, third person for announcements
- Be conversational but technically accurate
- The goose blog audience is developers — respect their intelligence
- Avoid marketing fluff; be genuine and specific
- Use concrete examples and code snippets over abstract explanations

**goose-Specific Conventions:**
- Refer to the project as "goose" (lowercase) when referencing the tool
- When linking to goose docs: `https://block.github.io/goose/`
- When linking to the repo: `https://github.com/block/goose`
- When linking to extensions: `https://block.github.io/goose/extensions`

#### 5. Social Metadata (`<head>` Section) — Required

Every blog post **must** end with a `<head>` section containing Open Graph and Twitter card meta tags. This is placed at the very end of the `index.md` file, after all content:

```html
<head>
  <meta property="og:title" content="YOUR TITLE HERE" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://block.github.io/goose/blog/YYYY/MM/DD/slug-title" />
  <meta property="og:description" content="YOUR DESCRIPTION HERE" />
  <meta property="og:image" content="https://block.github.io/goose/assets/images/BANNER_FILENAME_WITH_HASH.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="twitter:domain" content="block.github.io" />
  <meta name="twitter:title" content="YOUR TITLE HERE" />
  <meta name="twitter:description" content="YOUR DESCRIPTION HERE" />
  <meta name="twitter:image" content="https://block.github.io/goose/assets/images/BANNER_FILENAME_WITH_HASH.png" />
</head>
```

**Important:** The `og:image` and `twitter:image` URLs require a Docusaurus-generated filename that includes a content hash. You **cannot** guess this filename — it must be obtained from the local preview. See Step 6 for how to get it.

Field reference:
- `og:title` / `twitter:title` — same as the frontmatter `title`
- `og:description` / `twitter:description` — same as the frontmatter `description`
- `og:url` — the production URL: `https://block.github.io/goose/blog/YYYY/MM/DD/slug-title`
- `og:image` / `twitter:image` — the static image URL obtained from local preview (see Step 6)
- `twitter:card` — always `summary_large_image`
- `twitter:domain` — always `block.github.io`

When first creating the post, use `https://block.github.io/goose/assets/images/BANNER_FILENAME_WITH_HASH.png` as the placeholder for `og:image` and `twitter:image`. The `BANNER_FILENAME_WITH_HASH` portion will be replaced with the real filename after Step 6.

### Step 6: Preview Locally and Get the Image URL

The author needs to preview the blog post locally to:
1. Verify the post looks correct
2. **Get the static image URL** needed for the `<head>` social metadata

Tell the user to run this in a **separate terminal** (do **not** run this command directly — it blocks the terminal):

```bash
cd <goose-repo>/documentation
npm start
```

This starts a local dev server at `http://localhost:3000` with hot reloading.

Once the preview is running, instruct the user to:
1. Navigate to their blog post in the browser
2. Right-click the banner image → **Copy Image Address**
3. The copied URL will be something like:
   `http://localhost:3000/goose/assets/images/banner-a1b2c3d4e5f6.png`
4. **Extract the filename** (e.g., `banner-a1b2c3d4e5f6.png`)
5. Construct the production URL:
   `https://block.github.io/goose/assets/images/banner-a1b2c3d4e5f6.png`

Update the `<head>` section's `og:image` and `twitter:image` with this production URL.

### Step 7: Present the Draft for Review

**This step is critical.** Before considering the post done:

- Show the author the complete `index.md` content
- Highlight any decisions you made (title wording, section structure, intro framing)
- Ask if they want to adjust anything
- For mode 1: call out any formatting changes you made and why

Iterate based on feedback until the author is satisfied.

### Step 8: Final Review Checklist

Run through this checklist and fix any issues:

- [ ] Directory follows `YYYY-MM-DD-slug-title/` naming convention
- [ ] `index.md` exists in the directory
- [ ] Frontmatter includes `title`, `description`, and `authors`
- [ ] Author key exists in `authors.yml`
- [ ] Banner image (1200×600) is referenced after frontmatter
- [ ] Banner image file exists in the directory (or flagged as needed)
- [ ] `<!--truncate-->` marker is placed after the intro
- [ ] No `#` (h1) headers in the body — only `##` and below
- [ ] Code blocks have language identifiers
- [ ] Links to goose resources use the correct URLs
- [ ] `<head>` section is present at the end of the file
- [ ] `og:image` and `twitter:image` URLs are filled in from local preview
- [ ] Spelling and grammar are clean
- [ ] Post reads well from start to finish

## Content Types That Work Well

When helping the author brainstorm or choose a direction, these formats tend to perform well on the goose blog:

- **Tutorials and how-tos** — "How I built X with goose"
- **Deep dives** — architecture, features, or design decisions
- **Community spotlights** — contributor stories and use cases
- **Comparisons** — goose vs. other tools, honest assessments
- **Release announcements** — what's new and why it matters
- **Tips and workflows** — power-user guides and productivity hacks
- **Thought leadership** — opinions on AI agents, developer tools, open source

## Example

A complete blog post:

````markdown
---
title: "Building a Custom MCP Server for Your Team"
description: "A step-by-step guide to creating a Model Context Protocol server that connects goose to your team's internal tools."
authors:
  - ebony
---

![blog banner](banner.png)

If your team has internal tools that aren't covered by existing extensions, building a custom MCP server is easier than you think. In this post, I'll walk through how I built one for our team's deployment pipeline.

<!--truncate-->

## Why Build a Custom MCP Server?

goose connects to tools through the Model Context Protocol (MCP). While there are hundreds of community extensions available, sometimes your team has unique internal tools that need a custom integration.

## Getting Started

First, scaffold a new MCP server project:

```bash
npx create-mcp-server my-server
cd my-server
```

## Defining Your Tools

The core of any MCP server is its tool definitions...

## Wrapping Up

Building an MCP server took about an hour and saved our team countless context switches. If you want to learn more, check out the [MCP documentation](https://modelcontextprotocol.io/introduction) and the [goose extensions directory](https://block.github.io/goose/extensions).

<head>
  <meta property="og:title" content="Building a Custom MCP Server for Your Team" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://block.github.io/goose/blog/2025/07/01/custom-mcp-server" />
  <meta property="og:description" content="A step-by-step guide to creating a Model Context Protocol server that connects goose to your team's internal tools." />
  <meta property="og:image" content="https://block.github.io/goose/assets/images/banner-a1b2c3d4e5f6.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="twitter:domain" content="block.github.io" />
  <meta name="twitter:title" content="Building a Custom MCP Server for Your Team" />
  <meta name="twitter:description" content="A step-by-step guide to creating a Model Context Protocol server that connects goose to your team's internal tools." />
  <meta name="twitter:image" content="https://block.github.io/goose/assets/images/banner-a1b2c3d4e5f6.png" />
</head>
````
