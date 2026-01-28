---
name: pw-image-generation
description: AI 图像生成和处理工作流。通过提示词生成图像，支持文生图、图生图、批量生成、图床管理、长图合并、PPT 打包。核心特性是逐张确认生成，避免浪费 API 额度。
---

# Image-Generation - AI 图像生成工作流

> **核心理念**: 分析风格 → 设计提示词 → 用户确认 → 生成图像，避免额度浪费

## 核心功能

**图像生成**:
- 文生图: 根据文本描述生成图像
- 图生图: 基于参考图片生成类似风格的图像
- 批量生成: 使用提示词模板批量生成多张图像
- 风格一致: 保持系列图像的视觉风格统一

**图像处理**:
- 长图合并: 将系列图片垂直拼接为一张长图
- PPT 打包: 将系列图片打包为 PPT 文件 (每张图片一页)
- 图床管理: 上传图片到图床并管理删除链接

## 使用时机

**适用场景**:
- 用户明确要求 "生成图像"、"创建配图"、"制作插画"
- 用户提供文本描述并需要视觉化呈现
- 用户提供参考图片并要求生成类似风格的图像
- 用户需要为文章、PPT、社交媒体制作配图
- 用户需要批量生成风格一致的系列图像
- 用户需要将多张图片合并为长图或 PPT

**不适用场景**:
- 用户只是询问如何生成图像 (提供建议即可)
- 用户需要编辑现有图片 (使用图片编辑工具)
- 用户需要图像识别或分析 (使用视觉分析工具)
- 用户需要截图或屏幕录制 (使用系统工具)

---

## 工作流程

```
分析风格 → 设计提示词 → 安装依赖 → 配置API → 确认生成 → 保存图像
    ↓          ↓           ↓         ↓         ↓         ↓
  风格文件    提示词文件   node-fetch  secrets.md  逐张确认  images/
```

---

## 脚本目录

所有脚本位于 `~/.claude/skills/pw-image-generation/scripts/` 目录中。

**Agent 执行说明**:
1. 确定此 SKILL.md 文件的目录路径为 `SKILL_DIR`
2. 脚本路径 = `${SKILL_DIR}/scripts/<script-name>.ts`
3. 将本文档中的所有 `${SKILL_DIR}` 替换为实际路径

**可用脚本**:
| 脚本 | 功能 | 参数 |
|------|------|------|
| `generate-image.ts` | 生成图像 (逐张确认) | `[输出目录]` |
| `upload-image.ts` | 上传图片到图床 | `<图片路径>` |
| `delete-image.ts` | 管理图床图片 | `list\|delete <索引>\|delete-all` |
| `merge-to-long-image.ts` | 合并为长图 | `<图片目录> <输出文件>` |
| `merge-to-pptx.ts` | 打包为 PPT | `<图片目录> <输出文件>` |
| `analyze-image.ts` | 分析图像风格 | `<图像URL或路径>` |

## 快速开始

### Step 1: 创建项目目录

```bash
mkdir my-image-project && cd my-image-project
```

### Step 2: 复制配置模板（可选）

```bash
cp -r ~/.claude/skills/pw-image-generation/config.example ./config
cp ~/.claude/skills/pw-image-generation/references/.gitignore.template ./.gitignore
# 编辑 config/secrets.md 自定义 API 密钥（可选）
```

### Step 3: 创建提示词

```bash
mkdir -p prompts
cp ~/.claude/skills/pw-image-generation/references/prompt-templates/提示词模板.md ./prompts/我的提示词.md
vim ./prompts/我的提示词.md
```

参考 `references/style-library.md` 选择合适的风格。

### Step 4: 生成图像

```bash
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts
```

脚本会逐张询问确认，避免浪费额度。

---

## 工具脚本详解

### 1. 生成图像

**命令**:
```bash
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts [输出目录]
```

**参数说明**:
- `[输出目录]`: 可选，指定图像保存目录，默认为 `./images`

**工作流程**:
1. 读取 `prompts/` 目录下的所有提示词文件
2. 逐张显示提示词内容
3. 询问是否生成该图像 (y/n/q)
4. 生成图像并保存到输出目录
5. 支持中断和恢复

**确认选项**:
- `y` (yes): 生成当前图像
- `n` (no): 跳过当前图像，继续下一张
- `q` (quit): 退出生成流程

**示例**:
```bash
# 使用默认输出目录
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts

# 指定输出目录
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts ./my-images
```

