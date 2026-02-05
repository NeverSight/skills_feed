---
name: AI-Daily
description: AI 行业日报生成工具。自动采集 RSS + 爬取全文，通过 Claude 逐条分析生成涵盖大模型、产品发布、算法研究、芯片硬件、工具开源、投融资、政策监管等 8 个板块的日报。当用户说"生成AI日报"、"AI日报"或"日报"时触发。
---

# AI-Daily - AI 行业日报生成工具

自动采集、爬取全文、智能分析，生成带重要程度排序的 AI 行业日报。

## 工作流程

1. **收集新闻**: RSS 获取过去 24 小时新闻，保存为 `raw_news_YYYY-MM-DD.jsonl`
2. **生成分析清单**: 将新闻分类，生成结构化分析清单和元数据
3. **Claude 逐条分析**: 为每条新闻生成概述（5W1H）、短评、重要程度评分
4. **智能排序输出**: 按重要程度降序排列，生成最终日报

## 八大板块

1. **大模型** - GPT、Claude、Gemini、文心、通义等大模型更新
2. **产品与发布** - 新产品发布、功能更新
3. **算法与研究** - 论文、算法突破、研究成果
4. **芯片与硬件** - GPU、芯片、硬件产品
5. **工具与开源** - 开源项目、开发工具
6. **投融资与并购** - 融资、收购、IPO
7. **政策与监管** - 政策法规、监管动态
8. **事件与会议** - 行业活动、会议展览

## 使用方式

### Claude Code 对话

直接说：
- "生成AI日报"
- "AI日报"
- "日报"

### 手动运行（完整流程）

```bash
cd /Users/leefee/.claude/skills/AI-Daily/scripts

# 步骤1：收集新闻（生成 raw_news_YYYY-MM-DD.jsonl）
python3 collect_news.py --hours 24 --output ~/Desktop/AI-Daily

# 步骤2：生成分析清单
python3 daily_generator_v2.py analyze \
  --input ~/Desktop/AI-Daily/raw_news_$(date +%Y-%m-%d).jsonl \
  --output ~/Desktop/AI-Daily/analysis_list.txt

# 步骤3：告诉 Claude "分析 ~/Desktop/AI-Daily/analysis_list.txt"
# Claude 会逐条分析并生成结果

# 步骤4：告诉 Claude "根据分析结果生成日报"
# Claude 会按重要程度排序生成最终日报
```

## 输出格式

每条新闻包含：
- **概述**: 80-120字，遵循 5W1H 原则（Who/What/When/Where/Why/How）
- **短评**: 30-50字，分析行业影响和意义
- **重要程度**: ⭐ 1-5 星评级

日报末尾按重要程度排序：
- ⭐⭐⭐⭐⭐ 极其重要
- ⭐⭐⭐⭐ 重要
- ⭐⭐⭐ 值得关注
- ⭐⭐ 一般
- ⭐ 次要

## 技术依赖

- Python 3.10+
- feedparser (RSS 解析)
- crawlee (Playwright 爬虫)
- beautifulsoup4 (HTML 解析)
- requests (HTTP 请求)

**首次运行会自动安装缺少的依赖**

## 核心脚本

- `collect_news.py` - 新闻收集（RSS → jsonl）
- `daily_generator_v2.py` - 分析清单生成
- `category_classifier.py` - 新闻分类
- `news_fetcher.py` - 全文爬取
- `llm_generator.py` - LLM 提示词构建

## 作者

- **Leefee** - [GitHub](https://github.com/LeeFeee) - [X](https://x.com/leefee)

## License

MIT License
