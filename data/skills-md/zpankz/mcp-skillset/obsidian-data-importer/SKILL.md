---
name: obsidian-data-importer
description: Transform structured external data (CSV/JSON) into Obsidian's linked knowledge system while preserving semantic relationships, optimizing graph structure, and preventing data corruption through systematic validation and YAML-safe template generation.Enables seamless knowledge transfer from databases, spreadsheets, and APIs into personal knowledge management, maintaining referential integrity and facilitating emergence of insights through networked thought.
---

# Obsidian Data Importer

## Activation Conditions

This skill activates when:
- User uploads or provides CSV/JSON data files
- User requests Obsidian import assistance
- User mentions "Handlebars", "JSON/CSV Importer", "bulk import", or "data import"
- User wants to create multiple Obsidian notes from structured data

## Quick Start (3 Steps)

**For immediate use:**

1. **Provide your data** - Upload CSV/JSON file or paste content
2. **Confirm mapping** - Review proposed field assignments
3. **Receive template** - Get complete Handlebars template + instructions

→ **Simple example:** [01-task-list-csv](examples/simple/01-task-list-csv/TUTORIAL.md)

## System Architecture

```
obsidian-data-importer/
├── core/              → Processing engines (5 phases + 4 modules)
├── knowledge/         → Reference documentation (syntax, types, errors)
├── templates/         → Pattern library (8 templates + partials)
└── examples/          → Complete demonstrations (12 workflows)
```

### Component Diagram

```
[Data Input]
    ↓
[DataParser] ──→ [FieldAnalyzer] ──→ [TemplateGenerator] ──→ [Validator]
    ↓                ↓                      ↓                    ↓
 Parsed         Field Inventory        Template String      Validation
  Structure                                                   Report
                                           ↓
                                   [InstructionComposer]
                                           ↓
                                    Complete Package
```

## Workflow Overview

The system executes in 5 sequential phases:

| Phase | Purpose | Documentation | Output |
|-------|---------|---------------|--------|
| 1. **Ingestion** | Parse & analyze data structure | [Phase 1](core/phase-1-ingestion.md) | Field inventory |
| 2. **Strategy** | Map fields & select pattern | [Phase 2](core/phase-2-strategy.md) | Mapping decisions |
| 3. **Construction** | Generate Handlebars template | [Phase 3](core/phase-3-construction.md) | Template string |
| 4. **Validation** | Verify syntax & preview output | [Phase 4](core/phase-4-validation.md) | Validation report |
| 5. **Delivery** | Package with instructions | [Phase 5](core/phase-5-delivery.md) | Complete deliverable |

**Process Flow:**
```
CSV/JSON → Parse → Analyze → Map → Generate → Validate → Deliver
```

## Module Reference

### Core Processing Modules

| Module | Responsibility | Documentation | Key Functions |
|--------|---------------|---------------|---------------|
| **DataParser** | Input format handling | [data-parser.md](core/data-parser.md) | parseCSV(), parseJSON() |
| **FieldAnalyzer** | Type inference & analysis | [field-analyzer.md](core/field-analyzer.md) | inferType(), detectIssues() |
| **TemplateGenerator** | Handlebars construction | [template-generator.md](core/template-generator.md) | buildTemplate(), escapeYAML() |
| **Validator** | Syntax & correctness checking | [validator.md](core/validator.md) | validateYAML(), testRender() |

### Knowledge Base

| Topic | Content | Documentation |
|-------|---------|---------------|
| **YAML Safety** | Character escaping, quoting strategies | [yaml-safety.md](knowledge/yaml-safety.md) |
| **Handlebars Syntax** | Variables, conditionals, iteration | [handlebars-syntax.md](knowledge/handlebars-syntax.md) |
| **Type Mapping** | Detection algorithms, strategies | [type-mapping.md](knowledge/type-mapping.md) |
| **Error Resolution** | Common problems & solutions | [error-resolution.md](knowledge/error-resolution.md) |
| **Best Practices** | Optimization guidelines | [best-practices.md](knowledge/best-practices.md) |

## Template Library

### Base Templates
- **[base-generic.hbs](templates/base-generic.hbs)** - Minimal universal structure
- **[base-full.hbs](templates/base-full.hbs)** - Comprehensive with all features
- **[base-minimal.hbs](templates/base-minimal.hbs)** - Bare essentials only

### Domain-Specific Templates
- **[task-management.hbs](templates/task-management.hbs)** - Tasks, projects, status tracking
- **[reference-material.hbs](templates/reference-material.hbs)** - Books, articles, sources
- **[people-contacts.hbs](templates/people-contacts.hbs)** - Networking, relationships
- **[events-timeline.hbs](templates/events-timeline.hbs)** - Chronological data
- **[inventory-catalog.hbs](templates/inventory-catalog.hbs)** - Items, products, assets

**Template Composition:** All templates use modular partials from [templates/partials/](templates/partials/) for maximum reusability.

## Common Tasks (Quick Recipes)

| Task | Complexity | Example | Duration |
|------|------------|---------|----------|
| Import simple CSV | ⭐ | [01-task-list-csv](examples/simple/01-task-list-csv/) | 3 min |
| Handle special characters | ⭐⭐ | [02-contacts-csv](examples/simple/02-contacts-csv/) | 5 min |
| Process nested JSON | ⭐⭐⭐ | [04-nested-json-projects](examples/intermediate/04-nested-json-projects/) | 10 min |
| Fix YAML errors | ⭐⭐ | [10-special-chars-fix](examples/troubleshooting/10-special-chars-fix/) | 5 min |
| Link entities | ⭐⭐⭐ | [08-complex-relationships](examples/advanced/08-complex-relationships/) | 15 min |

