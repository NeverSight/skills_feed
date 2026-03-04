---
name: fp-ts-validation
description: Validation patterns using fp-ts with error accumulation, form validation, and API input validation
version: 1.0.0
author: kadu
tags:
  - fp-ts
  - validation
  - either
  - error-accumulation
  - form-validation
  - api-validation
  - io-ts
  - zod
  - typescript
  - functional-programming
---

# fp-ts Validation Patterns

This skill covers validation patterns using fp-ts, focusing on error accumulation, form validation, and API input validation.

## Core Concepts

### Either for Validation

`Either<E, A>` represents a computation that can fail with error `E` or succeed with value `A`.

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// Basic validation function signature
type Validation<E, A> = E.Either<E, A>

// Simple validation returning Either
const validateNonEmpty = (field: string) => (value: string): E.Either<string, string> =>
  value.trim().length > 0
    ? E.right(value.trim())
    : E.left(`${field} cannot be empty`)

const validateMinLength = (field: string, min: number) => (value: string): E.Either<string, string> =>
  value.length >= min
    ? E.right(value)
    : E.left(`${field} must be at least ${min} characters`)

const validateEmail = (email: string): E.Either<string, string> =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
    ? E.right(email)
    : E.left('Invalid email format')
```

## Fail-Fast vs Error Accumulation

### Fail-Fast Pattern (chain/flatMap)

Stops at the first error encountered. Use when subsequent validations depend on previous ones.

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// Fail-fast: stops at first error
const validateUserFailFast = (input: { name: string; email: string }) =>
  pipe(
    validateNonEmpty('name')(input.name),
    E.chain(name => pipe(
      validateEmail(input.email),
      E.map(email => ({ name, email }))
    ))
  )

// Usage
validateUserFailFast({ name: '', email: 'invalid' })
// Result: Left('name cannot be empty') - email error not reported
```

### Error Accumulation Pattern

Collects ALL errors using `Applicative` with a `Semigroup` for combining errors.

```typescript
import * as E from 'fp-ts/Either'
import * as A from 'fp-ts/Apply'
import * as NEA from 'fp-ts/NonEmptyArray'
import { pipe } from 'fp-ts/function'

// Define error type as NonEmptyArray for accumulation
type ValidationErrors = NEA.NonEmptyArray<string>

// Lift validation to use NonEmptyArray for errors
const validateNonEmptyV = (field: string) => (value: string): E.Either<ValidationErrors, string> =>
  value.trim().length > 0
    ? E.right(value.trim())
    : E.left(NEA.of(`${field} cannot be empty`))

const validateEmailV = (email: string): E.Either<ValidationErrors, string> =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
    ? E.right(email)
    : E.left(NEA.of('Invalid email format'))

const validateMinLengthV = (field: string, min: number) => (value: string): E.Either<ValidationErrors, string> =>
  value.length >= min
    ? E.right(value)
    : E.left(NEA.of(`${field} must be at least ${min} characters`))

// Get applicative that accumulates errors
const applicativeValidation = E.getApplicativeValidation(NEA.getSemigroup<string>())
```

## Using sequenceT and sequenceS

### sequenceT - Tuple-based Combining

Combines validations into a tuple, accumulating all errors.

```typescript
import { sequenceT } from 'fp-ts/Apply'

// Combine multiple validations with error accumulation
const validateUserWithSequenceT = (input: { name: string; email: string; age: string }) => {
  const validateAge = (age: string): E.Either<ValidationErrors, number> => {
    const parsed = parseInt(age, 10)
    return isNaN(parsed) || parsed < 0 || parsed > 150
      ? E.left(NEA.of('Age must be a valid number between 0 and 150'))
      : E.right(parsed)
  }

  return pipe(
    sequenceT(applicativeValidation)(
      validateNonEmptyV('name')(input.name),
      validateEmailV(input.email),
      validateAge(input.age)
    ),
    E.map(([name, email, age]) => ({ name, email, age }))
  )
}

// Usage - collects ALL errors
validateUserWithSequenceT({ name: '', email: 'invalid', age: '-5' })
// Result: Left(['name cannot be empty', 'Invalid email format', 'Age must be a valid number between 0 and 150'])
```

