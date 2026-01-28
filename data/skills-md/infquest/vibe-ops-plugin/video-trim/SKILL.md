---
name: video-trim
description: 裁剪视频片段，支持压缩、音频控制等选项。Use when user wants to 剪辑视频, 裁剪视频, 截取视频, 视频剪切, 切视频, trim video, cut video, clip video, extract video segment.
---

# Video Trimmer

裁剪视频片段，支持压缩、音频处理和输出格式选择。

## Usage

When the user wants to trim a video: $ARGUMENTS

## Instructions

你是一个视频裁剪助手，使用 ffmpeg 帮助用户裁剪视频。请按以下步骤操作：

### Step 1: 获取输入文件

如果用户没有提供输入文件路径，询问他们提供一个。

验证文件存在并获取信息：

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_name,width,height,r_frame_rate -of json "$INPUT_FILE"
```

向用户展示：
- 文件时长
- 分辨率（如果是视频）
- 编码信息
- 文件大小

### Step 2: 询问用户裁剪配置

**⚠️ 必须：你必须使用 AskUserQuestion 工具询问用户的偏好，然后再执行任何 ffmpeg 命令。不要跳过这一步或根据用户的初始请求做出假设。即使用户提供了一些参数（如开始/结束时间），你仍然必须询问压缩、音频处理等选项。**

使用 AskUserQuestion 工具收集用户偏好：

1. **开始时间**：从什么时间开始？（格式：HH:MM:SS 或秒数）
   - 让用户手动输入

2. **结束时间**：在哪里结束？
   - 选项：
     - "指定结束时间"
     - "指定持续时长"
     - "裁剪到视频末尾"

3. **压缩设置**：是否压缩输出文件？
   - 选项：
     - "不压缩 - 直接复制流（最快，无损）(Recommended)"
     - "轻度压缩（CRF 23，画质好）"
     - "中度压缩（CRF 28，平衡）"
     - "高度压缩（CRF 32，文件更小）"
     - "自定义 CRF 值"

4. **音频处理**：如何处理音频？
   - 选项：
     - "保留原始音频 (Recommended)"
     - "完全移除音频"
     - "重新编码音频（AAC 128k）"
     - "重新编码音频（AAC 256k，高质量）"

5. **附加选项**（多选）：需要其他选项吗？
   - 选项：
     - "在剪切点添加淡入/淡出效果"
     - "在中点生成缩略图"
     - "在开始处强制关键帧（更精确的剪切）"
     - "无需其他选项"

6. **输出格式**：输出什么格式？
   - 选项："与输入相同 (Recommended)"、"MP4"、"MKV"、"WebM"、"MOV"

7. **输出路径**：保存到哪里？（建议默认：input_trimmed.ext）

### Step 3: 构建 FFmpeg 命令

根据用户选择，构建 ffmpeg 命令：

#### 时间选项
```bash
# 开始时间
-ss HH:MM:SS

# 基于时长的结束
-t DURATION

# 基于结束时间
-to HH:MM:SS
```

**重要**：将 `-ss` 放在 `-i` 之前可以快速定位（输入定位），放在 `-i` 之后可以精确到帧（更慢但更精确）。

#### 压缩选项
```bash
# 不压缩（流复制）- 最快
-c copy

# 重新编码（允许压缩）
-c:v libx264 -crf VALUE -preset medium
```

CRF 值说明：
- 18-23：视觉无损到好画质
- 23-28：好到可接受的画质
- 28-32：较低画质，文件更小

#### 音频选项
```bash
# 保留原始（使用流复制）
-c:a copy

# 移除音频
-an

# 重新编码音频
-c:a aac -b:a 128k   # 或 256k
```

#### 附加选项
```bash
# 淡入/淡出（0.5秒）
-vf "fade=t=in:st=0:d=0.5,fade=t=out:st=END-0.5:d=0.5"
-af "afade=t=in:st=0:d=0.5,afade=t=out:st=END-0.5:d=0.5"

# 强制开始处关键帧（不使用流复制时）
-force_key_frames "expr:gte(t,0)"

# 生成缩略图
ffmpeg -ss MIDPOINT -i input -vframes 1 -q:v 2 thumbnail.jpg
```

### Step 4: 执行并报告

1. 执行前向用户展示完整的 ffmpeg 命令
2. 执行命令并显示进度
3. 报告成功/失败
4. 显示输出文件路径和大小对比

#### 命令模板

```bash
# 基础裁剪，使用流复制（最快）
ffmpeg -ss START -to END -i "INPUT" -c copy "OUTPUT"

# 带重新编码的裁剪
ffmpeg -ss START -to END -i "INPUT" -c:v libx264 -crf 23 -c:a aac -b:a 128k "OUTPUT"

# 无音频的裁剪
ffmpeg -ss START -to END -i "INPUT" -c:v copy -an "OUTPUT"
```

### Step 5: 验证输出

裁剪完成后，验证输出：

```bash
ffprobe -v error -show_entries format=duration,size -of json "OUTPUT_FILE"
```

报告：
- 输出时长是否符合预期
- 文件大小对比（原始 vs 裁剪后）
- 任何警告或问题

### 示例交互

用户：帮我把视频从 1:30 裁剪到 3:45
