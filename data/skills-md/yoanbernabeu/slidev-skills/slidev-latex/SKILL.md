---
name: slidev-latex
description: Render mathematical formulas with LaTeX/KaTeX in Slidev. Use this skill for equations, mathematical notation, and scientific content.
---

# LaTeX/KaTeX in Slidev

This skill covers rendering mathematical formulas and scientific notation in Slidev using KaTeX, a fast LaTeX math rendering library.

## When to Use This Skill

- Writing mathematical equations
- Scientific presentations
- Technical documentation
- Academic content
- Physics, chemistry, or engineering formulas

## Basic Syntax

### Inline Math

Surround with single `$`:

```markdown
The quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$ where $a \neq 0$.
```

### Block Math

Surround with double `$$`:

```markdown
$$
E = mc^2
$$
```

Or with line breaks:

```markdown
$$
\begin{aligned}
f(x) &= x^2 + 2x + 1 \\
     &= (x + 1)^2
\end{aligned}
$$
```

## Common Mathematical Notations

### Fractions

```markdown
Simple: $\frac{a}{b}$

Nested: $\frac{1}{\frac{a}{b} + c}$

Display: $$\frac{x^2 + y^2}{z}$$
```

### Exponents and Subscripts

```markdown
Exponent: $x^2$, $e^{i\pi}$
Subscript: $x_1$, $a_{ij}$
Combined: $x_1^2$, $a_{ij}^{n+1}$
```

### Square Roots

```markdown
Simple: $\sqrt{x}$
N-th root: $\sqrt[n]{x}$
Complex: $\sqrt{x^2 + y^2}$
```

### Greek Letters

```markdown
Lowercase: $\alpha$, $\beta$, $\gamma$, $\delta$, $\epsilon$, $\theta$, $\lambda$, $\mu$, $\pi$, $\sigma$, $\omega$

Uppercase: $\Gamma$, $\Delta$, $\Theta$, $\Lambda$, $\Pi$, $\Sigma$, $\Omega$
```

### Operators

```markdown
Sum: $\sum_{i=1}^{n} x_i$

Product: $\prod_{i=1}^{n} x_i$

Integral: $\int_{a}^{b} f(x) \, dx$

Double integral: $\iint_D f(x,y) \, dA$

Limit: $\lim_{x \to \infty} f(x)$
```

## Equations and Formulas

### Famous Equations

```markdown
$$
\text{Euler's Identity: } e^{i\pi} + 1 = 0
$$

$$
\text{Pythagorean: } a^2 + b^2 = c^2
$$

$$
\text{Einstein: } E = mc^2
$$

$$
\text{Schrödinger: } i\hbar\frac{\partial}{\partial t}\Psi = \hat{H}\Psi
$$
```

### Systems of Equations

```markdown
$$
\begin{cases}
x + y = 10 \\
2x - y = 5
\end{cases}
$$
```

### Aligned Equations

```markdown
$$
\begin{aligned}
(x + y)^2 &= x^2 + 2xy + y^2 \\
(x - y)^2 &= x^2 - 2xy + y^2 \\
(x + y)(x - y) &= x^2 - y^2
\end{aligned}
$$
```

### Matrices

```markdown
$$
A = \begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

$$
B = \begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}
$$

$$
\det(A) = \begin{vmatrix}
a & b \\
c & d
\end{vmatrix} = ad - bc
$$
```

## Mathematical Symbols

### Comparison

```markdown
$<$, $>$, $\leq$, $\geq$, $\neq$, $\approx$, $\equiv$, $\sim$
```

### Logic

```markdown
$\forall$ (for all), $\exists$ (exists), $\neg$ (not)
$\land$ (and), $\lor$ (or), $\Rightarrow$ (implies)
```

### Sets

```markdown
$\in$ (in), $\notin$ (not in), $\subset$, $\subseteq$
$\cup$ (union), $\cap$ (intersection)
$\emptyset$ (empty set), $\mathbb{R}$ (reals), $\mathbb{N}$ (naturals)
```

### Calculus

```markdown
$\frac{dy}{dx}$, $\frac{\partial f}{\partial x}$
$\nabla f$, $\nabla \cdot F$, $\nabla \times F$
```

### Arrows

```markdown
$\rightarrow$, $\leftarrow$, $\leftrightarrow$
$\Rightarrow$, $\Leftarrow$, $\Leftrightarrow$
$\mapsto$, $\to$
```