### sequenceS - Struct-based Combining

Combines validations into a struct/object, preserving field names.

```typescript
import { sequenceS } from 'fp-ts/Apply'

interface UserInput {
  name: string
  email: string
  password: string
}

interface ValidatedUser {
  name: string
  email: string
  password: string
}

const validateUserWithSequenceS = (input: UserInput): E.Either<ValidationErrors, ValidatedUser> =>
  sequenceS(applicativeValidation)({
    name: validateNonEmptyV('name')(input.name),
    email: validateEmailV(input.email),
    password: pipe(
      validateNonEmptyV('password')(input.password),
      E.chain(p => validateMinLengthV('password', 8)(p))
    )
  })

// Usage
validateUserWithSequenceS({ name: 'John', email: 'invalid', password: '123' })
// Result: Left(['Invalid email format', 'password must be at least 8 characters'])
```

## Form Validation with Error Accumulation

### Complete Form Validation Example

```typescript
import * as E from 'fp-ts/Either'
import * as A from 'fp-ts/Apply'
import * as NEA from 'fp-ts/NonEmptyArray'
import { sequenceS } from 'fp-ts/Apply'
import { pipe } from 'fp-ts/function'

// Custom error type with field information
interface FieldError {
  field: string
  message: string
}

type FormErrors = NEA.NonEmptyArray<FieldError>

const fieldError = (field: string, message: string): FormErrors =>
  NEA.of({ field, message })

const formApplicative = E.getApplicativeValidation(NEA.getSemigroup<FieldError>())

// Reusable validators
const required = (field: string) => (value: string): E.Either<FormErrors, string> =>
  value.trim().length > 0
    ? E.right(value.trim())
    : E.left(fieldError(field, 'This field is required'))

const minLength = (field: string, min: number) => (value: string): E.Either<FormErrors, string> =>
  value.length >= min
    ? E.right(value)
    : E.left(fieldError(field, `Must be at least ${min} characters`))

const maxLength = (field: string, max: number) => (value: string): E.Either<FormErrors, string> =>
  value.length <= max
    ? E.right(value)
    : E.left(fieldError(field, `Must be at most ${max} characters`))

const pattern = (field: string, regex: RegExp, message: string) => (value: string): E.Either<FormErrors, string> =>
  regex.test(value)
    ? E.right(value)
    : E.left(fieldError(field, message))

const email = (field: string) => pattern(field, /^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'Invalid email format')

const numeric = (field: string) => (value: string): E.Either<FormErrors, number> => {
  const num = parseFloat(value)
  return isNaN(num)
    ? E.left(fieldError(field, 'Must be a valid number'))
    : E.right(num)
}

const inRange = (field: string, min: number, max: number) => (value: number): E.Either<FormErrors, number> =>
  value >= min && value <= max
    ? E.right(value)
    : E.left(fieldError(field, `Must be between ${min} and ${max}`))

// Compose validators for a single field (fail-fast within field)
const composeValidators = <A, B>(
  v1: (a: A) => E.Either<FormErrors, B>,
  ...validators: Array<(b: B) => E.Either<FormErrors, B>>
) => (value: A): E.Either<FormErrors, B> =>
  validators.reduce(
    (acc, validator) => pipe(acc, E.chain(validator)),
    v1(value)
  )

// Registration form validation
interface RegistrationInput {
  username: string
  email: string
  password: string
  confirmPassword: string
  age: string
}

interface ValidatedRegistration {
  username: string
  email: string
  password: string
  age: number
}

const validateRegistration = (input: RegistrationInput): E.Either<FormErrors, ValidatedRegistration> => {
  const validateUsername = composeValidators(
    required('username'),
    minLength('username', 3),
    maxLength('username', 20),
    pattern('username', /^[a-zA-Z0-9_]+$/, 'Only letters, numbers, and underscores allowed')
  )

  const validateEmail = composeValidators(
    required('email'),
    email('email')
  )

  const validatePassword = composeValidators(
    required('password'),
    minLength('password', 8),
    pattern('password', /[A-Z]/, 'Must contain at least one uppercase letter'),
    pattern('password', /[a-z]/, 'Must contain at least one lowercase letter'),
    pattern('password', /[0-9]/, 'Must contain at least one number')
  )

  const validateAge = composeValidators(
    required('age'),
    numeric('age'),
    inRange('age', 13, 120)
  )

  // Cross-field validation
  const validatePasswordMatch = (): E.Either<FormErrors, void> =>
    input.password === input.confirmPassword
      ? E.right(undefined)
      : E.left(fieldError('confirmPassword', 'Passwords do not match'))

  return pipe(
    sequenceS(formApplicative)({
      username: validateUsername(input.username),
      email: validateEmail(input.email),
      password: validatePassword(input.password),
      age: validateAge(input.age),
      _passwordMatch: validatePasswordMatch()
    }),
    E.map(({ username, email, password, age }) => ({
      username,
      email,
      password,
      age
    }))
  )
}

// Usage
const result = validateRegistration({
  username: 'ab',
  email: 'invalid',
  password: 'weak',
  confirmPassword: 'different',
  age: '10'
})

// Result: Left([
//   { field: 'username', message: 'Must be at least 3 characters' },
//   { field: 'email', message: 'Invalid email format' },
//   { field: 'password', message: 'Must be at least 8 characters' },
//   { field: 'age', message: 'Must be between 13 and 120' },
//   { field: 'confirmPassword', message: 'Passwords do not match' }
// ])

// Helper to convert errors to a field-indexed object
const errorsToRecord = (errors: FormErrors): Record<string, string[]> =>
  errors.reduce((acc, err) => ({
    ...acc,
    [err.field]: [...(acc[err.field] || []), err.message]
  }), {} as Record<string, string[]>)

// For React forms
const getFieldErrors = (result: E.Either<FormErrors, unknown>) => (field: string): string[] =>
  pipe(
    result,
    E.fold(
      errors => errors.filter(e => e.field === field).map(e => e.message),
      () => []
    )
  )
```

