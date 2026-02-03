---
name: social-media-poster
description: Post content to LinkedIn and Twitter/X simultaneously. This skill should be used when the user wants to create social media posts, share content on LinkedIn or Twitter/X, or post to multiple platforms at once. Supports text posts, multiple image attachments, video uploads, and link sharing.
---

# Social Media Poster

Post content to LinkedIn and Twitter/X from the command line. Supports posting to individual platforms or all platforms simultaneously.

## When to Use This Skill

Use this skill when the user requests:
- Posting content to LinkedIn
- Posting content to Twitter/X
- Sharing updates on social media
- Creating posts with images or videos
- Cross-posting to multiple platforms

## Supported Platforms

| Platform | Script | Features |
|----------|--------|----------|
| LinkedIn | `linkedin_poster.py` | Text, images (up to 9), videos, links with previews |
| Twitter/X | `twitter_poster.py` | Text, images (up to 4), videos, threads |
| All | `post_all.py` | Post to all platforms in parallel |

## Quick Usage

### Post to All Platforms

```bash
cd ~/.claude/skills/social-media-poster
source venv/bin/activate
python scripts/post_all.py -t "Your post content" -i "./image.jpg" -u "https://example.com"
```

### Post with Video

```bash
python scripts/post_all.py -t "Check out this video!" -v "./video.mp4"
```

### Post with Multiple Images

```bash
python scripts/post_all.py -t "Photo gallery!" -i "./img1.jpg" -i "./img2.jpg" -i "./img3.jpg"
```

### Post to LinkedIn Only

```bash
python scripts/linkedin_poster.py -t "Post text" -i "./image.jpg" -u "https://link.com" --title "Link Title"
```

### Post to Twitter/X Only

```bash
python scripts/twitter_poster.py -t "Tweet text" -i "./image.jpg"
```

Note: Long-form posts are supported by default (for premium accounts). Use `--truncate` flag for non-premium accounts (280 char limit).

## Creating Posts Workflow

When creating posts for the user:

1. **Craft platform-appropriate content**
   - LinkedIn: Professional tone, longer form, more hashtags acceptable
   - Twitter: Same content works for premium accounts (long-form supported)

2. **Handle media attachments**
   - Images: Use `-i` flag (can be used multiple times for multiple images)
   - Videos: Use `-v` flag (supports MP4, MOV, AVI, WebM)
   - LinkedIn supports up to 9 images per post
   - Twitter supports up to 4 images per tweet

3. **Include relevant elements**
   - Hashtags for discoverability
   - Links to referenced content
   - Images/videos for engagement

4. **Post to platforms**
   - Use `post_all.py` for simultaneous posting
   - Use individual scripts when content differs significantly between platforms

## Command Reference

### post_all.py

```
--text, -t       Post content (required)
--image, -i      Path to image file (can use multiple times)
--video, -v      Path to video file
--url, -u        URL to include
--title          Title for link/image/video
--platforms, -p  Specific platforms: linkedin twitter
--sequential     Post one at a time instead of parallel
```

### linkedin_poster.py

```
--text, -t       Post content (required)
--image, -i      Path to image file (can use multiple times)
--video, -v      Path to video file
--url, -u        URL for link preview
--title          Title for link/image/video
--description    Description for link/image/video
```

### twitter_poster.py

```
--text, -t       Tweet content (required)
--image, -i      Path to image (can use multiple times, max 4)
--video, -v      Path to video file
--truncate       Truncate to 280 chars (for non-premium accounts)
```

## Video Upload Details

### LinkedIn Video Requirements
- **Format**: MP4 only
- **Size**: 75 KB to 500 MB
- **Length**: 3 seconds to 30 minutes
- **Process**: Chunked upload with automatic processing

### Twitter Video Requirements
- **Format**: MP4, MOV, AVI, WebM
- **Size**: Up to 512 MB
- **Length**: Up to 2 minutes 20 seconds (140 seconds)
- **Process**: Chunked upload with async processing

### Video Upload Process

The scripts handle video uploads automatically:
1. Initialize upload with file size
2. Upload in chunks (4MB for LinkedIn, 1MB for Twitter)
3. Finalize and wait for processing
4. Create post with processed video

## First-Time Setup

For initial setup, refer to `references/setup.md` for detailed instructions on:
- Creating LinkedIn Developer App
- Creating Twitter/X Developer Account
- Obtaining API credentials
- Configuring the `.env` file

## Environment Variables

The scripts require these environment variables in a `.env` file:

```
# LinkedIn
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=

# Twitter/X
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_BEARER_TOKEN=
```

## Platform Limitations

### LinkedIn
- Access token expires in ~60 days (run `get_token.py` to refresh)
- Requires "Share on LinkedIn" product approval
- Video processing may take 1-5 minutes

### Twitter/X
- Free tier: 1,500 tweets/month limit
- Basic tier ($100/mo): 3,000 tweets/month
- Requires OAuth 1.0a with Read+Write permissions
- Video processing is async (longer videos take more time)

## Resources

### scripts/
- `linkedin_poster.py` - Post to LinkedIn (text, images, videos, links)
- `twitter_poster.py` - Post to Twitter/X (text, images, videos)
- `post_all.py` - Post to all platforms
- `get_token.py` - LinkedIn OAuth token helper
- `requirements.txt` - Python dependencies

### references/
- `setup.md` - Detailed setup instructions for both platforms
