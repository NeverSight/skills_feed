---
name: yt-dlp
description: 强大的视频下载工具，支持 YouTube 和 1000+ 网站，自动选择最佳格式、字幕下载、播放列表处理
license: MIT
category: media-processing
tags: [video-download, youtube, bilibili, subtitle, media]
---

# yt-dlp 视频下载 Skill

基于 yt-dlp 的专业视频下载工具，支持 YouTube、Bilibili、Twitter、Instagram 等 1000+ 网站。

## 适用场景

- 下载 YouTube 视频（含 4K/8K、HDR）
- 下载 Bilibili 视频（自动登录）
- 下载社交媒体视频（Twitter、Instagram、TikTok）
- 批量下载播放列表/频道视频
- 提取音频（制作播客、音乐收藏）
- 下载视频字幕（用于翻译、学习）

## 核心特性

- **格式智能选择**: 自动选择最佳质量（视频+音频或仅视频）
- **字幕处理**: 自动下载可用字幕（支持多语言）
- **播放列表支持**: 批量下载，支持断点续传
- **元数据保留**: 保存标题、上传时间、描述等信息
- **模板化命名**: 自定义文件名格式（避免乱码）
- **代理支持**: 支持 HTTP/SOCKS 代理
- **速度限制**: 可控制下载速度，避免被限流

## 使用方式

### 基础用法

```bash
# 直接下载视频（最佳质量）
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# 下载到指定目录
yt-dlp -o "Downloads/%(title)s.%(ext)s" "URL"

# 仅下载音频（最佳质量 MP3）
yt-dlp -x --audio-format mp3 "URL"

# 下载字幕
yt-dlp --write-subs --sub-langs all "URL"
```

### 高级选项

```bash
# 选择特定质量
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "URL"

# 下载播放列表
yt-dlp -o "%(playlist_index)s-%(title)s.%(ext)s" "PLAYLIST_URL"

# 批量下载（从文件读取 URL）
yt-dlp -a urls.txt

# 限制下载速度（避免被封）
yt-dlp --limit-rate 1M "URL"

# 使用代理
yt-dlp --proxy http://127.0.0.1:7890 "URL"

# 下载后不合并（保留分离的视频/音频）
yt-dlp --keep-video "URL"
```

### 常用输出模板

```bash
# 保留原视频标题
-o "%(title)s.%(ext)s"

# 包含上传者信息
-o "%(uploader)s/%(title)s.%(ext)s"

# 包含上传日期
-o "%(upload_date)s-%(title)s.%(ext)s"

# 播放列表序号
-o "%(playlist_index)s-%(title)s.%(ext)s"

# 完整元数据（用于整理）
-o "%(uploader)s/%(upload_date)s-%(title)s-[%(id)s].%(ext)s"
```

## AI 辅助工作流

当用户提供视频链接时，AI 应按以下流程处理：

### 0. 前置检查：FFmpeg 依赖检测

**重要**: FFmpeg 是 yt-dlp 的必需依赖，必须在执行下载前检测并确保已安装。

**检测步骤**:

1. **检测 FFmpeg 是否已安装**:
   ```bash
   # macOS/Linux
   ffmpeg -version

   # Windows
   ffmpeg -version
   ```

2. **如果已安装**: 显示版本信息，继续执行下一步
   ```
   ✅ FFmpeg 已安装: ffmpeg version N-xxxxx
   ```

3. **如果未安装**: 立即停止，提示用户安装

   **根据操作系统提供安装指令**:

   - **macOS**:
     ```bash
     # 使用 Homebrew
     brew install ffmpeg

     # 或使用 MacPorts
     sudo port install ffmpeg
     ```

   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

   - **Linux (Arch/Manjaro)**:
     ```bash
     sudo pacman -S ffmpeg
     ```

   - **Linux (Fedora)**:
     ```bash
     sudo dnf install ffmpeg
     ```

   - **Windows**:
     ```bash
     # 使用 Scoop
     scoop install ffmpeg

     # 使用 Chocolatey
     choco install ffmpeg

     # 或从官网下载: https://ffmpeg.org/download.html
     ```

   - **验证安装**:
     ```bash
     ffmpeg -version
     ```

4. **安装后验证**: 重新执行检测命令，确认成功后才继续

**AI 应遵守的规则**:
- ❌ 如果 FFmpeg 未安装，**绝不**执行 yt-dlp 下载命令
- ✅ 必须明确告知用户为什么需要 FFmpeg（视频/音频合并、格式转换）
- ✅ 提供与用户操作系统匹配的安装命令
- ✅ 等待用户确认安装完成后才继续

### 1. 识别需求

询问用户（如果未明确说明）：
- 是否需要音频还是视频？
- 需要什么质量（1080p/4K/最佳）？
- 是否需要字幕？
- 是否需要元数据（缩略图、描述、info.json）？

### 2. 构建命令

