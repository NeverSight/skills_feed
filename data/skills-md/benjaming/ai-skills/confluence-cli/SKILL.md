---
name: confluence-cli
description: Use confluence-cli (NPM package) to manage Confluence content, pages, and spaces from the command line. Ideal for documentation workflows, bulk content operations, page migration, and when users request CLI-based Confluence interactions. Trigger on requests like "use Confluence CLI", "create Confluence pages via CLI", "migrate Confluence content", "automate documentation workflows", or when users want to script Confluence operations.
---

# Confluence CLI (NPM Package)

## Overview

confluence-cli is a community-developed command-line interface for Atlassian Confluence that enables content management directly from the terminal. This is a **third-party tool** (not official Atlassian), available via NPM.

**Use this skill when:**
- Users request CLI-based Confluence operations
- Documentation workflows need automation
- Bulk page operations are required
- Content migration between spaces is needed
- Users want to script documentation updates

**Important**: This is NOT the official Atlassian CLI (acli), which does not support Confluence. This is a community tool: https://github.com/pchuri/confluence-cli

## Installation

### Prerequisites
- Node.js and NPM installed

### Install Options

```bash
# Global installation (recommended for frequent use)
npm install -g confluence-cli

# Or use directly with npx (no installation)
npx confluence-cli --help
```

## Configuration

### Interactive Setup (Recommended)

```bash
# Launch configuration wizard
confluence init
```

The wizard will guide you through:
1. Selecting your Confluence instance type (Cloud or self-hosted)
2. Choosing appropriate API endpoints
3. Setting up authentication

### Environment Variables

Alternatively, configure using environment variables:

```bash
export CONFLUENCE_DOMAIN="yourcompany.atlassian.net"
export CONFLUENCE_EMAIL="your@email.com"
export CONFLUENCE_API_TOKEN="your-api-token"
export CONFLUENCE_API_PATH="/wiki/rest/api"  # Cloud default
export CONFLUENCE_AUTH_TYPE="basic"  # or "bearer"
```

**API Path Defaults:**
- Cloud: `/wiki/rest/api`
- Self-hosted/Data Center: `/rest/api`

## Authentication

### Getting API Tokens

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Label your token (e.g., "confluence-cli")
4. Copy the generated token

### Authentication Types

**Basic Auth (Cloud - Default)**
- Requires: Email + API Token
- Used automatically when `CONFLUENCE_EMAIL` is set

**Bearer Token (Self-hosted/Data Center)**
- Requires: Bearer token only
- Set `CONFLUENCE_AUTH_TYPE="bearer"`

## Core Commands

### 1. Read Pages

Retrieve page content in various formats:

```bash
# Read as text (default)
confluence read 123456789

# Read as HTML
confluence read 123456789 --format html

# Read as Markdown
confluence read 123456789 --format markdown

# Using page URL instead of ID
confluence read "https://yourcompany.atlassian.net/wiki/spaces/SPACE/pages/123456789"
```

**Formats:**
- `text` - Plain text (default)
- `html` - HTML format
- `markdown` - Markdown format (useful for documentation workflows)

### 2. Get Page Information

View metadata about a page:

```bash
# Get page metadata
confluence info 123456789

# Using URL
confluence info "https://yourcompany.atlassian.net/wiki/spaces/SPACE/pages/123456789"
```

Returns: Page ID, title, space, version, created/modified dates, authors, etc.

### 3. Search Content

Find pages using Confluence Query Language (CQL):

```bash
# Basic search
confluence search "API documentation"

# Search with result limit
confluence search "meeting notes" --limit 10

# Complex CQL queries
confluence search "type=page AND space=DEV AND title~'API'"
```

**Common CQL Patterns:**
- `type=page` - Pages only (not attachments)
- `space=SPACEKEY` - Within specific space
- `title~'keyword'` - Title contains keyword
- `text~'keyword'` - Content contains keyword
- `created >= now()-7d` - Created in last 7 days

### 4. List Spaces

View all accessible spaces:

```bash
# List all spaces
confluence spaces
```

Returns: Space keys, names, types, and URLs

### 5. Find Pages by Title

Locate pages by exact or partial title:

```bash
# Find in all spaces
confluence find "Project Documentation"

# Find in specific space
confluence find "API Guide" --space DEV
```

### 6. Create Pages

Create new pages with content:

