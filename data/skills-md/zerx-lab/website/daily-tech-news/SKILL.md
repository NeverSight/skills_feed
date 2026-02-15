---
name: daily-tech-news
description: "每日技术资讯搜集。搜索 AI、GitHub、前端、后端、开源项目等技术领域的最新资讯，生成中文摘要博客文章。关键词：资讯、新闻、daily news、tech news、AI news、GitHub trending。"
---

# Daily Tech News - 每日技术资讯深度搜集

自动搜索并汇总当日技术资讯，采用**多源交叉验证 + 深度调研 + 重要性评分**机制，生成高质量 Markdown 博客文章。

---

## ⚠️ 必需参数

**调用此 skill 时必须在 prompt 中指定目标日期：**

```
TARGET_DATE: YYYY-MM-DD 格式的日期
示例: 2026-02-02
```

**正确的调用方式：**
- ✅ "执行 /daily-tech-news 搜集 2026-02-02 的技术资讯"
- ✅ "运行 daily-tech-news skill，日期：2026-02-02"
- ❌ "执行 /daily-tech-news" （缺少日期参数）

执行过程中的所有日期（文件名、frontmatter、标题、搜索关键词）都必须使用此 TARGET_DATE。

---

## 核心理念

> **准确性第一** → 多源交叉验证 + 深度阅读原文
> **质量优于数量** → 重要性评分筛选 + 去重降噪
> **深度优于广度** → Top 3 资讯深度分析 + 技术解读

---

## Phase 1: 准备阶段

### Step 1.1: 确定搜索日期

**重要：日期必须从调用参数中获取，而非自行计算。**

当 GitHub Actions 或用户调用此 skill 时，会在 prompt 中指定目标日期。你必须：

1. **从 prompt 中提取日期**：查找 prompt 中明确指定的日期（格式：YYYY-MM-DD）
2. **使用该日期作为 `TARGET_DATE`**：所有后续操作都基于此日期
3. **禁止自行推算日期**：不要使用"昨天"、"今天"等相对日期

```
TARGET_DATE = 从 prompt 参数中提取的日期
格式: YYYY-MM-DD
示例: 2026-02-02
```

**日期使用规则：**
- 文件名：`daily-tech-news-{TARGET_DATE}.mdx`
- frontmatter date：`{TARGET_DATE}`
- 标题日期：将 TARGET_DATE 转换为中文格式（如 2026年02月02日）
- 搜索关键词：使用 TARGET_DATE

### Step 1.2: 初始化去重缓存

检查近 7 天已发布的资讯，避免重复报道：

```
读取 content/blog/daily-tech-news-*.mdx 最近 7 篇
提取已报道的：项目名、公司名、事件关键词
建立去重列表
```

---

## Phase 2: 多源深度搜索

### Step 2.1: 第一层 - 权威官方源（优先级最高）

**必须访问的权威源：**

| 来源 | URL | 说明 |
|------|-----|------|
| Hacker News | https://news.ycombinator.com/ | 技术社区风向标 |
| GitHub Trending | https://github.com/trending | 开源项目趋势 |
| Trendshift | https://trendshift.io/ | GitHub 趋势分析 |
| Product Hunt | https://www.producthunt.com/ | 新产品发布 |

**使用 WebFetch 直接获取**，提取当日热门内容（Top 10）。

### Step 2.2: 第二层 - 专业媒体源

**每个领域搜索 2-3 个专业关键词组合：**

#### AI / LLM 领域
```
搜索策略（按优先级）：
1. site:techcrunch.com AI {date}
2. site:theverge.com artificial intelligence {date}
3. "OpenAI" OR "Anthropic" OR "Google AI" announcement {date}
4. "LLM" OR "GPT" OR "Claude" release {date}
5. machine learning breakthrough research {date}
```

#### GitHub / 开源领域
```
搜索策略：
1. site:github.blog {date}
2. "open source" major release {date}
3. GitHub "stars" trending repository {date}
```

