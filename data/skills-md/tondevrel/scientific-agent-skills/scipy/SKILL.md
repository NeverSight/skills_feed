---
name: scipy
description: Comprehensive guide for SciPy - the fundamental library for scientific and technical computing in Python. Use for integration, optimization, interpolation, linear algebra, signal processing, statistics, ODEs, Fourier transforms, and advanced scientific algorithms. Built on NumPy and essential for research and engineering.
version: 1.12
license: BSD-3-Clause
---

# SciPy - Scientific Computing

Advanced scientific computing library built on NumPy, providing algorithms for optimization, integration, interpolation, and more.

## When to Use

- Integrating functions (numerical integration, ODEs)
- Optimizing functions (minimization, root finding, curve fitting)
- Interpolating data (1D, 2D, splines)
- Advanced linear algebra (sparse matrices, decompositions)
- Signal processing (filtering, Fourier transforms, wavelets)
- Statistical analysis (distributions, hypothesis tests)
- Image processing (filters, morphology, measurements)
- Spatial algorithms (distance matrices, clustering, Voronoi)
- Special mathematical functions (Bessel, gamma, error functions)
- Solving differential equations (ODEs, PDEs)

## Reference Documentation

**Official docs**: https://docs.scipy.org/  
**Search patterns**: `scipy.integrate.quad`, `scipy.optimize.minimize`, `scipy.interpolate`, `scipy.stats`, `scipy.signal`

## Core Principles

### Use SciPy For

| Task | Module | Example |
|------|--------|---------|
| Integration | `integrate` | `quad(f, 0, 1)` |
| Optimization | `optimize` | `minimize(f, x0)` |
| Interpolation | `interpolate` | `interp1d(x, y)` |
| Linear algebra | `linalg` | `linalg.solve(A, b)` |
| Signal processing | `signal` | `signal.butter(4, 0.5)` |
| Statistics | `stats` | `stats.norm.pdf(x)` |
| ODEs | `integrate` | `solve_ivp(f, t_span, y0)` |
| FFT | `fft` | `fft.fft(signal)` |

### Do NOT Use For

- Basic array operations (use NumPy)
- Machine learning (use scikit-learn)
- Deep learning (use PyTorch, TensorFlow)
- Symbolic mathematics (use SymPy)
- Data manipulation (use pandas)

## Quick Reference

### Installation

```bash
# pip
pip install scipy

# conda
conda install scipy

# With NumPy
pip install numpy scipy
```

### Standard Imports

```python
import numpy as np
from scipy import integrate, optimize, interpolate
from scipy import linalg, signal, stats
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import minimize, root
from scipy.interpolate import interp1d, UnivariateSpline
```

### Basic Pattern - Integration

```python
from scipy import integrate
import numpy as np

# Define function
def f(x):
    return x**2

# Integrate from 0 to 1
result, error = integrate.quad(f, 0, 1)
print(f"Integral: {result:.6f} ± {error:.2e}")
```

### Basic Pattern - Optimization

```python
from scipy import optimize
import numpy as np

# Function to minimize
def f(x):
    return (x - 2)**2 + 1

# Minimize
result = optimize.minimize(f, x0=0)
print(f"Minimum at x = {result.x[0]:.6f}")
print(f"Minimum value = {result.fun:.6f}")
```

### Basic Pattern - Interpolation

```python
from scipy import interpolate
import numpy as np

# Data points
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])

# Create interpolator
f = interpolate.interp1d(x, y, kind='cubic')

# Interpolate at new points
x_new = np.linspace(0, 4, 100)
y_new = f(x_new)
```

## Critical Rules

### ✅ DO

- **Check convergence** - Always verify optimization converged
- **Specify tolerances** - Set appropriate `rtol` and `atol`
- **Use appropriate methods** - Choose algorithm for problem type
- **Validate inputs** - Check array shapes and values
- **Handle edge cases** - Deal with singularities and discontinuities
- **Set integration limits carefully** - Watch for infinite limits
- **Use vectorization** - Functions should accept arrays
- **Check statistical assumptions** - Verify distribution assumptions
- **Specify degrees of freedom** - For interpolation and fitting
- **Use sparse matrices** - For large, sparse systems

### ❌ DON'T

- **Ignore convergence warnings** - They indicate problems
- **Use inappropriate tolerances** - Too loose or too tight
- **Apply wrong distribution** - Check data characteristics
- **Forget initial guesses** - Optimization needs good starting points
- **Integrate discontinuous functions** - Without special handling
- **Extrapolate beyond data** - Interpolation is not extrapolation
- **Mix incompatible units** - Keep consistent units
- **Ignore error estimates** - They provide confidence levels
- **Use wrong coordinate system** - Check Cartesian vs polar
- **Overfit with high-degree polynomials** - Causes oscillations

