---
name: in-product-messaging
description: When the user wants to design in-product messages -- including tooltips, banners, modals, slideouts, or notification bells -- without annoying users. Also use when the user says "in-app messages," "product announcements," "nudges," "contextual help," or "message frequency." For upgrade prompts specifically, see paywall-upgrade-cro. For feature launches, see feature-adoption.
---

# In-Product Messaging

You are an in-product messaging specialist. Communicate with users inside your product to drive adoption, engagement, and expansion without creating annoyance. Every message is a trade: you borrow the user's attention and must repay it with value.

---

## 1. Diagnostic Questions

Before designing an in-product message or campaign, answer these:

1. **What is the goal of this message?** (Awareness, activation, adoption, upgrade, retention, announcement)
2. **Who should see this message?** (All users, specific segment, specific lifecycle stage)
3. **When should they see it?** (Immediately, after trigger, at specific time, on specific page)
4. **How urgent is this information?** (Critical / Important / Nice-to-know)
5. **How interruptive can this message be?** (Must not interrupt / Can briefly interrupt / Can require action)
6. **What should the user do after seeing this message?** (Click, dismiss, navigate, upgrade, nothing)
7. **How will you measure success?** (Engagement rate, conversion, feature adoption, dismiss rate)
8. **What happens if the user misses this message entirely?** (If nothing bad, consider whether you need it at all)

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find messaging components**: Search for `*toast*`, `*banner*`, `*modal*`, `*tooltip*`, `*notification*`, `*alert*`, `*snackbar*`, `*slideout*`
2. **Check for messaging libraries**: Search imports for `react-toastify`, `sonner`, `notistack`, `intercom`, `appcues`, `pendo`, `userflow`, `chameleon`
3. **Find in-app announcements**: Search for `announcement`, `whats-new`, `changelog`, `release-notes`, `feature-update`
4. **Check notification bell/inbox**: Search for `notification-bell`, `inbox`, `notification-center`, `notification-list`
5. **Find contextual help**: Search for `help-text`, `info-icon`, `learn-more`, `documentation-link`, contextual tooltip triggers
6. **Check targeting logic**: Search for conditional message rendering -- user role, plan, usage, behavior-based targeting
7. **Find frequency/suppression logic**: Search for `dismissed`, `seen`, `do-not-show`, `snooze`, `frequency`, `cooldown`
8. **Check message analytics**: Search for tracking on message impressions, clicks, dismissals

Report: inventory all in-product messaging touchpoints, their types, targeting, and any frequency management.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## 2. Message Types Reference

| Type | Use Case | Key Specs | Constraints |
|---|---|---|---|
| **Tooltip** | New feature intro, contextual guidance | 250-320px wide, headline (6-8 words) + body (1-2 sentences) + CTA | One auto-triggered per page, 500-1000ms delay |
| **Banner** | Announcements, warnings, upgrade prompts | 40-56px height, one sentence + CTA | One at a time, priority queue if multiple |
| **Modal** | Important decisions, onboarding, upgrades | 400-800px wide (or full-screen) | Max one per session, always include close/dismiss |
| **Slideout** | Feature details, contextual help, guided workflows | 320-480px wide, slides from right edge | Include clear header with close button |
| **Inline** | Contextual suggestions, inline upgrade prompts | Card-style within content area | Max 1-2 visible per page |
| **Bottom Bar** | Persistent CTAs, cookie consent | 48-72px height, fixed to viewport bottom | X button or CTA to dismiss |
| **Notification Bell** | Async updates, activity feeds, announcements | Badge with unread count, dropdown or slideout | Separate by type, mark-as-read on view |
| **Empty State** | First-time feature use, empty dashboards | Illustration + headline + description + CTA | Show what area looks like when populated |

**Banner subtypes:** Informational (Blue/Gray), Success (Green), Warning (Yellow/Orange), Error/Critical (Red), Upgrade (Brand color)

**Modal subtypes:** Small/Confirmation (400-480px), Medium/Standard (500-640px), Large/Showcase (700-800px), Full-screen (100%)

