---
name: google-drive
description: Manage Google Drive files and folders. List, search, upload, download files, create folders, and manage sharing. Use when working with Google Drive file management.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# Google Drive

Interact with Google Drive for file management, search, and sharing.

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
   ```

2. **Download the skill** from [Releases](https://github.com/odyssey4me/agent-skills/releases) or use directly from this repository.

## Setup Verification

After installation, verify the skill is properly configured:

```bash
python scripts/google-drive.py check
```

This will check:
- Python dependencies (google-auth, google-auth-oauthlib, google-api-python-client, keyring, pyyaml)
- Authentication configuration
- Connectivity to Google Drive API

If anything is missing, the check command will provide setup instructions.

## Authentication

Google Drive uses OAuth 2.0 for authentication. For complete setup instructions, see:

1. [GCP Project Setup Guide](../../docs/gcp-project-setup.md) - Create project, enable Drive API
2. [Google OAuth Setup Guide](../../docs/google-oauth-setup.md) - Configure credentials

### Quick Start

1. Create `~/.config/agent-skills/google.yaml`:
   ```yaml
   oauth_client:
     client_id: your-client-id.apps.googleusercontent.com
     client_secret: your-client-secret
   ```

2. Run `python scripts/google-drive.py check` to trigger OAuth flow and verify setup.

### OAuth Scopes

The skill requests granular scopes for different operations:

| Scope | Permission | Used For |
|-------|-----------|----------|
| `drive.readonly` | Read files and metadata | list, search, download |
| `drive.file` | Create/edit files created by app | upload, create folders, share |
| `drive.metadata.readonly` | View file metadata only | get file info |

### Scope Errors

If you encounter "insufficient scope" errors, revoke your token and re-authenticate:

1. Revoke at https://myaccount.google.com/permissions
2. Clear token: `keyring del agent-skills google-drive-token-json`
3. Re-run: `python scripts/google-drive.py check`

## Commands

### check

Verify configuration and connectivity.

```bash
python scripts/google-drive.py check
```

This validates:
- Python dependencies are installed
- Authentication is configured
- Can connect to Google Drive API
- Displays your email address and storage usage

### auth setup

Store OAuth 2.0 client credentials for custom OAuth flow.

```bash
python scripts/google-drive.py auth setup \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

Credentials are saved to `~/.config/agent-skills/google-drive.yaml`.

### files list

List files in your Drive.

```bash
# List recent files
python scripts/google-drive.py files list

# List with search query
python scripts/google-drive.py files list --query "name contains 'report'"

# List with max results
python scripts/google-drive.py files list --max-results 20

# List sorted by name
python scripts/google-drive.py files list --order-by "name"

# Output as JSON
python scripts/google-drive.py files list --json
```

**Arguments:**
- `--query`: Drive search query (optional)
- `--max-results`: Maximum number of results (default: 10)
- `--order-by`: Sort order (default: "modifiedTime desc")
- `--json`: Output as JSON

### files search

Search for files with filters.

```bash
# Search by name
python scripts/google-drive.py files search --name "quarterly report"

# Search by MIME type
python scripts/google-drive.py files search --mime-type "application/pdf"

# Search in a specific folder
python scripts/google-drive.py files search --folder FOLDER_ID

# Combine filters
python scripts/google-drive.py files search --name "budget" --mime-type "application/vnd.google-apps.spreadsheet"

# Output as JSON
python scripts/google-drive.py files search --name "report" --json
```

**Arguments:**
- `--name`: File name to search for (partial match)
- `--mime-type`: MIME type filter
- `--folder`: Parent folder ID
- `--json`: Output as JSON

### files get

Get file metadata by ID.

```bash
# Get file details
python scripts/google-drive.py files get FILE_ID

# Output as JSON
python scripts/google-drive.py files get FILE_ID --json
```

**Arguments:**
- `file_id`: The file ID (required)
- `--json`: Output as JSON

### files download

Download a file from Google Drive.