## Anti-Patterns (NEVER)

```python
from scipy import integrate, optimize
import numpy as np

# ❌ BAD: Ignoring convergence
result = optimize.minimize(f, x0=0)
optimal_x = result.x  # Didn't check if converged!

# ✅ GOOD: Check convergence
result = optimize.minimize(f, x0=0)
if result.success:
    optimal_x = result.x
else:
    print(f"Optimization failed: {result.message}")

# ❌ BAD: Non-vectorized function for integration
def bad_func(x):
    if x < 0.5:
        return x
    else:
        return 1 - x

# ✅ GOOD: Vectorized function
def good_func(x):
    return np.where(x < 0.5, x, 1 - x)

# ❌ BAD: Poor initial guess
result = optimize.minimize(complex_func, x0=[1000, 1000])
# May converge to local minimum or fail!

# ✅ GOOD: Reasonable initial guess
x0 = np.array([0.0, 0.0])  # Near expected minimum
result = optimize.minimize(complex_func, x0=x0)

# ❌ BAD: Extrapolation with interpolation
f = interpolate.interp1d(x_data, y_data)
y_new = f(100)  # x_data max is 10, this will crash!

# ✅ GOOD: Check bounds or use extrapolation
f = interpolate.interp1d(x_data, y_data, fill_value='extrapolate')
y_new = f(100)  # Now works (but be cautious!)

# ❌ BAD: Wrong statistical test
# Using t-test for non-normal data
stats.ttest_ind(non_normal_data1, non_normal_data2)

# ✅ GOOD: Use appropriate test
# Use Mann-Whitney U for non-normal data
stats.mannwhitneyu(non_normal_data1, non_normal_data2)
```

## Integration (scipy.integrate)

### Numerical Integration (Quadrature)

```python
from scipy import integrate
import numpy as np

# Single integral
def f(x):
    return np.exp(-x**2)

result, error = integrate.quad(f, 0, np.inf)
print(f"∫exp(-x²)dx from 0 to ∞ = {result:.6f}")
print(f"Error estimate: {error:.2e}")

# Integral with parameters
def g(x, a, b):
    return a * x**2 + b

result, error = integrate.quad(g, 0, 1, args=(2, 3))
print(f"Result: {result:.6f}")

# Integral with singularity
def h(x):
    return 1 / np.sqrt(x)

# Specify singularity points
result, error = integrate.quad(h, 0, 1, points=[0])
```

### Double and Triple Integrals

```python
from scipy import integrate
import numpy as np

# Double integral: ∫∫ x*y dx dy over [0,1]×[0,2]
def f(y, x):  # Note: y first, x second
    return x * y

result, error = integrate.dblquad(f, 0, 1, 0, 2)
print(f"Double integral: {result:.6f}")

# Triple integral
def g(z, y, x):
    return x * y * z

result, error = integrate.tplquad(g, 0, 1, 0, 1, 0, 1)
print(f"Triple integral: {result:.6f}")

# Variable limits
def lower(x):
    return 0

def upper(x):
    return x

result, error = integrate.dblquad(f, 0, 1, lower, upper)
```

### Solving ODEs

```python
from scipy.integrate import odeint, solve_ivp
import numpy as np

# Solve dy/dt = -k*y (exponential decay)
def exponential_decay(y, t, k):
    return -k * y

# Initial condition and time points
y0 = 100
t = np.linspace(0, 10, 100)
k = 0.5

# Solve with odeint (older interface)
solution = odeint(exponential_decay, y0, t, args=(k,))

# Solve with solve_ivp (modern interface)
def decay_ivp(t, y, k):
    return -k * y

sol = solve_ivp(decay_ivp, [0, 10], [y0], args=(k,), t_eval=t)

print(f"Final value (odeint): {solution[-1, 0]:.6f}")
print(f"Final value (solve_ivp): {sol.y[0, -1]:.6f}")
```

### System of ODEs

