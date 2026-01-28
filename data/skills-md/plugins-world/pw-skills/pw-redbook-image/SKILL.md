---
name: pw-redbook-image
description: 将文章内容拆解为小红书风格的系列配图。支持从 URL、文件或文本生成封面图、内容图和结尾图，自动创建提示词并调用图片生成工具。
---

# 小红书风格图片生成

将文章内容智能拆解为小红书风格的系列配图，包含封面图、内容图和结尾图。

## 核心功能

- 智能拆解文章为多张配图 (2-10 张)
- 自动生成符合小红书风格的图片提示词
- 支持多种输入源 (URL、文件路径、文本内容)
- 自动创建结构化的工作目录
- 支持后处理 (合并长图、PPT、PDF)

## 使用时机

用户明确要求生成小红书风格配图时:
- "生成小红书配图"
- "制作小红书系列图"
- "将这篇文章做成小红书图片"
- "帮我做小红书风格的图文"

不适用场景:
- 用户只是询问如何制作 (提供建议即可)
- 用户需要单张封面图 (使用 pw-cover-image)
- 用户需要其他风格的图片 (使用通用图片生成工具)

## 使用方法

```bash
# 从 URL 生成
/pw-redbook-image https://example.com/article

# 从文本内容生成
/pw-redbook-image "文章内容..."

# 从 markdown 文件生成
/pw-redbook-image path/to/article.md
```

## 参数说明

- **输入源** (必需): 支持三种格式
  - URL: 以 http:// 或 https:// 开头的网址
  - 文件路径: 相对或绝对路径，支持 .md、.txt 等文本文件
  - 文本内容: 直接传入的文章内容字符串

## 小红书风格特征

- **比例**: 竖版（3:4 或 9:16）
- **风格**: 卡通风格、手绘风格
- **配色**: 莫兰迪色系、奶油色、米白色、浅粉、薄荷绿
- **文字**: 手绘风格文字，大标题突出，荧光笔划线强调
- **装饰**: 卡通元素、emoji 图标、手绘贴纸、对话气泡
- **排版**: 信息精简，多留白，要点分条呈现

## 内容拆解原则

- **封面图**: 强烈视觉冲击力，包含核心标题
- **内容图**: 每张聚焦 1 个核心观点
- **结尾图**: 总结/行动号召/金句

**图片数量**:
- 简单观点: 2-3 张
- 中等复杂度: 4-6 张
- 深度干货: 7-10 张

## 文件管理

### 输出目录

每个会话创建一个以主题命名的独立目录:

```
redbook-{topic-slug}/
├── source.md              # 源文章
├── prompts/               # 提示词文件
│   ├── 01_封面图.md
│   ├── 02_内容图_核心观点1.md
│   ├── 03_内容图_核心观点2.md
│   └── 04_结尾图.md
└── images/                # 生成的图片
    ├── 01_封面图.png
    ├── 02_内容图_核心观点1.png
    ├── 03_内容图_核心观点2.png
    └── 04_结尾图.png
```

**主题命名规则**:
1. 从文章标题/内容中提取主题（2-4 个词，kebab-case）
2. 示例: "如何提升工作效率" → `improve-work-efficiency`

### 冲突解决

如果 `redbook-{topic-slug}/` 已存在:
- 追加时间戳: `{topic-slug}-YYYYMMDD-HHMMSS`
- 示例: `improve-work-efficiency` 已存在 → `improve-work-efficiency-20260123-143052`

### 源文件

使用 `source.md` 或 `source-{原文件名}` 保存源文章。

## 工作流程

### 步骤 1: 获取文章内容

处理输入源:
- URL: 使用 WebFetch 抓取网页内容
- 文件路径: 使用 Read 读取文件内容
- 文本: 直接使用传入的内容

保存源内容:
- 创建工作目录 `redbook-{topic-slug}/`
- 保存源文件到 `source.md` 或 `source-{原文件名}`

### 步骤 2: 分析和拆解文章

使用 `${SKILL_DIR}/references/文章拆解模板.md` 分析文章:
- 提取主题和核心观点
- 确定图片数量 (2-10 张)
- 生成拆解方案，明确每张图的核心内容

