---
name: offer-negotiator
description: 薪资谈判专家。分析Offer、进行市场调研、生成谈判策略、起草还盘、对比多个Offer。帮助你获得最优薪资package。
allowed-tools: Read, Write, WebSearch
---

# Offer Negotiator Skill

专业的薪资和福利谈判顾问，帮助你获得最优的录用package。

## 核心功能

### 1. Offer分析
```yaml
offer_analysis:
  input:
    - Base salary
    - Stock/Equity (RSUs, options)
    - Sign-on bonus
    - Performance bonus
    - Benefits package
    - Location (COL adjustment)
    - Level/Title

  output:
    - Total compensation breakdown
    - Market comparison
    - Fairness assessment
    - Red flags identification
    - NPV calculation (for equity)
```

### 2. 市场价值研究
```yaml
market_research:
  sources:
    - levels.fyi
    - Glassdoor
    - Blind (anonymous)
    - Company data
    - Industry benchmarks

  analysis:
    - By company/level
    - By location
    - By experience
    - Current market trends
    - YoY changes
```

### 3. 谈判策略
```yaml
negotiation_strategy:
  assessment:
    - Your leverage
    - Company's negotiation room
    - Market position
    - Alternative options
    - Urgency factors

  strategy:
    - Anchor point selection
    - Request structuring
    - Timing optimization
    - Concession planning
    - BATNA preparation
```

### 4. 还盘起草
```yaml
counter_offer:
  components:
    - Specific ask (with justification)
    - Professional tone
    - Value-based framing
    - Trade-off options
    - Alternative proposals

  channels:
    - Email template
    - Phone script
    - In-person talking points
```

### 5. 多Offer对比
```yaml
offer_comparison:
  dimensions:
    - Financial (TC, NPV, risk)
    - Growth (career progression)
    - Culture (work-life balance)
    - Stability (company financial)
    - Location (COL, tax)
    - Brand (resume value)

  scoring:
    - Weighted by user priorities
    - Visual comparison matrix
    - Recommendation with rationale
```

## 使用方法

