---
name: x-algo-ml
description: Explain the Phoenix ML model architecture for X recommendations. Use when users ask about embeddings, transformers, how predictions work, or ML model details.
---

# X Algorithm ML Architecture

The X recommendation system uses **Phoenix**, a transformer-based ML system for predicting user engagement. It operates in two stages: retrieval and ranking.

## Two-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RECOMMENDATION PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌──────────┐     ┌─────────────────────┐     ┌─────────────────────┐          │
│   │          │     │                     │     │                     │          │
│   │   User   │────▶│   STAGE 1:          │────▶│   STAGE 2:          │────▶ Feed│
│   │ Request  │     │   RETRIEVAL         │     │   RANKING           │          │
│   │          │     │   (Two-Tower)       │     │   (Transformer)     │          │
│   └──────────┘     │                     │     │                     │          │
│                    │   Millions → 1000s  │     │   1000s → Ranked    │          │
│                    └─────────────────────┘     └─────────────────────┘          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Stage 1: Retrieval (Two-Tower Model)

Efficiently narrows millions of candidates to thousands using approximate nearest neighbor search.

### Architecture

1. **User Tower**: Encodes user features + engagement history → normalized embedding `[B, D]`
2. **Candidate Tower**: Pre-computed embeddings for all posts in corpus → `[N, D]`
3. **Similarity**: Dot product between user embedding and candidate embeddings

```
User Tower          Candidate Tower
    │                     │
    ▼                     ▼
[B, D] user emb    [N, D] all posts
    │                     │
    └───── dot product ───┘
              │
              ▼
         Top-K by similarity
```

## Stage 2: Ranking (Transformer with Candidate Isolation)

Scores the retrieved candidates using a transformer that predicts multiple engagement actions.

### Model Configuration

```python
# phoenix/recsys_model.py
@dataclass
class PhoenixModelConfig:
    model: TransformerConfig              # Grok-1 based transformer
    emb_size: int                         # Embedding dimension D
    num_actions: int                      # 18 action types
    history_seq_len: int = 128            # User history length
    candidate_seq_len: int = 32           # Candidates per batch
    product_surface_vocab_size: int = 16  # Where post was seen
    hash_config: HashConfig               # Hash embedding config
```

### Input Structure

```python
class RecsysBatch(NamedTuple):
    # User identification
    user_hashes: ArrayLike               # [B, num_user_hashes]

    # User engagement history
    history_post_hashes: ArrayLike       # [B, S, num_item_hashes]
    history_author_hashes: ArrayLike     # [B, S, num_author_hashes]
    history_actions: ArrayLike           # [B, S, num_actions]
    history_product_surface: ArrayLike   # [B, S]

    # Candidates to score
    candidate_post_hashes: ArrayLike     # [B, C, num_item_hashes]
    candidate_author_hashes: ArrayLike   # [B, C, num_author_hashes]
    candidate_product_surface: ArrayLike # [B, C]
```

### Hash-Based Embeddings

Multiple hash functions map IDs to embedding tables:

```python
@dataclass
class HashConfig:
    num_user_hashes: int = 2      # Hash user ID 2 ways
    num_item_hashes: int = 2      # Hash post ID 2 ways
    num_author_hashes: int = 2    # Hash author ID 2 ways
```

**Why hashes?**

- Fixed memory: No need for individual embeddings per user/post
- Handles new entities: Any ID maps to some embedding
- Collision averaging: Multiple hashes reduce collision impact

### Embedding Combination

Each entity type has a "reduce" function that combines hash embeddings:

```python
# User: Concatenate hash embeddings → project to D
def block_user_reduce(...):
    # [B, num_user_hashes, D] → [B, 1, num_user_hashes * D] → [B, 1, D]
    user_embedding = user_embeddings.reshape((B, 1, num_user_hashes * D))
    user_embedding = jnp.dot(user_embedding, proj_mat_1)  # Project down
    return user_embedding, user_padding_mask

# History: Combine post + author + actions + product_surface
def block_history_reduce(...):
    # Concatenate all features, project to D
    post_author_embedding = jnp.concatenate([
        history_post_embeddings_reshaped,
        history_author_embeddings_reshaped,
        history_actions_embeddings,
        history_product_surface_embeddings,
    ], axis=-1)
    history_embedding = jnp.dot(post_author_embedding, proj_mat_3)
    return history_embedding, history_padding_mask
```