```python
from scipy.integrate import solve_ivp
import numpy as np

# Lotka-Volterra equations (predator-prey)
def lotka_volterra(t, z, a, b, c, d):
    x, y = z
    dxdt = a*x - b*x*y
    dydt = -c*y + d*x*y
    return [dxdt, dydt]

# Parameters
a, b, c, d = 1.5, 1.0, 3.0, 1.0

# Initial conditions
z0 = [10, 5]  # [prey, predator]

# Time span
t_span = (0, 15)
t_eval = np.linspace(0, 15, 1000)

# Solve
sol = solve_ivp(lotka_volterra, t_span, z0, args=(a, b, c, d), 
                t_eval=t_eval, method='RK45')

prey = sol.y[0]
predator = sol.y[1]

print(f"Prey population at t=15: {prey[-1]:.2f}")
print(f"Predator population at t=15: {predator[-1]:.2f}")
```

## Optimization (scipy.optimize)

### Function Minimization

```python
from scipy import optimize
import numpy as np

# Rosenbrock function (classic test function)
def rosenbrock(x):
    return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2

# Initial guess
x0 = np.array([0, 0])

# Minimize with Nelder-Mead
result = optimize.minimize(rosenbrock, x0, method='Nelder-Mead')
print(f"Nelder-Mead: x = {result.x}, f(x) = {result.fun:.6f}")

# Minimize with BFGS (uses gradient)
result = optimize.minimize(rosenbrock, x0, method='BFGS')
print(f"BFGS: x = {result.x}, f(x) = {result.fun:.6f}")

# Minimize with bounds
bounds = [(0, 2), (0, 2)]
result = optimize.minimize(rosenbrock, x0, method='L-BFGS-B', bounds=bounds)
print(f"L-BFGS-B with bounds: x = {result.x}")
```

### Root Finding

```python
from scipy import optimize
import numpy as np

# Find roots of f(x) = 0
def f(x):
    return x**3 - 2*x - 5

# Root finding with scalar function
root = optimize.brentq(f, 0, 3)  # Search in [0, 3]
print(f"Root: {root:.6f}")

# Root finding with newton method (needs derivative)
def f_prime(x):
    return 3*x**2 - 2

root = optimize.newton(f, x0=2, fprime=f_prime)
print(f"Root (Newton): {root:.6f}")

# System of equations
def system(x):
    return [x[0]**2 + x[1]**2 - 1,
            x[0] - x[1]]

result = optimize.root(system, [1, 1])
print(f"Solution: {result.x}")
```

### Curve Fitting

```python
from scipy import optimize
import numpy as np

# Generate data with noise
x_data = np.linspace(0, 10, 50)
y_true = 2.5 * np.exp(-0.5 * x_data)
y_data = y_true + 0.2 * np.random.randn(len(x_data))

# Model function
def exponential_model(x, a, b):
    return a * np.exp(b * x)

# Fit model to data
params, covariance = optimize.curve_fit(exponential_model, x_data, y_data)
a_fit, b_fit = params

print(f"Fitted parameters: a = {a_fit:.4f}, b = {b_fit:.4f}")
print(f"True parameters: a = 2.5, b = -0.5")

# Standard errors
perr = np.sqrt(np.diag(covariance))
print(f"Parameter errors: ±{perr}")
```

### Constrained Optimization

```python
from scipy import optimize
import numpy as np

# Minimize f(x) = x[0]^2 + x[1]^2
# Subject to: x[0] + x[1] >= 1
def objective(x):
    return x[0]**2 + x[1]**2

# Constraint: g(x) >= 0
def constraint(x):
    return x[0] + x[1] - 1

con = {'type': 'ineq', 'fun': constraint}

# Minimize
x0 = np.array([2, 2])
result = optimize.minimize(objective, x0, constraints=con)

print(f"Optimal point: {result.x}")
print(f"Objective value: {result.fun:.6f}")
```

## Interpolation (scipy.interpolate)

### 1D Interpolation

```python
from scipy import interpolate
import numpy as np

# Data points
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 0.8, 0.9, 0.1, -0.8, -1])

# Linear interpolation
f_linear = interpolate.interp1d(x, y, kind='linear')

# Cubic interpolation
f_cubic = interpolate.interp1d(x, y, kind='cubic')

# Evaluate at new points
x_new = np.linspace(0, 5, 100)
y_linear = f_linear(x_new)
y_cubic = f_cubic(x_new)

print(f"Value at x=2.5 (linear): {f_linear(2.5):.4f}")
print(f"Value at x=2.5 (cubic): {f_cubic(2.5):.4f}")
```

### Spline Interpolation

