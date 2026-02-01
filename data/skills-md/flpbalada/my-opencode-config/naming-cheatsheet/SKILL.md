---
name: naming-cheatsheet
description: Apply language-agnostic naming conventions using the A/HC/LC pattern. Use when naming variables, functions, or reviewing code for naming consistency.
---

# Naming Cheatsheet

Comprehensive guidelines for naming variables and functions in any programming language, based on the A/HC/LC pattern.

## When to Use

- Naming new variables, functions, or classes
- Reviewing code for naming consistency
- Refactoring poorly named identifiers
- Teaching or establishing team naming conventions

## Core Principles (S-I-D)

Names must be:

| Principle       | Description                                              |
| --------------- | -------------------------------------------------------- |
| **Short**       | Not take long to type and remember                       |
| **Intuitive**   | Read naturally, close to common speech                   |
| **Descriptive** | Reflect what it does/possesses in the most efficient way |

```javascript
/* Bad */
const a = 5 // "a" could mean anything
const isPaginatable = a > 10 // sounds unnatural
const shouldPaginatize = a > 10 // made-up verb

/* Good */
const postCount = 5
const hasPagination = postCount > 10
const shouldPaginate = postCount > 10
```

## The A/HC/LC Pattern

The core pattern for naming functions:

```
prefix? + action (A) + high context (HC) + low context? (LC)
```

| Name                   | Prefix   | Action (A) | High Context (HC) | Low Context (LC) |
| ---------------------- | -------- | ---------- | ----------------- | ---------------- |
| `getUser`              |          | `get`      | `User`            |                  |
| `getUserMessages`      |          | `get`      | `User`            | `Messages`       |
| `handleClickOutside`   |          | `handle`   | `Click`           | `Outside`        |
| `shouldDisplayMessage` | `should` | `Display`  | `Message`         |                  |

**Context order matters:** `shouldUpdateComponent` means *you* update the component, while `shouldComponentUpdate` means *component* updates itself.

## Actions (Verbs)

### `get`

Accesses data immediately (shorthand getter). Also used for async operations.

```javascript
function getFruitCount() {
  return this.fruits.length
}

async function getUser(id) {
  const user = await fetch(`/api/user/${id}`)
  return user
}
```

### `set`

Sets a variable declaratively, from value A to value B.

```javascript
let fruits = 0

function setFruits(nextFruits) {
  fruits = nextFruits
}
```

### `reset`

Sets a variable back to its initial value or state.

```javascript
const initialFruits = 5
let fruits = initialFruits

function resetFruits() {
  fruits = initialFruits
}
```

### `remove` vs `delete`

| Action     | Use Case                              | Opposite |
| ---------- | ------------------------------------- | -------- |
| `remove`   | Removes something *from* a collection | `add`    |
| `delete`   | Completely erases from existence      | `create` |

```javascript
// remove - from a collection (paired with add)
function removeFilter(filterName, filters) {
  return filters.filter((name) => name !== filterName)
}

// delete - permanent erasure (paired with create)
function deletePost(id) {
  return database.find({ id }).delete()
}
```

**Key insight:** `add` needs a destination, `create` does not. Pair `remove` with `add`, `delete` with `create`.

### `compose`

Creates new data from existing data.

```javascript
function composePageUrl(pageName, pageId) {
  return pageName.toLowerCase() + '-' + pageId
}
```

### `handle`

Handles an action, often used for callback methods.

```javascript
function handleLinkClick() {
  console.log('Clicked a link!')
}

link.addEventListener('click', handleLinkClick)
```

## Prefixes

### Boolean Prefixes

| Prefix   | Usage                                           | Example                                    |
| -------- | ----------------------------------------------- | ------------------------------------------ |
| `is`     | Describes characteristic or state               | `isBlue`, `isPresent`, `isEnabled`         |
| `has`    | Describes possession of value or state          | `hasProducts`, `hasPermission`             |
| `should` | Positive conditional coupled with action        | `shouldUpdateUrl`, `shouldDisplayMessage`  |

```javascript
/* Bad */
const isProductsExist = productsCount > 0
const areProductsPresent = productsCount > 0

/* Good */
const hasProducts = productsCount > 0
```

### Boundary Prefixes

| Prefix       | Usage                           | Example                      |
| ------------ | ------------------------------- | ---------------------------- |
| `min`/`max`  | Minimum or maximum value        | `minPosts`, `maxRetries`     |
| `prev`/`next`| Previous or next state          | `prevPosts`, `nextPosts`     |

```javascript
function renderPosts(posts, minPosts, maxPosts) {
  return posts.slice(0, randomBetween(minPosts, maxPosts))
}

async function getPosts() {
  const prevPosts = this.state.posts
  const latestPosts = await fetch('...')
  const nextPosts = concat(prevPosts, latestPosts)
  this.setState({ posts: nextPosts })
}
```

## Rules to Follow

### 1. Use English Language

```javascript
/* Bad */
const primerNombre = 'Gustavo'
const amigos = ['Kate', 'John']

/* Good */
const firstName = 'Gustavo'
const friends = ['Kate', 'John']
```

### 2. Be Consistent with Naming Convention

Pick one convention (`camelCase`, `PascalCase`, `snake_case`) and stick to it.

```javascript
/* Bad - inconsistent */
const page_count = 5
const shouldUpdate = true

/* Good - consistent */
const pageCount = 5
const shouldUpdate = true
```

### 3. Avoid Contractions

```javascript
/* Bad */
const onItmClk = () => {}

/* Good */
const onItemClick = () => {}
```

### 4. Avoid Context Duplication

```javascript
class MenuItem {
  /* Bad - duplicates context */
  handleMenuItemClick = (event) => { ... }

  /* Good - reads as MenuItem.handleClick() */
  handleClick = (event) => { ... }
}
```

### 5. Reflect Expected Result

```javascript
/* Bad */
const isEnabled = itemCount > 3
return <Button disabled={!isEnabled} />

/* Good */
const isDisabled = itemCount <= 3
return <Button disabled={isDisabled} />
```

### 6. Use Singular/Plural Correctly

```javascript
/* Bad */
const friends = 'Bob'
const friend = ['Bob', 'Tony', 'Tanya']

/* Good */
const friend = 'Bob'
const friends = ['Bob', 'Tony', 'Tanya']
```

## Quick Reference

| Pattern              | Example                          |
| -------------------- | -------------------------------- |
| Get single item      | `getUser`, `getPost`             |
| Get collection       | `getUsers`, `getPosts`           |
| Get nested           | `getUserMessages`                |
| Set value            | `setUser`, `setTheme`            |
| Reset to initial     | `resetForm`, `resetFilters`      |
| Add to collection    | `addItem`, `addFilter`           |
| Remove from collection| `removeItem`, `removeFilter`    |
| Create new entity    | `createUser`, `createPost`       |
| Delete permanently   | `deleteUser`, `deletePost`       |
| Compose/build        | `composeUrl`, `buildQuery`       |
| Handle event         | `handleClick`, `handleSubmit`    |
| Boolean state        | `isActive`, `hasItems`, `shouldRender` |
| Boundaries           | `minCount`, `maxRetries`         |
| State transitions    | `prevState`, `nextState`         |

---

**Source:** [kettanaito/naming-cheatsheet](https://github.com/kettanaito/naming-cheatsheet)
