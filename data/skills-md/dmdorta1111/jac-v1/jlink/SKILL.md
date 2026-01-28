---
name: jlink
description: >
  Java automation toolkit for Creo Parametric (J-Link/Object TOOLKIT Java). Use when users ask about:
  writing Jlink applications, Session management, model/feature/parameter operations, interactive selection,
  assembly automation, drawing generation, UI/menu integration, batch processing, error handling,
  performance optimization, or any programmatic Creo design automation via Java.
---

# Jlink - Java Automation Toolkit for Creo Parametric

Jlink (Object TOOLKIT Java) is a free Java API that enables programmatic automation of Creo Parametric design tasks. It provides Session-based access to models, features, parameters, assemblies, and drawings.

## Quick Start

**New to Jlink?** Start here:
1. Read **Architecture Overview** below
2. Study **Basic Patterns** for initialization
3. Review **Common Tasks Decision Tree**
4. Check **Reference Guide** for specific operations

## Core Concepts

### Session Model (Entry Point)
All Jlink operations flow through a single `Session` object:

```java
// Get active session (main pattern)
Session session = pfcSession.GetCurrentSessionWithCompatibility(
    CreoCompatibility.C4Compatible
);

// Now use session for all operations
Model model = session.RetrieveModel(descriptor);
```

### Exception Handling (Universal)
All Jlink methods throw `jxthrowable`:

```java
try {
    // Any Jlink operation
    Model model = session.RetrieveModel(descriptor);
    Feature feat = model.GetFeatureByName("MY_FEATURE");
} catch (jxthrowable x) {
    x.printStackTrace();
    // Handle error
}
```

### Object Hierarchy
```
Session (connection to Creo)
├── Model (Part, Assembly, or Drawing)
│   ├── FeatureTree (all features)
│   ├── ParameterTable (model parameters)
│   └── Drawing-specific (sheets, views, notes)
├── UICommand (menu/toolbar integration)
└── Selection (interactive user selection)
```

## Architecture Overview

### Packages (20+ modules, but focus on core 6)

| Package | Purpose | Key Classes |
|---------|---------|------------|
| `pfcSession` | Session management | Session, Selection, UICommand |
| `pfcModel` | Models (parts, assemblies, drawings) | Model, ModelDescriptor, ModelType |
| `pfcFeature` | Feature creation & manipulation | Feature, FeatureCreate, FeatureType |
| `pfcParameter` | Parameters & dimensions | Parameter, ParamValue, DimensionType |
| `pfcGeometry` | Geometry operations | Point, Vector, Transform |
| `pfcAsyncConnection` | Async/remote operations | AsyncConnection, AsyncServer |

### Session Lifecycle

```java
// 1. Retrieve session (usually already exists)
Session session = pfcSession.GetCurrentSessionWithCompatibility(
    CreoCompatibility.C4Compatible
);

// 2. Work with models/features/parameters
try {
    // Do work
} catch (jxthrowable x) {
    // Handle errors
}

// 3. Cleanup (usually automatic in application context)
// No explicit disconnect needed for current session
```

## Basic Patterns

### 1. Model Operations

**Retrieve existing model:**
```java
// By name and type
ModelDescriptor descr = pfcModel.ModelDescriptor_Create(
    ModelType.MDL_PART,
    "my_part",
    null  // No directory
);
Model model = session.RetrieveModel(descr);

// Get current model in Creo
Model current = session.GetCurrentModel();
```

**Create/save model:**
```java
ModelDescriptor descr = pfcModel.ModelDescriptor_Create(
    ModelType.MDL_PART,
    "new_part",
    null
);
Model newModel = session.CreateModel(descr, null);

// Save to working directory
newModel.Save();  // or SaveAs(descriptor)
```

**Model types:**
- `ModelType.MDL_PART` - Part file
- `ModelType.MDL_ASSEMBLY` - Assembly file
- `ModelType.MDL_DRAWING` - Drawing file

### 2. Feature Access & Creation

**Get feature by name:**
```java
try {
    Feature feat = model.GetFeatureByName("EXTRUDE_1");
} catch (jxthrowable x) {
    // Feature not found
}
```

**Iterate features:**
```java
FeatureTree featTree = model.GetFeatureTree();
Sequence<Feature> features = featTree.GetFeatures();

for (int i = 0; i < features.GetMembersCount(); i++) {
    Feature f = features.GetMember(i);
    // Process feature
}
```

**Create feature (example: extrude):**
```java
FeatureCreateData createData = pfcFeature.FeatureCreate_Create(
    FeatureType.EXTRUDE,
    ModelRef.CURRENT,  // Current model
    "", null, null
);

// Set extrude depth
createData.SetIntParam("depth_type", 1);  // ONE_SIDED
createData.SetDoubleParam("depth_1", 10.0);  // 10 units

// Create and return feature
Feature newFeat = model.CreateFeature(createData);
```

### 3. Parameter Operations

**Get parameter value:**
```java
try {
    Parameter param = model.GetParam("THICKNESS");
    ParamValue val = param.GetValue();
    double thickness = val.GetDoubleValue();
} catch (jxthrowable x) {
    // Parameter not found
}
```

