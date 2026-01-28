---
name: mapbox-style-quality
description: Expert guidance on validating, optimizing, and ensuring quality of Mapbox styles through validation, accessibility checks, and optimization. Use when preparing styles for production, debugging issues, or ensuring map quality standards.
---

# Mapbox Style Quality Skill

This skill provides expert guidance on ensuring Mapbox style quality through validation, accessibility, and optimization tools.

## When to Use Quality Tools

### Pre-Production Checklist

Before deploying any Mapbox style to production:

1. **Validate all expressions** - Catch syntax errors before runtime
2. **Check color contrast** - Ensure text is readable (WCAG compliance)
3. **Validate GeoJSON sources** - Ensure data integrity
4. **Optimize style** - Reduce file size and improve performance
5. **Compare versions** - Understand what changed

### During Development

**When adding GeoJSON data:**

- Always validate external GeoJSON with `validate_geojson_tool` before using as a source

**When writing expressions:**

- Validate expressions with `validate_expression_tool` as you write them
- Catch type mismatches early (e.g., using string operator on number)
- Verify operator availability in your Mapbox GL JS version
- Test expressions with expected data types

**When styling text/labels:**

- Check foreground/background contrast with `check_color_contrast_tool`
- Aim for WCAG AA minimum (4.5:1 for normal text, 3:1 for large text)
- Use AAA standard (7:1 for normal text) for better accessibility
- Consider different background scenarios (map tiles, overlays)

### Before Committing Changes

**Compare style versions:**

- Use `compare_styles_tool` to generate a diff report
- Review all layer changes, source modifications, and expression updates
- Understand the impact of your changes
- Document significant changes in commit messages

### Before Deployment

**Optimize the style:**

- Run `optimize_style_tool` to reduce file size
- Remove unused sources that reference deleted layers
- Eliminate duplicate layers with identical properties
- Simplify boolean expressions for better performance
- Remove empty layers that serve no purpose

## Validation Best Practices

### GeoJSON Validation

**Always validate when:**

- Loading GeoJSON from user uploads
- Fetching GeoJSON from external APIs
- Processing GeoJSON from third-party sources
- Converting between data formats

**Common GeoJSON errors:**

- Invalid coordinate ranges (longitude > 180 or < -180)
- Unclosed polygon rings (first and last coordinates must match)
- Wrong coordinate order (should be [longitude, latitude], not [latitude, longitude])
- Missing required properties (type, coordinates, geometry)
- Invalid geometry types or nesting

**Example workflow:**

```
1. Receive GeoJSON data
2. Validate with validate_geojson_tool
3. If valid: Add as source to style
4. If invalid: Fix errors, re-validate
```

### Expression Validation

**Validate expressions for:**

- Filter conditions (`filter` property on layers)
- Data-driven styling (`paint` and `layout` properties)
- Feature state expressions
- Dynamic property calculations

**Common expression errors:**

- Type mismatches (string operators on numbers)
- Invalid operator names or wrong syntax
- Wrong number of arguments for operators
- Nested expression errors
- Using unavailable operators for your GL JS version

**Prevention strategies:**

- Validate as you write expressions, not at runtime
- Test expressions with representative data
- Use type checking (expectedType parameter)
- Validate in context (layer, filter, paint, layout)

### Accessibility Validation

**WCAG Levels:**

- **AA** (minimum): 4.5:1 for normal text, 3:1 for large text
- **AAA** (enhanced): 7:1 for normal text, 4.5:1 for large text

**Text size categories:**

- **Normal**: < 18pt or < 14pt bold
- **Large**: ≥ 18pt or ≥ 14pt bold

**Common scenarios to check:**

- Text labels on map tiles
- POI labels with background colors
- Custom markers with text
- UI overlays on maps
- Legend text and symbols
- Attribution text

**Testing strategy:**

- Test against both light and dark map tiles
- Consider overlay backgrounds (popups, modals)
- Test in different lighting conditions (mobile outdoor use)
- Verify contrast at different zoom levels

## Optimization Best Practices

### When to Optimize

**Before production deployment:**

- After all development changes are complete
- After merging multiple feature branches
- When style has grown significantly over time
- Before major releases or launches

**Benefits of optimization:**

- Faster initial load times
- Reduced bandwidth usage
- Better runtime performance
- Cleaner, more maintainable code

### Optimization Types

**Remove unused sources:**

- Automatically identifies sources not referenced by any layer
- Safe to remove without affecting functionality
- Common after deleting layers or refactoring

**Remove duplicate layers:**

- Finds layers with identical properties (excluding ID)
- Can occur when copying/pasting layers
- Reduces style complexity and file size

**Simplify expressions:**

- Converts `["all", true]` → `true`
- Converts `["any", false]` → `false`
- Converts `["!", false]` → `true`
- Converts `["!", true]` → `false`
- Improves expression evaluation performance

**Remove empty layers:**

- Removes layers with no paint or layout properties
- Preserves background layers (valid even when empty)
- Cleans up incomplete or placeholder layers

**Consolidate filters:**

- Identifies groups of layers with identical filter expressions
- Highlights opportunities for layer consolidation
- Doesn't automatically consolidate (informational only)

### Optimization Strategy

**Recommended order:**

