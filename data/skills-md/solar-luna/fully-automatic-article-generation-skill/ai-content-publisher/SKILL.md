---
name: ai-content-publisher
description: 自动生成高质量AI内容并发布到微信公众号。根据时间段智能选择内容类型（早8点=新工具介绍、午12点=实战教程、晚6点=行业动态），过滤无用信息（融资/市值等），生成吸引人且符合实际的标题。目标读者：AI开发者、AI产品经理、AI创业者。每次生成1篇高质量文章。当用户说"生成AI文章"、"写今天的公众号内容"、"AI内容自动发布"时使用。复用 wechat-tech-writer、wechat-article-formatter、wechat-draft-publisher skills。
allowed-tools: WebSearch, Skill, Bash, Read, Write
---

# AI内容自动发布系统

自动搜索最新AI资讯、智能选题、生成高质量文章并发布到微信公众号草稿箱。内容专注对AI开发者、产品经理、创业者有价值的高质量信息。

**架构说明**：本系统复用以下 skills：
- `wechat-tech-writer`：负责文章内容生成
- `wechat-article-formatter`：负责格式化为微信HTML
- `wechat-draft-publisher`：负责发布到草稿箱

本系统专注于：热点获取、智能选题、时间策略、发布调度。

**⚠️ 硬性要求 - 封面图必须从封面库选择**：
- **禁止使用 `canvas-design` 或任何其他方式生成封面图**
- 必须调用 `scripts/select_cover.py` 从封面库选择封面
- 封面库位置：`assets/covers/`
- 如果封面选择失败，整个发布流程必须报错退出

## 核心特性

- **文章模式**：支持标准模式和深度模式
  - **标准模式**（默认）：2000-3000字科普文章，适合日常发布
  - **深度模式**：5000字深度分析，适合专题文章
- **时间段策略**：根据发布时间自动选择内容类型
  - 早8点：新工具/新模型介绍
  - 中午12点：实战教程/技巧
  - 晚上6点：行业动态/深度分析
- **智能标题生成**：吸引人且符合实际，避免标题党
- **48小时时效性检查**：确保内容是最新的
- **智能过滤**：自动排除融资、市值等对开发者无用的信息
- **每次1篇**：专注质量而非数量

## 目标读者

- **AI开发者**：需要了解最新工具、技术、框架
- **AI产品经理**：需要关注行业趋势、产品动态
- **AI创业者**：需要获取市场洞察、竞争分析
- **AI新手/想入行者**：需要实用教程和学习路径

## 触发条件

当用户说以下类似话术时触发：
- "帮我生成今天的AI文章"
- "写今天的公众号内容"
- "AI内容自动发布"
- "生成AI开发者文章"
- "搜索AI动态并发布"

## 执行流程

### 步骤1：判断时间段和内容类型

```python
from datetime import datetime
from scripts.title_generator import get_time_slot_type, TIME_SLOT_CONTENT

# 获取当前时间和目标类型
target_type, time_slot = get_time_slot_type()
time_info = TIME_SLOT_CONTENT[time_slot]

print(f"当前时间: {datetime.now().strftime('%H:%M')}")
print(f"时段: {time_slot}")
print(f"内容类型: {time_info['description']}")
print(f"内容重点: {time_info['focus']}")
print(f"目标读者: {time_info['target_audience']}")
```

**时间段映射**：
- 6:00-11:00 → `morning` → 新工具/新模型介绍
- 11:00-16:00 → `afternoon` → 实战教程/技巧
- 16:00-6:00 → `evening` → 行业动态/深度分析

### 步骤2：获取当前日期并获取热点

```bash
# 确认当前日期
date_str=$(date +"%Y年%m月%d日")
echo "今天是: $date_str"

# 获取热点
cd /home/ubuntu/.claude/skills/ai-content-publisher
python3 scripts/fetch_hotspots.py
```

**热点来源**：
- AI公司官方博客（OpenAI、Anthropic、DeepMind、Meta AI、Hugging Face、Mistral）
- 技术媒体RSS（The Verge AI、VentureBeat AI、TechCrunch AI、MIT Tech Review）
- GitHub Trending（AI/ML热门项目）

**重要**：只获取48小时内的热点，确保内容是最新的。

### 步骤3：智能选题（选择1篇）

```bash
python3 scripts/selector.py
```

**选题策略**：
1. **根据时间段确定目标类型**
2. **过滤排除**：排除融资、市值、人事变动等无用信息
3. **针对性评分**：优先选择匹配目标类型的高分话题
4. **选择最佳**：只选择1个评分最高的选题

选中话题保存到：`cache/selected_topic.json`

