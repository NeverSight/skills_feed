---
name: aios-writing-facebook
description: >
  Write Facebook posts and group content. Use when asked to write, create,
  draft, or produce a Facebook post, Facebook update, Facebook group post,
  or Facebook content. Also use when user mentions Facebook in a social media
  writing context. Outputs longer-form discussion posts with engagement hooks.
metadata:
  author: claim-supply
  version: 1.0.0
---

# Writing Facebook

## Purpose
Produce publish-ready Facebook posts that match brand voice with a slightly more casual, discussion-oriented tone suited to the platform.

## When to Use
- User asks to write a Facebook post or group content
- User mentions Facebook in a writing context
- Orchestrator (aios-writing-social) delegates a Facebook post

### Do NOT Use For
- Other platforms (use aios-writing-linkedin, aios-writing-twitter, etc.)
- Facebook ads (use writing-ads)

## Context Loading
Read all context files listed in aios-writing-social.

## Process

### Step 1: Parse the Request
Extract topic, content pillar, audience, type.

Defaults if unspecified:
- Content Pillar: Pillar 2 — Industry Discussion Topics (25%)
- Audience: Marketing Directors
- Type: Educational

### Step 2: Write the Post

Facebook Format Rules:
- 300-600 words for detailed posts
- Slightly more casual than LinkedIn
- Questions drive engagement — end with a discussion prompt
- Include link if relevant
- Can use longer narrative format

Tone:
- Conversational, discussion-oriented
- Question-driven to spark comments
- More casual than LinkedIn but still professional
- Good for storytelling and longer takes

### Step 3: Self-Review
Apply all quality gates from aios-writing-social.

Additional Facebook checks:
- Post 300-600 words
- Ends with discussion question or engagement prompt
- Tone more casual than LinkedIn
- Link included if relevant

## Output Format

    PLATFORM: Facebook
    CONTENT PILLAR: [pillar]
    AUDIENCE: [segment]
    TYPE: [type]
    ---
    [POST TEXT]
    ---
    CTA: [discussion question]
    LINK: [if applicable]
    IMAGE PROMPT: [optional]
    NOTES: [reviewer notes]

## References
- references/hook-patterns.md
- references/post-templates.md
- shared/platform-specs.md
- shared/compliance-rules.md
