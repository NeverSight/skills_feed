---
name: equivariant-architecture-designer
description: Use when you have validated symmetry groups and need to design neural network architecture that respects those symmetries. Invoke when user mentions equivariant layers, G-CNN, e3nn, steerable networks, building symmetry into model, or needs architecture recommendations for specific symmetry groups. Provides architecture patterns and implementation guidance.
---

# Equivariant Architecture Designer

## What Is It?

This skill helps you **design neural network architectures that respect identified symmetry groups**. Given a validated group specification, it recommends architecture patterns, specific libraries, and implementation strategies.

**The payoff**: Equivariant architectures have fewer parameters, train faster, generalize better, and are more robust to distribution shift.

## Workflow

Copy this checklist and track your progress:

```
Architecture Design Progress:
- [ ] Step 1: Review group specification and requirements
- [ ] Step 2: Select architecture family
- [ ] Step 3: Choose specific layers and components
- [ ] Step 4: Design network topology
- [ ] Step 5: Select implementation library
- [ ] Step 6: Create architecture specification
```

**Step 1: Review group specification and requirements**

Gather the validated group specification. Confirm: which group(s) are involved, whether invariance or equivariance is needed, the data domain (images, point clouds, graphs, etc.), task type (classification, regression, generation), and any computational constraints. If group isn't specified, work with user to identify it first.

**Step 2: Select architecture family**

