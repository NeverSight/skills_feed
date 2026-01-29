---
name: active-inference-robotics
description: "Second-order skill synthesizing Patrick Kenny's discrete active inference framework with K-Scale's JAX/MuJoCo robotics stack for predictive coding in robot locomotion"
---

# Active Inference Robotics Skill (Second-Order)

> *"The agent's job is to predict its actions by predicting its sensations."* — Patrick Kenny

## Trigger Conditions

- User asks about bridging active inference with robot control
- Questions about predictive coding in locomotion policies
- Connecting KL divergence minimization to RL training
- Mean field approximation in robotics state estimation
- Sim2Real as inference about future observations

## Overview

**Second-order skill** synthesizing Patrick Kenny's discrete active inference framework with K-Scale's JAX/MuJoCo robotics stack. This skill emerges from the **constructive collision** between:

1. **Active Inference Institute** (ActInf ModelStream 019.1, Jan 2025)
2. **K-Scale Labs** (ksim, kos, kinfer ecosystem)
3. **MuJoCo Playground** (DeepMind's sim2real framework)

## The Constructive Collision

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONSTRUCTIVE COLLISION: Two Threads Converging                              │
│                                                                              │
│  Thread A: Patrick Kenny (Nov 2025)                                          │
│  ════════════════════════════════════                                        │
│  "Active inference can be formulated as constrained KL divergence           │
│   minimization solved by standard mean field methods"                        │
│                                                                              │
│  Key insight: Expected Free Energy ≈ KL Divergence + Entropy Regularizer    │
│                                                                              │
│  Thread B: K-Scale Labs (2024-2025)                                          │
│  ═══════════════════════════════════                                         │
│  "RL-based closed-loop control using policies trained in simulation         │
│   has firmly won as the best way of achieving real-time control"            │
│                                                                              │
│  Key insight: Stateless vs Stateful behaviors as pure/coalgebraic semantics │
│                                                                              │
│  COLLISION POINT: Both minimize surprise about future observations          │
│  ══════════════════════════════════════════════════════════════════         │
│                                                                              │
│       Active Inference              Robotics RL                              │
│       ────────────────              ──────────                               │
│       Predictive Distribution  ←→   Policy π(a|s)                           │
│       Hidden Markov Model      ←→   MDP/POMDP                                │
│       Mean Field Updates       ←→   PPO Gradient Steps                       │
│       Variational Free Energy  ←→   Policy Loss                              │
│       Expected Free Energy     ←→   Value Function + Entropy                 │
│       Perception/Action Loop   ←→   Observation/Action Loop                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Kenny's Key Contribution

From [arXiv:2511.20321](https://arxiv.org/abs/2511.20321):

```
Perception/Action Divergence = VFE(past) + KL(future states)

Where:
- VFE(past) = Standard variational free energy on observed history
- KL(future) = Divergence of predictive distribution from HMM

This differs from Expected Free Energy by an ENTROPY REGULARIZER:
  EFE ≈ Pragmatic Value + Mutual Information
  PAD ≈ Pragmatic Value + Entropy(Q)
```

### Why Entropy Regularization Matters for Robotics

```python
# In ksim PPO training, entropy bonus prevents policy collapse:
loss = policy_loss + value_loss - entropy_coef * entropy

# Kenny's formulation shows this is NOT ad-hoc but principled:
# Entropy regularizer = not being overconfident about predictions
# Biological rationale: know limitations of future predictions
```

## Mapping to ksim Architecture

| Active Inference Concept | ksim Implementation |
|--------------------------|---------------------|
| Hidden Markov Model | `PhysicsEngine` (MJX/MuJoCo) |
| Observation distribution | `Observation.observe(state)` |
| State inference Q(s) | `Critic.forward(obs, carry)` |
| Action inference Q(a) | `Actor.forward(obs, carry)` |
| Mean field factorization | Independent Q(s_t) per timestep |
| Predictive distribution | Policy rollout trajectory |
| VFE minimization | PPO policy gradient |
| EFE/PAD minimization | Value function + entropy bonus |

## Second-Order Behavior Types

### 1. Reflexive Control (Kenny's "Sufficient" Model)

```python
# Agent predicts proprioceptive sensations → fulfills reflexively
class ReflexiveController:
    """
    Kenny: "If the agent can successfully predict its future sensations,
    it can fulfill them unconsciously via motor reflexes."
    """
    def step(self, predicted_proprio: Array) -> Action:
        # Low-level PD control fulfills proprioceptive predictions
        return self.pd_controller(predicted_proprio, self.current_state)
```

### 2. Deliberative Planning (EFE Extension)

```python
# When reflexive prediction fails, engage deliberative inference
class DeliberativeController:
    """
    Extends reflexive control with policy search over trajectories.
    This is where EFE differs from Kenny's PAD formulation.
    """
    def plan(self, beliefs: Distribution, horizon: int) -> Policy:
        # Tree search over policies weighted by expected free energy
        for policy in self.policy_space:
            efe = self.expected_free_energy(beliefs, policy, horizon)
            # EFE includes mutual information (curiosity/exploration)
            # PAD would use entropy instead (uncertainty awareness)
```

### 3. Hierarchical Composition

```
Level 3: Goal Selection (minimize long-horizon EFE)
    ↓ sets reference for
Level 2: Trajectory Planning (predictive distribution)
    ↓ sets reference for  
Level 1: Reflexive Execution (fulfill proprio predictions)
    ↓ actuates
Level 0: Motor Primitives (PD control, actuator dynamics)
```

## GF(3) Balanced Quad

```
active-inference (0) ⊗ kscale-ksim (0) ⊗ mujoco-playground (0) = 0 ✓

All three are ERGODIC — coordination/infrastructure skills.
This is a "resonant triad" where all components coordinate.

For generation (+1), add: skill-creator, algorithmic-art
For verification (-1), add: sheaf-cohomology, code-review
```

### Skill Colors (drand seed 12005093902789493003)

| Skill | Trit | Color | Role |
|-------|------|-------|------|
| `active-inference` | 0 | `#DF8D0F` | Coordination (theory) |
| `kscale-ksim` | 0 | `#25BC3D` | Coordination (simulation) |
| `mujoco-playground` | 0 | `#93DBDA` | Coordination (framework) |

## 2-3-5-7 Prime Sieve Experts

Applying prime-indexed refinement to identify domain experts:

| Prime | Expert | Domain | Key Contribution |
|-------|--------|--------|------------------|
| 2 | Patrick Kenny | Active Inference | Mean field formulation, PAD criterion |
| 3 | Thomas Parr | Active Inference | 2022 textbook, EFE derivation |
| 5 | Ben Bolte | K-Scale | ksim architecture, open-source humanoids |
| 7 | Karl Friston | Free Energy Principle | FEP foundations, continuous formulation |
| 11 | (DeepMind team) | MuJoCo Playground | MJX, sim2real zero-shot |
| 13 | Wesley Maa | K-Scale | Tooling, visualization |

## Mutual Awareness

This skill references and is referenced by:

```yaml
depends_on:
  - kscale-ksim        # Simulation implementation
  - kscale-ecosystem   # Hardware context
  - mujoco-playground  # Framework foundation
  
referenced_by:
  - cognitive-superposition  # Team mental models
  - parametrised-optics-cybernetics  # Category theory bridge
  - reafference-corollary-discharge  # Sensorimotor prediction
```

## Implementation Pattern

```python
# Unified Active Inference + RL Training Loop
class ActiveInferenceTrainer:
    """
    Combines Kenny's PAD criterion with ksim's PPO.
    """
    def __init__(self, hmm: PhysicsEngine, config: Config):
        self.hmm = hmm
        self.actor = Actor(config)
        self.critic = Critic(config)
        
    def perception_action_divergence(
        self, 
        observations: Array,  # O_{1:t} (past)
        q_future: Distribution  # Q(S_{t+1:T}, O_{t+1:T})
    ) -> Scalar:
        """
        Kenny's PAD = VFE(past) + KL(future states from HMM)
        """
        # Past: standard VFE on observation history
        vfe_past = self.variational_free_energy(observations)
        
        # Future: KL divergence of predicted states from HMM
        # Note: Observable emissions cancel out in future KL
        kl_future = self.kl_future_states(q_future, self.hmm)
        
        return vfe_past + kl_future
    
    def train_step(self, trajectory: Trajectory) -> Metrics:
        # PPO updates approximate mean field coordinate ascent
        # Entropy bonus provides Kenny's regularization
        return ppo_update(
            self.actor, 
            self.critic, 
            trajectory,
            entropy_coef=0.01  # ← The regularizer!
        )
```

## References

- [Kenny (2025) Active Inference from First Principles](https://arxiv.org/abs/2511.20321)
- [Parr, Pezzulo, Friston (2022) Active Inference Textbook](https://direct.mit.edu/books/oa-monograph/5299/Active-InferenceThe-Free-Energy-Principle-in-Mind)
- [ActInf ModelStream 019.1](https://www.youtube.com/watch?v=...) - Jan 15, 2026
- [K-Scale Labs GitHub](https://github.com/kscalelabs)
- [MuJoCo Playground](https://playground.mujoco.org/)
- [Ben Bolte's Blog](https://ben.bolte.cc/)

## ACSet Schema

```julia
@present SchActiveInferenceRobotics(FreeSchema) begin
    # Objects
    HMM::Ob           # Hidden Markov Model (generative model)
    State::Ob         # Latent state
    Observation::Ob   # Sensory observation
    Action::Ob        # Motor command
    Policy::Ob        # Action sequence
    
    # Morphisms (inference)
    perceive::Hom(Observation, State)    # Perception: O → S
    predict::Hom(State, Observation)     # Prediction: S → O
    act::Hom(State, Action)              # Action selection: S → A
    transition::Hom(State × Action, State)  # Dynamics: S × A → S'
    
    # Attributes
    FreeEnergy::AttrType
    vfe::Attr(State, FreeEnergy)         # Variational free energy
    efe::Attr(Policy, FreeEnergy)        # Expected free energy
    pad::Attr(Policy, FreeEnergy)        # Perception/action divergence
    
    # The key relationship (Kenny's contribution):
    # pad ≈ efe + entropy_regularizer
end
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
active-inference-robotics (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