## API Input Validation

### Request Body Validation

```typescript
import * as E from 'fp-ts/Either'
import * as NEA from 'fp-ts/NonEmptyArray'
import { sequenceS } from 'fp-ts/Apply'
import { pipe } from 'fp-ts/function'

// API error types
interface ApiValidationError {
  code: string
  field: string
  message: string
}

type ApiErrors = NEA.NonEmptyArray<ApiValidationError>

const apiError = (code: string, field: string, message: string): ApiErrors =>
  NEA.of({ code, field, message })

const apiApplicative = E.getApplicativeValidation(NEA.getSemigroup<ApiValidationError>())

// Common API validators
const requiredField = <T>(field: string) => (value: T | null | undefined): E.Either<ApiErrors, T> =>
  value != null
    ? E.right(value)
    : E.left(apiError('REQUIRED', field, `${field} is required`))

const stringField = (field: string) => (value: unknown): E.Either<ApiErrors, string> =>
  typeof value === 'string'
    ? E.right(value)
    : E.left(apiError('INVALID_TYPE', field, `${field} must be a string`))

const numberField = (field: string) => (value: unknown): E.Either<ApiErrors, number> =>
  typeof value === 'number' && !isNaN(value)
    ? E.right(value)
    : E.left(apiError('INVALID_TYPE', field, `${field} must be a number`))

const arrayField = <T>(field: string) => (value: unknown): E.Either<ApiErrors, T[]> =>
  Array.isArray(value)
    ? E.right(value as T[])
    : E.left(apiError('INVALID_TYPE', field, `${field} must be an array`))

const uuidField = (field: string) => (value: string): E.Either<ApiErrors, string> =>
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value)
    ? E.right(value)
    : E.left(apiError('INVALID_FORMAT', field, `${field} must be a valid UUID`))

const enumField = <T extends string>(field: string, allowed: readonly T[]) => (value: string): E.Either<ApiErrors, T> =>
  allowed.includes(value as T)
    ? E.right(value as T)
    : E.left(apiError('INVALID_VALUE', field, `${field} must be one of: ${allowed.join(', ')}`))

// Create Order API validation
interface CreateOrderRequest {
  customerId: string
  items: Array<{
    productId: string
    quantity: number
  }>
  shippingAddress: {
    street: string
    city: string
    postalCode: string
    country: string
  }
  paymentMethod: string
}

interface ValidatedOrder {
  customerId: string
  items: Array<{ productId: string; quantity: number }>
  shippingAddress: {
    street: string
    city: string
    postalCode: string
    country: string
  }
  paymentMethod: 'credit_card' | 'paypal' | 'bank_transfer'
}

const validateOrderItem = (item: unknown, index: number): E.Either<ApiErrors, { productId: string; quantity: number }> => {
  if (typeof item !== 'object' || item === null) {
    return E.left(apiError('INVALID_TYPE', `items[${index}]`, 'Item must be an object'))
  }

  const obj = item as Record<string, unknown>

  return sequenceS(apiApplicative)({
    productId: pipe(
      requiredField<unknown>(`items[${index}].productId`)(obj.productId),
      E.chain(stringField(`items[${index}].productId`)),
      E.chain(uuidField(`items[${index}].productId`))
    ),
    quantity: pipe(
      requiredField<unknown>(`items[${index}].quantity`)(obj.quantity),
      E.chain(numberField(`items[${index}].quantity`)),
      E.chain(n => n > 0
        ? E.right(n)
        : E.left(apiError('INVALID_VALUE', `items[${index}].quantity`, 'Quantity must be positive'))
      )
    )
  })
}

const validateAddress = (address: unknown): E.Either<ApiErrors, ValidatedOrder['shippingAddress']> => {
  if (typeof address !== 'object' || address === null) {
    return E.left(apiError('INVALID_TYPE', 'shippingAddress', 'Shipping address must be an object'))
  }

  const obj = address as Record<string, unknown>

  return sequenceS(apiApplicative)({
    street: pipe(
      requiredField<unknown>('shippingAddress.street')(obj.street),
      E.chain(stringField('shippingAddress.street'))
    ),
    city: pipe(
      requiredField<unknown>('shippingAddress.city')(obj.city),
      E.chain(stringField('shippingAddress.city'))
    ),
    postalCode: pipe(
      requiredField<unknown>('shippingAddress.postalCode')(obj.postalCode),
      E.chain(stringField('shippingAddress.postalCode'))
    ),
    country: pipe(
      requiredField<unknown>('shippingAddress.country')(obj.country),
      E.chain(stringField('shippingAddress.country'))
    )
  })
}

const validateCreateOrder = (body: unknown): E.Either<ApiErrors, ValidatedOrder> => {
  if (typeof body !== 'object' || body === null) {
    return E.left(apiError('INVALID_TYPE', 'body', 'Request body must be an object'))
  }

  const obj = body as Record<string, unknown>

  // Validate items array with accumulation
  const validateItems = (items: unknown[]): E.Either<ApiErrors, Array<{ productId: string; quantity: number }>> => {
    if (items.length === 0) {
      return E.left(apiError('INVALID_VALUE', 'items', 'Order must contain at least one item'))
    }

    const validatedItems = items.map((item, index) => validateOrderItem(item, index))

    // Accumulate all item errors
    return validatedItems.reduce(
      (acc, itemResult) => pipe(
        sequenceS(apiApplicative)({ acc, item: itemResult }),
        E.map(({ acc, item }) => [...acc, item])
      ),
      E.right([]) as E.Either<ApiErrors, Array<{ productId: string; quantity: number }>>
    )
  }

  return pipe(
    sequenceS(apiApplicative)({
      customerId: pipe(
        requiredField<unknown>('customerId')(obj.customerId),
        E.chain(stringField('customerId')),
        E.chain(uuidField('customerId'))
      ),
      items: pipe(
        requiredField<unknown>('items')(obj.items),
        E.chain(arrayField<unknown>('items')),
        E.chain(validateItems)
      ),
      shippingAddress: pipe(
        requiredField<unknown>('shippingAddress')(obj.shippingAddress),
        E.chain(validateAddress)
      ),
      paymentMethod: pipe(
        requiredField<unknown>('paymentMethod')(obj.paymentMethod),
        E.chain(stringField('paymentMethod')),
        E.chain(enumField('paymentMethod', ['credit_card', 'paypal', 'bank_transfer'] as const))
      )
    })
  )
}

// Express middleware example
const validateRequest = <T>(validator: (body: unknown) => E.Either<ApiErrors, T>) =>
  (req: { body: unknown }, res: { status: (n: number) => { json: (body: unknown) => void } }, next: () => void) => {
    pipe(
      validator(req.body),
      E.fold(
        errors => res.status(400).json({
          error: 'Validation failed',
          details: errors
        }),
        validated => {
          (req as any).validatedBody = validated
          next()
        }
      )
    )
  }
```

