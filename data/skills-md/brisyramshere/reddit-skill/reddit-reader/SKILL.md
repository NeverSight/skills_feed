---
name: reddit-reader
description: 通过 Reddit OAuth2 API 搜索和阅读 Reddit 帖子、评论和子版块内容。当用户要求搜索 Reddit 讨论、浏览子版块帖子、阅读 Reddit 帖子内容和评论、了解 Reddit 社区对某个话题的看法时使用此 skill。支持按时间范围和排序方式筛选，支持读取完整帖子正文和嵌套评论树。
---

# Reddit Reader

## Overview

通过 Reddit OAuth2 API 访问 Reddit 内容的 skill，支持搜索帖子、浏览子版块、阅读帖子详情和评论。输出为结构化 Markdown，可直接用于分析和总结。

## Prerequisites

需要设置以下环境变量（从 https://www.reddit.com/prefs/apps 获取，创建 script 类型应用）：

- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`

依赖: `pip install requests`

## Usage Scenarios

当用户请求以下任务时触发：
- "搜索 Reddit 关于 xxx 的讨论"
- "看看 r/ClaudeAI 最近有什么热帖"
- "读一下这个 Reddit 帖子"
- "Reddit 上大家怎么看 xxx"
- "帮我找 Reddit 上关于 xxx 的经验分享"
- 任何涉及浏览、搜索、阅读 Reddit 内容的请求

## Workflow

### Step 1: Determine User Intent

根据用户请求识别需要执行的操作：

| 用户意图 | 子命令 | 示例 |
|----------|--------|------|
| 搜索特定话题 | `search` | "搜索 Reddit 上关于 Claude Code 的讨论" |
| 浏览子版块帖子列表 | `list` | "看看 r/ClaudeAI 最近的热帖" |
| 阅读具体帖子和评论 | `read` | "读一下这个帖子 https://reddit.com/r/..." |
| 了解子版块信息 | `subreddit` | "r/LocalLLaMA 是什么社区" |

### Step 2: Execute Script

使用 `scripts/reddit_reader.py` 执行对应操作。脚本路径相对于此 skill 目录。

#### Search - 搜索帖子

```bash
python3 scripts/reddit_reader.py search "query" [options]
```

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `query` | 搜索关键词（必填） | - | - |
| `--subreddit, -s` | 限定子版块 | 全站搜索 | 任意子版块名 |
| `--sort` | 排序方式 | relevance | relevance, hot, new, top, comments |
| `--time, -t` | 时间范围 | all | hour, day, week, month, year, all |
| `--limit, -l` | 返回条数 | 10 | 1-100 |

示例：
```bash
# 全站搜索，按热度排序，最近一周
python3 scripts/reddit_reader.py search "Claude Code tips" --sort hot --time week --limit 15

# 在特定子版块内搜索
python3 scripts/reddit_reader.py search "cursor vs claude" -s ClaudeAI --sort top --time month
```

#### List - 浏览子版块帖子

```bash
python3 scripts/reddit_reader.py list <subreddit> [options]
```

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `subreddit` | 子版块名（必填） | - | 如 ClaudeAI, LocalLLaMA |
| `--category, -c` | 帖子分类 | hot | hot, new, top, rising, controversial |
| `--time, -t` | 时间范围（top/controversial） | week | hour, day, week, month, year, all |
| `--limit, -l` | 返回条数 | 10 | 1-100 |

示例：
```bash
# 热门帖子
python3 scripts/reddit_reader.py list r/ClaudeAI --category hot --limit 10

# 本月最高赞帖子
python3 scripts/reddit_reader.py list LocalLLaMA --category top --time month --limit 20
```

#### Read - 阅读帖子和评论

```bash
python3 scripts/reddit_reader.py read <post_id_or_url> [options]
```

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `post` | 帖子 ID、完整 URL 或分享短链接（必填） | - | - |
| `--comment-sort` | 评论排序 | top | best, top, new, controversial, old |
| `--comment-limit` | 评论数量 | 30 | 任意整数 |
| `--comment-depth` | 嵌套深度 | 5 | 1-10 |

示例：
```bash
# 通过 URL 阅读
python3 scripts/reddit_reader.py read "https://www.reddit.com/r/ClaudeAI/comments/abc123/some_title"

# 通过分享短链接阅读（/s/ 格式，自动解析为真实帖子）
python3 scripts/reddit_reader.py read "https://www.reddit.com/r/ClaudeCode/s/C3mumg2tj8"

# 通过 ID 阅读，按最新评论排序
python3 scripts/reddit_reader.py read abc123 --comment-sort new --comment-limit 50
```

#### Subreddit - 查看子版块信息

```bash
python3 scripts/reddit_reader.py subreddit <name>
```

示例：
```bash
python3 scripts/reddit_reader.py subreddit ClaudeAI
```

### Step 3: Analyze and Summarize

脚本输出为 Markdown 格式。根据用户需求：
- **总结帖子列表**：提炼出主要话题和趋势
- **分析帖子内容**：总结正文要点和评论区核心观点
- **对比观点**：梳理评论中的不同立场和共识
- **提取经验**：从讨论中提取实用建议和经验

## References

详细的 Reddit API 端点参数参考见 `references/reddit_api.md`。

## Limitations

- 需要 Reddit API 凭证（client_id + client_secret）
- 只读访问，不支持发帖或评论
- 每分钟 100 次请求限制（OAuth 认证后）
- 搜索结果最多翻阅约 1000 条
- 无法访问私有子版块或已删除内容
