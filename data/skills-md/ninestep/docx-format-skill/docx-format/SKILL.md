---
name: docx-format
description: 使用 python-docx 精确读取、分析、修改 Word 文档（.docx）格式。当用户需要分析文档格式、批量修改格式、统一排版规范、处理中英文混排字体、修改交叉引用样式时使用此 skill。
---

# Word 文档格式处理

使用 python-docx 库精确操作 Word 文档格式，适用于格式分析、格式规范化、批量修改。

## 核心规则

**被调用时立即执行**：

1. **确认文件路径**：询问用户 Word 文档的完整路径
2. **明确需求**：确认是分析格式还是修改格式，目标规范是什么
3. **选择模板**：根据需求选择合适的代码模板或脚本
4. **生成脚本**：创建独立的 Python 脚本文件
5. **执行验证**：使用 `uv run` 执行并检查结果

**强制性约束**：

- ✓ **必须使用** `uv run --with python-docx python3 script.py`
- ✓ **必须处理** `doc.paragraphs` 和 `doc.tables`（文档正文常在表格内）
- ✓ **必须分设** 中英文字体（使用 `qn('w:eastAsia')`）
- ✓ **必须询问** 用户文件路径和输出路径
- ✗ **禁止使用** 直接 `python` 命令（缺少依赖）
- ✗ **禁止遗漏** 表格内容处理（常见错误）

## 何时使用

**触发场景**：
- 分析 Word 文档格式（字体/字号/缩进/行距）
- 批量修改文档格式
- 统一排版规范（学术论文、报告等）
- 处理中英文混排字体
- 修改交叉引用/参考文献样式

**触发关键词**：修改 Word 格式、统一字体、调整缩进、分析文档格式、参考文献格式

## 决策树

```
用户需求是什么？
├─ 不清楚当前格式 → 使用 scripts/analyze.py
├─ 应用公文标准 → 使用 scripts/format_official.py
├─ 应用学术标准 → 使用 scripts/format_academic.py
├─ 统一正文格式 → 使用【快速模板：批量格式化】
├─ 修改参考文献 → 使用【快速模板：参考文献处理】
└─ 自定义需求 → 基于【基础模板】组合
```

## 快速开始

### 基础模板

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

doc = Document('input.docx')

def set_font(run, cn='宋体', en='Times New Roman', size=10.5):
    """设置中英文字体"""
    run.font.name = en
    run._element.rPr.rFonts.set(qn('w:eastAsia'), cn)
    run.font.size = Pt(size)

def process_all_paragraphs(doc, process_func):
    """遍历所有段落（包括表格内）"""
    for para in doc.paragraphs:
        process_func(para)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    process_func(para)

# 使用示例
def format_para(para):
    para.paragraph_format.first_line_indent = Pt(21)
    for run in para.runs:
        set_font(run, cn='宋体', en='Times New Roman', size=10.5)

process_all_paragraphs(doc, format_para)
doc.save('output.docx')
```

### 快速模板：批量格式化

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

doc = Document('input.docx')

for para in doc.paragraphs:
    if len(para.text.strip()) > 30:
        para.paragraph_format.first_line_indent = Pt(21)
        para.paragraph_format.line_spacing = 1.5
        for run in para.runs:
            run.font.name = 'Times New Roman'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            run.font.size = Pt(10.5)

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                if len(para.text.strip()) > 30:
                    para.paragraph_format.first_line_indent = Pt(21)
                    for run in para.runs:
                        run.font.name = 'Times New Roman'
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
                        run.font.size = Pt(10.5)

doc.save('output.docx')
```

### 快速模板：参考文献处理

```python
from docx import Document
from docx.shared import Pt, RGBColor
import re

doc = Document('input.docx')
ref_pattern = re.compile(r'\[\d+\]')

for para in doc.paragraphs:
    if para.text.strip().startswith('[') and ']' in para.text[:5]:
        para.paragraph_format.first_line_indent = Pt(-21)
        para.paragraph_format.left_indent = Pt(21)

    for run in para.runs:
        if ref_pattern.search(run.text):
            run.font.color.rgb = RGBColor(0, 0, 255)

doc.save('output.docx')
```

## 执行检查清单

**生成脚本前**：
- [ ] 已确认用户提供的文件路径
- [ ] 已明确目标格式规范
- [ ] 已选择合适的模板或脚本

**脚本中必须包含**：
- [ ] 同时处理 `doc.paragraphs` 和 `doc.tables`
- [ ] 使用 `qn('w:eastAsia')` 设置中文字体
- [ ] 正确的输入/输出文件路径

**执行前提醒用户**：
- [ ] 备份原文件或使用不同的输出文件名
- [ ] 确认文件未被其他程序打开

**执行命令**：
```bash
uv run --with python-docx python3 script.py
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 修改未生效 | 遗漏表格内容 | 检查是否处理了 `doc.tables` |
| 中文字体不对 | 未用 `qn('w:eastAsia')` | 必须单独设置中文字体 |
| 文件打开失败 | 路径错误或文件被占用 | 检查路径，关闭 Word |
| 依赖缺失 | 未用 `uv run` | 使用完整命令 |

## 相关文档

- **STANDARDS.md** - 默认格式标准（公文/学术论文）和参数速查表
- **EXAMPLES.md** - 详细示例代码（多级标题、表格、图片、页眉页脚等）
- **scripts/** - 预置工具脚本（分析、公文格式化、学术格式化）

## Markdown 转 DOCX

直接读取 Markdown 文档并按格式要求写入 DOCX，无需 pandoc。

### 基础模板

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

doc = Document()

def add_heading(doc, text, level):
    """添加标题"""
    para = doc.add_paragraph(text)
    if level == 1:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.font.name = 'Arial'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
            run.font.size = Pt(15)
            run.font.bold = True
    elif level == 2:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in para.runs:
            run.font.name = 'Arial'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
            run.font.size = Pt(14)
            run.font.bold = True
    elif level == 3:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in para.runs:
            run.font.name = 'Arial'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
            run.font.size = Pt(12)
            run.font.bold = True

def add_paragraph(doc, text):
    """添加正文段落"""
    para = doc.add_paragraph(text)
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.paragraph_format.first_line_indent = Pt(24)
    para.paragraph_format.line_spacing = 1.5
    for run in para.runs:
        run.font.name = 'Times New Roman'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

# 读取 Markdown
with open('input.md', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        if not line:
            continue

        # 标题
        if line.startswith('# '):
            add_heading(doc, line[2:], 1)
        elif line.startswith('## '):
            add_heading(doc, line[3:], 2)
        elif line.startswith('### '):
            add_heading(doc, line[4:], 3)
        # 正文
        else:
            add_paragraph(doc, line)

doc.save('output.docx')
```

**使用预置脚本**：
```bash
uv run --with python-docx python3 .claude/skills/docx-format/scripts/md_to_docx.py input.md output.docx
```

## 注意事项

1. **只支持 .docx**：不支持旧版 .doc
2. **表格内容**：学术论文、报告等正文常在表格内，必须处理
3. **单位转换**：`font.size` 返回 EMU，需转换（÷ 914400 × 72）
4. **备份原文件**：修改前建议备份
5. **Markdown 转换**：使用 pandoc 转换后再格式化
