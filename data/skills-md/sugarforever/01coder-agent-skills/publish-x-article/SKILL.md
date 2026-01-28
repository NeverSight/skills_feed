---
name: publish-x-article
description: Publish Markdown articles to X (Twitter) Articles editor with proper formatting. Use when user wants to publish a Markdown file/URL to X Articles, or mentions "publish to X", "post article to Twitter", "X article", or wants help with X Premium article publishing. Handles cover image upload, converts Markdown to rich text, and automatically converts unsupported elements (tables, mermaid diagrams, deep headers) to images.
---

# Publish X Article

Publish Markdown content to X (Twitter) Articles editor, preserving formatting with rich text conversion. Automatically handles X Premium limitations by converting unsupported elements to images.

## Credits

This skill is inspired by and based on [wshuyi/x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill). Thank you to the original author for the foundational work.

## Interactive Setup: Ask Subscription Type

**IMPORTANT**: Before processing the article, ask the user about their X subscription type if not already known.

### Prompt the User

```
Before publishing, I need to know your X subscription type to handle formatting correctly:

1. **X Premium** - Basic tier ($8/month)
2. **X Premium+** - Plus tier ($16/month)

Which subscription do you have? (Premium / Premium+)
```

For Chinese users:
```
在发布之前，我需要了解您的 X 订阅类型以正确处理格式：

1. **X Premium** - 基础版 ($8/月)
2. **X Premium+** - 高级版 ($16/月)

您使用的是哪个版本？(Premium / Premium+)
```

### Remember the Answer

Once the user answers, remember their subscription type for the rest of the session. Don't ask again unless they explicitly want to change it.

## X Subscription Feature Comparison

| Feature | X Premium | X Premium+ |
|---------|-----------|------------|
| H1 headers (`#`) | Title only | Title only |
| H2 headers (`##`) | Yes | Yes |
| H3+ headers (`###`, etc.) | **No** | Yes |
| Markdown tables | **No** | Yes |
| Mermaid diagrams | **No** | **No** (not supported by X) |
| Code blocks | Blockquotes | Blockquotes |
| Bold, italic, links | Yes | Yes |
| Lists | Yes | Yes |
| Blockquotes | Yes | Yes |
| Images | Yes | Yes |

### Pre-Processing Required by Subscription

**X Premium (Basic):**
- Convert H3+ headers → H2 or bold
- Convert tables → PNG images
- Convert mermaid → PNG images

**X Premium+ (Plus):**
- Keep H3+ headers as-is
- Keep tables as-is (rendered natively)
- Convert mermaid → PNG images (still not supported)

## Prerequisites

- Playwright MCP for browser automation
- User logged into X with Premium subscription
- Python 3.9+ with dependencies:
  - macOS: `pip install Pillow pyobjc-framework-Cocoa markdown`
  - Windows: `pip install Pillow pywin32 clip-util markdown`
- For Mermaid diagrams: `npm install -g @mermaid-js/mermaid-cli`

## Scripts

Located in `~/.claude/skills/publish-x-article/scripts/`:

### parse_markdown.py
Parse Markdown and extract structured data:
```bash
python parse_markdown.py <markdown_file> [--output json|html] [--html-only]
```
Returns JSON with: title, cover_image, content_images (with block_index for positioning), html, total_blocks

### copy_to_clipboard.py
Copy image or HTML to system clipboard:
```bash
# Copy image (with optional compression)
python copy_to_clipboard.py image /path/to/image.jpg [--quality 80]

# Copy HTML for rich text paste
python copy_to_clipboard.py html --file /path/to/content.html
```

### table_to_image.py
Convert Markdown tables to PNG images:
```bash
python table_to_image.py /path/to/table.md /path/to/output.png [--style dark|light]
```

## Pre-Processing: Handle Unsupported Elements

**Before** publishing, scan the Markdown for unsupported elements and convert them to images.

### Step 0: Analyze Content for Limitations

```bash
# Check the markdown file for unsupported elements
cat /path/to/article.md
```

Look for:
1. **Deep headers (H3+)**: `###`, `####`, etc.
2. **Markdown tables**: Lines with `|` characters forming table structure
3. **Mermaid code blocks**: ` ```mermaid`

### Converting Unsupported Elements to Images

#### 1. Markdown Tables → PNG

When a table is detected:

```bash
# 1. Extract table to temp file
cat > /tmp/table.md << 'TABLE_EOF'
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
TABLE_EOF

# 2. Convert to image
python ~/.claude/skills/publish-x-article/scripts/table_to_image.py /tmp/table.md /tmp/table-001.png

