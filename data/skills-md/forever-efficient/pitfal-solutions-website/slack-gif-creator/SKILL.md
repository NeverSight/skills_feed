---
name: slack-gif-creator
description: Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."
license: Complete terms in LICENSE.txt
---

# Slack GIF Creator

A toolkit providing utilities and knowledge for creating animated GIFs optimized for Slack.

## Slack Requirements

**Dimensions:**
- Emoji GIFs: 128x128 (recommended)
- Message GIFs: 480x480

**Parameters:**
- FPS: 10-30 (lower is smaller file size)
- Colors: 48-128 (fewer = smaller file size)
- Duration: Keep under 3 seconds for emoji GIFs

## Core Workflow

```python
from PIL import Image, ImageDraw

# 1. Create frames
frames = []
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)
    # Draw your animation using PIL primitives
    frames.append(frame)

# 2. Save as GIF
frames[0].save(
    'output.gif',
    save_all=True,
    append_images=frames[1:],
    duration=100,  # ms per frame
    loop=0
)
```

## Drawing Graphics

### Drawing from Scratch
When drawing graphics from scratch, use PIL ImageDraw primitives:

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# Circles/ovals
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# Stars, triangles, any polygon
points = [(x1, y1), (x2, y2), (x3, y3)]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# Lines
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# Rectangles
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

## Animation Concepts

### Shake/Vibrate
Offset object position with oscillation using `math.sin()` or `math.cos()` with frame index.

### Pulse/Heartbeat
Scale object size rhythmically using `math.sin(t * frequency * 2 * math.pi)` for smooth pulse.

### Bounce
Object falls and bounces - use easing functions for landing.

### Spin/Rotate
Rotate object around center: `image.rotate(angle, resample=Image.BICUBIC)`

### Fade In/Out
Create RGBA image, adjust alpha channel, or use `Image.blend(image1, image2, alpha)`.

### Slide
Move object from off-screen to position with easing.

### Zoom
Scale and position for zoom effect - zoom in: scale from 0.1 to 2.0, crop center.

### Explode/Particle Burst
Create particles radiating outward with random angles and velocities.

## Optimization Strategies

1. **Fewer frames** - Lower FPS (10 instead of 20) or shorter duration
2. **Fewer colors** - Use 48 colors instead of 128
3. **Smaller dimensions** - 128x128 instead of 480x480
4. **Remove duplicates** - Skip identical frames

## Dependencies

```bash
pip install pillow imageio numpy
```
