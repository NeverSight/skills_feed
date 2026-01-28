---
name: pdfco
description: PDF processing API for conversion, extraction, merging, splitting and more
vm0_secrets:
  - PDFCO_API_KEY
---

# PDF.co

All-in-one PDF processing API. Convert, extract, merge, split, compress PDFs and more. Supports OCR for scanned documents.

> Official docs: https://docs.pdf.co/

---

## When to Use

Use this skill when you need to:

- Extract text from PDF files (with OCR support)
- Convert PDF to CSV, JSON, or other formats
- Merge multiple PDFs into one
- Split PDF into multiple files
- Compress PDF to reduce file size
- Convert HTML/URL to PDF
- Parse invoices and documents with AI

---

## Prerequisites

1. Create an account at https://pdf.co/
2. Get your API key from https://app.pdf.co/

Set environment variable:

```bash
export PDFCO_API_KEY="your-email@example.com_your-api-key"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### 1. PDF to Text

Extract text from PDF with OCR support:

Write to `/tmp/request.json`:

```json
{
  "url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-to-text/sample.pdf",
  "inline": true
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/to/text" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

**With specific pages (1-indexed):**

Write to `/tmp/request.json`:

```json
{
  "url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-to-text/sample.pdf",
  "pages": "1-3",
  "inline": true
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/to/text" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 2. PDF to CSV

Convert PDF tables to CSV:

Write to `/tmp/request.json`:

```json
{
  "url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-to-csv/sample.pdf",
  "inline": true
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/to/csv" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 3. Merge PDFs

Combine multiple PDFs into one:

Write to `/tmp/request.json`:

```json
{
  "url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-merge/sample1.pdf,https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-merge/sample2.pdf",
  "name": "merged.pdf"
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/merge" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 4. Split PDF

Split PDF by page ranges:

Write to `/tmp/request.json`:

```json
{
  "url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-split/sample.pdf",
  "pages": "1-2,3-"
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/split" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 5. Compress PDF

Reduce PDF file size:

Write to `/tmp/request.json`:

```json
{
  "url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-optimize/sample.pdf",
  "name": "compressed.pdf"
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/optimize" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 6. HTML to PDF

Convert HTML or URL to PDF:

Write to `/tmp/request.json`:

```json
{
  "html": "<h1>Hello World</h1><p>This is a test.</p>",
  "name": "output.pdf"
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/from/html" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

**From URL:**

Write to `/tmp/request.json`:

```json
{
  "url": "https://example.com",
  "name": "webpage.pdf"
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/from/url" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 7. AI Invoice Parser

Extract structured data from invoices:

Write to `/tmp/request.json`:

```json
{
  "url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/ai-invoice-parser/sample-invoice.pdf",
  "inline": true
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/ai-invoice-parser" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 8. Upload Local File

Upload a local file first, then use the returned URL:

**Step 1: Get presigned upload URL**

```bash
bash -c 'curl -s "https://api.pdf.co/v1/file/upload/get-presigned-url?name=myfile.pdf&contenttype=application/pdf" --header "x-api-key: ${PDFCO_API_KEY}"' | jq -r '.presignedUrl, .url'
```

Copy the presigned URL and file URL from the response.

**Step 2: Upload file**

Replace `<presigned-url>` with the URL from Step 1:

```bash
curl -X PUT "<presigned-url>" --header "Content-Type: application/pdf" --data-binary @/path/to/your/file.pdf
```

**Step 3: Use file URL in subsequent API calls**

Replace `<file-url>` with the file URL from Step 1:

Write to `/tmp/request.json`:

```json
{
  "url": "<file-url>",
  "inline": true
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/to/text" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 9. Async Mode (Large Files)

For large files, use async mode to avoid timeouts:

**Step 1: Start async job**

Write to `/tmp/request.json`:

```json
{
  "url": "https://example.com/large-file.pdf",
  "async": true
}
```

```bash
bash -c 'curl -s --location --request POST "https://api.pdf.co/v1/pdf/convert/to/text" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json' | jq -r '.jobId'
```

Copy the job ID from the response.

**Step 2: Check job status**

Replace `<job-id>` with the job ID from Step 1:

Write to `/tmp/request.json`:

```json
{
  "jobid": "<job-id>"
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/job/check" --header "x-api-key: ${PDFCO_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

---

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | URL to source file (required) |
| `inline` | boolean | Return result in response body |
| `async` | boolean | Run as background job |
| `pages` | string | Page range, **1-indexed** (e.g., "1-3", "1,3,5", "2-") |
| `name` | string | Output filename |
| `password` | string | PDF password if protected |
| `expiration` | integer | Output link expiration in minutes (default: 60) |

---

## Response Format

```json
{
  "url": "https://pdf-temp-files.s3.amazonaws.com/.../result.pdf",
  "pageCount": 5,
  "error": false,
  "status": 200,
  "name": "result.pdf",
  "credits": 10,
  "remainingCredits": 9990
}
```

With `inline: true`, the response includes `body` field with extracted content.

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/pdf/convert/to/text` | PDF to text (OCR supported) |
| `/pdf/convert/to/csv` | PDF to CSV |
| `/pdf/convert/to/json` | PDF to JSON |
| `/pdf/merge` | Merge multiple PDFs |
| `/pdf/split` | Split PDF by pages |
| `/pdf/optimize` | Compress PDF |
| `/pdf/convert/from/html` | HTML to PDF |
| `/pdf/convert/from/url` | URL to PDF |
| `/ai-invoice-parser` | AI-powered invoice parsing |
| `/document-parser` | Template-based document parsing |
| `/file/upload/get-presigned-url` | Get upload URL |
| `/job/check` | Check async job status |

---

## Guidelines

1. **File Sources**: Use direct URLs or upload files first via presigned URL
2. **Large Files**: Use `async: true` for files over 40 pages or 10MB
3. **OCR**: Automatically enabled for scanned PDFs (set `lang` for non-English)
4. **Rate Limits**: Check your plan at https://pdf.co/pricing
5. **Output Expiration**: Download results within expiration time (default 60 min)
6. **Credits**: Each operation costs credits; check `remainingCredits` in response
