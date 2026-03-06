---
name: yt-search-download
description: |
  YouTube 视频搜索、下载视频、下载字幕工具。结合 YouTube Data API v3 进行高级搜索，yt-dlp 下载视频/音频/字幕。
  核心能力：全站关键词搜索、频道浏览、按时间/播放量/相关度排序、下载视频、提取音频（MP3）、下载字幕（中英文）、查看视频详情。
  触发场景（任何涉及 YouTube 的操作都应使用此 skill）：
  - 搜索类："搜索YouTube"、"YouTube搜索"、"找YouTube视频"、"搜索[频道名]最新视频"、"查找[人名]的YouTube"、"[人名]最近更新的YouTube"、"YouTube上有什么关于XXX的"
  - 频道浏览类："浏览频道"、"看看[频道名]最新视频"、"[人名]最近发了什么视频"、"[人名]YouTube更新"、"查看[频道名]的视频列表"
  - 下载视频类："下载YouTube"、"下载这个视频"、"下载YouTube视频"、"把这个视频下载下来"、"保存视频"
  - 下载音频类："提取音频"、"下载音频"、"YouTube转MP3"、"只要音频"
  - 下载字幕类："下载字幕"、"提取字幕"、"获取字幕"、"下载YouTube字幕"、"中文字幕"、"英文字幕"、"提取文字"、"视频转文字"、"获取视频文本"
  - 视频信息类："视频详情"、"视频信息"、"这个视频多长"
  关键词匹配：只要用户消息中出现 "YouTube"、"油管"、"YT"、"yt" 加上搜索/下载/字幕/频道/视频等动作词，就应触发此 skill。
---

# YouTube 搜索 & 下载

基于 YouTube Data API v3 进行高级搜索，配合 yt-dlp 下载。

## 前置条件

