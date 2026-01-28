---
name: pw-aippt-old
description: 基于 PPT 模板生成新内容。PDF 自动转图片 → 分析模板风格 → 拆分文章内容 → 生成提示词 → AI 生图 → 打包 PPTX。
---

# AIPPT - AI PPT 生成工作流

> **定位**: 完全自动化 PPT 生成工作流
> **依赖**: pw-image-generation skill
> **核心**: 垫图约束风格 + 提示词替换内容 + AI 生图 + 打包 PPTX

## 快速开始

### 1. 准备项目

```bash
mkdir my-ppt-project && cd my-ppt-project
mkdir -p template prompts images
```

### 2. 准备模板（垫图）

**方法 1: PDF 自动转换（推荐）**

```bash
node ~/.claude/skills/pw-aippt/scripts/pdf-to-images.js template.pdf ./template 150
```

需要安装 poppler: `brew install poppler`

**方法 2: PowerPoint/Keynote 导出**

导出为 PNG 图片，保存到 `template/` 目录。详见 `references/01_导出方法.md`

### 3. 生成提示词

```bash
# 在 Claude Code 中执行
/pw-aippt https://example.com/article
# 或
/pw-aippt "文章内容..."
```

skill 会自动分析模板、拆解内容、生成提示词文件到 `prompts/` 目录。

### 4. 生成图片

```bash
node ~/.claude/skills/pw-image-generation/scripts/generate-image.js
```

### 5. 打包 PPTX

```bash
node ~/.claude/skills/pw-image-generation/scripts/merge-to-pptx.js ./images output.pptx
```

---

## 核心概念

### 工作流程

```
导出图片 → 风格提取 → 分析模板 → 内容分段 → 内容映射 → 生成提示词 → 生成图片 → 打包PPTX
    ↓          ↓          ↓          ↓          ↓            ↓           ↓          ↓
  垫图    风格定义    布局库      页面规划    提示词文件    prompts/    PNG文件    .pptx
```

**新增步骤说明**:
- **风格提取**: 按照标准化规范提取模板的设计美学、背景系统、字体系统、颜色系统、视觉元素和风格约束，形成可复用的风格定义文档

### 提示词结构

```markdown
## 提示词

```
参考这张 PPT 模板图片: {垫图URL}

生成新的内容页。

【风格约束】(严格遵守)
## 设计美学
{从模板分析中提取的设计美学描述}

## 背景系统
- 颜色: {精确 Hex 值}
- 纹理: {纹理描述}
- 渐变: {渐变信息}

## 字体系统
### 标题字体
- 字体: {字体名称}
- 粗细: {粗细}
- 大小: {大小}
- 颜色: {Hex 值}

### 正文字体
- 字体: {字体名称}
- 粗细: {粗细}
- 大小: {大小}
- 颜色: {Hex 值}

## 颜色系统
{从模板分析中提取的颜色表格}

## 视觉元素
{装饰元素列表}

## 风格规则
### 应该保持
- {保持的特征列表}

### 禁止改变
- 不添加幻灯片编号、页脚或 Logo (除非模板原有)
- {其他禁止项}

【不可改区域】(严格保持原样)
- {具体的不可改元素}

【可改区域】
- 页面标题改为: {新标题}
- 内容区改为: {新内容}

【生成指令】
保持专业风格，内容清晰易读。
absolutely no watermark, clean output only
```
```

详细示例见 `references/05_提示词模板示例.md`

**风格库使用**:
- 可以从 `references/styles/` 目录选择预定义的风格模板
- 支持的风格: corporate (商务), minimal (简约), technical (技术), creative (创意)
- 复制风格定义到提示词的【风格约束】部分，根据实际模板微调

---

## 核心原则

### 视觉一致性（重要）

系列图最常见的问题是风格不一致。必须保持一致的要素：

1. **视觉风格**: 配色、装饰、字体、背景与模板一致
2. **布局比例**: 保持相似的留白比例和元素位置
3. **装饰元素**: 使用相同类型的装饰
4. **LOGO/页码**: 所有图片都要包含（如果模板有）

**实现方法**:
- 使用垫图约束风格（图生图）
- 提示词中明确不可改区域
- 后续图片明确要求"保持与模板相同的风格"

**常见问题**:
1. 背景颜色改变 → 在"不可改区域"中明确约束背景
2. 装饰元素消失 → 详细列出每个装饰元素的位置和样式
3. 字体大小不一致 → 在所有提示词中统一字体大小规范

### 内容拆解

- **封面页**: 主标题 + 副标题，强烈视觉冲击力
- **目录页**: 章节列表，清晰的导航
- **内容页**: 每页聚焦 1 个核心观点
- **结束页**: 总结/感谢/联系方式

**页面数量**:
- 简单内容（<1500字）: 10-15 页
- 中等复杂度（1500-3000字）: 15-20 页
- 深度内容（>3000字）: 25-30 页

**文件命名**: 使用序号前缀，如 `01_封面页.md`, `02_目录页.md`

---

## 参考文档

| 文件 | 说明 |
|------|------|
| `references/01_导出方法.md` | PPT 导出为图片（垫图） |
| `references/02_PPT模板分析方法.md` | 分析模板，输出布局库和风格定义 |
| `references/03_内容分段方法.md` | 内容拆分为页面 |
| `references/04_内容映射方法.md` | 内容匹配布局，生成提示词 |
| `references/05_提示词模板示例.md` | 提示词格式示例（推荐） |
| `references/styles/README.md` | 风格库使用说明 |
| `references/styles/corporate.md` | 商务风格模板 |
| `references/styles/minimal.md` | 简约风格模板 |
| `references/styles/technical.md` | 技术风格模板 |
| `references/styles/creative.md` | 创意风格模板 |

---

## 注意事项

1. **垫图质量**: 导出的模板图片分辨率要高（建议 1920x1080 或更高）
2. **提示词准确性**: 明确描述可改/不可改区域，避免 AI 随意修改
3. **视觉一致性**: 使用垫图约束风格，确保所有页面风格一致
4. **第一张图很重要**: 生成第一张图后，仔细对比模板，确认无误后再批量生成
5. **避免 Markdown 格式**: 提示词中不要使用 `**加粗**` 等格式标记
