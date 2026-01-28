---
name: folder
description: Display project folder contents in the TriClaude FOLDER panel
---

# Folder Browser Skill

Displays the current project's file/folder structure in the dedicated FOLDER panel within TriClaude.

## Trigger Phrases

- "show folder"
- "open folder"
- "show files"
- "folder view"
- "show project files"
- "browse folder"

## How It Works

1. Reads the current project directory structure
2. Generates styled HTML with file listing
3. Sends to A2UI sidecar with `<!-- FOLDER:START -->` markers
4. Displays in the FOLDER panel (separate from A2UI)

## Execution Steps

### Step 1: Get Project Path

Determine the project path from:
- Current working directory
- Or ask user if unclear

### Step 2: Generate File Listing

```bash
# Get directory listing with details
ls -la "$PROJECT_PATH" | head -50
```

### Step 3: Get A2UI Log Path

Find the A2UI log path from the terminal startup message:
```
A2UI VISUALIZATION: Write HTML to /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/<terminal_id>/a2ui_input.log
```

### Step 4: Generate and Send HTML

Write folder HTML with FOLDER markers to the A2UI log file.

**Template:**

```bash
cat << 'FOLDER_EOF' >> $A2UI_LOG
<!-- FOLDER:START -->
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  height: 100%;
  background: #0f172a;
  color: #e2e8f0;
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 12px;
}
.container {
  padding: 16px;
  height: 100%;
  overflow: auto;
}
.header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 12px;
  border-bottom: 1px solid #334155;
  margin-bottom: 12px;
}
.header svg {
  width: 20px;
  height: 20px;
  color: #f59e0b;
}
.header h1 {
  font-size: 14px;
  font-weight: 600;
  color: #f8fafc;
}
.path {
  font-size: 11px;
  color: #64748b;
  margin-bottom: 16px;
  word-break: break-all;
}
.file-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.15s;
}
.file-item:hover {
  background: #1e293b;
}
.file-icon {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.file-icon.folder { color: #f59e0b; }
.file-icon.file { color: #64748b; }
.file-icon.code { color: #3b82f6; }
.file-icon.config { color: #a855f7; }
.file-icon.doc { color: #22c55e; }
.file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.file-name.folder { color: #f59e0b; font-weight: 500; }
.file-size {
  color: #64748b;
  font-size: 10px;
  flex-shrink: 0;
}
.file-date {
  color: #475569;
  font-size: 10px;
  flex-shrink: 0;
  width: 80px;
  text-align: right;
}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
    </svg>
    <h1>$PROJECT_NAME</h1>
  </div>
  <div class="path">$PROJECT_PATH</div>
  <div class="file-list">
    $FILE_ITEMS
  </div>
</div>
</body>
</html>
<!-- FOLDER:END -->
FOLDER_EOF
```

### Step 5: Generate File Items

For each file/directory, generate an item:

**Directory item:**
```html
<div class="file-item">
  <div class="file-icon folder">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M10 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V8a2 2 0 00-2-2h-8l-2-2z"/></svg>
  </div>
  <span class="file-name folder">dirname/</span>
  <span class="file-size">-</span>
  <span class="file-date">Jan 15</span>
</div>
```

**File item:**
```html
<div class="file-item">
  <div class="file-icon file">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
  </div>
  <span class="file-name">filename.txt</span>
  <span class="file-size">1.2K</span>
  <span class="file-date">Jan 15</span>
</div>
```

### File Type Icon Classes

| Extension | Class |
|-----------|-------|
| Directories | `folder` |
| `.js`, `.ts`, `.tsx`, `.py`, `.rs` | `code` |
| `.json`, `.yaml`, `.toml`, `.env` | `config` |
| `.md`, `.txt`, `.rst` | `doc` |
| Everything else | `file` |

## Complete Bash Script

Use this script to generate and display the folder:

