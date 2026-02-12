---
name: "reg-s-offering"
description: "Provides guidance on Regulation S offerings of securities under U.S. law. Helps determine eligibility for Regulation S exemption, identify applicable transaction categories (1, 2, or 3), understand safe harbor requirements under Rules 903 and 904, and navigate distribution compliance periods. Use this skill when advising on offshore securities offerings, Reg S transactions, or resales of restricted securities outside the United States."
metadata:
  author: "Skala Inc."
  license: "Apache-2.0"
  license-notice: "See LICENSE and NOTICE files in the repository"
  homepage: "https://skala.io/legal-skills"
  repository: "https://github.com/skala-io/legal-skills"
---

*First published on [Skala Legal Skills](https://www.skala.io/legal-skills)*

## Legal Disclaimer

This skill is provided for informational and educational purposes only and does not constitute legal advice. The analysis and information provided should not be relied upon as a substitute for consultation with a qualified attorney. No attorney-client relationship is created by using this skill. Securities laws are complex and fact-specific. The application of Regulation S depends on the particular circumstances of each offering. Laws and regulations vary by jurisdiction and change over time. Always consult with a licensed attorney in your jurisdiction for advice on specific legal matters. The creators and publishers of this skill disclaim any liability for actions taken or not taken based on the information provided.

---

# Regulation S Offering Advisor

## Overview

Regulation S provides a safe harbor from the registration requirements of Section 5 of the Securities Act of 1933 for offers and sales of securities that occur outside the United States. It is based on the territorial approach to Section 5, recognizing that U.S. registration requirements are primarily designed to protect U.S. investors.

### Key Principle

Regulation S establishes that Section 5 registration requirements do not apply to offers and sales of securities that occur outside the United States, provided certain conditions are met to prevent the securities from flowing back to U.S. persons during a restricted period.

### Two Safe Harbors

Regulation S contains two distinct safe harbors:

1. **Issuer Safe Harbor (Rule 903)**: For offers and sales by issuers, distributors, their affiliates, and persons acting on their behalf
2. **Resale Safe Harbor (Rule 904)**: For resales by persons other than the issuer, distributors, their affiliates, or persons acting on their behalf

---

## Quick Decision Workflow

### Step 1: Is Regulation S Potentially Available?

Ask these threshold questions:

- [ ] Is the offer or sale occurring **outside the United States**?
- [ ] Can the transaction qualify as an **"offshore transaction"**?
- [ ] Are there **no "directed selling efforts"** in the United States?

If YES to all → Proceed to Step 2
If NO to any → Regulation S safe harbors are not available

### Step 2: Are You the Issuer or a Reseller?

| If you are... | Use... |
|---------------|--------|
| Issuer, distributor, affiliate of issuer, or acting on their behalf | **Issuer Safe Harbor (Rule 903)** → Go to Step 3 |
| Any other person (investor, dealer, etc.) | **Resale Safe Harbor (Rule 904)** → See `references/resale-safe-harbor.md` |

### Step 3: Determine the Transaction Category (for Issuer Safe Harbor)

The Issuer Safe Harbor has three categories with progressively stricter requirements:

| Category | When It Applies | Restrictions |
|----------|-----------------|--------------|
| **Category 1** | Foreign issuer with no SUSMI; overseas directed offerings; certain government securities | Fewest restrictions |
| **Category 2** | Reporting foreign issuers (equity); reporting U.S. issuers (debt); non-reporting foreign issuers (debt) | Moderate restrictions |
| **Category 3** | All other offerings (typically non-reporting U.S. issuers, equity of non-reporting foreign issuers with SUSMI) | Most stringent restrictions |

**For detailed category determination**, see `references/category-determination.md`

### Step 4: Apply the Applicable Requirements

Based on your category, ensure compliance with:

1. **General conditions** (offshore transaction, no directed selling efforts)
2. **Offering restrictions** (if applicable)
3. **Distribution compliance period** requirements
4. **Legends and certifications** (if applicable)
5. **Special rules** for debt or equity securities

---

## Key Concepts Quick Reference

| Term | Brief Definition | Full Details |
|------|------------------|--------------|
| **U.S. Person** | Includes U.S. residents, domestic entities, and certain trusts/estates | `references/key-definitions.md` |
| **Offshore Transaction** | Offer not made to person in U.S.; buyer outside U.S. or on designated offshore securities market | `references/key-definitions.md` |
| **Directed Selling Efforts** | Activities that could condition the U.S. market for the securities | `references/key-definitions.md` |
| **SUSMI** | Substantial U.S. Market Interest – determines category for equity and debt | `references/key-definitions.md` |
| **Distribution Compliance Period** | 40 days or 6 months/1 year depending on category and security type | `references/key-definitions.md` |
| **Distributor** | Underwriter, dealer, or other person participating in distribution | `references/key-definitions.md` |

---

## Reference Materials

For detailed guidance on specific topics, consult these reference files:

| Topic | File |
|-------|------|
| Key defined terms and concepts | `references/key-definitions.md` |
| Issuer Safe Harbor (Rule 903) requirements | `references/issuer-safe-harbor.md` |
| Resale Safe Harbor (Rule 904) requirements | `references/resale-safe-harbor.md` |
| How to determine transaction category | `references/category-determination.md` |
| Special rules for debt securities (including TEFRA) | `references/debt-securities.md` |
| Special rules for equity securities | `references/equity-securities.md` |
| Practical compliance checklist | `references/practical-checklist.md` |

---

## Common Questions

### Can a U.S. issuer use Regulation S?
Yes. Regulation S is available to both U.S. and foreign issuers, though U.S. issuers typically fall into Category 2 (for debt) or Category 3 (for equity), which have more stringent requirements.

### Can Regulation S securities ever be sold to U.S. persons?
Yes, but generally only after the distribution compliance period has expired and in compliance with applicable resale restrictions. During the DCP, sales to U.S. persons are prohibited or heavily restricted depending on the category.

### What is the relationship between Regulation S and Rule 144A?
They are complementary. An offering can be structured with a Regulation S tranche (for non-U.S. investors) and a Rule 144A tranche (for U.S. qualified institutional buyers). See `references/resale-safe-harbor.md` for integration considerations.

### Does Regulation S provide a complete exemption from U.S. securities laws?
No. Regulation S only exempts offers and sales from Section 5 registration requirements. The antifraud provisions of U.S. securities laws continue to apply to offerings made in reliance on Regulation S.

---

## Using This Skill

When a user asks about Regulation S offerings:

1. **Start with the disclaimer** – remind users this is educational information, not legal advice
2. **Identify the transaction type** – issuer offering or resale?
3. **Determine the category** – use the workflow above
4. **Load relevant reference files** – provide detailed requirements from the appropriate reference documents
5. **Highlight key compliance points** – legends, certifications, DCP requirements
6. **Recommend legal counsel** – for any actual transaction

### Sample Prompt Handling

**User asks**: "We're a Delaware corporation wanting to sell equity offshore. What do we need to do?"

**Response approach**:
1. Note this is likely a Category 3 transaction (U.S. issuer, equity)
2. Load `references/issuer-safe-harbor.md` and `references/equity-securities.md`
3. Explain the strict Category 3 requirements
4. Provide the practical checklist from `references/practical-checklist.md`
5. Emphasize need for qualified securities counsel
