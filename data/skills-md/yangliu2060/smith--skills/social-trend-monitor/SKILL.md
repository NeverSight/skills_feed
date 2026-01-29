---
name: social-trend-monitor
description: 监控 Reddit、Instagram、TikTok 等社交平台的热门趋势，汇总生成跨平台趋势报告，帮助发现内容创作灵感和市场机会。
---

# 社交媒体趋势监控

跨平台监控 Reddit、Instagram、TikTok 的热门内容和趋势话题，生成综合趋势报告。

## 触发条件

当用户说以下内容时启动此技能：
- "查看社交趋势"
- "今天什么火"
- "热门话题"
- "trending topics"
- "社交媒体趋势"
- "Reddit/TikTok/Instagram 上什么火"

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    并行监控三大平台                        │
├─────────────────┬─────────────────┬─────────────────────┤
│                 │                 │                     │
▼                 ▼                 ▼                     │
┌───────────┐  ┌───────────┐  ┌───────────┐              │
│  Reddit   │  │ Instagram │  │  TikTok   │              │
│  热帖搜索  │  │  热门搜索  │  │  热门搜索  │              │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘              │
      │              │              │                     │
      ▼              ▼              ▼                     │
┌───────────┐  ┌───────────┐  ┌───────────┐              │
│  提取     │  │  提取     │  │  提取     │              │
│  Top 10   │  │  Top 10   │  │  Top 10   │              │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘              │
      │              │              │                     │
      └──────────────┼──────────────┘                     │
                     │                                    │
                     ▼                                    │
          ┌─────────────────────┐                        │
          │   汇总跨平台趋势     │                        │
          │   生成趋势报告       │                        │
          └──────────┬──────────┘                        │
                     │                                    │
                     ▼                                    │
          ┌─────────────────────┐                        │
          │   保存报告到本地     │                        │
          └─────────────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

## 执行步骤

### 步骤 1：确定监控范围

询问或从用户输入中识别：
- **目标平台**: Reddit / Instagram / TikTok（默认全部）
- **关注领域**: 科技、商业、娱乐、生活方式等（可选）
- **时间范围**: 今日、本周、本月（默认今日）

### 步骤 2：Reddit 趋势监控

**搜索策略**：
```
"Reddit trending today"
"Reddit popular posts {领域} site:reddit.com"
"r/popular top posts today"
"Reddit front page {日期}"
```

**提取信息**：
- 帖子标题
- Subreddit（板块）
- 点赞数/评论数
- 帖子链接
- 发布时间

**输出格式**：
```json
{
  "platform": "Reddit",
  "trends": [
    {
      "rank": 1,
      "title": "帖子标题",
      "subreddit": "r/technology",
      "upvotes": "45.2k",
      "comments": "3.2k",
      "url": "https://reddit.com/...",
      "posted": "8 hours ago"
    }
  ]
}
```

### 步骤 3：Instagram 趋势监控

**搜索策略**：
```
"Instagram trending hashtags today"
"Instagram viral posts {领域}"
"Instagram explore trending {日期}"
"most popular Instagram hashtags {领域}"
```

**提取信息**：
- 热门标签 (hashtags)
- 标签使用量/帖子数
- 代表性内容主题
- 热门创作者（可选）

**输出格式**：
```json
{
  "platform": "Instagram",
  "trends": [
    {
      "rank": 1,
      "hashtag": "#trending_topic",
      "posts_count": "2.5M posts",
      "theme": "主题描述",
      "sample_content": "典型内容描述"
    }
  ]
}
```

### 步骤 4：TikTok 趋势监控

**搜索策略**：
```
"TikTok trending sounds today"
"TikTok viral videos {领域}"
"TikTok trending hashtags {日期}"
"TikTok discover page trends"
```

**提取信息**：
- 热门声音/音乐
- 热门挑战/标签
- 视频播放量级别
- 趋势持续时间

**输出格式**：
```json
{
  "platform": "TikTok",
  "trends": [
    {
      "rank": 1,
      "type": "sound/hashtag/challenge",
      "name": "趋势名称",
      "views": "10M+",
      "description": "趋势描述",
      "duration": "trending for 3 days"
    }
  ]
}
```

### 步骤 5：跨平台趋势汇总

分析三个平台的数据，找出：

**共同趋势**：
- 多平台出现的相同话题
- 跨平台传播的内容

