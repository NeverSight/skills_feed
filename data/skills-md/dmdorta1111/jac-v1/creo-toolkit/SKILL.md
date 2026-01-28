---
name: creo-toolkit
description: >
  Expert-level PTC Creo Parametric TOOLKIT (C API) development resource. Use when users ask about:
  writing Creo TOOLKIT applications in C/C++, ProE/Creo API function usage, feature creation with
  element trees (holes, chamfers, rounds, datum points, datum axes, remove surfaces, extrusions),
  ProFeatureCreate/ProFeatureWithoptionsCreate/ProFeatureRedefine, ProMdl/ProSolid/ProFeature objects,
  visit functions and filtering, ProSelection and geometry references, curve and surface collections
  (ProCrvcollection/ProSrfcollection), UI programming with dialogs/menus/ribbons, asynchronous vs
  DLL mode, registry files (protk.dat/creotk.dat), error handling with ProError, geometry traversal
  and tessellation, assembly operations, drawing automation, layers and display status, relations
  and custom relation functions, parameters with units, material properties and mass calculations,
  manufacturing/NC programming, or debugging TOOLKIT applications.
---

# Creo Parametric TOOLKIT API Reference

Creo Parametric TOOLKIT is PTC's C-language API for customizing Creo Parametric. It provides controlled access to the Creo database and user interface through a library of C functions.

## API Style and Conventions

### Naming Convention
All functions follow: `Pro<ObjectType><Action>()`

```c
ProSolidRegenerate()      // Object=Solid, Action=Regenerate
ProFeatureDelete()        // Object=Feature, Action=Delete
ProSurfaceAreaEval()      // Object=Surface, Action=AreaEval
ProEdgeLengthEval()       // Object=Edge, Action=LengthEval
```

### Action Verbs
| Verb | Purpose |
|------|---------|
| Get | Read directly from database |
| Set | Write to database |
| Eval | Simple calculation result |
| Compute | Numerical analysis (geometry-based) |
| Visit | Traverse items with callback |
| Create | Create new object |
| Delete | Remove object |
| Alloc/Free | Memory management |

### Function Arguments
- First argument: target object
- Input arguments before output arguments
- Return type: `ProError` (enumerated status)

### Common Error Codes
```c
PRO_TK_NO_ERROR        // Success
PRO_TK_BAD_INPUTS      // Invalid arguments
PRO_TK_E_NOT_FOUND     // Item not found
PRO_TK_USER_ABORT      // User cancelled
PRO_TK_GENERAL_ERROR   // General failure
PRO_TK_OUT_OF_MEMORY   // Memory allocation failed
PRO_TK_BAD_CONTEXT     // Wrong mode/state
```

## Object Handles

### Opaque Handles (OHandle)
Memory pointers to Creo structures - volatile, may become invalid after regeneration:
```c
typedef void* ProMdl;
typedef struct sld_part* ProSolid;
typedef struct geom* ProSurface;
typedef struct curve_header* ProEdge;
typedef struct entity* ProAxis;
typedef struct entity* ProCsys;
```

### Database Handles (DHandle)
Persistent identifiers with type, ID, and owner:
```c
typedef struct pro_model_item {
    ProType type;
    int id;
    ProMdl owner;
} ProModelitem, ProGeomitem;
```

### Converting Between Handles
```c
// OHandle to DHandle
ProSurfaceIdGet(surface, &id);
ProModelitemInit(owner, PRO_SURFACE, id, &modelitem);

// DHandle to OHandle  
ProSurfaceInit(modelitem.owner, modelitem.id, &surface);
```

## Application Structure

### Required Entry Points
```c
#include "ProToolkit.h"

int user_initialize(int argc, char *argv[], 
                    char *version, char *build,
                    wchar_t err_buff[80])
{
    // Setup menus, notifications, initialization
    // Must contain at least one Pro* API call
    return 0;  // 0=success, non-zero=failure
}

void user_terminate()
{
    // Cleanup code
}
```

### Registry File (creotk.dat)
```
name MyApplication
startup dll
exec_file C:\path\to\myapp.dll
text_dir C:\path\to\text
allow_stop TRUE
end
```

### Application Modes
| Mode | Description | Use Case |
|------|-------------|----------|
| DLL | Dynamic linking into Creo | Production deployment |
| Multiprocess (spawn) | Separate process | Development/debugging |
| Asynchronous | Independent process | Batch operations |

