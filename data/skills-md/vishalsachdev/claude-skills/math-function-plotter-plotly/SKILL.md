---
name: math-function-plotter-plotly
description: This skill generates interactive mathematical function plots using Plotly.js for iframe embedding in intelligent textbooks. Creates visualizations with hover tooltips, interactive sliders to move points along curves, responsive design optimized for narrow layouts, and comprehensive educational documentation. Use this when users request plotting mathematical functions, graphing equations, visualizing f(x), or creating interactive function explorers for calculus, precalculus, physics, or engineering courses.
---

# Math Function Plotter - Plotly.js MicroSim Generator

## Overview

This skill generates interactive mathematical function plots using the Plotly.js JavaScript library. Each MicroSim is optimized for iframe embedding in narrow textbook layouts with minimal margins, responsive design, hover tooltips showing precise coordinates, and interactive sliders allowing users to explore points along the curve.

The skill creates complete MicroSim packages following the repository's standardized structure, including standalone HTML files, responsive CSS, interactive JavaScript, comprehensive markdown documentation, and Dublin Core metadata.

## When to Use This Skill

Invoke this skill when users request:

- "Plot a mathematical function"
- "Graph the equation y = ..."
- "Visualize f(x) = ..."
- "Create an interactive function plotter"
- "Show me a graph of [trigonometric/polynomial/exponential] function"
- "Make a plot I can embed in my textbook"
- "Generate a calculus visualization"
- "Create an interactive sine/cosine/tangent graph"

## Workflow

Follow these steps to create a mathematical function plot MicroSim:

### Step 1: Gather Requirements

Ask the user for the following information:

**Required:**

- **Function expression**: The mathematical function to plot (e.g., "sin(x)", "x^2", "e^(-x^2)")
- **Title**: Name for the MicroSim (e.g., "Sine Function", "Quadratic Function")
- **Domain**: Range of x-values to plot [xMin, xMax]

**Optional (with smart defaults):**

- **Range**: Y-axis limits [yMin, yMax] (auto-calculated if not provided)
- **Interactive point**: Initial x-position for the slider (default: midpoint of domain)
- **Slider step**: Increment for slider movement (default: (xMax - xMin) / 100)
- **Axis labels**: Custom labels for x and y axes (default: "x" and "y")
- **Subtitle**: Brief description (default: function expression)
- **Context**: Course/chapter where this will be used (for educational content)

**Example conversation:**

```
User: "Create a plot for the sine function"
Assistant: "I'll create an interactive sine function plot. Let me gather some details:

- Title: 'Sine Function Visualization'
- Function: sin(x)
- Domain: Would you like -2π to 2π (approximately -6.28 to 6.28)?
- Is this for a specific course or chapter?"
```

Use clear, friendly language when prompting users. Provide sensible defaults based on common mathematical conventions.

### Step 2: Create Directory Structure

Create the MicroSim directory following the standardized pattern:

```bash
docs/sims/[microsim-name]/
├── main.html
├── style.css
├── script.js
├── index.md
└── metadata.json
```

**Naming conventions:**

- Use kebab-case (lowercase with hyphens)
- Be descriptive but concise
- Examples: `sine-function`, `quadratic-parabola`, `exponential-decay`, `gaussian-bell-curve`

### Step 3: Generate main.html

Use the template from `assets/template-iframe-main.html` and replace placeholders:

**Placeholder replacements:**

- `{{TITLE}}` → Full title (e.g., "Sine Function Visualization")
- `{{SUBTITLE}}` → Function expression or description (e.g., "y = sin(x)")
- `{{X_MIN}}` → Minimum x value (e.g., -6.28)
- `{{X_MAX}}` → Maximum x value (e.g., 6.28)
- `{{X_STEP}}` → Slider step size (e.g., 0.01)
- `{{INITIAL_X}}` → Initial slider position (e.g., 0)

**Key features to preserve:**

- Minimal body margins (`margin: 0; padding: 0;`)
- Plotly.js CDN link (v2.27.0 or latest stable)
- Link to external `style.css` and `script.js`
- Semantic HTML5 structure

### Step 4: Generate style.css

Use the template from `assets/template-iframe-style.css`.

**Critical requirements:**

