---
name: obsidian-generate-vault
description: Generate a complete Obsidian vault structured as a second brain for software engineers. Use when the user asks to create, scaffold, or set up an Obsidian vault, note-taking system, second brain, or personal knowledge management (PKM) workspace. Copies a pre-built vault with numbered folders, templates (Templater syntax), and convention docs — ready to open in Obsidian.
---

# Obsidian Vault Generator

Generate a full Obsidian vault by copying a pre-built assets folder to the user's chosen location. The vault follows a PARA + Zettelkasten hybrid layout with Templater-based templates.

## Step 1 — Ask the user

Before creating anything, confirm:
1. **Vault path** — where to create it (e.g. `~/Documents/WorkVault`).
2. **Vault name** — display name for the Home page heading (defaults to the folder name from the path).

## Step 2 — Copy assets and personalize

1. Resolve the vault path (expand `~` if needed).
2. Create the target directory if it doesn't exist: `mkdir -p <vault-path>`.
3. Copy the entire assets folder contents into the vault path:
   ```
   cp -r <skill-dir>/assets/. <vault-path>/
   ```
   Where `<skill-dir>` is the directory containing this SKILL.md file.
4. Replace the `{{VAULT_NAME}}` placeholder in `Home.md` with the user's vault name:
   ```
   sed -i '' "s/{{VAULT_NAME}}/<vault-name>/g" <vault-path>/Home.md
   ```

## Step 3 — Report

Print a summary including:
- Vault path created
- Number of folders (expect ~12)
- Number of files (expect ~22)
- Number of templates (9)

Then remind the user:
- Open the vault root folder in Obsidian
- Install recommended community plugins: **Templater**, **Dataview**, **Calendar**
- Configure Templater to use `99-System/Templates/` as the template folder location
- The vault does **not** include `.obsidian/` configuration — Obsidian will create defaults on first open