```bash
# Create with inline content
confluence create "My New Page" SPACEKEY --content "Hello World!"

# Create from file
confluence create "Documentation" SPACEKEY --file ./content.md --format markdown

# Create with HTML content
confluence create "Release Notes" SPACEKEY --content "<h1>Version 2.0</h1>" --format html

# Create with storage format (Confluence native)
confluence create "Technical Doc" SPACEKEY --file ./doc.xml --format storage
```

**Key options:**
- `--content` - Inline content string
- `--file` - Read content from file
- `--format` - Content format: `markdown`, `html`, or `storage` (default: storage)

### 7. Create Child Pages

Create pages under existing parent pages:

```bash
# Create child page with inline content
confluence create-child "Subsection" 123456789 --content "Child content"

# Create from file
confluence create-child "API Reference" 123456789 --file ./api-docs.md --format markdown

# Using parent page URL
confluence create-child "Details" "https://...pages/123456789" --content "Details here"
```

### 8. Update Pages

Modify existing pages:

```bash
# Update title only
confluence update 123456789 --title "Updated Title"

# Update content only
confluence update 123456789 --content "New content" --format markdown

# Update from file
confluence update 123456789 --file ./updated-content.md --format markdown

# Update both title and content
confluence update 123456789 --title "New Title" --content "New content"
```

**Key options:**
- `--title` - Change page title
- `--content` - Inline content
- `--file` - Read content from file
- `--format` - Content format (markdown, html, storage)

### 9. Edit Workflow (Export → Modify → Update)

Export page for local editing:

```bash
# Export page to file in storage format
confluence edit 123456789 --output ./page.xml

# Edit the file locally with your preferred editor
# Then update back to Confluence
confluence update 123456789 --file ./page.xml --format storage
```

This workflow is useful for:
- Complex formatting changes
- Offline editing
- Version control integration
- Batch processing

### 10. Copy Page Trees

Duplicate page hierarchies with all children:

```bash
# Copy entire page tree
confluence copy-tree 123456789 987654321

# Copy with custom title for root page
confluence copy-tree 123456789 987654321 "Copied Documentation"

# Limit depth of copy
confluence copy-tree 123456789 987654321 --max-depth 2

# Exclude pages by pattern (wildcards supported)
confluence copy-tree 123456789 987654321 --exclude "temp*,*draft*,*obsolete*"

# Add delay between operations (for rate limiting)
confluence copy-tree 123456789 987654321 --delay-ms 500

# Dry run (preview without making changes)
confluence copy-tree 123456789 987654321 --dry-run
```

**Key options:**
- `--max-depth <number>` - Limit tree depth (default: unlimited)
- `--exclude <patterns>` - Comma-separated wildcard patterns to skip
- `--delay-ms <number>` - Milliseconds delay between API calls
- `--dry-run` - Preview what would be copied without making changes

**Exclusion patterns:**
- `*` matches any characters
- `?` matches single character
- Examples: `temp*`, `*draft*`, `archive-?`

### 11. View Statistics

Check CLI usage analytics:

```bash
# View usage statistics
confluence stats
```

**Disable analytics:**
```bash
export CONFLUENCE_CLI_ANALYTICS=false
```

## Content Formats

### Storage Format (Confluence Native)

Confluence's internal XML-based format (XHTML):

```xml
<p>This is <strong>bold</strong> and <em>italic</em> text.</p>
<ac:structured-macro ac:name="code">
  <ac:plain-text-body><![CDATA[console.log('Hello');]]></ac:plain-text-body>
</ac:structured-macro>
```

**When to use:**
- Maximum fidelity for Confluence-specific features
- Macros, layouts, and advanced formatting
- Export/import workflows

### HTML Format

Standard HTML:

```html
<h1>Heading</h1>
<p>Paragraph with <strong>bold</strong> text.</p>
<ul>
  <li>List item 1</li>
  <li>List item 2</li>
</ul>
```

**When to use:**
- Familiar syntax
- Converting from other HTML sources
- Simple formatting needs

### Markdown Format

GitHub-flavored Markdown:

```markdown
# Heading

Paragraph with **bold** text.

- List item 1
- List item 2

```code
console.log('Hello');
```
```

**When to use:**
- Developer documentation
- README files and similar content
- Simple, readable syntax
- Integration with markdown-based tools

**Note**: Markdown is converted to storage format server-side. Complex Confluence features may not be available.

## Best Practices

### 1. Authentication and Security

