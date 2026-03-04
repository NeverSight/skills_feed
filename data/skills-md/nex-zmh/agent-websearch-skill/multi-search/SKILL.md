---
name: multi-search
description: 智能多引擎搜索，自动检测网络环境并按优先级切换：DuckDuckGo -> Tavily -> Bing API -> Bing爬虫。支持自动配额管理和网络缓存。Invoke when user needs web search with automatic engine selection and network adaptation.
trigger: 当需要进行网络搜索、需要自动切换引擎、需要配额管理或网络环境可能变化时触发。
metadata: {"openclaw":{"emoji":"🔍","requires":{"python":["requests","tavily","duckduckgo_search"],"env":["TAVILY_API_KEY","BING_API_KEY"]},"install":[{"id":"pip","kind":"pip","package":"requests tavily duckduckgo_search","label":"Install dependencies (pip)"}]}}
---

# Multi-Search Skill - 智能多引擎搜索

本技能整合多个搜索引擎，自动检测网络环境，智能选择最佳可用引擎。

## 引擎优先级

### 质量优先模式 (prefer_quality=True)
1. Tavily API (1000次/月) - 质量最高，需 API Key
2. DuckDuckGo (无限免费) - 无需 API Key
3. Bing Web Search API (1000次/月) - 需 API Key
4. Bing 爬虫 (无限免费) - 最终回退

### 平衡模式 (prefer_quality=False, 默认)
1. DuckDuckGo (无限免费) - 优先免费引擎
2. Tavily API (1000次/月) - 如果配置了 API Key
3. Bing Web Search API (1000次/月)
4. Bing 爬虫 (无限免费)

## 核心能力

- 智能网络检测与引擎切换
- 自动配额管理（Tavily/Bing API）
- 支持网页内容抓取
- 5分钟网络检测缓存

## 使用方式

### 基本搜索
```python
from multi_search import search

# 平衡模式 - 优先免费引擎
results = search("Python tutorial", max_results=5)

# 质量优先模式 - 优先使用 Tavily
results = search("AI research", max_results=5, prefer_quality=True)

# 强制重新检测网络（切换 VPN 后使用）
results = search("OpenClaw skills", max_results=5, force_network_check=True)
```

### 搜索技能（自动质量优先）
```python
from multi_search import search_skills

results = search_skills("OpenClaw AI agent automation", max_results=10)
```

### 查看系统状态
```python
from multi_search import get_status

status = get_status()  # 使用缓存
status = get_status(force_network_check=True)  # 强制重新检测
```

### 抓取网页详细内容
```python
from multi_search import search, fetch_web_content, fetch_search_results_content

# 搜索并抓取第一个结果的详细内容
results = search("OpenClaw new features", max_results=3)
if results:
    content = fetch_web_content(results[0]['href'], max_length=3000)
    # content['title'], content['content'], content['success']

# 批量抓取所有搜索结果的详细内容
enriched_results = fetch_search_results_content(results, max_length=2000)
for r in enriched_results:
    if r.get('full_content'):
        # 使用 summarize 技能总结内容
        pass
```

### 与 Summarize 技能结合使用
```
OpenClaw 工作流：
1. 使用 multi-search 搜索关键词
2. 选择感兴趣的搜索结果
3. 使用 fetch_web_content() 抓取网页内容
4. 使用 summarize 技能总结网页内容
5. 将摘要呈现给用户
```

## 返回结果格式

```python
[
    {
        'title': '结果标题',
        'href': 'https://example.com',
        'body': '结果摘要...',
        'source': 'duckduckgo'  # 或 'tavily', 'bing_api', 'bing_scraper'
    }
]
```

## 参数说明

- `query`: 搜索关键词
- `max_results`: 最大结果数（默认5）
- `prefer_quality`: 是否优先质量（默认False）
- `force_network_check`: 是否强制重新检测网络（默认False）

## 注意事项

- DuckDuckGo: 免费无限，但某些网络环境无法访问
- Tavily: 质量高，需要 API key，1000次/月
- Bing API: 官方稳定，需要 Azure 账号，1000次/月
- Bing 爬虫: 免费无限，但可能受反爬影响
