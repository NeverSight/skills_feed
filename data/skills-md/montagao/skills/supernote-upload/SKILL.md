---
name: supernote-upload
description: Upload PDF and EPUB files to Supernote Cloud. Use this skill when the user wants to send documents to their Supernote device.
---

# Supernote Upload

Upload documents to Supernote Cloud for syncing to your Supernote device.

## Prerequisites Check

Before uploading, verify the `supernote` CLI is installed:

```bash
command -v supernote >/dev/null 2>&1 && echo "installed" || echo "not installed"
```

If not installed, install it:

```bash
pip install ~/hn2supernote/supernote_uploader
```

## Authentication Check

Verify authentication by listing the root folder:

```bash
supernote ls / 2>&1 | head -5
```

If this fails or prompts for credentials, the user needs to login first:

```bash
supernote login
```

After login, credentials are cached and subsequent commands work without prompting.

## Uploading Files

### Single file to Inbox (default)
```bash
supernote upload /path/to/document.pdf
```

### Single file to specific folder
```bash
supernote upload /path/to/document.pdf --folder /Documents/Books
```

### Multiple files
```bash
supernote upload file1.pdf file2.pdf --folder /Inbox/Articles
```

### Glob patterns
```bash
supernote upload *.pdf --folder /Documents
```

## Other Commands

### List folder contents
```bash
supernote ls /Inbox
```

### Create folder
```bash
supernote mkdir /Documents/NewFolder --parents
```

## Supported File Types

- PDF (.pdf)
- EPUB (.epub)

## Guidelines

1. Always check if `supernote` is installed before attempting to upload
2. If authentication fails, prompt the user to run `supernote login`
3. Default upload location is `/Inbox` if no folder is specified
4. Use `--folder` to specify a custom destination
5. Create folders with `--parents` flag to create intermediate directories
6. Report success/failure clearly to the user
