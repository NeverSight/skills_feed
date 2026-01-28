---
name: figma
description: Figma REST API for accessing design files, comments, components, and projects. Use this skill to read file contents, export images, manage comments, and integrate with Figma workspaces.
vm0_secrets:
  - FIGMA_API_TOKEN
---

# Figma API

Access and manage design files, components, comments, and projects in Figma workspaces via REST API.

> Official docs: `https://developers.figma.com/docs/rest-api/`

---

## When to Use

Use this skill when you need to:

- **Read design files** and extract components, styles, and frames
- **Export images** from Figma designs in various formats (PNG, JPG, SVG, PDF)
- **Get file version history** and track changes
- **Manage comments** on design files
- **List projects and files** in a team
- **Access design tokens** and styles
- **Get component information** from design systems
- **Retrieve team and project metadata**

---

## Prerequisites

### Getting Your API Token

1. Log in to [Figma](https://www.figma.com/)
2. Go to **Settings** page: https://www.figma.com/settings
3. Scroll down to **Personal access tokens** section
4. Click **Generate new token**
5. Enter a token name (e.g., `vm0-skills-test`)
6. Click **Create** and **immediately copy the token** (format: `figd_...`)
   - The token is only shown once - save it securely
   - If lost, you must delete and create a new token

```bash
export FIGMA_API_TOKEN="figd_..."
```

### Verify Token

Test your token with this command:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/me" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"'
```

Expected response: Your user information (id, email, handle)

### Finding File Keys

Figma file URLs contain the file key:

```
URL: https://www.figma.com/design/abc123XYZ/My-Design-File
File Key: abc123XYZ
```

The file key is the alphanumeric string between `/design/` (or `/file/`) and the next `/`.

### Rate Limits

- 60 requests per minute per IP address
- 429 status code = rate limited, retry after delay

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq '.[0]'
> ```

## How to Use

All examples assume `FIGMA_API_TOKEN` is set.

Base URL: `https://api.figma.com/v1`

---

### 1. Get File

Retrieve complete file structure including frames, components, and styles. Replace `<your-file-key>` with your actual file key:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '{name, lastModified, version, document: .document.children[0].name}'
```

Get specific version:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>?version=123" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"'
```

---

### 2. Get File Nodes

Retrieve specific nodes from a file by node IDs. Replace `<your-file-key>` with your file key and `<node-ids>` with comma-separated node IDs (e.g., `1:2,1:3`):

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>/nodes?ids=<node-ids>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.nodes'
```

Node IDs can be found in the file structure or by appending `?node-id=X-Y` to the Figma URL.

---

### 3. Get File Images

Export nodes as images in PNG, JPG, SVG, or PDF format. Replace `<your-file-key>` with your file key and `<node-ids>` with comma-separated node IDs:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/images/<your-file-key>?ids=<node-ids>&format=png&scale=2" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.images'
```

**Parameters:**
- `format`: `png`, `jpg`, `svg`, `pdf` (default: `png`)
- `scale`: `0.5`, `1`, `2`, `4` (default: `1`)
- `svg_outline_text`: `true` to convert text to outlines in SVG
- `svg_include_id`: `true` to include node IDs in SVG

Download an exported image. Replace `<your-file-key>` with your file key and `<node-id>` with the actual node ID:

```bash
IMAGE_URL="$(bash -c 'curl -s -X GET "https://api.figma.com/v1/images/<your-file-key>?ids=<node-id>&format=png" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq -r '.images["<node-id>"]')"

curl -s -o output.png "$IMAGE_URL"
```

---

### 4. Get Image Fills

Get download URLs for all images used in a file. Replace `<your-file-key>` with your file key:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>/images" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.meta.images'
```

---

### 5. Get File Comments

List all comments on a file. Replace `<your-file-key>` with your file key:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>/comments" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.comments[] | {id, message: .message, user: .user.handle, created_at}'
```

---

### 6. Post Comment

Add a comment to a file. Replace `<your-file-key>` with your file key.

Write to `/tmp/figma_request.json`:

```json
{
  "message": "This looks great!",
  "client_meta": {"x": 100, "y": 200}
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.figma.com/v1/files/<your-file-key>/comments" -H "X-Figma-Token: ${FIGMA_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/figma_request.json'
```

To comment on a specific node, add `client_meta` with node coordinates.

---

### 7. Delete Comment

Delete a comment by ID. Replace `<your-file-key>` with your file key and `<comment-id>` with the comment ID:

```bash
curl -s -X DELETE "https://api.figma.com/v1/files/<your-file-key>/comments/<comment-id>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"
```

---

### 8. Get File Versions

List version history of a file. Replace `<your-file-key>` with your file key:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>/versions" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.versions[] | {id, created_at, label, description, user: .user.handle}'
```

---

### 9. Get Team Projects

List all projects in a team. Replace `<your-team-id>` with your team ID:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/teams/<your-team-id>/projects" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.projects[] | {id, name}'
```

To find your team ID, go to your Figma team page and extract it from the URL: `https://www.figma.com/files/team/<your-team-id>/TeamName`

---

### 10. Get Project Files

List all files in a project. Replace `<your-project-id>` with your project ID:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/projects/<your-project-id>/files" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.files[] | {key, name, last_modified}'
```

---

### 11. Get Team Components

Get all published components in a team. Replace `<your-team-id>` with your team ID:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/teams/<your-team-id>/components" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.meta.components[] | {key, name, description, containing_frame: .containing_frame.name}'
```

---

### 12. Get Component

Get metadata for a specific component. Replace `<your-component-key>` with your component key:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/components/<your-component-key>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '{key, name, description, containing_frame}'
```

---

### 13. Get Team Styles

Get all published styles (colors, text, effects, grids) in a team. Replace `<your-team-id>` with your team ID:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/teams/<your-team-id>/styles" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.meta.styles[] | {key, name, description, style_type}'
```

**Style types:** `FILL`, `TEXT`, `EFFECT`, `GRID`

---

### 14. Get Style

Get metadata for a specific style. Replace `<your-style-key>` with your style key:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/styles/<your-style-key>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '{key, name, description, style_type}'
```

---

### 15. Get Current User

Get information about the authenticated user:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/me" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '{id, email, handle, img_url}'
```

---

### 16. Get Team Members

List all members of a team. Replace `<your-team-id>` with your team ID:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/teams/<your-team-id>/members" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.members[] | {id, email: .user.email, handle: .user.handle, role}'
```

---

### 17. Get Component Sets

Get component sets (variants) in a file. Replace `<your-file-key>` with your file key:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>/component_sets" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.meta.component_sets[] | {key, name, description}'
```

---

### 18. Search Files

Search for files in a team (requires team ID). Replace `<your-team-id>` with your team ID and `<search-query>` with your search term:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/teams/<your-team-id>/files?name=<search-query>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.files[] | {key, name, last_modified}'
```

---

## Common Workflows

### Export All Frames as Images

Replace `<your-file-key>` with your file key. First, get all frame IDs:

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq -r '.document.children[0].children[] | select(.type=="FRAME") | .id' | paste -sd "," -
```

Then export frames (replace `<frame-ids>` with the comma-separated frame IDs from the previous response):

```bash
bash -c 'curl -s -X GET "https://api.figma.com/v1/images/<your-file-key>?ids=<frame-ids>&format=png&scale=2" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.images'
```

### Extract Design Tokens

Replace `<your-file-key>` with your file key:

```bash
# Get color styles
bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq '.styles | to_entries[] | select(.value.styleType == "FILL") | {name: .value.name, key: .value.key}'
```

### Monitor File Changes

Replace `<your-file-key>` with your file key:

```bash
# Get current version
CURRENT_VERSION=$(bash -c 'curl -s -X GET "https://api.figma.com/v1/files/<your-file-key>" -H "X-Figma-Token: ${FIGMA_API_TOKEN}"' | jq -r '.version')

echo "Current version: $CURRENT_VERSION"
```

---

## Understanding File Structure

Figma files have a hierarchical structure:

```
FILE
└── CANVAS (page)
    ├── FRAME
    │   ├── RECTANGLE
    │   ├── TEXT
    │   └── GROUP
    │       └── VECTOR
    └── FRAME
        └── COMPONENT
```

Common node types: `CANVAS`, `FRAME`, `GROUP`, `VECTOR`, `BOOLEAN_OPERATION`, `STAR`, `LINE`, `ELLIPSE`, `REGULAR_POLYGON`, `RECTANGLE`, `TEXT`, `SLICE`, `COMPONENT`, `COMPONENT_SET`, `INSTANCE`

---

## Guidelines

1. **Cache file data**: File requests can be large; cache results when possible
2. **Use webhooks**: For real-time updates, consider Figma webhooks instead of polling
3. **Respect rate limits**: Implement exponential backoff for 429 responses
4. **Version control**: Use `version` parameter to access specific file versions
5. **Optimize exports**: Use appropriate scale and format for image exports to reduce file size
6. **Node IDs**: Node IDs are in format `X:Y` (e.g., `1:2`) and must be URL-encoded in some endpoints
7. **Team scope**: Many operations require team-level access; ensure your token has team permissions
8. **Pagination**: Some endpoints return paginated results; check for `next_page` in responses

---

## API Reference

- Main Documentation: https://developers.figma.com/docs/rest-api/
- Authentication: https://developers.figma.com/docs/rest-api/authentication/
- API Endpoints: https://developers.figma.com/docs/api/
- Webhooks: https://developers.figma.com/docs/webhooks/
- Plugins: https://www.figma.com/plugin-docs/
- Token Settings: https://www.figma.com/settings (under Personal access tokens)
