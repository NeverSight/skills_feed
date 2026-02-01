---
name: documentation-generator
description: Analyzes source code to automatically generate technical documentation and architecture diagrams. Use to maintain up-to-date API references and onboarding materials for engineering teams.
---
# Documentation Generator

## Purpose and Intent
The `documentation-generator` ensures that software projects remain maintainable by automatically creating and updating technical documentation directly from the source code.

## When to Use
- **Post-Development**: Run after a feature is completed to ensure the API docs are up to date.
- **Onboarding**: Use to generate architecture diagrams and overviews for new team members.

## When NOT to Use
- **High-Level Strategy**: This tool generates technical docs; it cannot write "Business Requirements" or "Product Vision" documents.

## Security and Data-Handling Considerations
- Operates locally; does not upload source code to external servers.
