---
name: symmetry-group-identifier
description: Use when you've identified candidate symmetries and need to map them to mathematical groups for architecture design. Invoke when user mentions cyclic groups, dihedral groups, Lie groups, SO(3), SE(3), permutation groups, or needs to formalize symmetries into group theory language. Provides taxonomy and mathematical foundations from Visual Group Theory principles.
---

# Symmetry Group Identifier

## What Is It?

This skill helps you **map identified symmetries to mathematical groups**. Once you know what transformations should leave your predictions unchanged, this skill formalizes them into the language of group theory.

**Why groups matter**: Neural network architectures are built around specific symmetry groups. Knowing your group tells you exactly which architecture patterns to use.

## Workflow

Copy this checklist and track your progress:

```
Group Identification Progress:
- [ ] Step 1: List symmetries from discovery phase
- [ ] Step 2: Classify each as discrete or continuous
- [ ] Step 3: Match to specific groups using taxonomy
- [ ] Step 4: Determine how groups combine
- [ ] Step 5: Verify group properties
- [ ] Step 6: Document final group specification
```

**Step 1: List symmetries from discovery phase**

Gather the identified symmetries from the discovery phase. List each identified transformation and whether it requires invariance or equivariance. Note confidence levels. If symmetries haven't been discovered yet, work with user to identify them through domain analysis first.

**Step 2: Classify each as discrete or continuous**

