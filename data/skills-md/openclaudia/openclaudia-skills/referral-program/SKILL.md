---
name: referral-program
description: >
  Design referral programs and viral growth loops. Use when asked to create
  referral systems, viral mechanics, word-of-mouth campaigns, or growth loops.
  Trigger phrases: "referral program", "viral loop", "refer a friend",
  "word of mouth", "viral coefficient", "referral incentive", "growth loop",
  "invite system", "ambassador program".
---

# Referral Program Design

Design effective referral programs and viral loops that drive sustainable growth.

---

## 1. Referral Program Frameworks

### One-Sided Incentives

Only the referrer gets rewarded.

**Best for:**
- Products with strong organic word-of-mouth
- Low-friction signups where the referred user needs no extra motivation
- Cost-sensitive businesses

**Examples:**
- Uber: "$10 credit for every friend you refer"
- Amazon Associates: Commission on referred purchases

**Template:**
```
Refer a friend and get [reward].
Share your unique link: [referral_url]
```

### Two-Sided Incentives

Both referrer and referred user get rewarded.

**Best for:**
- Products requiring activation effort from new users
- Competitive markets where new users need a nudge
- Subscription businesses

**Examples:**
- Dropbox: Both get 500MB extra storage
- Airbnb: Referrer gets $25 credit, friend gets $40 off first stay
- PayPal: Both get $10 when friend makes first transaction

**Template:**
```
Give [friend_reward], get [referrer_reward].
Share your link and you both win: [referral_url]
```

### Tiered Incentives

Rewards increase with number of successful referrals.

**Example tier structure:**
| Referrals | Reward |
|-----------|--------|
| 1 | Free month |
| 3 | Exclusive feature unlock |
| 5 | Premium plan for 3 months |
| 10 | Lifetime premium access |
| 25 | Cash payout or swag box |

**Best for:**
- Creating power referrers / ambassadors
- Products with passionate user bases
- Building a referral leaderboard culture

---

## 2. Viral Coefficient Calculation

The viral coefficient (K-factor) determines whether your referral loop is self-sustaining.

### Formula

```
K = i * c

Where:
  i = number of invites sent per user
  c = conversion rate of each invite

If K > 1: viral growth (each user brings more than one new user)
If K < 1: referrals supplement but don't replace other acquisition
```

### Example Calculation

```
Users send an average of 5 invites (i = 5)
15% of invites convert to signups (c = 0.15)
K = 5 * 0.15 = 0.75

With 1,000 initial users:
- Cycle 1: 1,000 * 0.75 = 750 new users
- Cycle 2: 750 * 0.75 = 563 new users
- Cycle 3: 563 * 0.75 = 422 new users
- Total after 10 cycles: ~3,570 additional users from referrals
```

### Viral Cycle Time

The speed of the viral loop matters as much as K:

```
Effective growth = K / cycle_time

A K of 0.5 with a 1-day cycle > K of 0.8 with a 30-day cycle
```

### How to Improve K

| Lever | Action |
|-------|--------|
| Increase invites (i) | Make sharing frictionless, prompt at key moments |
| Increase conversion (c) | Better landing page, stronger incentive, social proof |
| Reduce cycle time | Instant reward delivery, real-time notifications |

---

## 3. Referral Channels

### Email Referral

**Pros:** High conversion, personal, trackable
**Cons:** Lower volume, requires email access

Template:
```
Subject: I thought you'd like [Product] -- here's [reward] to try it

Hey [Name],

I've been using [Product] for [time] and it's been great for [specific benefit].

I wanted to share my referral link so you can get [friend_reward]:
[referral_url]

[Your name]
```

### Social Media Sharing

**Pros:** High reach, low effort, viral potential
**Cons:** Lower conversion rate, less personal

Platform-specific templates:

**Twitter/X:**
```
I just [achievement/milestone] with @Product! If you want to try it,
use my link and we both get [reward]: [referral_url]
```

**LinkedIn:**
```
I've been using [Product] to [professional benefit] and the results
have been impressive: [specific metric].

If you're looking for [solution], here's my referral link
(we both get [reward]): [referral_url]
```

**WhatsApp/SMS:**
```
Hey! I've been using [Product] and really like it. They have a
referral deal -- we both get [reward] if you sign up through my link:
[referral_url]
```

### In-App Referral

**Pros:** Highest intent, contextual, frictionless
**Cons:** Only reaches existing users

Best practices:
- Show referral prompt after a success moment (completed task, achievement, positive outcome)
- Pre-populate sharing message
- Show referral progress and rewards earned
- Add referral widget to account/settings page

### Unique Link vs. Referral Code

| Method | Pros | Cons |
|--------|------|------|
| Unique link | Frictionless, works in any channel | Harder to share verbally |
| Referral code | Easy to remember, shareable verbally | Extra step at signup |
| Both | Maximum flexibility | More complex to implement |

---

## 4. Referral Landing Page Template

The page a referred user sees when they click the referral link.

### Structure