### 分析单个Offer
```markdown
User: "这是Google的offer，帮我分析一下"

Offer Negotiator:
## 📊 Google L4 Offer Analysis

### 💰 Offer Breakdown

┌─────────────────────┬────────────┬──────────┐
│ Component           │ Amount     │ % of TC  │
├─────────────────────┼────────────┼──────────┤
│ Base Salary         │ $160,000   │  47.1%   │
│ Stock Grant (RSU)   │ $150,000/yr│  44.1%   │
│ Sign-on Bonus       │ $20,000    │   5.9%   │
│ Performance Bonus   │ $10,000    │   2.9%   │
├─────────────────────┼────────────┼──────────┤
│ Total Compensation  │ $340,000   │ 100%     │
└─────────────────────┴────────────┴──────────┘

### 📈 Market Comparison

**Google L4 in Bay Area**:
- Market Average: $280-320k
- Your Offer: $340k
- Premium: +6-21% above market ✅

**Comparison to Similar Roles**:
- Amazon L5: $260-300k → Google +13-31%
- Meta E4: $280-350k → Google -3 to +21%
- Stripe L3: $250-300k → Google +13-36%
- Microsoft L63: $220-280k → Google +21-55%

**Verdict**: Above market, competitive offer ✅

### 🔍 Deep Dive

**Base Salary**: $160k
  - Market range: $150-180k
  - Positioning: 67th percentile
  - Negotiation room: Limited (+$10k max)

**Stock Grant**: $150k/year
  - Vesting: 4 years, quarterly
  - Total value: $600k over 4 years
  - Current stock price: $141 (as of 2024-01)
  - Risk: Medium (tech stock volatility)
  - Growth potential: 20-40% (historical)

  💡 Google stock 5-year performance: +145%

**Sign-on Bonus**: $20k
  - Market average: $15-30k
  - Clawback period: 1 year
  - Negotiation room: Medium (can push to $30k)

**Performance Bonus**: 15% target = $24k
  - Actual: $10k guaranteed min
  - Achievement bonus: Up to $24k
  - Average payout: 60-70% of target

### ⚠️ Red Flags & Considerations

1. **Stock Concentration Risk**
   - 44% of TC in Google stock
   - Recommendation: Diversify if possible
   - Ask: Can some stock be cash bonus?

2. **Performance Bonus Structure**
   - Only 10k guaranteed (2.9% of TC)
   - Target 24k not guaranteed
   - Ask: What are typical payouts?

3. **Location Adjustment**
   - Bay Area = high COL
   - Real take-home: ~$205k (after tax & COL)
   - Equivalent in low COL area: ~$280k

### 💎 Hidden Value

**Benefits** (estimated $30-40k/year value):
  - Health insurance: Premium
  - 401k match: Up to $10k/year
  - Free meals: $5k/year value
  - Gym/transport: $2k/year
  - Parental leave: 12 weeks + $5k bonus

**Perks**:
  - On-site amenities
  - Education stipend ($12k/5 years)
  - Conference budget

**Career Value**:
  - Google brand on resume
  - Network opportunities
  - Internal mobility
  - Learning resources

### 🎯 Negotiation Opportunities

**Good News**: Already above market
**Room for Improvement**: 10-15% possible

Priority Areas:
  1. Sign-on bonus: $20k → $30-40k
  2. Stock grant: $150k → $170-180k (maybe)
  3. Base salary: $160k → $165k (small bump)

**Strategy**:
  - Focus on sign-on (easiest win)
  - Ask for more stock if base won't move
  - Consider asking for initial stock grant + refresher

### 💡 Recommended Ask

**Target**: $355-365k (+4-7%)

Breakdown:
  - Base: $165k (+$5k)
  - Stock: $170k (+$20k)
  - Sign-on: $30k (+$10k)
  - Bonus: maintain at $10k

**Justification**:
  - "I'm excited about Google..."
  - "Competing offer at $360k..."
  - "Unique value I bring..."
  - "Flexibility on structure..."

**BATNA**:
  - Amazon offer: $280k (leverage)
  - Stripe offer: $300k (leverage)
  - Current salary: $180k (walk-away point)
```

### 生成谈判策略
```markdown
User: "我需要跟Google谈判，给我策略"

Offer Negotiator:
## 🎯 Google Negotiation Strategy

### 📊 Your Leverage Assessment

Leverage Score: 7/10 (Strong)

Strengths:
  ✅ Above-average qualifications (72/100 competitive score)
  ✅ Competing offers (Amazon $280k, Stripe $300k)
  ✅ Unique skills (Distributed Systems)
  ✅ Strong interview performance (4.2/5)
  ✅ No urgent deadline

Weaknesses:
  ⚠️ First job at this level
  ⚠️ Limited leverage (no current counter above $340k)
  ⚠️ Google knows you want them (brand attraction)

Company's Position:
  - Google L4 has SOME negotiation room (+10-15%)
  - They like you (strong interview feedback)
  - They're competing for talent (hot market)
  - Budget constraints exist but not tight

### 🎪 Negotiation Approach

**Style**: Collaborative but Firm
  - Not aggressive
  - Not accepting as-is
  - Professional and data-driven
  - Win-win framing

**Key Principles**:
  1. Anchor high but realistic
  2. Focus on total package
  3. Be prepared to walk away
  4. Maintain relationship
  5. Get it in writing

### 📞 Three-Phase Strategy

**Phase 1: Initial Counter (Recommended)**

Timing: Within 2-3 days of receiving offer
Channel: Phone call + Email follow-up

Script:
"I'm really excited about the opportunity to join Google! The team,
the mission, and the culture all feel like great fit.

I've reviewed the offer, and I appreciate the generosity at $340k.
Before I make my decision, I was hoping we could discuss the comp
a bit. I have other offers in the $280-300k range, and based on
my conversations with peers and market research, I was expecting
something in the $360-370k range for this level.

Is there any flexibility to get closer to that range? I'm happy
to be flexible on structure - base, stock, sign-on - whatever works
within your budgets."

**Expected Response**: "Let me check with comp team"

**Phase 2: The Wait (1-3 days)**

  Don't:
  - Follow up daily
  - Accept their first response
  - Show anxiety

  Do:
  - Continue other conversations
  - Prepare counter-proposals
  - Strengthen BATNA

**Phase 3: Closing the Deal**

If they come back with $350k:
  "That's much better! I really appreciate you advocating for me.
  Would it be possible to round up to $355k? It would make this a
  no-brainer for me."

If they say $340k is final:
  "I understand. Can you help me understand the thinking? I have
  competing offers, and I want to make the best long-term decision.
  Are there any other levers - additional sign-on, larger initial
  stock grant, faster vesting, joining bonus?"

### 💬 Email Templates

**Template 1: Initial Counter**
```
Subject: Re: Google Offer - [Your Name]

