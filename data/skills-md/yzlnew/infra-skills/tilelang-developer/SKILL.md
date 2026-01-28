---
name: tilelang-developer
description: "Write, optimize, and debug high-performance AI compute kernels using TileLang (a Python DSL for GPU programming). Use when the user requests: (1) Writing custom GPU kernels for AI workloads (GEMM, Attention, MLA, etc.), (2) Optimizing existing TileLang code for NVIDIA, AMD, or Ascend hardware, (3) Implementing non-standard operators (like DeepSeek MLA, FlashAttention variants), (4) Debugging TileLang compilation or runtime errors, or (5) Cross-platform kernel development targeting multiple GPU vendors."
---

# TileLang Developer

Write high-performance AI compute kernels using TileLang - a tile-based programming model that bridges the gap between CUDA's low-level control and high-level abstractions.

## When to Use This Skill

Use this skill when the user needs to:
- Implement custom GPU kernels for AI operations (matrix multiplication, attention mechanisms, etc.)
- Optimize performance-critical operators for modern GPUs (NVIDIA Ampere/Hopper, AMD MI300X, Ascend NPU)
- Debug TileLang code or resolve performance issues
- Port kernels across different hardware platforms
- Understand or modify existing TileLang implementations

## Kernel Development Workflow

Follow these steps when writing a TileLang kernel:

### Step 1: Analyze Requirements

Gather essential information:

**Input/Output Specifications:**
- Tensor shapes (M, N, K dimensions)
- Data types (float16, float32, bfloat16, int8)
- Memory layout (row-major, column-major)

**Hardware Target:**
- NVIDIA GPU (Ampere A100, Hopper H100, etc.)
- AMD GPU (MI300X, etc.)
- Huawei Ascend NPU

**Performance Goals:**
- Target throughput or latency
- Memory bandwidth constraints
- Comparison baseline (cuBLAS, vendor libraries)

**Ask clarifying questions if details are missing.**

### Step 2: Set Up Kernel Structure

Create the basic kernel scaffold:

```python
import tilelang
import tilelang.language as T

@tilelang.jit(target="cuda", out_idx=[2])  # Specify output indices
def kernel_name(M, N, K, block_M, block_N, block_K):
    @T.prim_func
    def main(
        A: T.Buffer((M, K), "float16"),
        B: T.Buffer((K, N), "float16"),
        C: T.Buffer((M, N), "float16")
    ):
        # Kernel logic will go here
        pass

    return main
```

**Key decisions:**
- `target`: "cuda" (NVIDIA), "hip" (AMD), or "cpu"
- `out_idx`: List indices of output parameters
- Block dimensions: Typical values are 64, 128, or 256

### Step 3: Define Grid and Memory Hierarchy

Set up computation grid and allocate memory:

```python
# Define grid dimensions
with T.Kernel(
    T.ceildiv(N, block_N),  # Grid X
    T.ceildiv(M, block_M),  # Grid Y
    threads=128
) as (bx, by):

    # Allocate shared memory (L1 cache)
    A_shared = T.alloc_shared((block_M, block_K), "float16")
    B_shared = T.alloc_shared((block_K, block_N), "float16")

    # Allocate register fragments (accumulators)
    C_local = T.alloc_fragment((block_M, block_N), "float32")

    # CRITICAL: Apply swizzle layout to avoid bank conflicts
    T.annotate_layout({
        A_shared: T.make_swizzled_layout(A_shared),
        B_shared: T.make_swizzled_layout(B_shared)
    })
```

**Memory hierarchy:**
- **Global Memory** (HBM): Input/output tensors, slowest
- **Shared Memory** (L1): Explicitly managed cache, ~164KB on A100
- **Registers**: Fastest, used for accumulators and temporaries

**Critical optimization:** Always apply `T.make_swizzled_layout` to shared memory to eliminate bank conflicts.

### Step 4: Implement Computation Logic

Use TileLang primitives for data movement and computation:

```python
# Initialize accumulator
T.clear(C_local)

# Main computation loop with software pipelining
for k in T.Pipelined(T.ceildiv(K, block_K), num_stages=3):
    # Load tiles from global to shared memory
    T.copy(A[by * block_M, k * block_K], A_shared)
    T.copy(B[k * block_K, bx * block_N], B_shared)

    # Compute using Tensor Cores
    T.gemm(A_shared, B_shared, C_local, transpose_B=False)

# Write results back
T.copy(C_local, C[by * block_M, bx * block_N])
```

**Key primitives:**
- `T.copy`: Intelligent data transfer (auto-selects cp.async, TMA, etc.)
- `T.gemm`: Matrix multiplication using Tensor Cores
- `T.Pipelined`: Software pipelining to overlap compute and memory transfer
- `T.Parallel`: Element-wise parallel operations

**Pipeline stages:**
- `num_stages=2`: Double buffering
- `num_stages=3`: Triple buffering (recommended for most workloads)
- `num_stages=4+`: Diminishing returns, increases shared memory usage

### Step 5: Validate and Test

Generate test code to verify correctness:

```python
# Example instantiation
func = kernel_name(
    M=1024, N=1024, K=1024,
    block_M=128, block_N=128, block_K=32
)

# Test against reference implementation
import torch
A = torch.randn(1024, 1024, dtype=torch.float16, device='cuda')
B = torch.randn(1024, 1024, dtype=torch.float16, device='cuda')
C_tilelang = torch.empty(1024, 1024, dtype=torch.float16, device='cuda')
C_reference = A @ B

func(A, B, C_tilelang)

# Verify with appropriate tolerance for FP16
torch.testing.assert_close(C_tilelang, C_reference, rtol=1e-3, atol=1e-3)
```

### Step 6: Optimize Performance

Apply advanced optimizations if performance is suboptimal:

**Block Size Tuning:**
- A100: Try 128×128×32 or 64×64×32
- H100: Can use larger blocks (256×128×32)
- MI300X: May need smaller blocks due to 64KB shared memory limit

**Pipeline Depth:**
- Increase `num_stages` if memory-bound
- Decrease if shared memory is exhausted

**Warp Policy (for advanced cases):**
```python
T.gemm(A, B, C, policy=T.GemmWarpPolicy.FullRow)  # For attention
T.gemm(A, B, C, policy=T.GemmWarpPolicy.FullCol)  # For MLA decode
```

**Block-level swizzle:**
```python
T.use_swizzle(panel_size=10)  # Improves L2 cache hit rate
```

## Common Kernel Patterns

### Matrix Multiplication (GEMM)
Most fundamental kernel. See [EXAMPLES.md](references/EXAMPLES.md#matrix-multiplication-gemm) for complete implementation.

**Key features:**
- 3-stage pipelining
- Swizzle layout for shared memory
- Float32 accumulator for precision

### FlashAttention
Memory-efficient attention with online softmax. See [EXAMPLES.md](references/EXAMPLES.md#flashattention-v2) for complete implementation.

**Key features:**
- O(N) memory complexity
- Online softmax statistics
- Fused kernel (no intermediate materialization)

### DeepSeek MLA
Multi-Head Latent Attention with KV compression. See [EXAMPLES.md](references/EXAMPLES.md#deepseek-mla-decoding) for complete implementation.

**Key features:**
- Split-KV parallelization
- Non-standard dimensions
- FullCol warp policy for narrow matrices

## Reference Documentation

When you need specific information:

- **API details** (parameters, signatures, options): Read [API_REFERENCE.md](references/API_REFERENCE.md)
- **Complete code examples** (GEMM, Attention, MLA): Read [EXAMPLES.md](references/EXAMPLES.md)
- **Troubleshooting** (errors, performance issues): Read [DEBUGGING.md](references/DEBUGGING.md)

## Critical Performance Guidelines

Always include these optimizations:

1. **Swizzle layout for shared memory:**
   ```python
   T.annotate_layout({
       A_shared: T.make_swizzled_layout(A_shared)
   })
   ```

2. **Software pipelining:**
   ```python
   for k in T.Pipelined(num_blocks, num_stages=3):
   ```

3. **Float32 accumulators:**
   ```python
   C_local = T.alloc_fragment((M, N), "float32")  # Not float16
   ```

4. **Aligned block_K:**
   ```python
   block_K = 32  # Or 16, must align for Tensor Core
   ```

5. **Initialize accumulators:**
   ```python
   T.clear(C_local)
   ```

## Hardware-Specific Considerations

### NVIDIA GPUs
- **Ampere (A100)**: Use cp.async, num_stages=3, block_K=32
- **Hopper (H100)**: Can use TMA, larger blocks (256×128), num_stages=4
- Shared memory: 164KB (A100), 228KB (H100)

### AMD GPUs
- **MI300X**: Use target="hip", smaller blocks, 64KB shared memory limit
- Test with both HIP and CUDA backends for compatibility

### Huawei Ascend
- More experimental backend
- May require specific block sizes
- Consult Ascend-specific documentation

## Code Quality Standards

When generating TileLang code:

1. **Add explanatory comments** for non-obvious optimizations
2. **Specify hardware assumptions** (e.g., "optimized for A100")
3. **Include usage examples** showing instantiation
4. **Document block size choices** and tuning rationale
5. **Provide performance expectations** (e.g., "~90% of cuBLAS")

## Example Kernel Request Flow

**User:** "Write a FP16 matrix multiplication kernel for A100"

**Response:**
1. Clarify dimensions (if not specified)
2. Generate complete kernel code with:
   - Proper structure (@tilelang.jit, @T.prim_func)
   - Swizzle layouts
   - 3-stage pipelining
   - Appropriate block sizes (128×128×32)
3. Add usage example
4. Explain key optimizations:
   - "Swizzle layout eliminates bank conflicts"
   - "3-stage pipeline overlaps memory and compute"
   - "Float32 accumulator prevents overflow"
5. Suggest testing approach

## Troubleshooting Quick Reference

**Compilation errors:**
- Shared memory exceeded → Reduce block size or num_stages
- Shape mismatch → Verify dimension alignment in T.gemm

**Runtime errors:**
- Results all zeros → Check T.clear() and out_idx in decorator
- NaN/Inf → Use float32 accumulator, add epsilon in division

**Performance issues:**
- Low throughput → Verify swizzle layout and pipelining enabled
- Low occupancy → Reduce shared memory usage or block size
- Bank conflicts → Apply T.make_swizzled_layout

For detailed solutions, consult [DEBUGGING.md](references/DEBUGGING.md).