Match the symmetry group to an architecture family using [Architecture Selection Guide](#architecture-selection-guide). Key families: G-CNNs for discrete groups on grids, Steerable CNNs for continuous 2D groups, e3nn/NequIP for E(3) on point data, GNNs for permutation on graphs, DeepSets for permutation on sets. Consider trade-offs between expressiveness and efficiency.

**Step 3: Choose specific layers and components**

Select layer types based on [Layer Patterns](#layer-patterns). For each layer decide: convolution type (regular, group, steerable), nonlinearity (must preserve equivariance - use gated, norm-based, or tensor product), normalization (batch norm breaks equivariance - use layer norm or equivariant batch norm), pooling (for invariant outputs: use invariant pooling; for equivariant: preserve structure). For detailed design methodology, see [Methodology Details](./resources/methodology.md).

**Step 4: Design network topology**

Design the overall network structure: encoder architecture (how features are extracted), feature representations at each stage (irreps for Lie groups), pooling/aggregation strategy, output head matching task requirements. Use [Topology Patterns](#topology-patterns) for common designs. Balance depth vs. width for your group size.

**Step 5: Select implementation library**

Choose library based on [Library Reference](#library-reference). Match to your group, framework preference (PyTorch/JAX), and performance needs. Popular choices: e3nn (E(3)/O(3), PyTorch), escnn (discrete groups, PyTorch), pytorch_geometric (permutation, PyTorch). Ensure library supports your specific group.

**Step 6: Create architecture specification**

Document the design using [Output Template](#output-template). Include: layer-by-layer specification, representation types, library dependencies, expected parameter count, and pseudo-code or actual code skeleton. This specification guides implementation and subsequent equivariance verification. For ready-to-use implementation templates, see [Code Templates](./resources/templates.md). Quality criteria for this output are defined in [Quality Rubric](./resources/evaluators/rubric_architecture.json).

## Architecture Selection Guide

### By Symmetry Group

| Group | Domain | Recommended Architecture | Library |
|-------|--------|-------------------------|---------|
| Cₙ, Dₙ | 2D Images | G-CNN, Group Equivariant CNN | escnn, e2cnn |
| SO(2), O(2) | 2D Images | Steerable CNN, Harmonic Networks | escnn |
| SO(3) | Spherical | Spherical CNN | e3nn, s2cnn |
| SE(3), E(3) | Point clouds | Equivariant GNN, Tensor Field Networks | e3nn, NequIP |
| Sₙ | Sets | DeepSets | pytorch, jax |
| Sₙ | Graphs | Message Passing GNN | pytorch_geometric |
| E(3) × Sₙ | Molecules | E(3) Equivariant GNN | e3nn, SchNet |

### By Task Type

| Task | Output Type | Key Consideration |
|------|-------------|-------------------|
| Classification | Invariant scalar | Use invariant pooling |
| Regression (scalar) | Invariant scalar | Same as classification |
| Segmentation | Equivariant per-point | Preserve equivariance to output |
| Force prediction | Equivariant vector | Output as l=1 irrep |
| Pose estimation | Equivariant transform | Output rotation + translation |
| Generation | Equivariant structure | Equivariant decoder |

## Layer Patterns

### Equivariant Convolution Patterns

**Standard G-Convolution**:
```
(f ⋆ ψ)(g) = ∫_G f(h) ψ(g⁻¹h) dh
```
- Input: Feature map on group G
- Kernel: Function on G
- Output: Feature map on G

**Steerable Convolution**:
- Uses steerable kernels that transform predictably
- Parameterized by irreducible representations
- More efficient for continuous groups

**e3nn Tensor Product Layer**:
```python
# Combine features with different angular momenta
tp = o3.FullyConnectedTensorProduct(
    irreps_in1, irreps_in2, irreps_out
)
output = tp(input1, input2)
```

### Equivariant Nonlinearities

**Problem**: Standard nonlinearities (ReLU, etc.) break equivariance.

**Solutions**:

| Type | How It Works | When to Use |
|------|--------------|-------------|
| Norm-based | Apply nonlinearity to ||x|| | Scalars, invariant features |
| Gated | Use invariant to gate equivariant | General purpose |
| Tensor product | Nonlinearity via Clebsch-Gordan | e3nn, high-quality |
| Invariant features | Only apply to l=0 components | Simple, fast |

### Equivariant Normalization

**Batch Norm**: Breaks equivariance (different stats per orientation)
**Solutions**:
- Layer Norm (normalize per sample)
- Equivariant Batch Norm (normalize per irrep channel)
- Instance Norm (often OK)

### Pooling for Invariance

To get invariant output from equivariant features:

| Method | Formula | When to Use |
|--------|---------|-------------|
| Mean pooling | mean over group | Continuous groups |
| Sum pooling | sum over elements | Sets, graphs |
| Max pooling | max ||x|| | Discrete groups |
| Attention pooling | weighted sum | When importance varies |

## Topology Patterns

### Encoder-Decoder (Segmentation, Generation)

```
Input → [Equiv. Encoder] → Latent (equiv.) → [Equiv. Decoder] → Output
```
- Encoder: Progressive feature extraction
- Latent: Equivariant representation
- Decoder: Reconstruct with symmetry

### Encoder-Pooling (Classification)

```
Input → [Equiv. Encoder] → Features (equiv.) → [Invariant Pool] → [MLP] → Class
```
- Pool at the end to get invariant features
- Final MLP operates on invariant representation

### Message Passing (Graphs/Point Clouds)

```
Nodes → [MP Layer 1] → [MP Layer 2] → ... → [Aggregation] → Output
```
- Each layer: aggregate neighbors, update node
- Aggregation: sum/mean for invariance, per-node for equivariance

## Library Reference

### e3nn (PyTorch)

**Groups**: E(3), O(3), SO(3)
**Strengths**: Full irrep support, tensor products, spherical harmonics
**Use for**: Molecular modeling, 3D point clouds, physics

```python
from e3nn import o3
irreps = o3.Irreps("2x0e + 2x1o + 1x2e")  # 2 scalars, 2 vectors, 1 tensor
```

### escnn (PyTorch)

**Groups**: Discrete groups (Cₙ, Dₙ), continuous 2D (SO(2), O(2))
**Strengths**: Image processing, well-documented
**Use for**: 2D images with rotation/reflection symmetry

```python
from escnn import gspaces, nn
gspace = gspaces.rot2dOnR2(N=4)  # C4 rotation group
```

### pytorch_geometric (PyTorch)

**Groups**: Permutation (Sₙ)
**Strengths**: Graphs, batching, many GNN layers
**Use for**: Graph classification/regression, node prediction

```python
from torch_geometric.nn import GCNConv, global_mean_pool
```

### Other Libraries

| Library | Groups | Framework | Notes |
|---------|--------|-----------|-------|
| NequIP | E(3) | PyTorch | Molecular dynamics |
| MACE | E(3) | PyTorch | Molecular potentials |
| jraph | Sₙ | JAX | Graph networks |
| geomstats | Lie groups | NumPy/PyTorch | Manifold learning |

## Output Template

```
ARCHITECTURE SPECIFICATION
==========================

Target Symmetry: [Group name and notation]
Symmetry Type: [Invariant/Equivariant]
Task: [Classification/Regression/etc.]
Domain: [Images/Point clouds/Graphs/etc.]

Architecture Family: [e.g., E(3) Equivariant GNN]
Library: [e.g., e3nn]

Layer Specification:
1. Input Layer
   - Input type: [e.g., 3D coordinates + features]
   - Representation: [e.g., positions (l=1) + scalars (l=0)]

2. [Layer Name]
   - Type: [Convolution/Tensor Product/Message Passing]
   - Input irreps: [specification]
   - Output irreps: [specification]
   - Nonlinearity: [Gated/Norm/None]

3. [Continue for each layer...]

N. Output Layer
   - Aggregation: [Mean/Sum/Attention]
   - Output: [Invariant scalar / Equivariant vector / etc.]

Estimated Parameters: [count]
Key Dependencies: [library versions]

Code Skeleton:
[Provide implementation outline or pseudo-code]

NEXT STEPS:
- Implement the architecture using the specified library
- Verify equivariance through numerical testing after implementation
```