---

### 2. 上传图片到图床

**命令**:
```bash
npx -y bun ~/.claude/skills/pw-image-generation/scripts/upload-image.ts <图片路径>
```

**参数说明**:
- `<图片路径>`: 必需，要上传的本地图片文件路径

**功能特性**:
- 自动上传到 freeimage.host (永久存储)
- 返回可用的图片 URL
- 自动保存删除链接到 `.upload-history.json`
- 用于图生图的参考图上传

**示例**:
```bash
# 上传单张图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/upload-image.ts ./template/参考图.png

# 上传后会返回:
# - 图片 URL (用于提示词中的 image_url)
# - 删除链接 (保存在历史记录中)
```

**输出示例**:
```
上传成功!
图片 URL: https://iili.io/xxx.png
删除链接已保存到 .upload-history.json
```

---

### 3. 管理图床图片

**命令**:
```bash
# 列出所有上传的图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts list

# 删除指定索引的图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts delete <索引>

# 删除所有图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts delete-all
```

**参数说明**:
- `list`: 列出所有上传记录
- `delete <索引>`: 删除指定索引的图片 (索引从 0 开始)
- `delete-all`: 删除所有图片

**功能特性**:
- 查看上传历史和删除链接
- 单个或批量删除图片
- 自动更新历史记录文件

**示例**:
```bash
# 查看上传历史
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts list
# 输出:
# 0: 参考图.png - https://iili.io/xxx.png (2024-01-15)
# 1: 配图1.png - https://iili.io/yyy.png (2024-01-16)

# 删除索引为 0 的图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts delete 0

# 删除所有图片 (会要求确认)
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts delete-all
```

详细说明见 `references/图床上传.md`

---

### 4. 合并长图

**命令**:
```bash
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-long-image.ts <图片目录> <输出文件>
```

**参数说明**:
- `<图片目录>`: 必需，包含要合并的图片的目录
- `<输出文件>`: 必需，输出的长图文件名

**功能特性**:
- 垂直拼接多张图片
- 自动识别 jpg/png/gif/webp 格式
- 按文件名数字排序
- 保持原图宽度，自动计算高度

**依赖要求**:
需要安装 ImageMagick:
```bash
brew install imagemagick
```

**示例**:
```bash
# 合并 images 目录下的所有图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-long-image.ts ./images 长图.png

# 指定其他目录
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-long-image.ts ./my-images 合集.jpg
```

**使用场景**:
- 制作小红书/微信公众号长图
- 合并系列教程截图
- 制作图片合集展示

---

### 5. 合并为 PPT

**命令**:
```bash
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.ts <图片目录> <输出文件>
```

**参数说明**:
- `<图片目录>`: 必需，包含要打包的图片的目录
- `<输出文件>`: 必需，输出的 PPT 文件名

**功能特性**:
- 每张图片占一页
- 自动识别 jpg/png/gif/webp 格式
- 按文件名数字排序
- 16:9 比例，自动适应页面大小
- 图片居中显示

**示例**:
```bash
# 打包 images 目录下的图片为 PPT
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.ts ./images 配图.pptx

# 指定其他目录
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.ts ./my-images 展示.pptx
```

**使用场景**:
- 快速制作图片演示 PPT
- 打包系列配图用于分享
- 将生成的图像整理成演示文档

---

### 6. 分析图像风格

**命令**:
```bash
# 从 URL 分析
npx -y bun ~/.claude/skills/pw-image-generation/scripts/analyze-image.ts <图像URL>

# 从本地文件分析
npx -y bun ~/.claude/skills/pw-image-generation/scripts/analyze-image.ts <本地路径>
```

**参数说明**:
- `<图像URL或路径>`: 必需，要分析的图像 URL 或本地文件路径

**功能特性**:
- 分析图像的视觉风格
- 生成适合的提示词建议
- 识别颜色、构图、艺术风格
- 保存分析结果到 `analysis/` 目录

**示例**:
```bash
# 分析在线图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/analyze-image.ts https://example.com/image.jpg

# 分析本地图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/analyze-image.ts ./template/参考图.png
```

**使用场景**:
- 学习参考图片的风格特征
- 为图生图准备提示词
- 了解如何描述特定视觉风格


## 文件结构

### 项目目录结构

