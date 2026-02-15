---
name: obsidian-dashboard
description: This skill should be used when users want to generate comprehensive statistics and overview of their Obsidian vault, including file counts, types, tags, links, folder structure, and other metadata analysis.
---

# Obsidian Vault Dashboard Generator

This skill generates comprehensive statistics and visual overview of Obsidian note vaults. It analyzes files, tags, links, folder structure, and creates an interactive HTML dashboard.

## Purpose

To provide detailed insights into Obsidian vault structure and content through automated analysis and visualization.

## When to Use

- When users want to understand their vault structure
- To identify orphaned files, unused attachments, or broken links
- To analyze tag usage patterns and note organization
- To get file statistics and folder distribution
- To visualize vault growth and organization

## How to Use

1. **Run the Analysis Script**
   ```bash
   python3 /Users/cdd/.claude/skills/obsidian-dashboard/scripts/analyze_vault.py <vault_path>
   ```

2. **The script will generate:**
   - `vault_stats.json` - Raw statistics data
   - `dashboard.html` - Interactive HTML dashboard
   - `vault_report.md` - Markdown summary report

3. **Dashboard Features:**
   - File count and type distribution
   - Folder structure visualization
   - Tag usage analysis
   - Link analysis (internal/external/broken)
   - Recent activity tracking
   - Orphaned files detection
   - Attachment usage statistics

## Key Metrics Tracked

- **File Statistics**: Total files, notes, attachments, size distribution
- **Type Analysis**: .md, .pdf, .png, .jpg, .gif, .svg, .mp4, .webm, .mp3, .wav, .m4a
- **Tag Analysis**: Unique tags, tag frequency, nested tag structure
- **Link Analysis**: Internal links, external links, broken links, orphaned files
- **Folder Structure**: Depth, distribution, empty folders
- **Content Analysis**: Empty files, large files, old files
- **Activity Tracking**: Recently modified, created dates

## Output Files

- `dashboard.html`: Interactive dashboard with charts and tables
- `vault_stats.json`: Raw data for further processing
- `vault_report.md`: Markdown summary for vault documentation