- **Body margins**: MUST be `margin: 0; padding: 0;` for iframe embedding
- **Container padding**: Maximum 5px (reduces to 2px on mobile)
- **Header margins**: Maximum 5px top, 2px bottom
- **Background**: Use `aliceblue` (repository standard)
- **Responsive breakpoints**: 768px (tablet), 480px (mobile)
- **Plot height**: 400px desktop, 300px tablet, 250px mobile

**Testing**: Ensure the visualization looks good at widths from 320px to 1200px.

### Step 5: Generate script.js

Use the template from `assets/template-script.js` and replace placeholders:

**Placeholder replacements:**

- `{{FUNCTION_JS}}` → JavaScript function definition
  ```javascript
  function f(x) {
      return Math.sin(x);  // Example
  }
  ```
- `{{X_MIN}}`, `{{X_MAX}}` → Domain limits
- `{{Y_MIN}}`, `{{Y_MAX}}` → Range limits (or calculate automatically)
- `{{FUNCTION_LABEL}}` → Legend label (e.g., "y = sin(x)")
- `{{X_LABEL}}` → X-axis label (default: "x")
- `{{Y_LABEL}}` → Y-axis label (default: "y")
- `{{FILENAME}}` → Export filename (e.g., "sine-function")

**Function conversion guide:**

Common mathematical expressions to JavaScript:

| Math Notation | JavaScript Code |
|--------------|----------------|
| sin(x) | Math.sin(x) |
| cos(x) | Math.cos(x) |
| tan(x) | Math.tan(x) |
| e^x | Math.exp(x) |
| x^2 | Math.pow(x, 2) or x**2 |
| √x | Math.sqrt(x) |
| ln(x) | Math.log(x) |
| log₁₀(x) | Math.log10(x) |
| \|x\| | Math.abs(x) |

**Auto-calculate range** if not provided:

```javascript
// Sample the function to find y range
const samplePoints = 100;
const yValues = [];
for (let i = 0; i <= samplePoints; i++) {
    const x = xMin + (xMax - xMin) * i / samplePoints;
    yValues.push(f(x));
}
const yMin = Math.min(...yValues) * 1.1;  // Add 10% padding
const yMax = Math.max(...yValues) * 1.1;
```

### Step 6: Create index.md Documentation

Use the template from `assets/template-index.md` and customize:

**Required sections:**

1. **YAML frontmatter** with title, description, quality_score
2. **Level 1 header** matching the title
3. **Interactive visualization** (iframe embed)
4. **Fullscreen link button**
5. **Copy-paste embed code** in HTML code block
6. **Overview** - Purpose and features
7. **How to Use** - Step-by-step instructions
8. **Educational Applications** - Subject-specific use cases
9. **Customization Guide** - How to modify the MicroSim
10. **Technical Details** - Library version, implementation notes
11. **Lesson Plan Suggestions** - Learning objectives, activities, assessments
12. **References** - Links to documentation and resources

**Customization for specific functions:**

- **Trigonometric**: Mention periodicity, amplitude, phase shift
- **Polynomial**: Discuss degree, roots, turning points
- **Exponential**: Highlight growth/decay, asymptotes
- **Logarithmic**: Note domain restrictions, inverse relationships

**Lesson plan quality**: Provide specific, actionable activities with questions that use the slider interactivity. Example:

```markdown
**Activity 1: Finding Specific Values (10 minutes)**

1. Use the slider to find f(π/2). What value do you observe?
2. At what x-value does f(x) = 0.5? (Approximate using the slider)
3. Challenge: Find all x-values where f(x) = 0 in the visible range.
```

### Step 7: Create metadata.json

Use the template from `assets/template-metadata.json`:

**Required Dublin Core fields:**

- `title` - Same as MicroSim title
- `description` - 1-2 sentence summary
- `creator` - Author name or organization
- `date` - Creation date (YYYY-MM-DD format)
- `subject` - Array of keywords (include "mathematics" plus specific topics)
- `type` - Always "Interactive Simulation"
- `format` - Always "text/html"
- `language` - Always "en-US"
- `rights` - License (typically "CC BY 4.0")

**Optional educational fields:**

- `audience` - Target learners (e.g., "High school students", "College undergraduates")
- `educationalLevel` - Grade/level (e.g., "Grade 11-12", "Undergraduate")
- `learningResourceType` - Always "Interactive Plot"
- `interactivityType` - Always "active"
- `typicalLearningTime` - ISO 8601 duration (e.g., "PT10M" for 10 minutes)

