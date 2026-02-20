---
name: open-agreements
description: >-
  Fill standard legal agreement templates (NDAs, cloud service agreements, SAFEs)
  and produce signable DOCX files. Supports Common Paper, Bonterms, and
  Y Combinator templates. Use when the user needs to draft a legal agreement,
  create an NDA, fill a contract template, or generate a SAFE.
  DOCX generation requires Node.js >=20.
license: MIT
compatibility: Requires Node.js >=20 for DOCX rendering.
metadata:
  author: open-agreements
  version: "0.1.0"
---

# open-agreements

Fill standard legal agreement templates and produce signable DOCX files.

## Activation

Use this skill when the user wants to:
- Draft an NDA, confidentiality agreement, or cloud service agreement
- Generate a SAFE (Simple Agreement for Future Equity) for a startup investment
- Fill a legal template with their company details
- Generate a signable DOCX from a standard form

## Execution

### Step 1: Detect runtime

Determine which execution path to use:

```bash
if command -v open-agreements >/dev/null 2>&1; then
  echo "GLOBAL"
elif command -v node >/dev/null 2>&1; then
  echo "NPX"
else
  echo "PREVIEW_ONLY"
fi
```

- **GLOBAL**: The CLI is installed. Use `open-agreements` directly.
- **NPX**: Node.js is available. Use `npx -y open-agreements@latest` as the command prefix.
- **PREVIEW_ONLY**: No Node.js. Skip to Step 5 (preview fallback).

### Step 2: Discover templates

Run the list command with `--json` to get available templates and their fields:

**If GLOBAL:**
```bash
open-agreements list --json
```

**If NPX:**
```bash
npx -y open-agreements@latest list --json
```

The output is a JSON envelope. Parse the response and verify `schema_version` is `1`. Use the `items` array for template discovery.

```json
{
  "schema_version": 1,
  "cli_version": "0.1.0",
  "items": [...]
}
```

Each item in the `items` array has:
- `name`: template identifier (use this in the fill command)
- `description`: what the template is for
- `license`: SPDX license identifier (e.g. `CC-BY-4.0`, `CC-BY-ND-4.0`)
- `source_url`: URL to the original template source
- `source`: human-friendly source name (e.g. "Common Paper", "Y Combinator")
- `attribution_text`: required attribution text
- `fields`: array of field definitions with `name`, `type`, `required`, `section`, `description`, `default`

The `license` field tells you what you can do with the filled output:
- `CC-BY-4.0`: derivatives allowed, can redistribute with attribution
- `CC-BY-ND-4.0`: fill for your own use, do not redistribute modified versions

### Step 3: Help user choose a template

Present the available templates to the user. If they asked for a specific type (e.g., "NDA" or "SAFE"), filter to matching items. Ask the user to confirm which template to use.

If the selected template has a `CC-BY-ND` license, note that the CLI will print a license notice when filling. No extra steps are needed — all templates work the same from the user's perspective.

### Step 4: Interview user for field values

Group fields by `section`. Ask the user for values in rounds of up to 4 questions each. For each field, show:
- The field description
- Whether it's required
- The default value (if any)

Write the collected values to a temporary JSON file:

```bash
cat > /tmp/oa-values.json << 'FIELDS'
{
  "party_1_name": "Acme Corp",
  "party_1_email": "legal@acme.com",
  "party_2_name": "Beta Inc",
  "party_2_email": "legal@beta.com",
  "effective_date": "February 1, 2026",
  "purpose": "Evaluating a potential business partnership",
  "mnda_term": "2 years",
  "confidentiality_term": "2 years",
  "governing_law": "Delaware",
  "jurisdiction": "courts located in New Castle County, Delaware"
}
FIELDS
```

### Step 5: Render DOCX

**If GLOBAL:**
```bash
open-agreements fill <template-name> -d /tmp/oa-values.json -o <output-name>.docx
```

**If NPX:**
```bash
npx -y open-agreements@latest fill <template-name> -d /tmp/oa-values.json -o <output-name>.docx
```

**If PREVIEW_ONLY (no Node.js):**

Generate a markdown preview using the collected values. Label clearly:

```markdown
# PREVIEW ONLY -- install Node.js >=20 for signable DOCX output

## Mutual Non-Disclosure Agreement

Between **Acme Corp** and **Beta Inc**

Effective Date: February 1, 2026

...
```

Tell the user: "I've generated a preview. To produce a signable DOCX file, install Node.js 20+ and run this skill again."

### Step 6: Confirm output

Report the output file path to the user. Remind them to review the document before signing.

Clean up the temporary values file:
```bash
rm /tmp/oa-values.json
```

## Templates Available

Templates are discovered dynamically -- always run `list --json` for the current inventory.
Do NOT rely on a hardcoded list. The output of `list --json` is the single source of truth.

## Notes

- All templates produce Word DOCX files that preserve original formatting
- Templates are licensed by their respective authors (CC BY 4.0, CC0, or CC BY-ND 4.0)
- External templates (CC BY-ND 4.0, e.g. YC SAFEs) can be filled for your own use but must not be redistributed in modified form
- This tool does not provide legal advice -- consult an attorney
