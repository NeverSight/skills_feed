---
version: 1.0.0
name: prd-creator
description: Create comprehensive Product Requirements Documents (PRDs) combining Shape Up methodology, Amazon's Working Backwards approach, and traditional PRD practices. Use when users want to create detailed PRDs with appetite setting, rabbit hole identification, press releases, customer quotes, FAQs, and complete product specifications.
location: user
license: MIT
---

# PRD Creator Skill

Create comprehensive PRDs that combine the best of Shape Up methodology, Amazon's Working Backwards approach, and traditional PRD practices.

## When to Use

- Starting a new product or feature
- Defining scope and constraints for a project
- Preparing for a "bet" (Shape Up terminology)
- Needing a complete product specification
- Wanting to identify risks and rabbit holes early

## The 12-Section PRD Framework

### 1. Product Overview
- Project title and version
- One-line description
- Executive summary

### 2. Working Backwards (Amazon Style)
- Press release headline
- Customer quote (delighted user)
- Internal quote (team perspective)
- Call to action

### 3. Problem Definition
- Surface problem (what users say)
- Five Whys analysis (root cause)
- Job to be done
- Current workarounds
- Why this matters now

### 4. Appetite & Constraints (Shape Up)
- Time budget (2-week small batch or 6-week big batch)
- Bet type and team size
- Must Have (P0), Nice to Have (P1), Won't Have (P2)
- Trade-off priorities

### 5. Solution Shape
- Solution overview (fat marker sketch level)
- Key elements
- What we're NOT building (critical for scope control)

### 6. Boundaries & Rabbit Holes
- Out of bounds (explicit exclusions)
- Known rabbit holes (complexity warnings)
- Dependencies
- Mitigation strategies

