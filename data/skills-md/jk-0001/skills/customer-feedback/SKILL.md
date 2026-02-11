---
name: customer-feedback
description: Collect, analyze, and act on customer feedback to improve your product and business. Use when building feedback systems, running customer interviews, analyzing feature requests, measuring satisfaction (NPS, CSAT), or closing the feedback loop. Covers feedback collection methods, interview techniques, analysis frameworks, and how to decide what feedback to act on. Trigger on "customer feedback", "collect feedback", "user research", "customer interviews", "NPS", "feature requests", "feedback system".
---

# Customer Feedback

## Overview
Customer feedback is your compass. It tells you what's working, what's broken, and what to build next. But most solopreneurs either ignore feedback (and build the wrong things) or blindly implement every suggestion (and lose focus). This playbook shows you how to collect high-quality feedback, analyze it systematically, and act on what matters.

---

## Step 1: Build Your Feedback Collection System

Feedback doesn't come automatically. You need channels to capture it consistently.

**Feedback channels to set up:**

| Channel | When to Use | Setup |
|---|---|---|
| **In-app feedback widget** | Capture feedback at the moment of use | Tools: Canny, UserVoice, or custom form |
| **Email surveys** | Periodic check-ins (quarterly or post-milestone) | Tools: Typeform, Google Forms |
| **Customer interviews** | Deep qualitative insights | Manual scheduling (Calendly) |
| **Support tickets** | Capture pain points and bugs | Tools: Intercom, Help Scout, Zendesk |
| **NPS surveys** | Measure overall satisfaction | Tools: Delighted, SurveyMonkey |
| **Cancellation surveys** | Understand why people leave | Trigger on cancellation (see customer-retention) |
| **Feature request board** | Public place for customers to vote on ideas | Tools: Canny, ProductBoard |

**Minimum viable feedback system (for solopreneurs):**
1. In-app feedback button or email address for suggestions
2. NPS survey sent quarterly to all customers
3. Cancellation survey on every churn
4. Monthly customer interview with 2-3 active users

---

## Step 2: Run Customer Interviews That Uncover Truth

Interviews are the highest-value feedback method. But most people ask bad questions and get surface-level answers.

**Interview structure (30-45 min):**

### Part 1: Context (5-10 min)
Understand their situation and workflow.
```
"Tell me about your role and what a typical day looks like."
"What were you doing before you started using [Product]?"
"What made you look for a solution like ours?"
```

### Part 2: Usage (10-15 min)
Understand how they use your product.
```
"Walk me through the last time you used [Product]. What were you trying to do?"
"What do you love about [Product]?"
"What's frustrating or confusing?"
"If you could change one thing about it, what would it be?"
```

### Part 3: Outcomes (10-15 min)
Understand the value they're getting (or not getting).
```
"What problem does [Product] solve for you?"
"How do you measure success when using it?"
"What would happen if you stopped using [Product] tomorrow?"
```

### Part 4: Future (5 min)
Understand what they need next.
```
"What's the next big challenge you're facing that [Product] doesn't solve yet?"
"If we could build one thing for you, what would make this 10x more valuable?"
```

**Interview best practices:**
- Ask open-ended questions ("How do you...?" not "Do you like...?")
- Follow up with "Why?" or "Tell me more" to go deeper
- Listen 80%, talk 20%
- Don't sell or pitch during the interview — just learn
- Record with permission (tools: Zoom, Otter.ai) so you can focus on listening

**Who to interview:**
- **Power users** (use it most, see the most value) → understand best-case usage
- **Struggling users** (signed up but rarely use) → understand barriers
- **Churned customers** (canceled recently) → understand what failed

**Goal:** 2-3 interviews per month minimum. More if you're making big product decisions.

---

## Step 3: Measure Satisfaction with NPS

NPS (Net Promoter Score) is a simple way to measure overall satisfaction and loyalty.

**The question:**
```
"On a scale of 0-10, how likely are you to recommend [Product] to a friend or colleague?"
```

**Follow-up:**
```
"What's the main reason for your score?"
```

**Scoring:**
- **9-10 = Promoters** (love your product, will refer others)
- **7-8 = Passives** (satisfied but not enthusiastic)
- **0-6 = Detractors** (unhappy, at risk of churn)

**NPS Calculation:**
```
NPS = % Promoters - % Detractors
```

Example: 50% promoters, 10% detractors → NPS = +40

**Benchmarks:**
- NPS > +50 = Excellent
- NPS +30 to +50 = Good
- NPS 0 to +30 = Needs work
- NPS < 0 = Critical (more detractors than promoters)

