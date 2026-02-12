---
name: slidev-presenter-mode
description: Use Slidev presenter mode effectively. Use this skill for speaker notes, timer, remote control, and dual-screen presentations.
---

# Slidev Presenter Mode

This skill covers using Slidev's presenter mode for professional presentations, including speaker notes, timers, slide overview, and remote control features.

## When to Use This Skill

- Preparing for a live presentation
- Adding speaker notes
- Using dual-screen setup
- Remote control from phone
- Rehearsing with timer

## Accessing Presenter Mode

### Via Navigation

Click the presenter icon in the navigation bar (bottom-left).

### Via URL

Navigate directly to:

```
http://localhost:3030/presenter
```

### Keyboard Shortcut

Press `p` to toggle presenter mode (depends on configuration).

## Presenter Interface

The presenter view shows:

1. **Current Slide** - What audience sees
2. **Next Slide Preview** - Upcoming slide
3. **Speaker Notes** - Your notes
4. **Timer** - Elapsed/remaining time
5. **Slide Navigator** - Quick jump to any slide
6. **Click Counter** - Current animation state

## Speaker Notes

### Adding Notes

Use HTML comments at the end of a slide:

```markdown
# My Slide

Content visible to audience.

<!--
Speaker notes here:
- Remember to mention X
- Demo the feature
- Ask for questions
-->
```

### Markdown in Notes

Notes support Markdown formatting:

```markdown
<!--
## Key Points

1. **Important**: Emphasize this
2. *Note*: Optional detail
3. `Code reference`: Show in demo

> Quote to read aloud
-->
```

### Multi-line Notes

```markdown
<!--
First paragraph of notes.

Second paragraph with more details.

- Bullet point 1
- Bullet point 2
-->
```

### Notes Best Practices

```markdown
<!--
TIMING: 2 minutes

KEY MESSAGE:
Our solution reduces deployment time by 50%

REMEMBER TO:
- [ ] Show the demo
- [ ] Mention the case study
- [ ] Ask if there are questions

TRANSITION:
"Now let's look at how this works in practice..."
-->
```

## Dual-Screen Setup

### Recommended Setup

1. Open browser in **Play mode** on external display:
   ```
   http://localhost:3030
   ```

2. Open browser in **Presenter mode** on your screen:
   ```
   http://localhost:3030/presenter
   ```

3. Share/project the Play mode window to audience

### Automatic Sync

Both windows automatically synchronize:
- Navigation stays in sync
- Click animations sync
- Drawings sync (if enabled)

## Timer Features

### Starting/Stopping

- Click the timer to start/pause
- Click again to resume

### Timer Display

Shows:
- Elapsed time
- Can be configured for countdown

### Timer Tips

- Start timer when beginning presentation
- Use for time management
- Visible only to presenter

## Remote Control

### From Another Device

1. Start server with remote access:
   ```bash
   slidev --remote
   ```

2. Note the displayed URL (or use local network IP)

3. Open URL on phone/tablet

4. Control presentation remotely

### Password Protection

```bash
slidev --remote=your_password
```

Then access with:
```
http://[ip]:3030/presenter?password=your_password
```

### QR Code

Slidev can display a QR code for easy mobile access.

## Overview Mode

### Accessing Overview

- Press `o` key
- Or navigate to `/overview`

### Features

- See all slides at once
- Click to jump to any slide
- Edit notes inline (in overview mode)
- Preview click animations

## Navigation in Presenter Mode

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` / `→` | Next animation/slide |
| `←` | Previous animation/slide |
| `↑` / `↓` | Previous/next slide (skip animations) |
| `o` | Overview mode |
| `g` | Go to slide number |
| `Esc` | Exit fullscreen/overview |

### Touch/Swipe

On touch devices:
- Swipe left: Next slide
- Swipe right: Previous slide

### Click Areas

In presenter mode:
- Left side: Previous
- Right side: Next

## Presenter Mode Configuration

### In Frontmatter

```yaml
---
# Remote access settings
remote: true

# Presenter notes settings
presenter: true
---
```

### Disable Presenter for Shared Links

When sharing:
```bash
slidev build
```

The built version doesn't include presenter mode by default.

## Drawing Tools

### Enabling Drawings

```yaml
---
drawings:
  enabled: true
  persist: false
  syncAll: true
---
```

### Using Drawings

- Click pen icon in presenter mode
- Draw on current slide
- Drawings sync to audience view

### Presenter-Only Drawings

```yaml
---
drawings:
  presenterOnly: true
---
```

Only presenter can draw, visible to all.

## Recording Features

### Built-in Recording

1. Click record button in presenter mode
2. Select screen/window to record
3. Optionally enable camera
4. Start recording

### Recording Options

- Screen only
- Screen + camera
- Camera picture-in-picture

## Presentation Workflow

### Before Presenting

1. **Test Setup**: Verify dual-screen works
2. **Review Notes**: Read through all speaker notes
3. **Practice**: Run through with timer
4. **Check Animations**: Verify all clicks work
5. **Test Remote**: If using phone control

### During Presentation

1. **Use Notes**: Glance at key points
2. **Watch Timer**: Stay on schedule
3. **Preview Next**: Know what's coming
4. **Control Pace**: Use click counter

### Checklist

```markdown
PRE-PRESENTATION:
- [ ] Laptop charged/plugged in
- [ ] Projector/display connected
- [ ] Correct resolution set
- [ ] Browser in fullscreen (F11)
- [ ] Notifications disabled
- [ ] Presenter window on laptop screen
- [ ] Play window on projector

DURING:
- [ ] Timer started
- [ ] Notes visible
- [ ] Water nearby

POST:
- [ ] Save any drawings
- [ ] Export if needed
```

## Advanced Features

### Custom Presenter Layout

You can customize the presenter view through themes.

### Multiple Presenters

For co-presenting:
1. Both access presenter mode
2. Designate who controls navigation
3. Others can view but not control

### Rehearsal Mode

```bash
# Practice without audience
slidev --open
```

Then use presenter mode locally to practice.

## Troubleshooting

### Windows Not Syncing

1. Check both are on same URL base
2. Refresh both windows
3. Check network/firewall

### Notes Not Showing

1. Verify comment syntax: `<!-- notes -->`
2. Notes must be at end of slide
3. Check for syntax errors before notes

### Timer Reset

Timer persists during session but resets on page reload.

## Output Format

When preparing presenter content:

```markdown
# [Slide Title]

[Visible content for audience]

<!--
TIMING: [X minutes]

KEY POINTS:
- [Main message to convey]
- [Secondary point]

DEMO/ACTION:
- [What to show/do]

TRANSITION TO NEXT:
"[Connecting phrase to next slide]"
-->
```

**PRESENTER SETUP:**
1. URL for audience: `http://localhost:3030`
2. URL for presenter: `http://localhost:3030/presenter`
3. Remote URL: `http://[IP]:3030/?password=[pass]`
