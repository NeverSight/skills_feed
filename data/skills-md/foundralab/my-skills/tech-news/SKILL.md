---
name: tech-news
description: |
  聚合科技新闻并生成中文Markdown日报。抓取 Hacker News、GitHub Trending 等，
  翻译标题与摘要，可选上传配图到R2。Use when: 用户说"生成今日科技新闻"、"科技新闻"、"tech news"等。
triggers:
  - 生成今日科技新闻
  - 科技新闻
  - tech news
  - 抓取科技新闻
  - 获取今日新闻
inputs:
  - name: sources
    type: array
    description: 新闻源列表
    default: ["hackernews", "reddit-programming", "github-trending", "devto", "lobsters", "paperswithcode", "huggingface", "arxiv-ai"]
  - name: limit
    type: integer
    description: 最终精选文章数量
    default: 10
  - name: with_images
    type: boolean
    description: 是否抓取配图上传R2
    default: true
outputs:
  - name: markdown_content
    type: string
    description: Markdown格式新闻汇总
---

# 科技新闻聚合

从多源抓取热门科技新闻，翻译成中文并生成Markdown汇总，可选上传配图到R2。

## 使用场景

- 生成每日科技新闻汇总
- 需要多源聚合 + 中文摘要
- 需要带图片的Markdown报告

## 前置条件

- Python 3.8+ (`python3`)
- 翻译API：`MINIMAX_API_KEY` 或 `OPENAI_API_KEY`（Minimax 默认 `MiniMax-M2.1-lightning`）
- 图片上传（可选）：`~/.r2-upload.yml` 或 `R2_UPLOAD_CONFIG`
- 网络可访问新闻源与图片
- 可选性能参数：`FETCH_WORKERS`（默认 4）、`TRANSLATE_WORKERS`（默认 3）

## 推荐流程

1. 确认日期、来源、数量、是否需要图片与输出路径。
2. 运行 `python3 scripts/generate.py ...`。
3. 复查标题翻译、摘要质量、重复项与图片链接。
4. 如图片失败，可用 `--no-images` 重新生成或用 `scripts/process_images.py` 补图。

## 快速使用

```bash
python3 scripts/generate.py --date $(date +%F) --save ./news.md
```

## 常用参数

- `--sources <list>`: 指定新闻源（默认：hackernews reddit-programming github-trending devto lobsters paperswithcode huggingface arxiv-ai）
- `--count <n>`: 每源抓取数量（默认：15）
- `--limit <n>`: 最终精选数量（默认：10）
- `--max-images <n>`: 处理图片上限（默认：10）
- `--no-images`: 禁用图片处理
- `--output-only`: 仅输出Markdown

## 分类规则

- **AI与机器学习**: ai, llm, gpt, claude, model
- **开发工具与开源**: rust, python, github, framework
- **基础设施与云原生**: cloud, aws, kubernetes, docker
- **产品与设计**: product, design, ui, startup
- **趣闻与观点**: 其他

## 输出格式

采用固定结构，确保一致性：

```markdown
# 📰 YYYY-MM-DD 科技早报

> 📊 **今日导读**
> 精选 10 条科技新闻
> 来源：Hacker News(4) | GitHub Trending(3) | Lobsters(3)

---

## 📋 文章速览

**AI与机器学习**：3 篇
1. 文章标题一
2. 文章标题二
...

---

## AI 与机器学习

### 1. 文章中文标题

📰 **Hacker News**

<img src="https://r2.example.com/image.jpg" width="100%">

**摘要**：中文摘要内容...

**核心要点**：
• 要点一
• 要点二
• 要点三

🔗 [阅读原文](https://example.com)

---
```

完整模板与示例见 `references/EXAMPLES.md`。

## 参考

- `references/WORKFLOW.md`
- `references/SOURCES.md`
- `references/EXAMPLES.md`