#### 前端开发
```
搜索策略：
1. site:reactjs.org OR site:vuejs.org blog {date}
2. "React" OR "Vue" OR "Next.js" OR "Svelte" release {date}
3. frontend framework update {date}
4. JavaScript TypeScript major update {date}
```

#### 后端 / 基础设施
```
搜索策略：
1. site:kubernetes.io blog {date}
2. "Rust" OR "Go" programming release {date}
3. "Docker" OR "Kubernetes" announcement {date}
4. cloud infrastructure AWS Azure GCP {date}
```

#### 科技行业动态
```
搜索策略：
1. site:crunchbase.com funding {date}
2. tech startup Series A B C funding {date}
3. developer tools company announcement {date}
```

### Step 2.3: 第三层 - 中文技术社区

**补充中文原创内容：**
```
搜索策略：
1. site:juejin.cn 热门 {date}
2. site:infoq.cn {date}
3. site:segmentfault.com 头条 {date}
```

---

## Phase 3: 深度调研与验证

### Step 3.1: 信息交叉验证

**对每条候选资讯执行：**

```
1. 核心事实提取：
   - WHO: 涉及的公司/人物/项目
   - WHAT: 具体发生了什么
   - WHEN: 准确时间
   - WHERE: 发生地点/平台
   - WHY: 为什么重要

2. 多源验证（至少 2 个独立来源）：
   - 来源 A 报道 → WebFetch 获取原文
   - 来源 B 验证 → WebSearch 搜索相同事件
   - 对比核心事实是否一致

3. 置信度标记：
   ✓ 已验证（2+ 源确认）
   ? 待验证（仅单一来源）
   ⚠️ 有争议（来源间有矛盾）
```

### Step 3.2: 深度阅读原文

**对 Top 10 候选资讯，使用 WebFetch 获取完整内容：**

```
WebFetch 提取要点：
1. 文章核心论点
2. 关键数据和事实
3. 专家引用和评论
4. 技术细节和实现方式
5. 对开发者的实际影响
```

### Step 3.3: 重要性评分

**对每条资讯打分（满分 100 分）：**

| 维度 | 权重 | 评分标准 |
|------|------|----------|
| 影响范围 | 25% | 影响多少开发者？全球性 vs 局部性 |
| 实用性 | 25% | 开发者能否立即应用？解决什么问题？ |
| 新颖性 | 20% | 首次公布 vs 重复报道？突破性 vs 渐进式？ |
| 信息深度 | 15% | 有技术细节 vs 只有标题？ |
| 权威性 | 15% | 官方发布 vs 小道消息？来源可靠度？ |

**评分示例：**
```
Kubernetes 1.33 原生支持 Sidecar
- 影响范围: 24/25 (全球 K8s 用户)
- 实用性: 23/25 (直接改变部署方式)
- 新颖性: 18/20 (首次正式发布)
- 信息深度: 14/15 (有技术实现细节)
- 权威性: 15/15 (官方发布)
= 总分: 94/100 ⭐⭐⭐⭐⭐
```

### Step 3.4: 去重与降噪

**排除以下内容：**

```
❌ 标题党检测：
- 标题含"震惊"、"重磅"、"曝光"但无实质内容
- 标题与正文关键词严重不匹配
- 过多感叹号和问号

❌ 低质内容过滤：
- 与开发者无关的泛科技新闻
- 无具体信息的笼统报道（如"AI 继续发展"）
- 7 天内已报道过的重复事件
- 单一来源且无法验证的消息

❌ 内容去重：
- 同一事件的多篇报道只保留信息最丰富的一篇
- 优先保留官方来源 > 专业媒体 > 泛媒体
```

---

## Phase 4: Top 3 深度分析

### Step 4.1: 选择当日最重要的 3 条资讯

根据重要性评分，选择得分最高的 3 条资讯进行深度分析。

### Step 4.2: 深度分析模板

对每条 Top 3 资讯，撰写深度分析：

