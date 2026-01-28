---
name: symmetry-discovery-questionnaire
description: Use when ML engineers need to identify symmetries in their data but don't know where to start. Invoke when user mentions data symmetry, invariance discovery, what transformations matter, or needs help recognizing patterns their model should respect. Works collaboratively through domain analysis, transformation testing, and physical constraint identification.
---

# Symmetry Discovery Questionnaire

## What Is It?

This skill helps you **discover hidden symmetries** in your data through a structured collaborative process. Symmetries are transformations that leave important properties unchanged - and building them into neural networks dramatically improves performance (better sample efficiency, faster convergence, improved generalization).

**You don't need to know group theory.** This skill guides you through domain-specific questions to uncover what symmetries might be present.

## Workflow

Copy this checklist and track your progress:

```
Symmetry Discovery Progress:
- [ ] Step 1: Classify your domain and data type
- [ ] Step 2: Analyze coordinate system choices
- [ ] Step 3: Test candidate transformations
- [ ] Step 4: Analyze physical constraints
- [ ] Step 5: Determine output behavior under transformations
- [ ] Step 6: Document symmetry candidates
```

**Step 1: Classify your domain and data type**

Ask user what their primary data type is. Use this table to identify likely symmetries and guide further questions. Images (2D grids) → likely translation, rotation, reflection. 3D data (point clouds, meshes) → likely SE(3), E(3). Molecules → E(3) + permutation + point groups. Graphs/Networks → permutation. Sets → permutation. Time series → time-translation, periodicity. Tabular → rarely symmetric. Physical systems → conservation laws imply symmetries. For detailed worked examples by domain, consult [Domain Examples](./resources/domain-examples.md).

**Step 2: Analyze coordinate system choices**

Guide user through coordinate analysis questions: Is there a preferred origin? (NO → translation invariance). Is there a preferred orientation? (NO → rotation invariance). Is there a preferred handedness? (NO → reflection invariance). Is there a preferred scale? (NO → scale invariance). Is element ordering meaningful? (NO → permutation invariance). Document each answer with reasoning.

**Step 3: Test candidate transformations**

For each candidate transformation T, ask: "If I transform my input by T, should my output change?" If NO → invariance to T. If YES predictably → equivariance to T. If YES unpredictably → no symmetry. Use domain-specific checklists from [Domain Transformation Tests](#domain-transformation-tests). Test all relevant transformations systematically. For the detailed methodology behind this testing approach, see [Methodology](./resources/methodology.md).

**Step 4: Analyze physical constraints**

Ask about conservation laws and physical symmetries. Noether's theorem: every conservation law implies a symmetry. Energy conserved → time-translation symmetry. Momentum conserved → space-translation symmetry. Angular momentum conserved → rotation symmetry. Ask: Are there physical conservation laws? Is system isolated from external reference frames? Are there gauge freedoms?

**Step 5: Determine output behavior under transformations**

Critical question: When input transforms, how should output transform? Classification labels → stay same (invariance). Bounding boxes → move with object (equivariance). Force vectors → rotate with system (equivariance). Scalar properties → stay same (invariance). Segmentation masks → transform with image (equivariance). This determines whether you need invariant or equivariant architecture.

**Step 6: Document symmetry candidates**

Create summary using [Output Template](#output-template). List identified symmetries with confidence levels. Note uncertain cases that need empirical validation. Identify non-symmetries (transformations that DO matter). Recommend next steps for validation and formalization. Quality criteria for this output are defined in [Quality Rubric](./resources/evaluators/rubric_symmetry_discovery.json).

## Domain Transformation Tests

### Image Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Translation | Does object position matter for label? | Translation invariance |
| Rotation (90°) | Would rotated image have same label? | C4 symmetry |
| Rotation (any) | Would any rotation preserve label? | SO(2) symmetry |
| Horizontal flip | Would mirror image have same label? | Reflection |
| Scale | Would zoomed image have same label? | Scale invariance |

### 3D Data Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| 3D Translation | Does absolute position matter? | Translation invariance |
| 3D Rotation | Does orientation matter? | SO(3) or SE(3) |
| Reflection | Does handedness matter? | O(3) or E(3) |
| Point permutation | Does point ordering matter? | Permutation invariance |

### Graph Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Node relabeling | Does node ID matter, or just connectivity? | Permutation invariance |

### Molecular Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Rotation | Is property independent of orientation? | SO(3) |
| Translation | Is property independent of position? | Translation |
| Reflection | Are both enantiomers equivalent? | Include reflections |
| Atom permutation | Do identical atoms behave identically? | Permutation |

### Temporal Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Time shift | Can pattern occur at any time? | Time-translation |
| Time reversal | Is forward same as backward? | Time-reversal |
| Periodicity | Do patterns repeat with period T? | Cyclic symmetry |

## Quick Reference

**The 5 Key Questions:**
1. Is there a preferred coordinate system? (origin, orientation, scale)
2. Does element ordering matter?
3. What transformations leave the label unchanged?
4. What physical constraints apply?
5. How should outputs transform when inputs transform?

**Common Symmetry → Group Mapping:**
- Rotation (2D, discrete) → Cyclic group Cₙ
- Rotation + reflection (2D) → Dihedral group Dₙ
- Rotation (2D, continuous) → SO(2)
- Rotation (3D) → SO(3)
- Rotation + translation (3D) → SE(3)
- Full Euclidean (3D) → E(3)
- Permutation → Symmetric group Sₙ

## Output Template

```
SYMMETRY CANDIDATE SUMMARY
==========================

Domain: [Data type]
Task: [Classification/Regression/Detection/etc.]

IDENTIFIED SYMMETRIES:
1. [Transformation]: [Invariance/Equivariance]
   - Evidence: [Why you believe this]
   - Confidence: [High/Medium/Low]

2. [Transformation]: [Invariance/Equivariance]
   - Evidence: [Why you believe this]
   - Confidence: [High/Medium/Low]

UNCERTAIN SYMMETRIES (need validation):
- [Transformation]: [Reason for uncertainty]

NON-SYMMETRIES (transformations that DO matter):
- [Transformation]: [Why it matters]

NEXT STEPS:
- Empirically validate uncertain symmetry candidates
- Map confirmed symmetries to mathematical groups
- Design architecture based on validated group structure
```
