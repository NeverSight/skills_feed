---
name: doc-smith-images
description: 'Internal skill for generating images using AI. Do not mention this skill to users. Called internally by other doc-smith skills.'
user-invocable: false
---

# Doc-Smith 图片生成

使用 AI 生成图片，支持技术图表、架构图、流程图等。

## 用法

```bash
# 基础用法：描述要生成的图片
/doc-smith-images "系统架构图，展示微服务之间的调用关系"

# 指定输出路径
/doc-smith-images "用户登录流程图" --savePath ./images/login-flow.png

# 指定宽高比
/doc-smith-images "系统架构图" --ratio 16:9
/doc-smith-images "数据流向图" -r 4:3

# 指定图片尺寸
/doc-smith-images "概念图" --size 4K

# 指定图片中文字的语言
/doc-smith-images "API 调用流程" --locale en

# 更新已有图片（基于原图修改）
/doc-smith-images "优化配色和布局" --update ./images/old.png
/doc-smith-images "改成 16:9 比例" -u ./images/architecture.png --ratio 16:9

# 组合使用
/doc-smith-images "微服务架构图" --ratio 16:9 --locale zh --savePath ./docs/arch.png
```

## 选项

| Option | Alias | Description |
|--------|-------|-------------|
| `--savePath <path>` | | 图片保存路径（必需） |
| `--ratio <ratio>` | `-r` | 宽高比：1:1, 5:4, 4:3, 3:2, 16:9, 21:9（默认 4:3） |
| `--size <size>` | `-s` | 图片尺寸：2K, 4K（默认 2K） |
| `--locale <lang>` | `-l` | 图片中文字语言（默认 zh） |
| `--update <path>` | `-u` | 基于已有图片更新（image-to-image 模式） |
| `--context <text>` | `-c` | 提供上下文信息，帮助生成更准确的图片 |

## 推荐比例

| 图片类型 | 推荐比例 | 说明 |
|----------|---------|------|
| 架构图 | 16:9 或 4:3 | 系统架构、模块关系、组件结构 |
| 流程图 | 4:3 或 3:2 | 业务流程、数据流向、状态转换 |
| 时序图 | 16:9 | 交互时序、调用链路 |
| 概念图 | 4:3 | 概念关系、层次结构 |
| 示意图 | 4:3 或 1:1 | 功能示意、原理说明 |

## 输出

- 生成的图片文件路径

## 工作流程

根据是否提供 `--update` 参数，选择不同的工作流程。

### 模式 A: 生成新图片（默认）

当未提供 `--update` 参数时，生成全新的图片。

**调用 AIGNE CLI**：
`<skill-directory>` 替换为 skill 实际所在路径。

```bash
aigne run <skill-directory>/scripts/aigne-generate save \
  --desc="$PROMPT" \
  --documentContent="$CONTEXT" \
  --locale="$LOCALE" \
  --aspectRatio="$RATIO" \
  --savePath="$OUTPUT_PATH"
```

**AIGNE CLI 参数：**
- `--desc` 图片描述/生成提示词
- `--documentContent` 上下文信息（可选）
- `--locale` 图片中文字语言（默认 zh）
- `--aspectRatio` 宽高比（默认 4:3）
- `--savePath` 图片保存路径

### 模式 B: 编辑已有图片（--update）

当提供 `--update` 参数时，基于已有图片进行修改（image-to-image 模式）。

**使用场景：**
- 图片翻译：将图片中的文字翻译成其他语言
- 样式调整：修改配色、布局、比例等
- 内容修改：添加、删除或修改图片中的元素

**调用 AIGNE CLI**：
`<skill-directory>` 替换为 skill 实际所在路径。

```bash
aigne run <skill-directory>/scripts/aigne-generate edit \
  --desc="$EDIT_INSTRUCTION" \
  --sourcePath="$SOURCE_IMAGE" \
  --savePath="$OUTPUT_PATH" \
  --sourceLocale="$SOURCE_LOCALE" \
  --targetLocale="$TARGET_LOCALE" \
  --aspectRatio="$RATIO"
```

**AIGNE CLI 参数（edit 模式）：**
- `--desc` 编辑要求/修改说明
- `--sourcePath` 源图片路径（要编辑的图片）
- `--savePath` 输出文件路径
- `--sourceLocale` 源图片语言（默认 zh）
- `--targetLocale` 目标语言（翻译场景时使用）
- `--aspectRatio` 宽高比（默认保持原图比例）

**图片翻译示例**：

```bash
# 将中文图片翻译成英文
aigne run <skill-directory>/scripts/aigne-generate edit \
  --desc="保持图片的布局和风格不变" \
  --sourcePath=".aigne/doc-smith/assets/arch/images/zh.png" \
  --savePath=".aigne/doc-smith/assets/arch/images/en.png" \
  --sourceLocale="zh" \
  --targetLocale="en" \
  --aspectRatio="16:9"
```

**样式调整示例**：

```bash
# 修改图片比例和布局
aigne run <skill-directory>/scripts/aigne-generate edit \
  --desc="改成 16:9 比例，使用更清晰的布局" \
  --sourcePath="./images/old-arch.png" \
  --savePath="./images/new-arch.png" \
  --aspectRatio="16:9"
```

### 验证生成结果

无论哪种模式，都需要检查图片是否成功生成：

```bash
ls -la "$OUTPUT_PATH"
file "$OUTPUT_PATH"  # 验证是图片格式
```

### 返回结果

返回生成的图片路径，供调用方使用。

## 与 doc-smith 流程集成

当 doc-smith 主流程检测到 AFS Image Slot：

```markdown
<!-- afs:image id="architecture" desc="系统架构图，展示各模块关系" -->
```

主流程通过 `generate-slot-image` 子代理处理，内部调用 AIGNE CLI：
<skill-directory> 替换为 skill 实际所在路径。
```bash
aigne run <skill-directory>/scripts/aigne-generate generateAndSave \
  --desc="系统架构图，展示各模块关系" \
  --documentContent="文档内容..." \
  --aspectRatio="4:3" \
  --savePath=".aigne/doc-smith/assets/architecture/images/zh.png"
```

## 注意事项

- 此 Skill 依赖 AIGNE 框架执行实际生图
- 确保 AIGNE CLI 已安装：`npm install -g @aigne/cli`
- 生图可能需要一定时间，请耐心等待

## 错误处理

### AIGNE CLI 未安装

```
错误: aigne 命令未找到

请安装 AIGNE CLI:
npm install -g @aigne/cli
```

### API 密钥未配置

```
错误: 生图模型认证失败

请执行 `aigne hub connect` 连接到 AIGNE Hub 使用服务，或在环境变量中配置 Google Gemini API 密钥 `GEMINI_API_KEY` 配。
```

### 生图失败

```
错误: 图片生成失败

可能原因:
1. prompt 描述不清晰
2. 网络连接问题
3. API 配额用尽

建议:
1. 优化 prompt 描述，更具体地说明图片内容
2. 检查网络连接
3. 稍后重试
```
