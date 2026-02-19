---
name: video-motion-graphics
description: Use when creating After Effects compositions, Premiere Pro motion, video titles, explainer videos, or broadcast motion graphics.
---

# Video Motion Graphics

Apply Disney's 12 animation principles to After Effects, Premiere Pro, and video motion design.

## Quick Reference

| Principle | Motion Graphics Implementation |
|-----------|-------------------------------|
| Squash & Stretch | Overshoot expressions, elastic motion |
| Anticipation | Pre-movement, wind-up keyframes |
| Staging | Composition, depth, focus pulls |
| Straight Ahead / Pose to Pose | Frame-by-frame vs keyframe animation |
| Follow Through / Overlapping | Delayed layers, expression lag |
| Slow In / Slow Out | Graph editor curves, easing |
| Arc | Motion paths, rotation follows path |
| Secondary Action | Environment response, particle systems |
| Timing | 24/30/60fps considerations |
| Exaggeration | Scale beyond reality, dramatic motion |
| Solid Drawing | Z-space, 3D consistency, parallax |
| Appeal | Smooth, professional, emotionally resonant |

## Principle Applications

**Squash & Stretch**: Use scale property with different X/Y values. Overshoot expressions create elastic motion. Shape layers deform more naturally than pre-comps for organic squash.

**Anticipation**: Add 2-4 frames of reverse motion before primary action. Wind-up for reveals—slight scale down before scale up. Position anticipation: move opposite direction first.

**Staging**: Use depth of field to direct focus. Vignettes frame important content. Motion blur on secondary elements. Composition leads eye to focal point.

**Straight Ahead vs Pose to Pose**: Traditional frame-by-frame for character animation. Keyframe-based for graphic animation. Most motion graphics are pose-to-pose with expression refinement.

**Follow Through & Overlapping**: Use `valueAtTime()` expressions for lag. Stagger layer animation with offset. Secondary elements continue 4-8 frames past primary stop. Parent/child relationships with delayed response.

**Slow In / Slow Out**: Master the Graph Editor—never use linear keyframes. Easy Ease is starting point, customize curves. Bezier handles control acceleration. Speed graph shows velocity.

**Arc**: Enable motion path editing. Auto-orient rotation to path. Add roving keyframes for smooth arcs. Natural motion rarely travels in straight lines.

**Secondary Action**: Particles respond to primary motion. Shadows and reflections follow. Background elements shift with parallax. Audio waveforms drive visual elements.

**Timing**: 24fps: Cinematic feel, motion blur essential. 30fps: Broadcast standard, smoother. 60fps: Digital-first, very smooth. Hold frames (2s, 3s) for stylized timing.

**Exaggeration**: Motion graphics can push further than reality. Scale overshoots to 120-150%. Rotation extends past final. Color and effects can punctuate exaggeration.

**Solid Drawing**: 3D layers maintain spatial consistency. Parallax creates depth hierarchy. Consistent light direction across elements. Z-positioning creates believable space.

**Appeal**: Smooth interpolation, no jarring cuts. Color grading unifies composition. Typography has weight and personality. Motion feels intentional and professional.

## After Effects Techniques

### Overshoot Expression
```javascript
// Apply to any property for elastic overshoot
freq = 3;
decay = 5;
n = 0;
if (numKeys > 0) {
    n = nearestKey(time).index;
    if (key(n).time > time) n--;
}
if (n > 0) {
    t = time - key(n).time;
    amp = velocityAtTime(key(n).time - .001);
    w = freq * Math.PI * 2;
    value + amp * (Math.sin(t * w) / Math.exp(decay * t) / w);
} else {
    value;
}
```

### Stagger Expression
```javascript
// Apply delay based on layer index
delay = 0.1;
d = delay * (index - 1);
time - d;
```

## Timing Reference

| Element | Duration | Easing |
|---------|----------|--------|
| Text reveal | 15-25 frames | Ease out |
| Logo animation | 30-60 frames | Custom curve |
| Transition | 10-20 frames | Ease in-out |
| Lower third in | 12-18 frames | Ease out |
| Lower third out | 8-12 frames | Ease in |

## Export Considerations

- Preview at final framerate
- Enable motion blur for fast motion
- Check timing at 1x speed, not RAM preview
- Account for broadcast safe areas
- Test on target display format
