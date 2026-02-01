---
name: excel-export-validator
description: "Validates Customer Feedback Analyzer Excel exports with 7 view sheets, 36 columns, and professional formatting. Use when checking Excel files, verifying export quality, debugging Excel generation issues, before releasing new versions, or when modifying Excel export code. Ensures zero errors in customer-facing deliverables."
---

# Excel Export Validator - Customer Feedback Analyzer

## Critical Requirements

### Zero Errors Mandate
Every Excel export MUST be delivered with:
- ZERO formula errors (even though v3.9.0 uses static values)
- ZERO missing sheets
- ZERO column schema violations
- ZERO formatting errors

**This is customer-facing output - quality is non-negotiable.**

---

## Project-Specific Validation Rules

### 1. Sheet Structure (7 View Sheets + Calculated Data)

**Required Sheets (in order)**:

#### View Sheets (Task-Focused, Always First)
1. Management Dashboard View (RED tab)
   - Filter: Priority >= 60 OR Churn >= 40
   - Purpose: Executive priority review
   - Columns: 19 columns

2. Churn Risk Analysis View (ORANGE tab)
   - Filter: Churn >= 40 OR Exit Threat
   - Purpose: Customer retention focus
   - Columns: 11 columns

3. Pain Point Analysis View (YELLOW tab)
   - Filter: Has pain point
   - Purpose: Product improvement insights
   - Columns: 8 columns

4. Sentiment Analysis View (BLUE tab)
   - Filter: No filter (all data)
   - Purpose: Sentiment trends
   - Columns: 10 columns

5. Quality Control View (PURPLE tab)
   - Filter: Needs review OR quality issues
   - Purpose: QA validation
   - Columns: 14 columns

6. Duplicate Analysis View (GRAY tab)
   - Filter: Is duplicate
   - Purpose: Data cleanliness
   - Columns: 7 columns

#### Complete Data (End of Workbook)
7. Calculated Data (position 90, NO color/WHITE tab)
   - Filter: None (complete dataset)
   - Purpose: Power users, complete analysis
   - Columns: EXACTLY 36 columns

**Validation Command**:
```python
# Check sheet count and names
expected_sheets = [
    "Management Dashboard View",
    "Churn Risk Analysis View",
    "Pain Point Analysis View",
    "Sentiment Analysis View",
    "Quality Control View",
    "Duplicate Analysis View",
    "Calculated Data"
]

wb = load_workbook('export.xlsx')
actual_sheets = wb.sheetnames

assert len(actual_sheets) >= 7, f"Expected >= 7 sheets, got {len(actual_sheets)}"
for sheet in expected_sheets:
    assert sheet in actual_sheets, f"Missing sheet: {sheet}"
```

---

### 2. Column Schema (36 Columns in Calculated Data)

**GROUP 1: Primary Review Columns (10 columns)**
1. User Score (0-10 rating)
2. Customer Comment (text feedback)
3. AI Sentiment (Spanish NLP) (0-10 score)
4. Analysis Score (smart score selection)
5. Score Source (User/GPT-4o/AI Sentiment)
6. Sentiment Category (Promoter/Passive/Detractor)
7. Emotion (joy, frustration, anger, etc.)
8. Churn Risk (retention risk level)
9. Review Priority Score (0-100 urgency metric)
10. Pain Point Category (Primary)

**GROUP 2: Secondary Analysis Columns (7 columns)**
11. Pain Point Category (Secondary)
12. Pain Point Keywords (matched Spanish keywords)
13. Sentiment Score Alignment (0-1 match score)
14. Actionability Score (0-10 specificity)
15. Word Count (comment length)
16. Has Deep Insights (boolean flag)
17. Deep Insights JSON (structured analysis)

**GROUP 3: Duplicate Detection (5 columns)**
18. Is Duplicate (boolean)
19. Duplicate Count (times appeared)
20. Duplicate Group ID (group identifier)
21. First Occurrence ID (original row reference)
22. Is First Occurrence (boolean flag)

**GROUP 4: Quality Control (3 columns)**
23. Quality Flags (VERY_SHORT, GENERIC, etc.)
24. Analysis Tier (FULL_AI/BASIC_AI/FREE)
25. Problemas Detectados (Spanish translation)

**GROUP 5: AI Correction Details (4 columns)**
26. Original User Score (pre-adjustment)
27. Sentiment Score (Before Discrepancy Check)
28. Discrepancy Flag (large difference indicator)
29. Discrepancy Explanation (why correction made)

