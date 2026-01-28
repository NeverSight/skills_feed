---
name: pptx
description: "演示文稿的创建、编辑与分析。当需要创建/修改 .pptx、调整版式、添加批注或演讲者备注等任务时使用。"
license: MIT
---

# PPTX 创建、编辑与分析

## 概述

.pptx 为 ZIP，内含 XML 等资源。按任务选择对应工作流。

## 阅读与分析

### 文本提取
```bash
python -m markitdown path-to-file.pptx
```

### 原始 XML
批注、演讲者备注、版式、动画、主题等需解包后访问 XML。  
解包：`python ooxml/scripts/unpack.py <office_file> <output_dir>`  
关键路径：`ppt/presentation.xml`、`ppt/slides/slide{N}.xml`、`ppt/notesSlides/`、`ppt/comments/`、`ppt/slideLayouts/`、`ppt/theme/`、`ppt/media/`。  
**仿制设计时**：先分析 `ppt/theme/theme1.xml` 的配色与字体，再查看 `ppt/slides` 中的实际用法。

## 新建演示文稿（无模板）

使用 **html2pptx** 流程：HTML 幻灯片 → 精确定位的 .pptx。

### 设计原则
- 根据内容与品牌选择配色、字体；事先说明设计思路再写代码。  
- 仅用 web 安全字体（Arial、Helvetica、Times New Roman、Georgia 等）。  
- 通过字号、字重、颜色建立层级；保证可读性与一致性。

### 配色
结合主题、行业、情绪、受众选择 3～5 色，保证对比度。可参考原技能中的多组示例调色板（经典蓝、青绿与珊瑚、深紫与祖母绿等），或自建。

### 版式
- **首选**：全宽标题 + 双栏（如 40%/60%），一栏文字/要点，一栏图表。  
- 或整页图表。  
- **避免**：单栏内图表压文字下方。

### 流程
1. 阅读 html2pptx 相关文档。  
2. 用 HTML/CSS 搭建幻灯片，再转换为 .pptx。

## 编辑已有 .pptx

解包 → 按 ooxml 规范编辑 `ppt/slides/*.xml` 等 → 打包。批注、备注、版式、媒体路径见上述关键结构。

## 依赖与脚本

markitdown、ooxml 脚本（unpack/pack）。脚本路径以原技能仓库为准，必要时 `find . -name "unpack.py"` 定位。
