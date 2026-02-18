---
name: gplay-testers-orchestration
description: Beta testing groups and tester management for Google Play closed testing tracks. Use when managing testers and beta groups.
---

# Testers Orchestration for Google Play

Use this skill when you need to manage beta testers and testing groups.

## Understanding Testing Tracks

Google Play has several testing tracks:
- **Internal** - Up to 100 testers, instant access
- **Closed** - Invite-only testing groups
- **Open** - Public beta, anyone can join

## Manage Testers

### List testers for a track
```bash
gplay testers list \
  --package com.example.app \
  --edit $EDIT_ID \
  --track internal
```

### Get tester group details
```bash
gplay testers get \
  --package com.example.app \
  --edit $EDIT_ID \
  --track beta
```

### Update tester emails
```bash
gplay testers update \
  --package com.example.app \
  --edit $EDIT_ID \
  --track internal \
  --emails "user1@example.com,user2@example.com,user3@example.com"
```

### Add testers (append to existing list)
```bash
# Get current testers
CURRENT=$(gplay testers get --package com.example.app --edit $EDIT_ID --track internal \
  | jq -r '.testers[]' | paste -sd "," -)

# Add new testers
NEW_TESTERS="user4@example.com,user5@example.com"
ALL_TESTERS="$CURRENT,$NEW_TESTERS"

gplay testers update \
  --package com.example.app \
  --edit $EDIT_ID \
  --track internal \
  --emails "$ALL_TESTERS"
```

### Remove tester
```bash
# Get current testers
CURRENT=$(gplay testers get --package com.example.app --edit $EDIT_ID --track internal \
  | jq -r '.testers[]' | paste -sd "," -)

# Remove specific email
UPDATED=$(echo "$CURRENT" | tr ',' '\n' | grep -v "user@example.com" | paste -sd "," -)

gplay testers update \
  --package com.example.app \
  --edit $EDIT_ID \
  --track internal \
  --emails "$UPDATED"
```

## Complete Tester Workflow

### Setup internal testing
```bash
# 1. Create edit
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')

# 2. Upload build to internal track
gplay bundles upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --file app-internal.aab

# 3. Add testers
gplay testers update \
  --package com.example.app \
  --edit $EDIT_ID \
  --track internal \
  --emails "tester1@example.com,tester2@example.com"

# 4. Update track
gplay tracks update \
  --package com.example.app \
  --edit $EDIT_ID \
  --track internal \
  --json @track-config.json

# 5. Commit
gplay edits commit --package com.example.app --edit $EDIT_ID
```

### track-config.json
```json
{
  "releases": [{
    "versionCodes": [123],
    "status": "completed"
  }]
}
```

## Internal Testing (Quick Testing)

**Characteristics:**
- Up to 100 testers
- Instant access (no review)
- Ideal for rapid iteration

```bash
# Release to internal with testers
gplay release \
  --package com.example.app \
  --track internal \
  --bundle app.aab \
  --testers "dev1@company.com,dev2@company.com,qa@company.com"
```

## Closed Testing (Beta Groups)

**Characteristics:**
- Unlimited testers
- Can have multiple named groups
- Testers need opt-in link

### Create beta release
```bash
gplay release \
  --package com.example.app \
  --track beta \
  --bundle app.aab
```

### Testers join via opt-in link
Share this link with testers:
```
https://play.google.com/apps/testing/com.example.app
```

## Open Testing (Public Beta)

**Characteristics:**
- Anyone can join
- Public opt-in page
- Still requires Play Store review

```bash
gplay release \
  --package com.example.app \
  --track alpha \  # alpha track = open testing
  --bundle app.aab
```

## Tester Management Best Practices

### Organize testers by group

**Internal testing:**
- Developers
- QA team
- Product managers

**Closed beta:**
- Power users
- Customer advisory board
- Early adopters

**Open beta:**
- General public
- Community members

### Email list management

Store tester lists in files:

```bash
# testers-internal.txt
dev1@company.com
dev2@company.com
qa@company.com

# testers-beta.txt
poweruser1@example.com
poweruser2@example.com
feedback@example.com
```

Update from file:
```bash
EMAILS=$(cat testers-internal.txt | paste -sd "," -)
gplay testers update \
  --package com.example.app \
  --edit $EDIT_ID \
  --track internal \
  --emails "$EMAILS"
```

## Testing Workflow Examples

### Weekly Beta Release
```bash
#!/bin/bash
PACKAGE="com.example.app"

# Build
./gradlew bundleRelease

# Release to internal first
gplay release \
  --package $PACKAGE \
  --track internal \
  --bundle app/build/outputs/bundle/release/app-release.aab

# Wait 24 hours, monitor for crashes

# If stable, promote to beta
gplay promote \
  --package $PACKAGE \
  --from internal \
  --to beta
```

