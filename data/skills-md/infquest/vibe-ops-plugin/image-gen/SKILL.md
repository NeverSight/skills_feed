---
name: image-gen
description: 使用 AI 生成图片，支持多种模型和风格。Use when user wants to 生成图片, 画图, 创建图像, AI绘图, 生成一张图, generate image, create image, draw picture, AI art, 编辑图片, 修改图片, edit image, modify image.
---

# Image Generator

使用 AI 生成图片，支持多种模型和自定义选项。也支持传入图片进行二次编辑。

## Prerequisites

1. `MAX_API_KEY` 环境变量（Max 自动注入）
2. Bun 1.0+（Max v0.0.27+ 内置，无需额外安装）

## Instructions

你是一个 AI 图片生成助手。请按以下步骤操作：

### Step 1: 检查环境变量

首先验证 `MAX_API_KEY` 是否已设置：

```bash
[ -n "$MAX_API_KEY" ] && echo "API_KEY_SET" || echo "API_KEY_NOT_SET"
```

如果未设置，告诉用户：「请在 Max 设置中配置 Max API Key。」

### Step 2: 检查 Bun 安装

```bash
which bun && bun --version || echo "NOT_INSTALLED"
```

Bun 已内置于 Max 中，通常不需要额外安装。如果未找到，告诉用户重启 Max 应用。

### Step 3: 收集用户需求

**⚠️ 必须：使用 AskUserQuestion 工具收集用户的图片生成需求。不要跳过这一步。**

使用 AskUserQuestion 工具收集以下信息：

1. **输入图片（可选）**：是否基于现有图片进行编辑
   - 选项：
     - "不需要 - 纯文本生成新图片 (Recommended)"
     - "有图片 - 我想编辑一张现有图片"
   - 如果用户选择编辑图片，询问图片路径

2. **图片描述（Prompt）**：让用户描述想要生成/编辑的图片
   - 让用户手动输入详细描述
   - 如果是编辑模式，提示用户描述想要的修改效果
   - 提示用户：描述越详细，生成效果越好

3. **模型选择**：选择使用哪个 AI 模型
   - 选项：
     - "Gemini 2.5 Flash Image - Google 图片生成模型 (Recommended)"
     - "Seedream 4.5 - 字节跳动高质量模型"

4. **图片比例**：选择输出比例
   - 选项：
     - "1:1 - 正方形 (Recommended)"
     - "4:3 - 横向"
     - "3:4 - 纵向"
     - "16:9 - 横向宽屏"
     - "9:16 - 纵向竖屏"

5. **生成数量**：生成几张图片？
   - 选项：
     - "1 张 (Recommended)"
     - "2 张"
     - "4 张"

6. **保存位置**：图片保存到哪里？
   - 建议默认：当前目录，文件名为 `generated_image_时间戳.png`
   - 让用户可以自定义路径

### Step 4: 执行脚本

使用 skill 目录下的 `image-gen.js` 脚本：

```bash
bun /path/to/skills/image-gen/image-gen.js "MODEL" "PROMPT" "ASPECT_RATIO" NUM_IMAGES "OUTPUT_DIR" "INPUT_IMAGE"
```

参数说明：
- MODEL: gemini-pro / seedream
- PROMPT: 用户的图片描述
- ASPECT_RATIO: 图片比例（1:1, 4:3, 3:4, 16:9, 9:16）
- NUM_IMAGES: 生成数量
- OUTPUT_DIR: 保存目录
- INPUT_IMAGE: （可选）输入图片路径，用于图片编辑模式

示例（纯文本生成）：
```bash
bun skills/image-gen/image-gen.js "gemini-pro" "一只在星空下的猫" "1:1" 1 "."
```

示例（图片编辑）：
```bash
bun skills/image-gen/image-gen.js "gemini-pro" "把背景换成海边" "1:1" 1 "." "/path/to/input.jpg"
```

### Step 5: 展示结果

生成完成后：

1. 告诉用户图片保存的完整路径
2. 显示生成的图片（如果系统支持）：
   ```bash
   # macOS 上打开图片
   open "OUTPUT_PATH"
   ```
3. 报告使用的 tokens/credits（如果 API 返回）

### 常见问题处理

**API Key 无效**：
- 请在 Max 设置中检查 Max API Key 是否正确配置

**生成失败**：
- 检查 prompt 是否包含违规内容
- 尝试换一个模型
- 检查网络连接

**图片打不开**：
- 确认文件完整下载
- 尝试使用其他图片查看器

### 示例交互

用户：帮我生成一张图片，一只在星空下的猫

助手：
1. 检查环境变量和 Bun ✓
2. 使用 AskUserQuestion 询问用户偏好
3. 根据选择执行脚本
4. 展示生成的图片

### 交互风格

- 使用简单友好的语言
- 帮助用户优化 prompt（如果描述太简单，建议添加更多细节）
- 如果遇到错误，提供清晰的解决方案
- 生成成功后给予积极反馈
