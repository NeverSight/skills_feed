---
name: wechat-article
description: "Convert Markdown articles to WeChat Official Account compatible HTML format. Use when users need to convert Markdown files to WeChat articles, apply themed styling for WeChat formatting, generate inline CSS HTML compatible with WeChat editor, process technical articles with code blocks and tables for WeChat, or apply professional WeChat-style layouts with headers and footers."
user-invocable: false
---

# WeChat Article Converter

## Overview

Convert Markdown articles to WeChat Official Account (微信公众号) compatible HTML format with themed styling and inline CSS. This skill handles the entire conversion process automatically using the `md_to_wechat.py` script.

**Core capability:** Transform standard Markdown → WeChat-compatible HTML with professional styling.

## Workflow

### Step 1: Identify User Request

Trigger this skill when user asks for:
- Converting Markdown to WeChat format
- "转换为微信公众号格式"
- "生成微信文章"
- "公众号排版"
- Applying WeChat styling to articles

### Step 2: Gather Required Information

**Required:**
- Input Markdown file path (from user request or current directory)

**ALWAYS Ask User for Theme Selection:**
Use `AskUserQuestion` tool to present theme options to the user interactively.

Present these 3 theme options:

| Option | Theme Name | Best For |
|--------|-----------|----------|
| default | 专业蓝色 | 技术文章、教程、通用内容 |
| orange | 活力橙 | 运动、美食、娱乐、促销活动 |
| grid | 格子主题 | 带序号徽章、动画效果，支持清新绿/大气蓝配色 |

**Exception:** Skip theme selection if user explicitly specifies theme in request.

**Important:** If user selects "grid" theme, ask for color preference:
-清新绿 (green) - #52c41a，适合生活方式、健康、环保
- 大气蓝 (blue) - #007AFF，适合科技、商务、专业内容

**Additional Options (ask if needed):**
- Article title for WeChat header (default: none)
- Include WeChat header/footer (default: yes)

### Step 3: Execute Conversion

**Important:** Always use the absolute path to the skill script:
```bash
python3 ~/.claude/skills/wechat-article/scripts/md_to_wechat.py <input.md> [output.html] [options]
```

**ALWAYS use --preview flag to open browser with copy button:**

1. **Basic conversion with browser preview (RECOMMENDED):**
   ```bash
   python3 ~/.claude/skills/wechat-article/scripts/md_to_wechat.py input.md --theme <selected-theme> --preview
   ```

2. **With title and browser preview:**
   ```bash
   python3 ~/.claude/skills/wechat-article/scripts/md_to_wechat.py input.md --theme <theme> --title "<article-title>" --preview
   ```

3. **Content only (no WeChat elements) with preview:**
   ```bash
   python3 ~/.claude/skills/wechat-article/scripts/md_to_wechat.py input.md --theme <theme> --no-header-footer --preview
   ```

**Note:** The --preview flag will automatically open a browser page with:
- Article preview
- "复制 HTML 代码" button to copy the HTML
- Instructions for pasting into WeChat editor
- Visual preview of the styled article

### Step 4: Present Results to User

**Always:**
1. Confirm conversion completed successfully
2. Show which theme was used
3. Show output file location
4. Display a preview of the generated HTML (first ~30 lines)
5. Remind user they can copy-paste the HTML into WeChat editor

## Example Interactions

**Example 1: Standard workflow with theme selection and browser preview**
```
User: "把 article.md 转成微信公众号格式"

Claude: [Uses AskUserQuestion]
"请选择文章主题风格：
• default - 专业蓝色（技术文章、教程、通用内容）
• orange - 活力橙（运动、美食、娱乐、促销活动）
• grid - 格子主题（带序号徽章、动画效果，支持清新绿/大气蓝配色）"

User: [Selects] "grid"

Claude: [Uses AskUserQuestion]
"请选择格子主题配色：
• green - 清新绿 (#52c41a) - 生活方式、健康、环保
• blue - 大气蓝 (#007AFF) - 科技、商务、专业内容"

User: [Selects] "blue"

Claude: [Executes] python3 ~/.claude/skills/wechat-article/scripts/md_to_wechat.py article.md --theme grid --grid-color blue --preview
Claude: ✅ 使用格子主题（大气蓝）转换成功！浏览器已打开预览页面，点击"复制 HTML 代码"按钮即可复制到微信公众号编辑器。
```

**Example 2: User specifies theme directly**
```
User: "转换成微信公众号文章，用默认主题"

Claude: [Skips theme selection, user already specified]
Claude: [Executes] python3 ~/.claude/skills/wechat-article/scripts/md_to_wechat.py article.md --theme default --preview
Claude: ✅ 使用专业蓝色主题转换成功！浏览器已打开预览页面。
```

## Implementation Notes

### Available Themes

The skill currently includes 3 themes:

1. **default (专业蓝色)** - Professional blue theme
   - Primary color: #1e6bb8
   - Best for: Technical articles, tutorials, general content

2. **orange (活力橙)** - Vibrant orange theme
   - Primary color: #e67e22
   - Best for: Sports, food, entertainment, promotions

3. **grid (格子主题)** - Grid theme with number badges and animations
   - Default color: #52c41a (fresh green)
   - Alternative color: #007AFF (atmospheric blue)
   - Features: Numbered heading badges, rotation animations, auto list nesting
   - Best for: All content types, choose color based on topic
     - Green: Lifestyle, health, environmental topics
     - Blue: Technology, business, professional content

### Dependencies

The script requires:
- `markdown>=3.5.0` - Markdown parsing
- `beautifulsoup4>=4.12.0` - HTML processing
- `pygments>=2.16.0` - Code syntax highlighting

**Check if dependencies are installed before running. If not, install:**
```bash
pip3 install markdown beautifulsoup4 pygments
```

### Troubleshooting

**Issue:** Dependencies not found
**Solution:** Install with `pip3 install markdown beautifulsoup4 pygments`

**Issue:** Script not found
**Solution:** Use absolute path: `~/.claude/skills/wechat-article/scripts/md_to_wechat.py`

**Issue:** WeChat styles not appearing
**Solution:** Ensure user copies the entire HTML content including inline styles

## Resources

### scripts/md_to_wechat.py
Main conversion script. Execute with appropriate arguments based on user request.

### references/themes.md
Detailed theme specifications. Consult when helping user understand theme differences.

### assets/examples/sample.md
Example article demonstrating all supported features. Use for testing or showing user capabilities.
