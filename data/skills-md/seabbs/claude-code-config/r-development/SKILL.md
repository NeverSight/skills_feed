---
name: r-development
description: Expert guidance for R package development following best practices for devtools, testthat, roxygen2, and R ecosystem tools
---

# R Package Development

Use this skill when working with R packages to ensure proper development workflows, testing patterns, and documentation standards.

## Development Workflow

### Package Building and Management

```r
# Load package for interactive development
devtools::load_all()

# Update documentation (REQUIRED before committing R changes)
devtools::document()

# Run all tests
devtools::test()

# Run specific test file
testthat::test_file("tests/testthat/test-filename.R")

# Run tests matching a pattern
devtools::test(filter = "pattern")
testthat::test_local(filter = "pattern")

# Check package (R CMD check)
devtools::check()

# Build package
devtools::build()

# Install package locally
devtools::install()

# Check with vignettes built
devtools::check(build_args = c("--compact-vignettes=both"))
```

### Code Quality and Style

```r
# Lint package (configuration in .lintr)
lintr::lint_package()

# Lint specific file
lintr::lint("R/filename.R")

# Style code (pre-commit hook typically uses tidyverse style)
styler::style_pkg()

# Check test coverage
covr::package_coverage()
```

### Documentation Building

```r
# Build vignettes
devtools::build_vignettes()

# Build specific vignette
rmarkdown::render("vignettes/name.Rmd")

# Build pkgdown site locally
pkgdown::build_site()
```

## Testing Best Practices

### testthat Patterns

**Preferred expectations:**

- `expect_identical()` > `expect_equal()` (when exact match expected)
- Multiple `expect_true()` calls > stacking conditions with `&&`
- `expect_s3_class()` > `expect_true(inherits(...))`
- Use specific `expect_*` functions:
  - `expect_lt()`, `expect_gt()`, `expect_lte()`, `expect_gte()`
  - `expect_length()`
  - `expect_named()`
  - `expect_type()`

**Examples:**

```r
# Good
expect_identical(result, expected)
expect_s3_class(obj, "data.frame")
expect_lt(value, 10)
expect_true(condition1)
expect_true(condition2)

# Avoid
expect_equal(result, expected)  # when identical match is needed
expect_true(inherits(obj, "data.frame"))
expect_true(value < 10)
expect_true(condition1 && condition2)
```

### Test Organisation

- Use testthat edition 3
- Test files named `test-{component}.R`
- Helper files in `tests/testthat/helper-{name}.R`
- Setup files in `tests/testthat/setup.R` for shared fixtures
- Custom expectations in `tests/testthat/helper-expectations.R`

### Conditional Testing

```r
# Skip tests on CRAN
testthat::skip_on_cran()

# Skip if not on CI
testthat::skip_if_not(on_ci())

# Skip if package not available
testthat::skip_if_not_installed("package")
```

## Documentation Standards

### roxygen2 Best Practices

**Avoid duplication with `@inheritParams`:**

```r
#' @param x Input data
#' @param ... Additional arguments
my_function <- function(x, ...) {}

#' @inheritParams my_function
#' @param y Another parameter
wrapper_function <- function(x, y, ...) {}
```

**Documentation structure:**

- One sentence per line in descriptions
- Max 80 characters per line
- Use `@family` tags for related functions
- Use `@examples` or `@examplesIf` for examples
- UK English spelling

**Example documentation:**

```r
#' Process input data
#'
#' This function processes the input data according to specified parameters.
#' It returns a processed data frame with additional columns.
#'
#' @param data A data.frame containing the input data
#' @param method Character string specifying the processing method
#'
#' @return A data.frame with processed results
#'
#' @family preprocessing
#'
#' @examples
#' \dontrun{
#' result <- process_data(my_data, method = "standard")
#' }
#'
#' @export
process_data <- function(data, method = "standard") {
  # implementation
}
```

## Code Style Guidelines

### Naming Conventions

- **Internal functions**: Prefix with `.`

  ```r
  .internal_helper <- function() {}
  ```

- **Exported functions**: Use snake_case

  ```r
  public_function <- function() {}
  ```

### Formatting

- Max 80 characters per line
- No trailing whitespace
- No spurious blank lines
- Use tidyverse style guide
- Set up pre-commit hooks for automatic formatting

### Pre-commit Hooks

Typical `.pre-commit-config.yaml` includes:

- `style-files`: Auto-format R code
- `lintr`: Lint R code
- `readme-rmd-rendered`: Ensure README.md is up-to-date
- `parsable-R`: Check R syntax
- `deps-in-desc`: Check dependencies are in DESCRIPTION

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Common Data Structures

### data.table Usage

Many R packages use `data.table` for performance:

- Functions often expect/return `data.table` objects
- Use `data.table::setDT()` or custom `coerce_dt()` to ensure input is data.table
- Set keys for efficient joins: `data.table::setkey(dt, col)`
- Use `:=` for in-place modification

### S3 Classes

- Check class with `inherits()` or `expect_s3_class()`
- Document S3 methods properly
- Export constructors, not internal class definitions

## Package Dependencies

### Managing Dependencies

```r
# Use specific package functions with ::
package::function()

# Add to DESCRIPTION Imports or Suggests
usethis::use_package("package_name")
usethis::use_package("package_name", type = "Suggests")
```

### Common R Package Ecosystem Tools

- **devtools**: Development workflow
- **testthat**: Testing framework
- **roxygen2**: Documentation generation
- **usethis**: Package setup automation
- **lintr**: Code linting
- **styler**: Code formatting
- **covr**: Test coverage
- **pkgdown**: Website generation

## When to Use This Skill

Activate this skill when:

- Developing R packages
- Writing R tests
- Documenting R functions
- Setting up R package infrastructure
- Running R package checks
- Working with devtools, testthat, or roxygen2

This skill provides R-specific development patterns.
Project-specific architecture and domain knowledge should remain in project CLAUDE.md files.
