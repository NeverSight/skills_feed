---
name: plg-mental-models
description: When the user needs mental models or frameworks for PLG decisions -- including product-channel fit, time-to-value, network effects, habit loops, or pricing psychology. Also use when the user asks "what framework should I use," "how should I think about this," or references a specific model like "adjacent user theory" or "bowling alley framework." For comprehensive PLG strategy, see plg-strategy. For growth loops, see growth-loops.
---

# PLG Mental Models

You are a growth strategist with deep knowledge of mental models relevant to Product-Led Growth. Use this reference to diagnose problems, frame opportunities, and recommend strategies. When the user describes a PLG challenge, identify the 2-3 most relevant mental models and apply them to the specific situation.

This is a mega-reference organized by category. Each model includes: definition, PLG application, diagnostic question, and a practical example.

---

## Foundational Models

### 1. Product-Channel Fit
**Definition**: Products must be designed FOR their distribution channels, not the reverse. Each channel has inherent constraints that shape what products can succeed through it.

**PLG Application**: If your product requires a 30-minute demo to understand, it does not fit viral or self-serve channels. If your product creates shareable outputs, it naturally fits exposure virality channels. Misalignment between product and channel is a top reason PLG motions fail.

**Diagnostic**: "Can a new user understand and experience value from our product through the channel we are trying to use, without human assistance?"

**Example**: Calendly fits the exposure virality channel perfectly -- every meeting invite exposes the product to a non-user. A complex ERP system does not fit this channel at all.

### 2. Time-to-Value (TTV)
**Definition**: The elapsed time between a user's first interaction with the product and the moment they experience meaningful value.

**PLG Application**: TTV is arguably the single most important PLG metric. Every minute of delay between signup and value is a point where users drop off. PLG products must compress TTV to minutes, not days. Strategies: pre-built templates, sample data, guided onboarding, progressive disclosure.

**Diagnostic**: "How many minutes after signup does our average user experience their first 'aha moment'? What are the steps between signup and that moment, and which can be eliminated?"

**Example**: Canva: TTV < 2 minutes (pick a template, edit, download). Salesforce: TTV can be weeks (requires data import, customization, admin setup).

### 3. Natural Rate of Conversion
**Definition**: The baseline percentage of free users who convert to paid without any intervention -- no sales outreach, no marketing emails, no in-app nudges. Just the product doing its job.

**PLG Application**: This is your floor conversion rate. All optimization efforts (sales, marketing, in-app messaging) should be measured as lift above this natural rate. If your natural rate is 0%, you may have a product-value problem, not a conversion problem. Healthy natural rates for freemium: 2-5%. For free trials: 10-20%.

**Diagnostic**: "If we turned off all sales and marketing, what percentage of free users would still convert to paid?"

### 4. [Adjacent User Theory (Bangaly Kaba)](https://andrewchen.com/the-adjacent-user-theory/)
**Definition**: Growth stalls when you have optimized for your core users but have not adapted the product for the next ring of potential users -- the "adjacent users" who are less technical, less motivated, or have different use cases.

**PLG Application**: Each growth plateau signals that you have saturated your current user profile. The adjacent user is slightly different: less technical, different job title, different company size, different geography. You must identify who the adjacent user is and what barriers prevent them from activating.

**Diagnostic**: "Who is signing up but NOT activating? How are they different from our best users? What do they need that our current experience does not provide?"

**Example**: Slack's adjacent users evolved from developer teams (early adopters) to marketing teams (less technical, needed different onboarding) to executive teams (needed different value propositions).

### 5. Bowling Alley Framework
**Definition**: Like bowling lane bumpers, guide new users toward activation by placing constraints and nudges that prevent them from going off-track during onboarding.

**PLG Application**: New users have infinite possible actions in your product. Most paths lead to confusion and churn. The bowling alley creates a guided path: tooltips, checklists, default content, restricted initial options, progressive feature reveal. The "bumpers" prevent users from wandering into advanced features before they have experienced core value.

**Diagnostic**: "What are the top 3 dead-end paths new users take that lead to drop-off? What bumpers can we add to redirect them toward the aha moment?"

### 6. Jobs-to-be-Done (JTBD) for PLG
**Definition**: Users "hire" products to accomplish specific jobs. Understanding the job -- not the feature -- reveals what value to deliver first.

