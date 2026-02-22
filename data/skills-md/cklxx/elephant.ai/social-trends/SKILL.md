---
name: social-trends
description: 社交媒体热点趋势分析（抖音、微博、小红书等）。
triggers:
  intent_patterns:
    - "热点|trending|热搜|热榜|social|趋势|抖音|douyin|微博|weibo"
  context_signals:
    keywords: ["热点", "trending", "热搜", "热榜", "趋势"]
  confidence_threshold: 0.6
priority: 6
requires_tools: [bash]
max_tokens: 200
cooldown: 60
output:
  format: markdown
  artifacts: true
  artifact_type: document
---

# social-trends

社交媒体热点趋势分析。

## 调用

```bash
python3 skills/social-trends/run.py '{"platform":"douyin", "limit":20}'
```

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| platform | string | 否 | 平台（douyin/weibo/all），默认 all |
| limit | int | 否 | 返回条数，默认 20 |
| query | string | 否 | 关键词过滤 |
