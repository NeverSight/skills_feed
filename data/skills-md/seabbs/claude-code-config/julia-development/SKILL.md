---
name: julia-development
description: Expert guidance for Julia package development following SciML standards, Distributions.jl patterns, and Julia ecosystem best practices
---

# Julia Package Development

Use this skill when working with Julia packages to ensure proper development workflows, testing patterns, documentation standards, and performance best practices.

## Development Workflow

### Environment Management

```bash
# Start Julia with project environment
julia --project=.

# Activate project in REPL
using Pkg
Pkg.activate(".")

# Install dependencies
Pkg.instantiate()

# Update dependencies (PREFERRED over direct Project.toml editing)
Pkg.update()

# Add new dependency
Pkg.add("PackageName")

# Add development dependency
Pkg.add("PackageName"; io=devnull)  # Then manually move to extras/test deps

# Check package status
Pkg.status()
```

**IMPORTANT**: Always use `Pkg.update()` to update packages.
Never edit `Project.toml` directly for version updates.

### Testing

```bash
# Run all tests (from project root)
julia --project=. -e 'using Pkg; Pkg.test()'

# Run tests with test environment
julia --project=test test/runtests.jl

# Run tests skipping quality checks (if supported)
julia --project=test test/runtests.jl skip_quality
```

**Test Organization:**
- Use `TestItemRunner` with `@testitem` syntax for modular testing
- Organize tests by component: `test/component/`, `test/package/`
- Package-level tests in `test/package/` for quality (Aqua, DocTest, formatting)
- Use `@testitem "description" begin ... end` for individual test items

**Example test structure:**

```julia
using TestItemRunner

@testitem "Basic functionality" begin
    using MyPackage
    @test my_function(1) == 2
end

@testitem "Edge cases" begin
    using MyPackage
    @test_throws ArgumentError my_function(-1)
end
```

### Documentation

```bash
# Build documentation locally
julia --project=docs docs/make.jl

# Build docs skipping notebooks (faster)
julia --project=docs docs/make.jl --skip-notebooks
# or via environment variable
SKIP_NOTEBOOKS=true julia --project=docs docs/make.jl

# Start Pluto server for interactive notebooks
# (check project-specific task or command)
```

**Documentation Structure:**
- Use Documenter.jl for documentation
- Auto-deployment to GitHub Pages via CI
- Structure defined in `docs/pages.jl` or `docs/make.jl`

### Code Quality

```bash
# Run pre-commit hooks
pre-commit run --all-files

# JuliaFormatter (typically configured in .JuliaFormatter.toml)
# Usually handled by pre-commit hooks
```

**Quality Checks:**
- Aqua.jl tests for package quality
- JuliaFormatter.jl for code formatting
- Pre-commit hooks for automated checks

## Code Style Guidelines

### SciML Coding Standards

Follow SciML (Scientific Machine Learning) coding standards:
- Avoid type instability
- Ensure efficient precompilation
- Use appropriate type annotations for performance
- Write type-stable code

**Type Stability:**

```julia
# Good - type stable
function compute(x::Float64)
    result = 0.0  # Type is known
    for i in 1:10
        result += x * i
    end
    return result
end

# Avoid - type unstable
function compute_bad(x)
    result = 0  # Type might change
    for i in 1:10
        result = result + x * i  # Type may vary
    end
    return result
end
```

### Formatting Rules

- Max 80 characters per line
- No trailing whitespace
- No spurious blank lines
- Use JuliaFormatter.jl for consistent formatting

## Documentation Standards

### Docstring Syntax

Use `@doc` with either raw strings or regular strings:

```julia
# For simple docstrings without LaTeX or templates
@doc "
Brief description of the function.

# Arguments
- `x`: Description of x
- `y`: Description of y

# Returns
- Description of return value

# Examples
```jldoctest
julia> my_function(1, 2)
3
```
"
function my_function(x, y)
    return x + y
end

# For docstrings with LaTeX math
@doc raw"
Computes the mathematical function:

``f(x) = \int_0^x t^2 dt``

Use raw strings when including LaTeX to preserve backslashes.
"
function math_function(x)
    # implementation
end
```

### DocStringExtensions Templates

**IMPORTANT**: Template expansion rules:
- Use `@doc "` (regular string) for templates (allows expansion)
- Use `@doc """` with escaped backslashes when combining templates with LaTeX
- **NEVER** use `@doc raw"` with templates (prevents expansion)

