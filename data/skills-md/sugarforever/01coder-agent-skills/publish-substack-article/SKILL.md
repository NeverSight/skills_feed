---
name: publish-substack-article
description: Publish Markdown articles to Substack as drafts. Use when user wants to publish a Markdown file to Substack, or mentions "发布到 Substack", "Substack article", "publish to Substack". Handles Markdown-to-HTML conversion and saves as draft (never auto-publish).
---

# Publish Substack Article

Publish Markdown content to Substack post editor, converting Markdown to HTML and pasting as rich text. Saves as draft for user review before publishing.

## Prerequisites

- Browser automation MCP (either one):
  - **Chrome DevTools MCP** (`mcp__chrome-devtools__*`)
  - **Playwright MCP** (`mcp__playwright__*`)
- User logged into Substack
- Python 3 with `markdown` package (`pip install markdown`)
- `copy_to_clipboard.py` script (shared from publish-zsxq-article skill)

## Browser MCP Tool Mapping

This skill works with both Chrome DevTools MCP and Playwright MCP. Use whichever is available:

| Action | Chrome DevTools MCP | Playwright MCP |
|--------|---------------------|----------------|
| Navigate | `navigate_page` | `browser_navigate` |
| Take snapshot | `take_snapshot` | `browser_snapshot` |
| Take screenshot | `take_screenshot` | `browser_take_screenshot` |
| Click element | `click` | `browser_click` |
| Fill text | `fill` | `browser_type` |
| Press key | `press_key` | `browser_press_key` |
| Evaluate JS | `evaluate_script` | `browser_evaluate` |

**Detection**: Check available tools at runtime. If `mcp__chrome-devtools__navigate_page` exists, use Chrome DevTools MCP. If `mcp__playwright__browser_navigate` exists, use Playwright MCP.

## Key URLs

- Substack dashboard: `https://{publication}.substack.com/publish`
- Post editor: `https://{publication}.substack.com/publish/post/{postId}`
- Default publication: `verysmallwoods`

## Editor Interface

The Substack post editor uses **Tiptap** (ProseMirror-based WYSIWYG editor).

### Key Elements
- Title input: `textbox "title"` (placeholder: "Title")
- Subtitle input: `textbox "Add a subtitle…"`
- Content area: `.ProseMirror` (Tiptap editor, "Start writing...")
- Save status: `button "Saved"` (auto-saves)
- Preview button: `button "Preview"`
- Continue button: `button "Continue"` (publish flow - DO NOT USE)
- Settings sidebar: `button "Settings"` (title, description, thumbnail)

### Settings Sidebar (left panel)
When "Settings" or "File Settings" is open:
- Title: `textbox "Add a title..."`
- Description: `textbox "Add a description..."`
- Thumbnail: Upload button (3:2 aspect ratio)

### Toolbar
Bold, Italic, Strikethrough, Code, Link, Image, Audio, Video, Quote, Lists (bullet/ordered), Button, More (Code block, Divider, Footnote, LaTeX, etc.)

## Content Insertion Method

**CRITICAL: Use clipboard paste with HTML content**, NOT direct fill or plain Markdown paste.

The Tiptap editor handles HTML paste natively and renders it as rich content. The workflow is:

1. Convert Markdown to HTML using Python's `markdown` library
2. Copy HTML to system clipboard using `copy_to_clipboard.py html`
3. Focus the editor content area
4. Press Cmd+V (macOS) or Ctrl+V (Windows/Linux) to paste

**Why HTML paste?**
- `fill` tool → Content treated as plain text, no formatting
- Plain Markdown paste → Tiptap does NOT parse Markdown on paste
- HTML paste → Tiptap renders HTML as rich content (headings, code blocks, links, bold, etc.)

**Known limitation**: Substack's editor does NOT support HTML tables. Tables will be collapsed into plain text. See **Step 0: Pre-Processing** for converting tables to images.

## Main Workflow

### Step 0: Pre-Processing — Convert Tables to Images

Substack does NOT render HTML tables. They collapse into plain text. Any Markdown table must be converted to a PNG image and uploaded separately.

**Workflow:**

1. **Detect tables** in the Markdown file (lines with `|` forming table structure)

