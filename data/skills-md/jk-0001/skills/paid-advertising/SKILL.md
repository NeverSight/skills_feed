---
name: paid-advertising
description: Plan, launch, and optimize paid advertising campaigns for a solopreneur business. Use when running ads on Google, Facebook, LinkedIn, or other platforms to drive traffic, leads, or sales. Covers platform selection, campaign structure, ad copy and creative, targeting, budget allocation, conversion tracking, and optimization based on performance data. Trigger on "paid ads", "run ads", "Facebook ads", "Google ads", "advertising strategy", "ad campaign", "PPC", "how to advertise".
---

# Paid Advertising

## Overview
Paid ads let you buy attention and traffic immediately, unlike SEO or content marketing which take months. But most solopreneurs waste money on ads because they don't understand targeting, tracking, or optimization. This playbook shows you how to run profitable ad campaigns on a solopreneur budget — without burning cash on guesswork.

---

## Step 1: Decide If You're Ready for Paid Ads

Ads accelerate what's already working. If your funnel is broken, ads just speed up the bleeding.

**Don't run ads until you have:**
- [ ] A clear offer (what you're selling and to whom)
- [ ] A landing page or sales funnel that converts (even if at small scale)
- [ ] Unit economics that work (see unit-economics skill — LTV > CAC)
- [ ] At least $500-1,000 to test with (less than this and you won't get enough data)

**Rule:** Fix your funnel first, then amplify with ads. Never use ads to figure out if your product works.

---

## Step 2: Choose Your Ad Platform

Different platforms serve different audiences and goals. Pick based on where your ICP hangs out and what action you want them to take.

**Platform comparison:**

| Platform | Best For | Typical CPC | Strengths | Weaknesses |
|---|---|---|---|---|
| **Google Ads (Search)** | High-intent leads, people actively searching | $2-$10+ | Captures existing demand, high intent | Competitive, needs keyword research |
| **Facebook/Instagram Ads** | Awareness, B2C products, broad targeting | $0.50-$3 | Detailed targeting, visual, retargeting | Lower intent, ad fatigue |
| **LinkedIn Ads** | B2B, targeting by job title/company | $5-$15+ | Precise professional targeting | Expensive, smaller audience |
| **Google Ads (Display)** | Awareness, retargeting | $0.50-$2 | Massive reach, cheap impressions | Very low intent, banner blindness |
| **YouTube Ads** | Video products, B2C, brand building | $0.10-$0.30 per view | Engaging format, cheap views | Requires video production |
| **Twitter/X Ads** | Tech/startup audience, real-time topics | $0.50-$3 | Good for thought leadership, niche targeting | Smaller scale, engagement-focused |

**Selection criteria:**
- **Where does your ICP spend time?** B2B SaaS founders = LinkedIn or Google Search. E-commerce = Facebook/Instagram. Local services = Google Search + Facebook.
- **What's your goal?** Lead gen = Google Search or LinkedIn. Brand awareness = Facebook/Instagram. Direct sales = Facebook/Instagram for B2C, LinkedIn for B2B.
- **What's your budget?** Under $1,000/month = start with Facebook or Google Search. Over $3,000/month = test LinkedIn or multi-platform.

**Recommendation for solopreneurs:** Start with ONE platform. Master it before expanding.

---

## Step 3: Set Up Conversion Tracking (Do This First)

If you can't measure conversions, you can't optimize. Set up tracking BEFORE you launch any ads.

**What to track:**
- **Lead gen campaigns:** Form submissions, email signups, call bookings
- **E-commerce:** Purchases, add-to-cart, checkout initiated
- **SaaS:** Trial signups, demo requests, account creation

**How to set up tracking:**

**For Google Ads:**
- Install Google Tag (via Google Tag Manager or directly on site)
- Set up conversion actions in Google Ads dashboard
- Test with Google Tag Assistant

**For Facebook/Instagram Ads:**
- Install Meta Pixel on your website
- Create custom conversions in Events Manager
- Test with Meta Pixel Helper (Chrome extension)

**For LinkedIn Ads:**
- Install LinkedIn Insight Tag on your website
- Define conversion events in Campaign Manager

**Rule:** Don't trust platform reporting alone. Cross-check with Google Analytics or your CRM to verify conversions are being tracked accurately.

---

## Step 4: Structure Your First Campaign

Campaign structure matters. Poor structure makes optimization impossible.

**Campaign hierarchy (Facebook/Google/LinkedIn are similar):**
```
CAMPAIGN (the objective + budget)
  ↳ AD SET (the audience + placement + schedule)
    ↳ ADS (the creative + copy)
```

**Example structure (Facebook lead gen campaign):**
```
CAMPAIGN: "Lead Gen - Free Checklist"
  Budget: $30/day
  Objective: Lead generation

  ↳ AD SET 1: "Warm Audience - Website Visitors"
    Audience: People who visited website in last 30 days
    Placement: Facebook feed + Instagram feed
    Budget: $15/day

  ↳ AD SET 2: "Cold Audience - Interest-Based"
    Audience: SaaS founders, interested in automation
    Placement: Facebook feed + Instagram feed
    Budget: $15/day

    ↳ AD 1: Carousel with 5 checklist items teaser
    ↳ AD 2: Single image with bold headline
    ↳ AD 3: Video (30 sec) explaining the value
```

**Why this structure works:**
- Tests warm vs cold audiences separately (different performance, different optimization strategies)
- Tests multiple ad creatives against each audience
- Allocates budget based on what's working (you can shift $$ from cold to warm if warm performs better)

---

## Step 5: Write Ad Copy and Design Creative

Your ad creative (image/video + copy) determines whether people stop scrolling. Most solopreneur ads fail here.

**Ad copy formula (Facebook/LinkedIn/Instagram):**

```
HOOK (first line — stops the scroll)
  "Still spending 10 hours/week on manual reporting?"

AGITATE or RELATE (make them feel the pain or relate to the situation)
  "Most agencies waste entire days pulling data from 6 tools into one report."

SOLUTION (your offer)
  "Our automation template does it in 10 minutes."

PROOF (social proof or result)
  "Used by 500+ agencies to save 40+ hours/month."

CTA (clear action)
  "Download the free template → [link]"
```

**Google Search ads (text-based):**
```
HEADLINE 1: Include target keyword ("n8n Automation Services")
HEADLINE 2: State the benefit ("Save 20 Hours/Week")
HEADLINE 3: Include a differentiator ("Built for SaaS Teams")

DESCRIPTION 1: Expand on the value (150 characters max)
DESCRIPTION 2: Include a CTA and urgency/social proof
```

**Creative (image/video) best practices:**
- **Use faces** (ads with human faces get 38% more engagement)
- **Keep text minimal** (under 20% of image should be text — Facebook penalizes text-heavy images)
- **Show the outcome, not the process** (don't show a screenshot of your tool — show a happy customer or a result)
- **Test multiple formats:** Static image, carousel (3-5 images), video (15-30 sec)

**Rule:** Create 3-5 ad variations per ad set. Test different hooks, images, and CTAs. Let the data tell you which works.

---

## Step 6: Target the Right Audience

Bad targeting = wasted budget. Even great ads won't convert if shown to the wrong people.

**Audience targeting strategies:**

### Warm audiences (retargeting — start here)
These people already know you. Retargeting is 3-5x cheaper than cold traffic.
- Website visitors (last 30 days)
- Email list (upload to platform as a custom audience)
- Engaged social media followers (people who liked/commented on your posts)
- Video viewers (people who watched 50%+ of your videos)

### Cold audiences (targeting people who don't know you yet)
Use these after warm audiences are performing well:
- **Interest-based:** Target people interested in topics related to your product (e.g., "business automation", "project management tools")
- **Lookalike audiences:** Platform finds people similar to your existing customers (requires 100+ conversions to build)
- **Job title/company (LinkedIn):** Target specific roles (e.g., "VP of Marketing at SaaS companies with 50-200 employees")
- **Keyword-based (Google Search):** Target specific search queries (e.g., "best CRM for small business")

**Audience size guidance:**
- Too narrow (< 50K) = limited reach, high CPM
- Too broad (> 5M) = wasted spend on irrelevant people
- Sweet spot: 100K-1M for cold audiences, 1K-50K for warm audiences

---

## Step 7: Set Your Budget and Bidding Strategy

**Daily budget recommendations:**
- **Testing phase (first 2 weeks):** $20-50/day per ad set
- **Scaling phase (after finding winners):** Increase by 20-30% every 3 days (don't double overnight — it resets the algorithm)

**Bidding strategies:**

| Strategy | When to Use | Pros | Cons |
|---|---|---|---|
| **Lowest cost (auto-bid)** | Starting out, want maximum results | Easy, platform optimizes | Less control over CPA |
| **Target CPA** | You know your target cost per acquisition | Predictable costs | Needs 50+ conversions/week to work |
| **Manual CPC** (Google Search) | You want full control | Precise control | Time-intensive |

**Recommendation:** Start with lowest cost (auto-bid) for the first 2 weeks, then switch to target CPA once you have conversion data.

---

## Step 8: Launch, Monitor, and Optimize

**First 48 hours after launch:**
- Check ads are running (not stuck in review)
- Verify conversions are tracking (test submit a form yourself)
- Monitor spend (are you hitting daily budget limits?)

**Daily check (5 min):**
- Are ads still running? (Sometimes they get paused by the platform for policy issues)
- Is spend on track? (paused ad sets waste budget opportunity)

**Weekly optimization (30 min):**
- Review performance by ad set and ad
- Pause underperformers (CTR < 1% or CPA > 2x your target)
- Increase budget on winners by 20%
- Test new ad variations against winning ads

**Metrics to track:**

| Metric | What It Means | Healthy Benchmark |
|---|---|---|
| **CTR (Click-Through Rate)** | % of people who clicked your ad | 1-3% (higher is better) |
| **CPC (Cost Per Click)** | How much each click costs | Varies by platform (lower is better) |
| **CPL (Cost Per Lead)** | How much each lead costs | Should be < 30% of LTV |
| **ROAS (Return on Ad Spend)** | Revenue / Ad spend | > 3x (for every $1 spent, $3+ revenue) |
| **Conversion rate** | % of clicks that convert | Landing page dependent (2-5% is solid) |

**When to kill an ad:**
- After 500 impressions with CTR < 0.5% (creative doesn't resonate)
- After 100 clicks with 0 conversions (audience or landing page problem)
- CPA consistently 3x+ higher than target (not profitable)

**When to scale an ad:**
- CTR > 2%, CPA at or below target for 7+ days
- Increase budget by 20-30% every 3 days
- Duplicate winning ad sets to new audiences

---

## Step 9: Common Solopreneur Ad Mistakes (Avoid These)

- **Not testing enough creatives.** One ad per campaign = no data. Run 3-5 variations minimum.
- **Targeting too broad.** "Everyone ages 18-65" wastes money. Narrow it down.
- **Optimizing too early.** Don't pause ads after 1 day. Give each ad set 3-5 days and 50+ clicks before making decisions.
- **Sending traffic to your homepage.** Homepages convert terribly. Send to a dedicated landing page with one clear CTA.
- **Ignoring mobile.** 70%+ of social traffic is mobile. Test your landing page on mobile before running ads.
- **Not retargeting.** Most people don't convert on first visit. Retarget website visitors with a different ad/offer.

---

## When Paid Ads Make Sense (and When They Don't)

**Run ads if:**
- Your product/offer converts organically (even at small scale)
- LTV > 3x CAC (so there's margin for ad spend)
- You have budget to test ($500-1,000 minimum)
- You need speed (organic takes months, ads take days)

**Don't run ads if:**
- You haven't validated product-market fit yet (fix the product first)
- Your landing page converts < 2% (fix the page first)
- You can't track conversions (you'll fly blind)
- You're hoping ads will "figure it out" for you (they won't — they amplify what exists)
