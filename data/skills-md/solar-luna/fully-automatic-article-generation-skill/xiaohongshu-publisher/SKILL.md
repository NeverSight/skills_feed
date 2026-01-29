---
name: xiaohongshu-publisher
description: 自动发布内容到小红书平台。支持将文章转换为小红书格式（≤1000字，emoji风格）并通过API直接发布。当用户说"发布到小红书"、"推送到小红书"、"小红书发布"时使用此Skill。
allowed-tools: Bash, Read, Write, Skill
---

# 小红书自动发布 Skill

自动将内容发布到小红书平台。

## 功能

- **格式转换**: 将文章内容转换为小红书格式（≤1000字，emoji风格）
- **智能压缩**: 将长文章压缩到1000字以内，提取核心要点
- **直接发布**: 通过xiaohongshu-mcp服务直接发布到小红书账号

## 使用场景

当用户说以下类似话术时使用此Skill：
- "发布到小红书"
- "推送到小红书"
- "小红书发布"
- "同步到小红书"
- "发一篇小红书"

## 使用方法

### 方法1：简化脚本发布（推荐，快速）

```bash
cd ~/.claude/skills/xiaohongshu-publisher
python3 simple_publish.py "标题" "内容内容"
```

**示例**：
```bash
python3 simple_publish.py \
  "Gemini 3 Pro炸场了" \
  "🔥 Gemini 3 Pro炸场了！核心亮点：🏆推理能力第一..."
```

### 方法2：完整功能发布

```bash
cd ~/.claude/skills/xiaohongshu-publisher
python3 publisher.py \
  --title "文章标题" \
  --content "文章内容或文件路径" \
  --cover "封面图路径"
```

### 方法3：直接REST API调用

```bash
curl -s -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "标题",
    "content": "内容",
    "images": ["/app/images/cover.png"],
    "tags": ["AI", "科技"]
  }'
```

## 前置要求

1. **xiaohongshu-mcp 服务运行中**
   ```bash
   docker ps | grep xiaohongshu-mcp
   ```

2. **已登录小红书账号**
   - Cookies 已配置到 `~/xiaohongshu-mcp/docker/data/cookies.json`

## 限制

- 标题: 最多20字
- 正文: 最多1000字（含emoji）
- 图片: 最多9张

## API端点

- **发布接口**: `http://localhost:18060/api/v1/publish`
- **方法**: POST
- **Content-Type**: application/json
