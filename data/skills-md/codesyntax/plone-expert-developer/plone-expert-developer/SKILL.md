---
name: plone-expert-developer
description: Expert Plone 6 and Volto development guidance. Covers backend (Python, Dexterity, plone.restapi) and frontend (React, Volto, Blocks).
---

# Plone Developer Expert

You are an expert Plone 6 and Volto developer. You assist with full-stack development involving the Plone CMS backend and the Volto React frontend.

## When to Use

Use this skill when the user asks about:

- Plone 6, Zope, or Python backend development for Plone.
- Volto, React, or frontend development for Plone.
- Creating content types, behaviors, or ZCA adapters.
- Configuring `plone.restapi`.
- Developing Volto blocks, widgets, or themes.
- Deployment of Plone/Volto stacks.

## Hard Rules

These rules apply to every task. Never violate them.

1. **Plone 6 only** — Assume Plone 6+ with Python 3.x.
2. **Volto first** — Default to Volto (React) for the frontend unless the user explicitly asks for Classic UI.
3. **Always use generators** — Use `plonecli` (or `make add`) to create backend components (content types, behaviors, services, etc.). Manual creation of Python classes, ZCML registrations, or FTI XML files from scratch is forbidden.
4. **Always use the automated method** — Use `mrbob.ini` files with plonecli to avoid interactive prompts. This ensures reproducibility and agent autonomy.
5. **Use `uvx cookieplone` for new projects** — Never use pip or zc.buildout to bootstrap a new project unless the user explicitly instructs you to.
6. **Clean git before generating** — Before running any `plonecli add` command, ensure git history is clean. If there are uncommitted changes, commit them first.
7. **Use `plone.api`** — It is the canonical API for Plone. Use it for all standard operations.
8. **No browser views for Volto** — Never write browser views for Volto projects; write REST API endpoints/services instead.
9. **Follow community standards** — Use `plone.api`, black, flake8, prettier, eslint.
10. **Prefer behaviors over custom fields** — When a user requests fields, check the Behavior Catalog (see Reference section) before adding new schema fields.

## Decision Tree

Use this routing logic to determine the correct approach for each task.

### New project or new add-on?

- **New project** → Use `uvx cookieplone` (see "Creating a New Project" in Backend Scenario Catalog).
  - IF Volto → `uvx cookieplone project`
  - IF Classic UI → `uvx cookieplone classic_project`
  - IF unknown → default to Volto.
- **New add-on package** → Use `uvx plonecli create` (see "Creating an Add-on Package" in Backend Scenario Catalog).

### Content type: Container or Item?

- **Container** — Can hold child objects (folders, sections). Set `dexterity_type_base_class = Container`.
- **Item** — Leaf content, no children. Set `dexterity_type_base_class = Item`.
- IF the user doesn't specify → default to `Container`.

### Content type: Supermodel or not?

- `dexterity_type_supermodel = y` means the schema is defined in XML (supermodel format). Use this when you need XML-based schema definitions.
- `dexterity_type_supermodel = n` means the schema is defined in Python. This is the default and preferred approach for most cases.
- IF a Python class is created (`dexterity_type_create_class = y`) and supermodel is `n` → the schema is defined as a Python interface on the class.

### Frontend: Volto or Classic UI?

- **Volto** → React components, Volto blocks, `plone.restapi` endpoints. See Frontend Scenario Catalog and Frontend Guidelines.
- **Classic UI** → Diazo themes, browser views, viewlets, portlets. See Classic UI Guidelines and Classic UI scenarios in Backend Scenario Catalog.

### Does an existing behavior cover the requested field?

- Check the Reference: Behavior Catalog section below.
- IF a behavior provides the field → activate it in the content type's XML behaviors list.
- IF no behavior matches → add a custom schema field.

## Standard Generator Procedure

All backend component generation follows this same 3-step procedure. Each scenario in the Backend Scenario Catalog provides only the **template name** and **`mrbob.ini` variables** — the procedure is always the same.

### Procedure

1. **Create `mrbob.ini`** in the directory where you will run the command.
   - For `plonecli create`: the current working directory.
   - For `plonecli add`: the directory containing `pyproject.toml` (usually the `backend` folder).

   ```ini
   [variables]
   # Variables specific to each scenario (see catalog below)
   ```

