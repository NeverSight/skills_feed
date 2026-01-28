---
name: seo-analyzer
description: 基于 Google 官方文档的 SEO 自动检测工具。自动分析网址的技术 SEO、内容元数据、性能体验和链接结构，输出符合 Google 最佳实践的检测报告。使用场景：(1) 分析网站 SEO 状况，(2) 诊断搜索引擎排名问题，(3) 验证页面是否符合 Google Search Essentials 标准，(4) 生成可执行的 SEO 优化建议。
---

# SEO Analyzer Skill

基于 Google 官方文档的 SEO 自动检测工具。自动分析网址的技术 SEO、内容元数据、性能体验和链接结构，输出符合 Google 最佳实践的检测报告。

## 使用方法

### 自动模式 (推荐)

只需告诉 agent 检查某个 URL，skill 会自动完成所有工作：

```bash
python skills/seo-analyzer/scripts/seo_analyzer.py --auto <url>
```

**Skill 会自动:**
1. 检查 agent-browser 是否已安装
2. 如果已安装，调用 agent-browser 获取页面内容
3. 执行完整的 SEO 检查
4. 生成详细的检测报告

### 手动模式

如果 agent-browser 未安装，可以使用手动模式：

```bash
# 方式1: 从文件分析
python skills/seo-analyzer/scripts/seo_analyzer.py page.html <url>

# 方式2: 从 stdin 读取 (需要先手动获取 HTML)
agent-browser get source > page.html
python seo_analyzer.py page.html <url>
```

## 对于 Agent 的调用方式

当用户请求分析某个 URL 时：

```bash
# 使用自动模式
python skills/seo-analyzer/scripts/seo_analyzer.py --auto https://example.com
```

Agent 内部会：
1. 调用 `check_agent_browser_available()` 检查 agent-browser
2. 如果可用，调用 `fetch_page_with_agent_browser(url)` 获取页面
3. 如果不可用，提示用户安装 agent-browser
4. 调用 `analyze_page()` 执行 SEO 分析
5. 输出格式化报告

**Alternative** - save to file first:
```bash
# Step 1: Open page
agent-browser open <url> --timeout 30000

# Step 2: Save HTML to file
agent-browser get source > /tmp/page.html

# Step 3: Run analysis
python skills/seo-analyzer/scripts/seo_analyzer.py /tmp/page.html <url>
```

### Command-line Options

```bash
# Analyze HTML file
python skills/seo-analyzer/scripts/seo_analyzer.py page.html https://example.com

# Read from stdin (pipe from agent-browser)
agent-browser get source | python skills/seo_analyzer.py - https://example.com

# Output in JSON format (for programmatic use)
python seo_analyzer.py page.html https://example.com --json
```

## Workflow

1. **Crawl the URL** - Use agent-browser to load the page and capture HTML
2. **Extract page content** - Use `agent-browser get source` to get HTML
3. **Run SEO checks** - Pass HTML to seo_analyzer.py for evaluation
4. **Generate report** - Output findings with severity levels and recommendations

## For Agents: How to Analyze a URL

When asked to analyze a website's SEO, follow these steps:

```bash
# 1. Open the URL with agent-browser
agent-browser open <target_url> --timeout 30000

# 2. Get the HTML source from the browser
agent-browser get source > /tmp/target_page.html

# 3. Run the SEO analyzer
python skills/seo-analyzer/scripts/seo_analyzer.py /tmp/target_page.html <target_url>
```

**Or as a single command:**
```bash
agent-browser open <target_url> --timeout 30000 && agent-browser get source | python skills/seo-analyzer/scripts/seo_analyzer.py - <target_url>
```
agent-browser open <url> --timeout 30000
```

### Step 2: Extract the page HTML
After the page loads, get the HTML content:
```
agent-browser get source
```
Or use get text to extract visible content:
```
agent-browser get text "body"
```

### Step 3: Save HTML to file and run analysis
Write the HTML to a file, then run the analyzer:
```bash
# Save HTML content to a file
echo "<html>...</html>" > /tmp/page.html

