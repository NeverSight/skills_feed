---
name: roblox-ts
description: |
    Use when writing TypeScript code for Roblox using roblox-ts, especially when
    unsure if a JavaScript API exists or how to handle Luau interop
metadata:
    author: Christopher Buss
    version: "2026.1.31"
    source:
        Generated from https://github.com/roblox-ts/roblox-ts.com, scripts at
        https://github.com/christopher-buss/skills
---

> Based on roblox-ts v3.0.0, generated 2026-01-31

TypeScript-to-Luau transpiler for Roblox. This is "Roblox with TypeScript
syntax", not full JavaScript - many JS APIs don't exist.

## Core References

| Topic          | Description                                             | Reference                                                |
| -------------- | ------------------------------------------------------- | -------------------------------------------------------- |
| JS Differences | Missing APIs, assert() truthiness, any type, typeof     | [core-js-differences](references/core-js-differences.md) |
| Type Checking  | typeIs, classIs, RemoteEvent validation                 | [core-type-checking](references/core-type-checking.md)   |
| Constructors   | new syntax, DataType math (.add/.sub), collections      | [core-constructors](references/core-constructors.md)     |
| Utility Types  | satisfies, InstancePropertyNames, Services, ExtractKeys | [core-utility-types](references/core-utility-types.md)   |

## Features

| Topic          | Description                                               | Reference                                                      |
| -------------- | --------------------------------------------------------- | -------------------------------------------------------------- |
| Luau Interop   | $tuple, LuaTuple, type declarations, callbacks vs methods | [feature-luau-interop](references/feature-luau-interop.md)     |
| Game Hierarchy | Typing Workspace children with services.d.ts              | [feature-game-hierarchy](references/feature-game-hierarchy.md) |