1. Remove unused sources first (reduces noise for other checks)
2. Remove duplicate layers (eliminates redundancy)
3. Simplify expressions (improves readability and performance)
4. Remove empty layers (final cleanup)
5. Review consolidation opportunities (manual step)

**Selective optimization:**

```
// All optimizations (recommended for production)
optimize_style_tool({ style })

// Specific optimizations only
optimize_style_tool({
  style,
  optimizations: ['remove-unused-sources', 'simplify-expressions']
})
```

**Review before deploying:**

- Check the optimization report
- Verify size savings (percentReduction)
- Review the list of changes (optimizations array)
- Test the optimized style before deployment

## Style Comparison Workflow

### When to Compare Styles

**Before merging changes:**

- Review what changed in your feature branch
- Ensure no unintended modifications
- Generate change summary for PR description

**When investigating issues:**

- Compare working version vs. broken version
- Identify what changed between versions
- Narrow down root cause of problems

**During migrations:**

- Compare old format vs. new format
- Verify data integrity after conversion
- Document transformation differences

### Comparison Best Practices

**Use ignoreMetadata flag:**

```
// Ignore metadata differences (id, owner, created, modified)
compare_styles_tool({
  styleA: oldStyle,
  styleB: newStyle,
  ignoreMetadata: true
})
```

**Focus on meaningful changes:**

- Layer additions/removals
- Source changes
- Expression modifications
- Paint/layout property updates

**Document significant changes:**

- Note breaking changes in documentation
- Update style version numbers
- Communicate changes to team/users

## Quality Workflow Examples

### Basic Quality Check

```
1. Validate expressions in style
2. Check color contrast for text layers
3. Optimize if needed
```

### Full Pre-Production Workflow

```
1. Validate all GeoJSON sources
2. Validate all expressions (filters, paint, layout)
3. Check color contrast for all text layers
4. Compare with previous production version
5. Optimize style
6. Test optimized style
7. Deploy
```

### Troubleshooting Workflow

```
1. Compare working vs. broken style
2. Identify differences
3. Validate suspicious expressions
4. Check GeoJSON data if source-related
5. Verify color contrast if visibility issue
```

### Refactoring Workflow

```
1. Create backup of current style
2. Make refactoring changes
3. Compare before vs. after
4. Validate all modified expressions
5. Optimize to clean up
6. Review size impact
```

## Common Issues and Solutions

### Runtime Expression Errors

**Problem:** Map throws expression errors at runtime
**Solution:** Validate expressions with `validate_expression_tool` during development
**Prevention:** Add expression validation to pre-commit hooks or CI/CD

### Poor Text Readability

**Problem:** Text labels are hard to read on map
**Solution:** Check contrast with `check_color_contrast_tool`, adjust colors to meet WCAG AA
**Prevention:** Test text on both light and dark backgrounds, check at different zoom levels

### Large Style File Size

**Problem:** Style takes long to load or transfer
**Solution:** Run `optimize_style_tool` to remove redundancies and simplify
**Prevention:** Regularly optimize during development, remove unused sources immediately

### Invalid GeoJSON Source

**Problem:** GeoJSON source fails to load or render
**Solution:** Validate with `validate_geojson_tool`, fix coordinate issues, verify structure
**Prevention:** Validate all external GeoJSON before adding to style

### Unexpected Style Changes

**Problem:** Style changed but unsure what modified
**Solution:** Use `compare_styles_tool` to generate diff report
**Prevention:** Compare before/after for all significant changes, document modifications

## Integration with Development Workflow

### Git Pre-Commit Hook

```bash
# Validate expressions before commit
npm run validate-style

# Optimize before commit (optional)
npm run optimize-style
```

### CI/CD Pipeline

```
1. Validate all expressions
2. Check accessibility compliance
3. Run optimization (warning if significant savings)
4. Compare with production version
5. Generate quality report
```

### Code Review Checklist

- [ ] All expressions validated
- [ ] Text contrast meets WCAG AA
- [ ] GeoJSON sources validated
- [ ] Style optimized for production
- [ ] Changes documented in comparison report

## Best Practices Summary

**During Development:**

- Validate expressions as you write them
- Check GeoJSON data when adding sources
- Test color contrast for new text layers

**Before Committing:**

- Compare with previous version
- Document significant changes
- Validate modified expressions

**Before Production:**

- Run full validation suite
- Check accessibility compliance
- Optimize style
- Test optimized version
- Generate quality report

**Regular Maintenance:**

- Periodically optimize to prevent bloat
- Review and consolidate similar layers
- Update expressions to use simpler forms
- Remove deprecated or unused code

## Tool Quick Reference

| Tool                        | Use When               | Output                     |
| --------------------------- | ---------------------- | -------------------------- |
| `validate_geojson_tool`     | Adding GeoJSON sources | Valid/invalid + error list |
| `validate_expression_tool`  | Writing expressions    | Valid/invalid + error list |
| `check_color_contrast_tool` | Styling text labels    | Passes/fails + WCAG levels |
| `compare_styles_tool`       | Reviewing changes      | Diff report with paths     |
| `optimize_style_tool`       | Before deployment      | Optimized style + savings  |

## Additional Resources

- [Mapbox Style Specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [GeoJSON Specification (RFC 7946)](https://tools.ietf.org/html/rfc7946)
- [Mapbox Expression Reference](https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/)