**GROUP 6: Technical Scores (7 columns)**
30. Sentiment Score (GPT-4o-mini) (-1 to 1 scale)
31. Confidence Score (analysis confidence)
32-36. [Additional technical metrics]

**Validation Command**:
```python
# Verify column count in Calculated Data
ws = wb["Calculated Data"]
column_count = ws.max_column

assert column_count == 36, f"Expected 36 columns, got {column_count}"
```

---

### 3. Tab Colors (Professional Color Scheme)

**Required Tab Colors** (openpyxl RGB format):

```python
from openpyxl.worksheet.properties import TabColor

# View sheets (priority-based colors)
wb["Management Dashboard View"].sheet_properties.tabColor = TabColor("FF0000")  # RED
wb["Churn Risk Analysis View"].sheet_properties.tabColor = TabColor("FFA500")   # ORANGE
wb["Pain Point Analysis View"].sheet_properties.tabColor = TabColor("FFFF00")   # YELLOW
wb["Sentiment Analysis View"].sheet_properties.tabColor = TabColor("0000FF")    # BLUE
wb["Quality Control View"].sheet_properties.tabColor = TabColor("800080")       # PURPLE
wb["Duplicate Analysis View"].sheet_properties.tabColor = TabColor("808080")    # GRAY

# Calculated Data: No color (default white/none)
# Do NOT set tab color for Calculated Data
```

**Color Meanings**:
- RED: Urgent priority (Management Dashboard)
- ORANGE: Customer retention risk (Churn Risk)
- YELLOW: Product improvement needs (Pain Points)
- BLUE: Sentiment trends (analysis)
- PURPLE: Quality assurance (QA validation)
- GRAY: Data cleanliness (duplicates)

**Validation Command**:
```python
# Check tab colors
expected_colors = {
    "Management Dashboard View": "FF0000",
    "Churn Risk Analysis View": "FFA500",
    "Pain Point Analysis View": "FFFF00",
    "Sentiment Analysis View": "0000FF",
    "Quality Control View": "800080",
    "Duplicate Analysis View": "808080"
}

for sheet_name, expected_color in expected_colors.items():
    sheet = wb[sheet_name]
    actual_color = sheet.sheet_properties.tabColor
    if actual_color:
        assert actual_color.rgb == expected_color, \
            f"{sheet_name}: Expected {expected_color}, got {actual_color.rgb}"
```

---

### 4. Conditional Formatting Rules

**Review Priority Score Conditional Formatting**:
```python
from openpyxl.formatting.rule import ColorScaleRule

# Apply to Review Priority Score column (column I in most views)
priority_col = 'I'  # Adjust based on actual column

# Red (80-100) -> Yellow (60-80) -> Green (40-60)
color_scale = ColorScaleRule(
    start_type='num', start_value=40, start_color='63BE7B',  # Green
    mid_type='num', mid_value=60, mid_color='FFEB84',        # Yellow
    end_type='num', end_value=80, end_color='F8696B'         # Red
)

ws.conditional_formatting.add(f'{priority_col}2:{priority_col}1000', color_scale)
```

**Churn Risk Conditional Formatting**:
```python
# Similar color coding for Churn Risk column
# High risk (red), medium (yellow), low (green)
```

**Sentiment Discrepancy Highlighting**:
```python
# Highlight large gaps between User Score and AI Sentiment
# Gap >= 5.0 points should be visually flagged
```

**Validation Command**:
```python
# Verify conditional formatting applied
ws = wb["Management Dashboard View"]
rules = ws.conditional_formatting._cf_rules

assert len(rules) > 0, "No conditional formatting found in Management Dashboard"
```

---

### 5. Data Integrity Checks

**No Missing Required Columns**:
```python
# All 36 columns present in Calculated Data
# All view sheets have required subset of columns
```

**No #REF!, #VALUE!, #NAME! Errors**:
```python
# Even though v3.9.0 uses static values, check for any errors
for sheet in wb.sheetnames:
    ws = wb[sheet]
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                assert not cell.value.startswith('#'), \
                    f"Error in {sheet}!{cell.coordinate}: {cell.value}"
```

**Data Type Validation**:
```python
# User Score: numeric (0-10)
# AI Sentiment: numeric (0-10)
# Review Priority Score: numeric (0-100)
# Churn Risk: numeric (0-100)
# Is Duplicate: boolean
# Customer Comment: string
```

---

