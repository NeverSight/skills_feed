---
name: clinical-trial-schema-designer
description: Analyzes clinical trial protocols and generates CDISC-compliant (SDTM/ADaM) data schemas. Use when designing data ingestion pipelines for clinical research or preparing regulatory submissions.
---
# Clinical Trial Schema Designer

## Purpose and Intent
The `clinical-trial-schema-designer` bridges the gap between clinical research and data engineering. It helps automate the creation of standardized data structures (CDISC) based on clinical protocols, reducing the manual effort required for data ingestion and submission preparation.

## When to Use
- **Study Setup**: Use during the "Start-up" phase of a clinical trial to design the Electronic Data Capture (EDC) schemas.
- **Data Integration**: When merging data from multiple sources into a single study standard.
- **Submission Prep**: To ensure the data structure matches FDA/PMDA requirements for SDTM/ADaM.

## When NOT to Use
- **Unvalidated Systems**: Clinical data must be handled in GxP-validated environments. This tool generates the *design*, but the implementation must follow strict validation protocols.
- **Medical Decision Making**: This is a data structuring tool, not a clinical diagnostic or treatment tool.

## Error Conditions and Edge Cases
- **Ambiguous Protocols**: If the input text is vague about how a variable is measured, the generated schema may be incomplete.
- **Non-Standard Studies**: Phase 1 or highly experimental studies may use variables that don't fit existing CDISC domains perfectly.

## Security and Data-Handling Considerations
- **IP Protection**: Clinical protocols are intellectual property. Ensure the environment running this skill is secure.
- **No Patient Data**: This tool works on *protocols* (the plan), not the actual results (the data).