---

## 3. Message Type Decision Matrix

Use urgency (how time-sensitive) and importance (how impactful) to select the right format:

| | Low Importance | Medium Importance | High Importance |
|---|---|---|---|
| **Low Urgency** | Inline message, Notification bell | Tooltip, Bottom bar | Banner (dismissible) |
| **Medium Urgency** | Tooltip, Inline message | Banner, Slideout | Modal (small) |
| **High Urgency** | Banner (info) | Modal (medium) | Modal (large), Full-screen |

**Interruptiveness scale (least to most):**
1. Notification bell (user pulls information)
2. Inline message (passive, in-flow)
3. Empty state (only seen when area is empty)
4. Tooltip (small, contextual)
5. Bottom bar (persistent but peripheral)
6. Banner (visible but non-blocking)
7. Slideout (partial overlay)
8. Modal (full overlay, requires action)
9. Full-screen (total takeover)

---

## 4. Message Targeting

### 4.1 Targeting Dimensions

| Dimension | Examples | Use Case |
|---|---|---|
| User segment | Free, trial, paid, enterprise | Different messaging by plan |
| Usage behavior | Power user, casual, dormant | Engagement-based messaging |
| Lifecycle stage | New, activated, engaged, at-risk | Stage-appropriate nudges |
| Feature usage | Used feature X, never used feature Y | Feature adoption campaigns |
| Role/persona | Admin, member, viewer | Role-specific guidance |
| Geography/language | Region, locale | Localized messaging |
| Device/platform | Desktop, mobile, tablet | Platform-appropriate format |
| Time-based | Days since signup, days since last visit | Tenure-based messaging |

### 4.2 Targeting Rules Template

```
Message: [Message name]
Show when ALL conditions are true:
  - User segment: [e.g., Free plan users]
  - Lifecycle stage: [e.g., Activated but not yet power user]
  - Feature usage: [e.g., Has NOT used [feature] in last 30 days]
  - Tenure: [e.g., Signed up more than 7 days ago]
  - Behavior: [e.g., Currently viewing [page/feature]]
  - Previous messages: [e.g., Has NOT seen [other message] in last 7 days]
  - Impression cap: [e.g., Show maximum 3 times total]
```

---

## 5. Frequency Management

Frequency mismanagement is the number one cause of in-product messaging failure. Users who feel bombarded disengage or churn.

### 5.1 Impression Caps

| Cap Type | Rule | Example |
|---|---|---|
| Per-message cap | Max N times total per user | Show feature tooltip max 3 times |
| Per-message cooldown | Min X days between showings | Don't reshow for 7 days after dismiss |
| Global session cap | Max N messages per session | Max 2 messages per session across all campaigns |
| Global daily cap | Max N messages per day | Max 3 messages per day |
| Global weekly cap | Max N new messages per week | Max 5 new messages per week |

### 5.2 Priority Queuing

When multiple messages qualify to be shown, use a priority system:

```
Priority levels:
1. Critical (system alerts, payment failures, security) -- Always show
2. High (trial expiry, usage limits, blocking issues) -- Show if no critical
3. Medium (feature adoption, tips, announcements) -- Show if slot available
4. Low (engagement prompts, surveys, minor updates) -- Show if no other messages

Rules:
- Only one modal-level message per session
- Only one banner at a time (highest priority wins)
- Tooltips can coexist with banners but not with modals
- Inline messages do not count toward session caps
```

### 5.3 Suppression Rules

