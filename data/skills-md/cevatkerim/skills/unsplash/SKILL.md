---
name: unsplash
description: Search and fetch photos from Unsplash with proper attribution. Use when users need images for content, want photos by keyword, need random images for variety, or ask for stock photos. Automatically provides attribution required by Unsplash guidelines.
version: 1.0.0
license: MIT
---

# Unsplash Photo Search

Search and fetch high-quality photos from Unsplash with automatic attribution.

## Quick Start

```bash
# Search for photos
./scripts/search.sh "sunset beach"

# Get random photos
./scripts/random.sh "nature" 3

# Track download (when user downloads)
./scripts/track.sh PHOTO_ID
```

## Setup (Interactive)

**IMPORTANT:** If the script returns `UNSPLASH_ACCESS_KEY not set`, handle it interactively:

1. Ask the user: "I need an Unsplash API key to search for photos. You can get a free key at https://unsplash.com/developers - do you have one?"

2. Wait for the user to provide their key

3. Save the key to `.env` in the project root:
   ```bash
   echo "UNSPLASH_ACCESS_KEY=<user_provided_key>" >> .env
   ```

4. Re-run the original search/random command

The skill automatically loads `.env` from the project root on each run.

## Operations

### 1. Search Photos

Find photos by keyword with optional filters.

```bash
./scripts/search.sh QUERY [PAGE] [PER_PAGE] [ORDER_BY] [ORIENTATION] [COLOR]
```

**Parameters:**
- `QUERY` (required): Search keyword(s)
- `PAGE` (optional, default: 1): Page number for pagination
- `PER_PAGE` (optional, default: 10): Results per page (1-30)
- `ORDER_BY` (optional, default: "relevant"): Sort order ("relevant" or "latest")
- `ORIENTATION` (optional): Filter by orientation ("landscape", "portrait", "squarish")
- `COLOR` (optional): Filter by color ("black_and_white", "black", "white", "yellow", "orange", "red", "purple", "magenta", "green", "teal", "blue")

**Examples:**
```bash
# Basic search
./scripts/search.sh "mountain landscape"

# Search with filters
./scripts/search.sh "sunset" 1 5 latest landscape

# Search by color
./scripts/search.sh "flower" 1 10 relevant portrait red
```

### 2. Random Photos

Get random photos with optional filtering.

```bash
./scripts/random.sh [QUERY] [COUNT] [ORIENTATION]
```

**Parameters:**
- `QUERY` (optional): Topic/keyword to filter random photos
- `COUNT` (optional, default: 1): Number of photos (1-30)
- `ORIENTATION` (optional): Filter by orientation ("landscape", "portrait", "squarish")

**Examples:**
```bash
# Single random photo
./scripts/random.sh

# Random photos by topic
./scripts/random.sh "architecture" 5

# Random landscape photos
./scripts/random.sh "nature" 3 landscape
```

### 3. Track Download

Track when a user downloads a photo (required by Unsplash API guidelines).

```bash
./scripts/track.sh PHOTO_ID
```

**When to call:**
- When user actually downloads/saves the image file
- NOT when just viewing or displaying the photo
- Helps photographers get credit for downloads

**Example:**
```bash
./scripts/track.sh "abc123xyz"
```

## Output Format

All operations return JSON with complete photo information:

```json
{
  "id": "abc123xyz",
  "description": "A beautiful sunset over mountains",
  "alt_description": "orange sunset behind mountain range",
  "urls": {
    "raw": "https://...",
    "full": "https://...",
    "regular": "https://...",
    "small": "https://...",
    "thumb": "https://..."
  },
  "width": 6000,
  "height": 4000,
  "color": "#f3a460",
  "blur_hash": "L8H2#8-;00~q4n",
  "photographer_name": "Jane Smith",
  "photographer_username": "janesmith",
  "photographer_url": "https://unsplash.com/@janesmith?utm_source=claude_skill&utm_medium=referral",
  "photo_url": "https://unsplash.com/photos/abc123xyz?utm_source=claude_skill&utm_medium=referral",
  "attribution_text": "Photo by Jane Smith on Unsplash",
  "attribution_html": "Photo by <a href=\"https://unsplash.com/@janesmith?utm_source=claude_skill&utm_medium=referral\">Jane Smith</a> on <a href=\"https://unsplash.com/?utm_source=claude_skill&utm_medium=referral\">Unsplash</a>"
}
```

