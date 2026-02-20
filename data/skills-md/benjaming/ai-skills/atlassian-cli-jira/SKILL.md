---
name: atlassian-cli-jira
description: Use Atlassian CLI (acli) to manage Jira work items, projects, and workflows from the command line. Ideal for bulk operations, automation, scripting, and when users request CLI-based Jira interactions. Trigger on requests like "use Jira CLI", "create Jira issues via CLI", "bulk update Jira tickets", "automate Jira workflows", or when users want to script Jira operations.
---

# Atlassian CLI for Jira

## Overview

Atlassian CLI (acli) is the official command-line interface for Jira Cloud that enables management of work items, projects, and workflows directly from the terminal. Use this skill when:
- Users request CLI-based Jira operations
- Bulk operations are needed (updating multiple issues, bulk transitions)
- Automation or scripting is required
- Users want to avoid the Jira UI for repetitive tasks

## Authentication

Before using any Jira commands, authenticate using OAuth:

```bash
# Interactive OAuth login (recommended)
acli jira auth login --web

# Login with API token (for automation)
echo <token> | acli jira auth login --site "mysite.atlassian.net" --email "user@atlassian.com" --token
```

## Work Item Commands

Work items (issues/tickets) are the core of Jira. The CLI uses "workitem" instead of "issue".

### Create Work Items

```bash
# Basic creation
acli jira workitem create --summary "Fix login bug" --project "PROJ" --type "Bug"

# With additional fields
acli jira workitem create \
  --summary "Add new feature" \
  --project "PROJ" \
  --type "Story" \
  --assignee "user@example.com" \
  --label "frontend,priority" \
  --description "Detailed description here"

# From file content
acli jira workitem create --from-file "description.txt" --project "PROJ" --type "Task"

# From JSON (for complex work items)
acli jira workitem create --generate-json  # Generate template
acli jira workitem create --from-json "workitem.json"

# With ADF description (rich formatting)
acli jira workitem create \
  --summary "Implement user authentication" \
  --project "PROJ" \
  --type "Story" \
  --description '{
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "paragraph",
        "content": [
          {"type": "text", "text": "Implement secure user authentication with the following requirements:", "marks": [{"type": "strong"}]}
        ]
      },
      {
        "type": "bulletList",
        "content": [
          {
            "type": "listItem",
            "content": [
              {
                "type": "paragraph",
                "content": [
                  {"type": "text", "text": "OAuth 2.0 support"}
                ]
              }
            ]
          },
          {
            "type": "listItem",
            "content": [
              {
                "type": "paragraph",
                "content": [
                  {"type": "text", "text": "JWT token management"}
                ]
              }
            ]
          }
        ]
      }
    ]
  }'

# ADF description from file
acli jira workitem create \
  --summary "Database migration" \
  --project "PROJ" \
  --type "Task" \
  --description-file "description.adf.json"
```

**Key flags:**
- `--summary` (required): Work item title
- `--project` (required): Project key (e.g., "TEAM", "PROJ")
- `--type` (required): Work item type ("Task", "Bug", "Story", "Epic")
- `--assignee`: Email or account ID, use '@me' for self-assignment
- `--label`: Comma-separated labels
- `--description`: Plain text or Atlassian Document Format (ADF)
- `--description-file`: Read description from file (plain text or ADF)

### View Work Items

```bash
# View single work item
acli jira workitem view KEY-123

# View as JSON
acli jira workitem view KEY-123 --json

# View specific fields only
acli jira workitem view KEY-123 --fields summary,status,assignee,comment

# Open in browser
acli jira workitem view KEY-123 --web
```

### Search Work Items

Use JQL (Jira Query Language) to search:

```bash
# Basic search
acli jira workitem search --jql "project = TEAM"

# Complex search with pagination
acli jira workitem search --jql "project = TEAM AND status = 'In Progress'" --paginate

# Get count only
acli jira workitem search --jql "assignee = currentUser()" --count

# Export to CSV with specific fields
acli jira workitem search \
  --jql "project = TEAM" \
  --fields "key,summary,status,assignee" \
  --csv
```