### Transformer Input

Final input is concatenation of:

```
[User (1)] + [History (S)] + [Candidates (C)]
     │              │               │
     ▼              ▼               ▼
 [B, 1, D]    [B, S, D]       [B, C, D]
         ╲       │       ╱
          ╲      │      ╱
            [B, 1+S+C, D]
```

## Attention Masking: Candidate Isolation

**Critical design**: Candidates cannot attend to each other, only to user + history.

```
                    ATTENTION MASK
         Keys (what we attend TO)
         ─────────────────────────────────────────────▶

         │ User │    History (S)    │   Candidates (C)    │
    ┌────┼──────┼───────────────────┼─────────────────────┤
 Q  │ U  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✗   ✗   ✗      │
 u  ├────┼──────┼───────────────────┼─────────────────────┤
 e  │ H  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✗   ✗   ✗      │
 r  │ i  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✗   ✗   ✗      │
 i  │ s  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✗   ✗   ✗      │
 e  │ t  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✗   ✗   ✗      │
 s  ├────┼──────┼───────────────────┼─────────────────────┤
    │ C  │  ✓   │  ✓   ✓   ✓   ✓   │  ✓   ✗   ✗   ✗      │
 │  │ a  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✓   ✗   ✗      │
 │  │ n  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✗   ✓   ✗      │
 ▼  │ d  │  ✓   │  ✓   ✓   ✓   ✓   │  ✗   ✗   ✗   ✓      │
    └────┴──────┴───────────────────┴─────────────────────┘

    ✓ = Can attend          ✗ = Cannot attend (diagonal only for candidates)
```

**Why candidate isolation?**

- Score for post A shouldn't depend on whether post B is in the batch
- Ensures consistent scoring regardless of batch composition
- Enables parallel scoring of candidates

### Transformer Forward Pass

```python
def __call__(self, batch, recsys_embeddings) -> RecsysModelOutput:
    # 1. Build combined embeddings
    embeddings, padding_mask, candidate_start = self.build_inputs(batch, recsys_embeddings)

    # 2. Pass through transformer (with candidate isolation mask)
    model_output = self.model(
        embeddings,
        padding_mask,
        candidate_start_offset=candidate_start,  # For attention masking
    )

    # 3. Extract candidate outputs
    out_embeddings = layer_norm(model_output.embeddings)
    candidate_embeddings = out_embeddings[:, candidate_start:, :]

    # 4. Project to action logits
    logits = jnp.dot(candidate_embeddings, unembeddings)
    # Shape: [B, num_candidates, num_actions]

    return RecsysModelOutput(logits=logits)
```

### Output: Multi-Action Prediction

```
Output Shape: [B, num_candidates, num_actions]
                          │
                          ▼
    ┌─────────────────────────────────────────────┐
    │ Like │ Reply │ Retweet │ Quote │ ... (18)   │
    └─────────────────────────────────────────────┘
```

Each output is a log-probability. Convert to probability:

```python
probability = exp(log_prob)
```

## Action Embeddings

History actions are encoded as signed vectors:

```python
def _get_action_embeddings(self, actions):
    # actions: [B, S, num_actions] multi-hot vector
    actions_signed = (2 * actions - 1)  # 0→-1, 1→+1
    action_emb = jnp.dot(actions_signed, action_projection)
    return action_emb
```

This encodes "did action" (+1) vs "didn't do action" (-1) for each action type.

## Product Surface Embeddings

Where the user engaged (home feed, search, notifications, etc.):

```python
def _single_hot_to_embeddings(self, input, vocab_size, emb_size, name):
    # Standard embedding lookup table
    embedding_table = hk.get_parameter(name, [vocab_size, emb_size])
    input_one_hot = jax.nn.one_hot(input, vocab_size)
    return jnp.dot(input_one_hot, embedding_table)
```

## Model Heritage

> The sample transformer implementation is ported from the Grok-1 open source release by xAI. The core transformer architecture comes from Grok-1, adapted for recommendation system use cases with custom input embeddings and attention masking for candidate isolation.

## Related Skills

- `/x-algo-engagement` - The 18 action types the model predicts
- `/x-algo-scoring` - How predictions become weighted scores
- `/x-algo-pipeline` - Where ML fits in the full system
