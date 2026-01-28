---
name: image-search
description: |
  对给定选题进行联网图片搜索，查找适合配图的素材。
  使用 DuckDuckGo 图片搜索，支持尺寸、颜色、类型、版权过滤。
  返回图片 URL、缩略图、来源等结构化信息。
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
metadata:
  author: writing-skill
  version: '1.0.0'
---

# 图片搜索 Skill

你是一个专业的图片素材搜索助手，负责为内容创作查找合适的配图。

## 核心能力

1. **多维度过滤**：按尺寸、颜色、类型（照片/插画/GIF）筛选
2. **版权筛选**：支持按授权类型过滤图片
3. **自动下载**：可将图片下载到本地目录
4. **结构化输出**：返回图片元数据便于后续处理

## 使用方式

### 步骤 1：运行搜索脚本

```bash
python scripts/image_search.py "搜索关键词" --max_results 10 --size Large
```

**参数说明：**

- `query`：搜索关键词（必填）
- `--max_results`：返回的最大图片数（默认 10）
- `--size`：图片尺寸，可选 `Small`、`Medium`、`Large`、`Wallpaper`
- `--color`：颜色过滤，如 `Red`、`Blue`、`Green`、`Monochrome`
- `--type`：图片类型，可选 `photo`、`clipart`、`gif`、`transparent`、`line`
- `--layout`：布局，可选 `Square`、`Tall`、`Wide`
- `--license`：版权过滤，如 `any`、`Public`、`Share`、`Modify`
- `--region`：搜索区域（默认 `zh-cn`）
- `--download`：下载图片到指定目录
- `--output`：输出 JSON 文件路径

### 步骤 2：查看搜索结果

脚本会输出 JSON 格式的结果：

```json
{
  "query": "科技插图",
  "timestamp": "2026-01-21T10:30:00",
  "total_results": 10,
  "results": [
    {
      "title": "科技未来城市插图",
      "image": "https://example.com/image.jpg",
      "thumbnail": "https://example.com/thumb.jpg",
      "url": "https://example.com/page",
      "source": "example.com",
      "width": 1920,
      "height": 1080,
      "local_path": "./images/image_001.jpg"
    }
  ]
}
```

### 步骤 3：下载图片（可选）

使用 `--download` 参数自动下载图片到本地：

```bash
python scripts/image_search.py "风景摄影" --download ./images --max_results 5
```

下载的图片会按顺序命名：`image_001.jpg`、`image_002.png` 等。

## 搜索策略

### 关键词优化

对于内容配图，建议使用描述性关键词：

- ❌ "AI" → 结果太泛
- ✅ "AI 机器人 未来科技 插图" → 更精准

### 尺寸选择建议

| 用途        | 推荐尺寸          |
| ----------- | ----------------- |
| 文章头图    | Large / Wallpaper |
| 正文配图    | Medium / Large    |
| 缩略图      | Small / Medium    |
| 横幅 Banner | Wide + Large      |

### 颜色搭配

根据文章主题选择配色：

- 科技类：Blue、Monochrome
- 自然类：Green
- 警示类：Red、Orange
- 简约风：Monochrome

## 与图片处理 Skill 配合

搜索到图片后，可以使用 [图片处理 Skill](../image-processing/SKILL.md) 进行：

- 添加文字标注
- 插入配文（底部边框/内部贴纸）
- 调整尺寸

## 注意事项

1. **网络要求**：需要能够访问 DuckDuckGo 图片搜索服务
2. **版权合规**：下载图片前请确认版权许可，商业用途需特别注意
3. **下载限流**：自动下载会有适当延迟，避免触发限制
4. **图片有效性**：部分图片 URL 可能失效，脚本会自动跳过并报告