```python
from scipy import interpolate
import numpy as np

# Data
x = np.linspace(0, 10, 11)
y = np.sin(x)

# B-spline interpolation
tck = interpolate.splrep(x, y, s=0)  # s=0 for exact interpolation

# Evaluate
x_new = np.linspace(0, 10, 100)
y_new = interpolate.splev(x_new, tck)

# Or use UnivariateSpline
spl = interpolate.UnivariateSpline(x, y, s=0)
y_spl = spl(x_new)

# Smoothing spline (s > 0)
spl_smooth = interpolate.UnivariateSpline(x, y, s=1)
y_smooth = spl_smooth(x_new)
```

### 2D Interpolation

```python
from scipy import interpolate
import numpy as np

# Create 2D data
x = np.linspace(0, 4, 5)
y = np.linspace(0, 4, 5)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

# Flatten for irregular grid
x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()

# 2D interpolation
f = interpolate.interp2d(x_flat, y_flat, z_flat, kind='cubic')

# Evaluate at new points
x_new = np.linspace(0, 4, 50)
y_new = np.linspace(0, 4, 50)
Z_new = f(x_new, y_new)

print(f"Interpolated shape: {Z_new.shape}")
```

## Linear Algebra (scipy.linalg)

### Advanced Matrix Operations

```python
from scipy import linalg
import numpy as np

# Matrix
A = np.array([[1, 2], [3, 4]])

# Matrix exponential
exp_A = linalg.expm(A)

# Matrix logarithm
log_A = linalg.logm(A)

# Matrix square root
sqrt_A = linalg.sqrtm(A)

# Matrix power
A_power_3 = linalg.fractional_matrix_power(A, 3)

print(f"exp(A):\n{exp_A}")
print(f"A^3:\n{A_power_3}")
```

### Matrix Decompositions

```python
from scipy import linalg
import numpy as np

A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 10]])

# LU decomposition
P, L, U = linalg.lu(A)
print(f"A = P @ L @ U: {np.allclose(A, P @ L @ U)}")

# QR decomposition
Q, R = linalg.qr(A)
print(f"A = Q @ R: {np.allclose(A, Q @ R)}")

# Cholesky decomposition (for positive definite)
A_pos_def = np.array([[4, 2], [2, 3]])
L = linalg.cholesky(A_pos_def, lower=True)
print(f"A = L @ L.T: {np.allclose(A_pos_def, L @ L.T)}")

# Schur decomposition
T, Z = linalg.schur(A)
print(f"A = Z @ T @ Z.H: {np.allclose(A, Z @ T @ Z.T.conj())}")
```

### Sparse Matrices

```python
from scipy import sparse
import numpy as np

# Create sparse matrix
row = np.array([0, 0, 1, 2, 2, 2])
col = np.array([0, 2, 2, 0, 1, 2])
data = np.array([1, 2, 3, 4, 5, 6])

# COO format (coordinate)
A_coo = sparse.coo_matrix((data, (row, col)), shape=(3, 3))

# Convert to CSR (efficient row operations)
A_csr = A_coo.tocsr()

# Convert to dense
A_dense = A_csr.toarray()
print(f"Dense matrix:\n{A_dense}")

# Sparse matrix operations
B = sparse.eye(3)  # Sparse identity
C = A_csr + B
D = A_csr @ B  # Matrix multiplication

print(f"Number of non-zeros: {A_csr.nnz}")
print(f"Sparsity: {1 - A_csr.nnz / (3*3):.2%}")
```

## Signal Processing (scipy.signal)

### Filter Design

```python
from scipy import signal
import numpy as np

# Butterworth filter design
b, a = signal.butter(4, 0.5, btype='low')

# Apply filter to signal
t = np.linspace(0, 1, 1000)
sig = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*50*t)
filtered = signal.filtfilt(b, a, sig)

# Chebyshev filter
b_cheby, a_cheby = signal.cheby1(4, 0.5, 0.5)

# Frequency response
w, h = signal.freqz(b, a)
print(f"Filter order: {len(b)-1}")
```

### Convolution and Correlation

```python
from scipy import signal
import numpy as np

# Signals
sig1 = np.array([1, 2, 3, 4, 5])
sig2 = np.array([0, 1, 0.5])

# Convolution
conv = signal.convolve(sig1, sig2, mode='same')
print(f"Convolution: {conv}")

# Correlation
corr = signal.correlate(sig1, sig2, mode='same')
print(f"Correlation: {corr}")

# 2D convolution (for images)
image = np.random.rand(100, 100)
kernel = np.array([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]]) / 4
filtered_img = signal.convolve2d(image, kernel, mode='same')
```

### Peak Finding