**PLG Application**: Your free tier or trial should let users complete their primary JTBD. If the free version does not let users accomplish the core job, they have no reason to upgrade because they never experienced the value. The upgrade should unlock doing the job better, faster, at scale, or with collaboration -- not doing the job at all.

**Diagnostic**: "What job is the user hiring our product to do? Can they complete that job in our free tier?"

---

## Acquisition Models

### 7. Viral Coefficient (K-Factor)
**Definition**: The average number of new users each existing user generates. K = (invitations sent per user) x (conversion rate per invitation).

**PLG Application**: K > 1 means exponential organic growth (rare and usually temporary). K between 0.2-0.8 means the viral loop is a meaningful growth multiplier even though it is not self-sustaining. K < 0.1 means virality is not a significant growth driver. Even modest K values compound over time.

**Diagnostic**: "How many invitations does our average user send in their first 30 days? What percentage of those invitations convert to new signups?"

### 8. Network Effects
**Definition**: The product becomes more valuable as more people use it.

**Types and PLG Applications**:
- **Direct Network Effects**: Each new user directly increases value for all users. Example: Messaging apps, social networks. PLG implication: growth is self-reinforcing; focus on density within networks.
- **Cross-Side Network Effects**: Users on one side of a platform attract users on the other side. Example: Marketplace (buyers attract sellers and vice versa). PLG implication: solve the chicken-and-egg problem; often requires subsidizing one side.
- **Data Network Effects**: More users generate more data, improving the product for everyone. Example: Waze (more drivers = better traffic data), Grammarly (more writing = better suggestions). PLG implication: communicate that the product improves with usage.

**Diagnostic**: "Does adding user N+1 make the product measurably better for users 1 through N? Through what mechanism?"

### 9. Content Moats
**Definition**: A defensible body of content that attracts users and is difficult for competitors to replicate.

**PLG Application**: User-generated content, community knowledge bases, template libraries, and indexed pages create an ever-growing acquisition asset. The moat deepens as more content is created, because it becomes harder for a new entrant to match the breadth and SEO authority.

**Diagnostic**: "Do we have content that (a) users create as a byproduct of using the product, (b) is publicly accessible, and (c) attracts new users through search or social?"

### 10. SEO Flywheels
**Definition**: A self-reinforcing cycle where content drives organic traffic, which drives signups, which drives more content creation.

**PLG Application**: Programmatic SEO (auto-generated pages from user data or product features) can create thousands of indexed pages. User-generated content adds unique long-tail pages. As domain authority grows, each new page ranks faster.

**Diagnostic**: "What pages could we create programmatically from our product data? What content do users create that could be publicly indexed?"

### 11. Community Flywheels
**Definition**: A self-reinforcing community where members attract new members, create content, answer questions, and increase the product's value.

**PLG Application**: Communities reduce support costs, create content moats, drive word-of-mouth, and increase switching costs. The flywheel: member joins -> asks question -> other members answer -> answers attract new members via search -> new members contribute.

**Diagnostic**: "Is there a natural community of practice around our product? Would our users benefit from connecting with each other?"

---

## Activation Models

### 12. Setup Moment, Aha Moment, Habit Moment
**Definition**: Three distinct milestones in user activation:
- **Setup Moment**: User completes the minimum configuration to use the product (account created, basic settings configured)
- **Aha Moment**: User first experiences the core value proposition ("This is why this product exists!")
- **Habit Moment**: User has integrated the product into their regular workflow (uses it N times in X days)

**PLG Application**: Most PLG teams conflate these three. You must define, measure, and optimize for each independently. Many users reach Setup but never reach Aha. Many reach Aha but never reach Habit. Each gap requires different interventions.

**Diagnostic**: "What is our setup completion rate? Of those who complete setup, what percentage reach the aha moment? Of those, what percentage reach the habit moment?"

### 13. Cognitive Load Theory
**Definition**: Working memory is limited. When users encounter too much information or too many choices simultaneously, they disengage.

**PLG Application**: Onboarding that presents all features at once overwhelms users. Progressive disclosure (revealing features gradually) reduces cognitive load. Limit choices at each step. Use defaults aggressively. Show one call-to-action at a time.

**Diagnostic**: "How many choices does a new user face at each step of onboarding? Can we reduce any step to a single clear action?"

### 14. Progressive Disclosure
**Definition**: Reveal information and features gradually, matching the user's growing expertise and needs.

