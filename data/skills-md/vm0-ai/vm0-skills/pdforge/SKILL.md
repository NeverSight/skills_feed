---
name: pdforge
description: PDForge (PDF Noodle) API for generating PDFs from templates or HTML via curl.
vm0_secrets:
  - PDFORGE_API_KEY
---

# PDForge API (PDF Noodle)

Use the PDForge API via direct `curl` calls to **generate PDFs** from templates or raw HTML.

> Official docs: `https://docs.pdforge.com/`

Note: PDForge has been rebranded to PDF Noodle. Both `api.pdforge.com` and `api.pdfnoodle.com` work.

---

## When to Use

Use this skill when you need to:

- **Generate PDFs from reusable templates** with dynamic data
- **Convert HTML to PDF** directly
- **Create invoices, reports, or documents** programmatically
- **Export PNG images** instead of PDFs
- **Batch generate documents** using async endpoints with webhooks

---

## Prerequisites

1. Sign up at [PDF Noodle](https://pdfnoodle.com/) (formerly PDForge)
2. Go to the API Keys menu in the dashboard
3. Copy your API key (format: `pdfnoodle_api_xxxxx`)
4. Store it in the environment variable `PDFORGE_API_KEY`

```bash
export PDFORGE_API_KEY="pdfnoodle_api_your-key-here"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq '.field'
> ```

## How to Use

All examples below assume you have `PDFORGE_API_KEY` set.

Base URL: `https://api.pdfnoodle.com/v1`

---

### 1. Generate PDF from Template (Sync)

Generate a PDF using a pre-built template with dynamic data.

Write to `/tmp/pdforge_request.json`:

```json
{
  "templateId": "your-template-id",
  "data": {
    "name": "John Doe",
    "date": "2025-01-15",
    "items": [
      {"description": "Item 1", "price": 100},
      {"description": "Item 2", "price": 200}
    ]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdfnoodle.com/v1/pdf/sync" --header "Authorization: Bearer ${PDFORGE_API_KEY}" --header "Content-Type: application/json" -d @/tmp/pdforge_request.json'
```

**Response:**

```json
{
  "signedUrl": "https://storage.googleapis.com/...",
  "executionTime": 1234
}
```

The `signedUrl` is a temporary URL (expires in 1 hour) to download the generated PDF.

---

### 2. Generate PDF from Template (Async)

For batch processing, use the async endpoint with a webhook.

Write to `/tmp/pdforge_request.json`:

```json
{
  "templateId": "your-template-id",
  "webhook": "https://your-server.com/webhook",
  "data": {
    "name": "Jane Doe",
    "amount": 500
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdfnoodle.com/v1/pdf/async" --header "Authorization: Bearer ${PDFORGE_API_KEY}" --header "Content-Type: application/json" -d @/tmp/pdforge_request.json'
```

**Response:**

```json
{
  "requestId": "abc123"
}
```

The webhook will receive the `signedUrl` when generation is complete.

---

### 3. Convert HTML to PDF (Sync)

Convert raw HTML directly to PDF without a template.

Write to `/tmp/pdforge_request.json`:

```json
{
  "html": "<html><body><h1>Hello World</h1><p>This is a PDF generated from HTML.</p></body></html>"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdfnoodle.com/v1/html-to-pdf/sync" --header "Authorization: Bearer ${PDFORGE_API_KEY}" --header "Content-Type: application/json" -d @/tmp/pdforge_request.json'
```

---

### 4. Convert HTML to PDF with Styling

Include CSS for styled PDFs.

Write to `/tmp/pdforge_request.json`:

```json
{
  "html": "<html><head><style>body { font-family: Arial; } h1 { color: #333; } .invoice { border: 1px solid #ddd; padding: 20px; }</style></head><body><div class=\"invoice\"><h1>Invoice #001</h1><p>Amount: $500</p></div></body></html>"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdfnoodle.com/v1/html-to-pdf/sync" --header "Authorization: Bearer ${PDFORGE_API_KEY}" --header "Content-Type: application/json" -d @/tmp/pdforge_request.json'
```

---

### 5. Generate PNG Instead of PDF

Set `convertToImage` to true to get a PNG.

Write to `/tmp/pdforge_request.json`:

```json
{
  "html": "<html><body><h1>Image Export</h1></body></html>",
  "convertToImage": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdfnoodle.com/v1/html-to-pdf/sync" --header "Authorization: Bearer ${PDFORGE_API_KEY}" --header "Content-Type: application/json" -d @/tmp/pdforge_request.json'
```

---

### 6. Download Generated PDF

After getting the `signedUrl`, download the PDF:

Replace `<your-signed-url>` with the actual signed URL from the previous response:

```bash
curl -s -o output.pdf "https://storage.googleapis.com/<your-signed-url>"
```

---

## Request Parameters

### Template Endpoint Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `templateId` | string | Yes | Template ID from dashboard |
| `data` | object | Yes | Variables for the template |
| `webhook` | string | Async only | Webhook URL for delivery |
| `convertToImage` | boolean | No | Return PNG instead of PDF |
| `metadata` | object | No | PDF metadata (title, author, etc.) |
| `hasCover` | boolean | No | Hide header/footer on first page |
| `debug` | boolean | No | Enable debug mode |

### HTML Endpoint Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `html` | string | Yes | HTML content to convert |
| `convertToImage` | boolean | No | Return PNG instead of PDF |
| `metadata` | object | No | PDF metadata settings |
| `pdfParams` | object | No | PDF generation options |

### Metadata Object

```json
{
  "metadata": {
  "title": "Invoice #001",
  "author": "Company Name",
  "subject": "Monthly Invoice",
  "keywords": ["invoice", "payment"]
  }
}
```

---

## Guidelines

1. **Use templates for reusable documents**: Create templates in the dashboard for invoices, reports, etc.
2. **Use HTML endpoint for one-off documents**: When you don't need a reusable template
3. **Use async for batch processing**: Async endpoint is better for generating many PDFs
4. **Download promptly**: Signed URLs expire in 1 hour
5. **Include CSS inline**: For HTML to PDF, include all styles in the HTML
