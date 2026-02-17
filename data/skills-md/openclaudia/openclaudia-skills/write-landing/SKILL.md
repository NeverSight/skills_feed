---
name: write-landing
description: Create high-converting landing page copy and structure. Use when the user says "landing page", "sales page", "create a landing page", "landing page copy", "conversion page", "lead gen page", "signup page", "product page copy", "hero section", "write landing page", or asks for marketing page copy with conversion goals.
---

# Write Landing Page Skill

You are an expert conversion copywriter and landing page strategist. Create complete landing page copy with wireframe structure, optimized for both conversions and SEO. Output is ready to implement in Next.js/React with Tailwind CSS.

## Landing Page Process

### Step 1: Gather the Brief

Before writing, understand:

| Question | Why it matters |
|----------|---------------|
| **Product/Service:** What are you selling? | Core messaging foundation |
| **Target audience:** Who is the ideal customer? | Voice, pain points, language |
| **Primary goal:** What action should visitors take? | CTA optimization |
| **Traffic source:** How will people arrive? (Ads, organic, email) | Message match |
| **Price point:** How much does it cost? | Objection handling depth |
| **Key differentiator:** Why you over competitors? | USP positioning |
| **Proof points:** Testimonials, case studies, metrics? | Social proof section |
| **Existing brand voice:** Formal, casual, technical? | Tone consistency |

If the user doesn't provide all of these, ask for the critical ones (product, audience, goal) and make reasonable assumptions for the rest.

### Step 2: Choose the Page Structure

Select the right framework based on the product type and traffic temperature:

#### Framework A: PAS (Problem-Agitation-Solution)
**Best for:** Cold traffic, awareness stage, complex problems
```
Hero (Problem statement)
  -> Agitate (Consequences of not solving)
  -> Solution (Your product)
  -> Features/Benefits
  -> Social Proof
  -> CTA
```

#### Framework B: AIDA (Attention-Interest-Desire-Action)
**Best for:** Warm traffic, known product category
```
Hero (Attention-grabbing headline)
  -> Interest (Key features and hook)
  -> Desire (Benefits, social proof, FOMO)
  -> Action (CTA with urgency)
```

#### Framework C: Before-After-Bridge
**Best for:** Transformation products (SaaS, courses, coaching)
```
Hero (Before: current painful state)
  -> After (Vision of success)
  -> Bridge (Your product is the bridge)
  -> How it works
  -> Proof
  -> CTA
```

#### Framework D: Feature-Benefit Grid
**Best for:** Technical products, SaaS, feature-rich tools
```
Hero (Bold promise)
  -> Feature-benefit grid
  -> How it works (3 steps)
  -> Integrations/Compatibility
  -> Pricing
  -> FAQ
  -> CTA
```

### Step 3: Write Each Section

#### Section 1: Hero

The hero section has 5 seconds to hook the visitor. Every word must earn its place.

**Headline formula (H1):**

| Formula | When to use | Example |
|---------|------------|---------|
| `{End result} without {Pain point}` | When eliminating a known pain | "Build your website without writing code" |
| `{Action verb} your {metric} by {amount}` | When you have proven results | "Double your email open rates in 30 days" |
| `The {adjective} way to {desired outcome}` | When the method is the differentiator | "The fastest way to deploy full-stack apps" |
| `{Desired outcome} for {audience}` | When audience-specific | "Enterprise-grade security for startups" |
| `Stop {pain}. Start {benefit}.` | When the problem is acute | "Stop losing leads. Start closing deals." |
| `{Number} {people} use {product} to {outcome}` | When you have social proof scale | "50,000 marketers use Buffer to grow on social" |

**Headline rules:**
- Max 10 words (6-8 is ideal)
- Specific > vague ("50% faster" > "blazing fast")
- Benefit > feature ("Save 10 hours/week" > "AI-powered automation")
- Include the audience or their goal

**Subheadline (H2):**
Expand on the headline with specifics. Formula:
```
{Product} helps {audience} {achieve outcome} by {mechanism/method}. {Proof point or time frame}.
```
Example: "Acme helps SaaS teams automate their deployment pipeline with one-click CI/CD. Ship 10x faster from day one."

**CTA Button:**
- Use first-person: "Start my free trial" > "Start your free trial"
- Action-oriented: "Get started free" > "Submit" > "Sign up"
- Add micro-copy below: "No credit card required. Free for 14 days."
- Button color should contrast with background (high contrast = more clicks)

**Supporting element (choose one):**
- Product screenshot or demo video
- Key metric ("Trusted by 10,000+ companies")
- Logo bar of notable customers
- Short demo GIF

