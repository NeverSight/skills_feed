---
name: figma
description: Extract design data from Figma files. Use for getting design tokens, component specs, and generating code from Figma designs.
---

# Figma Integration

Extract design data and generate code from Figma.

## Prerequisites

Figma API token:
```bash
export FIGMA_ACCESS_TOKEN=figd_xxxxx
```

Get token from: Figma > Settings > Account > Personal Access Tokens

Optional: Install figma-export CLI for component/style exports:
```bash
bun add -g @figma-export/cli
```

## CLI Reference (figma-export)

For exporting components and styles, use the CLI:

### Export Components

```bash
# Export components to SVG
figma-export components FILE_KEY -o ./output

# With config file
figma-export use-config .figmaexportrc.js
```

### Export Styles

```bash
# Export styles as CSS
figma-export styles FILE_KEY -o ./styles
```

### Config File Example

Create `.figmaexportrc.js`:
```javascript
module.exports = {
  commands: [
    ['components', {
      fileId: 'YOUR_FILE_KEY',
      onlyFromPages: ['Icons'],
      outputters: [
        require('@figma-export/output-components-as-svg')({
          output: './icons'
        })
      ]
    }]
  ]
};
```

Then run:
```bash
figma-export use-config
```

## API Reference (curl)

### Get File

```bash
FILE_KEY="your-file-key"  # From Figma URL
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY" | jq
```

### Get Specific Node

```bash
NODE_ID="1:2"  # Node ID from Figma
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$NODE_ID" | jq
```

### Get Images

```bash
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/images/$FILE_KEY?ids=$NODE_ID&format=png&scale=2" | jq
```

### Get Comments

```bash
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/comments" | jq
```

### Get File Versions

```bash
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/versions" | jq
```

## Extract Design Tokens

### Get Styles

```bash
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/styles" | jq
```

### Extract Colors

```bash
#!/bin/bash
FILE_KEY=$1

# Get file with styles
STYLES=$(curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY" | jq '.styles')

# Get style nodes
STYLE_IDS=$(echo $STYLES | jq -r 'keys | join(",")')

curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$STYLE_IDS" | \
  jq '.nodes | to_entries | map(select(.value.document.type == "RECTANGLE")) |
      map({
        name: .value.document.name,
        color: .value.document.fills[0].color
      })'
```

### Extract Typography

```bash
curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY" | \
  jq '[.. | objects | select(.type == "TEXT") |
      {
        name: .name,
        fontFamily: .style.fontFamily,
        fontSize: .style.fontSize,
        fontWeight: .style.fontWeight,
        lineHeight: .style.lineHeightPx
      }] | unique'
```

## Component Inspection

### List Components

```bash
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/components" | jq
```

### Get Component Details

```bash
COMPONENT_ID="1:234"
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$COMPONENT_ID" | jq
```

### Export Component as SVG

```bash
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/images/$FILE_KEY?ids=$COMPONENT_ID&format=svg" | jq -r '.images | to_entries[0].value'
```

## Generate Code

### Design to Code with AI

```bash
# Get component node
NODE=$(curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$NODE_ID" | jq '.nodes | to_entries[0].value')

# Generate code
gemini -m pro -o text -e "" "Generate React component code from this Figma data:

$NODE

Requirements:
- Use Tailwind CSS
- TypeScript with proper types
- Match dimensions and spacing
- Include all text content
- Handle responsive behavior"
```

### Extract Spacing Values

```bash
curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$NODE_ID" | \
  jq '[.. | objects | select(.type == "FRAME") |
      {
        name: .name,
        padding: {
          top: .paddingTop,
          right: .paddingRight,
          bottom: .paddingBottom,
          left: .paddingLeft
        },
        itemSpacing: .itemSpacing
      }]'
```

## Workflow Patterns

### Sync Design Tokens

```bash
#!/bin/bash
# figma-sync-tokens.sh

FILE_KEY=$1
OUTPUT=${2:-"tokens.json"}

# Fetch and extract
curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY" | \
  jq '{
    colors: [.. | objects | select(.type == "RECTANGLE" and .name | startswith("color/")) |
      {name: .name, value: .fills[0].color}],
    typography: [.. | objects | select(.type == "TEXT" and .name | startswith("text/")) |
      {name: .name, font: .style}]
  }' > $OUTPUT

echo "Tokens saved to $OUTPUT"
```

### Export Icons

```bash
#!/bin/bash
# export-icons.sh

FILE_KEY=$1
OUTPUT_DIR=${2:-"./icons"}

mkdir -p $OUTPUT_DIR

# Get all icon components
ICONS=$(curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/components" | \
  jq -r '.meta.components[] | select(.name | startswith("icon/")) | .node_id')

for icon_id in $ICONS; do
  # Get SVG URL
  SVG_URL=$(curl -sH "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
    "https://api.figma.com/v1/images/$FILE_KEY?ids=$icon_id&format=svg" | \
    jq -r '.images | to_entries[0].value')

  # Download
  NAME=$(echo $icon_id | tr ':' '-')
  curl -s "$SVG_URL" > "$OUTPUT_DIR/$NAME.svg"
  echo "Exported: $NAME.svg"
done
```

## Best Practices

1. **Use file key from URL** - `figma.com/file/FILEKEY/...`
2. **Cache responses** - API has rate limits
3. **Use node IDs** - More efficient than full file
4. **Extract at build time** - Not runtime
5. **Version your tokens** - Track design changes
6. **Validate extractions** - Figma structure varies