## Visit Functions

Pattern for traversing collections:
```c
ProError MyVisitAction(ProFeature* feature, 
                       ProError status,
                       ProAppData app_data)
{
    // Process feature
    return PRO_TK_NO_ERROR;  // Continue visiting
    // return PRO_TK_E_FOUND; // Stop visiting
}

ProError MyFilter(ProFeature* feature, ProAppData app_data)
{
    // Return PRO_TK_CONTINUE to skip
    // Return any other value to visit
    return PRO_TK_NO_ERROR;
}

// Usage
ProSolidFeatVisit(solid, MyVisitAction, MyFilter, &my_data);
```

### Common Visit Functions
- `ProSolidFeatVisit()` - Features in solid
- `ProSolidSurfaceVisit()` - Surfaces in solid
- `ProSolidAxisVisit()` - Axes in solid
- `ProSolidCsysVisit()` - Coordinate systems
- `ProSolidQuiltVisit()` - Quilts
- `ProFeatureSurfaceVisit()` - Surfaces in feature
- `ProAsmcompVisit()` - Assembly components

## Expandable Arrays (ProArray)

Dynamic arrays for variable-size data:
```c
ProArray my_array;

// Allocate: count, element_size, growth_increment
ProArrayAlloc(0, sizeof(ProFeature), 10, &my_array);

// Add element
ProFeature feat;
ProArrayObjectAdd(&my_array, PRO_VALUE_UNUSED, 1, &feat);

// Get size
int size;
ProArraySizeGet(my_array, &size);

// Access elements
ProFeature* features = (ProFeature*)my_array;
for (int i = 0; i < size; i++) {
    // Use features[i]
}

// Free
ProArrayFree(&my_array);
```

## ProSelection Object

References geometry in assembly context:
```c
ProSelection selection;
ProModelitem modelitem;
ProAsmcomppath comp_path;

// Create selection
ProSelectionAlloc(&comp_path, &modelitem, &selection);

// Extract info
ProSelectionModelitemGet(selection, &modelitem);
ProSelectionAsmcomppathGet(selection, &comp_path);

// Free
ProSelectionFree(&selection);
```

## Models and File Operations

```c
ProMdl model;
ProName name;
ProMdlType type;

// Retrieve model
ProStringToWstring(name, "part_name");
ProMdlnameRetrieve(name, PRO_MDL_PART, &model);

// Get current model
ProMdlCurrentGet(&model);

// Save model
ProMdlSave(model);

// Erase from session
ProMdlErase(model);
```

## Feature Creation Overview

Features are created using Element Trees - hierarchical data structures:

1. Allocate root element: `PRO_E_FEATURE_TREE`
2. Add feature type: `PRO_E_FEATURE_TYPE`
3. Add feature-specific elements (including references via `ProSelectionToReference`)
4. Get current model and create model selection
5. Call `ProFeatureWithoptionsCreate()` with options array

### Standard Pattern (Recommended)
```c
ProError CreateFeatureExample()
{
    ProElement feat_elemtree, elem_feattype;
    ProMdl model;
    ProModelitem model_item;
    ProSelection model_selection;
    ProFeature created_feature;
    ProErrorlist errors;
    ProFeatureCreateOptions *options = NULL;
    ProError status;

    /* 1. Allocate root element */
    status = ProElementAlloc(PRO_E_FEATURE_TREE, &feat_elemtree);

    /* 2. Add feature type */
    status = ProElementAlloc(PRO_E_FEATURE_TYPE, &elem_feattype);
    status = ProElementIntegerSet(elem_feattype, PRO_FEAT_xxx);
    status = ProElemtreeElementAdd(feat_elemtree, NULL, elem_feattype);

    /* 3. Add feature-specific elements... */

    /* 4. Get current model and create selection */
    status = ProMdlCurrentGet(&model);
    status = ProMdlToModelitem(model, &model_item);
    status = ProSelectionAlloc(NULL, &model_item, &model_selection);

    /* 5. Set creation options */
    status = ProArrayAlloc(1, sizeof(ProFeatureCreateOptions), 1, (ProArray*)&options);
    options[0] = PRO_FEAT_CR_DEFINE_MISS_ELEMS;

    /* 6. Create the feature */
    status = ProFeatureWithoptionsCreate(model_selection, feat_elemtree,
        options, PRO_REGEN_NO_FLAGS, &created_feature, &errors);

    /* 7. Cleanup */
    status = ProArrayFree((ProArray*)&options);
    status = ProElementFree(&feat_elemtree);
    status = ProSelectionFree(&model_selection);

    return status;
}
```

