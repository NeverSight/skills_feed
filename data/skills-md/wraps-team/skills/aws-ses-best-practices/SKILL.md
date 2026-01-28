---
name: aws-ses-best-practices
description: Email deliverability, warming, compliance, and operational guidelines for AWS Simple Email Service.
---

# AWS SES Best Practices

Email deliverability, warming, compliance, and operational guidelines for AWS Simple Email Service.

## Email Authentication

### SPF (Sender Policy Framework)

Add to your domain's DNS:

```
v=spf1 include:amazonses.com ~all
```

**For custom MAIL FROM domain:**
```
# TXT record for mail.yourapp.com
v=spf1 include:amazonses.com ~all
```

### DKIM (DomainKeys Identified Mail)

SES provides three CNAME records for DKIM. Add all three:

```
# Example (actual values from SES console)
selector1._domainkey.yourapp.com CNAME selector1.dkim.amazonses.com
selector2._domainkey.yourapp.com CNAME selector2.dkim.amazonses.com
selector3._domainkey.yourapp.com CNAME selector3.dkim.amazonses.com
```

### DMARC (Domain-based Message Authentication)

Add TXT record to your domain:

```
# Start with monitoring mode
_dmarc.yourapp.com TXT "v=DMARC1; p=none; rua=mailto:dmarc@yourapp.com"

# After monitoring, move to quarantine
_dmarc.yourapp.com TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourapp.com"

# Production: reject unauthenticated emails
_dmarc.yourapp.com TXT "v=DMARC1; p=reject; rua=mailto:dmarc@yourapp.com"
```

### Custom MAIL FROM Domain

Improves deliverability by using your domain instead of `amazonses.com`:

```
# MX record for mail.yourapp.com
mail.yourapp.com MX 10 feedback-smtp.us-east-1.amazonses.com

# SPF record for mail.yourapp.com
mail.yourapp.com TXT "v=spf1 include:amazonses.com ~all"
```

## IP Warming

New SES accounts have limited sending reputation. Warm up gradually.

### Warming Schedule

| Day | Daily Volume | Notes |
|-----|--------------|-------|
| 1-2 | 200 | Start small, monitor bounces |
| 3-4 | 500 | Check complaint rate |
| 5-7 | 1,000 | Monitor reputation dashboard |
| 8-14 | 5,000 | Steady increase |
| 15-21 | 10,000 | |
| 22-30 | 25,000 | |
| 30+ | 50,000+ | Scale as needed |

### Warming Best Practices

1. **Start with engaged users** — Send to users who recently opened/clicked
2. **Prioritize transactional** — Welcome emails, password resets have high engagement
3. **Avoid cold lists** — Don't send to addresses that haven't engaged in 6+ months
4. **Monitor daily** — Check bounce/complaint rates in SES dashboard
5. **Slow down if issues** — If bounces > 5% or complaints > 0.1%, reduce volume

## Bounce Handling

### Types of Bounces

**Hard Bounces (Permanent):**
- Invalid/non-existent email address
- Domain doesn't exist
- **Action:** Remove immediately, never send again

**Soft Bounces (Temporary):**
- Mailbox full
- Server temporarily unavailable
- **Action:** Retry with exponential backoff, remove after 3-5 attempts

**Transient Bounces:**
- Auto-responders
- Challenge-response systems
- **Action:** Generally ignore, don't count against reputation

### Bounce Rate Thresholds

| Rate | Status | Action |
|------|--------|--------|
| < 2% | Healthy | Continue normally |
| 2-5% | Warning | Investigate, clean list |
| 5-10% | Critical | Stop sends, clean list aggressively |
| > 10% | Danger | SES may suspend account |

### Handling Bounces with Wraps

```typescript
// Wraps CLI sets up automatic bounce handling via SNS → Lambda → DynamoDB
// Query bounced addresses:
import { DynamoDBClient, QueryCommand } from '@aws-sdk/client-dynamodb';

const client = new DynamoDBClient({});
const bounces = await client.send(new QueryCommand({
  TableName: 'wraps-email-events',
  KeyConditionExpression: 'pk = :pk',
  ExpressionAttributeValues: {
    ':pk': { S: 'BOUNCE#hard' },
  },
}));
```

## Complaint Handling

### Complaint Rate Thresholds

| Rate | Status | Action |
|------|--------|--------|
| < 0.1% | Healthy | Continue normally |
| 0.1-0.3% | Warning | Review content, add unsubscribe |
| 0.3-0.5% | Critical | Pause marketing emails |
| > 0.5% | Danger | SES may suspend account |

### Reducing Complaints

1. **Clear unsubscribe** — One-click unsubscribe in every email
2. **Set expectations** — Tell users what/when you'll email during signup
3. **Honor preferences** — Let users choose email types/frequency
4. **Clean lists** — Remove unengaged users proactively
5. **Relevant content** — Only send what users signed up for

### List-Unsubscribe Header

Add to all marketing emails:

```typescript
// With raw email or custom headers
const headers = {
  'List-Unsubscribe': '<mailto:unsubscribe@yourapp.com>, <https://yourapp.com/unsubscribe>',
  'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
};
```

