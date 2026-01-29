---
name: venn-diagram-generator
description: This skill generates interactive Venn diagram visualizations using the venn.js JavaScript library. Use this skill when users request creating Venn diagrams, set visualizations, overlap diagrams, or comparison charts for educational textbooks. The skill creates complete MicroSim packages with standalone HTML files featuring colorful circles, clear labels, and interactive tooltips, saved to /docs/sims/ following the MicroSim pattern.
---

# Venn Diagram Generator

## Overview

Generate interactive Venn diagram visualizations using venn.js and D3.js for intelligent textbooks. Creates complete MicroSim packages with standalone HTML files, MkDocs integration, and Dublin Core metadata. Each diagram features customizable colors, interactive tooltips, and follows the educational MicroSim pattern for seamless integration into educational content.

## When to Use This Skill

Use the venn-diagram-generator skill when users request:

- Venn diagrams showing set relationships
- Comparison diagrams between 2-4 categories
- Visual representations of overlapping concepts
- Set theory illustrations
- Intersection and union visualizations
- Categorical relationship diagrams
- Euler diagrams

**Example user requests:**
- "Create a Venn diagram comparing Python, JavaScript, and Java"
- "Make a 2-circle Venn diagram showing cats and dogs"
- "Generate a diagram showing the overlap between AI, ML, and Data Science"
- "Visualize the relationship between sets A, B, and C"

## Workflow

### Step 1: Gather Diagram Requirements

If the user has NOT provided a title, ask them for one using clear, friendly language:

```
To create your Venn diagram, I need a title. What would you like to call this diagram?

Examples:
- "Programming Languages Comparison"
- "Pet Characteristics"
- "Technology Skill Overlap"
```

**Required information before proceeding:**

1. **Title**: Clear, descriptive name for the diagram
2. **Sets**: 2-4 distinct categories/sets to compare
3. **Relationships**: Understanding of which sets overlap and how
4. **Context**: Educational purpose or subject area
5. **Definitions**: Educational definitions for each set and intersection (for tooltips)

**Check for Existing Definitions (IMPORTANT):**

Before asking the user for definitions, check if `/docs/glossary.md` exists and contains definitions for the set terms:

1. **Read the glossary file** if it exists: `Read /docs/glossary.md`
2. **Extract relevant definitions** for each set/term in the diagram
3. **Use glossary definitions** if available - they are ISO 11179-compliant and ensure consistency
4. **Only ask the user** if definitions are missing or unclear

**Example glossary lookup:**
```
If creating diagram for "AI, Machine Learning, Deep Learning":
- Search glossary.md for "Artificial Intelligence", "Machine Learning", "Deep Learning"
- Extract the definitions
- Use them directly in the definitions object
```

**If the description is incomplete or unclear**, prompt the user for additional information:

```
To create an accurate Venn diagram, I need more information:

1. What sets/categories do you want to compare?
2. What items or characteristics are shared between sets?
3. Are there any items unique to each set?
4. What's the educational purpose of this diagram?
5. (Only if not in glossary) How would you define each set and their overlaps?
```

**Priority for Definitions:**

1. **First**: Check `/docs/glossary.md` for existing definitions
2. **Second**: Use definitions provided by the user
3. **Third**: Create concise, educational definitions based on context

**Note on Definitions:** Using glossary definitions ensures consistency across the textbook and leverages existing ISO 11179-compliant content. Every hover interaction becomes a teaching moment that reinforces concepts from the glossary.

### Step 2: Design the Venn Diagram Data

Consult `references/venn-js-reference.md` for detailed syntax guidance and examples.

**Design decisions:**

1. **Determine set count** (2, 3, or 4 circles):
   - 2 circles: Simple comparisons
   - 3 circles: Complex relationships with multiple overlaps
   - 4+ circles: Maximum complexity (use sparingly)

2. **Define set sizes**: Use proportional values that reflect relationships:
   - For symbolic diagrams: Use consistent sizes (e.g., all 10)
   - For data-driven diagrams: Use actual proportional values
   - Ensure intersections don't exceed smallest containing set