**Set parameter value:**
```java
Parameter param = model.GetParam("THICKNESS");
ParamValue newVal = pfcParameter.ParamValue_CreateDoubleParamValue(2.5);
param.SetValue(newVal);
```

**Model parameters:**
```java
// Get all parameters
ParameterTable paramTable = model.GetParameters();
Sequence<Parameter> params = paramTable.GetParams();

for (int i = 0; i < params.GetMembersCount(); i++) {
    Parameter p = params.GetMember(i);
    // Access param
}
```

### 4. Interactive Selection

**Get user selection:**
```java
UICommand cmd = session.UICreateCommand("custom.select", selectionListener);

// Selection types
SelectionOptions opts = pfcSelection.SelectionOptions_Create();
opts.AddFilterType(SelectionType.EDGE);  // Allow edge selection
opts.SetMaxSelectCount(5);  // Max 5 edges

Selection selection = session.UISelect(opts, null);
```

**Process selections:**
```java
int count = selection.GetSelectionCount();
for (int i = 0; i < count; i++) {
    SelectedObject selObj = selection.GetSelectionItem(i);
    GeometryType geomType = selObj.GetSelectionType();
    // Use selected geometry
}
```

### 5. Assembly Operations

**Add component:**
```java
ModelDescriptor compDescr = pfcModel.ModelDescriptor_Create(
    ModelType.MDL_PART,
    "component_name",
    null
);

ComponentFeat compFeat = (ComponentFeat)model.CreateFeature(
    pfcFeature.FeatureCreate_Create(
        FeatureType.COMPONENT,
        ModelRef.CURRENT,
        "", compDescr, null
    )
);
```

**Apply constraints:**
```java
Constraint constraint = pfcConstraint.Constraint_CreateMateConstraint(
    surfaceRef1,  // First reference
    surfaceRef2   // Second reference
);
model.AddConstraint(constraint);
```

### 6. Drawing Automation

**Create drawing view:**
```java
// Open template or create drawing
ModelDescriptor drawDescr = pfcModel.ModelDescriptor_Create(
    ModelType.MDL_DRAWING,
    "drawing_name",
    null
);
Model drawing = session.CreateModel(drawDescr, null);

// Add view (simplified)
DrawingSheet sheet = drawing.GetCurrentSheet();
DrawingView view = sheet.CreateGeneralView(modelRef, viewData);
```

## Common Tasks Decision Tree

**Choose task → find reference file → implement pattern**

### Model Management
- **Open/retrieve model** → `session.RetrieveModel(descriptor)`
- **Create new model** → `session.CreateModel(descriptor, null)`
- **Save model** → `model.Save()` or `model.SaveAs(descriptor)`
- **Check if modified** → `model.GetModified()` → bool

### Feature Operations
- **Get feature by name** → `solid.GetFeatureByName(name)`
- **Iterate all features** → `solid.ListFeaturesByType(true, null)`
- **Create feature** → `solid.CreateFeature(FeatureCreateInstructions)`
- **Delete feature** → `feature.CreateDeleteOp()` then execute
- **Get feature dimensions** → `feature.ListSubItems(ITEM_DIMENSION)` (returns ModelItems)

### Parameters
- **Get parameter** → `model.GetParam(name)` → `GetValue()`
- **Set parameter** → `param.SetValue(newValue)`
- **List all parameters** → `model.GetParameters().GetParams()`
- **Create parameter** → `model.AddParam()`

### Assembly
- **Add component** → Feature creation with `FeatureType.FEATTYPE_COMPONENT`
- **Apply constraint** → `componentFeat.SetConstraints(constraints, path)`
- **List components** → `solid.ListFeaturesByType(true, FeatureType.FEATTYPE_COMPONENT)`
- **Get subassembly** → `componentFeat.GetModelDescr()` → `session.RetrieveModel()`

### Interactive Selection
- **Select edges** → `SelectionOptions.AddFilterType(SelectionType.EDGE)`
- **Select surfaces** → `SelectionOptions.AddFilterType(SelectionType.SURFACE)`
- **Get selected geometry** → `selection.GetSelectionItem(i)` → process

### Drawing
- **Create view** → `sheet.CreateGeneralView(modelRef, viewData)`
- **Add note/dimension** → `sheet.CreateGeneralNote(position, text)`
- **Export/print** → Drawing-specific APIs
- **Get sheets** → `drawing.GetDrawingSheets()`

## Best Practices

1. **Always use try-catch** - All Jlink operations throw `jxthrowable`
2. **Validate model type** before specific operations (part vs assembly vs drawing)
3. **Regenerate after changes** - `model.Regenerate()` for feature/parameter changes
4. **Check references validity** - Geometry handles may become invalid after regen
5. **Batch operations** - Group model open/close for efficiency
6. **Session reuse** - Don't create new sessions; reuse `GetCurrentSessionWithCompatibility()`
7. **Clear resources** - Free large collections/selections after use
8. **Log operations** - Essential for debugging batch/async processes
9. **Handle missing features** - Wrap feature access in try-catch
10. **Test with actual model** - Jlink behavior varies by Creo configuration