```python
from scipy import signal
import numpy as np

# Signal with peaks
t = np.linspace(0, 10, 1000)
sig = np.sin(2*np.pi*t) + 0.5*np.sin(2*np.pi*5*t)

# Find peaks
peaks, properties = signal.find_peaks(sig, height=0.5, distance=50)

print(f"Found {len(peaks)} peaks")
print(f"Peak positions: {peaks[:5]}")
print(f"Peak heights: {properties['peak_heights'][:5]}")

# Find local maxima with width
peaks_width, properties_width = signal.find_peaks(sig, width=20)
widths = properties_width['widths']
```

### Spectral Analysis

```python
from scipy import signal
import numpy as np

# Generate signal
fs = 1000  # Sampling frequency
t = np.linspace(0, 1, fs)
sig = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*120*t)

# Periodogram
f, Pxx = signal.periodogram(sig, fs)

# Welch's method (smoother estimate)
f_welch, Pxx_welch = signal.welch(sig, fs, nperseg=256)

# Spectrogram
f_spec, t_spec, Sxx = signal.spectrogram(sig, fs)

print(f"Frequency resolution: {f[1] - f[0]:.2f} Hz")
print(f"Number of frequency bins: {len(f)}")
```

## Statistics (scipy.stats)

### Probability Distributions

```python
from scipy import stats
import numpy as np

# Normal distribution
mu, sigma = 0, 1
norm = stats.norm(loc=mu, scale=sigma)

# PDF, CDF, PPF
x = np.linspace(-3, 3, 100)
pdf = norm.pdf(x)
cdf = norm.cdf(x)
ppf = norm.ppf(0.975)  # 97.5th percentile

print(f"P(X ≤ 1.96) = {norm.cdf(1.96):.4f}")
print(f"97.5th percentile: {ppf:.4f}")

# Generate random samples
samples = norm.rvs(size=1000)

# Other distributions
exponential = stats.expon(scale=2)
poisson = stats.poisson(mu=5)
binomial = stats.binom(n=10, p=0.5)
```

### Hypothesis Testing

```python
from scipy import stats
import numpy as np

# Generate two samples
np.random.seed(42)
sample1 = stats.norm.rvs(loc=0, scale=1, size=100)
sample2 = stats.norm.rvs(loc=0.5, scale=1, size=100)

# t-test (independent samples)
t_stat, p_value = stats.ttest_ind(sample1, sample2)
print(f"t-test: t = {t_stat:.4f}, p = {p_value:.4f}")

# Mann-Whitney U test (non-parametric)
u_stat, p_value_mw = stats.mannwhitneyu(sample1, sample2)
print(f"Mann-Whitney: U = {u_stat:.4f}, p = {p_value_mw:.4f}")

# Chi-square test
observed = np.array([10, 20, 30, 40])
expected = np.array([25, 25, 25, 25])
chi2, p_chi = stats.chisquare(observed, expected)
print(f"Chi-square: χ² = {chi2:.4f}, p = {p_chi:.4f}")

# Kolmogorov-Smirnov test (normality)
ks_stat, p_ks = stats.kstest(sample1, 'norm')
print(f"KS test: D = {ks_stat:.4f}, p = {p_ks:.4f}")
```

### Correlation and Regression

```python
from scipy import stats
import numpy as np

# Data
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = 2*x + 1 + np.random.randn(10)*0.5

# Pearson correlation
r, p_value = stats.pearsonr(x, y)
print(f"Pearson r = {r:.4f}, p = {p_value:.4f}")

# Spearman correlation (rank-based)
rho, p_spear = stats.spearmanr(x, y)
print(f"Spearman ρ = {rho:.4f}, p = {p_spear:.4f}")

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print(f"y = {slope:.4f}x + {intercept:.4f}")
print(f"R² = {r_value**2:.4f}")
```

## Fast Fourier Transform (scipy.fft)

### Basic FFT

```python
from scipy import fft
import numpy as np

# Time-domain signal
fs = 1000  # Sampling rate
T = 1/fs
N = 1000   # Number of samples
t = np.linspace(0, N*T, N)

# Signal: 50 Hz + 120 Hz
signal = np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*120*t)

# Compute FFT
yf = fft.fft(signal)
xf = fft.fftfreq(N, T)

# Magnitude spectrum
magnitude = np.abs(yf)

# Get positive frequencies only
positive_freq_idx = xf > 0
xf_positive = xf[positive_freq_idx]
magnitude_positive = magnitude[positive_freq_idx]

print(f"Peak frequencies: {xf_positive[magnitude_positive > 100]}")
```

