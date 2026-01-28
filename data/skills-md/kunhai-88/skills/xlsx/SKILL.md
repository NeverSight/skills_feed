---
name: xlsx
description: "表格的创建、编辑与分析，支持公式、格式、数据分析与图表。当需要创建/读写 .xlsx、保留公式、做分析或可视化时使用。"
license: MIT
---

# XLSX 创建、编辑与分析

## 概述

支持 .xlsx、.xlsm、.csv、.tsv 等。按任务选择 pandas、openpyxl 等工具。**公式重算**可假定已安装 LibreOffice，配合 `recalc.py` 使用。

## 通用要求

### 所有 Excel 文件
- **零公式错误**：不得出现 #REF!、#DIV/0!、#VALUE!、#N/A、#NAME?  
- **更新模板时**：严格保持原有格式、样式与约定，不擅自统一化。

### 财务模型（无特别说明时）
- **颜色**：蓝=手工输入/可调假设，黑=公式，绿=本工作簿链接，红=外部链接，黄底=关键假设或待更新格。  
- **数字格式**：年份用文本如 "2024"；货币用 $#,##0，单位在表头注明；零显示为 "-"；百分比默认 0.0%；倍数 0.0x；负数用括号。  
- **公式**：假设集中放专用单元格，公式中引用单元格而非硬编码；校验引用、区间与循环引用。  
- **硬编码注明来源**：如 "Source: 10-K FY2024 P45, [URL]"。

## 读写与分析

### pandas
```python
import pandas as pd
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)
df.to_excel('output.xlsx', index=False)
```

## 关键：用公式而非硬编码

**错误**：在 Python 中算好再写死到单元格。  
**正确**：在表格中写 Excel 公式（如 `=SUM(B2:B9)`、`=B5*(1+$B$6)`），保持可更新性。

## 何时使用

- 新建带公式与格式的表格  
- 读取、分析、汇总数据  
- 修改已有表格并保留公式  
- 表格内分析与图表  
- 公式重算（配合 LibreOffice / recalc）