## Custom Error Types

### Branded Error Types

```typescript
import * as E from 'fp-ts/Either'
import * as NEA from 'fp-ts/NonEmptyArray'

// Domain-specific error types
type ValidationErrorCode =
  | 'REQUIRED'
  | 'MIN_LENGTH'
  | 'MAX_LENGTH'
  | 'PATTERN'
  | 'RANGE'
  | 'INVALID_TYPE'
  | 'BUSINESS_RULE'

interface DomainValidationError {
  readonly _tag: 'ValidationError'
  readonly code: ValidationErrorCode
  readonly field: string
  readonly message: string
  readonly metadata?: Record<string, unknown>
}

const validationError = (
  code: ValidationErrorCode,
  field: string,
  message: string,
  metadata?: Record<string, unknown>
): DomainValidationError => ({
  _tag: 'ValidationError',
  code,
  field,
  message,
  metadata
})

type DomainErrors = NEA.NonEmptyArray<DomainValidationError>

// Helper to create single error
const singleError = (
  code: ValidationErrorCode,
  field: string,
  message: string,
  metadata?: Record<string, unknown>
): DomainErrors => NEA.of(validationError(code, field, message, metadata))

// Validators with rich error metadata
const minLengthWithMeta = (field: string, min: number) => (value: string): E.Either<DomainErrors, string> =>
  value.length >= min
    ? E.right(value)
    : E.left(singleError('MIN_LENGTH', field, `Must be at least ${min} characters`, {
        actual: value.length,
        required: min
      }))
```

