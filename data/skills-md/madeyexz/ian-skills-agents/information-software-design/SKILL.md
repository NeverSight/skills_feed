---
name: information-software-design
description: Design principles from Bret Victor's "Magic Ink" for building information software. Use when designing dashboards, search results, calendars, finance apps, or any interface where users seek answers rather than manipulate objects. Ask "what can the user learn?" not "what can the user do?"
license: MIT
metadata:
  author: madeyexz
  version: "1.0.0"
---

# Information Software Design

A skill for designing information software based on Bret Victor's "Magic Ink" principles.

Use this skill when the user is designing or building software where the primary purpose is to help users **learn, understand, compare, and make decisions** - such as dashboards, search results, calendars, finance apps, recommendation systems, listings, or any interface where users seek answers rather than manipulate objects.

## How to Use This Skill

When helping the user design information software:

### Step 1: Identify What the User Wants to Learn

Start by asking: **"What questions is the user trying to answer?"**

Don't ask "what features should it have" or "what can the user do." Instead:

- What decisions is she trying to make?
- What comparisons does she need to draw?
- What conclusions is she seeking?

**Example questions for a movie listings app:**
- What movies are showing today, at which times?
- What movies are showing around a *particular* time?
- Are they good? What are they about?

**Example questions for a calendar app:**
- What do I have planned tonight?
- What are my friends doing?
- How does my work pattern look before milestones?

### Step 2: Design Context-Sensitive Information

The core insight: **Information software design is the design of context-sensitive graphics.**

Software should infer context from three sources (in order of preference):

#### 1. Environment (Best - No Interaction Required)
- **Date/time**: "Now" and "soon" are almost always the most relevant
- **Location**: "Here" is the most interesting spatial landmark
- **Physical environment**: Weather, traffic, nearby events
- **Other open software**: What websites, documents, emails are open?
- **Email/messages**: Names, addresses, topics in recent correspondence
- **Documents being created**: Writing about Egypt? "Cats" means ancient feline worship

#### 2. History (Good - Minimal Interaction)
- **Last-value predictors**: Show what the user looked at last time
- **Learning predictors**: Find patterns (always checks SF-bound trains in morning, Berkeley-bound in evening)
- **Collaborative filtering**: What did similar users find valuable? (Netflix, Amazon)
- **Velocity through data space**: Grand Canyon yesterday, Vegas today → suggest LA tomorrow

#### 3. Interaction (Last Resort - Maximize Information Per Click)
If interaction is unavoidable:
- **Graphical manipulation**: Show maps instead of address dropdowns, calendars instead of date pickers
- **Relative navigation**: Let users *correct* predictions, not *construct* from scratch
- **Tight feedback loops**: Every interaction should immediately update the display

### Step 3: Show the Data

Apply Edward Tufte's first rule: **Show the data.**

Ask: Does this interface present enough information to answer the user's questions?

**Anti-pattern (Amazon 2006):**
- Shows title, author, price
- Missing: Is it appropriate? Is it good? Table of contents, ratings distribution, reviews

**Better pattern:**
- Synopsis and table of contents (appropriateness)
- Ratings with distribution whiskers (quality + trustworthiness)
- All comparable by eye on single page (no memory required)

### Step 4: Arrange Data Spatially

Use the two spatial dimensions meaningfully.

**Anti-pattern (Yahoo Movies 2006):**
- Lists theaters alphabetically
- Forces user to scan, extract, mentally merge showtimes

**Better pattern:**
- Movies along one axis, times along another
- Eye can scan vertically to find all movies at a time
- Eye can scan horizontally to find all times for a movie

**Key principle**: Compare by *eye* (spatial), not by *memory* (temporal navigation)

### Step 5: Minimize Excise

**Excise** = effort demanded by the tool not directly in pursuit of the goal.

Navigation is almost always pure excise. The user doesn't want to navigate; she wants answers.

**Reduce excise by:**
- Using text weight/color to make critical info stand out
- Keeping content width to an eyespan for vertical scanning
- Eliminating unnecessary clicks (if click anywhere would mean "show details", make anywhere clickable)
- Removing state that users must track mentally

---

## Design Checklist

When reviewing an information software design:

- [ ] **Questions Answered**: Does the interface answer the user's actual questions without additional clicks?
- [ ] **Context Inferred**: Is the software using environment/history to predict context, or forcing the user to specify everything?
- [ ] **Spatial Arrangement**: Are the two dimensions used to reveal relationships, or just aesthetics?
- [ ] **Compare by Eye**: Can the user compare options visually, or must she navigate and remember?
- [ ] **Minimal Interaction**: Is interaction used only when environment and history are insufficient?
- [ ] **Graphical Manipulation**: Are controls domain-appropriate (maps for locations, calendars for dates)?
- [ ] **Feedback Loops**: Does every interaction immediately update the display?
- [ ] **No Excise**: Is there any navigation that doesn't directly serve learning?

---

## Common Mistakes to Avoid

### Mistake 1: Designing a Machine Instead of a Medium
Software designers often ask "What functions must it perform?" instead of "What will it look like?"

**Fix**: Start with the graphic design. What information appears? How is it arranged? The interaction model comes last.

### Mistake 2: Treating Navigation as Acceptable
If users are clicking through multiple screens to find answers, the design has failed.

**Fix**: Show more information upfront. Use context to filter. Make a single screen answer the question.

### Mistake 3: Uniform Visual Weight
When everything looks the same, nothing stands out.

**Fix**: Use typography, color, and whitespace to create hierarchy. Critical info in bold, supplementary info in grey.

### Mistake 4: Data Space as a Maze
Stateful software where users can "get lost" creates anxiety.

**Fix**: Reduce state. Make it trivial to return to sensible starting points. Navigation should be *correction*, not *construction*.

### Mistake 5: Interaction Without Feedback
If clicking a button doesn't immediately change what the user sees, the interaction is meaningless.

**Fix**: Every interaction should produce visible change to a context-sensitive graphic.

---

## The Fundamental Shift

**Old mindset**: "What can the user *do* with this software?"

**New mindset**: "What can the user *learn* from this software?"

Most software exists to help people learn:
- Calendar: Learn what to do when
- Finance app: Learn spending patterns and make decisions
- Search results: Learn what's available and choose
- Email: Keep mental models up-to-date (projects, conversations, relationships)

When you approach design this way, interaction becomes a last resort, and the primary challenge becomes: **How do I present this information so clearly that the user's questions are answered at a glance?**

---

## Source

Based on Bret Victor's "Magic Ink: Information Software and the Graphical Interface" (2006)
http://worrydream.com/MagicInk/