# Run the SEO analyzer
python skills/seo-analyzer/scripts/seo_analyzer.py /tmp/page.html <url>
```

### Integrated workflow (recommended)
Use stdin to pass HTML directly:
```bash
agent-browser get source | python skills/seo-analyzer/scripts/seo_analyzer.py - <url>
```

## Alternative: Analyze existing HTML file
If you already have HTML content saved:
```bash
python skills/seo-analyzer/scripts/seo_analyzer.py /path/to/page.html https://example.com/page
```

## Check Categories

### 1. Technical Requirements (搜索要素/技术要求)
- HTTP status code (must be 200)
- Googlebot accessibility
- Indexable content presence
- HTTPS usage
- robots.txt blocking detection
- noindex directive check

### 2. Title Tag (标题链接)
- Presence of `<title>` element
- Uniqueness across pages
- Descriptive, non-generic text
- Avoid keyword stuffing
- Proper length (not truncated)
- Brand inclusion if appropriate

### 3. Meta Description (片段)
- Presence of `<meta name="description">`
- Unique per page
- Descriptive, summarizes content
- Not keyword-stuffed
- Appropriate length

### 4. Headings Structure (SEO新手指南)
- H1 presence and uniqueness
- Logical heading hierarchy (H1→H2→H3)
- Heading text is descriptive
- Content is organized with headings

### 5. Link Accessibility (链接)
- Links use `<a href="...">` format
- Anchor text is descriptive
- No empty links
- No excessive link clustering
- External links use appropriate rel attributes (nofollow, sponsored, ugc)

### 6. Image Optimization (图像)
- Images have alt attributes
- Alt text is descriptive
- Images are near relevant content

### 7. Structured Data (结构化数据)
- JSON-LD, Microdata, or RDFa presence
- Valid schema.org types
- Required properties for supported types
- Content is visible to users
- Not blocked by robots.txt or noindex

### 8. URL Structure (网址结构)
- Descriptive URLs (not random IDs)
- Human-readable
- Logical directory structure
- Uses hyphens, not underscores

### 9. Canonical URL (规范化)
- Canonical tag presence
- Points to preferred URL
- HTTPS preferred over HTTP
- Consistent with actual URL

### 10. Content Quality (创建实用可靠以用户为中心的内容)
- Unique, original content
- Well-written, readable text
- No spelling/grammar errors
- Content is current/updated
- Provides value to users

### 11. Mobile-Friendliness (移动网站)
- Mobile-compatible design
- Touch-friendly elements
- Readable without zooming

### 12. Core Web Vitals (Core Web Vitals)
- LCP < 2.5s
- INP < 200ms
- CLS < 0.1
(Note: Requires JavaScript runtime measurement)

## Report Format

```markdown
# SEO Analysis Report

URL: <analyzed url>
Timestamp: <analysis time>

## Summary
- Total Issues: <count>
- Critical: <count>
- Warnings: <count>
- Passed: <count>

## Critical Issues
1. [Issue name]
   - Description
   - Location: <HTML element/selector>
   - Recommendation
   - Reference: seo-docs/<category>/<file>.md

## Warnings
1. [Issue name]
   - ...

## Passed Checks
- [Check name]
```

## Recommendations Priority

1. **Critical**: Must fix (blocks indexing/ranking)
2. **Warning**: Should fix (impacts performance)
3. **Info**: Nice to have (improves appearance)

## Reference Documents

Key seo-docs for SEO analysis:
- `seo基础知识/seo新手指南.md` - General SEO best practices
- `搜索要素/技术要求.md` - Technical requirements
- `排名和搜索结果呈现/标题链接.md` - Title tag guidelines
- `排名和搜索结果呈现/片段.md` - Meta description guidelines
- `排名和搜索结果呈现/结构化数据/了解结构化数据的工作方式.md` - Structured data
- `抓取和编入索引/链接.md` - Link accessibility
- `抓取和编入索引/规范化/如何使用relcanonical.md` - Canonical URLs
- `抓取和编入索引/robots.txt/概览.md` - robots.txt rules
- `排名和搜索结果呈现/网页体验/Core Web Vitals.md` - Core Web Vitals

## Limitations

- Cannot measure Core Web Vitals without JavaScript runtime
- Cannot verify if page is actually indexed in Google
- Cannot access server configuration (SSL, redirects)
- Content quality assessment is heuristic-based
- Mobile-friendliness is approximate without device simulation

## Integration with agent-browser

When analyzing a page:
1. Open page: `agent-browser open <url> --timeout 30000`
2. Get HTML: Use browser's get source function
3. Parse and analyze using SEO rules from seo-docs
4. Report findings with specific element selectors for fixes