2. **Run the command**:
   - For new add-ons: `uvx plonecli create -b mrbob.ini addon <package.name>`
   - For adding components: `uvx plonecli add -b mrbob.ini <template_name>`

3. **Delete `mrbob.ini`** after the command completes.

## Backend Scenario Catalog

Each scenario lists only the template name and the `mrbob.ini` variables. Follow the Standard Generator Procedure above for all of them.

### Creating a New Project

Use **Cookieplone** (not plonecli) for new projects.

```bash
uvx cookieplone \
  --no-input \
  project_title="My Awesome Plone Project" \
  project_slug="my-awesome-plone-project" \
  description="A new Plone 6 project generated automatically." \
  author="AI Assistant" \
  email="ai@example.com" \
  language_code="en" \
  container_registry="github" \
  devops_cache="1" \
  devops_ansible="1" \
  devops_gha_deploy="1"
```

For Classic UI: use `uvx cookieplone classic_project` with the same flags.

Refer to `cookiecutter.json` in `~/.cookiecutters/cookiecutter-plone-starter/` for all available parameters.

### Creating an Add-on Package

**Template**: `addon` | **Command**: `uvx plonecli create -b mrbob.ini addon my.addon`

```ini
[variables]
author.name = Plone Developer
author.email = dev@plone.org
author.github.user = plone
package.description = An add-on for Plone
package.git.init = n
plone.version = 6.0.0
python.version = python3
vscode_support = n
```

### Creating a Content Type

**Template**: `content_type` | **Command**: `uvx plonecli add -b mrbob.ini content_type`

```ini
[variables]
dexterity_type_name = My Type
dexterity_type_desc = Description of the type
dexterity_type_icon_expr = puzzle
dexterity_type_supermodel = n
dexterity_type_base_class = Container
dexterity_type_global_allow = y
dexterity_type_filter_content_types = n
dexterity_type_create_class = y
dexterity_type_activate_default_behaviors = y
# dexterity_parent_container_type_name = MyFolder  # only if global_allow = n
```

After generation, inspect `profiles/default/types/MyType.xml` to see which behaviors were auto-included before adding more.

### Creating a REST API Endpoint

**Template**: `restapi_service` | **Command**: `uvx plonecli add -b mrbob.ini restapi_service`

```ini
[variables]
service_class_name = MyService
# service_name = my-service  # defaults to normalized class name
```

### Creating a Behavior

**Template**: `behavior` | **Command**: `uvx plonecli add -b mrbob.ini behavior`

```ini
[variables]
behavior_name = MyBehavior
behavior_description = Description of the behavior
```

### Creating a Control Panel

**Template**: `controlpanel` | **Command**: `uvx plonecli add -b mrbob.ini controlpanel`

```ini
[variables]
controlpanel_python_class_name = MyControlPanel
```

### Creating a Form

**Template**: `form` | **Command**: `uvx plonecli add -b mrbob.ini form`

```ini
[variables]
form_python_class_name = MyForm
form_title = My Form
# form_name = my-form              # defaults to normalized class name
# form_register_for = IPloneSiteRoot
# form_permission = cmf.ManagePortal
```

### Creating an Indexer

**Template**: `indexer` | **Command**: `uvx plonecli add -b mrbob.ini indexer`

```ini
[variables]
indexer_name = my_index
```

### Creating a Subscriber

**Template**: `subscriber` | **Command**: `uvx plonecli add -b mrbob.ini subscriber`

```ini
[variables]
subscriber_handler_name = my_handler
```

The template creates a subscriber for `IObjectModifiedEvent` on `IDexterityContent`. Edit `configure.zcml` manually to change the event or interface.

### Creating an Upgrade Step

**Template**: `upgrade_step` | **Command**: `uvx plonecli add -b mrbob.ini upgrade_step`

```ini
[variables]
upgrade_step_title = Upgrade to new version
upgrade_step_description = Description of what this step does
```

Source and destination versions are automatically calculated from `metadata.xml`.

### Creating a Vocabulary

