---
name: bluesky
description: Guide for posting content to the Bluesky social network using the bsky terminal app. This skill should be used proactively when working in public repositories and there is interesting, shareable content (new features, insights, achievements, or announcements worth sharing with the community). Use it when asked to post to Bluesky, or when content seems worth sharing publicly.
---

# Bluesky

## Overview

Post content to the Bluesky social network using the `bsky` terminal application. This skill enables creating text posts, sharing images and videos with alt text, replying to posts, and quoting posts.

## When to Use This Skill

Use this skill in these scenarios:

1. **Explicitly requested** - When directly asked to post something to Bluesky
2. **Proactive sharing** - When working in public repositories and encountering:
   - Completed features or significant milestones worth announcing
   - Interesting technical insights or discoveries
   - Major achievements or project releases
   - Community-relevant updates or announcements

**Important:** Only suggest posting proactively when in public repositories. Never suggest posting for private or internal work.

## Core Capabilities

### 1. Text Posts

Create simple text posts using the `bsky post` command:

```bash
bsky post "Your message here"
```

For longer or multi-line posts, use stdin:

```bash
echo "Your longer message
with multiple lines" | bsky post --stdin
```

**Best practices:**
- Keep posts concise and engaging
- Use proper formatting and line breaks for readability
- Consider adding relevant hashtags at the end

### 2. Posts with Images

Include images in posts using the `--image` or `-i` flag:

```bash
bsky post "Check out this screenshot!" --image /path/to/image.png
```

**Multiple images:**

```bash
bsky post "Here are several images" \
  --image image1.png \
  --image image2.png \
  --image image3.png
```

**Add alt text for accessibility:**

```bash
bsky post "New feature screenshot" \
  --image screenshot.png \
  --image-alt "Dashboard showing user analytics with graphs"
```

**Best practices:**
- Always provide alt text using `--image-alt` for accessibility
- Alt text should be descriptive and concise
- Match the order of `--image-alt` flags to `--image` flags

### 3. Posts with Video

Share video content using the `--video` or `-v` flag:

```bash
bsky post "Demo of the new feature" --video demo.mp4
```

**With alt text:**

```bash
bsky post "Feature demo" \
  --video demo.mp4 \
  --video-alt "Screen recording showing the login flow with OAuth"
```

### 4. Replying to Posts

Reply to existing posts using the `-r` flag with the post URI or URL:

```bash
bsky post "Thanks for sharing!" -r at://did:plc:xyz/app.bsky.feed.post/abc123
```

### 5. Quote Posts

Quote an existing post using the `-q` flag:

```bash
bsky post "Great point about Go modules!" -q at://did:plc:xyz/app.bsky.feed.post/abc123
```

## Workflow Guidelines

When creating a post:

1. **Determine the content type** - Text only, with images, with video, reply, or quote
2. **Prepare the message** - Craft clear, concise text that provides context
3. **Prepare media if applicable** - Ensure images/videos are accessible and write descriptive alt text
4. **Construct the command** - Use appropriate flags based on content type
5. **Execute the post** - Run the `bsky post` command
6. **Verify success** - Check command output for confirmation

## Content Guidelines

When suggesting or creating posts:

- **Be authentic** - Share genuine insights and achievements
- **Provide value** - Ensure the post offers something useful to the community
- **Include context** - Don't assume everyone has background knowledge
- **Be professional** - Maintain appropriate tone for technical social media
- **Respect privacy** - Never share sensitive information or private repository details
- **Consider timing** - Only suggest sharing when the work is meaningful enough to warrant it

## Example Scenarios

### Scenario 1: Announcing a New Feature

```bash
bsky post "Just shipped a new feature in my Go library: automatic retry logic with exponential backoff!

Makes handling transient failures much easier. Check it out: https://github.com/user/repo" \
  --image feature-screenshot.png \
  --image-alt "Code snippet showing the new retry configuration API"
```

### Scenario 2: Sharing a Technical Insight

```bash
echo "TIL: Go's io.Pipe() is incredibly useful for streaming data between goroutines without buffering.

Perfect for processing large files without loading everything into memory.

Example use case: streaming CSV parsing → transformation → JSON encoding" | bsky post --stdin
```

### Scenario 3: Project Milestone

```bash
bsky post "Just reached 1,000 stars on my open source project!

Thanks to everyone in the community for the support and contributions. This wouldn't be possible without you!" \
  --image milestone-screenshot.png \
  --image-alt "GitHub repository page showing 1,000 stars"
```

### Scenario 4: Replying to Feedback

When someone shares or comments on your work, reply directly:

```bash
bsky post "Thanks for the detailed feedback! I've opened an issue to track this enhancement." \
  -r at://did:plc:xyz/app.bsky.feed.post/abc123
```

## Notes

- The `bsky` command uses your authenticated session from previous login
- If not logged in, run `bsky login` first
- Post URIs can be found from other `bsky` commands like `bsky timeline` or from the Bluesky web interface
- Multiple images/alt texts are supported by repeating the flags
- Images and videos should be local file paths accessible to the command
