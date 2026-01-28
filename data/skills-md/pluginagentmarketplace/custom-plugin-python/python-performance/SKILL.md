---
name: Python Performance
description: Master Python optimization techniques, profiling, memory management, and high-performance computing
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 07-best-practices
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: execution_time_improvement
---

# Python Performance Optimization

## Overview

Master performance optimization in Python. Learn to profile code, identify bottlenecks, optimize algorithms, manage memory efficiently, and leverage high-performance libraries for compute-intensive tasks.

## Learning Objectives

- Profile Python code to identify bottlenecks
- Optimize algorithms and data structures
- Manage memory efficiently
- Use compiled extensions (Cython, NumPy)
- Implement caching strategies
- Parallelize CPU-bound operations
- Benchmark and measure improvements

## Core Topics

### 1. Profiling & Benchmarking
- timeit module for micro-benchmarks
- cProfile for function-level profiling
- line_profiler for line-by-line analysis
- memory_profiler for memory usage
- py-spy for production profiling
- Flame graphs and visualization

**Code Example:**
```python
import timeit
import cProfile
import pstats

# 1. timeit for micro-benchmarks
def list_comprehension():
    return [x**2 for x in range(1000)]

def map_function():
    return list(map(lambda x: x**2, range(1000)))

# Compare performance
time_lc = timeit.timeit(list_comprehension, number=10000)
time_map = timeit.timeit(map_function, number=10000)
print(f"List comprehension: {time_lc:.4f}s")
print(f"Map function: {time_map:.4f}s")

# 2. cProfile for function profiling
def process_data():
    data = []
    for i in range(100000):
        data.append(i ** 2)
    return sum(data)

profiler = cProfile.Profile()
profiler.enable()
result = process_data()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)

# 3. Line profiling (requires line_profiler package)
# @profile decorator (add manually for line_profiler)
def slow_function():
    total = 0
    for i in range(1000000):
        total += i ** 2
    return total

# Run with: kernprof -l -v script.py

# 4. Memory profiling
from memory_profiler import profile

@profile
def memory_intensive():
    large_list = [i for i in range(1000000)]
    large_dict = {i: i**2 for i in range(1000000)}
    return len(large_list) + len(large_dict)

# Run with: python -m memory_profiler script.py
```

### 2. Algorithm & Data Structure Optimization
- Choosing efficient data structures
- Time complexity analysis
- Generator expressions vs lists
- Set operations for lookups
- Deque for queue operations
- Bisect for sorted lists

**Code Example:**
```python
import bisect
from collections import deque, Counter, defaultdict
import time

# 1. List vs Set for membership testing
# Bad: O(n) lookup
def find_in_list(items, target):
    return target in items  # Linear search

# Good: O(1) lookup
def find_in_set(items, target):
    items_set = set(items)
    return target in items_set

items = list(range(100000))
# List: 0.001s, Set: 0.000001s (1000x faster!)

# 2. Generator expressions for memory efficiency
# Bad: Creates entire list in memory
squares_list = [x**2 for x in range(1000000)]  # ~4MB

# Good: Generates on-demand
squares_gen = (x**2 for x in range(1000000))   # ~128 bytes

# 3. Deque for efficient queue operations
# Bad: O(n) pop from beginning
queue_list = list(range(10000))
queue_list.pop(0)  # Slow

# Good: O(1) pop from both ends
queue_deque = deque(range(10000))
queue_deque.popleft()  # Fast

# 4. Bisect for maintaining sorted lists
# Bad: O(n) insertion into sorted list
sorted_list = []
for i in [5, 2, 8, 1, 9]:
    sorted_list.append(i)
    sorted_list.sort()

# Good: O(log n) insertion
sorted_list = []
for i in [5, 2, 8, 1, 9]:
    bisect.insort(sorted_list, i)

# 5. Counter for frequency counting
# Bad: Manual counting
word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

# Good: Counter
word_count = Counter(words)
most_common = word_count.most_common(10)
```

### 3. Memory Management
- Memory allocation and garbage collection
- Object pooling
- Slots for memory-efficient classes
- Reference counting
- Weak references
- Memory leaks detection

