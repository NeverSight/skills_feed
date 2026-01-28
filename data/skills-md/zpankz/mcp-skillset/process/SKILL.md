---
name: process
description: "Batch processing for Obsidian vaults: bulk tag normalization, wikilink extraction/fixing, frontmatter edits, vault analysis, and migration workflows. Use when asked to analyze or modify many notes in an Obsidian vault at scale, or to script/automate vault-wide changes."
---

# Obsidian Batch Processing Skill

Use this skill to perform repeatable, vault-wide operations on Obsidian markdown files.
Keep this file lean and route to the correct reference or script instead of duplicating detail.

## Routing Map (read only what you need)

- `references/quickstart.md` - Setup plus a 5-minute tutorial. Use for first run or quick orientation.
- `references/cli-usage.md` - Full CLI reference. Use for exact flags, subcommands, and examples.
- `references/obsidian-syntax.md` - Obsidian markdown syntax, regex patterns, and edge cases. Use when parsing or transforming content.
- `references/processing-patterns.md` - Advanced workflows, migrations, QA, rollback strategies. Use for multi-step or high-risk operations.
- `examples/use-case-1-migrate-flat-to-hierarchical.md` - Large-scale migration example.
- `examples/use-case-2-fix-broken-links.md` - Broken link repair example.
- `examples/use-case-3-normalize-tags.md` - Tag normalization example.
- `examples/use-case-4-vault-statistics-report.md` - Analytics/reporting example.

## Script Index (entry points)

- `scripts/batch_processor.py` - Main CLI entry point and command routing.
- `scripts/wikilink_extractor.py` - Extract and analyze wikilinks.
- `scripts/tag_normalizer.py` - Normalize tags across a vault.
- `scripts/frontmatter_processor.py` - Bulk frontmatter operations.
- `scripts/vault_analyzer.py` - Vault statistics and health reports.

## Standard Workflow

1. Back up the vault.
2. Run a dry run when available.
3. Execute the operation.
4. Verify results with a report or spot checks.

## How to Use This Skill

- Pick the smallest reference file that answers the question.
- Summarize only what is needed, then point to the exact script or command.
- If the user asks for edits or new behavior, modify the relevant script and keep the CLI consistent with `references/cli-usage.md`.
