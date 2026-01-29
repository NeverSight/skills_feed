---
name: annas-to-notebooklm
description: 自动从 Anna's Archive 下载书籍并上传到 Google NotebookLM。支持 PDF/EPUB 格式，自动转换，一键创建知识库。
author: Adapted from zstmfhy/zlibrary-to-notebooklm
version: 1.0.0
---

# Anna's Archive to NotebookLM Skill

让 Claude 帮你自动下载书籍并上传到 NotebookLM，实现"零幻觉"的 AI 对话式阅读。

## 🎯 核心功能

- 一键下载书籍（从 Anna's Archive）
- 自动识别下载链接（在 `span.bg-gray-200` 标签中）
- 自动创建 NotebookLM 笔记本
- 上传文件并返回笔记本 ID
- 支持与 AI 进行基于书籍内容的对话

## 📋 激活条件

当用户提到以下需求时，使用此 Skill：

- 用户提供 Anna's Archive 书籍链接（包含 `annas-archive.pm`、`annas.archive` 等域名）
- 用户说"帮我把这本书上传到 NotebookLM"（并提供 Anna's 链接）
- 用户说"自动下载并读这本书"（并提供 Anna's 链接）
- 用户说"用 Anna's Archive 链接创建 NotebookLM 知识库"
- 用户要求从特定 URL 下载书籍并分析（且 URL 来自 Anna's Archive）

## 🔧 核心指令

当用户提供 Anna's Archive 链接时，按以下流程执行：

### Step 1: 提取信息

从用户提供的 URL 中提取：
- 完整 URL（通常是 `https://annas-archive.pm/slow_download/...` 格式）
- 书名（从 URL 或页面中推断）

### Step 2: 检查环境

检查必需的依赖和配置：

```bash
# 检查 Playwright
python3 -c "import playwright" 2>/dev/null || pip install playwright

# 检查 NotebookLM CLI
which notebooklm || echo "请安装 NotebookLM CLI"

# 检查登录状态（可选）
ls ~/.annas/storage_state.json 2>/dev/null || echo "建议先登录"
```

### Step 3: 自动下载

使用脚本访问 Anna's Archive 并下载：

```bash
cd /path/to/annas-to-notebooklm
python3 scripts/upload.py "<Anna's Archive URL>"
```

**下载逻辑：**

1. **访问下载页面**
2. **查找下载链接**：在 `span.bg-gray-200` 标签中查找包含下载 URL 的文本
3. **导航到下载地址**：直接访问下载链接
4. **保存文件**：下载到 `~/Downloads` 目录

**关键代码：**
```python
# 查找 span.bg-gray-200 元素
spans = await page.query_selector_all('span.bg-gray-200')

for span in spans:
    span_text = await span.inner_text()
    # span 的文本内容就是下载链接
    if span_text.strip().startswith('http'):
        download_url = span_text.strip()
        # 直接导航下载
        await page.goto(download_url)
```

### Step 4: 格式处理

脚本会自动处理：

1. **PDF**：直接使用（保留排版）
2. **EPUB**：转换为 Markdown（使用 `convert_epub.py`）
3. **大文件**：自动分块（>350k 词）

### Step 5: 创建并上传到 NotebookLM

脚本会自动：

```bash
# 创建笔记本
notebooklm create "书名" --json

# 上传文件
notebooklm source add "文件路径" --json
```

### Step 6: 返回结果

向用户返回：

```
✅ 下载成功！
📚 书名: [书名]
🆔 笔记本 ID: [notebook-id]
📄 来源 ID: [source-id]

现在你可以问我：
- "这本书的核心观点是什么？"
- "总结第3章的内容"
- "作者有哪些独特的见解？"
```

### Step 7: 错误处理

如果遇到错误：

1. **未找到登录会话**
   - 提示：运行 `python3 scripts/login.py`
   - 或：某些页面不需要登录，直接尝试即可

2. **未找到下载链接**
   - 检查 URL 格式是否正确
   - 确认页面是否完全加载
   - 查看 Anna's Archive 页面结构是否变化

3. **下载失败**
   - 检查网络连接
   - 尝试重新运行

4. **NotebookLM 上传失败**
   - 检查文件大小（限制 200MB）
   - 检查文件格式

## 📝 使用示例

### 示例 1：基本下载

**用户：**
```
帮我把这本书上传到 NotebookLM：
https://annas-archive.pm/slow_download/3cd1081b5bc0a229bb794f0d96f04e22/0/5
```

**Claude：**
```bash
cd /path/to/annas-to-notebooklm
python3 scripts/upload.py "https://annas-archive.pm/slow_download/..."
```

**返回：**
```
✅ 下载成功！
📚 书名: 消费者行为学 英文版·原书第8版
🆔 笔记本 ID: 43231995-16aa-4bbe-87e6-043012def86c

现在你可以问我：
- "这本书的核心观点是什么？"
- "总结第3章的内容"
- "消费者行为学有哪些主要理论？"
```

