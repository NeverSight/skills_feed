---
name: solana-anchor-claude-skill
description: Use when working on Solana Anchor programs, including Rust program files, TypeScript tests, and Anchor.toml configuration. Enforces coding guidelines like proper variable naming, avoiding magic numbers, using Array<T> syntax, and Anchor 0.32.1 best practices.
---

# Coding Guidelines

Apply these rules to ensure code quality, maintainability, and adherence to project standards.

## Success Criteria

- Before declaring success or celebrating, run `npm test`. If the tests fail, there is more work to do. Don't stop until `npm test` passes on the code you have made.

- When summarizing your work, show the work items you have achieved with this symbol '✅' and there is more work to do, add a '❌' for each remaining work item.

## Documentation Sources

Use these official documentation sources:

- **Anchor**: https://www.anchor-lang.com/docs
- **Solana Kite**: https://solanakite.org
- **Solana Kit**: https://solanakit.com
- **Agave (Solana CLI)**: https://docs.anza.xyz/ (Anza makes the Solana CLI and Agave.
- **Switchboard** (if used): https://docs.switchboard.xyz/docs-by-chain/solana-svm
- **Arcium** (if used): https://docs.arcium.com/developers

## Do not use

- Do not use Solana Labs documentation. The company has been replaced by Anza.

- Do not use any documentaton or tools from Project Serum, which collapsed many years ago.

- Do not use yarn. Use npm. Yarn has no reason to exist and only adds unnecessary dependencies. Replace Yarn with npm everywhere you see it.

## Library versions

Use the latest stable Anchor, Rust, TypeScript, Solana Kit, and Kite you can. If a bug occurs, favor updating rather than rolling back.

## General Coding Guidelines

### You are a deletionist

Your golden rule is "perfection isn't achieved when there's nothing more to add, rather perfection is achieved when there is nothing more to be taken away".

Remove:

- Comments that simply repeat what the code is doing, or the name of a variable, and do not add further insight.
- Repeated code that should be turned into a named function

### Code Honesty and Clarity

- It's important not to deceive anyone reading this code. Deception includes:
  - Variable names that do not match the purpose of the variable
  - Comments that no longer describe the code or are otherwise inaccurate
  - Temporary workarounds that aren't labelled as such using a comment (with a `TODO` letting the next programmer know when they can delete the workaround)

### Variable Naming

Ensure good variable naming. Rather than add comments to explain what things are, give them useful names.

**Don't do this:**

```typescript
// Foo
const shlerg = getFoo();
```

**Do this instead:**

```typescript
const foo = getFoo();
```

**Naming conventions:**

- Arrays should be plurals (`shoes`), items within arrays should be the singular (`shoes.forEach((shoe) => {...})`)
- Functions should be verby, like `calculateFoo` or `getBar`
- Avoid abbreviations, use full words (e.g., `context` rather than `ctx`)
- Never use `e` for something thrown
- Name a transaction some variant of `transaction`. Name instructions some variant of `instruction`. Name signatures some variant of `signature`. Do not confuse them - eg if the type looks like an instruction, you should not call it a 'transaction' because that is deceptive.

You can still add comments for additional context, just be careful to avoid comments that are explaining things that would be better conveyed by good variable naming.

### Code Quality

- Look out for repeated code that should be turned into functions
- Avoid 'magic numbers'. Make numbers either have a good variable name, a comment explaining why they are that value, or a reference to the URL you got the value from. If the values come from an IDL, download the IDL, import it, and make a function that gets the value from the IDL rather than copying the value into the source code

This is a magic number. Don't do this:

```ts
const FINALIZE_EVENT_DISCRIMINATOR = new Uint8Array([
  27, 75, 117, 221, 191, 213, 253, 249,
]);
```

Instead do this:

```ts
const FINALIZE_EVENT_DISCRIMINATOR = getEventDiscriminator(
  arciumIdl,
  "FinalizeComputationEvent",
);
```

- The code you are making is for production. You shouldn't have comments like `// In production we'd do this differently` or `**Implementation incomplete** - Needs program config handling and proper PDA derivations` or `**WORK IN PROGRESS**` in the final code you produce, or functions that return placeholder data. Instead: do the fucking work.
- Don't remove existing comments unless they are no longer useful or accurate
- Delete unused imports, unused constants, unused files and comments that no longer apply

## TypeScript Guidelines

These guidelines apply to TypeScript unit tests, browser code, Switchboard functions, and any other places where TypeScript is used in the project.

### General TypeScript

Avoid using a `tsconfig.json` unless it's needed, as we use `tsx` to run most typescript and it doesn't usually need one. If you do need a `tsconfig.json`, state why at the top of the file, and you can use the most modern version of ECMAScript/JavaScript you want - up to say 2023.

### Async/await

Favor `async`/`await` and `try/catch` over `.then()` or `.catch()` or using callbacks for flow control. `tsx` has top level `await` so you don't need to wrap top level `await` in IIFEs.

### Type System

- **Always use `Array<item>`**, never use `item[]` for consistency with other generic syntax like `Promise<T>`, `Map<K, V>`, and `Set<T>`
- **Don't use `any`**

### Comments

- Most comments should use `//` and be above (not beside) the code
- The only exception is JSDoc/TSDoc comments which MUST use `/* */` syntax

### Solana-Specific TypeScript