For each symmetry, determine: Is the transformation set finite (discrete) or infinite (continuous)? Discrete examples: 90° rotations (4 elements), permutations of n items (n! elements). Continuous examples: rotation by any angle, translation by any distance. Use [Group Taxonomy](#group-taxonomy) to guide classification. For mathematical foundations, see [Group Theory Primer](./resources/group-theory-primer.md).

**Step 3: Match to specific groups using taxonomy**

Use the [Discrete Groups](#discrete-groups) and [Continuous Groups](#continuous-groups-lie-groups) reference sections. Identify the specific group name and notation for each symmetry. Common matches: n-fold rotation → Cₙ, rotation+reflection → Dₙ, permutation → Sₙ, 3D rotation → SO(3), rigid motion → SE(3), full Euclidean → E(3). For detailed Lie group information (SO(3), SE(3), E(3)), consult [Lie Groups Reference](./resources/lie-groups.md).

**Step 4: Determine how groups combine**

If multiple symmetries are present, determine how they combine. Direct product (G × H): symmetries act independently. Semidirect product (G ⋊ H): one symmetry "twists" the other (e.g., SE(3) = SO(3) ⋊ ℝ³). Use [Combining Groups](#combining-groups) reference.

**Step 5: Verify group properties**

Check that identified structure satisfies group axioms: closure, associativity, identity, inverses. Verify important properties: Is it compact? (affects representation theory). Is it abelian? (commutative or not). Is it connected? (affects implementation). Use [Group Properties Checklist](#group-properties-checklist). For detailed verification methodology, see [Methodology](./resources/methodology.md).

**Step 6: Document final group specification**

Create specification using [Output Template](#output-template). Include: group name/notation, dimension/size, key properties, invariance vs equivariance requirements, and recommended architecture family. This specification provides the foundation for architecture design. Quality criteria for this output are defined in [Quality Rubric](./resources/evaluators/rubric_group_identification.json).

## Group Taxonomy

### Overview Diagram

```
                    SYMMETRY GROUPS
                          │
          ┌───────────────┴───────────────┐
          │                               │
     DISCRETE                        CONTINUOUS
          │                          (Lie Groups)
          │                               │
    ┌─────┼─────┐               ┌────────┼────────┐
    │     │     │               │        │        │
  Cyclic Dihedral Symmetric   SO(n)   SE(n)    E(n)
   Cₙ     Dₙ      Sₙ         rotations rigid   Euclidean
                              only    motions  (w/ reflect)
```

### Quick Reference Table

| Symmetry Type | Group | Notation | Elements | Common Use |
|---------------|-------|----------|----------|------------|
| n-fold rotation | Cyclic | Cₙ | n | Image rotation (90°, 60°) |
| Rotation + reflection | Dihedral | Dₙ | 2n | Regular polygons |
| Permutation | Symmetric | Sₙ | n! | Sets, graphs |
| 2D rotation (continuous) | Special orthogonal | SO(2) | ∞ | Continuous rotation |
| 3D rotation | Special orthogonal | SO(3) | ∞ | 3D orientation |
| 3D rigid motion | Special Euclidean | SE(3) | ∞ | Robotics, molecules |
| 3D with reflections | Euclidean | E(3) | ∞ | Chemistry, physics |

## Discrete Groups

### Cyclic Groups (Cₙ)

**What they represent**: Rotations by multiples of 360°/n

**Elements**: {e, r, r², ..., rⁿ⁻¹} where rⁿ = e (identity)

| Group | Rotations | Example |
|-------|-----------|---------|
| C₂ | 0°, 180° | Playing cards |
| C₄ | 0°, 90°, 180°, 270° | Square images |
| C₆ | 60° increments | Hexagonal patterns |

**Use when**: Rotation symmetry present but NOT reflection symmetry.

### Dihedral Groups (Dₙ)

**What they represent**: Rotations + reflections of regular n-gon

**Elements**: n rotations + n reflections = 2n total

| Group | Elements | Example |
|-------|----------|---------|
| D₄ | 8 | Square with diagonals (p4m group) |
| D₆ | 12 | Regular hexagon |

**Use when**: Both rotation AND reflection symmetry present.

### Symmetric Groups (Sₙ)

**What they represent**: All permutations of n elements

**Elements**: n! permutations

**Use when**: Element ordering is arbitrary (sets, graphs, point clouds).

## Continuous Groups (Lie Groups)

### SO(2) - 2D Rotations

**Elements**: Rotation by any angle θ ∈ [0, 2π)

**Matrix form**: R(θ) = [[cos θ, -sin θ], [sin θ, cos θ]]

**Use when**: Continuous rotation symmetry in 2D.

### SO(3) - 3D Rotations

**Elements**: All rotations in 3D (3 degrees of freedom)

**Representations**: Rotation matrices, quaternions, Euler angles, axis-angle

**Use when**: 3D orientation doesn't matter, but handedness does.

### SE(3) - 3D Rigid Motions

**Elements**: Rotations + Translations in 3D

**Structure**: SE(3) = SO(3) ⋊ ℝ³ (semidirect product)

**Use when**: Objects can be anywhere and in any orientation, handedness matters.

### E(3) - Full Euclidean Group

**Elements**: SE(3) + Reflections

**Structure**: E(3) = O(3) ⋊ ℝ³

**Use when**: SE(3) symmetry PLUS reflection symmetry (most molecules).

### Group Hierarchy

```
E(3) = O(3) ⋊ ℝ³
    │ exclude reflections
    ▼
SE(3) = SO(3) ⋊ ℝ³
    │ exclude translations
    ▼
SO(3)
    │ 2D restriction
    ▼
SO(2)
```

## Combining Groups

### Direct Product (G × H)

**When to use**: Symmetries act independently (neither affects the other).

**Example**: Image with separate translation and color permutation → SE(2) × S₃

**Property**: (g₁, h₁) · (g₂, h₂) = (g₁g₂, h₁h₂)

### Semidirect Product (G ⋊ H)

**When to use**: One symmetry "twists" the other (don't commute).

**Example**: SE(3) = SO(3) ⋊ ℝ³ (rotating then translating ≠ translating then rotating)

**Common cases**: SE(n) = SO(n) ⋊ ℝⁿ, E(n) = O(n) ⋊ ℝⁿ, Dₙ = Cₙ ⋊ C₂

## Group Properties Checklist

For your identified group, verify:

| Property | Question | Why It Matters |
|----------|----------|----------------|
| Compact | Is the group "bounded"? | Affects representation theory |
| Abelian | Does order matter? (g₁g₂ = g₂g₁?) | Simplifies architecture |
| Connected | Is group in one piece? | Affects irreducible representations |
| Finite | Finite number of elements? | Discrete vs continuous architecture |

## Group Selection by Domain

| Domain | Typical Group | Notes |
|--------|--------------|-------|
| 2D Image Classification | C₄ or D₄ | p4 or p4m groups |
| 3D Molecular Energy | E(3) × Sₙ | Full Euclidean + atom permutation |
| 3D Molecular Chirality | SE(3) × Sₙ | No reflections |
| Point Cloud Classification | SO(3) × Sₙ | Rotation + permutation |
| Graph Classification | Sₙ | Permutation invariant |
| Robotics | SE(3) | Sometimes with gravity constraint |

## Output Template

```
SYMMETRY GROUP SPECIFICATION
============================

Identified Symmetries:
1. [Symmetry] → Group: [name] ([notation])
2. [Symmetry] → Group: [name] ([notation])

Combined Group Structure:
- Full group: [G₁ × G₂] or [G₁ ⋊ G₂]
- Size: [# elements] or [continuous]

Group Properties:
- Compact: [Yes/No]
- Abelian: [Yes/No]
- Connected: [Yes/No]

Symmetry Requirements:
- [Group]: [Invariant/Equivariant] for [task type]

Recommended Architecture Family:
- [Architecture] supporting [group]

NEXT STEPS:
- Empirically validate symmetry hypotheses if not yet confirmed
- Design equivariant architecture based on group specification
```
