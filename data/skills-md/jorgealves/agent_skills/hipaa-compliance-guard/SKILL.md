---
name: hipaa-compliance-guard
description: Audits HealthTech applications for HIPAA technical safeguards like encryption and audit logging. Use when reviewing healthcare infrastructure or ensuring PHI is handled according to legal security standards.
---
# HIPAA Compliance Guard

## Purpose and Intent
The `hipaa-compliance-guard` is a specialized auditing tool for the healthcare industry. Its goal is to provide a technical assessment of how well an application adheres to the HIPAA Security Rule, specifically focusing on the protection of Electronic Protected Health Information (ePHI).

## When to Use
- **Architecture Reviews**: Run during the design phase to ensure encryption and logging are planned.
- **Pre-Audit Self-Assessment**: Use before a formal 3rd-party HIPAA audit to identify and fix low-hanging violations.
- **Infrastructure Changes**: Run after modifying Terraform or Cloud scripts to ensure security groups or encryption haven't been compromised.

## When NOT to Use
- **Real Patient Data**: This tool should NOT be used on live databases containing PHI. It is for checking the *systems* that handle the data.
- **Legal Certification**: Passing this audit does not mean you are "HIPAA Certified"; it means your technical configuration follows best practices.

## Error Conditions and Edge Cases
- **Obfuscated Infrastructure**: If cloud resources are created via manual console actions (ClickOps) instead of code, this tool cannot see them.
- **Custom Encryption**: Proprietary or non-standard encryption methods may be flagged as warnings.

## Security and Data-Handling Considerations
- **No PHI Access**: The tool is designed to look at configurations, not data.
- **Local Analysis**: Keep your infrastructure code local and run the scan within your trusted environment.
