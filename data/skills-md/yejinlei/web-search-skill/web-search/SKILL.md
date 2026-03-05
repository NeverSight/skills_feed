---
name: web-search
description: 通用网络搜索技能，支持多引擎搜索（百度、必应、DuckDuckGo），无需API密钥即可获取实时信息
version: 1.3.0
author: yejinlei
license: MIT
tags:
  - search
  - web
  - internet
  - baidu
  - bing
---

# Web Search Skill

A powerful web search skill supporting multiple search engines without requiring API keys.

## Features

- 🔍 **Multi-Engine Support**: Baidu (Playwright), Bing, DuckDuckGo
- 🌐 **No API Key Required**: Uses browser automation and web scraping
- 🔄 **Smart Fallback**: Automatically switches engines when one fails
- 📊 **Structured Results**: Returns clean search results with title, URL, and snippet
- 🚀 **High Performance**: Async support with Playwright browser automation

## Usage

### Basic Search

```python
result = main({
    "action": "search",
    "query": "Python tutorial",
    "num_results": 5
})
```

### Deep Search

```python
result = main({
    "action": "deep_search",
    "query": "machine learning latest research",
    "num_results": 5
})
```

### Web Page Crawling

```python
result = main({
    "action": "crawl",
    "url": "https://example.com"
})
```

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | string | Yes | Operation type: "search", "deep_search", or "crawl" |
| query | string | Conditional | Search query (required for search/deep_search) |
| url | string | Conditional | Target URL (required for crawl) |
| num_results | int | No | Number of results, default 5, max 20 |
| region | string | No | Region code, default 'cn-zh' |

## Output Format

### Search Result

```python
{
    "success": True,
    "query": "search query",
    "engine": "baidu+playwright",
    "num_results": 5,
    "results": [
        {
            "title": "Result title",
            "href": "https://...",
            "body": "Snippet content"
        }
    ],
    "message": "Search completed"
}
```

### Deep Search Result

```python
{
    "success": True,
    "query": "search query",
    "search_results": [...],
    "detailed_info": {
        "extracted_content": "..."
    },
    "message": "Deep search completed"
}
```

## Execution

**type**: script
**script_path**: scripts/web_search.py
**entry_point**: main
**dependencies**: 
  - uv>=0.1.0
  - requests>=2.28.0
  - baidusearch>=1.0.3
  - crawl4ai>=0.8.0
  - playwright>=1.40.0

## Search Strategy

1. **Primary**: `baidusearch` library (fastest, no browser)
2. **Secondary**: Playwright + Baidu (most reliable, bypasses anti-bot)
3. **Tertiary**: DuckDuckGo (privacy-focused)
4. **Fallback**: Bing (international)

## Notes

1. **First Run**: Playwright will download Chromium browser on first use (~100MB)
2. **Rate Limiting**: Be mindful of search frequency to avoid temporary blocks
3. **Network**: Requires internet connection
4. **Results**: May vary based on search engine algorithms and location

## Error Handling

- Returns `{"success": False, "message": "..."}` on errors
- Automatically retries with fallback engines
- Graceful degradation when optional dependencies are missing
