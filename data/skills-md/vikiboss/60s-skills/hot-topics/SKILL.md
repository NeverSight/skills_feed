---
name: hot-topics
description: 获取微博、知乎、百度、抖音、今日头条、B站等主流中文平台的实时热搜榜单和热门话题。Use when users want to know trending topics, hot searches, or popular content on Chinese social media platforms.
license: MIT
metadata:
  author: vikiboss
  version: "1.0"
  api_base: https://60s.viki.moe/v2
  tags:
    - trending
    - social-media
    - hot-search
    - china
---

# Hot Topics & Trending Content Skill

This skill helps AI agents fetch trending topics and hot searches from major Chinese social media and content platforms.

## When to Use This Skill

Use this skill when users:
- Want to know what's trending on social media
- Ask about hot topics or viral content
- Need to understand current popular discussions
- Want to track trending topics across platforms
- Research social media trends

## Supported Platforms

1. **Weibo (微博)** - Chinese Twitter equivalent
2. **Zhihu (知乎)** - Chinese Quora equivalent
3. **Baidu (百度)** - China's largest search engine
4. **Douyin (抖音)** - TikTok China
5. **Toutiao (今日头条)** - ByteDance news aggregator
6. **Bilibili (B站)** - Chinese YouTube equivalent

## API Endpoints

| Platform | Endpoint | Description |
|----------|----------|-------------|
| Weibo | `/v2/weibo` | Weibo hot search topics |
| Zhihu | `/v2/zhihu` | Zhihu trending questions |
| Baidu | `/v2/baidu/hot` | Baidu hot searches |
| Douyin | `/v2/douyin` | Douyin trending videos |
| Toutiao | `/v2/toutiao` | Toutiao hot news |
| Bilibili | `/v2/bili` | Bilibili trending videos |

All endpoints use **GET** method and base URL: `https://60s.viki.moe/v2`

## How to Use

### Get Weibo Hot Searches

```python
import requests

def get_weibo_hot():
    response = requests.get('https://60s.viki.moe/v2/weibo')
    return response.json()

hot_topics = get_weibo_hot()
print("🔥 微博热搜：")
for i, topic in enumerate(hot_topics['data'][:10], 1):
    print(f"{i}. {topic['title']} - 热度: {topic['热度']}")
```

### Get Zhihu Hot Topics

```python
def get_zhihu_hot():
    response = requests.get('https://60s.viki.moe/v2/zhihu')
    return response.json()

topics = get_zhihu_hot()
print("💡 知乎热榜：")
for topic in topics['data'][:10]:
    print(f"· {topic['title']}")
```

### Get Multiple Platform Trends

```python
def get_all_hot_topics():
    platforms = {
        'weibo': 'https://60s.viki.moe/v2/weibo',
        'zhihu': 'https://60s.viki.moe/v2/zhihu',
        'baidu': 'https://60s.viki.moe/v2/baidu/hot',
        'douyin': 'https://60s.viki.moe/v2/douyin',
        'bili': 'https://60s.viki.moe/v2/bili'
    }
    
    results = {}
    for name, url in platforms.items():
        try:
            response = requests.get(url)
            results[name] = response.json()
        except:
            results[name] = None
    
    return results

# Usage
all_topics = get_all_hot_topics()
```

### Simple bash examples

```bash
# Weibo hot search
curl "https://60s.viki.moe/v2/weibo"

# Zhihu trending
curl "https://60s.viki.moe/v2/zhihu"

# Baidu hot search
curl "https://60s.viki.moe/v2/baidu/hot"

# Douyin trending
curl "https://60s.viki.moe/v2/douyin"

# Bilibili trending
curl "https://60s.viki.moe/v2/bili"
```

## Response Format

Responses typically include:

```json
{
  "data": [
    {
      "title": "话题标题",
      "url": "https://...",
      "热度": "1234567",
      "rank": 1
    },
    ...
  ],
  "update_time": "2024-01-15 14:00:00"
}
```

## Example Interactions

### User: "现在微博上什么最火？"

```python
hot = get_weibo_hot()
top_5 = hot['data'][:5]

response = "🔥 微博热搜 TOP 5：\n\n"
for i, topic in enumerate(top_5, 1):
    response += f"{i}. {topic['title']}\n"
    response += f"   热度：{topic.get('热度', 'N/A')}\n\n"
```

### User: "知乎上大家在讨论什么？"

```python
zhihu = get_zhihu_hot()
response = "💡 知乎当前热门话题：\n\n"
for topic in zhihu['data'][:8]:
    response += f"· {topic['title']}\n"
```