根据需求自动生成 `yt-dlp` 命令：
- 自动检测网站类型
- 选择最佳格式选项
- 添加必要的参数
- 输出文件名模板

### 3. 执行下载

在用户的下载目录执行命令：
- Windows: `%USERPROFILE%/Downloads`
- macOS: `~/Downloads`
- Linux: `~/Downloads`

### 4. 验证结果

检查下载文件：
- 文件完整性
- 格式正确性
- 字幕存在性

## 常用场景命令

### YouTube 高清视频

```bash
# 1080p 视频 + 音频
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  -o "%(title)s.%(ext)s" "URL"

# 4K 视频
yt-dlp -f "bestvideo[height<=2160]+bestaudio/best[height<=2160]" \
  -o "%(title)s.%(ext)s" "URL"
```

### Bilibili 视频

```bash
# 需要 cookie（登录后导出）
yt-dlp --cookies cookies.txt \
  -o "%(title)s.%(ext)s" "URL"

# 下载弹幕（需要专用脚本）
yt-dlp --write-info-json "URL"
```

### 播客/音频提取

```bash
# 最佳质量 MP3
yt-dlp -x --audio-format mp3 \
  --audio-quality 0 \
  -o "%(title)s.%(ext)s" "URL"

# 批量下载播客列表
yt-dlp -x --audio-format mp3 \
  -o "%(playlist_index)s-%(title)s.%(ext)s" \
  "PLAYLIST_URL"
```

### 字幕下载

```bash
# 下载所有可用字幕
yt-dlp --write-subs --sub-langs all \
  --skip-download "URL"

# 下载内嵌字幕视频
yt-dlp --embed-subs --sub-langs en,zh "URL"

# 仅字幕（不下载视频）
yt-dlp --write-subs --skip-download "URL"
```

## 格式选择语法

```bash
# 格式选择代码
bestvideo+bestaudio    # 最佳视频+音频（分别下载后合并）
best                   # 最佳单文件（已合并）
worst                  # 最差质量（用于测试）

# 过滤器
bestvideo[height<=1080]      # 最高 1080p
bestvideo[fps<=30]           # 最高 30fps
bestvideo[filesize<500M]     # 小于 500MB
bestvideo[acodec=opus]       # 指定音频编码

# 组合
bestvideo[height<=1080]+bestaudio/best[height<=1080]

# 备选方案（从前到后尝试）
bestvideo+bestaudio/best
```

## 常见网站支持

| 网站 | 支持情况 | 特殊说明 |
|------|---------|---------|
| YouTube | ✅ 完全支持 | 需要代理（某些地区） |
| Bilibili | ✅ 支持 | 需要 cookie |
| Twitter/X | ✅ 支持 | - |
| Instagram | ✅ 支持 | - |
| TikTok | ✅ 支持 | - |
| Vimeo | ✅ 支持 | - |
| Twitch | ✅ 支持 | - |
| Coursera | ✅ 支持 | 需要登录 |
| Netflix | ⚠️ 有限支持 | 需要特定工具 |

## 配置文件

### 全局配置

创建 `~/.config/yt-dlp/config` (Linux/macOS) 或 `%APPDATA%\yt-dlp\config.txt` (Windows):

```ini
# 默认输出目录
-o ~/Downloads/%(title)s.%(ext)s

# 默认格式
-f bestvideo+bestaudio/best

# 下载字幕
--write-subs
--sub-langs en,zh

# 限制并发
--concurrent-fragments 4

# 速度限制
--limit-rate 2M
```

### 项目级配置

在项目目录创建 `yt-dlp.conf`:

```ini
# 项目特定配置
-o ./videos/%(title)s.%(ext)s
--cookies cookies.txt
--download-archive downloaded.txt
```

## 最佳实践

### 1. 网络稳定性

```bash
# 使用 aria2 作为下载器（支持断点续传）
yt-dlp --external-downloader aria2 \
  --external-downloader-args "-x 8 -k 1M" "URL"

# 重试机制
yt-dlp --retries 10 --fragment-retries 10 "URL"
```

### 2. 避免被封

```bash
# 限制速度
yt-dlp --limit-rate 1M "URL"

# 使用代理池
yt-dlp --proxy socks5://127.0.0.1:1080 "URL"

# 模拟浏览器
yt-dlp --user-agent "Mozilla/5.0..." "URL"
```

### 3. 元数据保留

```bash
# 保存所有元数据
yt-dlp --write-info-json --write-description \
  --write-thumbnail --embed-subs "URL"

# 下载为 mkv（支持所有元数据）
yt-dlp --merge-output-format mkv "URL"
```

### 4. 批量处理

```bash
# 从文件读取 URL
yt-dlp -a urls.txt -o "%(title)s.%(ext)s"

# 批量下载播放列表（断点续传）
yt-dlp --download-archive archive.txt \
  -o "%(title)s.%(ext)s" "PLAYLIST_URL"
```

