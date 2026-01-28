---
name: intelligems-segment-analysis
description: Analyze which audience segments each active Intelligems experiment is winning in. Shows device type, visitor type, and traffic source breakdowns with confidence levels. Use when you want to see segment-level performance of A/B tests.
---

# /intelligems-segment-analysis

Analyze segment-level performance of active Intelligems experiments.

Shows which segments (device, visitor type, traffic source) each experiment is winning in, with:
- Visitors and orders per segment
- Which variation is performing best
- RPV lift and confidence levels
- GPV lift (if COGS data exists)

---

## Prerequisites

- Python 3.8+
- Intelligems API key (get from Intelligems support)

---

## Step 1: Get API Key

**Ask the user for their Intelligems API key.**

If they don't provide it upfront, ask:

> "What's your Intelligems API key? You can get one by contacting support@intelligems.io"

**IMPORTANT:** Never use a hardcoded or default API key. The user must provide their own.

---

## Step 2: Set Up Project

Create a project directory with the analysis script:

```bash
mkdir -p intelligems-segment-analysis
cd intelligems-segment-analysis
```

### Create config.py

Copy from `references/config.py`:

```python
# Intelligems Segment Analysis Configuration

# API Configuration
API_BASE = "https://api.intelligems.io/v25-10-beta"

# Thresholds (Intelligems Philosophy: 80% is enough)
MIN_CONFIDENCE = 0.80  # 80% probability to beat baseline
MIN_RUNTIME_DAYS = 14  # Don't make status judgments until test runs 2+ weeks

# Segment types to analyze
SEGMENT_TYPES = [
    ("device_type", "BY DEVICE"),
    ("visitor_type", "BY VISITOR TYPE"),
    ("source_channel", "BY TRAFFIC SOURCE"),
]
```

### Create segment_analysis.py

Copy the full script from `references/segment_analysis.py`.

### Create .env

Create `.env` file with the user's API key:

```
INTELLIGEMS_API_KEY=<user's key here>
```

### Install Dependencies

```bash
pip install requests python-dotenv tabulate
```

---

## Step 3: Run Analysis

```bash
python segment_analysis.py
```

---

## Step 4: Interpret Results

**Status meanings:**
- **Doing well** - Variant beating control with 80%+ confidence
- **Not doing well** - Control beating variant with 80%+ confidence
- **Inconclusive** - Not enough confidence either way
- **Too early** - Test running less than 2 weeks (don't trust yet)
- **Low data** - Not enough orders to calculate confidence

**Example output:**

```
======================================================================
  Homepage Price Test
   Runtime: 21 days | Visitors: 45,000 | Orders: 320
======================================================================

📱 BY DEVICE
╭─────────┬──────────┬────────┬───────────┬─────────────┬──────────┬────────────╮
│ Segment │ Visitors │ Orders │ Variation │ Status      │ RPV Lift │ Confidence │
├─────────┼──────────┼────────┼───────────┼─────────────┼──────────┼────────────┤
│ Mobile  │   32,000 │    180 │ +5%       │ Doing well  │ +12.3%   │ 87%        │
│ Desktop │   13,000 │    140 │ +5%       │ Inconclusive│ +4.2%    │ 62%        │
╰─────────┴──────────┴────────┴───────────┴─────────────┴──────────┴────────────╯
```

This shows the +5% price variant is winning on mobile (87% confidence) but inconclusive on desktop.

---

## Troubleshooting

**"INTELLIGEMS_API_KEY not found"**
- Ensure `.env` file exists with the key
- Or export: `export INTELLIGEMS_API_KEY=your_key`

**"No active experiments found"**
- Check that experiments have status "started" in Intelligems dashboard

**"Error fetching experiments"**
- Verify API key is correct
- Check network connection

---

## References

- `references/segment_analysis.py` - Full analysis script
- `references/config.py` - Configuration file
- `references/setup-guide.md` - Detailed setup instructions
