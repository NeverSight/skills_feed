---
name: doc-sync
description: Check documentation consistency across README, man page, and help screen
---

# Documentation Sync Check

Compare documentation sources for consistency across keybindings and feature documentation.

## Instructions

1. **Read README keybindings section**: Use the Read tool to read `README.md`, then locate the `## Key` section (keybindings table)

2. **Read man page keybindings**: Use the Read tool to read `lazyworktree.1`, then locate the `KEYBINDINGS` section

3. **Read help screen text**: Use the Read tool to read `internal/app/screen/help.go`, then locate the `helpText` variable containing the in-app help content

## Analysis Required

Compare these three sources and identify:
1. Missing keybindings in any source
2. Inconsistent descriptions between sources
3. Outdated or incorrect information
4. British spelling violations
5. Specific recommendations to bring all sources into sync

Report findings with file paths and line numbers for any discrepancies found.