### Staged Beta Rollout
```bash
# Week 1: Internal team (10 people)
gplay release --package com.example.app --track internal --bundle app.aab

# Week 2: Beta group 1 (100 people)
gplay promote --package com.example.app --from internal --to beta

# Week 3: Open beta (unlimited)
gplay promote --package com.example.app --from beta --to alpha

# Week 4: Production with staged rollout
gplay promote --package com.example.app --from alpha --to production --rollout 10
```

## Share Testing Links

### Internal testing link
```
https://play.google.com/apps/internaltest/INTERNAL_TESTING_ID
```

Get from Play Console → Internal testing → Testers → Copy link

### Closed testing opt-in link
```
https://play.google.com/apps/testing/com.example.app
```

### Email template for testers
```
Subject: Join the Beta Test for [App Name]

Hi,

You've been invited to test the beta version of [App Name]!

To join:
1. Click this link: https://play.google.com/apps/testing/com.example.app
2. Tap "Become a tester"
3. Download the app from Google Play

Your feedback is valuable! Please report any issues to: beta@example.com

Thanks,
The [App Name] Team
```

## Monitor Beta Feedback

### Check feedback
```bash
# View recent reviews from beta testers
gplay reviews list --package com.example.app \
  | jq '.reviews[] | select(.comments[0].userComment.reviewerLanguage != null)'
```

### Crash reports
Use Play Console → Quality → Android vitals → Crashes and ANRs

Filter by version code to see beta-specific crashes.

## Automated Tester Management

### Sync from CSV
```bash
#!/bin/bash
# sync-testers.sh

PACKAGE="com.example.app"
CSV_FILE="testers.csv"

# Read emails from CSV (skip header)
EMAILS=$(tail -n +2 "$CSV_FILE" | cut -d',' -f1 | paste -sd "," -)

# Create edit
EDIT_ID=$(gplay edits create --package $PACKAGE | jq -r '.id')

# Update testers
gplay testers update \
  --package $PACKAGE \
  --edit $EDIT_ID \
  --track internal \
  --emails "$EMAILS"

# Commit
gplay edits commit --package $PACKAGE --edit $EDIT_ID

echo "Synced $(echo $EMAILS | tr ',' '\n' | wc -l) testers"
```

### testers.csv
```csv
email,name,role
dev1@company.com,Alice Developer,Developer
qa1@company.com,Bob QA,QA
pm@company.com,Carol PM,Product Manager
```

## Remove Inactive Testers

```bash
#!/bin/bash
# Remove testers who haven't tested in 30 days

PACKAGE="com.example.app"
EDIT_ID=$(gplay edits create --package $PACKAGE | jq -r '.id')

# Get current testers
CURRENT=$(gplay testers get --package $PACKAGE --edit $EDIT_ID --track beta \
  | jq -r '.testers[]')

# Filter active testers (implement your logic)
# This is a placeholder - you'd need to track activity separately
ACTIVE="tester1@example.com,tester2@example.com"

# Update
gplay testers update \
  --package $PACKAGE \
  --edit $EDIT_ID \
  --track beta \
  --emails "$ACTIVE"

gplay edits commit --package $PACKAGE --edit $EDIT_ID
```

## Testing Limits

| Track | Max Testers | Review Required | Access Speed |
|-------|-------------|-----------------|--------------|
| Internal | 100 | No | Instant |
| Closed | Unlimited | No | Minutes |
| Open | Unlimited | Yes | Days |
| Production | Unlimited | Yes | Days |

## Best Practices

### DO:
- ✅ Start with internal testing
- ✅ Gradually expand to beta
- ✅ Communicate clearly with testers
- ✅ Provide feedback channels
- ✅ Acknowledge tester contributions
- ✅ Keep tester lists up to date
- ✅ Remove inactive testers periodically

### DON'T:
- ❌ Skip internal testing
- ❌ Add everyone to all tracks
- ❌ Ignore tester feedback
- ❌ Leave broken builds in testing
- ❌ Forget to thank your testers
- ❌ Use production track for testing

## Track Selection Guide

**Use Internal when:**
- Initial feature testing
- Testing with dev/QA team only
- Need instant access
- < 100 testers

**Use Closed when:**
- Broader beta testing
- Need > 100 testers
- Want named beta groups
- Testing with customers

**Use Open when:**
- Public beta program
- Want maximum reach
- Community testing
- Pre-launch buzz

## Communication with Testers

### Release notes for testers
Include in app update:
```
Version 1.2.3 (Beta)

What's New:
- New feature X (please test thoroughly)
- Bug fixes for Y

Known Issues:
- Feature Z is work in progress
- Crash on Android 12 is being investigated

Please report issues to: beta@example.com
```

### Feedback collection
- In-app feedback button
- Dedicated Slack/Discord channel
- Email address
- Survey form

This helps you improve before production release!
