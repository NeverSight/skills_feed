---
name: publish-zsxq-article
description: Publish Markdown articles to Zsxq (知识星球) as drafts. Use when user wants to publish a Markdown file to Zsxq, or mentions "发布到知识星球", "星球文章", "zsxq article". Handles Markdown content input and saves as draft (never auto-publish).
---

# Publish Zsxq Article

Publish Markdown content to Zsxq (知识星球) article editor in Markdown mode, saving as draft for user review before publishing.

## Prerequisites

- Browser automation MCP (either one):
  - **Chrome DevTools MCP** (`mcp__chrome-devtools__*`)
  - **Playwright MCP** (`mcp__playwright__*`)
- User logged into Zsxq (知识星球)

## Browser MCP Tool Mapping

This skill works with both Chrome DevTools MCP and Playwright MCP. Use whichever is available:

| Action | Chrome DevTools MCP | Playwright MCP |
|--------|---------------------|----------------|
| Navigate | `navigate_page` | `browser_navigate` |
| Take snapshot | `take_snapshot` | `browser_snapshot` |
| Take screenshot | `take_screenshot` | `browser_take_screenshot` |
| Click element | `click` | `browser_click` |
| Fill text | `fill` | `browser_type` |
| Upload file | `upload_file` | `browser_file_upload` |
| Press key | `press_key` | `browser_press_key` |
| Evaluate JS | `evaluate_script` | `browser_console_exec` |

**Detection**: Check available tools at runtime. If `mcp__chrome-devtools__navigate_page` exists, use Chrome DevTools MCP. If `mcp__playwright__browser_navigate` exists, use Playwright MCP.

## Key URLs

- Login page: `https://wx.zsxq.com/login`
- Article editor: `https://wx.zsxq.com/article?groupId={groupId}`
- Default group ID: `51111858848454` (小木头的AI星球)

## Editor Interface

The Zsxq article editor has two modes:

### Rich Text Mode (Default)
- Standard WYSIWYG editor with formatting toolbar
- Click "切换到 Markdown 模式 (内测)" to switch

### Markdown Mode (Preferred)
- Uses **Milkdown** (ProseMirror-based WYSIWYG Markdown editor)
- Renders Markdown as formatted content (headings, bold, links, lists)
- Click "切换到富文本模式" to switch back

**IMPORTANT: Content Insertion Method**
The Milkdown editor requires content to be inserted via **paste event**, NOT direct fill:
- `fill` tool → Content treated as plain text, Markdown NOT rendered
- Paste event → Milkdown parses Markdown and renders it properly

### Key Elements in Markdown Mode
- Title input: textbox "请在这里输入标题"
- Content area: ProseMirror editor (`.ProseMirror` class)
- Save button: "保存" (saves as draft)
- Preview button: "预览"
- Publish button: "发布" (DO NOT USE - always save as draft)
- Tags: "添加标签"

## Main Workflow

### Step 1: Prepare Content

Read the Markdown file and extract:
- Title (from H1 header `# Title` or filename)
- Content (full Markdown body)

```bash
# Read the markdown file
cat /path/to/article.md
```

### Step 2: Navigate to Article Editor

```
# Navigate to the article editor with group ID
navigate_page: https://wx.zsxq.com/article?groupId=51111858848454
```

If not logged in, the page will redirect to login. Prompt user to log in manually:
```
请先登录知识星球，登录完成后告诉我。
Login URL: https://wx.zsxq.com/login
```

### Step 3: Switch to Markdown Mode

After page loads, check if already in Markdown mode by looking for "切换到富文本模式" text.

If in Rich Text mode (shows "切换到 Markdown 模式"):
1. Click "切换到 Markdown 模式 (内测)"
2. Confirm the dialog by clicking "确定"

```javascript
// Check current mode
const switchBtn = document.querySelector('[class*="switch"]');
if (switchBtn && switchBtn.innerText.includes('切换到 Markdown')) {
  // Need to switch to Markdown mode
}
```

### Step 4: Fill Title