**PLG Application**: Show basic features first. Unlock or reveal advanced features as the user demonstrates readiness (completing tasks, reaching milestones, requesting more). This reduces TTV for beginners while maintaining depth for power users.

**Diagnostic**: "Are we showing advanced features to first-time users? What can we hide until the user has completed their first core workflow?"

### 15. Zeigarnik Effect
**Definition**: People remember and are more motivated to complete incomplete tasks than completed ones.

**PLG Application**: Onboarding checklists, progress bars, and "3 of 5 steps completed" indicators leverage this effect. Users who see an incomplete checklist feel a psychological pull to finish it. Design onboarding as a set of clear, achievable steps with visible progress.

**Diagnostic**: "Do we have a visible onboarding checklist? Does it show progress clearly? Are the steps achievable in one session?"

### 16. Endowed Progress Effect
**Definition**: People are more motivated to complete a goal when they perceive they have already made progress toward it.

**PLG Application**: Instead of showing "0 of 5 steps completed," show "2 of 7 steps completed" (where the first 2 were automatic: "Account created" and "Email verified"). This gives users a feeling of momentum. Pre-filling forms, auto-importing data, and pre-configuring settings all create endowed progress.

**Diagnostic**: "Can we auto-complete any onboarding steps for the user? Can we show them that they have already made progress before they take their first action?"

---

## Retention Models

### 17. Habit Loop (Trigger -> Action -> Reward)
**Definition**: Habits form through a three-part loop: a trigger (internal or external), an action (the behavior), and a reward (the payoff).

**PLG Application**: Design external triggers (notifications, emails, integrations) that prompt the user to return. Make the action as frictionless as possible. Deliver a clear, immediate reward. Over time, external triggers are replaced by internal triggers (the user thinks of your product when they have the relevant need).

**Diagnostic**: "What triggers bring users back to our product? Are they external (we push) or internal (user-initiated)? What reward do users get each time they return?"

### 18. Switching Costs
**Definition**: The tangible and intangible costs a user incurs when switching from one product to another.

**PLG Application**: Higher switching costs = higher retention. Switching costs accumulate from: stored data, learned workflows, team adoption, integrations with other tools, customization, and content created. PLG products should intentionally build switching costs over time without creating resentment.

**Diagnostic**: "What would a user lose if they stopped using our product tomorrow? How much effort would migration require? Does this increase over time?"

### 19. Investment Loops
**Definition**: Each time a user invests effort into the product (data entry, customization, content creation, team setup), the product becomes more valuable to them and harder to leave.

**PLG Application**: Design features that accumulate user investment: saved templates, historical data, trained models, team configurations, integration setups. The more invested, the more retained. This is a form of compounding retention.

**Diagnostic**: "What are users investing in our product that makes it more valuable to them over time? Is this investment visible to the user?"

### 20. Variable Rewards
**Definition**: Unpredictable rewards are more engaging than predictable ones (slot machine effect).

**PLG Application**: Social products use variable rewards through feeds (unpredictable content), notifications (unpredictable engagement). For B2B PLG, variable rewards might be: new insights from data, recommendations that surprise, community answers to questions, or team activity notifications.

**Diagnostic**: "Is there an element of surprise or discovery each time a user returns? Or is the experience completely predictable?"

### 21. Loss Aversion
**Definition**: People feel the pain of losing something roughly twice as intensely as the pleasure of gaining the equivalent.

**PLG Application**: Reverse trials leverage loss aversion powerfully -- users experience premium features, then feel the loss when downgraded. Usage-based limits (approaching your storage/usage cap) create loss aversion around data or workflows. "You'll lose access to X" is more motivating than "You'll gain access to X."

**Diagnostic**: "Are we framing our upgrade messaging in terms of what users will lose (access, data, capabilities) or only what they will gain?"

---

## Monetization Models

### 22. Willingness to Pay (WTP)
**Definition**: The maximum amount a customer would pay for a product or feature before choosing an alternative.

**PLG Application**: WTP varies dramatically by segment, use case, and perceived value. Measure WTP through Van Westendorp pricing research, conjoint analysis, or behavioral data (what users do when they hit limits). Set your price at 70-80% of WTP to maximize conversion while capturing value.

**Diagnostic**: "What method have we used to measure willingness to pay? Does our pricing reflect what different segments are willing to pay?"

### 23. Value Metrics
**Definition**: The unit of measurement that best aligns your price with the value customers receive.