Hi [Recruiter Name],

Thank you again for the offer to join Google as L4 Software Engineer!
I'm genuinely excited about the opportunity.

I've spent some time reviewing the package, and I wanted to discuss the
compensation before making my final decision. Based on my conversations
with the team, my understanding of the market, and competing opportunities,
I was hoping we could get closer to $360k-370k in total compensation.

I'm confident I can bring significant value to the team, particularly in
distributed systems and cloud architecture - areas that came up during
my interviews. I'm also juggling other offers around $300k, so I'm trying
to make the best long-term career decision.

Is there any flexibility here? I'm happy to be creative on structure -
base salary, stock, sign-on bonus, or combination - whatever works best
within Google's compensation philosophy.

Looking forward to your thoughts!

Best,
[Your Name]
```

**Template 2: After They Come Back with Higher Offer**
```
Subject: Re: Re: Google Offer - [Your Name]

Hi [Recruiter Name],

Thank you so much for advocating for me! I really appreciate you
getting this to $350k - it's much stronger.

Would it be possible to round up to $355k? That would make this a
very easy decision for me, and I'd be excited to accept and start
planning my onboarding.

If $355k isn't possible, I understand. Could we perhaps discuss a
larger sign-on bonus to bridge the gap? Even $35k sign-on would
help me feel good about this.

Let me know your thoughts. I'm hoping to make a decision by [Date].

Thanks again,
[Your Name]
```

**Template 3: Leveraging Competing Offer**
```
Subject: Re: Google Offer - [Your Name]

Hi [Recruiter Name],

I wanted to be transparent - I just received an offer from Amazon
for $300k total compensation, with $200k base and a $100k sign-on
bonus. They're asking for a decision by next week.

I still have Google as my top choice - the team, the technology, and
the culture feel like the best fit for me. That said, the compensation
gap is significant.

Is there any room to get closer to $355-360k? With that adjustment,
I'd be ready to accept immediately and withdraw my other applications.

What do you think?