## Quick Validation Commands

### 1. Run Excel Export Tests
```bash
# Full test suite
cd api
PYTHONPATH=".:$PYTHONPATH" ./venv/Scripts/python -m pytest api/tests/domain/export/excel/ -v

# Specific test for column generation
PYTHONPATH=".:$PYTHONPATH" ./venv/Scripts/python -m pytest api/tests/integration/test_column_generation.py -v
```

### 2. Integration Test (Full Export)
```python
# File: api/tests/integration/test_excel_export_integration.py
# Generates complete Excel file and validates all requirements

cd api/tests/integration
python test_excel_export_integration.py
```

### 3. Visual Inspection Checklist
```
Open Excel file manually and verify:

[ ] All 7 view sheets present (in correct order)
[ ] Tab colors correct (RED/ORANGE/YELLOW/BLUE/PURPLE/GRAY)
[ ] Calculated Data has 36 columns
[ ] Conditional formatting applied (see color gradients)
[ ] No #REF!, #VALUE!, #NAME! errors
[ ] No blank rows in view sheets
[ ] No missing data in key columns
[ ] Column headers match schema
[ ] Data types correct (numbers, text, booleans)
[ ] Sheet positions correct (views first, Calculated Data at end)
```

### 4. Data Flow Validation
```bash
# Verify AI analysis columns present
cd api
python scripts/validation/validate_data_flow.py

# Should confirm:
# - Sentiment Score (GPT-4o-mini) present
# - Churn Risk calculated
# - Emotion detected
# - Pain Point Category assigned
# - Deep Insights JSON generated
```

---

## Common Issues and Fixes

### Issue 1: Missing View Sheets
**Symptom**: Only Calculated Data sheet present
**Root Cause**: View sheet generation skipped in code
**Fix**: Verify `create_view_sheets()` called in export service
**File**: `api/app/domain/export/excel/service/export_service.py`

### Issue 2: Wrong Column Count
**Symptom**: Calculated Data has != 36 columns
**Root Cause**: Column schema mismatch or missing columns
**Fix**: Check `CALCULATED_DATA_COLUMNS` constant
**File**: `api/app/domain/export/excel/constants/column_schemas.py`

### Issue 3: Tab Colors Missing
**Symptom**: All tabs white/default color
**Root Cause**: TabColor not applied after sheet creation
**Fix**: Apply tab colors after creating sheets
**File**: `api/app/domain/export/excel/service/export_service.py`
**Code**:
```python
from openpyxl.worksheet.properties import TabColor
ws.sheet_properties.tabColor = TabColor("FF0000")  # RED
```

### Issue 4: Conditional Formatting Not Applied
**Symptom**: No color gradients in Review Priority Score
**Root Cause**: Conditional formatting rules not added
**Fix**: Add ColorScaleRule after data populated
**File**: `api/app/domain/export/excel/sheets/view_sheets.py`

### Issue 5: AI Columns Missing
**Symptom**: Sentiment, Churn Risk, Emotion columns empty
**Root Cause**: AI analysis commented out or not running
**Fix**: Verify AI analysis in `calculated_data_sheet.py:163-248` uncommented
**File**: `api/app/domain/export/excel/sheets/core/calculated_data_sheet.py`

---

## When to Use This Skill

**Always use when**:
1. Modifying Excel export code
2. Adding new columns to schema
3. Creating new view sheets
4. Changing conditional formatting
5. Debugging Excel generation issues
6. Before releasing new version
7. After refactoring export service
8. When tests fail for Excel module

**Especially important when**:
- Customer-facing deliverables
- Production deployments
- Demo preparation
- Client presentations
- Quality audits

---

## When NOT to Use This Skill

**Skip for**:
- CSV exports (different validator)
- Internal Excel files (dev use only)
- Test data generation (unless testing export)
- Non-customer-facing analysis

---

## Integration with Development Workflow

### Pre-commit Hook Integration
```bash
# Add to .git/hooks/pre-commit
if git diff --cached --name-only | grep -q "api/app/domain/export/excel/"; then
    echo "Excel export modified. Running validation..."
    cd api
    PYTHONPATH=".:$PYTHONPATH" ./venv/Scripts/python -m pytest api/tests/domain/export/excel/ -v
    if [ $? -ne 0 ]; then
        echo "Excel validation failed. Fix tests before committing."
        exit 1
    fi
fi
```

### CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Excel Export Validation
  run: |
    cd api
    PYTHONPATH=".:$PYTHONPATH" ./venv/Scripts/python -m pytest api/tests/domain/export/excel/ -v
    PYTHONPATH=".:$PYTHONPATH" ./venv/Scripts/python -m pytest api/tests/integration/test_column_generation.py -v
```

---

## Red Flags (Stop and Fix Immediately)

1. Any sheet missing from required 7
2. Wrong tab colors (customer will notice)
3. Column count != 36 in Calculated Data
4. Missing conditional formatting (usability issue)
5. Any #REF!, #VALUE!, #NAME! errors
6. Empty AI analysis columns (Sentiment, Churn, Emotion)
7. View sheets showing complete data (should be filtered subsets)
8. Calculated Data not at end of workbook
9. Integration test failures
10. Visual inspection checklist failures

---

## Performance Expectations

**Excel Generation Speed**:
- 1,000 rows: ~5 seconds
- 10,000 rows: ~30 seconds
- 50,000 rows: ~2 minutes

**If slower than expected**:
- Check for N+1 query patterns
- Verify batch operations used
- Review conditional formatting complexity
- Profile with Python cProfile

**Memory Usage**:
- 1,000 rows: ~50 MB
- 10,000 rows: ~200 MB
- 50,000 rows: ~800 MB

**If memory issues occur**:
- Use write-only mode in openpyxl
- Process data in chunks
- Clear unused dataframes

---

## Version History

**v3.9.0 (November 2025)**:
- Modern Excel Builder with 7 view sheets
- Professional tab colors (RED/ORANGE/YELLOW/BLUE/PURPLE/GRAY)
- Advanced conditional formatting
- 36-column calculated data
- Progressive disclosure pattern
- All static values (no formulas)

**v3.8.0**:
- Enhanced analytics (Review Priority Score, Pain Points)
- 36-column schema
- Duplicate detection improvements

**v3.7.0**:
- Formula removal (static values only)
- Google Sheets compatibility
- 15-20% faster, 30% less memory

---

## Testing Strategy

### Unit Tests (Fast)
```bash
# Sheet generation
pytest api/tests/domain/export/excel/test_guide_sheet.py -v
pytest api/tests/domain/export/excel/test_calculated_data_sheet.py -v

# View sheets
pytest api/tests/domain/export/excel/test_view_sheets.py -v

# Formatters
pytest api/tests/domain/export/excel/test_formatters.py -v
```

### Integration Tests (Slower)
```bash
# Complete export
pytest api/tests/integration/test_excel_export_integration.py -v

# Column generation (verifies AI analysis)
pytest api/tests/integration/test_column_generation.py -v
```

### Manual Testing (Visual)
```bash
# Generate real export
cd api
python scripts/export/generate_ftth_export.py \
  --input datasets/ftth/ftth_846_reviews.csv \
  --output results/ftth_export_$(date +%Y%m%d).xlsx

# Open in Excel and verify visually
# Use checklist above
```

---

## Success Criteria

An Excel export is considered **validated and ready** when:

1. All 7 view sheets present
2. Tab colors correct (RED/ORANGE/YELLOW/BLUE/PURPLE/GRAY)
3. Calculated Data has exactly 36 columns
4. Conditional formatting applied and visible
5. Zero formula errors (even though using static values)
6. All tests passing (unit + integration)
7. Visual inspection checklist complete
8. Performance within expected range
9. Memory usage acceptable
10. Customer-facing quality achieved

---

## Quick Reference

**File Locations**:
- Export Service: `api/app/domain/export/excel/service/export_service.py`
- Sheet Generators: `api/app/domain/export/excel/sheets/`
- View Sheets: `api/app/domain/export/excel/sheets/view_sheets.py`
- Calculated Data: `api/app/domain/export/excel/sheets/core/calculated_data_sheet.py`
- Tests: `api/tests/domain/export/excel/`
- Integration Tests: `api/tests/integration/`

**Key Constants**:
- Column schemas: `api/app/domain/export/excel/constants/column_schemas.py`
- Colors: `api/app/domain/export/excel/constants/colors.py`
- Thresholds: `api/app/config/analysis_thresholds.py`

**Critical Checks**:
1. Sheet count: 7 minimum
2. Column count: 36 in Calculated Data
3. Tab colors: 6 colored + 1 white
4. Conditional formatting: Applied
5. AI columns: Present and populated

---

**Remember**: This is customer-facing output. Quality is non-negotiable. Zero errors, professional formatting, complete validation.
