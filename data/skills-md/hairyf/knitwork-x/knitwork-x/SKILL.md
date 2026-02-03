---
name: knitwork-x
description: Utilities to generate JavaScript and TypeScript code programmatically. Use when building code generators, AST-to-code output, or dynamic source generation.
metadata:
  author: hairyf
  version: "0.2.0"
  source: docs/ (current project)
---

knitwork-x provides **programmatic code generation** for JavaScript and TypeScript. It is forked from [knitwork](https://github.com/unjs/knitwork) and adds comprehensive TypeScript helpers: ESM (import/export), strings, variables, classes, interfaces, functions, types, control flow (if/try/loop/switch), and serialization (object/array/map/set). All `gen*` functions return **strings** suitable for splicing into source; they are pure and do not mutate inputs.

Use this skill when an agent needs to **generate code strings** (e.g. for codegen tools, plugins, or dynamic module output).

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Purpose, install, when to use | [core-overview](references/core-overview.md) |
| ESM | Import, export, default export, dynamic import | [core-esm](references/core-esm.md) |
| String | genString, escapeString, genTemplateLiteral | [core-string](references/core-string.md) |
| Variable | genVariable, genVariableName | [core-variable](references/core-variable.md) |
| Design Guidelines | Naming, params, options (for contributors) | [core-design-guidelines](references/core-design-guidelines.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Class | genClass, genConstructor, genProperty, genMethod, getter/setter | [features-class](references/features-class.md) |
| Interface | genInterface, genIndexSignature | [features-interface](references/features-interface.md) |
| Enum | genEnum, genConstEnum | [features-enum](references/features-enum.md) |
| Function | genFunction, genArrowFunction, genBlock, genParam | [features-function](references/features-function.md) |
| Type | genTypeAlias, genUnion, genIntersection, genMappedType, etc. | [features-type](references/features-type.md) |
| Conditional | genConditionalType, genTernary | [features-conditional](references/features-conditional.md) |
| Decorator | genDecorator | [features-decorator](references/features-decorator.md) |
| Module & Namespace | genModule, genNamespace, genDeclareNamespace | [features-module-namespace](references/features-module-namespace.md) |
| Condition | genIf, genElse, genElseIf | [features-condition](references/features-condition.md) |
| Try | genTry, genCatch, genFinally | [features-try](references/features-try.md) |
| Loop | genFor, genForOf, genWhile, genDoWhile | [features-loop](references/features-loop.md) |
| Switch | genSwitch, genCase, genDefault | [features-switch](references/features-switch.md) |
| Statement | genReturn, genThrow, genPrefixedBlock | [features-statement](references/features-statement.md) |
| Object & Serialization | genObject, genArray, genMap, genSet, genTypeObject | [features-object](references/features-object.md) |
| Utils | genComment, genKey, genLiteral, genRegExp, wrapInDelimiters | [features-utils](references/features-utils.md) |

## Key Points

- **Return type:** Every `gen*` function returns a `string` (code fragment).
- **Options:** Most accept an optional `options` object (e.g. `export`, `singleQuotes`, `indent`); default to `{}`.
- **Indent:** When supported, pass `indent` as the last parameter; use `indent + "  "` for nested blocks.
- **Strings:** Use `genString(input, options)` for quoted/escaped output so `singleQuotes` is respected.
- **Composing:** Combine `gen*` outputs (e.g. `genClass(..., [genConstructor(...)])`) to build larger snippets.
