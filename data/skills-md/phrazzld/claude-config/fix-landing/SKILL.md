---
name: fix-landing
description: |
  Run /check-landing, then fix the highest priority landing page issue.
  Creates one fix per invocation. Invoke again for next issue.
  Use /log-landing-issues to create issues without fixing.
---

# /fix-landing

Fix the highest priority landing page issue.

## What This Does

1. Invoke `/check-landing` to audit landing page
2. Identify highest priority issue
3. Fix that one issue
4. Verify the fix
5. Report what was done

**This is a fixer.** It fixes one issue at a time. Run again for next issue. Use `/copywriting` for copy improvements.

## Process

### 1. Run Primitive

Invoke `/check-landing` skill to get prioritized findings.

### 2. Fix Priority Order

Fix in this order:
1. **P0**: No landing page, redirects to app
2. **P1**: No value prop, no CTA, weak CTA, mobile broken, slow
3. **P2**: No social proof, single CTA, missing metadata
4. **P3**: Polish items

### 3. Execute Fix

**No landing page (P0):**
Create `app/page.tsx` or `app/(marketing)/page.tsx` with:
- Hero section with headline
- Feature highlights
- Call-to-action
- Social proof section

**No clear value prop (P1):**
Add compelling headline:
```tsx
<section className="hero">
  <h1 className="text-5xl font-bold">
    [Verb] your [noun]. [Benefit] in [timeframe].
  </h1>
  <p className="text-xl text-gray-600">
    [Product] helps you [primary benefit] without [common pain point].
  </p>
</section>
```

Examples:
- "Track your fitness. See results in weeks."
- "Write better code. Ship faster with confidence."
- "Manage your team. Focus on what matters."

**No CTA or weak CTA (P1):**
Add strong CTA:
```tsx
<a
  href="/signup"
  className="bg-primary text-white px-8 py-4 rounded-lg text-lg font-semibold"
>
  Start Free Trial →
</a>
```

CTA best practices:
- Action-oriented: "Start", "Get", "Try", "Create"
- Specific: "Start Free Trial" not "Submit"
- Visible: High contrast, above fold
- Multiple: Above fold + below fold

**Mobile broken (P1):**
Add responsive classes:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Features */}
</div>
```

Add mobile menu.

**Slow load time (P1):**
- Use `next/image` for images
- Use `next/font` for fonts
- Remove heavy client-side libraries from landing
- Ensure page is statically generated

**No social proof (P2):**
Add testimonials section:
```tsx
<section className="testimonials">
  <h2>What our users say</h2>
  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
    <blockquote>
      <p>"Quote from happy user"</p>
      <cite>Name, Title at Company</cite>
    </blockquote>
  </div>
</section>
```

### 4. Expert Panel Review (MANDATORY)

**Before returning fix to user, run expert panel review.**

See: `ui-skills/references/expert-panel-review.md`

1. Simulate 10 world-class advertorial experts (Ogilvy, Rams, Scher, Wiebe, Laja, Walter, Cialdini, Ive, Wroblewski, Millman)
2. Each expert scores the fixed section 0-100 with specific feedback
3. Calculate average score
4. **If average < 90:** Implement highest-impact feedback, iterate
5. **If average ≥ 90:** Proceed to verification

Example review output:
```markdown
Expert Panel Review: Hero Section Fix

| Expert | Score | Critical Improvement |
|--------|-------|---------------------|
| Ogilvy | 85 | Lead with user benefit, not feature |
| Wiebe | 82 | CTA needs specificity ("Start Free Trial" not "Get Started") |
| Laja | 78 | Add social proof above fold |
| Cialdini | 84 | Include urgency element |
...
**Average: 84.5** ❌ → Implementing top 4 improvements...
```

**Do not proceed until 90+ average achieved.**

### 5. Verify

After fix passes expert review:
```bash
# Check headline exists
grep -E "text-(4xl|5xl|6xl)" app/page.tsx

# Check CTA exists
grep -E "Start|Get Started|Try|Sign Up" app/page.tsx

# Check mobile responsiveness
grep -E "sm:|md:|lg:" app/page.tsx | head -5

# Check performance (if lighthouse CLI available)
lighthouse http://localhost:3000 --only-categories=performance
```

### 6. Report

```
Fixed: [P1] No clear value proposition

Updated: app/page.tsx
- Added hero section with headline
- Added sub-headline explaining benefit
- Added supporting visual

Copy:
- Headline: "Track your fitness journey. See results in weeks."
- Sub: "Volume helps you build consistent habits without complicated tracking."

Next highest priority: [P1] No CTA button
Run /fix-landing again to continue.
```

## Branching

Before making changes:
```bash
git checkout -b landing/improvements-$(date +%Y%m%d)
```

## Single-Issue Focus

Landing pages are high-impact. Test each change:
- A/B test major copy changes
- Measure conversion impact
- Keep changes reversible

Run `/fix-landing` repeatedly to optimize conversions.

## Related

- `/check-landing` - The primitive (audit only)
- `/log-landing-issues` - Create issues without fixing
- `/copywriting` - Marketing copy improvements
- `/cro` - Conversion rate optimization
