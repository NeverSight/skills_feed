---
name: product-analytics
description: When the user wants to set up product analytics -- including event taxonomy, tracking plans, funnel analysis, or tool selection (Mixpanel, Amplitude, PostHog). Also use when the user says "event tracking," "analytics setup," "tracking plan," "analytics implementation," or "user identification." For PLG metrics, see plg-metrics. For experimentation, see growth-experimentation.
---

# Product Analytics

You are a product analytics specialist. Set up and operationalize a product analytics system designed for PLG insights. This skill covers event taxonomy design, analytics tool selection, implementation best practices, and analysis frameworks that turn raw product data into growth decisions.

---

## Diagnostic Questions

Before designing your analytics system, answer:

1. **What questions do you need to answer?** (List the top 10 questions your team asks about user behavior)
2. **What analytics tools do you currently use?** (And what are you dissatisfied with?)
3. **What is your technical stack?** (Web, mobile, backend language, data warehouse)
4. **How many active users do you have?** (Affects tool pricing and data volume planning)
5. **Who will consume analytics?** (Engineers only, product managers, executives, marketing?)
6. **What is your privacy posture?** (GDPR, CCPA, SOC 2, data residency requirements)
7. **Do you have a data warehouse?** (Snowflake, BigQuery, Redshift, Databricks)
8. **What is your budget for analytics tooling?**

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find analytics SDKs**: Search for imports of `mixpanel`, `amplitude`, `posthog`, `segment`, `@segment/analytics-next`, `ga4`, `gtag`, `rudderstack`, `heap`
2. **Find tracking calls**: Search for `track(`, `capture(`, `logEvent(`, `gtag('event'`, `analytics.track(`, `posthog.capture(`
3. **List all tracked events**: Extract event names from tracking calls -- build an inventory of what's currently tracked
4. **Check user identification**: Search for `identify(`, `setUserId(`, `setUserProperties(`, `people.set(`
5. **Find tracking initialization**: Search for analytics init/setup code -- check if properly configured with API keys
6. **Check for a tracking plan**: Look for files like `events.ts`, `analytics.ts`, `tracking.ts`, `events.json` that define event schemas
7. **Find page/screen tracking**: Search for `page(`, `screen(`, `pageview`, route change tracking
8. **Check for server-side tracking**: Search backend code for analytics calls -- not just client-side

Report: list all tracked events, the SDK(s) in use, and gaps (e.g., "No server-side tracking", "No user identification", "Only 5 events tracked -- likely incomplete").

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## Analytics Stack for PLG

### The Four Layers

```
Layer 4: Analysis & Visualization
  Mixpanel, Amplitude, PostHog, Looker, Mode, Metabase

Layer 3: Data Warehouse (optional but recommended)
  Snowflake, BigQuery, Redshift, Databricks

Layer 2: Data Pipeline & Enrichment
  Segment, RudderStack, mParticle, Fivetran, Census (reverse ETL)

Layer 1: Event Collection
  SDK instrumentation, server-side tracking, CDP
```

### Recommended Stacks by Stage

**Early Stage (0-10K users)**: PostHog (open source, all-in-one) or Mixpanel/Amplitude free tier. Direct SDK integration. No data warehouse initially.

**Growth Stage (10K-100K users)**: Segment or RudderStack + Mixpanel or Amplitude + Snowflake or BigQuery + Reverse ETL.

**Scale Stage (100K+ users)**: Full CDP + Amplitude or custom analytics on warehouse + Looker or Mode + dbt + Feature flag system (LaunchDarkly, Statsig).

---

## Event Taxonomy Design

### Naming Convention

Use **object_action** format. `{object}_{action}` in snake_case.

**Rules**:
1. Object first, action second: `signup_completed` not `completed_signup`
2. Past tense for completed actions: `_completed`, `_created`, `_sent`
3. Present tense for state changes: `_viewed`, `_started`
4. Be specific: `project_created` not `item_created`
5. Avoid abbreviations: `subscription_upgraded` not `sub_upgr`

### Event Categories

#### Account Events
```
account_created, account_verified, account_deleted
sso_configured, team_created, team_member_added, team_member_removed
```

#### Onboarding Events
```
onboarding_started
onboarding_step_completed     (property: step_name, step_number)
onboarding_completed, onboarding_skipped
setup_wizard_started, setup_wizard_completed
sample_data_loaded, first_integration_connected
```

#### Core Feature Events
```
[product_specific_object]_created / _edited / _deleted / _shared / _exported
feature_used                  (property: feature_name, feature_category)
search_performed, filter_applied
```

#### Engagement Events
```
session_started
session_ended                 (property: duration_seconds)
page_viewed                   (property: page_name, page_category)
notification_received, notification_clicked
help_article_viewed, feedback_submitted
```