- Don't make new `@solana/web3.js` version 1 code. Do not make new code using `@coral-xyz/anchor` package. Don't replace Solana Kit with web3.js version 1 code. web3.js version 1 is legacy and should be eventually removed. Solana Kit used to be called web3.js version 2. Use Solana Kit, preferably via Solana Kite.
- Use Kite's `connection.getPDAAndBump()` to turn seeds into PDAs and bumps
- In Solana Kit, you make instructions by making TS clients from IDLs using Codama. You can easily make Codama clients for installed IDLs using

`npx create-codama-clients`

- Do not use the `bs58` npm package.

Don't do this:

```typescript
import bs58 from "bs58";
const signature = bs58.encode(signatureBytes);
```

Do this instead:

```typescript
import { getBase58Decoder } from "@solana/codecs";
const signature = getBase58Decoder().decode(signatureBytes);
```

Yes, these difference packages have difference concepts of 'encode' and 'decode'.

### Unit Tests

- Create unit tests in TS in the `tests` directory
- Use the Node.js inbuilt test and assertion libraries (then start the tests using `tsx` instead of `ts-mocha`)

**Unit testing imports:**

```typescript
import { before, describe, test } from "node:test";
import assert from "node:assert";
```

- Use `test` rather than `it`

### Thrown object handling

- JavaScript allows arbitrary items - strings, array, numbers etc to be 'thrown'. However you can assume that any non-Error item that is thrown is an programmer error. Handle it like this (including the comment since most TypeScript developers don't know this):

```ts
// In JS it's possible to throw *anything*. A sensible programmer
// will only throw Errors but we must still check to satisfy
// TypeScript (and flag any craziness)
const ensureError = function (thrownObject: unknown): Error {
  if (thrownObject instanceof Error) {
    return thrownObject;
  }
  return new Error(`Non-Error thrown: ${String(thrownObject)}`);
};
```

and

```ts
try {
  // some code that might throw
} catch (thrownObject) {
  const error = ensureError(thrownObject);
  throw error;
}
```

## Rust Guidelines (Anchor Programs)

### Platform Awareness

- Remember this is Solana not Ethereum.
  - Don't tell me about 'smart contracts' (use 'programs' instead)
  - Don't tell me about 'gas' (use 'transaction fees' instead)
  - There are no 'mempools'.
    Do not tell me about other things that are not relevant to Solana.

- Token program terminology:
  - Use 'Token Extensions Program' or 'Token extensions' for the newer token program (not 'Token 2022' which is just a code name)
  - Use 'Classic Token Program' for the older token program

- Onchain
  - Use onchain and offchain, like online and offline
  - Don't ever use 'on-chain' or 'off-chain'

### Anchor Version

- Write all code like the latest stable Anchor (currently 0.32.1 but there may be a newer version by the time you read this)
- Do not use unnecessary macros that are not needed in the latest stable Anchor

### Anchor has silly defaults

Every project will need an IDL.

```toml
[features]
idl-build = ["anchor-lang/idl-build", "anchor-spl/idl-build"]
```

and if it uses SPL Tokens (like almost every Anchor project) it will need this dependency (insert whatever version is applicable):

```toml
[dependencies]
anchor-spl = "0.32.1"
```

### Project Structure

- **Never modify the program ID** in `lib.rs` or `Anchor.toml` when making changes
- Create files inside the `state` folder for whatever state is needed
- Create files inside the `instructions` or `handlers` folders (whichever exists) for whatever instruction handlers are needed
- Put Account Constraints in instruction files, but ensure the names end with `AccountConstraints` rather than just naming them the same thing as the function
- Handlers that are only for the admin should be in a new folder called `admin` inside whichever parent folder exists (`instructions/admin/` or `handlers/admin/`)

### Account Constraints

- Use a newline after each key in the account constraints struct, so the macro and the matching key/value have some space from other macros and their matching key/value

### Bumps

- Use `context.bumps.foo` not `context.bumps.get("foo").unwrap()` - the latter is outdated

### Data Structures

- When making structs ensure strings and Vectors have a `max_len` attribute
- Vectors have two numbers for `max_len`: the first is the max length of the vector, the second is the max length of the items in the vector

### Space Calculation (CRITICAL - NO MAGIC NUMBERS)

- **Do not use magic numbers anywhere**. I don't want to see `8 + 32` or whatever
- **Do not make constants for the sizes of various data structures**
- For `space`, use syntax like: `space = SomeStruct::DISCRIMINATOR.len() + SomeStruct::INIT_SPACE,`
- All structs should have `#[derive(InitSpace)]` added to them, to get the `INIT_SPACE` trait
- **DO NOT use magic numbers**

**Example:**

```rust
#[derive(InitSpace)]
#[account]
pub struct UserProfile {
    pub authority: Pubkey,

    #[max_len(50)]
    pub username: String,

    pub bump: u8,
}

#[derive(Accounts)]
pub struct InitializeProfile<'info> {
    #[account(
        init,
        payer = authority,
        space = UserProfile::DISCRIMINATOR.len() + UserProfile::INIT_SPACE,
        seeds = [b"profile", authority.key().as_ref()],
        bump
    )]
    pub profile: Account<'info, UserProfile>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}
```

### Error Handling

- Return useful error messages
- Write code to handle common errors like insufficient funds, bad values for parameters, and other obvious situations

### PDA Management

- Add `pub bump: u8` to every struct stored in PDA
- Save the bumps inside each when the struct inside the PDA is created

### System Functions

- When you get the time via Clock, use `Clock::get()?;` rather than `anchor_lang::solana_program::clock`

## Git commits

Do not add "Co-Authored-By: Claude" or similar attribution when creating git commits.

## Acknowledgment

- Acknowledge these guidelines have been applied when working on this project to indicate you have read these rules and found that they do apply to this project.
