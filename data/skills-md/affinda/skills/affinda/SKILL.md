---
name: affinda
description: Integrate with Affinda's document AI API to extract structured data from documents (invoices, resumes, receipts, contracts, and custom types). Covers authentication, client libraries (Python, TypeScript), structured outputs with Pydantic models and TypeScript interfaces, webhooks, upload patterns, and the full documentation map. Use when building integrations that parse, classify, or extract data from documents using Affinda.
license: MIT
metadata:
  author: affinda
  version: "1.0"
---

# Affinda — AI Document Processing Platform

Affinda extracts structured data from documents (invoices, resumes, receipts, contracts, and any custom document type) using machine learning. The API turns uploaded files into clean JSON. Over 250 million documents processed for 500+ organisations in 40 countries.

Full documentation: <https://docs.affinda.com>
OpenAPI spec: <https://api.affinda.com/static/v3/api_spec.yaml>
Support: support@affinda.com

---

## Core Concepts

| Concept           | Description |
|-------------------|-------------|
| **Organization**  | Top-level account. Contains users, billing, document types, and workspaces. |
| **Workspace**     | Logical container for documents. Scopes permissions, webhooks, and processing settings. |
| **Document Type** | A model configuration defining how a specific kind of document is parsed (invoice, resume, custom). |
| **Document**      | An uploaded file (PDF, image, DOCX, etc.) plus its extracted data and metadata. |

The workflow is: **Upload -> Pre-process -> Split -> Classify -> Extract -> Validate -> Export**.

---

## API Basics

### Base URLs

| Region              | API Base URL                      | App URL                        |
|---------------------|-----------------------------------|--------------------------------|
| Australia (Global)  | `https://api.affinda.com`         | `https://app.affinda.com`      |
| United States       | `https://api.us1.affinda.com`     | `https://app.us1.affinda.com`  |
| European Union      | `https://api.eu1.affinda.com`     | `https://app.eu1.affinda.com`  |

Use the base URL matching the region where the user's account was created.

### Authentication

All requests require a Bearer token:

```
Authorization: Bearer <API_KEY>
```

API keys are per-user, managed at *Settings -> API Keys* in the Affinda dashboard. Up to 3 keys per user. Keys can have custom names and expiry dates. A key is only visible once at creation -- store it securely.

### Rate Limits and File Constraints

- **High-priority queue**: 30 documents/minute (exceeding returns `429`)
- **Low-priority queue**: No submission limit (set `lowPriority: true`)
- **Max file size**: 20 MB (5 MB for resumes)
- **Default page limit**: 20 pages per document (can be increased on request)
- **Supported formats**: PDF, DOC, DOCX, XLSX, ODT, RTF, TXT, HTML, PNG, JPG, TIFF, JPEG

---

## Client Libraries

### Python (recommended)

```bash
pip install affinda
```

```python
from pathlib import Path
from affinda import AffindaAPI, TokenCredential

credential = TokenCredential(token="YOUR_API_KEY")
client = AffindaAPI(credential=credential)

with Path("invoice.pdf").open("rb") as f:
    doc = client.create_document(file=f, workspace="YOUR_WORKSPACE_ID")

print(doc.data)  # Extracted JSON
```

GitHub: <https://github.com/affinda/affinda-python>
PyPI: <https://pypi.org/project/affinda/>

### TypeScript / JavaScript (recommended)

```bash
npm install @affinda/affinda
```

```typescript
import { AffindaAPI, AffindaCredential } from "@affinda/affinda";
import * as fs from "fs";

const credential = new AffindaCredential("YOUR_API_KEY");
const client = new AffindaAPI(credential);

const doc = await client.createDocument({
  file: fs.createReadStream("invoice.pdf"),
  workspace: "YOUR_WORKSPACE_ID",
});

console.log(doc.data); // Extracted JSON
```

GitHub: <https://github.com/affinda/affinda-typescript>
npm: <https://www.npmjs.com/package/@affinda/affinda>

### Other Libraries

