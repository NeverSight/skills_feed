---
name: skillsmp-searcher
description: SkillsMP技能商城搜索工具。用于在 https://skillsmp.com/ 网站上搜索和发现技能。支持关键词搜索和AI语义搜索两种模式。当用户需要：(1) 搜索特定主题的技能（如"SEO"、"视频制作"），(2) 通过自然语言描述查找相关技能（如"如何创建网络爬虫"），(3) 探索SkillsMP商城中的可用技能时使用此技能。
---

# SkillsMP 技能搜索

此技能提供对 SkillsMP 技能商城的搜索功能，帮助用户快速发现和定位所需的技能。

## API 配置

首次使用前，需要配置 API Key。API Key 存储在 `references/api_key.txt` 中。

格式：纯文本的 API Key 字符串（例如：`sk_live_skillsmp_eb_6A4Y9LJAhtzPFsmX0v67zhingVC0CrQZ4Qqlin4`）

**注意**：请确保 API Key 安全，不要将 SKILL.md 或包含 API Key 的文件提交到公共仓库。

## 搜索模式

### 1. 关键词搜索

使用 `scripts/search_skills.py` 进行基于关键词的搜索。

**适用场景**：
- 用户使用明确的关键词搜索（如 "SEO"、"PDF"、"翻译"）
- 需要按热门度或最新时间排序
- 需要分页浏览结果

**参数**：
- `q` (必需): 搜索关键词
- `page`: 页码，默认 1
- `limit`: 每页数量，默认 20，最大 100
- `sortBy`: 排序方式，`stars`（热门，默认）或 `recent`（最新）

**示例**：
```bash
python scripts/search_skills.py "SEO" --page 1 --limit 10 --sortBy stars
```

### 2. AI 语义搜索

使用 `scripts/ai_search.py` 进行基于语义理解的搜索。

**适用场景**：
- 用户使用自然语言描述需求（如"如何制作视频"、"帮我处理PDF文档"）
- 搜索意图复杂，需要理解上下文
- 不确定具体关键词，希望AI智能匹配

**参数**：
- `q` (必需): 自然语言搜索查询

**示例**：
```bash
python scripts/ai_search.py "How to create a web scraper"
```

## API 端点

详细的 API 文档请参考 `references/api_documentation.md`。

**基础 URL**: `https://skillsmp.com/api/v1`

| 端点 | 方法 | 功能 |
|------|------|------|
| `/skills/search` | GET | 关键词搜索 |
| `/skills/ai-search` | GET | AI 语义搜索 |

## 错误处理

API 错误码：

| 错误码 | HTTP状态 | 说明 |
|--------|----------|------|
| `MISSING_API_KEY` | 401 | 未提供 API Key |
| `INVALID_API_KEY` | 401 | API Key 无效 |
| `MISSING_QUERY` | 400 | 缺少必需的查询参数 |
| `INTERNAL_ERROR` | 500 | 服务器内部错误 |

错误响应格式：
```json
{
  "success": false,
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid"
  }
}
```

## 使用流程

1. 确保 API Key 已配置在 `references/api_key.txt`
2. 根据用户需求选择搜索模式：
   - 明确关键词 → 关键词搜索
   - 自然语言描述 → AI 语义搜索
3. 运行相应的脚本获取结果
4. 解析并展示搜索结果给用户
