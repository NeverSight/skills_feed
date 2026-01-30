---
name: q-methods
description: Draft methods sections for academic manuscripts following a structured, narrative style. Use when the user needs to write or refine a methods section for research papers involving computational methods (machine learning, statistical modeling, text analysis, simulation, network analysis, image processing, or other computational approaches). Produces clear, accessible prose without em-dashes or bullet points, with appropriate appendix cross-references for technical details.
---

# Methods Section Drafting

This skill guides drafting of methods sections for academic manuscripts in a clear, narrative style suitable for broad scholarly audiences.

## Core Principles

1. Write in flowing paragraphs without bullet points or em-dashes unless absolutely necessary
2. Keep technical jargon minimal in main text; reference appendix for implementation details
3. Organize by logical workflow stages (data collection, preprocessing, analysis, validation)
4. Include placeholders for coauthor contributions where information is missing
5. Balance conciseness with sufficient detail for replication understanding

## Standard Structure

### Data Collection and Preprocessing
- Describe sampling, recruitment, data sources (or mark as placeholder for coauthor)
- Describe preprocessing at conceptual level without code-specific language
- Reference appendix for technical parameters and library specifications

### Data Analysis
- Provide brief pipeline overview establishing the analytical approach
- Organize by analytical stages (e.g., topic modeling, classification, validation)
- For each stage: justify method choice, describe key parameters conceptually, reference appendix for details

### Validation
- Describe human validation sampling strategy
- Leave placeholders for reliability metrics if not yet available

## Writing Style Guidelines

Avoid phrases like "importing Python libraries" or "using pandas for data manipulation." Instead write conceptually: "Interview responses were organized by dimension" rather than "We filtered the DataFrame by question type."

Use hyphens (-) for compound modifiers. Never use em-dashes. Write numbers under ten as words unless in technical context.

When referencing appendix sections, use format: "Detailed parameters are provided in Appendix A" or "The complete system prompt is documented in Appendix E."

## Reference Files

For detailed examples and templates:
- See references/methods_template.md for the complete template structure
- See references/appendix_template.md for companion appendix structure