**平台特色**：
- 每个平台独有的热点
- 平台特定的内容形式

**趋势洞察**：
- 为什么这些内容火？
- 内容创作者可以如何借鉴？
- 品牌营销机会在哪里？

### 步骤 6：生成趋势报告

输出完整的 Markdown 报告：

```markdown
# 社交媒体趋势日报

**生成时间**: YYYY-MM-DD HH:MM
**监控平台**: Reddit, Instagram, TikTok
**关注领域**: [用户指定或"综合"]

---

## 📊 趋势概览

| 平台 | 最热话题 | 热度指标 |
|------|---------|---------|
| Reddit | #1话题 | 45.2k upvotes |
| Instagram | #1标签 | 2.5M posts |
| TikTok | #1声音 | 10M+ views |

---

## 🔴 Reddit 热门

### Top 1: [帖子标题]
- **板块**: r/subreddit
- **热度**: ⬆️ 45.2k | 💬 3.2k
- **链接**: [查看原帖](url)
- **看点**: 为什么火的简析

### Top 2: ...

---

## 📸 Instagram 热门

### Top 1: #hashtag
- **帖子量**: 2.5M posts
- **主题**: 主题描述
- **典型内容**: 内容形式描述
- **创作建议**: 如何跟进这个趋势

### Top 2: ...

---

## 🎵 TikTok 热门

### Top 1: [声音/挑战名称]
- **类型**: 声音 / 标签 / 挑战
- **播放量**: 10M+
- **持续时间**: 已火 3 天
- **玩法**: 如何参与

### Top 2: ...

---

## 🔥 跨平台共同趋势

1. **[话题A]** - 在 Reddit 和 TikTok 同时火爆
   - Reddit 角度: ...
   - TikTok 角度: ...

2. **[话题B]** - Instagram 和 TikTok 共同趋势
   - ...

---

## 💡 洞察与建议

### 内容创作者
- 建议1: ...
- 建议2: ...

### 品牌营销
- 机会1: ...
- 机会2: ...

### 值得关注
- 新兴趋势: ...
- 预测下一个热点: ...

---

*报告由 Claude Code social-trend-monitor 技能自动生成*
```

## 使用示例

### 示例 1：综合趋势查看

```
用户: 今天社交媒体上什么最火？

Claude:
1. 并行搜索三大平台趋势
2. 提取各平台 Top 10
3. 分析跨平台共同趋势
4. 生成趋势日报
```

### 示例 2：垂直领域趋势

```
用户: 科技圈最近在 Reddit 和 TikTok 上讨论什么？

Claude:
1. 聚焦科技领域关键词
2. 搜索 Reddit r/technology, r/programming 等
3. 搜索 TikTok #tech #coding 趋势
4. 对比分析输出
```

### 示例 3：创作灵感挖掘

```
用户: 我想做短视频，帮我看看 TikTok 上什么内容形式最火

Claude:
1. 深度搜索 TikTok 趋势
2. 分析热门视频的共同特点
3. 提供具体创作建议
```

## 数据存储

趋势报告保存在：`~/.claude/cache/social-trends/`

文件命名：`trends-{YYYY-MM-DD}.md`

历史趋势可供对比分析。

## 搜索优化技巧

### Reddit
- 使用 `site:reddit.com` 限定搜索范围
- 搜索特定 subreddit：`r/popular`, `r/all`, `r/technology`
- 时间限定：`"today"`, `"this week"`

### Instagram
- 搜索 hashtag 报告网站获取统计数据
- 关注 `#trending`, `#viral` 元标签
- 结合领域词如 `#techtok`, `#fashiontok`

### TikTok
- 搜索 TikTok 趋势报告网站
- 关注 `trending sounds`, `viral challenges`
- 搜索 TikTok 创作者分析内容

## 依赖工具

- **WebSearch**: 搜索各平台趋势信息
- **WebFetch**: 获取详细趋势页面数据
- **Write**: 保存趋势报告

## 限制说明

- 无法直接访问平台 API，依赖公开搜索结果
- Instagram/TikTok 数据可能不如 Reddit 完整
- 实时性受搜索引擎索引速度影响
- 部分平台内容需要登录才能查看详情

## 原始来源

改编自 n8n 模板：
- 模板ID: 8450
- 原名: Monitor Social Media Trends Across Reddit, Instagram & TikTok with Apify
- 链接: https://n8n.io/workflows/8450
