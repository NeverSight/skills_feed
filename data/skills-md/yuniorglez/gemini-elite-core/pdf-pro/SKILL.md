---
name: pdf-pro
id: pdf-pro
version: 1.1.0
description: "Master of PDF engineering, specialized in AI-driven extraction, high-fidelity Generation (Puppeteer), and PDF 2.0 Security."
last_updated: "2026-01-22"
---

# Skill: PDF Pro (Standard 2026)

**Role:** The PDF Pro is a specialized agent responsible for the entire lifecycle of document engineering. This includes "Semantic Extraction" using AI models, "High-Fidelity Generation" via headless browsers, and "Forensic Modification" using low-level byte manipulation. In 2026, the Squaads AI Core prioritizes Bun-native and JavaScript-first solutions for seamless integration with Next.js 16.2.

## 🎯 Primary Objectives
1.  **Semantic Extraction:** Move beyond raw text to structured JSON using LLM-assisted OCR and layout analysis.
2.  **High-Fidelity Generation:** Use Puppeteer/Playwright for pixel-perfect HTML-to-PDF conversion with CSS Print Support.
3.  **PDF 2.0 Compliance:** Implement AES-256 encryption, UTF-8 metadata, and accessible (Tagged) PDF structures.
4.  **Edge-Ready Processing:** Use lightweight libraries like `unpdf` for serverless and edge environments.

---

## 🏗️ The 2026 Toolbelt

### 1. Bun-Native & JS Libraries (Primary)
- **pdf-lib:** Byte-level modification, merging, splitting, and form filling.
- **unpdf:** Ultra-lightweight extraction for Edge/Serverless.
- **Puppeteer/Playwright:** The gold standard for generating PDFs from React templates.
- **Mistral/OpenAI OCR:** Semantic extraction for complex layouts and handwriting.

### 2. Forensic Utilities (Legacy/Advanced)
- **qpdf:** CLI tool for structural repairs and decryption.
- **poppler-utils:** Fast C-based text and image extraction.

---

## 🛠️ Implementation Patterns

### 1. High-Fidelity Generation (Next.js 16.2)
Generating PDFs from React components ensures visual consistency with the web app.

```tsx
// app/api/generate-pdf/route.ts
import puppeteer from 'puppeteer';

export async function POST(req: Request) {
  const { htmlContent } = await req.json();
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
  const pdfBuffer = await page.pdf({
    format: 'A4',
    printBackground: true,
    margin: { top: '20px', bottom: '20px' }
  });

  await browser.close();
  return new Response(pdfBuffer, {
    headers: { 'Content-Type': 'application/pdf' }
  });
}
```

### 2. AI-Driven Semantic Extraction
Using LLMs to turn unstructured PDF text into validated Zod schemas.

```typescript
import { unpdf } from 'unpdf';
import { generateObject } from 'ai'; // AI SDK 2026

async function extractInvoice(buffer: Buffer) {
  const { text } = await unpdf.extractText(buffer);
  
  const { object } = await generateObject({
    model: myModel,
    schema: invoiceSchema,
    prompt: `Extract structured data from this PDF text: ${text}`
  });
  
  return object;
}
```

---

## 🔒 PDF 2.0 Security & Integrity

### AES-256 Encryption
PDF 2.0 deprecates weak algorithms. Use `qpdf` or modern JS wrappers for secure locking.

```bash
# Secure a PDF with 2026 standards
qpdf --encrypt user-pass owner-pass 256 -- input.pdf secured.pdf
```

### Digital Signatures (PAdES)
Integrate with OIDC providers or Hardware Security Modules (HSMs) for legally binding signatures.

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** use `pypdf` for complex layout extraction; it fails on multi-column or overlapping text. Use `pdfplumber` or AI OCR.
2.  **NEVER** generate PDFs using `canvas` drawing commands if HTML/CSS templates are an option. Maintenance is a nightmare.
3.  **NEVER** store unencrypted PDFs containing PII (Personally Identifiable Information) in public S3 buckets.
4.  **NEVER** rely on `window.print()` for automated server-side generation. It is non-deterministic.

---

## 🛠️ Troubleshooting Guide

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **Missing Fonts** | System fonts not in container | Use Puppeteer with embedded Google Fonts or WOFF2. |
| **Garbled Text** | Complex CID encoding | Use `poppler` with `-enc UTF-8` or an AI-OCR layer. |
| **Huge File Size** | High-res images not optimized | Run a compression pass using `ghostscript` or `pdf-lib` scaling. |
| **Form Filling Fails** | Flattened PDF fields | Use `pdf-lib` to inspect `AcroForm` fields before writing. |

---

## 📚 Reference Library
- **[AI Extraction Patterns](./references/1-ai-extraction-patterns.md):** Mastering semantic document understanding.
- **[High-Fidelity Generation](./references/2-high-fidelity-generation.md):** HTML-to-PDF at scale.
- **[Legacy Utilities](./references/3-legacy-python-utilities.md):** When to reach for Python/CLI tools.

---

## 📜 Standard Operating Procedure (SOP)
1.  **Requirement Check:** Is the goal *Creation*, *Extraction*, or *Modification*?
2.  **Tool Selection:** 
    - Creation -> Puppeteer.
    - Extraction -> AI SDK + unpdf.
    - Modification -> pdf-lib.
3.  **Environment Check:** Is this running in an Edge Function? (If yes, avoid Puppeteer).
4.  **Implementation:** Build with strict TypeScript typing.
5.  **Audit:** Verify PDF 2.0 metadata and accessibility (A11y) tags.

---

## 📈 Quality Metrics
- **Extraction Accuracy:** > 98% (Measured against ground truth JSON).
- **Generation Speed:** < 2s for a 10-page document.
- **Security Audit:** Zero weak crypto algorithms (Verified via `qpdf`).

---

## 🔄 Last Refactor Details
- **By:** Gemini Elite Conductor
- **Date:** January 22, 2026
- **Version:** 1.1.0 (2026 Standard)
- **Focus:** Shift from Python-centric to JS-centric AI-integrated document engineering.

---

**End of PDF Pro Standard (v1.1.0)**
