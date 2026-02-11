---
name: cpp-api-documentation
description: Adds Doxygen-compatible documentation comments to C++ header files. Use this skill exclusively for adding or improving API documentation in existing header files (*.hpp, *.h). Do NOT create new resource files such as Doxyfile, scripts, or README files.
metadata:
  version: "1.3.0"
  activation:
    implicit: true
    priority: 2
    triggers:
      - "doxygen"
      - "API docs"
      - "API documentation"
      - "document the API"
      - "add doc comments"
    match:
      # Prefer C/C++ related prompts and repository areas.
      languages: ["cpp", "c", "c++"]
      paths: ["src/**/*.hpp", "src/**/*.h", "include/**/*.hpp", "include/**/*.h"]
      prompt_regex: "(?i)(api doc|doxygen|document the API|API docs|doc comments)"
  usage:
    load_on_prompt: true
    autodispatch: true
---

# API Documentation

Instructions for AI coding agents on adding Doxygen-compatible documentation comments to C++ header files.

> [!NOTE]
> This skill is for documenting header files only. Do NOT create new resource files (e.g., Doxyfile, scripts, README).

- [1. Benefits](#1-benefits)
- [2. Principles](#2-principles)
- [3. Patterns](#3-patterns)
  - [3.1. File Documentation](#31-file-documentation)
  - [3.2. Namespace Documentation](#32-namespace-documentation)
  - [3.3. Class Documentation](#33-class-documentation)
  - [3.4. Function/Method Documentation](#34-functionmethod-documentation)
  - [3.5. Cross-References](#35-cross-references)
  - [3.6. Member Documentation](#36-member-documentation)
  - [3.7. Enumerations](#37-enumerations)
  - [3.8. Grouping and Modules](#38-grouping-and-modules)
  - [3.9. Inheritance](#39-inheritance)
  - [3.10. Formula Documentation](#310-formula-documentation)
- [4. Workflow](#4-workflow)
- [5. Style Guide](#5-style-guide)
- [6. Template](#6-template)
  - [6.1. File Header Template](#61-file-header-template)
  - [6.2. Namespace Template](#62-namespace-template)
  - [6.3. Class Template](#63-class-template)
  - [6.4. Function Template](#64-function-template)
  - [6.5. Member Variable Template](#65-member-variable-template)
  - [6.6. Enumeration Template](#66-enumeration-template)
  - [6.7. Module/Group Template](#67-modulegroup-template)
  - [6.8. Formula Template](#68-formula-template)
- [7. References](#7-references)

## 1. Benefits

- Discoverability
  > Well-documented APIs enable developers to quickly understand and use components without reading implementation details.

- Maintainability
  > Documentation embedded in source code stays synchronized with implementation, reducing drift between code and documentation.

- Traceability
  > Documentation comments serve as living specifications, keeping API contracts synchronized with implementation.

## 2. Principles

Effective API documentation follows these core principles.

- Complete
  > Document all public APIs including classes, functions, parameters, return values, and exceptions. Private implementation details may be omitted.

- Contextual
  > Documentation provides context about usage patterns, performance characteristics, and thread safety guarantees.

- Consistent
  > Use a uniform style, format, terminology and structure throughout the API documentation using the patterns defined in this skill.

- Concise
  > Use clear, brief descriptions. Avoid redundant information that restates what is obvious from the signature.

- Concrete
  > Provide specific details about behavior, edge cases, and error conditions rather than vague statements.

- Convenient
  > Documentation should be easy to access and navigate, integrated with development tools and workflows.

- Accurate
  > Documentation must match the actual behavior. Update documentation whenever the implementation changes.

- Actionable
  > Include usage examples, preconditions, postconditions, and error handling to help developers use the API correctly.

## 3. Patterns

### 3.1. File Documentation

File-level documentation provides context for the entire header file.

- Purpose
  > Describes the file's role in the project architecture.

- Author
  > Identifies the original author(s) of the file.

- License
  > Specifies the licensing terms (typically SPDX identifier).

### 3.2. Namespace Documentation

Namespace-level documentation describes the purpose of the namespace.

- Brief
  > A one-line summary of what the namespace contains.

- Details
  > Extended description of the namespace's role and contents.

### 3.3. Class Documentation

Class-level documentation describes the abstraction.

- Brief
  > A one-line summary of what the class represents.

- Details
  > Extended description of responsibilities, invariants, and usage patterns.

- Template Parameters
  > For template classes, document each template parameter's purpose and constraints.

### 3.4. Function/Method Documentation

Function-level documentation describes the contract.

- Brief
  > A one-line summary of what the function does.

- Parameters
  > Document each parameter with `@param` including direction (`[in]`, `[out]`, `[in,out]`).

- Return Value
  > Document the return value with `@return` or `@retval` for specific values.

- Exceptions
  > Document thrown exceptions with `@throws` or `@exception`.

- Warnings
  > Use `@warning` for critical warnings about misuse.

- Notes
  > Use `@note` for important information.

- Preconditions
  > Document preconditions with `@pre`.

- Postconditions
  > Document postconditions with `@post`.

- Code Examples
  > Use `@code` and `@endcode` blocks for usage examples.

### 3.5. Cross-References

Cross-references link related documentation.

- See Also
  > Use `@see` to reference related functions, classes, or external resources.

### 3.6. Member Documentation

Member-level documentation clarifies data semantics.

- Inline Comments
  > Use `///< description` for trailing inline documentation.

- Block Comments
  > Use `/// description` for preceding documentation.

### 3.7. Enumerations

Enumerations document possible values and their meanings.

- Values
  > Document each enumerator with a brief Inline Comments description.

### 3.8. Grouping and Modules

Organize related elements into logical groups.

- Defgroups
  > Use `@defgroup` to create named documentation modules.

- Ingroups
  > Use `@ingroup` to add elements to existing groups.

- Memberof
  > Use `@memberof` for explicit class membership.

### 3.9. Inheritance

Class hierarchies and inherited documentation.

- Base Classes
  > Document inherited classes with `@copydoc` or `@copybrief` to reuse base class documentation.

### 3.10. Formula Documentation

Mathematical formulas using **LaTeX** syntax for algorithms and technical documentation.

- Inline Formulas
  > Use `\f$..\f$` for formulas that appear within running text (opens LaTeX math mode).

- Inline Text-Mode Formulas
  > Use `\f(...\f)` for LaTeX elements that don't require explicit math mode (e.g., logos like `\LaTeX`).

- Displayed Formulas
  > Use `\f[...\f]` for centered, unnumbered equations on separate lines.

- Environment Formulas
  > Use `\f{environment}{...\f}` for specific LaTeX environments (e.g., `eqnarray*`, `align`).

- MathJax Alternative
  > Enable `USE_MATHJAX` in Doxyfile for client-side formula rendering without requiring LaTeX installation.

- Custom Macros
  > Use `FORMULA_MACROFILE` configuration to define reusable LaTeX commands with `\newcommand`.

## 4. Workflow

> [!IMPORTANT]
> Do NOT create Doxyfile, scripts, or other resource files. Only modify header files.

1. Identify

    Identify undocumented or poorly documented public APIs in header files (e.g., `src/<module>/<header>.hpp`).

2. Add Documentation Comments

    Add Doxygen-compatible documentation comments directly to header files following the templates below.

3. Documentation Coverage Requirements

    Include comprehensive documentation for:

    - All public classes, structs, and enums
    - All public and protected member functions
    - All function parameters and return values
    - All template parameters
    - Exception specifications
    - Thread safety guarantees when applicable
    - Complexity guarantees for algorithms

4. Apply Templates

    Structure all documentation using the template patterns below.

5. Review

    Review documentation for accuracy and readability.

## 5. Style Guide

Doxygen supports multiple comment styles. Use the Javadoc style for consistency.

- Language
  > Write documentation in clear, concise English. Use present tense for descriptions ("Returns the sum" not "Will return the sum").

- Line Length
  > Keep documentation lines under 100 characters for readability.

- Block Comments
  > Use `/** ... */` for multi-line documentation blocks. Each line within the block should start with ` * `.

- Comment Style
  > Prefer `///` for single-line documentation and `/** */` for multi-line documentation blocks. Use Javadoc-style commands (`@param`, `@return`) rather than Qt-style (`\param`, `\return`).

- Brief Descriptions
  > Use `@brief` for explicit brief descriptions.

- Detailed Descriptions
  > Add detailed descriptions after the brief, separated by a blank line or using `@details`.

- Parameter Direction
  > Always specify parameter direction using `[in]`, `[out]`, or `[in,out]` for clarity.

- Code Examples
  > Use `@code` and `@endcode` blocks for usage examples within documentation.

- Cross-References
  > Use `@see` to reference related functions, classes, or external resources.

- Warnings and Notes
  > Use `@note` for important information and `@warning` for critical warnings.

- Deprecation
  > Mark deprecated APIs with `@deprecated` including migration guidance.

- TODO Items
  > Use `@todo` for planned improvements visible in generated documentation.

- Order of Tags
  > Follow this order for function documentation:
  > 1. `@brief`
  > 2. `@details` (if needed)
  > 3. `@tparam` (for templates)
  > 4. `@param`
  > 5. `@return`
  > 6. `@throws`
  > 7. `@pre`
  > 8. `@post`
  > 9. `@note`
  > 10. `@warning`
  > 11. `@see`
  > 12. `@deprecated`

## 6. Template

Use these templates for new documentation. Replace placeholders with actual values.

### 6.1. File Header Template

> [!NOTE]
> Place the `@file` block **after** the include guard (`#pragma once` or `#ifndef`/`#define`). This ensures the documentation is parsed once along with the declarations it describes and keeps preprocessor directives separate from API documentation.

```cpp
#pragma once

/**
 * @file <filename>.hpp
 * @brief One-line description of the file's purpose.
 *
 * Detailed description of the file's contents and design decisions.
 *
 * @author <author_name>
 * @copyright Copyright (c) <year> <organization>
 * @license SPDX-License-Identifier: <license_identifier>
 */
```

### 6.2. Namespace Template

```cpp
/**
 * @brief One-line description of namespace contents.
 *
 * Detailed description of the namespace's role, the types of
 * components it contains, and how they relate to each other.
 */
namespace namespace_name {

// Namespace contents

}  // namespace namespace_name
```

### 6.3. Class Template

```cpp
/**
 * @brief One-line description of the class.
 *
 * Detailed description of the class responsibility, key invariants,
 * and usage patterns.
 *
 * @tparam T Description of template parameter and constraints.
 *
 * @note Thread safety: Describe thread safety guarantees.
 *
 * @see RelatedClass
 *
 * @code
 * ClassName<int> obj;
 * obj.method(param);
 * @endcode
 */
template <typename T>
class ClassName
{
  // ...
};
```

### 6.4. Function Template

```cpp
/**
 * @brief One-line description of what the function does.
 *
 * Detailed description including algorithm details and edge cases.
 *
 * @param[in] param1 Description of the input parameter.
 * @param[out] param2 Description of the output parameter.
 * @param[in,out] param3 Description of bidirectional parameter.
 *
 * @return Description of the return value.
 * @retval specific_value Meaning of this specific return value.
 *
 * @throws std::invalid_argument If param1 is invalid.
 * @throws std::runtime_error If operation fails.
 *
 * @pre Preconditions that must be met before calling.
 * @post Postconditions guaranteed after successful execution.
 *
 * @note Important information for users.
 * @warning Critical warnings about potential misuse.
 *
 * @see relatedFunction()
 *
 * @code
 * auto result = functionName(input, output);
 * @endcode
 */
ReturnType functionName(const InputType& param1, OutputType& param2);
```

### 6.5. Member Variable Template

```cpp
class ClassName
{
private:
  int count_;       ///< Number of items currently stored.
  bool is_valid_;   ///< Whether the object is in a valid state.

  /// Description for simple members.
  int simple_member_;

  /**
   * @brief Buffer for temporary storage.
   *
   * Detailed explanation of the member's purpose and
   * synchronization requirements.
   */
  std::vector<char> buffer_;
};
```

### 6.6. Enumeration Template

```cpp
/**
 * @brief Description of what this enumeration represents.
 *
 * Detailed description of the enum's purpose and usage context.
 */
enum class EnumName
{
  Success,     ///< Operation completed successfully.
  Error,       ///< Operation failed with an error.
  Pending,     ///< Operation is still in progress.
  NotFound     ///< Requested item was not found.
};
```

### 6.7. Module/Group Template

```cpp
/**
 * @defgroup module_name Module Display Name
 * @brief One-line description of the module.
 *
 * Detailed description of the module purpose and components.
 *
 * @{
 */

// Classes and functions belonging to this group

/** @} */  // End of module_name
```

### 6.8. Formula Template

```cpp
/**
 * @brief Calculates the Euclidean distance between two points.
 *
 * The distance between \f$(x_1,y_1)\f$ and \f$(x_2,y_2)\f$ is
 * \f$\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}\f$.
 *
 * For complex equations, use displayed formulas:
 * \f[
 *   d = \sqrt{\sum_{i=1}^{n}(p_i - q_i)^2}
 * \f]
 *
 * Multi-line equations using eqnarray environment:
 * \f{eqnarray*}{
 *   E &=& mc^2 \\
 *   F &=& ma
 * \f}
 *
 * @param[in] x1 X-coordinate of the first point.
 * @param[in] y1 Y-coordinate of the first point.
 * @param[in] x2 X-coordinate of the second point.
 * @param[in] y2 Y-coordinate of the second point.
 *
 * @return The Euclidean distance \f$d \geq 0\f$.
 */
double distance(double x1, double y1, double x2, double y2);
```

## 7. References

- Doxygen [Manual](https://www.doxygen.nl/manual/) guide.
- Doxygen [Commands](https://www.doxygen.nl/manual/commands.html) reference.
- Doxygen [Configuration](https://www.doxygen.nl/manual/config.html) reference.
- Doxygen [Formulas](https://www.doxygen.nl/manual/formulas.html) reference.
- Google C++ Style Guide [Comments](https://google.github.io/styleguide/cppguide.html#Comments) section.