## Examples by Complexity

### Simple (Start Here)
- **[01-task-list-csv](examples/simple/01-task-list-csv/)** - Basic CSV with 5 fields
- **[02-contacts-csv](examples/simple/02-contacts-csv/)** - Special character handling
- **[03-books-json](examples/simple/03-books-json/)** - Simple JSON structure

### Intermediate
- **[04-nested-json-projects](examples/intermediate/04-nested-json-projects/)** - 2-level nesting
- **[05-array-handling](examples/intermediate/05-array-handling/)** - Repeated elements
- **[06-multi-source-merge](examples/intermediate/06-multi-source-merge/)** - Data combination

### Advanced
- **[07-deep-nested-json](examples/advanced/07-deep-nested-json/)** - 3+ level hierarchy
- **[08-complex-relationships](examples/advanced/08-complex-relationships/)** - Entity linking
- **[09-computed-fields](examples/advanced/09-computed-fields/)** - Derived values

### Troubleshooting
- **[10-special-chars-fix](examples/troubleshooting/10-special-chars-fix/)** - YAML safety
- **[11-empty-values](examples/troubleshooting/11-empty-values/)** - Conditional handling
- **[12-type-mismatches](examples/troubleshooting/12-type-mismatches/)** - Type corrections

## Integration & Extensions

### Complementary Obsidian Plugins
- **Templater** - Post-import transformations and computed fields
- **Dataview** - Query and aggregate imported data
- **QuickAdd** - Manual data entry workflows
- **Metadata Menu** - Interactive frontmatter management
- **Tag Wrangler** - Hierarchical tag organization

### Extending This Skill
1. **Add custom templates** - Place in `templates/` with metadata
2. **Create domain patterns** - Model specific industries or use cases
3. **Build preprocessors** - Transform data before import
4. **Develop validators** - Add custom validation rules
5. **Share examples** - Contribute to examples library

### Graph Structure Optimization
- Use `[[Wikilinks]]` for entities that should become nodes
- Create MOCs (Maps of Content) for large imports
- Apply hierarchical tags (e.g., `project/alpha/task-001`)
- Standardize date formats (ISO 8601)
- Preserve source URLs for traceability

## Capabilities & Boundaries

### ✅ What This Skill Does
- Parse CSV and JSON data structures
- Analyze fields with type inference
- Generate YAML-safe Handlebars templates
- Validate syntax and preview output
- Provide complete usage instructions
- Suggest graph optimization strategies

### ❌ What This Skill Does NOT Do
- Perform the actual import (requires user + plugin)
- Modify source data files
- Install or configure the plugin
- Post-process notes after import
- Fix corrupted YAML in existing notes
- Real-time data synchronization

### User Responsibilities
- Install JSON/CSV Importer plugin in Obsidian
- Save generated template to vault
- Execute import through plugin interface
- Review imported notes for accuracy
- Perform any post-import cleanup

## Execution Mode

When data is provided, the system automatically:

1. **Detects format** (CSV vs JSON)
2. **Parses structure** and analyzes fields
3. **Generates field inventory** with recommendations
4. **Proposes template pattern** based on data characteristics
5. **Requests confirmation** of field mappings
6. **Constructs template** with YAML safety
7. **Validates syntax** and generates preview
8. **Delivers package** with instructions

**Response Format:**

```markdown
## 📊 Data Analysis

[Field inventory table with types and recommendations]

## 🎯 Recommended Approach

Pattern: [Selected template]
Note Names: [Field for filenames]
Target Folder: [Suggested location]

## ⚠️ Warnings

[Special character issues, data quality concerns]

## ✨ Template

[Complete Handlebars template with documentation]

## 👁️ Preview

[Sample output from first data row]

## 📋 Instructions

[Step-by-step import procedure]

## 🔧 Troubleshooting

[Common issues and solutions]
```

## Metadata

**Version:** 2.0.0 (Modular Architecture)
**Created:** October 2025
**Compatibility:** Obsidian + JSON/CSV Importer plugin
**Complexity Level:** Intermediate to Advanced
**Skill Type:** Data transformation & template generation

**Prerequisites:**
- Obsidian (any recent version)
- JSON/CSV Importer plugin by "filing 42"
- Basic understanding of YAML frontmatter
- Familiarity with Markdown

**External Resources:**
- [JSON/CSV Importer Plugin](https://github.com/farling42/obsidian-import-json) - Official repository
- [Handlebars.js Guide](https://handlebarsjs.com/guide/) - Template syntax reference
- [YAML Specification](https://yaml.org/spec/) - Format specification
- [Obsidian Forum](https://forum.obsidian.md/) - Community support

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Support & Contribution

**For Issues:**
- Check [examples/troubleshooting/](examples/troubleshooting/) first
- Review [knowledge/error-resolution.md](knowledge/error-resolution.md)
- Consult [knowledge/best-practices.md](knowledge/best-practices.md)

**To Contribute:**
- Add examples to demonstrate new patterns
- Submit custom templates for specific domains
- Report edge cases or issues
- Improve documentation clarity

---

## Reception & Usage

**Skill Activation:** Simply provide your CSV or JSON data, and the system will immediately begin analysis and template generation.

**No explicit invocation required** - the skill recognizes data files and structured content automatically.

**For best results:** Include complete data samples (not fragments) so field analysis can be accurate.

Ready to import your data into Obsidian? Provide your file or paste your data to begin.