```tsx
{/* Hero Section */}
<section className="relative bg-white pt-20 pb-16 sm:pt-24 sm:pb-20 lg:pt-32 lg:pb-28">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-2xl text-center lg:max-w-4xl">
      {/* Eyebrow / Social proof badge */}
      <p className="text-sm font-semibold text-indigo-600">
        Trusted by 10,000+ teams
      </p>

      {/* H1 Headline */}
      <h1 className="mt-4 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
        {headline}
      </h1>

      {/* Subheadline */}
      <p className="mt-6 text-lg leading-8 text-gray-600 sm:text-xl">
        {subheadline}
      </p>

      {/* CTA Group */}
      <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
        <a href="#" className="rounded-lg bg-indigo-600 px-8 py-4 text-base font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
          {primaryCTA}
        </a>
        <a href="#" className="text-base font-semibold text-gray-900 hover:text-gray-700">
          {secondaryCTA} <span aria-hidden="true">&rarr;</span>
        </a>
      </div>

      {/* Micro-copy */}
      <p className="mt-4 text-sm text-gray-500">
        No credit card required. Free 14-day trial.
      </p>
    </div>

    {/* Hero Image/Video */}
    <div className="mt-16 sm:mt-20">
      <div className="rounded-xl bg-gray-900/5 p-2 ring-1 ring-gray-900/10 lg:rounded-2xl">
        {/* Product screenshot or demo */}
      </div>
    </div>
  </div>
</section>
```

---

#### Section 2: Problem / Pain Points

Make the reader feel understood. Describe their current situation precisely.

**Writing technique:** Use the reader's own language. Mirror the words they use in reviews, support tickets, and forums.

```tsx
<section className="bg-gray-50 py-16 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-2xl text-center">
      <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
        {problem_headline}
      </h2>
      <p className="mt-4 text-lg text-gray-600">
        {problem_description}
      </p>
    </div>

    <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
      {/* Pain point cards */}
      {painPoints.map((pain) => (
        <div className="rounded-lg border border-red-100 bg-white p-6">
          <div className="text-red-500 text-2xl mb-3">{pain.icon}</div>
          <h3 className="text-lg font-semibold text-gray-900">{pain.title}</h3>
          <p className="mt-2 text-gray-600">{pain.description}</p>
        </div>
      ))}
    </div>
  </div>
</section>
```

**Pain point formula:**
```
Title: "{Frustrating situation}"
Description: "You {specific scenario}. But {consequence}. And {escalation}."
```

Example:
- Title: "Deployment takes hours, not minutes"
- Description: "You push code and wait. Build fails. Fix it. Wait again. By the time it's live, the bug report queue has doubled. And your weekend is gone."

---

#### Section 3: Solution / How It Works

Transition from pain to solution. Show the product as the bridge.

**"How It Works" in 3 steps** (always 3 - humans love triads):

```tsx
<section className="bg-white py-16 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-2xl text-center">
      <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
        How it works
      </h2>
      <p className="mt-4 text-lg text-gray-600">
        Get started in minutes, not months.
      </p>
    </div>

    <div className="mt-16 grid grid-cols-1 gap-12 lg:grid-cols-3">
      {steps.map((step, i) => (
        <div className="text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100 text-indigo-600 font-bold text-xl">
            {i + 1}
          </div>
          <h3 className="mt-6 text-xl font-semibold text-gray-900">{step.title}</h3>
          <p className="mt-4 text-gray-600">{step.description}</p>
        </div>
      ))}
    </div>
  </div>
</section>
```

**Step formula:**
```
Step 1: "{Simple first action}" - Lower the barrier to entry
Step 2: "{Core value action}" - The product doing its thing
Step 3: "{Desired outcome}" - The result they care about
```

Example:
1. "Connect your repo" - Link your GitHub in one click
2. "Push your code" - Our AI handles builds, tests, and deployment
3. "Ship with confidence" - Go live in minutes with zero-downtime deploys

---

#### Section 4: Features & Benefits

Never list features alone. Always pair with the benefit (the "so what?").

**Feature-Benefit formula:**
```
Feature: {What it does}
Benefit: So you can {outcome the user cares about}
```

```tsx
<section className="bg-white py-16 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-2xl text-center">
      <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
        Everything you need to {desired outcome}
      </h2>
    </div>

    <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
      {features.map((feature) => (
        <div className="relative rounded-2xl border border-gray-200 p-8">
          <div className="text-indigo-600 mb-4">{feature.icon}</div>
          <h3 className="text-lg font-semibold text-gray-900">{feature.title}</h3>
          <p className="mt-2 text-gray-600">{feature.benefit}</p>
        </div>
      ))}
    </div>
  </div>
</section>
```

