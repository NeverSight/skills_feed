---
name: unifuncs-deep-search
description: 使用 UniFuncs API 进行深度搜索，高速全面地搜索信息。当用户需要深度搜索、深搜、全面信息收集时使用。
argument-hint: [搜索问题]
allowed-tools: Bash(curl:*)
---

# UniFuncs 深度搜索 Skill

高速、准确、全面的深度搜索能力。

## 首次使用配置

1. 前往 https://unifuncs.com/account 获取 API Key
2. 设置环境变量：`export UNIFUNCS_API_KEY="sk-your-api-key"`

## 使用方法

执行深度搜索：
```bash
curl -X POST "https://api.unifuncs.com/deepsearch/v1/chat/completions" \
  -H "Authorization: Bearer $UNIFUNCS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "s2", "messages": [{"role": "user", "content": "$ARGUMENTS"}]}'
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| messages | 搜索问题 | 必填 |
| model | `s2` 或 `s1` | s2 |

## 更多信息

- 详细 API 文档见 [api.md](references/api.md)