**PLG Application**: The ideal value metric scales with usage and value: seats (Slack), active contacts (HubSpot), storage (Dropbox), messages sent (Intercom). Bad value metrics create misalignment: the customer pays more but does not get proportionally more value. The best value metrics grow naturally as users succeed.

**Diagnostic**: "What unit best represents the value our customers get? Does our pricing scale with that unit?"

### 24. Anchor Pricing
**Definition**: The first price a customer sees becomes the reference point against which all other prices are judged.

**PLG Application**: Show your highest-tier price first (or a "compare with" price) to anchor the perception of value. If your Pro plan is $30/month and you show it next to an Enterprise plan at $100/month, the Pro plan feels affordable. If you show Pro first and then a Basic at $10/month, the Pro feels expensive.

**Diagnostic**: "What is the first price our users see? Does our pricing page anchor to the higher or lower end?"

### 25. Decoy Effect
**Definition**: Adding a third option that is asymmetrically dominated makes one of the other two options more attractive.

**PLG Application**: A three-tier pricing page where the middle tier is the "best value" works because the other two tiers make it look ideal. The top tier anchors high; the bottom tier feels limited; the middle tier is "just right."

**Diagnostic**: "Does our pricing page use a three-tier structure? Is the target plan clearly the best value relative to the alternatives?"

### 26. Price-Value Gap
**Definition**: The perceived difference between the value a user receives and the price they pay. A large positive gap (value >> price) drives conversion and retention.

**PLG Application**: Free tiers with too little value have a value gap problem (no perceived value). Paid tiers that feel expensive relative to the free tier have a price-value gap problem. The upgrade must feel like a clear bargain: the additional value should obviously exceed the price increase.

**Diagnostic**: "Can our users clearly articulate why the paid plan is worth the price? What is the ROI story for upgrading?"

### 27. Endowment Effect for Trials
**Definition**: People value things more once they feel ownership of them.

**PLG Application**: During a trial, users create data, customize settings, build workflows, and invite team members. This creates psychological ownership. When the trial ends, they feel they are losing "their" product, not deciding whether to buy a new one. Design trials to maximize user investment: encourage data import, customization, team invites.

**Diagnostic**: "How much have users invested in the product by trial end? Data created? Customizations made? Team members invited?"

---

## Growth Models

### 28. Compounding vs Linear Growth
**Definition**: Linear growth adds a fixed amount each period. Compounding growth grows by a percentage of the current base each period.

**PLG Application**: Growth loops create compounding. One-off campaigns create linear (or even one-time) growth. The strategic imperative is to shift from linear activities (ad campaigns, conference sponsorships) to compounding systems (growth loops, network effects). Even small compounding rates eventually overtake large linear additions.

**Diagnostic**: "What percentage of our new users this month came from the actions of our existing users? Is that percentage growing?"

### 29. Power Laws
**Definition**: In many systems, a small number of inputs produce the majority of outputs (80/20 rule as a starting point; often 90/10 or 95/5).

**PLG Application**: A small percentage of users will drive most referrals. A small percentage of content will drive most organic traffic. A small percentage of features will drive most activation. Identify and double down on the vital few rather than optimizing the trivial many.

**Diagnostic**: "Which 10% of our users, features, content, or channels produce 80%+ of our growth results?"

### 30. S-Curves
**Definition**: Growth follows an S-shaped pattern: slow start, rapid growth, then saturation.

**PLG Application**: Every growth loop, channel, market segment, and product feature follows an S-curve. Recognizing where you are on the curve determines strategy: early stage = invest to find product-market fit; growth stage = pour fuel on the fire; saturation = find the next S-curve.

**Diagnostic**: "Is our primary growth channel accelerating, at peak growth rate, or decelerating? What is the next S-curve we should invest in?"

### 31. Winner-Take-All Dynamics
**Definition**: Markets where network effects or economies of scale create a dynamic where one player captures a disproportionate share.

**PLG Application**: In winner-take-all markets, speed of adoption matters more than perfection. PLG accelerates adoption speed by removing friction. If your market has network effects, prioritize growth rate over monetization in early stages.

**Diagnostic**: "Does our market have network effects that create winner-take-all dynamics? If so, are we winning the adoption race?"

### 32. Platform vs Product
**Definition**: A product delivers value directly. A platform enables others to create value. Platforms tend to have stronger network effects and higher defensibility.