**Common JQL patterns:**
- `project = TEAM` - All work items in project
- `assignee = currentUser()` - Assigned to you
- `status = 'In Progress'` - Specific status
- `created >= -7d` - Created in last 7 days
- `priority = High` - High priority items
- `labels = backend` - With specific label

### Edit Work Items

```bash
# Edit by key
acli jira workitem edit --key "KEY-1" --summary "Updated summary"

# Bulk edit by multiple keys
acli jira workitem edit --key "KEY-1,KEY-2,KEY-3" --assignee "user@example.com"

# Edit via JQL query (powerful for bulk operations)
acli jira workitem edit \
  --jql "project = TEAM AND status = 'To Do'" \
  --assignee "user@example.com"

# Edit via filter
acli jira workitem edit --filter 10001 --description "Updated description" --yes

# Update description from file
acli jira workitem edit --key "KEY-1" --description-file "new-description.txt"

# Update with ADF description (rich formatting)
acli jira workitem edit --key "KEY-1" --description '{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Updated requirements:", "marks": [{"type": "strong"}]}
      ]
    },
    {
      "type": "orderedList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Add error handling"}
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Implement logging"}
              ]
            }
          ]
        }
      ]
    }
  ]
}'

# ADF description from file for bulk update
acli jira workitem edit \
  --jql "project = TEAM AND sprint = 'Sprint 10'" \
  --description-file "sprint-goals.adf.json"

# From JSON for complex updates
acli jira workitem edit --generate-json  # Generate template
acli jira workitem edit --from-json "update.json"
```

**Key flags:**
- `--key`: Single or comma-separated keys
- `--jql`: JQL query for bulk operations
- `--filter`: Filter ID to target work items
- `--summary`: Update summary
- `--description`: Update description (plain text or ADF)
- `--description-file`: Read description from file (plain text or ADF)
- `--assignee`: Change assignee (use '@me' for self, 'default' for project default)
- `--yes`: Skip confirmation (use with caution)

### Transition Work Items

Change work item status through workflow transitions:

```bash
# Transition by key
acli jira workitem transition --key "KEY-1" --status "In Progress"

# Bulk transition by keys
acli jira workitem transition --key "KEY-1,KEY-2" --status "Done"

# Transition via JQL (very powerful)
acli jira workitem transition \
  --jql "project = TEAM AND status = 'To Do'" \
  --status "In Progress"

# Transition via filter
acli jira workitem transition --filter 10001 --status "Done" --yes
```

### Assign Work Items

```bash
# Assign by key
acli jira workitem assign --key "KEY-1" --assignee "user@example.com"

# Self-assign
acli jira workitem assign --key "KEY-1" --assignee "@me"

# Assign to default
acli jira workitem assign --key "KEY-1" --assignee "default"

# Unassign
acli jira workitem assign --key "KEY-1" --assignee ""

# Bulk assign via JQL
acli jira workitem assign --jql "project = TEAM" --assignee "user@example.com"
```

### Clone Work Items

```bash
# Clone single work item
acli jira workitem clone --key "KEY-1" --to-project "TEAM"

# Clone multiple work items
acli jira workitem clone --key "KEY-1,KEY-2" --to-project "NEWTEAM"

# Clone via JQL
acli jira workitem clone --jql "project = TEAM" --to-project "ARCHIVE"

# Clone from filter
acli jira workitem clone --filter 10001 --to-project "TEAM"

# Clone from file with work item keys
acli jira workitem clone --from-file "keys.txt" --to-project "TEAM"
```

### Delete Work Items

```bash
# Delete single work item
acli jira workitem delete --key "KEY-1"

# Delete multiple work items
acli jira workitem delete --key "KEY-1,KEY-2,KEY-3"

# Delete via JQL
acli jira workitem delete --jql "project = OLDPROJECT"

# Delete via filter with auto-confirmation
acli jira workitem delete --filter 10001 --yes
```

### Archive/Unarchive Work Items

```bash
# Archive work items
acli jira workitem archive --key "KEY-1,KEY-2"
acli jira workitem archive --jql "project = TEAM AND status = Done"

# Unarchive work items
acli jira workitem unarchive --key "KEY-1"
acli jira workitem unarchive --jql "project = TEAM"
```

