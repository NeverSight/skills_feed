---
name: gplay-rollout-management
description: Staged rollout orchestration and monitoring for Google Play releases. Use when implementing gradual release strategies.
---

# Staged Rollout Management

Use this skill when you need to manage gradual releases on Google Play.

## What is Staged Rollout?

Staged rollout releases your app to a percentage of users, allowing you to:
- Monitor crash rates and reviews before full release
- Catch critical bugs with limited user impact
- Gradually increase distribution as confidence grows

## Start a Staged Rollout

### During initial release
```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --rollout 10
```

This releases to 10% of users.

### Promote with rollout
```bash
gplay promote \
  --package com.example.app \
  --from beta \
  --to production \
  --rollout 25
```

## Increase Rollout Percentage

```bash
# Increase to 25%
gplay rollout update \
  --package com.example.app \
  --track production \
  --rollout 25

# Increase to 50%
gplay rollout update \
  --package com.example.app \
  --track production \
  --rollout 50

# Increase to 100% (or use complete)
gplay rollout update \
  --package com.example.app \
  --track production \
  --rollout 100
```

## Halt Rollout

Pause distribution if issues are detected:

```bash
gplay rollout halt \
  --package com.example.app \
  --track production
```

**Effect:**
- Stops further distribution
- Existing users keep the update
- New users don't receive the update

## Resume Rollout

Resume after fixing issues:

```bash
gplay rollout resume \
  --package com.example.app \
  --track production
```

## Complete Rollout

Release to 100% of users:

```bash
gplay rollout complete \
  --package com.example.app \
  --track production
```

## Check Rollout Status

```bash
gplay tracks get \
  --package com.example.app \
  --track production \
  | jq '.releases[0].userFraction'
```

## Recommended Rollout Strategy

### Conservative (7-day rollout)
```bash
# Day 1: 10%
gplay release --package com.example.app --track production --bundle app.aab --rollout 10

# Day 2: 25% (monitor crash rate)
gplay rollout update --package com.example.app --track production --rollout 25

# Day 3: 50%
gplay rollout update --package com.example.app --track production --rollout 50

# Day 5: 75%
gplay rollout update --package com.example.app --track production --rollout 75

# Day 7: 100%
gplay rollout complete --package com.example.app --track production
```

### Aggressive (3-day rollout)
```bash
# Day 1: 25%
gplay release --package com.example.app --track production --bundle app.aab --rollout 25

# Day 2: 50%
gplay rollout update --package com.example.app --track production --rollout 50

# Day 3: 100%
gplay rollout complete --package com.example.app --track production
```

### Cautious (for critical apps)
```bash
# Day 1: 5%
gplay release --package com.example.app --track production --bundle app.aab --rollout 5

# Day 2: 10% (monitor carefully)
gplay rollout update --package com.example.app --track production --rollout 10

# Day 3: 25%
gplay rollout update --package com.example.app --track production --rollout 25

# Day 5: 50%
gplay rollout update --package com.example.app --track production --rollout 50

# Day 7: 75%
gplay rollout update --package com.example.app --track production --rollout 75

# Day 10: 100%
gplay rollout complete --package com.example.app --track production
```

## Monitoring During Rollout

### Check crash rate
Use Play Console → Quality → Android vitals

### Monitor reviews
```bash
# Get recent reviews
gplay reviews list \
  --package com.example.app \
  --paginate \
  | jq '.reviews[] | select(.createdTime > "2025-02-05") | {rating, text: .comments[0].userComment.text}'
```

### Filter 1-star reviews
```bash
gplay reviews list \
  --package com.example.app \
  | jq '.reviews[] | select(.rating == 1) | .comments[0].userComment.text'
```

## Decision Matrix

| Metric | Action |
|--------|--------|
| Crash rate < 1% | Continue rollout |
| Crash rate 1-2% | Halt, investigate |
| Crash rate > 2% | Halt, rollback if possible |
| 1-star reviews spike | Halt, investigate |
| ANR rate spike | Halt, investigate |
| No issues after 24h | Increase rollout |

## Rollback Strategy

Google Play doesn't support automatic rollback, but you can:

### Option 1: Upload hotfix
```bash
# Build hotfix with higher version code
./gradlew bundleRelease

# Release hotfix immediately to 100%
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-hotfix.aab
```

### Option 2: Promote previous version
This requires the previous version still be in beta track:

```bash
gplay promote \
  --package com.example.app \
  --from beta \
  --to production
```

## Best Practices

1. **Always start with <20%** - Catch issues early
2. **Monitor for 24 hours** between increases
3. **Have a hotfix plan** - Be ready to fix critical bugs quickly
4. **Set up alerts** - Monitor crash rates automatically
5. **Test thoroughly in beta** - Reduce production issues
6. **Communicate with users** - Update release notes
7. **Don't rush** - Gradual rollout is for safety

## Common Mistakes to Avoid

❌ **Don't:**
- Jump from 10% to 100% immediately
- Ignore crash rate increases
- Roll out during weekends/holidays (slower monitoring)
- Skip beta testing phase

✅ **Do:**
- Monitor crash rates constantly
- Have team available during rollout
- Prepare hotfix in advance
- Communicate expected timeline to stakeholders

## Automation Example

### CI/CD with automated rollout
```yaml
# .github/workflows/rollout.yml
name: Automated Rollout

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM

jobs:
  increase-rollout:
    runs-on: ubuntu-latest
    steps:
      - name: Get current rollout
        id: current
        run: |
          CURRENT=$(gplay tracks get --package $PACKAGE | jq -r '.releases[0].userFraction')
          echo "fraction=$CURRENT" >> $GITHUB_OUTPUT

      - name: Increase rollout
        if: steps.current.outputs.fraction < 1.0
        run: |
          NEW_FRACTION=$(echo "${{ steps.current.outputs.fraction }} + 0.25" | bc)
          gplay rollout update --package $PACKAGE --track production --rollout $NEW_FRACTION
```

## Support

For manual rollout control, always use the Google Play Console UI as a backup.
