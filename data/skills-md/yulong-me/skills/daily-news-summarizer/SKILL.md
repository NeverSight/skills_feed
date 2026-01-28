---
name: daily-news-summarizer
description: 自动总结多个新闻网站的当日要闻，使用浏览器自动化访问和读取新闻内容。适用于：用户请求"总结今天的新闻"、"获取今日要闻"、"生成新闻摘要"等任务；或用户询问"今天有什么重要新闻？"、"帮我看看新闻网站今天的头条"等问题。支持中文新闻网站（新浪、网易、腾讯等）和国际新闻网站（BBC、Reuters等），生成详细的Markdown格式摘要报告。
---

# 每日新闻摘要生成器

## Overview

此技能使用浏览器自动化（Playwright MCP工具）访问新闻网站，智能提取当日重要新闻并生成详细摘要。每个新闻条目包含3-5句话的AI摘要，最终输出为格式化的Markdown报告。

## 工作流程

### 第1步：确定新闻源

首先检查用户指定的新闻源。如果用户未指定，使用以下默认源：

**中文新闻网站：**
- 新浪新闻: https://news.sina.com.cn
- 网易新闻: https://news.163.com
- 腾讯新闻: https://news.qq.com
- 搜狐新闻: https://news.sohu.com

**国际新闻网站：**
- BBC News: https://www.bbc.com/news
- Reuters: https://www.reuters.com
- CNN: https://edition.cnn.com

**科技新闻：**
- 36氪: https://36kr.com
- 虎嗅: https://www.huxiu.com

如果用户有自定义配置文件 `~/.daily-news-config.yaml`，优先使用其中的配置。

### 第2步：访问新闻网站

使用Playwright MCP工具访问每个新闻源：

```bash
# 使用browser_navigate工具导航到网站
mcp__playwright__browser_navigate(url="https://news.sina.com.cn")
```

然后获取页面快照：

```bash
# 使用browser_snapshot获取页面可访问性快照
mcp__playwright__browser_snapshot()
```

### 第3步：提取新闻列表

从页面快照中分析并提取新闻条目。查找以下元素：

- 标题（headline/title）
- 链接（URL）
- 简短描述（description/excerpt，如果有）
- 时间信息（publish time，如果有）

**提取策略：**
1. 识别新闻列表区域（通常是包含多个文章链接的区域）
2. 提取每条新闻的标题和链接
3. 最多提取20条重要新闻
4. 去除重复和广告内容

示例代码模式：
```python
# 从快照中分析新闻链接
news_links = []
for item in snapshot:
    if '标题' in item or 'title' in str(item).lower():
        # 提取标题和链接
        news_links.append({
            'title': extract_title(item),
            'url': extract_url(item)
        })
```

### 第4步：访问具体新闻文章

对于提取的重要新闻（前10-15条），逐个访问完整文章页面：

```bash
# 导航到文章页面
mcp__playwright__browser_navigate(url=news_url)

# 获取文章内容快照
mcp__playwright__browser_snapshot()
```

从文章页面提取：
- 完整标题
- 正文内容
- 发布时间
- 作者信息（如果有）

### 第5步：生成AI摘要

为每篇文章生成3-5句话的详细摘要：

**摘要要求：**
1. 准确概括文章核心内容
2. 包含关键事实和细节（时间、地点、人物、事件）
3. 客观中立，不添加个人观点
4. 使用简洁明了的中文语言
5. 总共3-5句话，每句话信息量丰富

**提示词模板：**
```
请为以下新闻文章生成一个5句话的详细摘要。

标题：{title}

文章内容：
{content}

摘要要求：
1. 准确概括文章的核心内容
2. 包含关键事实和细节
3. 客观中立，不添加个人观点
4. 使用简洁明了的语言
5. 总共5句话，每句话信息量丰富

请生成摘要：
```

### 第6步：生成总体概述

在所有文章摘要生成后，生成一个当日新闻总体概述（3-5句话）：

**提示词模板：**
```
请为以下{count}条新闻生成一个总体概述（3-5句话），突出当日最重要的新闻主题和趋势：

新闻标题列表：
{titles}

请生成一个简短的总体概述：
```

### 第7步：生成Markdown报告

将所有内容整理成格式化的Markdown文件：