## Integration with io-ts

### Basic io-ts Integration

```typescript
import * as t from 'io-ts'
import * as E from 'fp-ts/Either'
import * as NEA from 'fp-ts/NonEmptyArray'
import { pipe } from 'fp-ts/function'
import { PathReporter } from 'io-ts/PathReporter'

// Define codec with io-ts
const UserCodec = t.type({
  name: t.string,
  email: t.string,
  age: t.number,
  role: t.union([t.literal('admin'), t.literal('user'), t.literal('guest')])
})

type User = t.TypeOf<typeof UserCodec>

// Convert io-ts errors to our error format
interface IoTsValidationError {
  field: string
  message: string
}

const fromIoTsErrors = (errors: t.Errors): NEA.NonEmptyArray<IoTsValidationError> => {
  const mapped = errors.map(error => ({
    field: error.context.map(c => c.key).filter(k => k !== '').join('.') || 'root',
    message: `Invalid value ${JSON.stringify(error.value)} supplied`
  }))
  return mapped as NEA.NonEmptyArray<IoTsValidationError>
}

// Decode with accumulated errors
const decodeUser = (input: unknown): E.Either<NEA.NonEmptyArray<IoTsValidationError>, User> =>
  pipe(
    UserCodec.decode(input),
    E.mapLeft(fromIoTsErrors)
  )

// Combine io-ts decoding with custom validation
const validateAndDecodeUser = (input: unknown): E.Either<NEA.NonEmptyArray<IoTsValidationError>, User> =>
  pipe(
    decodeUser(input),
    E.chain(user => {
      const errors: IoTsValidationError[] = []

      if (user.name.length < 2) {
        errors.push({ field: 'name', message: 'Name must be at least 2 characters' })
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(user.email)) {
        errors.push({ field: 'email', message: 'Invalid email format' })
      }
      if (user.age < 0 || user.age > 150) {
        errors.push({ field: 'age', message: 'Age must be between 0 and 150' })
      }

      return errors.length > 0
        ? E.left(errors as NEA.NonEmptyArray<IoTsValidationError>)
        : E.right(user)
    })
  )
```