3. **Choose color palette**: Select from educational-friendly schemes:
   - **Primary Colors**: Red (#FF6B6B), Cyan (#4ECDC4), Yellow (#FFE66D)
   - **Cool Tones**: Blue-Purple (#667eea), Purple (#764ba2), Sky Blue (#4facfe)
   - **Pastels**: Powder Blue (#a8dadc), Mint (#f1faee), Coral (#e63946)
   - **Custom**: Match textbook theme colors

4. **Structure the data** in venn.js format:

```javascript
// 2-Circle Example
var sets = [
  {sets: ['Python'], size: 100},
  {sets: ['JavaScript'], size: 100},
  {sets: ['Python', 'JavaScript'], size: 40}
];

// 3-Circle Example
var sets = [
  {sets: ['AI'], size: 100},
  {sets: ['ML'], size: 80},
  {sets: ['Data Science'], size: 90},
  {sets: ['AI', 'ML'], size: 60},
  {sets: ['AI', 'Data Science'], size: 50},
  {sets: ['ML', 'Data Science'], size: 55},
  {sets: ['AI', 'ML', 'Data Science'], size: 40}
];
```

### Step 3: Create the MicroSim Directory Structure

Create the diagram directory following the MicroSim pattern:

```bash
mkdir -p /docs/sims/[diagram-name]
```

**Naming convention:**
- Use kebab-case (lowercase with hyphens)
- Descriptive and concise (2-4 words max)
- Avoid special characters
- Examples: `programming-languages`, `pet-comparison`, `ml-ai-overlap`

### Step 4: Generate Files from Templates

Use the template files in `assets/template/` as a starting point. Replace all placeholders with actual content.

#### 4.1 Create script.js

Copy `assets/template/script.js` and replace placeholders:

- `{{VENN_DATA}}`: Replace with the actual sets array (from Step 2)
- `{{COLOR_SCHEME}}`: Replace with color configuration array
- **`{{DEFINITIONS}}`**: Create educational definitions object (see Educational Tooltips below)

**Example color scheme format:**
```javascript
var colorScheme = [
  {set: 'Python', color: '#667eea'},
  {set: 'JavaScript', color: '#764ba2'},
  {set: 'Java', color: '#4facfe'}
];
```

**Educational Tooltips (CRITICAL):**

Always create a definitions object that maps sets to educational content. Replace meaningless size values with definitions that explain what each region represents.

```javascript
// Example definitions object
var definitions = {
    'Python': 'High-level language known for readability and data science',
    'JavaScript': 'Language that runs in browsers for web interactivity',
    'Java': 'Platform-independent language used in enterprise applications',
    'JavaScript,Python': 'Both are dynamically typed and interpreted languages',
    'Java,Python': 'Both support object-oriented programming with classes',
    'Java,JavaScript': 'Both use C-like syntax and are widely adopted',
    'Java,JavaScript,Python': 'All three support variables, loops, and functions'
};

// Helper function to retrieve definitions
function getDefinition(sets) {
    var key = sets.sort().join(',');
    return definitions[key] || sets.join(" ∩ ");
}

// Use in tooltip (NOT d.size)
.on("mouseover", function(event, d) {
    tooltip.html(getDefinition(d.sets));  // Educational content
})
```

**Definition Guidelines:**

1. **Concise**: Keep under 100 characters (1 sentence ideal)
2. **Meaningful**: Focus on concepts, not numbers or technical details
3. **Educational**: Explain relationships for intersections
4. **Accessible**: Use language appropriate for target audience
5. **Consistent**: Maintain similar tone and structure across all definitions

**Good vs Bad Examples:**

✅ **Good**: "Systems that simulate human intelligence and decision-making"
✅ **Good**: "Overlap: Methods combining statistical analysis with AI"

❌ **Bad**: "Size: 150" (not educational)
❌ **Bad**: "This is the intersection of sets A and B containing 40 elements" (too technical)
❌ **Bad**: "Machine learning algorithms are techniques that..." (too long)

**Why This Matters:**

- Makes diagrams self-documenting for students
- Provides immediate context without reading external docs
- Reinforces learning objectives through interaction
- Transforms every hover into a teaching moment

**Important:** Ensure proper JavaScript syntax - the data will be embedded directly into the script.

#### 4.2 Create main.html

Copy `assets/template/main.html` and replace these placeholders:

- `{{TITLE}}`: Diagram title (e.g., "Programming Languages Comparison")
- `{{SUBTITLE}}`: Brief subtitle (e.g., "Interactive Venn Diagram")
- `{{DESCRIPTION}}`: 2-3 sentence explanation of what the diagram shows

The main.html template already includes:
- D3.js v7.9.0 from CDN
- venn.js v0.2.20 from CDN
- Link to style.css and script.js
- Proper HTML5 structure

#### 4.3 Create style.css

Copy `assets/template/style.css` directly - **no modifications needed** unless custom styling is requested.

The default stylesheet ensures:
- 16px minimum font size for accessibility
- Responsive design for mobile devices
- Interactive tooltip styling
- Clean, professional appearance
- Print-friendly styling

#### 4.4 Create index.md

Copy `assets/template/index.md` and replace placeholders:

- `{{TITLE}}`: Same as main.html title
- `{{META_DESCRIPTION}}`: SEO-friendly description (1 sentence)
- `{{OVERVIEW}}`: 1-paragraph overview of what the diagram illustrates
- `{{DESCRIPTION}}`: Detailed description of the visualization
- `{{SET_RELATIONSHIPS}}`: Bulleted list explaining relationships:
  ```markdown
  - **Set A**: Contains items X, Y, Z (unique to A)
  - **Set B**: Contains items M, N, O (unique to B)
  - **A ∩ B**: Shared items include P, Q
  ```
- `{{KEY_CONCEPTS}}`: Bulleted list of educational concepts illustrated
- `{{EDUCATIONAL_APPLICATIONS}}`: How teachers/students can use this diagram
- `{{DIAGRAM_NAME}}`: Directory name (for iframe embedding example)
- `{{RELATED_CONCEPTS}}`: Links to related textbook sections

#### 4.5 Create metadata.json

Copy `assets/template/metadata.json` and replace placeholders:

- `{{TITLE}}`: Diagram title
- `{{DESCRIPTION}}`: Brief description (2-3 sentences)
- `{{SUBJECT}}`: Educational subject area (e.g., "Mathematics", "Computer Science", "Biology")
- `{{DATE}}`: Current date in ISO format (YYYY-MM-DD)
- `{{COVERAGE}}`: Scope of content (e.g., "Introductory", "Intermediate", "Advanced")
- `{{AUDIENCE}}`: Target audience (e.g., "High School", "Undergraduate", "General")
- `{{SET_COUNT}}`: Number of main circles (2, 3, or 4)
- `{{INTERSECTION_COUNT}}`: Number of intersection areas
- `{{CONCEPTS_LIST}}`: JSON array of set labels with proper quoting:
  ```json
  "Set A", "Set B", "Set C"
  ```
- `{{BLOOM_LEVEL}}`: Highest Bloom's Taxonomy level (e.g., "Understand", "Apply", "Analyze")

**Example metadata.json:**

```json
{
  "title": "Programming Languages Comparison",
  "description": "Interactive Venn diagram showing the overlap and unique features of Python, JavaScript, and Java programming languages",
  "subject": "Computer Science",
  "creator": "Claude AI with Venn Diagram Generator Skill",
  "date": "2025-11-07",
  "type": "Interactive Venn Diagram",
  "format": "text/html",
  "language": "en-US",
  "coverage": "Introductory",
  "rights": "Educational Use",
  "audience": "Undergraduate",
  "diagram_type": "venn",
  "set_count": "3",
  "intersection_count": "7",
  "concepts": [
    "Python",
    "JavaScript",
    "Java",
    "Programming Paradigms",
    "Language Features"
  ],
  "bloom_taxonomy": "Understand",
  "version": "1.0",
  "library": "venn.js 0.2.20",
  "dependencies": ["d3.js 7.9.0"]
}
```

### Step 5: Validate and Test

Perform quality checks:

1. **Data validation**:
   - Verify intersection sizes don't exceed smallest containing set
   - Check that all set names are consistent across files
   - Ensure color array matches number of sets

2. **File structure**: Verify all 5 files are present:
   - ✓ index.md
   - ✓ main.html
   - ✓ style.css
   - ✓ script.js
   - ✓ metadata.json

3. **Placeholder replacement**: Check that no `{{PLACEHOLDERS}}` remain in any file

4. **JavaScript syntax**: Ensure script.js has valid JSON for sets array

5. **Responsive design**: Verify diagram adapts to different screen sizes

**Test the diagram:**

Open main.html directly in a browser to verify:
- Circles render correctly
- Colors display as intended
- Tooltips appear on hover
- Labels are readable
- No JavaScript errors in console

### Step 6: Update MkDocs Navigation (Optional)

If working within a textbook project with mkdocs.yml, suggest adding the diagram to navigation:

```yaml
nav:
  - Visualizations:
    - Programming Languages: sims/programming-languages/index.md
```

Or integrate into relevant chapter:

```yaml
nav:
  - Chapter 2 - Set Theory:
    - Introduction: chapters/02/index.md
    - Venn Diagrams: sims/set-relationships/index.md
```

### Step 7: Inform the User

Provide a clear summary of what was created:

```
✓ Created interactive Venn diagram: [Diagram Title]

Location: /docs/sims/[diagram-name]/

Files generated:
✓ main.html - Standalone interactive diagram with venn.js
✓ index.md - MkDocs integration page with iframe embed
✓ style.css - Responsive styling with tooltips
✓ script.js - Venn diagram data and interactive features
✓ metadata.json - Dublin Core metadata for searchability

Features:
• [X]-circle Venn diagram
• Interactive tooltips showing set intersections
• Customized color scheme
• Responsive design for mobile and desktop
• Educational-friendly 16px fonts

The diagram illustrates: [brief description of what it shows]

To view:
1. Standalone: Open /docs/sims/[diagram-name]/main.html in a browser
2. In textbook: Run `mkdocs serve` and navigate to the diagram page

Next steps:
- Test the diagram by opening main.html
- Add navigation link in mkdocs.yml (if applicable)
- Reference from relevant chapter content
- Consider creating related diagrams for connected concepts
```

## Best Practices

### Educational Tooltips - Primary Best Practice

**ALWAYS use educational definitions in tooltips instead of size values.** This is the most important improvement for educational Venn diagrams.

**The Problem:**
Default venn.js examples display size values like "150 users" which provide no educational value. Students see numbers instead of learning content.

**The Solution:**
Create a definitions object that maps each set and intersection to a clear, concise educational definition:

```javascript
var definitions = {
    'AI': 'Systems that simulate human intelligence, reasoning, and decision-making',
    'ML': 'Algorithms that learn patterns from data without explicit programming',
    'Deep Learning': 'Neural networks with multiple layers that learn complex representations',
    'AI,ML': 'Machine Learning is a subset of AI that focuses on learning from data',
    'ML,Deep Learning': 'Deep Learning is a specialized form of ML using neural networks',
    'AI,ML,Deep Learning': 'Deep Learning represents the intersection of AI and ML approaches'
};

function getDefinition(sets) {
    var key = sets.sort().join(',');
    return definitions[key] || sets.join(" ∩ ");
}
```

**Implementation Pattern:**

1. Create definitions object with all possible set combinations
2. Keep each definition under 100 characters (1 sentence)
3. Focus on meaning and relationships, not technical details
4. Use accessible language for your target audience
5. Use `getDefinition(d.sets)` in tooltip, NOT `d.size`

**Impact:**
Every hover interaction becomes a teaching moment that reinforces learning objectives and provides immediate context.

### Design Principles

1. **Clarity over Complexity**:
   - Prefer 2-3 circles for optimal readability
   - Use 4+ circles only when absolutely necessary
   - Consider multiple simple diagrams instead of one complex diagram

2. **Proportional Sizing**:
   - For data-driven diagrams, use actual proportions
   - For conceptual diagrams, use symbolic consistent sizes
   - Ensure mathematical validity (intersections ≤ smallest set)

3. **Color Selection**:
   - Use high-contrast colors for accessibility
   - Apply colorblind-safe palettes when possible
   - Maintain consistent opacity (0.70-0.85) for overlap visibility
   - Use color consistently across related diagrams

4. **Meaningful Labels**:
   - Keep set names concise (1-3 words)
   - Use Title Case for professional appearance
   - Ensure labels are educational and clear
   - Avoid jargon unless appropriate for audience

5. **Educational Context**:
   - Always explain what the diagram teaches
   - Provide real-world examples in documentation
   - Align with learning objectives
   - Include suggested classroom activities

### Accessibility

1. **Font Size**: Minimum 16px for readability from the back of a classroom
2. **Color Contrast**: WCAG AA compliance (4.5:1 minimum contrast ratio)
3. **Alternative Text**: Provide descriptive text in index.md
4. **Keyboard Navigation**: Diagrams work without mouse (D3.js handles this)
5. **Screen Readers**: Semantic HTML structure in main.html

### Educational Integration

1. **Align with Learning Goals**: Map diagram to specific learning objectives
2. **Bloom's Taxonomy**: Tag with appropriate cognitive level
3. **Prerequisites**: Document what students should know first
4. **Assessment**: Suggest comprehension questions in index.md
5. **Extensions**: Propose how students could modify the diagram

## Common Venn Diagram Patterns

### Pattern 1: Simple Comparison (2 Circles)

**Use case**: Comparing two categories with clear overlap

**Example**: "Fruits vs Vegetables"
```javascript
var sets = [
  {sets: ['Fruits'], size: 100},
  {sets: ['Vegetables'], size: 100},
  {sets: ['Fruits', 'Vegetables'], size: 20}  // e.g., Tomatoes
];
```

### Pattern 2: Triple Intersection (3 Circles)

**Use case**: Showing complex relationships between three domains

**Example**: "Math, Physics, Computer Science"
```javascript
var sets = [
  {sets: ['Math'], size: 100},
  {sets: ['Physics'], size: 100},
  {sets: ['CS'], size: 100},
  {sets: ['Math', 'Physics'], size: 40},      // e.g., Calculus
  {sets: ['Math', 'CS'], size: 35},           // e.g., Algorithms
  {sets: ['Physics', 'CS'], size: 30},        // e.g., Simulations
  {sets: ['Math', 'Physics', 'CS'], size: 15} // e.g., Computational Physics
];
```

### Pattern 3: Subset Representation (Nested)

**Use case**: Showing hierarchical relationships (one set inside another)

**Example**: "Animals > Mammals > Dogs"
```javascript
var sets = [
  {sets: ['Animals'], size: 150},
  {sets: ['Mammals'], size: 50},
  {sets: ['Animals', 'Mammals'], size: 50}  // Mammals ⊆ Animals
];
```

### Pattern 4: Disjoint Sets (No Overlap)

**Use case**: Showing mutually exclusive categories

**Example**: "Odd Numbers vs Even Numbers"
```javascript
var sets = [
  {sets: ['Odd'], size: 100},
  {sets: ['Even'], size: 100}
  // No intersection - sets are disjoint
];
```

## Troubleshooting

### Common Issues

**Issue: Sets data is invalid**
- **Symptom**: Diagram doesn't render or JavaScript errors
- **Solution**: Check that intersection sizes don't exceed individual set sizes
- **Example Fix**:
  ```javascript
  // BAD
  {sets: ['A'], size: 10},
  {sets: ['A','B'], size: 15}  // Can't be larger than A!

  // GOOD
  {sets: ['A'], size: 20},
  {sets: ['A','B'], size: 15}
  ```

**Issue: Colors not showing correctly**
- **Symptom**: All circles are same color
- **Solution**: Verify set names in color scheme exactly match set names in data
- **Example Fix**:
  ```javascript
  // Data uses 'Python' but colors use 'python' (case mismatch)
  var sets = [{sets: ['Python'], size: 10}];
  var colorScheme = [{set: 'python', color: '#667eea'}];  // Wrong!

  // Correct
  var colorScheme = [{set: 'Python', color: '#667eea'}];  // Fixed!
  ```

**Issue: Diagram too small/large**
- **Symptom**: Diagram doesn't fit container or is too small
- **Solution**: Adjust width/height in script.js `venn.VennDiagram()` call
- **Typical values**: Width 600px, Height 450px

**Issue: Labels cut off**
- **Symptom**: Set names or intersection values are truncated
- **Solution**:
  1. Increase diagram padding
  2. Shorten label text
  3. Increase container size
  4. Reduce font size (as last resort)

**Issue: Tooltips not appearing**
- **Symptom**: No tooltip on hover
- **Solution**: Check that tooltip CSS class exists in style.css and JavaScript event handlers are attached

**Issue: Diagram not responsive on mobile**
- **Symptom**: Diagram doesn't resize on small screens
- **Solution**: Verify `makeResponsive()` function is called and SVG has viewBox attribute

## Resources

### Bundled References

- **`references/venn-js-reference.md`**: Comprehensive venn.js guide with examples, data formats, styling options, color palettes, and troubleshooting
- **`ai-ml-dl-examplejs.js`**: Complete working example demonstrating educational tooltips with definitions for AI, ML, and Deep Learning relationships. Shows proper implementation of the definitions pattern.

### Bundled Templates

- **`assets/template/main.html`**: Standalone HTML diagram template with CDN links
- **`assets/template/style.css`**: Responsive stylesheet with tooltip and print styles
- **`assets/template/script.js`**: Interactive venn.js initialization with tooltips
- **`assets/template/index.md`**: MkDocs integration template
- **`assets/template/metadata.json`**: Dublin Core metadata template

### External Resources

- **venn.js GitHub**: https://github.com/benfred/venn.js
- **venn.js Examples**: https://benfred.github.io/venn.js/
- **D3.js Documentation**: https://d3js.org/
- **MkDocs Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **Set Theory Introduction**: https://en.wikipedia.org/wiki/Venn_diagram

## Examples

### Example 1: Two-Circle Comparison

**User Request:** "Create a Venn diagram comparing dogs and cats"

**Generated Data:**
```javascript
var sets = [
  {sets: ['Dogs'], size: 100},
  {sets: ['Cats'], size: 100},
  {sets: ['Dogs', 'Cats'], size: 40}
];

var colorScheme = [
  {set: 'Dogs', color: '#667eea'},
  {set: 'Cats', color: '#764ba2'}
];
```

**Set Relationships:**
- **Dogs Only**: Bark, very loyal, need walks, pack animals
- **Cats Only**: Meow, independent, use litter box, solitary hunters
- **Both**: Four legs, fur, domesticated, popular pets, carnivores

### Example 2: Three-Circle Knowledge Domains

**User Request:** "Show the overlap between AI, Machine Learning, and Data Science"

**Generated Data:**
```javascript
var sets = [
  {sets: ['AI'], size: 120},
  {sets: ['Machine Learning'], size: 100},
  {sets: ['Data Science'], size: 110},
  {sets: ['AI', 'Machine Learning'], size: 70},
  {sets: ['AI', 'Data Science'], size: 60},
  {sets: ['Machine Learning', 'Data Science'], size: 65},
  {sets: ['AI', 'Machine Learning', 'Data Science'], size: 50}
];

var colorScheme = [
  {set: 'AI', color: '#667eea'},
  {set: 'Machine Learning', color: '#764ba2'},
  {set: 'Data Science', color: '#f093fb'}
];

// Educational tooltips
var definitions = {
    'AI': 'Systems that simulate human intelligence and decision-making',
    'Machine Learning': 'Algorithms that learn patterns from data without explicit programming',
    'Data Science': 'Field combining statistics, analysis, and domain expertise to extract insights',
    'AI,Machine Learning': 'ML is a core approach within AI for building intelligent systems',
    'AI,Data Science': 'AI techniques applied to data analysis and predictive modeling',
    'Data Science,Machine Learning': 'ML provides the algorithms that data scientists use for analysis',
    'AI,Data Science,Machine Learning': 'The intersection where intelligent systems learn from data'
};

function getDefinition(sets) {
    var key = sets.sort().join(',');
    return definitions[key] || sets.join(" ∩ ");
}
```

**Set Relationships:**
- **AI Only**: Expert systems, robotics, natural language processing
- **ML Only**: Supervised learning, unsupervised learning, model training
- **Data Science Only**: Data visualization, statistics, data cleaning
- **AI ∩ ML**: Neural networks, deep learning
- **AI ∩ Data Science**: Predictive analytics, decision trees
- **ML ∩ Data Science**: Feature engineering, cross-validation
- **All Three**: Classification algorithms, regression, model evaluation

### Example 3: Programming Language Features

**User Request:** "Compare Python, JavaScript, and Java programming languages"

**Generated Data:**
```javascript
var sets = [
  {sets: ['Python'], size: 100},
  {sets: ['JavaScript'], size: 100},
  {sets: ['Java'], size: 100},
  {sets: ['Python', 'JavaScript'], size: 45},
  {sets: ['Python', 'Java'], size: 40},
  {sets: ['JavaScript', 'Java'], size: 35},
  {sets: ['Python', 'JavaScript', 'Java'], size: 25}
];

var colorScheme = [
  {set: 'Python', color: '#4ECDC4'},
  {set: 'JavaScript', color: '#FFE66D'},
  {set: 'Java', color: '#FF6B6B'}
];
```

**Set Relationships:**
- **Python Only**: Indentation-based syntax, data science libraries, simple syntax
- **JavaScript Only**: Runs in browsers, async/await, DOM manipulation
- **Java Only**: JVM-based, strongly typed, enterprise focus
- **Python ∩ JavaScript**: Dynamic typing, interpreted, first-class functions
- **Python ∩ Java**: Object-oriented, classes, large standard library
- **JavaScript ∩ Java**: C-like syntax, used in web development
- **All Three**: Variables, loops, functions, arrays/lists, popular languages

## Integration with Other Skills

This skill works well with other intelligent textbook skills:

- **glossary-generator**: **PRIMARY INTEGRATION** - Always check `/docs/glossary.md` first for ISO 11179-compliant definitions to use in tooltips. This ensures consistency across the textbook and reinforces glossary terms through interactive hover experiences.
- **learning-graph-generator**: Visualize concept dependencies as Venn diagrams showing prerequisite relationships
- **chapter-content-generator**: Embed diagrams in chapter content with iframe integration
- **quiz-generator**: Create questions about set relationships shown in the diagram
- **microsim-p5**: Use Venn diagrams for static set visualizations, p5.js for dynamic simulations

**Best Practice:** When creating Venn diagrams for an existing textbook project, always check the glossary first. This creates a cohesive learning experience where glossary terms are reinforced through multiple touchpoints (definitions, diagrams, quizzes).

## Version History

**v1.0** - Initial release
- 2-4 circle Venn diagram generation
- Interactive tooltips with hover effects
- Customizable color schemes
- Responsive design for mobile and desktop
- MicroSim package creation with full documentation
- Dublin Core metadata support
- Educational-friendly 16px fonts
