---
name: numba
description: A Just-In-Time (JIT) compiler for Python that translates a subset of Python and NumPy code into fast machine code. Developed by Anaconda, Inc. Highly effective for accelerating loops, custom mathematical functions, and complex numerical algorithms. Use for @njit, @vectorize, prange, cuda.jit, numba.typed, JIT compilation, parallel loops, GPU acceleration with CUDA, Monte Carlo simulations, numerical algorithms, and high-performance Python computing.
version: 0.59
license: BSD-2-Clause
---

# Numba - High-Performance Python with JIT

Numba makes Python code go fast. It works by decorating your functions with decorators that tell Numba to compile them. It is particularly effective for code that involves heavy numerical loops and NumPy array manipulations.

## When to Use

- When NumPy's built-in vectorization isn't enough for your specific algorithm.
- You have complex nested loops that are slow in standard Python.
- You need to write custom "ufuncs" (universal functions) that operate element-wise on arrays.
- High-performance physical simulations (Monte Carlo, N-body, Grid-based solvers).
- Accelerating code for execution on NVIDIA GPUs (CUDA).
- Creating parallelized code that utilizes all CPU cores without the overhead of multiprocessing.

## Reference Documentation

**Official docs**: https://numba.pydata.org/numba-doc/latest/index.html  
**User Guide**: https://numba.pydata.org/numba-doc/latest/user/index.html  
**Search patterns**: `@njit`, `@vectorize`, `prange`, `cuda.jit`, `numba.typed`

## Core Principles

### nopython Mode (@njit)

This is the "gold standard" for Numba. In this mode, Numba compiles the code without using the Python C-API, resulting in maximum speed. If it can't compile (e.g., because of unsupported Python objects), it throws an error.

### Just-In-Time (JIT) Compilation

Compilation happens the first time you call the function. The machine code is then cached for subsequent calls.

### Array-Oriented

Numba is designed to work with NumPy arrays. It understands their memory layout and can generate highly optimized loops over them.

## Quick Reference

### Installation

```bash
pip install numba
```

### Standard Imports

```python
import numpy as np
from numba import njit, prange, vectorize, guvectorize, cuda
```

### Basic Pattern - Accelerating a Loop

```python
import numpy as np
from numba import njit

# 1. Apply the @njit decorator (alias for @jit(nopython=True))
@njit
def sum_array(arr):
    res = 0.0
    # Standard Python loop that would be slow is now fast as C
    for i in range(arr.shape[0]):
        res += arr[i]
    return res

# 2. Execute
data = np.random.random(1_000_000)
result = sum_array(data) # First call compiles, then runs
```

## Critical Rules

### ✅ DO

- **Prefer @njit** - Always use nopython=True (or its alias @njit). It ensures your code is actually running at machine speed.
- **Use NumPy Arrays** - Numba is optimized for NumPy. Avoid standard Python lists inside jitted functions.
- **Enable Parallelism** - Use `@njit(parallel=True)` and `prange` instead of `range` for automatic multi-threading.
- **Cache Compiled Code** - Use `@njit(cache=True)` to avoid recompilation every time you restart your script.
- **Warm up** - Remember that the first call is slow due to compilation. In timing benchmarks, always run the function once before measuring.
- **Type Specifying (Optional)** - You can provide signatures (e.g., `(float64[:],)`) to speed up the very first call, but Numba usually infers them well.

### ❌ DON'T

- **Don't use Python Objects** - Strings, dictionaries, and custom classes are slow or unsupported in nopython mode. Use `numba.typed` for specialized containers if needed.
- **Don't JIT small functions** - The overhead of calling a jitted function from Python can outweigh the gains for trivial operations.
- **Don't use unsupported libraries** - You cannot use pandas, matplotlib, or requests inside an `@njit` function.
- **Don't modify global state** - Jitted functions should be "pure" as much as possible for stability.

## Anti-Patterns (NEVER)

```python
from numba import njit
import pandas as pd

# ❌ BAD: Using Pandas inside @njit (Unsupported)
@njit
def bad_func(df):
    return df['col'].sum() # Will raise a LoweringError

# ✅ GOOD: Pass NumPy arrays instead
@njit
def good_func(arr):
    return arr.sum()

# ❌ BAD: Using @jit without nopython=True
from numba import jit
@jit
def slow_func(x): # This might fall back to "Object Mode" (slow)
    return x + 1

# ✅ GOOD: Always ensure nopython mode
@njit
def fast_func(x):
    return x + 1

# ❌ BAD: Manual loops in Python to call a JIT function
# for i in range(1000):
#     process_element(arr[i]) # Calling JIT overhead 1000 times

# ✅ GOOD: Move the loop INSIDE the @njit function
@njit
def process_all(arr):
    for i in range(arr.shape[0]):
        process_element(arr[i])
```