## Comments

### Create Comments

```bash
# Create comment on single work item
acli jira workitem comment create --key "KEY-1" --body "This is a comment"

# Create comment on multiple work items
acli jira workitem comment create --key "KEY-1,KEY-2" --body "Bulk comment"

# Create comment via JQL
acli jira workitem comment create \
  --jql "project = TEAM" \
  --body "Comment on all work items"

# Create comment from file
acli jira workitem comment create --key "KEY-1" --body-file "comment.txt"
```

### Create Comments with ADF (Rich Formatting)

ADF (Atlassian Document Format) enables rich text formatting in comments. The acli automatically detects ADF when you provide valid JSON, so no special flag is needed.

**Important**: Comments only support plain text or ADF. Markdown is NOT supported.

#### ADF Node Support: Comments vs Descriptions

Jira **comments have a restricted ADF subset** compared to descriptions. Using unsupported nodes will cause "Comment body is not valid!" errors.

**✅ Safe for Comments:**
- Block nodes: `paragraph`, `bulletList`, `orderedList`, `codeBlock`
- Inline nodes: `text`, `hardBreak`, `mention`
- Text marks: `strong`, `em`, `code`, `link`, `strike`, `underline`

**❌ NOT Supported in Comments:**
- `heading` (use bold paragraph instead)
- `panel` (use regular paragraph)
- `table`, `tableRow`, `tableCell`
- `blockquote` (may not work)
- `emoji`, `date` (may not work)
- `rule` (horizontal rule - may not work)

**✅ Safe for Descriptions (work item create/edit):**
- All comment nodes PLUS: `heading`, `panel`, `table`, and more

**Best practice:** Test ADF on a single work item before bulk operations.

#### Simple formatted comment (inline)

```bash
acli jira workitem comment create --key "KEY-1" --body '{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Status update: "},
        {"type": "text", "text": "bug fixed", "marks": [{"type": "strong"}]},
        {"type": "text", "text": " and ready for testing."}
      ]
    }
  ]
}'
```

#### Comment with multiple paragraphs

```bash
acli jira workitem comment create --key "KEY-1" --body '{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Completed the following tasks:"}
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Fixed authentication bug"}
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Updated API documentation"}
              ]
            }
          ]
        }
      ]
    }
  ]
}'
```

#### Comment with code block

```bash
acli jira workitem comment create --key "KEY-1" --body '{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Error found in the authentication handler:"}
      ]
    },
    {
      "type": "codeBlock",
      "attrs": {"language": "javascript"},
      "content": [
        {
          "type": "text",
          "text": "if (user.token === null) {\n  throw new Error(\"Invalid token\");\n}"
        }
      ]
    }
  ]
}'
```

#### Comment with user mention

```bash
acli jira workitem comment create --key "KEY-1" --body '{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "mention",
          "attrs": {"id": "557058:f58131cb-b67d-43c7-b30d-6b58d40bd077"}
        },
        {"type": "text", "text": " can you review this change?"}
      ]
    }
  ]
}'
```

**Note**: To mention a user, you need their Atlassian account ID. Get it from user profile or API.

#### ADF from file (recommended for complex comments)

```bash
# Create ADF file: comment.adf.json
cat > comment.adf.json << 'EOF'
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Release Notes v2.5.0", "marks": [{"type": "strong"}]}
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Key changes in this release:"}
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Performance improvements", "marks": [{"type": "strong"}]}
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Bug fixes for edge cases"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
EOF

# Use the ADF file
acli jira workitem comment create --key "KEY-1" --body-file "comment.adf.json"

# Or add to multiple work items
acli jira workitem comment create --key "KEY-1,KEY-2,KEY-3" --body-file "comment.adf.json"
```

#### Common ADF formatting patterns

**Bold text:**
```json
{"type": "text", "text": "bold text", "marks": [{"type": "strong"}]}
```

**Italic text:**
```json
{"type": "text", "text": "italic text", "marks": [{"type": "em"}]}
```

**Inline code:**
```json
{"type": "text", "text": "code", "marks": [{"type": "code"}]}
```

