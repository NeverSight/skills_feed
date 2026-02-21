---
name: invoice-processor
description: Automatically process invoices (发票) from PDFs/images to Excel spreadsheets using AI vision recognition. Use this skill when users mention "发票", "invoice", "处理发票", "识别发票", "提取发票", or need to convert invoice files to Excel format. 
---

# Invoice Processor

Fully automated workflow for processing invoice files using AI vision models to extract structured information and generate formatted Excel reports.

## When to Use

**Auto-trigger when users mention:**
- "处理发票" / "识别发票" / "提取发票信息" / "发票转Excel"
- Processing invoice files (PDF, JPG, PNG)
- Converting invoices to Excel format

## Execution Environment Notes

**⚠️ CRITICAL: Path handling for non-ASCII directory names**

When the project directory contains Chinese or other non-ASCII characters (e.g., "发票助手agent"), you MUST use full relative paths from project root:

```bash
# ❌ WRONG - Will fail with encoding errors
python scripts/check_env.py

# ✅ CORRECT - Use full paths from .claude/skills/
python .claude/skills/invoice-processor/scripts/check_env.py
```

**Cross-platform compatibility:**
- Use Unix-style commands (Git Bash, Linux, macOS)
- ❌ `dir /b` → ✅ `ls`

## Setup

Create a `.env` file in the `invoice-processor` directory:

```bash
# Copy from template
cp .env.example .env

# Edit with your API key
# .env content:
GLM_API_KEY=your_actual_api_key_here
```

Get your API key from: https://open.bigmodel.cn/

## Workflow

### Step 1: Environment Check (Recommended)

```bash
python .claude/skills/invoice-processor/scripts/check_env.py
```

Verifies: GLM_API_KEY is set, required packages installed (aiohttp, PyMuPDF, openpyxl)

### Step 2: Recognize Invoices

```bash
# Default: process 'invoices' directory → 'invoice_results.json'
python .claude/skills/invoice-processor/scripts/invoice_ocr.py

# Custom paths
python .claude/skills/invoice-processor/scripts/invoice_ocr.py -i <input_path> -o <output.json>
```

**What it does:**
- Scans for invoice files (JPG, JPEG, PNG, PDF)
- Converts PDFs to images (200 DPI)
- Processes up to 5 files concurrently
- Extracts 9 fields: type, number, date, buyer/seller names, amounts (excl/incl tax), tax, items
- Saves to JSON with success/error status

**Arguments:**
- `-i, --input`: Input path (default: `invoices`)
- `-o, --output`: Output JSON (default: `invoice_results.json`)

**Prerequisites:**
- `.env` file with `GLM_API_KEY` (see Setup below)
- `pip install aiohttp PyMuPDF`

### Step 3: Generate Excel Report

```bash
# Default: 'invoice_results.json' → 'invoice_results.xlsx'
python .claude/skills/invoice-processor/scripts/convert_to_excel.py

# Custom paths
python .claude/skills/invoice-processor/scripts/convert_to_excel.py -i <input.json> -o <output.xlsx>
```

**What it does:**
- Reads JSON from Step 2
- Creates formatted Excel with 12 columns
- Auto-deletes input JSON after successful conversion

**Arguments:**
- `-i, --input`: Input JSON (default: `invoice_results.json`)
- `-o, --output`: Output Excel (default: `invoice_results.xlsx`)

**Prerequisites:**
- `pip install openpyxl`

## Usage Examples

### Basic (Non-ASCII directory names)

```bash
# Full 3-step workflow
python .claude/skills/invoice-processor/scripts/check_env.py
python .claude/skills/invoice-processor/scripts/invoice_ocr.py -i invoices -o invoice_results.json
python .claude/skills/invoice-processor/scripts/convert_to_excel.py -i invoice_results.json -o invoice_results.xlsx
```

### Custom Paths

```bash
python .claude/skills/invoice-processor/scripts/invoice_ocr.py -i invoices_2024 -o results_2024.json
python .claude/skills/invoice-processor/scripts/convert_to_excel.py -i results_2024.json -o report_2024.xlsx
```

## Troubleshooting

### Script Not Found / Encoding Errors
**Error:** `can't open file '...\��Ʊ����agent\scripts\...'`
**Cause:** Short paths (`scripts/`) fail in non-ASCII directories
**Solution:** Use full paths: `.claude/skills/invoice-processor/scripts/...`

### Command Not Found
**Error:** `dir: cannot access '/b'`
**Cause:** Windows CMD command in Unix shell
**Solution:** Use `ls` instead of `dir`

### API Key Not Set
**Error:** `错误: 请在 .env 文件中设置 GLM_API_KEY`
**Solution:** Create `.env` file in `invoice-processor` directory with `GLM_API_KEY=your_key`

### PDF Support Disabled
**Warning:** `未安装 PyMuPDF，PDF 支持已禁用`
**Solution:** `pip install PyMuPDF`

## Notes

- GLM API limit: 5 concurrent requests, 60s timeout per request
- Image limits: 5MB max, 6000x6000 pixels
- PDFs auto-converted to images (temp files cleaned up)
- **Path Best Practice:** Always use full relative paths (`.claude/skills/invoice-processor/scripts/`) when project directory contains non-ASCII characters

---

For detailed design principles, customization options, and architecture guidelines, see [README.md](README.md).