# 3. Replace table in markdown with image reference
# ![Table description](/tmp/table-001.png)
```

#### 2. Mermaid Diagrams → PNG

When a mermaid block is detected:

```bash
# 1. Extract mermaid to temp file
cat > /tmp/diagram.mmd << 'MERMAID_EOF'
flowchart TD
    A[Start] --> B[Process]
    B --> C[End]
MERMAID_EOF

# 2. Convert to image using mermaid-cli
mmdc -i /tmp/diagram.mmd -o /tmp/diagram-001.png -b white -s 2

# 3. Replace mermaid block in markdown with image reference
# ![Diagram description](/tmp/diagram-001.png)
```

#### 3. Deep Headers (H3+) → Simplified Structure

**Goal:** Preserve the article's logical structure and readability while working within X Premium's H2-only limitation.

**Guidelines for the AI:**

When you encounter H3, H4, or deeper headers in a Premium user's article, think about what the author intended:

- **If the header introduces a distinct subtopic** under a section, convert it to **bold text** as a paragraph opener. This maintains visual hierarchy without breaking X's formatting.

- **If the header is a major section that happens to be H3**, consider promoting it to H2 — but only if this doesn't create a flat, meaningless structure. The article should still flow logically.

- **If there's a deep hierarchy** (H2 → H3 → H4), flatten thoughtfully:
  - Keep H2 as H2
  - Convert H3 to **bold paragraph**
  - Convert H4 to *italic* or just merge into the paragraph naturally

- **Preserve meaning over structure.** A header like `### Why This Matters` might become a bold lead-in: `**Why does this matter?**` followed by the content. Use your judgment.

- **Read the content.** If an H3 header is just "Example" or "Note", it might work better as a blockquote or inline emphasis rather than a standalone bold line.

The goal is not mechanical conversion — it's creating an article that reads well on X while honoring the author's intent.

### Pre-Processing Workflow

Before publishing, read through the article and prepare it for X:

1. **Understand the article's structure** — Read it first. What are the main sections? How does the author use headers to organize ideas?

2. **Handle tables and mermaid diagrams** — These need to become images. Extract each one, convert to PNG, and note where they should be inserted.

3. **Adapt headers for the subscription tier:**
   - For **Premium+ users**: Keep headers as-is (H3+ supported)
   - For **Premium users**: Thoughtfully restructure H3+ headers while preserving the article's flow and intent (see guidelines above)

4. **Create the modified markdown** — Save your adapted version to a temp file, ready for parsing.

The goal is an article that reads naturally on X, not a mechanically transformed document.

## Main Workflow

**Strategy: "先文后图后分割线" (Text First, Images Second, Dividers Last)**

For articles with images and dividers, paste ALL text content first, then insert images and dividers at correct positions using block index.

1. **Pre-process**: Convert tables/mermaid to images, flatten deep headers
2. Parse modified Markdown with Python script → get title, images, dividers (all with block_index), HTML
3. Navigate to X Articles editor
4. Upload cover image (first image)
5. Fill title
6. Copy HTML to clipboard (Python) → Paste with Cmd+V
7. Insert content images at positions specified by block_index
8. **Insert dividers at positions specified by block_index** (via Insert > Divider menu)
9. Save as draft (NEVER auto-publish)

## 高效执行原则 (Efficiency Guidelines)

**目标**: 最小化操作之间的等待时间，实现流畅的自动化体验。

### 1. 避免不必要的 browser_snapshot

大多数浏览器操作（click, type, press_key 等）都会在返回结果中包含页面状态。**不要**在每次操作后单独调用 `browser_snapshot`，直接使用操作返回的页面状态即可。

```
❌ 错误做法：
browser_click → browser_snapshot → 分析 → browser_click → browser_snapshot → ...

✅ 正确做法：
browser_click → 从返回结果中获取页面状态 → browser_click → ...
```

### 2. 避免不必要的 browser_wait_for

只在以下情况使用 `browser_wait_for`：
- 等待图片上传完成（`textGone="正在上传媒体"`）
- 等待页面初始加载（极少数情况）

**不要**使用 `browser_wait_for` 来等待按钮或输入框出现 - 它们在页面加载完成后立即可用。

### 3. 并行执行独立操作

当两个操作没有依赖关系时，可以在同一个消息中并行调用多个工具：

```
✅ 可以并行：
- 填写标题 (browser_type) + 复制HTML到剪贴板 (Bash)
- 解析Markdown生成JSON + 生成HTML文件

❌ 不能并行（有依赖）：
- 必须先点击create才能上传封面图
- 必须先粘贴内容才能插入图片
```

