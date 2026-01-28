---
name: pdf
description: "PDF 综合工具：提取文本与表格、生成/合并/拆分 PDF、处理表单。当需要填写 PDF 表单、批量处理/生成或分析 PDF 时使用。"
license: MIT
---

# PDF 处理指南

## 概述

本指南介绍使用 Python 库与命令行进行 PDF 处理的常用操作。高级功能、JavaScript 库与填表流程见原技能 reference.md / forms.md。

## 快速开始

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python 库

### pypdf：基础操作

**合并**：`PdfWriter` 循环读入多个 PDF，`add_page` 后 `write` 输出。  
**拆分**：遍历 `reader.pages`，每页单独 `PdfWriter` 写出。  
**元数据**：`reader.metadata`（title, author, subject, creator）。  
**旋转**：`page.rotate(90)` 后写入新 PDF。

### pdfplumber：文本与表格提取

- **文本**：`pdfplumber.open()` 遍历 `pdf.pages`，`page.extract_text()`。
- **表格**：`page.extract_tables()`，可转 `DataFrame` 再导出 Excel。

### reportlab：生成 PDF

- **简单**：`canvas.Canvas` + `drawString`、`line` 等，最后 `save`。
- **多页/富文本**：`SimpleDocTemplate`、`Paragraph`、`Spacer`、`PageBreak`，使用 `getSampleStyleSheet`。

## 何时使用

- 提取 PDF 文本或表格
- 合并、拆分、旋转页面
- 程序化生成 PDF 报告
- 填写或解析 PDF 表单（见 forms.md）