```
### [标题] ⭐⭐⭐⭐⭐

**核心要点：**
- 要点1：[具体事实]
- 要点2：[具体事实]
- 要点3：[具体事实]

**技术解读：**
[这意味着什么？对开发者有什么影响？技术上如何实现？]

**背景上下文：**
[这个事件的历史背景是什么？为什么现在发生？]

**开发者行动建议：**
- 建议1：[具体可执行的行动]
- 建议2：[具体可执行的行动]

**相关链接：**
- 官方公告: [链接]
- 技术文档: [链接]
- 社区讨论: [链接]
```

---

## Phase 5: 生成博客文章

### Step 5.1: 文件结构

在 `content/blog/` 目录创建 MDX 文件。

**重要：必须使用 Phase 1 中从 prompt 提取的 `TARGET_DATE`**

**文件名**: `daily-tech-news-{TARGET_DATE}.mdx`

### Step 5.2: 内容模板

**日期格式转换：**
- `TARGET_DATE` 格式：`2026-02-02`
- 中文日期格式：`2026年02月02日`
- frontmatter date 格式：`2026-02-02`（与 TARGET_DATE 相同）

```mdx
---
title: 每日技术资讯 - {TARGET_DATE 转换为中文格式}
description: {当日资讯亮点摘要，50-100字，突出 Top 3。末尾添加"今日共收录N条经多源验证的重要技术资讯。"}
date: {TARGET_DATE}
---

## 🔥 今日焦点

{Top 3 资讯的深度分析，使用 Phase 4 的深度分析模板}

---

## AI / 人工智能

### {标题} ⭐⭐⭐⭐

{摘要内容，3-5句话，包含核心事实}

**为什么重要：** {一句话解释对开发者的影响}

- 来源: [{来源名称}]({URL})
- 验证: ✓ 多源确认

### {标题2}
...

## GitHub / 开源

### GitHub 热门项目

本日 GitHub 趋势榜热门项目：

- **[owner/repo-name](https://github.com/owner/repo-name)** (TypeScript, 12.5k ⭐) ⭐⭐⭐⭐
  AI 驱动的代码编辑器插件，支持多种 IDE。
  **亮点：** {为什么这个项目值得关注}

- **[owner/another-repo](https://github.com/owner/another-repo)** (Python, 8.2k ⭐) ⭐⭐⭐
  轻量级机器学习框架，专注于边缘设备部署。

- 来源: [GitHub Trending](https://github.com/trending), [Trendshift](https://trendshift.io/)

### {其他开源资讯}
...

## 前端开发

...

## 后端 / 基础设施

...

## 科技动态

...

---

## 📊 今日数据

| 指标 | 数值 |
|------|------|
| 搜索源数量 | {N} 个 |
| 候选资讯 | {N} 条 |
| 去重后 | {N} 条 |
| 最终收录 | {N} 条 |
| 多源验证率 | {N}% |

---

> 本文由 Claude 自动生成，采用多源交叉验证机制。如发现错误，欢迎反馈。
```

---

## Phase 6: 质量检查与提交

### Step 6.1: 最终质量检查

```
□ 所有资讯都有来源链接
□ Top 3 资讯都有深度分析
□ 重要性评分标记完整
□ 无重复内容
□ 无明显事实错误
□ MDX 安全检查（必须逐项确认）：
  □ 正文中无裸露的 < 符号（代码块内除外），已用 &lt; 替代
  □ 代码块语言标识符均为 Shiki 支持的语言（不确定则用 text）
  □ 正文中无裸露的 {} 花括号（代码块内除外）
□ 中文表达通顺
```

### Step 6.2: 提交更改

```bash
git add content/blog/daily-tech-news-{date}.mdx
git commit -m "docs: add daily tech news for {date}"
```

---

## 输出要求

| 要求 | 说明 |
|------|------|
| 语言 | 全部使用中文 |
| 格式 | MDX 文件，兼容 Next.js 博客 |
| 普通资讯长度 | 50-150 字摘要 |
| Top 3 深度分析 | 200-400 字/条 |
| 来源标注 | 必须标注原文链接 + 验证状态 |
| 分类数量 | 至少 3 个分类 |
| 总资讯数 | 10-20 条（质量优先） |
| 重要性评分 | 每条资讯标注 1-5 星 |