### 4. 连续执行浏览器操作

每个浏览器操作返回的页面状态包含所有需要的元素引用。直接使用这些引用进行下一步操作：

```
# 理想流程（每步直接执行，不额外等待）：
browser_navigate → 从返回状态找create按钮 → browser_click(create)
→ 从返回状态找上传按钮 → browser_click(上传) → browser_file_upload
→ 从返回状态找应用按钮 → browser_click(应用)
→ 从返回状态找标题框 → browser_type(标题)
→ 点击编辑器 → browser_press_key(Meta+v)
→ ...
```

### 5. 准备工作前置

在开始浏览器操作之前，先完成所有准备工作：
1. 扫描不支持的元素（表格、Mermaid、深层标题）
2. 转换表格/Mermaid 为图片
3. 解析 Markdown 获取 JSON 数据
4. 生成 HTML 文件到 /tmp/
5. 记录 title、cover_image、content_images 等信息

这样浏览器操作阶段可以连续执行，不需要中途停下来处理数据。

## Step 0: Read and Adapt the Article

**First, read the article.** Understand what it's about, how it's structured, and what the author is trying to communicate.

### Preserve the Original

**IMPORTANT:** Never modify the user's original file. If adaptations are needed:

1. Save the adapted version as a copy (e.g., `/tmp/article_adapted.md` or alongside the original as `article_for_x.md`)
2. Tell the user what was changed and where both files are:
   ```
   I've adapted your article for X Premium. Here's what changed:
   - Converted 2 tables to images
   - Restructured 3 H3 headers to bold text for better flow

   Original preserved: /path/to/article.md
   Adapted version: /path/to/article_for_x.md
   ```
3. Proceed with the adapted copy for publishing

This ensures the user can review the changes and keeps their original work intact.

### Adaptation Based on Subscription

### For Premium Users (Basic Tier)

Ask yourself:
- Are there tables? → Convert each to a PNG image
- Are there mermaid diagrams? → Convert each to a PNG image
- Are there H3+ headers? → Restructure them thoughtfully (see header guidelines above)

Create a modified version of the markdown that will work within Premium's limitations while preserving readability.

### For Premium+ Users

Ask yourself:
- Are there mermaid diagrams? → Convert to PNG (still not supported on any tier)
- Tables and H3+ headers can stay as-is

### Converting Elements to Images

```bash
# Tables → PNG
python ~/.claude/skills/publish-x-article/scripts/table_to_image.py /tmp/table-1.md /tmp/table-1.png

# Mermaid → PNG
mmdc -i /tmp/diagram-1.mmd -o /tmp/diagram-1.png -b white -s 2
```

Replace these elements in the markdown with image references, positioning them where the original element was.

## Step 1: Parse Markdown (Python)

Use `parse_markdown.py` to extract all structured data:

```bash
python ~/.claude/skills/publish-x-article/scripts/parse_markdown.py /path/to/modified_article.md
```

Output JSON:
```json
{
  "title": "Article Title",
  "cover_image": "/path/to/first-image.jpg",
  "content_images": [
    {"path": "/tmp/table-1.png", "block_index": 5, "after_text": "context..."},
    {"path": "/tmp/mermaid-1.png", "block_index": 12, "after_text": "another context..."}
  ],
  "dividers": [
    {"block_index": 7, "after_text": "context before divider..."},
    {"block_index": 15, "after_text": "another context..."}
  ],
  "html": "<p>Content...</p><h2>Section</h2>...",
  "total_blocks": 45
}
```

