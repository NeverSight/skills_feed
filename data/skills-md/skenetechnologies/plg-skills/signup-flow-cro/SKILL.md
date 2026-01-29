---
name: signup-flow-cro
description: When the user wants to optimize a signup or registration flow -- including field selection, social auth, single-step vs multi-step forms, or mobile signup. Also use when the user says "signup conversion," "registration form," "reduce signup friction," "signup A/B test," or "signup drop-off." For post-signup onboarding, see product-onboarding. For activation measurement, see activation-metrics.
---

# Signup Flow CRO

You are a signup flow optimization specialist. Use this skill when optimizing a product's registration or signup flow to maximize the percentage of visitors who successfully create an account and enter the product. In PLG, the signup flow is the front door -- every percentage point of improvement here compounds through the entire funnel. A 10% improvement in signup conversion has the same downstream impact as a 10% increase in top-of-funnel traffic, but is usually far cheaper to achieve.

## Diagnostic Questions

Before auditing a signup flow, ask the user:

1. What is your current signup completion rate? (If unknown, that's the first thing to measure)
2. How many form fields does your signup flow have?
3. Do you support social auth (Google, GitHub, SSO)?
4. Is your signup single-step or multi-step?
5. What percentage of your signups come from mobile vs desktop?
6. Do you require email verification before the user can access the product?
7. Do you collect payment information during signup?
8. What is your biggest suspected source of drop-off?
9. Do you have analytics on where users abandon the signup flow?
10. What does a new user see immediately after completing signup?

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find signup components**: Search for files matching `*signup*`, `*register*`, `*auth*`, `*login*` in component directories
2. **Count form fields**: Look for `<input>`, `<select>`, form field components -- count required vs optional fields
3. **Check social auth**: Search for OAuth providers -- `google`, `github`, `auth0`, `clerk`, `nextauth`, `supabase auth`, `firebase auth`
4. **Check form structure**: Is it single-step (one component) or multi-step (stepper, wizard, multiple routes)?
5. **Find validation logic**: Search for form validation libraries (`zod`, `yup`, `joi`, `react-hook-form`) and validation rules
6. **Check email verification**: Search for `verify`, `confirm`, `email verification` in auth flows
7. **Find analytics events**: Search for tracking calls on signup steps (`track`, `analytics`, `gtag`, `posthog`, `mixpanel`)
8. **Check mobile responsiveness**: Look for responsive breakpoints, mobile-specific signup styles

Report what you find before proceeding with the framework. Flag gaps (e.g., "No social auth detected", "No analytics on signup flow").

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## Field-by-Field Optimization

Every field in a signup form has a cost (friction, drop-off) and a value (data, personalization, qualification). Evaluate each field against this framework:

**Decision Framework for Each Field:**
1. Is this field required to create the account technically? (e.g., email/password)
2. Does this field meaningfully change the first-run experience?
3. Can this information be collected AFTER signup instead?
4. Can this information be inferred from other data?

If the answer to #1 and #2 is "no," remove the field or defer it to progressive profiling.

### Email Address

| Aspect | Recommendation |
|---|---|
| Keep or Remove | Always keep -- this is your primary identifier |
| Optimization | Use type="email" for mobile keyboard; validate in real-time (format + MX record check); show error inline, not after submit |
| Placeholder text | "name@company.com" (shows expected format) |
| Work email vs personal | If B2B, ask for "Work email" and validate domain is not a free provider (gmail, yahoo). But do not block -- some legitimate users use personal email |
| Auto-detection | Use email domain to pre-fill company name, industry, and company size |

### Password

| Aspect | Recommendation |
|---|---|
| Keep or Remove | Consider removing in favor of passwordless (magic link) |
| Optimization | Show password strength meter; allow show/hide toggle; validate requirements in real-time as user types |
| Requirements | Minimum 8 characters; avoid complex rules (uppercase + number + symbol) that cause frustration. NIST guidelines recommend length over complexity |
| Common pattern | Single password field (no "confirm password") -- the show/hide toggle replaces confirmation |
| Passwordless alternative | Magic link email + optional password set later. Reduces signup form to email-only |

### Full Name

| Aspect | Recommendation |
|---|---|
| Keep or Remove | Often removable -- defer to profile setup after activation |
| If keeping | Single "Full name" field, NOT separate first/last. Handles international names better and is one field instead of two |
| Optimization | Placeholder: "Your full name"; use for personalization in onboarding ("Welcome, Sarah!") |

### Company Name

| Aspect | Recommendation |
|---|---|
| Keep or Remove | Remove from signup form -- infer from email domain using a company data API (Clearbit, Apollo, etc.) |
| If keeping | Placeholder: "Your company"; use autocomplete against a company database |
| When essential | Only if your product requires workspace creation with a company name at signup |

### Role / Job Title

| Aspect | Recommendation |
|---|---|
| Keep or Remove | Remove from signup -- collect in welcome flow (post-signup) where it can personalize the experience |
| If keeping | Use a dropdown with 5-7 common roles, not a free text field |
| Value | Personalizes onboarding path and helps sales qualification, but rarely justifies signup friction |

### Phone Number

| Aspect | Recommendation |
|---|---|
| Keep or Remove | Almost always remove -- highest-friction field, perceived as invasive, causes significant drop-off |
| Exception | Required for SMS verification in high-security products or regulated industries |
| If keeping | Make optional; use country code auto-detection; explain WHY you need it |

### Company Size

| Aspect | Recommendation |
|---|---|
| Keep or Remove | Remove from signup -- infer from email domain or collect in welcome flow |
| If keeping | Use ranges (1-10, 11-50, 51-200, 200+) not exact number |
| Value | Useful for segmentation and sales routing, but better collected post-signup |

---

## Social Authentication

### When to Offer Social Auth

| Factor | Recommendation |
|---|---|
| Target audience is B2B | Offer Google Workspace SSO. Consider Microsoft for enterprise. |
| Target audience is developers | Offer GitHub. Consider GitLab and Bitbucket. |
| Target audience is enterprise | Offer SAML/SSO (required for enterprise sales). Typically gated to paid plans. |
| Target audience is consumer | Offer Google, Apple, Facebook (depends on geography). |
| Target audience is SMB | Google is usually sufficient. |

### Button Placement and Design

1. **Social buttons above email/password** -- reduces perceived effort ("I can sign up with one click")
2. **Use branded buttons** with proper logos, not generic icons
3. **Full-width buttons** outperform small icon-only buttons
4. **Button copy**: "Continue with Google" outperforms "Sign up with Google" (lower commitment language)
5. **Separator**: Use "or" divider between social buttons and email form
6. **Limit to 2-3 options** -- more social buttons creates paradox of choice
7. **Consistent on login AND signup** -- if you offer Google signup, offer Google login

### Trust Implications

- Social auth increases trust for unknown brands ("I don't have to give them my password")
- Social auth decreases trust in privacy-sensitive contexts ("I don't want to share my Google data")
- Always show what data you are requesting in the OAuth consent screen
- Never request unnecessary OAuth scopes (e.g., do not ask for contacts access if you do not need it)

---

## Single-Step vs Multi-Step Signup

### Single-Step Signup

All fields on one page. User fills in email, password, and any other fields, then clicks one submit button.

**Best for:**
- Forms with 3 or fewer fields
- High-intent users (pricing page CTA, after a product demo)
- Simple products with fast time-to-value

### Multi-Step Signup

Fields are broken across 2-3 pages or accordion sections. User completes one set of fields, then advances.

**Best for:**
- Forms requiring 4+ fields
- When you need to collect qualifying information
- When questions build on each other (e.g., "What is your role?" then "What will you use [product] for?")

### When Multi-Step Wins

Multi-step signup often outperforms single-step when:
1. **Total field count is 4+** -- breaking into steps reduces perceived effort
2. **Progressive commitment** -- getting users to enter email first creates commitment (foot-in-the-door effect)
3. **Conditional logic is needed** -- different roles need different follow-up questions
4. **Personalization requires it** -- answers to early questions change later steps or the product experience

### Multi-Step Design Rules

1. **Step 1: Email only** (or email + social auth) -- lowest possible barrier to start
2. **Show progress**: "Step 1 of 3" or a progress bar
3. **Allow back navigation** -- users should be able to change previous answers
4. **Save state** -- if a user leaves mid-flow and returns, resume where they left off
5. **No more than 3 steps** -- more causes steep drop-off
6. **Each step should have 1-3 fields** -- not 5+ fields spread across steps

---

## Progressive Profiling

Instead of collecting all user information at signup, progressive profiling collects information gradually across multiple sessions and touchpoints.

### Implementation Pattern

```
Signup:        Email + Password (or social auth)
First login:   "What's your role?" (welcome flow)
Day 2:         "What's your primary use case?" (in-app prompt)
Day 5:         "How big is your team?" (contextual when they invite someone)
Day 14:        "What tools do you currently use?" (integration setup page)
```

### Rules for Progressive Profiling

1. **Ask at the moment of relevance** -- ask about team size when they try to invite, not at signup
2. **Explain the value exchange** -- "Tell us your role so we can customize your dashboard"
3. **Make every question optional** -- always provide a "Skip" or "Not now" option
4. **Never ask the same question twice** -- persist answers and do not re-prompt
5. **Cap frequency** -- no more than 1 profiling question per session

---

## Email Verification

### Pre-Activation vs Post-Activation Verification

| Approach | How It Works | Pros | Cons |
|---|---|---|---|
| Pre-activation | User must verify email before accessing product | Cleaner data, prevents spam accounts | Adds friction, loses users who do not check email immediately |
| Post-activation | User accesses product immediately; verification required later (e.g., before inviting team or exporting) | Lower friction, faster time-to-value | Some unverified accounts, data quality risk |

**Recommendation:** Post-activation verification is almost always better for PLG. Let users into the product immediately. Gate specific high-value actions (inviting team, connecting integrations, upgrading) behind verification.

### Verification Methods

| Method | UX | Security | Recommendation |
|---|---|---|---|
| Click link in email | Simple, one-click | Medium | Best for most products |
| Enter 6-digit code | Requires switching context to copy code | Higher | Good for mobile-first products |
| Magic link (passwordless) | Combines signup and verification in one step | Medium | Best if going passwordless |

### Verification UX Best Practices

1. **Show a clear "check your email" page** with the email address displayed and a "Resend" button
2. **Auto-detect verification**: when the user clicks the link in another tab, auto-advance the waiting page
3. **Offer "Change email"** option on the waiting page (in case of typo)
4. **Resend cooldown**: Allow resend after 30 seconds, not immediately (prevents spam clicking)
5. **Check spam folder prompt**: After 60 seconds, suggest checking spam folder with instructions to whitelist

---

## Mobile Signup Optimization

### Thumb Zone Design

- Place primary CTA (signup button) in the easy-reach thumb zone (bottom half of screen)
- Place form fields in the natural scrolling area (center)
- Avoid placing critical elements in the hard-to-reach top corners

### Keyboard Optimization

| Field | Input Type | HTML Attribute |
|---|---|---|
| Email | Email keyboard with @ | `type="email"` `inputmode="email"` |
| Password | Text with show/hide | `type="password"` |
| Phone | Numeric keypad | `type="tel"` `inputmode="tel"` |
| Verification code | Numeric keypad | `inputmode="numeric"` `autocomplete="one-time-code"` |
| Name | Default text keyboard | `type="text"` `autocomplete="name"` |

### Autofill Optimization

- Use correct `autocomplete` attributes so browsers and password managers can auto-fill
- `autocomplete="email"` for email fields
- `autocomplete="new-password"` for registration password fields
- `autocomplete="name"` for full name
- `autocomplete="organization"` for company name
- Test with 1Password, LastPass, and browser native autofill

---

## Post-Submit Experience

What happens in the 5-10 seconds after a user clicks "Sign Up" is critical. This transition sets the tone for the entire onboarding experience.

### Options and Decision Framework

| Option | Best For | Implementation |
|---|---|---|
| Direct to product | Products with fast TTV, product-first onboarding | Redirect immediately to the product dashboard |
| Welcome flow | Products needing personalization data | Redirect to a 2-3 question flow, then to product |
| Confirmation page | Products requiring email verification before access | Show "Check your email" page with clear instructions |
| Loading transition | Products needing background setup (workspace creation) | Show a branded loading screen with progress messaging |

**Best practice:** Never show a generic "Thank you for signing up" page with no next action. Always direct the user toward the next step immediately.

### The Loading Transition

If your product needs time to provision a workspace, use this time wisely:

```
[Logo + Progress animation]
"Setting up your workspace..."
"Connecting your integrations..."
"Almost ready..."
"Welcome to [Product]! →"
```

Interleave setup messages with value propositions or tips to reduce perceived wait time.

---

## Signup Page Design

### Essential Elements

1. **Headline**: Value proposition in 6-10 words. "Start [benefit] in minutes" or "[Product] -- [value statement]"
2. **Social proof**: Customer logos, user count ("Join 50,000+ teams"), testimonial quote
3. **Form**: Minimal fields (see field-by-field analysis above)
4. **Trust signals**: Security badges, "No credit card required," privacy link, SOC2/GDPR compliance
5. **Value reminders**: 2-3 bullet points of key benefits next to the form
6. **Login link**: "Already have an account? Log in" -- prevents accidental duplicate signups

### Layout Patterns

- **Split screen**: Form on right, value prop + social proof on left (best for desktop B2B)
- **Centered form**: Form in center with social proof above/below (best for simple, mobile-first)
- **Full-page form**: Form takes full viewport, minimal distractions (best for high-intent pages)

### Trust Signals by Priority

1. "Free" or "No credit card required" -- removes #1 signup fear
2. Customer logos -- social proof from recognized brands
3. User count -- "Join 50,000+ teams" (only if the number is impressive)
4. Security certifications -- SOC2, GDPR, ISO (important for B2B)
5. Review scores -- G2, Capterra, TrustPilot ratings
6. Guarantee -- "14-day free trial" or "Cancel anytime"

---

## Signup Analytics

### Field-Level Drop-Off Tracking

Track not just whether users submit the form, but where they disengage.

**Metrics to track for each field:**
- **Field focus rate**: % of users who click/tap into this field
- **Field completion rate**: % of users who enter a valid value
- **Time per field**: How long users spend on each field
- **Error rate**: % of submissions with validation errors on this field
- **Error resolution rate**: % of users who fix the error vs abandon
- **Field-level drop-off**: % of users who interact with this field but abandon the form before submitting

### Analytics Implementation

```
Track these events:
- signup_page_viewed
- signup_field_focused (field_name)
- signup_field_completed (field_name, time_spent)
- signup_field_error (field_name, error_type)
- signup_submitted
- signup_succeeded
- signup_failed (error_type)
- social_auth_clicked (provider)
- social_auth_succeeded (provider)
- social_auth_failed (provider, error_type)
```

---

## A/B Test Ideas for Signup Flows

Here are 12 specific, testable hypotheses for signup flow optimization:

### Friction Reduction Tests

1. **Remove the name field**: Hypothesis: Removing the "Full name" field from signup will increase form completion by 5-10% without impacting activation rate.

2. **Passwordless signup**: Hypothesis: Replacing password field with magic link will increase signup conversion by 10-15% (particularly on mobile).

3. **Single field first step**: Hypothesis: Starting with email-only (Step 1) then password (Step 2) will increase overall completion vs. showing both fields at once.

4. **Defer email verification**: Hypothesis: Allowing product access before email verification will increase Day 1 activation by 15-25%.

### Social Auth Tests

5. **Social auth button position**: Hypothesis: Moving "Continue with Google" above the email form (instead of below) will increase social auth usage by 20-30% and total signup conversion by 5%.

6. **Add GitHub auth for dev tools**: Hypothesis: Adding GitHub authentication will increase developer signup conversion by 8-12%.

7. **Social auth copy**: Hypothesis: "Continue with Google" will outperform "Sign up with Google" by 3-5% due to lower-commitment language.

### Design and Copy Tests

8. **Social proof on signup page**: Hypothesis: Adding customer logos and "Join X teams" below the form will increase signup conversion by 5-8%.

9. **Value proposition headline**: Test specific outcome language ("Build dashboards in 5 minutes") vs. generic ("The best analytics platform").

10. **Remove navigation**: Hypothesis: Removing the site header/navigation on the signup page will increase focus and improve conversion by 3-5%.

### Flow Structure Tests

11. **Progressive profiling vs upfront**: Hypothesis: Collecting role and use case after signup (in the welcome flow) instead of during signup will increase form completion by 10-15% with no loss in data collection rate.

12. **Multi-step vs single-step**: Hypothesis: Breaking a 5-field form into 2 steps (email+password then name+company+role) will increase completion by 8-12%.

### Test Prioritization Framework

| Test | Effort | Expected Impact | Priority |
|---|---|---|---|
| Remove unnecessary fields | Low | Medium | P1 -- Do first |
| Defer email verification | Medium | High | P1 -- Do first |
| Social auth position/copy | Low | Low-Medium | P2 -- Quick win |
| Passwordless signup | Medium | Medium-High | P2 -- If password drop-off is high |
| Progressive profiling | Medium | Medium | P2 |
| Page design changes | Low | Low-Medium | P3 |
| Multi-step restructure | High | Medium | P3 -- Only if form has 4+ fields |

---

## Output Format: Signup Flow Optimization Audit

When auditing a signup flow, produce a document with these sections:

```
# [Product Name] -- Signup Flow Optimization Audit

## 1. Current State Assessment
- Current signup conversion rate: [X%] (visitor → account created)
- Number of fields: [N]
- Signup type: [Single-step / Multi-step]
- Social auth options: [List]
- Email verification: [Pre-activation / Post-activation]
- Mobile optimization: [Yes/No, specific issues]

## 2. Field-by-Field Audit

| Field | Keep/Remove/Defer | Rationale | Optimization Needed |
|---|---|---|---|
| Email | Keep | Required | [Specific improvement] |
| Password | [Recommendation] | [Reason] | [Specific improvement] |
| [Field 3] | [Recommendation] | [Reason] | [Specific improvement] |

## 3. Friction Points Identified
- Friction 1: [Description + evidence (drop-off data, heatmap, etc.)]
- Friction 2: [Description + evidence]
- Friction 3: [Description + evidence]

## 4. Recommendations (Prioritized)

### P1: High Impact, Low Effort
- Recommendation 1: [What to change + expected impact]
- Recommendation 2: [What to change + expected impact]

### P2: High Impact, Medium Effort
- Recommendation 3: [What to change + expected impact]

### P3: Medium Impact, Higher Effort
- Recommendation 4: [What to change + expected impact]

## 5. A/B Test Plan
- Test 1: [Hypothesis, variant description, success metric, estimated duration]
- Test 2: [Hypothesis, variant description, success metric, estimated duration]
- Test 3: [Hypothesis, variant description, success metric, estimated duration]

## 6. Signup Page Design Recommendations
- Layout: [Recommendation]
- Social proof: [What to add/change]
- Trust signals: [What to add/change]
- CTA copy: [Recommendation]
- Mobile: [Specific mobile improvements]

## 7. Expected Impact
- Estimated conversion rate improvement: [X-Y%]
- Incremental signups per month: [N]
- Downstream impact on activation: [Estimate]
```

---

## Related Skills

- `activation-metrics` -- Ensuring signup optimization is connected to downstream activation
- `product-onboarding` -- The experience immediately after signup
- `self-serve-motion` -- The broader self-serve customer journey that signup is part of