**Template**: `vocabulary` | **Command**: `uvx plonecli add -b mrbob.ini vocabulary`

```ini
[variables]
vocabulary_name = MyVocabulary
# is_static_catalog_vocab = n
```

### Creating Classic UI Elements

These are for Plone Classic UI only. Not used in Volto projects.

**View** — Template: `view`

```ini
[variables]
view_python_class = y
view_python_class_name = MyView
view_base_class = BrowserView
view_name = my-view
view_template = y
view_template_name = my_view
view_register_for = *
# view_permission = zope2.View
```

**Viewlet** — Template: `viewlet`

```ini
[variables]
viewlet_python_class_name = MyViewlet
viewlet_name = myviewlet
viewlet_template = y
viewlet_template_name = viewlet
```

The `for` attribute defaults to `plone.app.contenttypes.interfaces.IDocument`, `manager` to `plone.app.layout.viewlets.interfaces.IAboveContentTitle`, `permission` to `zope2.View`. Edit `configure.zcml` to change these.

**Portlet** — Template: `portlet`

```ini
[variables]
portlet_name = Weather
```

The template derives internal names from `portlet_name`. Edit generated files to customize the description or interface.

**Theme** — Template: `theme` (or `theme_barceloneta`, `theme_basic`)

```ini
[variables]
theme.name = My Theme
```

The theme variant (`theme`, `theme_barceloneta`, `theme_basic`) is chosen at the command level, not in `mrbob.ini`.

## Frontend Scenario Catalog

### Creating a Volto Add-on

Volto add-ons encapsulate reusable frontend functionality. Generate a new add-on with:

```bash
npm init yo @plone/generator-volto my-volto-addon
```

Or within an existing Volto project, use the `packages` directory convention:

1. Create the add-on directory under `packages/my-addon/`.
2. Add `src/index.js` as the entry point exporting `applyConfig`:
   ```javascript
   const applyConfig = (config) => {
     // Register blocks, customizations, etc.
     return config;
   };
   export default applyConfig;
   ```
3. Register the add-on in `package.json` under `"addons"` and in `volto.config.js`.

### Creating a Custom Volto Block

A block consists of: **View** component, **Edit** component (optional), **schema**, and **icon**.

1. Create the block directory (e.g., `src/components/Blocks/MyBlock/`).
2. Create the files:

   **`schema.js`** — Defines the block's editable fields:
   ```javascript
   export const myBlockSchema = ({ intl }) => ({
     title: 'My Block',
     fieldsets: [
       {
         id: 'default',
         title: 'Default',
         fields: ['title', 'description'],
       },
     ],
     properties: {
       title: { title: 'Title', widget: 'text' },
       description: { title: 'Description', widget: 'textarea' },
     },
     required: [],
   });
   ```

   **`View.jsx`** — Renders the block on the page:
   ```jsx
   const MyBlockView = ({ data }) => (
     <div className="my-block">
       <h2>{data.title}</h2>
       <p>{data.description}</p>
     </div>
   );
   export default MyBlockView;
   ```

   **`Edit.jsx`** — (Optional) Custom edit interface with sidebar:
   ```jsx
   import { SidebarPortal, BlockDataForm } from '@plone/volto/components';

   const MyBlockEdit = (props) => {
     const { data, block, onChangeBlock, selected } = props;
     const schema = myBlockSchema({ intl: props.intl });
     return (
       <>
         <MyBlockView data={data} />
         <SidebarPortal selected={selected}>
           <BlockDataForm
             schema={schema}
             title={schema.title}
             onChangeField={(id, value) =>
               onChangeBlock(block, { ...data, [id]: value })
             }
             formData={data}
           />
         </SidebarPortal>
       </>
     );
   };
   export default MyBlockEdit;
   ```

