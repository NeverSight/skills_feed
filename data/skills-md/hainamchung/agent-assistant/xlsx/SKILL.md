---
name: xlsx
description: Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for creating new spreadsheets, reading/analyzing data, modifying existing spreadsheets, or recalculating formulas.
source: anthropics/skills
license: Apache-2.0
---

# Excel/Spreadsheet Processing

## Reading and Analyzing Data

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Creating Excel Files with openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula - ALWAYS use formulas, not hardcoded values
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

## Editing Existing Files

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb.active

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)
sheet.delete_cols(3)

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## Critical: Use Formulas, Not Hardcoded Values

```python
# BAD - Hardcoding calculated values
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# GOOD - Using Excel formulas
sheet['B10'] = '=SUM(B2:B9)'
sheet['C5'] = '=(C4-C2)/C2'  # Growth rate
sheet['D20'] = '=AVERAGE(D2:D19)'
```

## Financial Model Standards

- **Blue text**: Hardcoded inputs
- **Black text**: ALL formulas
- **Green text**: Links from other worksheets
- **Yellow background**: Key assumptions

## Best Practices

- Use `data_only=True` to read calculated values
- For large files: Use `read_only=True` or `write_only=True`
- Formulas are preserved but not evaluated by openpyxl
