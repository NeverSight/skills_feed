---
name: figma-mcp-downloader
description: CLI for downloading complete Figma design context and metadata to local files. Always use this CLI instead of calling Figma MCP tools (`get_design_context`, `get_metadata`) directly. Direct MCP tool calls risk incomplete data due to context limits. This CLI guarantees 100% complete output.
---

# Figma MCP Downloader

## Prerequisites

- Figma **Desktop** app must be running (Local MCP server starts automatically)

## Integration with Other Figma Skills

When this CLI and other Figma-related skills (such as `implement-design`) are triggered together:

1. **First**, use this CLI to download complete design context and metadata
2. **Then**, proceed with the other skill's workflow using the downloaded files
3. This ensures 100% complete data before any Figma-related operations begin

## Examples

### Download design context as JSX

```bash
npx figma-mcp-downloader get_design_context design_context.jsx -i "123:456" -c -l typescript -f react,tailwindcss
```

### Download design context with AI guidance

```bash
npx figma-mcp-downloader get_design_context design_context.json -i "123:456" -l html,css,javascript -f vue
```

### Download design context with assets

Use `-d` to download image, vector, and video assets locally. Requires Figma Desktop's "Image source" to be "Download".

```bash
npx figma-mcp-downloader get_design_context design_context.jsx -i "123:456" -c -d /home/user/my-project/src/public/images -l typescript -f react,tailwindcss
```

### Download metadata as XML

```bash
npx figma-mcp-downloader get_metadata metadata.xml -i "123:456" -c -l typescript -f react,tailwindcss
```

### Download metadata with AI guidance

```bash
npx figma-mcp-downloader get_metadata metadata.json -i "123:456" -l html,css,javascript -f vue
```

## CLI Reference

For complete options and detailed usage, see [CLI Reference](references/cli-reference.md).