```
my-image-project/
├── config/
│   └── secrets.md           # API 配置（可选）
├── template/                # PDF 模板图片
├── prompts/                 # 提示词文件
├── analysis/                # 风格分析（可选）
├── images/                  # 生成的图像
└── .gitignore
```

### Skill 目录结构

```
pw-image-generation/
├── SKILL.md                  # 本文件（核心文档）
├── config.example/           # 配置模板
│   ├── README.md             # 配置说明
│   └── secrets.md            # API 配置模板
├── references/               # 参考文档
│   ├── .gitignore.template   # Git 忽略文件模板
│   ├── 图床上传.md           # 图床上传指南
│   ├── style-library.md      # 风格库（9种预设风格）
│   └── prompt-templates/
│       └── 提示词模板.md     # 提示词模板
└── scripts/
    ├── analyze-image.ts      # 分析图像风格
    ├── generate-image.ts     # 生成图像（支持确认和跳过）
    ├── upload-image.ts       # 上传图片到图床
    ├── delete-image.ts       # 管理和删除图床图片
    ├── merge-to-long-image.ts       # 合并长图
    └── merge-to-pptx.ts        # 打包为 PPT
```

---

## 常见问题和错误处理

### 1. 生成图像失败

**问题**: 图像生成失败或返回错误

**可能原因**:
- API 密钥未配置或无效
- 提示词格式不正确
- 网络连接问题
- API 额度不足

**解决方案**:
```bash
# 检查配置文件
cat config/secrets.md

# 验证提示词格式
cat prompts/提示词.md

# 测试网络连接
curl -I https://api.openai.com

# 查看详细错误信息 (脚本会自动显示)
```

---

### 2. 图床上传失败

**问题**: 上传图片到图床失败

**可能原因**:
- 图片文件不存在或路径错误
- 图片格式不支持
- 图片文件过大 (超过 10MB)
- 网络连接问题

**解决方案**:
```bash
# 检查文件是否存在
ls -lh ./template/图片.png

# 检查文件大小
du -h ./template/图片.png

# 如果文件过大，压缩图片
# 使用 ImageMagick 压缩
convert ./template/图片.png -quality 85 -resize 2000x2000\> ./template/图片_compressed.png
```

---

### 3. 合并长图失败

**问题**: 合并长图时报错 "ImageMagick not found"

**可能原因**:
- 未安装 ImageMagick
- ImageMagick 未添加到 PATH

**解决方案**:
```bash
# macOS 安装
brew install imagemagick

# 验证安装
convert --version

# 如果仍然失败，检查 PATH
which convert
```

---

### 4. PPT 生成失败

**问题**: 生成 PPT 时报错或 PPT 无法打开

**可能原因**:
- 图片目录为空或不存在
- 图片格式不支持
- 输出文件路径无效

**解决方案**:
```bash
# 检查图片目录
ls -la ./images

# 检查图片格式 (支持 jpg/png/gif/webp)
file ./images/*.png

# 确保输出目录存在
mkdir -p ./output
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.ts ./images ./output/配图.pptx
```

---

### 5. 提示词不生效

**问题**: 生成的图像与提示词描述不符

**可能原因**:
- 提示词描述不够具体
- 提示词语言混乱 (中英文混用)
- 提示词过长或过短
- 风格描述不明确

**解决方案**:
```markdown
# 不好的提示词
一张图片

# 好的提示词
水彩风格，温馨的咖啡馆场景，柔和的光线，暖色调，手绘质感

# 使用风格库
参考 references/style-library.md 选择合适的风格描述
```

---

### 6. 批量生成中断

**问题**: 批量生成过程中意外中断

**可能原因**:
- 网络不稳定
- 用户手动中断 (Ctrl+C)
- API 限流

**解决方案**:
- 脚本会自动跳过已生成的图像
- 重新运行生成命令即可继续
- 已生成的图像不会重复生成
- 使用 `n` 选项跳过不需要的图像

---

### 7. 配置文件问题

**问题**: 配置文件不生效或找不到

**可能原因**:
- 配置文件路径错误
- 配置文件格式不正确
- 未复制配置模板

**解决方案**:
```bash
# 复制配置模板
cp -r ~/.claude/skills/pw-image-generation/config.example ./config

# 检查配置文件
cat config/secrets.md

# 配置文件格式示例
# API_BASE_URL=https://api.openai.com/v1
# API_KEY=sk-xxx
```

---

## 最佳实践

### 图像尺寸规范