**Arrange features by importance:**
1. The feature that solves the #1 pain point (biggest, most prominent)
2. The feature that differentiates from competitors
3. Supporting features that round out the product
4. Nice-to-haves and integrations

---

#### Section 5: Social Proof

Social proof is the most persuasive element on the page. Layer multiple types:

**Types of social proof (use 2-3):**

| Type | Impact Level | Example |
|------|-------------|---------|
| Customer testimonials with photo + name + company | Highest | "Acme increased revenue 40% in 3 months" - Jane Doe, CEO at TechCo |
| Case study metrics | Highest | "From 2 deploys/week to 50 deploys/day" |
| Logo bar of customers | High | Well-known brand logos |
| Number of customers | High | "Join 50,000+ teams" |
| Star ratings / review scores | High | "4.8/5 on G2 (500+ reviews)" |
| Awards / certifications | Medium | "SOC 2 Certified", "G2 Leader 2025" |
| Media mentions | Medium | "As featured in TechCrunch, Forbes..." |
| Integration partners | Medium | "Works with Slack, GitHub, Jira..." |

```tsx
{/* Testimonial Section */}
<section className="bg-gray-50 py-16 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-2xl text-center">
      <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
        Loved by teams worldwide
      </h2>
    </div>

    <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-3">
      {testimonials.map((t) => (
        <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
          <div className="flex items-center gap-1 text-yellow-400">
            {/* 5 star icons */}
          </div>
          <blockquote className="mt-4 text-gray-700">
            &ldquo;{t.quote}&rdquo;
          </blockquote>
          <div className="mt-6 flex items-center gap-4">
            <img src={t.avatar} alt={t.name} className="h-12 w-12 rounded-full" />
            <div>
              <p className="font-semibold text-gray-900">{t.name}</p>
              <p className="text-sm text-gray-500">{t.role} at {t.company}</p>
            </div>
          </div>
        </div>
      ))}
    </div>

    {/* Logo bar */}
    <div className="mt-16">
      <p className="text-center text-sm font-semibold text-gray-500">
        Trusted by leading companies
      </p>
      <div className="mt-6 flex flex-wrap items-center justify-center gap-x-12 gap-y-6">
        {/* Customer logos */}
      </div>
    </div>
  </div>
</section>
```

**Testimonial writing rules:**
- Include specific outcomes ("40% more leads" > "more leads")
- Include name, role, company, and photo (real > stock)
- Match testimonials to the objection they overcome
- Put the most impressive testimonial closest to the CTA

---

#### Section 6: Objection Handling / FAQ

Address the top 5-7 objections that prevent conversion:

**Common objection categories:**

| Objection | How to address |
|-----------|---------------|
| "It's too expensive" | ROI comparison, cost of inaction, payment plans |
| "I don't have time to set up" | Quick start time, onboarding support, migration help |
| "What if it doesn't work for me?" | Guarantee, free trial, case studies from similar companies |
| "I'm locked into {competitor}" | Migration tools, comparison, switching cost analysis |
| "Is my data safe?" | Security certifications, compliance, data policies |
| "What if I need help?" | Support channels, response time SLA, documentation |
| "It looks too complex" | 3-step "how it works", demo video, free trial |

```tsx
<section className="bg-white py-16 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-3xl">
      <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl text-center">
        Frequently asked questions
      </h2>

      <dl className="mt-12 space-y-8">
        {faqs.map((faq) => (
          <div className="border-b border-gray-200 pb-8">
            <dt className="text-lg font-semibold text-gray-900">{faq.question}</dt>
            <dd className="mt-4 text-gray-600">{faq.answer}</dd>
          </div>
        ))}
      </dl>
    </div>
  </div>
</section>
```

---

#### Section 7: Pricing (if applicable)

Only include pricing on the landing page if:
- The product has clear, fixed pricing
- The user wants pricing on the page
- The traffic is warm/hot (they already know what the product does)

