---
name: wechat-article-formatter
description: Convert markdown to styled HTML for WeChat articles with auto image upload
---

# WeChat Article Formatter Skill

This skill formats markdown files into styled HTML optimized for WeChat public account articles using the bm.md rendering service.

## Overview

The skill performs the following workflow:
1. Reads the provided markdown file or content
2. Loads custom CSS styling from the `styles/custom.css` file in this skill's directory
3. **Scans for local images, uploads them, and replaces paths with online URLs**
4. Calls the bm.md API to render the markdown with WeChat-optimized styling
5. Outputs the formatted HTML that can be directly pasted into WeChat's article editor

## Usage

When the user invokes this skill, you should:

### Step 1: Identify the Input

The user will provide one of the following:
- A file path to a markdown file (e.g., `/path/to/article.md`)
- Raw markdown content directly in the conversation

If the input is unclear, ask the user to provide either a markdown file path or paste the markdown content directly.

### Step 2: Read the Custom CSS

Read the custom CSS file from this skill's directory:

```
{{SKILL_DIR}}/styles/custom.css
```

Use the Read tool to get the CSS content. This CSS provides the custom styling for the WeChat article.

### Step 3: Upload Local Images

Before rendering, scan the markdown content for local image references and upload them to get online URLs.

#### 3.1 Find All Image References

Parse the markdown to find all image references using the pattern `![alt](path)`. Look for:

- Standard markdown images: `![alt text](path/to/image.png)`
- Images with titles: `![alt text](path/to/image.png "title")`

#### 3.2 Identify Local Image Paths

For each image found, determine if it's a local file that needs uploading:

**Local paths (need upload):**
- Absolute paths starting with `/`: `/Users/james/images/photo.png`
- Relative paths: `./images/photo.png`, `../assets/image.jpg`, `images/pic.png`

**Already online (skip):**
- URLs starting with `http://` or `https://`
- Data URIs starting with `data:`

#### 3.3 Resolve Absolute Paths

For each local image, calculate its absolute path:

**If the user provided a markdown file path:**
- Use the markdown file's directory as the base directory
- For relative paths like `./images/photo.png` in `/Users/james/articles/post.md`:
  - Base directory: `/Users/james/articles/`
  - Absolute path: `/Users/james/articles/images/photo.png`

**If the user provided raw markdown content:**
- Ask the user for the base directory to resolve relative paths, OR
- Skip images with relative paths and inform the user they need to provide absolute paths

#### 3.4 Upload Images Using /image-upload Skill

For each local image with a valid absolute path:

1. Invoke the `/image-upload` skill with the absolute image path
2. The skill will upload the image and return an online URL
3. Keep a mapping of `original_path -> online_url`

Example invocation:
```
/image-upload /Users/james/articles/images/photo.png
```

The `/image-upload` skill will return a URL like `https://files.catbox.moe/abc123.png`.

#### 3.5 Replace Paths in Markdown

After all images are uploaded, replace the local paths in the markdown content with their corresponding online URLs:

**Before:**
```markdown
![My Photo](./images/photo.png)
![Screenshot](/Users/james/screenshots/demo.png)
```

**After:**
```markdown
![My Photo](https://files.catbox.moe/abc123.png)
![Screenshot](https://files.catbox.moe/def456.png)
```

**Important Notes:**
- Preserve the alt text and title exactly as they were
- Only replace the path portion of the image reference
- If an image upload fails, report the error and keep the original path (the user can fix it manually)
- Process images sequentially to avoid rate limiting

#### 3.6 Report Upload Summary

After processing all images, provide a summary:

```
Image Upload Summary:
✓ Uploaded: ./images/photo.png → https://files.catbox.moe/abc123.png
✓ Uploaded: /Users/james/screenshots/demo.png → https://files.catbox.moe/def456.png
✗ Failed: ./images/missing.png (File not found)
⊘ Skipped: https://example.com/existing.png (Already online)

Total: 2 uploaded, 1 failed, 1 skipped
```

### Step 4: Call the bm.md API

Make a POST request to the bm.md rendering API with the following configuration:

