---
name: csv-data-summarizer
description: Analyzes CSV files and generates comprehensive summary statistics and visualizations using Python and pandas - automatically and immediately without asking what the user wants.
---

# CSV Data Summarizer

This skill analyzes CSV files and provides comprehensive summaries with statistical insights and visualizations.

## When to Use This Skill

Claude should use this skill whenever the user:
- Uploads or references a CSV file
- Asks to summarize, analyze, or visualize tabular data
- Requests insights from CSV data
- Wants to understand data structure and quality

## ⚠️ CRITICAL BEHAVIOR REQUIREMENT ⚠️

**DO NOT ASK THE USER WHAT THEY WANT TO DO WITH THE DATA.**
**DO NOT OFFER OPTIONS OR CHOICES.**
**DO NOT SAY "What would you like me to help you with?"**
**DO NOT LIST POSSIBLE ANALYSES.**

**IMMEDIATELY AND AUTOMATICALLY:**
1. Run the comprehensive analysis
2. Generate ALL relevant visualizations
3. Present complete results
4. NO questions, NO options, NO waiting for user input

**THE USER WANTS A FULL ANALYSIS RIGHT AWAY - JUST DO IT.**

## How It Works

The skill intelligently adapts to different data types by inspecting the data first, then determining what analyses are most relevant:

**Automatic Analysis Steps:**

1. **Load and inspect** - Read CSV into pandas DataFrame
2. **Identify structure** - Detect column types, dates, numerics, categories
3. **Determine analyses** - Adapt based on actual data content
4. **Generate visualizations** - Only those that make sense for this dataset
5. **Present complete output** - Everything in one comprehensive response

**Only creates visualizations that make sense:**
- Time-series plots ONLY if date/timestamp columns exist
- Correlation heatmaps ONLY if multiple numeric columns exist
- Category distributions ONLY if categorical columns exist
- Histograms for numeric distributions when relevant

## Behavior Guidelines

✅ **CORRECT APPROACH - SAY THIS:**
- "I'll analyze this data comprehensively right now."
- "Here's the complete analysis with visualizations:"
- Then IMMEDIATELY show the full analysis

❌ **NEVER SAY THESE PHRASES:**
- "What would you like to do with this data?"
- "Here are some common options:"
- "I can create a comprehensive analysis if you'd like!"
- Any sentence ending with "?" asking for user direction

❌ **FORBIDDEN BEHAVIORS:**
- Asking what the user wants
- Listing options for the user to choose from
- Waiting for user direction before analyzing
- Providing partial analysis that requires follow-up
- Describing what you COULD do instead of DOING it

## Usage

The skill provides a Python function `summarize_csv(file_path)` that returns comprehensive text summary with statistics and generates multiple visualizations automatically.

## Technical Details

**Dependencies:** python>=3.8, pandas>=2.0.0, matplotlib>=3.7.0, seaborn>=0.12.0

**Files:**
- `analyze.py` - Core analysis logic
- `requirements.txt` - Python dependencies
- `examples/` - Sample datasets for testing