```bash
# Download a file
python scripts/google-drive.py files download FILE_ID --output /path/to/local/file

# Short form
python scripts/google-drive.py files download FILE_ID -o ./downloaded-file.pdf
```

**Arguments:**
- `file_id`: The file ID (required)
- `--output`, `-o`: Output file path (required)

**Note:** Google Docs, Sheets, and Slides cannot be downloaded directly. Use the Google Drive web interface to export them.

### files upload

Upload a file to Google Drive.

```bash
# Upload a file
python scripts/google-drive.py files upload /path/to/file.pdf

# Upload to a specific folder
python scripts/google-drive.py files upload /path/to/file.pdf --parent FOLDER_ID

# Upload with custom name
python scripts/google-drive.py files upload /path/to/file.pdf --name "Quarterly Report 2024"

# Upload with specific MIME type
python scripts/google-drive.py files upload /path/to/file --mime-type "text/csv"

# Output as JSON
python scripts/google-drive.py files upload /path/to/file.pdf --json
```

**Arguments:**
- `path`: Local file path (required)
- `--parent`: Parent folder ID
- `--mime-type`: MIME type (auto-detected if not provided)
- `--name`: Name for the file in Drive
- `--json`: Output as JSON

### folders create

Create a new folder.

```bash
# Create folder in root
python scripts/google-drive.py folders create "New Folder"

# Create folder inside another folder
python scripts/google-drive.py folders create "Subfolder" --parent FOLDER_ID

# Output as JSON
python scripts/google-drive.py folders create "Documents" --json
```

**Arguments:**
- `name`: Folder name (required)
- `--parent`: Parent folder ID
- `--json`: Output as JSON

### folders list

List contents of a folder.

```bash
# List folder contents
python scripts/google-drive.py folders list FOLDER_ID

# List with max results
python scripts/google-drive.py folders list FOLDER_ID --max-results 50

# Output as JSON
python scripts/google-drive.py folders list FOLDER_ID --json
```

**Arguments:**
- `folder_id`: The folder ID (required)
- `--max-results`: Maximum number of results (default: 100)
- `--json`: Output as JSON

### share

Share a file with a user.

```bash
# Share as reader (default)
python scripts/google-drive.py share FILE_ID --email user@example.com

# Share as writer
python scripts/google-drive.py share FILE_ID --email user@example.com --role writer

# Share as commenter
python scripts/google-drive.py share FILE_ID --email user@example.com --role commenter

# Share without sending notification
python scripts/google-drive.py share FILE_ID --email user@example.com --no-notify

# Output as JSON
python scripts/google-drive.py share FILE_ID --email user@example.com --json
```

**Arguments:**
- `file_id`: File ID to share (required)
- `--email`: Email address to share with (required)
- `--role`: Permission role - reader, writer, commenter, owner (default: reader)
- `--no-notify`: Don't send notification email
- `--json`: Output as JSON

### permissions list

List permissions for a file.

```bash
# List permissions
python scripts/google-drive.py permissions list FILE_ID

# Output as JSON
python scripts/google-drive.py permissions list FILE_ID --json
```

**Arguments:**
- `file_id`: The file ID (required)
- `--json`: Output as JSON

### permissions delete

Remove a permission from a file.

```bash
# Delete a permission
python scripts/google-drive.py permissions delete FILE_ID PERMISSION_ID
```

**Arguments:**
- `file_id`: The file ID (required)
- `permission_id`: The permission ID to delete (required)

## Examples

### Verify Setup

```bash
python scripts/google-drive.py check
```

### Find recent PDF files

```bash
python scripts/google-drive.py files list --query "mimeType='application/pdf'" --max-results 5
```

### Search for documents by name

```bash
python scripts/google-drive.py files search --name "project proposal"
```

### Download a file

```bash
# First, find the file ID
python scripts/google-drive.py files search --name "report.pdf"

# Then download it
python scripts/google-drive.py files download FILE_ID -o ./report.pdf
```

