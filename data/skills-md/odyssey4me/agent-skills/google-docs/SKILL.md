---
name: google-docs
description: Create and modify Google Docs documents. Read document content and structure, manage formatting, paragraphs, and styles. Use when working with Google Docs document management.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# Google Docs

Interact with Google Docs for document creation, editing, and content management.

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
   ```

2. **Download the skill** from [Releases](https://github.com/odyssey4me/agent-skills/releases) or use directly from this repository.

## Setup Verification

After installation, verify the skill is properly configured:

```bash
python scripts/google-docs.py check
```

This will check:
- Python dependencies (google-auth, google-auth-oauthlib, google-api-python-client, keyring, pyyaml)
- Authentication configuration
- Connectivity to Google Docs API

If anything is missing, the check command will provide setup instructions.

## Authentication

Google Docs uses OAuth 2.0 for authentication. For complete setup instructions, see:

1. [GCP Project Setup Guide](../../docs/gcp-project-setup.md) - Create project, enable Docs API
2. [Google OAuth Setup Guide](../../docs/google-oauth-setup.md) - Configure credentials

### Quick Start

1. Create `~/.config/agent-skills/google.yaml`:
   ```yaml
   oauth_client:
     client_id: your-client-id.apps.googleusercontent.com
     client_secret: your-client-secret
   ```

2. Run `python scripts/google-docs.py check` to trigger OAuth flow and verify setup.

### OAuth Scopes

The skill requests granular scopes for different operations:

| Scope | Permission | Used For |
|-------|-----------|----------|
| `documents.readonly` | Read documents | Reading document content and metadata |
| `documents` | Full access | Creating and modifying documents |

### Scope Errors

If you encounter "insufficient scope" errors, revoke your token and re-authenticate:

1. Revoke at https://myaccount.google.com/permissions
2. Clear token: `keyring del agent-skills google-docs-token-json`
3. Re-run: `python scripts/google-docs.py check`

## Commands

### check

Verify configuration and connectivity.

```bash
python scripts/google-docs.py check
```

This validates:
- Python dependencies are installed
- Authentication is configured
- Can connect to Google Docs API
- Creates a test document to verify write access

### auth setup

Store OAuth 2.0 client credentials for custom OAuth flow.

```bash
python scripts/google-docs.py auth setup \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

Credentials are saved to `~/.config/agent-skills/google-docs.yaml`.

**Options:**
- `--client-id` - OAuth 2.0 client ID (required)
- `--client-secret` - OAuth 2.0 client secret (required)

### documents create

Create a new blank Google Doc.

```bash
python scripts/google-docs.py documents create --title "My Document"
```

**Options:**
- `--title` - Document title (required)
- `--json` - Output as JSON

**Example:**
```bash
# Create a new document
python scripts/google-docs.py documents create --title "Project Notes"

# Output:
# ✓ Document created successfully
#   Title: Project Notes
#   Document ID: 1abc...xyz
#   URL: https://docs.google.com/document/d/1abc...xyz/edit
```

### documents get

Get document metadata and structure.

```bash
python scripts/google-docs.py documents get DOCUMENT_ID
```

**Arguments:**
- `document_id` - The Google Docs document ID

**Options:**
- `--json` - Output full document structure as JSON

**Example:**
```bash
# Get document metadata
python scripts/google-docs.py documents get 1abc...xyz

# Output:
# Title: Project Notes
# Document ID: 1abc...xyz
# Characters: 1234
# Revision ID: abc123
```

### documents read

Read document content as plain text.

```bash
python scripts/google-docs.py documents read DOCUMENT_ID
```

**Arguments:**
- `document_id` - The Google Docs document ID

**Options:**
- `--json` - Output as JSON with content field

**Example:**
```bash
# Read document content
python scripts/google-docs.py documents read 1abc...xyz

# Output: (plain text content of the document)
```

### content append

Append text to the end of a document.

```bash
python scripts/google-docs.py content append DOCUMENT_ID --text "Additional content"
```

**Arguments:**
- `document_id` - The Google Docs document ID

**Options:**
- `--text` - Text to append (required)
- `--json` - Output API response as JSON

**Example:**
```bash
# Append text
python scripts/google-docs.py content append 1abc...xyz --text "Meeting notes from today..."

# Output:
# ✓ Text appended successfully
```

### content insert

Insert text at a specific position in the document.

```bash
python scripts/google-docs.py content insert DOCUMENT_ID --text "Insert this" --index 10
```

**Arguments:**
- `document_id` - The Google Docs document ID

**Options:**
- `--text` - Text to insert (required)
- `--index` - Position to insert at, 0-based (required)
- `--json` - Output API response as JSON

