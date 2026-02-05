---
name: create-changelog
description: Generate customer announcements for feature releases. Creates announcement variants for configured channels (Slack/Email). Researches codebase to understand implementation, infers value propositions, and generates engaging announcements with links to documentation. Supports single feature or batch mode for multiple features.
---

# Create Changelog

Generate customer announcements for product feature releases.

## Purpose

Create professional, engaging announcements that inform customers about new features. Announcements are tailored to different channels (Slack, Email) and include links to detailed documentation.

## Input

The user will provide:

1. **Feature name**: e.g., "Dashboards", "Workflow Automation"
2. **Documentation URL**: Pylon public article URL
3. **Channels**: Which announcement types to generate (from config.yaml)
4. **Optional context**: Key benefits, target audience, additional details

## Process

### Step 1: Research Feature

Use the Task tool to understand the feature deeply:

**What to find:**

1. **Feature Purpose:**
   - What problem does it solve?
   - Who is it for?
   - Why is it valuable?

2. **Key Capabilities:**
   - Top 3-5 capabilities
   - What makes it unique?
   - How does it help users?

3. **User Benefits:**
   - Time saved
   - Improved workflow
   - Better outcomes
   - Reduced friction

4. **Target Audience:**
   - Specific user roles or teams
   - Use cases
   - Pain points it addresses

**Example exploration:**
```
Task: Explore

Research the [Feature Name] feature to create customer announcements.

Please find:
1. Main functionality and purpose
2. Top 3-5 capabilities
3. User benefits and value proposition
4. Target audience and use cases
5. Any unique or standout aspects

Focus on customer-facing value, not technical implementation.
```

### Step 2: Determine Announcement Channels

Check config.yaml for enabled channels:

```yaml
announcements:
  channels:
    - slack
    - email
```

**Generate announcements for each enabled channel.**

### Step 3: Create Announcement Directory

Create a directory for this feature's announcements:

```
output/changelogs/YYYY-MM-DD/[feature-slug]/
```

**Example:**
```
output/changelogs/2025-12-22/dashboards/
```

### Step 4: Generate Slack Announcement

**Purpose:** Short, engaging announcement for Slack channels

**Format:**

```markdown
# 🎉 New: [Feature Name]

[One compelling sentence about what it does and why it matters]

**Key capabilities:**
- ✨ [Capability 1] - [brief benefit]
- 🚀 [Capability 2] - [brief benefit]
- 💡 [Capability 3] - [brief benefit]
- 🎯 [Capability 4] - [brief benefit]

[One sentence about who should use it and why]

**Get started:** [Product URL if applicable]
**Learn more:** [Documentation URL]

---
*Have feedback? Reply to this thread or reach out to our team!*
```

**Guidelines:**
- Keep it concise (15-25 lines)
- Use emojis strategically (but not excessively)
- Focus on benefits, not features
- Include clear call-to-action
- Link to both product and documentation

**Example:**

```markdown
# 🎉 New: Dashboards

Get instant visibility into your team's workflows with customizable dashboards that surface the metrics that matter most.

**Key capabilities:**
- ✨ Real-time metrics - Track performance as it happens
- 🚀 Drag-and-drop customization - Build your perfect view in seconds
- 💡 Smart insights - Get actionable recommendations
- 🎯 Team collaboration - Share dashboards with your team

Perfect for managers and team leads who need to monitor progress, spot trends, and make data-driven decisions quickly.

**Get started:** https://app.yourproduct.com/dashboards
**Learn more:** https://yourproduct-kb.help.usepylon.com/articles/dashboards

---
*Have feedback? Reply to this thread or reach out to our team!*
```

**Save to:** `output/changelogs/YYYY-MM-DD/[feature-slug]/slack-announcement.md`

### Step 5: Generate Email Announcement

**Purpose:** More detailed announcement for email newsletters

**Format:**

