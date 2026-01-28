---
name: cli-demo-gif
version: 1.0.0
description: Generate CLI demo GIFs using vhs (Charmbracelet). Use when creating terminal recordings for README files or documentation.
---

# CLI Demo GIF Generator

Create polished terminal demo GIFs using [vhs](https://github.com/charmbracelet/vhs).

## Prerequisites

```bash
brew install vhs
```

## Usage

### 1. Create tape file

Place in `docs/demo/` to keep root clean:

```bash
mkdir -p docs/demo
```

### 2. Tape file structure

```tape
# Description comment
Output docs/demo/demo.gif

Set Shell "bash"
Set FontSize 16
Set Width 900
Set Height 500
Set Padding 20
Set Theme "Catppuccin Mocha"
Set TypingSpeed 50ms

# Commands here
Type "command --help"
Enter
Sleep 2s
```

### 3. For unpublished CLI packages

Use Hide/Show to set up aliases silently before the visible demo:

```tape
# Set up alias without showing it
Hide
Type "alias mycli='bun run src/cli/index.ts'"
Enter
Sleep 500ms
Show

# Now show the demo with clean commands
Type "mycli --help"
Enter
Sleep 2s
```

### 4. Generate GIF

```bash
vhs docs/demo/cli.tape
```

## Tape Commands Reference

| Command | Description |
|---------|-------------|
| `Output <path>` | Output file path (.gif, .mp4, .webm) |
| `Set Shell "bash"` | Shell to use |
| `Set FontSize <n>` | Font size (16 recommended) |
| `Set Width <n>` | Terminal width in pixels |
| `Set Height <n>` | Terminal height in pixels |
| `Set Padding <n>` | Padding around terminal |
| `Set Theme "<name>"` | Color theme |
| `Set TypingSpeed <duration>` | Delay between keystrokes |
| `Type "<text>"` | Type text |
| `Enter` | Press enter |
| `Sleep <duration>` | Wait (e.g., 2s, 500ms) |
| `Hide` | Stop recording |
| `Show` | Resume recording |
| `Ctrl+C` | Send interrupt |

## Recommended Themes

- `Catppuccin Mocha` - dark, modern
- `Dracula` - dark purple
- `Tokyo Night` - dark blue
- `One Dark` - dark
- `GitHub Dark` - GitHub's dark theme

## Tips

- Keep GIFs under 1MB for fast loading
- Use `Sleep` generously so viewers can read output
- 50ms typing speed looks natural
- 900x500 works well for most CLIs
- Show 3-5 commands max per GIF