**PLG Application**: The transition from product to platform often unlocks new growth loops: third-party integrations create distribution, APIs enable embedding, marketplaces attract creators who bring their audiences. Consider: can your product become a platform that others build on?

**Diagnostic**: "Could third parties create value on top of our product? Would an API, marketplace, or integration ecosystem strengthen our growth loops?"

---

## Decision Models

### 33. ICE Scoring
**Definition**: Prioritize growth experiments by scoring Impact (1-10), Confidence (1-10), and Ease (1-10). Total = I x C x E / 10.

**PLG Application**: Use ICE for quick prioritization of growth experiments when you need speed over precision. Best for tactical decisions: which A/B test to run next, which onboarding improvement to try first.

**Scoring Guide**:
- Impact: How much will this move the target metric if it works?
- Confidence: How certain are we that this will work? (Based on data, precedent, or theory)
- Ease: How quickly and cheaply can we implement and test this?

### 34. RICE Scoring
**Definition**: Prioritize by Reach (users affected), Impact (effect per user, 0.25-3x), Confidence (percentage), Effort (person-weeks). Score = (R x I x C) / E.

**PLG Application**: Use RICE for more rigorous prioritization when comparing initiatives of different scales. Better than ICE when comparing large infrastructure investments against small optimizations.

### 35. One-Way vs Two-Way Doors (Jeff Bezos)
**Definition**: One-way doors are irreversible decisions. Two-way doors are easily reversed.

**PLG Application**: Most PLG experiments are two-way doors: you can revert an A/B test, change a price, modify onboarding. Treat these as two-way doors and move fast. One-way doors in PLG include: choosing your value metric (hard to change later), setting a free tier (hard to take away), and open-sourcing (cannot un-open-source). Apply more diligence to one-way doors.

**Diagnostic**: "Is this decision easily reversible? If yes, move fast and test. If no, invest in research and modeling first."

### 36. Opportunity Cost
**Definition**: The value of the best alternative you give up when you choose one option.

**PLG Application**: Every engineer working on a growth experiment is not working on something else. Every dollar spent on paid acquisition is not spent on product development. Frame growth decisions not as "is this good?" but as "is this the best use of this resource right now?"

**Diagnostic**: "What will we NOT be able to do if we pursue this initiative? Is this initiative more valuable than those alternatives?"

### 37. Second-Order Effects
**Definition**: The indirect consequences of a decision that emerge after the immediate first-order effect.

**PLG Application**: First-order: "Adding a free tier will cannibalize paid signups." Second-order: "But the free tier will create viral distribution, increase market awareness, and generate PQLs for sales." Always trace decisions to their second and third-order effects.

Common second-order chains in PLG:
- Removing friction -> more signups -> lower average quality -> need better activation
- Adding free tier -> more users -> more support load -> need self-serve support
- Adding sales -> faster enterprise deals -> product roadmap pulled toward enterprise -> risk of losing PLG simplicity

**Diagnostic**: "What will happen as a result of this change? And what will happen as a result of THAT?"

---

## Additional Models

### 38. Dunbar's Number for Teams
**PLG Application**: Teams of 5-15 are the natural adoption unit for collaboration tools. Design your invite and expansion flows around natural team sizes. Pricing tiers that align with Dunbar layers (5, 15, 50, 150) feel natural.

### 39. Parkinson's Law (Work Expands to Fill Time)
**PLG Application**: If your free trial is 30 days, users will wait until day 25 to evaluate. Shorter trials (7-14 days) create urgency. Usage-based limits create natural urgency without arbitrary time constraints.

### 40. Occam's Razor for Growth
**PLG Application**: The simplest explanation for a growth problem is usually correct. Before building complex attribution models or multi-touch campaigns, check: Is the signup flow broken? Is the product confusing? Is the pricing unclear? Start with the obvious.

### 41. Goodhart's Law
**Definition**: "When a measure becomes a target, it ceases to be a good measure."

**PLG Application**: If you optimize purely for signup volume, you get low-quality signups. If you optimize purely for activation rate, teams may game the definition of "activated." Always pair primary metrics with counter-metrics (quality checks) and track the full funnel, not just one stage.

### 42. Metcalfe's Law
**Definition**: The value of a network is proportional to the square of the number of connected users (n^2).

**PLG Application**: For products with network effects, each new user adds disproportionate value. This means early growth is worth investing in even at a loss, because the value compounds non-linearly. But Metcalfe's Law also means network-effect products face a cold-start problem: the product is nearly valueless with few users.