### Custom io-ts Codecs with Validation

```typescript
import * as t from 'io-ts'
import * as E from 'fp-ts/Either'

// Custom branded types with validation
interface EmailBrand {
  readonly Email: unique symbol
}
type Email = t.Branded<string, EmailBrand>

const Email = t.brand(
  t.string,
  (s): s is Email => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s),
  'Email'
)

interface NonEmptyStringBrand {
  readonly NonEmptyString: unique symbol
}
type NonEmptyString = t.Branded<string, NonEmptyStringBrand>

const NonEmptyString = t.brand(
  t.string,
  (s): s is NonEmptyString => s.trim().length > 0,
  'NonEmptyString'
)

interface PositiveIntBrand {
  readonly PositiveInt: unique symbol
}
type PositiveInt = t.Branded<number, PositiveIntBrand>

const PositiveInt = t.brand(
  t.number,
  (n): n is PositiveInt => Number.isInteger(n) && n > 0,
  'PositiveInt'
)

// Codec using branded types
const ValidatedUserCodec = t.type({
  name: NonEmptyString,
  email: Email,
  age: PositiveInt
})

type ValidatedUser = t.TypeOf<typeof ValidatedUserCodec>
```

## Integration with Zod

### Zod with fp-ts Either

```typescript
import { z } from 'zod'
import * as E from 'fp-ts/Either'
import * as NEA from 'fp-ts/NonEmptyArray'
import { pipe } from 'fp-ts/function'

// Define Zod schema
const UserSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email format'),
  age: z.number().int().min(0).max(150),
  role: z.enum(['admin', 'user', 'guest'])
})

type ZodUser = z.infer<typeof UserSchema>

// Convert Zod errors to our format
interface ZodValidationError {
  field: string
  message: string
}

const fromZodError = (error: z.ZodError): NEA.NonEmptyArray<ZodValidationError> => {
  const errors = error.errors.map(err => ({
    field: err.path.join('.') || 'root',
    message: err.message
  }))
  return errors as NEA.NonEmptyArray<ZodValidationError>
}

// Parse with Either
const parseUser = (input: unknown): E.Either<NEA.NonEmptyArray<ZodValidationError>, ZodUser> => {
  const result = UserSchema.safeParse(input)
  return result.success
    ? E.right(result.data)
    : E.left(fromZodError(result.error))
}

// Combine Zod with additional fp-ts validation
const validateUser = (input: unknown): E.Either<NEA.NonEmptyArray<ZodValidationError>, ZodUser> =>
  pipe(
    parseUser(input),
    E.chain(user => {
      // Additional business logic validation
      const errors: ZodValidationError[] = []

      if (user.role === 'admin' && user.age < 18) {
        errors.push({ field: 'role', message: 'Admins must be at least 18 years old' })
      }

      return errors.length > 0
        ? E.left(errors as NEA.NonEmptyArray<ZodValidationError>)
        : E.right(user)
    })
  )
```

