---
name: video-note
displayName: Video Note
description: "Transform Obsidian video notes from the Vault into published notes on joelclaw.com. Use when publishing video notes, converting vault video content to the site, or when asked to 'publish a video note,' 'turn this video into a note,' 'publish from vault/videos,' or any task involving /Vault/Resources/videos → joelclaw content. Triggers on references to video notes, vault video files, or publishing video content to the blog."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, video, notes, publishing, obsidian]
---

# Video Note Publishing

Transform video notes from `/Users/joel/Vault/Resources/videos/` into published MDX notes on the joelclaw.com site at `apps/web/content/`.

## Source format

Vault video notes are Obsidian markdown with this frontmatter:

```yaml
type: video
source: https://www.youtube.com/watch?v=ID
channel: Channel Name
published: YYYY-MM-DD
duration: "HH:MM:SS"
nas_path: /volume1/home/joel/video/...
transcribed: YYYY-MM-DD
tags:
  - video
```

Body contains: H1 title, `> [!info] Source` callout, Executive Summary, Key Points, Speaker Context, Notable Quotes, Related links, Tags, and a collapsible Full Transcript.

## Output format

Publish as `.mdx` in `apps/web/content/` with this frontmatter:

```yaml
title: "Short descriptive title"
type: "note"
date: "YYYY-MM-DD"        # use today's date
description: "One-sentence hook in Joel's voice"
source: "YouTube URL"
channel: "Channel Name"
duration: "HH:MM:SS"
```

## Transformation workflow

1. Read the source vault note
2. Extract YouTube video ID from the `source` URL
3. Write the note in Joel's voice (read `joel-writing-style` skill — it's in the same `.agents/skills/` directory). Key rules:
   - Open with a hook, not a summary
   - Add a personal "why this matters to me" frame connecting the video to JoelClaw
   - Use short paragraphs, strategic profanity, bold for emphasis
   - End abruptly — no forced wrap-up
4. Embed the video with `<YouTube id="VIDEO_ID" />` after the intro
5. Include everything from the vault note **except the full transcript**:
   - Executive summary → rewrite as the intro (Joel's voice)
   - Key points → keep substance, tighten prose
   - Speaker context → "Who is [Speaker]" section
   - Notable quotes → curated "Quotes that stuck with me"
   - Related links → keep as "Related" section
6. Strip Obsidian syntax: `> [!info]` callouts → plain text, `[[wikilinks]]` → markdown links
7. Slug: kebab-case, concise (e.g., `openclaw-peter-steinberger-lex-fridman`)

## Voice reference

For Joel's writing style details, read [joel-writing-style SKILL.md](../joel-writing-style/SKILL.md) and its [voice examples](../joel-writing-style/references/voice-examples.md). Key points:

- Conversational first person, address reader as "you"
- Contractions always
- Bold for inline emphasis on key phrases
- Emoji sparingly (1-2 per note max)
- Headers as narrative beats, not outlines
- Links woven into sentences, never "click here"
- Credit people by name with links

## Content system details

See [content-system.md](references/content-system.md) for the joelclaw.com content types, MDX components, and routing.

## Example

See [example-note.md](references/example-note.md) for a complete published note showing the target format and voice.