- **.NET**: `dotnet add package Affinda.API` -- [GitHub](https://github.com/affinda/affinda-dotnet)
- **Java**: [Maven repository](https://mvnrepository.com/artifact/com.affinda.api/affinda-api-client) -- [GitHub](https://github.com/affinda/affinda-java)

> Note: The .NET and Java libraries may lag behind the Python and TypeScript libraries in feature parity.

### Direct HTTP (cURL)

```bash
curl -X POST https://api.affinda.com/v3/documents \
  -H "Authorization: Bearer $AFFINDA_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "workspace=YOUR_WORKSPACE_ID"
```

---

## Structured Outputs (Type-Safe Responses)

**This is the recommended approach for building robust integrations.** Affinda can generate typed models from your document type configuration, giving you auto-completion, validation, and type safety.

### Python -- Pydantic Models

Generate Pydantic v2 models that match your document type's field schema:

```bash
# Set your API key (or export AFFINDA_API_KEY)
python -m affinda generate_models --workspace-id=YOUR_WORKSPACE_ID
```

This creates a `./affinda_models/` directory with one `.py` file per document type. Each file contains Pydantic `BaseModel` classes with all your configured fields as typed, optional attributes.

**Use the generated models when calling the API:**

```python
from pathlib import Path
from affinda import AffindaAPI, TokenCredential
from affinda_models.invoice import Invoice  # Generated model

credential = TokenCredential(token="YOUR_API_KEY")
client = AffindaAPI(credential=credential)

with Path("invoice.pdf").open("rb") as f:
    doc = client.create_document(
        file=f,
        workspace="YOUR_WORKSPACE_ID",
        data_model=Invoice,  # Enables Pydantic validation
    )

# doc.parsed is a typed Invoice instance
print(doc.parsed.invoice_number)
print(doc.parsed.total_amount)

# doc.data is still available as raw JSON
print(doc.data)
```

**Handling validation errors gracefully:**

```python
with Path("invoice.pdf").open("rb") as f:
    doc = client.create_document(
        file=f,
        workspace="YOUR_WORKSPACE_ID",
        data_model=Invoice,
        ignore_validation_errors=True,  # Don't raise on schema mismatch
    )

if doc.parsed:
    print(doc.parsed.invoice_number)  # Type-safe access
else:
    print("Validation failed, falling back to raw data")
    print(doc.data)
```

**CLI options:**

```bash
python -m affinda generate_models --workspace-id=ID        # All types in a workspace
python -m affinda generate_models --document-type-id=ID    # Single document type
python -m affinda generate_models --organization-id=ID     # All types in an org
python -m affinda generate_models --output-dir=./my_models # Custom output path
python -m affinda generate_models --help                   # All options
```

### TypeScript -- Generated Interfaces

Generate TypeScript interfaces that match your document type's field schema:

```bash
# Set your API key (or export AFFINDA_API_KEY)
npm exec affinda-generate-interfaces -- --workspace-id=YOUR_WORKSPACE_ID
```

This creates an `./affinda-interfaces/` directory with one `.ts` file per document type. Each file contains TypeScript interfaces with all your configured fields.

**Use the generated interfaces for type-safe access:**

```typescript
import { AffindaAPI, AffindaCredential } from "@affinda/affinda";
import * as fs from "fs";
import { Invoice } from "./affinda-interfaces/Invoice";

const credential = new AffindaCredential("YOUR_API_KEY");
const client = new AffindaAPI(credential);

const doc = await client.createDocument({
  file: fs.createReadStream("invoice.pdf"),
  workspace: "YOUR_WORKSPACE_ID",
});

const parsed = doc.data as Invoice;
console.log(parsed.invoiceNumber);  // Type-safe access
console.log(parsed.totalAmount);
```

**CLI options:**

```bash
npm exec affinda-generate-interfaces -- --workspace-id=ID       # All types in workspace
npm exec affinda-generate-interfaces -- --document-type-id=ID   # Single document type
npm exec affinda-generate-interfaces -- --output-dir=./types    # Custom output path
npm exec affinda-generate-interfaces -- --help                  # All options
```

### Why Use Structured Outputs?

- **Type safety**: Catch field name typos and type mismatches at compile/lint time
- **Auto-completion**: IDE support for all extracted fields
- **Validation**: Pydantic automatically validates the API response structure
- **Schema-driven**: Models stay in sync with your document type configuration -- regenerate after schema changes
- **Documentation as code**: The generated models serve as living documentation of your extraction schema

---

## Document Upload Options

There are three patterns for submitting documents and retrieving results:

### 1. Synchronous (simplest)

Upload and block until parsing completes. The response contains the extracted data.

```python
doc = client.create_document(file=f, workspace="WORKSPACE_ID")
# wait defaults to True -- blocks until ready
print(doc.data)
```

**Best for**: Interactive apps, low volume, quick prototyping.
**Limitation**: Can timeout on large or complex documents.

### 2. Asynchronous with Polling

Upload with `wait=false`, receive a document ID, then poll `GET /documents/{id}` until `ready` is `true`.

```python
doc = client.create_document(file=f, workspace="WORKSPACE_ID", wait=False)
# doc.data is empty -- poll until ready
doc = client.get_document(doc.meta.identifier)
```

**Best for**: Batch processing, large documents, high volume.

### 3. Asynchronous with Webhooks (recommended for production)

Upload the document, then receive a webhook notification when processing completes. This is the most efficient pattern for production systems.

```python
# 1. Upload
doc = client.create_document(file=f, workspace="WORKSPACE_ID", wait=False)

# 2. Receive webhook at your endpoint when ready
# 3. Fetch full data
doc = client.get_document(identifier_from_webhook)
```

**Best for**: Real-time workflows, event-driven architectures, production systems.

See the [Webhooks section](#webhooks) below for setup details.

### Upload Parameters

| Parameter                | Type    | Description |
|--------------------------|---------|-------------|
| `file`                   | binary  | The document file. Mutually exclusive with `url`. |
| `url`                    | string  | URL to download and process. Mutually exclusive with `file`. |
| `workspace`              | string  | Workspace identifier (required). |
| `documentType`           | string  | Document type identifier (optional -- enables skip-classification). |
| `wait`                   | boolean | `true` (default): block until done. `false`: return immediately. |
| `customIdentifier`       | string  | Your internal ID for the document. |
| `expiryTime`             | ISO-8601| Auto-delete the document at this time. |
| `rejectDuplicates`       | boolean | Reject if duplicate of existing document. |
| `lowPriority`            | boolean | Route to low-priority queue (no rate limit). |
| `compact`                | boolean | Return compact response (with `wait=true`). |
| `deleteAfterParse`       | boolean | Delete data after parsing (requires `wait=true`). |
| `enableValidationTool`   | boolean | Make document viewable in validation UI. Set `false` for speed. |

---

## Response Structure

Each extracted field in the response includes metadata:

| Field                      | Description |
|----------------------------|-------------|
| `raw`                      | Raw extracted text before processing |
| `parsed`                   | Processed value after formatting and mapping |
| `confidence`               | Overall confidence score (0-1) |
| `classificationConfidence` | Confidence the field was correctly classified |
| `textExtractionConfidence` | Confidence text was correctly extracted |
| `isVerified`               | Whether the value has been validated (any means) |
| `isClientVerified`         | Whether validated by a human |
| `isAutoVerified`           | Whether auto-validated by rules |
| `rectangle`                | Bounding box coordinates on the page |
| `pageIndex`                | Which page the data appears on |

Document-level metadata includes `ready`, `failed`, `language`, `pages`, `isOcrd`, `ocrConfidence`, `reviewUrl`, `isConfirmed`, `isRejected`, `isArchived`, `errorCode`, and `errorDetail`.

Full metadata reference: <https://docs.affinda.com/reference/metadata>

---

## Webhooks

Affinda uses RESTHooks -- webhook subscriptions managed via REST API. Webhooks can be scoped to an organization or workspace.

### Available Events

| Event                          | Description |
|--------------------------------|-------------|
| `document.parse.completed`     | Parsing finished (succeeded or failed) |
| `document.parse.succeeded`     | Parsing succeeded |
| `document.parse.failed`        | Parsing failed |
| `document.validate.completed`  | Document confirmed (manually or auto) |
| `document.classify.completed`  | Classification finished |
| `document.classify.succeeded`  | Classification succeeded |
| `document.classify.failed`     | Classification failed |
| `document.rejected`            | Document rejected |

### Setup Flow

1. **Subscribe** -- `POST /v3/resthook_subscriptions` with `targetUrl`, `event`, and `organization` (or `workspace`).
2. **Confirm** -- Affinda sends a `POST` to your `targetUrl` with an `X-Hook-Secret` header. Respond with `200`, then call `POST /v3/resthook_subscriptions/activate` with that secret.
3. **Receive** -- Affinda sends webhook payloads to your endpoint. Respond `200` to acknowledge.

### Signature Verification

Enable payload signing via Organization Settings -> Webhook Signature Key. Incoming webhooks include an `X-Hook-Signature` header (`<timestamp>.<signature>`). Verify using HMAC-SHA256:

```python
import hmac, hashlib, json, time

def verify_webhook(request, sig_key: bytes) -> bool:
    sig_header = request.headers["X-Hook-Signature"]
    timestamp, sig_received = sig_header.split(".")
    sig_calculated = hmac.new(sig_key, msg=request.body, digestmod=hashlib.sha256).hexdigest()

    sig_ok = hmac.compare_digest(sig_received, sig_calculated)
    body = json.loads(request.body)
    time_ok = (time.time() - body["timestamp"]) < 600  # 10 min window
    return sig_ok and time_ok
```

### Webhook Payload

The payload contains document metadata (not the full parsed data). Use the `identifier` to fetch full results:

```json
{
  "id": "e3bd1942-...",
  "event": "document.parse.completed",
  "timestamp": 1665637107,
  "payload": {
    "identifier": "abcdXYZ",
    "ready": true,
    "failed": false,
    "fileName": "invoice.pdf",
    "workspace": { "identifier": "...", "name": "..." }
  }
}
```

### Retry Behavior

- `200` -- Success, delivery confirmed
- `410` -- Subscription auto-deleted (endpoint "gone")
- Other 4xx/5xx -- Retried with exponential backoff for ~1 day

Full webhook docs: <https://docs.affinda.com/reference/webhooks>

---

## Embedded Validation UI

Affinda provides a human-in-the-loop validation interface that can be embedded in your application via iframe. Each document response includes a `reviewUrl` -- a signed URL valid for 60 minutes.

**Implementation pattern:**
1. Store only the Affinda document `identifier` in your system
2. When a user needs to review, fetch a fresh `reviewUrl` via `GET /documents/{id}`
3. Embed the URL in an iframe
4. Do not persist the URL -- treat it as ephemeral

The UI supports custom theming (colors, fonts, border radius) in embedded mode. Contact Affinda to configure.

Full embedded docs: <https://docs.affinda.com/reference/embedded>

---

## Key API Methods

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/v3/documents` | Upload and parse a document |
| GET    | `/v3/documents/{id}` | Retrieve a document and its data |
| PATCH  | `/v3/documents/{id}` | Update document fields/status |
| DELETE | `/v3/documents/{id}` | Delete a document |
| GET    | `/v3/documents` | List documents (with filtering) |
| GET    | `/v3/documents/{id}/redacted` | Download redacted PDF |

### Workspaces

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/v3/workspaces` | List workspaces |
| POST   | `/v3/workspaces` | Create a workspace |
| GET    | `/v3/workspaces/{id}` | Get workspace details |
| PATCH  | `/v3/workspaces/{id}` | Update workspace |
| DELETE | `/v3/workspaces/{id}` | Delete workspace |

### Annotations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/v3/annotations` | List annotations for a document |
| POST   | `/v3/annotations` | Create an annotation |
| PATCH  | `/v3/annotations/{id}` | Update an annotation |
| POST   | `/v3/annotations/batch_create` | Batch create annotations |
| POST   | `/v3/annotations/batch_update` | Batch update annotations |
| POST   | `/v3/annotations/batch_delete` | Batch delete annotations |

### Webhooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/v3/resthook_subscriptions` | Create subscription |
| POST   | `/v3/resthook_subscriptions/activate` | Activate with X-Hook-Secret |
| GET    | `/v3/resthook_subscriptions` | List subscriptions |
| PATCH  | `/v3/resthook_subscriptions/{id}` | Update subscription |
| DELETE | `/v3/resthook_subscriptions/{id}` | Delete subscription |

Full API reference: <https://docs.affinda.com/reference/getting-started>
OpenAPI spec: <https://api.affinda.com/static/v3/api_spec.yaml>

---

## Common Integration Patterns

Affinda supports six integration workflow patterns depending on where validation logic lives and where exceptions are handled:

| Pattern | Description | Webhook Event |
|---------|-------------|---------------|
| **W1** -- No validation | Upload -> get JSON. No rules, no human review. | `document.parse.completed` |
| **W2** -- Client-side validation | Same as W1; your system applies rules after export. | `document.parse.completed` |
| **W3** -- Affinda validation logic | Affinda validates automatically; no human review. | `document.validate.completed` |
| **W4** -- Review all in Affinda | Humans review every document in Affinda UI. | `document.validate.completed` |
| **W5** -- Client rules + Affinda review | Your rules, pushed back as warnings; flagged docs reviewed in Affinda. | `document.parse.completed` then `document.validate.completed` |
| **W6** -- Full Affinda validation | Affinda validates; exceptions reviewed in Affinda UI. | `document.validate.completed` |

For most new integrations, **W1 or W2** is the simplest starting point. **W6** provides the most automation with human-in-the-loop for exceptions.

Full solution design guide: <https://docs.affinda.com/academy/solution-design>

---

## Common Errors

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| `duplicate_document_error` | Document rejected as duplicate | Disable "Reject duplicates" or upload unique files |
| `no_text_found` | No extractable text | Check file is not a photo of an object; try OCR |
| `file_corrupted` | File is corrupted | Re-upload a valid file |
| `file_too_large` | Exceeds 20 MB limit | Reduce file size |
| `invalid_file_type` | Unsupported format | Use PDF, DOC, DOCX, XLSX, ODT, RTF, TXT, HTML, PNG, JPG, TIFF, JPEG |
| `no_parsing_credits` | Out of credits | Purchase more credits and reparse |
| `password_protected` | File is password-protected | Remove password and re-upload |
| `document_classification_failed` | No matching document type | Check document type configuration or disable "Reject Documents" |
| `capacity_exceeded` | System capacity exceeded | Wait and retry |
| `parse_terminated` | Exceeded timeout | Contact Affinda for custom limits |

Full error reference: <https://docs.affinda.com/error-glossary>

---

## Documentation Map

Use this index to find detailed information on specific topics. Each link goes to the full documentation page.

### Affinda Academy (Tutorials)

- **[Getting Started](https://docs.affinda.com/academy/getting-started)** -- Core concepts: organizations, workspaces, document types, statuses, and the processing workflow.
- **[Creating a New Model](https://docs.affinda.com/academy/model-creation)** -- Step-by-step guide to creating extraction models from scratch.
- **[Improving Accuracy](https://docs.affinda.com/academy/improving-accuracy)** -- Strategies for 99%+ accuracy via model memory, field prompts, and OCR settings.
- **[User Validation of Extracted Data](https://docs.affinda.com/academy/review-extraction)** -- How to validate and correct extractions in the Affinda UI.
- **[Table Editor](https://docs.affinda.com/academy/table-editor)** -- Grid and freeform modes for validating table extractions.
- **[Reviewing Splitting & Classification](https://docs.affinda.com/academy/split-classify)** -- How to correct document splitting and classification.
- **[Schema Design Best Practices](https://docs.affinda.com/academy/schema-design)** -- Field configuration trade-offs, advanced options, and schema design guidance.
- **[Straight-Through Processing](https://docs.affinda.com/academy/straight-through-processing)** -- Data mapping, validation rules, and auto-confirmation for full automation.
- **[Integration Workflows](https://docs.affinda.com/academy/solution-design)** -- Six workflow patterns (W1-W6) for different integration scenarios.
- **[Integration Agent](https://docs.affinda.com/academy/integration-agent)** -- No-code integrations using AI agent and Pipedream.

### Configuration Guide

**Overview & Workflow:**
- **[Workflow](https://docs.affinda.com/configuration/workflow)** -- End-to-end document processing pipeline stages.
- **[Glossary](https://docs.affinda.com/configuration/glossary)** -- Platform terminology definitions.
- **[Document Status](https://docs.affinda.com/configuration/document-status)** -- For Review, Confirmed, Archived, Rejected states.

**Ingestion & Pre-Processing:**
- **[Ingestion](https://docs.affinda.com/configuration/ingestion)** -- Upload methods: manual, email, API.
- **[Email Upload](https://docs.affinda.com/configuration/email-upload)** -- Email-to-workspace document ingestion.
- **[Pre-Processing](https://docs.affinda.com/configuration/preprocessing)** -- Automated cleaning before extraction.
- **[OCR](https://docs.affinda.com/configuration/ocr)** -- OCR modes: Skip, Auto-detect, Partial, Full.
- **[Duplicates](https://docs.affinda.com/configuration/duplicates)** -- Duplicate detection and rejection.

**Splitting, Classification & Extraction:**
- **[Splitting](https://docs.affinda.com/configuration/splitting)** -- Auto-separate multi-document files.
- **[Classification](https://docs.affinda.com/configuration/classification)** -- Auto-categorize documents by type.
- **[Field Configuration](https://docs.affinda.com/configuration/field-configuration)** -- Field names, types, and settings.
- **[Standard Fields](https://docs.affinda.com/configuration/standard-fields)** -- Text, numbers, dates, location, phone, URL types.
- **[Groups & Tables](https://docs.affinda.com/configuration/group-table-fields)** -- Repeating structures and line items.
- **[Picklists & Data Sources](https://docs.affinda.com/configuration/picklists)** -- Controlled vocabularies and master data matching.
- **[Checkboxes](https://docs.affinda.com/configuration/checkboxes)** -- Label and true/false checkbox extraction.
- **[Image Fields](https://docs.affinda.com/configuration/images)** -- Signature, headshot, and seal extraction.
- **[Model Memory](https://docs.affinda.com/configuration/model-memory)** -- RAG-based learning from validated documents.

**Validation & Export:**
- **[Machine Validation](https://docs.affinda.com/configuration/machine-validation)** -- Automated validation overview.
- **[Validation Rules](https://docs.affinda.com/configuration/validation-rules)** -- Natural-language business rule creation.
- **[Confidence](https://docs.affinda.com/configuration/confidence)** -- Confidence scoring and thresholds.
- **[User Validation](https://docs.affinda.com/configuration/user-validation)** -- Human review interface.
- **[Data Export](https://docs.affinda.com/configuration/export-data)** -- JSON, XML, CSV export options.
- **[Redaction](https://docs.affinda.com/configuration/redaction)** -- PDF redaction of sensitive data.
- **[User Management](https://docs.affinda.com/configuration/user-management)** -- Roles and permissions.

### API Reference

- **[Quick Start](https://docs.affinda.com/reference/getting-started)** -- First API call walkthrough with code examples.
- **[Authentication](https://docs.affinda.com/reference/authentication)** -- API key management and rotation.
- **[Upload Options](https://docs.affinda.com/reference/upload-options)** -- Sync, async polling, and webhook patterns.
- **[Metadata](https://docs.affinda.com/reference/metadata)** -- Field-level and document-level metadata reference.
- **[Limits](https://docs.affinda.com/reference/limits)** -- Rate limits, file size limits, page limits.
- **[Webhooks](https://docs.affinda.com/reference/webhooks)** -- Webhook setup, events, signature verification.
- **[Embedded Mode](https://docs.affinda.com/reference/embedded)** -- Embedding validation UI via iframe.
- **[Client Libraries](https://docs.affinda.com/reference/client-libraries)** -- Python, JavaScript, .NET, Java SDKs.
- **[Structured Outputs (Pydantic)](https://docs.affinda.com/reference/pydantic-models)** -- Generate Python Pydantic models from document types.
- **[TypeScript Interfaces](https://docs.affinda.com/reference/typescript-interfaces)** -- Generate TypeScript interfaces from document types.

### Resume Parsing Guide

- **[Getting Started](https://docs.affinda.com/resumes/getting-started)** -- Resume parsing product overview and workspace setup.
- **[Integration](https://docs.affinda.com/resumes/integration)** -- Resume parser API integration with code examples.
- **[Credits](https://docs.affinda.com/resumes/credits)** -- Per-document credit system for resume parsing.
- **[Data Extracted](https://docs.affinda.com/resumes/data-extracted)** -- All fields extracted from resumes with sample JSON.
- **[Taxonomies](https://docs.affinda.com/resumes/taxonomies)** -- Skills, job titles, and occupation standardization.
- **[Resume Redactor](https://docs.affinda.com/resumes/resume-redactor)** -- Automated PII redaction for unbiased hiring.
- **[Resume Summary](https://docs.affinda.com/resumes/resume-summary)** -- AI-generated candidate summaries.
- **[Job Description Parser](https://docs.affinda.com/resumes/job-description-parser)** -- Structured extraction from job descriptions.
- **[Search & Match](https://docs.affinda.com/resumes/search-match)** -- Candidate/job matching with scoring and search UI.

### Additional Resources

- **[Error Glossary](https://docs.affinda.com/error-glossary)** -- Error codes and resolutions.
- **[FAQs](https://docs.affinda.com/faqs)** -- Common questions on capabilities, configuration, and troubleshooting.
- **[Billing](https://docs.affinda.com/billing)** -- Credits, pricing, and payment.
- **[Data Retention](https://docs.affinda.com/data-retention)** -- Document deletion and expiry policies.
- **[Deployment & Data Residency](https://docs.affinda.com/deployment-data-residency)** -- Regional servers and enterprise options.
- **[Product Updates](https://docs.affinda.com/updates)** -- Changelog and release notes.
- **[Status](https://status.affinda.com/)** -- Service availability dashboard.