## List Hygiene

### Email Validation

Validate emails at signup:

```typescript
// Basic format validation
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Check for common typos
const typoSuggestions: Record<string, string> = {
  'gmial.com': 'gmail.com',
  'gmal.com': 'gmail.com',
  'hotmal.com': 'hotmail.com',
  'yaho.com': 'yahoo.com',
};

// Use email verification service for important signups
// (e.g., ZeroBounce, NeverBounce, Hunter)
```

### Engagement-Based Cleanup

Remove or suppress addresses based on engagement:

| Last Engagement | Action |
|-----------------|--------|
| < 30 days | Active, send normally |
| 30-90 days | Reduce frequency |
| 90-180 days | Re-engagement campaign |
| 180+ days | Suppress from regular sends |
| 365+ days | Remove from list |

### Suppression Lists

Maintain lists of addresses to never email:

```typescript
// Hard bounces - permanent suppression
// Complaints - permanent suppression
// Unsubscribes - honor indefinitely
// Role addresses - suppress (admin@, info@, support@)
```

## Content Best Practices

### Subject Lines

- **Keep it short** — Under 50 characters
- **Be specific** — Tell them what's inside
- **Avoid spam triggers** — No ALL CAPS, excessive punctuation, "FREE!!!"
- **Personalize** — Include name or relevant detail

### Email Body

1. **Text version** — Always include plain text alternative
2. **Image-to-text ratio** — Keep images < 40% of content
3. **Hosted images** — Use absolute URLs, not embedded images
4. **Alt text** — Every image needs alt text
5. **Mobile-friendly** — Single column, 600px max width
6. **Clear CTA** — One primary call-to-action

### Avoid Spam Triggers

**Words to avoid:**
- FREE, WINNER, CONGRATULATIONS
- Act now, Limited time, Urgent
- $$, Make money, Cash bonus
- Click here, Buy now

**Formatting to avoid:**
- ALL CAPS
- Excessive punctuation!!!
- Red text
- Large fonts
- Invisible text (white on white)

## Sending Patterns

### Consistent Schedule