根据不同使用场景选择合适的图像尺寸:

| 场景 | 比例 | 推荐像素 | 说明 |
|------|------|----------|------|
| 文章配图 | 16:9 | 1920×1080 | 高清标准, 适配大屏阅读 |
| 公众号封面 | 2.35:1 | 900×383 | 微信官方推荐尺寸 |
| 小红书封面/配图 | 3:4 | 1242×1660 | 小红书推荐, 适配 iPhone 屏幕 |
| X 文章封面 | 5:2 | 1500×600 | X Articles 官方推荐 |
| 论文配图 | 16:9 | 1920×1080 | 高清标准 |

**补充说明**:
- 小红书也支持 1:1 (1080×1080) 和 4:3 (1440×1080)
- 公众号次图封面可用 200×200 (1:1)

**使用建议**:
- 在提示词中指定尺寸: `size: 1920x1080` 或 `aspect_ratio: 16:9`
- 优先使用推荐尺寸, 避免后期裁剪导致构图失衡
- 不同平台的尺寸要求不同, 生成前确认目标平台

---

### 提示词设计

**基本原则**:
- 具体明确: 详细描述场景、风格、颜色、构图
- 风格统一: 使用风格库中的预设风格描述
- 语言一致: 全英文或全中文，避免混用
- 长度适中: 50-200 字为宜，过短缺乏细节，过长容易混乱

**推荐结构**:
```markdown
[风格] + [主体] + [场景] + [氛围] + [技术细节]

示例:
水彩风格，一只可爱的小猫，坐在窗台上，温暖的午后阳光，柔和的色彩，手绘质感
```

**参考资源**:
- `references/style-library.md`: 9 种预设风格
- `references/prompt-templates/提示词模板.md`: 提示词模板

---

### 图像生成流程

**推荐步骤**:
1. 先生成 1-2 张测试图像，验证提示词效果
2. 根据测试结果调整提示词
3. 确认效果满意后，批量生成剩余图像
4. 使用确认机制，避免浪费 API 额度
5. 定期备份生成的图像

**避免浪费**:
- 每次生成前仔细检查提示词
- 使用 `n` 选项跳过不需要的图像
- 使用 `q` 选项及时退出
- 不要盲目批量生成

---

### 图生图技巧

**上传参考图**:
```bash
# 1. 上传参考图到图床
npx -y bun ~/.claude/skills/pw-image-generation/scripts/upload-image.ts ./template/参考图.png

# 2. 复制返回的 URL

# 3. 在提示词中使用
# image_url: https://iili.io/xxx.png
# prompt: 类似风格的场景，保持色调和构图
```

**注意事项**:
- 参考图尺寸建议 1024x1024 或更大
- 参考图清晰度要高
- 提示词要明确说明保留哪些特征
- 可以多次尝试不同的提示词组合

---

### 文件管理

**目录结构建议**:
```
my-image-project/
├── config/              # 配置文件 (不提交到 git)
├── template/            # 参考图片
├── prompts/             # 提示词文件
│   ├── 01-封面.md
│   ├── 02-内容1.md
│   └── 03-内容2.md
├── images/              # 生成的图像
│   ├── 01-封面.png
│   ├── 02-内容1.png
│   └── 03-内容2.png
└── output/              # 最终输出 (长图/PPT)
```

**命名规范**:
- 提示词文件: 使用数字前缀排序 (01-, 02-, 03-)
- 生成的图像: 自动使用提示词文件名
- 便于批量处理和排序

---

### 性能优化

**提高生成速度**:
- 使用较小的图像尺寸 (1024x1024 而非 2048x2048)
- 避免过于复杂的提示词
- 合理使用图生图 (比文生图更快)

**节省 API 额度**:
- 使用确认机制，不要跳过确认
- 先测试单张，再批量生成
- 保存好的提示词作为模板复用
- 定期清理图床上不需要的图片

---

### 质量控制

**检查清单**:
- [ ] 提示词描述清晰具体
- [ ] 风格描述统一一致
- [ ] 测试图像效果满意
- [ ] 图像尺寸和格式正确
- [ ] 文件命名规范有序
- [ ] 备份重要图像

**常见问题**:
- 图像风格不一致: 检查提示词中的风格描述
- 图像质量不佳: 增加技术细节描述 (如 "高清"、"细节丰富")
- 图像内容偏差: 提示词更具体，增加约束条件

---

## 重要提示

### 避免额度浪费

