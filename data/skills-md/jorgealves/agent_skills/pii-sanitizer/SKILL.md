---
name: pii-sanitizer
description: Detects and redacts Personally Identifiable Information (PII) like emails, phone numbers, and credit cards. Use when cleaning logs, datasets, or communications to comply with GDPR/CCPA privacy standards.
---
# PII Sanitizer

## Purpose and Intent
The `pii-sanitizer` is a data protection tool designed to identify and mask Personally Identifiable Information (PII) from datasets, logs, or communications to comply with privacy regulations like GDPR and CCPA.

## When to Use
- **Log Scrubbing**: Clean application logs before sending them to centralized logging platforms (e.g., ELK, Datadog).
- **Dataset Preparation**: Sanitize production data before using it in staging or training environments.
- **Customer Support**: Mask sensitive info in support tickets before sharing them with engineering teams.

## When NOT to Use
- **Encryption**: This is a redaction tool, not an encryption tool. It is for removing data, not securing it for later retrieval.
- **Structured Database Migration**: While it handles some structure, specialized ETL tools are better for massive DB sanitization.

## Error Conditions and Edge Cases
- **False Positives**: Strings that resemble PII (like internal serial numbers) might be accidentally redacted.
- **Ambiguous Context**: "Rose" could be a name (PII) or a flower; the tool may err on the side of caution.
- **Encoding Issues**: Ensure input text is UTF-8 to avoid detection failures on special characters.

## Security and Data-Handling Considerations
- **Zero Retention**: Input data must never be saved to disk.
- **Local Processing**: Highly recommended to run this within a secure perimeter so sensitive raw data never leaves the local environment.
