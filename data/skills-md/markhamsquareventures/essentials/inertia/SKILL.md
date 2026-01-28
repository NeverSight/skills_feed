---
name: inertia
description: How to work effectively with Inertia, always use when developing frontend features
---

# Inertia

## Instructions

## Inertia + React

- Use `router.visit()` or `<Link>` for navigation instead of traditional links.

<code-snippet name="Inertia Client Navigation" lang="react">

import { Link } from '@inertiajs/react'

<Link href="/">Home</Link>

</code-snippet>

## Inertia + React Forms

<code-snippet name="`<Form>` Component Example" lang="react">

import { Form } from '@inertiajs/react'

export default () => (

<Form action="/users" method="post">
{({
errors,
hasErrors,
processing,
wasSuccessful,
recentlySuccessful,
clearErrors,
resetAndClearErrors,
defaults
}) => (
<>
<input type="text" name="name" />

        {errors.name && <div>{errors.name}</div>}

        <button type="submit" disabled={processing}>
            {processing ? 'Creating...' : 'Create User'}
        </button>

        {wasSuccessful && <div>User created successfully!</div>}
        </>
    )}
    </Form>

)

</code-snippet>
