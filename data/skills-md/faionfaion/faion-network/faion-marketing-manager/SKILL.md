---
name: faion-marketing-manager
description: "Marketing orchestrator: GTM, content, growth, conversion optimization."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Marketing Manager Orchestrator

Pure orchestrator that coordinates marketing activities by routing to specialized sub-skills.

## Purpose

Routes marketing tasks to appropriate sub-skill based on domain. No methodologies in this skill - all execution happens in sub-skills.

## Architecture

| Sub-Skill | Purpose | Methodologies |
|-----------|---------|---------------|
| **faion-gtm-strategist** | GTM strategy, product launches, positioning, pricing, partnerships, customer success | 26 |
| **faion-content-marketer** | Content strategy, copywriting, SEO, email campaigns, social media, video/podcast production | 16 + 30 refs |
| **faion-growth-marketer** | Analytics, experiments, A/B testing, AARRR metrics, retention, viral loops | 30 |
| **faion-conversion-optimizer** | Landing pages, CRO, funnels, PLG, onboarding flows | 13 |
| **faion-ppc-manager** | Paid advertising (Google Ads, Meta Ads, LinkedIn Ads) | External skill |
| **faion-seo-manager** | Technical SEO, AEO, Core Web Vitals optimization | External skill |
| **faion-smm-manager** | Social media management (Twitter, LinkedIn, Instagram growth) | External skill |

**Total:** 85+ methodologies across 7 specialized sub-skills

## Decision Tree

| If you need... | Route to | Example Tasks |
|---------------|----------|---------------|
| **GTM & Launch** | faion-gtm-strategist | Product Hunt launch, GTM strategy, positioning, pricing strategy, partnership programs, customer success playbooks |
| **Content Creation** | faion-content-marketer | Content strategy, blog posts, copywriting, email campaigns, social posts, video scripts, podcast production |
| **Growth & Analytics** | faion-growth-marketer | AARRR framework, A/B testing, retention analysis, viral loops, cohort analysis, growth experiments |
| **Conversion** | faion-conversion-optimizer | Landing page optimization, funnel analysis, CRO experiments, PLG strategies, onboarding flows |
| **Paid Ads** | faion-ppc-manager | Google Ads campaigns, Meta Ads optimization, LinkedIn Ads, PPC strategy |
| **SEO Technical** | faion-seo-manager | Technical SEO audits, AEO optimization, Core Web Vitals, search ranking |
| **Social Media Mgmt** | faion-smm-manager | Twitter growth, LinkedIn strategy, Instagram content, community building |

## Routing Examples

### Launch Scenario
```
Product Launch
├─→ faion-gtm-strategist (GTM strategy, positioning, launch timeline)
├─→ faion-content-marketer (launch content, press release, email campaign)
├─→ faion-conversion-optimizer (landing page, free trial flow)
├─→ faion-growth-marketer (metrics tracking, launch experiments)
└─→ faion-ppc-manager (paid launch campaigns)
```

### Content Marketing Scenario
```
Content Marketing Program
├─→ faion-content-marketer (content strategy, editorial calendar, creation)
├─→ faion-seo-manager (technical SEO, on-page optimization)
├─→ faion-growth-marketer (content metrics, A/B testing)
└─→ faion-smm-manager (social distribution)
```

### Growth Optimization Scenario
```
Growth Optimization
├─→ faion-growth-marketer (AARRR analysis, experiment design, analytics)
├─→ faion-conversion-optimizer (funnel optimization, PLG tactics)
├─→ faion-content-marketer (growth content, email nurture)
└─→ faion-ppc-manager (paid acquisition scaling)
```

### Brand Building Scenario
```
Brand Building
├─→ faion-gtm-strategist (brand positioning, messaging)
├─→ faion-content-marketer (brand content, thought leadership)
├─→ faion-smm-manager (social media presence)
└─→ faion-seo-manager (brand search optimization)
```

## Execution Pattern

1. **Analyze** task intent and marketing domain
2. **Route** to appropriate sub-skill(s) via Skill tool
3. **Invoke** one or more sub-skills as needed
4. **Coordinate** multi-skill workflows if needed
5. **Report** consolidated results to user

## Quick Reference

| Marketing Goal | Primary Sub-Skill | Secondary Sub-Skills |
|----------------|-------------------|---------------------|
| Launch product | gtm-strategist | content-marketer, conversion-optimizer, ppc-manager |
| Acquire users | content-marketer | growth-marketer, seo-manager, ppc-manager |
| Optimize conversion | conversion-optimizer | growth-marketer |
| Scale growth | growth-marketer | ppc-manager, content-marketer |
| Build brand | content-marketer | gtm-strategist, smm-manager, seo-manager |
| Retain users | growth-marketer | content-marketer |
| Partnerships | gtm-strategist | content-marketer |
| Improve SEO | seo-manager | content-marketer |
| Social presence | smm-manager | content-marketer |
| Paid campaigns | ppc-manager | conversion-optimizer, growth-marketer |

## Related Skills

**Upstream:**
- faion-net (parent orchestrator)

**Downstream (coordinated by this skill):**
- faion-gtm-strategist
- faion-content-marketer
- faion-growth-marketer
- faion-conversion-optimizer
- faion-ppc-manager
- faion-seo-manager
- faion-smm-manager

**Adjacent:**
- faion-researcher (market research, competitor analysis)
- faion-product-manager (product positioning, roadmap)
- faion-ux-ui-designer (design for marketing)

## Coordination Patterns

### Single Sub-Skill Tasks
Route directly to the appropriate sub-skill for focused execution.

### Multi-Sub-Skill Workflows
For complex marketing programs, coordinate multiple sub-skills:

1. **Sequential** - GTM strategy → content creation → distribution
2. **Parallel** - Content + paid ads + social media simultaneously
3. **Iterative** - Experiments → analysis → optimization → repeat

---

*Marketing Manager Orchestrator v2.1*
*Pure Orchestrator | 7 Sub-Skills | 85+ Methodologies*