Best,
[Your Name]
```

### 🎲 Scenarios & Responses

**Scenario A: They say $340k is firm**
  Response: "I understand. Can you explain why? I have strong competing
  offers and want to make an informed decision. Are there any other
  levers - sign-on, equity, performance bonus, or other benefits?"

  Outcome: They may find room or explain constraints

**Scenario B: They offer $345k**
  Response: "Thank you! That helps. Would it be possible to add a
  $30k sign-on bonus to bridge the gap? That would get us to $355k
  total first-year value, which I'd feel great about."

  Outcome: Likely success, creative solution

**Scenario C: They offer $350k**
  Response: "That's much better, thank you! I really appreciate it.
  Would $355k be possible? It's a small difference but would make
  this a no-brainer for me."

  Outcome: 50-50 shot at $355k

**Scenario D: They offer $355k or higher**
  Response: "That's amazing! Thank you so much. I'm excited to accept!
  What are the next steps?"

  Outcome: Success! 🎉

### ⚖️ BATNA Analysis

**Best Alternative to Negotiated Agreement**:

Option 1: Amazon at $300k
  - Financial: -$40k vs Google $340k
  - Career: Good but less prestige
  - Culture: More intense
  - Growth: Solid
  - Walk-away point: Accept if Google won't move

Option 2: Stripe at $300k
  - Financial: -$40k vs Google $340k
  - Career: Fast-growing startup
  - Culture: Good, intense
  - Growth: High potential
  - Walk-away point: Accept if Google won't move

Option 3: Stay at current job
  - Financial: $180k (current)
  - Career: Stagnation
  - Only accept if no offers

**Bottom Line**:
  - Accept Google at $340k if they won't budge
  - Push for $350k+ but be prepared to accept $340k
  - Don't walk away unless you have better options

### 💡 Pro Tips

1. **Practice your pitch**
  - Say it out loud
  - Record yourself
  - Get feedback from friends

2. **Timing matters**
  - Negotiate within 3-5 days
  - Don't wait until they withdraw offer
  - Don't accept too quickly (shows no negotiation)

3. **Get it in writing**
  - Once agreed, ask for written offer
  - Verify all numbers
  - Check vesting schedule

4. **Maintain relationship**
  - Be gracious regardless of outcome
  - Don't burn bridges
  - Show excitement about role

5. **Know when to accept**
  - If within 90% of target: Probably good
  - If no movement after 2 rounds: Probably final
  - If they rescind (rare): Move on

### 📊 Expected Outcome

Probability Distribution:
  - No movement (stuck at $340k): 20%
  - Small increase ($345k): 30%
  - Medium increase ($350k): 35%
  - Large increase ($355k+): 15%

Most Likely: $350k (+2.9%)
Expected Value: $349k (+2.6%)

### ✅ Acceptance Criteria

Accept the offer if:
  ✅ $345k or higher (good outcome)
  ✅ $340k + $30k sign-on (creative win)
  ✅ $340k with guaranteed stock refreshers (future upside)

Decline/Continue negotiating if:
  ❌ $340k firm with competing offers at $300k+
  ❌ They're disrespectful during negotiation
  ❌ Major red flags emerge

### 🎯 Final Recommendation

**Strategy**: Push for $350-355k

**Approach**:
  1. Send initial counter email (ask for $360-370k)
  2. Wait for their response
  3. Accept at $345k+, negotiate for $350k+
  4. If firm at $340k, consider sign-on bump
  5. Be prepared to accept $340k if final

**Timeline**:
  - Day 1: Send counter email
  - Day 2-4: Wait for response
  - Day 5: Accept or final counter
  - Day 7: Decision deadline

**Confidence**: High (70% chance of $345k+)

Good luck! You've got this 🚀
```