**Subject keyword selection:**

Choose 3-5 specific keywords from:

- Mathematics: algebra, geometry, trigonometry, calculus, statistics
- Physics: kinematics, waves, thermodynamics, electromagnetism
- Engineering: signals, control-systems, circuits
- Computer Science: algorithms, numerical-methods, machine-learning

### Step 8: Test and Validate

Perform the following checks:

**Visual Testing:**

1. Open `main.html` in a browser
2. Verify the plot renders correctly
3. Check that axes are labeled and readable
4. Confirm tooltips appear on hover
5. Test slider interaction - point should move smoothly along curve
6. Resize browser window - verify responsive behavior

**Functional Testing:**

1. Slider range: Ensure slider covers the full x domain
2. Point accuracy: Verify point position matches slider value
3. Tooltips: Check coordinate precision (3 decimal places)
4. Export: Test PNG export functionality
5. Mobile: Test on small screen sizes (320px width minimum)

**Documentation Review:**

1. Verify iframe embed works in `index.md`
2. Check all placeholders are replaced
3. Ensure lesson plan is specific to the function
4. Validate all markdown links work

**Metadata Validation:**

1. Confirm `metadata.json` is valid JSON
2. Check all required Dublin Core fields are present
3. Verify subject keywords are relevant

**Integration (if part of a textbook project):**

1. Update `mkdocs.yml` navigation if needed
2. Add references to the MicroSim in relevant chapters
3. Link from glossary terms if applicable

## Best Practices

### Educational Design

1. **Tooltip content**: Use educational definitions, not just raw coordinates
   - Good: "At x=π/2 (1.571), sin(x) reaches its maximum value of 1"
   - Avoid: "1.571, 1.000"

2. **Slider purpose**: Design slider activities that promote exploration
   - "Find where f(x) = 0"
   - "What happens as x approaches infinity?"
   - "Locate the maximum value"

3. **Lesson integration**: Reference specific textbook concepts
   - Link to chapter sections
   - Use consistent notation with textbook
   - Address common misconceptions

### Technical Design

1. **Function sampling**: Use 500 points minimum for smooth curves
2. **Domain selection**: Choose domains that show key features
   - Trigonometric: Show 1-3 complete periods
   - Polynomial: Include all real roots if possible
   - Exponential: Show meaningful change (3-5 orders of magnitude)

3. **Range calculation**: Add 10% padding above/below extrema for visual clarity

4. **Responsive design**: Test at widths: 320px, 480px, 768px, 1024px, 1200px

5. **Performance**: Keep total points under 2000 for smooth rendering

### Accessibility

1. **Color choices**: Ensure sufficient contrast (WCAG AA minimum)
2. **Font sizes**: Minimum 12px, scale up to 16px on desktop
3. **Alt text**: Provide text descriptions of function behavior
4. **Keyboard navigation**: Slider should be keyboard-accessible (built-in with HTML range input)

### Documentation Quality

1. **Mathematical notation**: Use proper LaTeX or Unicode symbols
   - π not pi, ≈ not ~, ² not ^2 (in markdown text)
2. **Code examples**: Provide copy-paste ready snippets
3. **References**: Link to authoritative sources (MDN, Plotly docs, math references)

## Common Function Configurations

### Trigonometric Functions

```javascript
// Sine function
function f(x) { return Math.sin(x); }
// Domain: -2π to 2π (-6.28 to 6.28)
// Range: -1.5 to 1.5

// Cosine function
function f(x) { return Math.cos(x); }
// Domain: -2π to 2π
// Range: -1.5 to 1.5

// Tangent function (with discontinuities)
function f(x) { return Math.tan(x); }
// Domain: -π to π (-3.14 to 3.14)
// Range: -10 to 10 (limited for visibility)

// Damped sine wave
function f(x) { return Math.exp(-x/5) * Math.sin(x); }
// Domain: 0 to 20
// Range: Auto-calculate
```

### Polynomial Functions

```javascript
// Quadratic
function f(x) { return x**2; }
// Domain: -5 to 5
// Range: 0 to 25

// Cubic
function f(x) { return x**3 - 3*x; }
// Domain: -3 to 3
// Range: Auto-calculate

// Quartic with multiple turning points
function f(x) { return x**4 - 4*x**2 + 1; }
// Domain: -3 to 3
// Range: Auto-calculate
```

### Exponential and Logarithmic