**Link:**
```json
{
  "type": "text",
  "text": "Click here",
  "marks": [{"type": "link", "attrs": {"href": "https://example.com"}}]
}
```

**Multiple marks (bold + italic):**
```json
{
  "type": "text",
  "text": "bold and italic",
  "marks": [{"type": "strong"}, {"type": "em"}]
}
```

### List Comments

```bash
# List all comments for a work item
acli jira workitem comment list --key "KEY-1"

# List as JSON
acli jira workitem comment list --key "KEY-1" --json
```

### Get Comment Visibility Options

```bash
# Get available visibility options
acli jira workitem comment visibility
```

## Attachments

### List Attachments

```bash
# List attachments for a work item
acli jira workitem attachment list --key "KEY-1"

# List as JSON
acli jira workitem attachment list --key "KEY-1" --json
```

### Download Attachments (API Workaround)

The CLI cannot download attachment content. Use the Jira REST API directly.

Requires env vars: `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_BASE_URL`

**Download single attachment:**
```bash
# First list attachments to get ID and filename
acli jira workitem attachment list --key "KEY-1" --json

# Download by attachment ID
curl -L \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/attachment/content/$ATTACHMENT_ID" \
  --output "$ATTACHMENT_NAME"
```

**Download all attachments for an issue:**
```bash
# Get all attachment IDs and names, then download each
acli jira workitem attachment list --key "KEY-1" --json | \
  jq -r '.[] | "\(.id) \(.filename)"' | \
  while read -r id name; do
    curl -L -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
      "$JIRA_BASE_URL/rest/api/3/attachment/content/$id" \
      --output "$name"
  done
```

## Project Commands

### List Projects

```bash
# List default projects (30)
acli jira project list

# List recently viewed projects
acli jira project list --recent

# List all projects with pagination
acli jira project list --paginate

# List with custom limit
acli jira project list --limit 50

# Export to JSON
acli jira project list --json
```

### View Project

```bash
# View project details
acli jira project view --project-key "TEAM"

# View as JSON
acli jira project view --project-key "TEAM" --json
```

### Create Project

```bash
# Create from existing project
acli jira project create \
  --from-project "TEAM" \
  --key "NEWTEAM" \
  --name "New Project"

# With additional details
acli jira project create \
  --from-project "TEAM" \
  --key "NEWTEAM" \
  --name "New Project" \
  --description "Project description" \
  --url "https://example.com" \
  --lead-email "user@example.com"

# From JSON
acli jira project create --generate-json  # Generate template
acli jira project create --from-json "project.json"
```

### Update Project

```bash
# Update project key and name
acli jira project update \
  --project-key "TEAM1" \
  --key "TEAM" \
  --name "Updated Name"

# From JSON
acli jira project update --generate-json  # Generate template
acli jira project update --from-json "project.json"
```

### Archive/Restore Projects

```bash
# Archive project
acli jira project archive --project-key "OLDTEAM"

# Restore archived project
acli jira project restore --project-key "OLDTEAM"
```

### Delete Project

```bash
# Delete project
acli jira project delete --project-key "OLDPROJECT"
```

## Dashboard Commands

```bash
# Dashboard operations (check documentation for specific commands)
acli jira dashboard --help
```

## Filter Commands

```bash
# Filter operations (check documentation for specific commands)
acli jira filter --help
```

## Best Practices

### Bulk Operations

For bulk operations, use JQL or filters instead of comma-separated keys when possible:

```bash
# Good: Use JQL for flexible bulk operations
acli jira workitem edit --jql "project = TEAM AND status = 'To Do'" --assignee "@me"

# Good: Use filters for reusable bulk operations
acli jira workitem transition --filter 10001 --status "Done" --yes
```

### Safety

Use `--yes` flag cautiously, especially with delete operations:

```bash
# Preview first by running without --yes
acli jira workitem delete --jql "project = OLDPROJECT"

# Add --yes only after verifying
acli jira workitem delete --jql "project = OLDPROJECT" --yes
```

### JSON Templates

For complex operations, generate JSON templates first:

```bash
# Generate template
acli jira workitem create --generate-json > template.json

# Edit template.json with your data
# Then create from JSON
acli jira workitem create --from-json "template.json"
```

### Output Formats

Use appropriate output formats for different use cases:

```bash
# Human-readable (default)
acli jira workitem view KEY-1

# JSON for scripting/parsing
acli jira workitem view KEY-1 --json

# CSV for spreadsheets
acli jira workitem search --jql "project = TEAM" --csv
```

### Working with ADF

When working with ADF (Atlassian Document Format) for rich formatting:

#### When to use ADF vs Plain Text

**Use ADF when you need:**
- Rich text formatting (bold, italic, underline)
- Structured content (lists, headings, tables)
- Code blocks with syntax highlighting
- User mentions (@mentions)
- Links embedded in text
- Complex layouts

**Use plain text when:**
- Simple status updates or short notes
- Automation scripts where formatting isn't needed
- Quick comments without special formatting
- Performance is critical (ADF is more verbose)

#### Auto-detection

The acli automatically detects whether input is plain text or ADF JSON. No special flag is required:

```bash
# Plain text - automatically detected
acli jira workitem comment create --key "KEY-1" --body "Simple comment"

# ADF - automatically detected by JSON structure
acli jira workitem comment create --key "KEY-1" --body '{"version": 1, "type": "doc", "content": [...]}'
```

#### Best practices for ADF

**1. Use files for reusability:**
```bash
# Create reusable ADF templates
cat > templates/status-update.adf.json << 'EOF'
{
  "version": 1,
  "type": "doc",
  "content": [...]
}
EOF

# Reuse across multiple work items
acli jira workitem comment create --key "KEY-1,KEY-2" --body-file "templates/status-update.adf.json"
```

**2. Test ADF before bulk operations:**
```bash
# Test on single work item first
acli jira workitem comment create --key "KEY-TEST" --body-file "comment.adf.json"

# Verify it looks correct in Jira UI
acli jira workitem view KEY-TEST --web

# Then apply to multiple items
acli jira workitem comment create --jql "project = TEAM" --body-file "comment.adf.json"
```

**3. Keep ADF simple and maintainable:**
```bash
# Good: Simple, readable structure
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Status: "},
        {"type": "text", "text": "Complete", "marks": [{"type": "strong"}]}
      ]
    }
  ]
}

# Avoid: Overly complex nested structures that are hard to maintain
```

**4. Validate ADF structure:**

Ensure your ADF always includes:
- `"version": 1` - Required ADF version
- `"type": "doc"` - Required root node type
- `"content": [...]` - Array of block nodes (can be empty)

**5. Common patterns for building ADF programmatically:**

```bash
# Using jq to build ADF dynamically
ISSUE_KEY="KEY-1"
STATUS="Complete"

jq -n --arg status "$STATUS" '{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Status: "},
        {"type": "text", "text": $status, "marks": [{"type": "strong"}]}
      ]
    }
  ]
}' | acli jira workitem comment create --key "$ISSUE_KEY" --body "$(cat)"
```

#### Common ADF issues and solutions

**Issue**: "Comment body is not valid!" error
- **Cause**: Using ADF nodes that aren't supported in comments (heading, panel, table, etc.)
- **Solution**: Stick to safe comment nodes: paragraph, bulletList, orderedList, codeBlock, text, and basic marks
- **Example fix**: Replace `{"type": "heading"}` with `{"type": "paragraph", "content": [{"type": "text", "text": "...", "marks": [{"type": "strong"}]}]}`

**Issue**: Comment appears as raw JSON text
- **Cause**: Invalid ADF structure or missing required fields
- **Solution**: Validate that `version`, `type`, and `content` are present

**Issue**: Special characters break the ADF
- **Cause**: Unescaped quotes or special characters in bash
- **Solution**: Use files (`--body-file`) instead of inline JSON for complex content