- 每次生成前都会询问确认
- 支持跳过已生成的图像
- 一张一张生成，避免批量消耗额度

### 配置管理

- 配置文件 `config/secrets.md` 是可选的
- 未配置时使用默认配置 (需要设置环境变量 API_KEY)
- 配置文件不会提交到版本控制 (已在 .gitignore 中)
- 支持自定义 API 端点和模型

### 运行环境

脚本使用 Bun 运行，无需本地安装依赖:

```bash
# 直接运行，Bun 会自动处理依赖
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts
```

**系统要求**:
- Node.js 或 Bun 运行时
- macOS/Linux/Windows (WSL)
- 合并长图需要 ImageMagick

---

## 配置说明

查看 `config.example/secrets.md` 了解配置选项:

**可配置项**:
- `API_BASE_URL`: API 基础 URL (默认: OpenAI API)
- `ANALYSIS_MODEL_ID`: 图像分析模型 (默认: gpt-4-vision-preview)
- `GENERATION_MODEL_ID`: 图像生成模型 (默认: dall-e-3)
- `API_KEY`: API 密钥 (必需)

**配置示例**:
```markdown
# config/secrets.md
API_BASE_URL=https://api.openai.com/v1
ANALYSIS_MODEL_ID=gpt-4-vision-preview
GENERATION_MODEL_ID=dall-e-3
API_KEY=sk-your-api-key-here
```

---

## 风格库

Skill 提供 9 种预设风格，保证图像风格一致性:

- 水彩风格 (watercolor) - 柔和温馨
- 扁平化设计 (flat-design) - 现代简洁
- 3D 渲染 (3d-render) - 立体真实
- 油画风格 (oil-painting) - 艺术经典
- 赛博朋克 (cyberpunk) - 科幻未来
- 像素艺术 (pixel-art) - 复古怀旧
- 手绘插画 (hand-drawn) - 温暖个性
- 照片写实 (photorealistic) - 高度真实
- 抽象艺术 (abstract) - 情感表达

查看 `references/style-library.md` 了解每种风格的详细说明和使用场景。

---

## 使用建议

### Agent 使用指南

当用户请求生成图像时:

1. **确认需求**: 询问用户图像用途、风格偏好、数量
2. **准备环境**: 引导用户创建项目目录和配置
3. **设计提示词**: 根据需求设计提示词，参考风格库
4. **生成测试**: 先生成 1-2 张测试图像
5. **批量生成**: 确认效果后批量生成
6. **后期处理**: 根据需要合并长图或打包 PPT

### 典型工作流

**场景 1: 文章配图**
```bash
# 1. 创建项目
mkdir article-images && cd article-images

# 2. 准备提示词
mkdir prompts
# 创建 prompts/01-封面.md, 02-配图1.md 等

# 3. 生成图像
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts

# 4. 合并长图 (可选)
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-long-image.ts ./images 长图.png
```

**场景 2: PPT 配图**
```bash
# 1. 创建项目
mkdir ppt-images && cd ppt-images

# 2. 准备提示词 (按页面顺序命名)
mkdir prompts
# 创建 prompts/01-标题页.md, 02-内容1.md 等

# 3. 生成图像
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts

# 4. 打包为 PPT
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.ts ./images 配图.pptx
```

**场景 3: 图生图**
```bash
# 1. 上传参考图
npx -y bun ~/.claude/skills/pw-image-generation/scripts/upload-image.ts ./template/参考图.png

# 2. 在提示词中使用返回的 URL
# prompts/01-类似风格.md:
# image_url: https://iili.io/xxx.png
# prompt: 类似风格的场景，保持色调和构图

# 3. 生成图像
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts
```

---

## 命令速查

```bash
# 生成图像
npx -y bun ~/.claude/skills/pw-image-generation/scripts/generate-image.ts [输出目录]

# 上传图片
npx -y bun ~/.claude/skills/pw-image-generation/scripts/upload-image.ts <图片路径>

# 管理图床
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts list
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts delete <索引>
npx -y bun ~/.claude/skills/pw-image-generation/scripts/delete-image.ts delete-all

# 合并长图
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-long-image.ts <图片目录> <输出文件>

# 打包 PPT
npx -y bun ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.ts <图片目录> <输出文件>

# 分析图像
npx -y bun ~/.claude/skills/pw-image-generation/scripts/analyze-image.ts <图像URL或路径>
```
