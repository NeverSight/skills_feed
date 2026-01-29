---
name: usd-editor
description: Guide for modifying USD ASCII (.usda) files, including prims, properties, composition arcs, variants, and transforms. Use when editing or reviewing .usda files by hand.
---

# USD Editor

## Description and Goals

This skill guides safe, minimal edits to USD ASCII (.usda) files and the proper use of USD command-line tools. It focuses on preserving stage structure, using correct specifiers and property types, and avoiding composition mistakes while making targeted changes.

### Goals

- Make precise edits without disrupting existing USD composition
- Preserve file formatting and authoring style
- Use correct prim specifiers, property types, and relationships
- Avoid common USD pitfalls (wrong paths, missing xformOpOrder, broken connections)
- Guide safe manipulation and inspection of USD assets using the command-line tools

## What This Skill Should Do

When asked to modify a .usda file, this skill should:

1. **Inspect the stage structure** - Identify root prims, scopes, and relevant paths.
2. **Choose the correct specifier** - Use `over` for edits to existing prims, `def` for new prims.
3. **Edit only what is necessary** - Preserve unrelated content and formatting.
4. **Respect composition** - Avoid changing subLayers, references, or variants unless asked.
5. **Validate connections and paths** - Ensure `SdfPath` targets are valid and type-compatible.

If the change is material- or shader-related for RealityKit, prefer the `shadergraph-editor` skill for node-specific guidance.

### Quick Start Workflow

1. Locate the prim path you need to edit (search by prim name or `SdfPath`).
2. Determine whether you should `over` an existing prim or `def` a new one.
3. Apply the smallest possible change (attribute value, relationship target, or child prim).
4. If adding transforms, update `xformOpOrder` to match your new ops.
5. Re-check any paths or connections you touched.

## Information About the Skill

### Core Concepts

#### Stage and Layer
A USD stage is composed of one or more layers. A .usda file is a single ASCII layer that can sublayer or reference others.

#### Prim and Specifier
A prim is a scene graph node. Specifiers control behavior: `def` creates, `over` modifies, `class` defines a reusable template.

#### Properties
Attributes store typed data; relationships (`rel`) point to other prims.

#### Composition Arc
Mechanisms like sublayers, references, and payloads that bring other USD data into the stage.

#### SdfPath
A path to a prim or property, written like `</Root/Child>` or `</Root/Mat.outputs:surface>`.

#### List Editing
USD list ops (`prepend`, `append`, `delete`, `add`) modify lists without replacing them.

#### Variants
Variant sets provide alternative content branches for a prim.

#### Time Samples
Animated or time-varying data stored in `timeSamples` dictionaries.

### Reference Tables

| Reference | When to Use |
|-----------|-------------|
| [`usd-syntax`](references/usd-syntax.md) | When you need a refresher on .usda syntax, values, and path formats. |
| [`prims-properties`](references/prims-properties.md) | When adding or editing prims, attributes, or relationships. |
| [`composition-variants`](references/composition-variants.md) | When touching sublayers, references, payloads, or variant sets. |
| [`transforms-units`](references/transforms-units.md) | When editing transforms, xformOps, or stage units/up axis metadata. |
| [`time-samples`](references/time-samples.md) | When modifying animated/time-sampled properties. |
| [`command-line-tools`](references/command-line-tools.md) | When you need a quick reference for common USD command-line tools. |
| [`usdcat`](references/usdcat.md) | When converting, flattening, or inspecting USD files. |
| [`usdchecker`](references/usdchecker.md) | When validating USD or USDZ assets, including RealityKit-focused checks. |
| [`usdrecord`](references/usdrecord.md) | When rendering images from USD files. |
| [`usdtree`](references/usdtree.md) | When inspecting the prim hierarchy of a USD file. |
| [`usdzip`](references/usdzip.md) | When creating or inspecting USDZ packages. |
| [`usdcrush`](references/usdcrush.md) | When compressing USD or USDZ assets for size. |
| [`usdextract`](references/usdextract.md) | When extracting files from USD-compatible packages. |

### Implementation Patterns

#### Override an Existing Prim

```usda
over "Mesh"
{
    token visibility = "invisible"
}
```

#### Add a Simple Xform with Translate

```usda
def Xform "Pivot"
{
    double3 xformOp:translate = (0.0, 0.1, 0.0)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}
```

#### Bind a Material Relationship

```usda
rel material:binding = </Materials/Mat>
```

### Pitfalls and Checks

- Don't replace a prim with `def` when you only need an `over`.
- Keep `xformOpOrder` consistent with the ops you add or remove.
- Verify `SdfPath` targets exist and match the expected property type.
- Avoid editing composition arcs unless explicitly requested.
- Preserve existing formatting and comments to minimize diff noise.