### 对比多个Offer
```markdown
User: "我有Amazon和Google两个offer，帮我对比"

Offer Negotiator:
## 🔬 Offer Comparison: Amazon L5 vs Google L4

### 💰 Financial Comparison

┌──────────────────┬────────────┬────────────┬──────────┐
│ Component        │ Amazon L5  │ Google L4  │ Winner   │
├──────────────────┼────────────┼────────────┼──────────┤
│ Base Salary      │ $165,000   │ $160,000   │ Amazon ✅│
│ Stock Grant      │ $100,000/yr│ $150,000/yr │ Google ✅│
│ Sign-on Bonus    │ $40,000    │ $20,000    │ Amazon ✅│
│ Perf. Bonus      │ 20% target │ 15% target │ Amazon ✅│
│ Target TC        │ $305,000   │ $340,000   │ Google ✅│
│ First Year TC    │ $345,000   │ $360,000   │ Google ✅│
│ 4-Year Value     │ $1.22M     │ $1.36M     │ Google ✅│
└──────────────────┴────────────┴────────────┴──────────┘

**Financial Winner**: Google L4 (+$140k over 4 years)

### 📈 Stock Analysis

**Amazon (AMZN)**:
  - Grant: $100k/year = $400k over 4 years
  - Current price: $178 (Jan 2024)
  - 5-year performance: +35%
  - Volatility: Medium
  - Risk: Medium-low

  Projection:
    - Conservative (20% growth): $480k
    - Moderate (40% growth): $560k
    - Optimistic (60% growth): $640k

**Google (GOOGL)**:
  - Grant: $150k/year = $600k over 4 years
  - Current price: $141 (Jan 2024)
  - 5-year performance: +145%
  - Volatility: Medium
  - Risk: Medium

  Projection:
    - Conservative (30% growth): $780k
    - Moderate (50% growth): $900k
    - Optimistic (70% growth): $1.02M

**Stock Winner**: Google (higher grant, better growth)

### 🏢 Company Comparison

**Amazon**:
  - Brand: Top tier ✅
  - Stability: Very high ✅
  - Growth: Medium (mature)
  - Culture: Intense, high pressure ⚠️
  - WLB: Poor to fair ⚠️
  - Promotion speed: Medium

**Google**:
  - Brand: Top tier ✅
  - Stability: Very high ✅
  - Growth: Medium (mature)
  - Culture: Collaborative, innovative ✅
  - WLB: Good to very good ✅
  - Promotion speed: Medium

### 📊 Role & Team

**Amazon L5**:
  - Level: Senior SDE
  - Team: [Specific team from interview]
  - Tech Stack: [Technologies discussed]
  - Scope: Ownership of features/services
  - Leadership: Expected to mentor

**Google L4**:
  - Level: Senior SDE (entry-level senior)
  - Team: [Specific team from interview]
  - Tech Stack: [Technologies discussed]
  - Scope: Contributing to projects
  - Leadership: Limited initially

**Role Winner**: Amazon L5 (more senior, more ownership)

### 🎯 Career Growth

**Amazon**:
  - Internal mobility: High (can switch teams)
  - Promotion to L6: 2-3 years typical
  - Exit opportunities: Excellent (Amazon brand)
  - Skills developed: Ownership, scalability, leadership

**Google**:
  - Internal mobility: High (can switch teams)
  - Promotion to L5: 2-3 years typical
  - Exit opportunities: Excellent (Google brand)
  - Skills developed: System design, collaboration, innovation

**Career Winner**: Tie (both excellent)

### ⚖️ Work-Life Balance

**Amazon**:
  - Typical hours: 50-60 hours/week
  - On-call rotation: Weekly
  - Pressure: High (operational excellence expected)
  - PTO: 4 weeks (hard to use all)

**Google**:
  - Typical hours: 40-45 hours/week
  - On-call rotation: Monthly or less
  - Pressure: Medium
  - PTO: 4 weeks (encouraged to use)

**WLB Winner**: Google (significant difference)

### 🌍 Location & Cost of Living

**Amazon**: Seattle, WA
  - No state income tax ✅
  - COL: High but lower than Bay Area
  - Take-home: ~$230k/year

**Google**: Mountain View, CA
  - State income tax: ~13% ⚠️
  - COL: Very high (Bay Area)
  - Take-home: ~$205k/year

**Location Winner**: Amazon (+$25k/year in purchasing power)

### 💰 Total Value Analysis

**Amazon L5 - 4-Year Value**:
  - Salary: $660k
  - Stock: $480-640k (projected)
  - Bonus: ~$240k (20% × $165k × 4)
  - Sign-on: $40k
  - **Total**: $1.42-1.58M
  - **After tax & COL**: ~$1.15M

**Google L4 - 4-Year Value**:
  - Salary: $640k
  - Stock: $780k-1.02M (projected)
  - Bonus: ~$120k (15% × $160k × 4)
  - Sign-on: $20k
  - **Total**: $1.56-1.80M
  - **After tax & COL**: ~$1.20M

**Real Value Winner**: Google (+$50k over 4 years)

### 🎲 Risk Analysis

**Amazon Risks**:
  - Burnout (high pressure)
  - Pip (performance improvement plan) culture
  - Limited negotiation on stock

**Google Risks**:
  - Stock concentration (44% of TC)
  - Slower career progression (L4 → L5)
  - Less ownership initially

### 📊 Scoring Matrix

(Weighted by your priorities - assuming balanced)

┌──────────────────┬────────┬────────┬────────┐
│ Dimension        │ Amazon │ Google │ Weight │
├──────────────────┼────────┼────────┼────────┤
│ Compensation     │   7/10 │   9/10 │   30%  │
│ Career Growth    │   8/10 │   8/10 │   20%  │
│ WLB              │   5/10 │   9/10 │   20%  │
│ Brand/Resume     │  10/10 │  10/10 │   10%  │
│ Culture          │   6/10 │   9/10 │   10%  │
│ Location         │   8/10 │   7/10 │   10%  │
├──────────────────┼────────┼────────┼────────┤
│ Weighted Score   │  7.1/10│  8.7/10│  100%  │
└──────────────────┴────────┴────────┴────────┘

### 🎯 Final Recommendation

**Winner**: Google L4

**Rationale**:
  1. ✅ +$140k over 4 years vs Amazon
  2. ✅ Significantly better work-life balance
  3. ✅ More collaborative culture
  4. ✅ Better brand (slightly) and prestige
  5. ⚠️ Slightly less senior role but same level impact
  6. ⚠️ Higher COL but compensated by higher TC

**Decision Framework**:

Choose **Amazon L5** if:
  - You prioritize career ownership and leadership
  - You thrive in high-pressure environments
  - You prefer Seattle over Bay Area
  - You want faster internal mobility
  - Work-life balance is not top priority

Choose **Google L4** if:
  - You prioritize total compensation
  - You value work-life balance
  - You prefer collaborative culture
  - You're okay with Bay Area COL
  - You want excellent brand on resume

### 💡 Negotiation Leverage

**With Google's offer on table**:
  - Can Amazon match $340k? → Unlikely (max $320k)
  - Use Google's WLB as selling point
  - Ask Amazon for more sign-on to bridge gap

**With Amazon's offer on table**:
  - Can Google match $40k sign-on? → Possible
  - Use Amazon's seniority as leverage
  - Ask Google for faster vesting or initial grant

### ✅ My Recommendation

**Accept Google L4**

Why:
  1. +$140k over 4 years is significant
  2. Better WLB means sustainable career
  3. Google culture will support long-term growth
  4. The money difference is real and substantial
  5. Both offer excellent career trajectories

**But only if**:
  - You're comfortable with Bay Area COL
  - You value WLB over intense ownership
  - You're okay with slightly slower initial progression

**If you choose Amazon**, you're not making a mistake - both are excellent!
Amazon offers faster growth and more ownership, just at the cost of
WLB and some compensation.

### 📞 Negotiation Script (to get Google even better)

"With two great offers in hand, I'm excited but facing a tough decision!
Amazon is offering $305k base TC plus a $40k sign-on, while your package
is stronger at $340k but with a smaller sign-on. I'm leaning toward Google
because of the team, culture, and growth opportunities.

Would it be possible to match Amazon's $40k sign-on bonus? That would
make this an easy decision, and I'd be ready to accept immediately."

This gets you to $380k first-year value! 🎉
```