---

## 信息源优先级

### 第一优先级（权威官方）
- GitHub 官方博客、Trending
- 各框架/语言官方博客（React、Vue、Rust、Go 等）
- 公司官方公告（Google、Microsoft、AWS 等）

### 第二优先级（专业媒体）
- Hacker News（社区风向标）
- TechCrunch、The Verge（科技深度报道）
- InfoQ、掘金（中文技术社区）

### 第三优先级（泛媒体）
- 一般科技新闻网站
- 社交媒体热点
- 个人博客

---

## 标题党识别规则

**自动降权或排除：**

```
❌ 情绪化词汇过多：震惊、重磅、曝光、惊天、颠覆
❌ 过度夸张：史上最强、彻底改变、完全碾压
❌ 模糊表述：某公司、据说、可能、或将
❌ 无实质内容：AI 继续发展、技术在进步
❌ 标题与内容不符：标题说重大突破，内容只是小更新
```

---

## ⚠️ MDX 安全规则（必须严格遵守）

MDX 不是普通 Markdown，它会将内容解析为 JSX。以下规则**必须**在生成内容时遵守，否则会导致 Vercel 构建失败：

### 规则 1：转义裸露的 `<` 符号

MDX 会把 `<` 解析为 JSX 标签开始。在非 HTML/JSX 上下文中的 `<` **必须**用 `&lt;` 替代。

**常见触发场景和修复方式：**

```
❌ 影响版本 <1.123.17 的用户    → 报错：Unexpected character `1`
✅ 影响版本 &lt;1.123.17 的用户

❌ 当 x < 10 时               → 报错：Unexpected character `1`
✅ 当 x &lt; 10 时

❌ Array<string>              → 报错：解析为 JSX
✅ `Array<string>`            → 用行内代码包裹
✅ Array&lt;string&gt;         → 或用 HTML 实体
```

**注意：** 在代码块（` ``` `）内部的 `<` 不需要转义，代码块内是安全的。

### 规则 2：代码块语言标识符必须是 Shiki 支持的语言

代码块的语言标识符（` ```language `）必须使用 Shiki 已知的语言名称，否则构建时会报 `ShikiError: Language "xxx" is not included in this bundle`。

**安全的语言标识符（常用）：**
```
text, plaintext, txt, bash, shell, sh, javascript, js, typescript, ts,
python, py, json, yaml, yml, html, css, sql, go, rust, java, c, cpp,
markdown, md, diff, toml, xml, graphql, docker, dockerfile, ini, csv
```

**不存在的/不安全的语言标识符：**
```
❌ ```td        → Shiki 无此语言，改用 ```text
❌ ```nushell   → Shiki 无此语言，改用 ```shell 或 ```text
❌ ```hcl       → 改用 ```text
```

**原则：如果不确定某个语言是否被 Shiki 支持，一律使用 `text`。**

### 规则 3：花括号 `{}` 会被解析为 JSX 表达式

MDX 中的 `{` 和 `}` 在正文中会被当作 JSX 表达式求值。

```
❌ 格式：{名称}    → 报错：名称 is not defined
✅ 格式：\{名称\}  → 转义
✅ 格式：`{名称}`  → 用行内代码包裹
```

**注意：** 在代码块内部的 `{}` 不需要转义。

---

## 注意事项

1. **深度优于广度**：宁可收录 10 条高质量资讯，也不要 30 条低质内容
2. **验证优于速度**：确保每条资讯经过多源验证
3. **解读优于转述**：提供技术解读和开发者行动建议
4. **去重优于重复**：检查近 7 天已发布内容，避免重复报道
5. **英文搜索 + 中文输出**：搜索时使用英文关键词效果更好
6. **保持客观中立**：避免主观评价和情绪化表达