**Key fields:**
- `block_index`: The image/divider should be inserted AFTER block element at this index (0-indexed)
- `total_blocks`: Total number of block elements in the HTML
- `after_text`: Kept for reference/debugging only, NOT for positioning
- `dividers`: Array of divider positions (markdown `---` must be inserted via X's menu, not HTML `<hr>`)

Save HTML to temp file for clipboard:
```bash
python parse_markdown.py modified_article.md --html-only > /tmp/article_html.html
```

## Step 2: Open X Articles Editor

```
browser_navigate: https://x.com/compose/articles
```

**重要**: 页面加载后会显示草稿列表，不是编辑器。需要：

1. **等待页面加载完成**: 使用 `browser_snapshot` 检查页面状态
2. **立即点击 "create" 按钮**: 不要等待 "添加标题" 等编辑器元素，它们只有点击 create 后才出现
3. **等待编辑器加载**: 点击 create 后，等待编辑器元素出现

```
# 1. 导航到页面
browser_navigate: https://x.com/compose/articles

# 2. 获取页面快照，找到 create 按钮
browser_snapshot

# 3. 点击 create 按钮（通常 ref 类似 "create" 或带有 create 标签）
browser_click: element="create button", ref=<create_button_ref>

# 4. 现在编辑器应该打开了，可以继续上传封面图等操作
```

**注意**: 不要使用 `browser_wait_for text="添加标题"` 来等待页面加载，因为这个文本只有在点击 create 后才出现，会导致超时。

If login needed, prompt user to log in manually.

## Step 3: Upload Cover Image

1. Click "添加照片或视频" button
2. Use browser_file_upload with the cover image path (from JSON output)
3. Verify image uploaded

## Step 4: Fill Title

- Find textbox with "添加标题" placeholder
- Use browser_type to input title (from JSON output)

## Step 5: Paste Text Content (Python Clipboard)

Copy HTML to system clipboard using Python, then paste:

```bash
# Copy HTML to clipboard
python ~/.claude/skills/publish-x-article/scripts/copy_to_clipboard.py html --file /tmp/article_html.html
```

Then in browser:
```
browser_click on editor textbox
browser_press_key: Meta+v
```

This preserves all rich text formatting (H2, bold, links, lists).

## Step 6: Insert Content Images (Block Index Positioning)

**关键改进**: 使用 `block_index` 精确定位，而非依赖文字匹配。

### 定位原理

粘贴 HTML 后，编辑器中的内容结构为一系列块元素（段落、标题、引用等）。每张图片的 `block_index` 表示它应该插入在第 N 个块元素之后。

### 操作步骤

1. **获取所有块元素**: 使用 browser_snapshot 获取编辑器内容，找到 textbox 下的所有子元素
2. **按索引定位**: 根据 `block_index` 点击对应的块元素
3. **粘贴图片**: 复制图片到剪贴板后粘贴

For each content image (from `content_images` array):

```bash
# 1. Copy image to clipboard (with compression)
python ~/.claude/skills/publish-x-article/scripts/copy_to_clipboard.py image /path/to/img.jpg --quality 85
```

```
# 2. Click the block element at block_index
# Example: if block_index=5, click the 6th block element (0-indexed)
browser_click on the element at position block_index in the editor

# 3. Paste image
browser_press_key: Meta+v

# 4. Wait for upload (use short time, returns immediately when done)
browser_wait_for textGone="正在上传媒体" time=2
```

### 反向插入

**注意**: 每插入一张图片后，后续图片的实际位置会偏移。建议按 `block_index` **从大到小**的顺序插入图片。

如果有3张图片，block_index 分别为 5, 12, 27：
1. 先插入 block_index=27 的图片
2. 再插入 block_index=12 的图片
3. 最后插入 block_index=5 的图片

## Step 6.5: Insert Dividers (Via Menu)

**重要**: Markdown 中的 `---` 分割线不能通过 HTML `<hr>` 标签粘贴（X Articles 会忽略它）。必须通过 X Articles 的 Insert 菜单插入。

### 为什么需要特殊处理

X Articles 有自己的原生分割线元素，只能通过 Insert > Divider 菜单插入。HTML `<hr>` 标签会被完全忽略。

### 操作步骤

For each divider (from `dividers` array), in **reverse order of block_index**:

```
# 1. Click the block element at block_index position
browser_click on the element at position block_index in the editor

# 2. Open Insert menu
browser_click on "Insert" button (Add Media button)

# 3. Click Divider menu item
browser_click on "Divider" menuitem

# Divider is inserted at cursor position
```

### 反向插入

和图片一样，按 `block_index` **从大到小**的顺序插入分割线，避免位置偏移问题。

### 与图片的插入顺序

建议先插入所有图片，再插入所有分割线。两者都按 block_index 从大到小的顺序：

1. 插入所有图片（从最大 block_index 开始）
2. 插入所有分割线（从最大 block_index 开始）

## Step 7: Save Draft

1. Verify content pasted (check word count indicator)
2. Draft auto-saves, or click Save button if needed
3. Click "预览" to verify formatting
4. Report: "Draft saved. Review and publish manually."

## Critical Rules

1. **NEVER publish** - Only save draft
2. **Pre-process first** - Convert tables/mermaid/deep headers before parsing
3. **First image = cover** - Upload first image as cover image
4. **Rich text conversion** - Always convert Markdown to HTML before pasting
5. **Use clipboard API** - Paste via clipboard for proper formatting
6. **Block index positioning** - Use block_index for precise image/divider placement
7. **Reverse order insertion** - Insert images and dividers from highest to lowest block_index
8. **H1 title handling** - H1 is used as title only, not included in body
9. **Dividers via menu** - Markdown `---` must be inserted via Insert > Divider menu (HTML `<hr>` is ignored)

## Supported Formatting (After Pre-Processing)

| Element | Support | Notes |
|---------|---------|-------|
| H2 (`##`) | Native | Section headers |
| Bold (`**`) | Native | Strong emphasis |
| Italic (`*`) | Native | Emphasis |
| Links (`[](url)`) | Native | Hyperlinks |
| Ordered lists | Native | 1. 2. 3. |
| Unordered lists | Native | - bullets |
| Blockquotes (`>`) | Native | Quoted text |
| Code blocks | Converted | → Blockquotes |
| Tables | Converted | → PNG images |
| Mermaid | Converted | → PNG images |
| H3+ headers | Converted | → H2 or bold |
| Dividers (`---`) | Menu insert | → Insert > Divider |

## Example Flow

User: "Publish /path/to/article.md to X"

```bash
# Step 0: Analyze content
# Found: 1 table, 1 mermaid diagram, 2 H3 headers

# Step 0.1: Convert table to image
python ~/.claude/skills/publish-x-article/scripts/table_to_image.py /tmp/table-1.md /tmp/table-1.png

# Step 0.2: Convert mermaid to image
mmdc -i /tmp/mermaid-1.mmd -o /tmp/mermaid-1.png -b white -s 2

# Step 0.3: Create modified markdown with image refs and flattened headers
# Save to /tmp/article_modified.md

# Step 1: Parse modified markdown
python ~/.claude/skills/publish-x-article/scripts/parse_markdown.py /tmp/article_modified.md > /tmp/article.json
python ~/.claude/skills/publish-x-article/scripts/parse_markdown.py /tmp/article_modified.md --html-only > /tmp/article_html.html
```

2. Navigate to https://x.com/compose/articles
3. Click create, upload cover image (browser_file_upload for cover only)
4. Fill title (from JSON: `title`)
5. Copy & paste HTML:
   ```bash
   python ~/.claude/skills/publish-x-article/scripts/copy_to_clipboard.py html --file /tmp/article_html.html
   ```
   Then: browser_press_key Meta+v
6. For each content image (including converted table/mermaid PNGs), **in reverse order of block_index**:
   ```bash
   python copy_to_clipboard.py image /path/to/img.jpg --quality 85
   ```
   - Click block element at `block_index` position
   - browser_press_key Meta+v
   - Wait until upload complete
7. Verify in preview
8. "Draft saved. Please review and publish manually."

## Best Practices

### 为什么用 block_index 而非文字匹配？

1. **精确定位**: 不依赖文字内容，即使多处文字相似也能正确定位
2. **可靠性**: 索引是确定性的，不会因为文字相似而混淆
3. **调试方便**: `after_text` 仍保留用于人工核验

### 为什么用 Python 而非浏览器内 JavaScript？

1. **本地处理更可靠**: Python 直接操作系统剪贴板，不受浏览器沙盒限制
2. **图片压缩**: 上传前压缩图片 (--quality 85)，减少上传时间
3. **代码复用**: 脚本固定不变，无需每次重新编写转换逻辑
4. **调试方便**: 脚本可单独测试，问题易定位

### 等待策略

**关键理解**: `browser_wait_for` 的 `textGone` 参数会在文字消失时**立即返回**，`time` 只是最大等待时间，不是固定等待时间。

```
# 正确用法：短 time 值，条件满足立即返回
browser_wait_for textGone="正在上传媒体" time=2

# 错误用法：固定长时间等待
browser_wait_for time=5  # 无条件等待5秒，浪费时间
```

### 封面图 vs 内容图

- **封面图**: 使用 browser_file_upload（因为有专门的上传按钮）
- **内容图**: 使用 Python 剪贴板 + 粘贴（更高效）

## Troubleshooting

### Table not rendering correctly
- Ensure Pillow is installed: `pip install pillow`
- Check table markdown syntax is valid

### Mermaid conversion fails
- Install mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`
- Check mermaid syntax is valid

### Deep headers still showing
- Manually flatten `###` → `##` or `**bold**`
- Re-run pre-processing

### Image upload timeout
- Compress images with `--quality 70`
- Use shorter `browser_wait_for time=2`