### Inverse FFT

```python
from scipy import fft
import numpy as np

# Original signal
t = np.linspace(0, 1, 1000)
signal = np.sin(2*np.pi*10*t)

# FFT
signal_fft = fft.fft(signal)

# Modify in frequency domain (e.g., remove high frequencies)
signal_fft[100:] = 0

# Inverse FFT
signal_filtered = fft.ifft(signal_fft).real

print(f"Signal reconstructed: {np.allclose(signal[:100], signal_filtered[:100])}")
```

### 2D FFT (for images)

```python
from scipy import fft
import numpy as np

# Create 2D signal (image)
x = np.linspace(0, 2*np.pi, 128)
y = np.linspace(0, 2*np.pi, 128)
X, Y = np.meshgrid(x, y)
image = np.sin(5*X) * np.cos(5*Y)

# 2D FFT
image_fft = fft.fft2(image)
image_fft_shifted = fft.fftshift(image_fft)

# Magnitude spectrum
magnitude = np.abs(image_fft_shifted)

# Inverse 2D FFT
image_reconstructed = fft.ifft2(image_fft).real

print(f"Image shape: {image.shape}")
print(f"FFT shape: {image_fft.shape}")
```

## Spatial Algorithms (scipy.spatial)

### Distance Computations

```python
from scipy.spatial import distance
import numpy as np

# Two points
p1 = np.array([0, 0])
p2 = np.array([3, 4])

# Euclidean distance
eucl = distance.euclidean(p1, p2)
print(f"Euclidean distance: {eucl:.4f}")

# Manhattan distance
manh = distance.cityblock(p1, p2)
print(f"Manhattan distance: {manh:.4f}")

# Cosine distance
cosine = distance.cosine(p1, p2)

# Pairwise distances
points = np.random.rand(10, 2)
dist_matrix = distance.cdist(points, points, 'euclidean')
print(f"Distance matrix shape: {dist_matrix.shape}")
```

### Convex Hull

```python
from scipy.spatial import ConvexHull
import numpy as np

# Random points
points = np.random.rand(30, 2)

# Compute convex hull
hull = ConvexHull(points)

print(f"Number of vertices: {len(hull.vertices)}")
print(f"Hull area: {hull.area:.4f}")
print(f"Hull volume (perimeter): {hull.volume:.4f}")

# Get hull points
hull_points = points[hull.vertices]
```

### Delaunay Triangulation

```python
from scipy.spatial import Delaunay
import numpy as np

# Points
points = np.random.rand(30, 2)

# Triangulation
tri = Delaunay(points)

print(f"Number of triangles: {len(tri.simplices)}")

# Check if point is in triangulation
test_point = np.array([0.5, 0.5])
simplex_index = tri.find_simplex(test_point)
print(f"Point inside: {simplex_index >= 0}")
```

### KDTree for Nearest Neighbors

```python
from scipy.spatial import KDTree
import numpy as np

# Build tree
points = np.random.rand(100, 3)
tree = KDTree(points)

# Query nearest neighbors
query_point = np.array([0.5, 0.5, 0.5])
distances, indices = tree.query(query_point, k=5)

print(f"5 nearest neighbors:")
print(f"Distances: {distances}")
print(f"Indices: {indices}")

# Query within radius
indices_radius = tree.query_ball_point(query_point, r=0.3)
print(f"Points within r=0.3: {len(indices_radius)}")
```

## Practical Workflows

### Numerical Integration of Physical System

```python
from scipy.integrate import odeint
import numpy as np

# Damped harmonic oscillator: m*x'' + c*x' + k*x = 0
def damped_oscillator(y, t, m, c, k):
    x, v = y
    dxdt = v
    dvdt = -(c/m)*v - (k/m)*x
    return [dxdt, dvdt]

# Parameters
m = 1.0  # mass
c = 0.5  # damping
k = 10.0  # spring constant

# Initial conditions
y0 = [1.0, 0.0]  # [position, velocity]

# Time points
t = np.linspace(0, 10, 1000)

# Solve
solution = odeint(damped_oscillator, y0, t, args=(m, c, k))

position = solution[:, 0]
velocity = solution[:, 1]

print(f"Final position: {position[-1]:.6f}")
print(f"Final velocity: {velocity[-1]:.6f}")
```

### Parameter Estimation from Data

