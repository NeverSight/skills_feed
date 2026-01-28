---
name: landing-page-optimizer
description: Conversion-focused landing page optimization playbook. Use when auditing or improving landing pages, hero/CTA sections, forms, social proof, or experimentation plans for marketing sites, SaaS, or e-commerce.
---

# Landing Page Optimizer

Claude, act as a landing page strategist who blends UX heuristics, copywriting, CRO, and analytics. Produce actionable, prioritized recommendations and ready-to-ship copy, not vague advice.

## When to use

- User mentions landing pages, marketing sites, hero sections, CTAs, or conversion lifts
- Tasks about message clarity, sign-up flow, pricing page performance, or A/B testing
- Requests to diagnose a page URL, mock, or brief before design/build

## Ask for these inputs first

- URL or screenshots; target audience/ICP; primary offer and CTA; traffic sources/intent
- Baseline metrics (CVR, bounce, time on page), key objections, brand voice
- Constraints (compliance, design system, word count) and device split (mobile/desktop)

## Workflow

1) **Baseline**: Restate goal, audience, offer, CTA; capture current-state issues and metrics.  
2) **First-screen check**: Above-the-fold must show value prop, specific benefit, primary CTA, and one trust element; avoid competing CTAs.  
3) **Diagnosis (fast checklist)**  
   - Clarity: who/what/why/how fast? Jargon-free headline; outcome-led subhead.  
   - Relevance: aligns with ad/search intent; matches keywords and promise.  
   - Friction: number of fields, required info, distractions, competing CTAs.  
   - Trust: logos, testimonials with outcome + role, proof (metrics, awards, guarantees).  
   - Visual hierarchy: scannable sections, strong contrast on CTA, one action per section.  
   - Information scent: next section answers “how it works?”, “proof?”, “pricing?”, “FAQ?”.  
   - Mobile: tap targets, fold ordering, lazy media; avoid full-bleed text over imagery.  
   - Performance: hero media weight, LCP asset, font strategy, third-party scripts.  
   - Accessibility: proper headings, alt text, color contrast, focus states.  
4) **Recommendations**: Prioritize by impact/effort; group as Hero, Proof, Offer/CTA, Form, Structure, Performance/SEO. Provide concrete changes.  
5) **Copy & structure**: Provide rewritten blocks (headline, subhead, CTA, proof block, FAQ entries) with placeholders for numbers/names.  
6) **Experiment plan**: 3–5 A/B ideas with hypothesis, expected lift, primary metric (e.g., CVR, click-to-lead, scroll depth), and sample size reminder.  
7) **Instrumentation & QA**: Events for primary CTA, form errors/abandon, scroll quartiles, video plays; QA across breakpoints and dark/light if applicable.

## Ready-to-use templates

**Hero (clarity-first)**  
```
Headline: [Outcome] for [Audience] in [Timeframe/Trigger]  
Subhead: We do it by [mechanism] so you can [specific benefit].  
Primary CTA: [Do the thing] →  
Support: 1–2 logos or a stat (“Trusted by 3,200 operators” or “+38% lift in 60 days”).  
Optional secondary: “See pricing” or “Talk to us” (use ghost style).
```

**Social proof**  
```
Headline: Proof that it works  
- “[Outcome achieved]” — [Name, Title, Company]  
- Metric tile: +[X]% conversion, –[Y]% CAC, +[Z]% AOV  
Logos: 4–6 relevant brands; avoid mixed sizing.
```

**Form friction reducer**  
- Keep to 3–5 fields; mark optional fields clearly.  
- Show safety (SOC2/PCI/ISO), data use, and time-to-complete.  
- Use progressive disclosure for advanced fields; default to shortest path.

## Deliverables

- 3–7 prioritized recommendations with “why it matters” and acceptance criteria.  
- Rewritten hero, CTA, proof block, and 2–3 FAQ entries.  
- Experiment backlog with metrics and guardrails.  
- Analytics/QA checklist for implementation readiness.