```markdown
# New: [Feature Name]

Hello,

We're excited to announce [Feature Name], [one sentence value proposition].

## What is [Feature Name]?

[2-3 sentences explaining what it is and what problem it solves. Focus on customer pain points and how this addresses them.]

## Key Capabilities

**[Capability 1 Name]**
[1-2 sentences explaining what it does and why it's valuable]

**[Capability 2 Name]**
[1-2 sentences explaining what it does and why it's valuable]

**[Capability 3 Name]**
[1-2 sentences explaining what it does and why it's valuable]

[Add 2-3 more capabilities as appropriate]

## Who Should Use This?

[Feature Name] is perfect for [target audience description]. Whether you're [use case 1], [use case 2], or [use case 3], [Feature Name] helps you [key benefit].

## Getting Started

Ready to try it? [Call to action - e.g., "Access Dashboards from your main menu" or "Enable the integration in Settings"]

For detailed instructions and best practices, check out our [documentation](https://yourproduct-kb.help.usepylon.com/articles/[slug]).

## What's Next?

We're continuously improving [Feature Name] based on your feedback. Have suggestions or questions? Reply to this email or reach out to our support team.

---

Best regards,
The [Product Name] Team

**Documentation:** [Documentation URL]
```

**Guidelines:**
- Professional but friendly tone
- More detail than Slack (40-60 lines)
- Structured with clear sections
- Multiple calls-to-action
- Personal touch (team signature)

**Example:**

```markdown
# New: Dashboards

Hello,

We're excited to announce Dashboards, a powerful new way to visualize and track your team's workflows in real-time.

## What are Dashboards?

Dashboards give you instant visibility into the metrics that matter most to your team. Instead of digging through data or running manual reports, you can now see key performance indicators at a glance and spot trends before they become issues.

## Key Capabilities

**Real-Time Metrics**
Track your team's performance as it happens. Dashboards update automatically, so you always have the latest information without refreshing or waiting for scheduled reports.

**Drag-and-Drop Customization**
Build the perfect dashboard for your needs in seconds. Add, remove, and rearrange widgets to focus on what matters most to you and your team.

**Smart Insights**
Get actionable recommendations based on your data. Our analytics engine surfaces trends, anomalies, and opportunities you might otherwise miss.

**Team Collaboration**
Share dashboards with your team or create role-specific views. Everyone sees the information they need, presented the way they need it.

**Export and Reporting**
Generate reports directly from your dashboards for stakeholder updates, retrospectives, or compliance needs.

## Who Should Use This?

Dashboards are perfect for managers and team leads who need to monitor progress, identify bottlenecks, and make data-driven decisions quickly. Whether you're tracking project milestones, monitoring workflow efficiency, or managing team workload, Dashboards help you stay on top of what's happening.

## Getting Started

Ready to try it? Access Dashboards from your main menu under "Analytics". Your first dashboard is automatically created with recommended widgets, but you can customize it however you like.

For detailed instructions, widget explanations, and best practices, check out our [documentation](https://yourproduct-kb.help.usepylon.com/articles/dashboards).

## What's Next?

We're continuously improving Dashboards based on your feedback. Have suggestions for new widgets, better visualizations, or additional features? Reply to this email or reach out to our support team.

---

Best regards,
The [Product Name] Team

**Documentation:** https://yourproduct-kb.help.usepylon.com/articles/dashboards
```

**Save to:** `output/changelogs/YYYY-MM-DD/[feature-slug]/email-announcement.md`

### Step 6: Create README with Metadata

Create a README file with feature metadata and release checklist:

```markdown
# [Feature Name] Release

## Overview

**Feature:** [Feature Name]
**Category:** [Category]
**Release Date:** [Date or TBD]
**Target Audience:** [Who this is for]

## Description

[2-3 sentences describing what this feature is and what problem it solves]

## Key Capabilities

- [Capability 1]
- [Capability 2]
- [Capability 3]
- [Capability 4]

## URLs

**Product:** https://app.yourproduct.com/[feature-path]
**Documentation:** [Pylon public URL]
**Internal docs:** [Pylon internal URL if available]

## Announcement Files

- ✅ `slack-announcement.md` - Slack channel announcement
- ✅ `email-announcement.md` - Email newsletter announcement

## Release Checklist

### Pre-Release
- [ ] Documentation reviewed and approved
- [ ] Screenshots captured and embedded
- [ ] Announcement copy reviewed
- [ ] Feature fully tested in production
- [ ] Support team briefed

### Distribution
- [ ] Post to Slack #announcements channel
- [ ] Send email newsletter
- [ ] Update in-app changelog (if applicable)
- [ ] Share with customer success team

### Post-Release
- [ ] Monitor feedback channels
- [ ] Track feature adoption
- [ ] Document common questions for FAQ
- [ ] Plan follow-up improvements

## Technical Details

**Documentation file:** `output/features/YYYY-MM-DD_[feature-slug]/[feature-slug].md`
**Screenshots:** `output/screenshots/[feature]-*.png`
**Database changes:** [Migrations or N/A]
**Feature flags:** [Flags used or N/A]

## Notes

[Any additional context, caveats, or important information for the release team]
```

