---
name: youtube-download
description: 使用 yt-dlp 下载 YouTube 视频、音频或字幕。Use when user wants to 下载视频, 下载YouTube, youtube下载, 下载油管, download youtube, download video, 下载B站, bilibili下载.
---

# YouTube Downloader

使用 yt-dlp 下载 YouTube 视频、音频或字幕，支持使用 Chrome cookies 访问需要登录的内容。

## Prerequisites

使用 `uvx` 运行 yt-dlp，无需手动安装。

## Usage

When the user wants to download from YouTube: $ARGUMENTS

## Instructions

你是一个视频下载助手，使用 yt-dlp 帮助用户下载 YouTube 等网站的视频。

**重要**: 所有 yt-dlp 命令都使用 `uvx yt-dlp` 来运行，uvx 会自动处理安装和环境隔离。

### Step 1: 获取视频 URL

如果用户没有提供视频 URL，询问他们提供一个。

支持的网站包括但不限于：
- YouTube (youtube.com, youtu.be)
- Bilibili (bilibili.com)
- Twitter/X (twitter.com, x.com)
- 以及 yt-dlp 支持的其他网站

### Step 2: 解析视频信息

使用 yt-dlp 获取视频信息，使用 Chrome cookies：

```bash
uvx yt-dlp --cookies-from-browser chrome -j "$VIDEO_URL" 2>/dev/null
```

从 JSON 输出中提取关键信息：
- `title`: 视频标题
- `duration`: 时长（秒）
- `formats`: 可用格式列表
- `subtitles`: 可用字幕
- `automatic_captions`: 自动生成的字幕

向用户展示：
- 视频标题
- 时长
- 可用的视频质量（如 1080p, 720p, 480p 等）
- 可用的音频格式
- 可用的字幕语言

如果解析失败，可能是需要登录或视频不可用，告知用户具体原因。

### Step 3: 询问用户下载选项

**⚠️ 必须：使用 AskUserQuestion 工具收集用户的偏好。不要跳过这一步。**

使用 AskUserQuestion 工具收集以下信息：

1. **下载内容**：你想下载什么？
   - 选项：
     - "视频+音频 - 完整视频文件 (Recommended)"
     - "仅音频 - MP3/M4A 格式"
     - "仅字幕 - SRT/VTT 格式"
     - "视频+音频+字幕 - 全部下载"

2. **视频质量**（如果选择下载视频）：选择视频质量
   - 选项：
     - "最高质量 (Recommended)"
     - "1080p - Full HD"
     - "720p - HD"
     - "480p - SD（节省空间）"
     - "最低质量（最小文件）"

3. **音频格式**（如果选择仅下载音频）：选择音频格式
   - 选项：
     - "MP3 - 通用格式 (Recommended)"
     - "M4A - 高质量"
     - "最佳质量（保持原始格式）"

4. **字幕语言**（如果有字幕可用）：选择字幕语言
   - 根据解析结果动态生成选项
   - 常见选项：中文、英文、日文、自动生成字幕

5. **输出路径**：保存到哪里？
   - 建议默认：当前目录
   - 让用户可以自定义路径

### Step 4: 构建 yt-dlp 命令

根据用户选择，构建 yt-dlp 命令：

#### 基础选项（始终使用）

```bash
--cookies-from-browser chrome  # 使用 Chrome cookies
-o "%(title)s.%(ext)s"         # 输出文件名格式
--no-playlist                   # 不下载播放列表
```

#### 视频+音频下载

```bash
# 最高质量
uvx yt-dlp --cookies-from-browser chrome -f "bestvideo+bestaudio/best" --merge-output-format mp4 -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"

# 指定分辨率
uvx yt-dlp --cookies-from-browser chrome -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" --merge-output-format mp4 -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"

# 720p
uvx yt-dlp --cookies-from-browser chrome -f "bestvideo[height<=720]+bestaudio/best[height<=720]" --merge-output-format mp4 -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"
```

#### 仅下载音频

```bash
# MP3 格式
uvx yt-dlp --cookies-from-browser chrome -x --audio-format mp3 --audio-quality 0 -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"

# M4A 格式
uvx yt-dlp --cookies-from-browser chrome -x --audio-format m4a --audio-quality 0 -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"

# 最佳质量（原始格式）
uvx yt-dlp --cookies-from-browser chrome -x --audio-quality 0 -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"
```

#### 仅下载字幕

```bash
# 下载所有字幕
uvx yt-dlp --cookies-from-browser chrome --write-subs --skip-download -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"

# 下载特定语言字幕
uvx yt-dlp --cookies-from-browser chrome --write-subs --sub-langs "zh,en" --skip-download -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"

# 下载自动生成的字幕
uvx yt-dlp --cookies-from-browser chrome --write-auto-subs --sub-langs "zh,en" --skip-download -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"

# 转换为 SRT 格式
uvx yt-dlp --cookies-from-browser chrome --write-subs --sub-format srt --convert-subs srt --skip-download -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"
```

#### 视频+字幕一起下载

```bash
uvx yt-dlp --cookies-from-browser chrome -f "bestvideo+bestaudio/best" --merge-output-format mp4 --write-subs --sub-langs "zh,en" --embed-subs -o "OUTPUT_PATH/%(title)s.%(ext)s" "URL"
```

### Step 5: 执行下载

1. 执行前向用户展示完整的 yt-dlp 命令
2. 执行命令并显示下载进度
3. 报告成功/失败

### Step 6: 验证输出

下载完成后：

```bash
ls -la "OUTPUT_PATH"
```

报告：
- 下载的文件名和大小
- 如果下载了字幕，列出字幕文件
- 任何警告或问题

### 常见问题处理

**需要登录的内容**：
- 确保用户已在 Chrome 中登录对应网站
- 如果仍然失败，建议用户手动导出 cookies

**地区限制**：
- 提示用户可能需要使用代理
- 使用 `--geo-bypass` 尝试绕过限制

**下载失败**：
- 检查 URL 是否正确
- 尝试更新 yt-dlp：`uvx --refresh yt-dlp --version`
- 检查网络连接

### 示例交互

用户：帮我下载这个 YouTube 视频 https://www.youtube.com/watch?v=xxx

助手：
1. 解析视频信息，展示标题、时长、可用质量
2. 使用 AskUserQuestion 询问下载选项
3. 执行下载（使用 uvx yt-dlp）
4. 报告结果

### 交互风格

- 使用简单友好的语言
- 清晰展示视频信息和可用选项
- 如果遇到错误，提供清晰的解决方案
- 下载成功后给予积极反馈