## Advanced Features

### Line Highlighting in Math

````markdown
$$ {1|3|all}
\begin{aligned}
f(x) &= x^2 \\      // Click 1
f'(x) &= 2x \\      // Click 1
f''(x) &= 2         // Click 2
\end{aligned}
$$
````

### Custom Colors

```markdown
$$
{\color{red} x^2} + {\color{blue} y^2} = {\color{green} z^2}
$$
```

### Boxed Formulas

```markdown
$$
\boxed{E = mc^2}
$$
```

### Text in Math

```markdown
$$
f(x) = \begin{cases}
x & \text{if } x \geq 0 \\
-x & \text{otherwise}
\end{cases}
$$
```

## Chemistry Formulas

Enable mhchem extension in `vite.config.ts`:

```typescript
import 'katex/contrib/mhchem'
export default {}
```

Then use:

```markdown
$$\ce{H2O}$$

$$\ce{2H2 + O2 -> 2H2O}$$

$$\ce{CO2 + C -> 2CO}$$

$$\ce{Hg^2+ ->[I-] HgI2 ->[I-] [Hg^{II}I4]^2-}$$
```

## Physics Formulas

### Mechanics

```markdown
$$
F = ma \quad \text{(Newton's Second Law)}
$$

$$
W = \int_a^b \vec{F} \cdot d\vec{s}
$$

$$
KE = \frac{1}{2}mv^2
$$
```

### Electromagnetism

```markdown
$$
\vec{F} = q(\vec{E} + \vec{v} \times \vec{B})
$$

$$
\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}
$$
```

### Quantum Mechanics

```markdown
$$
\hat{p} = -i\hbar\frac{\partial}{\partial x}
$$

$$
\Delta x \cdot \Delta p \geq \frac{\hbar}{2}
$$
```

## Statistics

```markdown
$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

$$
\sigma^2 = \frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2
$$

$$
P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}
$$
```

## Machine Learning

```markdown
$$
J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}[y^{(i)}\log(h_\theta(x^{(i)})) + (1-y^{(i)})\log(1-h_\theta(x^{(i)}))]
$$

$$
\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}
$$

$$
\nabla_\theta J(\theta) = \frac{1}{m} X^T (h_\theta(X) - y)
$$
```

## Best Practices

### 1. Keep Formulas Readable

❌ **Too dense**
```markdown
$\frac{\frac{a}{b}+\frac{c}{d}}{\frac{e}{f}-\frac{g}{h}}$
```

✓ **Broken into steps**
```markdown
Let $x = \frac{a}{b} + \frac{c}{d}$ and $y = \frac{e}{f} - \frac{g}{h}$

Then the result is $\frac{x}{y}$
```

### 2. Use Display Mode for Complex Formulas

❌ **Complex inline**
```markdown
The integral $\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$ is fundamental.
```

✓ **Display mode**
```markdown
The Gaussian integral:
$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$
```

### 3. Add Context

```markdown
**Theorem**: For any triangle with sides $a$, $b$, $c$:

$$a^2 + b^2 = c^2$$

*where $c$ is the hypotenuse.*
```

### 4. Use Aligned for Multi-Step

```markdown
$$
\begin{aligned}
\text{Given: } & x + y = 5 \\
\text{And: } & x - y = 1 \\
\text{Adding: } & 2x = 6 \\
\text{Therefore: } & x = 3, y = 2
\end{aligned}
$$
```

## Common Mistakes

❌ **Missing escape for special characters**
```markdown
$50%$ (error!)
```

✓ **Escaped correctly**
```markdown
$50\%$
```

❌ **Missing braces for multi-character**
```markdown
$x^10$ (shows x¹0)
```

✓ **With braces**
```markdown
$x^{10}$
```

## Output Format

When creating math content:

```markdown
# [Topic Title]

[Brief explanation of the concept]

**Definition/Formula:**
$$
[Main formula in display mode]
$$

**Where:**
- $[variable]$ = [meaning]
- $[variable]$ = [meaning]

**Example:**
[Step-by-step solution]

$$
\begin{aligned}
\text{Step 1: } & [equation] \\
\text{Step 2: } & [equation] \\
\text{Result: } & [final answer]
\end{aligned}
$$
```