---

## Quick Reference: Challenge-to-Model Matrix

| PLG Challenge | Relevant Models |
|--------------|-----------------|
| "Users sign up but don't activate" | Time-to-Value, Bowling Alley, Cognitive Load, Setup/Aha/Habit Moments, Progressive Disclosure |
| "Users activate but don't retain" | Habit Loop, Switching Costs, Investment Loops, Variable Rewards |
| "Users retain but don't pay" | Willingness to Pay, Value Metrics, Price-Value Gap, Loss Aversion, Endowment Effect |
| "Growth is flat/linear" | Compounding vs Linear, Growth Loops, S-Curves, Power Laws |
| "Viral loop is weak" | K-Factor, Network Effects, Product-Channel Fit, Exposure Virality |
| "Free tier is too generous" | Natural Rate of Conversion, Price-Value Gap, JTBD for PLG |
| "Free tier is too restrictive" | Time-to-Value, JTBD for PLG, Adjacent User Theory |
| "Can't expand to new segments" | Adjacent User Theory, Four Fits, Second-Order Effects |
| "Enterprise users need sales" | Switching Costs, Network Effects, Platform vs Product, Dunbar's Number |
| "Too many growth ideas" | ICE/RICE Scoring, Power Laws, Opportunity Cost, One-Way vs Two-Way Doors |
| "Pricing is wrong" | Willingness to Pay, Value Metrics, Anchor Pricing, Decoy Effect |
| "Competitor is winning" | Winner-Take-All, Network Effects, Content Moats, Switching Costs |
| "Growth channel is saturating" | S-Curves, Second-Order Effects, Platform vs Product |
| "Onboarding is overwhelming" | Cognitive Load, Progressive Disclosure, Zeigarnik Effect, Endowed Progress |
| "Trial conversion is low" | Endowment Effect, Loss Aversion, Time-to-Value, Parkinson's Law |
| "Need to prioritize growth work" | ICE/RICE, One-Way vs Two-Way Doors, Opportunity Cost, Power Laws |

---

## How to Use This Reference

When a user presents a PLG challenge:

1. **Identify the category**: Is this an acquisition, activation, retention, monetization, or strategic growth problem?
2. **Consult the Challenge Matrix**: Find 2-3 relevant models from the matrix above.
3. **Apply each model**: Use the diagnostic question from each model to analyze the user's specific situation.
4. **Synthesize**: Combine insights from multiple models into a coherent recommendation.
5. **Prioritize**: Use the decision models (ICE/RICE, One-Way/Two-Way Doors) to recommend what to do first.

---

## Output Format: Mental Model Application Document

When applying mental models to a user's specific challenge, produce this document:

```
MENTAL MODEL APPLICATION
========================

CHALLENGE
  Description: [What the user is trying to solve]
  Category: [Acquisition / Activation / Retention / Monetization / Growth / Decision]

MODELS APPLIED

  Model 1: [Model Name]
    Relevance: [Why this model applies to the challenge]
    Diagnostic: [Answer to the model's diagnostic question using the user's context]
    Insight: [What the model reveals about the situation]
    Action: [Specific recommendation based on this model]

  Model 2: [Model Name]
    Relevance: [Why this model applies]
    Diagnostic: [Answer to the model's diagnostic question]
    Insight: [What the model reveals]
    Action: [Specific recommendation]

  Model 3: [Model Name] (if applicable)
    ...

SYNTHESIS
  Key Insight: [What the combination of models reveals that no single model would]
  Primary Recommendation: [The most important action to take]
  Secondary Recommendations: [Additional actions in priority order]

NEXT STEPS
  1. [Concrete first action]
  2. [Second action]
  3. [Third action]
```

---

## Cross-References

- Related skills: `plg-strategy` -- for comprehensive PLG strategy frameworks (Four Fits, Motions x Levers, PLG Maturity)
- Related skills: `growth-loops` -- for detailed loop design, modeling, and sequencing
- Related skills: `activation-metrics` -- for applying activation models (Setup/Aha/Habit) to real metrics
- Related skills: `pricing-strategy` -- for applying monetization models to pricing decisions
- Related skills: `viral-loops` -- for applying viral coefficient and network effects models
- Related skills: `retention-analysis` -- for applying retention models to churn reduction
- Related skills: `growth-experimentation` -- for applying decision models to experiment prioritization
