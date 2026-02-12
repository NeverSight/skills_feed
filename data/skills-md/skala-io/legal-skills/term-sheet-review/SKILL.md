---
name: "term-sheet-review"
description: "Review VC term sheets for pre-seed, seed, and Series A rounds. Analyzes each clause from investor or startup perspective, identifies investor-friendly vs. founder-friendly terms, flags deviations from market standards, and provides negotiation guidance. Use when reviewing any VC term sheet, evaluating investment terms, or preparing for funding negotiations. Triggers on term sheet, VC financing, Series A, seed round, liquidation preference, anti-dilution, protective provisions."
metadata:
  author: "Skala Inc."
  license: "Apache-2.0"
  license-notice: "See LICENSE and NOTICE files in the repository"
  homepage: "https://skala.io/legal-skills"
  repository: "https://github.com/skala-io/legal-skills"
---

*First published on [Skala Legal Skills](https://www.skala.io/legal-skills)*

## Legal Disclaimer

This skill is provided for informational and educational purposes only and does not constitute legal advice. The analysis and information provided should not be relied upon as a substitute for consultation with a qualified attorney. No attorney-client relationship is created by using this skill. Laws and regulations vary by jurisdiction and change over time. Always consult with a licensed attorney in your jurisdiction for advice on specific legal matters. The creators and publishers of this skill disclaim any liability for actions taken or not taken based on the information provided.

---

# VC Term Sheet Review

## Overview

Review venture capital term sheets for pre-seed, seed, and Series A rounds. Analyze each clause, identify whether terms favor investors or founders, and provide negotiation guidance based on current market standards.

## Workflow

1. **Ask user role**: Investor or Startup founder?
2. **Identify investment stage**: Pre-seed, Seed, Series A, or Series B+
3. **Extract and analyze each clause** against market standards
4. **Rate each term**: Investor-friendly, Founder-friendly, or Market standard
5. **Provide tailored recommendations** based on user's role
6. **Generate summary** with key negotiation points

## Initial Questions

Before reviewing a term sheet, ask the user:

```
1. Are you the INVESTOR or the STARTUP in this transaction?
2. [If not clear from document] What stage is this financing? (Pre-seed/Seed/Series A)
```

**Series B+ handling**: If the term sheet is for Series B or later:
> "I should note that my expertise is primarily in pre-seed through Series A transactions. Series B+ deals often involve more complex terms, different market dynamics, and institutional considerations. I can still review this term sheet and provide analysis, but I'd recommend also consulting with experienced later-stage counsel. Would you like me to proceed with the review?"

## Clause Analysis Framework

For each clause, provide:
- **Current term**: What the term sheet says
- **Market standard**: What's typical for this stage (see references/market-standards.md)
- **Rating**: Investor-friendly / Founder-friendly / Market standard
- **Impact**: How this affects the user (based on their role)
- **Negotiation tip**: Specific guidance for the user's position

## Key Clauses to Review

Analyze these clauses in order (see references/clause-analysis.md for detailed guidance):

### Economics
1. **Valuation** (pre-money, post-money, option pool)
2. **Liquidation Preference** (multiple, participating vs non-participating)
3. **Dividends** (cumulative vs non-cumulative, rate)
4. **Anti-dilution** (full ratchet vs weighted average)
5. **Pay-to-play**

### Control
6. **Board Composition** (seats, observer rights)
7. **Protective Provisions** (veto rights)
8. **Drag-along Rights**
9. **Voting Rights**

### Other Rights
10. **Pro-rata Rights** (participation in future rounds)
11. **Information Rights**
12. **Registration Rights**
13. **Right of First Refusal / Co-sale**
14. **Founder Vesting**
15. **No-shop Period**

## Output Format

Structure your review as:

```
## Term Sheet Review Summary

**Company**: [Name]
**Round**: [Stage]
**Reviewing as**: [Investor/Startup]

## Overall Assessment
[2-3 sentence summary of the deal's overall character]

## Clause-by-Clause Analysis

### 1. Valuation
- **Term**: [What's stated]
- **Assessment**: [Rating]
- **Analysis**: [Impact and context]
- **Recommendation**: [For this user's role]

[Continue for each clause...]

## Key Negotiation Points
1. [Most important issue to address]
2. [Second priority]
3. [Third priority]

## Red Flags
- [Any terms significantly outside market norms]

## Summary Table
| Clause | Rating | Priority to Negotiate |
|--------|--------|----------------------|
| ... | ... | ... |
```

## References

- **references/market-standards.md**: Current market standards by stage (2024-2025 data)
- **references/clause-analysis.md**: Detailed analysis guidance for each clause type
