---
name: documentation-router
description: Routes documentation and explanation tasks. Triggers on document, explain, readme, api-docs, changelog, guide, comment, describe, write-docs.
---

# Documentation Router

Routes documentation, explanation, and writing tasks.

## Subcategories

### Code Documentation
```yaml
triggers: [comment, docstring, jsdoc, type-doc]
skills:
  - sc:document: Focused component documentation
  - sc:explain: Clear explanations
```

### Project Documentation
```yaml
triggers: [readme, guide, setup, installation, contributing]
skills:
  - dev:documentation:create-readme-section: README sections
  - sc:index: Comprehensive documentation
```

### Release Documentation
```yaml
triggers: [changelog, release-notes, version, breaking-changes]
skills:
  - dev:documentation:create-release-note: Release notes
```

### API Documentation
```yaml
triggers: [api-docs, endpoints, swagger, openapi]
skills:
  - sc:document: API documentation
  - sc:design: API design
```

## Routing Decision Tree

```
documentation request
    │
    ├── Code-level?
    │   ├── Comments? → sc:document
    │   └── Explanation → sc:explain
    │
    ├── Project-level?
    │   ├── README? → create-readme-section
    │   └── Full docs → sc:index
    │
    ├── Release?
    │   └── create-release-note
    │
    └── API?
        └── sc:document
```

## Managed Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| sc:document | Component docs | "document", "describe" |
| sc:explain | Explanations | "explain", "clarify" |
| sc:index | Full documentation | "index", "comprehensive" |
| create-readme-section | README | "readme", "setup guide" |
| create-release-note | Release notes | "changelog", "release" |
