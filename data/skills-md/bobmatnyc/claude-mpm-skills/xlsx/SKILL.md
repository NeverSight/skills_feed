---
name: xlsx
description: Working with Excel files programmatically.
updated_at: 2025-10-30T17:00:00Z
tags: [excel, xlsx, spreadsheet, data]
progressive_disclosure:
  entry_point:
    summary: "Working with Excel files programmatically."
    when_to_use: "When working with xlsx or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Excel/XLSX Manipulation

Working with Excel files programmatically.

## Python (openpyxl)

### Reading Excel
```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active  # Get active sheet

# Read cell
value = ws['A1'].value

# Iterate rows
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
```

### Writing Excel
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Data"

# Write data
ws['A1'] = 'Name'
ws['B1'] = 'Age'
ws.append(['John', 30])
ws.append(['Jane', 25])

wb.save('output.xlsx')
```

### Formatting
```python
from openpyxl.styles import Font, PatternFill

# Bold header
ws['A1'].font = Font(bold=True)

# Background color
ws['A1'].fill = PatternFill(start_color="FFFF00", fill_type="solid")

# Number format
ws['B2'].number_format = '0.00'  # Two decimals
```

### Formulas
```python
# Add formula
ws['C2'] = '=A2+B2'

# Sum column
ws['D10'] = '=SUM(D2:D9)'
```

## Python (pandas)

### Reading Excel
```python
import pandas as pd

# Read sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Read multiple sheets
dfs = pd.read_excel('data.xlsx', sheet_name=None)
```

### Writing Excel
```python
# Write DataFrame
df.to_excel('output.xlsx', index=False)

# Multiple sheets
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet1')
    df2.to_excel(writer, sheet_name='Sheet2')
```

### Data Transformation
```python
# Filter
filtered = df[df['Age'] > 25]

# Group by
grouped = df.groupby('Department')['Salary'].mean()

# Pivot
pivot = df.pivot_table(values='Sales', index='Region', columns='Product')
```

## JavaScript (xlsx)

```javascript
import XLSX from 'xlsx';

// Read file
const workbook = XLSX.readFile('data.xlsx');
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];

// Convert to JSON
const data = XLSX.utils.sheet_to_json(worksheet);

// Write file
const newWorksheet = XLSX.utils.json_to_sheet(data);
const newWorkbook = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(newWorkbook, newWorksheet, 'Data');
XLSX.writeFile(newWorkbook, 'output.xlsx');
```

## Common Operations

### CSV to Excel
```python
import pandas as pd

df = pd.read_csv('data.csv')
df.to_excel('data.xlsx', index=False)
```

### Excel to CSV
```python
df = pd.read_excel('data.xlsx')
df.to_csv('data.csv', index=False)
```

### Merging Excel Files
```python
dfs = []
for file in ['file1.xlsx', 'file2.xlsx', 'file3.xlsx']:
    df = pd.read_excel(file)
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
combined.to_excel('merged.xlsx', index=False)
```

## Remember
- Close workbooks after use
- Handle large files in chunks
- Validate data before writing
- Use pandas for data analysis, openpyxl for formatting
