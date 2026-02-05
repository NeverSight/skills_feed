---
name: form-filling
description: "Fill PDF and image forms using the Datalab Python SDK. Triggers: form filling, PDF forms, fillable documents, FormFillingOptions, batch fill forms."
compatibility: "Requires Python 3.10+, datalab-python-sdk, python-dotenv, and DATALAB_API_KEY (env or .env)."
---

# Datalab Form Filling

Fill PDF and image forms using the Datalab Python SDK (`datalab-python-sdk`).

## Prerequisites

```bash
pip install datalab-python-sdk python-dotenv
```

**API Key Setup**: The SDK requires `DATALAB_API_KEY`. Either:

- Set as environment variable: `export DATALAB_API_KEY=your_key`
- Or use a `.env` file in your project directory (recommended)

## Workflow

1. Gather field data from the user (field names, values, descriptions)
2. Determine form source (local file, URL, or image)
3. Configure options (context, confidence threshold, page range)
4. Fill the form using the SDK
5. Check results and handle unmatched fields

## When NOT to Use This Skill

- **Form creation** - This fills existing forms, doesn't create new ones
- **OCR/text extraction** - Use Datalab's OCR endpoints instead
- **Non-form documents** - Regular PDFs without fillable fields or clear form structure

## Quick Start

Use this in a **script file** (`.py`). In a notebook or REPL, `__file__` is undefined—use explicit paths for the form and output instead.

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from datalab_sdk import DatalabClient, FormFillingOptions

# In a .py file: script_dir = Path(__file__).parent. In notebook/REPL: script_dir = Path(".")
script_dir = Path(__file__).parent
load_dotenv(script_dir / ".env")

client = DatalabClient(api_key=os.getenv("DATALAB_API_KEY"))

options = FormFillingOptions(
    field_data={
        "full_name": {"value": "John Doe", "description": "Full legal name"},
        "date_of_birth": {"value": "1990-01-15", "description": "Date of birth"},
    },
    context="Employment application form",
    confidence_threshold=0.5,
)

form_path = script_dir / "form.pdf"
result = client.fill(str(form_path), options=options)
result.save_output(str(script_dir / "filled_form.pdf"))

print(f"Filled: {result.fields_filled}")
print(f"Not found: {result.fields_not_found}")
```

## Using the Fill Form Script

For quick command-line filling, use the bundled script. Run from the skill directory or use the full path:

```bash
# From skill directory (form.pdf and field_data.json in current dir)
python scripts/fill_form.py form.pdf field_data.json -o filled.pdf

# From another directory: use full paths for script, form, and field data
python /path/to/form-filling/scripts/fill_form.py /path/to/form.pdf /path/to/field_data.json -o filled.pdf
```

Options: `-o output.pdf`, `-c "context string"`, `-t 0.7` (threshold), `-p "0-2"` (pages 1-3, 0-indexed), `--async`

See `scripts/sample_field_data.json` for a template. The `field_data.json` format:

```json
{
  "name": { "value": "Jane Smith", "description": "Full name" },
  "ssn": { "value": "123-45-6789", "description": "Social Security Number" }
}
```

## Key Guidance

### Field Data Design

- Always include `description` for each field to improve matching accuracy
- Use `context` to describe the form type (e.g., "IRS W-4 Employee's Withholding Certificate")
- Field values are always strings, even for numbers and dates

### Supported Field Types

Text, date, numeric, checkbox (`"Yes"`/`"No"`), and signature (rendered as text).

### Handling Unmatched Fields

If `result.fields_not_found` is non-empty:

1. Improve field descriptions to better match the form's labels
2. Add or refine the `context` parameter
3. Lower `confidence_threshold` to catch more matches

### URL Source

```python
result = client.fill(file_url="https://example.com/form.pdf", options=options)
```

### Image Forms (Scanned PDFs, PNG, JPG)

The SDK handles image-based forms automatically:

```python
# Scanned form or image file
result = client.fill("scanned_form.png", options=options)
result.save_output("filled_form.png")  # Output matches input format
```

### Async Processing

For batch operations or non-blocking calls. Paths are relative to the current working directory.

```python
from datalab_sdk import AsyncDatalabClient, FormFillingOptions

async with AsyncDatalabClient(api_key=os.getenv("DATALAB_API_KEY")) as client:
    result = await client.fill("form.pdf", options=options)
    result.save_output("filled.pdf")
```

## Common Pitfalls

### API Key Not Found

**Problem**: `DatalabAPIError: You must pass in an api_key or set DATALAB_API_KEY`

**Solution**: The `.env` file isn't auto-loaded. Always:

1. Use `load_dotenv()` with explicit path: `load_dotenv(Path(__file__).parent / ".env")`
2. Pass API key explicitly: `DatalabClient(api_key=os.getenv("DATALAB_API_KEY"))`

### File Not Found When Running Script

**Problem**: Relative paths like `"form.pdf"` fail when script runs from a different directory.

**Solution**: Use absolute paths based on script location:

```python
script_dir = Path(__file__).parent
form_path = script_dir / "form.pdf"
result = client.fill(str(form_path), options=options)
```

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'datalab_sdk'`

**Solution**: Install the SDK first:

```bash
pip install datalab-python-sdk python-dotenv
```

## References

- **Full API details**: See [references/api-reference.md](references/api-reference.md) for installation/prerequisites, FormFillingOptions, confidence threshold tuning, image form handling, batch async patterns, result fields, error handling, and client configuration