**Code Example:**
```python
import gc
import sys
from weakref import WeakValueDictionary

# 1. __slots__ for memory-efficient classes
# Bad: Regular class (56 bytes per instance)
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Good: Slots class (32 bytes per instance - 43% smaller!)
class SlottedPoint:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

print(sys.getsizeof(RegularPoint(1, 2)))  # 56 bytes
print(sys.getsizeof(SlottedPoint(1, 2)))  # 32 bytes

# 2. Object pooling for expensive objects
class ObjectPool:
    def __init__(self, factory, max_size=10):
        self.factory = factory
        self.max_size = max_size
        self.pool = []

    def acquire(self):
        if self.pool:
            return self.pool.pop()
        return self.factory()

    def release(self, obj):
        if len(self.pool) < self.max_size:
            self.pool.append(obj)

# Usage
db_pool = ObjectPool(lambda: DatabaseConnection(), max_size=5)
conn = db_pool.acquire()
# Use connection
db_pool.release(conn)

# 3. Weak references to prevent memory leaks
class Cache:
    def __init__(self):
        self._cache = WeakValueDictionary()

    def get(self, key):
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value

# 4. Manual garbage collection for large operations
def process_large_dataset():
    for batch in large_data:
        process_batch(batch)
        # Force garbage collection after each batch
        gc.collect()

# 5. Context managers for resource cleanup
class ManagedResource:
    def __enter__(self):
        self.resource = allocate_resource()
        return self.resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.resource.cleanup()
        return False
```

### 4. High-Performance Computing
- NumPy vectorization
- Numba JIT compilation
- Cython for C extensions
- Multiprocessing for parallelism
- Concurrent.futures
- Performance comparison

**Code Example:**
```python
import numpy as np
from numba import jit
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

# 1. NumPy vectorization
# Bad: Python loops (slow)
def python_sum(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# Good: NumPy vectorization (100x faster!)
def numpy_sum(n):
    arr = np.arange(n)
    return np.sum(arr ** 2)

# Benchmark: python_sum(1000000) = 0.15s
#           numpy_sum(1000000)  = 0.002s

# 2. Numba JIT compilation
@jit(nopython=True)  # Compile to machine code
def fast_function(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# First call: compilation + execution
# Subsequent calls: 50x faster than pure Python!

# 3. Multiprocessing for CPU-bound tasks
def cpu_intensive_task(n):
    return sum(i * i for i in range(n))

# Single process
result = cpu_intensive_task(10000000)

# Multiple processes
with ProcessPoolExecutor(max_workers=4) as executor:
    ranges = [2500000, 2500000, 2500000, 2500000]
    results = executor.map(cpu_intensive_task, ranges)
    total = sum(results)

# 4x speedup on 4 cores!

# 4. Caching for expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# fibonacci(100) without cache: ~forever
# fibonacci(100) with cache: instant

# 5. Memory views for zero-copy operations
def process_array(data):
    # Bad: Creates copy
    subset = data[1000:2000]

    # Good: Zero-copy view
    view = memoryview(data)[1000:2000]
```

## Hands-On Practice

### Project 1: Performance Profiler
Build a comprehensive profiling tool.

**Requirements:**
- CPU profiling with cProfile
- Memory profiling
- Line-by-line analysis
- Visualization (flame graphs)
- HTML report generation
- Bottleneck identification

**Key Skills:** Profiling tools, visualization, analysis

### Project 2: Data Processing Pipeline
Optimize data processing pipeline.

**Requirements:**
- Load large CSV files (1GB+)
- Transform and clean data
- Aggregate statistics
- Compare Python/NumPy/Pandas approaches
- Measure memory usage
- Optimize to <2GB RAM

**Key Skills:** NumPy, memory optimization, benchmarking

### Project 3: Parallel Computing
Implement parallel algorithms.

**Requirements:**
- Matrix multiplication
- Image processing
- Monte Carlo simulation
- Compare threading/multiprocessing/asyncio
- Measure speedup
- Handle shared state

**Key Skills:** Parallelism, performance measurement

## Assessment Criteria

- [ ] Profile code to identify bottlenecks
- [ ] Choose appropriate data structures
- [ ] Optimize algorithms for time complexity
- [ ] Manage memory efficiently
- [ ] Use vectorization where applicable
- [ ] Implement effective caching
- [ ] Parallelize CPU-bound operations

## Resources

### Official Documentation
- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips) - Official tips
- [NumPy Docs](https://numpy.org/doc/) - NumPy documentation
- [Numba Docs](https://numba.pydata.org/) - JIT compilation

### Learning Platforms
- [High Performance Python](https://www.oreilly.com/library/view/high-performance-python/9781492055013/) - O'Reilly book
- [Python Performance](https://realpython.com/python-performance/) - Real Python guide
- [Optimizing Python](https://www.youtube.com/watch?v=zQeYx87mfyw) - PyCon talks

### Tools
- [cProfile](https://docs.python.org/3/library/profile.html) - CPU profiling
- [memory_profiler](https://pypi.org/project/memory-profiler/) - Memory profiling
- [py-spy](https://github.com/benfred/py-spy) - Sampling profiler
- [Scalene](https://github.com/plasma-umass/scalene) - CPU/GPU/memory profiler

## Next Steps

After mastering Python performance, explore:
- **Cython** - C extensions for Python
- **PyPy** - Alternative Python interpreter
- **Dask** - Parallel computing library
- **CUDA** - GPU programming with Python