**Endpoint:** `POST https://bm.md/api/markdown/render`

**Request Body:**
```json
{
  "markdown": "<the markdown content>",
  "markdownStyle": "green-simple",
  "platform": "wechat",
  "enableFootnoteLinks": true,
  "openLinksInNewWindow": true,
  "customCss": "<content from {{SKILL_DIR}}/styles/custom.css as string>"
}
```

**Parameter Details:**
| Parameter | Type | Value | Description |
|-----------|------|-------|-------------|
| `markdown` | string | (content) | The markdown content to render |
| `markdownStyle` | string | `"green-simple"` | Base styling theme for the rendered output |
| `platform` | string | `"wechat"` | Target platform optimization |
| `enableFootnoteLinks` | boolean | `true` | Convert links to footnotes |
| `openLinksInNewWindow` | boolean | `true` | Links open in new window |
| `customCss` | string | (CSS content) | Custom CSS from `styles/custom.css` file |

Use the Bash tool with curl to make the API request:

```bash
curl -X POST https://bm.md/api/markdown/render \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "<escaped markdown content>",
    "markdownStyle": "green-simple",
    "platform": "wechat",
    "enableFootnoteLinks": true,
    "openLinksInNewWindow": true,
    "customCss": "<escaped CSS content from styles/custom.css>"
  }'
```

**Important Notes:**
- `markdownStyle` must be exactly `"green-simple"` (lowercase with hyphen)
- `customCss` should contain the entire CSS file content as a JSON-escaped string
- Properly escape the markdown and CSS content for JSON (escape quotes, newlines, backslashes, etc.)
- The response will be JSON with the rendered HTML in the `result` field

### Step 5: Output the Result

After receiving the API response:

1. Extract the HTML from the `result` field in the JSON response
2. Save the HTML to a file (default: same name as input with `.html` extension, or `output.html` if content was provided directly)
3. Display a success message with the output file path

### Step 6: Offer to Publish (Optional)

After formatting is complete, ask the user if they want to publish the article to WeChat:

> "The article has been formatted and saved to `<output_path>`. Would you like me to publish it as a draft to your WeChat public account using the `/wechat-article-publisher` skill?"

If the user confirms, invoke the `/wechat-article-publisher` skill with the formatted HTML content.

## Example Workflow

**User:** Format my article at `/Users/james/articles/my-post.md`

**Assistant Actions:**
1. Read the markdown file at `/Users/james/articles/my-post.md`
2. Read the custom CSS from this skill's `styles/custom.css`
3. Scan markdown for local images:
   - Find `![Demo](./images/demo.png)` and `![Screenshot](../screenshots/app.png)`
   - Resolve paths: `/Users/james/articles/images/demo.png`, `/Users/james/screenshots/app.png`
   - Upload each image using `/image-upload` skill
   - Replace paths with returned URLs
4. Call the bm.md API with the updated markdown and CSS
5. Save the result to `/Users/james/articles/my-post.html`
6. Report success (including image upload summary) and ask about publishing

## API Response Format

The bm.md API returns:
```json
{
  "result": "<div id=\"bm-md\">...</div>"
}
```

The `result` field contains the fully styled HTML with inline CSS, ready to be copied into WeChat's rich text editor.

## Styling Features

The custom CSS provides:
- Clean typography with Optima/Microsoft YaHei fonts
- Green accent color theme (rgb(53, 179, 120))
- Properly styled headings, paragraphs, and lists
- Code blocks with syntax highlighting
- Blockquotes with left border accent
- Responsive tables
- Optimized spacing for mobile reading

## Error Handling

If the API call fails:
1. Display the error message to the user
2. Suggest checking the markdown content for any issues
3. Offer to retry the request

If the markdown file cannot be read:
1. Verify the file path exists
2. Check file permissions
3. Report the specific error to the user

## Dependencies

This skill integrates with:
- `/image-upload` - For uploading local images to hosting providers and getting shareable URLs (required for local image support)
- `/wechat-article-publisher` - For publishing formatted articles as drafts to WeChat public accounts (optional)
