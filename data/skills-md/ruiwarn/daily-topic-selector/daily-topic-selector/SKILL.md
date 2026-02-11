---
name: daily-topic-selector
version: "1.0.0"
description: Daily topic fetcher that collects articles from multiple sources (RSS, API, HTML), scores and ranks them by relevance, and generates enhanced Chinese reports.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
user-invocable: true
triggers:
  - "/daily-topic-selector"
  - "抓取今日选题"
  - "获取每日选题"
  - "fetch daily topics"
  - "run daily-topic-selector"
  - "运行 daily-topic-selector"
  - "grab daily topics"
---

# daily-topic-selector

每日选题抓取工具 - 从多个内容源获取最新文章并评分排序

## 触发方式

当用户说以下内容时触发此技能：
- "抓取今日选题"
- "获取每日选题"
- "运行 daily-topic-selector"
- "/daily-topic-selector"
- "fetch daily topics"

## 功能说明

此技能用于从多个内容源（RSS、API、HTML、JSON）抓取最新文章，并通过评分系统筛选出最值得阅读的内容。

支持的数据源：
- TLDR AI - AI 领域每日简报
- Hacker News - 技术社区热门内容
- Import AI - AI 政策与研究深度分析
- James Clear - 习惯与个人成长
- Wait But Why - 长文深度思考

## 使用指令

### 基础用法

```bash
# 抓取最近 1 天的内容（输出到当前目录的 daily_output/）
python $SKILL_DIR/scripts/run.py

# 抓取最近 N 天的内容
python $SKILL_DIR/scripts/run.py --days 3

# 指定其他输出目录
python $SKILL_DIR/scripts/run.py --output_dir /path/to/output
```

**说明**：默认输出到当前工作目录下的 `daily_output/YYYY-MM-DD/` 目录。

### 高级用法

```bash
# 只抓取特定源
python $SKILL_DIR/scripts/run.py --only_sources hn,import_ai

# 指定时间范围
python $SKILL_DIR/scripts/run.py --since 2024-01-01T00:00:00Z

# 调整抓取参数
python $SKILL_DIR/scripts/run.py --limit_per_source 100 --timeout 30
```

## 输出文件

运行后会生成 5 个文件：

| 文件 | 说明 |
|------|------|
| `daily_topics.md` | 原始 Markdown 日报 |
| `daily_topics_zh.md` | 增强版日报（含中文翻译和摘要） |
| `daily_topics.json` | 机器可读的 JSON 数据 |
| `fetch_log.txt` | 抓取日志 |
| `run_meta.json` | 运行元信息 |

## 执行流程

当用户触发此 skill 时，按以下步骤执行：

### 步骤 1：运行 Python 脚本抓取数据

```bash
python3 $SKILL_DIR/scripts/run.py
```

脚本完成后会输出结构化结果：
```
===== RESULT =====
OUTPUT_DIR=/path/to/daily_output/YYYY-MM-DD
JSON_FILE=/path/to/daily_output/YYYY-MM-DD/daily_topics.json
MD_FILE=/path/to/daily_output/YYYY-MM-DD/daily_topics.md
NEW_COUNT=33
==================
```

### 步骤 2：读取 JSON_FILE 进行后处理

1. 读取上述 `JSON_FILE` 路径的文件
2. 为英文标题生成中文翻译和摘要
3. 在 `OUTPUT_DIR` 下创建 `daily_topics_zh.md`

#### 增强后的 Markdown 格式

```markdown
### 1. [原始英文标题](URL)
- **中文**：中文标题翻译
- **时间**：2026-01-09 16:46 | **分数**：85.0
- **Points**: 509 | **Comments**: 701
- **标签**：`云服务`, `监管`, `科技公司`
- **摘要**：一句话中文摘要，帮助读者快速了解文章主题和价值。
```

#### 翻译和摘要要求

- **中文标题**：简洁准确，保留关键信息，不超过 30 字
- **中文摘要**：1-2 句话，说明文章主题、核心观点或为什么值得阅读
- **标签优化**：将通用标签（如 tech, startup）替换为更具体的中文标签
- **批量处理**：一次性处理所有条目，然后一次性写入文件

#### 处理示例

原始条目：
```json
{
  "title": "Cloudflare CEO on the Italy fines",
  "tags": ["tech", "startup", "programming"],
  ...
}
```