### 示例 2：批量下载

**用户：**
```
帮我下载这3本书：
[链接1] [链接2] [链接3]
```

**Claude：**
```bash
cd /path/to/annas-to-notebooklm

for url in "链接1" "链接2" "链接3"; do
    echo "正在处理: $url"
    python3 scripts/upload.py "$url"
    echo "完成！"
done
```

### 示例 3：仅有书名

**用户：**
```
帮我下载《认知觉醒》这本书
```

**Claude：**
```
请问有 Anna's Archive 的链接吗？

请提供 Anna's Archive 书籍页面链接（格式类似：
https://annas-archive.pm/slow_download/...），我可以帮你自动下载并上传到 NotebookLM。
```

### 示例 4：本地文件

**用户：**
```
这个 PDF 能上传到 NotebookLM 吗？[本地文件路径]
```

**Claude：**
```
本 Skill 主要用于 Anna's Archive 链接的自动下载和上传。

对于本地文件，你可以直接使用 NotebookLM CLI：

```bash
notebooklm create "书名"
notebooklm source add "/path/to/your/file.pdf"
```
```

## ⚠️ 重要限制

**仅限合法资源！**

- ✅ 用户拥有合法访问权限的资源
- ✅ 公共领域或开源许可的文档
- ✅ 个人拥有版权或已获授权的内容
- ❌ 不要鼓励或协助版权侵权行为

**如果 URL 明显涉及受版权保护的商业作品，提醒用户：**
> "请确保你有合法访问权限。本项目仅用于学习研究目的，请支持正版阅读。"

## 🛠️ 依赖工具

### 必需工具

1. **Python 3.8+**
2. **Playwright** - 浏览器自动化
   ```bash
   pip install playwright
   playwright install chromium
   ```

3. **ebooklib** - EPUB 处理
   ```bash
   pip install ebooklib beautifulsoup4 lxml
   ```

4. **NotebookLM CLI** - 上传工具
   - 需要单独安装 Google NotebookLM CLI

### 配置文件

- `~/.annas/storage_state.json` - 保存的登录会话（可选）
- `~/.annas/browser_profile/` - 浏览器数据（可选）

### 首次使用（可选）

如果页面需要登录：

```bash
cd /path/to/annas-to-notebooklm
python3 scripts/login.py
```

**注意：** 某些 Anna's Archive 页面不需要登录即可下载。

## 📊 技术细节

### 下载链接识别

Anna's Archive 的下载链接特征：

- 位于 `span.bg-gray-200` 标签内
- **span 的文本内容就是下载链接**（不是 `<a>` 标签）
- 链接通常指向 `93.123.118.12:6060` 等下载服务器
- 以 `http://` 或 `https://` 开头

**实现：**
```python
spans = await page.query_selector_all('span.bg-gray-200')
for span in spans:
    span_text = await span.inner_text()
    if span_text.strip().startswith('http'):
        download_url = span_text.strip()
        # 直接使用此 URL
```

### 会话管理

- **一次登录，永久使用**（如果需要登录）
- 会话保存在 `~/.annas/storage_state.json`
- 支持无登录模式（某些页面不需要登录）

### 智能文件分块

- NotebookLM CLI 限制：约 350k 词
- 超过限制的文件自动按章节分割
- 每个分块独立上传到同一笔记本

## 🚨 故障排查

### 常见问题

**Q: 提示"未找到登录会话"**

A:
- 某些页面不需要登录，可以忽略此提示
- 如果确实需要登录：运行 `python3 scripts/login.py`

**Q: 未找到下载链接**

A:
- 确认 URL 格式正确（应该是 `annas-archive.pm/slow_download/...`）
- 检查网络连接
- 查看 Anna's Archive 页面结构是否变化

**Q: 下载失败，超时**

A:
- 可能是网络问题
- 下载服务器可能繁忙，建议重试

**Q: NotebookLM 上传失败**

A:
- 检查文件大小（限制 200MB）
- 检查文件格式（支持 PDF、EPUB、Markdown 等）
- 确认 NotebookLM CLI 已正确安装

## 📚 相关资源

- [NotebookLM 官方文档](https://notebooklm.google.com/)
- [Anna's Archive 网站](https://annas-archive.pm/)
- [Playwright 文档](https://playwright.dev/)
- [原始项目](https://github.com/zstmfhy/zlibrary-to-notebooklm)

## 🎓 学习资源

如果你想了解更多：

- **如何高效使用 NotebookLM**：询问"NotebookLM 有哪些使用技巧？"
- **如何创建个人知识库**：询问"如何用 NotebookLM 构建知识管理系统？"
- **AI 对话式阅读**：询问"怎样让 AI 帮我深度阅读一本书？"

---

**Skill Version:** 1.0.0
**Last Updated:** 2025-01-17
**Author:** Adapted from zstmfhy/zlibrary-to-notebooklm
**License:** MIT
