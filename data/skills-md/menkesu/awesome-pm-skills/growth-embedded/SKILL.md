---
name: growth-embedded
description: Builds growth loops into products from day 1 using YC playbook (Gustaf Alstromer), Casey Winters growth frameworks, and Elena Verna's retention-first approach. Use when adding viral mechanics, instrumenting analytics, creating referral systems, or optimizing for retention over acquisition.
---

# Growth-First Development

## When This Skill Activates

Claude uses this skill when:
- Building features that could have viral mechanics
- Adding referral or sharing functionality
- Implementing analytics and tracking
- Designing for network effects
- Optimizing for activation and retention

## Core Frameworks

### 1. YC Growth Playbook (Source: Gustaf Alstromer, Partner at YC)

**The Three Growth Levers:**

**📈 Acquisition** - How users discover you
**🎯 Activation** - First value experience
**🔁 Retention** - Users coming back

**Priority Order:**
> "Retention first, activation second, acquisition last. Don't acquire users you can't retain."

**Growth Loops:**
```
User gets value → Shares with others → New users → Cycle repeats
```

**Examples:**
- Dropbox: More storage for referrals
- Superhuman: Invite-only creates FOMO
- Notion: Shared docs bring collaborators

---

### 2. Network Effects Patterns

**Types:**

**Direct Network Effects:**
- More users = more value for all
- Example: Social networks, marketplaces

**Data Network Effects:**
- More usage = smarter product
- Example: Recommendations, AI features

**Platform Network Effects:**
- More developers = more integrations
- Example: Shopify apps, Zapier

---

### 3. Referral Mechanics

**Double-Sided Incentive:**
```
Referrer gets: [benefit]
Referred gets: [benefit]
Both win: [shared value]
```

**Tracking:**
```javascript
// Referral flow
generateReferralLink(user) {
  const link = `app.com/ref/${user.id}`;
  track('referral_link_generated', { userId: user.id });
  return link;
}

// Attribution
onSignup(referralCode) {
  const referrer = getUserByRefCode(referralCode);
  track('referral_signup', { 
    referrer: referrer.id,
    referred: newUser.id 
  });
  giveReward(referrer);
  giveReward(newUser);
}
```

---

### 4. Activation Optimization

**Time to Value:**
> "Get users to 'aha moment' as fast as possible"

**Activation Milestones:**
1. Signup complete
2. Setup complete
3. First value delivered
4. Habit formed

**Measure:**
```
Activation Rate = (Users who reached value) / (Total signups)
```

---

## Decision Tree: Growth Feature

```
NEW FEATURE
│
├─ Can users share this? ──────YES──→ ADD SHARE FUNCTIONALITY
│  NO ↓
│
├─ Creates network effects? ───YES──→ OPTIMIZE FOR VIRAL LOOPS
│  NO ↓
│
├─ First-time experience? ─────YES──→ OPTIMIZE ACTIVATION
│  NO ↓
│
├─ Repeat usage? ──────────────YES──→ INSTRUMENT RETENTION TRACKING
│  NO ↓
│
└─ STANDARD FEATURE ←──────────────────┘
   (Still track basic analytics)
```

## Action Templates

### Template 1: Referral System

```markdown
# Referral Feature

## Incentive Structure
- **Referrer gets:** [reward]
- **Referred gets:** [reward]
- **Both benefit:** [shared value]

## Implementation
```javascript
// Generate referral link
const link = generateReferralLink(user);

// Track shares
track('referral_shared', { 
  channel: ['email', 'social', 'link'],
  userId: user.id 
});

// Track conversions
track('referral_converted', {
  referrerId: referrer.id,
  referredId: newUser.id,
  timeToConversion: timestamp
});

// Reward both
giveReward(referrer, 'storage_upgrade');
giveReward(newUser, 'welcome_bonus');
```

## Metrics
- Link generation rate
- Share rate
- Conversion rate (clicked → signed up)
- Activation rate (signed up → activated)
- K-factor (viral coefficient)
```

