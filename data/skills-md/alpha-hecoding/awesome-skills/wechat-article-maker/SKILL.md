---
name: wechat-article-maker
description: 智能创作并发布微信公众号文章。支持内容理解、链接分析、Markdown转换、图片清洗、样式处理和一键发布。当用户提到"创作公众号文章"、"发布文章链接"、"生成微信文章"、"推送到微信公众号"、"发布文章到微信公众号"时使用。
---

# 微信公众号文章创作与发布

## 语言

**匹配用户语言**：使用用户所用的语言进行回应。用户用中文则用中文回应，用英文则用英文回应。

## 目录结构

```
wechat-article-maker/
├── scripts/                  # TypeScript 源文件
│   ├── wechat-api.ts        # API 发布逻辑
│   ├── wechat-article.ts    # 浏览器发布逻辑
│   ├── wechat-browser.ts    # 图文发布逻辑
│   ├── image-utils.ts       # 图片处理工具（sharp 集成）
│   ├── generate-cover.ts    # 封面生成逻辑
│   ├── md-to-wechat.ts      # Markdown 转换逻辑
│   ├── ensure-deps.ts       # 依赖自动安装
│   └── md/                  # Markdown 渲染引擎
│       ├── render.ts
│       ├── themes/          # 主题样式
│       └── extensions/      # 扩展插件
├── references/              # 参考文档
├── SKILL.md                 # 技能文档
└── README.md                # 项目说明
```

**Agent 执行**：确定此 SKILL.md 目录为 `SKILL_DIR`，所有命令通过 `npx -y bun` 运行：

### 运行方式

```bash
# 设置技能目录
SKILL_DIR="${SKILL_DIR}"

# 所有脚本通过 npx -y bun 运行（跨平台统一）
npx -y bun "${SKILL_DIR}/scripts/wechat-api.ts" article.md --inline-css
npx -y bun "${SKILL_DIR}/scripts/md-to-wechat.ts" article.md --theme grace
npx -y bun "${SKILL_DIR}/scripts/generate-cover.ts" --title "标题" --output cover.jpg
```

**依赖自动安装**：脚本首次运行时会自动检测并安装所需依赖，无需手动操作。

## 依赖安装

**自动安装**：所有依赖会在脚本首次运行时自动安装，无需手动操作。

**运行时要求**：
- ✅ Bun（推荐，通过 `npx -y bun` 使用）

**依赖说明**（自动安装）：
- `front-matter` - Frontmatter 解析
- `highlight.js` - 代码高亮
- `marked` - Markdown 渲染引擎
- `reading-time` - 阅读时间计算
- `juice` - CSS 内联转换
- `@napi-rs/canvas` - 高性能图片生成（可选，用于封面）
- `sharp` - 图片处理库（内置，用于图片清理和封面生成）

**依赖说明**：
- `sharp` 会在首次运行时通过 `scripts/ensure-deps.ts` 自动安装
- 如果可选依赖未安装，`generate-cover` 会自动生成 SVG 格式的封面图（微信也支持）

## 功能概述

本技能提供完整的微信公众号文章工作流：

1. **内容创作模式**：输入文本内容，智能理解、生成文章
2. **链接发布模式**：输入文章链接，下载、处理并发布
3. **Markdown 转换**：内置 Markdown 到 HTML 转换，支持多主题
4. **图片处理**：自动下载、清洗元数据、符合微信规范
5. **样式转换**：自动将 CSS 转为内联样式
6. **一键发布**：支持 API（快速）和浏览器（可视化）两种方式

## 偏好设置（EXTEND.md）

使用 Bash 检查 EXTEND.md 存在性（优先级顺序）：

```bash
# 检查项目级别
test -f .awesome-skills/wechat-article-maker/EXTEND.md && echo "project"

# 检查用户级别（跨平台：$HOME 在 macOS/Linux/WSL 上都可用）
test -f "$HOME/.awesome-skills/wechat-article-maker/EXTEND.md" && echo "user"
```

┌────────────────────────────────────────────────────────────┬───────────────────┐
│                            路径                            │       位置        │
├────────────────────────────────────────────────────────────┼───────────────────┤
│ .awesome-skills/wechat-article-maker/EXTEND.md               │ 项目目录          │
├────────────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.awesome-skills/wechat-article-maker/EXTEND.md         │ 用户主目录        │
└────────────────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  结果     │                                  操作                                     │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ 找到      │ 读取、解析、应用设置                                                      │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ 未找到    │ 使用默认值                                                                │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md 支持**：默认主题 | 默认发布方法（api/browser）| 默认作者 | Chrome 配置文件路径

## 工作流程选择

根据用户输入自动选择工作流程：

| 输入类型 | 识别方式 | 工作流程 |
|---------|---------|---------|
| 纯文本内容 | 不包含链接 | 内容创作流程 |
| 文本 + 参考链接 | 包含链接，但主体是文本描述 | 内容创作流程（含链接分析）|
| 单个文章链接 | 仅包含 URL，或明确说"发布这篇文章" | 链接发布流程 |
| Markdown 文件路径 | 以 `.md` 结尾的文件路径 | Markdown 转换发布流程 |
| HTML 文件路径 | 以 `.html` 结尾的文件路径 | 直接发布流程 |

---

## 流程 1: 内容创作与发布

当用户输入文本内容（可选包含参考链接）时使用此流程。

### 创作进度清单

复制此清单并在完成时勾选：

```
内容创作进度：
- [ ] 步骤 0: 加载偏好设置
- [ ] 步骤 1: 内容分析与链接提取
- [ ] 步骤 2: 链接内容获取与理解
- [ ] 步骤 3: 询问创作偏好
- [ ] 步骤 4: 生成 Markdown 文章
- [ ] 步骤 5: 用户确认与优化
- [ ] 步骤 6: 转换为 HTML
- [ ] 步骤 7: 准备封面图
- [ ] 步骤 8: 发布到微信
- [ ] 步骤 9: 完成报告
```

### 步骤 0: 加载偏好设置

检查并加载 EXTEND.md 设置（见上方偏好设置部分）。

### 步骤 1: 内容分析与链接提取

分析用户输入：

1. **提取所有链接**：

```bash
# 提取 HTTP/HTTPS 链接
echo "$user_input" | grep -oE 'https?://[^\s]+' > /tmp/links.txt
```

2. **判断内容类型**：
   - 如果仅有单个链接且无其他文本 → 转到**流程 2: 链接发布流程**
   - 如果有文本内容（可选链接）→ 继续内容创作流程

### 步骤 2: 链接内容获取与理解

**如果内容中包含参考链接**：

1. **获取每个链接的内容**：

```typescript
// 使用 WebFetch 获取并分析
for (const url of links) {
  const content = await WebFetch(url, `
    请提取并总结以下信息：
    1. 文章标题
    2. 作者（如有）
    3. 核心观点（3-5个要点）
    4. 关键数据或案例
    5. 可引用的金句

    以结构化格式返回，便于后续引用。
  `);
}
```

2. **整理参考资料**：
   - 为每个链接创建摘要卡片
   - 标注关键引用点
   - 记录可用图片或数据

### 步骤 3: 询问创作偏好

使用 AskUserQuestion 询问用户偏好：

```
文章创作配置

问题1：文章风格
header: "风格"
选项：
- 专业分析 - 深度解读，适合技术或行业分析（推荐）
- 轻松科普 - 通俗易懂，适合大众读者
- 教程指南 - 步骤清晰，适合实操性内容
- 观点评论 - 表达看法，适合热点评论

问题2：文章长度
header: "长度"
选项：
- 短文（800-1200字）- 快速阅读
- 中等（1500-2500字）- 平衡深度与可读性（推荐）
- 长文（3000字+）- 深度长文

问题3：参考资料处理（如有链接）
header: "引用方式"
选项：
- 深度引用和分析 - 详细解读原文观点（推荐）
- 简要提及和链接 - 点到为止
- 仅作背景参考 - 不明确引用
```

### 步骤 4: 生成 Markdown 文章

基于用户输入、参考资料和偏好生成文章：

1. **标题生成要求**：

文章标题必须包含以下 5 个特点中的至少 3 个：

| 特点 | 说明 | 示例 |
|------|------|------|
| **痛点明确** | 直击目标读者的具体困扰 | 《还在手动改代码？这个工具让你开发效率提升 300%》 |
| **数字吸引** | 用具体数字增加可信度 | 《我花了 3 个月，整理了 1000 个 Python 技巧》 |
| **结果导向** | 承诺可量化的收益或改变 | 《学会这招，你的代码审查通过率提升 90%》 |
| **情绪调动** | 激发好奇心、紧迫感或共鸣 | 《千万别再这样写代码了！后果很严重》 |
| **悬念设置** | 制造悬念引发点击欲望 | 《99% 的程序员都不知道的调试技巧》 |

**标题公式参考**：
- 痛点 + 数字 + 结果：《花了 100 小时排错？这 3 个技巧让你秒定位 Bug》
- 数字 + 悬念：《7 个隐秘的 VS Code 功能，第 5 个太绝了》
- 情绪 + 痛点：《别再犯这个低级错误！新手程序员最常踩的 5 个坑》

2. **排版规范**：

**段落结构**：
- 每段控制在 3-5 行，避免大段文字
- 重要数据单独成段并加粗
- 关键结论前置，细节后置

**配图位置**：
- 标题下方放置封面图
- 每个步骤/章节后放置效果示意图
- 结尾放置总结图或行动号召图

**代码块**：
- 代码块前后留白（空行分隔）
- 必须使用语法高亮标注语言类型
- 关键行添加注释说明

**金句设计**：
- 核心观点单独成段
- 使用加粗或引用格式突出
- 控制在 20 字以内，便于记忆和传播

3. **文章结构**：

```markdown
---
title: 文章标题（遵循 5 大标题原则）
author: 作者名（从 EXTEND.md 或默认值）
summary: 文章摘要（120字以内，突出核心价值）
featureImage: 封面图路径（可选）
date: YYYY-MM-DD
---

# 文章标题（痛点明确 + 数字吸引 + 结果导向）

![封面图](cover.jpg)

引言段落，2-3行即可，
直接点明读者能获得什么价值。

## 第一部分：核心问题

（3-5行，聚焦痛点）

**关键数据单独成段加粗**

配合说明文字，3-4行即可。

![步骤效果图](step1.jpg)

## 第二部分：解决方案

分段讲解，每段 3-5 行。

```python
# 代码块前后留白
# 标注语言类型实现语法高亮
def solution():
    return "success"
```

> **金句：核心观点单独成段，增强记忆点**

![效果对比图](step2.jpg)

## 第三部分：实战案例

具体步骤 + 效果图，
让读者有代入感。

## 总结

简洁有力的结论，2-3 行。

![总结图](summary.jpg)

---

**参考资料**：
- [文章标题](链接)
```

2. **保存文件**：

```bash
# 生成 slug（文件名）
title="文章标题"
slug=$(echo "$title" | \
  iconv -t ascii//TRANSLIT 2>/dev/null | \
  tr '[:upper:]' '[:lower:]' | \
  tr ' ' '-' | \
  tr -cd '[:alnum:]-' | \
  cut -c1-50)

# 创建目录并保存
output_dir="wechat-articles/$(date +%Y-%m-%d)"
mkdir -p "$output_dir"
echo "$article_content" > "$output_dir/$slug.md"
```

3. **展示给用户**：

```
✓ 文章已生成

📄 标题：$title
📏 长度：约 $word_count 字
📁 保存位置：$output_dir/$slug.md

[文章预览内容...]

请选择下一步操作...
```

### 步骤 5: 用户确认与优化

使用 AskUserQuestion 询问：

```
文章已生成，请选择操作

header: "下一步"
选项：
- 直接发布 - 转换为 HTML 并发布到微信（推荐）
- 修改内容 - 说明需要调整的部分
- 重新生成 - 使用不同风格或角度
- 仅保存文件 - 不发布，稍后手动处理
```

**如果用户选择修改**：
1. 收集修改意见
2. 更新文章内容
3. 重新保存并展示
4. 再次询问下一步

**如果用户选择重新生成**：
- 返回步骤 3，重新询问偏好
- 使用不同的创作角度

### 步骤 6: 转换为 HTML

使用内置的 Markdown 渲染引擎转换：

1. **询问主题**（如未在 EXTEND.md 中指定）：

| 主题 | 描述 |
|------|------|
| `default` | 经典主题 - 传统排版，标题居中带底边，二级标题白字彩底 |
| `grace` | 优雅主题 - 文字阴影，圆角卡片，精致引用块（推荐）|
| `simple` | 简洁主题 - 现代极简风，不对称圆角，清爽留白 |

2. **执行转换**：

```bash
npx -y bun "${SKILL_DIR}/scripts/md-to-wechat.ts" \
  "$output_dir/$slug.md" \
  --theme grace \
  --output "$output_dir"
```

3. **解析输出 JSON**：

```json
{
  "title": "文章标题",
  "author": "作者",
  "summary": "摘要",
  "htmlPath": "路径/to/article.html",
  "contentImages": [
    {
      "placeholder": "WECHATIMGPH_1",
      "localPath": "/path/to/image1.jpg",
      "originalPath": "原始路径"
    }
  ]
}
```

### 步骤 7: 准备封面图

**封面图强制规则**（优先级顺序）：

1. **显式指定**：检查 Frontmatter 字段（`featureImage`, `coverImage`, `cover`, `image`）。
2. **自动首图回退**：若未显式指定封面，且文章中包含图片，**必须**自动提取并使用文章中的第一张图片作为封面。
3. **自动生成**：**只有**在文章中完全没有图片时，才触发封面图生成逻辑。

**如果没有指定且文章内无图片**，询问用户：

```
封面图设置（文章中未发现图片）

header: "封面来源"
选项：
- 自动生成 - 基于文章标题生成渐变背景封面（推荐）
- 提供路径 - 指定本地文件或 URL
- 暂不设置 - 稍后手动添加
```

**如果选择自动生成**：

1. **优先尝试多模态大模型生成**（如果 Agent 支持）：
   - 如果当前 Agent 环境具备文生图能力（Text-to-Image），请根据文章标题和摘要生成一张高质量的封面图。
   - 要求：2:1 比例（如 1024x512），风格现代、简洁，适合作为公众号封面。
   - 保存为：`$output_dir/$slug-cover.jpg`
   - **注意**：如果 Agent 无法生成图片（例如无工具支持），则直接使用下方降级方案。

2. **降级方案（使用脚本生成）**：

   如果无法使用大模型生成图片，则运行以下命令生成渐变背景文字封面：

```bash
# 使用 Node.js 脚本生成（无系统依赖）
npx -y bun "${SKILL_DIR}/scripts/generate-cover.ts" \
  --title "$title" \
  --output "$output_dir/$slug-cover.jpg" \
  --gradient-start "#667eea" \
  --gradient-end "#764ba2"
```

**封面要求**：
- 格式：JPEG, PNG, GIF 或 WebP
- 推荐尺寸：900x500px（2:1 比例）
- 文件大小：< 2MB

### 步骤 8: 发布到微信

询问发布方式：

```
发布方式选择

header: "发布方法"
选项：
- API 方式 - 快速发布，需要 API 凭证（推荐）
- 浏览器方式 - 可视化操作，需要 Chrome
- 仅输出 HTML - 保存文件，稍后手动发布
```

#### 选项 A: API 方式发布

1. **检查 API 凭证**：

```bash
# 检查项目级别
test -f .awesome-skills/.env && grep -q "WECHAT_APP_ID" .awesome-skills/.env && echo "project"

# 检查用户级别
test -f "$HOME/.awesome-skills/.env" && grep -q "WECHAT_APP_ID" "$HOME/.awesome-skills/.env" && echo "user"
```

2. **如果凭证缺失**，引导设置：

```
微信 API 凭证未找到

获取凭证步骤：
1. 访问 https://mp.weixin.qq.com
2. 进入：开发 → 基本配置
3. 复制 AppID 和 AppSecret

保存位置？
A) 项目级别：.awesome-skills/.env（仅此项目）
B) 用户级别：~/.awesome-skills/.env（所有项目）
```

创建 `.env` 文件：

```bash
WECHAT_APP_ID=<用户输入>
WECHAT_APP_SECRET=<用户输入>
```

3. **执行发布**：

```bash
npx -y bun "${SKILL_DIR}/scripts/wechat-api.ts" \
  "$output_dir/$slug.html" \
  --title "$title" \
  --summary "$summary" \
  --cover "$cover_image" \
  --inline-css
```

**重要**：`--inline-css` 参数将 CSS 转为内联样式，微信公众号不支持 `<style>` 标签。

#### 选项 B: 浏览器方式发布

```bash
npx -y bun "${SKILL_DIR}/scripts/wechat-article.ts" \
  --html "$output_dir/$slug.html" \
  --title "$title" \
  --summary "$summary"
```

**首次运行**：会打开 Chrome 浏览器，需要扫码登录微信公众号。

#### 选项 C: 仅输出 HTML

```bash
echo "✓ HTML 文件已保存至：$output_dir/$slug.html"
echo ""
echo "文件包含："
echo "• 内联样式（符合微信规范）"
echo "• 完整的文章内容"
echo "• 本地图片路径"
```

### 步骤 9: 完成报告

发布成功后，显示摘要：

```
✓ 微信公众号文章创作与发布完成！

创作信息：
• 输入：用户文本内容
• 参考链接：$link_count 个
• 文章风格：$style
• 文章长度：$word_count 字

发布信息：
• 标题：$title
• 作者：$author
• 摘要：$summary
• 主题：$theme
• 图片：$image_count 张
• 封面：$cover_source

发布方式：API / 浏览器

结果：
✓ 草稿已保存到微信公众号
• media_id: $media_id

下一步：
→ 管理草稿：https://mp.weixin.qq.com（登录后进入「内容管理」→「草稿箱」）

生成的文件：
• $output_dir/$slug.md（Markdown 源文件）
• $output_dir/$slug.html（HTML 文件）
• $output_dir/$slug-cover.jpg（封面图）
```

---

## 流程 2: 链接文章发布

当用户输入单个文章链接时使用此流程。

### 发布进度清单

复制此清单并在完成时勾选：

```
链接发布进度：
- [ ] 步骤 0: 加载偏好设置
- [ ] 步骤 1: 链接验证
- [ ] 步骤 2: 文章下载与解析
- [ ] 步骤 3: 图片下载与清洗
- [ ] 步骤 4: 样式转换（CSS 内联）
- [ ] 步骤 5: 用户确认
- [ ] 步骤 6: 准备封面图
- [ ] 步骤 7: 执行发布
- [ ] 步骤 8: 完成报告
```

### 步骤 0: 加载偏好设置

检查并加载 EXTEND.md 设置。

### 步骤 1: 链接验证

验证链接可访问性：

```bash
# 检查链接状态
status_code=$(curl -sI -w "%{http_code}" -o /dev/null "$url")
if [ "$status_code" = "200" ]; then
  echo "链接有效"
else
  echo "链接无法访问，状态码: $status_code"
fi
```

### 步骤 2: 文章下载与解析

使用 WebFetch 获取文章内容：

```typescript
const article = await WebFetch(url, `
请提取以下信息并以 JSON 格式返回：

{
  "title": "文章标题",
  "author": "作者（如果有）",
  "summary": "文章摘要或简介（120字以内）",
  "content": "HTML 格式的正文内容，保留原始样式和结构",
  "images": ["图片URL数组"],
  "featureImage": "封面图URL（如果有）",
  "publishDate": "发布日期（如果有）"
}

注意：
- content 需要包含完整的 HTML 标签和样式
- images 包含文章中所有的图片URL
- 保留原文的段落、标题、列表等结构
`);
```

### 步骤 3: 图片下载与清洗

1. **创建临时目录**：

```bash
temp_dir="wechat-temp/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$temp_dir/images"
```

2. **下载所有图片**：

```bash
# 解析图片URL数组并下载
image_index=1
for img_url in "${images[@]}"; do
  # 获取文件扩展名
  ext="${img_url##*.}"
  ext="${ext%%\?*}"  # 移除URL参数

  # 下载图片
  output_file="$temp_dir/images/image_${image_index}.${ext}"
  curl -L -o "$output_file" "$img_url" 2>/dev/null

  image_index=$((image_index + 1))
done
```

3. **图片元数据清洗**：

脚本 `wechat-api.ts` 会自动执行以下清洗：

- **检测 JPEG 图片**中的非标准元数据
- **清除 AIGC/Coze 标记**（微信不支持）
- **保留有效的 EXIF 数据**和图像内容
- **自动重试**：如果上传失败（错误码 40113），强制清洗后重试

算法（参考 `scripts/wechat-api.ts:105-180`）：

```typescript
function cleanImageMetadata(buffer: Buffer): Buffer {
  // 检查 JPEG 签名
  if (buffer[0] !== 0xff || buffer[1] !== 0xd8) return buffer;

  // 检测 AIGC 标记
  const headerStr = buffer.slice(0, 2048).toString('binary');
  const hasAigcMarker = headerStr.includes('AIGC{') || headerStr.includes('Coze');

  if (!hasAigcMarker) return buffer;

  // 跳过非标准 APP 段（0xeb, 0xec 等）
  // 保留标准段（APP0-APP9, DQT, SOF 等）
  // 返回清洗后的 buffer
}
```

### 步骤 4: 样式转换（CSS 内联）

**关键步骤**：微信公众号不支持 `<style>` 标签，必须将 CSS 转为内联样式。

1. **保存原始 HTML**：

```bash
echo "$html_content" > "$temp_dir/original.html"
```

2. **执行 CSS 内联转换**：

```bash
# 使用 wechat-api.ts 的内联转换功能
# 注意：这里先生成处理后的 HTML，不立即发布
npx -y bun "${SKILL_DIR}/scripts/wechat-api.ts" \
  "$temp_dir/original.html" \
  --inline-css \
  --output "$temp_dir/processed.html" \
  --dry-run
```

3. **替换图片路径**：

```bash
# 将远程图片URL替换为本地路径
for i in {1..${#images[@]}}; do
  sed -i "s|${images[$i-1]}|$temp_dir/images/image_$i.jpg|g" "$temp_dir/processed.html"
done
```

### 步骤 5: 用户确认

展示处理结果并询问：

```
文章处理完成

📄 标题：$title
✍️ 作者：$author
📝 摘要：$summary
🌐 原文：$original_url
🖼️ 图片：共 $image_count 张（已下载并清洗元数据）
🎨 样式：已转换为内联样式（符合微信规范）

HTML 已保存至：$temp_dir/processed.html

请选择操作
```

使用 AskUserQuestion：

```
header: "发布选项"
选项：
- 直接发布（API）- 快速发布到草稿箱（推荐）
- 浏览器发布 - 打开浏览器可视化操作
- 仅输出 HTML - 保存文件，稍后手动处理
- 取消 - 不保存
```

### 步骤 6: 准备封面图

与流程 1 的步骤 7 相同，**遵循封面图强制规则**：

1. 优先使用原文提取的 `featureImage`。
2. 若无显式封面，自动使用下载图片中的第一张作为封面。
3. 仅在原文完全没有图片时，才询问生成封面。

### 步骤 7: 执行发布

根据用户选择执行：

#### 选项 A: 直接发布（API）

```bash
npx -y bun "${SKILL_DIR}/scripts/wechat-api.ts" \
  "$temp_dir/processed.html" \
  --title "$title" \
  --summary "$summary" \
  --cover "$cover_image" \
  --inline-css
```

**API 方式特性**：
- ✓ 自动下载远程图片
- ✓ 自动清洗图片元数据（AIGC/Coze 标记）
- ✓ 如果上传失败（40113），强制清洗后重试
- ✓ 支持格式：JPEG, PNG, GIF, WebP

#### 选项 B: 浏览器发布

```bash
npx -y bun "${SKILL_DIR}/scripts/wechat-article.ts" \
  --html "$temp_dir/processed.html" \
  --title "$title" \
  --summary "$summary"
```

#### 选项 C: 仅输出 HTML

```bash
# 复制到永久位置
output_path="wechat-articles/$(date +%Y-%m-%d)/$slug.html"
mkdir -p "$(dirname "$output_path")"
cp "$temp_dir/processed.html" "$output_path"
cp -r "$temp_dir/images" "$(dirname "$output_path")/"

echo "✓ HTML 已保存至：$output_path"
echo "✓ 图片已保存至：$(dirname "$output_path")/images/"
```

### 步骤 8: 完成报告

```
✓ 链接文章发布完成！

原文信息：
• 链接：$original_url
• 标题：$title
• 作者：$author

处理信息：
• 下载并转换 HTML
• 清洗 $image_count 张图片元数据
• 转换样式为内联格式
• 生成封面图：$cover_source

发布信息：
• 方式：API / 浏览器
• 主题：保留原样式
• 状态：✓ 草稿已保存

结果：
• media_id: $media_id

下一步：
→ 管理草稿：https://mp.weixin.qq.com（登录后进入「内容管理」→「草稿箱」）

生成的文件：
• $output_path（处理后的 HTML）
• $(dirname "$output_path")/images/（清洗后的图片）
```

---

## 流程 3: Markdown 文件发布

当用户提供 `.md` 文件路径时使用此流程。

### 快速发布

```bash
# 一键转换并发布
npx -y bun "${SKILL_DIR}/scripts/md-to-wechat.ts" \
  "$markdown_file" \
  --theme grace \
  --output ./output

# 然后使用 API 发布
npx -y bun "${SKILL_DIR}/scripts/wechat-api.ts" \
  "$html_output" \
  --inline-css \
  --cover "$cover_image"
```

### 步骤说明

1. **解析 Markdown**：提取 frontmatter（title, author, summary 等）
2. **转换为 HTML**：应用主题样式
3. **处理图片**：下载远程图片，替换为本地路径
4. **发布**：同流程 1 的步骤 8

---

## 流程 4: HTML 文件直接发布

当用户提供 `.html` 文件路径时使用此流程。

### 快速发布

```bash
# 直接发布（自动内联 CSS）
npx -y bun "${SKILL_DIR}/scripts/wechat-api.ts" \
  "$html_file" \
  --title "文章标题" \
  --summary "摘要" \
  --cover "$cover_image" \
  --inline-css
```

**注意**：必须使用 `--inline-css` 参数，否则样式会丢失。

---

## 图文发布（图文消息）

用于发布短内容 + 多张图片（最多 9 张）。

### 使用方法

```bash
# 从 Markdown 文件发布
npx -y bun "${SKILL_DIR}/scripts/wechat-browser.ts" \
  --markdown article.md \
  --images ./images/

# 直接指定内容和图片
npx -y bun "${SKILL_DIR}/scripts/wechat-browser.ts" \
  --title "标题" \
  --content "内容" \
  --image img1.png \
  --image img2.png \
  --submit
```

### 参数说明

| 参数 | 描述 |
|------|------|
| `--markdown <path>` | Markdown 文件 |
| `--title <text>` | 标题 |
| `--content <text>` | 内容文字 |
| `--image <path>` | 图片路径（可多次使用）|
| `--images <dir>` | 图片目录 |
| `--submit` | 自动提交 |

详见：[references/image-text-posting.md](references/image-text-posting.md)

---

## 主题样式

内置三种主题（位于 `scripts/md/themes/`）：

### default - 经典主题

- 传统排版风格
- 标题居中，带底边装饰
- 二级标题：白字彩底
- 适合：正式文章、行业报告

### grace - 优雅主题（推荐）

- 文字带柔和阴影
- 圆角卡片式引用块
- 精致的列表样式
- 适合：科普文章、个人博客

### simple - 简洁主题

- 现代极简风格
- 不对称圆角设计
- 清爽留白
- 适合：教程、短文

### 自定义主题

1. 在 `scripts/md/themes/` 创建新的 CSS 文件
2. 基于 `base.css` 扩展样式
3. 使用 `--theme <name>` 参数应用

---

## 配置与环境

### 环境变量

从以下位置加载配置（优先级从高到低）：

1. 环境变量
2. `<cwd>/.awesome-skills/.env`
3. `~/.awesome-skills/.env`

必需的环境变量（API 发布方式）：

```bash
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

可选的环境变量：

```bash
WECHAT_BROWSER_CHROME_PATH=/path/to/chrome  # 自定义 Chrome 路径
```

### EXTEND.md 配置示例

```markdown
# wechat-article-maker 配置

## 默认设置

- 主题：grace
- 发布方式：api
- 作者：宝玉
- Chrome 配置文件：~/.chrome-wechat

## 自动操作

- 自动生成封面：true
- 自动清洗图片：true
- 自动内联样式：true

## 创作偏好

- 默认文章风格：专业分析
- 默认文章长度：中等（1500-2500字）
- 默认引用方式：深度引用和分析
```

---

## 技术细节

### Markdown 渲染引擎

使用 `markdown-it` 及扩展（位于 `scripts/md/`）：

- **基础渲染**：`render.ts`
- **扩展插件**：
  - `alert.ts` - GitHub 风格提示块
  - `footnotes.ts` - 脚注支持
  - `katex.ts` - 数学公式
  - `toc.ts` - 目录生成
  - `infographic.ts` - 信息图
  - `ruby.ts` - 注音
  - `slider.ts` - 滑块
  - `plantuml.ts` - UML 图表

### 图片处理算法

**元数据清洗**（`scripts/image-utils.ts`）：

内置 sharp 库提供可靠的图片处理能力：

1. **智能检测**：扫描图片前 2KB，检测 AIGC/Coze/Adobe 等非标准元数据标记
2. **深度清理**：使用 sharp 重新编码 JPEG，彻底移除所有元数据
3. **自动降级**：sharp 不可用时，使用手动解析作为后备方案
4. **尺寸优化**：自动调整超大图片（限制 1920x1080）以符合微信规范

```typescript
// 图片处理流程
const result = await cleanImage(buffer, forceClean);
// 返回: { buffer, wasCleaned, method: "sharp"|"manual"|"none", originalSize, cleanedSize }
```

**双引擎清理策略**：

| 方法 | 优先级 | 说明 |
|------|--------|------|
| **Sharp 重新编码** | 首选 | 完全重新编码图片，100% 移除元数据 |
| **手动解析** | 后备 | 解析 JPEG 段结构，跳过非标准标记 |

**自动重试逻辑**：

```typescript
try {
  await uploadImage(imageBuffer);
} catch (error) {
  if (error.code === 40113) {
    // 强制使用 sharp 深度清理后重试
    const cleanedBuffer = await cleanImage(imageBuffer, true);
    await uploadImage(cleanedBuffer);
  }
}
```

### CSS 内联转换

使用 `juice` 或类似库将 CSS 规则转换为内联样式：

**之前**：
```html
<style>
  h1 { color: blue; font-size: 24px; }
</style>
<h1>标题</h1>
```

**之后**：
```html
<h1 style="color: blue; font-size: 24px;">标题</h1>
```

**为什么需要**：微信公众号编辑器不支持 `<style>` 标签，只接受内联样式。

### 封面图生成

**方式 1: 多模态大模型生成（推荐）**

如果 Agent 具备文生图能力，优先根据文章内容生成定制化封面图。这能提供更具吸引力和相关性的视觉效果。

**方式 2: 纯 Node.js（无系统依赖）**

脚本：`scripts/generate-cover.ts`

```bash
npx -y bun "${SKILL_DIR}/scripts/generate-cover.ts" \
  --title "文章标题" \
  --output cover.jpg \
  --gradient-start "#667eea" \
  --gradient-end "#764ba2" \
  --width 900 \
  --height 500
```

特性：
- ✓ 无需 ImageMagick
- ✓ 支持多种图片库（@napi-rs/canvas、sharp、SVG）
- ✓ 自动换行长标题
- ✓ 可自定义颜色和尺寸
- ✓ 跨平台（Node.js/Bun）

**方式 2: ImageMagick（如已安装）**

```bash
convert -size 900x500 \
  -define gradient:angle=135 \
  gradient:'#667eea'-'#764ba2' \
  -gravity center \
  -font "DejaVu-Sans-Bold" \
  -pointsize 48 \
  -fill white \
  -annotate +0-30 "标题第一行" \
  -pointsize 36 \
  -annotate +0+30 "标题第二行" \
  cover.jpg
```

---

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 依赖未安装 | 依赖会在首次运行时自动安装 |
| Cannot find module | 尝试重新运行命令，会自动安装缺失依赖 |
| 封面图生成 SVG 而非 PNG/JPEG | 可选依赖未安装，运行 `cd ${SKILL_DIR}/scripts && npm install @napi-rs/canvas` 或接受 SVG 格式 |
| 链接无法访问 | 检查网络连接，尝试使用代理或 VPN |
| 图片上传失败 (40113) | sharp 自动深度清理元数据后重试，无需手动处理 |
| 样式丢失 | 确保使用了 `--inline-css` 参数 |
| API 错误 40001 | access_token 无效或过期，检查 API 凭证 |
| API 错误 40164 (invalid ip) | 在微信公众号后台添加服务器 IP 到白名单：<br/>mp.weixin.qq.com → 开发 → 基本配置 → IP白名单 |
| Chrome 未找到 | 设置环境变量 `WECHAT_BROWSER_CHROME_PATH` |
| 标题/摘要缺失 | 手动指定 `--title` 和 `--summary` 参数 |
| 粘贴失败（浏览器方式）| 检查系统剪贴板权限 |
| Markdown 转换错误 | 检查 Markdown 语法，确保 frontmatter 格式正确 |

---

## 最佳实践

### 1. 内容创作

- ✓ 提供清晰的创作意图和目标读者
- ✓ 引用链接时说明如何使用（深度分析 vs 简要提及）
- ✓ 预览后再发布，避免返工
- ✓ 保存 Markdown 源文件，便于后续修改
- ✓ **标题必须包含至少 3 个特点**：痛点明确、数字吸引、结果导向、情绪调动、悬念设置
- ✓ **段落控制 3-5 行**，重要数据单独成段加粗
- ✓ **金句单独成段**，控制在 20 字以内，便于传播

### 2. 链接发布

- ✓ 确认链接可访问（避免需要登录的页面）
- ✓ 检查原文图片质量（模糊图片建议替换）
- ✓ 优先使用 API 方式（快速可靠）
- ✓ 发布前预览处理后的 HTML

### 3. 样式与排版

- ✓ 专业文章用 `default` 主题
- ✓ 大众内容用 `grace` 主题（推荐）
- ✓ 教程类用 `simple` 主题
- ✓ 确保图片清晰度（推荐 2x 分辨率）
- ✓ 封面图使用 2:1 比例（900x500px）

### 4. 发布流程

- ✓ 首次使用先配置 API 凭证
- ✓ 发布前在草稿箱预览
- ✓ 保留源文件（markdown/html）以便后续修改
- ✓ 定期备份已发布的文章

### 5. 图片处理

- ✓ 使用高质量原图（避免二次压缩）
- ✓ 图片尺寸适中（宽度 800-1200px）
- ✓ 文件大小控制在 1MB 以内
- ✓ 如有 AIGC 图片，让脚本自动清洗

### 6. 排版与可读性

**段落结构**：
- ✓ 每段 3-5 行，避免视觉疲劳
- ✓ 重要数据/结论单独成段并加粗
- ✓ 复杂内容分点说明，不要堆砌

**配图策略**：
- ✓ 标题下方必放封面图
- ✓ 关键步骤后放置效果图/示意图
- ✓ 文章结尾放置总结图或 CTA 图

**代码展示**：
- ✓ 代码块前后留空行
- ✓ 必须标注编程语言实现语法高亮
- ✓ 关键行添加注释，辅助理解

**金句设计**：
- ✓ 核心观点提炼成金句，单独成段
- ✓ 使用 `**加粗**` 或 `> 引用` 突出
- ✓ 长度控制在 20 字内，朗朗上口

---

## 功能对比

| 功能 | 内容创作 | 链接发布 | Markdown 发布 | HTML 发布 | 图文发布 |
|------|---------|---------|--------------|----------|---------|
| 输入类型 | 文本 + 链接 | 单个链接 | .md 文件 | .html 文件 | 短文 + 图片 |
| 内容理解 | ✓ | ✓ | ✗ | ✗ | ✗ |
| 文章生成 | ✓ | ✗ | ✗ | ✗ | ✗ |
| Markdown 转换 | ✓ | ✗ | ✓ | ✗ | ✓ |
| 主题样式 | ✓ | 保留原样 | ✓ | 保留原样 | ✗ |
| 图片清洗 | ✓ | ✓ | ✓ | ✓ | ✗ |
| CSS 内联 | ✓ | ✓ | ✓ | ✓ | ✗ |
| 封面生成 | ✓ | ✓ | ✓ | ✓ | ✗ |
| API 发布 | ✓ | ✓ | ✓ | ✓ | ✗ |
| 浏览器发布 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 适用场景 | 原创内容 | 转载/分享 | 本地文章 | 现成 HTML | 图片展示 |

---

## 使用示例

### 示例 1: 创作新文章（纯文本）

```
用户：创作一篇关于 AI 编程助手发展趋势的文章

Agent：
✓ 分析内容类型 → 纯文本创作模式
✓ 询问文章风格、长度 → 用户选择"专业分析"、"中等"
✓ 生成文章并展示
✓ 用户确认后转换为 HTML（grace 主题）
✓ 自动生成封面图
✓ 使用 API 发布到草稿箱

结果：
• 文章保存至 wechat-articles/2026-02-09/ai-coding-assistant-trends.md
• HTML 输出至 wechat-articles/2026-02-09/ai-coding-assistant-trends.html
• 封面图：wechat-articles/2026-02-09/ai-coding-assistant-trends-cover.jpg
• 微信草稿箱 media_id: abc123...
```

### 示例 2: 基于链接创作

```
用户：基于这篇文章创作一篇公众号文章，深度分析其中的观点：
https://example.com/ai-future

Agent：
✓ 提取链接并获取内容
✓ 整理关键观点和数据
✓ 询问创作方向 → 用户选择"专业分析"、"深度引用"
✓ 生成文章，引用原文 3 个核心观点，加入自己的分析
✓ 用户确认后发布

结果：
• 生成了 2300 字的深度分析文章
• 引用了原文 3 个观点和 2 个数据
• 添加了参考资料链接
• 已发布到微信草稿箱
```

### 示例 3: 直接发布链接文章

```
用户：发布这篇文章到公众号：https://blog.example.com/great-article

Agent：
✓ 识别为链接发布模式
✓ 下载文章 HTML 和 5 张图片
✓ 清洗图片元数据（检测到 2 张含 AIGC 标记，已清洗）
✓ 转换样式为内联格式
✓ 展示处理结果
✓ 用户确认"直接发布"
✓ 使用 API 发布

结果：
• 处理后 HTML：wechat-temp/20260209-153000/processed.html
• 清洗后图片：wechat-temp/20260209-153000/images/ (5张)
• 微信草稿箱 media_id: xyz789...
```

### 示例 4: Markdown 文件发布

```
用户：发布这个 Markdown 文件：./posts/my-article.md

Agent：
✓ 读取文件，解析 frontmatter
✓ 询问主题 → 用户选择 "grace"
✓ 转换为 HTML，应用主题样式
✓ 下载文章中的 3 张远程图片
✓ 自动生成封面图（基于标题）
✓ 发布到微信

结果：
• HTML 输出至 ./posts/my-article.html
• 封面图：./posts/my-article-cover.jpg
• 已发布到草稿箱
```

### 示例 5: 图文消息发布

```
用户：发布一组产品图片到公众号，标题是"新品上市"

Agent：
✓ 识别为图文发布模式
✓ 打开浏览器，定位到图文消息编辑器
✓ 填写标题
✓ 上传 6 张图片
✓ 提交发布

结果：
• 图文消息已保存到草稿箱
• 包含 6 张产品图片
```

---

## 参考文档

| 主题 | 文档 |
|------|------|
| 图文发布参数、自动压缩 | [references/image-text-posting.md](references/image-text-posting.md) |
| 文章主题、图片处理 | [references/article-posting.md](references/article-posting.md) |

---

## 权限要求

- **网络访问**：获取链接内容、下载图片
- **文件读写**：保存文章、图片和配置
- **环境变量**：读取微信 API 凭证
- **外部命令**：调用 bun/npx 执行 TypeScript 脚本
- **浏览器**（可选）：Chrome 用于浏览器发布方式

---

## 依赖与许可

### 核心依赖

- **Bun/Node.js**：运行 TypeScript 脚本（Node.js >= 18.0.0）
- **npm/bun**：包管理器（用于安装依赖）

### 自动安装的依赖

脚本会在首次运行时通过 `scripts/ensure-deps.ts` 自动安装以下依赖：

**必需包**：
- `front-matter` - Frontmatter 解析
- `highlight.js` - 代码高亮
- `marked` - Markdown 渲染引擎
- `reading-time` - 阅读时间计算
- `juice` - CSS 内联转换库

**可选包**（封面图生成）：
- `@napi-rs/canvas` - 高性能图片生成
- `sharp` - 图片处理库

### 运行时依赖（可选）

- **Chrome/Chromium**：浏览器发布方式需要
- **微信公众号 API 凭证**：API 发布方式需要

### 许可证

- Markdown 渲染引擎基于 MIT 许可证
- 微信公众号 API 使用需遵守微信公众平台服务协议

---

## 致谢

本技能整合了以下功能和技术：

- **Markdown 渲染**：基于 marked 及扩展插件
- **样式主题**：参考微信公众号优秀排版实践
- **图片处理**：JPEG 元数据清洗算法
- **微信 API**：官方文档和最佳实践

---

## 更新日志

### v1.0.3 (2026-02-10)

- ✓ 优化封面图规则：设置为强制逻辑。未指定封面时，若文章中有图则默认使用第一张，仅在文章无图时才生成默认封面。

### v1.0.2 (2026-02-10)

- ✓ 优化配图策略：优先使用多模态大模型生成高质量封面图
- ✓ 修正 `md-to-wechat.ts` 脚本支持 `--output` 参数

### v1.0.1 (2026-02-10)

- ✓ 新增标题生成 5 大原则（痛点明确、数字吸引、结果导向、情绪调动、悬念设置）
- ✓ 新增文章排版规范（段落结构、配图位置、代码块、金句设计）
- ✓ 优化内容创作流程，提升文章可读性和传播性

### v1.0.0 (2026-02-09)

- ✓ 整合内容创作和链接发布功能
- ✓ 内置 Markdown 转 HTML 转换器
- ✓ 支持三种主题样式（default, grace, simple）
- ✓ 自动图片元数据清洗
- ✓ CSS 自动内联转换
- ✓ 封面图生成（无系统依赖）
- ✓ API 和浏览器两种发布方式
- ✓ 完整的工作流程和错误处理

---

**技能版本**：1.0.3
**最后更新**：2026-02-10
**作者**：整合自 wechat-article-writer 和 baoyu-post-to-wechat
