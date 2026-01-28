---
name: contract-analyzer
description: Review contracts for concerning clauses, extract key terms, compare to standard terms, and flag unusual provisions. Use when user needs contract review, legal document analysis, or agreement evaluation.
---

# Contract Analyzer

Intelligent contract review highlighting risks, key terms, and unusual provisions.

## When to Use This Skill

Activate when the user:
- Provides a contract or agreement to review
- Asks "review this contract"
- Needs to understand contract terms
- Wants concerning clauses identified
- Mentions NDA, employment agreement, freelance contract
- Needs to compare contract terms
- Asks about legal document analysis

## ⚠️ Important Disclaimers

**Include this disclaimer in every output:**
> ⚠️ **Legal Disclaimer**: This is informational analysis only, not legal advice. Always consult with a qualified attorney for legal matters. Contract interpretation can be complex and jurisdiction-specific.

## Instructions

1. **Identify Contract Type**
   - Employment agreement
   - Independent contractor/freelance agreement
   - Non-disclosure agreement (NDA)
   - Service agreement
   - Partnership agreement
   - Software license
   - Real estate agreement
   - Purchase agreement

2. **Extract Key Terms**

   **Financial Terms:**
   - Payment amount and schedule
   - Rate increases or bonuses
   - Expense reimbursement
   - Late payment penalties
   - Price adjustments

   **Duration and Termination:**
   - Contract length
   - Renewal terms (automatic or manual)
   - Termination conditions
   - Notice period required
   - Termination fees or penalties

   **Intellectual Property:**
   - Work-for-hire provisions
   - IP ownership (who owns what)
   - IP assignment clauses
   - License grants
   - Pre-existing IP protections

   **Liability and Indemnification:**
   - Liability caps
   - Indemnification obligations
   - Insurance requirements
   - Warranty disclaimers

   **Other Critical Terms:**
   - Non-compete clauses
   - Confidentiality obligations
   - Dispute resolution (arbitration, jurisdiction)
   - Governing law
   - Amendment procedures

3. **Flag Concerning Clauses**

   **Red Flags (High Risk):**
   - Unlimited liability
   - Perpetual non-compete
   - Automatic renewal without notice
   - Unreasonable indemnification
   - One-sided termination rights
   - Unclear payment terms
   - Overly broad IP assignment
   - Waiver of legal rights
   - Mandatory arbitration (in some contexts)

   **Yellow Flags (Review Carefully):**
   - Long non-compete duration
   - Broad confidentiality scope
   - Short termination notice
   - Net 60+ payment terms
   - Restrictive exclusivity clauses
   - Unilateral amendment rights

4. **Compare to Industry Standards**
   - Note terms that deviate from typical agreements
   - Identify unusually favorable or unfavorable terms
   - Flag missing standard protections
   - Note one-sided provisions

5. **Assess Balance**
   - Is contract heavily favoring one party?
   - Are obligations reciprocal?
   - Are penalties balanced?
   - Are protections mutual?

6. **Provide Actionable Recommendations**
   - Specific clauses to negotiate
   - Alternative language suggestions
   - Questions to ask the other party
   - Terms to add or clarify
   - Deal-breakers to consider

## Output Format