```bash
# Store credentials securely in environment variables
# Add to ~/.bashrc, ~/.zshrc, or use a secrets manager
export CONFLUENCE_API_TOKEN="your-token-here"

# Rotate API tokens regularly
# Revoke old tokens from: https://id.atlassian.com/manage-profile/security/api-tokens

# Use separate tokens for different environments
export CONFLUENCE_DEV_TOKEN="dev-token"
export CONFLUENCE_PROD_TOKEN="prod-token"
```

### 2. Bulk Operations

For bulk operations, combine with shell tools:

```bash
# Search and process multiple pages
confluence search "type=page AND space=DEV" | while read -r line; do
  # Extract page ID and process
  # Add delays to respect rate limits
  sleep 1
done

# Batch create pages from directory of markdown files
for file in docs/*.md; do
  title=$(basename "$file" .md)
  confluence create "$title" DEV --file "$file" --format markdown
  sleep 0.5  # Rate limit protection
done
```

### 3. Rate Limiting

Respect Confluence API rate limits:

```bash
# Add delays in scripts
sleep 0.5  # 500ms between calls

# Use --delay-ms for copy-tree operations
confluence copy-tree SOURCE TARGET --delay-ms 500

# Monitor for rate limit errors and implement backoff
```

### 4. Error Handling in Scripts

```bash
#!/bin/bash

# Check if confluence is installed
if ! command -v confluence &> /dev/null; then
  echo "confluence-cli not found. Install: npm install -g confluence-cli"
  exit 1
fi

# Check authentication
if ! confluence spaces &> /dev/null; then
  echo "Authentication failed. Run: confluence init"
  exit 1
fi

# Perform operations with error checking
if confluence create "My Page" DEV --content "Hello"; then
  echo "Page created successfully"
else
  echo "Failed to create page"
  exit 1
fi
```

### 5. Version Control Integration

```bash
# Export pages for version control
mkdir -p confluence-backup
for page_id in 123456 234567 345678; do
  confluence read "$page_id" --format markdown > "confluence-backup/${page_id}.md"
done

# Commit to git
cd confluence-backup
git add .
git commit -m "Backup Confluence pages"
git push
```

### 6. Content Migration

```bash
# Migrate space documentation to new space

# 1. Export all pages from source space
SOURCE_SPACE="OLD"
TARGET_SPACE="NEW"

# Get root pages in source space
confluence search "type=page AND space=$SOURCE_SPACE AND parent is null" > root_pages.txt

# 2. For each root page, copy tree to target space
# (Manual: create corresponding parent page in target space first)
# Then copy children:
confluence copy-tree SOURCE_PAGE_ID TARGET_PAGE_ID
```

## Common Use Cases

### Documentation Workflow

```bash
# 1. Create documentation structure
confluence create "API Documentation" DEV --content "# API Docs"
ROOT_ID=123456789

# 2. Create subsections
confluence create-child "Authentication" $ROOT_ID --file ./auth.md --format markdown
confluence create-child "Endpoints" $ROOT_ID --file ./endpoints.md --format markdown
confluence create-child "Examples" $ROOT_ID --file ./examples.md --format markdown

# 3. Update as docs evolve
confluence update $ROOT_ID --file ./updated-overview.md --format markdown
```

### Content Search and Export

```bash
# Find and export all API documentation
confluence search "type=page AND title~'API'" --limit 50 | \
  grep -o '[0-9]\{8,\}' | \
  while read page_id; do
    confluence read "$page_id" --format markdown > "export/${page_id}.md"
  done
```

### Space Migration

```bash
# Copy documentation from one space to another
# (Requires manual creation of target parent page first)

SOURCE_ROOT=123456789  # Root page in source space
TARGET_ROOT=987654321  # Root page in target space (pre-created)

confluence copy-tree $SOURCE_ROOT $TARGET_ROOT "Migrated Documentation" \
  --exclude "*draft*,*temp*" \
  --delay-ms 500 \
  --dry-run  # Remove after verifying
```

### Automated Updates

```bash
#!/bin/bash
# Update release notes automatically

VERSION="2.0.0"
DATE=$(date +"%Y-%m-%d")
PAGE_ID=123456789

# Generate release notes from git log
echo "# Release $VERSION ($DATE)" > release-notes.md
echo "" >> release-notes.md
git log --oneline --since="2 weeks ago" >> release-notes.md

# Update Confluence page
confluence update $PAGE_ID --file release-notes.md --format markdown

echo "Release notes updated for version $VERSION"
```