```bash
#!/bin/bash
PROJECT_PATH="${1:-$(pwd)}"
PROJECT_NAME=$(basename "$PROJECT_PATH")
A2UI_LOG="${A2UI_LOG:-/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/default/a2ui_input.log}"

# Generate file items HTML
FILE_ITEMS=""
while IFS= read -r line; do
  # Parse ls -la output
  perms=$(echo "$line" | awk '{print $1}')
  size=$(echo "$line" | awk '{print $5}')
  month=$(echo "$line" | awk '{print $6}')
  day=$(echo "$line" | awk '{print $7}')
  name=$(echo "$line" | awk '{for(i=9;i<=NF;i++) printf "%s ", $i; print ""}' | xargs)

  # Skip . and .. and empty
  [[ "$name" == "." || "$name" == ".." || -z "$name" ]] && continue

  # Determine if directory
  if [[ "${perms:0:1}" == "d" ]]; then
    icon_class="folder"
    icon_svg='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M10 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V8a2 2 0 00-2-2h-8l-2-2z"/></svg>'
    name_class="folder"
    name="${name}/"
    size="-"
  else
    # Determine file type
    ext="${name##*.}"
    case "$ext" in
      js|ts|tsx|jsx|py|rs|go|java|c|cpp|h) icon_class="code" ;;
      json|yaml|yml|toml|env|ini|conf) icon_class="config" ;;
      md|txt|rst|doc) icon_class="doc" ;;
      *) icon_class="file" ;;
    esac
    icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
    name_class=""
    # Format size
    if [[ "$size" -gt 1048576 ]]; then
      size="$(echo "scale=1; $size/1048576" | bc)M"
    elif [[ "$size" -gt 1024 ]]; then
      size="$(echo "scale=1; $size/1024" | bc)K"
    fi
  fi

  FILE_ITEMS+="<div class=\"file-item\"><div class=\"file-icon $icon_class\">$icon_svg</div><span class=\"file-name $name_class\">$name</span><span class=\"file-size\">$size</span><span class=\"file-date\">$month $day</span></div>"
done < <(ls -la "$PROJECT_PATH" 2>/dev/null | tail -n +2)

# Write to A2UI log
cat << FOLDER_EOF >> "$A2UI_LOG"
<!-- FOLDER:START -->
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; background: #0f172a; color: #e2e8f0; font-family: 'SF Mono', 'Fira Code', monospace; font-size: 12px; }
.container { padding: 16px; height: 100%; overflow: auto; }
.header { display: flex; align-items: center; gap: 8px; padding-bottom: 12px; border-bottom: 1px solid #334155; margin-bottom: 12px; }
.header svg { width: 20px; height: 20px; color: #f59e0b; }
.header h1 { font-size: 14px; font-weight: 600; color: #f8fafc; }
.path { font-size: 11px; color: #64748b; margin-bottom: 16px; word-break: break-all; }
.file-list { display: flex; flex-direction: column; gap: 2px; }
.file-item { display: flex; align-items: center; gap: 10px; padding: 6px 8px; border-radius: 4px; cursor: pointer; transition: background 0.15s; }
.file-item:hover { background: #1e293b; }
.file-icon { width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.file-icon.folder { color: #f59e0b; }
.file-icon.file { color: #64748b; }
.file-icon.code { color: #3b82f6; }
.file-icon.config { color: #a855f7; }
.file-icon.doc { color: #22c55e; }
.file-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.file-name.folder { color: #f59e0b; font-weight: 500; }
.file-size { color: #64748b; font-size: 10px; flex-shrink: 0; }
.file-date { color: #475569; font-size: 10px; flex-shrink: 0; width: 80px; text-align: right; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
    <h1>$PROJECT_NAME</h1>
  </div>
  <div class="path">$PROJECT_PATH</div>
  <div class="file-list">
$FILE_ITEMS
  </div>
</div>
</body>
</html>
<!-- FOLDER:END -->
FOLDER_EOF

echo "Folder view sent to FOLDER panel"
```

## TriClaude Integration

This skill requires TriClaude to have the FOLDER panel enabled. The panel:
- Uses a separate toggle button (cyan/teal color)
- Displays content sent with `<!-- FOLDER:START -->` markers
- Works independently of the A2UI visualization panel

## Example Session

```
User: show folder
Agent:
1. Detects CWD is /home/yousuf/local_workspaces/skills
2. Generates file listing HTML
3. Writes to A2UI log with FOLDER markers
4. Says: "Folder view displayed in FOLDER panel"
```

## Notes

- The folder view is static (generated at time of request)
- To refresh, say "show folder" again
- Subdirectories can be viewed by specifying the path: "show folder src/"