#### Monetization Events
```
upgrade_prompt_viewed         (property: prompt_location, prompt_trigger)
upgrade_prompt_clicked
plan_comparison_viewed
plan_selected                 (property: plan_name, billing_cycle)
checkout_started, checkout_completed, checkout_abandoned
plan_changed                  (property: from_plan, to_plan, change_type)
subscription_cancelled        (property: reason, feedback)
```

#### Sharing / Viral Events
```
invite_sent                   (property: invite_method, recipient_count)
invite_accepted, invite_link_created
content_shared                (property: share_method, content_type)
referral_link_shared, referral_signup_completed
```

### Event Properties

#### Standard Properties (Auto-Attached to Every Event)

```
user_id, anonymous_id, account_id, timestamp, session_id
platform (web/ios/android/api), app_version
user_agent, ip_address (hash for privacy), page_url, referrer
```

#### User Properties (Stored on Profile)

```
signup_date, signup_source, signup_method
plan_type, activation_status, engagement_score
role, company_name, company_size, industry
first_value_date, last_active_date, total_sessions, feature_count_used
```

#### Account Properties (Stored on Account/Group)

```
account_created_date, plan_type, mrr, seat_count
active_user_count, activation_status, health_score
pql_status, csm_assigned
```

---

## Essential Events for PLG

### Signup Flow

| Event | Properties | Purpose |
|-------|-----------|---------|
| `signup_page_viewed` | source, referrer | Track signup page traffic |
| `signup_started` | method (email/sso/social) | Track signup intent |
| `signup_completed` | method, source, referrer | Measure signup conversion |
| `email_verified` | time_to_verify | Track verification friction |

### Activation Events

| Event | Properties | Purpose |
|-------|-----------|---------|
| `aha_moment_reached` | trigger_action, time_from_signup | Track activation |
| `key_feature_first_used` | feature_name | Track feature discovery |
| `first_value_delivered` | value_type | Track time-to-value |

### Core Usage Events

| Event | Properties | Purpose |
|-------|-----------|---------|
| `session_started` | entry_point, device | Track session frequency |
| `feature_used` | feature_name, feature_category, context | Track feature adoption |
| `[core_object]_created` | object_type, method | Track creation activity |
| `error_encountered` | error_type, error_code, page | Track UX friction |

### Collaboration Events

| Event | Properties | Purpose |
|-------|-----------|---------|
| `invite_sent` | method, role, count | Track viral loop input |
| `invite_accepted` | method, time_to_accept | Track viral loop conversion |
| `team_created` | size | Track team expansion |
| `shared_item_created` | item_type, visibility | Track sharing behavior |

### Monetization Events

| Event | Properties | Purpose |
|-------|-----------|---------|
| `upgrade_prompt_viewed` | location, trigger, plan_shown | Track upgrade exposure |
| `upgrade_prompt_clicked` | location, trigger | Track upgrade intent |
| `checkout_started` | plan, amount | Track checkout entry |
| `checkout_completed` | plan, amount, payment_method | Track conversion |
| `checkout_abandoned` | plan, step, reason | Track checkout friction |
| `plan_changed` | from_plan, to_plan, reason | Track plan changes |

---

## User Identification

### The Identification Flow

```
1. Anonymous Visit: Assign anonymous_id (cookie/device ID). Track all events.
2. Signup/Login: Call identify(user_id, traits). Merge anonymous events with user_id.
3. Cross-Device: Same user_id links activity across devices.
4. Account Association: Call group(account_id, traits). Enables account-level analytics.
```

### Best Practices

1. Generate anonymous_id immediately on first page load
2. Call identify() at both signup AND login
3. Use stable user_id (database primary key, not email)
4. Set user properties at identify time
5. Set group/account at login
6. Handle multiple accounts -- track which one is active

### Common Pitfalls

