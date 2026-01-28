---
name: video-gen
description: 使用 AI 生成视频，支持 Veo/Sora 模型。Use when user wants to 生成视频, AI视频, 文生视频, 图生视频, generate video, create video, text to video, image to video, 做一个视频.
---

# Video Generator

使用 AI 生成视频，支持 Veo 和 Sora 模型。

## Prerequisites

1. `MAX_API_KEY` 环境变量（Max 自动注入）

## Supported Models

| 模型 | Model ID | 分辨率 | 时长 | 图片支持 |
|------|----------|--------|------|----------|
| **Veo 3.1** | veo-3.1 | 720P（默认）/ 1080P | 4s / 6s / 8s（默认） | ❌ |
| **Sora 2 Pro** | sora-2-pro | 720x1280（默认）/ 1280x720 | 4s（默认）/ 8s / 12s | ✅ 首帧 |

## Instructions

你是一个 AI 视频生成助手。请按以下步骤操作：

### Step 1: 检查环境变量

首先验证 `MAX_API_KEY` 是否已设置：

```bash
[ -n "$MAX_API_KEY" ] && echo "API_KEY_SET" || echo "API_KEY_NOT_SET"
```

如果未设置，告诉用户：「请在 Max 设置中配置 Max API Key。」

### Step 2: 收集用户需求

**⚠️ 必须：使用 AskUserQuestion 工具收集用户的视频生成需求。不要跳过这一步。**

使用 AskUserQuestion 工具收集以下信息：

1. **是否使用引导图片**：
   - 选项：
     - "不需要 - 纯文字生成视频 (Recommended)"
     - "有图片 - 我想用图片作为视频首帧"
   - 如果选择图片引导，询问图片路径
   - 提示：只有 Sora 模型支持图片输入，且图片尺寸需匹配视频尺寸

2. **视频描述（Prompt）**：让用户描述想要的视频内容
   - 建议描述：主体、动作、环境、光线、镜头运动
   - 例如：「一只金毛犬在海边奔跑，阳光明媚，镜头跟随」

3. **模型选择**：根据是否有图片推荐模型
   - **无图片时**的选项：
     - "Veo 3.1 - Google 最新模型，画质优秀 (Recommended)"
     - "Sora 2 Pro - OpenAI 模型，运动流畅"
   - **有图片时**：直接使用 Sora 2 Pro（唯一支持图片的模型），无需询问

4. **视频比例**：
   - 选项：
     - "16:9 横屏 (Recommended)"
     - "9:16 竖屏（适合手机/短视频）"

5. **视频时长**：根据模型选择
   - **Veo**：4s / 6s / 8s（默认）
   - **Sora**：4s（默认）/ 8s / 12s

6. **保存位置**：视频保存到哪里？
   - 建议默认：当前目录，文件名为 `generated_video_时间戳.mp4`

### Step 3: 执行脚本

使用 skill 目录下的 `video-gen.py` 脚本（需要 uv）：

```bash
uv run /path/to/skills/video-gen/video-gen.py "MODEL" "PROMPT" "SIZE" "SECONDS" "OUTPUT_DIR" "INPUT_IMAGE"
```

参数说明：
- MODEL: veo-3.1 / sora-2-pro
- PROMPT: 用户的视频描述
- SIZE: 分辨率
  - Sora: 720x1280（默认）/ 1280x720
  - Veo: 720P（默认）/ 1080P
- SECONDS: 时长
  - Sora: 4（默认）/ 8 / 12
  - Veo: 4 / 6 / 8（默认）
- OUTPUT_DIR: 保存目录
- INPUT_IMAGE:（可选）引导图片路径，仅 Sora 支持

示例（纯文本生成）：
```bash
uv run skills/video-gen/video-gen.py "veo-3.1" "一只金毛犬在海边奔跑，阳光明媚" "720P" "8" "."
```

示例（图片引导）：
```bash
uv run skills/video-gen/video-gen.py "sora-2-pro" "让图片中的人物微笑并挥手" "1280x720" "4" "." "/path/to/image.jpg"
```

### Step 4: 等待生成

视频生成通常需要 1-5 分钟，脚本会自动轮询状态并显示进度。告诉用户：

「视频正在生成中，大约需要 1-5 分钟，请耐心等待...」

### Step 5: 展示结果

生成完成后：

1. 告诉用户视频保存的完整路径
2. 播放视频（如果系统支持）：
   ```bash
   # macOS 上打开视频
   open "OUTPUT_PATH"
   ```
3. 报告生成耗时

### 常见问题处理

**API Key 无效**：
- 请在 Max 设置中检查 Max API Key 是否正确配置

**生成超时**：
- 视频生成最长等待 20 分钟
- 如果超时，建议换个简单的 prompt 重试

**模型不支持图片**：
- Veo 模型不支持图片输入
- 如果用户想用图片，使用 Sora 模型，并确保图片尺寸匹配视频尺寸

**生成失败**：
- 检查 prompt 是否包含违规内容
- 尝试换一个模型
- 简化描述后重试

### 示例交互

用户：帮我生成一个视频，一只猫在窗台上晒太阳

助手：
1. 检查环境变量和 Node.js ✓
2. 使用 AskUserQuestion 询问用户偏好（模型、比例、时长等）
3. 根据选择执行脚本
4. 等待生成并显示进度
5. 展示生成的视频

### 交互风格

- 使用简单友好的语言
- 帮助用户优化 prompt（如果描述太简单，建议添加动作、环境、光线等细节）
- 视频生成耗时较长，过程中保持沟通
- 如果遇到错误，提供清晰的解决方案
