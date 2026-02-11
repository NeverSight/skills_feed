---
name: video-copy-analyzer
description: >
  视频文案分析一站式工具。下载在线视频（B站/YouTube/抖音等）、使用FunASR Nano进行中文语音转录、
  自动校正文稿、并进行三维度综合分析（TextContent/Viral/Brainstorming）。
  使用场景：当用户需要分析短视频文案、提取视频内容、学习爆款文案技巧时。
  关键词：视频分析、文案分析、语音转文字、FunASR、Whisper、爆款分析、视频下载
---

# 视频文案分析工具

一站式视频内容提取与文案分析，支持 B站、YouTube、抖音 等平台。

## 首次使用设置

首次使用时，询问用户：

> "请设置默认工作目录（用于保存下载的视频和分析报告）：
> 
> A. 使用默认目录：`~/video-analysis/`
> B. 每次手动指定目录
> C. 指定一个固定目录：[请输入路径]"

保存用户选择供后续使用。

## 依赖环境检测

运行前检测以下依赖，如缺失则提示安装：

```bash
# 1. yt-dlp
yt-dlp --version

# 2. FFmpeg
ffmpeg -version

# 3. Python 依赖
python -c "import pysrt; from dotenv import load_dotenv; print('OK')"

# 4. RapidOCR (用于烧录字幕识别，ONNX 轻量版)
python -c "from rapidocr_onnxruntime import RapidOCR; print('OK')"

# 5. FunASR (中文语音转录，推荐)
python -c "from funasr import AutoModel; print('OK')"

# 6. requests (用于抖音下载)
python -c "import requests; print('OK')"
```

**安装命令（如缺失）**：
```bash
# 基础依赖
pip install yt-dlp pysrt python-dotenv requests

# FunASR (中文语音转录，轻量且效果好)
pip install funasr modelscope

# RapidOCR (ONNX 轻量版，用于烧录字幕识别)
pip install rapidocr-onnxruntime

# Whisper (备选方案)
pip install openai-whisper
```

## 工作流程（4 阶段）

### 阶段 1: 下载视频

1. 获取用户视频 URL 和输出目录
2. **判断视频平台**：
   - **抖音链接**（douyin.com 或 v.douyin.com）：使用专用脚本下载
   - **其他平台**（B站、YouTube等）：使用 yt-dlp 下载

#### 抖音视频下载

对于抖音链接，使用 `scripts/download_douyin.py`：

```bash
python scripts/download_douyin.py "<抖音链接>" "<输出路径>"
```

**支持的抖音链接格式**：
- 短链接：`https://v.douyin.com/xxxxx`
- 长链接：`https://www.douyin.com/video/xxxxx`
- 精选页：`https://www.douyin.com/jingxuan?modal_id=xxxxx`
- 分享链接：`https://m.douyin.com/share/video/xxxxx`

**下载流程**：
```
抖音链接
    ↓
[Mobile UA 访问] ──→ 获取重定向后页面
    ↓
[提取 RENDER_DATA] ──→ 解析视频元数据
    ↓
[提取 play_addr] ──→ 获取无水印视频URL
    ↓
[下载视频] ──→ 保存到指定路径
```

#### 其他平台下载（yt-dlp）

对于 B站、YouTube 等平台：

```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --merge-output-format mp4 \
  -o "<output_dir>/%(id)s.%(ext)s" \
  "<video_url>"
```

3. 记录视频文件路径

### 阶段 2: 智能字幕提取

使用 scripts/extract_subtitle_funasr.py 进行智能字幕提取，自动选择最佳方案：

```bash
python scripts/extract_subtitle_funasr.py <视频路径> <输出SRT路径>
```

**智能提取流程（三层优先级）**：

```
视频输入
    ↓
[1️⃣ 内嵌字幕检测] ──→ 检测到字幕流 ──→ 直接提取（准确度最高）
    ↓ 未检测到
[2️⃣ 烧录字幕检测] ──→ 采样帧 OCR 识别 ──→ 检测到文字 ──→ 全视频 OCR 提取
    ↓ 未检测到
[3️⃣ FunASR 语音转录] ──→ 中文优化转录（效果优于 Whisper）
    ↓
输出 SRT 字幕
```

**三层提取策略详解**：