### Upload and share a file

```bash
# Upload the file
python scripts/google-drive.py files upload ./presentation.pdf --name "Q4 Presentation"

# Share with a colleague
python scripts/google-drive.py share FILE_ID --email colleague@example.com --role writer
```

### Organize files into folders

```bash
# Create a folder
python scripts/google-drive.py folders create "Project Documents"

# Upload files to the folder
python scripts/google-drive.py files upload ./doc1.pdf --parent FOLDER_ID
python scripts/google-drive.py files upload ./doc2.pdf --parent FOLDER_ID

# List folder contents
python scripts/google-drive.py folders list FOLDER_ID
```

## Drive Search Query Syntax

Common search operators:

| Operator | Description | Example |
|----------|-------------|---------|
| `name contains` | Name contains string | `name contains 'report'` |
| `name =` | Exact name match | `name = 'Budget 2024.xlsx'` |
| `mimeType =` | File type | `mimeType = 'application/pdf'` |
| `'ID' in parents` | In folder | `'folder_id' in parents` |
| `modifiedTime >` | Modified after | `modifiedTime > '2024-01-01'` |
| `trashed =` | Trashed status | `trashed = false` |
| `starred =` | Starred status | `starred = true` |
| `sharedWithMe` | Shared files | `sharedWithMe = true` |

Combine operators with `and` or `or`:

```bash
# PDF files modified this year
"mimeType = 'application/pdf' and modifiedTime > '2024-01-01'"

# Spreadsheets containing 'budget'
"name contains 'budget' and mimeType = 'application/vnd.google-apps.spreadsheet'"

# Files in a specific folder that are not trashed
"'folder_id' in parents and trashed = false"
```

For the complete reference, see [drive-queries.md](references/drive-queries.md).

## Common MIME Types

| Type | MIME Type |
|------|-----------|
| Folder | `application/vnd.google-apps.folder` |
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| PDF | `application/pdf` |
| Word | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Excel | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| PowerPoint | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| Text | `text/plain` |
| CSV | `text/csv` |
| Image (JPEG) | `image/jpeg` |
| Image (PNG) | `image/png` |

## Troubleshooting

### Check command fails

Run `python scripts/google-drive.py check` to diagnose issues. It will provide specific error messages and setup instructions.

### Authentication failed

1. Verify your OAuth client ID and client secret are correct in `~/.config/agent-skills/google.yaml`
2. Token expired or corrupted - clear and re-authenticate:
   ```bash
   keyring del agent-skills google-drive-token-json
   python scripts/google-drive.py check
   ```

### Permission denied

Your OAuth token may not have the necessary scopes. Revoke access at https://myaccount.google.com/permissions, clear your token, and re-authenticate.

### Cannot download Google Docs

Google Docs, Sheets, and Slides are not binary files - they cannot be downloaded directly. Use the Google Drive web interface to export them to a downloadable format (PDF, DOCX, etc.).

### Import errors

Ensure dependencies are installed:
```bash
pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
```

### Rate limiting

Drive API has quota limits. If you hit rate limits, wait a few minutes before retrying. For high-volume usage, consider requesting quota increases in the Google Cloud Console.

## API Scopes

This skill requests the following OAuth scopes:

- `https://www.googleapis.com/auth/drive.readonly` - Read files and metadata
- `https://www.googleapis.com/auth/drive.file` - Create, modify, delete files created by the app
- `https://www.googleapis.com/auth/drive.metadata.readonly` - View file metadata only

These scopes provide file management capabilities while following the principle of least privilege.

## Security Notes

- **OAuth tokens** are stored securely in your system keyring
- **Client secrets** are stored in `~/.config/agent-skills/google-drive.yaml` with file permissions 600
- **No passwords** are stored - only OAuth tokens
- **Tokens refresh automatically** when using the skill
- **Browser-based consent** ensures you approve all requested permissions

Always review OAuth consent screens before granting access to your Google Drive.