## 常见问题

### Q: 下载速度慢？

A: 尝试以下方法：
- 使用 `--limit-rate` 限制速度
- 使用代理 `--proxy`
- 切换格式选择（避免需要合并）
- 使用 `--concurrent-fragments` 增加并发

### Q: 视频和音频分离？

A: 使用以下任一方法：
```bash
# 方法1：指定合并格式
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mp4 "URL"

# 方法2：使用 FFmpeg 合并
yt-dlp -f bestvideo+bestaudio --keep-video "URL"
ffmpeg -i video.mp4 -i audio.m4v -c copy output.mp4
```

### Q: 如何下载付费/会员内容？

A: 需要 cookie：
1. 使用浏览器插件导出 cookie（如 "Get cookies.txt"）
2. 使用 `--cookies cookies.txt` 参数
3. 注意：cookie 会过期，需要定期更新

### Q: Bilibili 下载失败？

A: 常见解决方案：
```bash
# 使用 cookie
yt-dlp --cookies cookies.txt "URL"

# 使用 CNCore 提取器
yt-dlp --extractor-args "bilivideo:session_data=..." "URL"

# 参考：https://github.com/yt-dlp/yt-dlp/wiki/Installation
```

### Q: 如何下载直播？

A:
```bash
# 从当前开始下载
yt-dlp "URL"

# 从直播开始时下载（需要录制）
yt-dlp --live-from-start "URL"

# 等待直播开始
yt-dlp --wait-for-video "URL"
```

## 技术细节

### 依赖项

- **FFmpeg**: 必需（用于视频/音频合并、格式转换）
- **Python 3.8+**: 运行环境
- **RAR** (可选): 用于某些网站的下载

### 安装

```bash
# pip 安装
pip install yt-dlp

# 包管理器（推荐）
# macOS
brew install yt-dlp

# Linux (Arch)
pacman -S yt-dlp

# Windows (Scoop)
scoop install yt-dlp

# 更新
yt-dlp --update
```

### AI 辅助检查清单

在生成下载命令前，确认：

- [ ] 网站是否受支持
- [ ] 是否需要 cookie/代理
- [ ] 用户需要的质量/格式
- [ ] 输出目录和文件名
- [ ] 是否需要字幕
- [ ] 是否需要元数据

### AI 输出格式

生成的命令应包含：
1. 命令说明（做什么）
2. 完整命令（可复制粘贴）
3. 参数解释（为什么这样选择）
4. 预期结果（会得到什么文件）
5. 注意事项（可能的错误）

示例：
```markdown
## 下载 YouTube 视频（1080p）

**命令说明**: 下载 1080p 视频和最佳音频，自动合并为 MP4

**完整命令**:
```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  -o "%(title)s.%(ext)s" \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**参数解释**:
- `-f "bestvideo[height<=1080]+bestaudio"`: 选择最高 1080p 视频和最佳音频
- `-o "%(title)s.%(ext)s"`: 文件名使用原视频标题
- 自动合并为单个 MP4 文件

**预期结果**: `Downloads/Rick Astley - Never Gonna Give You Up.mp4`

**注意事项**:
- 需要 FFmpeg 已安装
- 下载速度取决于网络和 YouTube 限制
- 如需 4K，将 `1080` 改为 `2160`
```

## 进阶技巧

### 自定义提取器

```bash
# 使用特定提取器
yt-dlp --extractor-args "youtube:player_client=android" "URL"

# 跳过年龄验证
yt-dlp --extractor-args "youtube:player_client=ios" "URL"
```

### 播放列表过滤

```bash
# 仅下载前 10 个
yt-dlp --playlist-end 10 "PLAYLIST_URL"

# 下载特定范围
yt-dlp --playlist-start 5 --playlist-end 15 "PLAYLIST_URL"

# 反向播放列表
yt-dlp --playlist-reverse "PLAYLIST_URL"

# 随机顺序
yt-dlp --playlist-random "PLAYLIST_URL"
```

### 信息提取

```bash
# 仅查看可用格式（不下载）
yt-dlp --list-formats "URL"

# 查看 JSON 信息
yt-dlp --dump-json "URL"

# 查看播放列表信息
yt-dlp --flat-playlist --print "%(title)s" "PLAYLIST_URL"
```

## 参考资源

- [官方文档](https://github.com/yt-dlp/yt-dlp)
- [格式选择语法](https://github.com/yt-dlp/yt-dlp#format-selection)
- [支持网站列表](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- [Wiki](https://github.com/yt-dlp/yt-dlp/wiki)

## 许可证

MIT License - 自由使用、修改和分发

## 贡献

欢迎提交 Issue 和 Pull Request 改进此 Skill！

---

**注意**: 请遵守目标网站的服务条款和版权法律。仅下载您有权访问的内容。