### 7. Goals & Anti-Goals
- Business goals
- User goals
- Anti-goals (what we're intentionally not solving)
- Success definition

### 8. Customer & Users
- Primary persona
- Secondary personas
- User journey
- Frequency of use

### 9. FAQ Section
- External FAQs (customer questions)
- Internal FAQs (stakeholder questions)
- Technical FAQs (implementation questions)

### 10. Success Metrics
- North Star metric
- Leading indicators (early signals)
- Lagging indicators (outcome metrics)
- Counter metrics (watch-outs)
- Definition of done
- Kill criteria (when to stop)

### 11. Technical Approach
- Architecture overview
- Key technical decisions
- Security considerations
- Performance requirements
- Integration points

### 12. Betting Table Decision
- Why this now (opportunity cost)
- Expected return
- Confidence level (1-10)
- Kill criteria

## The Conversation Process

The PRD creation follows a slot-filling conversation:

1. **Initiate** - Project name, version, press release headline, core problem
2. **Problem Exploration** - Five Whys analysis to reach root cause
3. **Set Appetite** - Time budget and constraints before solutions
4. **Shape Solution** - Broad strokes, not pixel-perfect
5. **Identify Rabbit Holes** - Proactive complexity identification
6. **Working Backwards** - Customer quotes and FAQs
7. **Define Success** - Metrics and kill criteria
8. **Make the Bet** - Justify the investment

## Slot Map Structure

```json
{
  "Product Overview": {
    "Project Title": "",
    "Version Number": "",
    "One-Line Description": "",
    "Executive Summary": ""
  },
  "Working Backwards": {
    "Press Release Headline": "",
    "Customer Quote": "",
    "Internal Quote": "",
    "Call to Action": ""
  },
  "Problem Definition": {
    "Surface Problem": "",
    "Five Whys Analysis": {
      "Why 1": "",
      "Why 2": "",
      "Why 3": "",
      "Why 4": "",
      "Why 5": ""
    },
    "Root Cause": "",
    "Jobs to be Done": "",
    "Current Workarounds": "",
    "Why This Matters Now": ""
  },
  "Appetite & Constraints": {
    "Time Budget": "",
    "Bet Type": "",
    "Team Size": "",
    "Must Have (P0)": [],
    "Nice to Have (P1)": [],
    "Won't Have (P2)": [],
    "Trade-off Priorities": []
  },
  "Solution Shape": {
    "Solution Overview": "",
    "Key Elements": [],
    "Fat Marker Sketches": "",
    "Breadboard Description": "",
    "What We're NOT Building": []
  },
  "Boundaries & Rabbit Holes": {
    "Out of Bounds": [],
    "Known Rabbit Holes": [],
    "Complexity Warnings": [],
    "Dependencies": [],
    "Mitigation Strategies": []
  },
  "Goals & Anti-Goals": {
    "Business Goals": [],
    "User Goals": [],
    "Anti-Goals": [],
    "Success Definition": ""
  },
  "Customer & Users": {
    "Primary Persona": "",
    "Secondary Personas": [],
    "User Journey": "",
    "Frequency of Use": ""
  },
  "FAQ Section": {
    "External FAQs": [{"Q": "", "A": ""}],
    "Internal FAQs": [{"Q": "", "A": ""}],
    "Technical FAQs": [{"Q": "", "A": ""}]
  },
  "Success Metrics": {
    "North Star Metric": "",
    "Leading Indicators": [],
    "Lagging Indicators": [],
    "Counter Metrics": [],
    "Definition of Done": ""
  },
  "Technical Approach": {
    "Architecture Overview": "",
    "Key Technical Decisions": [],
    "Security Considerations": "",
    "Performance Requirements": "",
    "Integration Points": []
  },
  "Betting Table Decision": {
    "Why This Now": "",
    "Opportunity Cost": "",
    "Expected Return": "",
    "Confidence Level": "",
    "Kill Criteria": []
  }
}
```

## Final PRD Template

```markdown
# PRD: {project_title}

## Executive Summary
**Version:** {version_number}  
**Headline:** {press_release_headline}  
**One-liner:** {one_line_description}

{executive_summary}

## The Problem

### What We Heard
"{surface_problem}"

### Root Cause Analysis (5 Whys)
1. Why? {why_1}
2. Why? {why_2}
3. Why? {why_3}
4. Why? {why_4}
5. Why? {why_5}

**Root Cause:** {root_cause}

### Job to be Done
{jobs_to_be_done}

### Current Workarounds
{current_workarounds}

## The Appetite

**Time Budget:** {time_budget}  
**Bet Type:** {bet_type}  
**Team Size:** {team_size}

### Priorities
**Must Have (P0):**
{must_have_list}

**Nice to Have (P1):**
{nice_to_have_list}

**Won't Have (P2):**
{wont_have_list}

### Trade-offs
{trade_off_priorities}

## The Solution Shape

### Overview
{solution_overview}

### Key Elements
{key_elements}

### What We're NOT Building
{not_building_list}

## Boundaries & Rabbit Holes

### Known Complexity
{rabbit_holes_and_warnings}

### Mitigation
{mitigation_strategies}

## Working Backwards

### Press Release
**{press_release_headline}**

*"{customer_quote}"* - Happy Customer

*"{internal_quote}"* - Product Team

**{call_to_action}**

### FAQs
{all_faqs_formatted}

## Success Criteria

### North Star
{north_star_metric}

### Definition of Done
{definition_of_done}

### Kill Criteria
{kill_criteria}

## The Bet

### Why Now?
{why_this_now}

### Confidence Level
{confidence_level}/10

### Expected Return
{expected_return}
```

## Key Principles

1. **Start with the problem, not the solution** - Use Five Whys to reach root cause
2. **Set appetite before exploring solutions** - Time budget is a constraint, not an estimate
3. **Identify rabbit holes early** - Proactively flag complexity that could spiral
4. **Write from the customer's perspective** - Working backwards creates clarity
5. **Define clear success and kill criteria** - Know when to stop or pivot
6. **Make the bet explicit** - Justify why this deserves the time investment

## Usage

Invoke this skill when you need to create a comprehensive PRD. The skill will guide you through a conversational slot-filling process to gather all necessary information before generating the final document.

**Example prompts:**
- "Create a PRD for an AI-powered code review tool"
- "I need to define requirements for a mobile habit tracking app"
- "Help me write a product spec for a new payment feature"
