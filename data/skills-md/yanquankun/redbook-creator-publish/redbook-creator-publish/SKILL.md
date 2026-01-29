---
name: redbook-creator-publish
description: "小红书帖子创作与发布技能。用于：(1) 生成小红书风格的帖子内容（标题+正文+标签）(2) 生成帖子相关的配图 (3) 自动上传到小红书创作者平台（默认自动上传，失败时自动提供手动指引） (4) 生成本地预览HTML文件。触发词：小红书创作、create redbook、小红书、红书、笔记创作、帖子创作"
---

# 小红书帖子创作与发布技能

## 概述

本技能帮助用户创作小红书风格的优质内容，包括标题、正文、标签、配图，并**默认自动上传**到小红书创作者平台。

**重要更新（v3.0）**：
- 🐍 **Python 实现**：使用 Playwright for Python 实现浏览器自动化（新增）
- 🚀 **默认自动上传**：无需询问用户，直接执行自动上传
- 🔧 **智能降级**：自动上传失败时自动提供详细手动上传指引
- ✅ 配图改为 PNG/JPG 格式（不再使用 HTML）
- ✅ 预览 HTML 和 MD 文档支持显示图片
- ✅ 使用 Playwright 浏览器自动化（比 Selenium 更快更稳定）
- ✅ DOM 选择器配置化
- ✅ 话题深度搜索功能

## 前置检查

在开始工作流程前，必须检查并准备以下环境：

### 1. 检查 Python 环境（必需）

```bash
python3 --version
```

**要求**：Python 3.0 或更高版本

**如果未安装或版本过低**：
- 输出错误信息：`❌ 未检测到 Python 3+ 环境`
- 提示用户：
  ```
  本技能需要 Python 3.0+ 支持。

  安装方法:
  - macOS: brew install python3
  - Windows: 访问 https://www.python.org/ 下载安装

  安装完成后请重新运行此技能。
  ```
- **停止执行**，等待用户安装 Python

### 2. 检查 Playwright 是否安装（首次自动安装）

```bash
python3 -c "import playwright" 2>/dev/null && echo "Playwright installed" || echo "Playwright not found"
```

**如果未安装**：
- 输出信息：`🔍 检测到 Playwright 未安装，正在自动安装...`
- 自动执行安装：
  ```bash
  pip3 install playwright
  playwright install chromium
  ```
- 显示安装进度和结果
- 安装完成后输出：`✅ Playwright 安装完成`

**如果已安装**：
- 输出：`✅ Playwright 已安装`

### 3. 检查 Chrome 浏览器（用于 HTML 转图片）

```bash
# macOS
test -d "/Applications/Google Chrome.app" && echo "Chrome installed" || echo "Chrome not found"
```

**如果未安装**：
- 输出警告信息：`⚠️  未检测到 Chrome 浏览器`
- 提示用户：
  ```
  配图转换需要 Chrome（HTML 转 PNG 功能）。

  下载地址: https://www.google.com/chrome/

  注意：Playwright 会使用 Chromium 进行自动化上传，不依赖系统 Chrome
  ```
- 可以继续执行（配图可稍后手动生成）

## 工作流程

### 第一步：确定创作主题并深度搜索

**重要**：无论用户是否提供话题，都必须先进行深度搜索，确保内容的准确性和时效性。

#### 1.1 话题确定

- **用户提供话题**：使用用户提供的话题
- **用户未提供话题**：搜索当日最新的 AI 资讯或热门话题作为创作素材

#### 1.2 深度搜索（必须执行）

使用 WebSearch 工具对话题进行深度搜索：

**搜索要求**：
- 搜索至少 2-3 个相关关键词
- 获取最新的数据、案例、用户反馈（确保信息来自最新年份（如2026年）
- 了解话题的热度和讨论方向
- 确保内容符合主题并有深度

**示例搜索关键词**：
- 话题"AI工具"：
  - "2026最新AI工具推荐"
  - "AI工具使用教程案例"
  - "AI工具效率提升数据"
- 话题"工作效率"：
  - "提高工作效率方法2026"
  - "效率工具推荐使用体验"
  - "时间管理技巧实战"

**搜索输出**：
```
🔍 正在深度搜索话题: [话题名称]

搜索关键词 1: [关键词]
- 找到 X 个相关结果
- 关键信息: [摘要]

搜索关键词 2: [关键词]
- 找到 X 个相关结果
- 关键信息: [摘要]

✅ 搜索完成，已获取充足素材
```

### 第二步：生成帖子内容

参考 [references/style-guide.md](references/style-guide.md) 了解小红书内容风格规范。

#### 标题要求

- **字数限制**：不超过20个字
- **可以使用emoji**：适当添加1-2个emoji增加吸引力
- **钩子设计**：标题必须包含钩子元素，激发用户好奇心

**标题钩子类型**：
- 数字型：「3个方法」「5分钟学会」
- 疑问型：「为什么...」「你知道吗」
- 利益型：「省钱」「变美」「提效」
- 悬念型：「没想到...」「竟然...」
- 共鸣型：「终于找到了」「后悔没早知道」

#### 正文要求

- **语言**：使用中文（技术专有名词可保留英文）
- **字数要求**：正文内容必须在 **300-500字** 之间，内容要充实有料
- **结构**：开头钩子 → 核心内容（详细展开）→ 总结/互动
- **段落**：每段2-4行，善用分段和空行
- **符号**：适当使用分隔符增强阅读体验
- **素材来源**：基于深度搜索结果，整合最新信息和案例

**正文钩子段示例**：
```
姐妹们！这个方法我藏了好久了...
不敢相信，我居然现在才发现这个...
分享一个让我效率翻倍的小技巧...
```

**正文内容展开要求**：
- 每个要点要有详细说明，不能只是一句话带过
- 加入个人使用体验和感受（可以基于搜索到的用户反馈改写）
- 提供具体的使用场景和案例（使用搜索到的真实案例）
- 适当加入对比（使用前 vs 使用后）
- 引用搜索到的数据增加可信度

**内容输出格式**：
```markdown
## 标题
[生成的标题，包含emoji]

## 正文
[开头钩子段 - 引发共鸣，30-50字]

[核心内容 - 详细展开每个要点，200-350字]
- 使用搜索到的数据和案例
- 加入具体使用场景
- 提供对比和体验

[总结段 - 归纳重点，30-50字]

[互动引导 - 引导评论收藏，20-30字]

## 标签
#标签1 #标签2 #标签3 #标签4 #标签5 #标签6 #标签7 #标签8
```

### 第三步：生成配图（PNG/JPG 格式）

**重要变更**：不再使用 HTML 格式，直接生成 PNG/JPG 图片。

#### 图片生成流程

1. **先生成 HTML 模板**（临时文件）：使用 Newsprint 风格创建卡片
2. **转换为 PNG**：使用 Chrome headless 模式截图
3. **删除临时 HTML**：只保留 PNG 文件

#### 图片要求

- **数量**：生成 **1张** 主图配图即可（不再需要多张裁剪）
- **格式**：PNG 或 JPG（推荐 PNG）
- **尺寸**：**9:16 竖版比例**（小红书标准竖版比例）
  - 尺寸：1080x1920 px
  - 比例：9:16（小红书最佳展示比例）
  - 直接按原尺寸生成，不做缩放或裁剪
- **内容对应**：图片内容需要概括文章的核心要点
- **风格要求**：
  - **重要**：每张图片根据内容各自设计，不要所有图片风格都一样
  - 可以使用不同的布局、配色、字体组合
  - 减少AI感，追求自然、真实的视觉效果
  - 配色自然和谐，不要过于饱和
  - 可参考 Newsprint 报纸风格，但不限于此风格
- **文字**：
  - 图片中如需文字，**必须使用中文**
  - 字体清晰易读，**绝对不允许出现乱码**
  - 使用高清渲染确保文字显示清晰
- **安全**：使用合规、保险的元素，避免敏感内容

#### 配图类型规划

只生成 **1张主图**，不再需要多张裁剪：

| 图片序号 | 文件名 | 图片类型 | 内容说明 |
|---------|--------|---------|---------|
| 第1张 | cover.png | 主图 | 9:16 竖版主图，包含标题和核心内容，吸引点击 |

**注意**：
- 只生成一张 9:16 的高清主图即可
- 图片尺寸：1080x1920 px（直接生成，不做缩放）
- 图片风格根据内容自行设计，可以多样化
- 确保文字清晰，无乱码
- 在 HTML 设计时，卡片尺寸直接设置为 1080x1920px

#### 设计系统参考

**重要**：图片风格不需要统一，可以根据内容各自设计。

**可选设计风格**：
1. **Newsprint 报纸风格**（参考 [assets/image-templates.html](assets/image-templates.html)）
   - 致敬印刷报纸的黄金时代
   - 高对比度排版、网格布局
   - 适合严肃、专业的内容

2. **现代简约风格**
   - 大量留白，简洁排版
   - 柔和配色，圆角设计
   - 适合轻松、友好的内容

3. **杂志封面风格**
   - 大标题，醒目视觉
   - 多彩配色，吸引眼球
   - 适合推荐、盘点类内容

4. **卡片堆叠风格**
   - 多层卡片，信息丰富
   - 清晰层次，易于阅读
   - 适合教程、步骤类内容

**设计原则**（所有风格通用）：
- 文字必须清晰，使用中文，绝对不允许乱码
- 内容丰富但不拥挤，留有呼吸空间
- 配色自然和谐，符合主题
- 突出核心信息，次要信息可适当弱化

**Design Tokens（设计变量）**：
```css
--background: #F9F9F7;  /* 报纸米白色 */
--foreground: #111111;  /* 墨黑色 */
--muted: #E5E5E0;       /* 分隔灰 */
--accent: #CC0000;      /* 编辑红（仅用于强调） */
```

**字体系统**：
- **标题**：`Noto Serif SC`（中文衬线，粗体，大字号）
- **正文**：`Noto Sans SC`（中文无衬线）
- **UI/标签**：`Inter`（英文无衬线，大写，字母间距加宽）
- **数据/日期**：`JetBrains Mono`（等宽字体）

**核心设计规则**：
1. **零圆角**：所有元素必须使用 `border-radius: 0`
2. **高对比度**：黑白为主，红色仅作点缀
3. **可见网格**：使用边框分隔，模拟报纸栏目
4. **大写标签**：`text-transform: uppercase; letter-spacing: 0.15em`
5. **点状背景纹理**：模拟报纸印刷效果
6. **悬停效果**：颜色反转（黑变白，白变黑）
7. **灰度图片**：图片默认灰度处理

#### HTML 转 PNG 的执行步骤

**步骤 1**：创建临时 HTML 文件
```bash
# 创建临时目录
mkdir -p ./redbook-article/[主题]-[日期]/temp/

# 使用 Write 工具生成 HTML 文件
# 文件: ./redbook-article/[主题]-[日期]/temp/cover.html
```

**步骤 2**：使用 Python 脚本转换为 PNG
```bash
python3 /Users/a58/.claude/skills/redbook-creator-publish/scripts/html_to_image.py \
  ./redbook-article/[主题]-[日期]/temp/ \
  --output ./redbook-article/[主题]-[日期]/images/
```

**步骤 3**：清理临时文件
```bash
rm -rf ./redbook-article/[主题]-[日期]/temp/
```

**输出日志示例**：
```
🎨 生成配图...

📝 创建临时 HTML 模板...
  ✅ cover.html
  ✅ content-1.html
  ✅ content-2.html
  ✅ summary.html

🖼️  转换为 PNG 图片...
使用 Chrome: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

转换: cover.html -> cover.png ... ✅
转换: content-1.html -> content-1.png ... ✅
转换: content-2.html -> content-2.png ... ✅
转换: summary.html -> summary.png ... ✅

完成: 4/4 个文件转换成功

🗑️  清理临时文件...
✅ 配图生成完成！
```

### 第四步：生成本地文件

在用户当前工作目录下创建完整的文件结构：

#### 目录结构

```
redbook-article/
└── [帖子主题]-[YYYY-MM-DD]/
    ├── [帖子主题]-[YYYY-MM-DD].html      # 预览文件（显示图片）
    ├── [帖子主题]-[YYYY-MM-DD].md        # Markdown格式（显示图片+路径）
    ├── [帖子主题]-[YYYY-MM-DD].txt       # 纯文本原始内容
    ├── images/
    │   ├── cover.png                      # 封面图
    │   ├── content-1.png                  # 内容图1
    │   ├── content-2.png                  # 内容图2
    │   ├── summary.png                    # 总结图
    │   └── ...
    ├── config.json                        # 帖子配置信息
    └── publish_config_temp.json           # 发布配置（临时）
```

#### 文件内容说明

**1. HTML 预览文件**（必须显示图片）：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>[标题]</title>
  <style>
    /* Newsprint 风格 CSS */
  </style>
</head>
<body>
  <div class="preview-container">
    <h1>[标题]</h1>

    <!-- 显示配图 -->
    <div class="images-grid">
      <img src="images/cover.png" alt="封面图">
      <img src="images/content-1.png" alt="内容图1">
      <!-- ... 更多图片 -->
    </div>

    <div class="content">
      [正文内容]
    </div>

    <div class="tags">
      [标签]
    </div>
  </div>
</body>
</html>
```

**2. Markdown 文件**（.md）（必须显示图片+路径）：
```markdown
# [标题]

## 配图预览

![封面图](images/cover.png)

![内容图1](images/content-1.png)

![内容图2](images/content-2.png)

![总结图](images/summary.png)

## 正文

[完整正文内容，保留格式]

## 标签

[所有标签]

---

## 配图路径列表

便于在其他 Markdown 工具中查看：

- 封面图：`images/cover.png`
- 内容图1：`images/content-1.png`
- 内容图2：`images/content-2.png`
- 总结图：`images/summary.png`

---

*生成时间：[YYYY-MM-DD HH:mm:ss]*
*字数统计：[字数] 字*
```

**3. 纯文本文件**（.txt）：
```
[标题]

[正文内容，纯文本格式，可直接复制]

[标签，空格分隔]
```

**4. 配置文件**（config.json）：
```json
{
  "title": "帖子标题",
  "content": "正文内容",
  "tags": ["标签1", "标签2", "标签3"],
  "images": [
    "images/cover.png",
    "images/content-1.png",
    "images/content-2.png",
    "images/summary.png"
  ],
  "created_at": "2026-01-26T12:00:00",
  "word_count": 450,
  "search_keywords": ["关键词1", "关键词2"],
  "sources": ["来源1", "来源2"]
}
```

**执行命令**：
```bash
# 创建目录结构
mkdir -p ./redbook-article/[帖子主题]-[日期]/images

# 生成各个文件（使用Write工具）
```

**完成后告知用户**：
```
✅ 文件已生成！

📁 保存位置：./redbook-article/[帖子主题]-[日期]/

包含以下文件：
├── [帖子主题]-[日期].html    # 预览文件（可在浏览器中打开查看）
├── [帖子主题]-[日期].md      # Markdown文章（显示图片）
├── [帖子主题]-[日期].txt     # 纯文本（可直接复制粘贴）
├── images/                    # 配图文件夹（PNG格式）
│   ├── cover.png             # 封面图 ⭐
│   ├── content-1.png         # 内容图1
│   ├── content-2.png         # 内容图2
│   └── summary.png           # 总结图
└── config.json               # 配置信息

💡 提示：
- 在浏览器中打开 .html 文件可预览完整效果
- 在 Markdown 编辑器中打开 .md 文件可查看图文内容
- images/ 文件夹中的图片可以直接上传到小红书
```

### 第五步：浏览器自动化上传

**重要**：默认执行自动上传，无需询问用户。只有自动上传失败时才提示手动上传。

#### 5.1 检查并安装 Playwright

首先检查 Playwright 是否已安装：

```bash
python3 -c "import playwright" 2>/dev/null && echo "Playwright installed" || echo "Playwright not found"
```

**如果未安装**：
```
🔍 检测到 Playwright 未安装，正在自动安装...

Playwright 是现代化的浏览器自动化工具，用于自动上传内容到小红书。
安装过程约需 1-2 分钟...
```

自动执行安装：
```bash
pip3 install playwright
playwright install chromium
```

显示安装进度和结果：
```
⏳ 正在安装 Playwright...
⏳ 正在下载 Chromium 浏览器...
✅ Playwright 安装完成！
```

**如果已安装**：
```
✅ Playwright 已安装，跳过安装步骤
```

#### 5.2 前置提示

**必须显示的重要提示**：
```
==========================================================
  🚀 准备自动上传到小红书
==========================================================

⚠️  重要提示：
   1. 首次使用需要在浏览器中登录小红书账号
      （浏览器会自动打开，请完成登录）

   2. 网络连接正常

   3. 上传过程中请勿操作浏览器
      （预计耗时：30-60秒）

即将开始自动上传...
```

**不需要等待用户确认**，直接开始上传流程。

#### 5.3 执行自动上传

使用 Playwright Python 脚本执行上传：

```bash
python3 /Users/a58/.claude/skills/redbook-creator-publish/scripts/auto_upload_playwright.py \
  --config ./redbook-article/[主题]-[日期]/config.json
```

**脚本参数说明**：
- `--config` 或 `-c`：配置文件路径（必需）
- `--headless`：使用无头模式（可选，默认显示浏览器窗口）

#### 上传流程步骤

Playwright 脚本会自动执行以下步骤，每步都会输出日志：

**步骤 1：打开小红书创作者平台**

脚本会：
1. 使用 Playwright 启动 Chromium 浏览器
2. 打开小红书创作者平台上传页面
3. 检查登录状态，如果未登录会等待用户登录

**输出日志**：
```
🌐 步骤 1/5: 打开小红书创作者平台
   URL: https://creator.xiaohongshu.com/publish/publish?from=menu&target=image
   ✅ 页面加载成功
```

或者（如果未登录）：
```
🌐 步骤 1/5: 打开小红书创作者平台
   URL: https://creator.xiaohongshu.com/publish/publish?from=menu&target=image
   ⚠️  检测到未登录，请先登录...
   等待登录完成...
   ✅ 登录成功
   ✅ 页面加载成功
```

**步骤 2：上传图片**

脚本会：
1. 定位文件上传输入框
2. 一次性上传所有图片（封面图必须是第一张）
3. 等待图片上传完成

**输出日志**：
```
📸 步骤 2/5: 上传图片
   DOM选择器: input[type="file"][accept*="image"]
   图片数量: 4 张
   封面图: cover.png (第一张)

   上传中...
   ✅ cover.png 上传成功
   ✅ content-1.png 上传成功
   ✅ content-2.png 上传成功
   ✅ summary.png 上传成功

   ✅ 所有图片上传完成
```

**步骤 3：填写标题**

脚本会：
1. 定位标题输入框
2. 清空并填写标题内容
3. 模拟真实输入（带延迟）

**输出日志**：
```
✍️  步骤 3/5: 填写标题
   DOM选择器: .c-input_inner input[type="text"]
   标题内容: 🔥 3个AI工具让效率翻倍
   ✅ 标题填写完成
```

**步骤 4：填写正文**

脚本会：
1. 定位正文编辑器
2. 填写正文内容和标签
3. 模拟真实输入（逐段输入）

**输出日志**：
```
📝 步骤 4/5: 填写正文
   DOM选择器: .ql-editor
   正文字数: 387 字
   ✅ 正文填写完成
```

**步骤 5：点击发布**

脚本会：
1. 定位发布按钮
2. 点击发布
3. 等待发布完成

**输出日志**：
```
🚀 步骤 5/5: 点击发布
   DOM选择器: .css-k405vo
   ✅ 已点击发布按钮

   ⏳ 等待发布完成...
   ✅ 发布成功！
```

#### 完整上传日志示例

```
==========================================================
  🚀 小红书自动上传
==========================================================

⚠️  重要提示：
   1. 首次使用需要在浏览器中登录小红书账号
   2. 上传过程中请勿操作浏览器
   3. 预计耗时：30-60秒

即将开始自动上传...

🌐 步骤 1/5: 打开小红书创作者平台
   URL: https://creator.xiaohongshu.com/publish/publish?from=menu&target=image
   ✅ 页面加载成功

📸 步骤 2/5: 上传图片
   DOM选择器: input[type="file"][accept*="image"]
   图片数量: 4 张
   封面图: cover.png (第一张)

   上传中...
   ✅ cover.png 上传成功
   ✅ content-1.png 上传成功
   ✅ content-2.png 上传成功
   ✅ summary.png 上传成功

   ✅ 所有图片上传完成

✍️  步骤 3/5: 填写标题
   DOM选择器: .c-input_inner input[type="text"]
   标题内容: 🔥 3个AI工具让效率翻倍
   ✅ 标题填写完成

📝 步骤 4/5: 填写正文
   DOM选择器: .ql-editor
   正文字数: 387 字
   ✅ 正文填写完成

🚀 步骤 5/5: 点击发布
   DOM选择器: .css-k405vo
   ✅ 已点击发布按钮

   ⏳ 等待发布完成...
   ✅ 发布成功！

==========================================================
  🎉 上传完成！
==========================================================

帖子已成功发布到小红书创作者平台

🔗 查看帖子：
   请在小红书创作者平台查看发布结果
   https://creator.xiaohongshu.com/

💡 提示：
   - 发布后可能需要平台审核
   - 审核通过后会在小红书APP中显示

浏览器将在 5 秒后关闭...
```

#### 错误处理

每个步骤都有错误处理，如果失败则输出详细错误信息：

**示例 1：DOM 元素未找到**
```
❌ 步骤 2/5 失败: 上传图片
   错误: 未找到上传控件

   可能原因:
   1. 小红书平台更新了页面结构
   2. DOM选择器配置不正确

   解决方案:
   1. 在浏览器中打开 https://creator.xiaohongshu.com/publish/publish
   2. 按 F12 打开开发者工具
   3. 找到上传控件的新选择器
   4. 通过环境变量 UPLOAD_INPUT_SELECTOR 更新选择器

   当前选择器: input[type="file"][accept*="image"]
```

**示例 2：上传超时**
```
❌ 步骤 2/5 失败: 上传图片
   错误: 上传超时

   可能原因:
   1. 网络连接不稳定
   2. 图片文件过大
   3. 小红书服务器响应慢

   解决方案:
   1. 检查网络连接
   2. 稍后重试
   3. 或使用手动上传方式
```

#### DOM 选择器配置

可以通过环境变量自定义 DOM 选择器（当小红书平台更新页面结构时）：

```bash
# 在运行脚本前设置环境变量
export UPLOAD_INPUT_SELECTOR='input[type="file"][accept*="image"]'
export TITLE_INPUT_SELECTOR='.c-input_inner input[type="text"]'
export CONTENT_CONTAINER_SELECTOR='.ql-editor'
export PUBLISH_BUTTON_SELECTOR='.css-k405vo'
export IMAGE_ITEM_SELECTOR='.upload-list-item'

# 然后运行上传脚本
python3 auto_upload_playwright.py --config config.json
```

或者在 Python 脚本调用前设置：

```python
import os
os.environ['UPLOAD_INPUT_SELECTOR'] = 'input[type="file"]'
# 然后调用脚本
```

#### 5.4 自动上传失败后的处理

**重要**：只有当自动上传失败时，才显示以下手动上传指引。

检测到以下任一错误时，判定为自动上传失败：
- Playwright 未安装且安装失败
- Python 环境问题
- DOM 元素未找到（平台更新了页面结构）
- 上传超时（网络问题或服务器响应慢）
- 用户登录超时
- 任何导致上传流程中断的错误

**失败时的输出格式**：

```
==========================================================
  ❌ 自动上传失败
==========================================================

失败原因：[具体错误信息]

别担心，内容已经准备好了，请使用手动方式上传：

📋 手动上传步骤：

1️⃣  打开小红书创作者平台
   https://creator.xiaohongshu.com/publish/publish?from=menu&target=image

2️⃣  上传图片（按顺序）
   📂 位置：./redbook-article/[主题]-[日期]/images/

   ⚠️  重要：必须按以下顺序上传（第一张是封面图）：

   1. cover.png          ← 封面图（第一张）
   2. content-1.png      ← 内容图1
   3. content-2.png      ← 内容图2
   4. summary.png        ← 总结图（或其他内容图）

3️⃣  填写标题
   📄 打开：[主题]-[日期].txt
   复制第一行标题，粘贴到小红书标题输入框

4️⃣  填写正文
   📄 从 .txt 文件复制正文内容
   粘贴到小红书正文输入框

5️⃣  添加标签
   📄 从 .txt 文件复制标签行
   粘贴到小红书标签输入框

6️⃣  点击发布
   等待平台审核通过

==========================================================

📂 文件位置：
   ./redbook-article/[主题]-[日期]/

💡 提示：
   - 可以在浏览器中打开 .html 文件预览效果
   - .txt 文件中包含所有需要复制的内容
   - 图片都在 images/ 文件夹中
```

**输出示例**：
```
==========================================================
  ❌ 自动上传失败
==========================================================

失败原因：未检测到小红书登录状态

别担心，内容已经准备好了，请使用手动方式上传：

📋 手动上传步骤：

1️⃣  打开小红书创作者平台
   https://creator.xiaohongshu.com/publish/publish?from=menu&target=image

2️⃣  上传图片（按顺序）
   📂 位置：./redbook-article/AI工具调研-2026-01-26/images/

   ⚠️  重要：必须按以下顺序上传（第一张是封面图）：

   1. cover.png          ← 封面图（第一张）
   2. content-1.png      ← 内容图1
   3. content-2.png      ← 内容图2
   4. summary.png        ← 总结图

3️⃣  填写标题
   📄 打开：AI工具调研-2026-01-26.txt
   复制标题：🔥 2026最火AI工具调研！效率暴涨3倍

4️⃣  填写正文
   📄 从 .txt 文件复制正文内容

5️⃣  添加标签
   📄 复制：#AI工具 #效率提升 #人工智能 ...

6️⃣  点击发布

==========================================================

📂 文件位置：./redbook-article/AI工具调研-2026-01-26/
```

## 完整工作流程示例

```
用户：小红书创作 分享一个提高工作效率的AI工具

AI执行步骤：

✅ 前置检查
   - Python: v3.11.0 ✅
   - Playwright: 已安装 ✅
   - Chrome: 已安装 ✅

🔍 深度搜索话题
   - 搜索关键词 1: "2026最新AI工具推荐"
   - 搜索关键词 2: "AI工具效率提升案例"
   - 搜索关键词 3: "AI工具使用教程"
   - ✅ 已获取充足素材

📝 生成帖子内容
   - 标题: 🔥 3个AI工具让效率翻倍
   - 正文: 450字（基于搜索结果整合）
   - 标签: 8个

🎨 生成配图
   - 创建 HTML 模板 (4个)
   - 转换为 PNG (4个)
   - 清理临时文件
   - ✅ 配图生成完成

📁 生成本地文件
   - .html 预览文件（显示图片）
   - .md Markdown文件（显示图片+路径）
   - .txt 纯文本文件
   - images/ 配图文件夹 (PNG)
   - config.json 配置文件
   - ✅ 文件生成完成

🚀 自动上传到小红书
   - 检查 Playwright: 已安装 ✅
   - 显示上传提示（首次需登录）
   - 步骤 1/5: 打开创作者平台 ✅
   - 步骤 2/5: 上传图片 (4张) ✅
   - 步骤 3/5: 填写标题 ✅
   - 步骤 4/5: 填写正文 ✅
   - 步骤 5/5: 点击发布 ✅
   - ✅ 发布成功！

🎉 任务完成！

---

如果自动上传失败，会显示：

❌ 自动上传失败
   失败原因: [具体错误]

   📋 提供详细的手动上传步骤
   📂 文件位置已准备好
```

## 注意事项

### 内容创作要求
- ✅ 所有生成内容必须原创，基于深度搜索结果整合
- ✅ 正文字数必须在300-500字之间
- ✅ 配图数量必须在3-6张之间，格式为 PNG/JPG
- ✅ 内容需符合小红书社区规范
- ✅ 避免敏感词汇和违规内容
- ✅ 图片文字使用中文，确保无乱码
- ✅ 标签数量建议8-10个，覆盖热门和精准标签
- ✅ 配图风格要自然，使用 Newsprint 风格

### 自动上传流程
- ✅ **默认执行自动上传**，无需询问用户
- ✅ 首次使用会自动安装 Playwright（需要 Python 3.8+ 环境）
- ✅ 首次使用需要在自动打开的浏览器中登录小红书账号
- ✅ Playwright 会记住登录状态，后续使用无需重复登录
- ✅ 封面图必须作为第一张上传
- ✅ 每个自动化步骤都必须输出日志
- ✅ 错误处理要详细，提供解决方案
- ✅ **只有自动上传失败时才提示手动上传**

### 技术配置
- ✅ DOM 选择器支持配置化（通过环境变量）
- ✅ 支持有头/无头模式（默认显示浏览器窗口）
- ✅ 图片转换使用 Chrome headless 模式
- ✅ 自动清理临时文件
- ✅ Playwright 持久化登录状态

## 相关文档

- [README.md](README.md) - 使用说明和安装指南
- [references/style-guide.md](references/style-guide.md) - 小红书内容风格规范
- [assets/image-templates.html](assets/image-templates.html) - Newsprint 设计模板
- [assets/preview-template.html](assets/preview-template.html) - 预览页面模板
- [scripts/html_to_image.py](scripts/html_to_image.py) - HTML 转 PNG 脚本
- [scripts/auto_upload_playwright.py](scripts/auto_upload_playwright.py) - Playwright 自动上传脚本
- [scripts/upload_to_redbook.py](scripts/upload_to_redbook.py) - 手动上传辅助脚本

## Playwright 参考资料

- 官方网站: https://playwright.dev/python/
- 中文文档: https://playwright.dev/python/docs/intro
- GitHub: https://github.com/microsoft/playwright-python
- API 文档: https://playwright.dev/python/docs/api/class-playwright

**基本用法**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 页面导航
    page.goto('https://example.com')

    # 元素选择和操作
    page.locator('.button').click()
    page.locator('input').fill('text')

    # 文件上传
    page.locator('input[type="file"]').set_input_files(['file.png'])

    # 等待元素
    page.wait_for_selector('.element')

    # 截图
    page.screenshot(path='screenshot.png')

    browser.close()
```
