---
name: invoice-generation
description: Generate professional invoices, receipts, quotes, and financial documents using each::sense AI. Create branded business documents with automatic calculations, multi-currency support, and customizable layouts.
metadata:
  author: eachlabs
  version: "1.0"
---

# Invoice Generation

Generate professional invoices, receipts, quotes, and financial documents using each::sense. This skill creates visually appealing, accurate business documents optimized for printing and digital delivery.

## Features

- **Invoices**: Professional invoices with line items, taxes, and totals
- **Receipts**: Transaction receipts for completed payments
- **Quotes/Estimates**: Pre-sale quotes with validity periods
- **Credit Notes**: Refund and adjustment documents
- **Purchase Orders**: Procurement and ordering documents
- **Multi-Currency**: Support for various currencies and formats
- **Tax Calculations**: Automatic VAT, GST, sales tax handling
- **Company Branding**: Custom logos, colors, and layouts
- **Recurring Templates**: Standardized templates for repeat billing

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional invoice for web development services, $2,500 total, due in 30 days",
    "mode": "max"
  }'
```

## Document Types & Use Cases

| Document Type | Use Case | Key Elements |
|---------------|----------|--------------|
| Invoice | Billing for goods/services | Line items, tax, due date, payment terms |
| Receipt | Payment confirmation | Transaction ID, payment method, timestamp |
| Quote/Estimate | Pre-sale pricing | Validity period, optional items, terms |
| Credit Note | Refunds/adjustments | Reference to original invoice, reason |
| Purchase Order | Procurement | Vendor details, shipping info, approval |
| Proforma Invoice | Pre-shipment | Similar to invoice, marked as proforma |

## Use Case Examples

### 1. Basic Invoice Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a simple invoice: Invoice #INV-2024-001, From: Acme Corp (123 Business St, NY 10001), To: Client Inc (456 Customer Ave, LA 90001), Service: Consulting Services - $1,500. Due date: March 15, 2024. Clean, professional design.",
    "mode": "max"
  }'
```

### 2. Detailed Invoice with Line Items

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a detailed invoice with multiple line items: Invoice #INV-2024-042 From: Digital Solutions LLC To: TechStart Inc Line items: 1) Website Development - 40 hours @ $150/hr = $6,000 2) UI/UX Design - 20 hours @ $125/hr = $2,500 3) SEO Setup - flat rate $800 4) Hosting (Annual) - $480 Subtotal, 8% tax, and grand total. Payment terms: Net 30. Include bank transfer details section.",
    "mode": "max"
  }'
```

### 3. Invoice with Company Branding

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded invoice for a creative agency. Company: Pixel Perfect Studios, use modern minimalist design with a navy blue and gold color scheme. Include space for logo at top left. Invoice #PP-2024-089 to MediaMax Corp. Services: Brand Identity Package $4,500, Social Media Templates $1,200, Brand Guidelines Document $800. Total $6,500. Due in 14 days. Include Pay Now button placeholder and QR code area for payment link.",
    "mode": "max",
    "image_urls": ["https://example.com/company-logo.png"]
  }'
```

### 4. Receipt Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a payment receipt: Receipt #REC-78432 From: Cloud Services Pro To: Johnson Enterprises Payment received: $3,250.00 Payment method: Credit Card (Visa ending 4242) Transaction ID: TXN-2024-02-15-98765 Date: February 15, 2024 at 2:34 PM For: Invoice #INV-2024-038 (Annual SaaS Subscription) Status: PAID in full. Include a thank you message and support contact.",
    "mode": "max"
  }'
```

### 5. Quote/Estimate Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a project quote/estimate: Quote #QT-2024-015 From: BuildRight Construction To: Greenfield Properties Project: Office Renovation - 2nd Floor Line items: 1) Demolition and prep - $8,500 2) Electrical work - $12,000 3) Plumbing updates - $6,500 4) Flooring (800 sq ft) - $9,600 5) Painting and finishing - $4,200 6) Project management (10%) - $4,080 Total estimate: $44,880 Valid for 30 days. Include terms: 50% deposit required, final payment on completion. Add signature line for acceptance.",
    "mode": "max"
  }'
```

### 6. Multi-Currency Invoice

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an international invoice in Euros: Invoice #EU-2024-0023 From: TechGlobal GmbH (Berlin, Germany, VAT: DE123456789) To: Societe Digitale SARL (Paris, France, VAT: FR987654321) Services: Software License (Enterprise) - 12 months @ 850 EUR/month = 10,200 EUR Implementation Services - 3,500 EUR Training (Remote) - 1,800 EUR Subtotal: 15,500 EUR VAT (19%): 2,945 EUR Total: 18,445 EUR Payment: SEPA transfer, IBAN: DE89 3704 0044 0532 0130 00, BIC: COBADEFFXXX Due: 30 days. Reverse charge note for intra-EU B2B.",
    "mode": "max"
  }'
```

### 7. Invoice with Tax Calculations

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an invoice with complex tax breakdown: Invoice #TAX-2024-156 From: Retail Solutions Inc (GST: 12-3456789) To: Shop & Save Stores Line items with different tax rates: 1) POS Hardware (5 units @ $899) = $4,495 - Standard rate 10% GST 2) Software License = $2,400 - Standard rate 10% GST 3) Installation Services = $1,200 - Standard rate 10% GST 4) Training Materials (books) = $350 - Zero rated 5) Extended Warranty = $600 - Exempt Subtotal: $9,045 GST Summary: Standard rated (10%): $8,095 x 10% = $809.50 Zero rated: $350 x 0% = $0 Exempt: $600 Total GST: $809.50 Grand Total: $9,854.50 Include ABN and tax invoice statement.",
    "mode": "max"
  }'
```