**Save to:** `output/changelogs/YYYY-MM-DD/[feature-slug]/README.md`

### Step 7: Verify Announcements

Check all generated files:

✅ **Slack Announcement:**
- Concise (15-25 lines)
- Engaging and energetic
- Clear benefits
- Links to product and documentation

✅ **Email Announcement:**
- Professional tone
- Comprehensive (40-60 lines)
- Well-structured
- Multiple CTAs
- Team signature

✅ **README:**
- Complete metadata
- Release checklist
- All URLs present
- Technical details documented

### Step 8: Document Results

Provide a summary:

```markdown
## Announcements Created: [Feature Name]

**Location:** `output/changelogs/YYYY-MM-DD/[feature-slug]/`

### Files Generated:

1. **slack-announcement.md**
   - Length: [X] lines
   - Tone: Engaging and energetic
   - Target: Slack channels

2. **email-announcement.md**
   - Length: [X] lines
   - Tone: Professional and comprehensive
   - Target: Email newsletter

3. **README.md**
   - Metadata and release checklist
   - All URLs and references

### Key Messaging:

**Value Proposition:** [One sentence]

**Target Audience:** [Who it's for]

**Top 3 Benefits:**
1. [Benefit 1]
2. [Benefit 2]
3. [Benefit 3]

### Links Included:

- Product URL: [URL]
- Documentation: [Pylon URL]

### Next Steps:

1. Review announcements for accuracy and tone
2. Schedule announcement distribution
3. Brief customer success team
4. Monitor feedback after release
```

## Batch Mode (Multiple Features)

For releases with multiple features, create a consolidated changelog:

**File:** `output/changelogs/YYYY-MM-DD/combined-release.md`

**Format:**

```markdown
# [Month] [Year] Product Update

## 🎉 What's New

### [Feature 1 Name]
[2-3 sentences describing the feature]
**Learn more:** [Documentation URL]

### [Feature 2 Name]
[2-3 sentences describing the feature]
**Learn more:** [Documentation URL]

## 🛠️ Improvements

- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

## 🐛 Bug Fixes

- [Fix 1]
- [Fix 2]

---

For detailed information about any of these updates, visit our [documentation](https://docs.yourproduct.com) or contact our support team.
```

## Writing Guidelines

### Tone and Style

**DO:**
- ✅ Use "you" and "your" (user-focused)
- ✅ Focus on benefits over features
- ✅ Be specific and concrete
- ✅ Use active voice
- ✅ Show excitement appropriately

**DON'T:**
- ❌ Use technical jargon
- ❌ Focus on implementation details
- ❌ Make exaggerated claims
- ❌ Assume prior knowledge
- ❌ Be overly formal or corporate

### Structure

- **Lead with value:** First sentence should explain why this matters
- **Keep it scannable:** Use headings, bullets, short paragraphs
- **End with action:** Clear next steps for the reader
- **Link strategically:** Product URL and documentation URL

### Emojis (Slack Only)

Use emojis to add visual interest, but don't overdo it:

- ✅ 3-5 emojis total
- ✅ Title + bullet points
- ❌ Not in every line
- ❌ Not multiple per line

## Integration with Release Workflow

This skill is the final step in the release workflow:

1. Capture screenshots (capture-screenshots skill)
2. Upload to Pylon CDN (sync-docs skill)
3. Create documentation (update-product-doc skill)
4. Sync to Pylon (sync-docs skill)
5. ✅ **Create announcements** ← You are here

The public article URL from sync-docs should be provided to this skill for inclusion in announcements.
