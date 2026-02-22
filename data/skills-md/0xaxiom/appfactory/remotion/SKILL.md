---
name: remotion
description: Use when generating or modifying Remotion video code, creating demo videos, or working with the demo-video/ directory
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Remotion Video Generation Skills

App Factory includes an integrated Remotion video pipeline for generating demo videos of built applications.

## When This Skill Applies

- Working with files in `demo-video/` directory
- Running `/factory video` command
- Creating or modifying Remotion compositions
- Debugging video rendering issues
- Understanding frame-based animations

## Project Structure

```
demo-video/
├── src/
│   ├── index.ts              # Remotion entry point
│   ├── Root.tsx              # Composition registry
│   ├── compositions/
│   │   └── AppFactoryDemo.tsx # Main demo video (10s, 1920x1080)
│   └── components/
│       ├── Title.tsx         # Animated title
│       ├── BulletPoints.tsx  # Staggered highlights
│       ├── VerificationBadge.tsx # PASS badge
│       └── Footer.tsx        # UTC timestamp
├── remotion.config.ts        # Remotion configuration
└── package.json              # Dependencies (Remotion v4.x)
```

## Critical Rules (MUST FOLLOW)

### 1. Frame-Based Animations ONLY

```typescript
// CORRECT: Use useCurrentFrame() for all animations
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: 'clamp',
});

// FORBIDDEN: CSS animations/transitions
// Never use: animation:, transition:, @keyframes
```

### 2. Interpolate with Clamping

```typescript
// ALWAYS use extrapolation clamping
const value = interpolate(frame, [0, 60], [0, 100], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

### 3. Spring Animations

```typescript
// Use spring() for physics-based animations
const springValue = spring({
  fps,
  frame,
  config: { damping: 200, stiffness: 100 },
  durationInFrames: 40,
});
```

### 4. Determinism Requirements

- Timestamps MUST be input props, never `new Date()`
- Use `timeZone: 'UTC'` for all date formatting
- No `Math.random()` or non-deterministic values
- Same props must produce identical video output

### 5. Component Structure

```typescript
// All compositions must follow this pattern
export const MyComposition: React.FC<Props> = (props) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* Sequenced content */}
      <Sequence from={0} durationInFrames={60}>
        <Scene1 />
      </Sequence>
      <Sequence from={60} durationInFrames={60}>
        <Scene2 />
      </Sequence>
    </AbsoluteFill>
  );
};
```

## Pipeline Integration

### Auto-Generation Flow

1. Local Run Proof verification runs
2. `RUN_CERTIFICATE.json` created with `status: "PASS"`
3. Hook triggers `post-run-certificate-video.mjs`
4. Demo video rendered to `demo/out/<slug>.mp4`

### Manual Rendering

```bash
# Basic usage
node scripts/render-demo-video.mjs --cwd ./my-app --slug my-app

# With custom highlights
node scripts/render-demo-video.mjs \
  --cwd ./my-app \
  --slug my-app \
  --title "My Amazing App" \
  --highlights '["Feature 1", "Feature 2", "Feature 3"]'
```

### Props Schema

```typescript
interface AppFactoryDemoProps {
  title: string; // App name
  slug: string; // URL-safe identifier
  verifiedUrl: string; // Localhost URL that passed health check
  timestamp: string; // ISO 8601 timestamp (UTC)
  highlights: string[]; // 4-6 bullet points
  certificateHash: string; // SHA256 of RUN_CERTIFICATE.json
}
```

## Debugging

```bash
# Preview in Remotion Studio
cd demo-video && npm run studio

# Render specific composition
npx remotion render src/index.ts AppFactoryDemo output.mp4

# Check for TypeScript errors
npx tsc --noEmit
```

## Common Patterns

### Fade In/Out

```typescript
const fadeIn = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: 'clamp',
});
const fadeOut = interpolate(frame, [duration - 30, duration], [1, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
const opacity = fadeIn * fadeOut;
```

### Staggered Animation

```typescript
items.map((item, index) => {
  const delay = index * 10; // 10 frames between each
  const itemOpacity = interpolate(
    frame,
    [delay, delay + 20],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  return <Item key={index} style={{ opacity: itemOpacity }} />;
});
```

### Scale with Spring

```typescript
const scaleSpring = spring({
  fps,
  frame: frame - startFrame,
  config: { damping: 80, stiffness: 200 },
});
const scale = interpolate(scaleSpring, [0, 1], [0.8, 1]);
```

## Error Codes

| Code    | Meaning                 | Resolution                                   |
| ------- | ----------------------- | -------------------------------------------- |
| FAC-006 | Video render failed     | Check Remotion logs, verify ffmpeg installed |
| FAC-007 | Certificate missing     | Run Local Run Proof first                    |
| FAC-008 | Props validation failed | Check prop types match schema                |

## Reference

- [Remotion Documentation](https://www.remotion.dev/docs)
- [App Factory Demo Video README](./demo-video/README.md)
- [Local Run Proof Gate](./scripts/local-run-proof/README.md)
