---
name: scope-cutting
description: >
  Cut scope ruthlessly using Shape Up's appetite-first approach.
  Use when asked to reduce scope, find the MVP, trim features,
  ship faster, or figure out what to cut. Applies fixed time
  variable scope thinking and scope hammering techniques.
---

Cut scope by flipping the question. Instead of "How long will this take?" ask "How much time is this problem WORTH?" Set the appetite first, then shape the solution to fit. This is Shape Up's core insight: fixed time, variable scope.

## Set the Appetite

Before touching scope, declare the time budget:

- **Small batch:** 1-2 weeks for 1-2 people
- **Big batch:** 6 weeks max for a small team

If a project takes more than 6 weeks (or 3 weeks for 1-3 people per Linear's method), it's too big. Break it down or walk away.

The appetite is NOT an estimate. An estimate says "this will take X." An appetite says "this is WORTH X." If the shaped solution doesn't fit the appetite, cut scope until it does — or kill the project.

## Scope Hammering

For every item in the spec, ask these questions in order:

1. **Must-have or nice-to-have?** If the feature ships without it and users still get value, it's nice-to-have. Cut it.
2. **Shippable without it?** Can you deploy a working version that doesn't include this? If yes, cut it from v1.
3. **Edge case or core path?** If fewer than 20% of users will encounter this scenario, defer it.
4. **Compare to baseline.** The baseline is NO feature — not the ideal version. "Is this better than nothing?" always wins over "Is this as good as it could be?"

## Shape the Solution Down

When scope is still too big after hammering:

- **Cut breadth, not quality.** Support 1 auth provider well instead of 3 badly. Handle the happy path completely instead of covering every error state.
- **Remove entire surfaces.** Kill the settings page. Remove the dashboard. Ship with sensible defaults instead of configurability.
- **Time-bound the edge cases.** "We'll handle CSV import of up to 1,000 rows. Above that, they email us." Solve it manually until scale demands automation.
- **Ask: "What's the simplest version a customer would thank us for?"** That's your scope.

## Circuit Breaker (Shape Up)

If it doesn't ship in one cycle, it's cancelled by default. No automatic rollover. The team must re-pitch for another cycle. This prevents zombie projects that drag on forever.

## Guidelines

- CRITICAL: NEVER cut quality — cut BREADTH. A polished feature that does one thing > a buggy feature that does five.
- NEVER estimate. Set appetite. "This is worth 2 weeks" not "This will take 2 weeks."
- NEVER let v1 have more than 5 must-haves. If it does, you haven't scoped hard enough.
- ALWAYS compare to baseline (no feature at all), not to the ideal implementation.
- ALWAYS ask "What can we ship in [appetite]?" not "How long until we ship everything?"
- NEVER carry work over automatically. Unfinished work must be re-pitched.

---

*Built on Shape Up (Basecamp) and the Linear Method. Skills from [productskills](https://github.com/assimovt/productskills).*