图片数量建议:
- 简单观点: 2-3 张
- 中等复杂度: 4-6 张
- 深度干货: 7-10 张

### 步骤 3: 生成提示词文件

创建 `redbook-{topic-slug}/prompts/` 目录，根据图片类型选择模板:
- 封面图: `${SKILL_DIR}/references/封面图模板.md`
- 内容图: `${SKILL_DIR}/references/内容图模板.md`
- 结尾图: `${SKILL_DIR}/references/结尾图模板.md`

为每张图生成独立的提示词文件:
- 命名格式: `01_封面图.md`, `02_内容图_关键词.md`, `03_结尾图.md`
- 提示词使用英文，避免 Markdown 格式
- 包含风格关键词和配色方案

### 步骤 4: 生成图片

检查可用的图片生成技能:
- 优先使用 pw-danger-gemini-web
- 如有多个技能可用，询问用户选择

逐张生成图片:
- 输出目录: `redbook-{topic-slug}/images/`
- 显示生成进度
- 图片按序号排序
- 第一张图生成后，确认风格再继续批量生成

### 步骤 5: 后处理 (可选)

合并长图 (需要 ImageMagick):
```bash
brew install imagemagick
node ~/.claude/skills/pw-image-generation/scripts/merge-to-long-image.js \
  redbook-{topic-slug}/images \
  redbook-{topic-slug}/长图.png
```

合并为 PPT:
```bash
node ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.js \
  redbook-{topic-slug}/images \
  redbook-{topic-slug}/配图.pptx
```

合并为 PDF:
```bash
node ~/.claude/skills/pw-image-generation/scripts/merge-to-pdf.js \
  redbook-{topic-slug}/images \
  redbook-{topic-slug}/配图.pdf
```

### 步骤 6: 输出摘要

生成完成后输出:
```
小红书系列图已生成!

主题: [主题]
图片数量: [数量] 张
工作目录: redbook-{topic-slug}/

后续步骤:
- 预览所有图片确认风格一致性
- 如需要可使用合并工具生成长图、PPT 或 PDF
```

## 最佳实践

风格一致性:
- 第一张图生成后确认风格，再批量生成其余图片
- 所有图片使用相同的风格关键词和配色方案
- 作者信息统一放在右下角，格式保持一致

内容设计:
- 每张图聚焦一个核心观点，不要放太多内容
- 多留白，提高可读性
- 标题要大而突出，关键词用荧光笔划线强调

提示词优化:
- 使用英文提示词，效果更好
- 避免 Markdown 格式，使用纯文本描述
- 明确指定比例 (3:4 或 9:16)、风格 (卡通/手绘)、配色 (莫兰迪色系)

## 常见问题

问题: 生成的图片风格不一致
解决: 在提示词中明确指定相同的风格关键词，如 "cartoon style, hand-drawn, pastel colors"

问题: 图片内容太多，不够简洁
解决: 减少每张图的文字量，拆分为更多张图片，每张聚焦一个观点

问题: URL 抓取失败
解决: 检查网址是否可访问，或直接复制文章内容作为文本输入

问题: 目录已存在
解决: 自动追加时间戳，如 `improve-work-efficiency-20260123-143052`

问题: 图片生成失败
解决: 检查图片生成技能是否可用，确认 API 配置正确

## 模板参考

| 模板文件 | 用途 | 位置 |
|------|------|------|
| 文章拆解模板.md | 将文章拆解为系列图的分析模板 | `${SKILL_DIR}/references/` |
| 封面图模板.md | 封面图提示词生成模板 | `${SKILL_DIR}/references/` |
| 内容图模板.md | 内容图提示词生成模板 | `${SKILL_DIR}/references/` |
| 结尾图模板.md | 结尾图提示词生成模板 | `${SKILL_DIR}/references/` |

## 扩展配置

通过 EXTEND.md 支持自定义配置，检查路径 (优先级顺序):
1. `.pw-skills/pw-redbook-image/EXTEND.md` (项目级)
2. `~/.pw-skills/pw-redbook-image/EXTEND.md` (用户级)

如果找到，在工作流程之前加载。扩展内容会覆盖默认值。

可自定义内容:
- 默认图片数量范围
- 风格关键词和配色方案
- 作者信息格式
- 输出目录命名规则
