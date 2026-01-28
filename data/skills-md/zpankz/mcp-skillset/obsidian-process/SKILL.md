---
name: obsidian-process
description: This skill should be used when batch processing Obsidian markdown vaults. Handles wikilink extraction, tag normalization, frontmatter CRUD operations, and vault analysis. Use for vault-wide transformations, link auditing, tag standardization, metadata management, and migration workflows. Integrates with obsidian-markdown for syntax validation and obsidian-data-importer for structured imports.
---

# Obsidian Process

Modular Python batch processing toolkit for Obsidian vault operations with dry-run support, backup/rollback capabilities, and comprehensive reporting.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BatchProcessor (Base)                     │
│  - find_markdown_files()  - read_file()  - write_file()    │
│  - VaultContext (rollback)  - ProcessingResult (output)     │
└──────────────────────────┬──────────────────────────────────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
     ▼                     ▼                     ▼
┌──────────┐        ┌──────────┐         ┌──────────────┐
│ Wikilink │        │   Tag    │         │ Frontmatter  │
│Extractor │        │Normalizer│         │  Processor   │
└──────────┘        └──────────┘         └──────────────┘
```

## Quick Start

### Extract All Wikilinks

```bash
python scripts/wikilink_extractor.py --vault /path/to/vault --output links.json
```

### Normalize Tags

```bash
python scripts/tag_normalizer.py --vault /path/to/vault --case lower --dry-run
```

### Process Frontmatter

```bash
python scripts/frontmatter_processor.py --vault /path/to/vault --operation add --key status --value draft
```

## Modules

### 1. BatchProcessor (base class)

All processors inherit from `BatchProcessor`:

```python
from batch_processor import BatchProcessor, ProcessingResult, VaultContext

class MyProcessor(BatchProcessor):
    def process(self) -> ProcessingResult:
        with VaultContext(self) as ctx:
            for file in self.find_markdown_files():
                content = self.read_file(file)
                # Transform content
                self.write_file(file, new_content)
        return ProcessingResult(success=True, files_processed=n, ...)
