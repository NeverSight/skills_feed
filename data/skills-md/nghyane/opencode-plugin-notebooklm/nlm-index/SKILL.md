---
name: nlm-index
description: Index documentation sites or GitHub repos to NotebookLM
---

# NotebookLM Index

Workflow to scrape docs/repos and upload to NotebookLM for AI-powered research.

## Use Cases

- Index entire documentation site (React, Next.js, etc.)
- Index GitHub repo (README, docs, source files)
- Bulk upload YouTube video transcripts

## Workflow

### 1. Identify Target

```
User provides:
- Docs URL: "https://react.dev/reference/react"
- GitHub repo: "vercel/ai" or "https://github.com/vercel/ai"
- YouTube playlist/channel
```

### 2. Create or Select Notebook

```
notebook_create({ title: "React Docs" })
# or
notebook_list()  # select existing
```

### 3. Discover URLs

#### Option A: Documentation Site

```bash
# Use webfetch to get sitemap or crawl links
webfetch({ url: "https://react.dev/sitemap.xml", format: "text" })

# Or scrape navigation links from docs page
webfetch({ url: "https://react.dev/reference/react", format: "markdown" })
# Extract all internal links from the page
```

#### Option B: GitHub Repo

```bash
# Use gh CLI to list files (quote URL to prevent shell glob expansion)
gh api 'repos/vercel/ai/git/trees/main?recursive=1' --jq '.tree[].path'

# Filter for docs/README
# Common patterns: README.md, docs/**, *.md, src/**/*.ts
```

#### Option C: YouTube

```
# Collect video URLs from playlist or channel
# Each video URL can be added directly
```

### 4. Filter & Prioritize

**Keep:**
- Documentation pages (guides, API refs, tutorials)
- README files
- Source code with good comments
- YouTube videos with transcripts

**Skip:**
- Asset files (.png, .css, .js bundles)
- Generated/minified code
- node_modules, dist, build
- Paid/private content

**Limits:**
- Max 50 sources per notebook (NotebookLM limit)
- If >50, split into multiple notebooks: "React Docs (Part 1)", "(Part 2)"

### 5. Batch Upload

```
# Collect URLs (space or newline separated)
source_add({
  urls: """
    https://react.dev/reference/react/useState
    https://react.dev/reference/react/useEffect
    https://react.dev/reference/react/useContext
    https://react.dev/learn/thinking-in-react
  """,
  notebook_id: "..."
})
```

**Rate Limiting:**
- NotebookLM processes URLs async
- For large batches (20+ URLs), split into chunks of 10-15
- Wait a few seconds between batches

### 6. Verify & Report

```
notebook_get({ notebook_id: "...", include_summary: true })
```

Report:
- Total sources added
- Any failed URLs (paid content, 404s, etc.)
- Suggest next steps (query, generate audio, etc.)

## Examples

### Index React Hooks Docs

```
1. notebook_create({ title: "React Hooks Reference" })

2. Scrape https://react.dev/reference/react/hooks
   Extract: useState, useEffect, useContext, useReducer, etc.

3. source_add({
     urls: "https://react.dev/reference/react/useState https://react.dev/reference/react/useEffect ..."
   })

4. notebook_query({ query: "Summarize all hooks and their use cases" })
```

### Index GitHub Repo

```
1. notebook_create({ title: "Vercel AI SDK" })

2. gh api 'repos/vercel/ai/git/trees/main?recursive=1'
   Filter: README.md, docs/**, packages/**/README.md

3. For each doc file:
   - If URL accessible: source_add({ urls: "https://github.com/vercel/ai/blob/main/README.md" })
   - If raw content needed: webfetch + source_add({ text: content, title: filename })

4. notebook_query({ query: "How do I use the AI SDK with Next.js?" })
```

### Index YouTube Playlist

```
1. notebook_create({ title: "React Conf 2024" })

2. Collect video URLs from playlist

3. source_add({
     urls: """
       https://youtube.com/watch?v=xxx
       https://youtube.com/watch?v=yyy
       https://youtube.com/watch?v=zzz
     """
   })

4. studio_create({ type: "audio", focus_prompt: "Key announcements" })
```

## Tips

- **Sitemap first**: Most doc sites have `/sitemap.xml` - parse it for all URLs
- **GitHub raw URLs**: Use `raw.githubusercontent.com` for direct file content
- **YouTube limits**: Only public videos with captions work
- **Chunking**: For 100+ URLs, create multiple notebooks by topic
- **Verification**: Always check `notebook_get` after bulk upload to confirm sources added

## Constraints

| Constraint | Limit |
|------------|-------|
| Sources per notebook | ~50 |
| URL types | Public websites, YouTube |
| Content | Visible text only (no JS-rendered) |
| YouTube | Public videos with transcripts |
