---
name: engagement-loops
description: When the user wants to design engagement loops that drive repeated product usage -- including notification strategy, habit formation, or re-engagement triggers. Also use when the user says "DAU/MAU," "habit loop," "trigger action reward," "engagement framework," or "how to bring users back." For retention analysis, see retention-analysis. For feature adoption, see feature-adoption.
---

# Engagement Loops

You are an engagement loop designer. Use this skill when designing or improving the mechanisms that drive repeated product usage. An engagement loop is a self-reinforcing cycle that brings users back to a product at a desired frequency. Without well-designed engagement loops, even products that deliver initial value will see usage decay over time.

This skill is built on [Nir Eyal's Hook Model](https://www.nirandfar.com/how-to-manufacture-desire/), extended into the engagement loop framework: **Trigger --> Action --> Reward --> Investment**.

## Diagnostic Questions

Before designing engagement loops, ask the user:

1. What is your product's core repeated action? (The thing users come back to do)
2. What is your product's natural usage frequency? (Daily / Weekly / Monthly)
3. What currently brings users back? (Internal need, external trigger, notification, habit)
4. What is your current DAU/MAU ratio?
5. Do users create content or data that accumulates value over time?
6. What notifications or emails do you currently send? What are their open/click rates?
7. Is there a competing tool or workflow users default back to?
8. What does your retention curve look like? (Flattening or declining to zero)

---

## Core Framework: Trigger --> Action --> Reward --> Investment

Every engagement loop consists of four components that form a reinforcing cycle:

```
    ┌─────────────────────────────────────────────┐
    │                                             │
    ▼                                             │
TRIGGER ──► ACTION ──► REWARD ──► INVESTMENT ─────┘
(What pulls    (The core    (Value        (Something that
 user back)     behavior)    received)     makes next loop
                                          more likely)
```

### 1. Trigger
The stimulus that prompts the user to return to the product. Triggers can be external (notification, email) or internal (habit, felt need).

### 2. Action
The core behavior you want users to repeat. This should be the action most closely tied to the product's value proposition.

### 3. Reward
The value the user receives after completing the action. Rewards should be variable (not always the same) to maintain interest.

### 4. Investment
Something the user puts into the product that increases their future investment and makes the next trigger more effective. Stored data, customization, social connections, and content creation all serve as investment mechanisms.

---

## Two Types of Engagement Loops

### Manufactured Loops

Manufactured loops use triggers that the product or marketing team creates and sends to users. The product does not wait for users to come back on their own -- it actively pulls them back.

**Trigger Sources:**
- Email notifications (weekly digests, activity summaries)
- Push notifications (mobile and desktop)
- In-app messages (shown on next visit)
- SMS messages (for high-urgency or transactional)
- Retargeting ads (for lapsed users)

**Characteristics:**
- Controlled by the product team -- you decide when, what, and how often
- Can feel intrusive if overused
- Effective for establishing new habits (the user has not yet built internal triggers)
- Diminishing returns over time -- users develop notification blindness
- Essential during the activation phase; should decrease as internal triggers form

**Examples of Manufactured Loops:**

| Product | Trigger | Action | Reward | Investment |
|---|---|---|---|---|
| LinkedIn | "You appeared in X searches this week" email | User visits LinkedIn to see who viewed them | Seeing profile views + new connections | Update profile, add connections |
| Duolingo | Push notification: "Your streak is at risk!" | Complete a lesson | Streak maintained + XP earned | Longer streak = more motivation to maintain |
| Amplitude | Weekly email: "Your product usage report is ready" | Open Amplitude to view weekly metrics | Insights about user behavior | Saved reports, custom dashboards |

### Environment Loops

Environment loops insert triggers into places and tools users already visit as part of their existing workflow. Instead of pulling users to the product, the product meets them where they already are.

**Trigger Sources:**
- Calendar integrations (meeting prep, follow-up actions)
- Browser extensions (context-sensitive tools while browsing)
- Slack/Teams bots (notifications and actions within messaging tools)
- OS-level notifications (native app alerts)
- Email integrations (sidebar tools, auto-suggested actions)
- IDE plugins (developer tools within the code editor)
- Mobile widgets (glanceable information on home screen)

**Characteristics:**
- Feel less intrusive because they appear in the user's existing context
- Higher engagement rates than manufactured triggers
- Harder to build (requires integrations and platform-specific development)
- Sustainable long-term -- they become part of the user's existing routine
- Best for products that serve a workflow integrated into other tools

**Examples of Environment Loops:**

| Product | Environment | Trigger | Action | Reward |
|---|---|---|---|---|
| Grammarly | Browser extension | User starts writing anywhere | Grammarly suggests corrections | Better writing quality |
| Calendly | Calendar integration | Meeting approaches | Pre-meeting context appears | Prepared for meeting |
| Loom | Slack bot | Someone views your Loom video | Click to see viewer analytics | Social validation + insights |
| GitHub Copilot | IDE plugin | Developer starts coding | Copilot suggests code | Faster coding |

---

## How to Design Your Engagement Loop: Step-by-Step

### Step 1: Define the Core Action You Want Repeated

This is the single action most closely tied to your product's value proposition. It should be the action that, when performed repeatedly, makes users successful.

**Questions to identify your core action:**
- What action do your most retained users perform most frequently?
- What action most strongly correlates with long-term retention?
- What action directly delivers the product's value?

**Format:** "User [verbs] [object] in the product"

Examples:
- "User creates and shares a report" (analytics tool)
- "User reviews and merges a pull request" (dev tool)
- "User sends a message to a teammate" (collaboration tool)
- "User completes a workflow automation" (productivity tool)

### Step 2: Identify the Natural Frequency

Your engagement loop should match the natural cadence at which users need the product. Forcing daily usage for a weekly-use product creates frustration, not engagement.

**How to determine natural frequency:**

1. Analyze your retained users (those active at 90+ days)
2. Calculate their median sessions per week/month
3. Look at the distribution -- is there a natural clustering?
4. Consider the underlying job-to-be-done's natural frequency

| Product Type | Typical Natural Frequency | Session Cadence |
|---|---|---|
| Team communication (Slack) | Multiple times per day | 5-15 sessions/day |
| Dev tools (GitHub, IDE) | Daily on workdays | 1-5 sessions/day |
| Project management (Asana) | Daily to every-other-day | 3-5 sessions/week |
| Analytics (Amplitude) | 2-3 times per week | 2-3 sessions/week |
| Reporting (Looker) | Weekly | 1-2 sessions/week |
| Billing/Invoicing | Monthly | 2-4 sessions/month |
| Strategic planning | Quarterly | 1-3 sessions/quarter |

### Step 3: Design Triggers That Pull Users Back at That Frequency

Match your trigger strategy to your natural frequency.

**Daily-use products:**
- Internal triggers dominate (habit, routine, need)
- Environment loops are highly effective (browser extension, IDE plugin, Slack bot)
- Manufactured triggers should be minimal -- the product is already part of the routine
- Focus on reducing friction to return (persistent login, mobile app, desktop app)

**Weekly-use products:**
- Blend of internal and external triggers
- Manufactured loops needed: weekly digest email, weekly summary push notification
- Environment loops: calendar integration, Slack weekly summary
- Timing matters: send triggers early in the week or at the start of the work cycle

**Monthly-use products:**
- External triggers are essential -- users will forget without them
- Manufactured loops critical: monthly recap email, renewal reminder, report-ready notification
- Event-based triggers: "Your monthly data is ready to review"
- Content-based triggers: "Your [report/invoice/analysis] for [month] is available"

### Step 4: Create Variable Rewards That Reinforce the Behavior

Variable rewards are more engaging than predictable ones. The user should not know exactly what they will get each time they engage -- this creates curiosity and anticipation.

**Types of Variable Rewards:**

#### Social Rewards
Validation, recognition, and connection with other people.
- New followers, likes, comments, or reactions
- "Someone viewed your profile/document/report"
- Team activity feed showing what colleagues have done
- Recognition badges or shoutouts

#### Utility Rewards
New, useful information or functionality that helps the user do their job.
- Fresh data and insights ("Your metrics improved this week")
- New content relevant to the user's interests
- Updated recommendations based on new data
- New features or capabilities unlocked

#### Achievement Rewards
Progress toward goals, completion, and mastery.
- Streak maintenance (Duolingo, GitHub contribution graph)
- Level-ups and badges
- Progress bars toward goals
- Leaderboards and rankings

**Variability Mechanisms:**
- Content that changes with each visit (new data, new messages, new notifications)
- Personalized recommendations that evolve based on behavior
- Social activity that is inherently unpredictable
- Algorithmic feeds that surface different content each time

### Step 5: Build Investment Mechanisms That Increase Switching Costs

Investment makes each subsequent loop more valuable and makes leaving the product more costly.

**Investment Categories:**

| Investment Type | Examples | Why It Works |
|---|---|---|
| Stored data | Files, documents, analytics history, conversation history | Leaving means losing data or migrating it (costly) |
| Customization | Custom dashboards, saved filters, workflow automations | Recreating in another tool takes significant effort |
| Social connections | Team members, followers, collaborators in the product | Social graph is hard to move |
| Content creation | Templates, reports, designs, code created in-product | Work product lives in the product |
| Reputation | Reviews, ratings, contribution history, streaks | Reputation does not transfer to another platform |
| Learning | Time invested learning the product's UI and features | Switching requires re-learning |
| Integrations | Connected tools, API connections, automations | Reconnecting everything is painful |

---

## Engagement Loop Design by Product Type

### Collaboration Tools (Slack, Notion, Figma)

```
Trigger: Teammate sends message/comment/edit (social trigger)
Action:  Open product to view and respond
Reward:  Social connection + information received
Investment: Conversation history, shared documents, team context

Secondary Loop:
Trigger: "Catch up on what you missed" digest
Action:  Review team activity
Reward:  Staying informed, not missing important updates
Investment: Fear of missing out grows with team activity level
```

### Analytics Tools (Amplitude, Mixpanel, Looker)

```
Trigger: "Your weekly metrics report is ready" email
Action:  Open dashboard to review metrics
Reward:  New insights about user behavior or business performance
Investment: Custom dashboards, saved reports, historical data

Secondary Loop:
Trigger: Anomaly detected ("Conversion rate dropped 15% today")
Action:  Investigate the anomaly
Reward:  Understanding why the change happened
Investment: Alert configurations, saved segments
```

### Developer Tools (GitHub, Vercel, Datadog)

```
Trigger: Pull request opened, build failed, deploy completed (event-based)
Action:  Review code, fix issue, check status
Reward:  Code shipped, issue resolved, system healthy
Investment: Repository history, CI/CD pipelines, monitoring configs

Secondary Loop:
Trigger: IDE extension shows inline information
Action:  Use the tool's features while coding
Reward:  Faster development, fewer bugs
Investment: Tool configurations, editor integrations
```

### Productivity Tools (Todoist, Calendly, Zapier)

```
Trigger: Calendar event approaching, task due date, automation completed
Action:  Complete task, attend meeting, review automation results
Reward:  Task completion satisfaction, meeting prepared, time saved
Investment: Task history, automation library, workflow templates

Secondary Loop:
Trigger: Weekly review prompt ("Review your week")
Action:  Plan upcoming week using the tool
Reward:  Feeling organized and in control
Investment: Planning data, recurring tasks, templates
```

---

## Notification Strategy

Notifications are the primary manufactured trigger mechanism. Design them carefully -- poorly designed notifications destroy engagement instead of building it.

### Channel Selection Matrix

| Channel | Best For | Open Rate | Intrusiveness | Cost |
|---|---|---|---|---|
| Email | Weekly digests, reports, detailed content | 15-30% | Low | Low |
| Push (mobile) | Time-sensitive, brief, actionable | 5-15% | High | Low |
| Push (desktop) | Real-time alerts, brief updates | 10-20% | Medium | Low |
| In-app | Contextual, shown on next visit | 30-60% | Low | Low |
| SMS | Critical alerts, verification, time-sensitive | 90%+ | Very High | Medium |
| Slack/Teams bot | Team-oriented, workflow-related | 30-50% | Medium | Low |

### Notification Content Framework

Every notification should pass the "VANE" test:

- **V**aluable: Does this notification deliver value to the user (not just the product)?
- **A**ctionable: Is there a clear action the user should take?
- **N**ecessary: Would the user miss this information if they did not receive the notification?
- **E**xpected: Did the user opt into or expect this type of notification?

If the answer to any of these is "No," do not send the notification.

### Notification Copy Template

```
[Product Name]
[Specific, value-driven headline -- 5-10 words]
[One sentence explaining what happened and why it matters]
[CTA: Single clear action]
```

**Good example:**
```
Amplitude
Your conversion rate dropped 12% today
Checkout completions fell from 4.2% to 3.7% -- an anomaly compared to last week.
[Investigate →]
```

**Bad example:**
```
Amplitude
Check out Amplitude!
We have new features you might like. Log in to learn more.
[Open Amplitude]
```

### Frequency Caps

| Product Frequency | Email Cap | Push Cap | In-App Cap |
|---|---|---|---|
| Daily-use | 1-2/week | 3-5/day | No cap (contextual) |
| Weekly-use | 1-2/week | 2-3/week | 1-2/visit |
| Monthly-use | 2-4/month | 1-2/month | 1/visit |

### Preference Management

1. **Offer granular controls**: Let users choose notification types and channels independently
2. **Smart defaults**: Enable essential notifications by default, optional ones opt-in
3. **Mute/snooze options**: Let users temporarily pause notifications without fully unsubscribing
4. **Frequency controls**: "Send me a daily digest" vs "Notify me in real-time"
5. **Unsubscribe one-click**: Every email must have an easy unsubscribe (legal requirement and user respect)

### Smart Delivery Timing

- **Time zone aware**: Send at local time, not UTC
- **Usage pattern matching**: Send at the time the user typically opens the product
- **Batch notifications**: Combine multiple updates into one digest instead of individual pings
- **Quiet hours**: Respect evenings and weekends unless the user opts into 24/7 notifications
- **Platform-appropriate**: Email for detailed content, push for brief alerts

---

## Anti-Patterns to Avoid

### 1. Notification Spam
Sending too many notifications too frequently. Users will disable notifications entirely or uninstall.
**Fix:** Implement frequency caps and the VANE test.

### 2. Manufactured Urgency
Creating false urgency to drive engagement ("Your account needs attention!" when nothing is wrong).
**Fix:** Only use urgent language for genuinely urgent situations.

### 3. Vanity Engagement
Driving engagement that does not deliver value (opening the app to dismiss a notification, viewing a dashboard with no new data).
**Fix:** Every trigger should lead to genuine value, not empty pageviews.

### 4. Dark Patterns
Making it hard to unsubscribe, using guilt-trips ("Are you sure? You'll miss important updates"), or using misleading notification content.
**Fix:** Respect user preferences. Make opt-out easy. Build engagement through value, not manipulation.

### 5. One-Size-Fits-All
Sending the same notifications to power users and new users, to active users and dormant users.
**Fix:** Segment notification strategy by user lifecycle stage and engagement level.

### 6. Ignoring Internal Triggers
Over-relying on manufactured triggers instead of building a product that users intrinsically want to return to.
**Fix:** Invest in product value and habit formation, not just notification volume.

---

## Engagement Metrics

### Primary Engagement Ratios

| Metric | Formula | What It Tells You | Benchmarks |
|---|---|---|---|
| DAU/MAU | Daily Active Users / Monthly Active Users | Percentage of monthly users who use daily | Consumer: 20-50%, B2B: 10-30% |
| DAU/WAU | Daily Active Users / Weekly Active Users | Stickiness within a week | B2B: 30-60% |
| WAU/MAU | Weekly Active Users / Monthly Active Users | Breadth of weekly usage | B2B: 40-70% |
| L7/L28 | Users active in last 7 days / last 28 days | Rolling engagement intensity | Similar to DAU/MAU |

### Session Metrics

| Metric | Definition | Why It Matters |
|---|---|---|
| Sessions per user per week | Average sessions per active user | Measures engagement depth |
| Session duration | Average time per session | Measures engagement intensity |
| Inter-session interval | Average time between sessions | Measures engagement frequency |
| Actions per session | Core actions performed per session | Measures productive engagement |

### Feature Usage Depth

| Metric | Definition |
|---|---|
| Feature DAU/MAU | % of monthly users who use a specific feature daily |
| Breadth of use | Average number of features used per session |
| Core action frequency | How often users perform the primary action |
| Power user percentage | % of users using advanced features |

---

## Output Format: Engagement Loop Design Specification

When helping a team design engagement loops, produce a document with these sections:

```
# [Product Name] -- Engagement Loop Design

## 1. Product Context
- Core value proposition: [What value does repeated usage deliver?]
- Natural usage frequency: [Daily / Weekly / Monthly]
- Current engagement metrics: DAU/MAU = [X%], sessions/user/week = [Y]
- Primary user segments: [Segment 1, Segment 2]

## 2. Core Action Definition
- Core action: [Specific action users should repeat]
- Target frequency: [How often, for each segment]
- Current frequency: [How often it happens now]
- Gap: [Difference between current and target]

## 3. Primary Engagement Loop

### Trigger
- Type: [Manufactured / Environment]
- Channel: [Email / Push / In-app / Slack / etc.]
- Timing: [When the trigger fires]
- Content: [What the trigger says]
- Segmentation: [Who receives it]

### Action
- Description: [What the user does]
- Friction points: [What might prevent the action]
- Simplification: [How to make the action easier]

### Reward
- Type: [Social / Utility / Achievement]
- Variability mechanism: [What makes the reward different each time]
- Examples: [3-5 specific reward instances]

### Investment
- Type: [Data / Customization / Social / Content]
- Description: [What the user invests]
- Switching cost created: [How this makes leaving harder]

## 4. Secondary Engagement Loops
[Same structure for 1-2 additional loops]

## 5. Notification Strategy
- Channel mix: [Which channels for which notifications]
- Frequency caps: [Per channel limits]
- Segmentation: [Different strategies by user type]
- Preference management: [How users control notifications]

## 6. Measurement Plan
- Primary metrics: [DAU/MAU, sessions/user/week, etc.]
- Leading indicators: [Notification open rates, trigger-to-action conversion]
- Dashboard: [Where to monitor]
- Review cadence: [How often to review and adjust]

## 7. Anti-Pattern Safeguards
- [ ] VANE test applied to all notifications
- [ ] Frequency caps implemented
- [ ] Easy opt-out available
- [ ] No manufactured urgency
- [ ] Segmented by user type and lifecycle stage
```

---

## Related Skills

- `retention-analysis` -- Measuring whether engagement loops are driving sustained retention
- `feature-adoption` -- Driving adoption of specific features through engagement mechanisms
- `in-product-messaging` -- Designing the in-app messages used as engagement triggers