增强后：
```markdown
### 1. [Cloudflare CEO on the Italy fines](https://...)
- **中文**：Cloudflare CEO 回应意大利罚款事件
- **时间**：2026-01-09 16:46 | **分数**：100.0
- **Points**: 509 | **Comments**: 701
- **标签**：`云服务`, `欧盟监管`, `互联网基础设施`
- **摘要**：Cloudflare CEO 在社交媒体上回应意大利监管机构的罚款决定，讨论了欧洲互联网监管趋势及其对云服务商的影响。
```

## 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--days` | 1 | 抓取最近 N 天的内容 |
| `--since` | - | 抓取该时间之后的内容 (ISO 格式) |
| `--output_dir` | . | 输出目录 |
| `--limit_per_source` | 50 | 每个源最大抓取条数 |
| `--only_sources` | - | 只抓取指定源 (逗号分隔) |
| `--config` | 自动 | 配置目录路径 |
| `--incremental` | true | 增量模式 |
| `--timeout` | 20 | 请求超时 (秒) |
| `--retries` | 2 | 失败重试次数 |

## 依赖要求

运行前请确保已安装依赖：

```bash
pip install requests feedparser beautifulsoup4 lxml PyYAML
```

## 配置说明

### 配置文件查找顺序

程序按以下优先级查找配置：

1. `--config` 参数指定的目录
2. `~/.config/daily-topic-selector/` （用户自定义配置）
3. `$SKILL_DIR/config/` （默认配置）

### 配置合并机制

**重要**：用户配置与默认配置会自动合并，这意味着：

- ✅ **自动获取新源**：当 skill 更新添加了新的数据源，用户无需修改配置即可使用
- ✅ **保留用户自定义**：用户对现有源的修改不会被覆盖
- ✅ **灵活禁用源**：用户可以通过 `enabled: false` 禁用不想要的源

#### 合并规则

| 场景 | 行为 |
|------|------|
| 默认源，用户未修改 | 使用默认配置（自动获取更新） |
| 默认源，用户有自定义 | 用户配置覆盖默认配置 |
| skill 新增源，用户无配置 | 自动启用新源 |
| skill 新增源，用户设置 `enabled: false` | 保持禁用 |
| 用户自定义源（默认配置中不存在） | 保留用户配置 |

### 初始化用户配置

首次使用时，可复制默认配置到用户目录：

```bash
mkdir -p ~/.config/daily-topic-selector
cp $SKILL_DIR/config/*.yaml ~/.config/daily-topic-selector/
```

**注意**：复制后用户配置将覆盖对应的默认配置。如果只想微调某些设置，建议只创建包含需要修改部分的配置文件。

### 最佳实践

#### 方式一：完全自定义（复制全部配置）

适合需要完全控制配置的用户：

```bash
cp $SKILL_DIR/config/*.yaml ~/.config/daily-topic-selector/
# 编辑配置文件进行自定义
```

⚠️ 缺点：skill 更新新源时需要手动添加

#### 方式二：增量自定义（推荐）

只创建包含需要修改部分的配置，其余使用默认值：

```yaml
# ~/.config/daily-topic-selector/sources.yaml
# 只需要写需要修改的部分

sources:
  # 禁用不想要的源
  wait_but_why:
    enabled: false

  # 修改现有源的配置
  hacker_news:
    scoring:
      base_score: 30  # 调整基础分

  # 添加自定义源
  my_custom_source:
    enabled: true
    name: "我的数据源"
    # ...
```

✅ 优点：自动获取 skill 更新的新源

### 配置文件

- `sources.yaml` - 数据源配置
- `scoring.yaml` - 评分规则配置

### 添加新数据源

编辑 `~/.config/daily-topic-selector/sources.yaml`：

```yaml
my_new_source:
  enabled: true
  name: "新数据源"
  description: "描述"

  fetch_methods:
    - method: rss
      priority: 1
      config:
        url: "https://example.com/feed"

  default_tags: ["tag1"]

  scoring:
    base_score: 30
```

### 调整评分规则

编辑 `~/.config/daily-topic-selector/scoring.yaml`：

```yaml
global_keywords:
  ai_hot:
    keywords: ["OpenAI", "GPT", "Claude"]
    bonus: 15
```
