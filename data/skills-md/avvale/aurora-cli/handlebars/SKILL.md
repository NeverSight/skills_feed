---
name: handlebars
description: >
  Deep knowledge for creating and modifying Handlebars templates (.hbs files).
  Trigger: When user needs to create/modify .hbs templates, add helpers, work with template syntax, or understand Handlebars patterns.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "handlebars, hbs, templates, helpers, partials, template syntax"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Task
---

## When to Use

Use this skill when:
- Creating or modifying `.hbs` template files
- Adding new Handlebars helpers or partials
- Debugging template rendering issues
- Understanding existing template patterns in Aurora CLI
- Working with dynamic code generation

---

## Critical Patterns

### Aurora CLI Template Engine Setup

The template engine is configured in `src/@cliter/utils/template-engine.ts`:
- Uses `handlebars` library with `handlebars-helpers` addon (189+ built-in helpers)
- Custom helpers are registered in `src/@cliter/handlebars/helpers/`
- Partials are registered in `src/@cliter/handlebars/partials/`
- Templates are in `src/templates/` (back/, front/, pipeline/)

**Important**: Aurora CLI includes ALL helpers from the `handlebars-helpers` package automatically. These 189+ helpers are available in every template without any additional configuration.

### Helper Registration Pattern

```typescript
// src/@cliter/handlebars/helpers/my-helper.ts
import * as handlebars from 'handlebars';

handlebars.registerHelper('myHelper', function(param1: string, param2: any, options)
{
    // options.data.root contains all template data
    // options.fn(this) executes block content
    // options.inverse(this) executes else block
    return result;
});
```

### Partial Registration Pattern