**When to send:** Quarterly to all active customers. Or trigger after 30-90 days of usage.

**What to do with the data:**
- **Follow up with detractors** (< 7): "Thanks for the feedback. Can I ask what we could do better?"
- **Celebrate promoters** (9-10): "So glad to hear that! Would you be open to leaving a review?"
- **Look for patterns in the "why" responses** → These are your action items

---

## Step 4: Organize and Analyze Feedback

Raw feedback is noise. Organized feedback is signal.

**How to organize feedback (use a simple spreadsheet or tool like Canny, Notion):**

```
FEEDBACK | SOURCE | CATEGORY | CUSTOMER SEGMENT | PRIORITY | STATUS
"Need bulk export" | In-app | Feature Request | Power users | High | Roadmap
"Onboarding is confusing" | Interview | UX Issue | New users | High | In Progress
"Price is too high" | Cancellation Survey | Pricing | SMB | Medium | Tracking
```

**Categories:**
- Feature request (new functionality)
- Bug or technical issue
- UX or usability issue
- Pricing or billing
- Docs or support gap

**Analysis workflow (monthly, 30 min):**
1. Review all feedback from the past month
2. Group by theme (which issues or requests are mentioned most?)
3. Identify the top 3 patterns
4. Cross-reference with product roadmap (see product-roadmap skill)
5. Decide what to act on (see Step 5)

**Look for:**
- **High-frequency requests** (10+ people ask for the same thing → strong signal)
- **High-value customer requests** (your top 20% of revenue — these carry more weight)
- **Early churn triggers** (feedback from users who cancel in first 30 days → onboarding issues)

---

## Step 5: Decide What Feedback to Act On

Not all feedback is equal. Some is gold. Most is noise. Your job is to filter.

**Framework: Act on feedback if it meets 2+ of these criteria:**

1. **High frequency:** 10+ customers mention it
2. **High value:** Requested by top 20% of customers (by revenue)
3. **Strategic fit:** Aligns with your product vision and roadmap
4. **Prevents churn:** Addressing it would keep at-risk customers
5. **Quick win:** Low effort, high impact (can ship in < 1 week)

**Examples:**

| Feedback | Frequency | Value Segment | Strategic Fit | Act? |
|---|---|---|---|---|
| "Add bulk export" | 15 mentions | Power users | Yes | ✅ Yes (high freq + strategic fit) |
| "Support Android app" | 2 mentions | SMB | No | ❌ No (low freq + not strategic) |
| "Dashboard loads slowly" | 30 mentions | All segments | Yes | ✅ Yes (high freq + prevents churn) |
| "Can you integrate with [obscure tool]?" | 1 mention | One user | No | ❌ No (one-off request) |

**How to say no to feedback:**
```
"Thanks for the suggestion! We're focused on [current theme] right now, so this
won't make it into the next few months. We'll keep it on the radar and revisit
as priorities evolve."
```

---

## Step 6: Close the Feedback Loop

The fastest way to lose trust is to ask for feedback and then ignore it. Always close the loop.

**What closing the loop looks like:**

1. **Acknowledge receipt:** "Thanks for the feedback — we've logged it and will review it."
2. **Share progress:** If you act on it, tell them. "Hey, remember you asked for X? We just shipped it!"
3. **Explain why not:** If you don't act on it, explain why. "We considered X but decided to focus on Y because [reason]."

**Communication channels:**
- **In-app changelog** (announce new features and fixes)
- **Email updates** (monthly or quarterly newsletter with what shipped)
- **Direct outreach** (for high-value customers who requested something you built)

**Why this matters:** When customers see their feedback leads to real changes, they feel heard and invested. They become advocates, not just users.

---

## Step 7: Feedback Mistakes to Avoid

- **Not collecting feedback proactively.** Waiting for customers to reach out means you only hear from the loudest or most frustrated. Set up regular channels.
- **Asking leading questions.** "Would you like it if we added X?" is a bad question. People will say yes to be polite. Ask open-ended questions instead.
- **Acting on every piece of feedback.** You're not a feature factory. Filter ruthlessly.
- **Only collecting feedback from happy customers.** Churned customers and struggling users have the most valuable insights.
- **Not closing the loop.** If you ask for feedback and never act on it or explain your decisions, people stop giving feedback.
- **Treating all feedback equally.** Feedback from your best customers (high LTV, engaged, aligned with your ICP) matters 10x more than feedback from low-fit customers.
