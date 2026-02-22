---
name: problem-validation
description: >
  Validate whether a problem is worth solving before building anything.
  Use when asked to validate a problem, assess problem-solution fit,
  decide whether to build something, or evaluate if a problem is real.
  Scores problems on frequency, intensity, willingness to pay, and
  existing workarounds.
---

Validate problems with evidence, not opinions. A problem worth solving is one that people encounter frequently, feel intensely, and have already tried to solve. If nobody has attempted a workaround, the problem isn't painful enough to build for.

## Scoring Framework

Rate each dimension 1-5 based on evidence:

### Frequency (How often does this happen?)
- 5: Daily or multiple times per day
- 4: Weekly
- 3: Monthly
- 2: Quarterly
- 1: Rarely or once

### Intensity (How painful is it when it happens?)
- 5: Blocks critical work, causes real losses (money, time, reputation)
- 4: Major friction, significant workarounds needed
- 3: Annoying but manageable
- 2: Minor inconvenience
- 1: Barely noticeable

### Existing Workarounds (Are people already trying to solve it?)
- 5: Paying for imperfect solutions or built custom tools
- 4: Cobbled together multi-tool workflows (spreadsheets + email + manual steps)
- 3: Have a basic process but it's tedious
- 2: Occasionally Google for solutions
- 1: Haven't tried to solve it

### Willingness to Pay (Would they pay to make this go away?)
- 5: Already spending money on partial solutions
- 4: Have explicitly said they'd pay (and named a number)
- 3: Would "probably" pay (hypothetical — discount this)
- 2: Want it free
- 1: Haven't considered paying

**Validation Score = Frequency x Intensity x Workarounds x WTP**

- **250+**: Strong signal. Build.
- **100-249**: Promising. Needs more evidence on weak dimensions.
- **Under 100**: Weak. Either pivot the problem framing or walk away.

Example: "PDF Export" — Frequency: 3 (monthly board reports), Intensity: 2 (screenshot workaround exists), Workarounds: 4 (3 users built browser-print-to-PDF workflows), WTP: 1 (nobody has paid for an export tool). Score = 3 x 2 x 4 x 1 = **24**. Verdict: Kill — not painful enough.

## Evidence Requirements

Every score MUST cite evidence. Acceptable evidence types, strongest first:

1. **Observed behavior:** You watched someone struggle with this
2. **Spending:** They pay for alternatives or workarounds
3. **Time invested:** They built custom solutions (scripts, spreadsheets, processes)
4. **Quotes from interviews:** Direct quotes about past behavior (Mom Test compliant)
5. **Support tickets / forum posts:** Public complaints with specifics
6. **Survey responses:** Weakest — people say one thing and do another

If your only evidence is survey responses or "my friend said," your validation is weak.

## Go / No-Go Decision

**Go** when:
- Score 250+ with evidence across all four dimensions
- At least 5 people independently describe the same problem
- Someone has spent money or significant time on workarounds

**Investigate more** when:
- Score 100-249 with strong evidence on 2-3 dimensions
- You've talked to fewer than 5 people
- Workaround evidence is weak

**Kill** when:
- Score under 100
- Nobody has tried to solve the problem themselves
- "Willingness to pay" is entirely hypothetical
- You've talked to 5+ people and stories don't converge

## Guidelines

- CRITICAL: NEVER validate based on opinions or surveys alone. Require evidence of past behavior.
- ALWAYS require workaround evidence. No workarounds = not painful enough.
- NEVER count "I would definitely use that!" as validation. Enthusiasm is not evidence.
- ALWAYS talk to at least 5 people in the ICP before making a go/no-go call.
- NEVER confuse "interesting problem" with "problem worth solving." Interesting doesn't pay the bills.

---

*Built on YC's "talk to users" philosophy and The Mom Test (Rob Fitzpatrick). Skills from [productskills](https://github.com/assimovt/productskills).*
