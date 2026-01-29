---
name: bilibili-subtitle
description: 从 Bilibili 视频提取字幕、转录无字幕视频、生成结构化摘要。触发条件：Bilibili URL (bilibili.com)、BV ID (BV1xxx)、或"提取B站字幕"等请求。
user-invocable: true
---

# Bilibili 字幕提取工具

从 Bilibili 视频提取字幕，支持 AI 字幕检测和 ASR 转录回退。

## Quick Reference

| 任务 | 命令 |
|------|------|
| 基本提取 | `pixi run python -m bilibili_subtitle "BV1234567890"` |
| 快速模式 | `pixi run python -m bilibili_subtitle "URL" --skip-proofread --skip-summary` |
| 双语输出 | `pixi run python -m bilibili_subtitle "URL" --output-lang zh+en` |
| 指定目录 | `pixi run python -m bilibili_subtitle "URL" -o ./subtitles` |

## 前置条件

### 1. 安装

```bash
cd ~/.agents/skills/bilibili-subtitle
./install.sh
pixi shell
```

### 2. 外部工具

| 工具 | 用途 | 安装 |
|------|------|------|
| BBDown | 视频信息/字幕下载 | `brew install bbdown` |
| ffmpeg | 音频转换 | `brew install ffmpeg` |

### 3. API Keys

| Key | Provider | 用途 |
|-----|----------|------|
| `ANTHROPIC_API_KEY` | [Anthropic](https://console.anthropic.com/) | 校对/翻译/摘要 |
| `DASHSCOPE_API_KEY` | [阿里云 DashScope](https://dashscope.console.aliyun.com/) | ASR 转录（仅无字幕时需要） |

```bash
# 添加到 ~/.zshrc
export ANTHROPIC_API_KEY="your-key"
export DASHSCOPE_API_KEY="your-key"  # 可选
```

### 4. BBDown 认证

```bash
BBDown login  # 扫码登录，Cookie 保存在 BBDown.data
```

## 触发方式

- `/bilibili-subtitle [URL]`
- "提取这个B站视频的字幕 [URL]"
- "把这个视频转成文字 BV1234567890"
- "生成这个视频的摘要 [URL]"

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | Bilibili URL 或 BV ID | 必填 |
| `--output-dir, -o` | 输出目录 | `./output` |
| `--output-lang` | 输出语言 `zh`/`en`/`zh+en` | `zh` |
| `--skip-proofread` | 跳过校对 | false |
| `--skip-summary` | 跳过摘要 | false |
| `--cache-dir` | 缓存目录 | `./.cache` |
| `--verbose, -v` | 详细输出 | false |

## 输出文件

```
output/
├── {video_id}.zh.srt          # SRT 字幕
├── {video_id}.zh.vtt          # VTT 字幕
├── {video_id}.transcript.md   # Markdown 逐字稿
├── {video_id}.summary.json    # 结构化摘要
└── {video_id}.summary.md      # 摘要 (Markdown)
```

## 处理流程

```
URL → BBDown 检测 → [有字幕?]
                     ├─ YES → 加载 SRT → 校对 → 输出
                     └─ NO  → 下载音频 → ASR 转录 → 校对 → 输出
```

## Progress Updates

```
⏳ 检测视频字幕: BV1234567890
✅ 视频ID: BV1234567890
   标题: 视频标题
   有字幕: True
⏳ 加载字幕文件...
✅ 加载 120 个字幕段落
⏳ 校对字幕...
✅ 校对完成，修改 5 处
⏳ 生成输出文件...
✅ SRT: output/BV1234567890.zh.srt
✅ VTT: output/BV1234567890.zh.vtt
✅ MD:  output/BV1234567890.transcript.md
⏳ 生成摘要...
✅ Summary JSON: output/BV1234567890.summary.json
✅ Done! 输出目录: ./output
```

## 错误处理

### 1. BBDown 未安装
- **错误**: `command not found: BBDown`
- **原因**: BBDown 未安装或不在 PATH 中
- **解决**: `brew install bbdown` 或从 GitHub 下载

### 2. BBDown 认证失败
- **错误**: `需要登录` 或下载失败
- **原因**: Cookie 过期或未登录
- **解决**: 运行 `BBDown login` 重新扫码

### 3. ASR 转录失败
- **错误**: `Missing DASHSCOPE_API_KEY`
- **原因**: 视频无字幕且未配置 DashScope
- **解决**: 设置 `DASHSCOPE_API_KEY` 环境变量

### 4. 校对/摘要失败
- **错误**: `Missing ANTHROPIC_API_KEY`
- **原因**: 未配置 Anthropic API
- **解决**: 设置 `ANTHROPIC_API_KEY` 或使用 `--skip-proofread --skip-summary`

## 示例

### 基本用法

```bash
pixi run python -m bilibili_subtitle "https://www.bilibili.com/video/BV1234567890/"
```

### 快速提取（跳过 AI 处理）

```bash
pixi run python -m bilibili_subtitle "BV1234567890" --skip-proofread --skip-summary -v
```

### 双语输出

```bash
pixi run python -m bilibili_subtitle "BV1234567890" --output-lang zh+en
```

---

**版本**: v0.1.0
