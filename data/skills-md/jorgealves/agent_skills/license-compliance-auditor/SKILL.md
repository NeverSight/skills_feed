---
name: license-compliance-auditor
description: Scans project dependencies and verifies licenses against a whitelist of approved open-source licenses. Use to ensure legal compliance in software projects and prevent the introduction of restricted licenses.
---
# License Compliance Auditor

## Purpose and Intent
The `license-compliance-auditor` ensures that software projects remain legally compliant by automatically verifying that all direct and transitive dependencies use licenses approved by the organization.

## When to Use
- **Dependency Onboarding**: Run when adding a new library to a project.
- **CI/CD Gates**: Use as a blocking step in pipelines to prevent merging code with non-compliant licenses (e.g., preventing GPL in a proprietary product).
- **Release Preparation**: Audit the entire dependency tree before a major release.

## When NOT to Use
- **Legal Advice**: This tool provides technical checks based on metadata; it does not replace professional legal counsel.
- **Custom Licenses**: It may struggle with proprietary or highly customized license text not found in SPDX registries.

## Error Conditions and Edge Cases
- **Missing Metadata**: If a package doesn't define a license in its manifest, it will be flagged as "Unknown".
- **Dual Licensing**: Packages with multiple licenses (e.g., "MIT OR GPL") will require manual review.
- **Unsupported Ecosystems**: Attempting to run on a language not supported by the `ecosystem` input will fail.

## Security and Data-Handling Considerations
- **ReadOnly**: The tool only reads manifest files.
- **Privacy**: No source code is uploaded; only package names and versions are used to check license registries.