```typescript
// src/@cliter/handlebars/partials/my-partial.ts
import * as handlebars from 'handlebars';

handlebars.registerPartial('myPartial', `
{{#each items}}
    {{ this.name }}
{{/each}}
`);
```

---

## Handlebars Syntax Guide

### Basic Expressions

```handlebars
{{! Comment - not rendered }}
{{ variable }}                    {{! Simple output }}
{{{ rawHtml }}}                   {{! Unescaped HTML }}
{{ helper param1 param2 }}        {{! Helper call }}
{{ object.property }}             {{! Property access }}
{{ ../parentContext }}            {{! Parent context access }}
```

### Whitespace Control

```handlebars
{{~expression}}     {{! Trim whitespace before }}
{{expression~}}     {{! Trim whitespace after }}
{{~expression~}}    {{! Trim both sides }}
```

### Block Helpers

```handlebars
{{#if condition}}
    content if true
{{else}}
    content if false
{{/if}}

{{#each array}}
    {{@index}} - {{@first}} - {{@last}} - {{this}}
{{/each}}

{{#unless condition}}
    content if false
{{/unless}}

{{#with object}}
    {{property}}  {{! Access object.property }}
{{/with}}
```

### Custom Block Helpers (Aurora CLI)

```handlebars
{{#loops 10}}
    {{@index}} {{@first}} {{@last}}
{{/loops}}

{{#eq value1 value2}}
    content if equal
{{/eq}}

{{#unlessEq value1 value2}}
    content if not equal
{{/unlessEq}}
```

---

## Aurora CLI Helper Categories

### String Transformation Helpers

| Helper | Description | Example |
|--------|-------------|---------|
| `toCamelCase` | Convert to camelCase | `{{ toCamelCase "my_name" }}` → `myName` |
| `toPascalCase` | Convert to PascalCase | `{{ toPascalCase "my_name" }}` → `MyName` |
| `toKebabCase` | Convert to kebab-case | `{{ toKebabCase "myName" }}` → `my-name` |
| `toSnakeCase` | Convert to snake_case | `{{ toSnakeCase "myName" }}` → `my_name` |
| `sumStrings` | Concatenate strings | `{{ sumStrings "Hello" " " "World" }}` |
| `singleLine` | Remove line breaks | `{{ singleLine multiLineText }}` |

### Variable Management Helpers

```handlebars
{{! Set a variable in root context }}
{{ setVar 'myVar' 'value' }}
{{ setVar 'myVar' (someHelper param) }}

{{! Use the variable }}
{{ myVar }}
```

### Array/Object Helpers

```handlebars
{{! Create an array }}
{{ setVar 'items' (array 'item1' 'item2' 'item3') }}

{{! Create an object }}
{{ setVar 'obj' (object key1='value1' key2='value2') }}

{{! Push to array }}
{{ push myArray (object name='newItem') }}

{{! Check if has items }}
{{#if (hasItems myArray)}}
    has items
{{/if}}
```

### Conditional Helpers

```handlebars
{{! Ternary operator }}
{{ ternary condition 'trueValue' 'falseValue' }}

{{! Check if undefined }}
{{#if (isUndefined variable)}}
    is undefined
{{/if}}

{{! Not in array }}
{{#if (notInArray item array)}}
    not in array
{{/if}}
```

### Property Filter Helpers

Most property helpers filter `schema.aggregateProperties`:

```handlebars
{{! Get properties without timestamps }}
{{#each (getWithoutTimestampsProperties schema.aggregateProperties)}}
    {{ name }}
{{/each}}

{{! Get enum properties }}
{{#each (getEnumProperties schema.aggregateProperties)}}
    {{ name }}: {{ type }}
{{/each}}

{{! Get relationship properties }}
{{#each (getWithRelationshipOneToOneProperties schema.aggregateProperties)}}
    {{ relationship.aggregateName }}
{{/each}}
```

### Import Manager Helper

```handlebars
{{! Initialize imports array }}
{{
    setVar 'importsArray' (
        array
            (object items=(array 'Injectable') path='@nestjs/common')
            (object items='MyClass' path='./my-class')
    )
~}}

{{! Add more imports dynamically }}
{{
    push importsArray
        (object items='AnotherClass' path='./another')
~}}

{{! Render all imports }}
{{{ importManager (object imports=importsArray) }}}
```

### ID Generation Helpers

```handlebars
{{ uuid 'fieldName' }}           {{! Generate deterministic UUID }}
{{ nanoid 'fieldName' }}         {{! Generate NanoID }}
{{ randomIntegerDigits 5 }}      {{! Random integer with N digits }}
{{ randomDecimalDigits 2 3 }}    {{! Random decimal (int.dec) }}
```

---

## Handlebars-Helpers Package (Built-in)

Aurora CLI includes all 189+ helpers from the `handlebars-helpers` package. These are available automatically in all templates.

### String Helpers (36 helpers)

```handlebars
{{ append "hello" " world" }}        {{! "hello world" }}
{{ camelcase "foo bar" }}            {{! "fooBar" }}
{{ capitalize "hello" }}             {{! "Hello" }}
{{ capitalizeAll "hello world" }}    {{! "Hello World" }}
{{ dashcase "fooBar" }}              {{! "foo-bar" }}
{{ dotcase "fooBar" }}               {{! "foo.bar" }}
{{ ellipsis "long text..." 10 }}     {{! "long te..." }}
{{ hyphenate "foo bar" }}            {{! "foo-bar" }}
{{ lowercase "HELLO" }}              {{! "hello" }}
{{ pascalcase "foo bar" }}           {{! "FooBar" }}
{{ pathcase "fooBar" }}              {{! "foo/bar" }}
{{ prepend "world" "hello " }}       {{! "hello world" }}
{{ remove "foobar" "bar" }}          {{! "foo" }}
{{ replace "foobar" "bar" "baz" }}   {{! "foobaz" }}
{{ reverse "abc" }}                  {{! "cba" }}
{{ sentence "hello. world" }}        {{! "Hello. World" }}
{{ snakecase "fooBar" }}             {{! "foo_bar" }}
{{ split "a,b,c" "," }}              {{! ["a","b","c"] }}
{{ startsWith "hello" "he" }}        {{! true }}
{{ titleize "hello world" }}         {{! "Hello World" }}
{{ trim "  hello  " }}               {{! "hello" }}
{{ truncate "long text" 5 }}         {{! "long..." }}
{{ truncateWords "a b c d" 2 }}      {{! "a b..." }}
{{ uppercase "hello" }}              {{! "HELLO" }}
{{ center "text" 10 }}               {{! Centers with spaces }}
{{#isString value}}is string{{/isString}}
```

### Array Helpers (28 helpers)

```handlebars
{{ after myArray 2 }}                {{! Items after index 2 }}
{{ arrayify value }}                 {{! Converts to array }}
{{ before myArray 3 }}               {{! First 3 items }}
{{ first myArray }}                  {{! First item }}
{{ first myArray 3 }}                {{! First 3 items }}
{{ last myArray }}                   {{! Last item }}
{{ last myArray 2 }}                 {{! Last 2 items }}
{{ length myArray }}                 {{! Array length }}
{{ join myArray ", " }}              {{! "a, b, c" }}
{{ reverse myArray }}                {{! Reversed array }}
{{ sort myArray }}                   {{! Sorted array }}
{{ sortBy myArray "name" }}          {{! Sort by property }}
{{ unique myArray }}                 {{! Remove duplicates }}
{{ itemAt myArray 2 }}               {{! Item at index 2 }}
{{ pluck users "name" }}             {{! Extract "name" from objects }}
{{#inArray "a" myArray}}found{{/inArray}}
{{#isArray value}}is array{{/isArray}}
{{#equalsLength myArray 5}}has 5{{/equalsLength}}

{{#forEach myArray}}
  {{@index}} {{@first}} {{@last}} {{this}}
{{/forEach}}

{{#eachIndex myArray}}
  {{item}} at {{index}}
{{/eachIndex}}

{{#filter myArray}}{{/filter}}
{{#map myArray}}{{/map}}
{{#some myArray}}{{/some}}
{{#withFirst myArray}}{{this}}{{/withFirst}}
{{#withLast myArray 2}}{{this}}{{/withLast}}
{{#withGroup myArray 3}}{{this}}{{/withGroup}}
{{#withSort myArray "name"}}{{this}}{{/withSort}}
```

### Comparison Helpers (24 helpers)

```handlebars
{{#and value1 value2}}both truthy{{/and}}
{{#or value1 value2}}at least one truthy{{/or}}
{{#not value}}falsey{{/not}}
{{#eq a b}}equal{{/eq}}
{{#is a b}}loosely equal{{/is}}
{{#isnt a b}}not equal{{/isnt}}
{{#gt a b}}greater than{{/gt}}
{{#gte a b}}greater or equal{{/gte}}
{{#lt a b}}less than{{/lt}}
{{#lte a b}}less or equal{{/lte}}
{{#compare a ">" b}}comparison{{/compare}}
{{#contains collection value}}found{{/contains}}
{{#has value pattern}}matches{{/has}}
{{#ifEven num}}even{{/ifEven}}
{{#ifOdd num}}odd{{/ifOdd}}
{{#ifNth 10 2}}every 2nd{{/ifNth}}
{{#isTruthy value}}truthy{{/isTruthy}}
{{#isFalsey value}}falsey{{/isFalsey}}
{{#neither a b}}both falsey{{/neither}}
{{ default value "fallback" }}       {{! Returns fallback if undefined }}
{{#unlessEq a b}}not equal{{/unlessEq}}
{{#unlessGt a b}}not greater{{/unlessGt}}
{{#unlessLt a b}}not less{{/unlessLt}}
```

### Math Helpers (16 helpers)

```handlebars
{{ abs -5 }}                         {{! 5 }}
{{ add 1 2 }}                        {{! 3 }}
{{ subtract 5 2 }}                   {{! 3 }}
{{ multiply 3 4 }}                   {{! 12 }}
{{ divide 10 2 }}                    {{! 5 }}
{{ modulo 10 3 }}                    {{! 1 }}
{{ ceil 4.3 }}                       {{! 5 }}
{{ floor 4.7 }}                      {{! 4 }}
{{ round 4.5 }}                      {{! 5 }}
{{ avg myNumbers }}                  {{! Average of array }}
{{ sum myNumbers }}                  {{! Sum of array }}
{{ random 1 100 }}                   {{! Random between 1-100 }}
{{ plus 1 2 }}                       {{! Alias for add }}
{{ minus 5 2 }}                      {{! Alias for subtract }}
{{ times 3 4 }}                      {{! Alias for multiply }}
{{ remainder 10 3 }}                 {{! Alias for modulo }}
```

### Number Helpers (9 helpers)

```handlebars
{{ bytes 1024 }}                     {{! "1 KB" }}
{{ addCommas 1000000 }}              {{! "1,000,000" }}
{{ phoneNumber "1234567890" }}       {{! "(123) 456-7890" }}
{{ toAbbr 1000000 }}                 {{! "1m" }}
{{ toExponential 12345 2 }}          {{! "1.23e+4" }}
{{ toFixed 3.14159 2 }}              {{! "3.14" }}
{{ toFloat "3.14" }}                 {{! 3.14 }}
{{ toInt "42" }}                     {{! 42 }}
{{ toPrecision 3.14159 3 }}          {{! "3.14" }}
```

### Object Helpers (14 helpers)

```handlebars
{{ get object "nested.path" }}       {{! Get nested value }}
{{ getObject object "key" }}         {{! Get key-value pair }}
{{ JSONstringify object }}           {{! JSON string }}
{{ JSONparse jsonString }}           {{! Parse JSON }}
{{ stringify value }}                {{! String representation }}
{{#hasOwn object "key"}}has key{{/hasOwn}}
{{#isObject value}}is object{{/isObject}}
{{#forIn object}}{{@key}}: {{this}}{{/forIn}}
{{#forOwn object}}{{@key}}: {{this}}{{/forOwn}}
{{#extend obj1 obj2}}{{/extend}}
{{#merge obj1 obj2}}{{/merge}}
{{#pick context "a" "b"}}{{/pick}}
{{ toPath "a" "b" "c" }}             {{! "a.b.c" }}
```

### URL Helpers (9 helpers)

```handlebars
{{ encodeURI "hello world" }}        {{! "hello%20world" }}
{{ decodeURI "hello%20world" }}      {{! "hello world" }}
{{ escape value }}                   {{! URL escaped }}
{{ urlResolve base path }}           {{! Resolved URL }}
{{ urlParse url }}                   {{! Parsed URL object }}
{{ stripQuerystring url }}           {{! URL without query }}
{{ stripProtocol url }}              {{! URL without protocol }}
{{ url_encode value }}               {{! Alias for encodeURI }}
{{ url_decode value }}               {{! Alias for decodeURI }}
```

### Date Helpers (3 helpers)

```handlebars
{{ year }}                           {{! Current year }}
{{ date }}                           {{! Current date }}
{{ moment date "YYYY-MM-DD" }}       {{! Format with moment.js }}
```

### Path Helpers (8 helpers)

```handlebars
{{ basename "/a/b/file.txt" }}       {{! "file.txt" }}
{{ dirname "/a/b/file.txt" }}        {{! "/a/b" }}
{{ extname "file.txt" }}             {{! ".txt" }}
{{ stem "file.txt" }}                {{! "file" }}
{{ resolve "a" "b" "c" }}            {{! Absolute path }}
{{ relative "/a/b" "/a/c" }}         {{! "../c" }}
{{ segments path 0 2 }}              {{! Path segments range }}
{{ absolute path 1 }}                {{! Directory segment }}
```

### Collection Helpers (2 helpers)

```handlebars
{{#isEmpty collection}}empty{{/isEmpty}}
{{#iterate collection}}{{this}}{{/iterate}}
```

### Inflection Helpers (2 helpers)

```handlebars
{{ inflect count "item" "items" }}   {{! Pluralization }}
{{ ordinalize 1 }}                   {{! "1st" }}
{{ ordinalize 22 }}                  {{! "22nd" }}
```

### Regex Helpers (2 helpers)

```handlebars
{{ toRegex "pattern" "gi" }}         {{! Creates RegExp }}
{{#test "hello" "ell"}}matches{{/test}}
```

### HTML Helpers (7 helpers)

```handlebars
{{ sanitize "<b>text</b>" }}         {{! "text" }}
{{{ ul myArray }}}                   {{! <ul><li>...</li></ul> }}
{{{ ol myArray }}}                   {{! <ol><li>...</li></ol> }}
{{{ css "styles.css" }}}             {{! <link rel="stylesheet"...> }}
{{{ js "script.js" }}}               {{! <script src="..."></script> }}
{{ attr attributes }}                {{! Stringifies HTML attributes }}
{{ thumbnailImage image }}           {{! Figure with thumbnail }}
```

### Markdown Helpers (2 helpers)

```handlebars
{{{ markdown "**bold**" }}}          {{! <strong>bold</strong> }}
{{{ md "./file.md" }}}               {{! Rendered markdown file }}
```

### Misc Helpers (5 helpers)

```handlebars
{{ typeOf value }}                   {{! "string", "array", etc. }}
{{ noop }}                           {{! Renders block without processing }}
{{ option "key" }}                   {{! Get value from options }}
{{#withHash key="value"}}{{key}}{{/withHash}}
{{ frame }}                          {{! Frame-related helper }}
```

### Logging Helpers (11 helpers)

```handlebars
{{ log "message" }}                  {{! Console log }}
{{ info "info message" }}            {{! Info level }}
{{ warn "warning" }}                 {{! Warning level }}
{{ error "error" }}                  {{! Error level }}
{{ success "done" }}                 {{! Success message }}
{{ ok "ok" }}                        {{! Ok message }}
{{ danger "danger" }}                {{! Danger message }}
{{ bold "text" }}                    {{! Bold formatting }}
{{ _debug value }}                   {{! Debug output }}
{{ _inspect value }}                 {{! Inspect value }}
```

> **Full Reference**: See [references/handlebars-helpers-reference.md](references/handlebars-helpers-reference.md) for complete documentation.

---

## Decision Tree

```
Need string transformation? → toCamelCase, toPascalCase, toKebabCase, toSnakeCase (Aurora)
                           → camelcase, pascalcase, snakecase, dashcase (handlebars-helpers)
Need to store temporary data? → setVar
Need to build arrays/objects? → array, object, push
Need conditional rendering? → if, unless, eq, unlessEq, ternary, and, or, not, compare
Need to iterate? → each, loops, forEach, eachIndex, forIn, forOwn
Need to filter properties? → get*Properties helpers (Aurora custom)
Need to manage imports? → importManager with importsArray
Need unique IDs? → uuid, nanoid
Need math operations? → add, subtract, multiply, divide, ceil, floor, round
Need string manipulation? → trim, split, replace, truncate, append, prepend
Need array operations? → first, last, sort, unique, filter, map, join
Need object access? → get, hasOwn, forIn, forOwn
Need URL handling? → encodeURI, decodeURI, urlParse, stripQuerystring
Need path operations? → basename, dirname, extname, resolve
```

---

## Code Examples

### Example 1: Creating a New Helper

```typescript
// src/@cliter/handlebars/helpers/is-required-property.ts
import * as handlebars from 'handlebars';
import { Property } from '../../types';

handlebars.registerHelper('isRequiredProperty', function(
    property: Property,
)
{
    return !property.nullable && !property.hasOwnProperty('defaultValue');
});
```

### Example 2: Using Multiple Helpers in Template

```handlebars
{{! Generate TypeScript interface }}
export interface {{ toPascalCase schema.moduleName }}Input
{
{{#each (getWithoutTimestampsProperties schema.aggregateProperties)}}
    {{ toCamelCase name }}{{#if nullable}}?{{/if}}: {{ getDtoTypeProperty this ../config }};
{{/each}}
}
```

### Example 3: Complex Import Management

```handlebars
{{
    setVar 'importsArray' (
        array
            (object items=(array 'Injectable' 'Inject') path='@nestjs/common')
    )
~}}
{{#each (getEnumProperties schema.aggregateProperties)}}
{{
    push ../importsArray
        (object items=(toPascalCase name) path='@api/graphql')
~}}
{{/each}}
{{{ importManager (object imports=importsArray) }}}
```

### Example 4: Conditional Blocks with Context

```handlebars
{{#each (getDtoProperties schema.aggregateProperties)}}
{{#if (isAllowProperty ../schema.moduleName this)}}
    {{#eq type ../propertyType.ENUM}}
        // Handle enum type
        {{ toPascalCase ../schema.moduleName }}{{ toPascalCase name }}
    {{else}}
        // Handle other types
        {{ getDtoTypeProperty this ../config }}
    {{/eq}}
{{/if}}
{{/each}}
```

---

## Commands

```bash
# Build after adding helpers
yarn build

# Find all helpers
ls src/@cliter/handlebars/helpers/

# Find helper usage in templates
grep -r "helperName" src/templates/

# Test template rendering
yarn test
```

---

## Common Mistakes to Avoid

1. **Missing whitespace control**: Use `~` to trim unwanted whitespace
   ```handlebars
   {{! Bad - adds extra lines }}
   {{#if condition}}
   content
   {{/if}}

   {{! Good - clean output }}
   {{~#if condition}}
   content
   {{~/if}}
   ```

2. **Wrong context access**: Use `../` to access parent context in loops
   ```handlebars
   {{#each items}}
       {{ ../schema.moduleName }}  {{! Access parent, not current item }}
   {{/each}}
   ```

3. **Forgetting to register helper**: Add import in `src/@cliter/handlebars/helpers/index.ts`

4. **Using `{{` instead of `{{{`**: For HTML/code output, use triple braces to avoid escaping

---

## Resources

- **Templates**: See [assets/](assets/) for helper and partial templates
- **Aurora Helpers**: See [references/helpers-reference.md](references/helpers-reference.md) for Aurora CLI custom helpers
- **Built-in Helpers**: See [references/handlebars-helpers-reference.md](references/handlebars-helpers-reference.md) for handlebars-helpers package
- **GitHub**: https://github.com/helpers/handlebars-helpers