- Send at consistent times (users learn to expect your emails)
- Avoid sudden volume spikes (looks like spam)
- Spread large sends over time (don't blast all at once)

### Time Zone Awareness

```typescript
// Send at optimal local time
const sendAtLocalTime = (email: string, preferredHour: number) => {
  const userTimezone = getUserTimezone(email); // from user preferences
  const now = new Date();
  const targetTime = new Date(now.toLocaleString('en-US', { timeZone: userTimezone }));
  targetTime.setHours(preferredHour, 0, 0, 0);

  if (targetTime < now) {
    targetTime.setDate(targetTime.getDate() + 1);
  }

  return targetTime;
};
```

### Throttling for Large Lists

```typescript
// Don't send 100k emails at once
const BATCH_SIZE = 1000;
const DELAY_BETWEEN_BATCHES_MS = 60000; // 1 minute

async function sendBulk(recipients: string[], template: string) {
  for (let i = 0; i < recipients.length; i += BATCH_SIZE) {
    const batch = recipients.slice(i, i + BATCH_SIZE);
    await email.sendBulkTemplate({
      from: 'hello@yourapp.com',
      template,
      destinations: batch.map(to => ({ to, templateData: {} })),
    });

    if (i + BATCH_SIZE < recipients.length) {
      await sleep(DELAY_BETWEEN_BATCHES_MS);
    }
  }
}
```

## Monitoring & Alerts

### Key Metrics to Track

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Bounce Rate | < 2% | > 5% |
| Complaint Rate | < 0.1% | > 0.3% |
| Delivery Rate | > 95% | < 90% |
| Open Rate | > 20% | < 10% |
| Click Rate | > 2% | < 1% |

### CloudWatch Alarms

Wraps CLI sets up basic alarms. Add custom ones:

```typescript
// High bounce rate alarm
const alarm = new cloudwatch.Alarm(this, 'HighBounceRate', {
  metric: new cloudwatch.Metric({
    namespace: 'AWS/SES',
    metricName: 'Bounce',
    statistic: 'Sum',
    period: Duration.hours(1),
  }),
  threshold: 50,
  evaluationPeriods: 1,
  comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
});
```

### SES Reputation Dashboard

Check regularly in AWS Console → SES → Reputation Metrics:
- Account status (Healthy, Under review, Paused)
- Bounce rate trend
- Complaint rate trend

## Compliance

### CAN-SPAM (US)

1. **Accurate headers** — From/reply-to must be accurate
2. **No deceptive subjects** — Subject must reflect content
3. **Physical address** — Include valid postal address
4. **Unsubscribe** — Clear, working unsubscribe mechanism
5. **Honor opt-outs** — Process within 10 business days

### GDPR (EU)

1. **Consent** — Clear, explicit opt-in for marketing
2. **Right to access** — Provide data on request
3. **Right to erasure** — Delete data on request
4. **Data portability** — Export data in common format
5. **Lawful basis** — Document why you're processing data

### CASL (Canada)

1. **Express consent** — Written/verbal permission required
2. **Implied consent** — Limited (existing relationship, published email)
3. **Unsubscribe** — Honor within 10 days
4. **Identification** — Sender identity and contact info

### Footer Template

```html
<footer style="font-size: 12px; color: #666;">
  <p>
    You're receiving this email because you signed up at yourapp.com.
  </p>
  <p>
    <a href="{{unsubscribe_url}}">Unsubscribe</a> |
    <a href="{{preferences_url}}">Email Preferences</a>
  </p>
  <p>
    Your Company, Inc.<br>
    123 Main Street<br>
    City, State 12345
  </p>
</footer>
```

## SES Limits & Quotas

### Default Limits (Sandbox)

- 200 emails/24 hours
- 1 email/second
- Can only send to verified addresses

### Production Limits

- Varies based on account history
- Start at 50,000/day, 14/second
- Request increases as needed

### Requesting Limit Increase

1. AWS Console → SES → Account Dashboard
2. Click "Request Production Access" or "Request Limit Increase"
3. Provide:
   - Use case description
   - Expected volume
   - Bounce/complaint handling process
   - List collection method

## Troubleshooting

### "Email not delivered"

1. Check SES console for bounces/complaints
2. Verify recipient didn't unsubscribe
3. Check spam folder
4. Test with mail-tester.com

### "High bounce rate"

1. Validate email addresses at signup
2. Remove old addresses (180+ days inactive)
3. Use double opt-in
4. Check for typos in bulk imports

### "High complaint rate"

1. Add clear unsubscribe link
2. Review email content
3. Reduce frequency
4. Segment engaged vs unengaged users

### "Emails going to spam"

1. Verify SPF, DKIM, DMARC are set up
2. Check content for spam triggers
3. Warm up sending volume gradually
4. Build engagement (opens/clicks improve reputation)

## AWS CLI Diagnostics

### Account Status

```bash
# Get sending quota and daily usage
aws ses get-send-quota

# Check if in sandbox (SESv2)
aws sesv2 get-account

# Account-level suppression settings
aws sesv2 get-account --query 'SuppressionAttributes'
```

### Identity Verification

```bash
# List verified domains
aws ses list-identities --identity-type Domain

# List verified email addresses
aws ses list-identities --identity-type EmailAddress

# Check verification status for a domain
aws ses get-identity-verification-attributes \
  --identities yourapp.com

# Full identity details (SESv2)
aws sesv2 get-email-identity --email-identity yourapp.com
```

### DKIM Status

```bash
# Check DKIM configuration
aws ses get-identity-dkim-attributes --identities yourapp.com

# SESv2 DKIM details
aws sesv2 get-email-identity --email-identity yourapp.com \
  --query 'DkimAttributes'
```

### MAIL FROM Configuration

```bash
# Check custom MAIL FROM domain
aws ses get-identity-mail-from-domain-attributes \
  --identities yourapp.com
```

### Configuration Sets

```bash
# List all configuration sets
aws sesv2 list-configuration-sets

# Get details for a configuration set
aws sesv2 get-configuration-set \
  --configuration-set-name my-config-set

# List event destinations
aws sesv2 get-configuration-set-event-destinations \
  --configuration-set-name my-config-set
```

### Sending Statistics

```bash
# Basic send stats (last 2 weeks, 15-min intervals)
aws ses get-send-statistics

# CloudWatch metrics for sends
aws cloudwatch get-metric-statistics \
  --namespace AWS/SES \
  --metric-name Send \
  --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 3600 \
  --statistics Sum
```

### Reputation Metrics

```bash
# Bounce rate (last 7 days)
aws cloudwatch get-metric-statistics \
  --namespace AWS/SES \
  --metric-name Reputation.BounceRate \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 86400 \
  --statistics Average

# Complaint rate (last 7 days)
aws cloudwatch get-metric-statistics \
  --namespace AWS/SES \
  --metric-name Reputation.ComplaintRate \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 86400 \
  --statistics Average
```

### Suppression List

```bash
# List suppressed addresses
aws sesv2 list-suppressed-destinations

# Filter by reason
aws sesv2 list-suppressed-destinations --reasons BOUNCE
aws sesv2 list-suppressed-destinations --reasons COMPLAINT

# Check specific address
aws sesv2 get-suppressed-destination \
  --email-address user@example.com

# Remove from suppression list
aws sesv2 delete-suppressed-destination \
  --email-address user@example.com

# Add to suppression list
aws sesv2 put-suppressed-destination \
  --email-address user@example.com \
  --reason COMPLAINT
```

### Test Sending

```bash
# Send test email
aws ses send-email \
  --from verified@yourapp.com \
  --to recipient@example.com \
  --subject "Test Email" \
  --text "This is a test email sent via AWS CLI."

# Verify email address (sandbox mode)
aws ses verify-email-identity --email-address test@example.com
```

### DNS Verification (External)

```bash
# Check DKIM records
dig +short TXT selector1._domainkey.yourapp.com

# Check SPF record
dig +short TXT yourapp.com | grep spf

# Check DMARC record
dig +short TXT _dmarc.yourapp.com

# Check MX record (for custom MAIL FROM)
dig +short MX mail.yourapp.com
```