### Setting Element Values (Preferred Type-Specific Functions)
```c
/* Integer values */
ProElementIntegerSet(elem, PRO_FEAT_HOLE);

/* Double values */
ProElementDoubleSet(elem, 25.5);

/* Wide string values */
ProName wname;
ProStringToWstring(wname, "MY_FEATURE");
ProElementWstringSet(elem, wname);

/* Reference values (from selections) */
ProReference reference;
ProSelectionToReference(selection, &reference);
ProElementReferenceSet(elem, reference);

/* Collection values */
ProElementCollectionSet(elem, collection);
```

See **references/element-trees.md** and **references/feature-creation-examples.md** for detailed patterns.

## Error Handling Pattern

```c
ProError status;
status = ProSomeFunction(...);
if (status != PRO_TK_NO_ERROR) {
    switch (status) {
        case PRO_TK_BAD_INPUTS:
            // Handle invalid inputs
            break;
        case PRO_TK_E_NOT_FOUND:
            // Handle not found
            break;
        default:
            // Handle other errors
            break;
    }
}
```

## Wide Strings

Creo uses wide character strings for internationalization:
```c
wchar_t wname[PRO_NAME_SIZE];
char cname[PRO_NAME_SIZE];

// Convert string to wstring
ProStringToWstring(wname, "MyName");

// Convert wstring to string
ProWstringToString(cname, wname);

// Wide string operations
ProWstringCopy(dest, source, PRO_VALUE_UNUSED);
ProWstringCompare(str1, str2, PRO_VALUE_UNUSED, &result);
int length;
ProWstringLengthGet(wstr, &length);
```

## Reference Files

For detailed information, see:
- **references/element-trees.md** - Feature creation with element trees
- **references/feature-creation-examples.md** - Complete feature examples (holes, chamfers, datum points/axes, remove surface)
- **references/core-objects.md** - Core object types and relationships  
- **references/common-functions.md** - Common function patterns
- **references/ui-programming.md** - User interface programming
- **references/utility-functions.md** - ProUtil* helper functions from PTC examples (NOT official API)
- **references/layers-relations-materials.md** - Layers, relations, parameters, and material operations

## Curve and Surface Collections

For features that operate on multiple edges or surfaces (chamfers, rounds, remove surface):

### Curve Collection (Edges)
```c
#include <ProCrvcollection.h>

ProCollection collection;
ProCrvcollinstr instr;
ProReference reference;

ProCrvcollectionAlloc(&collection);
ProCrvcollinstrAlloc(PRO_CURVCOLL_ADD_ONE_INSTR, &instr);
ProSelectionToReference(edge_selection, &reference);
ProCrvcollinstrReferenceAdd(instr, reference);
ProCrvcollectionInstructionAdd(collection, instr);

/* Optional: add tangent chain */
ProCrvcollinstrAlloc(PRO_CURVCOLL_ADD_TANGENT_INSTR, &instr);
ProCrvcollectionInstructionAdd(collection, instr);

/* Set in element */
ProElementCollectionSet(elem, collection);
```

### Surface Collection
```c
#include <ProSrfcollection.h>

ProCollection collection;
ProSrfcollinstr instr;
ProReference reference;
ProSrfcollref instr_ref;

ProSrfcollectionAlloc(&collection);
ProSrfcollinstrAlloc(1, PRO_B_TRUE, &instr);
ProSrfcollinstrIncludeSet(instr, 1);

ProSelectionToReference(surface_selection, &reference);
ProSrfcollrefAlloc(PRO_SURFCOLL_REF_SINGLE, reference, &instr_ref);
ProSrfcollinstrReferenceAdd(instr, instr_ref);
ProSrfcollectionInstructionAdd(collection, instr);
```

## Layer Operations

