---
name: post-to-x
description: 发布内容和文章到 X (Twitter)。支持带图片的普通推文和 X Articles（长文）。使用真实的 Chrome 和 CDP 来绕过自动化检测。
---

# 发布到 X (Twitter)

使用真实的 Chrome 浏览器发布内容、图片和长篇文章到 X（绕过反机器人检测）。

## 功能

- **普通推文**: 文本 + 最多 4 张图片
- **X Articles**: 发布带有丰富格式和图片的 Markdown 文件（需要 X Premium）

## 用法

```bash
# 仅发布文本
/post-to-x "Your post content here"

# 发布带图片的推文
/post-to-x "Your post content" --image /path/to/image.png

# 发布带多张图片的推文 (最多 4 张)
/post-to-x "Your post content" --image img1.png --image img2.png

# 实际提交发布
/post-to-x "Your post content" --submit
```

## 先决条件

- 已安装 Google Chrome 或 Chromium
- 已安装 `bun` (用于运行脚本)
- 首次运行：在打开的浏览器窗口中登录 X

## 快速开始 (推荐)

直接使用 `x-browser.ts` 脚本：

```bash
# 预览模式 (不发布)
npx -y bun ./scripts/x-browser.ts "Hello from Claude!" --image ./screenshot.png

# 实际发布
npx -y bun ./scripts/x-browser.ts "Hello!" --image ./photo.png --submit
```

脚本流程：
1. 启动禁用了反检测功能的真实 Chrome
2. 使用持久化配置文件（只需登录一次）
3. 通过 CDP 输入文本并粘贴图片
4. 等待 30 秒进行预览（或使用 `--submit` 立即发布）

## 手动工作流

如果您更喜欢通过分步控制：

### 步骤 1: 复制图片到剪贴板

```bash
npx -y bun ./scripts/copy-to-clipboard.ts image /path/to/image.png
```

### 步骤 2: 使用 Playwright MCP (如果 Chrome 会话可用)

```bash
# 导航
mcp__playwright__browser_navigate url="https://x.com/compose/post"

# 获取元素引用
mcp__playwright__browser_snapshot

# 输入文本
mcp__playwright__browser_click element="editor" ref="<ref>"
mcp__playwright__browser_type element="editor" ref="<ref>" text="Your content"

# 粘贴图片 (复制到剪贴板后)
mcp__playwright__browser_press_key key="Meta+v"  # macOS
# 或
mcp__playwright__browser_press_key key="Control+v"  # Windows/Linux

# 截图以验证
mcp__playwright__browser_take_screenshot filename="preview.png"
```

## 参数

| 参数 | 描述 |
|-----------|-------------|
| `<text>` | 发布内容 (位置参数) |
| `--image <path>` | 图片文件路径 (可重复，最多 4 张) |
| `--submit` | 实际发布 (默认: 仅预览) |
| `--profile <dir>` | 自定义 Chrome 配置文件目录 |

## 图片支持

- 格式: PNG, JPEG, GIF, WebP
- 每条推文最多 4 张图片
- 图片被复制到系统剪贴板，然后通过快捷键粘贴

## 示例会话

```
User: /post-to-x "Hello from Claude!" --image ./screenshot.png

Claude:
1. Runs: npx -y bun ./scripts/x-browser.ts "Hello from Claude!" --image ./screenshot.png
2. Chrome opens with X compose page
3. Text is typed into editor
4. Image is copied to clipboard and pasted
5. Browser stays open 30s for preview
6. Reports: "Post composed. Use --submit to post."
```

## 故障排除

- **Chrome not found**: 设置 `X_BROWSER_CHROME_PATH` 环境变量
- **Not logged in**: 首次运行会打开 Chrome - 手动登录，Cookies 会被保存
- **Image paste fails**: 验证剪贴板脚本: `npx -y bun ./scripts/copy-to-clipboard.ts image <path>`
- **Rate limited**: 等待几分钟后重试

## 工作原理

`x-browser.ts` 脚本使用 Chrome DevTools Protocol (CDP) 来：
1. 启动真实的 Chrome (非 Playwright)，带参数 `--disable-blink-features=AutomationControlled`
2. 使用持久化配置文件目录来保存登录会话
3. 通过 CDP 命令与 X 交互 (Runtime.evaluate, Input.dispatchKeyEvent)
4. 从系统剪贴板粘贴图片

这种方法绕过了 X 阻止 Playwright/Puppeteer 的反自动化检测。

## 注意事项

- 首次运行需要手动登录 (会话会被保存)
- 使用 `--submit` 前请务必预览
- 操作完成后浏览器会自动关闭
- 支持 macOS, Linux, 和 Windows

---

# X Articles (长文发布)

发布 Markdown 文章到 X Articles 编辑器，支持富文本格式和图片。

## X Article 用法

```bash
# 发布 Markdown 文章 (预览模式)
/post-to-x article /path/to/article.md

# 带自定义封面图片
/post-to-x article article.md --cover ./hero.png

# 带自定义标题
/post-to-x article article.md --title "My Custom Title"

# 实际发布 (不仅仅是草稿)
/post-to-x article article.md --submit
```

## Articles 先决条件

- X Premium 订阅 (Articles 功能必需)
- 已安装 Google Chrome
- 已安装 `bun`

## Article 脚本

直接使用 `x-article.ts`:

```bash
npx -y bun ./scripts/x-article.ts article.md
npx -y bun ./scripts/x-article.ts article.md --cover ./cover.jpg
npx -y bun ./scripts/x-article.ts article.md --submit
```

## Markdown 格式

```markdown
---
title: My Article Title
cover_image: /path/to/cover.jpg
---

# Title (becomes article title)

Regular paragraph text with **bold** and *italic*.

## Section Header

More content here.

![Image alt text](./image.png)

- List item 1
- List item 2

1. Numbered item
2. Another item

> Blockquote text

[Link text](https://example.com)

\`\`\`
Code blocks become blockquotes (X doesn't support code)
\`\`\`
```

## Frontmatter 字段

| 字段 | 描述 |
|-------|-------------|
| `title` | 文章标题 (或使用第一个 H1) |
| `cover_image` | 封面图片路径或 URL |
| `cover` | cover_image 的别名 |
| `image` | cover_image 的别名 |

## 图片处理

1. **封面图片**: 第一张图片或 Frontmatter 中的 `cover_image`
2. **远程图片**: 自动下载到临时目录
3. **占位符**: 内容中的图片使用 `[[IMAGE_PLACEHOLDER_N]]` 格式
4. **插入**: 找到占位符，选中，并将其替换为实际图片

## Markdown 转 HTML 脚本

转换 Markdown 并检查结构：

```bash
# 获取包含所有元数据的 JSON
npx -y bun ./scripts/md-to-html.ts article.md

# 仅输出 HTML
npx -y bun ./scripts/md-to-html.ts article.md --html-only

# 保存 HTML 到文件
npx -y bun ./scripts/md-to-html.ts article.md --save-html /tmp/article.html
```

JSON 输出:
```json
{
  "title": "Article Title",
  "coverImage": "/path/to/cover.jpg",
  "contentImages": [
    {
      "placeholder": "[[IMAGE_PLACEHOLDER_1]]",
      "localPath": "/tmp/x-article-images/img.png",
      "blockIndex": 5
    }
  ],
  "html": "<p>Content...</p>",
  "totalBlocks": 20
}
```

## 支持的格式

| Markdown | HTML 输出 |
|----------|-------------|
| `# H1` | 仅标题 (不在正文中) |
| `## H2` - `###### H6` | `<h2>` |
| `**bold**` | `<strong>` |
| `*italic*` | `<em>` |
| `[text](url)` | `<a href>` |
| `> quote` | `<a>` |
| `` `code` `` | `<code>` |
| ```` ``` ```` | `<blockquote>` (X 限制) |
| `- item` | `<ul><li>` |
| `1. item` | `<ol><li>` |
| `![](img)` | Image placeholder |

## Article 工作流

1. **解析 Markdown**: 提取标题、封面、内容图片，生成 HTML
2. **启动 Chrome**: 带有 CDP 的真实浏览器，持久化登录
3. **导航**: 打开 `x.com/compose/articles`
4. **创建文章**: 如果在列表页，点击创建按钮
5. **上传封面**: 使用文件输入上传封面图片
6. **填写标题**: 将标题输入到标题字段
7. **粘贴内容**: 将 HTML 复制到剪贴板，粘贴到编辑器
8. **插入图片**: 对于每个占位符 (倒序):
   - 在编辑器中找到占位符文本
   - 选中占位符
   - 将图片复制到剪贴板
   - 粘贴以替换选中内容
9. **预览**: 浏览器保持打开 60 秒以供预览
10. **发布**: 仅在使用 `--submit` 标志时发布

## Article 示例会话

```
User: /post-to-x article ./blog/my-post.md --cover ./thumbnail.png

Claude:
1. Parses markdown: title="My Post", 3 content images
2. Launches Chrome with CDP
3. Navigates to x.com/compose/articles
4. Clicks create button
5. Uploads thumbnail.png as cover
6. Fills title "My Post"
7. Pastes HTML content
8. Inserts 3 images at placeholder positions
9. Reports: "Article composed. Review and use --submit to publish."
```

## Article 故障排除

- **No create button**: 确保 X Premium 订阅处于活动状态
- **Cover upload fails**: 检查文件路径和格式 (PNG, JPEG)
- **Images not inserting**: 验证粘贴的内容中是否存在占位符
- **Content not pasting**: 检查 HTML 剪贴板: `npx -y bun ./scripts/copy-to-clipboard.ts html --file /tmp/test.html`

## Article 发布工作原理

1. `md-to-html.ts` 将 Markdown 转换为 HTML:
   - 提取 Frontmatter (标题, 封面)
   - 将 Markdown 转换为 HTML
   - 用唯一的占位符替换图片
   - 将远程图片下载到本地
   - 返回结构化 JSON

2. `x-article.ts` 通过 CDP 发布:
   - 启动真实 Chrome (绕过检测)
   - 使用持久化配置文件 (已保存的登录)
   - 通过 DOM 操作导航和填充编辑器
   - 从系统剪贴板粘贴 HTML
   - 查找/选择/替换每个图片占位符

## 脚本参考

| 脚本 | 用途 |
|--------|---------|
| `x-browser.ts` | 普通推文 (文本 + 图片) |
| `x-article.ts` | Article 发布 (Markdown) |
| `md-to-html.ts` | Markdown → HTML 转换 |
| `copy-to-clipboard.ts` | 复制图片/HTML 到剪贴板 |
