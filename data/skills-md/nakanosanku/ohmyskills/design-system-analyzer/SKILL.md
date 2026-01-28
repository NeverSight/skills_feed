---
name: design-system-analyzer
description: Analyze any website's UI style using ChromeDevTools to extract precise CSS tokens, animations, and interaction states. Handles complex sites and anti-bot measures by guiding the user. Triggers on "analyze this site", "extract UI style", "create design system from [URL]", or "learn visual style".
---
# Design System Analyzer

Analyze websites via ChromeDevTools to extract deep CSS logic (keyframes, transitions, tokens) and generate comprehensive Design System System Prompts.

## Critical Rules

1. **MUST** output the final prompt using EXACTLY the structure in `references/design-system-template.md`
2. **MUST** limit extraction data to prevent context overflow (see analysis-guide.md for limits)
3. **MUST** fill ALL template placeholders with extracted or observed values
4. **NEVER** skip sections - use "Not observed" if data unavailable

## Best Practice: Use Your Own Chrome

For the best experience (no CAPTCHAs, shared login cookies), advise the user to run Chrome with:
`chrome.exe --remote-debugging-port=9222`
(See **[references/setup-guide.md](references/setup-guide.md)** for details)

---

## Workflow Overview

```
[1. Navigate] → [2. Anti-Bot Check] → [3. Deep Extraction] → [4. Synthesize to Template]
```

**IMPORTANT**: Do NOT take screenshots. Screenshots consume excessive context and are unnecessary - all visual data is extracted from CSS.

---

## Step 1: Navigate & Anti-Bot Check

```
mcp__chrome-devtools__navigate_page (url: "<target-url>")
```

**Immediately check for bot challenges:**

```javascript
() => {
  const text = document.body.innerText.toLowerCase();
  const title = document.title.toLowerCase();
  if (text.includes('cloudflare') || text.includes('verify you are human') || title.includes('just a moment')) {
    return 'CHALLENGE_DETECTED';
  }
  return 'OK';
}
```

**IF CHALLENGE_DETECTED**:
1. **PAUSE** all actions.
2. Tell the user: "Bot protection detected. Please manually solve the CAPTCHA in the browser, then confirm here."
3. Wait for user confirmation before proceeding.

---

## Step 2: Deep CSS Extraction

Run the extraction scripts from `references/analysis-guide.md` **in order**:

| Order | Script | Purpose | Max Items |
|-------|--------|---------|-----------|
| 1 | CSS Variables & Tokens | Colors, spacing, typography variables | 50 tokens |
| 2 | Animation & Keyframes | @keyframes, animation usage, transitions | 10 KF, 15 trans |
| 3 | Interaction States | :hover, :focus, :active rules | 15 rules |
| 4 | Typography | Font stacks from key elements | 7 elements |
| 5 | Layout & Spacing | Border radius, gaps, shadows | 5 each |
| 6 | Tech Stack | Framework detection | - |

**IMPORTANT**: Each script has built-in limits. Do NOT modify to extract more data.

---

## Step 3: Synthesize to Template

**MANDATORY**: Generate output using EXACTLY the template structure from `references/design-system-template.md`.

### Template Mapping Table

| Extracted Data | Template Section | Notes |
|----------------|------------------|-------|
| `tokens.colors` | `Design Token System > Colors` | Format as table |
| `tokens.spacing` | `Spacing, Radius & Borders` | Include radius values |
| `tokens.typography` | `Typography` | Include font stacks |
| Typography script | `Typography > Font Stacks, Type Scale` | Computed styles |
| `keyframes` | `Animation & Motion > Key Animations` | Full keyframe definitions |
| `animationUsage` | `Animation & Motion > Timing` | Duration, easing |
| `transitions` | `Animation & Motion > Timing` | Common patterns |
| `interactions` | `Component Styling > State Transitions` | Hover/focus effects |
| Layout sampler | `Layout Principles` | Spacing system |
| Tech stack | `Implementation Notes` | Tailwind/CSS notes |

### Output Format Checklist

Before outputting, verify ALL these sections are present:

- [ ] `<role>` block (copy exactly from template)
- [ ] `<design-system>` wrapper
- [ ] `## Design Philosophy` with Core Principles, Vibe, Historical Context
- [ ] `## Design Token System` with Colors table, Typography, Spacing
- [ ] `## Component Styling Principles` with Buttons, Cards, Form Inputs
- [ ] `## Layout Principles` with Spacing System, Grid, Responsive
- [ ] `## The "Signature" Factor` with 3 mandatory elements
- [ ] `## Animation & Motion` with Philosophy, Timing, Key Animations
- [ ] `## Accessibility Constraints`
- [ ] `## Anti-Patterns` with Visual and Interaction no-nos
- [ ] `## Implementation Notes` with tech-specific guidance
- [ ] `## Aesthetic Checklist` with 4 verification items
- [ ] Closing `</design-system>`

---

## Resources

- **[references/design-system-template.md](references/design-system-template.md)**: The REQUIRED output template
- **[references/analysis-guide.md](references/analysis-guide.md)**: Deep extraction scripts with context limits
- **[references/setup-guide.md](references/setup-guide.md)**: Guide for reusing user's Chrome