### 步骤4：生成吸引人的标题

```python
from scripts.title_generator import generate_title

# 读取选中的话题
import json
with open('cache/selected_topic.json', 'r') as f:
    topic = json.load(f)

# 生成标题（会根据内容类型自动选择合适的模板）
generated_title = generate_title(topic, topic['content_type'])

print(f"生成标题: {generated_title}")
```

**标题生成原则**：
- ✅ 包含具体数字（"3个技巧"、"5步搞定"）
- ✅ 直接利益点（"让你效率提升10倍"）
- ✅ 明确具体（不模糊）
- ✅ 适当长度（避免被截断）
- ✅ 符合实际（标题与内容匹配）
- ❌ 避免标题党（"震惊！"、"必看！"等）

### 步骤5：生成文章内容

使用 **wechat-tech-writer** 的 `generate.py` 脚本生成文章：

```bash
# 标准模式（默认）
python3 /home/ubuntu/wechat_article_skills/wechat-tech-writer/generate.py \
  --topic "$TOPIC_TITLE" \
  --url "$TOPIC_URL" \
  --type "$CONTENT_TYPE" \
  --output "$OUTPUT_DIR" \
  --mode standard

# 深度模式（5000字专题文章）
python3 /home/ubuntu/wechat_article_skills/wechat-tech-writer/generate.py \
  --topic "$TOPIC_TITLE" \
  --url "$TOPIC_URL" \
  --type "$CONTENT_TYPE" \
  --output "$OUTPUT_DIR" \
  --mode deep
```

**模式说明**：
- `standard`：2000-3000字，标准科普文章（定时任务使用）
- `deep`：5000字，深度分析文章（手动触发特殊需求时使用）

将生成的文章保存到：
```
output/{日期}/article/
├── article.md
```

### 步骤5.5：从封面库选择封面图（⚠️ 强制要求）

```bash
# 根据内容类型从封面库选择封面
python3 scripts/select_cover.py "$CONTENT_TYPE" "output/{日期}/article/"
```

**封面选择规则**：
- `new_tool` → `tool_*.png`（蓝色AI工具、深色编码、橙色生产力）
- `tutorial` → `tutorial_*.png`（绿色学习）
- `industry_news` → `news_*.png`（蓝色数据、紫色分析）

封面复制为：`output/{日期}/article/cover.png`

**⚠️ 严禁**：
- 禁止使用 `/canvas-design` 生成封面
- 禁止使用任何AI生成封面
- 如果 `select_cover.py` 失败，必须报错退出

### 步骤6：格式化HTML

使用 **wechat-article-formatter** 转换：

```bash
python3 /home/ubuntu/.claude/skills/wechat-article-formatter/convert.py \
  --input output/{日期}/article/article.md \
  --theme tech \
  --output output/{日期}/article/article_wechat.html
```

### 步骤7：发布到草稿箱

使用 **wechat-draft-publisher** 发布：

```bash
python3 /home/ubuntu/.claude/skills/wechat-draft-publisher/publisher.py \
  --title "{文章标题}" \
  --content output/{日期}/article/article_wechat.html \
  --cover output/{日期}/article/cover.png \
  --author "阳桃AI干货"
```

### 步骤8：发布到小红书（新增）

使用 **xiaohongshu-publisher** 发布精简版：

```bash
# 1. 复制封面图到Docker挂载目录
cp output/{日期}/article/cover.png /home/ubuntu/xiaohongshu-mcp/docker/images/xhs_cover_{日期}.png

# 2. 通过API发布到小红书
curl -s -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "{压缩标题（≤20字）}",
    "content": "{精简正文（≤1000字，保留核心要点）}",
    "images": ["/app/images/xhs_cover_{日期}.png"],
    "tags": ["AI", "编程工具"]
  }'
```

**内容精简规则**：
- 标题：≤20字（从微信标题提取关键词）
- 正文：≤1000字（提取3-5个核心要点）
- 风格：使用emoji、短句、列表格式
- 互动：结尾添加引导语（"欢迎评论点赞收藏"）

**注意**：Docker服务必须运行在 `http://localhost:18060`

### 步骤9：完成总结

```
✅ AI内容生成完成（双平台发布）

生成时间：{当前时间}
内容类型：{类型}

【微信公众号】
标题：{完整标题}
字数：{字数}字
状态：已发布到草稿箱
Media ID：{media_id}

【小红书】
标题：{压缩标题}
字数：{压缩字数}字
状态：已发布
链接：小红书App查看

---
请前往微信公众号后台查看草稿：
https://mp.weixin.qq.com
```

## 标题写作参考