**Example:**
```bash
# Insert text at the beginning (index 1, after title)
python scripts/google-docs.py content insert 1abc...xyz --text "Introduction\n\n" --index 1

# Output:
# ✓ Text inserted successfully
```

**Note:** Index 0 is before the document content. Index 1 is at the beginning of content.

### content delete

Delete a range of content from the document.

```bash
python scripts/google-docs.py content delete DOCUMENT_ID --start-index 10 --end-index 50
```

**Arguments:**
- `document_id` - The Google Docs document ID

**Options:**
- `--start-index` - Start position, inclusive (required)
- `--end-index` - End position, exclusive (required)
- `--json` - Output API response as JSON

**Example:**
```bash
# Delete characters 10-50
python scripts/google-docs.py content delete 1abc...xyz --start-index 10 --end-index 50

# Output:
# ✓ Content deleted successfully
```

**Warning:** Be careful with indices. Deleting the wrong range can corrupt document structure.

### formatting apply

Apply text formatting to a range of text.

```bash
python scripts/google-docs.py formatting apply DOCUMENT_ID \
  --start-index 1 --end-index 20 --bold --italic
```

**Arguments:**
- `document_id` - The Google Docs document ID

**Options:**
- `--start-index` - Start position, inclusive (required)
- `--end-index` - End position, exclusive (required)
- `--bold` - Apply bold formatting
- `--italic` - Apply italic formatting
- `--underline` - Apply underline formatting
- `--font-size SIZE` - Set font size in points
- `--json` - Output API response as JSON

**Example:**
```bash
# Make title bold and larger
python scripts/google-docs.py formatting apply 1abc...xyz \
  --start-index 1 --end-index 20 --bold --font-size 18

# Apply italic to a section
python scripts/google-docs.py formatting apply 1abc...xyz \
  --start-index 50 --end-index 100 --italic

# Output:
# ✓ Formatting applied successfully
```

## Examples

### Create and populate a document

```bash
# Create a new document
DOC_ID=$(python scripts/google-docs.py documents create --title "Weekly Report" --json | jq -r '.documentId')

# Add content
python scripts/google-docs.py content append $DOC_ID --text "Weekly Report\n\n"
python scripts/google-docs.py content append $DOC_ID --text "Summary: This week's accomplishments...\n"

# Format the title
python scripts/google-docs.py formatting apply $DOC_ID --start-index 1 --end-index 14 --bold --font-size 18

# Read it back
python scripts/google-docs.py documents read $DOC_ID
```

### Read and extract content

```bash
# Get document info
python scripts/google-docs.py documents get 1abc...xyz

# Extract plain text
python scripts/google-docs.py documents read 1abc...xyz > document.txt

# Get full JSON structure
python scripts/google-docs.py documents get 1abc...xyz --json > document.json
```

### Edit existing content

```bash
# Insert a new section
python scripts/google-docs.py content insert 1abc...xyz \
  --text "\n\nNew Section\n" --index 100

# Format the new section header
python scripts/google-docs.py formatting apply 1abc...xyz \
  --start-index 102 --end-index 113 --bold

# Append more content
python scripts/google-docs.py content append 1abc...xyz \
  --text "Additional details about the new section..."
```

## Troubleshooting

### "Insufficient scope" errors

You need to revoke and re-authenticate to grant additional permissions:

1. Go to https://myaccount.google.com/permissions
2. Find "Agent Skills" and remove access
3. Delete stored token: `keyring del agent-skills google-docs-token-json`
4. Run `python scripts/google-docs.py check` to re-authenticate

### Cannot find document

Make sure you're using the correct document ID from the URL:
- URL: `https://docs.google.com/document/d/1abc...xyz/edit`
- Document ID: `1abc...xyz`

### Index errors when inserting/deleting

Use `documents get --json` to see the document structure and valid index ranges. Remember:
- Index 0 is before any content
- Index 1 is at the start of document body
- The last index is the document length

### Dependencies not found

Install required dependencies:

```bash
pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
```

### OAuth flow fails

Ensure your GCP project has:
1. Google Docs API enabled (`docs.googleapis.com`)
2. OAuth 2.0 credentials created
3. OAuth consent screen configured
4. Your email added as a test user (if app is in testing mode)

See [docs/gcp-project-setup.md](../../docs/gcp-project-setup.md) for detailed instructions.

## Related Skills

- [Google Drive](../google-drive/SKILL.md) - File management (Drive manages file metadata, Docs manages content)
- [Google Sheets](../google-sheets/SKILL.md) - Spreadsheet management
- [Google Slides](../google-slides/SKILL.md) - Presentation management

## API Reference

For advanced usage, see:
- [Google Docs API Documentation](https://developers.google.com/docs/api)
- [Document structure](https://developers.google.com/docs/api/how-tos/documents)
- [Formatting reference](references/formatting-guide.md)
