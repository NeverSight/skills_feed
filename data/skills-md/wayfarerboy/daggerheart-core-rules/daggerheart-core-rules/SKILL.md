---
name: daggerheart-core-rules
description: Comprehensive guide to the Daggerheart Tabletop Roleplaying Game (TTRPG). Use this skill when users ask questions about Daggerheart rules, character creation, classes, gameplay mechanics, GM guidance, adversaries, or lore.
---

# Daggerheart Core Rules Skill

This skill allows you to answer questions about the Daggerheart RPG by referencing the Core Rulebook.

## Rulebook Structure

The rulebook is organized into several main markdown files in `references/`.

### Directory Map

- **Introduction & Principles** (`references/01_introduction_and_principles.md`)
- **Character Creation** (`references/02_character_creation.md`)
- **Core Mechanics** (`references/03_core_mechanics.md`)
- **Equipment** (`references/04_equipment.md`)
- **Running the Game (GM Guide)** (`references/05_running_the_game_gm_guide.md`)
- **Adversaries & Environments** (`references/06_adversaries_and_environments.md`)
- **Campaign Frames** (`references/07_campaign_frames.md`)
- **Appendix & Reference** (`references/08_appendix_and_reference.md`)

## Advanced Workflows

For complex GM scenarios, consult the specialized guides in `references/workflows/`:

1.  **Character Analysis** (`character_logic.md`): Use for questions about specific PC/NPC builds, class feature interactions, or conflicting rules.
2.  **Worldbuilding & Narrative** (`worldbuilding.md`): Use for creating custom locations, lore questions, or describing scenes with Daggerheart flavor.
3.  **Adversary Tactics** (`adversary_tactics.md`): Use for questions about monster behavior, combat balance, or running encounters.
4.  **GM Improvisation** (`gm_improv.md`): Use when the GM needs help reacting to unexpected player choices, "failing forward," or redirecting the plot.
5.  **Combat Orchestration** (`combat_orchestration.md`): Use for managing the Action Tracker, range bands, and the spotlight during combat.
6.  **Leveling & Multiclassing** (`leveling_multiclassing.md`): Use for character advancement, trait upgrades, and multiclassing rules.
7.  **Session Zero & Planning** (`session_zero_planning.md`): Use for starting campaigns, setting safety tools, and collaborative worldbuilding.

## How to Use

1.  **Identify the Intent:**
    *   **Simple Rule Lookup:** Proceed to step 2 (Search References).
    *   **Complex Scenario:** Match the request to one of the "Advanced Workflows" above and follow its steps.
2.  **Search References:**
    - Use `search_file_content` to find specific keywords across the relevant reference files (e.g., search "Stress" in `references/03_core_mechanics.md`).
3.  **Read Context:** Read the relevant files to understand the rules. Information often spans multiple pages.
4.  **Cite Page Numbers:** Always include the page number in your response. Page numbers can be identified by the `<!-- PAGE_START: XXX -->` markers within the main reference files. Format citations as `(p. XXX)`.

## Style Guide

- **Citations:** Every rule or piece of lore you quote should be followed by a page citation, e.g., "Duality Dice consist of a Hope die and a Fear die (p. 090)."
- **Terminology:** Use exact game terms (e.g., "Hope Die", "Fear Die", "Action Tracker", "Experiences").
- **Mechanics:** When explaining mechanics, be precise about dice rolls, modifiers, and resource costs.
- **Lore:** Distinguish between "flavor text" and actual mechanics.
