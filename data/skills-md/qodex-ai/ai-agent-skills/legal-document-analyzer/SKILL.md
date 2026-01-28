---
name: legal-document-analyzer
description: Build agents for legal document analysis, contract review, and compliance checking. Handles document parsing, risk identification, and legal research. Use when creating contract analysis tools, legal research assistants, compliance checkers, or document review systems.
---

# Legal Document Analyzer

Build intelligent legal document analysis agents that review contracts, identify risks, and provide legal insights.

## Document Parsing

See [examples/legal_document_parser.py](examples/legal_document_parser.py) for `LegalDocumentParser`:
- Parse PDF, DOCX, and text documents
- Extract and structure document content
- Identify sections, clauses, definitions, parties, and dates

## Contract Analysis

See [examples/contract_analyzer.py](examples/contract_analyzer.py) for `ContractAnalyzer`:
- Identify contract type (NDA, employment, service, purchase, lease)
- Extract key terms (dates, renewal, payment, performance metrics)
- Extract obligations, rights, and liabilities

## Risk Identification

See [examples/contract_risk_analyzer.py](examples/contract_risk_analyzer.py) for `ContractRiskAnalyzer`:
- Analyze financial risks (unlimited liability, price escalations)
- Identify legal risks (ambiguous terms, conflicting clauses)
- Assess operational risks
- Check compliance risks (GDPR, data protection)

## Legal Research

Build legal research capabilities to:
- Find applicable laws for contract type and jurisdiction
- Identify regulatory requirements
- Research relevant case law
- Identify standard practices and precedents

## Compliance Checking

Build compliance checking capabilities to:
- Verify contract compliance with regulations
- Identify compliance gaps
- Generate compliance recommendations
- Track required clauses and documentation

## Report Generation

See [examples/legal_report_generator.py](examples/legal_report_generator.py) for `LegalReportGenerator`:
- Generate comprehensive contract analysis reports
- Format key terms and obligations
- Present risk assessments
- Provide actionable recommendations

## Best Practices

### Document Review
- ✓ Review full document systematically
- ✓ Identify all parties and roles
- ✓ Understand key terms and conditions
- ✓ Identify potential risks
- ✓ Check for compliance

### Risk Management
- ✓ Prioritize high-severity risks
- ✓ Negotiate unfavorable terms
- ✓ Seek legal counsel for major issues
- ✓ Document agreed changes
- ✓ Keep signed copies

### Compliance
- ✓ Understand applicable regulations
- ✓ Ensure required clauses present
- ✓ Document compliance measures
- ✓ Review regulatory updates
- ✓ Train team on obligations

## Tools & Resources

### Document Processing
- pypdf
- python-docx
- textract
- OCR libraries

### Legal Research
- LexisNexis
- Westlaw
- Google Scholar
- Free Law Project

## Getting Started

1. Upload contract document
2. Parse document structure
3. Identify contract type
4. Extract key terms and obligations
5. Analyze for risks
6. Check compliance
7. Generate report
8. Provide recommendations

