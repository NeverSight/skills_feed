---
name: docx
description: "Word 文档的创建、编辑与分析，支持修订、批注、格式保留与文本提取。当需要创建 .docx、修改内容、处理修订/批注或其它文档任务时使用。"
license: MIT
---

# DOCX 创建、编辑与分析

## 概述

.docx 本质为 ZIP，内含 XML 等资源。按任务类型选择不同工作流。

## 工作流选择

- **仅阅读/分析** → 文本提取或原始 XML 访问
- **新建文档** → 「创建新 Word 文档」流程
- **编辑已有文档**：
  - 自己的文档 + 简单修改 → 基础 OOXML 编辑
  - 他人文档 / 法律、学术、商业、政府文档 → **修订流程（Redlining）**（推荐或必须）

## 阅读与分析

### 文本提取
用 pandoc 转为 markdown，可保留修订：

```bash
pandoc --track-changes=all path-to-file.docx -o output.md
# 选项: --track-changes=accept/reject/all
```

### 原始 XML
批注、复杂格式、结构、媒体、元数据需解包后读 XML。  
解包：`python ooxml/scripts/unpack.py <office_file> <output_directory>`  
关键路径：`word/document.xml`、`word/comments.xml`、`word/media/`；修订用 `<w:ins>`、`<w:del>`。

## 创建新文档

使用 **docx-js**（JavaScript/TypeScript）。先完整阅读 docx-js.md，再以 Document / Paragraph / TextRun 构建，用 `Packer.toBuffer()` 导出 .docx。

## 编辑已有文档

使用 **Document 库**（Python，操作 OOXML）。流程：  
1. 完整阅读 ooxml.md  
2. 解包：`unpack.py <office_file> <output_directory>`  
3. 用 Document 库编写脚本编辑  
4. 打包：`pack.py <input_directory> <office_file>`

## 修订流程（Redlining）

1. **markdown 表示**：`pandoc --track-changes=all ... -o current.md`  
2. **识别并分批修改**：按章节/类型/难度分组，每批约 3～10 处。  
3. **解包、阅读 ooxml.md**，按建议 RSID 使用。  
4. **分批实现**：`grep` 定位 `word/document.xml`，用 `get_node` 等实现变更，`doc.save()`。  
5. **打包**：`pack.py` 生成 .docx。  
6. **验证**：再次 `pandoc --track-changes=all` 转 md，`grep` 核对修改是否完整、无多余变更。

**原则**：仅标记实际变更的文本；未改部分复用原 `<w:r>` 与 RSID。

## 转成图片

```bash
soffice --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
# -f / -l 可指定页范围
```

## 依赖

pandoc、docx（npm）、LibreOffice、poppler-utils、defusedxml（pip）。