## Reference Files

For detailed information, see:
- **jlink-session.md** - Session creation, lifecycle, compatibility modes
- **jlink-models.md** - Model operations (open, create, save, properties)
- **jlink-features.md** - Feature creation, types, dimension manipulation
- **jlink-parameters.md** - Parameter access, modification, validation
- **jlink-assembly.md** - Assembly operations, constraints, components
- **jlink-drawing.md** - Drawing automation, views, sheets, export
- **jlink-selection.md** - Interactive selection, geometry types, filters
- **jlink-patterns.md** - Complete end-to-end workflow patterns
- **jlink-error-handling.md** - Exception strategies, recovery, logging
- **jlink-performance.md** - Optimization techniques, caching, async patterns

## Installation & Setup

**Prerequisites:**
- Creo 4.0+ with J-Link/OTK selected during installation
- Java 21+ JDK for Creo 12.4+ (class file version 65.0)
- IDE: Eclipse, IntelliJ, or VS Code

**CLASSPATH configuration (Creo 12.4+):**
```
${CREO_HOME}/Common Files/text/java/otk.jar
${CREO_HOME}/Common Files/text/java/pfcasync.jar
```

**CLASSPATH configuration (Creo 4.0-11.x):**
```
${CREO_HOME}/Common Files/otk_java_free/*.jar
```

**Application registration (jlink.txt):**
```
DESCRIPTION=MyApp
STARTUP=DLL
JAVA_MAIN_CLASS=com.mycompany.MyApp
JLINK_VERSION=11.0
CLASSPATH=MyApp.jar
```

## Common Use Cases

**Batch Model Modification:**
1. Get session
2. For each model: RetrieveModel() → modify parameters → Regenerate() → Save()

**Assembly Generation from Data:**
1. Create base assembly
2. For each component: AddFeature(COMPONENT) → ApplyConstraints()
3. Save assembly

**Feature Extraction for CAM:**
1. Get model
2. Iterate features by type
3. Extract geometry references
4. Generate NC code or CNC path data

**Parameter-Driven Design:**
1. Get session
2. Modify model parameters
3. Regenerate model
4. Extract modified geometry
5. Generate drawings/exports

**UI Integration:**
1. Create UICommand
2. Register in menu/toolbar
3. Handle selection via SelectionListener
4. Apply changes to model

## Creo 12.4 API Quick Reference

### Verified Methods (from JAR analysis)
| Interface | Method | Returns | Description |
|-----------|--------|---------|-------------|
| Session | `GetCurrentDirectory()` | String | Current working dir |
| Session | `GetActiveModel()` | Model | Current active model |
| Session | `RetrieveModel(ModelDescriptor)` | Model | Open model |
| Model | `GetFullName()` | String | Full model path |
| Model | `GetFileName()` | String | File name only |
| Model | `GetType()` | ModelType | MDL_PART/MDL_ASSEMBLY |
| Model | `ListParams()` | Parameters | All parameters |
| Solid | `ListFeaturesByType(Boolean, FeatureType)` | Features | Get features |
| Solid | `GetFeatureByName(String)` | Feature | Get single feature |
| Solid | `GetPrincipalUnits()` | UnitSystem | Unit system |
| Feature | `GetName()` | String | Feature name |
| Feature | `GetFeatType()` | FeatureType | Feature type |
| Feature | `GetStatus()` | FeatureStatus | SUPPRESSED/ACTIVE/etc |
| Feature | `ListSubItems(ModelItemType)` | ModelItems | Get dimensions etc |
| Feature | `ListChildren()` | Features | Dependent features |
| BaseDimension | `GetDimValue()` | double | Dimension value |
| BaseDimension | `SetDimValue(double)` | void | Set dimension |
| ComponentFeat | `GetModelDescr()` | ModelDescriptor | Component model |
| Parameter | `GetValue()` | ParamValue | Parameter value |
| ParamValue | `GetDoubleValue()` | Double | Numeric value |
| ParamValue | `GetStringValue()` | String | String value |

### Non-Existent Methods (Common Mistakes)
| Wrong Method | Correct Alternative |
|--------------|---------------------|
| `session.IsAlive()` | Try-catch `GetCurrentDirectory()` |
| `session.GetWorkingDirectory()` | `GetCurrentDirectory()` |
| `session.UISetComputeMode()` | Not available in Creo 12.4 |
| `model.GetModelName()` | `GetFullName()` or `GetFileName()` |
| `feat.GetSuppressed()` | `GetStatus() == FEAT_SUPPRESSED` |
| `feat.GetFailed()` | `GetStatus() == FEAT_UNREGENERATED` |
| `feat.ListDimensions()` | `ListSubItems(ITEM_DIMENSION)` |
| `dim.GetValue()` | `GetDimValue()` (BaseDimension) |
| `compFeat.GetModelDescriptor()` | `GetModelDescr()` |
| `model.GetUnitsystem()` | `Solid.GetPrincipalUnits()` |

## Unresolved Questions

- Async connection best practices for distributed teams
- Performance optimization for large assemblies (100+ components)
- Integration patterns with SmartAssembly scripting workflow