- Identifying too late (anonymous events won't merge)
- Using email as user_id (emails change)
- Not handling logged-out states
- Missing server-side identification
- Not aliasing anonymous_id to user_id on signup

---

## Analytics Tool Comparison

| Tool | Strengths | Best For |
|------|-----------|----------|
| **Mixpanel** | Funnel analysis, flexible event queries, JQL | Event-driven segmentation |
| **Amplitude** | Behavioral cohorting, pathfinding, Amplitude Experiment | Advanced behavioral analysis |
| **PostHog** | Open source, session recordings, feature flags, all-in-one | Self-hosted, privacy-conscious |
| **Heap** | Autocapture, retroactive analysis, low engineering effort | Teams without extensive tracking |
| **GA4** | Free, Google Ads integration | Website/marketing analytics (weak for product analytics) |

---

## Analysis Frameworks

### Funnel Analysis

**Key PLG Funnels**:
1. **Signup**: Landing page -> signup started -> signup completed -> email verified
2. **Activation**: Signup completed -> onboarding -> setup completed -> aha moment
3. **Monetization**: Upgrade prompt viewed -> plan comparison -> checkout started -> checkout completed
4. **Invite**: Invite sent -> invite opened -> invite accepted -> invitee activated

**Checklist**:
- [ ] Define conversion window
- [ ] Segment by user properties (plan, source, device, company size)
- [ ] Identify largest drop-off step
- [ ] Compare funnels across time periods
- [ ] Calculate median time between steps

### Cohort Analysis

**Types**: Acquisition cohorts (by signup date), behavioral cohorts (by actions taken), property cohorts (by user attributes).

**Reading cohort tables**:
- **Rows** = cohorts. Should flatten. Later cohorts flattening higher = product improving.
- **Columns** = time periods. Same column improving over time = retention improving.
- **Diagonals** = specific calendar date across cohorts. Useful for identifying product changes that affected all users.

### Feature Usage Analysis

```
For each feature:
  - Discovery rate: % who used it at least once
  - Adoption rate: % who use it regularly
  - Retention correlation: Does using it correlate with higher retention?
  - Usage depth: How intensely do adopters use it?

To find "magic features":
  1. Create two cohorts: used Feature X in first 7 days vs did not
  2. Compare D30/D60/D90 retention
  3. Features with largest retention gap = promote in onboarding
  4. Caution: correlation != causation. Validate with experiments.
```

---

## Data Quality

### Event Validation

1. Naming follows convention
2. All required properties included
3. Correct types (numbers as numbers, strings as strings)
4. Timestamps in UTC
5. Events fire exactly once per action (no duplicates)
6. Edge cases handled (error, timeout, retry)

### QA Checklist

- [ ] Events fire in dev/staging
- [ ] Event names match taxonomy exactly
- [ ] Properties populated correctly
- [ ] Tested on all platforms (web, mobile, API)
- [ ] Tested with anonymous and identified users
- [ ] identify/alias flow works (signup, login, logout, re-login)
- [ ] No PII in event properties (unless intended)
- [ ] Event volume is reasonable
- [ ] Validated in analytics tool's live event stream

### Data Governance

1. **Taxonomy document**: Single source of truth for all events
2. **Change management**: Review/approval for adding, changing, or removing events
3. **Versioning**: Version your taxonomy
4. **Ownership**: Assign owner per event category
5. **Deprecation**: Mark deprecated before removing
6. **Audit cadence**: Review quarterly

---

## Privacy and Compliance

### GDPR Compliance Checklist

- [ ] Obtain consent before tracking
- [ ] Document lawful basis for each data collection type
- [ ] Implement data subject access requests
- [ ] Implement right to deletion
- [ ] Set data retention policies
- [ ] Ensure analytics vendors have DPAs
- [ ] Handle cross-border data transfers

### Data Retention Policy Template

```
Data Type: [Event data / User properties / Session recordings]
Retention Period: [12 months / 24 months / 36 months]
Justification: [Business need]
Deletion Method: [Automatic / Manual / On request]
Owner: [Person responsible]
```

---

## Self-Serve Analytics

**Tier 1 -- Dashboards** (everyone): PLG metrics, feature adoption, funnels, cohort retention.

**Tier 2 -- Guided exploration** (PMs, growth team): Funnel builder, cohort builder, segmentation, feature comparison.

**Tier 3 -- SQL access** (analysts): Read-only data warehouse, SQL templates, dbt models, BI tool (Looker, Metabase, Mode).

---

## Output Format

### Deliverable 1: Event Taxonomy Document

```
## [Category Name]

### [event_name]
- **Description**: When and why this event fires
- **Trigger**: Specific user action or system event
- **Properties**:
  - property_name (type): Description
- **Platform**: web / mobile / server / all
- **Owner**: [Team]
- **Status**: active / deprecated
```

### Deliverable 2: Implementation Plan

```
Phase 1 (Week 1-2): Core tracking
- Signup and onboarding events, session tracking, user identification

Phase 2 (Week 3-4): Feature tracking
- Core feature events, engagement events, error tracking

Phase 3 (Week 5-6): Growth tracking
- Monetization events, viral/sharing events, retention events

Phase 4 (Ongoing): Optimization
- Data quality audits, dashboard creation, team training
```

### Deliverable 3: Dashboard Specifications

For each dashboard: name and audience, metrics and event sources, visualization types, filters/segments, refresh cadence.

---

## Cross-References

Related skills: `plg-metrics`, `activation-metrics`, `engagement-loops`, `user-segmentation`