| 层级 | 方法 | 适用场景 | 准确度 | 速度 |
|------|------|---------|--------|------|
| **L1** | 内嵌字幕提取 | 视频自带字幕流 | ⭐⭐⭐⭐⭐ | ⚡ 极快 |
| **L2** | RapidOCR 烧录字幕识别 | 字幕烧录在画面中 | ⭐⭐⭐⭐ | 🚀 快 |
| **L3** | FunASR Nano 语音转录 | 无字幕，纯语音 | ⭐⭐⭐ | 🐢 中等 |

**技术栈说明**：

- **RapidOCR (ONNX)**: 用于检测和提取烧录在视频画面中的字幕
  - 🚀 轻量级：ONNX Runtime 推理，无需 GPU
  - 🎯 跨平台：Windows/Linux/Mac 均支持
  - 📦 易部署：单 pip 安装，无复杂依赖
  - ✨ 高精度：基于 PaddleOCR 模型优化

- **FunASR Nano**: 阿里开源中文语音识别模型
  - 🚀 轻量级：~100MB vs Whisper Large ~1.5GB
  - 🎯 中文优化：针对中文语音专门训练，效果优于 Whisper
  - ⏱️ 时间戳：支持字级别时间戳
  - 💨 速度快：CPU 上也能快速运行

**备选方案**：

如需使用 Whisper（英文内容推荐）：
```bash
python scripts/extract_subtitle.py <视频路径> <输出SRT路径>
```

如需手动控制，可使用原 transcribe_audio.py：
```bash
python scripts/transcribe_audio.py <视频路径> <输出SRT路径> [模型] [语言] [设备]
```

### 阶段 3: 文稿校正

1. 读取 SRT 字幕文件
2. 合并字幕为连续文本
3. 基于上下文语义进行智能校正：
   - 修正同音字错误
   - 修正专业术语
   - 补充标点符号
4. 输出校正后的文字稿（Markdown 格式）

**校正输出格式**：
```markdown
# 视频语音转录文字稿

**视频来源**: [URL]
**转录时间**: [日期]

---

## 完整文字稿

[校正后的正文内容]

---

## 原始 SRT 字幕

[带时间戳的原始转录]
```

### 阶段 4: 三维度综合分析

应用三个分析框架进行深度分析：

#### 4.1 TextContent Analysis 视角
- 叙事结构分析
- 叙事声音分析
- 修辞手法识别
- 词库提取

#### 4.2 Viral-Abstract-Script 视角
- Viral-5D 框架诊断（Hook/Emotion/爆点/CTA/社交货币）
- 风格定位
- 爆款潜力评估
- 优化建议

#### 4.3 Brainstorming 视角
- 核心价值拆解
- 2-3 种创意方向探索
- 增量验证点

**分析输出格式**：
```markdown
# 视频文案综合分析报告（三维度）

## 一、TextContent Analysis 视角
[叙事结构、修辞手法、词库]

## 二、Viral-Abstract-Script 视角
[Viral-5D诊断、风格定位、优化建议]

## 三、Brainstorming 视角
[价值拆解、创意方向、验证点]

## 四、综合评估与建议
[评分、改进建议、改写示例]
```

## 完成后输出

完成所有阶段后，向用户播报：

```
✅ 视频文案分析完成！

📁 输出目录: <用户指定的目录>

📄 生成文件:
  - <视频ID>.mp4         (原始视频)
  - <视频ID>.srt         (原始字幕)
  - <视频ID>_文字稿.md    (校正后文字稿)
  - <视频ID>_分析报告.md  (三维度分析报告)

🔗 快速打开:
  [文字稿](<文字稿路径>)
  [分析报告](<分析报告路径>)
```

## 参考文件

- [download_douyin.py](scripts/download_douyin.py): 抖音视频下载脚本
- [extract_subtitle_funasr.py](scripts/extract_subtitle_funasr.py): 智能字幕提取脚本（FunASR + RapidOCR）
- [extract_subtitle.py](scripts/extract_subtitle.py): 字幕提取脚本（Whisper）
- [transcribe_audio.py](scripts/transcribe_audio.py): 音频转录脚本
- [analysis-frameworks.md](references/analysis-frameworks.md): 三个分析框架详解