**Issue**: User mention doesn't work
- **Cause**: Incorrect account ID format
- **Solution**: Get exact account ID from user profile or API, format: `557058:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Issue**: ADF works in descriptions but fails in comments
- **Cause**: Comments have a more restricted ADF subset than descriptions
- **Solution**: See "ADF Node Support: Comments vs Descriptions" section above for safe nodes

## ADF Quick Reference

Complete reference for ADF (Atlassian Document Format) node types and formatting options.

### Basic Structure

**Minimum valid ADF document:**
```json
{
  "version": 1,
  "type": "doc",
  "content": []
}
```

**Simple paragraph:**
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Hello world"}
      ]
    }
  ]
}
```

### Text Formatting (Marks)

**Bold (strong):**
```json
{"type": "text", "text": "bold text", "marks": [{"type": "strong"}]}
```

**Italic (emphasis):**
```json
{"type": "text", "text": "italic text", "marks": [{"type": "em"}]}
```

**Underline:**
```json
{"type": "text", "text": "underlined", "marks": [{"type": "underline"}]}
```

**Strikethrough:**
```json
{"type": "text", "text": "deleted", "marks": [{"type": "strike"}]}
```

**Inline code:**
```json
{"type": "text", "text": "code", "marks": [{"type": "code"}]}
```

**Link:**
```json
{
  "type": "text",
  "text": "Click here",
  "marks": [
    {
      "type": "link",
      "attrs": {"href": "https://example.com"}
    }
  ]
}
```

**Combined formatting (bold + italic):**
```json
{
  "type": "text",
  "text": "bold and italic",
  "marks": [
    {"type": "strong"},
    {"type": "em"}
  ]
}
```

### Headings

⚠️ **NOT supported in comments** - Use bold paragraphs instead. Works in descriptions only.

**Heading levels 1-6:**
```json
{
  "type": "heading",
  "attrs": {"level": 1},
  "content": [
    {"type": "text", "text": "Heading 1"}
  ]
}
```

Available levels: 1, 2, 3, 4, 5, 6

**Comment-safe alternative:**
```json
{
  "type": "paragraph",
  "content": [
    {"type": "text", "text": "Heading Text", "marks": [{"type": "strong"}]}
  ]
}
```

### Lists

**Bullet list:**
```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {"type": "text", "text": "First item"}
          ]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {"type": "text", "text": "Second item"}
          ]
        }
      ]
    }
  ]
}
```

**Ordered list:**
```json
{
  "type": "orderedList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {"type": "text", "text": "First item"}
          ]
        }
      ]
    }
  ]
}
```

**Nested lists:**
```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {"type": "text", "text": "Parent item"}
          ]
        },
        {
          "type": "bulletList",
          "content": [
            {
              "type": "listItem",
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {"type": "text", "text": "Nested item"}
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Code Blocks

**Code block with language:**
```json
{
  "type": "codeBlock",
  "attrs": {"language": "javascript"},
  "content": [
    {
      "type": "text",
      "text": "function hello() {\n  console.log('Hello');\n}"
    }
  ]
}
```

**Supported languages:** javascript, python, java, typescript, bash, sql, json, xml, html, css, etc.

**Code block without language:**
```json
{
  "type": "codeBlock",
  "content": [
    {"type": "text", "text": "Plain code block"}
  ]
}
```

### Mentions

**User mention:**
```json
{
  "type": "mention",
  "attrs": {
    "id": "557058:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
}
```

**Note**: Get user account ID from Jira user profile or API.

### Panels (Colored Blocks)

⚠️ **NOT supported in comments** - Use regular paragraphs instead. Works in descriptions only.

**Info panel:**
```json
{
  "type": "panel",
  "attrs": {"panelType": "info"},
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "This is an info panel"}
      ]
    }
  ]
}
```

**Panel types:** `info`, `note`, `warning`, `error`, `success`

### Block Quote

```json
{
  "type": "blockquote",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "This is a quote"}
      ]
    }
  ]
}
```

### Horizontal Rule

```json
{
  "type": "rule"
}
```

### Hard Break

**Line break within paragraph:**
```json
{
  "type": "paragraph",
  "content": [
    {"type": "text", "text": "First line"},
    {"type": "hardBreak"},
    {"type": "text", "text": "Second line"}
  ]
}
```

### Emoji

```json
{
  "type": "emoji",
  "attrs": {
    "shortName": ":smile:",
    "id": "1f604",
    "text": "😄"
  }
}
```

### Date

```json
{
  "type": "date",
  "attrs": {
    "timestamp": "1672531200000"
  }
}
```

### Ready-to-Use Templates

**Status update with formatting:**
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Status: ", "marks": [{"type": "strong"}]},
        {"type": "text", "text": "Completed ✓", "marks": [{"type": "strong"}, {"type": "em"}]}
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Next steps: Review and merge PR"}
      ]
    }
  ]
}
```