```javascript
// Exponential growth
function f(x) { return Math.exp(x); }
// Domain: -2 to 2
// Range: 0 to 10

// Exponential decay
function f(x) { return Math.exp(-x); }
// Domain: 0 to 5
// Range: 0 to 1.2

// Natural logarithm
function f(x) { return Math.log(x); }
// Domain: 0.1 to 10 (must be positive)
// Range: Auto-calculate

// Gaussian/Normal distribution
function f(x) {
    const mu = 0, sigma = 1;
    return Math.exp(-0.5 * ((x-mu)/sigma)**2) / (sigma * Math.sqrt(2*Math.PI));
}
// Domain: -4 to 4
// Range: 0 to 0.5
```

### Physics and Engineering

```javascript
// Projectile motion (trajectory)
function f(x) {
    const v0 = 20, angle = 45 * Math.PI/180, g = 9.8;
    return x * Math.tan(angle) - (g * x**2) / (2 * v0**2 * Math.cos(angle)**2);
}
// Domain: 0 to 40
// Range: Auto-calculate

// Simple harmonic motion
function f(x) {
    const A = 1, omega = 2, phi = 0;
    return A * Math.cos(omega * x + phi);
}
// Domain: 0 to 10
// Range: -1.5 to 1.5
```

## Troubleshooting

### Issue: Plot appears blank

**Causes:**
- Function returns NaN for some x-values
- Domain/range mismatch
- JavaScript function syntax error

**Solutions:**
- Check browser console for errors
- Verify function definition in `script.js`
- Test function with sample values: `console.log(f(0), f(1), f(-1))`
- Add domain validation:
  ```javascript
  function f(x) {
      if (x <= 0) return NaN;  // For log functions
      return Math.log(x);
  }
  ```

### Issue: Slider doesn't update the point

**Causes:**
- Incorrect trace index in `Plotly.restyle`
- Event listener not attached
- Slider ID mismatch

**Solutions:**
- Verify point trace is index 1 (curve is index 0)
- Check slider ID matches: `document.getElementById('x-slider')`
- Confirm event listener is after DOM load
- Test with: `console.log('Slider value:', e.target.value)`

### Issue: Tooltips show incorrect values

**Causes:**
- Hover template formatting error
- Point coordinates not calculated correctly

**Solutions:**
- Check `hovertemplate` syntax in trace definition
- Verify decimal precision: `%{x:.3f}` for 3 decimal places
- Test point calculation: `console.log(pointX, pointY)`

### Issue: Layout too cramped in iframe

**Causes:**
- Margins/padding too large
- Plot height too tall for container

**Solutions:**
- Reduce container padding to 2-5px maximum
- Check responsive breakpoints are working
- Test iframe height: Try 500px, 600px, 700px
- Verify `margin` in Plotly layout:
  ```javascript
  margin: { l: 50, r: 20, t: 10, b: 50 }
  ```

### Issue: Function looks jagged/pixelated

**Causes:**
- Not enough sample points
- Domain too large for point count

**Solutions:**
- Increase `numPoints` in config (try 500-1000)
- For discontinuous functions, handle special points
- Add more points near areas of rapid change

## References

### Plotly.js Documentation

- [Plotly.js Official Documentation](https://plotly.com/javascript/)
- [Line Charts Guide](https://plotly.com/javascript/line-charts/)
- [Scatter Plots](https://plotly.com/javascript/line-and-scatter/)
- [Hover Text and Formatting](https://plotly.com/javascript/hover-text-and-formatting/)
- [Layout Configuration](https://plotly.com/javascript/reference/layout/)
- [Responsive Plots](https://plotly.com/javascript/responsive-fluid-layout/)

### JavaScript Math Functions

- [MDN Math Object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math)
- [Math.sin()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/sin)
- [Math.pow()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/pow)
- [Math.exp()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/exp)

### Educational Resources

- [Desmos Graphing Calculator](https://www.desmos.com/calculator) - Reference for function visualization
- [GeoGebra](https://www.geogebra.org/) - Interactive mathematics software
- [Khan Academy - Functions](https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:functions)

### MicroSim Standards

- [MicroSim Standardization Skill](../microsim-standardization/SKILL.md) - Quality rubric and requirements
- [Dublin Core Metadata](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) - Metadata standards
- [Plotly.js CDN](https://cdn.plot.ly/) - Latest library versions