### Template 2: Activation Flow

```markdown
# Activation Optimization

## Time to Value
- Target: <[X] minutes
- Current: [Y] minutes

## Activation Funnel
1. **Signup** (100% of signups)
2. **Profile Setup** ([X]%)
3. **First Action** ([X]%)
4. **Aha Moment** ([X]%)
5. **Habit Formation** ([X]%)

## Drop-off Points
- Biggest drop-off: [identify]
- Why: [hypothesis]
- Fix: [solution]

## Implementation
```javascript
// Track activation milestones
track('activation_milestone', {
  milestone: 'profile_complete',
  userId: user.id,
  timeToComplete: seconds
});

// Identify where users drop off
if (!completedSetup(user, 24hours)) {
  sendReminderEmail(user);
}
```
```

### Template 3: Growth Analytics

```markdown
# Growth Metrics Dashboard

## Acquisition
- New signups: [X per day]
- Channels: [organic, referral, paid]
- Cost per acquisition: [$X]

## Activation
- Activation rate: [X]%
- Time to first value: [X] minutes
- Drop-off point: [step in funnel]

## Retention
- Day 1: [X]%
- Day 7: [X]%
- Day 30: [X]%
- Retention curve: [improving / flat / declining]

## Referral
- K-factor: [X] (viral coefficient)
- Referral rate: [X]% of users refer
- Conversion rate: [X]% of referred sign up

## Implementation
```javascript
// Track key events
track('user_activated', { userId, timestamp });
track('user_retained_day7', { userId, timestamp });
track('referral_sent', { referrerId, channel });
```
```

## Quick Reference

### 🚀 Growth Checklist

**Acquisition:**
- [ ] Referral system implemented
- [ ] Viral loops identified
- [ ] Share buttons prominent

**Activation:**
- [ ] Time to value < 5 minutes
- [ ] Onboarding optimized
- [ ] Aha moment clear

**Retention:**
- [ ] Usage triggers implemented
- [ ] Email/push notifications
- [ ] Habit formation designed

**Analytics:**
- [ ] Cohort retention tracking
- [ ] Funnel analysis
- [ ] Attribution tracking

---

## Real-World Examples

### Example 1: Dropbox Referral

**Incentive:**
- Referrer: +500MB storage
- Referred: +500MB storage
- Both win: More space

**Result:** 35% of signups from referrals

---

### Example 2: Superhuman Activation

**Time to Value:**
- < 2 minutes to first email sent
- Guided onboarding
- Keyboard shortcuts taught early

**Result:** 90%+ retention

---

### Example 3: Notion Network Effects

**Growth Loop:**
- User creates doc → Shares with team → Team joins Notion → Creates more docs → Cycle repeats

**Result:** Viral growth in teams

---

## Common Pitfalls

### ❌ Mistake 1: Optimizing Acquisition Before Retention
**Problem:** Leaky bucket - users leave as fast as they join
**Fix:** Fix retention first, then acquire

### ❌ Mistake 2: No Viral Mechanics
**Problem:** Every user requires paid acquisition
**Fix:** Build sharing into core features

### ❌ Mistake 3: Slow Activation
**Problem:** Users drop off before seeing value
**Fix:** Get to aha moment in < 5 minutes

---

## Related Skills

- **zero-to-launch** - For building growth into MVP
- **metrics-frameworks** - For measuring growth metrics
- **exp-driven-dev** - For A/B testing growth features
- **user-feedback-system** - For improving retention

---

## Key Quotes

**Gustaf Alstromer:**
> "Retention first, activation second, acquisition last. Don't pour water into a leaky bucket."

**Casey Winters:**
> "The best growth loops are built into the product, not bolted on."

**Elena Verna:**
> "Acquisition is a tax on poor retention."

---

## Further Learning

- **references/yc-growth-playbook.md** - Complete YC growth frameworks
- **references/referral-examples.md** - Successful referral programs
- **references/activation-patterns.md** - Onboarding best practices
- **references/retention-strategies.md** - Building habit-forming products