1. Find the title textbox with placeholder "请在这里输入标题"
2. Click to focus
3. Type the title

```
click: title textbox
fill: title textbox with article title
```

### Step 5: Insert Markdown Content (via Paste Event)

**CRITICAL: Do NOT use `fill` tool** - it inserts plain text without Markdown rendering.

Instead, use `evaluate_script` to simulate a paste event:

```javascript
// Simulate paste event to trigger Milkdown's Markdown parsing
() => {
  const markdownContent = `YOUR_MARKDOWN_CONTENT_HERE`;

  const editorEl = document.querySelector('.ProseMirror');
  if (!editorEl) return { error: 'Editor not found' };

  // Focus the editor
  editorEl.focus();

  // Create and dispatch paste event
  const clipboardData = new DataTransfer();
  clipboardData.setData('text/plain', markdownContent);

  const pasteEvent = new ClipboardEvent('paste', {
    bubbles: true,
    cancelable: true,
    clipboardData: clipboardData
  });

  editorEl.dispatchEvent(pasteEvent);

  return { success: true, charCount: markdownContent.length };
}
```

This method:
1. Creates a ClipboardEvent with the Markdown content
2. Dispatches it to the ProseMirror editor
3. Milkdown's paste handler parses and renders the Markdown

### Step 6: Add Tags (Optional)

1. Click "添加标签"
2. Enter tag text
3. Confirm

### Step 7: Save as Draft

**IMPORTANT: Always save as draft, NEVER click "发布" (Publish)**

1. Click "保存" button to save as draft
2. Verify save was successful

```
click: "保存" button
```

### Step 8: Verify and Report

After saving:
1. Check for success message or draft status
2. Report to user:
```
草稿已保存。请在知识星球中预览并手动发布。
Draft saved. Please review in Zsxq and publish manually.
```

## Complete Example Flow

User: "把 /path/to/my-article.md 发布到知识星球"

```
1. Read /path/to/my-article.md
   - Extract title from H1 or first line
   - Get full content

2. Navigate to https://wx.zsxq.com/article?groupId=51111858848454

3. Check if logged in
   - If not, prompt user to login

4. Switch to Markdown mode if needed
   - Click "切换到 Markdown 模式 (内测)"
   - Confirm dialog

5. Fill title
   - Click title input
   - Use `fill` tool to set title text

6. Insert content via paste event
   - Use `evaluate_script` to simulate paste event
   - This triggers Milkdown to parse and render Markdown

7. Save as draft
   - Click "保存"

8. Report success
   - "草稿已保存，请手动预览并发布"
```

## Critical Rules

1. **NEVER click "发布"** - Only save as draft using "保存"
2. **Always use Markdown mode** - Switch if in Rich Text mode
3. **Check login status** - Prompt user to login if needed
4. **Preserve original file** - Never modify the source Markdown file
5. **Report completion** - Tell user the draft is saved and needs manual review

## Troubleshooting

### Markdown Not Rendering (Shows Raw Syntax)
If you see raw Markdown syntax like `**bold**` or `[link](url)` instead of rendered formatting:
- **Cause**: Content was inserted using `fill` tool instead of paste event
- **Solution**: Use the `evaluate_script` method to simulate a paste event (see Step 5)

The Milkdown editor only parses Markdown when content is pasted, not when directly set.

### Login Required
If page redirects or shows login prompt:
```
请先登录知识星球: https://wx.zsxq.com/login
登录完成后告诉我。
```

### Content Too Long
Zsxq has a 100,000 character limit. If content exceeds:
```
文章内容超过100000字符限制，请考虑拆分文章。
```

### Switch Mode Dialog
When switching to Markdown mode, a confirmation dialog appears:
- Message: "确定要切换编辑器？当前内容将不会同步至新编辑器"
- Click "确定" to confirm

### Editor Not Loading
If editor elements are not visible:
1. Wait for page to fully load
2. Take a new snapshot
3. If still not loading, refresh the page

## Element Reference

