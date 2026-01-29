---
name: ai-readability-audit
description: AI网站可读性审计，模拟AI爬虫视角检查网站结构，评估对LLM的友好程度，提供具体优化建议。
---

# AI 网站可读性审计

模拟 AI 爬虫的视角审计你的网站，检查结构化数据、Meta 信息是否对大模型友好。

## 为什么需要 AI 可读性审计？

传统的 SEO 审计关注 Googlebot，但 AI 搜索时代，你的网站还需要对 LLM 友好：
- **ChatGPT** 通过 Bing 抓取网页
- **Perplexity** 直接抓取和引用网站
- **Claude** 通过搜索增强回答问题

如果你的网站对 AI 不友好，就可能失去 AI 搜索带来的流量。

## 触发条件

当用户说以下内容时启动此技能：
- "检查这个网站对AI是否友好"
- "AI可读性审计"
- "LLM friendliness check"
- "网站AI优化检查"

## 工作流程

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  输入网站URL     │───▶│  获取HTML内容    │───▶│  提取关键特征    │
│                 │    │  (WebFetch)     │    │  Meta/Schema等  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
                              ┌─────────────────────────────────────┐
                              │           AI 可读性分析              │
                              │  • 结构化数据检查                    │
                              │  • 语义标签评估                      │
                              │  • 内容清晰度评分                    │
                              │  • 生成优化建议                      │
                              └─────────────────────────────────────┘
```

## 执行步骤

### 步骤 1：获取网页内容

使用 WebFetch 获取目标 URL 的完整 HTML 内容。

### 步骤 2：提取 HTML 特征

分析以下关键元素：

**Meta 信息**
```html
<title>...</title>
<meta name="description" content="...">
<meta name="keywords" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
```

**结构化数据**
```html
<script type="application/ld+json">...</script>
<!-- Schema.org 标记 -->
```

**语义标签**
```html
<header>, <nav>, <main>, <article>, <section>, <aside>, <footer>
<h1>, <h2>, <h3>...
```

**内容结构**
- 标题层级是否正确
- 段落长度是否合理
- 列表和表格使用情况
- 链接文本是否描述性

### 步骤 3：AI 可读性评估

按以下维度打分（每项 0-10 分）：

| 维度 | 权重 | 检查项 |
|------|------|--------|
| **结构化数据** | 25% | Schema.org、JSON-LD、Open Graph |
| **语义 HTML** | 20% | 语义标签使用、标题层级 |
| **Meta 完整性** | 15% | title、description、keywords |
| **内容清晰度** | 20% | 段落结构、关键信息位置 |
| **技术可访问性** | 20% | 无 JS 可读性、robots.txt |

**总分计算**：加权平均，满分 100 分

### 步骤 4：生成审计报告

```markdown
# AI 可读性审计报告

**网站**: [URL]
**审计时间**: YYYY-MM-DD HH:mm
**综合评分**: XX/100 ⭐⭐⭐☆☆

---

## 评分详情

| 维度 | 得分 | 状态 |
|------|------|------|
| 结构化数据 | X/10 | ✅/⚠️/❌ |
| 语义 HTML | X/10 | ✅/⚠️/❌ |
| Meta 完整性 | X/10 | ✅/⚠️/❌ |
| 内容清晰度 | X/10 | ✅/⚠️/❌ |
| 技术可访问性 | X/10 | ✅/⚠️/❌ |

---

## 检测结果

### ✅ 做得好的地方

1. [好的方面1]
2. [好的方面2]

### ❌ 需要改进的地方

1. **问题**: [问题描述]
   **影响**: [对AI可读性的影响]
   **建议**: [具体修复建议]

2. **问题**: [问题描述]
   **影响**: [对AI可读性的影响]
   **建议**: [具体修复建议]

---

## 详细分析

### 结构化数据

**检测到的 Schema 类型**:
- [x] Organization
- [ ] Article
- [ ] Product
- [ ] FAQ

**建议添加**:
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "author": {...}
}
```

### Meta 标签

| 标签 | 当前值 | 建议 |
|------|--------|------|
| title | [当前值] | [建议值] |
| description | [当前值] | [建议值] |

### 语义结构

**标题层级**:
```
H1: [标题] ✅
├── H2: [子标题]
│   ├── H3: [小节]
│   └── H3: [小节]
└── H2: [子标题]
```

**问题**: [如有问题]

---

## 优先修复清单

按影响程度排序：

1. 🔴 **高优先级**: [问题] - 预计提升 X%
2. 🟡 **中优先级**: [问题] - 预计提升 X%
3. 🟢 **低优先级**: [问题] - 预计提升 X%

---

## AI 搜索兼容性

| AI 搜索引擎 | 兼容性 | 说明 |
|-------------|--------|------|
| ChatGPT (Bing) | ⭐⭐⭐ | [说明] |
| Perplexity | ⭐⭐⭐ | [说明] |
| Google SGE | ⭐⭐ | [说明] |

---

*报告由 Claude Code 自动生成*
```

## 使用示例

### 示例 1：审计单个页面

```
用户: 帮我检查 https://example.com 对AI是否友好

Claude:
1. 获取页面 HTML
2. 提取 Meta、Schema 等信息
3. 评估各维度得分
4. 生成详细审计报告
```

### 示例 2：批量审计

```
用户: 检查这几个页面的AI可读性
- https://example.com/
- https://example.com/about
- https://example.com/pricing

Claude:
[依次审计每个页面，生成汇总报告]
```

## 数据存储

审计结果默认保存到：`~/.claude/cache/ai-readability-audit/`

建议保存以下文件（便于复查、对比与回归）：
- `audit-{域名}-{YYYYMMDD-HHMMSS}.md`：完整审计报告（可直接分享/粘贴）
- `audit-{域名}-{YYYYMMDD-HHMMSS}.json`：结构化结果（评分、问题清单、建议、关键证据）

可选（体积较大，按需开启）：
- `html-{域名}-{YYYYMMDD-HHMMSS}.html`：抓取到的原始 HTML（用于排查“抓取内容与页面不一致”）

## AI 可读性最佳实践

### 1. 必备的结构化数据

```html
<!-- 组织信息 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "公司名",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png"
}
</script>

<!-- 文章页面 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题",
  "author": {"@type": "Person", "name": "作者名"},
  "datePublished": "2025-01-01"
}
</script>
```

### 2. 语义 HTML 模板

```html
<main>
  <article>
    <header>
      <h1>文章标题</h1>
      <p>文章摘要/描述</p>
    </header>

    <section>
      <h2>第一部分</h2>
      <p>内容...</p>
    </section>

    <footer>
      <p>作者信息、发布日期等</p>
    </footer>
  </article>
</main>
```

### 3. 关键信息前置

```
✅ 好的结构：
[核心结论/定义] - 第一段
[支持论据1]
[支持论据2]
[详细解释]

❌ 不好的结构：
[背景介绍]
[历史沿革]
[详细解释]
[最后才是结论]
```

## 依赖工具

- **WebFetch**: 获取网页 HTML 内容
- **Write**: 保存审计报告

## 限制说明

- 只能审计可公开访问的页面
- SPA/JavaScript 渲染的内容可能无法完整获取
- 无法检测 robots.txt 对 AI 爬虫的限制

## 原始来源

改编自 n8n 模板：
- 模板ID: 4151
- 原名: AI SEO Readability Audit: Check Website Friendliness for LLMs
- 链接: https://n8n.io/workflows/4151