```markdown
# Contract Analysis Report

⚠️ **Legal Disclaimer**: This is informational analysis only, not legal advice. Always consult with a qualified attorney for legal matters.

## Contract Overview
- **Type**: [Contract type]
- **Parties**: [Your company] & [Other party]
- **Effective Date**: [Date]
- **Term**: [Duration]

---

## 🚨 Red Flags (Critical Issues)

### 1. Unlimited Personal Liability (Section X)
**Clause**: "[Quote problematic language]"

**Risk**: You could be personally liable for unlimited damages, even beyond insurance coverage.

**Standard Alternative**: Liability should be capped at contract value or insurance limits.

**Recommendation**: Negotiate liability cap of $X or insurance policy limit.

---

## ⚠️ Yellow Flags (Concerning Terms)

### 2. 2-Year Non-Compete (Section Y)
**Clause**: "[Quote]"

**Concern**: Prevents working in your field for 24 months.

**Industry Standard**: 6-12 months is more typical for this role.

**Recommendation**: Negotiate reduction to 6 months and narrower geographic/industry scope.

---

## 💰 Financial Terms

| Term | Details | Assessment |
|------|---------|------------|
| Payment | $X,XXX/month | ✓ Reasonable |
| Payment Schedule | Net 60 | ⚠️ Long (Net 30 preferred) |
| Late Fees | None | ⚠️ Consider adding |
| Rate Increases | Annual 3% | ✓ Good |

---

## 📋 Key Terms Summary

### Intellectual Property
- **Ownership**: [Who owns work product]
- **Assessment**: ⚠️ Clause X assigns all IP, including pre-existing work
- **Recommendation**: Add carve-out for pre-existing IP

### Termination
- **Notice Period**: 30 days
- **Termination for Convenience**: [Yes/No]
- **Assessment**: ✓ Reasonable terms

### Confidentiality
- **Duration**: 3 years post-termination
- **Scope**: [Broad/Narrow]
- **Assessment**: ✓ Standard

### Dispute Resolution
- **Method**: Mandatory arbitration (JAMS rules)
- **Jurisdiction**: [State]
- **Assessment**: ⚠️ Limits court access; may favor large company

---

## ⚖️ Balance Assessment

**Overall Balance**: ⚠️ Somewhat one-sided

**Favors**: [Party name]

**Issues**:
- Termination rights are one-sided (they can terminate for convenience, you cannot)
- Indemnification obligations only apply to you
- They can amend terms with 30 days notice

---

## ✅ Positive Terms

1. Clear payment schedule
2. Reasonable confidentiality duration
3. Insurance requirements are standard
4. IP ownership for pre-existing work protected

---

## 📝 Negotiation Recommendations

### Must Negotiate (Deal Critical)
1. **Liability Cap**: Add cap of $XXX,XXX or insurance limits
2. **Non-Compete**: Reduce to 6 months

### Should Negotiate (High Priority)
3. **Payment Terms**: Request Net 30 instead of Net 60
4. **Mutual Termination**: Add for-convenience termination rights for both parties

### Consider Negotiating (Nice to Have)
5. **Arbitration**: Add option for small claims court
6. **Amendment Rights**: Require mutual consent for material changes

---

## ❓ Questions to Ask

1. "Can we cap liability at the contract value of $X?"
2. "Would you consider reducing the non-compete period to 6 months?"
3. "Can we adjust payment terms to Net 30?"
4. "Is the mandatory arbitration clause negotiable?"

---

## 🚩 Missing Clauses

Standard provisions not included:
- Force majeure clause (pandemic, natural disasters)
- Data protection/GDPR compliance
- Insurance requirements
- Warranty of authority

---

## Overall Recommendation

**Risk Level**: ⚠️ Medium-High

**Action**: Do NOT sign as-is. Negotiate key terms (liability cap, non-compete, payment terms) before signing. Consult attorney for review.

**Deal Assessment**: [Acceptable if concerns addressed / Proceed with caution / Significant concerns]
```

## Examples

**User**: "Review this freelance contract"
**Response**: Identify contract type (independent contractor) → Extract payment terms, IP ownership, termination → Flag unlimited indemnification clause → Note missing late payment terms → Compare to standard freelance agreements → Recommend specific negotiations

**User**: "Is this NDA reasonable?"
**Response**: Analyze confidentiality scope (overly broad, includes "residual knowledge") → Check duration (perpetual - concerning) → Review reciprocity (one-way NDA) → Flag concerning terms → Suggest mutual NDA with 3-year term

**User**: "What should I look out for in this employment agreement?"
**Response**: Review compensation, benefits, IP assignment → Flag broad non-compete (entire industry, 2 years) → Note missing remote work provisions → Check termination clauses → Identify one-sided provisions → Provide negotiation priorities

## Best Practices

- Always include legal disclaimer
- Quote specific problematic language
- Provide section/clause numbers
- Explain *why* something is concerning (not just that it is)
- Offer specific alternative language
- Prioritize issues (must-fix vs. nice-to-have)
- Compare to industry standards when possible
- Note missing standard protections
- Consider user's leverage and circumstances
- Provide negotiation talking points
- Be specific with recommendations
- Highlight positive terms too (not just negative)
- Use clear risk indicators (🚨 ⚠️ ✓)
- Make output scannable and actionable
