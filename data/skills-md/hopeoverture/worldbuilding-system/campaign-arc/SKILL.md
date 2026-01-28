---
name: campaign-arc
description: Track multi-session story arcs, plot threads, and campaign progression. Manages ongoing narratives, NPC relationships, party goals, and session continuity across multiple game sessions.
argument-hint: "[world] [--new|--status|--update|--session N]"
---

# Campaign Arc Tracker

Track campaign: $ARGUMENTS

## Overview

This skill manages long-running campaign narratives by tracking:
- **Story Arcs:** Multi-session plot threads with beginning, middle, and end
- **Plot Threads:** Individual storylines that weave through sessions
- **Party Goals:** What the players are working toward
- **NPC Relationships:** How NPCs feel about the party over time
- **Session Continuity:** Where things left off and what's pending
- **Foreshadowing:** Seeds planted for future reveals
- **Consequences:** Delayed effects of party actions

## Campaign State File

Campaign data is stored in `Worlds/[World Name]/.campaign-state.json`:

```json
{
  "version": "1.0",
  "world_name": "Eldermyr",
  "campaign_name": "The Shattered Crown",
  "party": {
    "members": ["Thorin", "Elara", "Marcus", "Zara"],
    "level": 5,
    "base_of_operations": "[[Aldersgate]]"
  },
  "current_session": 12,
  "session_log": [
    {
      "number": 12,
      "date": "2025-01-15",
      "location": "[[The Sunken Palace]]",
      "summary": "Explored underwater ruins, found ancient artifact",
      "cliffhanger": "Cultists arrived as party found the artifact"
    }
  ],
  "story_arcs": [],
  "plot_threads": [],
  "npc_relationships": {},
  "foreshadowing": [],
  "consequences": [],
  "last_updated": "ISO timestamp"
}
```

## Instructions

### Parse Arguments

| Command | Purpose |
|---------|---------|
| `[world]` | View campaign status for this world |
| `[world] --new` | Create new campaign tracker |
| `[world] --status` | Show full campaign dashboard |
| `[world] --update` | Update after a session |
| `[world] --session N` | View specific session details |
| `[world] --arc [name]` | View or create specific story arc |
| `[world] --thread [name]` | View or create specific plot thread |

---

## Creating a New Campaign (--new)

### Step 1: Campaign Basics

Ask the user:
> "Let's set up campaign tracking for [World Name]."
>
> 1. **Campaign Name:** What's this campaign called?
> 2. **Party Members:** Who are the player characters?
> 3. **Starting Level:** What level is the party?
> 4. **Base of Operations:** Where does the party call home?
> 5. **Campaign Hook:** What's the main premise or goal?

### Step 2: Initial Story Arc

Ask:
> "What's the main story arc the party is currently pursuing?"
>
> **Arc Name:** (e.g., "The Search for the Lost King")
> **Arc Goal:** What does completing this arc achieve?
> **Current Phase:** Beginning / Rising Action / Climax / Resolution
> **Key NPCs:** Who are the major players in this arc?
> **Key Locations:** Where does this arc take place?

### Step 3: Active Plot Threads

Ask:
> "What ongoing plot threads exist? List any subplots, side quests, or dangling mysteries."
>
> For each thread:
> - **Thread Name:** (e.g., "The Missing Merchant")
> - **Status:** Active / Dormant / Resolved
> - **Related Arc:** Which story arc does this connect to?
> - **Urgency:** Low / Medium / High / Critical
> - **Next Beat:** What happens next if players engage?

### Step 4: NPC Relationship Baseline

Ask:
> "List key NPCs and their current relationship with the party:"
>
> | NPC | Disposition | Reason |
> |-----|-------------|--------|
> | [[Lord Varic]] | Friendly | Party saved his daughter |
> | [[The Owl]] | Neutral | Hasn't met them yet |
> | [[High Confessor Maren]] | Hostile | Party exposed his corruption |

### Step 5: Save Campaign State

Create the `.campaign-state.json` file with all gathered information.

---

## Campaign Status Dashboard (--status)

Display comprehensive overview:

```
╔══════════════════════════════════════════════════════════════════╗
║              CAMPAIGN: The Shattered Crown                        ║
║              World: Eldermyr | Session: 12 | Party Level: 5       ║
╠══════════════════════════════════════════════════════════════════╣
║ PARTY                                                             ║
║ • Thorin (Dwarf Fighter)    • Elara (Elf Wizard)                 ║
║ • Marcus (Human Cleric)     • Zara (Halfling Rogue)              ║
║ Base: [[Aldersgate]]                                              ║
╠══════════════════════════════════════════════════════════════════╣
║ ACTIVE STORY ARCS                                                 ║
║ ┌─────────────────────────────────────────────────────────────┐  ║
║ │ [■■■■■□□□□□] The Shattered Crown (50% - Rising Action)      │  ║
║ │ [■■■□□□□□□□] The Cult of Shadows (30% - Beginning)          │  ║
║ └─────────────────────────────────────────────────────────────┘  ║
╠══════════════════════════════════════════════════════════════════╣
║ PLOT THREADS                                                      ║
║ 🔴 CRITICAL: The Ritual begins at the next full moon (2 sessions)║
║ 🟠 HIGH: [[The Owl]] requests a meeting                          ║
║ 🟡 MEDIUM: Missing merchant still unresolved                      ║
║ 🟢 LOW: Elara's family sword needs reforging                      ║
╠══════════════════════════════════════════════════════════════════╣
║ NPC RELATIONSHIPS                                                 ║
║ 😊 Friendly: [[Lord Varic]], [[Sister Elspeth]], [[Grom Smith]]  ║
║ 😐 Neutral: [[The Owl]], [[Captain Aldric]]                      ║
║ 😠 Hostile: [[High Confessor Maren]], [[The Crimson Hand]]       ║
╠══════════════════════════════════════════════════════════════════╣
║ FORESHADOWING (planted seeds)                                     ║
║ • Session 8: Strange symbol found in ruins (not yet revealed)    ║
║ • Session 10: NPC mentioned "the sleeper beneath" cryptically    ║
╠══════════════════════════════════════════════════════════════════╣
║ PENDING CONSEQUENCES                                              ║
║ • Session 9: Party killed the Baron's son - revenge coming       ║
║ • Session 11: Left cultist alive - he reported to superiors      ║
╠══════════════════════════════════════════════════════════════════╣
║ LAST SESSION (#12) CLIFFHANGER:                                   ║
║ "Cultists arrived as party found the artifact in the Sunken      ║
║  Palace. Roll initiative next session!"                           ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Post-Session Update (--update)

### Step 1: Session Summary

Ask:
> "Let's record Session [N+1]. What happened?"
>
> 1. **Date:** When was this session?
> 2. **Location(s):** Where did the party go?
> 3. **Summary:** What happened in 2-3 sentences?
> 4. **Major Events:** Any significant occurrences?
> 5. **Cliffhanger:** How did the session end?

### Step 2: Arc Progress

For each active story arc:
> "Did 'The Shattered Crown' arc progress?"
> - No change
> - Minor progress (moved forward slightly)
> - Major progress (completed a phase)
> - Resolved (arc complete!)
> - Complicated (new obstacles emerged)

### Step 3: Plot Thread Updates

> "Update plot thread status:"
>
> | Thread | Previous | New Status | Notes |
> |--------|----------|------------|-------|
> | Missing Merchant | Active | Resolved | Found him in dungeon |
> | The Ritual | Active | Critical | Only 2 sessions left! |

### Step 4: NPC Relationship Changes

> "Did any NPC relationships change?"
>
> - [[Lord Varic]]: Friendly → Grateful (party saved the city)
> - [[The Owl]]: Neutral → Suspicious (party broke into his office)

### Step 5: New Seeds

> "Any foreshadowing planted this session?"
>
> - What was hinted at?
> - What's the eventual reveal?
> - When might it pay off?

### Step 6: New Consequences

> "Any actions that will have future consequences?"
>
> - What did the party do?
> - What's the consequence?
> - When will it trigger?

### Step 7: Save Updates

Update `.campaign-state.json` with all new information.

---

## Story Arc Management (--arc)

### Creating a New Arc

```
/campaign-arc Eldermyr --arc "The Dragon's Return"
```

Ask:
> **Arc Name:** The Dragon's Return
> **Arc Type:** Main Quest / Side Quest / Character Arc / World Event
> **Description:** What's this arc about?
> **Phases:**
> 1. Beginning: What starts the arc?
> 2. Rising Action: What complications arise?
> 3. Climax: What's the pivotal moment?
> 4. Resolution: How might it end?
>
> **Connections:**
> - Related NPCs: [[list]]
> - Related Locations: [[list]]
> - Related Plot Threads: [[list]]

### Arc Progress Tracking

```
Arc: The Shattered Crown
Phase: Rising Action (2 of 4)
Progress: ████████░░░░░░░░░░░░ 40%

Milestones:
✓ Discovered the crown was shattered
✓ Found the first fragment
○ Find the second fragment
○ Find the third fragment
○ Reforge the crown
○ Crown the true heir
```

---

## Plot Thread Management (--thread)

### Creating a Thread

```
/campaign-arc Eldermyr --thread "The Poisoned Well"
```

Ask:
> **Thread Name:** The Poisoned Well
> **Type:** Mystery / Combat / Social / Exploration
> **Status:** Active
> **Urgency:** Medium
> **Related Arc:** (optional)
>
> **Thread Beats:**
> 1. Discovery: Village reports illness
> 2. Investigation: Clues point to old mine
> 3. Confrontation: Undead necromancer in mine
> 4. Resolution: Destroy phylactery, cure village
>
> **Current Beat:** 2 (Investigation)

### Thread Tracking

```
Active Threads: 5
─────────────────────────────────────────
🔴 The Ritual (CRITICAL) - 2 sessions until trigger
   Beat 3/4: Locate ritual site before full moon

🟠 The Owl's Request (HIGH) - Meeting scheduled
   Beat 1/3: Accept or decline the job

🟡 Missing Merchant (MEDIUM) - Dormant 3 sessions
   Beat 2/4: Follow leads to Trader's Rest

🟢 Elara's Sword (LOW) - Character goal
   Beat 1/3: Find the legendary smith

🟢 Haunted Lighthouse (LOW) - Optional side quest
   Beat 1/4: Hear rumors at tavern
```

---

## Integration with Other Skills

### With `/session-prep`
Campaign state informs session prep:
- Active plot threads become session focus options
- NPC relationships affect NPC behavior suggestions
- Pending consequences can trigger

### With `/random-encounter`
- NPC relationship status affects encounter tone
- Active plot threads can spawn related encounters

### With `/create-entity`
- New NPCs automatically added to relationship tracker
- New locations linked to active arcs

---

## Examples

```bash
# Create new campaign tracker
/campaign-arc Eldermyr --new

# View campaign dashboard
/campaign-arc Eldermyr --status

# Update after session 13
/campaign-arc Eldermyr --update

# View session 10 details
/campaign-arc Eldermyr --session 10

# Create new story arc
/campaign-arc Eldermyr --arc "The Dragon's Return"

# Create new plot thread
/campaign-arc Eldermyr --thread "The Missing Heir"

# Quick status check
/campaign-arc Eldermyr
```