| Element | Selector/Identifier | Description |
|---------|---------------------|-------------|
| Title input | textbox "请在这里输入标题" | Article title (max 60 chars) |
| Content area | `.ProseMirror` (Milkdown editor) | Markdown content (max 100000 chars) |
| Save button | "保存" | Save as draft |
| Preview button | "预览" | Preview article |
| Publish button | "发布" | DO NOT USE |
| Mode switch | "切换到 Markdown 模式" / "切换到富文本模式" | Toggle editor mode |
| Tags | "添加标签" | Add article tags |
| Word count | "正文字数：X /100000" | Character counter |

## Image Upload

Image upload works in **both** Rich Text mode and Markdown mode using the `upload_file` tool.

### Prerequisites
- Check image file size first: if > 500KB, compress to WebP or reduce quality
- Use `ls -la /path/to/image.png` to check file size

### Image Upload Workflow

Image upload works with the image button in both editor modes:

1. **Take snapshot** to find the image button ref/uid
   - Rich Text mode: `button "image"`
   - Markdown mode: `generic description="Add image"`

2. **Upload image**

   Chrome DevTools MCP:
   ```
   upload_file:
     uid: <image button uid>
     filePath: /path/to/image.png
   ```

   Playwright MCP:
   ```
   browser_file_upload:
     ref: <image button ref>
     paths: ["/path/to/image.png"]
   ```

3. **Verify upload** - take screenshot to confirm image appears in editor

### Key Elements for Image Upload

| Mode | Image Button | Selector in Snapshot |
|------|-------------|---------------------|
| Rich Text | button "image" | `button "image"` |
| Markdown | Add image | `generic description="Add image"` |

### Example Image Upload (Markdown Mode)

```
# 1. Take verbose snapshot to find image button
take_snapshot(verbose=true)

# 2. Find "Add image" button (e.g., uid=26_59)
# Look for: generic description="Add image"

# 3. Upload image directly to the button
upload_file:
  uid: 26_59  # (example uid for "Add image" button)
  filePath: /Users/user/Downloads/image.png

# 4. Verify with screenshot
take_screenshot
```

### Example Image Upload (Rich Text Mode)

```
# 1. Take snapshot to find image button
take_snapshot

# 2. Find image button (e.g., uid=12_7)
# Look for: button "image"

# 3. Upload image to the button
upload_file:
  uid: 12_7  # (example uid for image button)
  filePath: /Users/user/Downloads/image.png

# 4. Verify with screenshot
take_screenshot
```

### Image Size Limits
- Maximum recommended: 500KB per image
- For larger images, compress first using tools like ImageMagick or sips:
  ```bash
  # Check size
  ls -la /path/to/image.png

  # Compress if needed (macOS)
  sips -s format jpeg -s formatOptions 80 /path/to/image.png --out /path/to/image_compressed.jpg
  ```

### Troubleshooting Image Upload

**Image not appearing after upload:**
- Take a fresh verbose snapshot to get correct uid for image button
- Verify the image file exists and is accessible
- Check the word count indicator - it should increase after successful upload

**Finding the correct button uid:**
- Use `take_snapshot(verbose=true)` to see element descriptions
- In Markdown mode, look for `generic description="Add image"`
- In Rich Text mode, look for `button "image"`

## Technical Details

The Zsxq article editor uses two different editors:

### Rich Text Mode (Quill)
- **Quill**: A modern WYSIWYG editor
- **Image upload**: Works via `upload_file` tool to `button "image"`
- **Toolbar**: Standard formatting buttons including image

### Markdown Mode (Milkdown)
- **Milkdown**: A plugin-driven WYSIWYG markdown editor
- **ProseMirror**: The underlying rich-text editing framework
- **Paste handling**: Milkdown intercepts paste events and parses Markdown content
- **Image upload**: Works via `upload_file` tool to `generic description="Add image"`

This is why the user's workflow via md.bytenote.net works - pasting from any source triggers Milkdown's Markdown parser, resulting in properly rendered content.