1. **YouTube API Key**：
   ```bash
   echo $YT_BROWSE_API_KEY
   ```
   如果为空：[Google Cloud Console](https://console.cloud.google.com/) → 启用 YouTube Data API v3 → 创建 API Key → 写入 `~/.zshrc`：
   ```bash
   export YT_BROWSE_API_KEY=your_key
   ```

2. **yt-dlp**（下载用）：
   ```bash
   brew install yt-dlp   # macOS
   pip install yt-dlp     # 或 pip 安装
   ```

## 命令说明

脚本路径：`~/.claude/skills/yt-search-download/scripts/yt_search.py`

### 全站关键词搜索

```bash
python3 scripts/yt_search.py search "关键词" -n 20
```

| 参数 | 说明 |
|------|------|
| `-n 20` | 最多返回条数（默认 20） |
| `-o date` | 按时间排序（默认 relevance） |
| `-o viewCount` | 按播放量排序（API 级，准确） |
| `--sort-by views` | 本地二次排序（按播放量降序） |
| `--sort-by duration-asc` | 本地排序：时长从短到长 |
| `--sort-by duration-desc` | 本地排序：时长从长到短 |
| `--min-duration 30m` | 过滤：最短时长（支持 `30m`、`1h`、`1h30m`、纯数字=分钟） |
| `--max-duration 1h` | 过滤：最长时长 |
| `--after 2024-01-01` | 发布时间起 |
| `--before 2024-12-31` | 发布时间止 |
| `-c @handle` | 限定频道 |
| `-d` | 显示简介 |
| `--json` | JSON 格式输出 |

### 浏览频道视频

```bash
# 频道最新视频（按时间倒序）
python3 scripts/yt_search.py channel @channelHandle -n 10

# 频道内关键词搜索
python3 scripts/yt_search.py channel @channelHandle -q "关键词"

# 频道内按播放量排序
python3 scripts/yt_search.py channel @channelHandle -o viewCount

# 只看长视频（超过 1 小时）
python3 scripts/yt_search.py channel @channelHandle --min-duration 1h

# 只看短视频（30 分钟内），按时长升序
python3 scripts/yt_search.py channel @channelHandle --max-duration 30m --sort-by duration-asc
```

频道格式支持：`@handle`、`https://youtube.com/@handle`、频道 ID（`UCxxxx`）

### 下载视频

```bash
# 最佳画质下载到 ~/Downloads
python3 scripts/yt_search.py download "VIDEO_URL"

# 指定画质
python3 scripts/yt_search.py download "VIDEO_URL" -q 1080p

# 指定目录
python3 scripts/yt_search.py download "VIDEO_URL" --dir ~/Desktop

# 仅下载音频（MP3）
python3 scripts/yt_search.py download "VIDEO_URL" --audio-only
```

### 视频详情查询

```bash
python3 scripts/yt_search.py info "VIDEO_URL"
```

## 输出格式（Markdown 表格）

脚本已输出 Markdown 表格，AI **必须将每行的 `【译】___` 替换为实际中文翻译**后再呈现给用户。

最终呈现效果：

| # | 标题（原文 → 中文译文） | 日期 | 时长 | 播放量 |
|---|------------------------|------|------|--------|
| 1 | [Rick Beato: Greatest Guitarists...](url)<br>里克·贝阿托：史上最伟大的吉他手 | 2026-03-01 | 2h33m | 302.2K |
| 2 | [State of AI in 2026: LLMs, Coding...](url)<br>2026年AI现状：大模型、编程、Scaling法则 | 2026-01-31 | 4h25m | 741.7K |

**🔴 强制规范**：
- ✅ 保留原英文标题（作为可点击链接）
- ✅ `【译】___` 替换为简洁中文译文（放在链接后同一单元格）
- ✅ 所有视频逐行翻译，不得跳过
- ❌ 不询问用户是否需要翻译（直接翻译）
- ❌ 不把 `【译】___` 原样输出给用户

## 典型工作流

**找某频道最新视频并下载：**
1. `channel @handle -n 10` → 浏览结果
2. 问用户要下载哪个
3. `download "URL"` → 保存到 ~/Downloads

**搜索 + 按播放量筛选：**
1. `search "关键词" -o viewCount -n 20`

**提取播客音频：**
1. `search "播客名" -o date -n 5`
2. `download "URL" --audio-only`

### 下载字幕（默认同时输出 SRT + TXT）

**标准流程**：下载字幕转为 SRT，同时生成保留时间戳的 TXT（供 AI 总结用，时间戳有助于定位内容）。

```bash
# Step 1：下载字幕并转为 SRT（英文优先，无则用自动字幕）
yt-dlp --cookies-from-browser chrome \
  --write-auto-sub --write-sub \
  --sub-lang en,zh-Hans \
  --convert-subs srt \
  --skip-download \
  -o "~/Downloads/%(title)s.%(ext)s" \
  "VIDEO_URL"
# 输出：~/Downloads/视频标题.en.srt 或 .zh-Hans.srt

# Step 2：从 SRT 生成 TXT（保留时间戳，仅去除序号和空行，供 AI 总结使用）
python3 -c "
import re, sys
srt = open(sys.argv[1]).read()
# 去除序号行（纯数字行），保留时间戳和字幕文本
txt = re.sub(r'^\d+\s*\n', '', srt, flags=re.MULTILINE)
txt = re.sub(r'\n{3,}', '\n\n', txt).strip()
txt_path = sys.argv[1].replace('.srt', '.txt')
open(txt_path, 'w').write(txt)
print(f'已保存：{txt_path}')
" ~/Downloads/视频标题.en.srt
# 输出：~/Downloads/视频标题.en.txt（格式：时间戳 + 字幕文本）
```

TXT 格式示例（保留时间戳，便于 AI 总结时引用具体时间点）：
```
00:00:01,000 --> 00:00:04,000
Welcome to the Lex Fridman podcast.

00:00:05,000 --> 00:00:09,000
Today we're talking about the greatest guitarists of all time.
```

**其他场景**：
```bash
# 仅中文字幕（SRT + TXT）
yt-dlp --cookies-from-browser chrome --write-auto-sub --write-sub \
  --sub-lang zh-Hans --convert-subs srt --skip-download \
  -o "~/Downloads/%(title)s.%(ext)s" "VIDEO_URL"

# 字幕 + 视频一起下载
yt-dlp --cookies-from-browser chrome --write-auto-sub --write-sub \
  --sub-lang en --convert-subs srt \
  -o "~/Downloads/%(title)s.%(ext)s" "VIDEO_URL"
```

> **规范**：下载字幕时**始终加 `--convert-subs srt`**，下载完成后**始终执行 Step 2 生成 TXT**，让用户同时拿到 `.srt`（带时间轴）和 `.txt`（纯文本）两个文件。

## 高级用法（直接用 yt-dlp）

```bash
# 列出可用格式
yt-dlp --cookies-from-browser chrome -F "VIDEO_URL"

# 下载整个播放列表
yt-dlp --cookies-from-browser chrome -o "~/Downloads/%(playlist_title)s/%(title)s.%(ext)s" "PLAYLIST_URL"
```
