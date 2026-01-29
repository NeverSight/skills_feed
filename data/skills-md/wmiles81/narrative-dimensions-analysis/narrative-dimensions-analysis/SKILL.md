---
name: narrative-dimensions-analysis
description: Physics-inspired story analysis system that treats narrative as trajectories through dimensional space. Tracks dimensions like intimacy, trust, power, and stakes to calculate tension, validate pacing, and diagnose story problems. Genre-aware with formulas for romance, thriller, mystery, and fantasy. Use when analyzing story structure, engineering tension, validating character arcs, diagnosing pacing issues, or generating dimensional targets for scenes.
# Narrative Dimensions Analysis System
---

A physics-inspired approach to story analysis that treats narrative as movement through multidimensional phase space.

## Quick Start

For immediate analysis, specify:
1. **Content level**: concept, outline, chapter, book, or series
2. **Genre**: romance, dark-romance, thriller, mystery, sci-fi, fantasy, or hybrid
3. **What to analyze**: structure, pacing, tension, character arcs, or full diagnostic

## Core Concept

Stories exist as trajectories through N-dimensional space where each dimension represents an independent narrative variable. Tension and other dramatic qualities emerge from the configuration of these dimensions.

**State Vector**: `s(t) = [intimacy, power_diff, info_asym, alignment, proximity, vulnerability, desire, stakes, trust]`

## Basis Dimensions (Independent Variables)

### Primary Dimensions (0-10 scale unless noted)

1. **INTIMACY** - Emotional closeness between characters
2. **POWER_DIFFERENTIAL** - Agency imbalance (-5 to +5, where 0 = balanced)
3. **INFORMATION_ASYMMETRY** - Knowledge gaps between characters
4. **GOAL_ALIGNMENT** - How much characters want the same thing
5. **PHYSICAL_PROXIMITY** - Literal spatial distance
6. **VULNERABILITY** - Emotional walls up/down state
7. **DESIRE** - Attraction/pull between characters
8. **STAKES** - Magnitude of consequences
9. **TRUST** - Belief in other's reliability

### Secondary Dimensions (genre-specific)

- **DANGER** - Physical threat level (thriller/suspense)
- **MYSTERY** - Unknown elements to reader (mystery/thriller)
- **WORLD_COMPLEXITY** - Setting intricacy (fantasy/sci-fi)
- **SOCIAL_PRESSURE** - External judgment (contemporary romance)
- **MORAL_AMBIGUITY** - Ethical grayness (dark romance)

## Emergent Properties (Calculated)

### Tension Formula

Base tension emerges from dimensional configuration:

```
TENSION = w₁(stakes) + w₂(info_asymmetry) + w₃(goal_misalignment) + 
          w₄(vulnerability - trust) + w₅(desire - proximity) + w₆(|power_diff|)
```

Genre-specific weights in `references/genre-weights.json`

### Other Emergent Properties

- **CONFLICT** = f(power_diff, goal_misalignment, desire with proximity deficit)
- **CHEMISTRY** = f(desire, proximity, vulnerability, productive info_asymmetry)
- **PACING** = ||ds/dt|| (velocity through phase space)
- **DRAMATIC_IRONY** = reader_info - character_info

## Analysis Procedures

### Structure Analysis

1. Map current dimensional configuration
2. Check genre constraint satisfaction
3. Identify trajectory patterns
4. Validate ending coordinates match genre requirements

### Pacing Diagnostic

Calculate velocity vector: `v(t) = ds/dt`

- **Stuck**: ||v|| ≈ 0 (no dimensional movement)
- **Rushed**: ||v|| > threshold (teleportation between states)
- **Optimal**: 2-3 dimensions shifting per unit

### Tension Engineering

To increase tension:
- Maximize (stakes - trust)
- Maximize (desire - proximity)
- Increase information asymmetry with high vulnerability
- Force proximity with misaligned goals

### Arc Validation

Check if dimensional changes are "earned":
- Each jump > 2 points needs catalyst event
- Trajectory must be continuous (no teleportation)
- Character growth shows across multiple dimensions

### The "Black Moment" Formula

Peak crisis configuration:
- Stakes → MAX
- Trust → MIN
- Goal Alignment → SHATTERED
- Desire → HIGH (maintains investment)

## Genre-Specific Configurations

See `references/genre-configs.md` for detailed patterns

### Quick Genre Templates

**Romance**: Must end at intimacy ≥ 8, trust ≥ 7
**Dark Romance**: Maintain power_diff fluctuation, high stakes throughout
**Thriller**: Danger + stakes high, trust variable
**Mystery**: Information asymmetry drives plot until revelation
**Enemies-to-Lovers**: Goal alignment slowest mover

## Diagnostic Outputs

### Scene-Level Analysis
- Current dimensional state
- Dimensional velocity (what's changing)
- Tension calculation
- Suggested adjustments

### Chapter-Level Analysis
- Dimensional trajectory map
- Pacing assessment
- Arc progression check
- Genre compliance status

### Book-Level Analysis
- Full phase space trajectory
- Character arc paths
- Pacing heat map
- Black moment validation
- Ending coordinate check

## Scripts

- `scripts/calculate_tension.py` - Compute tension from dimensional state
- `scripts/validate_trajectory.py` - Check if arc is properly earned
- `scripts/generate_report.py` - Create full dimensional analysis report

## References

- `references/genre-weights.json` - Tension formula weights by genre
- `references/genre-configs.md` - Detailed genre conventions and constraints
- `references/catalyst-events.md` - Events that justify dimensional jumps
- `references/diagnostic-patterns.md` - Common problems and solutions

## Usage Examples

### Diagnosing a Flat Scene
```python
# Current state shows no movement
state = {"intimacy": 5, "trust": 5, "stakes": 5, ...}
# All dimensions static = death
# Solution: Move 2-3 dimensions
```

### Planning Dark Romance Arc
```
Start: power_diff=+5, trust=0, stakes=10, desire=3
Mid: power_diff oscillates, trust climbs slowly, stakes high
End: power_diff=0, trust=8, stakes=personal, desire=10
```

### Engineering High Tension Chapter
```
Target configuration:
- Stakes: 9
- Trust: 2  
- Information Asymmetry: 8
- Vulnerability: 7
- Physical Proximity: 8 (forced closeness)
```

## Key Principles

1. **Stories are trajectories** - Not events but dimensional movement
2. **Tension emerges** - From configuration, not arbitrary assignment  
3. **Pacing is velocity** - How fast you move through phase space
4. **Genres constrain paths** - Not destinations but allowable trajectories
5. **Earned moments** - Require proper path integration, not jumps

Remember: The same kiss hits differently at intimacy=2 vs intimacy=8. Context is configuration.