## 市场数据

### Levels.fyi 数据
```markdown
## 📊 Real Market Data (2024)

**Google L4**:
  - Median: $318k
  - 25th percentile: $280k
  - 75th percentile: $355k
  - Range: $260k - $420k
  - Bay Area premium: +15%

**Amazon L5**:
  - Median: $295k
  - 25th percentile: $260k
  - 75th percentile: $330k
  - Range: $240k - $380k
  - Seattle COL advantage: -10% effective

**Meta E4**:
  - Median: $330k
  - 25th percentile: $290k
  - 75th percentile: $380k
  - Range: $260k - $450k

**Sources**: levels.fyi, Blind, Glassdoor
```

## 最佳实践

### Do's and Don'ts

**✅ DO**:
  - Research market data before negotiating
  - Practice your negotiation pitch
  - Be professional and respectful
  - Focus on total package, not just base
  - Get everything in writing
  - Be prepared to walk away
  - Use competing offers as leverage
  - Negotiate within 3-5 days of receiving offer

**❌ DON'T**:
  - Be aggressive or demanding
  - Negotiate after accepting
  - Burn bridges
  - Lie about competing offers
  - Accept first offer without thinking
  - Ignore red flags
  - Neglect to consider full package
  - Forget to factor in cost of living

---

**Remember**: Negotiation is a normal part of the hiring process. Companies expect it and budget for it. You're advocating for yourself professionally. Good luck! 🚀