```
[Hero Section]
- Headline: "[Referrer's name] invited you to [Product]"
- Subheadline: "Sign up now and get [friend_reward]"
- CTA button: "Claim your [reward]"

[Social Proof]
- "[Referrer's name] and X others use [Product]"
- Logos of known customers
- Key metric: "Trusted by X users"

[Value Proposition]
- 3 key benefits with icons
- Brief product description

[How It Works]
- Step 1: Sign up (takes 30 seconds)
- Step 2: [Key activation action]
- Step 3: Enjoy [reward] + the product

[CTA Repeat]
- "Join [Referrer's name] on [Product]"
- Urgency: "This offer expires in [X days]"

[FAQ]
- When do I get my reward?
- What does [Product] do?
- Is there a catch?
```

---

## 5. Case Studies

### Dropbox (2008-2010)

- **Mechanic:** Two-sided -- both get 500MB extra storage
- **Result:** 3,900% growth in 15 months (100K to 4M users)
- **Key insight:** The reward (storage) was the product itself, making it self-reinforcing
- **Viral coefficient:** Estimated ~0.6-0.7 (supplemental, not purely viral)

### Airbnb (2014)

- **Mechanic:** Two-sided -- $25 travel credit for referrer, $40 off first booking for friend
- **Result:** 300% increase in bookings from referral program 2.0
- **Key insight:** Redesigned referral page to feel like a gift, not spam. Personalized with referrer's photo and travel history
- **Viral coefficient:** Low K but high LTV per referred user

### PayPal (1999-2000)

- **Mechanic:** Two-sided -- $20 per referral (later reduced to $10, then $5)
- **Result:** 7-10% daily growth, reaching 1M users in first year
- **Key insight:** Cash incentive drove massive initial growth, then reduced as network effects kicked in
- **Cost:** $60-70M in referral bonuses, but each user was worth much more in LTV

### Robinhood (2014-2015)

- **Mechanic:** Wait-list with move-up-the-line incentive + free stock for referrals
- **Result:** 1M waitlist signups before launch
- **Key insight:** Scarcity (waitlist) + social proof (your position) + tangible reward (free stock)

---

## 6. Implementation Checklist

### Technical Setup

- [ ] Generate unique referral links/codes per user
- [ ] Build referral tracking (link clicks, signups, activations, rewards)
- [ ] Set up attribution window (how long after click does signup count?)
- [ ] Implement fraud detection (self-referral, fake accounts, VPN abuse)
- [ ] Build reward fulfillment (automatic credit, manual approval, or hybrid)
- [ ] Create referral dashboard for users (invites sent, pending, completed, rewards earned)

### Fraud Prevention

- [ ] Block self-referrals (same IP, same device, same email domain)
- [ ] Require activation action before reward (not just signup)
- [ ] Set daily/weekly referral limits per user
- [ ] Flag suspicious patterns (bulk signups from same IP range)
- [ ] Implement clawback for fraudulent referrals

### Program Design Decisions

| Decision | Options |
|----------|---------|
| Reward type | Cash, credit, product features, swag, charity donation |
| Reward timing | On signup, on activation, on first purchase |
| Reward amount | Test multiple amounts; higher is not always better |
| Expiration | Referral links expire after X days? Rewards expire? |
| Limit | Max referrals per user per month? |
| Eligibility | All users or only paid/active users? |

---

## 7. Referral Email Sequences

### Invite Reminder (to existing users)

```
Subject: You have [X] invites waiting

Hey [Name],

Did you know you can give your friends [reward] and get [reward] for yourself?

You've invited [0/N] friends so far. Share your link:
[referral_url]

Here's what [Product] users are saying:
"[Testimonial]" -- [Customer name]
```

### Referred User Welcome

```
Subject: [Referrer] sent you a gift -- [reward] inside

Hey there!

[Referrer's name] thinks you'd love [Product], so they're giving you [reward] to try it.

[CTA: Claim your reward]

What is [Product]?
[1-sentence description]

What you'll get:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]
- Plus [friend_reward] from [Referrer's name]

This offer expires in [X] days.
```

### Referral Success Notification

```
Subject: [Friend's name] just signed up -- you earned [reward]!

Great news, [Name]!

[Friend's name] accepted your invitation and signed up for [Product].
Your [reward] has been added to your account.

Keep sharing: you've referred [X] friends so far.
[referral_url]

[Show progress toward next tier if using tiered rewards]
```

---

## 8. Measuring Success

### Key Metrics

| Metric | Formula | Good Benchmark |
|--------|---------|----------------|
| Participation rate | Users who share / total users | 15-25% |
| Shares per user | Total shares / participating users | 3-5 |
| Click-through rate | Link clicks / shares | 20-40% |
| Conversion rate | Signups / link clicks | 10-25% |
| Viral coefficient (K) | Invites * conversion rate | 0.3-0.7 typical |
| Viral cycle time | Avg days from invite to new user's first invite | 1-7 days |
| Referral revenue | Revenue from referred users | Track separately |
| CAC via referral | Reward cost / acquired users | Compare to paid CAC |

### A/B Tests to Run

1. Reward amount ($10 vs $20 vs $50)
2. Reward type (credit vs cash vs feature unlock)
3. One-sided vs two-sided incentive
4. Referral prompt timing (after signup vs after first success)
5. Landing page copy (gift framing vs deal framing)
6. Email subject lines for referral invites
7. Social sharing copy variations