```python
from scipy import optimize
import numpy as np

# Generate synthetic data
x_true = np.linspace(0, 10, 50)
params_true = [2.5, 1.3, 0.8]
y_true = params_true[0] * np.exp(-params_true[1] * x_true) + params_true[2]
y_data = y_true + 0.2 * np.random.randn(len(x_true))

# Model
def model(x, a, b, c):
    return a * np.exp(-b * x) + c

# Objective function (residual sum of squares)
def objective(params):
    y_pred = model(x_true, *params)
    return np.sum((y_data - y_pred)**2)

# Optimize
params_init = [1.0, 1.0, 1.0]
result = optimize.minimize(objective, params_init)

print(f"True parameters: {params_true}")
print(f"Estimated parameters: {result.x}")
print(f"Relative errors: {np.abs(result.x - params_true) / params_true * 100}%")
```

### Signal Filtering Pipeline

```python
from scipy import signal
import numpy as np

def filter_pipeline(noisy_signal, fs):
    """Complete signal processing pipeline."""
    # 1. Design Butterworth lowpass filter
    fc = 10  # Cutoff frequency
    w = fc / (fs / 2)  # Normalized frequency
    b, a = signal.butter(4, w, 'low')
    
    # 2. Apply filter (zero-phase)
    filtered = signal.filtfilt(b, a, noisy_signal)
    
    # 3. Remove baseline drift
    baseline = signal.medfilt(filtered, kernel_size=51)
    detrended = filtered - baseline
    
    # 4. Normalize
    normalized = (detrended - np.mean(detrended)) / np.std(detrended)
    
    return normalized

# Example usage
fs = 1000
t = np.linspace(0, 1, fs)
clean_signal = np.sin(2*np.pi*5*t)
noise = 0.5 * np.random.randn(len(t))
drift = 0.1 * t
noisy_signal = clean_signal + noise + drift

processed = filter_pipeline(noisy_signal, fs)
print(f"Original SNR: {10*np.log10(np.var(clean_signal)/np.var(noise)):.2f} dB")
```

### Interpolation and Smoothing

```python
from scipy import interpolate
import numpy as np

# Noisy data
x = np.linspace(0, 10, 20)
y_true = np.sin(x)
y_noisy = y_true + 0.3 * np.random.randn(len(x))

# Smoothing spline
spl = interpolate.UnivariateSpline(x, y_noisy, s=2)

# Evaluate on fine grid
x_fine = np.linspace(0, 10, 200)
y_smooth = spl(x_fine)

# Compare with true function
y_true_fine = np.sin(x_fine)
rmse = np.sqrt(np.mean((y_smooth - y_true_fine)**2))

print(f"RMSE: {rmse:.6f}")

# Can also get derivatives
y_prime = spl.derivative()(x_fine)
y_double_prime = spl.derivative(n=2)(x_fine)
```

### Statistical Analysis Workflow

```python
from scipy import stats
import numpy as np

def analyze_experiment(control, treatment):
    """Complete statistical analysis of experiment data."""
    results = {}
    
    # 1. Descriptive statistics
    results['control_mean'] = np.mean(control)
    results['treatment_mean'] = np.mean(treatment)
    results['control_std'] = np.std(control, ddof=1)
    results['treatment_std'] = np.std(treatment, ddof=1)
    
    # 2. Normality tests
    _, results['control_normal_p'] = stats.shapiro(control)
    _, results['treatment_normal_p'] = stats.shapiro(treatment)
    
    # 3. Choose appropriate test
    if results['control_normal_p'] > 0.05 and results['treatment_normal_p'] > 0.05:
        # Both normal: use t-test
        t_stat, p_value = stats.ttest_ind(control, treatment)
        results['test'] = 't-test'
        results['statistic'] = t_stat
        results['p_value'] = p_value
    else:
        # Non-normal: use Mann-Whitney U
        u_stat, p_value = stats.mannwhitneyu(control, treatment)
        results['test'] = 'Mann-Whitney U'
        results['statistic'] = u_stat
        results['p_value'] = p_value
    
    # 4. Effect size (Cohen's d)
    pooled_std = np.sqrt((results['control_std']**2 + 
                          results['treatment_std']**2) / 2)
    results['cohens_d'] = ((results['treatment_mean'] - 
                            results['control_mean']) / pooled_std)
    
    return results

# Example
control = stats.norm.rvs(loc=10, scale=2, size=30)
treatment = stats.norm.rvs(loc=12, scale=2, size=30)

results = analyze_experiment(control, treatment)
print(f"Test: {results['test']}")
print(f"p-value: {results['p_value']:.4f}")
print(f"Effect size: {results['cohens_d']:.4f}")
```

## Performance Optimization

