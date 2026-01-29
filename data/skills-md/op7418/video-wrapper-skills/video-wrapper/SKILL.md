---
name: video-wrapper
description: 为访谈视频添加综艺特效（花字、卡片、人物条、章节标题等）。支持 4 种视觉主题，先分析字幕内容生成建议供用户审批，再渲染视频。
argument-hint: <video-file> <subtitle-file> [config.json] [output.mp4]
user-invocable: true
allowed-tools: Bash, Read, Write
context: fork
agent: general-purpose
---

# 访谈视频处理器

基于 Python + Playwright + MoviePy 的视频特效处理工具，使用 HTML/CSS/Anime.js 渲染高质量视觉效果。

## 工作流程

### 第一步：分析字幕内容

当用户提供视频和字幕文件时，先分析字幕内容，生成特效建议：

1. 读取字幕文件 (.srt)
2. 分析内容，识别：
   - 嘉宾信息（用于人物条）
   - 话题切换点（用于章节标题）
   - 关键词和术语（用于花字）
   - 专业名词（用于名词卡片）
   - 精彩观点（用于金句卡片）
   - 数字数据（用于数据动画）
   - 核心要点（用于要点列表）
3. 生成建议列表，展示给用户审核

### 第二步：用户审核

将建议以 Markdown 格式展示给用户：

```
## 视觉特效建议

**主题**: notion

### 1. 人物条 (Lower Third)
- **姓名**: Dario Amodei
- **职位**: CEO
- **公司**: Anthropic
- **出现时间**: 1000ms

### 2. 花字高亮 (Fancy Text)
1. **通用人工智能** (emphasis)
   时间: 2630ms - 5500ms
   原因: 核心概念首次提及

...
```

用户可以：
- 确认全部建议
- 修改部分建议
- 删除不需要的组件
- 添加新的组件

### 第三步：生成配置并渲染

根据用户审批后的建议生成 config.json，然后渲染视频。

## 可用组件

| 组件 | 用途 | 配置字段 |
|------|------|----------|
| 人物条 (lower_third) | 显示嘉宾信息 | name, role, company, startMs, durationMs |
| 章节标题 (chapter_title) | 话题切换标题 | number, title, subtitle, startMs, durationMs |
| 花字 (fancy_text) | 概括当前观点 | text, style, startMs, endMs, position |
| 名词卡片 (term_card) | 解释术语 | chinese, english, description, firstAppearanceMs |
| 金句卡片 (quote_callout) | 突出精彩观点 | text, author, startMs, durationMs, position |
| 数据动画 (animated_stats) | 展示数字 | prefix, number, unit, label, startMs |
| 要点列表 (bullet_points) | 总结核心要点 | title, points[], startMs, durationMs |
| 社交媒体条 (social_bar) | 关注引导 | platform, label, handle, startMs, durationMs |

### 花字使用规范

⚠️ **重要**：花字必须遵循以下规范：

1. **必须是短语**：用简短的句子概括说话人当时的观点
   - ✅ 正确：「AI发展是平滑曲线」「智能增长类似摩尔定律」
   - ❌ 错误：「人工智能」「摩尔定律」（这些是单词，应该用名词卡片）

2. **与名词卡片互补**：
   - 花字：概括观点（如「智能每年翻倍增长」）
   - 名词卡片：解释术语（如「摩尔定律：集成电路晶体管数量每18-24个月翻一番」）

3. **位置在上方**：默认显示在屏幕上方区域（字幕上方），避免遮挡人脸

### 社交媒体条使用规范

- 默认显示时长：8 秒（比其他组件更长，给用户足够时间记住）
- 通常在视频结尾出现
- 支持平台：twitter, weibo, youtube

## 主题系统

支持 4 种视觉主题：

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `notion` | 温暖知识风 | 教育、知识分享 |
| `cyberpunk` | 霓虹未来感 | 科技、前沿话题 |
| `apple` | 极简优雅 | 商务、专业访谈 |
| `aurora` | 渐变流光 | 创意、艺术内容 |

## 配置文件格式

```json
{
  "theme": "notion",
  "lowerThirds": [
    {
      "name": "Dario Amodei",
      "role": "CEO",
      "company": "Anthropic",
      "startMs": 1000,
      "durationMs": 5000
    }
  ],
  "chapterTitles": [
    {
      "number": "Part 1",
      "title": "指数增长的本质",
      "subtitle": "The Nature of Exponential Growth",
      "startMs": 0,
      "durationMs": 4000
    }
  ],
  "keyPhrases": [
    {
      "text": "通用人工智能",
      "style": "emphasis",
      "startMs": 2630,
      "endMs": 5500
    }
  ],
  "termDefinitions": [
    {
      "chinese": "摩尔定律",
      "english": "Moore's Law",
      "description": "集成电路晶体管数量每18-24个月翻一番",
      "firstAppearanceMs": 37550,
      "displayDurationSeconds": 6
    }
  ],
  "quotes": [
    {
      "text": "AI 的发展是一个非常平滑的指数曲线",
      "author": "— Dario Amodei",
      "startMs": 30000,
      "durationMs": 5000
    }
  ],
  "stats": [
    {
      "prefix": "增长率 ",
      "number": 240,
      "unit": "%",
      "label": "计算能力年增长",
      "startMs": 45000,
      "durationMs": 4000
    }
  ],
  "bulletPoints": [
    {
      "title": "核心观点",
      "points": [
        "AI 发展是平滑的指数曲线",
        "类似摩尔定律的智能增长",
        "没有突然的奇点时刻"
      ],
      "startMs": 50000,
      "durationMs": 6000
    }
  ]
}
```

## 依赖安装

```bash
# 进入虚拟环境
cd ~/.claude/skills/video-wrapper
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

## 命令行使用

```bash
# 使用浏览器渲染器（推荐）
python src/video_processor.py video.mp4 subs.srt config.json output.mp4

# 指定渲染器
python src/video_processor.py video.mp4 subs.srt config.json -r browser
python src/video_processor.py video.mp4 subs.srt config.json -r pil
```

## 技术实现

- **视觉渲染**: HTML + CSS + Anime.js (通过 Playwright 截图)
- **视频合成**: MoviePy
- **动画引擎**: Anime.js (Spring 物理动画)
- **备用渲染**: Python PIL

## 文件结构

```
~/.claude/skills/video-wrapper/
├── src/
│   ├── video_processor.py    # 主处理脚本
│   ├── browser_renderer.py   # Playwright 渲染器
│   ├── content_analyzer.py   # 内容分析器
│   ├── fancy_text.py         # PIL 花字（备用）
│   └── term_card.py          # PIL 卡片（备用）
├── templates/
│   ├── fancy-text.html       # 花字模板
│   ├── term-card.html        # 名词卡片模板
│   ├── lower-third.html      # 人物条模板
│   ├── chapter-title.html    # 章节标题模板
│   ├── quote-callout.html    # 金句卡片模板
│   ├── animated-stats.html   # 数据动画模板
│   └── bullet-points.html    # 要点列表模板
├── static/
│   ├── css/
│   │   ├── effects.css       # 基础效果
│   │   ├── theme-notion.css  # Notion 主题
│   │   ├── theme-cyberpunk.css
│   │   ├── theme-apple.css
│   │   └── theme-aurora.css
│   └── js/
│       └── anime.min.js      # Anime.js
└── requirements.txt
```

## 注意事项

- 视频处理需要较长时间，请耐心等待
- 确保有足够的磁盘空间存储输出视频
- Playwright 渲染效果更好，但需要安装 Chromium
- 如果 Playwright 不可用，会自动回退到 PIL 渲染