## Parallelism and Vectorization

### Automatic Multi-threading

```python
from numba import njit, prange

@njit(parallel=True)
def parallel_sum(A):
    # Use prange for the loop that should be parallelized
    s = 0
    for i in prange(A.shape[0]):
        s += A[i]
    return s
```

### Creating Fast ufuncs (@vectorize)

```python
from numba import vectorize

# This creates a NumPy ufunc that supports broadcasting
@vectorize(['float64(float64, float64)'], target='parallel')
def fast_add(x, y):
    return x + y

# Now you can use it on massive arrays
res = fast_add(arr1, arr2)
```

## Working with Structs and Types

### numba.typed for Non-Array Data

```python
from numba.typed import List, Dict
from numba import njit

@njit
def use_typed_list():
    l = List()
    l.append(1.0)
    return l
```

## GPU Acceleration (numba.cuda)

### Writing CUDA Kernels

```python
from numba import cuda

@cuda.jit
def my_kernel(io_array):
    # Calculate thread indices
    pos = cuda.grid(1)
    if pos < io_array.size:
        io_array[pos] *= 2

# Usage
data = np.ones(256)
threadsperblock = 32
blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock
my_kernel[blockspergrid, threadsperblock](data)
```

## Practical Workflows

### 1. Fast Monte Carlo Simulation

```python
import random

@njit(parallel=True)
def monte_carlo_pi(nsamples):
    acc = 0
    for i in prange(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples
```

### 2. Custom Image Filter (Stencil)

```python
from numba import njit

@njit
def apply_threshold(image, threshold):
    M, N = image.shape
    result = np.zeros_like(image)
    for i in range(M):
        for j in range(N):
            if image[i, j] > threshold:
                result[i, j] = 255
    return result
```

### 3. Solving a Physics Grid (Laplace Equation)

```python
@njit
def solve_laplace(u, niters):
    M, N = u.shape
    for n in range(niters):
        for i in range(1, M-1):
            for j in range(1, N-1):
                u[i, j] = 0.25 * (u[i+1, j] + u[i-1, j] + u[i, j+1] + u[i, j-1])
    return u
```

## Performance Optimization

### The inspect_types() method

Use this to see if Numba had to fall back to expensive Python objects or if it managed to optimize everything to native types.

```python
fast_func.inspect_types() # Prints color-coded annotated code
```

### Avoid Array Allocation in Loops

Pre-allocate arrays outside the `@njit` function or pass them as arguments to avoid memory management overhead.

```python
# ✅ GOOD:
@njit
def compute_into(out_arr, in_arr):
    for i in range(in_arr.shape[0]):
        out_arr[i] = in_arr[i] * 2
```

## Common Pitfalls and Solutions

### The "Global Variable" problem

Numba captures the value of global variables at the time of compilation.

```python
# ❌ Problem: Changing a global variable won't affect the jitted function
K = 10
@njit
def f(x): return x + K

K = 20
f(1) # Result is still 11!

# ✅ Solution: Pass constants as arguments
```

### Object Mode Fallback

If Numba says "Object mode is enabled", your code will be slow.

```python
# ✅ Solution: Force nopython mode
@njit # If this throws error, fix the code instead of removing @njit
```

### Random Seed in Parallel

Using `np.random` in `parallel=True` requires care to ensure independent streams for each thread. Standard `random.random()` or `np.random.random()` inside Numba are thread-safe and handle seeding per-thread automatically.

## Best Practices

1. **Always use @njit** - Never use `@jit` without `nopython=True`
2. **Pre-allocate arrays** - Avoid creating arrays inside hot loops
3. **Use prange for parallelism** - Enable automatic multi-threading with `parallel=True` and `prange`
4. **Cache compiled functions** - Use `cache=True` to avoid recompilation
5. **Warm up functions** - Call jitted functions once before benchmarking
6. **Pass NumPy arrays** - Convert Python lists to NumPy arrays before calling jitted functions
7. **Avoid Python objects** - Use `numba.typed.List` and `numba.typed.Dict` if you need containers
8. **Check compilation mode** - Use `inspect_types()` to verify nopython mode
9. **Handle first-call overhead** - Remember the first call compiles the function
10. **Use appropriate signatures** - Optional but can speed up first compilation

Numba is the bridge that allows Python to compete with C++ and Fortran in the high-performance computing arena. It removes the "Python tax" from your loops, enabling rapid prototyping without sacrificing execution speed.