```

**Key Features**:
- `--dry-run`: Preview changes without modifying files
- `--verbose`: Detailed logging output
- Automatic backup before modifications
- Rollback on errors via `VaultContext`

### 2. WikilinkExtractor

Extracts and analyzes all wikilink formats:

| Format | Example | Captured Fields |
|--------|---------|-----------------|
| Basic | `[[Note]]` | target |
| Alias | `[[Note\|Display]]` | target, display_text |
| Header | `[[Note#Section]]` | target, header |
| Block | `[[Note^abc123]]` | target, block_id |
| Embed | `![[Image.png]]` | target, is_embedded |

**Output**: JSON with `link_index`, `backlink_index`, `statistics`

```bash
# Build link graph
python scripts/wikilink_extractor.py --vault ./vault --output graph.json

# Find broken links
python scripts/wikilink_extractor.py --vault ./vault --find-broken
```

### 3. TagNormalizer

Handles both inline (`#tag`) and frontmatter tags:

**Operations**:
- Case normalization: `lower`, `upper`, `title`
- Pattern-based rules via JSON config
- Hierarchy parsing: `#project/active/urgent` → 3 levels

```bash
# Normalize all tags to lowercase
python scripts/tag_normalizer.py --vault ./vault --case lower

# Apply custom rules
python scripts/tag_normalizer.py --vault ./vault --rules rules.json
```

**Rules JSON Format**:
```json
{
  "rules": [
    {"pattern": "^todo$", "replacement": "task", "case_sensitive": false},
    {"pattern": "^WIP$", "replacement": "in-progress"}
  ]
}
```

### 4. FrontmatterProcessor

Full YAML frontmatter CRUD with templates and validators:

**Operations**:
- `add`: Add/update field (merges with existing)
- `remove`: Delete field from frontmatter
- `update`: Same as add (explicit intent)
- `validate`: Check against registered validators
- `template`: Apply predefined templates

```bash
# Add created date to all files
python scripts/frontmatter_processor.py --vault ./vault \
  --operation add --key created --value "2024-01-01"

# Apply article template
python scripts/frontmatter_processor.py --vault ./vault \
  --operation template --template article

# Validate all frontmatter
python scripts/frontmatter_processor.py --vault ./vault --operation validate
```

**Built-in Templates**:
- `basic`: created, tags, aliases
- `article`: created, modified, tags, aliases, author, published, draft
- `meeting`: created, tags, attendees, date, location

## Integration Patterns

### With obsidian-markdown Skill

Use obsidian-process for batch operations, then validate with obsidian-markdown:

```
1. obsidian-process: Normalize tags vault-wide
2. obsidian-markdown: Validate Obsidian syntax compliance
3. obsidian-process: Generate validation report
```

### With obsidian-data-importer Skill

Process imported data after ingestion:

```
1. obsidian-data-importer: Convert CSV/JSON to markdown
2. obsidian-process: Apply frontmatter templates
3. obsidian-process: Build wikilink index
4. obsidian-markdown: Validate final output
```

## Common Workflows

### Vault Health Check

```bash
# 1. Extract all wikilinks
python scripts/wikilink_extractor.py --vault ./vault --output links.json

# 2. Identify orphaned notes (no incoming links)
python scripts/wikilink_extractor.py --vault ./vault --find-orphans

# 3. Validate frontmatter
python scripts/frontmatter_processor.py --vault ./vault --operation validate
```

### Tag Migration

```bash
# 1. Preview changes with dry-run
python scripts/tag_normalizer.py --vault ./vault --case lower --dry-run

# 2. Apply normalization
python scripts/tag_normalizer.py --vault ./vault --case lower

# 3. Report statistics
python scripts/tag_normalizer.py --vault ./vault --stats-only
```

### Frontmatter Standardization

```bash
# 1. Apply template to all notes
python scripts/frontmatter_processor.py --vault ./vault \
  --operation template --template basic --dry-run

# 2. Add custom fields
python scripts/frontmatter_processor.py --vault ./vault \
  --operation add --key project --value "[[Projects/Main]]"
```

## ProcessingResult Schema

All processors return standardized results:

```python
@dataclass
class ProcessingResult:
    success: bool
    files_processed: int
    files_modified: int
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]  # Operation-specific data
    timestamp: str
```

## Safety Features

| Feature | Description |
|---------|-------------|
| `--dry-run` | Preview all changes without writing |
| Backup | Automatic `.bak` files before modification |
| Rollback | `VaultContext` reverts on exceptions |
| Logging | Timestamped operation logs |
| Validation | Pre-write content validation |

## Extension Guide

To add a new processor:

```python
from batch_processor import BatchProcessor, ProcessingResult

class MyProcessor(BatchProcessor):
    def __init__(self, vault_path, dry_run=False, verbose=False):
        super().__init__(vault_path, dry_run, verbose)
        # Custom initialization

    def process_file(self, file_path: Path) -> bool:
        content = self.read_file(file_path)
        # Transform content
        return self.write_file(file_path, new_content)

    def process(self) -> ProcessingResult:
        for file in self.find_markdown_files():
            self.process_file(file)
        return ProcessingResult(success=True, ...)
```

## CLI Reference

All scripts share common arguments:

```
--vault PATH      Path to Obsidian vault (required)
--dry-run         Preview changes without modifying
--verbose, -v     Enable detailed logging
--output PATH     Output file for results (JSON)
```

### wikilink_extractor.py

```
--find-broken     Report links to non-existent notes
--find-orphans    Report notes with no incoming links
--stats-only      Output statistics without full index
```

### tag_normalizer.py

```
--case {lower,upper,title}  Case normalization mode
--rules PATH                JSON file with transformation rules
--stats-only                Output tag statistics only
```

### frontmatter_processor.py

```
--operation {add,remove,update,validate,template}
--key KEY         Frontmatter key for add/remove/update
--value VALUE     Value to set (supports JSON arrays/objects)
--template NAME   Template name for template operation
```

## LSP Integration

**When to use**: Semantic analysis requiring graph-awareness—backlink chains, cross-vault renaming, broken link detection with context.

**Setup**:
```bash
export ENABLE_LSP_TOOL=1
# Requires: markdown-oxide in PATH (cargo install markdown-oxide)
```

**Core Capabilities** (via `scripts/lsp_integration.py`):

| Operation | Purpose |
|-----------|---------|
| `findReferences` | Find all backlinks to a note |
| `goToDefinition` | Resolve wikilink targets |
| `workspaceSymbol` | Search vault for tags/headings |
| `diagnostics` | Detect broken links |
| `rename` | Cross-vault symbol renaming |

**Key Classes**:
- `LSPClient`: Low-level LSP protocol wrapper
- `MarkdownOxideIntegration`: High-level Obsidian operations
- `RecursiveLSP`: Graph traversal (backlink chains, orphan detection, strongly connected components)
- `VaultLSPAnalyzer`: Extends BatchProcessor with LSP-powered vault analysis

**CLI Quick Reference**:
```bash
# Analyze entire vault
python scripts/lsp_integration.py analyze-vault --vault ~/vault --output analysis.json

# Find recursive backlinks
python scripts/lsp_integration.py recursive-backlinks --vault ~/vault --file note.md --depth 3
```

**Detailed Documentation**: See `references/lsp-patterns.md` for:
- Complete LSP method reference
- Recursive query patterns (backlink chains, reference graphs, transitive closure)
- Batch processing strategies with caching
- Integration patterns with WikilinkExtractor, TagNormalizer, VaultAnalyzer
- Performance optimization and troubleshooting
