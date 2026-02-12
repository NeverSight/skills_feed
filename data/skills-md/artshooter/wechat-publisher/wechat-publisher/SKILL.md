---
name: wechat-publisher
version: 1.0.0
description: |
  将 Markdown 文章智能排版并发布到微信公众号草稿箱。
  AI 生成创意 HTML，上传图片，发布到草稿箱。

  触发场景：用户说"发布到微信"、"推送到公众号"、"微信文章发布"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
allowed-edit-paths:
  - /tmp
allowed-bash-commands:
  - python3 ~/.claude/skills/wechat-publisher/scripts/image_uploader.py
  - python3 ~/.claude/skills/wechat-publisher/scripts/publisher.py
  - python3 (inline scripts)
  - ls, cd, pwd, rm
  - grep
---

# WeChat Publisher Skill

将 Markdown 文章智能排版并发布到微信公众号草稿箱。

**核心特性**:
- AI 生成创意 HTML（非模板化）
- 自动上传图片
- 自动使用默认封面（如果没有图片）
- 零人工干预

---

## 工作流程

### Step 1: 读取 Markdown

```bash
# 文章通常在桌面
ls ~/Desktop/*.md
```

使用 Read tool 读取文章内容。

---

### Step 1.5: 提取标题并分离正文

读取 Markdown 后，需要分离标题和正文：

1. **提取标题**: 文章标题通常是第一行的 `# 标题` 或文件名
2. **分离正文**: 从 Markdown 内容中移除标题行，只保留正文部分
3. **保存标题**: 将标题保存为变量，用于后续 API 调用

**示例**:
```python
# 假设 markdown_content 是读取的原始内容
lines = markdown_content.strip().split('\n')

# 提取标题（第一行如果是 # 开头）
if lines[0].startswith('#'):
    title = lines[0].lstrip('#').strip()
    body_content = '\n'.join(lines[1:]).strip()
else:
    # 使用文件名作为标题
    title = filename.replace('.md', '')
    body_content = markdown_content

# body_content 就是不含标题的正文，传给 AI 转换
```

**重要**: 只把 `body_content`（不含标题）传给下一步的 AI 转换。

---

### Step 2: AI 生成 HTML

遵循 `references/AI_CONVERTER_PROMPT.md` 提示词，将**正文内容**（不含标题）转换为 HTML。

**核心要求**:
- 允许标签: `p, br, strong, em, span, img, a, table, tr, td`
- 所有样式: inline + `!important`
- 禁止: `div, section, class, id, SVG, 动画, Emoji`
- 图片路径: 完全保留，不修改

**输出**: 保存到 `/tmp/article_styled.html`

---

### Step 3: 上传图片

扫描 HTML 中的本地图片，逐个上传到微信：

```bash
python3 ~/.claude/skills/wechat-publisher/scripts/image_uploader.py <image_path>
```

替换 HTML 中的 src 为微信 CDN URL。

---

### Step 4: 自动修复

在 `create_draft()` 中自动执行轻量修复:
1. 删除标签间空白 → 防止莫名空行
2. 确保所有样式有 `!important`
3. 强制禁用缩进 (`text-indent: 0`)
4. 移除不支持样式 (box-shadow, transform 等)

---

### Step 5: 提取元数据

- **标题**: 文件名（去除 .md 后缀）
- **作者**: 从配置文件读取（如果配置了），否则留空
- **封面**: 自动使用默认封面图（如果文章没有图片）

---

### Step 6: 发布草稿

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '/Users/as/.claude/skills/wechat-publisher/scripts')
from publisher import WeChatPublisher

with open('/tmp/article_styled.html', 'r', encoding='utf-8') as f:
    content = f.read()

publisher = WeChatPublisher()
result = publisher.create_draft(
    title="文章标题",
    content=content,
    # author 参数可以省略，会自动使用配置文件中的作者名
    # 如果需要覆盖配置，可以传入: author="特定作者名"
    thumb_media_id="",  # 留空则自动使用默认黑色封面
    digest="",
    content_base_dir="/path/to/article/directory"
)

print(f"Draft media_id: {result['media_id']}")
EOF
```

---

### Step 7: 清理

```bash
rm -f /tmp/article_styled.html
```

报告成功信息：
```
✓ 文章已成功发布到微信草稿箱！
Draft ID: {media_id}

查看草稿: https://mp.weixin.qq.com → 素材管理 → 草稿箱
```

---

## 资源文件

- **默认封面图**: `assets/default_cover.png` (900x500, 纯黑色)

## 参考文档

- **AI 转换提示词**: `references/AI_CONVERTER_PROMPT.md`