### 8. Recurring Invoice Template

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a recurring monthly invoice template: Invoice #[AUTO-NUMBER] From: CloudHost Pro Services To: [CLIENT NAME] Billing Period: [MONTH YEAR] Recurring Services: 1) Dedicated Server Hosting - $299/month 2) Managed Backup Service - $49/month 3) SSL Certificate - $9/month 4) Technical Support (Business) - $149/month Monthly Total: $506 Mark as RECURRING INVOICE. Show billing cycle: Monthly, auto-renews. Next billing date field. Include: Update payment method link, Cancel subscription link. Modern SaaS-style design with clean typography.",
    "mode": "max"
  }'
```

### 9. Credit Note/Refund Document

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a credit note: Credit Note #CN-2024-008 From: Premium Supplies Co To: Office Depot Partners Original Invoice: #INV-2024-892 dated January 10, 2024 Reason for credit: Goods returned - defective items Credit items: 1) Ergonomic Chair Model X (2 units @ $450) = -$900 2) Return shipping covered = -$45 Total Credit: $945.00 Original invoice total: $2,340 Remaining balance due: $1,395 Note: Credit has been applied to your account. Future invoices will reflect this adjustment. Authorized by: [Signature line]. Use red accent color to indicate credit/refund.",
    "mode": "max"
  }'
```

### 10. Purchase Order Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a purchase order: PO #PO-2024-0456 From (Buyer): MegaCorp Industries, 789 Corporate Blvd, Chicago IL 60601, Purchasing Dept Contact: Jane Smith, jane@megacorp.com To (Vendor): Industrial Supplies Ltd, 321 Warehouse Way, Detroit MI 48201 Ship To: MegaCorp Warehouse B, 456 Distribution Dr, Chicago IL 60602 Order Items: 1) Steel Brackets SKU-SB100 - 500 units @ $2.50 = $1,250 2) Mounting Hardware Kit SKU-MH200 - 200 units @ $8.00 = $1,600 3) Safety Cables SKU-SC300 - 1000 units @ $1.25 = $1,250 4) Industrial Adhesive SKU-IA400 - 50 gallons @ $45 = $2,250 Subtotal: $6,350 Shipping: $285 Total: $6,635 Required delivery date: March 1, 2024 Payment terms: Net 45 Special instructions: Deliver to loading dock B, call 30 min before arrival. Include approval signature lines for Requester, Manager, and Purchasing.",
    "mode": "max"
  }'
```

## Multi-Turn Invoice Iteration

Use `session_id` to refine invoices across multiple requests:

```bash
# Initial invoice creation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an invoice for marketing services, $5,000 total from Creative Agency to StartupXYZ",
    "session_id": "invoice-project-001"
  }'

# Add more line items
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Break that down into: Strategy $2,000, Content Creation $1,800, Ad Management $1,200. Add 7% sales tax.",
    "session_id": "invoice-project-001"
  }'

# Update styling
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Update the design to use a green and white color scheme, add payment instructions for Stripe.",
    "session_id": "invoice-project-001"
  }'
```

## Batch Document Generation

Generate multiple related documents:

```bash
# Generate invoice
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create invoice #INV-001 for Project Alpha, $10,000 consulting fee to Acme Corp",
    "session_id": "project-alpha-docs",
    "mode": "eco"
  }'

# Generate matching receipt after payment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching receipt for that invoice, payment received via wire transfer today",
    "session_id": "project-alpha-docs",
    "mode": "eco"
  }'
```

## Best Practices

### Invoice Design
- **Clear hierarchy**: Company info at top, line items in middle, totals prominent
- **Readable fonts**: Use professional, legible typography
- **Adequate spacing**: Avoid cluttered layouts
- **Contact info**: Always include how to reach you for questions

### Required Information
- **Unique invoice number**: Sequential or coded system
- **Issue and due dates**: Clear payment timeline
- **Full business details**: Names, addresses, tax IDs
- **Itemized charges**: Description, quantity, rate, amount
- **Payment instructions**: Bank details, accepted methods

### Legal Compliance
- Include tax registration numbers where required
- Use correct tax rates for jurisdiction
- Mark documents appropriately (Invoice, Quote, Proforma)
- Include required legal disclaimers

## Prompt Tips for Financial Documents

When generating invoices and financial documents, include:

1. **Document type**: Invoice, receipt, quote, credit note, PO
2. **Parties**: Full details for sender and recipient
3. **Items/Services**: Descriptions, quantities, rates
4. **Calculations**: Tax rates, discounts, totals
5. **Terms**: Payment due date, validity period
6. **Branding**: Colors, style preferences, logo
7. **Additional fields**: PO numbers, project references, notes

### Example Prompt Structure

```
"Create a [document type] #[number]
From: [company name and details]
To: [client name and details]
Items: [list with quantities and prices]
Tax: [rate and type]
Terms: [payment terms]
Style: [design preferences]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final client-facing invoices, branded documents | Slower | Highest |
| `eco` | Draft invoices, internal documents, bulk generation | Faster | Good |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `document-generation` - General document creation
- `business-card-generation` - Business card design
- `letterhead-generation` - Company letterhead design
