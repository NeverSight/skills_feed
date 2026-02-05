---
name: screenshot
description: "Find and display recent screenshots. Triggers: screenshot, check screenshot, show screenshot, recent screenshot, last screenshot."
compatibility: "Windows, macOS, Linux"
allowed-tools: "Bash, Glob, Read"
depends-on: []
related-skills: []
---

# Screenshot Viewer

Quickly find and display recent screenshots from common screenshot directories.

## Usage

```
/screenshot          # Show last 5 screenshots (default)
/screenshot 1        # Show only the most recent
/screenshot 10       # Show last 10 screenshots
```

## How It Works

1. **Auto-detect screenshot locations** - Checks common directories in this order:
   - Windows: `Pictures\Screenshots`, ShareX, Greenshot, OneDrive\Screenshots
   - macOS: `~/Desktop`, `~/Screenshots`
   - Linux: `~/Pictures`, `~/Desktop`

2. **Find recent screenshots** - Uses Glob to find image files (png, jpg, jpeg, gif, webp) sorted by modification time

3. **Display visually** - Uses Read tool to show screenshots so you can analyze and discuss them

## Implementation

### Step 1: Detect Screenshot Directory

Check common locations and use the first one that exists:

**Windows:**
```bash
# Priority order
1. %USERPROFILE%\Pictures\Screenshots           # Windows 11 native
2. %USERPROFILE%\Documents\ShareX\Screenshots   # ShareX
3. %USERPROFILE%\Pictures\Greenshot             # Greenshot
4. %USERPROFILE%\OneDrive\Pictures\Screenshots  # OneDrive sync
5. %USERPROFILE%\Pictures                       # Fallback
```

**macOS:**
```bash
1. ~/Desktop              # Default macOS location
2. ~/Screenshots          # Custom folder
3. ~/Pictures             # Fallback
```

**Linux:**
```bash
1. ~/Pictures/Screenshots # GNOME/KDE
2. ~/Pictures             # Fallback
3. ~/Desktop              # Alternative
```

### Step 2: Find Recent Screenshots

Use Glob to find image files, sorted by modification time:

```bash
# Find all image files in screenshot directory
fd -e png -e jpg -e jpeg -e gif -e webp . "$SCREENSHOT_DIR" --max-depth 1 -t f --exec stat --format="%Y %n" {} \; | sort -rn | head -n $COUNT
```

Or using native tools:

**Windows (PowerShell):**
```powershell
Get-ChildItem "$env:USERPROFILE\Pictures\Screenshots" -File |
  Where-Object {$_.Extension -match '\.(png|jpg|jpeg|gif|webp)$'} |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First $COUNT
```

**Unix (Bash):**
```bash
find "$SCREENSHOT_DIR" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.webp" \) -printf '%T@ %p\n' | sort -rn | head -n $COUNT | cut -d' ' -f2-
```

### Step 3: Display Screenshots

For each screenshot found, use Read tool to display it visually:

```
Found 3 screenshots in C:\Users\...\Pictures\Screenshots

1. Screenshot_2026-01-28_14-32-10.png (45 KB, 2 minutes ago)
[Read tool displays image visually]

2. Screenshot_2026-01-28_14-15-03.png (128 KB, 19 minutes ago)
[Read tool displays image visually]

3. Screenshot_2026-01-28_13-58-22.png (67 KB, 36 minutes ago)
[Read tool displays image visually]
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `count` | 5 | Number of screenshots to show |

**Examples:**
- `/screenshot` - Show last 5
- `/screenshot 1` - Show only most recent
- `/screenshot 10` - Show last 10

## Output Format

```
Screenshots from [directory]

## Screenshot 1 of N
**File**: [filename]
**Size**: [size] KB
**Modified**: [time ago]

[Visual display of screenshot via Read tool]

## Screenshot 2 of N
...
```

## Edge Cases

### No Screenshot Directory Found

```
No screenshot directory found.

Checked locations:
  - C:\Users\...\Pictures\Screenshots (not found)
  - C:\Users\...\Documents\ShareX\Screenshots (not found)
  - C:\Users\...\Pictures\Greenshot (not found)

To use this skill, either:
  1. Take a screenshot (Win+Shift+S on Windows)
  2. Specify a custom directory: /screenshot --dir="C:\path\to\screenshots"
```

### No Screenshots Found

```
No screenshots found in C:\Users\...\Pictures\Screenshots

Directory exists but contains no image files (.png, .jpg, .jpeg, .gif, .webp)
```

### Count Exceeds Available

```
Found 3 screenshots (requested 10)

Showing all 3:
[displays all available screenshots]
```

## Performance

- **Fast** - Uses filesystem tools (fd or native) instead of reading all files
- **Efficient** - Only reads the exact number requested
- **Token-conscious** - Large screenshots are automatically resized by Read tool

## Custom Directory (Optional)

To use a non-standard directory:

```
/screenshot 5 --dir="C:\Custom\Path"
```

Or create a project-specific config in `.claude/screenshot.json`:

```json
{
  "directory": "C:\\Custom\\Screenshots",
  "default_count": 3,
  "file_extensions": ["png", "jpg", "webp"]
}
```

## Integration

Works well with:
- `/explain` - Explain what's in the screenshot
- `/review` - Review UI/code in screenshot
- Browser automation tools - Verify screenshot matches expected state

## Notes

- Respects modification time (newest first)
- Ignores subdirectories (only top-level)
- Supports common image formats (png, jpg, jpeg, gif, webp)
- Works across Windows, macOS, Linux with platform-specific paths