```c
#include <ProLayer.h>

/* Create layer */
ProLayer layer;
layer.owner = model;
ProStringToWstring(layer.layer_name, "MY_LAYER");
ProLayerCreate(&layer);

/* Add item to layer */
ProLayerItem item;
item.type = PRO_FEATURE;
item.id = feature_id;
ProLayerItemAdd(&layer, &item);

/* Set display status */
ProLayerDisplaystatusSet(&layer, PRO_LAYER_TYPE_BLANK);
ProWindowRepaint(-1);
```

## Custom Relation Functions

```c
#include <ProRelSet.h>

/* Register function for use in relations dialog */
ProRelfuncArg *args;
ProArrayAlloc(1, sizeof(ProRelfuncArg), 1, (ProArray*)&args);
args[0].type = PRO_PARAM_DOUBLE;
args[0].attributes = PRO_RELF_ATTR_NONE;

ProRelationFunctionRegister("my_calc", args,
    MyReadFunc,    /* For RHS - returns value */
    MyWriteFunc,   /* For LHS - sets value */
    NULL, PRO_B_FALSE, NULL);
```

## Utility Functions Note

Functions starting with `ProUtil*` (e.g., `ProUtilVectorCross`, `ProUtilMatrixInvert`, `ProUtilFeatCreate`) 
are **custom helper functions from PTC's example code**, NOT official Pro/TOOLKIT API. They are found in
headers like `UtilMath.h`, `UtilMatrix.h`, `UtilFeats.h`. To use them, either include the source files
from PTC's examples or implement equivalent functionality.

## Menu System (Legacy Menus)

For custom menus in Pro/TOOLKIT:

```c
#include <ProMenu.h>

int menu_id;
int action;

/* Register menu from .mnu file */
ProMenuFileRegister("MYMENU", "mymenu.mnu", &menu_id);

/* Set button actions */
ProMenubuttonActionSet("MYMENU", "Option1", MyAction, NULL, 1);
ProMenubuttonActionSet("MYMENU", "Option2", MyAction, NULL, 2);
ProMenubuttonActionSet("MYMENU", "MYMENU", MyMenuExit, NULL, -1);

/* Create and process menu */
ProMenuCreate(PROMENUTYPE_MAIN, "MYMENU", &menu_id);
ProMenuProcess("MYMENU", &action);

/* Action callback */
int MyAction(ProAppData data, int value)
{
    /* Process selection based on value */
    return 0;
}

/* Exit menu */
int MyMenuExit(ProAppData data, int value)
{
    ProMenuDeleteWithStatus(value);
    return 0;
}
```

## Best Practices

1. **Always check return status** of Pro* functions
2. **Free allocated memory** - ProArray, ProSelection, ProElement, ProReference, etc.
3. **Use PRO_TK_NO_ERROR** for success checks
4. **Include proper headers** - ProToolkit.h first, then object-specific headers
5. **Validate wchar_t size** with `ProWcharSizeVerify()` in user_initialize
6. **Use DLL mode** for production, multiprocess for debugging
7. **Unlock applications** before distribution with `protk_unlock.bat`
8. **Base makefiles** on PTC-provided samples for correct compiler flags
9. **Use ProFeatureWithoptionsCreate** instead of ProFeatureCreate for better control
10. **Use type-specific element setters** (ProElementIntegerSet, ProElementDoubleSet) over ProValueData
11. **Convert selections to references** using ProSelectionToReference for element trees
12. **Use PRO_FEAT_CR_DEFINE_MISS_ELEMS** option to prompt for missing elements during development
13. **Distinguish ProUtil* functions** - they are NOT official API, come from example code

## Common Headers by Task

| Task | Required Headers |
|------|------------------|
| Feature creation | ProFeature.h, ProElement.h, ProElemId.h, ProFeatType.h, ProFeatForm.h |
| Hole features | ProHole.h |
| Rounds/Chamfers | ProRound.h, ProChamfer.h, ProCrvcollection.h |
| Datum features | ProDtmPln.h, ProDtmAxis.h, ProDtmPnt.h, ProDtmCsys.h |
| Extrusions | ProExtrude.h, ProStdSection.h, ProSection.h |
| Selections | ProSelection.h, ProSelbuffer.h |
| Parameters | ProParameter.h, ProParamval.h |
| Materials | ProMaterial.h, ProMdlUnits.h |
| Layers | ProLayer.h |
| Relations | ProRelSet.h |
| Menus | ProMenu.h, ProMenuBar.h |
| Dialogs | ProUIDialog.h, ProUI*.h |
