---
name: daily-ai-brief
description: 每日 AI 内容源更新追踪与摘要。涵盖指定的 YouTube 播客、Twitter/X 博主及 Newsletter。适用于用户请求"RSS总结"、"日报"、"看看更新"时。
---

# Daily AI Brief - 每日 AI 简报

此 Skill 作为一个手动 RSS 聚合器，用于检查指定列表中的内容创作者在过去 24 小时内的更新，并生成带有原文链接的摘要报告。

## 1. 内容源列表

### 📺 视频播客频道 (YouTube)

| 频道名称 | 链接 |
|:---:|:---|
| **Latent Space** | [YouTube](https://www.youtube.com/playlist?list=PLWEAb1SXhjlfkEF_PxzYHonU_v5LPMI8L) |
| **AI & I** | [YouTube](https://www.youtube.com/playlist?list=PLuMcoKK9mKgHtW_o9h5sGO2vXrffKHwJL) |
| **Google DeepMind** | [YouTube](https://www.youtube.com/playlist?list=PLqYmG7hTraZBiUr6_Qf8YTS2Oqy3OGZEj) |
| **The AI Daily Brief** | [YouTube](https://www.youtube.com/playlist?list=PLRYSuzHGhXPmKnOpd-f588cNNmTe2S9FP) |
| **TBPN** | [YouTube](https://www.youtube.com/@TBPNLive) |
| **Training Data** | [YouTube](https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8) |
| **Lenny's Podcast** | [YouTube](https://www.youtube.com/@LennysPodcast) |
| **Behind the Craft** | [YouTube](https://www.youtube.com/playlist?list=PLIWHjbvRtljj4RewVNv_znkUe-3E-NKd2) |
| **No Priors** | [YouTube](https://www.youtube.com/@NoPriorsPodcast) |
| **Unsupervised Learning** | [YouTube](https://www.youtube.com/@RedpointAI) |
| **Minus One Podcast** | [YouTube](https://www.youtube.com/playlist?list=PLmYVYFmFwGm3txxUduawn7i53C5rDjjd7) |
| **Lightcone Podcast** | [YouTube](https://www.youtube.com/playlist?list=PLQ-uHSnFig5Ob4XXhgSK26Smb4oRhzFmK) |

### 🐦 X (Twitter) 博主

**核心关注名单：**
- **Andrej Karpathy**: [@karpathy](https://x.com/karpathy)
- **Swyx**: [@swyx](https://x.com/swyx)
- **Greg Isenberg**: [@gregisenberg](https://x.com/gregisenberg)
- **Lenny Rachitsky**: [@lennysan](https://x.com/lennysan)
- **Josh Woordward**: [@joshwoodward](https://x.com/joshwoodward)
- **Kevin Weil**: [@kevinweil](https://x.com/kevinweil)
- **Peter Yang**: [@petergyang](https://x.com/petergyang)
- **Nan Yu**: [@thenanyu](https://x.com/thenanyu)
- **Madhu Guru**: [@realmadhuguru](https://x.com/realmadhuguru)
- **Mckay Wrigley**: [@mckaywrigley](https://x.com/mckaywrigley)
- **Steven Johnson**: [@stevenbjohnson](https://x.com/stevenbjohnson)
- **Amanda Askell**: [@AmandaAskell](https://x.com/AmandaAskell)
- **Cat Wu**: [@_catwu](https://x.com/_catwu)
- **Thariq**: [@trq212](https://x.com/trq212)
- **Google Labs**: [@GoogleLabs](https://x.com/GoogleLabs)
- **George Mack**: [@george__mack](https://x.com/george__mack)
- **Raiza Martin**: [@raizamrtn](https://x.com/raizamrtn)
- **Amjad Masad**: [@amasad](https://x.com/amasad)
- **Guillermo Rauch**: [@rauchg](https://x.com/rauchg)
- **Riley Brown**: [@rileybrown](https://x.com/rileybrown)
- **Alex Albert**: [@alexalbert__](https://x.com/alexalbert__)
- **Hamel Husain**: [@HamelHusain](https://x.com/HamelHusain)
- **Aaron Levie**: [@levie](https://x.com/levie)
- **Ryo Lu**: [@ryolu_](https://x.com/ryolu_)
- **Garry Tan**: [@garrytan](https://x.com/garrytan)
- **Lulu Cheng Meservey**: [@lulumeservey](https://x.com/lulumeservey)
- **Justine Moore**: [@venturetwins](https://x.com/venturetwins)
- **Matt Turck**: [@mattturck](https://x.com/mattturck)
- **Julie Zhuo**: [@joulee](https://x.com/joulee)
- **Gabriel Peters**: [@GabrielPeterss4](https://x.com/GabrielPeterss4)
- **PJ Ace**: [@PJaccetturo](https://x.com/PJaccetturo)
- **Zara Zhang**: [@zarazhangrui](https://x.com/zarazhangrui)

### 📧 Newsletters

| 名称 | 地址 |
|:---|:---|
| **AI Valley** | https://www.theaivalley.com/ |
| **Every** | https://every.to/ |
| **The Keyword (Google)** | https://blog.google/ |
| **Ben's Bites** | https://bensbites.beehiiv.com/ |
| **AINews by smol.ai** | https://news.smol.ai/ |
| **Peter Yang (Creator Economy)** | https://creatoreconomy.so/ |

---

## 2. 执行流程 (Hybrid v2)

### 核心变更
本 Skill 现在支持 **自动数据抓取** 和 **邮件发送**。请优先使用 Python 脚本执行，以确保数据的绝对新鲜和准确。

### 第一步：自动化抓取 (Python)
运行 `feed_fetcher.py` 获取过去 27 小时内的所有更新。

**命令：**
```bash
python3 scripts/feed_fetcher.py
```
*(如果没有安装 `feedparser`，请先运行 `pip install feedparser`)*

**逻辑：**
- 如果输出 `NO_UPDATES_FOUND`，则说明主要渠道无更新。
- 如果输出 JSON 数据，请阅读该 JSON，作为撰写简报的**唯一事实来源**。

### 第二步：补充搜索 (WebSearch - 可选)
如果 Python 脚本未能覆盖某些非 RSS 源（如特定的 Twitter 讨论），可以使用 WebSearch 进行补充：
- QUERY: `twitter "Andrej Karpathy" OR "swyx" AI status after:2026-01-18`

### 第三步：撰写报告
根据获取的 JSON 数据和补充搜索结果，撰写 Markdown 简报。请保持原有的 Markdown 格式。

### 第四步：发送邮件 (可选)
如果用户配置了 SMTP 环境，可以使用 `email_sender.py` 发送。

**命令：**
```bash
# 需要先设置环境变量 (推荐在 .bashrc 或 .zshrc 中设置)
# export SMTP_USER="your@gmail.com"
# export SMTP_PASSWORD="app_password"

python3 scripts/email_sender.py "path/to/generated_report.md"
```

---

## 3. 输出模板 (保持不变)

```markdown
# 📅 [MM-DD] 每日 AI 观察简报 (v2)

> 🤖 **摘要**：[基于 JSON 数据的总结]

## 📺 视频 & 播客 (Verified)
*数据来源：RSS Feed*

- **[标题]**
  - 🔗 **观看**：[Link]
  - 📝 **简介**：[Summary from JSON]
  - ⏱️ **时间**：[Date]

(以下栏目根据是否有数据动态展示)
```

---

## 3. 输出模板

```markdown
# 📅 [MM-DD] 每日 AI 观察简报

> 🤖 **摘要**：今日重点更新主要集中在 [一句话总结核心趋势，如：OpenAI 新模型发布、Agent 开发工具等]...

## 📺 视频播客更新
*捕捉深度对话与行业趋势*

- **[频道名] - [视频标题]**
  - 🔗 **链接**：[URL]
  - 💡 **核心看点**：[一句话总结视频核心内容或嘉宾观点]
  - ⏱️ **发布时间**：[如：10小时前]

*(若无重要更新，注明：今日主要频道暂无重磅长视频更新)*

## 🐦 X (Twitter) 社区热议
*捕捉即时观点与技术动态*

- **@[博主名]**：[推文内容概括]
  - 🔗 **原文**：[Tweet URL]
  - 🔥 **话题**：#[Tag] [如：Cursor技巧、模型微调]

## 📧 Newsletters 精选
*深度阅读与行业汇总*

- **[Newsletter 名称] - [期号/标题]**
  - 🔗 **阅读**：[URL]
  - 📝 **摘要**：[简述本期主要涵盖的内容，如：3个新工具推荐、1篇深度分析]

---
*生成时间：YYYY-MM-DD HH:mm*
```

## 4. 注意事项
1.  **链接至关重要**：用户非常依赖原文链接，**必须**确保链接准确且可点击。
2.  **去重**：如果同一博主在 X 和 Newsletter 发了相同内容，优先展示 Newsletter 的深度内容，或在 X 中简要提及。
3.  **时效性**：严格把控时间，不要放入 3 天以前的旧闻。
4.  **失败处理**：如果无法获取某个特定源的更新，可以跳过，不要编造。