2. **Create styled HTML** for each table:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: white; }
table { border-collapse: collapse; width: 100%; font-size: 15px; line-height: 1.6; }
th { background: #f8f8f8; font-weight: 600; text-align: left; padding: 10px 16px; border-bottom: 2px solid #e0e0e0; }
td { padding: 8px 16px; border-bottom: 1px solid #eee; }
tr:hover { background: #fafafa; }
code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 13px; font-family: 'SF Mono', Menlo, monospace; }
</style>
</head>
<body>
<table>
<!-- table content here -->
</table>
</body>
</html>
```

3. **Render to screenshot**: Open the HTML file in a browser tab, take a screenshot, close the tab:

```
# Open HTML in new tab
browser_navigate or new_page: file:///tmp/table1.html

# Take screenshot
browser_take_screenshot: filename=/tmp/table1.png, fullPage=true

# Close tab and return to editor
browser_tabs: action=close
```

4. **Note the position** of each table in the article for later insertion (after which heading/paragraph)

5. **Remove table Markdown** from the content before HTML conversion (so it won't appear as plain text in the pasted content)

**Image upload** happens after pasting the main content — see Step 7.

### Step 1: Prepare Content

Read the Markdown file and extract:
- **Title**: from YAML frontmatter `title` field, or H1 header `# Title`, or filename
- **Subtitle**: from YAML frontmatter `excerpt` or `description` field
- **Content**: full Markdown body (strip YAML frontmatter and any cross-reference links)

### Step 2: Convert Markdown to HTML

Use Python's `markdown` library with `tables` and `fenced_code` extensions:

```python
import markdown
import re

with open('/path/to/article.md', 'r') as f:
    content = f.read()

# Strip YAML frontmatter
content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

# Strip cross-reference links (e.g., English version link)
# Adjust pattern as needed for your articles
content = re.sub(r'^> .* available at.*\n\n?', '', content, flags=re.MULTILINE)

# Convert to HTML
html = markdown.markdown(content, extensions=['tables', 'fenced_code'])

# Write to temp file
with open('/tmp/substack_article.html', 'w') as f:
    f.write(html)
```

**IMPORTANT**: Do NOT use `nl2br` extension - it converts single newlines to `<br>` tags, causing extra line breaks in the editor.

### Step 3: Navigate to Substack

Navigate to the Substack dashboard and create a new post:

```
# Navigate to Substack dashboard
navigate to: https://verysmallwoods.substack.com/publish
```

If not logged in, prompt user to log in:
```
请先登录 Substack，登录完成后告诉我。
Please log in to Substack first, then let me know.
```

### Step 4: Create New Post

From the dashboard, create a new text post:
1. Click "Create new" in the sidebar
2. Select "Text post" (or navigate directly to a new post URL)

Alternatively, if the editor is already open with an empty post, proceed directly.

### Step 5: Fill Title and Subtitle

1. Click the title textbox (`textbox "title"`)
2. Type the article title
3. Click the subtitle textbox (`textbox "Add a subtitle…"`)
4. Type the subtitle/excerpt

```
click: title textbox
fill/type: article title

click: subtitle textbox
fill/type: article subtitle
```

### Step 6: Insert HTML Content (via Clipboard Paste)

**CRITICAL: Do NOT use `fill` tool** - it inserts plain text without formatting.

1. Copy HTML to system clipboard:

```bash
python3 /path/to/copy_to_clipboard.py html --file /tmp/substack_article.html
```

2. Click the editor content area (`.ProseMirror` or paragraph element inside it)

3. Press Cmd+V to paste:

```
press_key: Meta+v  (macOS)
press_key: Control+v  (Windows/Linux)
```

This triggers Tiptap's HTML paste handler, which renders the content as rich text with proper formatting.

### Step 7: Insert Table Images

If the article had tables converted to images in Step 0, insert them now:

1. **Navigate to the correct position** in the editor — click on the paragraph or empty line where the table should appear (after the relevant heading/text)

2. **Click the Image toolbar button** (`button "Image"`) — a dropdown menu appears with options: Image, Gallery, Stock photos, Generate image

3. **Click "Image" menuitem** from the dropdown — a file chooser dialog opens

4. **Upload the image** via file chooser:
   - Playwright MCP: `browser_file_upload` with the image path
   - Chrome DevTools MCP: `upload_file` with the image path

**Important notes:**
- **File path restriction**: Playwright MCP only allows file uploads from within allowed roots (project directories). If your image is in `/tmp/`, copy it to the project directory first
- **Repeat for each table**: Position cursor at the correct location, then upload each table image
- **Delete residual text**: If table content was pasted as plain text (because it wasn't removed in pre-processing), select it (triple-click to select paragraph) and delete before inserting the image

### Step 8: Verify Draft

After pasting:
1. Check the "Saved" status indicator (green dot + "Saved" text)
2. Take a snapshot to verify content structure
3. Optionally take a screenshot for visual verification

The editor auto-saves, so no explicit save action is needed.

### Step 9: Report Completion

```
草稿已保存到 Substack。请在 Substack 中预览并手动发布。
Draft saved to Substack. Please preview and publish manually.

Post URL: https://verysmallwoods.substack.com/publish/post/{postId}
```

## Complete Example Flow

User: "把 /path/to/my-article.md 发布到 Substack"

```
0. Pre-process tables (if any)
   - Detect Markdown tables
   - Create styled HTML for each table
   - Render to screenshots (open in browser, screenshot, close tab)
   - Remove table Markdown from content
   - Note insertion positions

1. Read /path/to/my-article.md
   - Extract title from frontmatter or H1
   - Extract subtitle from frontmatter excerpt
   - Get full Markdown content (with tables removed)

2. Convert Markdown to HTML
   - Strip frontmatter
   - Use markdown.markdown() with ['tables', 'fenced_code']
   - Write to /tmp/substack_article.html

3. Navigate to Substack dashboard or new post

4. Check if logged in
   - If not, prompt user to login

5. Fill title and subtitle

6. Copy HTML to clipboard + Paste
   - python3 copy_to_clipboard.py html --file /tmp/substack_article.html
   - Click editor content area
   - Press Cmd+V

7. Insert table images at correct positions
   - For each table: click position → Image button → Image menuitem → file upload

8. Verify draft saved
   - Check "Saved" status

9. Report success
   - "草稿已保存，请手动预览并发布"
```

## Critical Rules

1. **NEVER click "Continue"** - This starts the publish flow. Only save as draft (auto-save handles this)
2. **Always convert to HTML first** - Plain Markdown will not be parsed by the Tiptap editor
3. **Use clipboard paste** - The only reliable way to insert formatted content
4. **Check login status** - Prompt user to login if needed
5. **Preserve original file** - Never modify the source Markdown file
6. **Report completion** - Tell user the draft is saved and needs manual review
7. **No `nl2br` extension** - Causes double line breaks
8. **Tables → images** - Pre-process tables before pasting content; upload images after paste
9. **Playwright file paths** - Playwright MCP restricts file uploads to allowed roots; copy temp files to project directory before uploading

## Troubleshooting

### Content Shows as Plain Text (No Formatting)
If you see raw HTML tags or unformatted text:
- **Cause**: Content was inserted using `fill` tool instead of clipboard paste
- **Solution**: Use the `copy_to_clipboard.py` + Cmd+V method (see Step 6)

### Tables Not Rendering (Shows Plain Text)
Substack's Tiptap editor does not support HTML tables. They collapse into inline plain text.
- **Solution**: Convert tables to styled HTML → render as screenshots → upload as images (see Step 0 and Step 7)
- **Alternative**: Restructure simple tables as formatted lists
- **If plain text already pasted**: Triple-click the plain text paragraph to select it, press Backspace to delete, then insert the table image at that position

### Login Required
If page shows login prompt:
```
请先登录 Substack: https://verysmallwoods.substack.com
登录完成后告诉我。
```

### Editor Not Loading
If editor elements are not visible:
1. Wait for page to fully load
2. Take a new snapshot
3. If still not loading, refresh the page

### Clipboard Copy Fails
If `copy_to_clipboard.py` fails:
- Ensure dependencies: `pip install pyobjc-framework-Cocoa` (macOS)
- Check the HTML file exists and is readable
- Try copying a smaller test string first

## Element Reference

| Element | Selector/Identifier | Description |
|---------|---------------------|-------------|
| Title input | `textbox "title"` | Post title |
| Subtitle input | `textbox "Add a subtitle…"` | Post subtitle |
| Content area | `.ProseMirror` (Tiptap editor) | Post content |
| Save status | `button "Saved"` | Auto-save indicator |
| Preview button | `button "Preview"` | Preview post |
| Continue button | `button "Continue"` | DO NOT USE - starts publish flow |
| Settings button | `button "Settings"` | Open settings sidebar |
| Exit button | `button "Exit"` | Exit editor |
| Image button | `button "Image"` | Opens image upload dropdown |
| Image menuitem | `menuitem "Image"` | Opens file chooser for image upload |
| Author button | `button "{PublicationName}"` | Author/publication selector |

## Technical Details

### Editor Stack
- **Tiptap**: A headless, framework-agnostic rich-text editor built on ProseMirror
- **ProseMirror**: The underlying rich-text editing framework
- **Paste handling**: Tiptap natively parses HTML from clipboard and converts to its internal document model

### Content Conversion Pipeline
```
Markdown file
    ↓ (Python markdown library)
HTML string
    ↓ (copy_to_clipboard.py)
System clipboard (text/html + text/plain)
    ↓ (Cmd+V keyboard shortcut)
Tiptap ProseMirror editor
    ↓ (auto-save)
Substack draft
```

### Supported Formatting
The following Markdown elements are correctly rendered after HTML conversion and paste:

| Markdown Element | Substack Support | Notes |
|-----------------|-----------------|-------|
| Headings (H2-H6) | Yes | H1 not recommended (title is separate) |
| Bold / Italic | Yes | |
| Inline code | Yes | |
| Code blocks | Yes | Syntax highlighting may vary |
| Links | Yes | |
| Blockquotes | Yes | |
| Bullet lists | Yes | |
| Ordered lists | Yes | |
| Horizontal rules | Yes | |
| Tables | No → Image | Convert to styled HTML, screenshot, upload as image |
| Images | Manual | Upload via Image toolbar button → file chooser |