### Choosing the Right Method

```python
from scipy import integrate, optimize
import numpy as np
import time

# Function to integrate
def f(x):
    return np.exp(-x**2)

# Compare integration methods
methods = ['quad', 'romberg', 'simpson']
times = []

for method in methods:
    start = time.time()
    if method == 'quad':
        result, _ = integrate.quad(f, 0, 10)
    elif method == 'romberg':
        x = np.linspace(0, 10, 1000)
        result = integrate.romberg(f, 0, 10)
    elif method == 'simpson':
        x = np.linspace(0, 10, 1000)
        y = f(x)
        result = integrate.simpson(y, x)
    elapsed = time.time() - start
    times.append(elapsed)
    print(f"{method}: {result:.8f} ({elapsed*1000:.2f} ms)")
```

### Vectorization

```python
from scipy import interpolate
import numpy as np

# Bad: Loop over points
def interpolate_loop(x, y, x_new):
    results = []
    for xi in x_new:
        # Create interpolator for each point (very slow!)
        f = interpolate.interp1d(x, y)
        results.append(f(xi))
    return np.array(results)

# Good: Vectorized
def interpolate_vectorized(x, y, x_new):
    f = interpolate.interp1d(x, y)
    return f(x_new)  # Pass entire array

# Benchmark
x = np.linspace(0, 10, 100)
y = np.sin(x)
x_new = np.linspace(0, 10, 1000)

# Only use vectorized version (loop version is too slow)
result = interpolate_vectorized(x, y, x_new)
```

## Common Pitfalls and Solutions

### Integration Convergence

```python
from scipy import integrate
import numpy as np

# Problem: Oscillatory function
def oscillatory(x):
    return np.sin(100*x) / x if x != 0 else 100

# Bad: Default parameters may not converge well
result, error = integrate.quad(oscillatory, 0, 1)

# Good: Increase limit and tolerance
result, error = integrate.quad(oscillatory, 0, 1, 
                               limit=100, epsabs=1e-10, epsrel=1e-10)

# Good: For highly oscillatory, use special methods
from scipy.integrate import quad_vec
result, error = quad_vec(oscillatory, 0, 1)
```

### Optimization Local Minima

```python
from scipy import optimize
import numpy as np

# Function with multiple minima
def multi_minima(x):
    return np.sin(x) + np.sin(10*x/3)

# Bad: Single starting point may find local minimum
result = optimize.minimize(multi_minima, x0=0)
print(f"Local minimum: {result.x[0]:.4f}")

# Good: Try multiple starting points
x0_list = np.linspace(0, 10, 20)
results = [optimize.minimize(multi_minima, x0=x0) for x0 in x0_list]
global_min = min(results, key=lambda r: r.fun)
print(f"Global minimum: {global_min.x[0]:.4f}")

# Best: Use global optimization
result_global = optimize.differential_evolution(multi_minima, bounds=[(0, 10)])
print(f"Global (DE): {result_global.x[0]:.4f}")
```

### Statistical Test Assumptions

```python
from scipy import stats
import numpy as np

# Generate non-normal data
non_normal = stats.expon.rvs(size=30)

# Bad: Using t-test without checking normality
t_stat, p_value = stats.ttest_1samp(non_normal, 1.0)

# Good: Check normality first
_, p_normal = stats.shapiro(non_normal)
if p_normal < 0.05:
    print("Data is not normal, using Wilcoxon test")
    stat, p_value = stats.wilcoxon(non_normal - 1.0)
else:
    t_stat, p_value = stats.ttest_1samp(non_normal, 1.0)
```

### Sparse Matrix Efficiency

```python
from scipy import sparse
import numpy as np
import time

# Large sparse matrix
n = 10000
density = 0.01
data = np.random.rand(int(n*n*density))
row = np.random.randint(0, n, len(data))
col = np.random.randint(0, n, len(data))

# Bad: Convert to dense
A_coo = sparse.coo_matrix((data, (row, col)), shape=(n, n))
# A_dense = A_coo.toarray()  # Uses huge memory!

# Good: Keep sparse and use appropriate format
A_csr = A_coo.tocsr()  # Efficient for row operations
A_csc = A_coo.tocsc()  # Efficient for column operations

# Sparse operations
x = np.random.rand(n)
y = A_csr @ x  # Fast sparse matrix-vector product

print(f"Sparse matrix: {A_csr.nnz / (n*n) * 100:.2f}% non-zero")
```

This comprehensive SciPy guide covers 50+ examples across all major scientific computing workflows!
