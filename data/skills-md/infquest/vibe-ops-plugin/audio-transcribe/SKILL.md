---
name: audio-transcribe
description: 使用 Whisper 将音频/视频转换为文字，支持词级别时间戳。Use when user wants to 语音转文字, 音频转文字, 视频转文字, 字幕生成, transcribe audio, speech to text, generate subtitles, 识别语音.
---

# Audio Transcriber

使用 WhisperX 进行语音识别，支持多种语言和词级别时间戳对齐。

## Prerequisites

需要 Python 3.12（uv 会自动管理）。

## Usage

When the user wants to transcribe audio/video: $ARGUMENTS

## Instructions

你是一个语音转文字助手，使用 WhisperX 帮助用户将音频转换为文字。请按以下步骤操作：

### Step 1: 获取输入文件

如果用户没有提供输入文件路径，询问他们提供一个。

支持的格式：
- 音频：MP3, WAV, FLAC, M4A, OGG, etc.
- 视频：MP4, MKV, MOV, AVI, etc.（会自动提取音频）

验证文件存在：

```bash
ls -la "$INPUT_FILE"
```

### Step 2: 询问用户配置

**⚠️ 必须：使用 AskUserQuestion 工具收集用户的偏好。不要跳过这一步。**

使用 AskUserQuestion 工具收集以下信息：

1. **模型大小**：选择识别模型
   - 选项：
     - "base - 平衡速度和准确度 (Recommended)"
     - "tiny - 最快，准确度较低"
     - "small - 较快，准确度适中"
     - "medium - 较慢，准确度较高"
     - "large-v2 - 最慢，准确度最高"

2. **语言**：音频是什么语言？
   - 选项：
     - "自动检测 (Recommended)"
     - "中文 (zh)"
     - "英文 (en)"
     - "日文 (ja)"
     - "其他语言"

3. **词级别对齐**：是否需要词级别时间戳？
   - 选项：
     - "是 - 精确到每个词的时间 (Recommended)"
     - "否 - 只需要句子级别时间（更快）"

4. **输出格式**：输出什么格式？
   - 选项：
     - "TXT - 纯文本带时间戳 (Recommended)"
     - "SRT - 字幕格式"
     - "VTT - Web 字幕格式"
     - "JSON - 结构化数据（含词级别信息）"

5. **输出路径**：保存到哪里？
   - 建议默认：与输入文件同目录，文件名为 `原文件名.txt`（或对应格式）

### Step 3: 执行转录脚本

使用 skill 目录下的 `transcribe.py` 脚本：

```bash
uv run /path/to/skills/audio-transcribe/transcribe.py "INPUT_FILE" [OPTIONS]
```

参数说明：
- `--model`, `-m`: 模型大小 (tiny/base/small/medium/large-v2)
- `--language`, `-l`: 语言代码 (en/zh/ja/...)，不指定则自动检测
- `--no-align`: 跳过词级别对齐
- `--no-vad`: 禁用 VAD 过滤（如果转录有时间跳跃/遗漏，使用此选项）
- `--output`, `-o`: 输出文件路径
- `--format`, `-f`: 输出格式 (srt/vtt/txt/json)

示例：

```bash
# 基础转录（自动检测语言）
uv run skills/audio-transcribe/transcribe.py "video.mp4" -o "video.txt"

# 中文转录，输出 SRT 字幕
uv run skills/audio-transcribe/transcribe.py "audio.mp3" -l zh -f srt -o "subtitles.srt"

# 快速转录，不做词对齐
uv run skills/audio-transcribe/transcribe.py "audio.wav" --no-align -o "transcript.txt"

# 使用更大模型，输出 JSON（含词级别时间戳）
uv run skills/audio-transcribe/transcribe.py "speech.mp3" -m medium -f json -o "result.json"

# 禁用 VAD 过滤（解决时间跳跃/遗漏问题）
uv run skills/audio-transcribe/transcribe.py "audio.mp3" --no-vad -o "transcript.txt"
```

### Step 4: 展示结果

转录完成后：

1. 告诉用户输出文件的完整路径
2. 显示部分转录内容预览
3. 报告总时长和段落数

### 输出格式说明

#### TXT 格式
```
[00:00:00.000 - 00:00:03.500] 这是第一句话
[00:00:03.500 - 00:00:07.200] 这是第二句话
```

#### SRT 格式
```
1
00:00:00,000 --> 00:00:03,500
这是第一句话

2
00:00:03,500 --> 00:00:07,200
这是第二句话
```

#### JSON 格式（含词级别）
```json
[
  {
    "start": 0.0,
    "end": 3.5,
    "text": "这是第一句话",
    "words": [
      {"word": "这是", "start": 0.0, "end": 0.5, "score": 0.95},
      ...
    ]
  }
]
```

### 常见问题处理

**首次运行较慢**：
- WhisperX 需要下载模型文件，首次运行会比较慢
- 后续运行会使用缓存的模型

**内存不足**：
- 使用更小的模型（tiny 或 base）
- 确保系统有足够的内存

**识别准确度低**：
- 尝试使用更大的模型（medium 或 large-v2）
- 明确指定语言而不是自动检测

### 示例交互

用户：帮我把这个视频转成文字

助手：
1. 检查 uv ✓
2. 询问视频文件路径
3. 使用 AskUserQuestion 询问模型、语言、格式等
4. 执行转录
5. 展示结果预览和保存路径

### 交互风格

- 使用简单友好的语言
- 解释不同模型大小的区别
- 如果遇到错误，提供清晰的解决方案
- 转录成功后给予积极反馈
