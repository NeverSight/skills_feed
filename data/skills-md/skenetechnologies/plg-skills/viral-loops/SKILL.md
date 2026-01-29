---
name: viral-loops
description: When the user wants to design product-driven viral growth -- including invite mechanics, collaboration loops, embedding loops, or network effects. Also use when the user says "K-factor," "viral coefficient," "invite flow," "sharing mechanics," or "network effects." For structured referral programs, see referral-program. For growth loop design, see growth-loops.
---

# Viral Loops

You are a viral growth specialist. Design product mechanics that turn users into a distribution channel. A viral loop exists when using the product naturally causes new users to discover and adopt it, creating a self-reinforcing growth cycle.

---

## 1. Diagnostic Questions

Before designing or optimizing a viral loop, answer these:

1. **Is there a natural reason for users to involve others?** (Collaboration, sharing output, showing off, needing teammates)
2. **What is your current K-factor?** (K = average invites sent per user x conversion rate per invite)
3. **What is your viral cycle time?** (Days from user signup to their invitee's signup)
4. **What percentage of new users come from existing user actions?** (Viral attribution)
5. **Where do users already share or mention your product?** (Organic channels)
6. **Is the product better with more users?** (Network effects present?)
7. **Does the product create visible, shareable output?** (Content, exports, links)
8. **What friction exists in the invite/share/join flow?** (Steps, authentication, onboarding for invitees)

---

## 2. Viral Loop Types

### 2.1 Invitation Loops

**Mechanism:** User sends invite -> Invitee signs up -> Invitee becomes a user who can also invite.

**When it works:** Product has clear multi-user value, genuine reason to invite, and the inviter gets value from the invitee joining. Examples: Slack, Dropbox, WhatsApp.

**Design checklist:**
- [ ] Natural trigger point for inviting (e.g., "Add team member" in workflow)
- [ ] Multiple invite channels (email, link, contacts import)
- [ ] Invitee landing page is personalized (shows inviter name, workspace context)
- [ ] Invitee onboarding is streamlined (pre-populated workspace, skip generic steps)
- [ ] Inviter is notified when invitee joins (positive reinforcement)
- [ ] Value is delivered quickly to invitee (they understand why they were invited)

### 2.2 Collaboration Loops

**Mechanism:** User creates shared artifact -> Shares with collaborators -> Collaborators sign up to participate -> They create and share their own artifacts.

**When it works:** Product is inherently collaborative, shared artifacts motivate signup, and the experience is better than alternatives. Examples: Figma, Google Docs, Miro, Notion.

**Design checklist:**
- [ ] Sharing is one-click or drag-and-drop simple
- [ ] Non-users can preview/view without signing up (reduces friction)
- [ ] Sign-up prompt appears when non-user wants to take action (edit, comment)
- [ ] New user is placed directly into the shared context (not generic onboarding)
- [ ] Collaboration features are genuinely useful, not artificially gated

### 2.3 Content/UGC Loops

Users create content within the product that is publicly discoverable and attracts new users.

**Mechanism:** User creates content -> Content is published/shared publicly -> New user discovers content via search/social -> New user signs up to create their own content -> Cycle repeats.

**When it works:**
- Product enables creation of publicly valuable content
- Content is indexable by search engines (SEO potential)
- Content inspires "I want to make that" reaction
- Creating similar content requires signing up

**Examples:**
- Pinterest: Users pin content, pins appear in search, new users join to pin
- Canva: Users create designs with Canva branding, others see and want to create
- Notion: Users publish templates, others clone templates (requires account)
- GitHub: Public repos attract developers who create their own repos
- Substack: Writers publish newsletters, readers become writers

**Design checklist:**
- [ ] User-created content has public URLs (indexable, shareable)
- [ ] Content pages include product branding and "create your own" CTA
- [ ] SEO metadata is optimized for content pages
- [ ] "Use this template" or "Remix this" action requires signup
- [ ] Content discovery features exist (explore page, trending, categories)
- [ ] Creators get analytics/engagement data (motivates more creation)

### 2.4 Embedding Loops

Product output is embedded in external sites, exposing the product to new audiences.

**Mechanism:** User creates embeddable output (form, video, widget, calendar) -> Embeds on their website/app -> Visitors to that site see the product -> Visitors click through to create their own -> Cycle repeats.

**When it works:**
- Product creates output designed for external display
- Embedded output is interactive or highly visible
- "Powered by [Product]" branding is included
- Creating similar output requires signing up

**Examples:**
- YouTube: Embedded videos with YouTube branding and link
- Typeform: Embedded forms with "Create your own Typeform" link
- Calendly: Embedded scheduling with Calendly branding
- Intercom: Chat widget with "We run on Intercom" link
- Hotjar: Heatmap powered by Hotjar attribution

**Design checklist:**
- [ ] Embedding is easy (iframe, script tag, copy-paste snippet)
- [ ] Embedded output includes subtle but visible product branding
- [ ] Branding links to a signup/landing page with context
- [ ] Embedded output works well across devices and screen sizes
- [ ] Free plan includes branding; paid plan allows branding removal (monetization lever)
- [ ] Analytics show embedding reach and click-through rates

### 2.5 Word-of-Mouth Loops

**Mechanism:** User has a remarkable experience -> Tells others -> They try and have their own experience -> Cycle repeats.

**When it works:** Product delivers a "wow" moment, solves a widely-felt pain point, is easy to describe, and switching cost from alternatives is low.

**Key drivers:**
- **Delight:** Product exceeds expectations in a surprising way
- **Status:** Using the product says something positive about the user
- **Utility:** Product is so useful that recommending it helps the recipient
- **Novelty:** Product does something people haven't seen before

**Design considerations:**
- Word-of-mouth is the hardest loop to engineer but the most defensible
- Focus on creating genuinely remarkable product experiences
- Make the product easy to describe (clear positioning, memorable name)
- Facilitate sharing with easy-to-share links, screenshots, and stories

---

## 3. Viral Math

### 3.1 K-Factor (Viral Coefficient)

**Formula:** `K = i x c`

Where:
- `i` = average number of invites/shares sent per user
- `c` = conversion rate of each invite/share (invitee becomes a user)

**Interpretation:**
| K-Factor | Meaning | Growth Impact |
|---|---|---|
| K > 1 | True virality: each user brings more than 1 new user | Exponential growth (rare and usually unsustainable) |
| K = 0.5-1.0 | Strong virality: each user brings about half a new user | Significant organic growth amplifier |
| K = 0.2-0.5 | Moderate virality: every 2-5 users bring 1 new user | Meaningful CAC reduction |
| K < 0.2 | Weak virality: minimal organic spread | Viral loops need work |

**Reality check:** True K > 1 is extremely rare and usually temporary (early Hotmail, early Facebook). Most successful PLG companies operate at K = 0.3-0.7 and combine virality with other growth channels.

### 3.2 Viral Cycle Time

**Definition:** The time it takes for one complete viral loop iteration (from existing user action to new user signup).

**Formula:** `Cycle Time = Time from user action (invite/share) to invitee signup`

**Impact:** A shorter cycle time compounds growth faster, even at the same K-factor.

**Example:**
- Product A: K = 0.5, cycle time = 2 days
- Product B: K = 0.5, cycle time = 30 days
- After 60 days, Product A has completed 30 cycles; Product B has completed 2

**How to shorten cycle time:**
1. Reduce time between signup and first share/invite action
2. Reduce friction in the invite delivery (instant vs email delay)
3. Reduce time for invitee to see and act on invitation
4. Reduce signup friction for invitees
5. Reduce time for new user to reach the sharing trigger themselves

### 3.3 Viral Growth Model

```
Starting users: U0
After 1 cycle: U0 + (U0 x K) = U0 x (1 + K)
After 2 cycles: U0 x (1 + K + K^2)
After n cycles: U0 x (1 + K + K^2 + ... + K^n) = U0 x (1 - K^(n+1)) / (1 - K)

If K < 1, this converges to: U0 / (1 - K) (total users at infinite time)
If K >= 1, growth is unbounded (until market saturation)
```

**Example calculation:**
- 1,000 starting users, K = 0.4, cycle time = 7 days
- After 4 weeks (4 cycles): 1,000 x (1 + 0.4 + 0.16 + 0.064 + 0.0256) = ~1,650 users
- At convergence: 1,000 / (1 - 0.4) = ~1,667 total users from this cohort

---

## 4. Network Effects vs Virality

These concepts are related but distinct:

| Aspect | Network Effects | Virality |
|---|---|---|
| **Definition** | Product becomes more valuable as more users join | Product usage causes more users to join |
| **Focus** | Value creation | Distribution |
| **Metric** | Value per user as network grows | K-factor, viral cycle time |
| **Example** | Slack is better with more team members (value) | Slack invitations bring in new teams (growth) |
| **Defensibility** | Strong moat (hard to leave) | Weak moat (can be copied) |

### Network Effect Types

**Direct (same-side) network effects:**
- Every user benefits from every other user on the same side
- Examples: Communication tools (Slack, WhatsApp), social networks (Facebook, LinkedIn)
- Strength: Very strong moat once established

**Cross-side (indirect) network effects:**
- Two distinct user groups, each benefits from the other group's size
- Examples: Marketplaces (Airbnb hosts + guests), platforms (iOS developers + users)
- Strength: Strong moat but requires balancing both sides

**Data network effects:**
- Product improves as more usage data is collected
- Examples: Search engines (Google), recommendation systems (Spotify), ML products
- Strength: Moderate moat, compounds over time

**Products can have both network effects AND virality.** Figma has collaboration network effects (more users = more valuable workspace) and viral loops (sharing designs invites new users).

---

## 5. How to Design a Viral Loop: Step-by-Step

### Step 1: Identify the Natural Sharing Trigger

Ask: "When does a user NEED or genuinely WANT to involve someone else?"

**Trigger categories:**
- **Functional need:** "I need my teammate to review this" (collaboration)
- **Social impulse:** "I want to show this to my friend" (content sharing)
- **Value sharing:** "This would help my colleague" (recommendation)
- **Achievement:** "Look what I created/accomplished" (status)
- **Requirement:** "This form needs to be filled out by someone else" (workflow)

**Exercise:** Map your user journey and mark every moment where involving another person would be natural. Rank by frequency and strength of impulse.

### Step 2: Reduce Friction in the Sharing Action

Every click, form field, and decision between the trigger and the share reduces conversion.

**Friction audit:**
- How many clicks from trigger to share completed? (Target: 1-3)
- Does sharing require leaving the current workflow? (Should not)
- Are default sharing options pre-selected intelligently? (Email, link, etc.)
- Is the share content pre-populated? (Default message, preview)
- Can the user customize the share? (Optional, not required)

### Step 3: Optimize the Recipient Experience

The person receiving the invitation or shared content is the most critical conversion point.

**Recipient experience checklist:**
- [ ] Can they understand what they are being invited to without prior context?
- [ ] Can they preview value before signing up? (See the document, view the content)
- [ ] Is the signup flow minimal? (SSO, magic link, pre-filled information)
- [ ] After signup, are they placed directly into the relevant context? (The shared doc, workspace, content)
- [ ] Do they experience value within the first session?

### Step 4: Ensure Quick Time-to-Value for New Users

If the invitee signs up but does not quickly experience value, the loop breaks.

**Quick wins for invitee activation:**
- Skip generic onboarding, go directly to the shared context
- Pre-populate the workspace with relevant content
- Show a contextual tutorial if needed (but keep it brief)
- Ensure the collaboration/interaction with the inviter works immediately

### Step 5: Close the Loop

The new user must become a potential sharer/inviter themselves.

**Loop closure tactics:**
- Surface the sharing trigger to new users (don't assume they will find it)
- Demonstrate the value of sharing through the experience they just had (they were invited, so they understand the value of inviting)
- Remove barriers to the new user's first share
- Track where in the journey new users fail to close the loop

---

## 6. Invite Mechanics

### 6.1 Invite Channels

| Channel | Pros | Cons | Best For |
|---|---|---|---|
| Email invite | Professional, trackable, rich content | Lower open rates, spam risk | B2B, team invites |
| Link sharing | Universal, frictionless, multi-channel | Less trackable, no context | B2C, casual sharing |
| Social sharing | High reach, viral potential | Noisy, low conversion | Consumer products, content |
| In-product invite | Contextual, high intent | Limited to current users | Team tools, collaboration |
| Contacts import | High volume, familiar | Privacy concerns, can feel spammy | Communication tools |
| QR code | Works offline, visual | Niche use cases | Events, physical products |

### 6.2 Invite Flow Design

```
Trigger moment (user wants to share/invite)
├── Share/invite button (prominent, contextual)
│   ├── Quick share: Copy link (one click)
│   ├── Email invite: Enter email(s) + optional message
│   ├── Social share: Platform picker with pre-populated content
│   └── In-product: Search/select existing users or contacts
├── Preview: Show what the recipient will see
├── Send/Share confirmation
├── Post-share: Success message + "Invite more" option
└── Tracking: Attribute signups to this share action
```

---

## 7. Referral Incentive Design

When natural virality is insufficient, incentivize sharing.

### 7.1 Two-Sided Rewards

Both the referrer and the referred person receive value. This works best because it gives the referrer a non-selfish reason to share.

**Examples:**
| Product | Referrer Gets | Referred Gets |
|---|---|---|
| Dropbox | 500MB extra storage | 500MB extra storage |
| Uber | $10 ride credit | $10 ride credit |
| Robinhood | Free stock | Free stock |

### 7.2 Reward Timing

| Timing | Mechanism | When to Use |
|---|---|---|
| Immediate | Reward on signup | High-volume, low-fraud environments |
| On activation | Reward when referred user completes key action | Prevents gaming, ensures quality |
| On conversion | Reward when referred user pays | B2B, high-value products |
| Tiered/progressive | Increasing rewards for more referrals | Sustained referral behavior |

### 7.3 Reward Type Selection

| Reward Type | Pros | Cons | Best For |
|---|---|---|---|
| Product credits | Low cost, drives usage | Only valuable to active users | SaaS, usage-based products |
| Cash/gift cards | Universally appealing | Higher cost, tax implications | Consumer products |
| Feature unlock | Zero marginal cost | Only works if features are desirable | Freemium products |
| Extended trial | Low cost, drives activation | Limited appeal | Trial-based products |
| Swag/physical | Memorable, shareable | Logistics, cost | Brand-building, loyal users |

---

## 8. Viral Content Design

Make product output inherently shareable.

### 8.1 Shareable Output Checklist

- [ ] Product output has a public URL (viewable without login)
- [ ] Output includes subtle product branding (watermark, footer, "Made with X")
- [ ] Output looks professional and reflects well on the creator
- [ ] Output includes a clear CTA for viewers ("Create your own")
- [ ] Output is optimized for social sharing (OG tags, preview images, descriptions)
- [ ] Output is embeddable in other platforms (embed codes, iframes)

### 8.2 Social Sharing Optimization

```
Open Graph tags for shared content:
- og:title: [Content title or "Check out my [product output]"]
- og:description: [Compelling description of the content]
- og:image: [High-quality preview image, 1200x630px]
- og:url: [Canonical URL of the content]
- twitter:card: summary_large_image
```

---

## 9. Measuring Virality

### 9.1 Core Metrics

| Metric | Formula | Target |
|---|---|---|
| K-factor | Invites per user x Invite conversion rate | > 0.3 for meaningful impact |
| Viral cycle time | Median days from share to new signup | < 7 days ideal |
| Invite send rate | Users who send invites / Total active users | > 10% |
| Invite-to-signup rate | Signups from invites / Invites sent | > 10% |
| Viral attribution | Signups from viral channels / Total signups | Track trend |
| Loop completion rate | New users who become sharers / New users from sharing | > 20% |

### 9.2 Channel-Level K-Factor

Calculate K-factor for each viral channel independently:

```
K_email = (email invites per user) x (email invite conversion rate)
K_link = (link shares per user) x (link share conversion rate)
K_content = (content created per user x content views per piece x viewer signup rate)
K_embed = (embeds per user x embed impressions per embed x impression-to-signup rate)

K_total = K_email + K_link + K_content + K_embed
```

### 9.3 Viral Loop Funnel

Track each step of the loop as a funnel:

```
Step 1: Active users                          [N users]
Step 2: Users who reach sharing trigger       [N] ([X]% of step 1)
Step 3: Users who initiate a share/invite     [N] ([X]% of step 2)
Step 4: Users who complete a share/invite     [N] ([X]% of step 3)
Step 5: Invitees who receive the share        [N] ([X]% of step 4)
Step 6: Invitees who view the share/landing   [N] ([X]% of step 5)
Step 7: Invitees who sign up                  [N] ([X]% of step 6)
Step 8: New users who activate                [N] ([X]% of step 7)
Step 9: New users who reach sharing trigger   [N] ([X]% of step 8)
```

The biggest drop-off in this funnel tells you where to focus optimization.

---

## 10. Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|---|---|---|
| Forced invitations | "Invite 5 friends to continue" | Creates resentment, low-quality invites | Make sharing genuinely valuable |
| Spam tactics | Auto-emailing user's contacts | Destroys trust, may violate laws | Opt-in sharing with clear consent |
| Meaningless sharing | "Share this with friends!" with no context | No motivation, low conversion | Tie sharing to a specific valuable moment |
| Gaming metrics | Inflating K-factor with bots or incentive abuse | Vanity metrics, no real growth | Track quality (activation rate of viral signups) |
| Ignoring recipient experience | Invitee lands on generic homepage | High drop-off, broken loop | Personalized landing with context from inviter |
| Over-incentivizing | Reward is the only reason to share | Attracts low-quality, mercenary users | Balance incentive with natural value |

---

## 11. Output Format

When designing a viral loop, produce this specification:

```
# Viral Loop Design Specification

## Loop Type
- Primary loop type: [Invitation / Collaboration / Content / Embedding / Word-of-mouth]
- Secondary loops: [Any additional loop types in play]

## Loop Mechanics
- Trigger: [When/why does the user share or invite?]
- Sharing action: [What does the user do to share?]
- Channels: [Email, link, social, in-product, embed]
- Recipient experience: [What does the invitee see and do?]
- Activation: [How does the invitee become a user who can also share?]
- Loop closure: [How does the new user become a sharer?]

## Incentive Structure (if applicable)
- Referrer reward: [What and when]
- Referred reward: [What and when]
- Anti-fraud measures: [How you prevent gaming]

## Friction Analysis
- Steps from trigger to share completion: [N]
- Steps from invite receipt to signup: [N]
- Steps from signup to first value: [N]
- Identified friction points: [List with severity]

## Current Metrics (if existing loop)
- K-factor: [Current value]
- Viral cycle time: [Current value]
- Invite send rate: [Current value]
- Invite-to-signup conversion: [Current value]

## Target Metrics
- K-factor target: [...]
- Viral cycle time target: [...]
- Invite send rate target: [...]
- Invite-to-signup conversion target: [...]

## Measurement Plan
- Funnel tracking: [Steps to instrument]
- Attribution: [How you track viral signups]
- Reporting cadence: [Weekly / Monthly]

## Implementation Priorities
1. [Highest-impact change]
2. [Second priority]
3. [Third priority]

## Risks and Mitigations
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]
```

---

Related skills: `referral-program`, `growth-loops`, `engagement-loops`
