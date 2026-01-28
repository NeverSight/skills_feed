---
name: component-usage-analysis
description: Analyse component dependencies and usage patterns in a Drupal/Twig component library. Use when user asks to find where a component is used, check if a component can be safely removed, audit component dependencies, find components using specific properties, or analyse impact of refactoring a component.
---

# Component Usage Analysis

Analyse component dependencies and usage patterns to support safe refactoring and removal.

## Trigger Phrases

- "Find all usages of `<component>`"
- "Which components use `<component>`?"
- "Check if `<component>` can be safely removed"
- "Find components using `<component>` with property X"
- "Audit dependencies for `<component>`"
- "What would break if I change `<component>`?"

## Configuration

This skill assumes the component library structure:

```
apps/component-library/
├── src/components/
│   ├── elements/
│   ├── patterns/
│   ├── template-components/
│   └── templates/
```

## Analysis Methodology

### Step 1: Identify the Target

Clarify with the user:

1. **Target component**: Which component to analyse (e.g., `elements/image`)
2. **Properties of interest**: Specific properties to filter by (optional)
3. **Analysis goal**: Usage audit, removal check, or refactoring impact

### Step 2: Twig Include Analysis

Find all components that include the target via Twig.

**Search pattern:**

```bash
grep -rn "{% include \"@<tier>/<component>" src/components/
```

**Example for `elements/image`:**

```bash
grep -rn '{% include "@elements/image' src/components/
```

For each match:

1. Note the file path (consuming component)
2. Extract the `with {}` block to identify which properties are passed
3. Record whether target properties are present

**Extracting the `with` block:**

Twig includes may span multiple lines:

```twig
{% include "@elements/image/image.twig" with {
    src: item.image.src,
    alt: item.image.alt,
    description: item.image.description
} %}
```

Use multi-line search or examine files directly when the `with` block is complex.

See [references/search-patterns.md](references/search-patterns.md) for detailed patterns.

### Step 3: Mock Reference Analysis

Find all components whose mocks reference the target component.

**Search pattern:**

```bash
grep -rn '\$ref: <tier>/<component>#' src/components/
```

**Example for `elements/image`:**

```bash
grep -rn '\$ref: elements/image#' src/components/
```

For each match:

1. Note the file path and variant name referenced
2. Look up the referenced variant in the target's `mocks.yaml`
3. Check if the variant includes the properties of interest

**Cross-referencing variants:**

If a mock uses `$ref: elements/image#with-caption`, check `elements/image/mocks.yaml` to see what properties that variant defines.

### Step 4: Categorise Results

Group findings into categories based on the analysis goal:

**For property-specific analysis:**

- **Uses WITH property X**: Components that pass/use the property
- **Uses WITHOUT property X**: Components that use the target but don't use property X

**For removal analysis:**

- **Direct Twig includes**: Would break immediately
- **Mock references only**: May need mock updates but won't break rendering
- **No dependencies**: Safe to remove

**For refactoring analysis:**

- **Affected by change**: Components using the property/feature being changed
- **Unaffected**: Components using the target but not the changed aspect

### Step 5: Verification

Ensure comprehensive coverage before reporting:

1. **Count total files:**

   ```bash
   find src/components -name "*.twig" | wc -l
   find src/components -name "mocks.yaml" | wc -l
   ```

2. **Verify search found expected files:**
   - Spot-check known usages
   - Confirm count matches expectations

3. **Check for alternative patterns:**
   - Embedded includes: `{% include "@elements/image/image.twig" %}`
   - Variable includes: `{% include image_template %}`
   - Embed blocks: `{% embed "@elements/image/image.twig" %}`

4. **Report confidence level:**
   - High: All patterns checked, counts verified
   - Medium: Primary patterns checked
   - Low: Quick scan only

## Output Format

Provide results in a clear structure:

```
## Component Usage Analysis: <component>

### Summary
- Total usages found: X
- Twig includes: Y
- Mock references: Z

### Uses WITH <property>
1. `patterns/card/card.twig` - passes description in with block
2. `patterns/teaser/mocks.yaml` - references variant with description

### Uses WITHOUT <property>
1. `patterns/hero/hero.twig` - only passes src, alt
2. `template-components/header/mocks.yaml` - references minimal variant

### Verification
- Searched X .twig files
- Searched Y mocks.yaml files
- Confidence: High
```

## Common Scenarios

### Scenario: Removing a Property

User: "Can I remove the `copyright` property from `elements/image`?"

1. Search for Twig includes passing `copyright`
2. Search for mock references to variants with `copyright`
3. Report which components would need updates
4. Recommend: Update consumers first, then remove property

### Scenario: Safe Component Removal

User: "Is `elements/legacy-button` used anywhere?"

1. Search for Twig includes of the component
2. Search for mock references
3. Search for library references in templates
4. If zero results across all searches → safe to remove

### Scenario: Refactoring Impact

User: "I want to rename `description` to `caption` in `elements/image`"

1. Find all usages passing `description`
2. Provide list of files requiring updates
3. Estimate scope of change

## Notes

- Always verify comprehensively before recommending removal
- Check both Twig files AND mocks.yaml files
- Consider indirect dependencies (component A uses B which uses C)
- Report confidence level with results