```tsx
<section className="bg-gray-50 py-16 sm:py-24" id="pricing">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-2xl text-center">
      <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
        Simple, transparent pricing
      </h2>
      <p className="mt-4 text-lg text-gray-600">
        {pricing_subheadline}
      </p>
    </div>

    <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-3">
      {plans.map((plan) => (
        <div className={`rounded-2xl p-8 ring-1 ${plan.featured ? 'bg-indigo-600 text-white ring-indigo-600' : 'bg-white ring-gray-200'}`}>
          <h3 className="text-lg font-semibold">{plan.name}</h3>
          <p className="mt-2 text-sm opacity-80">{plan.description}</p>
          <p className="mt-6">
            <span className="text-4xl font-bold">${plan.price}</span>
            <span className="text-sm opacity-80">/month</span>
          </p>
          <ul className="mt-8 space-y-3">
            {plan.features.map((f) => (
              <li className="flex items-center gap-3">
                {/* Check icon */}
                <span>{f}</span>
              </li>
            ))}
          </ul>
          <a href="#" className={`mt-8 block w-full rounded-lg py-3 text-center font-semibold ${plan.featured ? 'bg-white text-indigo-600' : 'bg-indigo-600 text-white'}`}>
            {plan.cta}
          </a>
        </div>
      ))}
    </div>
  </div>
</section>
```

**Pricing copy rules:**
- Anchor with the highest plan first (or highlight the middle plan)
- Use specific numbers ("$49/mo" > "Starting at...")
- Show value: "$49/mo - less than the cost of one lost lead"
- Feature the most popular plan with a badge
- Include annual discount toggle if applicable

---

#### Section 8: Final CTA

The closing CTA should create urgency and restate the core value:

```tsx
<section className="bg-indigo-600 py-16 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-2xl text-center">
      <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
        {final_headline}
      </h2>
      <p className="mt-4 text-lg text-indigo-100">
        {final_subheadline}
      </p>
      <div className="mt-10">
        <a href="#" className="rounded-lg bg-white px-8 py-4 text-base font-semibold text-indigo-600 shadow-sm hover:bg-indigo-50">
          {finalCTA}
        </a>
      </div>
      <p className="mt-4 text-sm text-indigo-200">
        {risk_reversal - e.g., "30-day money-back guarantee. Cancel anytime."}
      </p>
    </div>
  </div>
</section>
```

**Final CTA formulas:**
```
"Ready to {desired outcome}?"
"Start {action}ing today"
"Join {number}+ {audience} already {outcome}"
"Don't let {pain point} hold you back"
"{Outcome} is one click away"
```

### Step 4: SEO Optimization

Landing pages should rank too. Include:

**Meta tags:**
- Title: "{Product} - {Primary benefit} | {Brand}" (50-60 chars)
- Description: "{Product} helps {audience} {outcome}. {Proof point}. {CTA}." (150-160 chars)

**On-page SEO:**
- H1 includes primary keyword
- Primary keyword in first 100 words
- Image alt text with keyword
- Internal links to and from the landing page
- Schema markup (Product, Organization, FAQ, or SoftwareApplication)

**Reminder:** Landing pages for paid traffic may need `noindex` if they duplicate content from organic pages.

### Step 5: Conversion Optimization Checklist

Before delivering, verify:

- [ ] Single, clear CTA (one primary action per page)
- [ ] CTA appears 3+ times (hero, middle, end)
- [ ] CTA button text is action-oriented and first-person
- [ ] Page loads fast (minimize scripts, optimize images)
- [ ] Mobile responsive (all sections tested at 375px)
- [ ] No navigation menu (or minimal) to reduce exit points
- [ ] Social proof within scroll of first CTA
- [ ] Risk reversal near every CTA (guarantee, free trial, no CC)
- [ ] Benefit-first headlines (not feature-first)
- [ ] Specific numbers > vague claims
- [ ] White space between sections (not cluttered)
- [ ] Contrast on CTA buttons (stands out from page)
- [ ] Urgency element where authentic (limited spots, deadline, rising price)

## Output Format

Deliver in this order:

1. **Page strategy** - Framework chosen, audience, goal, messaging hierarchy
2. **Full copy document** - All sections with headlines, body copy, CTAs, and micro-copy
3. **Wireframe structure** - Section order with Tailwind component code
4. **SEO metadata** - Title, description, schema markup
5. **A/B test suggestions** - 2-3 elements to test first (headline, CTA, social proof)

## Important Notes

- Every claim needs proof. "Best tool" needs a G2 ranking. "Fastest" needs a benchmark. Unsubstantiated claims reduce trust.
- Write at a Grade 6-8 reading level. Simple words, short sentences, clear logic.
- If the user provides brand guidelines or voice preferences, follow them. If not, default to: confident, clear, conversational, not salesy.
- For SaaS: emphasize ease of setup, time to value, and integration ecosystem.
- For e-commerce: emphasize product quality, shipping speed, return policy, and reviews.
- For services: emphasize expertise, process, results, and risk reversal.