```julia
using DocStringExtensions

# Good - template will expand
@doc "
$(TYPEDSIGNATURES)

Brief description.

# Fields
$(TYPEDFIELDS)
"
struct MyType
    "Field description"
    field::Int
end

# Good - template + LaTeX with escaped backslashes
@doc """
\$(TYPEDSIGNATURES)

Computes: ``f(x) = \\int_0^x t^2 dt``

Note the escaped backslashes in LaTeX: \\int, not \int
"""
function combined_function(x)
    # implementation
end

# Avoid - raw string prevents template expansion
@doc raw"
$(TYPEDSIGNATURES)  # This will NOT expand!
"
```

### Documentation Structure Best Practices

- Keep interface method docstrings concise (1-2 lines)
- Use "See also" sections for cross-references
- Avoid duplication between related functions (pdf/logpdf, cdf/logcdf)
- Include mathematical formulations in main type/constructor docstrings
- Provide minimal but sufficient examples using `@example` blocks

**Cross-referencing:**

```julia
@doc "
Compute the cumulative distribution function.

See also: [`logcdf`](@ref)
"
function cdf(d::MyDist, x::Real)
    # implementation
end

@doc "
Compute the log cumulative distribution function.

See also: [`cdf`](@ref)
"
function logcdf(d::MyDist, x::Real)
    # implementation
end
```

## Package Structure

Typical Julia package structure:
```
MyPackage.jl/
├── src/
│   ├── MyPackage.jl        # Main module file with exports
│   ├── component1.jl       # Component implementations
│   ├── component2.jl
│   ├── docstrings.jl       # DocStringExtensions templates
│   └── utils/
├── test/
│   ├── runtests.jl         # Main test file
│   ├── component1/         # Tests by component
│   ├── component2/
│   └── package/            # Quality tests (Aqua, formatting)
├── docs/
│   ├── make.jl             # Documentation build script
│   ├── src/                # Documentation source
│   └── pages.jl            # Page structure (optional)
├── Project.toml            # Package dependencies
└── README.md
```

## Performance Best Practices

### Type Stability

```julia
# Check type stability with @code_warntype
@code_warntype my_function(args...)

# Look for red (Any) types - indicates type instability
```

### Precompilation

```julia
# Ensure efficient precompilation
# Use PrecompileTools.jl for complex packages
using PrecompileTools

@compile_workload begin
    # Representative workload for precompilation
    my_function(example_args...)
end
```

### Performance Patterns

- Use in-place operations when possible (`!` suffix convention)
- Preallocate arrays for loops
- Use `@simd`, `@inbounds` when safe
- Consider `StaticArrays.jl` for small fixed-size arrays
- Profile with `@time`, `@benchmark` (BenchmarkTools.jl)

## Common Dependencies and Patterns

### Distributions.jl Interface

When implementing distributions:
- Implement required methods: `pdf`, `logpdf`, `cdf`, `logcdf`, `quantile`, `rand`
- Implement support methods: `minimum`, `maximum`, `insupport`
- Optionally implement: `mean`, `var`, `std` (if analytically tractable)
- Vectorization handled automatically via broadcasting
- Consider specialized batch methods: `pdf!`, `logpdf!`, `cdf!`

### Turing.jl and AD Compatibility

Ensure compatibility with automatic differentiation:
- ForwardDiff.jl
- ReverseDiff.jl
- Zygote.jl
- Enzyme.jl

Avoid non-differentiable operations in AD-sensitive code.

## Common Julia Ecosystem Tools

- **Pkg**: Package management
- **TestItemRunner**: Modern testing framework
- **Documenter.jl**: Documentation generation
- **DocStringExtensions**: Documentation templates
- **JuliaFormatter.jl**: Code formatting
- **Aqua.jl**: Package quality testing
- **BenchmarkTools.jl**: Performance benchmarking
- **PrecompileTools.jl**: Precompilation optimization

## When to Use This Skill

Activate this skill when:
- Developing Julia packages
- Writing Julia tests
- Documenting Julia functions
- Setting up Julia package infrastructure
- Working with Distributions.jl, Turing.jl, or SciML packages
- Optimising Julia code performance

This skill provides Julia-specific development patterns.
Project-specific architecture and domain knowledge should remain in project CLAUDE.md files.