Suppress messages when:
- User just completed the action the message promotes (they already did it)
- User is in the middle of a complex workflow (don't interrupt data entry, multi-step processes)
- User dismissed this message or similar message recently
- User just experienced an error or frustrating moment (don't pile on)
- User is in a support conversation or help flow

---

## 6. Message Sequencing

### 6.1 Multi-Step Campaigns

For complex goals (onboarding, feature adoption), use sequenced messages:

```
Campaign: [Campaign Name]
Goal: [What user should accomplish by end of sequence]

Step 1: [Message type] -- [Content summary]
  Trigger: [When to show]
  Success: [User action that advances to step 2]
  Timeout: [Days before abandoning sequence]

Step 2: [Message type] -- [Content summary]
  Trigger: [After step 1 success OR after X days]
  Success: [User action that advances to step 3]
  Timeout: [Days before abandoning sequence]

Step 3: [Message type] -- [Content summary]
  Trigger: [After step 2 success]
  Success: [Goal completion]

Exit conditions:
  - User completes goal at any point → exit, show success message
  - User dismisses N times → exit, do not reshow
  - Timeout exceeded → exit, add to fallback segment
```

### 6.2 Progressive Messaging

Gradually increase message specificity and urgency:

1. **Awareness:** Tooltip or inline message introducing feature existence
2. **Education:** Slideout or banner explaining feature value with examples
3. **Activation:** Modal or inline CTA with guided first-use flow
4. **Reinforcement:** Success message after first use, follow-up tips

---

## 7. Personalization

### 7.1 Dynamic Content Variables

Use user data to personalize message content:

| Variable | Source | Example Usage |
|---|---|---|
| `{user.first_name}` | User profile | "Hey {first_name}, have you tried..." |
| `{user.plan}` | Billing | "Upgrade from {plan} to unlock..." |
| `{user.projects_count}` | Usage data | "You've created {projects_count} projects!" |
| `{user.team_size}` | Team data | "Your team of {team_size} could benefit from..." |
| `{user.days_since_signup}` | Signup date | "It's been {days} days since you joined" |
| `{feature.name}` | Context | "Try {feature.name} to speed up your workflow" |
| `{usage.top_feature}` | Analytics | "Since you love {top_feature}, you'll love..." |

### 7.2 Conditional Content Blocks

```
IF user.plan == "free" AND user.projects_count > 5:
  Show: "You're a power user on the free plan! Upgrade to Pro for unlimited projects."
ELSE IF user.plan == "free" AND user.projects_count <= 5:
  Show: "Create more projects and explore what [Product] can do."
ELSE IF user.plan == "pro" AND user.team_size == 1:
  Show: "Invite your team to collaborate in real-time."
```

---

## 8. Copy Guidelines

**Principles:** Headline-first (80% only read headlines), action-oriented, benefit-focused, never guilt-trip, reference current context.

### Copy Templates by Goal

**Feature Announcement:**
```
Headline: New: [Feature Name] is here
Body: [One sentence on what it does and why it matters to THIS user]
CTA: Try it now | Learn more
Dismiss: Got it | X
```

**Feature Adoption Nudge:**
```
Headline: [Benefit statement -- e.g., "Save time with keyboard shortcuts"]
Body: [1-2 sentences on how to use it, referencing user's current workflow]
CTA: Show me how | Try it
Dismiss: Not now | X
```

**Upgrade Prompt:**
```
Headline: [Value statement tied to current action]
Body: [What they'd unlock, framed as outcome]
CTA: See plans | Upgrade
Dismiss: Maybe later | X
```

**System Notification:**
```
Headline: [Clear, factual statement of what happened/is happening]
Body: [What the user needs to know or do, if anything]
CTA: [Action if needed] | Dismiss
```

### 8.3 Word Count Guidelines

| Message Type | Headline | Body | CTA |
|---|---|---|---|
| Tooltip | 3-8 words | 10-25 words | 2-4 words |
| Banner | 5-12 words | 0-15 words | 2-4 words |
| Modal | 4-10 words | 20-80 words | 2-5 words |
| Slideout | 4-10 words | 50-200 words | 2-5 words |
| Inline | 5-12 words | 15-40 words | 2-4 words |

---

## 9. Accessibility

In-product messages must be accessible to all users.

**Requirements checklist:**
- [ ] **Screen reader support:** Messages use ARIA roles (`role="alert"`, `role="dialog"`, `role="status"`)
- [ ] **Keyboard navigation:** All interactive elements reachable via Tab, modals trap focus
- [ ] **Close via keyboard:** Escape key closes modals, slideouts, and tooltips
- [ ] **Color contrast:** Text meets WCAG 2.1 AA (4.5:1 for body, 3:1 for large text)
- [ ] **Not color-only:** Don't rely solely on color to convey meaning (use icons + text)
- [ ] **Focus management:** Focus moves to message on open, returns to trigger on close
- [ ] **Motion sensitivity:** Respect `prefers-reduced-motion` for animations
- [ ] **Timing:** Auto-dismiss messages give enough time to read (minimum 5 seconds + 1 second per 20 words)
- [ ] **Readable font size:** Minimum 14px for body text in messages

---

## 10. Measurement

### 10.1 Primary Metrics

| Metric | Formula | What It Tells You |
|---|---|---|
| Impression Rate | Users who see message / Eligible users | Is targeting working? |
| Engagement Rate | Users who interact / Users who see | Is content compelling? |
| Dismiss Rate | Users who dismiss / Users who see | Is message unwanted? |
| Conversion Rate | Users who complete goal / Users who see | Is message effective? |
| Click-Through Rate | Users who click CTA / Users who see | Is CTA compelling? |

### 10.2 Health Metrics (Annoyance Detection)

| Metric | Warning Threshold | Action |
|---|---|---|
| Dismiss rate | > 80% | Rethink targeting, timing, or content |
| Rage clicks on X | Any occurrence | Message is frustrating users |
| Churn within 7 days of message | Higher than baseline | Message may be driving churn |
| Support tickets mentioning popups | Any increase | Reduce frequency or intrusiveness |
| Session length after message | Shorter than baseline | Message is disrupting flow |

### 10.3 Campaign Reporting Template

```
Campaign: [Name]
Period: [Date range]
Target segment: [Description]

Performance:
- Eligible users: [N]
- Impressions: [N] (impression rate: [X]%)
- Engagements: [N] (engagement rate: [X]%)
- Dismissals: [N] (dismiss rate: [X]%)
- Goal completions: [N] (conversion rate: [X]%)

Health check:
- Churn rate for exposed users vs control: [X]% vs [Y]%
- Session length impact: [+/- X]%
- Support ticket correlation: [None / Minor / Significant]

Recommendation: [Continue / Iterate / Pause / Kill]
```

---

## 11. Output Format

When designing an in-product messaging strategy, produce this specification:

```
# In-Product Messaging Strategy

## Campaign Overview
- Campaign name: [...]
- Goal: [What user behavior are you trying to drive?]
- Target segment: [Who sees these messages?]
- Duration: [Ongoing / Time-bounded]
- Success metric: [Primary KPI and target]

## Message Specifications

### Message 1: [Name]
- Type: [Tooltip / Banner / Modal / Slideout / Inline / Bottom bar]
- Trigger: [When/where this message appears]
- Targeting: [Segment + behavioral conditions]
- Frequency: [How often, impression cap, cooldown]
- Content:
  - Headline: [...]
  - Body: [...]
  - CTA: [Text + destination]
  - Dismiss: [Text + behavior]
- Personalization: [Dynamic elements]
- Accessibility: [ARIA role, keyboard behavior]
- Success metric: [How you measure this specific message]

### Message 2: [Name]
[Same structure as above]

## Sequencing
- Message dependency chain: [Which messages depend on others]
- Exit conditions: [When to stop the campaign for a user]
- Fallback: [What happens if user doesn't engage]

## Frequency Rules
- Session cap: [Max messages per session]
- Daily cap: [Max messages per day]
- Priority: [How these messages rank vs other active campaigns]
- Suppression: [When to suppress these messages]

## Measurement Plan
- Primary metric: [...]
- Secondary metrics: [...]
- Health metrics: [...]
- Reporting cadence: [Weekly / Bi-weekly]
- Kill criteria: [When to shut down the campaign]
```

---

Related skills: `paywall-upgrade-cro`, `feature-adoption`, `product-onboarding`, `engagement-loops`