### Backup and Restore

```bash
# Backup script
BACKUP_DIR="./confluence-backup-$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Export pages from specific space
confluence search "type=page AND space=DEV" | \
  grep -o '[0-9]\{8,\}' | \
  while read page_id; do
    confluence read "$page_id" --format storage > "$BACKUP_DIR/${page_id}.xml"
    confluence info "$page_id" > "$BACKUP_DIR/${page_id}-info.json"
    sleep 0.5
  done

tar -czf "confluence-backup-$(date +%Y%m%d).tar.gz" "$BACKUP_DIR"
```

## Integration with Claude Code

When using this skill in Claude Code:

1. **Check installation**: Verify `confluence` command is available
2. **Verify authentication**: Run `confluence spaces` to test
3. **Use Bash tool**: Execute confluence commands via Bash tool
4. **Parse output**: Most commands output human-readable text; use `--format` flags where available
5. **Handle page IDs**: Extract page IDs from URLs or search results
6. **Rate limiting**: Add delays in bulk operations
7. **Error handling**: Check exit codes and provide helpful error messages
8. **Confirm destructive operations**: Warn before bulk updates or deletions

## Troubleshooting

### Authentication Issues

```bash
# Check if configuration exists
ls -la ~/.confluence/

# Re-run initialization
confluence init

# Test connection
confluence spaces
```

### API Errors

```bash
# Verify API token is valid
# Check: https://id.atlassian.com/manage-profile/security/api-tokens

# Ensure correct domain format
# Cloud: "yourcompany.atlassian.net"
# NOT: "https://yourcompany.atlassian.net"

# Check API path matches your instance type
# Cloud: /wiki/rest/api
# Self-hosted: /rest/api
```

### Rate Limiting

```bash
# If you encounter rate limits:
# - Add delays between operations (--delay-ms or sleep)
# - Reduce batch sizes
# - Space out operations over time
```

### Content Format Issues

```bash
# If content doesn't render correctly:
# - Try different format: --format storage, html, or markdown
# - Export existing similar page to see format: confluence edit PAGE_ID --output example.xml
# - Use storage format for maximum compatibility
```

## Limitations

### Third-Party Tool

- **Not official Atlassian product**: Community-maintained
- **Support**: Through GitHub issues, not Atlassian support
- **Updates**: Dependent on community contributions
- **Compatibility**: May lag behind Confluence API changes

### API Limitations

- **No attachment management**: Cannot upload/download attachments via this CLI
- **Limited macro support**: Complex Confluence macros may not work with markdown/HTML formats
- **No admin operations**: User/space management not supported
- **Rate limits**: Subject to Confluence Cloud API rate limits

### Format Conversions

- **Markdown limitations**: Not all Confluence features available in markdown
- **HTML to storage**: May require manual adjustment for complex layouts
- **Macros**: Best created/edited in storage format

## Alternative Tools

### Official Atlassian CLI (acli)

- **Status**: Does NOT currently support Confluence (only Jira)
- **If support added**: May become preferred official tool
- **Current**: Use for Jira operations only

### Appfire Confluence CLI

- **Type**: Commercial Marketplace app
- **Features**: More comprehensive admin/automation features
- **Cost**: Requires purchase/licensing
- **Use case**: Enterprise automation, advanced admin tasks

### Confluence REST API

- **Direct API calls**: Using curl or similar tools
- **Flexibility**: Maximum control
- **Complexity**: More code required
- **Use case**: Custom integrations, specific requirements

## Help and Documentation

```bash
# Main help
confluence --help

# Command help
confluence read --help
confluence create --help
confluence copy-tree --help

# Version info
confluence --version
```

**External Resources:**
- GitHub: https://github.com/pchuri/confluence-cli
- NPM: https://www.npmjs.com/package/confluence-cli
- Confluence REST API: https://developer.atlassian.com/cloud/confluence/rest/v1/

## Important Notes

- **Third-party tool**: Not official Atlassian - community-developed
- **Cloud and self-hosted**: Supports both, but configuration differs
- **API tokens**: Required for authentication - obtain from Atlassian account settings
- **Rate limits**: Respect Confluence API rate limits in bulk operations
- **Content formats**: Storage format provides best fidelity for Confluence features
- **No official CLI**: Atlassian's official CLI (acli) does not support Confluence currently
- **Analytics**: Tool collects anonymous usage data (opt-out via environment variable)
