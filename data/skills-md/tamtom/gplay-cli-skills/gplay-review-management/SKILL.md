---
name: gplay-review-management
description: Review monitoring, filtering, and automated responses for Google Play. Use when managing user reviews and feedback.
---

# Review Management for Google Play

Use this skill when you need to monitor and respond to user reviews.

## List Reviews

### Get all reviews
```bash
gplay reviews list --package com.example.app
```

### Get all reviews with pagination
```bash
gplay reviews list --package com.example.app --paginate
```

### Table output (human-readable)
```bash
gplay reviews list \
  --package com.example.app \
  --output table
```

## Filter Reviews

### By rating
```bash
# Get 1-star reviews
gplay reviews list --package com.example.app \
  | jq '.reviews[] | select(.rating == 1)'

# Get 5-star reviews
gplay reviews list --package com.example.app \
  | jq '.reviews[] | select(.rating == 5)'

# Get reviews with 3 stars or less
gplay reviews list --package com.example.app \
  | jq '.reviews[] | select(.rating <= 3)'
```

### By date
```bash
# Reviews from last 7 days
DATE_7_DAYS_AGO=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)
gplay reviews list --package com.example.app \
  | jq --arg date "$DATE_7_DAYS_AGO" \
    '.reviews[] | select(.comments[0].userComment.lastModified.time > $date)'
```

### By language
```bash
# English reviews only
gplay reviews list --package com.example.app \
  | jq '.reviews[] | select(.comments[0].userComment.language == "en")'
```

### Reviews containing keywords
```bash
# Find reviews mentioning "crash"
gplay reviews list --package com.example.app \
  | jq '.reviews[] | select(.comments[0].userComment.text | contains("crash"))'
```

## Get Specific Review

```bash
gplay reviews get \
  --package com.example.app \
  --review-id REVIEW_ID
```

## Reply to Reviews

### Reply to single review
```bash
gplay reviews reply \
  --package com.example.app \
  --review-id REVIEW_ID \
  --text "Thank you for your feedback! We've fixed this issue in version 1.2.3."
```

### Reply templates

**Bug report response:**
```bash
gplay reviews reply \
  --package com.example.app \
  --review-id REVIEW_ID \
  --text "Thank you for reporting this issue. We've identified the problem and a fix will be available in the next update. Please update to version X.X.X when it's released."
```

**Feature request response:**
```bash
gplay reviews reply \
  --package com.example.app \
  --review-id REVIEW_ID \
  --text "Thank you for your suggestion! We've added this to our roadmap and will consider it for a future release."
```

**Positive review response:**
```bash
gplay reviews reply \
  --package com.example.app \
  --review-id REVIEW_ID \
  --text "Thank you so much for your kind words! We're glad you're enjoying the app."
```

**Crash report response:**
```bash
gplay reviews reply \
  --package com.example.app \
  --review-id REVIEW_ID \
  --text "We're sorry you experienced a crash. This issue has been fixed in version X.X.X. Please update and let us know if you continue to have problems."
```

## Automated Review Response

### Script to reply to unreplied 1-star reviews
```bash
#!/bin/bash

PACKAGE="com.example.app"

# Get all unreplied 1-star reviews
gplay reviews list --package $PACKAGE --paginate \
  | jq -r '.reviews[] | select(.rating == 1 and (.comments | length == 1)) | .reviewId' \
  | while read REVIEW_ID; do
    echo "Replying to review: $REVIEW_ID"
    gplay reviews reply \
      --package $PACKAGE \
      --review-id "$REVIEW_ID" \
      --text "Thank you for your feedback. We're sorry to hear about your experience. Please email support@example.com so we can help resolve this issue."
  done
```

## Review Analytics

### Count reviews by rating
```bash
gplay reviews list --package com.example.app --paginate \
  | jq '[.reviews[] | .rating] | group_by(.) | map({rating: .[0], count: length})'
```

### Average rating calculation
```bash
gplay reviews list --package com.example.app --paginate \
  | jq '[.reviews[].rating] | add / length'
```

### Most common words in reviews
```bash
gplay reviews list --package com.example.app --paginate \
  | jq -r '.reviews[].comments[0].userComment.text' \
  | tr '[:upper:]' '[:lower:]' \
  | tr -s ' ' '\n' \
  | sort | uniq -c | sort -rn | head -20
```

