---
name: amazon-shopping
version: "1.0.1"
description: Search Amazon.com, extract product data, and present ranked recommendations. Use when user asks to shop on Amazon, find products, compare items, or research purchases. Prioritizes review count over rating.
allowed-tools: "Bash(agent-browser*)"
---

# Amazon Shopping

Search Amazon and recommend products based on user preferences.

---

## ⚠️ MANDATORY FIRST STEP - REQUIREMENTS GATHERING

**YOU MUST ASK CLARIFYING QUESTIONS BEFORE ANY BROWSER AUTOMATION.**

DO NOT proceed to search until you understand:
- **Budget**: Price range they're comfortable with
- **Usage**: Who/what it's for (personal, gift, professional)
- **Deal-breakers**: Features they must have or avoid

Use `AskUserQuestion` to gather this information. Only after receiving answers should you proceed to Step 2.

**Example questions for any product:**
- Budget range (under $25, $25-50, $50-100, $100+)
- Primary use case (personal, gift, professional)
- Key preferences (brand, features, quality vs value)

---

## Quick Start (After Requirements Gathered)

1. ~~**Gather requirements**: Ask about budget, usage, deal-breakers~~ → **DONE in mandatory step above**
2. **Search Amazon**: Use agent-browser to search and capture snapshot
3. **Extract data**: Pull ASINs, prices, ratings, review counts
4. **Present recommendations**: Ranked by user's criteria

## Prerequisites

- `agent-browser` CLI at `/opt/homebrew/bin/agent-browser`
- Internet access to Amazon.com
- Run command examples from this skill's root directory (the folder containing `SKILL.md`) so relative paths like `scripts/...` and `reference/...` resolve correctly.

## Search Workflow

### Step 1: Open Amazon

```bash
agent-browser open https://www.amazon.com
```

### Step 2: Fill Search

```bash
agent-browser fill "[role='searchbox']" "<search query>"
agent-browser press Enter
sleep 5  # Wait for page load
```

### Step 3: Capture Results

```bash
agent-browser snapshot > results.txt
```

### Step 4: Extract Products WITH Their ASINs (NEW METHOD)

**⚠️ CRITICAL: NEVER extract ASINs separately from product names. This causes mismatches.**

**Use the container-based extraction script** instead of grep:
```bash
# Extract product name AND its ASIN from THE SAME container
python3 scripts/extract_products.py results.txt
```

The script parses the YAML/indented structure of the accessibility tree and identifies product containers (list items containing both heading and link), then extracts product name AND its ASIN from THE SAME container.

**Output format:**
```json
[
  {"name": "Product Name", "asin": "B0XXXXXXXXX", "ref": "e123", "line_index": 42},
  ...
]
```

**❌ WRONG METHOD - Causes ASIN/Product Mismatches:**
```bash
# NEVER DO THIS - Extracts ASINs separately, loses product association
grep -oE "dp/[A-Z0-9]{10}" results.txt | sed 's|dp/||'
# Or using context windows that can pick up wrong ASINs:
grep -B2 -A2 "Product Name" results.txt | grep -oE "dp/[A-Z0-9]{10}"
```

### Step 5: MANDATORY Product Page Verification (ENFORCED)

**For EVERY product before presenting it to the user, you MUST verify:**

```bash
# Use the verification script
bash scripts/verify_products.sh results.txt
```

The verification script:
1. Opens each product page individually
2. Verifies the page title matches expected product
3. Extracts the ACTUAL price from the product page
4. Extracts rating and review count
5. Only outputs VERIFIED products

**Manual verification (if script unavailable):**
```bash
# Open product page
agent-browser open https://www.amazon.com/dp/[ASIN]
sleep 3
agent-browser snapshot | grep -iE "price|One-time purchase"

# Verify:
# 1. Title matches the product you're recommending
# 2. Price is current and accurate (look for "One-time purchase: $XX.XX")
```

**⚠️ MANDATORY VERIFICATION RULES:**
- If ASIN redirects to different product → DISCARD
- If page title doesn't match expected product → DISCARD
- If price cannot be found → DISCARD
- Only present VERIFIED products with ✓ marker

**⚠️ NEVER extract prices from search results pages** - prices shown in search results often don't match actual product page prices due to variants, promotions, or different sellers.

See reference/asin-extraction.md for detailed patterns.

## Common Issues

| Issue | Solution |
|-------|----------|
| CAPTCHA | Wait 60s, retry |
| Rate limited | Wait 2-3 min |
| No results | Broaden search |

See [reference/common-errors.md](reference/common-errors.md) for complete troubleshooting.

## Output Format

**ALL presented products MUST be verified on their actual product pages.**

```markdown
## Amazon Shortlist - [Category]

### 1. [Product] - $XX.XX ✓ VERIFIED
**ASIN**: [ASIN] (verified on product page)
**Rating**: X.X/5 (X,XXX reviews)
**Amazon**: https://www.amazon.com/dp/[ASIN]
**Why this**: [Reason]
**Key specs**: [Specs]
```

**⚠️ Do NOT present unverified products.** The ✓ VERIFIED marker confirms that:
1. The ASIN link goes to the actual product (not a redirect)
2. The price is current from the product page
3. The title matches what was recommended

See [reference/output-formats.md](reference/output-formats.md) for templates.

## Ranking Priority

When ratings are similar (within 0.5), prioritize review count.

Example: 4.0 with 10,000 reviews > 5.0 with 100 reviews

## Optional: Ranking Script

For 10+ products, use the ranking script:

```bash
python3 scripts/rank_products.py products.jsonl --budget 100 --priority rating
```