### User: "对比各平台热点"

```python
def compare_platform_trends():
    all_topics = get_all_hot_topics()
    
    summary = "📊 各平台热点概览\n\n"
    
    platforms = {
        'weibo': '微博',
        'zhihu': '知乎',
        'baidu': '百度',
        'douyin': '抖音',
        'bili': 'B站'
    }
    
    for key, name in platforms.items():
        if all_topics.get(key):
            top_topic = all_topics[key]['data'][0]
            summary += f"{name}：{top_topic['title']}\n"
    
    return summary
```

## Best Practices

1. **Rate Limiting**: Don't call APIs too frequently, data updates every few minutes
2. **Error Handling**: Always handle network errors and invalid responses
3. **Caching**: Cache results for 5-10 minutes to reduce API calls
4. **Top N**: Usually showing top 5-10 items is sufficient
5. **Context**: Provide platform context when showing trending topics

## Common Use Cases

### 1. Daily Trending Summary

```python
def get_daily_trending_summary():
    weibo = get_weibo_hot()
    zhihu = get_zhihu_hot()
    
    summary = "📱 今日热点速览\n\n"
    summary += "【微博热搜】\n"
    summary += "\n".join([f"{i}. {t['title']}" 
                          for i, t in enumerate(weibo['data'][:3], 1)])
    summary += "\n\n【知乎热榜】\n"
    summary += "\n".join([f"{i}. {t['title']}" 
                          for i, t in enumerate(zhihu['data'][:3], 1)])
    
    return summary
```

### 2. Find Common Topics Across Platforms

```python
def find_common_topics():
    all_topics = get_all_hot_topics()
    
    # Extract titles from all platforms
    all_titles = []
    for platform_data in all_topics.values():
        if platform_data and 'data' in platform_data:
            all_titles.extend([t['title'] for t in platform_data['data']])
    
    # Simple keyword matching (can be improved)
    from collections import Counter
    keywords = []
    for title in all_titles:
        keywords.extend(title.split())
    
    common = Counter(keywords).most_common(10)
    return f"🔍 热门关键词：{', '.join([k for k, _ in common])}"
```

### 3. Platform-specific Trending Alert

```python
def check_trending_topic(keyword):
    platforms = ['weibo', 'zhihu', 'baidu']
    found_in = []
    
    for platform in platforms:
        url = f'https://60s.viki.moe/v2/{platform}' if platform != 'baidu' else 'https://60s.viki.moe/v2/baidu/hot'
        data = requests.get(url).json()
        
        for topic in data['data']:
            if keyword.lower() in topic['title'].lower():
                found_in.append(platform)
                break
    
    if found_in:
        return f"✅ 话题 '{keyword}' 正在以下平台trending: {', '.join(found_in)}"
    return f"❌ 话题 '{keyword}' 未在主流平台trending"
```

### 4. Trending Content Recommendation

```python
def recommend_content_by_interest(interest):
    """Recommend trending content based on user interest"""
    all_topics = get_all_hot_topics()
    
    recommendations = []
    for platform, data in all_topics.items():
        if data and 'data' in data:
            for topic in data['data']:
                if interest.lower() in topic['title'].lower():
                    recommendations.append({
                        'platform': platform,
                        'title': topic['title'],
                        'url': topic.get('url', '')
                    })
    
    return recommendations
```

## Platform-Specific Notes

### Weibo (微博)
- Updates frequently (every few minutes)
- Includes "热度" (heat score)
- Some topics may have tags like "热" or "新"

### Zhihu (知乎)
- Focuses on questions and discussions
- Usually more in-depth topics
- Great for understanding what people are curious about

### Baidu (百度)
- Reflects search trends
- Good indicator of mainstream interest
- Includes various categories

### Douyin (抖音)
- Video-focused trending
- Entertainment and lifestyle content
- Young audience interests

### Bilibili (B站)
- Video platform trends
- ACG (Anime, Comic, Games) culture
- Creative content focus

## Troubleshooting

### Issue: Empty or null data
- **Solution**: API might be updating, retry after a few seconds
- Check network connectivity

### Issue: Old timestamps
- **Solution**: Data is cached, this is normal
- Most platforms update every 5-15 minutes

### Issue: Missing platform
- **Solution**: Ensure correct endpoint URL
- Check API documentation for changes

## Related Resources

- [60s API Documentation](https://docs.60s-api.viki.moe)
- [GitHub Repository](https://github.com/vikiboss/60s)
