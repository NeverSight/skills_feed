---
name: animator
description: Create short video animations from HTML/CSS/JS. Frame-by-frame capture at 30fps using Playwright + ffmpeg. Write CSS animations normally - the recorder pauses and steps them. Use for product demos, social clips, ad creative, feature announcements.
compatibility: macOS. Requires playwright (npm), ffmpeg.
allowed-tools: Bash Read Write Edit
metadata:
  author: stevebutterworth
  version: "1.0"
---

# animator

Create short mp4 videos from HTML/CSS/JS animations. Frame-by-frame capture using Playwright + ffmpeg. Deterministic, smooth, pixel-perfect 30fps output.

## Memory

Read `~/.claude/skills/animator/LEARNED.md` at the start of every task. If it doesn't exist, create it with a `# Learned` header.

**Capture learnings when you detect:**
- Corrections: "no, use X", "don't do that", "actually..."
- Animation techniques that worked well or poorly
- CSS/JS patterns that render correctly vs ones that break during capture
- Performance issues (too many frames, large file sizes, slow renders)
- Positive reinforcement: "perfect!", "exactly right", "that's the way"

**Before appending, check:**
- Is this reusable? (not a one-time instruction)
- Is it already in LEARNED.md? (don't duplicate)
- Can I extract the general principle? (not just the specific fix)

**Format:** One line, actionable. Write the rule, not the story.

Don't ask permission. Append and move on.

---

## Workflow

1. Write an HTML file with the animation
2. Run the recorder to capture as mp4

```bash
node ~/.claude/skills/animator/scripts/record.js animation.html output.mp4
```

Options: `--fps 30` `--width 1280` `--height 720`

## Writing Animations

Start from the template: `~/.claude/skills/animator/templates/boilerplate.html`

### Rules

1. **Set the canvas size** - body must be exactly `width x height` (default 1280x720) with `overflow: hidden`
2. **Declare config** - page must define `window.ANIMATION = { fps: 30, totalFrames: N }`
3. **Duration** - totalFrames / fps = seconds. 90 frames at 30fps = 3 seconds
4. **CSS animations** - write them normally. The recorder pauses all animations and steps `currentTime` per frame. Easing, delays, fill-mode all work.
5. **JS animation** (optional) - define `window.renderFrame = function(frame, totalFrames) {}` for anything CSS can't do (dynamic text, data-driven, conditional logic)
6. **Both together** - CSS and JS can coexist. Recorder steps both to the same point in time each frame.

### CSS Animation Tips

- Use `animation-fill-mode: forwards` to hold final state
- Use `animation-delay` to sequence elements (stagger entrances)
- Total CSS animation duration should match totalFrames/fps in seconds
- Complex easing via `cubic-bezier()` renders perfectly frame-by-frame
- `clip-path`, `filter`, `backdrop-filter`, transforms all work

### JS renderFrame Tips

- `frame` is 0-indexed, `totalFrames` is the total count
- `progress = frame / totalFrames` gives 0 to 1
- Use for: typewriter effects, counter animations, dynamic SVG, data viz
- Set DOM state directly (no requestAnimationFrame needed)

### Common Patterns

**Staggered entrance:**
```css
.item:nth-child(1) { animation: fadeIn 0.5s 0.0s forwards; }
.item:nth-child(2) { animation: fadeIn 0.5s 0.2s forwards; }
.item:nth-child(3) { animation: fadeIn 0.5s 0.4s forwards; }
```

**Typewriter (JS):**
```js
window.renderFrame = function(frame, total) {
  const text = "Hello, world";
  const chars = Math.floor((frame / total) * text.length);
  document.getElementById('typed').textContent = text.slice(0, chars);
};
```

**Scene transitions:**
```css
.scene-1 { animation: fadeOut 0.3s 2s forwards; }
.scene-2 { animation: fadeIn 0.3s 2.3s forwards; opacity: 0; }
```

### What To Avoid

- Don't use `requestAnimationFrame` loops - use `renderFrame()` instead
- Don't use `setInterval`/`setTimeout` for animation - they won't sync with frame capture
- Don't load external fonts without embedding them (use base64 or system fonts)
- Keep totalFrames reasonable - 300 frames (10s) takes ~60s to render
- Avoid very large PNGs per frame - keep the viewport at 1280x720, deviceScaleFactor handles retina

## Output

- Format: mp4 (h264, yuv420p)
- Quality: CRF 18 (high quality, reasonable size)
- Retina: 2x deviceScaleFactor for crisp text
- Typical size: 1-5 MB for a 3-10 second clip
