---
name: ai-news-digest
description: Multi-source AI news aggregation and digest generation with deduplication, classification, and source tracing. Supports 20+ sources, 5 theme categories, multi-language output (ZH/EN/JA), and image export.
---

<!-- i18n-examples:start -->
## 调用 / Invoke / 呼び出し

### 中文
- "用 ai-news-digest 生成今天的 AI 资讯简报"
- "用 ai-news-digest 获取昨天的 AI 新闻"
- "用 ai-news-digest 看看前天有什么 AI 动态"
- "帮我用 ai-news-digest 整理一下最近的 AI 资讯"

### English
- "Use ai-news-digest to generate today's AI news digest"
- "Use ai-news-digest to get yesterday's AI news in English"
- "Generate an AI news summary for 2026-01-20 using ai-news-digest"
- "Use ai-news-digest to summarize recent AI developments"

### 日本語
- "ai-news-digest で今日のAIニュース要約を日本語で作成して"
- "ai-news-digest で昨日のAIニュースを取得して"
- "ai-news-digest を使って最近のAI動向をまとめて"
- "ai-news-digest で一昨日のAI関連ニュースを教えて"
<!-- i18n-examples:end -->

# 目标

在指定时间窗口内，从一组 AI 资讯信源获取最新内容并产出“可验收”的资讯简报：

- 交付物：1 份 Markdown 简报（可选同时给 JSON 数据）
- 每条资讯：标题、时间、来源、链接、1-3 句摘要、标签（可选“为什么重要”）
- 默认策略：RSS/Atom 优先，HTML 兜底；不绕过付费墙
- 默认输出：**中文**（如来源为英文，需翻译为中文再输出）

# 输入（先问清）

- 时间窗口（默认“当天”）：
  - 自然语言：`今天/昨天/前天`（可扩展 `过去7天/最近24小时`）
  - 指定日期：`YYYY-MM-DD`（按用户时区解释为“当天 00:00-23:59:59”）
  - 具体起止时间：`since/until`（含时区）
- 时区：默认 `UTC+8`（建议实现默认 `Asia/Shanghai`），用户可显式指定
- 输出语言：默认 `zh`（中文）；可选 `en` / `both`
- 主题范围：研究/产品/开源/投融资/政策（可多选）
- 信源范围：使用默认列表或用户指定子集（见 `references/sources.md`）
- 输出格式：Markdown（默认）/ JSON / 两者
- 篇数上限：总数与每个主题上限（默认总 20）
- 处理深度：仅标题摘要（默认）/ 尝试正文提取（对非付费内容）

# 流程（推荐架构）

1. 载入信源清单（RSS 优先；无法 RSS 的再做 HTML 适配）
2. 拉取条目并标准化（标题/链接/发布时间/摘要/来源）
3. 去重与合并（同链接/同标题近似/跨源重复）
4. 主题分类与排序（时间 + 信源权重 + 关键词）
5. 生成简报（套用模板 `assets/digest-template.md`，附来源链接）
6. 质检（时间窗口命中、无重复、每条都有链接/来源）

# 护栏（合规与稳定性）

- 不绕过付费墙/登录限制；付费内容仅使用公开标题/摘要/元信息
- 尊重站点条款与 robots；必要时降级为“只收 RSS 条目”
- 失败可降级：只输出“可获取”的部分并列出失败信源清单与原因
- 翻译/摘要必须保留可追溯性：输出中始终保留原始链接与来源；必要时在 JSON 保留原文 `title_raw/summary_raw`
- 任何写文件/覆盖导出前先确认输出路径与是否覆盖

# 如何运行

## CLI 命令

```bash
# 进入脚本目录
cd skills/public/ai-news-digest/scripts

# 获取今天的资讯摘要
python run.py --day 今天

# 获取昨天的资讯
python run.py --day yesterday

# 如遇本地 SSL 证书链问题（不推荐），可禁用校验
python run.py --day yesterday --insecure

# 指定日期
python run.py --day 2026-01-15

# 输出 JSON 格式
python run.py --day 今天 --format json

# 输出分享图片（需安装 Pillow）
python run.py --day 今天 --format image

# 输出横版图片（适合公众号）
python run.py --day 今天 --format image --image-preset landscape

# 输出浅色主题图片
python run.py --day 今天 --format image --image-theme light

# 写入文件
python run.py --day 今天 --out digest.md

# 使用 LLM 翻译（需配置 API key）
python run.py --day 今天 --llm

# 详细输出
python run.py --day 今天 --verbose

# 运行冒烟测试
python run.py --test
```

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--day, -d` | 日期（今天/昨天/前天/YYYY-MM-DD） | 今天 |
| `--since` | 起始时间（ISO 8601） | - |
| `--until` | 结束时间（ISO 8601） | - |
| `--tz` | 时区 | Asia/Shanghai |
| `--lang, -l` | 输出语言（zh/en） | zh |
| `--format, -f` | 输出格式（markdown/json/image） | markdown |
| `--image-preset` | 图片尺寸（portrait/landscape/square） | portrait |
| `--image-theme` | 图片主题（dark/light） | dark |
| `--out, -o` | 输出文件路径 | - |
| `--topics, -t` | 主题过滤（逗号分隔） | 全部 |
| `--sources, -s` | 信源过滤（ID，逗号分隔） | 全部 |
| `--max` | 最大条数 | 20 |
| `--max-per-topic` | 每主题最大条数 | 5 |
| `--llm` | 使用 LLM 翻译 | 否 |
| `--verbose, -v` | 详细输出 | 否 |
| `--insecure` | 禁用 SSL 证书校验（不推荐） | 否 |

## 脚本模块说明

| 脚本 | 功能 |
|------|------|
| `run.py` | CLI 入口，整合所有模块 |
| `time_window.py` | 时间窗口解析 |
| `fetch_feeds.py` | Feed 抓取（缓存/限速/重试） |
| `parse_feeds.py` | RSS/Atom 解析与规范化 |
| `dedupe.py` | 去重与多信源合并 |
| `classify_rank.py` | 主题分类与排序 |
| `render_digest.py` | Markdown/JSON 渲染 |
| `render_image.py` | 图片渲染（社交分享卡片） |
| `summarize_llm.py` | LLM 翻译（可选） |

## 依赖

**必需**（Python 标准库）：
- Python 3.10+
- 无第三方依赖即可运行 Markdown/JSON 输出

**可选**（增强功能）：
- `Pillow`: 图片渲染功能（`--format image`）
- `pyyaml`: 更完整的 YAML 解析（脚本内置简化解析器，无需安装也能正常加载 `sources.yaml`）
- `anthropic` 或 `openai`: LLM 翻译功能

### 安装可选依赖

```bash
# 安装图片渲染支持
pip install Pillow

# 安装所有可选依赖
pip install Pillow pyyaml anthropic
```

> **注意**：
> - 未安装 Pillow 时，Markdown 和 JSON 输出正常工作，仅图片输出不可用
> - 未安装 pyyaml 时，脚本会使用内置的简化 YAML 解析器，可正常加载完整信源列表

# 资源

- 数据模型与输出规范：`references/output-spec.md`
- 信源注册表：`references/sources.yaml`
- 信源评估说明：`references/sources.md`
- 时间窗口规范：`references/time-window.md`
- 主题关键词：`references/topic-keywords.md`
- 翻译规范：`references/translation.md`
- Markdown 模板：`assets/digest-template.md`
- LLM 提示词：`assets/summarize-prompt.md`
