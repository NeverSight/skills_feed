---
name: update-storybook-snapshots
description: Update Storybook visual regression snapshots after intentional UI changes. Use when visual tests fail due to expected changes, or when asked to update snapshots.
---

# Update Storybook Snapshots

## Overview

Storybook snapshots are baseline images used for visual regression testing. When UI components change intentionally, snapshots must be updated to reflect the new expected appearance.

## When to Update Snapshots

Update snapshots when:
- You intentionally changed component styling
- You added new UI components with stories
- You modified component layout or structure
- Design system updates affected component appearance

Do NOT update snapshots when:
- You didn't intentionally change the UI
- The visual diff shows a bug or regression
- You're unsure why the appearance changed

## Update Process

### Step 1: Run Tests to See Failures

```bash
pnpm test:storybook
```

Review which snapshots failed. Failures generate diff images.

### Step 2: Review Diff Images

Diff images are saved to:
```
packages/keychain/__image_snapshots__/__diff_output__/
```

Each diff image shows:
- **Left**: Expected (baseline)
- **Center**: Difference highlighted
- **Right**: Actual (current)

Verify the changes are intentional before proceeding.

### Step 3: Update Snapshots

```bash
pnpm test:storybook:update
```

This regenerates all snapshot images based on current component rendering.

### Step 4: Review Updated Snapshots

Check the updated images look correct:
```bash
# List changed snapshot files
git status packages/*/__image_snapshots__/

# View specific changes (if you have an image viewer)
ls packages/keychain/__image_snapshots__/*.png
```

### Step 5: Commit the Updates

```bash
git add packages/*/__image_snapshots__/
git commit -m "chore: update storybook snapshots"
```

## Snapshot Locations

```
packages/keychain/__image_snapshots__/
├── components-*.png           # Component snapshots
├── __diff_output__/           # Diff images (not committed)
│   └── *-diff.png
```

## Common Scenarios

### New Component Added

1. Create the component
2. Add a Storybook story in `packages/keychain/src/components/`
3. Run `pnpm test:storybook:update` to generate initial snapshot
4. Commit both the component and snapshot

### Theme/Design System Update

When design tokens or theme changes affect multiple components:

```bash
# Update all snapshots at once
pnpm test:storybook:update

# Review all changes
git diff --stat packages/*/__image_snapshots__/

# Commit with descriptive message
git add packages/*/__image_snapshots__/
git commit -m "chore: update snapshots for design system changes"
```

### CI Auto-Updates

The CI workflow (`test.yml`) can auto-update snapshots and push:
- If running on a PR branch
- If the only failures are visual differences
- Creates commit "chore: update storybook snapshots"

This means if you push changes that affect visuals, CI may auto-commit updated snapshots to your PR.

## Troubleshooting

### Tests timeout

Storybook must be able to start:
```bash
# Kill any existing Storybook process
pkill -f storybook

# Ensure port 6006 is free
lsof -i :6006

# Try running Storybook manually first
pnpm storybook
```

### Inconsistent snapshots

If snapshots differ between local and CI:
- Ensure you're using the same Node version (20.x)
- Font rendering can differ between platforms
- CI uses a specific Docker image for consistency

### Missing dependencies

```bash
pnpm clean && pnpm i && pnpm build:deps
```

## Script Helper

There's also a helper script available:
```bash
./scripts/update-storybook-snapshot.sh
```

## Best Practices

1. **Review every diff** - Don't blindly update snapshots
2. **Small commits** - Update snapshots in their own commit
3. **Descriptive messages** - Mention what changed if significant
4. **Clean baseline** - Don't commit diff images (they're gitignored)
5. **CI consistency** - If local passes but CI fails, investigate the difference