```markdown
# 每日新闻摘要

**日期**: 2024年01月07日
**生成时间**: 08:00
**新闻数量**: 15条

## 📰 今日概述

今日要闻的总体概述，3-5句话总结当日最重要的新闻主题...

## 📋 详细新闻

### 1. 新闻标题

**发布时间**: 2024-01-07 10:30
**来源**: [新浪新闻](https://example.com/article)

**摘要**: 第一句话摘要。第二句话摘要。第三句话摘要。第四句话摘要。第五句话摘要，包含关键细节。

---

### 2. 另一条新闻标题

**发布时间**: 2024-01-07 09:15
**来源**: [网易新闻](https://example.com/article2)

**摘要**: 摘要内容...

---

## 统计信息

- **总新闻数**: 15
- **新闻源**: 新浪新闻、网易新闻、BBC News
- **类别**: 时政、财经、科技、国际

*本摘要由AI自动生成，内容来源于各大新闻网站*
```

### 第8步：保存文件

将生成的Markdown保存到文件。默认位置：
- 目录: `~/Daily-News-Summary/`
- 文件名: `news-summary-{date}.md`（例如：news-summary-2024-01-07.md）

使用Write工具保存：
```python
Write(file_path="~/Daily-News-Summary/news-summary-2024-01-07.md", content=markdown_content)
```

## 处理特殊场景

### 场景1：用户询问特定主题的新闻

如果用户说"今天有什么科技新闻？"或"政治方面的新闻"：

1. 在提取新闻时进行过滤，只保留相关主题
2. 或者在访问时直接导航到对应的分类页面
   - 科技新闻: https://news.sina.com.cn/tech/
   - 财经新闻: https://news.sina.com.cn/finance/

### 场景2：用户指定新闻网站

如果用户说"总结BBC今天的新闻"或"只看新浪新闻"：

1. 只访问用户指定的新闻源
2. 跳过其他默认源

### 场景3：快速摘要模式

如果用户说"简单总结一下"或"快速浏览"：

1. 每篇文章只生成1-2句话摘要
2. 减少文章数量（5-10条）
3. 生成更简洁的总体概述

### 场景4：详细模式

如果用户说"详细总结"或"完整报告"：

1. 每篇文章生成5-7句话摘要
2. 增加文章数量（15-20条）
3. 为每篇文章添加更多细节（引用、数据等）

## 最佳实践

1. **并行处理**: 可以同时打开多个浏览器标签页访问不同新闻源，使用 `mcp__playwright__browser_tabs(action="new")` 创建新标签

2. **错误处理**: 如果某个网站无法访问，继续处理其他网站，并在最终报告中注明

3. **去重**: 不同新闻源可能报道同一事件，需要识别并合并重复新闻

4. **优先级排序**: 将重要新闻（时政、重大事件）放在前面

5. **时间信息**: 尽可能保留新闻的发布时间，并按时间倒序排列

6. **资源清理**: 任务完成后使用 `mcp__playwright__browser_close()` 关闭浏览器

## 调试和日志

在执行过程中，向用户报告进度：

```
✓ 正在访问新浪新闻...
✓ 已提取20条新闻
✓ 正在生成摘要 (1/20)...
✓ 正在生成摘要 (2/20)...
...
✓ 生成总体概述...
✓ 摘要已保存到 ~/Daily-News-Summary/news-summary-2024-01-07.md
```

## 配置文件（可选）

如果用户创建了 `~/.daily-news-config.yaml`，读取其配置：

```yaml
news_sources:
  - name: "新浪新闻"
    url: "https://news.sina.com.cn"
    enabled: true
    language: "zh"

  - name: "BBC News"
    url: "https://www.bbc.com/news"
    enabled: true
    language: "en"

output:
  directory: "~/Daily-News-Summary"
  format: "markdown"

summary:
  max_articles: 20
  sentences_per_article: 5
```

使用Read工具读取配置：
```python
Read(file_path="~/.daily-news-config.yaml")
```

## 完整示例对话

**用户**: 总结今天的新闻

**Claude**:
1. 访问新浪新闻首页
2. 访问网易新闻首页
3. 访问BBC News首页
4. 提取重要新闻列表
5. 逐个访问新闻文章页面
6. 生成每篇文章的详细摘要
7. 生成总体概述
8. 保存到 ~/Daily-News-Summary/news-summary-2024-01-07.md

✅ 已完成！共处理15条新闻，摘要已保存。