**Bug report with code:**
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Found a bug in the authentication handler:", "marks": [{"type": "strong"}]}
      ]
    },
    {
      "type": "codeBlock",
      "attrs": {"language": "javascript"},
      "content": [
        {"type": "text", "text": "if (token === undefined) {\n  // Missing validation\n}"}
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Expected behavior: Should throw an error when token is undefined"}
      ]
    }
  ]
}
```

**Release notes (for descriptions only - uses heading and panel):**
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 3},
      "content": [
        {"type": "text", "text": "Release v2.5.0"}
      ]
    },
    {
      "type": "panel",
      "attrs": {"panelType": "success"},
      "content": [
        {
          "type": "paragraph",
          "content": [
            {"type": "text", "text": "Ready for production deployment"}
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "New features:", "marks": [{"type": "strong"}]}
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Enhanced authentication"}
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Performance improvements"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Release notes (comment-safe version):**
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Release v2.5.0", "marks": [{"type": "strong"}]}
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "✅ Ready for production deployment", "marks": [{"type": "em"}]}
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "New features:", "marks": [{"type": "strong"}]}
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Enhanced authentication"}
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Performance improvements"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Integration with Claude Code

When using this skill in Claude Code:

1. **Always check authentication first**: Run `acli jira auth login --web` if needed
2. **Use bash_tool**: Execute acli commands using bash_tool
3. **Parse output**: Use `--json` flag for programmatic parsing
4. **Handle errors**: Check return codes and provide helpful error messages
5. **Confirm destructive operations**: Always warn before delete/bulk operations
6. **Use JQL for filtering**: Prefer JQL over manual key lists for bulk operations

## Common Use Cases

### Daily Workflow

```bash
# View your assigned work items
acli jira workitem search --jql "assignee = currentUser() AND status != Done"

# Transition work to in progress
acli jira workitem transition --key "KEY-1" --status "In Progress"

# Add comment
acli jira workitem comment create --key "KEY-1" --body "Started working on this"
```

### Bulk Updates

```bash
# Reassign all open items in a sprint
acli jira workitem edit \
  --jql "sprint = 'Sprint 10' AND status != Done" \
  --assignee "new-owner@example.com"

# Close all resolved items
acli jira workitem transition \
  --jql "project = TEAM AND resolution is not EMPTY" \
  --status "Done"
```

### Project Migration

```bash
# Clone all items from one project to another
acli jira workitem clone \
  --jql "project = OLDTEAM" \
  --to-project "NEWTEAM"

# Archive old project
acli jira project archive --project-key "OLDTEAM"
```

### Reporting

```bash
# Export all items to CSV
acli jira workitem search \
  --jql "project = TEAM AND created >= -30d" \
  --fields "key,summary,status,assignee,created" \
  --csv > report.csv

# Count items by status
acli jira workitem search --jql "project = TEAM AND status = 'To Do'" --count
acli jira workitem search --jql "project = TEAM AND status = 'In Progress'" --count
acli jira workitem search --jql "project = TEAM AND status = 'Done'" --count
```

## Help and Documentation

Get help for any command:

```bash
# Main help
acli --help

# Jira commands help
acli jira --help

# Work item commands help
acli jira workitem --help

# Specific command help
acli jira workitem create --help
```

## Important Notes

- **Work items vs Issues**: ACLI uses "workitem" terminology instead of "issue"
- **Authentication required**: Must authenticate before using any commands
- **Cloud only**: ACLI is for Jira Cloud, not Data Center or Server
- **Atlassian Government Cloud**: Not supported
- **Pagination**: Use `--paginate` for large result sets
- **Rate limits**: Be mindful of API rate limits for bulk operations