### Zod Refinements with Error Accumulation

```typescript
import { z } from 'zod'
import * as E from 'fp-ts/Either'
import * as NEA from 'fp-ts/NonEmptyArray'
import { sequenceS } from 'fp-ts/Apply'

// Separate schemas for independent validation
const nameSchema = z.string().min(2, 'Name must be at least 2 characters')
const emailSchema = z.string().email('Invalid email format')
const ageSchema = z.number().int().min(0, 'Age must be non-negative').max(150, 'Age must be at most 150')

interface ValidationError {
  field: string
  message: string
}

type ValidationErrors = NEA.NonEmptyArray<ValidationError>

const parseWithField = <T>(schema: z.ZodType<T>, field: string) => (value: unknown): E.Either<ValidationErrors, T> => {
  const result = schema.safeParse(value)
  return result.success
    ? E.right(result.data)
    : E.left(NEA.of({ field, message: result.error.errors[0]?.message || 'Validation failed' }))
}

const applicativeValidation = E.getApplicativeValidation(NEA.getSemigroup<ValidationError>())

// Validate with error accumulation
const validateUserAccumulated = (input: { name: unknown; email: unknown; age: unknown }) =>
  sequenceS(applicativeValidation)({
    name: parseWithField(nameSchema, 'name')(input.name),
    email: parseWithField(emailSchema, 'email')(input.email),
    age: parseWithField(ageSchema, 'age')(input.age)
  })

// Usage - all errors collected
validateUserAccumulated({ name: 'A', email: 'invalid', age: -5 })
// Result: Left([
//   { field: 'name', message: 'Name must be at least 2 characters' },
//   { field: 'email', message: 'Invalid email format' },
//   { field: 'age', message: 'Age must be non-negative' }
// ])
```

## Best Practices

### 1. Choose the Right Pattern

```typescript
// Use fail-fast (chain) when:
// - Validations depend on each other
// - You want to short-circuit on first failure
// - Performance is critical

// Use error accumulation (sequenceT/sequenceS) when:
// - Validations are independent
// - You want to show all errors to users
// - Building form validation
```

### 2. Structure Error Types

```typescript
// Good: Structured errors with codes
interface StructuredError {
  code: string      // Machine-readable
  field: string     // Which field failed
  message: string   // Human-readable
  metadata?: unknown // Additional context
}

// Bad: Just strings
type BadError = string
```

### 3. Separate Schema Validation from Business Rules

```typescript
// Schema validation (structure/types) - use io-ts or Zod
const UserSchema = z.object({
  email: z.string().email(),
  age: z.number()
})

// Business rules - use fp-ts validation
const validateBusinessRules = (user: User) =>
  sequenceS(applicativeValidation)({
    emailDomain: validateCorporateEmail(user.email),
    ageRestriction: validateAgeForRole(user.age, user.role)
  })

// Combine both
const validateUser = (input: unknown) =>
  pipe(
    parseSchema(input),
    E.chain(validateBusinessRules)
  )
```

### 4. Create Reusable Validator Combinators

```typescript
// Combinator that runs multiple validators on same value
const all = <E, A>(...validators: Array<(a: A) => E.Either<NEA.NonEmptyArray<E>, A>>) =>
  (value: A): E.Either<NEA.NonEmptyArray<E>, A> =>
    pipe(
      validators.map(v => v(value)),
      results => results.reduce(
        (acc, result) => pipe(
          sequenceS(E.getApplicativeValidation(NEA.getSemigroup<E>()))({ acc, result }),
          E.map(() => value)
        ),
        E.right(value) as E.Either<NEA.NonEmptyArray<E>, A>
      )
    )

// Usage
const validatePassword = all(
  minLength('password', 8),
  hasUppercase('password'),
  hasLowercase('password'),
  hasNumber('password')
)
```