### 好标题的要素

| 要素 | 说明 | 示例 |
|------|------|------|
| 具体数字 | "3个技巧"、"5步搞定" | "3步用LangChain搭建AI应用" |
| 直接利益 | "让...效率提升..." | "Claude Code：让开发者效率提升3倍" |
| 明确具体 | 不模糊，有针对性 | "OpenAI o3：AI开发者需要知道的3个变化" |
| 适当长度 | 避免被截断 | 微信限制64字节（约20个汉字） |
| 符合实际 | 标题与内容匹配 | 不夸大、不模糊 |

### 标题模板

**工具介绍类**：
- `{工具名}：让{benefit}的AI助手`
- `发布！{工具名}，{core_feature}`
- `{tool_name}：{benefit}的完整指南`

**教程类**：
- `{action}：用{tool}实现{goal}`
- `{number}步教你{action}（附代码）`
- `手把手教你：用{tool}{action}`

**行业动态类**：
- `{event}：{impact}需要知道的事`
- `{event}发布，{target_audience}如何应对`
- `解读{event}：{core_change}`

**技巧总结类**：
- `{number}个{skill}技巧，让{benefit}`
- `提升{skill}的{number}个方法`
- `{skill}进阶：{number}个实用技巧`

### 避免标题党

❌ **不要用**：
- "震惊！"、"必看！"、"惊呆了！"
- "你绝对想不到..."
- 过度承诺
- 故意模糊

✅ **应该用**：
- 实事求是
- 突出价值
- 明确具体
- 适度吸引

## 配置文件

### config/sources.yaml
- RSS源列表
- GitHub配置
- 时效性设置（48小时）
- 每次获取数量限制

## 输出目录

```
output/
└── {日期}/
    └── article/
        ├── article.md           # 原始文章
        ├── cover.png            # 封面图（从封面库选择，⚠️ 禁止生成）
        └── article_wechat.html  # 微信HTML格式
```

cache/
├── hotspots.json         # 原始热点
└── selected_topic.json   # 选中的话题（单个）
```

## 定时任务配置

### Crontab 配置

```bash
# 编辑定时任务
crontab -e

# 添加以下内容（早8点、中午12点、晚上6点）
0 8,12,18 * * * cd /home/ubuntu && claude skill ai-content-publisher >> /var/log/ai-content.log 2>&1
```

### Cron 表达式说明

```
┌───────────── 分钟 (0-59)
│  ┌────────── 小时 (0-23)
│  │   ┌────── 日期 (1-31)
│  │   │  ┌─── 月份 (1-12)
│  │   │  │ ┌ 星期 (0-7)
│  │   │  │ │
*  *  *  *  *  命令
```

- `0 8,12,18 * * *` = 每天 8:00、12:00、18:00 执行
- `>> /var/log/ai-content.log` = 日志追加到文件
- `2>&1` = 错误也重定向到日志

## 质量标准

### 内容质量要求

- **原创性**：用自己的语言重新组织，不照搬原文
- **准确性**：事实和数据必须可靠
- **实用性**：必须有具体价值，对读者有帮助
- **可读性**：语言自然流畅，适合公众号风格
- **字数要求**：2000-3000字

### 标题质量要求

- **长度限制**：不超过64字节（约20个汉字）
- **吸引力**：让人想点击，但不夸张
- **信息量**：包含核心信息，让读者知道会学到什么
- **匹配度**：标题与内容完全一致

## 注意事项

1. **⚠️ 封面图强制要求**：
   - **必须**从封面库选择（`assets/covers/`）
   - **禁止**使用 `/canvas-design` 生成封面
   - **禁止**使用任何AI生成封面
   - 封面选择失败则报错退出，不继续发布

2. **日期检查**：所有搜索操作前必须先确认当前日期
3. **时效性**：只使用48小时内的热点
4. **时间段策略**：根据时间自动选择合适的内容类型
5. **质量第一**：宁可少发，也要保证质量
6. **标题规范**：吸引人但不标题党
7. **草稿箱发布**：先保存到草稿箱，用户可人工审核后正式发布

## 参考资源

### 标题写作技巧
- [10倍点击量：2025年的标题生成器](https://www.iweaver.ai/zh/guide/headline-generator-in-2025/)
- [技术文章如何取标题、封面、配图](https://cloud.tencent.com/developer/article/2277070)
- [如何打造爆款文章标题？把握1个公式，9个套路，5个细节](https://www.digitaling.com/articles/893297.html)
- [AI生成公众号推文神器：3分钟打造爆款内容的秘密武器](https://www.uecloud.net/geo/article/Zj5)