## Monitor for Specific Issues

### Find crash-related reviews
```bash
gplay reviews list --package com.example.app --paginate \
  | jq '.reviews[] | select(.comments[0].userComment.text | test("crash|freeze|hang"; "i"))'
```

### Find reviews mentioning competitors
```bash
gplay reviews list --package com.example.app --paginate \
  | jq '.reviews[] | select(.comments[0].userComment.text | test("competitor_name"; "i"))'
```

### Find reviews with refund requests
```bash
gplay reviews list --package com.example.app --paginate \
  | jq '.reviews[] | select(.comments[0].userComment.text | test("refund|money back"; "i"))'
```

## Review Response Best Practices

### DO:
- ✅ Respond within 24-48 hours
- ✅ Be professional and empathetic
- ✅ Acknowledge the issue
- ✅ Provide a solution or timeline
- ✅ Thank users for feedback
- ✅ Personalize responses when possible

### DON'T:
- ❌ Argue with users
- ❌ Use template responses for everything
- ❌ Ignore negative reviews
- ❌ Make promises you can't keep
- ❌ Be defensive
- ❌ Copy-paste the same response to every review

## Response Templates

### General bug fix
```
Thank you for reporting this. We've identified the issue and it will be fixed in our next update (version X.X.X). We appreciate your patience!
```

### Already fixed
```
Thank you for your feedback! This issue has been resolved in our latest version (X.X.X). Please update your app and let us know if you continue to experience any problems.
```

### Need more info
```
Thank you for your feedback. We'd like to help resolve this issue. Could you please email us at support@example.com with more details about what happened? This will help us investigate further.
```

### Feature request
```
Thank you for the suggestion! We've added this to our feature backlog and will consider it for a future release. Please keep the feedback coming!
```

### Positive review
```
Thank you so much! We're thrilled to hear you're enjoying the app. If you have any suggestions for improvements, we'd love to hear them!
```

## Monitoring Dashboard

Create a simple review dashboard:

```bash
#!/bin/bash
PACKAGE="com.example.app"

echo "=== Review Dashboard ==="
echo ""

# Total reviews
TOTAL=$(gplay reviews list --package $PACKAGE --paginate | jq '.reviews | length')
echo "Total reviews: $TOTAL"

# Rating distribution
echo ""
echo "Rating distribution:"
gplay reviews list --package $PACKAGE --paginate \
  | jq -r '.reviews[] | .rating' \
  | sort | uniq -c | sort -rn

# Avg rating
AVG=$(gplay reviews list --package $PACKAGE --paginate \
  | jq '[.reviews[].rating] | add / length')
echo ""
echo "Average rating: $AVG"

# Unreplied reviews
UNREPLIED=$(gplay reviews list --package $PACKAGE --paginate \
  | jq '[.reviews[] | select(.comments | length == 1)] | length')
echo ""
echo "Unreplied reviews: $UNREPLIED"

# Recent 1-star
echo ""
echo "Recent 1-star reviews:"
gplay reviews list --package $PACKAGE \
  | jq -r '.reviews[] | select(.rating == 1) | "\(.comments[0].userComment.lastModified.time): \(.comments[0].userComment.text)"' \
  | head -5
```

## Scheduled Review Check

### Daily review check (cron)
```bash
# Add to crontab
0 9 * * * /path/to/check-reviews.sh
```

### check-reviews.sh
```bash
#!/bin/bash
PACKAGE="com.example.app"

# Get unreplied 1-star and 2-star reviews
UNREPLIED=$(gplay reviews list --package $PACKAGE \
  | jq '[.reviews[] | select(.rating <= 2 and (.comments | length == 1))] | length')

if [ "$UNREPLIED" -gt 0 ]; then
  echo "⚠️  You have $UNREPLIED unreplied negative reviews!"
  # Send notification (email, Slack, etc.)
fi
```

## Integration with Support System

Forward reviews to support email:

```bash
#!/bin/bash
# Get reviews mentioning "support" or "help"
gplay reviews list --package com.example.app --paginate \
  | jq -r '.reviews[] | select(.comments[0].userComment.text | test("support|help"; "i")) |
    "Review ID: \(.reviewId)\nRating: \(.rating)\nText: \(.comments[0].userComment.text)\n---"' \
  | mail -s "Support Reviews" support@example.com
```
