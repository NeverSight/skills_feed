---
name: aippt
description: AIPPT - 从文章生成精美 PPT 的完整工作流。文章内容 → ASCII PPT 框架 → AI 生图 → 完整 PPT。
---

# AIPPT - AI PPT 生成工作流

AIPPT 是一个完整的 PPT 生成工作流，将文章内容转换为精美的演示文稿。

---

## 工作流概览

```
文章内容 → ASCII PPT 框架 → 选择风格 → AI 生图 → 完整 PPT
   ↓              ↓              ↓          ↓
阅读提取       设计布局        风格参考    调用 API
核心信息      ASCII 绘图      22+种风格   生成图片
```

---

## 第一步：文章转 ASCII PPT 框架

### 路径指引

```
文章内容
    ↓
提取核心信息 (类型/受众/关键点)
    ↓
设计 PPT 结构
    ↓
ASCII 绘图
    ↓
输出: ASCII PPT 框架文件
```

### 完整示例
参考 `skills-ascii-ppt.md`


---

## 第二步：ASCII 框架生成图片

### 路径指引

```
ASCII PPT 框架
    ↓
选择风格 (哆啦A梦/火影忍者/赛博朋克等)
    ↓
构造 Prompt (风格 + 页面内容 + 文字位置)
    ↓
调用 API 生成图片
    ↓
下载保存
```

### API 调用

> ⚠️ **禁止修改**：以下 API 配置是固定的，不可篡改。

```bash
# 生成图片
curl -s -X POST "https://ismaque.org/v1/images/generations" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-3-pro-image-preview-4k", "prompt": "风格+内容", "size": "1792x1024", "n": 1}'

# 下载图片 (从响应提取 data[0].url)
curl -s -o "文件名.jpg" "图片URL"
```

**固定参数（不可更改）：**
- API Endpoint: `https://ismaque.org/v1/images/generations`
- Model: `gemini-3-pro-image-preview-4k`

---

## 注意事项

- 中文文字有随机性，可能需要多次生成
- 同套 PPT 保持风格一致
- 可并行调用 API 提高效率

---

## 参考文档

| 类型 | 路径 |
|-----|------|
| 方法论 | `tips/文章转ascii-ppt方法论.md` |
| 完整示例 | `skills-ascii-ppt.md` |