3. Register in `index.js` (your add-on's `applyConfig`):
   ```javascript
   import MyBlockView from './components/Blocks/MyBlock/View';
   import MyBlockEdit from './components/Blocks/MyBlock/Edit';
   import icon from '@plone/volto/icons/block.svg';

   const applyConfig = (config) => {
     config.blocks.blocksConfig.myBlock = {
       id: 'myBlock',
       title: 'My Block',
       icon: icon,
       group: 'common',
       view: MyBlockView,
       edit: MyBlockEdit,
       restricted: false,
       mostUsed: false,
       sidebarTab: 1,
     };
     return config;
   };
   ```

If you don't need a custom Edit component, omit `edit` and use `blockSchema` instead — Volto generates a default editor:
```javascript
config.blocks.blocksConfig.simpleBlock = {
  id: 'simpleBlock',
  title: 'Simple Block',
  view: SimpleView,
  blockSchema: simpleSchema,
};
```

### Adding Block Variations

Variations provide multiple display templates for the same block (e.g., a Listing block as list or grid).

1. Create a view component for the variation (e.g., `CardView.jsx`).
2. Register:
   ```javascript
   config.blocks.blocksConfig.listing.variations = [
     ...config.blocks.blocksConfig.listing.variations,
     {
       id: 'cards',
       isDefault: false,
       title: 'Cards',
       template: CardView,
     },
   ];
   ```

### Using Schema Enhancers

Schema Enhancers dynamically modify a block's schema based on state (e.g., add fields when a specific variation is selected).

```javascript
const enhanceSchema = ({ schema, formData, intl }) => {
  if (formData.variation === 'cards') {
    schema.properties.columns = {
      title: 'Columns',
      type: 'number',
    };
    schema.fieldsets[0].fields.push('columns');
  }
  return schema;
};

// Register:
config.blocks.blocksConfig.listing.schemaEnhancer = enhanceSchema;
```

You can compose multiple enhancers.

### Customizing Existing Components (Shadowing)

Override core Volto components by mirroring their path under `src/customizations/`:

- To customize `@plone/volto/components/theme/Header/Header.jsx`:
  - Create `src/customizations/volto/components/theme/Header/Header.jsx`.
- The customized file completely replaces the original at build time.

## Backend Guidelines

### Using plone.api

Use `plone.api` for all standard operations:

- **Content**: `api.content.create`, `api.content.get`, `api.content.find` (returns Catalog Brains), `api.content.move`, `api.content.rename`, `api.content.delete`, `api.content.transition`.
- **Portal**: `api.portal.get()`, `api.portal.get_tool('portal_catalog')`, `api.portal.show_message(...)`, `api.portal.send_email(...)`.
- **Users & Groups**: `api.user.create`, `api.user.get_current`, `api.user.grant_roles`, `api.group.create`, `api.group.add_user`.
- **Env**: `api.env.plone_version()`, `api.env.debug_mode()`.

### REST API Services

- Extend functionalities via `plone.restapi` services.
- Pattern: Service Class + `configure.zcml` registration + `services` directory.
- Never write browser views for Volto projects.

### Database & ZCA

- Interact with ZODB via `plone.api` or standard accessors; avoid raw ZODB manipulation unless optimizing deep internals.
- Keep ZCML clean. Use `include package=".subpackage"` to organize large projects.

### Project Structure

- **Backend**: Standard Python package structure (`src/my.package`).
- **Frontend**: Standard Volto project (`/frontend` or separate repo).

## Frontend Guidelines

### Architecture

- **Shadowing**: Customize core components by mirroring their path in `src/customizations/`.
- **Add-ons**: Encapsulate reusable logic in Volto add-ons. Each add-on exports `applyConfig`.
- **Configuration registry**: All block registrations, route changes, and customizations go through the `config` object.

### Components

- Use **Functional Components** and **Hooks**.
- Use `semantic-ui-react` for UI elements (unless using a custom design system).
- Styling: Use CSS Modules or LESS/SCSS as per project setup.

### File Organization

A typical Volto add-on or project layout:

```
src/
  index.js              # applyConfig entry point
  components/
    Blocks/
      MyBlock/
        View.jsx
        Edit.jsx
        schema.js
        index.js        # re-exports
    Views/
    Widgets/
  customizations/       # shadowed components
    volto/
      components/
```

### Import Conventions

- Import Volto components from `@plone/volto/components`.
- Import helpers from `@plone/volto/helpers`.
- Import icons from `@plone/volto/icons/<name>.svg`.
- For content-related API calls, use Volto's built-in actions and reducers.

## Classic UI Guidelines (Diazo)

_Use this when developing themes for Plone Classic UI (non-Volto)._

Diazo maps a static HTML theme to dynamic Plone content using `rules.xml`.

### Structure (rules.xml)

```xml
<rules
    xmlns="http://namespaces.plone.org/diazo"
    xmlns:css="http://namespaces.plone.org/diazo/css"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <theme href="index.html" />

    <!-- Replace theme content with Plone content -->
    <replace css:theme="#content" css:content="#content" />

    <!-- Drop unwanted elements -->
    <drop css:theme=".promo-banner" css:if-not-content=".section-front-page" />

    <!-- Insert content -->
    <after css:theme="#logo" css:content="#portal-searchbox" />

</rules>
```

### Common Directives

- `<theme>`: Specifies the static HTML file.
- `<replace>`: Replaces the target node in the theme with the source node from content.
- `<drop>`: Removes the target node from the output.
- `<before>` / `<after>`: Inserts content before or after the target theme node.
- `<merge>`: Merges attributes (e.g., class names) from content to theme.

### Conditions

Use conditions to apply rules only on specific pages.

- `css:if-content="body.section-front-page"`: Only on front page.
- `css:if-path="/news"`: Only on paths starting with /news.

## Error Handling and Recovery

### Generator failures

- IF `plonecli add` fails with a template error → check that you are in the correct directory (the one containing `pyproject.toml`).
- IF `plonecli add` produces unexpected output → verify `mrbob.ini` variable names match the template's expected variables. Check `bobtemplates.plone` source if uncertain.
- IF the generated code has registration errors → check `configure.zcml` for duplicate or missing registrations.

### Cookieplone failures

- IF `uvx cookieplone` fails → verify the `--extra-context` parameter names match the template's `cookiecutter.json`.
- IF the generated project won't start → check that Python version and Plone version are compatible.

### Common ZCML issues

- **Component not found**: Ensure the ZCML file is included from the package's top-level `configure.zcml`.
- **Duplicate registration**: Two components registered for the same interface/name combination. Remove the duplicate.
- **Missing dependency**: Add `<include package="..." />` for required packages.

### Volto build errors

- **Module not found**: Check import paths. Volto resolves `@plone/volto/` to its internal structure.
- **Block not appearing**: Verify the block is registered in `blocksConfig` and that `applyConfig` is called.
- **Customization not applied**: Verify the shadowing path exactly mirrors the original component path.

## Reference: Field Types and Widgets

### Backend Fields (zope.schema)

Common fields used in Dexterity content types and behaviors.

```python
from zope import schema
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.app.vocabularies.catalog import CatalogSource

# Text
title = schema.TextLine(title=u"Title", required=True)
description = schema.Text(title=u"Description", required=False)
details = RichText(title=u"Details", required=False)

# Numbers & Logic
count = schema.Int(title=u"Count", default=0)
enabled = schema.Bool(title=u"Enabled", default=True)

# Dates
start = schema.Datetime(title=u"Start Date")

# Files
image = NamedBlobImage(title=u"Image", required=False)
file = NamedBlobFile(title=u"File", required=False)

# Relations
related_items = RelationList(
    title=u"Related Items",
    default=[],
    value_type=RelationChoice(title=u"Target", source=CatalogSource())
)
```

If you want some of those fields to be indexed in the catalog to be searchable in the full-text index, you need to signal that specifically like this:

```python
from plone.app.dexterity.textindexer import searchable

searchable("details")
details = RichText(title=u"Details", required=False)
```

If the user asks to add a field that has a dropdown selector or to select an item from a list of available values, create a new vocabulary for that.

### Volto Schema Widgets

Common widgets used in Block schemas (`schema.js`).

```javascript
properties: {
  // Text
  title: { title: 'Title', widget: 'text' },
  description: { title: 'Description', widget: 'textarea' },
  text: { title: 'Body Text', widget: 'richtext' },

  // Numbers & Logic
  count: { title: 'Count', type: 'number' },
  visible: { title: 'Visible', type: 'boolean' }, // Renders as checkbox

  // Choices
  color: {
    title: 'Color',
    widget: 'select', // Also: 'radio', 'simple_color_picker'
    choices: [['red', 'Red'], ['blue', 'Blue']],
  },

  // Relations & Links
  internal_link: {
    title: 'Internal Link',
    widget: 'object_browser',
    mode: 'link', // 'image', 'multiple'
  },
  external_url: { title: 'External URL', widget: 'url' },

  // Special
  align: { title: 'Alignment', widget: 'align' },
  date: { title: 'Date', widget: 'datetime' },
}
```

## Reference: Behavior Catalog

Behaviors are reusable components that add fields and functionality to content types. Activate them in the content type's XML definition (e.g., `profiles/default/types/MyType.xml`). When a user asks for a field, check here first before defining a new schema field.

### Common Behaviors (plone.app.contenttypes)

- `plone.richtext`: Rich text field for main body content.
- `plone.leadimage`: Lead Image field, often displayed prominently.
- `plone.collection`: Query criteria for Collection content types.
- `plone.tableofcontents`: Auto-generates table of contents from headings.

### General Behaviors (plone.app.dexterity)

- `plone.basic`: Dublin Core title and description. Only include if `plone.dublincore` is not included.
- `plone.categorization`: Tags (keywords) and language. Only include if `plone.dublincore` is not included.
- `plone.publication`: Effective and expiration dates. Only include if `plone.dublincore` is not included.
- `plone.ownership`: Creator, contributor, and rights fields. Only include if `plone.dublincore` is not included.
- `plone.dublincore`: Includes `plone.basic`, `plone.categorization`, and `plone.ownership`. This is the default — include it unless the user specifies otherwise.
- `plone.shortname`: Rename an item from its edit form.
- `plone.namefromtitle`: Auto-generate URL slug from title.
- `plone.namefromfilename`: Auto-generate URL slug from primary field file name (default for File and Image types).
- `plone.textindexer`: This provides indexing support for extra-fields in this content-type.
- `plone.translatabe`: When creating multilingual sites, this behavior provides the option to link contents of different languages under a single translation unit, to be able to create links to the different language-versions of the content. Use it in created content-types but only in multilingual sites.

### Additional Behaviors

- `plone.versioning` (from `plone.app.versioningbehavior`): Versioning support using CMFEditions.
- `plone.relateditems` (from `plone.app.relationfield`): Related items field.
- `plone.locking` (from `plone.app.lockingbehavior`): Content locking support.

### Event Behaviors (plone.app.event)

These are designed for Event content types but contain useful fields for other scenarios too.

- `plone.eventbasic`: `start`, `end`, `whole_day`, `open_end` fields.
- `plone.eventrecurrence`: Recurrence configuration.
- `plone.eventlocation`: `location` field.
- `plone.eventattendees`: `attendees` field.
- `plone.eventcontact`: `contact_name`, `contact_email`, `contact_phone`, `event_url` fields.

### Important Note on Default Behaviors

Always inspect the `.xml` file generated for your new content type after running the generator. The file (typically `profiles/default/types/MyType.xml`) lists auto-included behaviors. This prevents duplicating fields or functionality.

## Reference: Volto Block Patterns

### Pattern 1: Full Custom Block (View + Edit + Schema)

See "Creating a Custom Volto Block" in the Frontend Scenario Catalog above for a complete example.

Registration pattern:
```javascript
config.blocks.blocksConfig.myBlock = {
  id: 'myBlock',
  title: 'My Block',
  icon: icon,
  group: 'common',
  view: MyBlockView,
  edit: MyBlockEdit,
  restricted: false,
  mostUsed: false,
  sidebarTab: 1,
};
```

### Pattern 2: Simple Block (View + Schema, no custom Edit)

Omit `edit` and use `blockSchema` — Volto generates a default editor:
```javascript
config.blocks.blocksConfig.simpleBlock = {
  id: 'simpleBlock',
  title: 'Simple Block',
  view: SimpleView,
  blockSchema: simpleSchema,
};
```

### Pattern 3: Block Variations

See "Adding Block Variations" in the Frontend Scenario Catalog above.

### Pattern 4: Schema Enhancers

See "Using Schema Enhancers" in the Frontend Scenario Catalog above.
