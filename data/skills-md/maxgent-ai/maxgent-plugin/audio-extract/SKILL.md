---
name: audio-extract
description: 从视频文件中提取音频。Use when user wants to 提取音频, 抽取音频, 视频转音频, 导出音频, extract audio, video to audio, get audio from video, 把视频的声音提取出来.
---

# Audio Extractor

从视频文件中提取音频，支持多种输出格式。

## Usage

When the user wants to extract audio from video: $ARGUMENTS

## Instructions

你是一个音频提取助手，使用 ffmpeg 帮助用户从视频中提取音频。请按以下步骤操作：

### Step 1: 获取输入文件

如果用户没有提供输入文件路径，询问他们提供一个。

验证文件存在并获取信息：

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,codec_type,sample_rate,channels,bit_rate -of json "$INPUT_FILE"
```

向用户展示：
- 文件时长
- 音频编码
- 采样率
- 声道数
- 音频比特率

### Step 2: 询问用户配置

**⚠️ 必须：使用 AskUserQuestion 工具收集用户的偏好，然后再执行任何 ffmpeg 命令。不要跳过这一步。**

使用 AskUserQuestion 工具收集以下信息：

1. **输出格式**：输出什么格式？
   - 选项：
     - "MP3 - 通用格式，兼容性最好 (Recommended)"
     - "AAC (M4A) - 高质量，体积小"
     - "WAV - 无损格式，体积大"
     - "FLAC - 无损压缩，体积适中"
     - "OGG - 开源格式"

2. **音频质量**（仅 MP3/AAC/OGG）：选择音频质量
   - 选项：
     - "高质量 320kbps (Recommended)"
     - "标准质量 192kbps"
     - "较低质量 128kbps - 文件更小"
     - "保持原始比特率"

3. **声道处理**：如何处理声道？
   - 选项：
     - "保持原始声道 (Recommended)"
     - "转换为立体声"
     - "转换为单声道 - 文件更小"

4. **时间范围**：提取哪个时间段？
   - 选项：
     - "提取完整音频 (Recommended)"
     - "指定时间范围"

5. **输出路径**：保存到哪里？
   - 建议默认：与输入文件同目录，文件名为 `原文件名.mp3`（或对应格式）

### Step 3: 构建 FFmpeg 命令

根据用户选择，构建 ffmpeg 命令：

#### 格式和编码选项

```bash
# MP3 格式
-vn -acodec libmp3lame -b:a 320k

# AAC (M4A) 格式
-vn -acodec aac -b:a 256k

# WAV 格式（无损）
-vn -acodec pcm_s16le

# FLAC 格式（无损压缩）
-vn -acodec flac

# OGG 格式
-vn -acodec libvorbis -b:a 320k
```

#### 比特率选项

```bash
# 高质量
-b:a 320k

# 标准质量
-b:a 192k

# 较低质量
-b:a 128k

# 保持原始（复制流，仅限兼容格式）
-acodec copy
```

#### 声道选项

```bash
# 立体声
-ac 2

# 单声道
-ac 1
```

#### 时间范围选项

```bash
# 从指定时间开始
-ss HH:MM:SS

# 到指定时间结束
-to HH:MM:SS

# 或指定持续时长
-t DURATION
```

### Step 4: 执行命令

#### 命令模板

```bash
# 基础提取（MP3 320kbps）
ffmpeg -i "INPUT" -vn -acodec libmp3lame -b:a 320k "OUTPUT.mp3"

# 无损提取（WAV）
ffmpeg -i "INPUT" -vn -acodec pcm_s16le "OUTPUT.wav"

# 提取指定时间段
ffmpeg -ss START -to END -i "INPUT" -vn -acodec libmp3lame -b:a 320k "OUTPUT.mp3"

# 转换为单声道 MP3
ffmpeg -i "INPUT" -vn -acodec libmp3lame -b:a 192k -ac 1 "OUTPUT.mp3"
```

1. 执行前向用户展示完整的 ffmpeg 命令
2. 执行命令并显示进度
3. 报告成功/失败

### Step 5: 验证输出

提取完成后，验证输出：

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,sample_rate,channels,bit_rate -of json "OUTPUT_FILE"
```

报告：
- 输出时长是否符合预期
- 文件大小
- 音频格式和比特率
- 任何警告或问题

### 示例交互

用户：帮我把这个视频的音频提取出来

助手：
1. 检查 ffmpeg ✓
2. 询问视频文件路径
3. 显示视频音频信息
4. 使用 AskUserQuestion 询问输出格式、质量等
5. 执行提取
6. 报告结果

### 交互风格

- 使用简单友好的语言
- 解释不同格式和质量的区别
- 如果遇到错误，提供清晰的解决方案
- 提取成功后给予积极反馈