## Image URLs

The `urls` object contains different sizes:
- **raw**: Original unprocessed image
- **full**: Full resolution (max width/height: 5472px)
- **regular**: Web display size (1080px wide)
- **small**: Thumbnail (400px wide)
- **thumb**: Small thumbnail (200px wide)

**Recommended:** Use `urls.regular` for most web content (best quality/size balance).

## Attribution Requirements

**CRITICAL:** Unsplash requires attribution for all image usage.

### Always Include Attribution

When presenting photos to users, you MUST include one of:

1. **attribution_text** (for plain text contexts):
   ```
   Photo by Jane Smith on Unsplash
   ```

2. **attribution_html** (for HTML/web contexts):
   ```html
   Photo by <a href="...">Jane Smith</a> on <a href="...">Unsplash</a>
   ```

### Placement Guidelines

- Place attribution near the image (below or in caption)
- Make it visible and readable
- Don't remove or hide the attribution
- Attribution is required by Unsplash API terms

### Why Attribution Matters

- Gives credit to photographers
- Required by Unsplash API terms of service
- Violating attribution can result in API access suspension

## Common Workflows

### Blog Post Hero Image

```bash
# Search for relevant image
./scripts/search.sh "technology workspace" 1 3 latest landscape

# Present options to user with attribution
# User selects one
# Display image with attribution_html in blog post
```

### Gallery of Random Images

```bash
# Get variety of images
./scripts/random.sh "travel" 10

# Display all images with their attributions
```

### Specific Color Palette

```bash
# Search for images matching brand colors
./scripts/search.sh "abstract" 1 5 latest "" blue
```

## Error Handling

**Missing API Key:**
```
ERROR: UNSPLASH_ACCESS_KEY not set
```
→ See "Setup (Interactive)" section above. Ask user for key, save to `.env`, and retry.

**Rate Limit Exceeded:**
```
ERROR: Rate limit exceeded (50/hour in demo mode)
```
Wait an hour or use production credentials with higher limits.

**Invalid API Key:**
```
ERROR: Invalid API key
```
Check that your API key is correct.

**No Results:**
```json
[]
```
Empty array returned if no photos match search criteria.

## Dependencies

Required tools (standard on macOS/Linux):
- `bash` - Shell interpreter
- `curl` - HTTP client
- `jq` - JSON processor

Install jq if missing:
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq
```

## Rate Limits

- **Demo mode**: 50 requests/hour
- **Production mode**: 5,000 requests/hour

Production mode requires:
1. Creating an Unsplash app
2. Getting app approval from Unsplash
3. Using your production access key

## Best Practices

1. **Use specific search terms** - More specific queries yield better results
2. **Filter by orientation** - Match your layout needs (landscape/portrait)
3. **Always include attribution** - Required by API terms
4. **Use regular size for web** - Best quality/performance balance
5. **Track actual downloads** - Only call track.sh when user downloads
6. **Cache results** - Don't re-search for the same keywords
7. **Respect rate limits** - Monitor usage in demo mode

## More Examples

See detailed usage patterns in: `examples/usage-examples.md`

## Troubleshooting

**Scripts not executable:**
```bash
chmod +x scripts/*.sh
```

**jq not found:**
```bash
brew install jq  # macOS
```

**API errors:**
- Check internet connection
- Verify API key is set correctly
- Check rate limit hasn't been exceeded
- Ensure photo_id is valid (for track.sh)

## Links

- Unsplash API Documentation: https://unsplash.com/documentation
- Get API Key: https://unsplash.com/developers
- Unsplash Guidelines: https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines
