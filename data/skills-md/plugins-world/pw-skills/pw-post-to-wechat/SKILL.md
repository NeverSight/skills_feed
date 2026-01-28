---
name: pw-post-to-wechat
description: |
  发布内容到微信公众号的自动化工具。

  核心功能:
  - 图文发表: 多图配文模式, 支持最多 9 张图片
  - 文章发表: 完整 Markdown 格式化, 保留样式和排版
  - 自动化流程: 使用 Chrome CDP 自动登录、填充、发布
  - 智能压缩: 标题和内容超限时自动压缩
  - 主题支持: 文章发表支持 default、grace、simple 三种主题

  使用时机:
  - 用户明确要求 "发布到微信公众号"、"发送到公众号"
  - 用户提供 markdown 文件或内容需要发布
  - 用户需要批量发布图文内容

  不适用场景:
  - 用户只是询问如何发布 (提供建议即可)
  - 用户需要编辑现有公众号文章 (手动操作)
  - 用户需要发布到其他平台 (使用对应平台工具)
---

# 微信公众号发布工具

自动化发布内容到微信公众号, 支持图文和文章两种模式。

## 使用方法

### 图文发表 (多图配文)

```bash
# 从 markdown 文件和图片目录生成
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./images/

# 使用明确的参数
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --title "标题" --content "内容" --image img1.png --image img2.png --submit

# 仅预览不保存
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./images/
```

### 文章发表 (完整 Markdown)

```bash
# 发布 markdown 文章 (默认主题)
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md

# 指定主题
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --theme grace
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --theme simple

# 覆盖标题和作者
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --title "自定义标题" --author "作者名"
```

**说明**: `${SKILL_DIR}` 代表本技能的安装目录, Agent 会在运行时替换为实际路径。

## 参数说明

### 图文发表参数

#### --markdown <path>

指定 Markdown 文件路径, 自动提取标题和内容。

**参数类型**: 文件路径 (可选)

**功能说明**:
- 解析 frontmatter 获取标题和作者
- 如果没有 frontmatter, 使用第一个 H1 标题
- 提取首段作为内容 (最多 1000 字)
- 标题超过 20 字时自动压缩

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown ./article.md --images ./pics/
```

**Markdown 格式**:
```markdown
---
title: 文章标题
author: 作者名
---

# 这是标题 (如果没有 frontmatter)

这是首段内容, 会被提取为图文内容...
```

**最佳实践**:
- 使用 frontmatter 明确指定标题和作者
- 首段内容应简洁有力, 吸引读者
- 标题控制在 20 字以内避免压缩

#### --images <dir>

指定图片目录, 上传目录中所有图片。

**参数类型**: 目录路径 (可选)

**功能说明**:
- 上传目录中所有 PNG/JPG 文件
- 按文件名字母顺序排序
- 最多支持 9 张图片 (微信限制)

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./images/
```

**最佳实践**:
- 使用数字前缀命名: `01-cover.png`, `02-content.png`
- 确保图片清晰度适合移动端查看
- 控制图片数量在 9 张以内

#### --title <text>

直接指定文章标题。

**参数类型**: 字符串 (可选)

**限制**: 最多 20 字, 超出自动压缩

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --title "如何提升效率" --content "内容..." --image cover.png
```

**压缩规则**:
- 原始: "如何在一天内彻底重塑你的人生"
- 压缩: "一天内重塑你的人生"

**最佳实践**:
- 标题简洁有力, 突出核心价值
- 避免冗余词汇 (如何、怎样等)
- 使用数字和动词增强吸引力

#### --content <text>

直接指定文章内容。

**参数类型**: 字符串 (可选)

**限制**: 最多 1000 字, 超出自动压缩

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --title "标题" --content "这是内容..." --image img.png
```

**最佳实践**:
- 内容应简洁明了, 引导用户点击查看
- 突出文章核心价值和亮点
- 控制在 1000 字以内避免压缩

#### --image <path>

指定单个图片文件, 可重复使用添加多张图片。

**参数类型**: 文件路径 (可选, 可重复)

**限制**: 最多 9 张图片

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --title "标题" --content "内容" --image img1.png --image img2.png --image img3.png
```

**最佳实践**:
- 第一张图片作为封面, 应最具吸引力
- 图片顺序影响展示效果
- 确保图片格式为 PNG 或 JPG

#### --submit

保存为草稿, 默认仅预览不保存。

**参数类型**: 布尔标志 (可选)

**默认行为**: 不保存, 仅预览

**使用场景**:
- 确认内容无误后再添加此参数保存
- 批量发布时使用

**使用示例**:
```bash
# 仅预览
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./pics/

# 保存为草稿
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./pics/ --submit
```

**注意事项**:
- 保存后需要在微信公众号后台手动发布
- 建议先预览确认无误再保存

#### --profile <dir>

指定 Chrome 配置文件目录, 保持登录状态。

**参数类型**: 目录路径 (可选)

**默认行为**: 使用临时配置文件

**使用场景**:
- 避免每次都需要扫码登录
- 多账号管理

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./pics/ --profile ~/.chrome-wechat
```

**最佳实践**:
- 为不同公众号账号创建不同的配置文件目录
- 定期清理配置文件避免占用过多空间

### 文章发表参数

#### --markdown <path>

指定要转换和发布的 Markdown 文件。

**参数类型**: 文件路径 (必需)

**功能说明**:
- 完整解析 Markdown 格式
- 保留标题、列表、引用、代码块等样式
- 自动处理图片占位符和替换

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md
```

**支持的 Markdown 语法**:
- 标题: `#`, `##`, `###`
- 粗体: `**text**`
- 斜体: `*text*`
- 列表: `-`, `1.`
- 引用: `>`
- 代码块: ` ``` `
- 链接: `[text](url)`
- 图片: `![alt](path)`

**最佳实践**:
- 使用标准 Markdown 语法
- 图片使用相对路径
- 避免使用过于复杂的嵌套结构

#### --theme <name>

指定文章主题样式。

**参数类型**: 字符串 (可选)

**可选值**:
- `default` - 默认主题, 简洁大方
- `grace` - 优雅主题, 适合正式内容
- `simple` - 极简主题, 突出内容本身

**默认值**: default

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --theme grace
```

**主题特点**:

| 主题 | 适用场景 | 特点 |
|------|----------|------|
| default | 通用内容 | 平衡美观和可读性 |
| grace | 正式文章、专业内容 | 优雅排版, 强调层次 |
| simple | 技术文档、教程 | 极简风格, 突出内容 |

**最佳实践**:
- 技术文章推荐 simple
- 品牌内容推荐 grace
- 日常内容使用 default

#### --title <text>

覆盖从 Markdown 提取的标题。

**参数类型**: 字符串 (可选)

**默认行为**: 从 Markdown frontmatter 或 H1 提取

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --title "自定义标题"
```

**使用场景**:
- Markdown 文件没有标题
- 需要使用不同于文件中的标题
- 针对不同平台使用不同标题

#### --author <name>

指定文章作者名。

**参数类型**: 字符串 (可选)

**默认值**: 宝玉

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --author "张三"
```

**最佳实践**:
- 使用真实作者名增强可信度
- 团队账号可使用团队名称

#### --summary <text>

指定文章摘要。

**参数类型**: 字符串 (可选)

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --summary "这是一篇关于..."
```

**最佳实践**:
- 摘要应简洁明了, 概括文章核心
- 控制在 100 字以内
- 突出文章价值和亮点

#### --html <path>

使用预渲染的 HTML 文件替代 Markdown。

**参数类型**: 文件路径 (可选)

**使用场景**:
- 已有渲染好的 HTML 内容
- 需要使用自定义样式
- 复杂排版需求

**使用示例**:
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --html article.html
```

**注意事项**:
- HTML 需要符合微信公众号编辑器要求
- 图片仍需使用占位符处理

#### --profile <dir>

指定 Chrome 配置文件目录。

**参数类型**: 目录路径 (可选)

**功能**: 与图文发表的 --profile 参数相同

## 功能对比

| 功能 | 图文发表 | 文章发表 |
|------|----------|----------|
| 多图支持 | 支持 (最多 9 张) | 支持 (内联图片) |
| Markdown 支持 | 标题/内容提取 | 完整格式化 |
| 自动标题压缩 | 支持 (压缩到 20 字) | 不支持 |
| 内容压缩 | 支持 (压缩到 1000 字) | 不支持 |
| 主题支持 | 不支持 | 支持 (default, grace, simple) |
| 适用场景 | 快速发布多图内容 | 长文章、技术文档 |

## 工作流程

### 图文发表流程

1. **解析内容**:
   - 从 Markdown 文件提取标题和内容
   - 或使用 --title 和 --content 直接指定

2. **处理图片**:
   - 从 --images 目录读取所有图片
   - 或使用多个 --image 参数指定图片
   - 按文件名排序

3. **自动化发布**:
   - 打开 Chrome 浏览器
   - 导航到微信公众号图文编辑器
   - 上传所有图片
   - 填充标题和内容
   - 根据 --submit 参数决定是否保存

4. **输出结果**:
   - 报告发布状态
   - 显示图片数量
   - 提示后续操作

### 文章发表流程

1. **解析 Markdown**:
   - 读取 Markdown 文件
   - 提取标题、作者等元数据
   - 识别所有图片引用

2. **生成 HTML**:
   - 将 Markdown 转换为 HTML
   - 应用选定的主题样式
   - 图片替换为占位符 `[[IMAGE_PLACEHOLDER_N]]`

3. **自动化发布**:
   - 打开 Chrome 浏览器
   - 导航到微信公众号文章编辑器
   - 粘贴 HTML 内容到编辑器

4. **替换图片**:
   - 对每个占位符:
     - 查找并选中占位符文本
     - 滚动到可见区域
     - 按 Backspace 删除占位符
     - 从剪贴板粘贴图片

5. **输出结果**:
   - 报告发布状态
   - 显示图片数量
   - 提示后续操作

## 前置要求

- 已安装 Google Chrome
- `bun` 运行时 (通过 `npx -y bun` 自动安装)
- 首次运行需要在打开的浏览器窗口中登录微信公众号

## 常见问题

### 登录相关

**问题**: 每次运行都需要扫码登录

**解决方案**: 使用 --profile 参数指定配置文件目录
```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./pics/ --profile ~/.chrome-wechat
```

**问题**: 登录后立即退出

**解决方案**:
- 检查网络连接
- 确保微信公众号账号状态正常
- 尝试清除配置文件重新登录

### 图片相关

**问题**: 图片上传失败

**解决方案**:
- 检查图片格式 (仅支持 PNG/JPG)
- 检查图片大小 (建议小于 5MB)
- 确保图片路径正确

**问题**: 图片顺序错误

**解决方案**:
- 使用数字前缀命名: `01-`, `02-`, `03-`
- 或使用多个 --image 参数按顺序指定

### 内容相关

**问题**: 标题被压缩

**解决方案**:
- 标题控制在 20 字以内
- 或手动编辑压缩后的标题

**问题**: 内容被压缩

**解决方案**:
- 内容控制在 1000 字以内
- 或使用文章发表模式发布完整内容

### 浏览器相关

**问题**: 找不到 Chrome

**解决方案**: 设置环境变量
```bash
export WECHAT_BROWSER_CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

**问题**: 粘贴失败

**解决方案**:
- 检查系统剪贴板权限
- 确保 Chrome 有权限访问剪贴板
- macOS 需要在系统设置中授予权限

## 脚本参考

所有脚本位于本技能的 `scripts/` 子目录中。

**Agent 执行说明**:
1. 确定此 SKILL.md 文件的目录路径为 `SKILL_DIR`
2. 脚本路径 = `${SKILL_DIR}/scripts/<script-name>.ts`
3. 将文档中所有 `${SKILL_DIR}` 替换为实际路径

**可用脚本**:

| 脚本 | 用途 | 说明 |
|------|------|------|
| `wechat-browser.ts` | 图文发表 | 多图配文模式 |
| `wechat-article.ts` | 文章发表 | 完整 Markdown 格式 |
| `md-to-wechat.ts` | Markdown 转换 | 转换为微信 HTML |
| `copy-to-clipboard.ts` | 剪贴板操作 | 复制内容到剪贴板 |
| `paste-from-clipboard.ts` | 粘贴操作 | 发送真实粘贴按键 |

## 使用示例

### 示例 1: 快速发布图文

```bash
# 场景: 有一篇 markdown 文章和一个图片目录
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown ./article.md --images ./xhs-images/

# 执行流程:
# 1. 解析 markdown 元数据:
#    - 标题: "如何在一天内彻底重塑你的人生" → "一天内重塑你的人生"
#    - 作者: 从 frontmatter 或使用默认值
# 2. 从首段提取内容
# 3. 在 xhs-images/ 中找到 7 张图片
# 4. 打开 Chrome, 导航到微信"图文"编辑器
# 5. 上传所有图片
# 6. 填充标题和内容
# 7. 报告: "图文已发布, 包含 7 张图片。"
```

### 示例 2: 发布完整文章

```bash
# 场景: 发布一篇技术文章, 使用 simple 主题
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown ./tech-article.md --theme simple

# 执行流程:
# 1. 解析 markdown, 找到 5 张图片
# 2. 生成带占位符的 HTML
# 3. 打开 Chrome, 导航到微信编辑器
# 4. 粘贴 HTML 内容
# 5. 对每张图片:
#    - 选中 [[IMAGE_PLACEHOLDER_1]]
#    - 滚动到可见区域
#    - 按 Backspace 删除
#    - 粘贴图片
# 6. 报告: "文章已编排, 包含 5 张图片。"
```

### 示例 3: 批量发布

```bash
# 场景: 批量发布多篇文章
for file in articles/*.md; do
  npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts \
    --markdown "$file" \
    --images "images/$(basename $file .md)/" \
    --submit \
    --profile ~/.chrome-wechat
done
```

### 示例 4: 自定义参数发布

```bash
# 场景: 完全自定义标题、内容和图片
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts \
  --title "2024 年度总结" \
  --content "回顾这一年的成长与收获..." \
  --image cover.png \
  --image chart1.png \
  --image chart2.png \
  --submit
```

## 扩展支持

通过 EXTEND.md 自定义配置。

**检查路径** (优先级顺序):
1. `.pw-skills/pw-post-to-wechat/EXTEND.md` (项目级)
2. `~/.pw-skills/pw-post-to-wechat/EXTEND.md` (用户级)

如果找到, 在工作流之前加载。扩展内容会覆盖默认值。

## 参考文档

- **图文发表**: 查看 `references/image-text-posting.md` 了解详细的图文发表指南
- **文章发表**: 查看 `references/article-posting.md` 了解详细的文章发表指南

## 注意事项

- 图文发表标题最多 20 字, 内容最多 1000 字
- 图片最多 9 张 (微信限制)
- 首次运行需要扫码登录
- 使用 --profile 参数可以保持登录状态
- 建议先预览确认无误再使用 --submit 保存
- 文章发表支持完整 Markdown 格式
- 图片处理需要系统剪贴板权限
- macOS 需要在系统设置中授予 Chrome 剪贴板权限
