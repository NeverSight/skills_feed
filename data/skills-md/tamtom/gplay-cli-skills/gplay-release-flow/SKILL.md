---
name: gplay-release-flow
description: End-to-end release workflows for Google Play tracks (internal, beta, production) using gplay release, promote, and rollout commands. Use when asked to upload a build, distribute to testers, or release to production.
---

# Release flow (Internal, Beta, Production)

Use this skill when you need to get a new build onto Google Play Store.

## Preconditions
- Ensure credentials are set (`gplay auth login` or `GPLAY_SERVICE_ACCOUNT` env var).
- Build must be an AAB (App Bundle) or APK.
- Version code must be higher than previous releases.
- Service account needs "Release Manager" permission in Play Console.

## Android Release

### Preferred end-to-end commands

**Internal track** (for internal testing):
```bash
gplay release \
  --package com.example.app \
  --track internal \
  --bundle app-release.aab
```

**Beta track** (for beta testers):
```bash
gplay release \
  --package com.example.app \
  --track beta \
  --bundle app-release.aab \
  --release-notes @release-notes.json
```

**Production with staged rollout** (gradual release):
```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --release-notes @release-notes.json \
  --rollout 10
```

**Dry run** (preview the release without executing):
```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --dry-run
```

### Release with metadata (listings and screenshots)

**Include store listings from a directory**:
```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --listings-dir ./metadata \
  --screenshots-dir ./metadata
```

**Skip metadata or screenshots**:
```bash
# Upload bundle only, skip metadata sync
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --skip-metadata

# Upload bundle and metadata, skip screenshots
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --listings-dir ./metadata \
  --skip-screenshots
```

**Combine listings and screenshots directories**:
```bash
gplay release \
  --package com.example.app \
  --track beta \
  --bundle app-release.aab \
  --listings-dir ./metadata/listings \
  --screenshots-dir ./metadata/images \
  --release-notes @release-notes.json
```

### Manual sequence (when you need more control)

1. **Create edit session**:
   ```bash
   EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')
   ```

2. **Upload bundle**:
   ```bash
   gplay bundles upload \
     --package com.example.app \
     --edit $EDIT_ID \
     --file app-release.aab
   ```

3. **Update track**:
   ```bash
   gplay tracks update \
     --package com.example.app \
     --edit $EDIT_ID \
     --track production \
     --json @track-config.json
   ```

4. **Validate edit**:
   ```bash
   gplay edits validate --package com.example.app --edit $EDIT_ID
   ```

5. **Commit edit** (publishes changes):
   ```bash
   gplay edits commit --package com.example.app --edit $EDIT_ID
   ```

## Track Promotion

Promote a release from one track to another:

```bash
# Promote from internal to beta
gplay promote \
  --package com.example.app \
  --from internal \
  --to beta

# Promote from beta to production with 25% rollout
gplay promote \
  --package com.example.app \
  --from beta \
  --to production \
  --rollout 25
```

## Staged Rollout Management

**Start with 10% rollout**:
```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app.aab \
  --rollout 10
```

**Increase to 50%**:
```bash
gplay rollout update \
  --package com.example.app \
  --track production \
  --rollout 50
```

**Halt rollout** (pause distribution):
```bash
gplay rollout halt --package com.example.app --track production
```

**Resume rollout**:
```bash
gplay rollout resume --package com.example.app --track production
```

**Complete rollout** (release to 100%):
```bash
gplay rollout complete --package com.example.app --track production
```

## Release Notes Format

### JSON format (multi-locale)
`release-notes.json`:
```json
{
  "en-US": "Bug fixes and performance improvements",
  "es-ES": "Correcciones de errores y mejoras de rendimiento",
  "fr-FR": "Corrections de bugs et améliorations des performances"
}
```

### Plain text format (single locale)
You can also provide release notes as plain text for a single locale:
```bash
gplay release \
  --package com.example.app \
  --track beta \
  --bundle app.aab \
  --release-notes "Bug fixes and performance improvements" \
  --release-notes-locale en-US
```

Or from a text file:
```bash
gplay release \
  --package com.example.app \
  --track beta \
  --bundle app.aab \
  --release-notes @release-notes.txt \
  --release-notes-locale en-US
```

## Release Flags Reference

| Flag | Description |
|------|-------------|
| `--package` | App package name (required) |
| `--track` | Target track (required) |
| `--bundle` | Path to AAB file (required) |
| `--release-notes` | Release notes (JSON file with `@`, plain text, or text file with `@`) |
| `--release-notes-locale` | Locale for plain text release notes (e.g., `en-US`) |
| `--rollout` | Rollout percentage (1-100) |
| `--listings-dir` | Directory containing store listings to sync |
| `--screenshots-dir` | Directory containing screenshots to upload |
| `--skip-metadata` | Skip metadata/listings sync during release |
| `--skip-screenshots` | Skip screenshots upload during release |
| `--dry-run` | Preview the release without executing |
| `--output` | Output format (`json`, `table`, `markdown`) |

## Pre-release Checklist
Before releasing, verify:
- [ ] Version code is incremented
- [ ] AAB/APK is signed with correct keystore
- [ ] ProGuard/R8 mapping files uploaded (for crash reports)
- [ ] Release notes written for all locales
- [ ] Testing completed on internal/beta track
- [ ] Service account has correct permissions
- [ ] Dry run passes: `gplay release ... --dry-run`

## Common Release Strategies

**Strategy 1: Internal -> Beta -> Production**
```bash
# Week 1: Internal
gplay release --package com.example.app --track internal --bundle app.aab

# Week 2: Beta (after testing)
gplay promote --package com.example.app --from internal --to beta

# Week 3: Production with staged rollout
gplay promote --package com.example.app --from beta --to production --rollout 10
gplay rollout update --package com.example.app --track production --rollout 50  # Day 2
gplay rollout complete --package com.example.app --track production            # Day 7
```

**Strategy 2: Direct to Production with Staged Rollout**
```bash
# Day 1: 10%
gplay release --package com.example.app --track production --bundle app.aab --rollout 10

# Day 2: 25%
gplay rollout update --package com.example.app --track production --rollout 25

# Day 3: 50%
gplay rollout update --package com.example.app --track production --rollout 50

# Day 7: 100%
gplay rollout complete --package com.example.app --track production
```

**Strategy 3: Full release with metadata and dry-run verification**
```bash
# 1. Dry run to verify everything
gplay release \
  --package com.example.app \
  --track production \
  --bundle app.aab \
  --listings-dir ./metadata \
  --screenshots-dir ./metadata \
  --release-notes @release-notes.json \
  --rollout 10 \
  --dry-run

# 2. Execute the release
gplay release \
  --package com.example.app \
  --track production \
  --bundle app.aab \
  --listings-dir ./metadata \
  --screenshots-dir ./metadata \
  --release-notes @release-notes.json \
  --rollout 10
```

## Notes
- Always use `--help` to verify flags for the exact command.
- Use `--output table` for human-readable output; default is JSON.
- For CI/CD, use `GPLAY_SERVICE_ACCOUNT` environment variable.
- Upload deobfuscation files after each release for crash symbolication.
- Use `--dry-run` in CI to validate releases before actual deployment.
